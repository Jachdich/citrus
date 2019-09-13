#include <stdio.h>
#include <stdlib.h>
#include "vm.h"
#include "definitions.h"

void iconst() {
    int number = getNextCodeInt();
    StackObj top;
    top.type = INT;
    top.size = 1;
    top.idata = malloc(sizeof(int));
    top.idata[0] = number;
    stack[++sp] = top;
}

void iadd() {
    StackObj * operand_a = &stack[sp--];
    StackObj * operand_b = &stack[sp--];
    operand_a->idata[0] += operand_b->idata[0];
    stack[++sp] = *operand_a;
}

void isub() {
    StackObj * operand_a = &stack[sp--];
    StackObj * operand_b         = &stack[sp--];
    operand_b->idata[0] -= operand_a->idata[0];
    stack[++sp] = *operand_b;
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
    int length = getNextCodeInt();
    StackObj top;
    top.type = STRING;
    top.size = length;
    top.cdata = malloc(sizeof(char) * length);
    for (int i = 0; i < length; i++) {
        top.cdata[i] = (char)code[ip++];
    }
    stack[++sp] = top;
}

void strprint() {
    StackObj * top = &stack[sp--];
    for (int i = 0; i < top->size; i++) {
        printf("%c", top->cdata[i]);
    }
}

void icompare() {
    StackObj * a = &stack[sp--];
    StackObj * b = &stack[sp--];
    if (a->type != b->type) {
        equal = 0;
        return;
    }
    if (a->idata[0] != b->idata[0]) {
        equal = 0;
        return;
    }
    equal = 1;
}

void jump() {
    StackObj * top = &stack[sp--];
    int addr = top->idata[0];
    ip = addr;
}

void jump_zero() {
    if (equal) {
        jump();
    } else {
        sp--;
    }
}

void duplicate() {
    stack[sp + 1] = stack[sp];
    sp++;
}

void gload() {
    int address = getNextCodeInt();
    StackObj * var = &globals[address];
    stack[++sp] = *var;
}

void gstore() {
    int address = getNextCodeInt();
    StackObj * data = &stack[sp--];
    globals[address] = *data;
}
void load() {
    int offset = getNextCodeInt();
    //printf("LOAD OFFSET: %d, LOAD ABS: %d\n", offset, fp + offset);
    StackObj * data = &stack[fp + offset];
    stack[++sp] = *data;
}
void store() {
    int offset = getNextCodeInt();
    StackObj * top = &stack[sp--];
    stack[fp + offset] = *top;
}
