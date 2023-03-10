# Functions

Functions are defined like this:  
```
function_name: fn(args) -> ret_type = expr[;]
```

Function definitions can optionally end with a semicolon, which is useful when defining a single expression function. In that example, `expr` can represent either a single expression, a compound statement or a compound expression (which is a compound statement that ends with a single expression). This leads to two styles of function definitions:

```
add: fn(a: i32, b: i32) -> i32 = a + b;
```
and
```
add: fn(a: i32, b: i32) -> i32 = {
    let result = a + b; // you can use statements in here
    result // final line must be expression: note lack of ;
}
```

## Generic functions

Citrus supports primitive generics, similar to very basic C++ templates:
```
add: fn<T>(a: T, b: T) -> T = a + b;
```

The generic names are specified inside <angle brackets>. The actual type of each generic will be infered from where the function is called. In this case, `T` will be substituted as `f64`:

```
let result = add(12.0, 24.0);
```

**EXPERIMENTAL**

Generics can require types to adhere to a specific protocol (see the Protocols section), although specifying a protocol is not necessary and allows for duck typing if omitted. Protocols can be specified like this:

```
add: fn<T: Add>(a: T, b: T) -> T = a + b;
```

That implicitly calls `a.__add__(b)`, thus the `Add` protocol is needed. Here's a clearer example:

```
print: fn<T: ToString>(value: T) = println(value.to_string());

ToString: protocol {
    to_string: fn(self: Self*) -> String;
}
```

