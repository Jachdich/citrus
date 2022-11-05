run: citrus
	./citrus
	
compile.py.out: compile.py
	gcc -w -x c -E compile.py -o compile.py.out

citrus.s: compile.py.out
	python3 compile.py.out

%.o: %.c
	gcc -c -o $@ $^

%.o: %.s
	gcc -c -o $@ $^

citrus: citrus.o io.o
	gcc -o citrus $^