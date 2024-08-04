import pyparsing as pp
from pyparsing import alphas, alphanums
pp.ParserElement.enableLeftRecursion()

class Ast:
    def __init__(self, src, pos, tokens):
        self.src = src
        self.pos = pos
        self.lineno = -1
        self.column = -1
        total = 0
        for i, line in enumerate(src.split("\n")):
            if total + len(line) + 1 >= pos:
                self.lineno = i + 1
                self.column = pos - total
            total += len(line) + 1

    def get_context(self):
        s = "\n".join(self.src.split("\n")[self.lineno-3:self.lineno]) + "\n"
        s += " " * (self.column) + "^ " + str(self.lineno) + ":" + str(self.column)
        return "\n" + s + "\n"
                
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

class Ident(Ast):
    name: str
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.name = tokens[0]
        type_assert(self.name, str)

    def __repr__(self):
        return f"Ident({self.name})"

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
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.vals = tokens
        [type_assert(g, GenericIdent) for g in self.vals]
        assert len(self.vals) > 0

    def __repr__(self):
        return f"TypeIdent({', '.join(map(repr, self.vals))})"

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

class FuncExpr(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        

ident = pp.Word(alphas + "_", alphanums + "_").set_parse_action(Ident)
namespaced_ident = pp.DelimitedList(ident, "::").set_parse_action(NamespacedIdent)
str_lit = (pp.Suppress('"') - pp.Word(pp.printables + " ", exclude_chars='"') - pp.Suppress('"')).set_parse_action(StrLit)
literal = str_lit | pp.pyparsing_common.number.set_parse_action(NumLit)

type_ident = pp.Forward()
generic_list = pp.DelimitedList(type_ident, ",", allow_trailing_delim=True)
generic_def_list = pp.Group(pp.DelimitedList(ident, ",", allow_trailing_delim=True))
generic_ident = (ident - pp.Optional(pp.Suppress("<") - generic_list - pp.Suppress(">"))).set_parse_action(GenericIdent)
type_ident << pp.DelimitedList(generic_ident, "::").set_parse_action(TypeIdent)
arg_def = (ident - pp.Suppress(":") - type_ident)
arg_def_list = pp.Group(pp.DelimitedList(arg_def, ",", allow_trailing_delim=True))

expr = pp.Forward()

math_expr = pp.infix_notation(expr,
    [
        (pp.oneOf("@ &"), 1, pp.opAssoc.RIGHT, UnOp),
        (pp.oneOf("* / %"), 2, pp.opAssoc.LEFT, BinOp),
        (pp.oneOf("+ -"), 2, pp.opAssoc.LEFT, BinOp),
        (pp.oneOf(">= <= == > < !="), 2, pp.opAssoc.LEFT, BinOp),
        (pp.oneOf("= += -= *= /="), 2, pp.opAssoc.LEFT, BinOp),
    ]
)

func_expr = ((pp.Keyword("func") | pp.Keyword("proc")) -\
    pp.Optional(pp.Suppress("<") - generic_def_list - pp.Suppress(">")) -\
    pp.Suppress("(") - pp.Optional(arg_def_list, []) - pp.Suppress(")") -\
    expr)#.set_parse_action(FuncExpr)


statement = expr + pp.Suppress(";")
block_expr = pp.Suppress("{") - pp.ZeroOrMore(statement) - pp.Optional(expr) - pp.Suppress("}")
expr << (func_expr | block_expr | math_expr | ident | literal)

definition = pp.Keyword("const") - type_ident - pp.Suppress("=") - expr - pp.Optional(pp.Suppress(";"))

program = pp.ZeroOrMore(definition)

class CG:
    def __init__(self):
        self.globals = {}
    def compile(self, parsed: list[Ast]):
        pass
        # for smt in parsed:
            

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
    p(program, "const Vec<T>::new = func<T, U>(init_len: usize, allocator: std::alloc::Allocator<T>) { 1 }")

    parsed = program.parse_string("const main = func() 0;")
    cg = CG()
    print(cg.compile(parsed))

