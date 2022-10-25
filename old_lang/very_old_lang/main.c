/*
CITRUS bytecode interpreter;
Author: James Kitching;
*/ 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <assert.h>
#include <unistd.h>

#define METASIZE 2 //bytes of metadata before data
/*;
STACK
4 ;length
0 ;type (str)
62 ;data (byte 1)
65 ;data (byte 2)
69 ;data (byte 3)
35 ;data (byte 4)

0 str
1 int
2 bool
3 double
4 list
5 dict
6 unspecified/long/byte
*/

char** str_split(char* a_str, const char a_delim) {
    char** result    = 0;
    size_t count     = 0;
    char* tmp        = a_str;
    char* last_comma = 0;
    char delim[2];
    delim[0] = a_delim;
    delim[1] = 0;

    /* Count how many elements will be extracted. */
    while (*tmp) {
        if (a_delim == *tmp) {
            count++;
            last_comma = tmp;
        }
        tmp++;
    }

    /* Add space for trailing token. */
    count += last_comma < (a_str + strlen(a_str) - 1);

    /* Add space for terminating null string so caller
       knows where the list of returned strings ends. */
    count++;

    result = malloc(sizeof(char*) * count);

    if (result) {
        size_t idx  = 0;
        char* token = strtok(a_str, delim);

        while (token) {
            assert(idx < count);
            *(result + idx++) = strdup(token);
            token = strtok(0, delim);
        }
        assert(idx == count - 1);
        *(result + idx) = 0;
    }
    return result;
}

int debug = 0; //prints debugs if 1
int step = 0; //use the debug console?

int stack[65536];
int * code;
int * data;
int var[1024];
int heap[65536];

int pc;
int stackpointer = -1;
int var_ptr = -1;
int name_ptr = -1;
int flag;
int codelength;
int datalength;
int last_var;
int prompt;

void pinstr() {
	printf("CODE %d, ", code[pc]);
	int operands = 0;
	if        (code[pc] == 0)  { printf("pass");
	} else if (code[pc] == 1)  { printf("load_const"); operands = 1;
	} else if (code[pc] == 2)  { printf("load_value"); operands = 1;
	} else if (code[pc] == 3)  { printf("init_value"); operands = 1;
	} else if (code[pc] == 4)  { printf("store_value");
	} else if (code[pc] == 5)  { printf("add_values"); 
	} else if (code[pc] == 6)  { printf("sub_values");
	} else if (code[pc] == 7)  { printf("mul_values");
	} else if (code[pc] == 8)  { printf("div_values");
	} else if (code[pc] == 9)  { printf("compare");
	} else if (code[pc] == 10) { printf("jump");
	} else if (code[pc] == 11) { printf("jump_if_false");
	} else if (code[pc] == 12) { printf("print_value");
	} else if (code[pc] == 13) { printf("input");
	} else if (code[pc] == 14) { printf("dupl");
	} else if (code[pc] == 15) { printf("reverse");
	} else if (code[pc] == 16) { printf("swap");
	} else if (code[pc] == 17) { printf("int");
	} else if (code[pc] == 18) { printf("str");
	} else if (code[pc] == 19) { printf("double"); }
	if (operands > 0) {
		printf(", OPERANDS");
	}
	for (int i = 0; i < operands; i++) {
		printf(" %d", code[pc + i + 1]);
	}
	printf("\n");
}

void pvar_ref(){
	for (int i = 0; i < 10; i++) {
		printf("%d ", var[i]);
	}
	printf("\n");
}

void pdata() {
	for (int i = 0; i < datalength; i++) {
		printf("%d ", data[i]);
	}
	printf("\n");
}

