import os
import math
import inspect
from pprint import pprint
from parser import *

INT_TYPES = ["i8", "i16", "i32", "i64", "u8", "u16", "u32", "u64"]

# need some info about the return type of an expression (be that func sig or a Type)

# TODO for Vec:
# struct templates
# [] operator
# sizeof() (& macros?)
# operator overloading
# calling associated functions

# TODO hacky things to fix:
# multiple .s
# struct init order

def can_be_coerced(from_, to):
    # same type always able to convert
    if from_ == to: return True
    
    if from_.num_ptr == 1 and (from_.name == "void" or to.name == "void"):
        # void pointers are coercible to and from any type
        return True
    
    if from_.name in INT_TYPES and to.name in INT_TYPES:
        if from_.name[0] == "i" and to.name[0] == "u":
            return False # can't coerce signed to unsigned

        fbits = int(from_.name[1:])
        tbits = int(to.name[1:])
        if from_.name[0] == "u" and to.name[0] == "i":
            return tbits > fbits # must have more bits in the signed to fit the unsigned
        else:
            # same signedness can coerce if dest bits >= source bits
            return tbits >= fbits
    
    # TODO support other datatypes
    return False

def combine_types(lty, rty):
    if lty.num_ptr != 0 or rty.num_ptr != 0:
        raise SyntaxError("Pointer arith isn't supported yet")
    num_tys = INT_TYPES + ["f32", "f64"]
    if rty.name in INT_TYPES and lty.name in INT_TYPES:
        # both ints, biggest wins
        lsigned = lty.name[0] == "i"
        rsigned = rty.name[0] == "i"
        lbits = int(lty.name[1:])
        rbits = int(rty.name[1:])
        if lsigned or rsigned:
            outsigned = "i"
            signed = True
        else:
            outsigned = "u"
            signed = False

        outbits = max(lbits, rbits)
        return Type([Ident([outsigned + str(outbits)])])

    elif rty.name in num_tys and lty.name in num_tys:
        # at least one is float, return biggest float type
        if lty.name[0] == "f":
            lfbits = int(lty.name[1:])
        else:
            lfbits = 0
        if rty.name[0] == "f":
            rfbits = int(rty.name[1:])
        else:
            rfbits = 0
        
        outbits = max(lfbits, rfbits)
        return Type([Ident(["f" + str(outbits)])])
    else:
        raise SyntaxError(f"Cannot combine types '{lhs}' and '{rhs}'")

class FuncSig:
    def __init__(self, name, args, ret_ty, ast, generic=False):
        self.name = name
        self.args = args
        self.ret_ty = ret_ty
        self.is_generic = generic
        self.ast = ast
        
class StructSig:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

class LocalVar:
    def __init__(self, name, ty):
        self.name = name
        self.ty = ty
        
    def __repr__(self):
        return f"LocalVar('{self.name}', {self.ty})"

def mangle_func(name, templates):
    get_mangle_type = lambda t: t.name + "p" * t.num_ptr
    return "_".join([name] + [get_mangle_type(i) for i in templates.values()])

