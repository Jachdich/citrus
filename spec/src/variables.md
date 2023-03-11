# Variables

Variables are defined using `let` (immutable) or `mut` (mutable):

```citrus
let a = 6;
mut counter = 0;
counter += 1;
```

# Types

The built in types are similar to rust: `u8` to `u64` for unsigned ints, `i8` to `i64` for signed ints, `f32` and `f64` for floating point numbers, `char` is (probably) equivalent to `i8`, and `bool` is either `true` or `false`.

## Types in liblemon

- `String`: Immutable array of `char`s  
- `Vec`: Resizable generic array

TODO: more