int error(int e) {
	if (e == 1) {
		printf("An error occurred: Invalid type conversion (Code %d)\n", e);
		return 1;
	} else if (e == 2) {
		printf("Could not open bytecode file\n");
		return 1;
	} else if (e == 3) {
		printf("Jump address has wrong type\n");
		return 1;
	} else if (e == 4) {
		printf("The operands for the mathmatical operation were of different types! Please cast them to the same type.\n");
		return 1;
	} else if (e == 5) {
		printf("Out of memory!\n");
		return 6;
	} else if (e == 6) {
		printf("Warning: too much data for type 'double'\n");
		return 1;
	} else if (e == 7) {
		printf("Warning: too much data found for type 'int': may be out of memory, corrupt or compiler error\n");
		return 1;
	} else {
		printf("An error occurred: Unknown error (Code %d)\n", e);
		return 1;
	}
}

int castint() {
	int length = stack[stackpointer];
	stackpointer--;
	int type = stack[stackpointer];
	stackpointer--;
	
	char str[2];
	char buffer[length];
	memset(buffer, 0, length);
	char *ptr;
	if (type == 0) {
		for (int i = 0; i < length; i++) {
			memset(str, 0, 2); //reset 'str'
			sprintf(str, "%c", stack[stackpointer]); //get the char for the ascii value on the top of the stack
			strcat(buffer, str); //add it to the buffer
			stackpointer--; //get next value read
		}
		//int result = (int)strtol(buffer, &ptr, 10);
	} else if (type == 2) {
		return error(1);
	} else if (type == 3) {
		int exponent;
		int before_dp;
		int after_dp;
		for (int i = 0; i < length; i++) {
			if (i == 0) {
				exponent = stack[stackpointer];
			} else if (i == 1) {
				before_dp = stack[stackpointer];
			} else if (i == 2) {
				after_dp = stack[stackpointer];
			} else {
				error(6);
			}
		}
		double result;
		result = (double)after_dp;
		for (int i = 0; i < exponent; i++) {
			result /= 10;
		}
		result += before_dp;
		printf("%f\n", result * 1000000);
		
	} else if (type == 6 || type == 1) {
		//int result = stack[stackpointer];
	}
	int result;
	stackpointer++;
	stack[stackpointer] = result;
	stackpointer++;
	stack[stackpointer] = 1; //int is type 1
	stackpointer++;
	stack[stackpointer] = 1; //int has length of 1
	return 0;
}

int caststr() {
	return 0;
}

int castdbl() {
	return 0;
}

void pstack() {
	printf("STACKPOINTER: %d\n", stackpointer);
	char s_ptr_index[64];
	int length;
	for (int i = 0; i < 40; i++) {
		memset(s_ptr_index, 0, 64);
		sprintf(s_ptr_index, "%d ", stack[i]);
		printf(s_ptr_index);
		if (i < stackpointer) {
			length += strlen(s_ptr_index);
		}
	}
	printf("\n");
	for (int i = 0; i < length; i++) {
		printf(" ");
	}
	printf("^\n");
}

void pheap() {
	printf("VARPTR: %d\n", var_ptr);
	char s_ptr_index[64];
	int length;
	for (int i = 0; i < 40; i++) {
		memset(s_ptr_index, 0, 64);
		sprintf(s_ptr_index, "%d ", heap[i]);
		printf(s_ptr_index);
		if (i <= var_ptr) {
			length += strlen(s_ptr_index);
		}
	}
	printf("\n");
	for (int i = 0; i < length; i++) {
		printf(" ");
	}
	printf("^\n");
}

void pvars() {
	for (int index = 0; index < last_var; index++) {
		int name = var[index];
		
		int length = heap[name];
		int type = heap[name + 1];
		for (int i = 0; i < length; i++) {
			printf("%d", heap[name + i + METASIZE]);
		}
		printf(" TYPE: %d LENGTH: %d", type, length);
		printf("\n");
	}
}

