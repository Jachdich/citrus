from backends.x86asm import *

if __name__ == "__main__":
    import argparse, sys, traceback
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
    
    def exception_hook(exctype, value, tb):
        traceback_formated = traceback.format_exception(exctype, value, tb)
        traceback_string = "".join(traceback_formated)
        print(traceback_string, file=sys.stderr)
        print(a.format_code(True))
        
        sys.exit(1)
        
    sys.excepthook = exception_hook

    out = a.gen(parse(source), args.filename, args.debug)
    print(out)
    if args.output is None:
        output_file = ".".join(input_file.split(".")[:-1]) + ".s"
    else:
        output_file = args.output
    
    with open(output_file, "w") as f:
        f.write(out)
