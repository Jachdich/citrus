import os
import math
import inspect
from pprint import pprint
from parser import *

def can_be_coerced(from_, to):
    # same type always able to convert
    if from_ == to: return True
    
    if from_ in INT_TYPES and to in INT_TYPES:
        if from_[0] != to[0]:
            return False # can't coerce signed to unsigned or vice versa
        fbits = int(from_[1:])
        tbits = int(to[1:])
        # can coerce if dest bits >= source bits
        return tbits >= fbits
    
    # TODO support other datatypes
    return False

class FuncSig:
    def __init__(self, name, args, ret_ty):
        self.name = name
        self.args = args
        self.ret_ty = ret_ty

class LocalVar:
    def __init__(self, name, ty, loc):
        self.name = name
        self.ty = ty
        self.loc = loc

class CG:
    def __init__(self):
        self.code = []

    def funccall(self, ast, reg_hint=None):
        funcname = ast[0]
        func_sig = self.get_global(funcname.val)
        if func_sig is None:
            raise SyntaxError(f"Unknown function '{funcname}'")
            
        num_args = len(ast) - 1
        if num_args != len(func_sig.args):
            raise SyntaxError(f"Function '{funcname}' expects {len(func_sig.args)} args but {num_args} were given")
        # TODO arg types
        saved_regs = []

        arg_regs = ARGS_REGS[:num_args]
        
        # try to get the args in the right registers
        to_move = []
        to_free = [] # free these regs later
        for i, arg in enumerate(ast[1:]):
            actual_reg, ty = self.expr(arg, reg_hint=RegHint(wanted=arg_regs[i]))
            # if they couldnæ then move them later
            if actual_reg != arg_regs[i]:
                to_move.append((actual_reg, arg_regs[i]))
            to_free.append(actual_reg)
        
        # save caller saved regs
        for reg in CALLER_SAVED_REGS:
            if self.is_reg_used(reg) and not reg in to_free:
                saved_regs.append(reg)
                self.code_append(("pushq", reg))
        
        # move args that weren't in the right regs            
        for from_, to in to_move:
            self.code_append(("movq", from_, to))
        
        # free args
        for reg in to_free:
            self.regfree(reg)

        self.code_append(("call", funcname.val))

        # figure out what register to return        
        if reg_hint != None and not self.is_reg_used(reg_hint):
            # use the hint
            ret_reg = self.regalloc(RegHint(wanted=reg_hint))
        else:
            # try to just allocate rax because it's already in rax
            ret_reg = self.regalloc(RegHint(wanted="%rax"))
            if ret_reg is None:
                # this is a bit annoying, rax is already allocated
                ret_reg = self.regalloc()
        
        # only move ret value if it's not rax
        if ret_reg != "%rax":
            self.code_append(("movq", "%rax", ret_reg))
        
        # restore saved regs
        for reg in saved_regs:
            self.code_append(("popq", reg))
            
        return (ret_reg, func_sig.ret_ty)
    
    def binexpr(self, ast, reg_hint=None):
        op = ast.op
        
        lhs = self.expr(ast.operands[0], lhs_hint)
        for i, rhs_expr in enumerate(ast.operands[1:]):
            rhs = self.expr(rhs_expr, hint)
        
            int_tys = ["u64", "u32", "u16", "u8", "i64", "i32", "i16", "i8"]
            if rty in ["f64", "f32"] or lty in ["f64", "f32"]:
                raise SyntaxError("Floats not supported yet")
                if rty == "f64" or lty == "f64":
                    ty = "f64"
                else:
                    ty = "f32"
            elif rty in int_tys and lty in int_tys:
                lsigned = lty[0] == "i"
                rsigned = rty[0] == "i"
                lbits = int(lty[1:])
                rbits = int(rty[1:])
                if lsigned or rsigned:
                    outsigned = "i"
                    signed = True
                else:
                    outsigned = "u"
                    signed = False
            
                outbits = max(lbits, rbits)
                ty = outsigned + str(outbits)
            else:
                raise SyntaxError(f"Incompatible types for operator '{op}': type '{lty}' and type '{rty}'")
        
            if op == "/" or op == "%":
                rhs = self.int_div(lhs, rhs, signed, op)        
            else:
                if op == "+":
                    instr = "addq"
                elif op == "*":
                    instr = ("i" if signed else "") + "mulq"
                elif op == "-":
                    instr = "subq"
                self.code_append((instr, lhs, rhs))
                
            self.regfree(lhs)
            lhs = rhs
            lty = rty

        return rhs, ty
        
    def int_literal(self, ast):
        reg = self.regalloc(reg_hint)
        self.code_append(("movq", "$" + str(ast.val), reg))
        return reg, "i32" # TODO figure this out

    def ident(self, ast, reg_hint=None):
        var = self.get_local(ast.val)
        if var is None:
            raise SyntaxError("Undefined symbol '" + ast.val + "'")
        
        reg = self.regalloc(reg_hint)
        self.code_append(("movq", f"-{var.loc}(%rbp)", reg))
        return reg, var.ty
    
    def var_assign(self, ast, reg_hint=None):
        var = self.get_local(ast.lval)
        if var is None:
            raise SyntaxError(f"Undefined variable '{ast.lval}'")
        rval, ret_ty = self.expr(ast.rval, reg_hint=reg_hint)
        if not can_be_coerced(ret_ty, var.ty):
            raise SyntaxError(f"Attempt to assign expression of type '{ret_ty}' to variable '{ast.lval}' (type '{var.ty}')")
        
        self.code_append(("movq", rval, f"-{var.loc}(%rbp)"))
        return rval, var.ty
    
    def ifsmt(self, ast):
        ret_reg, ret_ty = self.expr(ast.condition)
        self.code_append(("test", ret_reg, ret_reg))
        end_label   = self.gen_label()
        if ast.else_body is not None:
            false_label = self.gen_label()
            self.code_append(("jne", false_label))
        else:
            self.code_append(("jne", end_label))
        
        for smt in ast.body:
            self.smt(smt)
            
        if ast.else_body is not None:
            self.code_append(("jp", end_label))
            self.code_append((false_label + ":",))
            for smt in ast.else_body:
                self.smt(smt)
        
        self.code_append((end_label + ":",))
    
    def expr(self, ast):
        if type(ast) == IntLit:
            return self.int_literal(ast)
        # elif type(ast) == BinOp:
        #     return self.binexpr(ast, reg_hint=reg_hint)
        # elif type(ast) == FuncCall:
        #     return self.funccall(ast, reg_hint=reg_hint)
        # elif type(ast) == Ident:
        #     return self.ident(ast, reg_hint=reg_hint)
        # elif type(ast) == VarAssign:
        #     return self.var_assign(ast, reg_hint=reg_hint)
        else:
            print("Not implemented: expression type " + ast.get_name())
            exit(1)

    def smt(self, ast):
        if type(ast) == VarDef:
            if ast.val != None:
                # convert defs into assigns cos that's how we roll
                ast = VarAssign([Ident(ast.name), ast.val])
                retval, rettype = self.expr(ast)
                self.regfree(retval)
            else:
                # nothing to assing; return
                return
        elif type(ast) == IfSmt:
            self.ifsmt(ast)
        else:
            retval, rettype = self.expr(ast)
            self.regfree(retval)
    
    def gen_fn_sig(self, ast):
        ret_ty = ast.ret_ty
        if ret_ty is None:
            ret_ty = "void"
        
        check_valid_type(ret_ty)
        args = [a[1] for a in ast.args] # just types
        sig = FuncSig(ast.name, args, ret_ty)
        return sig
   
    def funcdef(self, ast):
        sig = self.gen_fn_sig(ast)
        self.globals.append(sig)
        
        if ast.forward_decl:
            return
        
        ret_ty = ast.ret_ty
        if ret_ty is None:
            ret_ty = "void"

        # size of locals (first calculate size of args)
        locsize = sum([sizeof(a[1]) for a in ast.args])
        
        self.locals.append([])
        
        locdefs = filter(lambda n: type(n) == VarDef, ast.body)
        
        loc = 0
        idx = 0
        # add locals to symtable
        for name, ty in ast.args:
            check_valid_type(ty)
            self.locals[-1].append(LocalVar(name, ty, loc))
            self.code_append(("movq", arg_regs[idx], f"-{loc}(%rbp)"))
            loc += sizeof(ty)
            idx += 1

        for d in locdefs:
            check_valid_type(d.ty)
            self.locals[-1].append(LocalVar(d.name, d.ty, loc))
            locsize += sizeof(d.ty)
            loc += sizeof(d.ty)
        
        # move locals to their variable positions
        self.code_append((ast.name + ":",))
        if locsize > 0:
            self.code_append(("pushq", "%rbp"))
            self.code_append(("movq",  "%rsp",       "%rbp"))
            self.code_append(("subq" , "$" + str(locsize), "%rsp"))
        
        arg_regs = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"]
        
        for smt in ast.body[:-1]:
            self.smt(smt)
        
        if ast.body.get_name() == "compoundexpr":
            ret_val, actual_ret_ty = self.expr(ast.body[-1])
        else:
            self.smt(ast.body[-1])
            ret_val = None
            actual_ret_ty = "void"
            
        if not can_be_coerced(actual_ret_ty, ret_ty):
            raise SyntaxError(f"Function '{str(ast[0])}' should return type '{ret_ty}', but last expression is of type '{actual_ret_ty}'")
        
        if ret_val is not None and ret_val != "%rax":
            self.code_append(("movq", ret_val, "%rax"))
            self.regfree(ret_val)
        elif ret_val == "%rax":
            self.regfree(ret_val)
        
        if locsize > 0:
            self.code_append(("addq", "$" + str(locsize), "%rsp"))
            self.code_append(("popq", "%rbp"))
        self.code_append(("ret",))
        
        self.locals.pop()
        
    def importsmt(self, smt, already_imported):
        if not os.path.isfile(smt.fname):
            raise ImportError(f"{smt.fname}: No such file or directlry")
        with open(smt.fname, "r") as f:
            source = f.read()
            
        already_imported.append(smt.fname)
        
        ast = parse(source)
        for smt in ast:
            if smt.get_name() == "funcdef":
                self.globals.append(self.gen_fn_sig(smt))
            elif smt.get_name() == "import" and smt.fname not in already_imported:
                # recursively import anything we haven't already
                self.importsmt(smt, already_imported)
        

    def gen(self, ast, fname, debug=False):
        pprint(ast.as_list())
        for smt in ast:
            if smt.get_name() == "funcdef":
                self.funcdef(smt)
            elif smt.get_name() == "import":
                self.importsmt(smt, [fname])
            else:
                print(f"Invalid syntax: Unexpected token '{smt}'")
                exit(1)
        
        return self.format_code(debug)
        
    def format_code(self, debug=False):
        fmt_code = ".text\n" + "\n".join([".globl " + sig.name + "\n.type " + sig.name + ", @function" for sig in self.globals])
        fmt_code += "\n"
        skip_next = False
        for i, line in enumerate(self.code):
            if type(line) == str and debug:
                # debug statement in the code
                fmt_code += "    # " + line + "\n"
                continue
            if skip_next:
                skip_next = False
                continue

            dbg = line[-1]
            instr = line[:-1]
            
            # find next instruction (could be comments in the way)
            offset = 1
            ninstr = None
            while offset + i < len(self.code) and type(self.code[i + offset]) == str:
                offset += 1
                
            # check if mov is redundant (e.g. rax -> rcx then rcx -> rdx)
            if ninstr is not None and \
               instr[0][:3] == "mov" and \
               ninstr[0][:3] == "mov" and \
               instr[2] == ninstr[1]:
                # redundant mov
                skip_next = True
                instr = list(instr)
                instr[2] = ninstr[2]
            
            # labels are unindented
            if not (len(instr) == 1 and instr[0].endswith(":")):
                curr_line = "    "
            else:
                curr_line = ""
            
            for i, ipart in enumerate(instr):
                bit_of_line = ipart
                if i < len(instr) - 1 and i != 0:
                    bit_of_line += ","
                curr_line += bit_of_line + " " * (12 - len(bit_of_line))
            
            if debug:
                curr_line += " " * (48 - len(curr_line))
                curr_line += "# " + dbg
            fmt_code += curr_line + "\n"
        return fmt_code

