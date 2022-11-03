from pyparsing import *
import os

# expr = Forward()

integer = Combine(Optional("-") + Word("0123456789"))
decimal = Combine(Optional("-") + Word("0123456789") + Literal(".") + Word("0123456789"))
number = decimal | Group(integer).set_results_name("int_literal")

expr = Forward()
mulexpr = Forward()
term = (Suppress("(") + expr + Suppress(")")) | number

mulexpr << (Group(term + (Literal("*") | Literal("/") | Literal("%")) + mulexpr).set_results_name("binexpr")| term)
expr << (Group(mulexpr + (Literal("+") | Literal("-")) + expr).set_results_name("binexpr")| mulexpr)

print_smt = Literal("print") + expr + Suppress(";")
smt = Group(print_smt | (expr + Suppress(";")))
prog = ZeroOrMore(smt)

def to_list(pr):
    if isinstance(pr, ParseResults):
        return [to_list(n) for n in pr]
    else:
        return pr

def test(inp, out):
    try:
        res = prog.parseString(inp, parseAll=True)
        res = to_list(res)
    except ParseException as e:
        res = str(e)

    if res == out:
        print("\x1b[92m✓\x1b[0m", inp, "=>", res)
    else:
        print("\x1b[91mx\x1b[0m", inp, "=>", res, "!=", out, "(expected)")


def run_tests():
    test("0;", ["0"])
    test("76139;", ["76139"])
    test("32.33;", ["32.33"])
    test("-341;", ["-341"])
    test("-32.133;", ["-32.133"])
    test("132 + 1.324;", [["132", "+", "1.324"]])
    test("1 + 2 + 3;", [["1", "+", ["2", "+", "3"]]])
    test("1 + 2 * 3;", [["1", "+", ["2", "*", "3"]]])
    test("(1 + 2) * 3;", [[["1", "+", "2"], "*", "3"]])
    test("1 * 2 + 3;", [[["1", "*", "2"], "+", "3"]])

    test("print 1 + 1;", ['print', ['1', '+', '1']]);
run_tests()


test_prog = """
print 1 + 1;
print 6 * 9;
"""

def parse(text):
    return prog.parse_string(text, parse_all=True)


class CG:
    def __init__(self):
        self.code = ".text\n.global main\n.type main, @function\nmain:"
        self.regs = ["%rax", "%rbx", "%rcx", "%rdx"]
        self.regs_used = [False, False, False, False]
        
    def regalloc(self):
        for i, reg in enumerate(self.regs_used):
            if not reg:
                self.regs_used[i] = True
                return self.regs[i]
    
        return None
        
    def regfree(self, reg):
        idx = self.regs.index(reg)
        self.regs_used[idx] = False
    
    def printsmt(self, ast):
        expr = ast[1]
        ret_reg = self.expr(expr)
        self.code += "movq " + ret_reg + ", %rdi\n"
        self.code += "call putd\n"
        self.regfree(ret_reg)
        
    def binexpr(self, ast):
        lhs = self.expr(ast[0])
        op = ast[1]
        rhs = self.expr(ast[2])
        if op == "+":
            self.code += "addq "
        elif op == "*":
            self.code += "imul "        
        self.code += lhs + ", " + rhs + "\n"
        
        self.regfree(lhs)
        return rhs
        
    def int_literal(self, ast):
        reg = self.regalloc()
        self.code += "movq $" + str(ast[0]) + ", " + reg + "\n"
        return reg
            
    def expr(self, ast):
        if ast.get_name() == "binexpr":
            return self.binexpr(ast)
        elif ast.get_name() == "int_literal":
            return self.int_literal(ast)
        else:
            print("Not implemented: expression type " + ast.getName())
            exit(1)
    def gen(self, ast):
        print(ast.__repr__())
        for smt in ast:
            if smt[0] == "print":
                self.printsmt(smt)
            else:
                print(f"Invalid syntax: Unexpected token '{smt[0]}'")
                exit(1)
        
        self.code += "ret\n"
        with open("test2.s", "w") as f:
            f.write(self.code)
        print(self.code)
    
a = CG()
a.gen(parse(test_prog))