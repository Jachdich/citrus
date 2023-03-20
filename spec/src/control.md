# Control flow

Most of the control flow in citrus is the same as rust, and very similar to C, C++, java, js, etc.

## If statements

No parentheses needed:

```citrus
if a == b {
    print("Equal");
} elif a > b {
    print("More")
} else {
    print("Less");
}
```

If statements are also expressions, like in rust:

```citrus
let a = if a == b {
    6
} elif a > b {
    7
} else {
    8
};
```

## While loops

```citrus
while a == b {
    // break and continue supported as usual
    if c == d {
        continue;
    }
    if e == f {
        break;
    }
}
```

## For loops

Like python, loop over an iterator:

```citrus
for n in some_iter {
    print(n);
}
```

`range` function would do ranges like python as well.

## Match statements

TODO idk how to do these, do I want it as powerful as rust & python or simple like C or somewhere inbetween?

Also can be used as expressions like `if`s.
