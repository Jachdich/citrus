from pyparsing import *
import os

# expr = Forward()

integer = Combine(Optional("-") + Word("0123456789"))

expr = integer

prog = ZeroOrMore(expr)

for fname in [n for n in os.listdir("tests") if not "_output" in n]:
    fname = os.path.join("tests", fname)
    with open(fname + "_output", "r") as f:
        expected_output = f.read().strip()
        
    with open(fname, "r") as f:
        inp = f.read()
        
    out = prog.parseString(inp)
    if str(out) == expected_output:
        print("Test " + fname + " passed")
    else:
        print("Test " + fname + " FAILED")
        print("Output: " + str(out))
        print("Expected output: " + expected_output)