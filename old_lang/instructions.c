#include <stdio.h>
#include <stdlib.h>
#include "vm.h"
#include "definitions.h"

void iconst() {
    INT_DATATYPE number = getNextCodeInt();
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
    INT_DATATYPE length = getNextCodeInt();
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
    INT_DATATYPE address = getNextCodeInt();
    StackObj * var = &globals[address];
    stack[++sp] = *var;
}

void gstore() {
    INT_DATATYPE address = getNextCodeInt();
    StackObj * data = &stack[sp--];
    //printf("ADDR: %d, IDATA: %d\n", address, data->idata[0]);
    globals[address] = *data;
}

void load() {
    INT_DATATYPE offset = getNextCodeInt();
    //printf("LOAD OFFSET: %d, LOAD ABS: %d\n", offset, fp + offset);
    StackObj * data = &stack[fp + offset];
    stack[++sp] = *data;
}

void store() {
    INT_DATATYPE offset = getNextCodeInt();
    StackObj * top = &stack[sp--];
    stack[fp + offset] = *top;
}

void call() {
    StackObj frame;
    frame.type = INT;
    frame.size = 1;
    frame.idata = malloc(sizeof(int));
    frame.idata[0] = fp;
    stack[++sp] = frame;
     
    StackObj instruction;
    instruction.type = INT;
    instruction.size = 1;
    instruction.idata = malloc(sizeof(int));
    instruction.idata[0] = fp;
    stack[++sp] = instruction;
    
    fp = sp;
    sp += 10;
    ip = getNextCodeInt();
}

void ret() {
    sp = fp;
    StackObj * top = &stack[sp--];
    fp = top->idata[0];
    StackObj * top2 = &stack[sp--];
    ip = top2->idata[0];  
}