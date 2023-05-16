# Structs

Structs are defined like this:

```citrus
StructName: struct {
    member_a: f64;
    radius: i16;
    others: Vec<SomeOtherStruct>;
}
```

## Associated functions

AKA methods, are functions defined on a struct. Citrus implements a version of (Uniform Function Call Syntax)[https://en.wikipedia.org/wiki/Uniform_Function_Call_Syntax], where the function `foo` defined on the type `Bar` is the same as the function `Bar_foo` with the first parameter being of type `Bar*`.

Associated functions are defined by using the namespacing operator (`::`) in the same way that they can be used:

```citrus
StructName::foo: func(StructName *self) = ...;
```