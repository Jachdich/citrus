#include <stdio.h>
#include <stdint.h>

struct Test {
  int a;
  int b;
  int c;
  int d;
};

struct Test fn() {
  return (struct Test){1, 2, 3, 4};
}

int main() {
    struct Test test = fn();
    return test.a + test.b + test.c + test.d;
}