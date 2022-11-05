#define LNO (" " * (56 - len_of_last_line(self.code)) + "# " + str(getframeinfo(currentframe()).lineno) + "\t" + str([reg for i, reg in enumerate(self.regs) if self.regs_used[i]]) + "\n")

from pyparsing import *
import os
import math
from inspect import currentframe, getframeinfo

def len_of_last_line(code):
    col = 0
    for char in code.split("\n")[-1]:
        print("char is: " + str(ord(char)))
        if char == "\t":
            col = (math.floor(col / 8) + 1) * 8
        else:
            col += 1
    
    return col

ident = Word(alphas + "_")
type_ = Literal("i64")
integer = Combine(Optional("-") + Word("0123456789"))
decimal = Combine(Optional("-") + Word("0123456789") + Literal(".") + Word("0123456789"))
number = decimal | Group(integer).set_results_name("int_literal")

OPAREN, CPAREN, COMMA, COLON, SEMI, EQ, OBRACE, CBRACE = map(Suppress, "(),:;={}")
addexpr = Forward()
mulexpr = Forward()
expr = Forward()
smt = Forward()
term = (OPAREN + expr + CPAREN) | number | Group(ident).set_results_name("ident")
compoundsmt = Group(OBRACE + ZeroOrMore(smt) + CBRACE).set_results_name("compoundsmt")
compoundexpr = Group(OBRACE + ZeroOrMore(smt) + expr + CBRACE).set_results_name("compoundexpr")

mulexpr << (Group(term + (Literal("*") | Literal("/") | Literal("%")) + mulexpr).set_results_name("binexpr")| term)
addexpr << (Group(mulexpr + (Literal("+") | Literal("-")) + addexpr).set_results_name("binexpr") | mulexpr)

funccall = Group(ident + OPAREN + ZeroOrMore(expr + COMMA) + Optional(expr) + CPAREN).set_results_name("funccall")

eqfunc       =  Group(EQ + expr + SEMI).set_results_name("compoundexpr")
compoundfunc =  compoundexpr | compoundsmt

funcdef = Group(Suppress("fn") + ident + OPAREN + 
          Group(Group(ZeroOrMore(ident + COLON + type_ + COMMA) + Optional(ident + COLON + type_)) + CPAREN +
          Optional(Suppress("->") + type_)) + (compoundfunc | eqfunc)).set_results_name("funcdef")

expr << (funccall | addexpr)

smt << (expr + Suppress(";"))
prog = ZeroOrMore(funcdef)

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


test_prog = """

fn add(a: i64, b: i64) -> i64 = a + b;

fn add_maybe(a: i64, b: i64) -> i64 {
    putd(a);
    putd(b);
    add(a, b)
}
fn main() -> i64 {
    putd(add_maybe(1, 1));
    0
}

"""

def parse(text):
    return prog.parse_string(text, parse_all=True)

