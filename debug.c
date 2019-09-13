#include <stdio.h>
#include "vm.h"
#include "definitions.h"

void printstack() {
    for (int i = STACK_START; i < sp + 1; i++) {
        if (stack[i].type == INT) {
            printf("%d,", stack[i].idata[0]);
        } else if (stack[i].type == STRING) {
            printf("%s,", stack[i].cdata);
        }
    }
    printf("\n");
}

void printcode() {
    printf("IP is %d, code[ip] is %d (or %c)\n", ip - 1, code[ip - 1], code[ip - 1]);
    for (int i = 0; i < codelen; i++) {
        printf("%d,", code[i]);
    }
    printf("\n");
    for (int i = 0; i < codelen; i++) {
        printf("%c,", code[i]);
    }
    printf("\n");
}

void printinstr(char instr) {
    printf("Instruction %d (", instr);
    switch (instr) {
        case NOP:      printf("NOP"); break;
        case ICONST:   printf("ICONST"); break;
        case STRCONST: printf("STRCONST"); break;
        case STRPRINT: printf("STRPRINT"); break;
        case IPRINT:   printf("IPRINT"); break;
        case IADD:     printf("IADD"); break;
        case ISUB:     printf("ISUB"); break;
        case ICOMP:    printf("ICOMP"); break;
        case JMP:      printf("JMP"); break;
        case JZ:       printf("JZ"); break;
        case DUP:      printf("DUP"); break;
        case GLOAD:    printf("GLOAD"); break;
        case GSTORE:   printf("GSTORE"); break;
        case LOAD:     printf("LOAD"); break;
        case STORE:    printf("STORE"); break;
        case HALT:     printf("HALT"); break;
        default:       printf("INVALID");
    }
    printf(")\n");
}