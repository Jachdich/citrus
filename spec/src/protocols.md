# Protocols

A protocol is a set of features that a struct must have. This can include associated functions and members. Unlike rust traits or java interfaces, protocols do not allow for any kind of polymorphism. They are just a tool to better specify what can be passed into a function, as duck typing can be ambiguous. The special value `Self` refers to whichever type the protocol is being implemented on. Here is an example of a protocol definition:

```citrus
Shape: protocol {
    calculate_area: fn(self: Self*) -> f64;
    get_radius: fn(self: Self*) -> f64;
    radius: f64;
}
```

You can implement default methods on protocols, to allow code reuse:

```citrus
//TODO this syntax is MID!
// Since get_radius is the same for all shapes, it makes sense to implement it here
Shape::get_radius: fn(self: Self*) -> f64 = self.radus;

// It's implemented like a generic function, with added sugar
get_radius: fn<T: Shape>(self: T*) -> f64 = self.radius;
```

Here's an example of implementing a protocol on a struct:

```citrus
Square: struct(Shape) {
    radius: f64;
    colour: u32;
}

Square::calculate_area: fn(self: Square*) -> f64 = self.radius * self.radius * 4;
```

## Anonymous protocols

If you don't want to create a named protocol, then you can define features a struct must have anonymously. A consequence of this is that the protocol is checked against whatever struct is passed in, instead of requiring the struct to explicitly implement the protocol. This allows for what is effectively still duck typing but with better error reporting. Here's an example of defining an anonymous protocol:

```citrus
do_something: fn<T, U>(var: T) -> U 
    T with (a: fn(Self*, i32), c: U),
    U with (foo: fn(i32)), 
= {
    var.a(1);
    var.c.foo(6);
    var.c
}
```

Or alternatively the syntax could be

```citrus
do_something: fn<T, U>(var: T) -> U where
    T has (a: fn(Self*, i32), c: U),
    U has (foo: fn(i32)), 
= {
    var.a(1);
    var.c.foo(6);
    var.c
}
```
