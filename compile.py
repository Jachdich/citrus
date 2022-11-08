#define LNO() (str(getframeinfo(currentframe()).lineno) + "    " + str([reg for i, reg in enumerate(self.regs) if self.regs_used[i]]))
#define REGALLOC() self.regalloc(dbg=str(getframeinfo(currentframe()).function + ":" + getframeinfo(currentframe()).lineno)

def LNO():
    previous_frame = inspect.currentframe().f_back
    (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
    self = previous_frame.f_locals.get("self")
    posinfo = function_name + ":" + str(line_number)
    return posinfo + " " * (18 - len(posinfo)) + str([reg + " " + str(self.reg_allocator[reg]) for i, reg in enumerate(self.regs) if self.regs_used[i]])

def REGALLOC(reg_wanted=None):
    previous_frame = inspect.currentframe().f_back
    self = previous_frame.f_locals.get("self")
    return self.regalloc(reg_wanted, ALLOCDBG(previous_frame))

def ALLOCDBG(frame=None):
    if frame is None:
        previous_frame = inspect.currentframe().f_back
    else:
        previous_frame = frame
    (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
    self = previous_frame.f_locals.get("self")
    dbginfo = function_name + ":" + str(line_number)
    return dbginfo

from pyparsing import *
import os
import math
import inspect
from pprint import pprint

ident = Word(alphas + "_")
type_ = Literal("i64") | Literal("i32") | Literal("u64") | Literal("u32") | ident
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
          Optional(Suppress("->") + type_)) + (compoundfunc | eqfunc | SEMI)).set_results_name("funcdef")

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


with open("citrus.lime", "r") as f:
    test_prog = f.read()

def parse(text):
    return prog.parse_string(text, parse_all=True)

ARGS_REGS = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"]
CALLER_SAVED_REGS = ["%rax", "%rcx", "%rdx", "%rsi", "%rdi", "%r8", "%r9"]

class ExprRes:
    def __init__(self, reg, ty):
        self.reg = reg
        self.ty = ty

class FuncSig:
    def __init__(self, name, args, ret_ty):
        self.name = name
        self.args = args
        self.ret_ty = ret_ty

class LocalVar:
    def __init__(self, name, ty, loc):
        self.name = name
        self.ty = ty
        self.loc = loc

