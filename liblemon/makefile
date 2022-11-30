OBJECTS := io.o string.o
PYTHON = python3.9

liblemon.a: $(OBJECTS)
	ar -rc $@ $^
	ranlib $@

%.o: %.c
	gcc -c -o $@ $^

%.o: %.s
	gcc -c -o $@ $^

%.c: %.lime
	$(PYTHON) ../main.py -g -b c -o $@ $^
	
