from backends import x86asm, llvm, cgen, c_with_ir
from parser import parse

if __name__ == "__main__":
    import argparse, sys, traceback
    parser = argparse.ArgumentParser(
                    prog="Citrus",
                    description='Compile citrus code')
    parser.add_argument("filename")
    parser.add_argument("-o", "--output", help="Specify output file name. Default: <input filename>.s")
    parser.add_argument("-g", "--debug", action="store_true", help="Enable debug comments in assembly")
    parser.add_argument("-b", "--backend", default="x86asm", help="Specify which backend to compile with. Options are llvm, x86asm, c, c_with_ir. Default is x86asm")
    parser.add_argument("-I", "--import", action="append", help="Specify additional directories to search for imports")
    args = parser.parse_args()
    try:
        with open(args.filename, "r") as f:
            source = f.read()
    except FileNotFoundError:
        print(args.filename + ": No such file or directory")
        exit(1)
    
    if args.backend == "x86asm":
        backend = x86asm
    elif args.backend == "llvm":
        backend = llvm
    elif args.backend == "c":
        backend = cgen
    elif args.backend == "c_with_ir":
        backend = c_with_ir
   
    a = backend.CG(args.filename) 
    
    def exception_hook(exctype, value, tb):
        traceback_formated = traceback.format_exception(exctype, value, tb)
        traceback_string = "".join(traceback_formated)
        print(traceback_string, file=sys.stderr)
        print(a.format_code(True))
        
        sys.exit(1)
        
    sys.excepthook = exception_hook
    
    import_dirs = getattr(args, "import")
    if import_dirs is None:
        import_dirs = ["."]
    out = a.gen(parse(source), args.debug, import_dirs)
    print(out)
    if args.output is None:
        output_file = ".".join(input_file.split(".")[:-1]) + {"x86asm": ".s", "llvm": ".ll", "c": ".c", "c_with_ir": ".c"}[args.backend]
    else:
        output_file = args.output
    
    with open(output_file, "w") as f:
        f.write(out)
