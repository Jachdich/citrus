import pyparsing as pp
from pyparsing import alphas, alphanums
from enum import StrEnum, unique
pp.ParserElement.enableLeftRecursion()

class BinTree:
    def __init__(self, left: BinTree | None, right: BinTree | None):
        self.left = left
        self.right = right

class Ast:
    def __init__(self, src: str, pos, tokens):
        self.src = src
        self.pos = pos
        self.column = -1
        self.lineno = src.count("\n", 0, pos) + 1
        while src[pos] != "\n" and pos > 0:
            pos -= 1
            self.column += 1

    def get_context(self):
        s = "\n".join(self.src.split("\n")[max(self.lineno-3, 0):self.lineno]) + "\n"
        s += " " * (self.column) + "^ " + str(self.lineno) + ":" + str(self.column)
        return "\n" + s + "\n"

@unique
class Primitive(StrEnum):
    I8 = "i8"
    I16 = "i16"
    I32 = "i32"
    I64 = "i64"
    U8 = "u8"
    U16 = "u16"
    U32 = "u32"
    U64 = "u64"
    F32 = "f32"
    F64 = "f64"
    CHAR = "char"
    VOID = "void"
    STRUCT = "struct"
    FUNCTION = "fn"

class Type:
    name: str
    generics: list
    primitive: Primitive
    complex: bool
    concrete: bool
    def __init__(self, primitive, name=None, generics=None):
        if primitive == Primitive.STRUCT or primitive == Primitive.FUNCTION:
            assert name is not None, "Structs must have a name"
            self.name = name

            if generics is not None:
                self.generics = generics
            else:
                self.generics = []

            self.complex = True # dealing with a complex type
        else:
            self.complex = False # just the primitive

        self.primitive = primitive

    def get_mangled_name(self, resolved_generics: dict=None):
        if not self.complex:
            # just a primitive
            return self.primitive
        else:
            if resolved_generics is None and len(self.generics) > 0:
                raise RuntimeException("Cannot get mangled name without knowing the generic resolutions!")
            return self.name + "".join(["_" + resolved_generics[g].get_mangled_name() for g in self.generics])


class CG:
    def __init__(self):
        self.globals: dict[str, Type] = {}

    def add_global(self, name: str, ast: Ast):
        if name in self.globals:
            raise SyntaxError(f"{ast.get_context()}Redefinition of '{name}'")
        self.globals[name] = ast

    def get_global(self, name: str) -> Type:
        for sig in self.globals:
            if sig == name:
                return sig

    def is_valid_type(self, ty: Type):
        # for arg in ty.generics:
        #     if not self.is_valid_type(arg): return False
        if ty.c_name().strip("*") in ["i32", "i64", "i16", "i8", "u64", "u32", "u16", "u8", "f64", "f32", "char", "void"]:
            return True
        return self.get_global(ty.c_name()) != None

    def check_valid_type(self, ty):
        if not self.is_valid_type(ty):
            raise SyntaxError(f"{ty.get_context()}Unknown type '{ty}'")
    
    def compile(self, parsed: list[Ast]):
        total_code = '#include "citrus.h"\n'
        for smt in parsed:
            total_code += "// " + str(smt) + "\n"
            code, exprcode = smt.compile(self, 0)
            assert exprcode is None, "statements shouldn't generate an expression"
            if code is not None:
                total_code += code + "\n\n"
        return total_code

def type_assert(var, types):
    if not isinstance(var, types):
        raise TypeError(f"Expected type {types} and instead got {type(var)}")

class NumLit(Ast):
    val: int | float
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.val = int(tokens[0])
        type_assert(self.val, (int, float))
        
    def from_val(val):
        return NumLit([val])
    
    def __repr__(self):
        return f"NumLit({self.val})"
    def __str__(self):
        return str(self.val)

    def get_type(self):
        return Type("u16")

    def compile(self, state, indent):
        return None, str(self.val)
        

class StrLit(Ast):
    val: str
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.val = tokens[0]
        type_assert(self.val, str)
        
    def from_val(val):
        return StrLit([val])
    
    def __repr__(self):
        return f"StrLit({self.val})"
    def __str__(self):
        return str(self.val)

    def compile(self, state, indent):
        return None, f'"{self.val}"'

class Ident(Ast):
    name: str
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.name = tokens[0]
        type_assert(self.name, str)

    def __repr__(self):
        return f"Ident({self.name})"

    def compile(self, state: CG, indent):
        state.check_valid_type(self)
        return None, self.name

    def c_name(self) -> str:
        return self.name

class GenericIdent(Ast):
    name: str
    generics: list["TypeIdent"]
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.name = tokens[0].name
        self.generics = tokens[1:] if len(tokens) > 1 else []
        type_assert(self.name, str)
        [type_assert(g, TypeIdent) for g in self.generics]

    def __repr__(self):
        gens = f"<{', '.join(map(repr, self.generics))}>" if len(self.generics) > 0 else ""
        return f"GenericIdent({self.name}{gens})"

    def c_name(self) -> str:
        return self.name