class CG:
    def __init__(self):
        self.code = []
        self.regs = ["%rax", "%rcx", "%rdx", "%rsi", "%rdi", "%r8", "%r9"]
        self.regs_used = [False] * len(self.regs)
        self.reg_allocator = {}
        self.globals = []
        self.locals = []
        
    def regalloc(self, reg_wanted=None, dbginfo=None):
        if reg_wanted != None:
            if self.is_reg_used(reg_wanted):
                print("Debug: request reg " + reg_wanted + ", but already used")
                return self.regalloc(dbginfo=dbginfo)
            
            self.set_reg_used(reg_wanted, dbginfo)
            return reg_wanted
        
        for i, reg in enumerate(self.regs_used):
            if not reg:
                self.regs_used[i] = True
                self.reg_allocator[self.regs[i]] = dbginfo
                return self.regs[i]
        print("Debug: request reg, all used")
        return None
    
    def regfree(self, reg):
        idx = self.regs.index(reg)
        self.regs_used[idx] = False
        del self.reg_allocator[reg]
        
    def is_reg_used(self, reg):
        return self.regs_used[self.regs.index(reg)]
    
    def set_reg_used(self, reg, dbg):
        self.reg_allocator[reg] = dbg
        self.regs_used[self.regs.index(reg)] = True
        
    def get_global(self, name):
        for sig in self.globals:
            if sig.name == name:
                return sig
    def get_local(self, name):
        for var in self.locals[-1]:
            if var.name == name:
                return var
    
    def funccall(self, ast, reg_hint=None):
        funcname = ast[0]
        func_sig = self.get_global(funcname)
        if func_sig is None:
            raise SyntaxError(f"Unknown function '{funcname}'")
            
        num_args = len(ast) - 1
        if num_args != len(func_sig.args):
            raise SyntaxError(f"Function '{funcname}' expects {len(func_sig.args)} args but {num_args} were given")
        # TODO arg types
        saved_regs = []

        arg_regs = ARGS_REGS[:num_args]
        
        # try to get the args in the right registers
        to_move = []
        to_free = [] # free these regs later
        for i, arg in enumerate(ast[1:]):
            actual_reg, ty = self.expr(arg, reg_hint=arg_regs[i])
            # if they couldnæ then move them later
            if actual_reg != arg_regs[i]:
                to_move.append((actual_reg, arg_regs[i]))
            to_free.append(actual_reg)
        
        # save caller saved regs
        for reg in CALLER_SAVED_REGS:
            if self.is_reg_used(reg) and not reg in to_free:
                saved_regs.append(reg)
                self.code.append(("pushq", reg, LNO()))
        
        # move args that weren't in the right regs            
        for from_, to in to_move:
            self.code.append(("movq", from_, to, LNO()))
        
        # free args
        for reg in to_free:
            self.regfree(reg)

        self.code.append(("call", str(funcname), LNO()))

        # figure out what register to return        
        if reg_hint != None and not self.is_reg_used(reg_hint):
            # use the hint
            ret_reg = REGALLOC(reg_hint)
        else:
            # try to just allocate rax because it's already in rax
            ret_reg = REGALLOC("%rax")
            if ret_reg is None:
                # this is a bit annoying, rax is already allocated
                ret_reg = REGALLOC()
        
        # only move ret value if it's not rax
        if ret_reg != "%rax":
            self.code.append(("movq", "%rax", ret_reg, LNO()))
        
        # restore saved regs
        for reg in saved_regs:
            self.code.append(("popq", reg, LNO()))
            
        return (ret_reg, func_sig.ret_ty)
    
    def binexpr(self, ast, reg_hint=None):
        op = ast[1]
        """if ast[0].get_name() == "int_literal" and ast[2].get_name() == "int_literal":
            # constexpr
            if op == "+":
                return self.int_literal([int(ast[0][0]) + int(ast[2][0])])
            if op == "-":
                return self.int_literal([int(ast[0][0]) - int(ast[2][0])])
            if op == "*":
                return self.int_literal([int(ast[0][0]) * int(ast[2][0])])
            if op == "/":
                return self.int_literal([int(ast[0][0]) // int(ast[2][0])])"""

        rhs, rty = self.expr(ast[2], reg_hint)
        lhs, lty = self.expr(ast[0])
            
        self.regfree(lhs)
        int_tys = ["u64", "u32", "u16", "u8", "i64", "i32", "i16", "i8"]
        if rty in ["f64", "f32"] or lty in ["f64", "f32"]:
            if rty == "f64" or lty == "f64":
                ty = "f64"
            else:
                ty = "f32"
        elif rty in int_tys and lty in int_tys:
            lsigned = lty[0] == "i"
            rsigned = rty[0] == "i"
            lbits = int(lty[1:])
            rbits = int(rty[1:])
            if lsigned or rsigned:
                outsigned = "i"
            else:
                outsigned = "u"
            
            outbits = max(lbits, rbits)
            ty = outsigned + str(outbits)
        else:
            raise SyntaxError(f"Incompatible types for operator '{op}': type '{lty}' and type '{rty}'")
        
        
        
        
        if op == "/" or op == "%":
            # TODO maybe unnecessary MOVs
            if self.is_reg_used("%rdx"):
                self.code.append(("pushq", "%rdx", LNO()))
            if self.is_reg_used("%rax"):
                self.code.append(("pushq", "%rax", LNO()))
            self.code.append(("movq", lhs, "%rax", LNO()))
            self.code.append(("cdq", LNO()))
            self.code.append(("idivq", rhs, LNO()))
            if op == "/":
                self.code.append(("movq", "%rax", rhs, LNO()))
            else:
                self.code.append(("movq", "%rdx", rhs, LNO()))
            if self.is_reg_used("%rdx"):
                self.code.append(("popq", "%rax", LNO()))
            if self.is_reg_used("%rax"):
                self.code.append(("popq", "%rdx", LNO()))
        else:
            if op == "+":
                instr = "addq"
            elif op == "*":
                instr = ("i" if ty[0] == "i" else "") + "mulq"
            elif op == "-":
                instr = "subq"

            self.code.append((instr, lhs, rhs, LNO()))
        
        return rhs, ty
        
    def int_literal(self, ast, reg_hint=None):
        reg = REGALLOC(reg_hint)
        self.code.append(("movq", "$" + str(ast[0]), reg, LNO()))
        return reg, "i64" # TODO figure this out

    def ident(self, ast, reg_hint=None):
        name = ast[0]
        var = self.get_local(name)
        if var is None:
            raise SyntaxError("Undefined symbol '" + name + "'")
        
        if reg_hint is not None:
            reg = reg_hint
        else:
            reg = REGALLOC()
        self.code.append(("movq", f"-{var.loc}(%rbp)", reg, LNO()))
        return reg, var.ty
            
    def expr(self, ast, reg_hint=None):
        if ast.get_name() == "binexpr":
            return self.binexpr(ast, reg_hint=reg_hint)
        elif ast.get_name() == "int_literal":
            return self.int_literal(ast, reg_hint=reg_hint)
        elif ast.get_name() == "funccall":
            return self.funccall(ast, reg_hint=reg_hint)
        elif ast.get_name() == "ident":
            return self.ident(ast, reg_hint=reg_hint)
        else:
            print("Not implemented: expression type " + ast.getName())
            exit(1)
    
    def sizeof(self, ty):
        return {"i64": 8, "i32": 4, "i16": 2, "i8": 1,
                "u64": 8, "u32": 4, "u16": 2, "u8": 1,
                "f64": 8, "f32": 4, "char": 1}[ty]

    def smt(self, ast):
        retval, rettype = self.expr(ast)
        self.regfree(retval)
    
    def is_valid_type(self, ty):
        return ty in ["i32", "i64", "i16", "i8", "u64", "u32", "u16", "u8", "f64", "f32", "char", "void"]

    def check_valid_type(self, ty):
        if not self.is_valid_type(ty):
            raise SyntaxError(f"Unknown type '{ty}'")
    
    def funcdef(self, ast):
        if len(ast[1]) > 1:
            ret_ty = ast[1][1]
        else:
            ret_ty = "void"

        self.check_valid_type(ret_ty)
        args = ast[1][0][1::2]        
        sig = FuncSig(str(ast[0]), args, ret_ty)
        self.globals.append(sig)
        
        if len(ast) < 3:
            # it's a foward declaration
            return
        
        locsize = sum(map(self.sizeof, ast[1][0][1::2]))
        
        self.locals.append([])
        
        self.code.append((str(ast[0]) + ":", LNO()))
        if locsize > 0:
            self.code.append(("pushq", "%rbp", LNO()))
            self.code.append(("movq",  "%rsp",       "%rbp", LNO()))
            self.code.append(("subq" , "$" + str(locsize), "%rsp", LNO()))
        
        arg_regs = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"]
        loc = 0
        idx = 0
        for name, ty in zip(ast[1][0][::2], ast[1][0][1::2]):
            self.check_valid_type(ty)
            self.locals[-1].append(LocalVar(name, ty, loc))
            self.code.append(("movq", arg_regs[idx], f"-{loc}(%rbp)", LNO()))
            loc += self.sizeof(ty)
            idx += 1
        
        for smt in ast[2][:-1]:
            self.smt(smt)
        
        if ast[2].get_name() == "compoundexpr":
            ret_val, actual_ret_ty = self.expr(ast[2][-1])
        else:
            self.smt(ast[2][-1])
            ret_val = None
            actual_ret_ty = "void"
            
        if actual_ret_ty != ret_ty:
            raise SyntaxError(f"Function '{str(ast[0])}' should return type '{ret_ty}', but last expression is of type '{actual_ret_ty}'")
        
        if ret_val is not None and ret_val != "%rax":
            self.code.append(("movq", ret_val, "%rax", LNO()))
            self.regfree(ret_val)
        elif ret_val == "%rax":
            self.regfree(ret_val)
        
        if locsize > 0:
            self.code.append(("addq", "$" + str(locsize), "%rsp", LNO()))
            self.code.append(("popq", "%rbp", LNO()))
        self.code.append(("ret", LNO()))
        
        self.locals.pop()

    def gen(self, ast, debug=False):
        pprint(ast.as_list())
        for smt in ast:
            if smt.get_name() == "funcdef":
                self.funcdef(smt)
            else:
                print(f"Invalid syntax: Unexpected token '{smt[0]}'")
                exit(1)
        
        fmt_code = ".text\n" + "\n".join([".globl " + sig.name + "\n.type " + sig.name + ", @function" for sig in self.globals])
        fmt_code += "\n"
        for line in self.code:
            dbg = line[-1]
            instr = line[:-1]
            
            ""# labels are unindented
            if not (len(instr) == 1 and instr[0].endswith(":")):
                curr_line = "    "
            else:
                curr_line = ""
            
            for i, ipart in enumerate(instr):
                bit_of_line = ipart
                if i < len(instr) - 1 and i != 0:
                    bit_of_line += ","
                curr_line += bit_of_line + " " * (12 - len(bit_of_line))
            
            if debug:
                curr_line += " " * (48 - len(curr_line))
                curr_line += "# " + dbg
            fmt_code += curr_line + "\n"
        return fmt_code
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
                    prog="Citrus",
                    description='Compile citrus code')
    parser.add_argument("filename")
    parser.add_argument("-o", "--output", help="Specify output file name. Default: <input filename>.s")
    parser.add_argument("-g", "--debug", action="store_true", help="Enable debug comments in assembly")
    args = parser.parse_args()
    try:
        with open(args.filename, "r") as f:
            source = f.read()
    except FileNotFoundError:
        print(args.filename + ": No such file or directory")
        exit(1)
    
    a = CG()
    out = a.gen(parse(source), args.debug)
    print(out)
    if args.output is None:
        output_file = ".".join(input_file.split(".")[:-1]) + ".s"
    else:
        output_file = args.output
    
    with open(output_file, "w") as f:
        f.write(out)