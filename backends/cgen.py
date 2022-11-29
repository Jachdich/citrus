import os
import math
import inspect
from pprint import pprint
from parser import *

INT_TYPES = ["i8", "i16", "i32", "i64", "u8", "u16", "u32", "u64"]

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

def combine_types(lty, rty):
    num_tys = INT_TYPES + ["f32", "f64"]
    if rty in INT_TYPES and lty in INT_TYPES:
        # both ints, biggest wins
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
        return outsigned + str(outbits)
    elif rty in num_tys and lty in num_tys:
        # at least one is float, return biggest flaot type
        if lty[0] == "f":
            lfbits = int(lty[1:])
        else:
            lfbits = 0
        if rty[0] == "f":
            rfbits = int(rty[1:])
        else:
            rfbits = 0
        
        outbits = max(lfbits, rfbits)
        return "f" + str(outbits)
    else:
        raise SyntaxError(f"Cannot combine types '{lhs}' and '{rhs}'")

class FuncSig:
    def __init__(self, name, args, ret_ty):
        self.name = name
        self.args = args
        self.ret_ty = ret_ty

class LocalVar:
    def __init__(self, name, ty):
        self.name = name
        self.ty = ty


class CG:
    def __init__(self):
        self.code = ""
        self.globals = []
        self.locals = []
        self.var = 0
        self.indent = 0
        
    def get_indent(self, offset=0):
        return " " * ((self.indent + offset) * 4)
    
    def figure_out_type(self, ast, locals=None):
        if locals == None:
            locals = []
        if type(ast) == IntLit:
            return "i32"
        elif type(ast) == BinOp:
            lty = self.figure_out_type(ast.operands[0])
            for rty in map(self.figure_out_type, ast.operands[1:]):
                lty = combine_types(lty, rty)
            return lty
        elif type(ast) == CompoundExpr:
            for smt in ast.smts:
                if type(smt) == VarDef:
                    if smt.ty is None:
                        smt.ty = self.figure_out_type(smt.val, locals=locals)
                    locals.append(LocalVar(smt.name, smt.ty))
            return self.figure_out_type(ast.expr, locals=locals)
        elif type(ast) == CompoundSmt:
            return "void"
        elif type(ast) == Ident:
            if ast.val in [l.name for l in locals]:
                return next(filter(lambda l: l.name == ast.val, locals)).ty
            return self.get_local(ast.val).ty
        else:
            raise NotImplementedError(f"Not implemented figuring out type of ast {repr(ast)}")
    
    def gen_var_name(self):
        self.var += 1
        return "__var" + str(self.var)
        
    def get_global(self, name):
        for sig in self.globals:
            if sig.name == name:
                return sig

    def get_local(self, name):
        for var in self.locals[-1]:
            if var.name == name:
                return var
        
        raise SyntaxError(f"Undefined variable '{name}'")
    
    def funccall(self, ast):
        funcname = ast.name
        func_sig = self.get_global(funcname)
        if func_sig is None:
            raise SyntaxError(f"Unknown function '{funcname}'")
            
        num_args = len(ast.args)
        if num_args != len(func_sig.args):
            raise SyntaxError(f"Function '{funcname}' expects {len(func_sig.args)} args but {num_args} were given")
        # TODO arg types
        
        args = []
        for a in ast.args:
            args.append(self.expr(a))
                    
        if func_sig.ret_ty != "void":
            # var_name = self.gen_var_name()
            # self.code += func_sig.ret_ty + " " + var_name + " = " + funcname + "(" + ", ".join(args) + ");\n"
            # return var_name
            return funcname + "(" + ", ".join(args) + ")"
        else:
            self.code += self.get_indent() + funcname + "(" + ", ".join(args) + ");\n"
        
    def binexpr(self, ast):
        op = ast.op
        tmp_code = ""
        
        # for the sake of simplicity here, I'm going to assume that operators =, +=, -=. /= and *= are only 2 (so a += b += c isn't valid)
        # I should probably implement that in the parser at some point, either that or make it valid here
        if op in ["=", "-=", "+=", "/=", "*="]:
            rval = self.expr(ast.operands[1])
            self.code += self.get_indent() + ast.operands[0].val + " " + op + " " + rval + ";\n"
            return ast.operands[0].val

        for i, expr in enumerate(ast.operands):
            resval = self.expr(expr)
            tmp_code += resval
            if i < len(ast.operands) - 1:
                tmp_code += op
                
        # ty = self.figure_out_type(ast)
        # var_name = self.gen_var_name()
        # self.code += ty + " " + var_name + " = " + tmp_code + ";\n"
        # return var_name
        return tmp_code

    def int_literal(self, ast):
        ty = "i32" # TODO figure this out
        # tmp = self.gen_var_name()
        # self.code += ty + " " + tmp + " = " + str(ast) + ";\n"
        # return tmp
        return str(ast)

    def ident(self, ast):
        var = self.get_local(ast.val)
        if var is None:
            raise SyntaxError("Undefined symbol '" + ast.val + "'")
        
        return var.name
    
    def var_assign(self, ast):
        var = self.get_local(ast.lval)
        expr_res = self.expr(ast.rval)
        ret_ty = self.figure_out_type(ast.rval)
        if not can_be_coerced(ret_ty, var.ty):
            raise SyntaxError(f"Attempt to assign expression of type '{ret_ty}' to variable '{ast.lval}' (type '{var.ty}')")
        
        self.code += self.get_indent() + var.name + " = " + expr_res + ";\n"
        return var
    
    def ifsmt(self, ast):
        cond = self.expr(ast.condition)
        self.code += f"{self.get_indent()}if ({cond}) {{\n"
        self.indent += 1
        for smt in ast.body.smts:
            self.smt(smt)
        self.indent -= 1
        self.code += self.get_indent() + "}"
        if ast.else_body is not None:
            self.indent += 1
            self.code += " else {\n"
            for smt in ast.else_body.smts:
                self.smt(smt)
            self.indent -= 1
            self.code += self.get_indent() + "}"
        
        self.code += "\n"
        
    def whilesmt(self, ast):
        cond = self.expr(ast.condition)
        self.code += f"{self.get_indent()}while ({cond}) {{\n"
        self.indent += 1
        for smt in ast.body.smts:
            self.smt(smt)
            
        # update condition
        # cond2 = self.expr(ast.condition)
        # self.code += cond + " = " + cond2 + ";\n"
        self.indent -= 1
        self.code += self.get_indent() + "}\n"
               
    def ifexpr(self, ast: IfExpr):
        ifbtype = self.figure_out_type(ast.body)
        elsebtype = self.figure_out_type(ast.else_body)
        if not can_be_coerced(ifbtype, elsebtype) and not can_be_coerced(elsebtype, ifbtype):
            raise SyntaxError("Else body returns incompatible type '{elsebtype}' (if body returns '{ifbtype}')")
        
        ret_ty = combine_types(ifbtype, elsebtype)
        tmp_name = self.gen_var_name()
        cond_res = self.expr(ast.condition)
        self.code += self.get_indent() + ret_ty + " " + tmp_name + ";\n"
        self.code += self.get_indent() + "if (" + cond_res + ") {\n"
        self.indent += 1
        for smt in ast.body.smts[:-1]:
            self.smt(smt)
        if_res = self.expr(ast.body.expr)
        self.code += self.get_indent() + tmp_name + " = " + if_res + ";\n" + self.get_indent(-1) + "} else {\n"
        for smt in ast.else_body.smts[:-1]:
            self.smt(smt)
        
        else_res = self.expr(ast.else_body.expr)
        self.code += self.get_indent() + tmp_name + " = " + else_res + ";\n" + self.get_indent(-1) + "}\n"
        self.indent -= 1
        
        return tmp_name
    
    def vardef(self, ast: VarDef):
        if ast.ty is None:
            if ast.val is None:
                raise SyntaxError("Black magic fuckery is not supported yet")
            
            ast.ty = self.figure_out_type(ast.val)
        
        if type(ast.ty) == FnType:
            raise SyntaxError("Lambdas are not supported yet")
        else:
            if ast.val is not None:
                expr_res = self.expr(ast.val)
        
            # TODO this generates bad code (too many var defs)
            self.code += self.get_indent() + ast.ty + " " + ast.name
            if ast.val is not None:
                self.code += " = " + expr_res
            self.code += ";\n"
        
        self.locals[-1].append(LocalVar(ast.name, ast.ty))
    
    def expr(self, ast):
        if type(ast) == BinOp:
            return self.binexpr(ast)
        elif type(ast) == IntLit:
            return self.int_literal(ast)
        elif type(ast) == FuncCall:
            return self.funccall(ast)
        elif type(ast) == Ident:
            return self.ident(ast)
        elif type(ast) == VarAssign:
            return self.var_assign(ast)
        elif type(ast) == IfExpr:
            return self.ifexpr(ast)
        else:
            print("Not implemented: expression type " + str(type(ast)))
            exit(1)
    
    def smt(self, ast):
        if type(ast) == VarDef:
            self.vardef(ast)
        elif type(ast) == IfSmt:
            self.ifsmt(ast)
        elif type(ast) == WhileSmt:
            self.whilesmt(ast)
        else:
            self.expr(ast)
    
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
            self.code += f"{sig.ret_ty} {sig.name}({', '.join([str(ty) for ty in sig.args])});\n"
            return
        
        self.locals.append([])
        
        locdefs = filter(lambda n: type(n) == VarDef, ast.body.smts)
        
        # add locals to symtable
        for name, ty in ast.args:
            check_valid_type(ty)
            self.locals[-1].append(LocalVar(name, ty))

        ret_ty = ast.ret_ty
        if ret_ty is None:
            ret_ty = self.figure_out_type(ast.body)
        else:
            actual_ret_ty = self.figure_out_type(ast.body)
            if not can_be_coerced(actual_ret_ty, ret_ty):
                raise SyntaxError(f"Function '{str(ast)}' should return type '{ret_ty}', but last expression is of type '{actual_ret_ty}'")
        sig.ret_ty = ret_ty

        self.code += f"{sig.ret_ty} {sig.name}({', '.join([str(ty) + ' ' + str(name) for name, ty in ast.args])}) {{\n"
        
        self.indent += 1
        for smt in ast.body.smts:
            self.smt(smt)
        
        if type(ast.body) == CompoundExpr:
            ret_val = self.expr(ast.body.expr)
            self.code += self.get_indent() + "return " + ret_val + ";\n"
            
        self.locals.pop()
        self.code += "}\n"
        self.indent -= 1
        
    def structdef(self, smt):
        self.code += "typedef struct " + smt.name + " {\n"
        for name, ty in smt.members:
            self.code += "    " + ty + " " + name + ";\n"
        self.code += "};\n"
        
    def importsmt(self, smt, already_imported):
        if not os.path.isfile(smt.fname):
            raise ImportError(f"{smt.fname}: No such file or directlry")
        with open(smt.fname, "r") as f:
            source = f.read()
            
        already_imported.append(smt.fname)
        
        ast = parse(source)
        for smt in ast:
            if type(smt) == FnDef:
                self.funcdef(smt)
            elif type(smt) == ImportSmt and smt.fname not in already_imported:
                # recursively import anything we haven't already
                self.importsmt(smt, already_imported)
        

    def gen(self, ast, fname, debug=False):
        pprint(ast.as_list())
        for smt in ast:
            if type(smt) == FnDef:
                self.funcdef(smt)
            elif type(smt) == StructDef:
                self.structdef(smt)
            elif type(smt) == ImportSmt:
                self.importsmt(smt, [fname])
            else:
                print(f"Invalid syntax: Unexpected token '{smt}'")
                exit(1)
        
        return self.format_code(debug)
        
    def format_code(self, debug=False):
        defs = """
#include <stdint.h>
#define i8  int8_t
#define i16 int16_t
#define i32 int32_t
#define i64 int64_t
#define u8  uint8_t
#define u16 uint16_t
#define u32 uint32_t
#define u64 uint64_t
#define f32 float
#define f64 double
"""
        return defs + self.code
