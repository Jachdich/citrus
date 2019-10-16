#ifndef INT

#define INT 0
#define STRING 1
#define FLOAT 2

#define NOP 'n'
#define ICONST 'i'
#define IPRINT 'o'
#define STRCONST 's'
#define STRPRINT 'p'
#define IADD 'a'
#define ISUB 'e'
#define JMP 'j'
#define JZ 'z'
#define ICOMP 'c'
#define DUP 'd'
#define GLOAD 'g'
#define GSTORE 'f'
#define LOAD 'q'
#define STORE 'w'
#define HALT 'h'
#define CALL '#'
#define RET 'r'

#define INT_IS_64 0
#define STACK_START 50

#if INT_IS_64 == 0
#define INT_DATATYPE int
#else
#define INT_DATATYPE long
#endif

#endif
