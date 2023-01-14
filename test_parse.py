from pyparsing import *

constant = Word("0123456789")
ident = Word(alphas)

expr = Forward()
primary = Group(constant | ident | Literal("(") + expr + Literal(")"))
postfix = Forward()
postfix <<= Group(primary | postfix + Literal("[") + expr + Literal("]"))
expr <<= ((primary + Literal("+") + primary) | postfix)

res = expr.parse_string("(1 + 1)[3]", parse_all=True)
print(res.as_list())