from pyparsing import *
import os

# expr = Forward()

integer = Combine(Optional("-") + Word("0123456789"))
decimal = Combine(Optional("-") + Word("0123456789") + Literal(".") + Word("0123456789"))
number = decimal | integer 

expr = Forward()
mulexpr = Forward()
term = Group("(" + expr + ")") | number

mulexpr << (Group(term + (Literal("*") | Literal("/")) + mulexpr) | term)
expr << (Group(mulexpr + (Literal("+") | Literal("-")) + expr) | mulexpr)

prog = ZeroOrMore(expr)


def test(inp, out):
    try:
        res = prog.parseString(inp, parseAll=True)
    except ParseException as e:
        res = str(e)

    if res == out:
        print("\x1b[92m✓\x1b[0m", inp, "=>", res)
    else:
        print("\x1b[91mx\x1b[0m", inp, "=>", res, "!=", out, "(expected)")


def run_tests():
    test("0", ["0"])
    test("76139", ["76139"])
    test("32.33", ["32.33"])
    test("-341", ["-341"])
    test("-32.133", ["-32.133"])
    test("132 + 1.324", ["132", "+", "1.324"])
    test("1 + 2 + 3", ["1", "+", "2", "+", "3"])
    test("1 + 2 * 3", ["1", "+", ["2", "*", "3"]])
    test("1 * 2 + 3", [["1", "*", "2"], "+", "3"])

run_tests()