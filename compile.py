from pyparsing import *
import os

ident = Word(alphas)
type_ = Literal("i64")
integer = Combine(Optional("-") + Word("0123456789"))
decimal = Combine(Optional("-") + Word("0123456789") + Literal(".") + Word("0123456789"))
number = decimal | Group(integer).set_results_name("int_literal")

addexpr = Forward()
mulexpr = Forward()
expr = Forward()
term = (Suppress("(") + expr + Suppress(")")) | number | ident

mulexpr << (Group(term + (Literal("*") | Literal("/") | Literal("%")) + mulexpr).set_results_name("binexpr")| term)
addexpr << (Group(mulexpr + (Literal("+") | Literal("-")) + addexpr).set_results_name("binexpr") | mulexpr)

funccall = Group(ident + Suppress("(") + ZeroOrMore(expr + Suppress(",")) + Optional(expr) + Suppress(")")).set_results_name("funccall")
funcdef = Group(Suppress("fn") + ident + Suppress("(") + 
        Group(ZeroOrMore(ident + Suppress(":") + type_ + Suppress(",")) + Optional(ident + Suppress(":") + type_)) + Suppress(")") +
         Suppress("->") + type_ + Suppress("=") + expr + Suppress(";")).set_results_name("funcdef")
expr << (funccall | addexpr)

smt = (expr + Suppress(";")) | funcdef
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
# run_tests()


test_prog = """
fn add(a: i64, b: i64) -> i64 = a + b;
putd(add(1, 1));
"""

def parse(text):
    return prog.parse_string(text, parse_all=True)


class CG:
    def __init__(self):
        self.code = ".text\n.global main\n.type main, @function\nmain:\n"
        self.regs = ["%rax", "%rbx", "%rcx", "%rdx", "%rsi", "%rdi", "%r8", "%r9"]
        self.regs_used = [False] * len(self.regs)
        
    def regalloc(self, reg_wanted=None):
        if reg_wanted != None:
            idx = self.regs.index(reg_wanted)
            if self.regs_used[idx]:
                print("Debug: request reg " + reg_wanted + ", but used")
                return None
            self.regs_used[idx] = True
            return reg_wanted
        
        for i, reg in enumerate(self.regs_used):
            if not reg:
                self.regs_used[i] = True
                return self.regs[i]
        print("Debug: request reg, all used")
        return None
    
    def regfree(self, reg):
        idx = self.regs.index(reg)
        self.regs_used[idx] = False
        
    def alloc_arg_regs(self, num_args):
        args_order = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"]
        if len(args_order) < num_args:
            assert False, "stack args are not supported yet"
        
        stack_saved_regs = []
        free_regs = [] # to be freed later
        for i in range(num_args):
            # if we need a reg and it's used, push to stack
            if self.regs_used[self.regs.index(args_order[i])]:
                self.code += "pushq " + args_order[i] + "\n"
                self.regfree(args_order[i])
                stack_saved_regs.append(args_order[i])
            else:
                free_regs.append(args_order[i])
            assert self.regalloc(args_order[i]) != None, "Regalloc should give the register since it was just freed"
        
        return args_order[:num_args], stack_saved_regs, free_regs
        
    def funccall(self, ast):
        funcname = ast[0]
        num_args = len(ast) - 1
        regs, stack_saved_regs, free_regs = self.alloc_arg_regs(num_args)
        
        # make sure rax is available for return value
        saved_rax = False
        if self.regs_used[self.regs.index("%rax")]:
            self.code += "pushq %rax\n"
            self.regfree("%rax")
            saved_rax = True
        assert self.regalloc("%rax") != None, "Regalloc should give rax since it was just freed"
        
        for i, arg in enumerate(ast[1:]):
            reg = self.expr(arg)
            self.code += "movq " + reg + ", " + regs[i] + "\n"
            self.regfree(reg)
        
        self.code += "call " + str(funcname) + "\n"
        
        ret_reg = self.regalloc()
        self.code += "movq %rax, " + ret_reg + "\n"
        
        if saved_rax:
            self.code += "popq %rax\n"
        else:
            self.regfree("%rax")
        
        for reg in reversed(stack_saved_regs):
            self.code += "popq " + reg + "\n"
        
        for reg in free_regs:
            self.regfree(reg)
            
        return ret_reg
    
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
        elif ast.get_name() == "funccall":
            return self.funccall(ast)
        else:
            print("Not implemented: expression type " + ast.getName())
            exit(1)
    
    def funcdef(self, ast):
        pass

    def gen(self, ast):
        print(ast.dump())
        for smt in ast:
            if smt.get_name() == "funccall":
                reg = self.expr(smt)
                self.regfree(reg)
            elif smt.get_name() == "funcdef":
                self.funcdef(smt)
            else:
                print(f"Invalid syntax: Unexpected token '{smt[0]}'")
                exit(1)
        
        self.code += "ret\n"
        with open("test2.s", "w") as f:
            f.write(self.code)
        print(self.code)
    
a = CG()
a.gen(parse(test_prog))
