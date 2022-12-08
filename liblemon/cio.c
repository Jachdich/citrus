#include <stdio.h>

typedef struct {
  unsigned long length;
  char *data;
} String;

void putd(int d) {
  printf("%d\n", d);
}

void putstr(String *s) {
  for (unsigned long i = 0; i < s->length; i++) {
    putc(s->data[i], stdout);
  }
  putc('\n', stdout);
}