class NamespacedIdent(Ast):
    vals: list[Ident]
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.vals = tokens
        [type_assert(g, Ident) for g in self.vals]
        assert len(self.vals) > 0

    def __repr__(self):
        return f"NamespacedIdent({', '.join(map(repr, self.vals))})"

class TypeIdent(Ast):
    vals: list[GenericIdent]
    num_ptr: int
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.vals = list(tokens[1])
        self.num_ptr = len(tokens[0])
        [type_assert(g, GenericIdent) for g in self.vals]
        assert len(self.vals) > 0

    def __repr__(self):
        return f"TypeIdent({', '.join(map(repr, self.vals))})"

    def c_name(self) -> str:
        return "_".join([val.c_name() for val in self.vals]) + "*" * self.num_ptr

class BinOp(Ast):
    op: str
    operands: tuple[Ast, Ast]
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.op = tokens[0][1]
        self.operands = tuple(tokens[0][::2])
        type_assert(self.op, str)
        assert len(self.operands) == 2
        type_assert(self.operands[0], Ast)
        type_assert(self.operands[1], Ast)
    
    def __repr__(self):
        return "BinOp(" + f" {self.op} ".join(map(repr, self.operands)) + ")"
    def __str__(self):
        return f" {self.op} ".join(map(str, self.operands))

    def compile(self, state, indent): 
        return None, f" {self.op} ".join(map(str, self.operands))

class BlockExpr(Ast):
    smts: list[Ast]
    expr: Ast
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.smts = tokens[:-1]
        self.expr = tokens[-1]
        type_assert(self.smts, list)
        [type_assert(s, Ast) for s in self.smts]
        type_assert(self.expr, Ast)

    def __repr__(self):
        return f"{{ {'; '.join(map(repr, self.smts))}; {self.expr} }}"
    

class UnOp(Ast):
    op: str
    operand: Ast
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.operand = tokens[0][0]
        self.op = tokens[0][1]
        type_assert(self.op, str)
        type_assert(self.operand, Ast)
    
    def __repr__(self):
        return f"UnOp({repr(self.operand)}{self.op})"

    def __str__(self):
        return f"{self.operand}{self.op}"

