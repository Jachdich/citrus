# Functions

Functions are defined like this:  
```citrus
function_name: fn(args) -> ret_type = expr[;]
```

Function definitions can optionally end with a semicolon, which is useful when defining a single expression function. In that example, `expr` can represent either a single expression, a compound statement or a compound expression (which is a compound statement that ends with a single expression). This leads to two equivalent styles of function definitions:

```citrys
add: fn(a: i32, b: i32) -> i32 = a + b;
```
and
```citrus
add: fn(a: i32, b: i32) -> i32 = {
    let result = a + b; // you can use statements in here
    result // final line must be expression: note lack of ;
}
```

## Generic functions

Citrus supports primitive generics, similar to very basic C++ templates:
```citrus
add: fn<T>(a: T, b: T) -> T = a + b;
```

The generic names are specified inside <angle brackets>. The actual type of each generic will be infered from where the function is called. In this case, `T` will be substituted as `f64`:

```citrus
let result = add(12.0, 24.0);
```

### **EXPERIMENTAL** Protocols

Generics can require types to adhere to a specific protocol (see the [Protocols](protocols.md) chapter for more detail). Specifying a protocol is not necessary and allows for duck typing if omitted, but gives more information about what types can be passed to a function and allow for better error messages. Protocols can be specified with a `:` after a generic name, like this:

```citrus
print: fn<T: ToString>(value: T) = println(value.to_string());
```

The `ToString` protocol may be defined like this:

```citrus
ToString: protocol {
    to_string: fn(self: Self*) -> String;
}
```

Implicit protocols are covered in the [Protocols](protocols.md) chapter.

## Default & named arguments

Any argument can be specified using a name, regardless of order:

```citrus
// better date order here
print_date: fn(day: i32, month: i32, year: i32) = {
    // implementation
}

main: fn() -> i32 = {
    // but you can use the worse order if you want
    print_date(month=3, day=12, year=2029); // citrus release date
    print_date(month=3, 12, 2029); // ERROR!
    0
}
```

After a single named argument is specified, the rest of the arguments must be named as well otherwise the order is ambiguous.

Default arguments **must** be named, and can be declared and used like this:

```citrus
// assume the year hasn't changed yet lol
print_date: fn(day: i32, month: i32, year: i32 = 2023) = {
    // implementation
}

main: fn() -> i32 = {
    print_date(3, 12, 2029); // ERROR!
    print_date(3, 12, year=2029); // better
    print_date(1, 1); // also ok
    0
}
```