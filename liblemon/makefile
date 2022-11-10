OBJECTS := io.o

liblemon.a: $(OBJECTS)
	ar -rc $@ $^
	ranlib $@

%.o: %.c
	gcc -c -o $@ $^

%.o: %.s
	gcc -c -o $@ $^

