
from pyparsing import *
from string import printable
ParserElement.enablePackrat()
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

class UnOp:
    def __init__(self, tokens):
        self.operand = tokens[0][0]
        self.op = tokens[0][1]
    
    def __repr__(self):
        return f"UnOp({self.operand}{self.op})"

class ImportSmt:
    def __init__(self, tokens):
        self.fname = tokens[1]
    
    def __repr__(self):
        return f"Import({self.fname})"
    def __str__(self):
        return f'import "{self.fname}"'

class FnDef:
    def __init__(self, tokens):
        print(tokens)
        if len(tokens[0]) == 1:
            self.name = tokens[0][0].val
            self.assoc_struct = None
        else:
            self.name = tokens[0][1].val
            self.assoc_struct = tokens[0][0].val
        
        self.template_args = [i.val for i in tokens[1]]
        
        self.args = list(zip([n.val for n in tokens[2][0][::2]], tokens[2][0][1::2])) # (name, type) pairs
        self.ret_ty = tokens[2][1] if len(tokens[2]) > 1 else None
        if len(tokens) == 4:
            self.forward_decl = False
            self.body = tokens[3]
        else:
            self.forward_decl = True
            self.body = None
    
    def __getattribute__(self, val):
        """super hacky shit to basically get the right name, cos I'm lazy"""
        if val == "name":
            if self.assoc_struct is None:
                return super().__getattribute__("name")
            else:
                return self.assoc_struct + "_" + super().__getattribute__("name")
        else:
            return super().__getattribute__(val)

     
    def __repr__(self):
        return f"FnDef({self.name}<{self.template_args}>({', '.join([str(a) + ': ' + str(b) for a, b in self.args])}) = {self.body})"


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

class Type:
    def __init__(self, tokens):
        print("TYPE TOKENS", tokens)
        if tokens[0] == "fn":
            self.fn_ptr = True
            self.args = list(zip([n.val for n in tokens[1][::2]], tokens[1][1::2])) # (name, type) pairs
            if len(tokens) > 2:
                self.ty = tokens[2]
            else:
                self.ty = None
                
        else:
            self.fn_ptr = False
            if type(tokens[0]) == str and tokens[0] == "*":
                self.name = "void"
                self.num_ptr = len(tokens)
            else:
                self.name = tokens[0].val
                if len(tokens) > 1:
                    self.num_ptr = len([n for n in tokens[1:] if n == "*"])
                else:
                    self.num_ptr = 0

    def __repr__(self):
        if self.fn_ptr:
            return f"fn({', '.join([n + ': ' + repr(t) for n, t in self.args])})" + (("-> " + self.ty.val) if self.ty is not None else "")
        else:
            return "Type(" + self.name + "*" * self.num_ptr + ")"
    
    def __eq__(self, other):
        # TODO SUPER FUCKING HACKY! DO IT BETTER
        # HACK
        return self.name == other.name and self.num_ptr == other.num_ptr
    
    def __hash__(self):
        return hash(self.name) ^ hash(self.num_ptr)

class StructDef:
    def __init__(self, tokens):
        self.name = tokens[0].val
        self.template_args = tokens[1]
        self.members = list(zip([n.val for n in tokens[2:][::2]], tokens[2:][1::2]))
    
    def __repr__(self):
        return f"Struct({self.name} {{{', '.join([n + ': ' + repr(t) for n, t in self.members])}}})"

class StructInit:
    def __init__(self, tokens):
        self.struct_name = tokens[0].val
        self.init_args = list(zip([n.val for n in tokens[1:][::2]], tokens[1:][1::2]))

    def __repr__(self):
        return f"StructInit({self.struct_name} {{{', '.join([n + ': ' + repr(t) for n, t in self.init_args])}}})"
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

