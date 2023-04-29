# Control flow


## Loops

In all loops, `break` and `continue` work as expected.

### While loops

While loops can be fairly normal like so:
```citrus
let cond = true;
while cond {
    if magic {
        cond = false;
    }
}
```

But can also support iterating variables, either externally declared, or declared inside the scope using `with`:
```citrus
let i = 0;
while i < 5; i++ {
    
}

with i = 0 while i < 5; i++ {
    
}
```

### For loops

Foreach (aka python- or rust-style) for loops:
```citrus
for i in 0..5 {
    
}
```

Alternative range definition:
```citrus
for 0 <= i < 10 {
    
}
```

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

## Match statements

TODO idk how to do these, do I want it as powerful as rust & python or simple like C or somewhere inbetween?

Also can be used as expressions like `if`s.