void load_value(int index) {
	int name = var[index];
	
	if (debug == 1) {
		printf("INDEX %d; NAME %d;\n", index, name);
	}
	
	int length = heap[name];
	int type = heap[name + 1];
	int result[length];
	for (int i = 0; i < length; i++) {
		result[i] = heap[name + i + METASIZE];
	}
	//push the result
	for (int i = 0; i < length; i++) {
		stackpointer++;
		stack[stackpointer] = result[i];
	}
	stackpointer++;
	stack[stackpointer] = type; 
	stackpointer++;
	stack[stackpointer] = length; //stack is now [data], type, length
}

void init_value() {
	//pop to 'buffer' 3769866304
	int length = stack[stackpointer];
	stackpointer--;
	int type = stack[stackpointer];
	stackpointer--;
	
	int buffer[length];
	
	for (int i = 0; i < length; i++) {
		buffer[i] = stack[stackpointer];
		stackpointer--;
	}
	var_ptr++;
	heap[var_ptr] = length;
	name_ptr++;
	var[name_ptr] = var_ptr;
	var_ptr++;
	heap[var_ptr] = type;
	
	if (debug == 1) {
		printf("DEBUG var %d created\n", name_ptr);
	}
	
	for (int i = length - 1; i > -1; i--) {
		var_ptr++;
		heap[var_ptr] = buffer[i];
	}
	last_var++;
}

void store_value(int index) {
	int name = var[index];
	if (debug == 1) {
		printf("INDEX %d; NAME %d;\n", index, name);
	}
	int var_length = heap[name];
	int length = stack[stackpointer];
	stackpointer--;
	int type = stack[stackpointer];
	stackpointer--;
	
	int buffer[length];
	
	for (int i = 0; i < length; i++) {
		buffer[i] = stack[stackpointer];
		stackpointer--;
	}
	if (length <= var_length) {
		heap[name] = length;
		heap[name + 1] = type;
		if (debug == 1) {
			printf("DEBUG var %d can fit! Overwriting...\n", index);
		}
		for (int i = 0; i < length; i++) {
			heap[name + i + METASIZE] = buffer[i];
		}
	} else {
		var_ptr++;
		heap[var_ptr] = length;
		var_ptr++;
		heap[var_ptr] = type;
		var[index] = var_ptr;
		if (debug == 1) {
			printf("DEBUG var %d was too big! copying...\n", index);
		}
		for (int i = 0; i < length; i++) {
			var_ptr++;
			heap[var_ptr] = buffer[i];
		} 
	}
}

void _defrag() {
	//pass
}

void swap() {
	//pop
	int length = stack[stackpointer];
	stackpointer--;
	int type = stack[stackpointer];
	stackpointer--;
	
	int buffer[length];
	
	for (int i = 0; i < length; i++) {
		buffer[i] = stack[stackpointer];
		stackpointer--;
	}
	//pop
	int length_2 = stack[stackpointer];
	stackpointer--;
	int type_2 = stack[stackpointer];
	stackpointer--;
	
	int buffer_2[length];
	
	for (int i = 0; i < length; i++) {
		buffer_2[i] = stack[stackpointer];
		stackpointer--;
	}
	
	//push back again
	for (int i = length - 1; i <= 0; i++) {
		stackpointer++;
		stack[stackpointer] = buffer[i];
	}
	stackpointer++;
	stack[stackpointer] = type;
	stackpointer++;
	stack[stackpointer] = length;
	
	for (int i = length_2 - 1; i <= 0; i++) {
		stackpointer++;
		stack[stackpointer] = buffer_2[i];
	}
	stackpointer++;
	stack[stackpointer] = type_2;
	stackpointer++;
	stack[stackpointer] = length_2;
}


void rev() { //reverse the order of a multi-length item on the stack
	//pop
	int length = stack[stackpointer];
	stackpointer--;
	int type = stack[stackpointer];
	stackpointer--;
	
	int buffer[length];
	int ptr = -1;
	
	for (int i = 0; i < length; i++) {
		buffer[ptr] = stack[stackpointer];
		ptr++;
		stackpointer--;
	}
	//push back again (reverses direction)
	for (int i = 0; i < length; i++) {
		stackpointer++;
		stack[stackpointer] = buffer[i];
	}
	stackpointer++;
	stack[stackpointer] = type;
	stackpointer++;
	stack[stackpointer] = length;
}

