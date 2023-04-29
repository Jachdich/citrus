# Control flow

## If statements & expressions

Basically like 

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

```citrus


```