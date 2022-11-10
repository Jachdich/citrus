PYTHON = python3.9

SOURCES := $(shell find src -maxdepth 1 -name "*.lime" -type f)
OBJECTS := $(patsubst src/%,build/%,$(SOURCES:.lime=.o))
run: citrus
	./citrus
	
build/%.s: src/%.lime
	$(PYTHON) compile.py -o $@ -g $^

build/%.o: build/%.s
	gcc -c -o $@ $^

liblemon/liblemon.a:
	+make -C liblemon

citrus: $(OBJECTS) liblemon/liblemon.a
	gcc -o citrus $^ -Lliblemon -llemon

clean:
	rm -rf build/* citrus

.PHONY: clean
