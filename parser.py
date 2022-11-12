
from pyparsing import *
from string import printable

class IntLit:
    def __init__(self, tokens):
        self.val = int(tokens[0])
        
    def from_val(val):
        return IntLit([val])
    
    def __repr__(self):
        return f"{self.val}IL"
    def __str__(self):
        return str(self.val)
        
    def get_name(self):
        return "int_literal"

class Ident:
    def __init__(self, tokens):
        self.val = tokens[0]
    
    def __repr__(self):
        return f"Ident({self.val})"
    def __str__(self):
        return self.val
    
    def get_name(self):
        return "ident"

class BinOp:
    def __init__(self, tokens):
        self.op = tokens[0][1]
        self.operands = tokens[0][::2]
    
    def __repr__(self):
        return "BinOp(" + f" {self.op} ".join(map(repr, self.operands)) + ")"
    def __str__(self):
        return f" {self.op} ".join(map(str, self.operands))
        
    # TODO maybe bad
    def get_name(self):
        return "binexpr"

class ImportSmt:
    def __init__(self, tokens):
        self.fname = tokens[1]
    
    def __repr__(self):
        return f"Import({self.fname})"
    def __str__(self):
        return f'import "{self.fname}"'

    def get_name(self):
        return "import"

class FnDef:
    def __init__(self, tokens):
        self.name = tokens[0][0].val
        self.args = zip(tokens[0][1][0][::2], tokens[0][1][0][1::2]) # (name, type) pairs
        self.ret_ty = tokens[0][1][1].val if len(tokens[0][1]) > 1 else None
        if len(tokens[0]) == 3:
            self.forward_decl = False
            self.body = tokens[0][2]
        else:
            self.forward_decl = True
    
    def __repr__(self):
        return f"FnDef({self.name}({', '.join([str(a) + ': ' + str(b) for a, b in self.args])}) {{{self.body}}})"
    
    def get_name(self):
        return "funcdef"

class VarAssign:
    def __init__(self, tokens):
        self.lval = tokens[0].val
        self.rval = tokens[1]
    
    def __str__(self):
        return f"{self.lval} = {self.rval}"
    
    def __repr__(self):
        return f"VarAssign({self.lval} = {self.rval})"
    
    def get_name(self):
        return "varassign"

class VarDef:
    def __init__(self, tokens):
        tokens = tokens[0]
        self.name = tokens[0].val
        tokens.pop(0)
        
        self.ty = None
        self.val = None
        
        while len(tokens) > 0:
            if type(tokens[0]) == Ident:
                self.ty = tokens[0].val
            else:
                self.val = tokens[0]
                
            tokens.pop(0)
        
    def __str__(self):
        return f"let {self.name}: {self.ty} = {self.val};"
    
    def __repr__(self):
        return f"VarDef({self.name}" + \
               (f": {self.ty}" if self.ty is not None else "") + \
               (f" = {repr(self.val)}" if self.val is not None else "") + ")"
    
    def get_name(self):
        return "vardef"

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

importsmt = (Literal("import") + QuotedString(quoteChar='"')).set_parse_action(ImportSmt)

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
          Optional(Suppress("->") + type_)) + (compoundfunc | eqfunc | SEMI)).set_parse_action(FnDef)

vardef = Group(Suppress("let") + ident + Optional(COLON + ident) + Optional(EQ + expr) + SEMI).set_parse_action(VarDef)
varassign = (ident + EQ + expr).set_parse_action(VarAssign)

expr << (varassign | funccall | mathexpr)

smt << (vardef | (expr + Suppress(";")))
prog = ZeroOrMore(importsmt | funcdef)

def parse(text):
    return prog.parse_string(text, parse_all=True)