class CG:
    def __init__(self, fname):
        self.code = ""
        self.fns = []
        self.structs = []
        self.globals = []
        self.locals = []
        self.var = 0
        self.indent = 0
        self.already_imported = [os.path.abspath(fname)]
        self.forward_defs = []
    
    
    def is_valid_type(self, ty):
        if ty.name in ["i32", "i64", "i16", "i8", "u64", "u32", "u16", "u8", "f64", "f32", "char", "void"]:
            return True
        return self.get_global(ty.name) != None

    def check_valid_type(self, ty):
        if not self.is_valid_type(ty):
            raise SyntaxError(f"Unknown type '{ty}'")
    
    def get_indent(self, offset=0):
        return " " * ((self.indent + offset) * 4)
    
    def get_actual_ret_ty(self, ast: FuncCall, locals=None):
        sig = self.get_global(ast.name)
        if not sig.ret_ty.name in sig.ast.template_args:
            # return type is not dependant on a template
            return sig.ret_ty
        else:
            template_name = sig.ret_ty
            index = sig.ast.template_args.index(template_name.name)
            # get the relevant arg expression passed in which defines the template
            exp = ast.args[index]
            return self.figure_out_type(exp, locals)

    def figure_out_type(self, ast, locals=None) -> Type:
        if locals == None:
            locals = []
        if type(ast) == IntLit:
            # TODO: how????
            return Type([Ident(["u16"])])
        elif type(ast) == BinOp:
            lty = self.figure_out_type(ast.operands[0], locals)
            if ast.op == ".":
                # HACK: assumes only one . (a.b.c is not valid)
                sig = self.get_global(self.figure_out_type(ast.operands[0], locals).name)
                if ast.operands[1].val in [i[0] for i in sig.fields]:
                    return [i[1] for i in sig.fields if i[0] == ast.operands[1].val][0] # hacky shit
                else:
                    raise SyntaxErro(f"bad field {ast.operands[1]} in {ast.operands[0]}")
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
            return Type([Ident(["void"])])
        elif type(ast) == Ident:
            if ast.val in [l.name for l in locals]:
                return next(filter(lambda l: l.name == ast.val, locals)).ty
            return self.get_local(ast.val).ty
        elif type(ast) == StructInit:
            return Type([Ident([self.get_global(ast.struct_name).name])])
        elif type(ast) == FuncCall:
            return self.get_actual_ret_ty(ast, locals)
        elif type(ast) == UnOp:
            ty = self.figure_out_type(ast.operand, locals)
            if ast.op == "&":
                ty.num_ptr += 1
                return ty
            elif ast.op == "*":
                ty.num_ptr -= 1
                return ty
            else:
                raise NotImplementedError("Not implemented figuring out unop " + ast.op)
        else:
            raise NotImplementedError(f"Not implemented figuring out type of ast {repr(ast)}")
    
    def get_type(self, ty):
        return ty.name + "*" * ty.num_ptr
    
    def gen_var_name(self):
        self.var += 1
        return "__var" + str(self.var)
        
    def get_global(self, name, *, no_except=False):
        for sig in self.globals:
            if sig.name == name:
                return sig
        if not no_except:
            raise SyntaxError(f"Undefined global '{name}'")

    def get_local(self, name, *, no_except=False):
        for var in self.locals[-1]:
            if var.name == name:
                return var
        if not no_except:
            raise SyntaxError(f"Undefined variable '{name}'")
    
    def funccall(self, ast: FuncCall):
        func_expr = self.expr(ast.fn_expr)
        func_sig = self.get_global(funcname)
        if func_sig is None:
            raise SyntaxError(f"Unknown function '{funcname}'")
        
        num_args = len(ast.args)
        if num_args != len(func_sig.args):
            raise SyntaxError(f"Function '{funcname}' expects {len(func_sig.args)} args but {num_args} were given")
        
        args = []
        templates = {}
        for i, a in enumerate(ast.args):
            actual_ty = self.figure_out_type(a)
            expected_ty = func_sig.args[i]
            if expected_ty.name in func_sig.ast.template_args:
                templates[expected_ty] = actual_ty
            else:
                if not can_be_coerced(actual_ty, expected_ty):
                    raise SyntaxError(f"Function '{funcname}' expects argument argument {i + 1} to be of type '{expected_ty}', but it is actually type '{actual_ty}'")
            args.append(self.expr(a))
        
        if func_sig.is_generic:
            # HACK save code, kinda hacky
            code = self.code
            self.code = ""
            self.make_fn_from_sig(func_sig, with_template_args=templates)
            self.code = code

        if func_sig.ret_ty.name != "void" or func_sig.ret_ty.num_ptr != 0:
            return mangle_func(funcname, templates) + "(" + ", ".join(args) + ")"
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
        
        # operator. gets special treatment
        if op == ".":
            # TODO: check that each field exists
            lval = ast.operands[0]
            ty = self.figure_out_type(lval)
            rvals = ast.operands[1:]
            if ty.num_ptr == 0:
                tmp_code += "(" + self.expr(lval) + ")." + ".".join([val.val for val in rvals])
            elif ty.num_ptr == 1:
                tmp_code += "(" + self.expr(lval) + ")->" + ".".join([val.val for val in rvals])
            else:
                raise SyntaxError("Can't access field '" + rvals[0].val + "' on object of type " + str(ty))
            return tmp_code
            
        for i, expr in enumerate(ast.operands):
            resval = self.expr(expr)
            tmp_code += resval
            if i < len(ast.operands) - 1:
                tmp_code += op
                
        return tmp_code
    
    def unop(self, ast):
        return ast.op + self.expr(ast.operand)

    def int_literal(self, ast):
        # ty = "i32" # TODO figure this out
        # tmp = self.gen_var_name()
        # self.code += ty + " " + tmp + " = " + str(ast) + ";\n"
        # return tmp
        return str(ast)

    def ident(self, ast):
        var = self.get_local(ast.val, no_except=True)
        if var is not None:
            return var.name
        
        var = self.get_global(ast.val, no_except=True)
        if var is not None:
            return var.name
            
        raise SyntaxError("Undefined symbol '" + ast.val + "'")
    
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
        self.code += self.get_indent() + self.get_type(ret_ty) + " " + tmp_name + ";\n"
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
        
        if ast.ty.fn_ptr:
            raise SyntaxError("Lambdas are not supported yet")
        else:
            if ast.val is not None:
                expr_res = self.expr(ast.val)
        
            self.code += self.get_indent() + self.get_type(ast.ty) + " " + ast.name
            if ast.val is not None:
                self.code += " = " + expr_res
            self.code += ";\n"
        self.locals[-1].append(LocalVar(ast.name, ast.ty))
    
    def structinit(self, ast):
        return f"({ast.struct_name}){{{', '.join([self.expr(v[1]) for v in ast.init_args])}}}"
    
    def expr(self, ast):
        # print("expr", ast)
        if type(ast) == BinOp:
            return self.binexpr(ast)
        elif type(ast) == UnOp:
            return self.unop(ast)
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
        elif type(ast) == StructInit:
            return self.structinit(ast)
        else:
            print("Not implemented: expression type " + str(type(ast)))
            exit(1)
    
    def smt(self, ast):
        # print("smt", ast)
        if type(ast) == VarDef:
            self.vardef(ast)
        elif type(ast) == IfSmt:
            self.ifsmt(ast)
        elif type(ast) == WhileSmt:
            self.whilesmt(ast)
        else:
            res = self.expr(ast)
            if res is not None:
                self.code += self.get_indent() + res + ";\n"
    
    def gen_fn_sig(self, ast):
        ret_ty = ast.ret_ty
        if ret_ty is None:
            ret_ty = Type([Ident(["void"])])
        
        if len(ast.template_args) != 0:
            generic = True
        else:
            generic = False
            self.check_valid_type(ret_ty)
        args = [a[1] for a in ast.args] # just types
        sig = FuncSig(ast.name, args, ret_ty, ast, generic)
        return sig
   
    def add_global(self, glob):
        for g in self.globals:
            if g.name == glob.name:
                raise SyntaxError(f"Redefinition of '{glob.name}'")
        self.globals.append(glob)

    def funcdef(self, ast, always_forward=False):
        sig = self.gen_fn_sig(ast)
        self.add_global(sig)
        if sig.is_generic:
            # don't make the function yet!
            return
        
        self.make_fn_from_sig(sig, always_forward)
        
    def make_fn_from_sig(self, sig, always_forward=False, with_template_args=None):
        if self.code != "":
            raise RuntimeError("Expected code to be empty, but it contained '" + self.code + "'")
        if with_template_args is None:
            with_template_args = {}
        
        get_real_type = lambda ty: with_template_args.get(ty, ty)
        
        func_name = mangle_func(sig.name, with_template_args)        
        if sig.ast.forward_decl or always_forward:
            self.forward_defs.append(f"{self.get_type(get_real_type(sig.ret_ty))} {func_name}({', '.join([self.get_type(get_real_type(ty)) for ty in sig.args])});")
            return
        
        self.locals.append([])
        
        locdefs = filter(lambda n: type(n) == VarDef, sig.ast.body.smts)
        
        # add locals to symtable
        for name, ty in sig.ast.args:
            if ty in with_template_args:
                ty = with_template_args[ty]
            self.check_valid_type(ty)
            self.locals[-1].append(LocalVar(name, ty))

        ret_ty = get_real_type(sig.ast.ret_ty)
        if ret_ty is None:
            ret_ty = self.figure_out_type(sig.ast.body)
        else:
            actual_ret_ty = self.figure_out_type(sig.ast.body)
            if not can_be_coerced(actual_ret_ty, ret_ty):
                raise SyntaxError(f"Function '{str(sig.ast)}' should return type '{ret_ty}', but last expression is of type '{actual_ret_ty}'")
        
        sig.ret_ty = ret_ty

        self.code += f"{self.get_type(sig.ret_ty)} {func_name}({', '.join([self.get_type(get_real_type(ty)) + ' ' + str(name) for name, ty in sig.ast.args])}) {{\n"
        
        self.indent += 1
        for smt in sig.ast.body.smts:
            self.smt(smt)
        
        if type(sig.ast.body) == CompoundExpr:
            ret_val = self.expr(sig.ast.body.expr)
            self.code += self.get_indent() + "return " + ret_val + ";\n"
            
        self.locals.pop()
        self.code += "}\n"
        self.indent -= 1
        self.fns.append(self.code)
        self.code = ""
        
    def structdef(self, smt):
        code = "typedef struct {\n"
        for name, ty in smt.members:
            code += "    " + self.get_type(ty) + " " + name + ";\n"
        code += "} " + smt.name + ";\n"
        self.structs.append(code)
        self.add_global(StructSig(smt.name, smt.members))
        
    def importsmt(self, smt, additional_dirs):
        source = None
        full_path = None
        for dir in additional_dirs:
            full_path = os.path.abspath(os.path.join(dir, smt.fname))
            if os.path.isfile(full_path):
                with open(full_path, "r") as f:
                    source = f.read()
                break
        
        if source is None:
            raise ImportError(f"Unresolved import: '{smt.fname}'")
        if full_path in self.already_imported:
            # already done, bail
            return

        self.already_imported.append(full_path)
        
        ast = parse(source)
        for smt in ast:
            if type(smt) == FnDef:
                self.funcdef(smt, True)
            elif type(smt) == StructDef:
                self.structdef(smt)
            elif type(smt) == ImportSmt:
                # recursively import
                self.importsmt(smt, additional_dirs)
        

    def gen(self, ast, debug, imports):
        pprint(ast.as_list())
        # print(reconst_src(ast))
        print()
        for smt in ast:
            if type(smt) == FnDef:
                self.funcdef(smt)
            elif type(smt) == StructDef:
                self.structdef(smt)
            elif type(smt) == ImportSmt:
                self.importsmt(smt, imports)
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
        forwards = "\n".join(self.forward_defs)
        fns = "\n".join(self.fns)
        structs = "\n".join(self.structs)
        return defs + "\n" + structs + "\n" + forwards + "\n" + fns + "\n"
