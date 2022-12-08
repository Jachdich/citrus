OBJECTS := cio.o io.o string.o
PYTHON = python3.9

liblemon.a: $(OBJECTS)
	ar -rc $@ $^
	ranlib $@

%.o: %.c
	gcc -c -g -o $@ $^

%.o: %.s
	gcc -c -o $@ $^

%.c: %.lime
	$(PYTHON) ../main.py -I .. -g -b c -o $@ $^
	
clean:
	rm *.o *.a io.c string.c