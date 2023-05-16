SOURCES := $(shell find . -type f -name "*.lime")
C_SOURCES := $(patsubst %,csrc/%,$(SOURCES:.lime=.c))
OBJECTS := $(patsubst csrc/%,obj/%,$(C_SOURCES:.c=.o)) obj/cio.o
PYTHON = python3.9

liblemon.a: $(OBJECTS)
	ar -rc $@ $^
	ranlib $@

obj/%.o: csrc/%.c
	gcc -c -g -o $@ $^

obj/cio.o: cio.c
	gcc -c -g -o $@ $^

%.o: %.s
	gcc -c -o $@ $^

.PRECIOUS: csrc/%.c
csrc/%.c: %.lime
	$(PYTHON) ../main.py -I .. -g -b c -o $@ $^
	
clean:
	rm -f obj/*.o *.a csrc/*.c