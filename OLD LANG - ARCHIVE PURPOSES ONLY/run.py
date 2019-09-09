import sys, re
sys.argv.append("code.hex")

class Interpreter:
    def __init__(self, code, data):
        #with open(sys.argv[1],"r") as f:
        #    code = f.read().strip(" ").replace(" ","")
        #self.code, self.data = code.split("ff")
        self.data = data
        self.code = code
        self.data = re.findall("..", self.data)
        self.var = []
        self.stack = []
        self.result = False
        self.EXEC_DICT = {
                          "00": ["pass",         0],
                          "01": ["load_const",   1],
                          "02": ["load_value",   1],
                          "03": ["store_value",  1],
                          "04": ["add_values",   0],
                          "05": ["sub_values",   0],
                          "06": ["div_values",   0],
                          "07": ["mul_values",   0],
                          "08": ["compare",      0],
                          "09": ["jump",         1],
                          "0A": ["jump_if_false",1],
                          "0B": ["print_value",  1],
                          }
        self.FUNC_DICT = {
            "pass":          self.noop,
            "load_const":    self.load_const,
            "load_value":    self.load_value,
            "store_value":   self.store_value,
            "add_values":    self.add_values,
            "sub_values":    self.sub_values,
            "div_values":    self.div_values,
            "mul_values":    self.mul_values,
            "compare":       self.compare,
            "jump":          self.jump,
            "jump_if_false": self.jump_false,
            "print_value":   self.print_value,
            }

    def noop(self, operands):
        pass
    
    def push(self, data):
        for item in data:
            self.stack.append(item)
        self.stack.append(len(data))
        
    def jump(self, operands):
        self.pc = int(operands[0], 16) * 2
        
    def pop(self):
        length = self.stack.pop()
        out = []
        for i in range(length):
            out.append(self.stack.pop())
        out.reverse()
        return [str(i) for i in out]
    
    def load_const(self, operands):
        length = int(self.data[int(operands[0], 16)], 16)
        data = []
        for i in range(length):
            data.append(self.data[int(operands[0], 16) + i + 1])
        out = [int("".join(data), 16)]
        self.push(out)
        
    def load_value(self, operands):
        length = int(self.var[int(operands[0], 16)], 16)
        data = []
        for i in range(length):
            data.append(self.var[int(operands[0], 16) + i + 1])
        data.reverse()
        out = [int(i, 16) for i in data]
        self.push(out)
    
    def store_value(self, opernads):
        for i, item in enumerate(self.pop()):
            self.var[operands[0] + i]
        self.stack.append(len(data))
    
    def add_values(self, operands):
        a = int("".join(self.pop()))
        b = int("".join(self.pop()))
        #print(a)
        #print(b)
        self.push([a + b])

    def sub_values(self, operands):
        a = int(self.pop()[0])
        b = int(self.pop()[0])
        self.push([b - a])

    def mul_values(self, operands):
        a = int(self.pop()[0])
        b = int(self.pop()[0])
        self.push([a * b])

    def div_values(self, operands):
        a = int(self.pop()[0])
        b = int(self.pop()[0])
        self.push([b / a])
        
    def print_value(self, operands):
        out = ""
        if operands[0] == "00":
            for item in self.pop():
                out += str(item)
            print(out)
        elif operands[0] == "01":
            for item in self.pop():
                out += chr(item)
            print(out)
            
    def compare(self, operands):
        a = self.pop()
        b = self.pop()
        if a == b:
            self.result = True
        else:
            self.result = False
            
    def jump_false(self, operands):
        #print self.pc
        if not self.result:
            self.jump(operands)
        else:
            self.pc += 2
        #print self.pc
            
    def execute(self):
        self.pc = 0
        while self.pc < len(self.code):
            number_of_operands = self.EXEC_DICT[self.code[self.pc:self.pc+2]][1]
            func = self.EXEC_DICT[self.code[self.pc:self.pc+2]][0]
            #printf
            operands = []
            for i in range(number_of_operands):
                self.pc += 2
                operands.append(self.code[self.pc:self.pc + 2])
            function = self.FUNC_DICT[func]
            function(operands)
            if not "jump" in func:
                self.pc += 2
            #print(self.stack)

#code = Interpreter("01000102040B", "0101020100")
#code.execute()
#print(code.stack)
