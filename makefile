C_SOURCES = $(wildcard *.c)
HEADERS = $(wildcard *.h)

vm: ${C_SOURCES} ${HEADERS}
	gcc ${C_SOURCES} ${HEADERS} -o vm -Wall

clean:
	rm -rf vm *~
