#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdint.h>

#define INT 0
#define STRING 1
#define CHAR 2
#define FLOAT 3

#define NOP 'n'
#define ICONST 'i'
#define IPRINT 'd'
#define STRCONST 's'
#define STRPRINT 'p'
#define IADD 'a'
#define HALT 'h'

typedef struct StackObj {
    int type;
    int size;
    union {
        int * idata;
        float * fdata;
        char * cdata;
    };
} StackObj;

int sp = -1;
int fp = 0;
int ip = 0;

int codelen = 0;

uint8_t * code; // {STRCONST, 11, 'h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!', STRPRINT};
StackObj stack[1024];

void iconst() {
    int c = code[ip++];
    StackObj top;
    top.type = INT;
    top.size = 1;
    top.idata = malloc(sizeof(int));
    top.idata[0] = c;
    stack[++sp] = top;
}

void iadd() {
    StackObj * operand_a = &stack[sp--];
    StackObj * operand_b = &stack[sp--];
    operand_a->idata[0] += operand_b->idata[0];
    stack[++sp] = *operand_a;
}

void iprint() {
    StackObj * top = &stack[sp--];
    if (top->size != 1) {
        printf("Error: Stack is corrupted! (int size != 1)\n");
    } else if (top->type != INT) {
        printf("Error: iprint needs type INT(0), got type %d\n", top->type);
    } else {
        printf("%d\n", top->idata[0]);
    }
}

void strconst() {
    int length = code[ip++] << 8;
    length = (length << 8) + (code[ip++] << 8);
    length = (length << 8) + (code[ip++] << 8);
    length = (length << 8) + (code[ip++]);
    StackObj top;
    top.type = STRING;
    top.size = length;
    top.cdata = malloc(sizeof(char) * length);
    for (int i = 0; i < length; i++) {
        top.cdata[i] = (char)code[ip++];
        //printf("%c", code[ip - 1]);
    }
    stack[++sp] = top;
}

void strprint() {
    StackObj * top = &stack[sp--];
    for (int i = 0; i < top->size; i++) {
        printf("%c", top->cdata[i]);
    }
    //printf("\n");
}

int load_file(char * filename) {
    FILE * f;
    struct stat st;
    
    if ((f = fopen(filename, "r"))) {
        fstat(fileno(f), &st);
        code = (uint8_t *)malloc(st.st_size);
        fread((void *) code, 1, st.st_size, f);
        codelen = st.st_size;
    } else {
        printf("Error reading file %s\n", filename);
        return 1;
    }
    return 0;
}

int main(int argc, char ** argv) {
    if (argc != 2) {
        printf("Error: Expected file as argument\n");
        return 1;
    }
    if (load_file(argv[1]) == 1) {
        return 1;
    }

    while (ip < codelen) {
        char instruction = code[ip++];
        switch (instruction) {
            case NOP: break;
            case ICONST: iconst(); break;
            case STRCONST: strconst(); break;
            case STRPRINT: strprint(); break;
            case IPRINT: iprint(); break;
            case IADD: iadd(); break;
            case HALT: return 0;
            default: printf("ERROR: Invalid instruction %d\n", instruction);
        }
    }
    return 0;
}