void load_const(int index) {
	int length = data[index];
	index++;
	int type = data[index];
	for (int i = length; i > 0; i--) {
		stackpointer++;
		stack[stackpointer] = data[i + index];
	}
	stackpointer++;
	stack[stackpointer] = type;
	stackpointer++;
	stack[stackpointer] = length;
}

void jump() {
	stackpointer--; //discard length; result should be 64bit int so length 1
	int type = stack[stackpointer];
	stackpointer--;
	
	if (type != 1 && type != 6) { //if it's not a 64(32)bit int (length 1) then...
		error(3); //error
	} else { //if correct type then jump
		pc = stack[stackpointer] - 1; //-1 because the PC gets incremented afrer each instruction
	}
}

void jumpf() {
	if (flag == 0) { //if the last compare returned true...
		//jump
		stackpointer--; //discard length; result should be 64bit int so length 1
		int type = stack[stackpointer];
		stackpointer--;
		
		if (type != 1 && type != 6) { //if it's not a 64bit int (length 1) then...
			error(3); //error
		} else { //if correct type then jump
			pc = stack[stackpointer] - 1;
			stackpointer--;
		}
	} else { //if it returned false...
		stackpointer -= 3; //remove address from the stack
		//do nothing: advance to the next instruction
	}
}

void compare() {
	//compares the top two values on the stack and sets "flag" accordingly
	
	int lengthof_a = stack[stackpointer];
	stackpointer--;
	int typeof_a = stack[stackpointer];
	stackpointer--;
	int a[lengthof_a];
	
	for (int i = 0; i < lengthof_a; i++) {
		a[i] = stack[stackpointer];
		stackpointer--;
	}
	
	int lengthof_b = stack[stackpointer];
	stackpointer--;
	int typeof_b = stack[stackpointer];
	stackpointer--;
	int b[lengthof_b];
	
	for (int i = 0; i < lengthof_b; i++) {
		b[i] = stack[stackpointer];
		stackpointer--;
	}
	
	if (typeof_a != typeof_b) {
		flag = 0;
		return;
	}
	
	if (lengthof_a != lengthof_b) {
		flag = 0;
		return;
	} else {
		for (int i = 0; i < lengthof_a; i++) {
			if (a[i] != b[i]) {
				flag = 0;
				return;
			}
		}
		flag = 1;
	}
	
}

void prints() {
	//print the top of the stack
	int length = stack[stackpointer];
	stackpointer--;
	int type = stack[stackpointer];
	stackpointer--;
	
	//printf("%d\n", type);
	
	if (type == 3) {
		int exponent;
		int before_dp;
		int after_dp;
		
		exponent = stack[stackpointer];
		//before_dp = stack[stackpointer - 1];
		after_dp = stack[stackpointer - 2];
		stackpointer -= 3;
		if (length > 3) {
			error(6);
		}
		double result;
		result = (double)after_dp;
		for (int i = 0; i < exponent; i++) {
			result /= 10;
		}
		printf("%.16f", result);
	} else if (type == 2) {
		if (stack[stackpointer] == 0) {
			printf("False");
		} else {
			printf("True");
		}
		stackpointer--;
	} else if (type == 0) {
		for (int i = 0; i < length; i++) {
			printf("%c", stack[stackpointer]);
			stackpointer--;
		}
	} else if (type == 1) {
		if (length != 1) {
			error(7);
		}
		printf("%d", stack[stackpointer]);
		stackpointer--;
	}
	printf("\n");
}

void usr_input() {
	char buf[100];
	fgets(buf, 100, stdin);
	printf("%s\n", buf);
}

