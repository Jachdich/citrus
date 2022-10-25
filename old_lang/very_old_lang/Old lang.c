#include <stdio.h>

int flag = 0;
int pc;
int stackpointer;
int stack[1024];
int code[] = {00,00,00,00,00,00,00,00};
int data[1024] = {00,00,00,00};

int get_length() {
    int length = stack[stackpointer];
    stackpointer --;
    return length;
}

int pass() {
    return 0;
}

int load_value(int operands[]) {
    return 0;
}

int * pop(int values[])  {
    for (int i = 0; i < sizeof(values); i++) {
        values[i] = stack[stackpointer];
        stackpointer--;
    }
    return values;
}

int push(int values[]) {
return 0;
}

int add_values(int values[]) {
    int length = get_length();
    int *p;
    int inArr[length];
    p = pop(inArr);
    int result[length];
    for (int i = 0; i < length; i++) {
        result[i] = *(p + i);
    }
    int a = result[0];
    
    length = get_length();
    int *p2;
    int inArr2[length];
    p2 = pop(inArr2);
    int result2[length];
    for (int i = 0; i < length; i++) {
        result2[i] = *(p2 + i);
    }
    int b = result2[0];
}

int print_value(int values[]) {
return 0;
}

int jump(int values[]) {
return 0;
}

int compare(int values[]) {
return 0;
}

int jump_false(int values[]) {
return 0;
}

int runCommand(int operands[], char cmd[]) {
    if (cmd == "load_value") {
        load_value(operands);
    } else if (cmd == "add_values") {
        add_values(operands);
    } else if (cmd == "print_value") {
        print_value(operands);
    } else if (cmd == "jump") {
        jump(operands);
    } else if (cmd == "compare") {
        compare(operands);
    } else if (cmd == "jump_if_false") {
        jump_false(operands);
    } else if (cmd == "pass") {
        pass();
    } else {
        return 127;
    }
    return 0;
}

int main(void) {
printf("oof");
return 0;
}

