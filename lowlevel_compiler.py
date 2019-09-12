def pad(string, length, char):
    return char * (length - len(string)) + string

class Compiler:
    def __init__(self, code):
        self.code = self.clean(code)

    def clean(self, code):
        return code

    def assemble(self):
        #pass 1
        out = ""
        for line in self.code.split("\n"):
            if line.startswith("\\") and not line == "\\\\":
                number = hex(int(line.strip("\\")))[2:]
                number = pad(number, 8, "0")
                a = number[:2]
                b = number[2:4]
                c = number[4:6]
                d = number[6:]
                print("NUMBER:", number, a, b, c, d)
                print("NOTHER DEBUG:", chr(int(d, 16)))
                out += chr(int(a, 16)) + "\n" + chr(int(b, 16)) + "\n" + chr(int(c, 16)) + "\n" + chr(int(d, 16)) + "\n"
            else:
                out += line + "\n"
        print(out)
        out2 = ""
        #pass 2 - sub labels for addresses
        addr_lookup = {}
        current_address = 0
        for line in out.split("\n"):
            print("'"+line+"'")
            if line == "":
                continue
            
            if line.endswith(":") and not line == ":":
                addr_lookup[line.strip(":")] = current_address
                
            if line.startswith("$") and not line == "$":
                current_address += 4
                
            elif not line.endswith(":") or line == ":":
                current_address += 1
        
        for line in out.split("\n"):
            if line.startswith("$") and not line == "$":
                number = hex(addr_lookup[line.strip("$")])[2:]
                number = pad(number, 8, "0")
                a = number[:2]
                b = number[2:4]
                c = number[4:6]
                d = number[6:]
                out2 += chr(int(a, 16)) + chr(int(b, 16)) + chr(int(c, 16)) + chr(int(d, 16))
            else:
                if not line.endswith(":") or line == ":":
                    out2 += line
                

        return out2

c = Compiler("""
start:
i
\\11
i
$start
j
""")

#print([ord(i) for i in c.assemble()])
with open("assembler.vm", "w") as f:                
    f.write(c.assemble())

for char in c.assemble():
    if ord(char) > 50:
        print(char)
    else:
        print("ORD:" + str(ord(char)))

