EOF, PLUS, INTEGER, MINUS = "EOF", "PLUS", "INTEGER", "MINUS"

class Token:
    def __init__(self, t_type, value):
        self.value = value
        self.type = t_type

    def __str__(self):
        return "Token({type}, {value})".format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()

class Compiler(object):
    def __init__(self, text):
        # client string input, e.g. "3 + 5", "12 - 5", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]
        self.data = []

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def neatify(self, not_so_neat):
        if len(not_so_neat) == 1:
            neat = "0" + not_so_neat
        elif len(not_so_neat) == 0:
            neat = "00"
        else:
            neat = not_so_neat
        return neat

    def expr(self):
        """Parser / Interpreter

        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        """
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be an integer
        left = self.current_token
        self.eat(INTEGER)

        # we expect the current token to be either a '+' or '-'
        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        # we expect the current token to be an integer
        right = self.current_token
        self.eat(INTEGER)
    
        bytecode = []
        if op.type == PLUS:
            self.data.append("01")
            self.data.append(self.neatify(str(left.value)))
            bytecode.append("load_const {index}".format(index = len(self.data) - 2))
            self.data.append("01")
            self.data.append(self.neatify(str(right.value)))
            bytecode.append("load_const {index}".format(index = len(self.data) - 2))
            bytecode.append("add_values")
        else:
            self.data.append("01")
            self.data.append(self.neatify(str(left.value)))
            bytecode.append("load_const {index}".format(index = len(self.data) - 2))
            self.data.append("01")
            self.data.append(self.neatify(str(right.value)))
            bytecode.append("load_const {index}".format(index = len(self.data) - 2))
            bytecode.append("sub_values")
        return bytecode, self.data

            

code = "8+2"
import s_compile, run
c = Compiler(code)
c_h = s_compile.Compiler()
output = c.expr()
c_h.s_compile("\n".join(output[0]))
print "".join(c_h.c_code)
print c.data
i = run.Interpreter("".join(c_h.c_code), "".join([str(i) for i in output[1]]))
i.execute()
print i.stack