void do_maths(char* op) {
	int result;
	
	int lengthof_a = stack[stackpointer];
	stackpointer--;
	int typeof_a = stack[stackpointer];
	stackpointer--;
	int a[lengthof_a];
	
	for (int i = 0; i < lengthof_a; i++) {
		a[i] = stack[stackpointer];
		stackpointer--;
	}
	
	int lengthof_b = stack[stackpointer];
	stackpointer--;
	int typeof_b = stack[stackpointer];
	stackpointer--;
	int b[lengthof_b];
	
	for (int i = 0; i < lengthof_b; i++) {
		b[i] = stack[stackpointer];
		stackpointer--;
	}
	
	if (typeof_a != typeof_b) {
		error(4);
	} else {
		if (typeof_a == 1 || typeof_a == 6) {
			if (op == '+') {
				result = a[0] + b[0];
			} else if (op == '-') {
				result = a[0] - b[0];
			} else if (op == '*') {
				result = a[0] * b[0];
			} else if (op == '/') {
				result = a[0] / b[0];
			}
		} else if (typeof_a == 3) {
			int exponent;
			int before_dp;
			int after_dp;
			if (lengthof_a != lengthof_b) {
				error(6);
			}
			for (int i = 0; i < lengthof_a; i++) {
				if (i == 0) {
					exponent = stack[stackpointer];
				} else if (i == 1) {
					before_dp = stack[stackpointer];
				} else if (i == 2) {
					after_dp = stack[stackpointer];
				} else {
					error(6);
				}
			}
			double result;
			result = (double)after_dp;
			for (int i = 0; i < exponent; i++) {
				result /= 10;
			}
		} else if (typeof_a == 0) {
			if (op == "+") {
				int result[lengthof_a + lengthof_b];
				//result = strcat(a, b);
			} else {
				printf("Wrong operation for type 'string'\n");
			}
			stackpointer++;
			//stack[stackpointer] = result;
			stackpointer++;
			//stack[stackpointer] = sizeof(result) / sizeof(int);
		} else if (typeof_a == 2 || typeof_a == 4 || typeof_a == 5) {
			printf("Mathmatical operations not currenetly supported on type &d\n", typeof_a);
		}
	}
}

void rep() {
	//duplicate the top of the stack
	
	//pop off the top item
	int length = stack[stackpointer];
	stackpointer--;
	int result[length + 1];
	for (int i = 0; i < length; i++) {
		result[i] = stack[stackpointer];
		stackpointer--;
	}
	
	for (int i = 0; i < 2; i++) {
		//push 'result' twice
		
		for (int j = 0; j < length; j++) { //push the data
			stackpointer++;
			stack[stackpointer] = result[j];
		}
		//push the length
		stackpointer++;
		stack[stackpointer] = length;
	}
}

void push_pc() {
	stack[stackpointer + 0] = pc;
	stack[stackpointer + 1] = 1;
	stack[stackpointer + 2] = 1;
	stackpointer += 3;
}

void usage(char * argv[]) {
	printf("Usage: %s [filename | -h | --help]\n", argv[0]);
	printf("%s                  [-v, --verbose]\n", argv[0]);
	printf("%s                  [-d, --debug]\n", argv[0]);
}

int execute(char * str_code, int operand) {
	printf("%s %d", str_code, operand);
	char *ptr;
	int code = (int)strtol(str_code, &ptr, 10);
	int e;
	if        (code == 0)  {	 			//pass
	} else if (code == 1)  { load_const(operand);  //load_const
	} else if (code == 2)  { load_value(operand);  //load_value
	} else if (code == 3)  { init_value();  //init_value
	} else if (code == 4)  { store_value(operand); //store_value
	} else if (code == 5)  { do_maths("+"); //add_values
	} else if (code == 6)  { do_maths("-"); //sub_values
	} else if (code == 7)  { do_maths("*"); //mul_values
	} else if (code == 8)  { do_maths("/"); //div_values
	} else if (code == 9)  { compare();     //compare
	} else if (code == 10) { jump();        //jump
	} else if (code == 11) { jumpf();       //jump_if_false
	} else if (code == 12) { prints();      //print_value
	} else if (code == 13) { usr_input();	//input
	} else if (code == 14) { rep();			//dupl
	} else if (code == 15) { rev();			//reverse
	} else if (code == 16) { swap();		//swap
	} else if (code == 17) { e = castint();	//int(top_of_stack)
	} else if (code == 18) { e = caststr();	//str(top_of_stack)
	} else if (code == 19) { e = castdbl();	//double(top_of_stack)
	} else { return 16; }
	if (debug == 1) {
		pstack();
		pheap();
	}
	if (!(e == 0)) {
		int fatal = error(e);
		if (fatal == 1) {
			return e;
		}
	}
	return 0;
}

