PYTHON = python3.9

SOURCES := $(shell find src -maxdepth 1 -name "*.lime" -type f)
OBJECTS := $(patsubst src/%,build/%,$(SOURCES:.lime=.o))
run: citrus
	./citrus
	
# build/%.s: src/%.lime
#	$(PYTHON) main.py -b x86asm -o $@ -g $^

build/%.c: src/%.lime
	$(PYTHON) main.py -g -b c -o $@ $^

build/%.o: build/%.s
	gcc -c -o $@ $^

build/%.o: build/%.c
	gcc -c -Wall -o $@ $^

liblemon/liblemon.a:
	+make -C liblemon

citrus: $(OBJECTS) liblemon/liblemon.a
	gcc -o citrus $^ -Lliblemon -llemon

clean:
	rm -rf build/* citrus

.PHONY: clean
