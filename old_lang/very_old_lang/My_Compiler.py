"""
--Oct 4 2018--
Line count: 340
Finally! Multidigit expressions!
54+46 is valid;
so is 14+9-1002!
Next up: BODMAS

nah cant be bothered. Winging another one in a different style
"""

class Unary(object):
    pass

class Token(object):
    def __init__(self, _type, value):
        self.type  = _type
        self.value = value

    def __str__(self):
        return "Token('{t}', '{value}')".format(t=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos]
        self.current_token = None

    def advance(self):
        if not self.pos >= len(self.text) - 1:
            self.pos += 1
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.skip_whitespace()
                
            elif self.current_char.isdigit():
                result = self.integer()
                return Token("integer", result)
            
            elif self.current_char == "+":
                self.advance()
                return Token("plus", "+")
            
            elif self.current_char == "-":
                self.advance()
                return Token("minus", "-")
            
            elif self.current_char == "/":
                self.advance()
                return Token("div", "/")
            
            elif self.current_char == "*":
                self.advance()
                return Token("mul", "*")
        return Token("EOF", None)

class Compiler(object):
    """c = Compiler(Lexer("5+10"))
       c.expr() ->  sheep20 -> Glow"""
    def __init__(self, lexer):
        self.lexer = lexer

    def neatify(self, not_so_neat):
        not_so_neat = str(not_so_neat)
        if len(not_so_neat) % 2 == 1:
            neat = "0" + not_so_neat
        else:
            neat = not_so_neat
        return neat

    def eat(self, _type):
        if self.lexer.current_token.type == _type:
            self.lexer.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError("'{_type}' is invalid at this time".format(_type=self.lexer.current_token.type))

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
                
            elif self.lexer.current_token.type == "div":
                self.eat("div")
                value = self.lexer.current_token.value
                self.eat("integer")
                data.append(len(self.neatify(hex(int(value))[2:])) // 2)
                data.append(hex(int(value))[2:])
                result.append("load_const {index}".format(index=str(len(data) - len(self.neatify(hex(value)[2:])))))
                result.append("div_values")
                
        return result, data
    
    def expr(self):
        self.lexer.current_token = self.lexer.get_next_token()
        
        data, value = self.term([])

        result = []

        while self.lexer.current_token.type in ("plus", "minus"):
            
            if self.lexer.current_token.type == "plus":
                self.eat("plus")
                value, data = self.term(data)
                for i in value:
                    result.append(i)
                result.append("add_values")
                
            elif self.lexer.current_token.type == "minus":
                self.eat("minus")
                value, data = self.term(data)
                for i in value:
                    result.append(i)
                result.append("sub_values")

        data = [self.neatify(i) for i in data[0:]]
                
        return result, data

code = "1+2 - 10 / 2"
import s_compile, run
l = Lexer(code)
c = Compiler(l)
c_h = s_compile.Compiler()
code = c.expr()
data = code[1]
code = code[0]
print(code)

"""
#print(output)
c_h.s_compile("\n".join(code))
print("".join(c_h.c_code))
print("".join(data))
i = run.Interpreter("".join(c_h.c_code), "".join([str(i) for i in data]))
i.execute()
print(i.stack)
"""