class FuncCall(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.fn_expr = tokens[0]
        if len(tokens) > 1:
            self.args = tokens[1:]
        else:
            self.args = []
            
    def __repr__(self):
        return f"FuncCall({self.fn_expr}({self.args}))"

    def __str__(self):
        return f"{self.fn_expr}({self.args})"

    def compile(self, state, indent):
        fn_expr_body, fn_expr_ret = self.fn_expr.compile(state, indent)
        args_body, args_ret = zip(*[arg.compile(state, indent) for arg in self.args])
        bodies = list(filter(lambda x: x is not None, args_body + (fn_expr_body,)))
        if len(bodies) > 0:
            body = "\n".join(bodies)
        else:
            body = None

        return body, f"{fn_expr_ret}({', '.join(args_ret)})"

class FuncExpr(Ast):
    generic_defs: list[Ident]
    args: list[tuple[Ident, TypeIdent]]
    body: Ast | None
    ret_type: TypeIdent | None
    is_proc: bool
    is_forward: bool
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.is_proc = tokens[0] == "proc"
        self.generic_defs = list(tokens[1])
        self.args = [(x[0], x[1]) for x in tokens[2]]
        self.ret_type = tokens[3]
        self.body = tokens[4]
        if self.body is None:
            self.is_forward = True
        else:
            self.is_forward = False

        type_assert(self.generic_defs, list)
        [type_assert(g, Ident) for g in self.generic_defs]
        type_assert(self.args, list)
        [(type_assert(g, tuple), type_assert(g[0], Ident), type_assert(g[1], TypeIdent)) for g in self.args]
        type_assert(self.body, (Ast, type(None)))
        type_assert(self.ret_type, (TypeIdent, type(None)))

    def __repr__(self):
        if len(self.generic_defs) > 0:
            generics = "<" + ", ".join(map(str, self.generic_defs)) + ">"
        else:
            generics = ""

        return f"{'proc' if self.is_proc else 'func'}{generics}({', '.join(map(repr, self.args))}): {self.ret_type}, {self.body}"

class Definition(Ast):
    name: TypeIdent
    value: Ast
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.name = tokens[1]
        self.value = tokens[2]
        type_assert(self.name, TypeIdent)
        type_assert(self.value, Ast)

    def __repr__(self):
        return f"const {self.name} = {self.value};"

    def compile(self, state: CG, indent: int):
        state.add_global(self.name.c_name(), self.name)
        # if defining a function, do it properly
        if isinstance(self.value, FuncExpr):
            if self.value.is_forward:
                return None, None
            indent += 1
            name = self.name.c_name()
            if self.value.ret_type is None:
                ret_ty = Type(Primitive.VOID)
            else:
                ret_ty = self.value.ret_type.c_name()
            args = ", ".join(f"{ty.c_name()} {name.name}" for name, ty in self.value.args)
            for arg in self.value.args:
                state.check_valid_type(arg[1])
            body = ""
            if isinstance(self.value.body, BlockExpr):
                for s in self.value.body.smts:
                    s_body, s_ret = s.compile(state, indent)
                    if s_body is not None:
                        body += s_body
                    if s_ret is not None:
                        body += f"{' ' * 4 * indent}{s_ret};\n"
                extra_body, ret = self.value.body.expr.compile(state, indent)
                if extra_body is not None:
                    body += extra_body + ";\n"
            else:
                body, ret = self.value.body.compile(state, indent)
            return f"{ret_ty} {name}({args}) {{\n{body}{' ' * 4 * indent}return {ret};\n}}", None

# const add<T> = func<T>(a: T, b: T): T a + b;

ident = pp.Word(alphas + "_", alphanums + "_").set_parse_action(Ident)
namespaced_ident = pp.DelimitedList(ident, "::").set_parse_action(NamespacedIdent)
str_lit = (pp.Suppress('"') - pp.Word(pp.printables + " ", exclude_chars='"') - pp.Suppress('"')).set_parse_action(StrLit)
literal = str_lit | pp.pyparsing_common.number.set_parse_action(NumLit)

expr = pp.Forward()

type_ident = pp.Forward()
generic_list = pp.DelimitedList(type_ident, ",", allow_trailing_delim=True)
generic_def_list = pp.Group(pp.DelimitedList(ident, ",", allow_trailing_delim=True))
generic_ident = (ident - pp.Optional(pp.Suppress("<") - generic_list - pp.Suppress(">"))).set_parse_action(GenericIdent)
type_ident << (pp.Group(pp.ZeroOrMore("*")) - pp.Group(pp.DelimitedList(generic_ident, "::"))).set_parse_action(TypeIdent)
arg_def = pp.Group(ident - pp.Suppress(":") - type_ident)
arg_def_list = pp.Group(pp.DelimitedList(arg_def, ",", allow_trailing_delim=True))
arg_expr_list = pp.DelimitedList(expr, ',', allow_trailing_delim=True)

primary_expr = ident | literal | (pp.Suppress("(") + expr + pp.Suppress(")"))

postfix_expr = pp.Forward()
postfix_expr <<= (postfix_expr + pp.Suppress("(") + pp.Optional(arg_expr_list) + pp.Suppress(")")).set_parse_action(FuncCall)\
                 | primary_expr

math_expr = pp.infix_notation(postfix_expr,
    [
        (pp.oneOf("@ &"), 1, pp.opAssoc.RIGHT, UnOp),
        (pp.oneOf("* / %"), 2, pp.opAssoc.LEFT, BinOp),
        (pp.oneOf("+ -"), 2, pp.opAssoc.LEFT, BinOp),
        (pp.oneOf(">= <= == > < !="), 2, pp.opAssoc.LEFT, BinOp),
        (pp.oneOf("= += -= *= /="), 2, pp.opAssoc.LEFT, BinOp),
    ]
)

func_expr = ((pp.Keyword("func") | pp.Keyword("proc")) -\
    pp.Optional(pp.Suppress("<") - generic_def_list - pp.Suppress(">"), []) -\
    pp.Suppress("(") - pp.Optional(arg_def_list, []) - pp.Suppress(")") -\
    pp.Optional(pp.Suppress(":") - type_ident, None) -\
    pp.Optional(expr, None)).set_parse_action(FuncExpr)


statement = expr + pp.Suppress(";")
block_expr = (pp.Suppress("{") - pp.ZeroOrMore(statement) - pp.Optional(expr) - pp.Suppress("}")).set_parse_action(BlockExpr)
expr << (func_expr | block_expr | math_expr | ident | literal)

definition = (pp.Keyword("const") - type_ident - pp.Suppress("=") - expr - pp.Optional(pp.Suppress(";"))).set_parse_action(Definition)

program = pp.ZeroOrMore(definition)

if __name__ == "__main__":
    def p(parser, text):
        parser.parse_string(text, parse_all=True).pprint()
    
    # print(program.parse_string("const a = 1;", parse_all=True))
    # p(generic_ident, "test")
    # p(generic_ident, "test<T>")
    # p(generic_ident, "test<T, U, V>")
    # p(type_ident, "test")
    # p(type_ident, "test<T>")
    # p(type_ident, "test<T, U, V>")
    # p(type_ident, "name::space::test")
    # p(type_ident, "name::space::test<T>")
    # p(type_ident, "name::space::test<T, U, V>")
    # p(type_ident, "name<T>::space<T, U>::test")
    # p(arg_def, "a: b")
    # p(arg_def, "a: B::c<T>")
    # p(arg_def, "a: B::c<std::io::File>")
    # p(program, "const x = func() {}")
    # p(program, "const a::b = func(a: b) { 1; \"hello\"; 3.31; func() 2 };")
    # p(program, "const Vec<T>::new = func<T, U>(init_len: usize, allocator: std::alloc::Allocator<T>) { 1 }")
    p(expr, "1 + 1")

    with open("test.lime", "r") as f:
        source = f.read()
    parsed = program.parse_string(source)
    parsed.pprint()
    cg = CG()
    code = cg.compile(parsed)
    print(code)
    with open("out.c", "w") as f:
        f.write(code)