template_list = Group(Suppress("<") + delimitedList(ident) + Suppress(">"))
arg_list = Group(ZeroOrMore(ident + COLON + type_ + COMMA) + Optional(ident + COLON + type_))
type_ << ((Literal("fn") + OPAREN + arg_list + CPAREN + Optional(Suppress("->") + type_)) |
          (ident + Optional(template_list, []) + ZeroOrMore("*")) |
          Literal("*")).set_parse_action(Type)

# term = (OPAREN + expr + CPAREN) | number | Group(ident).set_results_name("ident")
term = number | ident
compoundsmt = (OBRACE + ZeroOrMore(smt) + CBRACE).set_parse_action(CompoundSmt)
compoundexpr = (OBRACE + ZeroOrMore(smt) + expr + CBRACE).set_parse_action(CompoundExpr)

importsmt = (Literal("import") + QuotedString(quoteChar='"')).set_parse_action(ImportSmt)

# mulexpr << (Group(term +    (Literal("*") | Literal("/") | Literal("%")) + expr).set_results_name("binexpr") | term)
# addexpr << (Group(mulexpr + (Literal("+") | Literal("-")) + expr).set_results_name("binexpr") | mulexpr)
# cmpexpr << (Group(addexpr + (Literal(">=") | Literal("<=") | Literal("==") | Literal(">") | Literal("<")) + expr).set_results_name("binexpr") | addexpr)

structinit = (ident + OBRACE + delimitedList(ident + Suppress(":") + expr, ",") + CBRACE).set_parse_action(StructInit)

funccall = (ident + OPAREN + ZeroOrMore(expr + COMMA) + Optional(expr) + CPAREN).set_parse_action(FuncCall)
ifexpr = (Suppress("if") + expr + compoundexpr + Suppress("else") + compoundexpr).set_parse_action(IfExpr)
nonmathexpr = (ifexpr | funccall | structinit | term | ident)
mathexpr = infix_notation(nonmathexpr,
    [
        (".", 2, opAssoc.LEFT, BinOp),
        (oneOf("* &"), 1, opAssoc.LEFT, UnOp),
        (oneOf("* / %"), 2, opAssoc.LEFT, BinOp),
        (oneOf("+ -"), 2, opAssoc.LEFT, BinOp),
        (oneOf(">= <= == > < !="), 2, opAssoc.LEFT, BinOp),
        (oneOf("= += -= *= /="), 2, opAssoc.LEFT, BinOp),
    ]
)

eqfunc       =  (EQ + expr + SEMI).set_parse_action(CompoundExpr)
compoundfunc =  EQ + (compoundexpr | compoundsmt) + Optional(SEMI)

funcdef = (Group(ident + Optional(Suppress("::") + ident)) + Suppress(":") + (Suppress("fn") | Suppress("proc")) +
          Optional(template_list, []) +
          OPAREN + Group(arg_list + CPAREN + Optional(Suppress("->") + type_)) +
          (compoundfunc | eqfunc | SEMI)).set_parse_action(FnDef)


structdef = (ident + Suppress(":") + Suppress("struct") + 
            Optional(template_list, []) + OBRACE +
            ZeroOrMore(ident + Suppress(":") + type_ + SEMI) + CBRACE).set_parse_action(StructDef)

vardef = Group(Suppress("let") + ident + Optional(COLON + type_) + Optional(EQ + expr) + SEMI).set_parse_action(VarDef)

whilesmt = (Suppress("while") + expr + compoundsmt).set_parse_action(WhileSmt)

ifsmt  = (Suppress("if") + expr + compoundsmt + Optional(Suppress("else") + compoundsmt)).set_parse_action(IfSmt)
expr << (compoundexpr | mathexpr | nonmathexpr)

smt << (whilesmt | vardef | ifsmt | (expr + Suppress(";")))
prog = ZeroOrMore(importsmt | funcdef | structdef)
prog.ignore(comment)

def parse(text):
    try:
        return prog.parse_string(text, parse_all=True)
    except ParseException as err:
        print(err.explain())
        exit(1)

