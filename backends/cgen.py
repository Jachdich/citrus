import os
import math
import inspect
from pprint import pprint
from parser import *

INT_TYPES = ["i8", "i16", "i32", "i64", "u8", "u16", "u32", "u64"]

# TODO
# a.b() doesn't work with templates

# TODO for Vec:
# struct templates
# [] operator
# sizeof() (& macros?)
# operator overloading

# TODO hacky things to fix:
# multiple .s
# struct init order

# temp var name counter
var = 0

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

def combine_numeric_types(lty, rty):
    """Calculate the resultant type from performing an operation on two numeric types. Often this will be the bigger type."""
    if lty == rty:
        return lty
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
        raise SyntaxError(f"{lty.get_context()}Cannot combine types '{lty}' and '{rty}'")

class FuncSig:
    def __init__(self, name, args, ret_ty, ast, assoc=False, generic=False):
        self.name = name
        self.args = args
        self.ret_ty = ret_ty
        self.is_generic = generic
        self.ast = ast
        self.is_assoc_fn = assoc

    def __repr__(self):
        return f"FuncSig({self.name}, {self.args}, {self.ret_ty}, {self.is_generic}, {self.is_assoc_fn})"
        
class StructSig:
    def __init__(self, name, fields, generic=False):
        self.name = name
        self.fields = fields
        self.is_generic = generic

    def __repr__(self):
        return f"StructSig({self.name} {{ {self.fields}) }})"

class LocalVar:
    def __init__(self, name, ty):
        self.name = name
        self.ty = ty
        
    def __repr__(self):
        return f"LocalVar('{self.name}', {self.ty})"

class Type:
    def __init__(self, name: str, num_ptr: int=0, template_args: list=None):
        self.name = name
        self.num_ptr = num_ptr
        self.template_args = template_args or []

    def get_mangled_name(self):
        return "_".join([name + "p" * self.num_ptr] + [i.name + "p" * i.num_ptr for i in self.template_args])

class CEmitter:
    def __init__(self):
        self.code = ""
        self.indent = 0

    def get_indent(self, offset=0):
        return " " * ((self.indent + offset) * 4)

    def gen_var_name(self):
        global var
        var += 1
        return "__var" + str(var)

