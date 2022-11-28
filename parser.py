
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

class Ident:
    def __init__(self, tokens):
        self.val = tokens[0]
    
    def __repr__(self):
        return f"Ident({self.val})"
    def __str__(self):
        return self.val

class BinOp:
    def __init__(self, tokens):
        self.op = tokens[0][1]
        self.operands = tokens[0][::2]
    
    def __repr__(self):
        return "BinOp(" + f" {self.op} ".join(map(repr, self.operands)) + ")"
    def __str__(self):
        return f" {self.op} ".join(map(str, self.operands))

class ImportSmt:
    def __init__(self, tokens):
        self.fname = tokens[1]
    
    def __repr__(self):
        return f"Import({self.fname})"
    def __str__(self):
        return f'import "{self.fname}"'

class FnDef:
    def __init__(self, tokens):
        self.name = tokens[0].val
        # wtf is this
        self.args = list(zip(map(lambda i: getattr(i, "val"), tokens[1][0][::2]), map(lambda i: getattr(i, "val"), tokens[1][0][1::2]))) # (name, type) pairs
        self.ret_ty = tokens[1][1].val if len(tokens[1]) > 1 else None
        if len(tokens) == 3:
            self.forward_decl = False
            self.body = tokens[2]
        else:
            self.forward_decl = True
    
    def __repr__(self):
        return f"FnDef({self.name}({', '.join([str(a) + ': ' + str(b) for a, b in self.args])}) {self.body})"


class VarAssign:
    def __init__(self, tokens):
        self.lval = tokens[0].val
        self.rval = tokens[1]
    
    def __str__(self):
        return f"{self.lval} = {self.rval}"
    
    def __repr__(self):
        return f"VarAssign({self.lval} = {self.rval})"

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
            elif type(tokens[0]) == FnType:
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

class IfSmt:
    def __init__(self, tokens):
        self.condition = tokens[0]
        self.body = tokens[1]
        if len(tokens) == 3:
            self.else_body = tokens[2]
        else:
            self.else_body = None
        
    def __str__(self):
        return f"if {self.condition} {self.body} else {self.else_body}"
    
    def __repr__(self):
        return f"IfSmt({self.condition}, {self.body}" + (f", {self.else_body})" if self.else_body is not None else ")")

class WhileSmt:
    def __init__(self, tokens):
        self.condition = tokens[0]
        self.body = tokens[1]
    
    def __repr__(self):
        return f"WhileSmt({self.condition} {self.body})"

class IfExpr(IfSmt):
    def __init__(self, tokens):
        super().__init__(tokens)

class CompoundSmt:
    def __init__(self, tokens):
        self.smts = tokens
    
    def __repr__(self):
        return f"CompoundSmt({{{self.smts}}})"

class CompoundExpr:
    def __init__(self, tokens):
        self.smts = tokens[:-1]
        self.expr = tokens[-1]
    
    def __repr__(self):
        return f"CompoundExpr({{{self.smts + [self.expr,]}}})"

class FuncCall:
    def __init__(self, tokens):
        self.name = tokens[0].val
        if len(tokens) > 1:
            self.args = tokens[1:]
        else:
            self.args = []
            
    def __repr__(self):
        return f"FuncCall({self.name}({self.args}))"

class FnType:
    def __init__(self, tokens):
        self.args = list(zip(map(lambda i: getattr(i, "val"), tokens[0][::2]), map(lambda i: getattr(i, "val"), tokens[0][1::2]))) # (name, type) pairs
        if len(tokens) > 1:
            self.ty = tokens[1]
        else:
            self.ty = None
            
    def __repr__(self):
        return f"fn({', '.join([n + ': ' + t for n, t in self.args])})" + (("-> " + self.ty.val) if self.ty is not None else "")

comment = Literal("//") + restOfLine

OPAREN, CPAREN, COMMA, COLON, SEMI, EQ, OBRACE, CBRACE = map(Suppress, "(),:;={}")
ident = Word(alphas + "_", alphanums + "_").set_parse_action(Ident)
integer = Combine(Optional("-") + Word("0123456789"))
decimal = Combine(Optional("-") + Word("0123456789") + Literal(".") + Word("0123456789"))

number = decimal | integer.set_parse_action(IntLit)

addexpr = Forward()
mulexpr = Forward()
cmpexpr = Forward()
expr = Forward()
smt = Forward()
type_ = Forward()

arg_list = Group(ZeroOrMore(ident + COLON + type_ + COMMA) + Optional(ident + COLON + type_))
type_ << ((Suppress("fn") + OPAREN + arg_list + CPAREN + Optional(Suppress("->") + type_)).set_parse_action(FnType) | ident)

# term = (OPAREN + expr + CPAREN) | number | Group(ident).set_results_name("ident")
term = number | ident
compoundsmt = (OBRACE + ZeroOrMore(smt) + CBRACE).set_parse_action(CompoundSmt)
compoundexpr = (OBRACE + ZeroOrMore(smt) + expr + CBRACE).set_parse_action(CompoundExpr)

importsmt = (Literal("import") + QuotedString(quoteChar='"')).set_parse_action(ImportSmt)

# mulexpr << (Group(term +    (Literal("*") | Literal("/") | Literal("%")) + expr).set_results_name("binexpr") | term)
# addexpr << (Group(mulexpr + (Literal("+") | Literal("-")) + expr).set_results_name("binexpr") | mulexpr)
# cmpexpr << (Group(addexpr + (Literal(">=") | Literal("<=") | Literal("==") | Literal(">") | Literal("<")) + expr).set_results_name("binexpr") | addexpr)
mathexpr = infix_notation(term,
    [
        (oneOf("* / %"), 2, opAssoc.LEFT, BinOp),
        (oneOf("+ -"), 2, opAssoc.LEFT, BinOp),
        (oneOf(">= <= == > < !="), 2, opAssoc.LEFT, BinOp),
        (oneOf("= += -= *= /="), 2, opAssoc.LEFT, BinOp),
    ]
)

funccall = (ident + OPAREN + ZeroOrMore(expr + COMMA) + Optional(expr) + CPAREN).set_parse_action(FuncCall)

eqfunc       =  (EQ + expr + SEMI).set_parse_action(CompoundExpr)
compoundfunc =  compoundexpr | compoundsmt

funcdef = (ident + Suppress(":") + Suppress("fn") + OPAREN + 
          Group(arg_list + CPAREN + Optional(Suppress("->") + type_)) +
          (compoundfunc | eqfunc | SEMI)).set_parse_action(FnDef)


vardef = Group(Suppress("let") + ident + Optional(COLON + type_) + Optional(EQ + expr) + SEMI).set_parse_action(VarDef)

whilesmt = (Suppress("while") + expr + compoundsmt).set_parse_action(WhileSmt)

ifsmt  = (Suppress("if") + expr + compoundsmt + Optional(Suppress("else") + compoundsmt)).set_parse_action(IfSmt)
ifexpr = (Suppress("if") + expr + compoundexpr + Suppress("else") + compoundexpr).set_parse_action(IfExpr)
expr << (ifexpr | funccall | mathexpr)

smt << (whilesmt | vardef | ifsmt | (expr + Suppress(";")))
prog = ZeroOrMore(importsmt | funcdef)
prog.ignore(comment)

def parse(text):
    try:
        return prog.parse_string(text, parse_all=True)
    except ParseException as err:
        print(err.explain())
        exit(1)

