PYTHON = python3.9

run: citrus
	./citrus
	
build/citrus.s: compile.py citrus.lime
	$(PYTHON) compile.py -o build/citrus.s -g citrus.lime

build/%.o: build/%.s
	gcc -c -o $@ $^

liblemon/liblemon.a:
	+make -C liblemon

citrus: build/citrus.o liblemon/liblemon.a
	gcc -o citrus build/citrus.o -Lliblemon -llemon