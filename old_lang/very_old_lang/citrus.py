#s_compile broken? jump does not receive address
#jif then straight to j

import sys
import re
import binascii

sys.argv.append("test.lime")
sys.argv.append("-o")
sys.argv.append("test.lasm")
sys.argv.append("-C")

def lex(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens

RESERVED = 'RESERVED'
INT      = 'int'
ID       = 'ID'
EOL      = 'EOL'

token_exprs = [
    (r'\n',                    "EOL"),
    (r'[ \n\t]+',              None),
    (r'#[^\n]*',               None),
    (r'==',                    "=="),
    (r',',                     ","),
    (r'\{',                    "{"),
    (r'\}',                    "}"),
    (r'\(',                    "("),
    (r'\)',                    ")"),
    (r';',                     RESERVED),
    (r'\+',                    RESERVED),
    (r'-',                     RESERVED),
    (r'\*',                    RESERVED),
    (r'/',                     RESERVED),
    (r'<=',                    RESERVED),
    (r'<',                     RESERVED),
    (r'>=',                    RESERVED),
    (r'>',                     RESERVED),
    (r'=',                     "assign"),
    (r'!=',                    RESERVED),
    (r'and',                   RESERVED),
    (r'or',                    RESERVED),
    (r'not',                   RESERVED),
    (r'if',                    "if"),
    (r'else',                  "else"),
    (r'while',                 "while"),
    (r'print',                 "print"),
    (r'def',                   "def"),
    (r'EOL',                   EOL),
    (r'var',                   "var"),
    (r'"(.*?)"',               "string"),
    (r"'(.*?)'",               "string"),
    (r'[0-9]+',                INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
]

def imp_lex(characters):
    return lex(characters, token_exprs)

global data
global label
global var_ref
global last_var
data = []
label = 0
var_ref = {}
last_var = 0

class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0]
        self.result = []

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos]
        #print(self.current_token)
        
    def eat(self, val):
        if self.current_token[1] == val:
            self.advance()
        else:
            raise SyntaxError("Wrong token! expected '{}' but got '{}'".format(val, self.current_token[1]))
    
    def parse(self):
        global label
        global data
        global var_ref
        global last_var
        self.tokens.append(("END", "END"))
        
        while self.pos < len(self.tokens) - 2 and (not self.current_token[0] == "END"):
            #print(self.current_token)
            if self.current_token[1] == "def":
                self.eat("def")
                name = self.current_token[0]
                self.eat("ID")
                self.eat("(")
                args = []
                while not self.current_token[1] == ")":
                    args.append(self.current_token[0])
                    self.eat("ID")
                    if not self.current_token[0] == ")":
                        self.eat(",")

                print(args)
                
            if self.current_token[1] == "ID":
                if self.current_token[0] in var_ref:
                    name = self.current_token[0]
                    self.eat("ID")
                    self.eat("assign")
                    value = self.current_token[0]
                    if self.current_token[1] == "string":
                        t = "string"
                        self.eat("string")
                    elif self.current_token[1] == "int":
                        t = "int"
                        self.eat("int")
                    self.result.append("LOAD_CONST {}".format(len(data)))
                    if t == "int":
                        data += [1, 1, int(value)]
                    else:
                        hexstr = binascii.hexlify(value[1:][:-1].encode("ascii"))
                        data.append(len(hexstr) / 2)
                        data.append(0)
                        bytesize = 2
                        data += [int(i, 16) for i in [hexstr[j:j+bytesize] for j in range(0, len(hexstr), bytesize)]]
                    self.result.append("STORE_VALUE {}".format(var_ref[name]))
                    self.eat("EOL")
                else:
                    raise SyntaxError("Variable '{}' was not initialised.".format(self.current_token[0]))
            if self.current_token[0] == "var":
                self.eat("var")
                name = self.current_token[0]
                self.eat("ID")
                self.eat("assign")
                value = self.current_token[0]
                if self.current_token[1] == "string":
                    t = "string"
                    self.eat("string")
                elif self.current_token[1] == "int":
                    t = "int"
                    self.eat("int")
                var_ref[name] = last_var
                last_var += 1
                self.result.append("LOAD_CONST {}".format(len(data)))
                if t == "int":
                    data += [1, 1, int(value)]
                else:
                    hexstr = binascii.hexlify(value[1:][:-1].encode("ascii"))
                    data.append(len(hexstr) / 2)
                    data.append(0)
                    bytesize = 2
                    data += [int(i, 16) for i in [hexstr[j:j+bytesize] for j in range(0, len(hexstr), bytesize)]]
                self.result.append("INIT_VALUE")
                self.eat("EOL")
                    
            if self.current_token[0] == "print":
                self.eat("print")
                raw_val = self.current_token[0]
                if self.current_token[1] == "ID":
                    self.eat("ID")
                    self.result.append("LOAD_VALUE {}".format(var_ref[raw_val]))
                else:
                    index = len(data)
                    if self.current_token[1] == "int":
                        self.eat("int")
                        data += [1, 1, int(raw_val)]
                    else:
                        self.eat("string")
                        hexstr = binascii.hexlify(raw_val[1:][:-1].encode("ascii"))
                        data.append(len(hexstr) / 2)
                        data.append(0)
                        bytesize = 2
                        data += [int(i, 16) for i in [hexstr[j:j+bytesize] for j in range(0, len(hexstr), bytesize)]]
                    self.result.append("LOAD_CONST {}".format(index))
                self.eat("EOL")
                self.result.append("PRINT_VALUE")
                
            if self.current_token[0] == "if":
                compare = False
                self.eat("if")
                while not self.current_token[1] == EOL and not self.current_token[1] == "{":
                    if self.current_token[1] == ID:
                        self.result.append("LOAD_VALUE {}".format(var_ref[self.current_token[0]]))
                        self.eat("ID")
                    if self.current_token[1] == INT:
                        value = int(self.current_token[0])
                        self.eat(INT)
                        index = len(data)
                        self.result.append("LOAD_CONST {}".format(str(index)))
                        data += [1, 1, value]
                    if self.current_token[0] == "==":
                        self.eat("==")
                        compare = True
                if compare:
                    self.result.append("COMPARE")
                    
                self.eat("{")
                self.eat("EOL")
                jump_label = label
                self.result.append("JUMP_IF_FALSE ." + str(label))
                label += 1
                to_compile = []
                opened = 1
                closed = 0
                
                while not opened == closed:
                    if self.current_token[0] == "{":
                        opened += 1
                    if self.current_token[0] == "}":
                        closed += 1
                    if opened == closed:
                        break
                    to_compile.append(self.current_token)
                    self.advance()
                    
                self.eat("}")
                code, d = Parser(to_compile).parse()
                self.result += code
                self.result.append("." + str(jump_label) + ":")
                if self.current_token[1] == "else":
                    self.eat("else")
                    self.eat("{")
                    self.eat("EOL")
                    to_compile = []
                    opened = 1
                    closed = 0
                    jumpto = label
                    label += 1
                    self.result.insert(-1, "JUMP .{}".format(jumpto))
                    
                    while not opened == closed:
                        if self.current_token[0] == "{":
                            opened += 1
                        if self.current_token[0] == "}":
                            closed += 1
                        if opened == closed:
                            break
                        to_compile.append(self.current_token)
                        self.advance()
                    self.eat("}")
                    code, d = Parser(to_compile).parse()
                    self.result += code
                    self.result.append("." + str(jumpto) + ":")
        return self.result, data
    def term(self, data):
        value = self.lexer.current_token.value
        self.eat("integer")

        result = []

        data.append(len(self.neatify(hex(int(value))[2:])) // 2)
        data.append(int(value))
        result.append("load_const {index}".format(index=str(len(data) - len(self.neatify(hex(value)[2:])))))

        while self.lexer.current_token.type in ("mul", "div"):
            
            if self.lexer.current_token.type == "mul":
                self.eat("mul")
                value = self.lexer.current_token.value
                self.eat("integer")
                data.append(len(self.neatify(hex(int(value))[2:])) // 2)
                data.append(int(value))
                result.append("load_const {index}".format(index=str(len(data) - len(self.neatify(hex(value)[2:])))))
                result.append("mul_values")
                
            elif self.lexer.current_token.type == "/":
                self.eat("/")
                value = self.lexer.current_token[0]
                self.eat("int")
                data.append(len(self.neatify(hex(int(value))[2:])) // 2)
                data.append(hex(int(value))[2:])
                result.append("load_const {index}".format(index=str(len(data) - len(self.neatify(hex(value)[2:])))))
                result.append("div_values")
                
        return self.result, data
    
    def expr(self):
        self.lexer.current_token = self.lexer.get_next_token()
        
        data, value = self.term([])

        result = []

        while self.current_token[0] in ("+", "-"):
            
            if self.lexer.current_token == "+":
                self.eat("+")
                value, data = self.term(data)
                for i in value:
                    result.append(i)
                result.append("add_values")
                
            elif self.lexer.current_token.type == "-":
                self.eat("-")
                value, data = self.term(data)
                for i in value:
                    result.append(i)
                result.append("sub_values")
                
        return result, data
    
def usage():
    print("Usage: {0} <filename> [args]".format(sys.argv[0]))
    print("                       -C        : Compile but don't assemble")
    print("                       -o <file> : Output file")
    sys.exit(1)

args = None
output_filename = None

if len(sys.argv) <= 1:
    usage()
else:
    input_filename = sys.argv[1]
    output_filename = input_filename.strip(".lime") + ".lbc" #LBC stands for Lime ByteCode
    if len(sys.argv) >  2:
        args = sys.argv[1:]
        for i, arg in enumerate(args):
            if arg == "-o":
                output_filename = args[i + 1]

with open(input_filename, "r") as f:
    characters = f.read()
print(characters)
tokens = imp_lex(characters)

p = Parser(tokens)
code, data = p.parse()

if args and "-C" in args:
    with open(output_filename, "w") as f:
        f.write("\n".join([str(i) for i in code]))
        f.write("\n" + str(len(data) + 1) + ", " + ", ".join([str(i) for i in data]))
else:
    from s_compile import Compiler
    c = Compiler()
    c.loads("\n".join([str(i) for i in code]), data)
    c.s_compile()
    code, data = [int(i) for i in c.c_code] + [0, 0], [int(i) for i in c.data] + [0, 0]

    with open(output_filename, "w") as f:
        f.write(str(len(code) - 1) + ", " + ", ".join([str(i) for i in code]))
        f.write("\n" + str(len(data) - 1) + ", " + ", ".join([str(i) for i in data]))
