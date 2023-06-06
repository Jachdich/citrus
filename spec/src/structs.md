# Datastructures

## Structs

Structs are defined like this:

```citrus
StructName: struct {
    member_a: f64;
    radius: i16;
    others: Vec<SomeOtherStruct>;
}
```

### Associated functions

AKA methods, are functions defined on a struct. Citrus implements a version of (Uniform Function Call Syntax)[https://en.wikipedia.org/wiki/Uniform_Function_Call_Syntax], where the function `foo` defined on the type `Bar` is the same as the function `Bar_foo` with the first parameter being of type `Bar*`.

Associated functions are defined by using the namespacing operator (`::`) in the same way that they can be used:

```citrus
const StructName::foo = fn(StructName *self) = self.value;
```

## Enums

Enums are C-like.

## Unions

## Errors

## Bitflags

## Tuples

Tuples are essentially arrays with length known at compile-time, but that can contain multiple different datatypes. They're useful for returning multiple values from functions, or otherwise grouping data without having to create a dedicated struct. Tuples can be created with a comma, like in python. They can also be deconstructed in a similar manner.

Example use of tuples:
```citrus
// swap a and b, by constructing and deconstructing a tuple.
let a, b = b, a;

const divmod = fn(a, b: i32) -> (i32, i32) {
    return a / b, a % b;
}

// alternatively, infer the return type with `=` syntax
const divmod = fn(a, b: i32) = a / b, a % b;

let quotient, remainder = divmod(1, 2);

```