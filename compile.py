import os
import math
import inspect
from pprint import pprint
from parser import *

def regalloc_debuginfo(previous_frame):
    (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
    self = previous_frame.f_locals.get("self")
    dbginfo = function_name + ":" + str(line_number)
    return dbginfo

ARGS_REGS = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"]
CALLER_SAVED_REGS = ["%rax", "%rcx", "%rdx", "%rsi", "%rdi", "%r8", "%r9"]
INT_TYPES = ["i32", "i64", "i16", "i8", "u64", "u32", "u16", "u8"]

def sizeof(ty):
    return {"i64": 8, "i32": 4, "i16": 2, "i8": 1,
            "u64": 8, "u32": 4, "u16": 2, "u8": 1,
            "f64": 8, "f32": 4, "char": 1}[ty]

def is_valid_type(ty):
    return ty in ["i32", "i64", "i16", "i8", "u64", "u32", "u16", "u8", "f64", "f32", "char", "void"]

def check_valid_type(ty):
    if not is_valid_type(ty):
        raise SyntaxError(f"Unknown type '{ty}'")
        
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
        
class RegHint:
    def __init__(self, wanted=None, unwanted=None):
        if type(wanted) == str:
            self.wanted = [wanted]
        else:
            self.wanted = [] if wanted is None else wanted
            
        if type(unwanted) == str:
            self.unwanted = [unwanted]
        else:
            self.unwanted = [] if unwanted is None else unwanted

class CG:
    def __init__(self):
        self.code = []
        self.regs = ["%rax", "%rcx", "%rdx", "%rsi", "%rdi", "%r8", "%r9", "%r10", "%r11", "%r12", "%r13", "%r14", "%r15"]
        self.regs_used = [False] * len(self.regs)
        self.reg_allocator = {}
        self.globals = []
        self.locals = []
        self.O_CONSTANT_FOLDING = False
        
    def regalloc(self, reg_hint=None):
        if reg_hint == None:
            reg_hint = RegHint()
        previous_frame = inspect.currentframe().f_back
        dbginfo = regalloc_debuginfo(previous_frame)
        if len(reg_hint.wanted) > 0:
            for reg_wanted in reg_hint.wanted:
                if not self.is_reg_used(reg_wanted):
                    self.set_reg_used(reg_wanted, dbginfo)
                    return reg_wanted
            
            self.code.append("Request reg " + " or ".join(reg_hint.wanted) + ", but already used")
            reg_hint.wanted = []

        for i, reg in enumerate(self.regs_used):
            if not reg and not self.regs[i] in reg_hint.unwanted:
                self.regs_used[i] = True
                self.reg_allocator[self.regs[i]] = dbginfo
                return self.regs[i]
        self.code.append("Error assigning register, all were used")
        return None
    
    def code_append(self, ln):
        previous_frame = inspect.currentframe().f_back
        filename, line_number, function_name, lines, index = inspect.getframeinfo(previous_frame)
        self = previous_frame.f_locals.get("self")
        posinfo = function_name + ":" + str(line_number)
        dbginfo = posinfo + " " * (18 - len(posinfo)) + str([reg + " " + str(self.reg_allocator[reg]) for i, reg in enumerate(self.regs) if self.regs_used[i]])
        self.code.append(ln + (dbginfo,))
    
    def regfree(self, reg):
        previous_frame = inspect.currentframe().f_back
        filename, line_number, function_name, lines, index = inspect.getframeinfo(previous_frame)
        self.code.append("Freeing " + reg + " called from " + function_name + ":" + str(line_number))
        idx = self.regs.index(reg)
        self.regs_used[idx] = False
        del self.reg_allocator[reg]
        
    def is_reg_used(self, reg):
        return self.regs_used[self.regs.index(reg)]
    
    def set_reg_used(self, reg, dbg):
        self.reg_allocator[reg] = dbg
        self.regs_used[self.regs.index(reg)] = True
        
    def get_global(self, name):
        for sig in self.globals:
            if sig.name == name:
                return sig
    def get_local(self, name):
        for var in self.locals[-1]:
            if var.name == name:
                return var
    
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
                self.append_code(("pushq", reg))
        
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
    
    def int_div(self, lhs, rhs, signed, op):
        # TODO test this bit
        if rhs == "%rdx" or rhs == "%rax":
            # big problem, as rdx and rax are used for dividend
            # first, allocate new register
            old_rhs = rhs
            rhs = self.regalloc(RegHint(unwanted=["%rax", "%rdx"]))
            # second, free old rhs
            self.regfree(old_rhs)
            # third, move regs
            self.code_append(("movq", old_rhs, rhs))
            
        # save regs that are used for dividend
        if self.is_reg_used("%rdx"):
            self.code_append(("pushq", "%rdx"))
        if self.is_reg_used("%rax"):
            self.code_append(("pushq", "%rax"))
            
        # if it's not already, dividend goes in rax
        if lhs != "%rax": self.code_append(("movq", lhs, "%rax"))
        # sign extend rax to rdx
        self.code_append(("cdq",))
        self.code_append((("i" if signed else "") + "divq", rhs))
        
        if op == "/":
            # quotient is in rax
            self.code_append(("movq", "%rax", rhs))
        else:
            # remainder is in rdx
            self.code_append(("movq", "%rdx", rhs))
            
        # unsave regs again
        if self.is_reg_used("%rdx"):
            self.code_append(("popq", "%rdx"))
        if self.is_reg_used("%rax"):
            self.code_append(("popq", "%rax"))
        
        # may have had to modify rhs
        return rhs

    def binexpr(self, ast, reg_hint=None):
        op = ast.op
        
        """"
        if rhs_expr.get_name() == "int_literal" and lhs_expr.get_name() == "int_literal" and self.O_CONSTANT_FOLDING:
            # constexpr
            if op == "+":
                return self.int_literal(IntLit.from_val(ast.lhs + ast.rhs))
            if op == "-":
                return self.int_literal(IntLit.from_val(ast.lhs - ast.rhs))
            if op == "*":
                return self.int_literal(IntLit.from_val(ast.lhs * ast.rhs))
            if op == "/":
                return self.int_literal(IntLit.from_val(ast.lhs // ast.rhs))
        """
        # try and get dividend in rax, then less work later
        if op == "/":
            lhs_hint = RegHint(wanted="%rax")
        else:
            lhs_hint = RegHint()
        
        lhs, lty = self.expr(ast.operands[0], lhs_hint)
        for i, rhs_expr in enumerate(ast.operands[1:]):
            hint = None
            if op == "/":
                hint = RegHint(unwanted=["rax", "rdx"])
            if i == len(ast.operands[1:]) - 1:
                hint = reg_hint
            rhs, rty = self.expr(rhs_expr, hint)
        
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
        
    def int_literal(self, ast, reg_hint=None):
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
    
    def expr(self, ast, reg_hint=None):
        if ast.get_name() == "binexpr":
            return self.binexpr(ast, reg_hint=reg_hint)
        elif ast.get_name() == "int_literal":
            return self.int_literal(ast, reg_hint=reg_hint)
        elif ast.get_name() == "funccall":
            return self.funccall(ast, reg_hint=reg_hint)
        elif type(ast) == Ident:
            return self.ident(ast, reg_hint=reg_hint)
        elif type(ast) == VarAssign:
            return self.var_assign(ast, reg_hint=reg_hint)
        else:
            print("Not implemented: expression type " + ast.get_name())
            exit(1)
    
    def smt(self, ast):
        if type(ast) == VarDef:
            if ast.val != None:
                # convert defs into assigns cos that's how we roll
                ast = VarAssign([Ident(ast.name), ast.val])
            else:
                # nothing to assing; return
                return
        
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

if __name__ == "__main__":
    import argparse, sys, traceback
    parser = argparse.ArgumentParser(
                    prog="Citrus",
                    description='Compile citrus code')
    parser.add_argument("filename")
    parser.add_argument("-o", "--output", help="Specify output file name. Default: <input filename>.s")
    parser.add_argument("-g", "--debug", action="store_true", help="Enable debug comments in assembly")
    args = parser.parse_args()
    try:
        with open(args.filename, "r") as f:
            source = f.read()
    except FileNotFoundError:
        print(args.filename + ": No such file or directory")
        exit(1)
    
    a = CG()
    
    def exception_hook(exctype, value, tb):
        traceback_formated = traceback.format_exception(exctype, value, tb)
        traceback_string = "".join(traceback_formated)
        print(traceback_string, file=sys.stderr)
        print(a.format_code(True))
        
        sys.exit(1)
        
    sys.excepthook = exception_hook

    out = a.gen(parse(source), args.filename, args.debug)
    print(out)
    if args.output is None:
        output_file = ".".join(input_file.split(".")[:-1]) + ".s"
    else:
        output_file = args.output
    
    with open(output_file, "w") as f:
        f.write(out)