class CG:
    def __init__(self, fname):
        self.fns = []
        self.structs = []
        self.globals = {}
        self.locals = {}
        self.already_imported = [os.path.abspath(fname)]
        self.forward_defs = []

    def is_valid_type(self, ty):
        for arg in ty.template_args:
            if not self.is_valid_type(arg): return False
        if ty.name in ["i32", "i64", "i16", "i8", "u64", "u32", "u16", "u8", "f64", "f32", "char", "void"]:
            return True
        return self.get_global(ty.name) != None

    def check_valid_type(self, ty):
        if not self.is_valid_type(ty):
            raise SyntaxError(f"{ty.get_context()}Unknown type '{ty}'")
    
    def get_actual_ret_ty(self, ast: FuncCall, locals=None):
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

        if type(ast) == Type:
            # already a type, do nothing
            return ast
        elif type(ast) == IntLit:
            # TODO: how????
            return Type("u16")
        elif type(ast) == BinOp:
            lty = self.figure_out_type(ast.operands[0], locals)
            if ast.op == ".":
                # HACK: assumes only one . (a.b.c is not valid)
                name = self.figure_out_type(ast.operands[0], locals).name
                sig = self.get_global(name)
                if sig is None:
                    raise SyntaxError(f"{ast.get_context}Unknown type '{name}'")

                # search for the type in the list of (name, type) pairs
                for field_name, field_type in sig.fields:
                    if field_name == ast.operands[1].val:
                        return field_type

                # haven't found it yet, must not exist
                raise SyntaxError(f"{ast.get_context()}bad field {ast.operands[1]} in {ast.operands[0]}")
            for rty in map(self.figure_out_type, ast.operands[1:]):
                lty = combine_numeric_types(lty, rty)
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
            
            loc = self.get_local(ast.val)
            if loc is not None:
                return loc.ty
            
            glob = self.get_global(ast.val)
            if glob is not None:
                return glob
            raise SyntaxError(ast.get_context() + "Undefined symbol '" + ast.val + "'")
            
        elif type(ast) == StructInit:
            sig = self.get_global(ast.struct_name)
            if sig is None:
                raise SyntaxError(f"{ast.get_context()}Unknown type '{ast.struct_name}'")
            return Type(ast.src, ast.pos, [Ident(ast.src, ast.pos, [sig.name])])
        elif type(ast) == FuncCall:
            return self.get_actual_ret_ty(ast, locals)
        elif type(ast) == UnOp:
            ty = self.figure_out_type(ast.operand, locals)
            num_ptr = ty.num_ptr
            if ast.op == "&":
                num_ptr += 1
                return Type(None, name=ty.name, num_ptr=num_ptr)
            elif ast.op == "*":
                num_ptr -= 1
                return Type(None, name=ty.name, num_ptr=num_ptr)
            else:
                raise NotImplementedError("Not implemented figuring out unop " + ast.op)
        elif type(ast) == IfExpr:
            return self.figure_out_type(ast.body, locals)
        else:
            raise NotImplementedError(f"Not implemented figuring out type of ast {repr(ast)}")
    
    def get_type(self, ty):
        return ty.name + "*" * ty.num_ptr
    
    def get_fn_name(self, ast: FuncCall):
        if type(ast.fn_expr) == Ident:
            return ast.fn_expr.val, None
        elif type(ast.fn_expr) == BinOp and ast.fn_expr.op in (".", "::"):
            if len(ast.fn_expr.operands) == 2:
                # only 2 operands, can just eval lhs
                lhs, rhs = ast.fn_expr.operands
            else:
                rhs = ast.fn_expr.operands.pop()
                lhs = ast.fn_expr
            assert type(rhs) == Ident, "Wtf, rhs is " + repr(rhs)
            l_ty = self.figure_out_type(lhs)
            return l_ty.name + "_" + rhs.val, lhs
        else:
            raise RuntimeError(f"{ast.get_context()}Wtf, type of ast.fn_expr is", repr(ast.fn_expr))
        
    def funccall(self, ast: FuncCall, em: CEmitter):
        func_name, self_expr = self.get_fn_name(ast)
        func_sig = self.get_global(func_name)
        if func_sig is None:
            raise SyntaxError(f"{ast.get_context()}Unknown function '{func_name}'")
        num_args = len(ast.args)
        if func_sig.is_assoc_fn and ast.fn_expr.op == ".":
            num_args += 1
            if self.figure_out_type(self_expr).num_ptr != 1:
                # automatically make self into a pointer
                self_expr = UnOp(ast.src, ast.pos, [[self_expr, "&"]])
            ast.args = [self_expr] + ast.args
        if num_args != len(func_sig.args):
            raise SyntaxError(f"{ast.get_context()}Function '{func_name}' expects {len(func_sig.args)} args but {num_args} were given")
        
        args = []
        templates = {}
        for i, a in enumerate(ast.args):
            actual_ty = self.figure_out_type(a)
            expected_ty = func_sig.args[i]
            if expected_ty.name in func_sig.ast.template_args:
                templates[expected_ty] = actual_ty
            else:
                if not can_be_coerced(actual_ty, expected_ty):
                    raise SyntaxError(f"{ast.get_context()}Function '{func_name}' expects argument argument {i + 1} to be of type '{expected_ty}', but it is actually type '{actual_ty}'")
            args.append(self.expr(a))

        # kinda hacky: if the function is associated with a generic struct, any generic arguments should be defined by the struct it is called on
        # e.g.
        # Slice<char>::from_ptr(0, 0)
        # assuming from_ptr is generic over T and associated with Slice<T>, T should be char since it was explicitly called on Slice<char>
        if func_sig.is_generic and func_sig.is_assoc_fn and ast.fn_expr.op == "::" and len(self.figure_out_type(ast.fn_expr.operands[0]).template_args) > 0:
            templates[Type(ast.src, ast.pos, None, name="T", num_ptr=1, template_args=[])] = Type(ast.src, ast.pos, None, name="char", num_ptr=0, template_args=[])
        
        if func_sig.is_generic:
            inner_em = CEmitter()
            self.make_fn(ast, inner_em, with_template_args=templates)

        if func_sig.ret_ty.name != "void" or func_sig.ret_ty.num_ptr != 0:
            return mangle_func(func_name, templates) + "(" + ", ".join(args) + ")"
        else:
            em.code += self.get_indent() + func_name + "(" + ", ".join(args) + ");\n"
        
    def binexpr(self, ast, em):
        op = ast.op
        tmp_code = ""
        
        # for the sake of simplicity here, I'm going to assume that operators =, +=, -=. /= and *= are only 2 (so a += b += c isn't valid)
        # I should robably implement that in the parser at some point, either that or make it valid here
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
                raise SyntaxError(f"{ast.get_context()}Can't access field '" + rvals[0].val + "' on object of type " + str(ty))
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
        var = self.get_local(ast.val)
        if var is not None:
            return var.name
        
        var = self.get_global(ast.val)
        if var is not None:
            return var.name
            
        raise SyntaxError(f"{ast.get_context()}Undefined symbol '" + ast.val + "'")
    
    def var_assign(self, ast):
        var = self.get_local(ast.lval)
        if var is None:
            raise SyntaxError(f"{ast.get_context()}Unknown variable '{ast.lval}'")
        expr_res = self.expr(ast.rval)
        ret_ty = self.figure_out_type(ast.rval)
        if not can_be_coerced(ret_ty, var.ty):
            raise SyntaxError(f"{ast.get_context()}Attempt to assign expression of type '{ret_ty}' to variable '{ast.lval}' (type '{var.ty}')")
        
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
            raise SyntaxError(f"{ast.get_context()}Else body returns incompatible type '{elsebtype}' (if body returns '{ifbtype}')")
        
        ret_ty = combine_numeric_types(ifbtype, elsebtype)
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
                raise SyntaxError(f"{ast.get_context()}Black magic fuckery is not supported yet")
            ast.ty = self.figure_out_type(ast.val)
        
        if ast.ty.fn_ptr:
            raise SyntaxError(f"{ast.get_context()}Lambdas are not supported yet")
        else:
            if ast.val is not None:
                expr_res = self.expr(ast.val)
        
            self.code += self.get_indent() + self.get_type(ast.ty) + " " + ast.name
            if ast.val is not None:
                self.code += " = " + expr_res
            self.code += ";\n"
        self.locals[-1].append(LocalVar(ast.name, ast.ty))
    
    def structinit(self, ast):
        struct_sig = self.get_global(ast.struct_name)
        if struct_sig is None:
            raise SyntaxError(f"{ast.get_context()}Struct '{ast.struct_name}' does not exist")
        arg_list = []
        for name, ty in struct_sig.fields:
            for n, e in ast.init_args:
                if n == name:
                    if not can_be_coerced(self.figure_out_type(e), ty):
                        raise SyntaxError(f"{ast.get_context()}Expected type '{ty}' but got '{self.figure_out_type(e)}' instead for field '{name}' of struct '{ast.struct_name}'")
                    arg = self.expr(e)
                    arg_list.append(arg)
        return f"({ast.struct_name}){{{', '.join(arg_list)}}}"
    
    def expr(self, ast):
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
            raise NotImplementedError("Not implemented: expression type " + str(type(ast)))
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
            ret_ty = Type("void")
        
        if len(ast.template_args) != 0:
            generic = True
        else:
            generic = False
            self.check_valid_type(ret_ty)
        args = [a[1] for a in ast.args] # just types
        name = ast.get_mangled_name()
        sig = FuncSig(name, args, ret_ty, ast, ast.assoc_struct is not None, generic)
        return sig
   
    def add_global(self, name: str, ast: Ast):
        if name in self.globals:
            raise SyntaxError(f"Redefinition of '{name}'")
        self.globals[name] = ast

    def funcdef(self, ast: FnDef, always_forward=False):
        self.add_global(ast.get_semimangled_name(), ast)
        # check if generic - if not, don't make the function yet!
        if len(ast.template_args) == 0:
            self.make_fn(ast, always_forward)
        
    def make_fn(self, sig, always_forward=False, with_template_args=None):
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
                raise SyntaxError(f"{actual_ret_ty.get_context()}Function '{str(sig.ast)}' should return type '{ret_ty}', but last expression is of type '{actual_ret_ty}'")
        
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
        # TODO generic args as part of steruct sig
        self.add_global(StructSig(smt.name, smt.members))
        if len(smt.template_args) > 0:
            return
        code = "typedef struct {\n"
        for name, ty in smt.members:
            code += "    " + self.get_type(ty) + " " + name + ";\n"
        code += "} " + smt.name + ";\n"
        self.structs.append(code)
        
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
        em = CEmitter()
        for smt in ast:
            if type(smt) == FnDef:
                self.funcdef(smt, em)
            elif type(smt) == StructDef:
                self.structdef(smt, em)
            elif type(smt) == ImportSmt:
                self.importsmt(smt, imports, em)
            else:
                print(f"{smt.get_context()}Invalid syntax: Unexpected token '{smt}'")
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
