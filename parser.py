import inspect
from pyparsing import *
from string import printable
from pprint import pprint
# ParserElement.enablePackrat()
ParserElement.enableLeftRecursion()

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
                

class IntLit(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.val = int(tokens[0])
        
    def from_val(val):
        return IntLit([val])
    
    def __repr__(self):
        return f"{self.val}IL"
    def __str__(self):
        return str(self.val)

class Ident(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.val = tokens[0]
    
    def __repr__(self):
        return f"Ident({self.val})"
    def __str__(self):
        return self.val

class BinOp(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        if len(tokens) > 1 and tokens[1] in ["[", ".", "::"]: # special case operators
            self.op = tokens[1]
            self.operands = [tokens[0], tokens[2]]
        else:
            self.op = tokens[0][1]
            self.operands = tokens[0][::2]
    
    def __repr__(self):
        return "BinOp(" + f" {self.op} ".join(map(repr, self.operands)) + ")"
    def __str__(self):
        return f" {self.op} ".join(map(str, self.operands))

class UnOp(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.operand = tokens[0][0]
        self.op = tokens[0][1]
    
    def __repr__(self):
        return f"UnOp({repr(self.operand)}{self.op})"

class ImportSmt(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.fname = tokens[1]
    
    def __repr__(self):
        return f"Import({self.fname})"
    def __str__(self):
        return f'import "{self.fname}"'

class FnDef(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        if len(tokens[0]) == 1:
            self.name = tokens[0][0].val
            self.assoc_struct = None
        else:
            self.name = tokens[0][2].val
            self.assoc_struct = Type(src, pos, None, name=tokens[0][0].val, num_ptr=0, template_args=tokens[0][1])
        
        self.template_args = tokens[2]
        
        self.args = list(zip([n.val for n in tokens[3][0][::2]], tokens[3][0][1::2])) # (name, type) pairs
        self.ret_ty = tokens[3][1] if len(tokens[3]) > 1 else None
        if len(tokens) == 5:
            self.forward_decl = False
            self.body = tokens[4]
        else:
            self.forward_decl = True
            self.body = None

    def __repr__(self):
        return f"FnDef({(self.assoc_struct.name + '::') if self.assoc_struct is not None else ''}{self.name}<{self.template_args}>({', '.join([str(a) + ': ' + str(b) for a, b in self.args])}) -> {self.ret_ty} = {self.body})"

    def get_mangled_name(self):
        if self.assoc_struct is not None:
            return self.assoc_struct.name + "_" + self.name
        return self.name

class VarAssign(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.lval = tokens[0].val
        self.rval = tokens[1]
    
    def __str__(self):
        return f"{self.lval} = {self.rval}"
    
    def __repr__(self):
        return f"VarAssign({self.lval} = {self.rval})"

class VarDef(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        tokens = tokens[0]
        self.name = tokens[0].val
        tokens.pop(0)
        
        self.ty = None
        self.val = None
        
        while len(tokens) > 0:
            if type(tokens[0]) == Type:
                self.ty = tokens[0]
            else:
                self.val = tokens[0]
                
            tokens.pop(0)
        
    def __str__(self):
        return f"let {self.name}: {self.ty} = {self.val};"
    
    def __repr__(self):
        return f"VarDef({self.name}" + \
               (f": {self.ty}" if self.ty is not None else "") + \
               (f" = {repr(self.val)}" if self.val is not None else "") + ")"

class IfSmt(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.condition = tokens[0]
        self.body = tokens[1]
        self.elifs = list(zip(tokens[2][::2], tokens[2][1::2])) # (expr, body) pairs
        if len(tokens) == 4:
            self.else_body = tokens[3]
        else:
            self.else_body = None
        
    def __str__(self):
        return f"if {self.condition} {self.body} {' '.join(['elif ' + str(t[0]) + ' ' + str(t[1]) for t in self.elifs])} else {self.else_body}"
    
    def __repr__(self):
        return f"IfSmt({self.condition}, {self.body}" +\
                (", " if len(self.elifs) > 0 else "") +\
                ", ".join(["Elif(" + repr(t[0]) + ", " + repr(t[1]) + ")" for t in self.elifs]) +\
                (f", {self.else_body})" if self.else_body is not None else ")")

class WhileSmt(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.condition = tokens[0]
        self.body = tokens[1]
    
    def __repr__(self):
        return f"WhileSmt({repr(self.condition)} {repr(self.body)})"

class IfExpr(IfSmt):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)

class CompoundSmt(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.smts = tokens
    
    def __repr__(self):
        return f"CompoundSmt({{{self.smts}}})"

class CompoundExpr(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.smts = tokens[:-1]
        self.expr = tokens[-1]
    
    def __repr__(self):
        return f"CompoundExpr({{{self.smts + [self.expr,]}}})"

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

class Type(Ast):
    def __init__(self, src, pos, tokens, *, name=None, num_ptr=None, template_args=None):
        super().__init__(src, pos, tokens)
        self.fn_ptr = False
        self.template_args = []
        if name is not None and num_ptr is not None:
            self.name = name
            self.num_ptr = num_ptr
            if template_args is not None:
                self.template_args = template_args
            return

        if type(tokens[0]) == str and tokens[0] == "*":
            self.name = "void"
            self.num_ptr = len(tokens)
        else:
            self.name = tokens[0].val
            if len(tokens) > 2:
                self.num_ptr = len([n for n in tokens[2:] if n == "*"])
            else:
                self.num_ptr = 0
            self.template_args = tokens[1]

    def __repr__(self):
        if self.fn_ptr:
            return f"fn({', '.join([n + ': ' + repr(t) for n, t in self.args])})" + (("-> " + self.ty.val) if self.ty is not None else "")
        else:
            return "Type(" + self.name + (("<" + ", ".join(map(repr, self.template_args)) + ">") if len(self.template_args) > 0 else "")  + "*" * self.num_ptr + ")"
    
    def __str__(self):
        return self.name + (("<" + ", ".join(map(repr, self.template_args)) + ">") if len(self.template_args) > 0 else "")  + "*" * self.num_ptr
    
    def __eq__(self, other):
        if self.fn_ptr:
            return self.args == other.args and self.ty == other.ty
        else:
            return self.name == other.name and self.num_ptr == other.num_ptr
    
    def __hash__(self):
        if self.fn_ptr:
            return hash(self.args) ^ hash(self.ty)
        else:
            return hash(self.name) ^ hash(self.num_ptr)

    def get_mangled_name(self):
        templates = ""
        if len(self.template_args) > 0:
            templates = "_" + "_".join([n.get_mangled_name() for n in self.template_args])
        return self.name + templates

class StructDef(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.name = tokens[0].val
        self.template_args = tokens[1]
        self.members = list(zip([n.val for n in tokens[2:][::2]], tokens[2:][1::2]))
    
    def __repr__(self):
        return f"Struct({self.name} {{{', '.join([n + ': ' + repr(t) for n, t in self.members])}}})"

class StructInit(Ast):
    def __init__(self, src, pos, tokens):
        super().__init__(src, pos, tokens)
        self.struct_name = tokens[0].val
        self.init_args = list(zip([n.val for n in tokens[2:][::2]], tokens[2:][1::2]))

    def __repr__(self):
        return f"StructInit({self.struct_name} {{{', '.join([str(n) + ': ' + repr(t) for n, t in self.init_args])}}})"

comment = Literal("//") + restOfLine

OPAREN, CPAREN, COMMA, COLON, SEMI, EQ, OBRACE, CBRACE = map(Suppress, "(),:;={}")
ident = Word(alphas + "_", alphanums + "_").set_parse_action(Ident)
integer = Combine(Optional("-") + Word("0123456789")).set_parse_action(IntLit)
decimal = Combine(Optional("-") + Word("0123456789") + Literal(".") + Word("0123456789"))

expr = Forward()
smt = Forward()
type_ = Forward()

# arg_expr_list = delimitedList(expr, delim=",")

# primary = ident | number | OPAREN + expr + CPAREN
# postfix = primary\
#           | postfix + OPAREN + CPAREN\
#           | postfix + OPAREN + arg_expr_list + CPAREN\
#           | postfix + Literal("*")\
#           | postfix + Literal("&")

# mul_expr <<= postfix | mul_expr + Literal("*") + postfix | mul_expr

# template_list = Group(Suppress("<") + delimitedList(ident) + Suppress(">"))
# arg_def_list = Group(ZeroOrMore(ident + COLON + type_ + COMMA) + Optional(ident + COLON + type_))
# type_ << ((ident + Optional(template_list, []) + ZeroOrMore("*")) |
#           OneOrMore("*")).set_parse_action(Type)

# # term = (OPAREN + expr + CPAREN) | number | Group(ident).set_results_name("ident")
# term = number | ident
compoundsmt = (OBRACE + ZeroOrMore(smt) + CBRACE).set_parse_action(CompoundSmt)
compoundexpr = (OBRACE + ZeroOrMore(smt) + expr + CBRACE).set_parse_action(CompoundExpr)

importsmt = (Literal("import") + QuotedString(quoteChar='"')).set_parse_action(ImportSmt)

# subscript = (expr + Suppress("[") + expr + Suppress("]"))
# ifexpr = (Suppress("if") + expr + compoundexpr + Suppress("else") + compoundexpr).set_parse_action(IfExpr)
# funccall = (ident + ZeroOrMore(Literal("::") | Literal(".") + ident)) + OPAREN + ZeroOrMore(expr + Suppress(",")) + CPAREN
# nonmathexpr = (subscript | ifexpr | funccall | structinit | term | ident)

eqfunc       =  (EQ + expr + SEMI).set_parse_action(CompoundExpr)
compoundfunc =  Optional(EQ) + (compoundexpr | compoundsmt) + Optional(SEMI)

# funcdef = (Group(ident + Optional(Suppress("::") + ident)) + Suppress(":") + (Literal("fn") | Literal("proc")) +
#           Optional(template_list, []) +
#           Group(Optional(OPAREN + arg_def_list + CPAREN, []) + Optional(Suppress("->") + type_)) +
#           (compoundfunc | eqfunc | SEMI)).set_parse_action(FnDef)


vardef = Group(Suppress("let") + ident + Optional(COLON + type_) + Optional(EQ + expr) + SEMI).set_parse_action(VarDef)

while_smt = (Suppress("while") + expr + compoundsmt).set_parse_action(WhileSmt)

# ifsmt  = (Suppress("if") + expr + compoundsmt + Optional(Suppress("else") + compoundsmt)).set_parse_action(IfSmt)
# expr << (compoundexpr | mathexpr | nonmathexpr)

def parse(text):
    try:
        return prog.parse_string(text, parse_all=True)
    except ParseException as err:
        print(err.explain())
        exit(1)

constant = decimal | integer

arg_expr_list = Forward()
arg_expr_list <<= expr ^ (arg_expr_list + COMMA + expr)

primary_expr = ident | constant | (OPAREN + expr + CPAREN)

postfix_expr = Forward()
postfix_expr  <<= (postfix_expr + OPAREN + Optional(arg_expr_list) + CPAREN).set_parse_action(FuncCall)\
                | (postfix_expr + Literal("[") + expr + Suppress("]")).set_parse_action(BinOp)\
                | (postfix_expr + Literal(".") + ident).set_parse_action(BinOp)\
                | (type_ + Literal("::") + ident).set_parse_action(BinOp)\
                | primary_expr

if_expr = Forward()
if_expr <<= (Suppress("if") + expr + compoundexpr + Group(ZeroOrMore(Suppress("elif") + expr + compoundexpr)) + Suppress("else") + compoundexpr).set_parse_action(IfExpr) | postfix_expr
if_smt = (Suppress("if") + expr + compoundsmt + Group(ZeroOrMore(Suppress("elif") + expr + compoundsmt)) + Optional(Suppress("else") + compoundsmt)).set_parse_action(IfSmt)


mathexpr = infix_notation(if_expr,
    [
        # (oneOf(". ::"), 2, opAssoc.LEFT, BinOp),
        (oneOf("@ &"), 1, opAssoc.RIGHT, UnOp),
        (oneOf("* / %"), 2, opAssoc.LEFT, BinOp),
        (oneOf("+ -"), 2, opAssoc.LEFT, BinOp),
        (oneOf(">= <= == > < !="), 2, opAssoc.LEFT, BinOp),
        (oneOf("= += -= *= /="), 2, opAssoc.LEFT, BinOp),
    ]
)

# smt << (whilesmt | vardef | ifsmt | (expr + Suppress(";")))
smt <<= vardef | while_smt | if_smt | expr + SEMI

template_list = Group(Suppress("<") + delimitedList(type_, delim=",") + Suppress(">"))
arg_def_list = Group(ZeroOrMore(ident + COLON + type_ + COMMA) + Optional(ident + COLON + type_))
type_ << ((ident + Optional(template_list, []) + ZeroOrMore("*")) |
          OneOrMore("*")).set_parse_action(Type)

funcdef = (Group(
                ((ident + Optional(template_list, [])) + Suppress("::") + ident) | ident
            ) +
            Suppress(":") +
            (Literal("fn") | Literal("proc$") | Literal("proc") | Literal("func") | Literal("fun")) +
            Optional(template_list, []) +
            Group(Optional(OPAREN + arg_def_list + CPAREN, []) +
            Optional(Suppress("->") + type_)) +
            (compoundfunc | eqfunc | SEMI)
        ).set_parse_action(FnDef)

structdef = (ident + Suppress(":") + Suppress("struct") + 
            Optional(template_list, []) + OBRACE +
            ZeroOrMore(ident + Suppress(":") + type_ + SEMI) + CBRACE).set_parse_action(StructDef)


structinit = (ident + Optional(template_list) + OBRACE + delimitedList(ident + Suppress(":") + expr, ",") + CBRACE).set_parse_action(StructInit)
expr <<= (structinit | mathexpr)

prog = ZeroOrMore(importsmt | funcdef | structdef)
prog.ignore(comment)

# TODO this is the anonymous protocol grammar
# arg_type_list = type_ + ZeroOrMore(COMMA + type_) + Optional(COMMA)
# proto_element = Group(ident + COLON + ((Suppress("fn") + OPAREN + arg_type_list + CPAREN + Optional(Suppress("->") + type_)) | type_))
# anon_proto = ident + Suppress("with") + OPAREN + proto_element + ZeroOrMore(COMMA + proto_element) + Optional(COMMA)

# print(arg_type_list.parse_string("Self*, i32"))
# print(proto_element.parse_string("a: fn(Self*, i32) -> i32"))
# print(anon_proto.parse_string("T with (a: fn(Self*, i32), c: U)"))

if __name__ == "__main__":
    def p(t, v=prog):
        print(v.parse_string(t, parseAll=True))

    p("hello(a, 3)", expr)
    p("69 * 4", expr)
    p("@asdf + 3 + &c", expr)
    p("1 == 2", expr)
    p("if 3 { 1 } else { 2 }", expr)

    print(smt.parse_string("1==2;"))
    print(prog.parse_string("String::parse: fn<T,U>(a: f64, b: T) -> U = { 1 == 2; if a == 3 { 1 } else { 2 } }", parseAll=True))
    print(compoundexpr.parse_string("{ 1 == 2; if b == 2 { 3 == 4; } if a == 3 { 1 } elif a == 4 { 2 } else { 3 } }", parseAll=True))

    print(expr.parse_string("vec[16]", parseAll=True))
    print(smt.parse_string("let a = 4;", parseAll=True))


    p("let seg = malloc(seg_len);", smt)
    p("make_seg: func(data: char*, seg_len: u32) -> Slice<char> {}")
    p("while pos < self.length { 1; }", smt)
    p("Vec<Slice<char>>::new", expr)
    p("Vec<T>::new: fn<T>() = 0;")
    p("Vec<T> { a: 1, b: 2 }", expr)
    p("Vec<T>::__drop__: proc$<T>(self: Vec<T>*) = {}")