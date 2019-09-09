CC=gcc
PY=citrus.py
CFLAGS=
OBJ = main.o
PyCompiler = pyinstaller
PYFLAGS = --onefile

citrus: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

.PHONY: clean

clean: clean
    rm *.o
    rm *.spec
    rm -r build
    rm -r dist
    rm -r .idlerc
    rm -r __pycache__


jcc: $(PY)
    $(PyCompiler) citrus.py $(PYCFLAGS)
    cp dist/citrus.exe jcc.exe