int main(int argc, char *argv[]) {
	if (argc <= 1) {
	    prompt = 1;
    } else {
		prompt = 0;
		if (strcmp(argv[1], "-h") == 0 || strcmp(argv[1], "--help") == 0) {
			 usage(argv);
		} else {
			FILE *file = fopen(argv[1], "r");
			if (file == 0) {
				int fatal = error(2);
				if (fatal == 1) { return 2; }
			} else {
				int x;
				char str[32];
				memset(str, 0, 32);
				int ptr = 0;
				char *ptr_0;
				int section = 0;
				
				int temp_flag = 0;
				int file_len;
				int file_len_data;
				x = fgetc(file);
				while (x != EOF) {
					//printf("%c", x);
					if (!(x == ',' || x == '\n')) {
						if (x != ' ') {
							char str_copy[32];
							memcpy(str_copy, str, 32);
							sprintf(str, "%s%c", str_copy, x);
							printf("%s\n", str);
						}
					} else if (x == ',' && section == 0) {
						if (temp_flag == 0) {
							temp_flag = 1;
							file_len = (int)strtol(str, &ptr_0, 10);
							code = malloc((file_len * sizeof(int)) + 16); //allocate expected memory plus 16 bytes for error
							memset(str, 0, 32); //reset string
							if (code == NULL) {
								return error(5); //out of memory
							}
						} else {
							codelength++;
							code[ptr] = (int)strtol(str, &ptr_0, 10);
							memset(str, 0, 32);
							ptr++;
						}
					} else if (x == ',' && section == 1) {
						if (temp_flag == 0) {
							temp_flag = 1;
							file_len_data = (int)strtol(str, &ptr_0, 10);
							data = malloc((file_len * sizeof(int)) + 16); //allocate expected memory plus 16 bytes for error
							memset(str, 0, 32); //reset string
							if (code == NULL) {
								return error(5); //out of memory
							}
						} else {
							datalength++;
							data[ptr] = (int)strtol(str, &ptr_0, 10);
							memset(str, 0, 32);
							ptr++;
						}
					} 
					if (x == '\n') {
						section = 1;
						ptr = 0;
						temp_flag = 0;
						memset(str, 0, 32);
					}
					x = fgetc(file);
					printf("%d\n", x == EOF);
				}
				if (debug == 1) {
					for (int i = 0; i < 16; i++) {
						printf("%d,", code[i]);
					}
					printf("\n");
					for (int i = 0; i < 16; i++) {
						printf("%d,", data[i]);
					}
					printf("\n");
				}
				fclose(file);
				if (codelength != file_len || datalength != file_len_data) {
					printf("%d %d\n %d %d\n", codelength, file_len, datalength, file_len_data);
					
					return error(2);
				}
			}
		}
		
    }
	if (argc >= 3) {
		for (int i = 2; i < argc; i++) {
			if (strcmp(argv[i], "-v") == 0 || strcmp(argv[i], "--verbose") == 0) {
				debug = 1;
			} else if (strcmp(argv[i], "-d") == 0 || strcmp(argv[i], "--debug") == 0) {
				step = 1;
			}
		}
	}
	char cmd[100];
	while(pc < codelength) {
		if (step == 1) {
			while (1) {
				memset(cmd, 0, 100);
				printf("> ");
				fgets(cmd, 100, stdin);
				char ** ops = str_split(cmd, ' ');
				if (strcmp("advance\n", cmd) == 0) {
					printf("\n");
					break;
				} else if (strcmp("stack\n", cmd) == 0) {
					pstack();
				} else if (strcmp("heap\n", cmd) == 0) {
					pheap();
				} else if (strcmp("var\n", cmd) == 0) {
					pvars();
				} else if (strcmp("instr\n", cmd) == 0) {
					pinstr();
				} else if (strcmp("data\n", cmd) == 0) {
					pdata();
				} else if (strcmp("var_ref\n", cmd) == 0) {
					pvar_ref();
				} else if (strcmp("flag\n", cmd) == 0) {
					printf("%d\n", flag);
				} else if (strcmp("exec", ops[0]) == 0) {
					int operand;
					if (sizeof(ops) > 1) {
						char * s_op = ops[2];
						char * ptr;
						operand = (int)strtol(s_op, &ptr, 10);
					} else {
						operand = 0;
					}
					execute(ops[1], operand);
				} else if (strcmp("help\n", cmd) == 0) {
					printf("advance: advances to the next instruction\n");
					printf("stack  : prints the stack\n");
					printf("heap   : prints the heap\n");
					printf("var    : prints the currently defined variables\n");
					printf("instr  : prints the instruction that will be executed next\n");
					printf("data   : prints the static constants\n");
					printf("var_ref: prints the addresses in the heap for each variable\n");
					printf("exec   : executes the argument as bytecode\n");
					printf("help   : prints this message\n");
				} else {
					if (strcmp("\n", cmd) != 0) {
						printf("Unknown command: try 'help' for a list\n");
					}
				}
			}
		}
		int e = 0;
		if (debug == 1) {
			printf("CODE %d\n", code[pc]);
		}
		if        (code[pc] == 0)  { pc++; 			//pass
		} else if (code[pc] == 1)  { load_const(code[pc + 1]); pc += 2; //load_const
		} else if (code[pc] == 2)  { load_value(code[pc + 1]); pc += 2; //load_value
		} else if (code[pc] == 3)  { init_value(); pc++;				//init_value
		} else if (code[pc] == 4)  { store_value(code[pc + 1]); pc += 2;//store_value
		} else if (code[pc] == 5)  { do_maths("+"); pc++;				//add_values
		} else if (code[pc] == 6)  { do_maths("-"); pc++;				//sub_values
		} else if (code[pc] == 7)  { do_maths("*"); pc++;				//mul_values
		} else if (code[pc] == 8)  { do_maths("/"); pc++;				//div_values
		} else if (code[pc] == 9)  { compare(); pc++;    				//compare
		} else if (code[pc] == 10) { jump(); pc++;       				//jump
		} else if (code[pc] == 11) { jumpf(); pc++;      				//jump_if_false
		} else if (code[pc] == 12) { prints(); pc++;     				//print_value
		} else if (code[pc] == 13) { usr_input(); pc++;					//input
		} else if (code[pc] == 14) { rep();	 pc++;						//dupl
		} else if (code[pc] == 15) { rev(); pc++;						//reverse
		} else if (code[pc] == 16) { swap(); pc++;						//swap
		} else if (code[pc] == 17) { e = castint(); pc++;				//int(top_of_stack)
		} else if (code[pc] == 18) { e = caststr(); pc++;				//str(top_of_stack)
		} else if (code[pc] == 19) { e = castdbl(); pc++;				//double(top_of_stack)
		} else { return 16; }
		if (debug == 1) {
			pstack();
			pheap();
		}
		if (!(e == 0)) {
			int fatal = error(e);
			if (fatal == 1) {
				return e;
			} else {
				continue;
			}
		}
	}
	return 0;
}