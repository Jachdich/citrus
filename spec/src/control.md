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
mut i = 0;
while i < 5, i++ {
    
}

with mut i = 0, while i < 5, i++ {
    
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

If each branch has only a single expression, the curly braces can be omitted: (Maybe, it could cause parsing issues so I might not add this)

```citrus
let a = if a == b 6 else 7;
```

## Match statements

TODO idk how to do these, do I want it as powerful as rust & python or simple like C or somewhere inbetween?

Like if statements, match statements can be used as expressions. Variables can be matched against literal values, ranges (for numbers), lists of acceptable values, and other variables:
```citrus
let x = 3;
let compare_to = 30;
let description = match x {
    0 => "zero",
    1..10 => "small",
    69, 420 => "funny",
    compare_to => "equal to variable: " + compare_to.to_string()
    else => "other: " + x.to_string(),
};
```