class CG:
    def __init__(self):
        self.code = ""
        self.regs = ["%rax", "%rcx", "%rdx", "%rsi", "%rdi", "%r8", "%r9"]
        self.regs_used = [False] * len(self.regs)
        self.funcs = []
        self.locals = []
        
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
        if reg is None:
            print("Debug: may be a bug idk, reg was none")
        idx = self.regs.index(reg)
        self.regs_used[idx] = False
        
    def alloc_arg_regs(self, num_args):
        args_order = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"]
        if len(args_order) < num_args:
            assert False, "stack args are not supported yet"
        return args_order[:num_args]
        
    def is_reg_used(self, reg):
        return self.regs_used[self.regs.index(reg)]
    
    def funccall(self, ast):
        funcname = ast[0]
        num_args = len(ast) - 1
        
        caller_saved_regs = ["%rax", "%rcx", "%rdx", "%rsi", "%rdi", "%r8", "%r9"]
        saved_regs = []
        for reg in caller_saved_regs:
            if self.is_reg_used(reg):
                saved_regs.append(reg)
                self.code += "\tpushq\t" + reg; self.code += LNO
        
        regs = self.alloc_arg_regs(num_args)
        
        for i, arg in enumerate(ast[1:]):
            reg = self.expr(arg)
            self.code += "\tmovq\t" + reg + ",\t" + regs[i]; self.code += LNO
            self.regfree(reg)
        
        self.code += "\tcall\t" + str(funcname); self.code += LNO
        
        ret_reg = self.regalloc()
        self.code += "\tmovq\t%rax,\t" + ret_reg; self.code += LNO
        
        for reg in saved_regs:
            self.code += "\tpopq\t" + reg; self.code += LNO
            
        return ret_reg
    
    def binexpr(self, ast):
        lhs = self.expr(ast[0])
        op = ast[1]
        rhs = self.expr(ast[2])
        if op == "+":
            self.code += "\taddq\t"
        elif op == "*":
            self.code += "\timul\t"        
        self.code += lhs + ",\t" + rhs; self.code += LNO
        
        self.regfree(lhs)
        return rhs
        
    def int_literal(self, ast):
        reg = self.regalloc()
        self.code += "\tmovq\t$" + str(ast[0]) + ",\t" + reg; self.code += LNO
        return reg
    
    def ident(self, ast):
        name = ast[0]
        print(self.locals)
        if not name in self.locals[-1]:
            print("Undefined symbol '" + name + "'")
            raise SyntaxError()
            
        reg = self.regalloc()
        self.code += f"\tmovq\t-{self.locals[-1][name][1]}(%rbp),\t{reg}"; self.code += LNO
        return reg
            
    def expr(self, ast):
        print(ast)
        if ast.get_name() == "binexpr":
            return self.binexpr(ast)
        elif ast.get_name() == "int_literal":
            return self.int_literal(ast)
        elif ast.get_name() == "funccall":
            return self.funccall(ast)
        elif ast.get_name() == "ident":
            return self.ident(ast)
        else:
            print("Not implemented: expression type " + ast.getName())
            exit(1)
    
    def sizeof(self, ty):
        return 8 #everything is long for now
        
    def smt(self, ast):
        retval = self.expr(ast)
        self.regfree(retval)
    
    def funcdef(self, ast):
        self.funcs.append(str(ast[0]))
        locsize = sum(map(self.sizeof, ast[1][0][::2]))
        
        self.locals.append({})
        
        self.code += str(ast[0]) + ":\n"
        if locsize > 0:
            self.code += "\tpushq\t%rbp"; self.code += LNO + f"\tmovq\t%rsp,\t%rbp\n\tsubq\t${locsize},\t%rsp\n"
        
        arg_regs = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"]
        loc = 0
        idx = 0
        for name, ty in zip(ast[1][0][::2], ast[1][0][1::2]):
            self.locals[-1][name] = (ty, loc)
            self.code += f"\tmovq\t{arg_regs[idx]},\t-{loc}(%rbp)"; self.code += LNO
            loc += self.sizeof(ty)
            idx += 1
        
        for smt in ast[2][:-1]:
            self.smt(smt)
        
        if ast[2].get_name() == "compoundexpr":
            ret_val = self.expr(ast[2][-1])
        else:
            self.smt(ast[2][-1])
            ret_val = None
        
        if ret_val is not None:
            self.code += "\tmovq\t" + ret_val + ",\t%rax"; self.code += LNO
        
        if locsize > 0:
            self.code += "\tleave"; self.code += LNO
        self.code += "\tret"; self.code += LNO
        
        self.locals.pop()

    def gen(self, ast):
        print(ast.dump())
        for smt in ast:
            if smt.get_name() == "funcdef":
                self.funcdef(smt)
            else:
                print(f"Invalid syntax: Unexpected token '{smt[0]}'")
                exit(1)
        
        self.code = ".text\n" + "\n".join([".globl " + name + "\n.type " + name + ", @function" for name in self.funcs]) + "\n" + self.code
        with open("citrus.s", "w") as f:
            f.write(self.code)
        print(self.code)
    
a = CG()
a.gen(parse(test_prog))

    
