
from pyparsing import *

class IntLit:
    def __init__(self, tokens):
        self.val = int(tokens[0])
        
    def from_val(val):
        return IntLit([val])
    
    def __repr__(self):
        return f"{self.val}IL"
        
    def get_name(self):
        return "int_literal"

class Ident:
    def __init__(self, tokens):
        self.val = tokens[0]
    
    def __repr__(self):
        return f"Ident({self.val})"

class BinOp:
    def __init__(self, tokens):
        self.op = tokens[0][1]
        self.operands = tokens[0][::2]
    
    def __repr__(self):
        return "BinOp(" + f" {self.op} ".join(map(str, self.operands)) + ")"
        
    # TODO maybe bad
    def get_name(self):
        return "binexpr"



ident = Word(alphas + "_", alphanums + "_").set_parse_action(Ident)
type_ = ident
integer = Combine(Optional("-") + Word("0123456789"))
decimal = Combine(Optional("-") + Word("0123456789") + Literal(".") + Word("0123456789"))

number = decimal | integer.set_parse_action(IntLit)

OPAREN, CPAREN, COMMA, COLON, SEMI, EQ, OBRACE, CBRACE = map(Suppress, "(),:;={}")
addexpr = Forward()
mulexpr = Forward()
cmpexpr = Forward()
expr = Forward()
smt = Forward()
# term = (OPAREN + expr + CPAREN) | number | Group(ident).set_results_name("ident")
term = number | ident
compoundsmt = Group(OBRACE + ZeroOrMore(smt) + CBRACE).set_results_name("compoundsmt")
compoundexpr = Group(OBRACE + ZeroOrMore(smt) + expr + CBRACE).set_results_name("compoundexpr")


# mulexpr << (Group(term +    (Literal("*") | Literal("/") | Literal("%")) + expr).set_results_name("binexpr") | term)
# addexpr << (Group(mulexpr + (Literal("+") | Literal("-")) + expr).set_results_name("binexpr") | mulexpr)
# cmpexpr << (Group(addexpr + (Literal(">=") | Literal("<=") | Literal("==") | Literal(">") | Literal("<")) + expr).set_results_name("binexpr") | addexpr)
mathexpr = infix_notation(term,
    [
        (oneOf("* /"), 2, opAssoc.LEFT, BinOp),
        (oneOf("+ -"), 2, opAssoc.LEFT, BinOp),
        (oneOf(">= <= == > <"), 2, opAssoc.LEFT, BinOp),
    ]
)

funccall = Group(ident + OPAREN + ZeroOrMore(expr + COMMA) + Optional(expr) + CPAREN).set_results_name("funccall")

eqfunc       =  Group(EQ + expr + SEMI).set_results_name("compoundexpr")
compoundfunc =  compoundexpr | compoundsmt

funcdef = Group(Suppress("fn") + ident + OPAREN + 
          Group(Group(ZeroOrMore(ident + COLON + type_ + COMMA) + Optional(ident + COLON + type_)) + CPAREN +
          Optional(Suppress("->") + type_)) + (compoundfunc | eqfunc | SEMI)).set_results_name("funcdef")

expr << (funccall | mathexpr)

smt << (expr + Suppress(";"))
prog = ZeroOrMore(funcdef)

def parse(text):
    return prog.parse_string(text, parse_all=True)

