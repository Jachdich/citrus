SOURCES = $(wildcard *.c)
HEADERS = $(wildcard *.h)

CFLAGS = -Wall -g

vm: ${SOURCES} ${HEADERS}
	gcc ${SOURCES} ${HEADERS} -o vm ${CFLAGS}
    
clean:
	rm -rf vm ~* *.ghc
