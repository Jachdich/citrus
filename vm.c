#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>

#include "definitions.h"
#include "debug.h"
#include "instructions.h"

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
int equal = 0;

uint8_t * code; // {STRCONST, 11, 'h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!', STRPRINT};
StackObj stack[1024];
StackObj globals[1024];

int getNextCodeInt() {
    int length = code[ip++] << 8;
    length = (length << 8) | (code[ip++] << 8);
    length = (length << 8) | (code[ip++] << 8);
    length = (length << 8) | (code[ip++]);
    return length;
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
    if (argc < 2) {
        printf("Error: Expected file as argument\n");
        return 1;
    }
    if (load_file(argv[1]) == 1) {
        return 1;
    }
    
    int debug = 0;
    int ARG_START = 2;
    if (argc == 3) {
        if (strcmp(argv[2], "-d") == 0) {
            debug = 1;
            ARG_START = 3;
        }
    }
    for (int i = ARG_START; i < argc; i++) {
        StackObj top;
        int length = strlen(argv[i]);
        top.type = STRING;
        top.size = length;
        top.cdata = malloc(sizeof(char) * length);
        top.cdata = argv[i];
        stack[++sp] = top;
    }

    while (ip < codelen) {
        char instruction = code[ip++];
        if (debug) {
            while (1) {
                char inp[100];
                printf("> ");
                fgets(inp, 100, stdin);
                if (strcmp("advance\n", inp) == 0 || strcmp("a\n", inp) == 0) {
                    printf("\n");
                    break;
                } else if (strcmp("stack\n", inp) == 0) {
                    printstack();
                } else if (strcmp("instr\n", inp) == 0) {
                    printinstr(instruction);
                } else if (strcmp("code\n", inp) == 0) {
                    printcode();
                } else if (strcmp("\n", inp) == 0) {
                    printstack();
                    printinstr(instruction);
                    break;
                }
            }
        }
        switch (instruction) {
            case NOP: break;
            case ICONST: iconst(); break;
            case STRCONST: strconst(); break;
            case STRPRINT: strprint(); break;
            case IPRINT: iprint(); break;
            case IADD: iadd(); break;
            case ISUB: isub(); break;
            case ICOMP: icompare(); break;
            case JMP: jump(); break;
            case JZ: jump_zero(); break;
            case DUP: duplicate(); break;
            case GLOAD: gload(); break;
            case GSTORE: gstore(); break;
            case LOAD: load(); break;
            case STORE: store(); break;
            case HALT: return 0;
            default: printf("ERROR: Invalid instruction %d\n", instruction);
        }
    }
    return 0;
}
