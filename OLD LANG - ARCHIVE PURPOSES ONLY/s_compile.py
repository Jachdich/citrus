import sys
sys.argv.append("code.scs")

class Compiler:
    def __init__(self):
        self.OPCODE_DICT = {
                            "pass"         : 0,
                            "load_const"   : 1,
                            "load_value"   : 2,
                            "init_value"   : 3,
                            "store_value"  : 4,
                            "add_values"   : 5,
                            "sub_values"   : 6,
                            "mul_values"   : 7,
                            "div_values"   : 8,
                            "compare"      : 9,
                            "jump"         : 10,
                            "jump_if_false": 11,
                            "print_value"  : 12,
                            "input"        : 13,
                            "dupl"         : 14,
                            "reverse"      : 15,
                            "swap"         : 16,
                            "int"          : 17,
                            "str"          : 18,
                            "double"       : 19,
                            "float"        : 20,
                            }
    
    def s_compile(self):
        sc_code = []
        c_code  = []
        j_referance = {}
        for line in self.code.lower().split("\n"):
            opcode = line.split(" ")[0]
            operands = line.split(" ")[1:]
            #print("Opcode:", opcode + ", Operands:", operands)
            if not (line.startswith(".") and line[-1] == ":"):
                hex_opcode = self.OPCODE_DICT[opcode]
                sc_code.append(str(hex_opcode))
                for i in operands:
                    sc_code.append(str(i))
            else:
                sc_code.append(line)
        for line in sc_code:
            if line.startswith(".") and not line[-1] == ":":
                c_code.insert(-1, 1)
                c_code.insert(-1, line)
            else:
                c_code.append(line)
        self.c_code = c_code
        c_code = []
        for line_num, line in enumerate(self.c_code):
            if str(line)[0] == "." and str(line)[-1] == ":":
                j_referance[line.strip(":")] = line_num
            else:
                c_code.append(line)
        self.c_code = c_code
        for key in j_referance:
            #print(key)
            self.data.append(1)
            self.data.append(1)
            self.data.append(j_referance[key])
            self.c_code = "!!".join([str(i) for i in self.c_code])
            self.c_code = self.c_code.replace(str(key), str(len(self.data) - 3))
            self.c_code = self.c_code.split("!!")

    def loads(self, s, data):
        self.code = s
        self.data = data

    def outs(self):
        return self.c_code

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(" ".join([str(i) for i in self.c_code]))

    def open_f(self, filename):
        with open(filename, "r") as f:
            self.code = f.read()

if __name__ == "__main__":
    s = Compiler()
    s.loads("""load_const 1
load_const 3
compare
jump_if_false .test
load_value 7
print_value
.test:
pass""", [])
    s.s_compile()
