void putd(long);

long add_maybe(long a, long b) {
  putd(a);
  putd(b);
  return a + b;
}

void main() {
  putd(add_maybe(1, 1));
}