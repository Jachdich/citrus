#ifndef VM_H
#define VM_H
#include "definitions.h"

typedef struct StackObj {
    int type;
    int size;
    union {
        INT_DATATYPE * idata;
        float * fdata;
        char * cdata;
    };
} StackObj;

extern unsigned char * code;
extern StackObj globals[1024];
extern int ip;
extern int sp;
extern int fp;
extern int codelen;
extern int equal;
extern StackObj stack[1024];

int getNextCodeInt();

#endif
