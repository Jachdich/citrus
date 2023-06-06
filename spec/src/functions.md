# Functions


IDEAS:

```citrus
// previous syntax idea would be using : like this
// but that is a bit weird cos normally the : dictates the type not the value
Befunge: struct {
    a: i32;
    b: i64;
    do_something: fn(self: Befunge*) = |self| self.a;
    something_else: fn(self: Befunge*) {
        a
    }

}
// perhaps dictate the type and then follow it by a lambda?
let add: fn(a, b: i32) = |a, b| a + b;

// or, omit the type directly and just set the instance variable to a lambda
let Befunge = struct {
    a: i32;
    b: i32 = 1;
    c: fn(self: Befunge*) = fn(self: Befunge*) {

    };
    d = fn(self: Befunge*) = self.a;
}

let Befunge::init = fn(self: Befunge*) {
    self.c();
    self.d();
}

let Befunge::get_a = fn(self: Befunge) = self.a;


// that would lead to syntax like this
let add = fn(a, b: i32) = a + b;

// perhaps after the variable is declared with the type of fn(...), whatever comes after the = is coerced to code
// like how `let a: i64 = 6;` coerces 6 to an i64.

let add: fn(a, b: i32) = a + b;

// which is baiscally what I had before but with a `let`

// anyway, I hate syntax, time to sleep.
```


Functions are defined like this:  
```citrus
function_name: fun(args) -> ret_type = expr[;]
```

Function definitions can optionally end with a semicolon, which is useful when defining a single expression function. In that example, `expr` can represent either a single expression, a compound statement or a compound expression (which is a compound statement that ends with a single expression). This leads to two equivalent styles of function definitions:

```citrys
add: fun(a: i32, b: i32) -> i32 = a + b;
```
and
```citrus
add: fun(a: i32, b: i32) -> i32 = {
    let result = a + b; // you can use statements in here
    result // final line must be expression: note lack of ;
}
```

## Generic functions

Citrus supports basic generics, similar to very basic C++ templates:
```citrus
add: fun<T>(a: T, b: T) -> T = a + b;
```

The generic names are specified inside <angle brackets>. The actual type of each generic will be infered from where the function is called. In this case, `T` will be substituted as `f64`:

```citrus
let result = add(12.0, 24.0);
```

### (experimental) Protocols

Generics can require types to adhere to a specific protocol (see the [Protocols](protocols.md) chapter for more detail). Specifying a protocol is not necessary and allows for duck typing if omitted, but gives more information about what types can be passed to a function and allow for better error messages. Protocols can be specified with a `:` after a generic name, like this:

```citrus
print: fun<T: ToString>(value: T) = println(value.to_string());
```

The `ToString` protocol may be defined like this:

```citrus
ToString: protocol {
    to_string: fun(self: Self*) -> String;
}
```

Implicit protocols are covered in the [Protocols](protocols.md) chapter.

## Default & named arguments

Any argument can be specified using a name, regardless of order:

```citrus
// better date order here
print_date: fun(day: i32, month: i32, year: i32) = {
    // implementation
}

main: fun() -> i32 = {
    // but you can use the worse order if you want
    print_date(month=3, day=12, year=2029); // citrus release date
    print_date(month=3, 12, 2029); // ERROR! Can't use unnamed arguments after named
    0
}
```

After a single named argument is specified, the rest of the arguments must be named as well otherwise the order is ambiguous.

Default arguments **must** be named, and can be declared and used like this:

```citrus
// assume the year hasn't changed yet lol
print_date: fun(day: i32, month: i32, year: i32 = 2023) = {
    // implementation
}

main: fun() -> i32 = {
    print_date(3, 12, 2029); // ERROR! default arguments must be named
    print_date(3, 12, year=2029); // better
    print_date(1, 1); // also ok
    0
}
```

## fn, proc, proc$

Basically, anything declared `fun` is a _pure function_^*, and anything declared `proc` is a procedure that is allowed to cause side effects. `proc`s can call other `proc`s or `fun`s, whereas `fun`s can only call other `fun`s.

*Not really pure: normally, pure functions cannot mutate anything, but I thought that was a bit restrictive for a low level language such as this.

Allowed in `fun`s:
    - Any kind of conditions, control flow, loops, arithmatic, etc.
    - Reading and mutating stack arrays declared inside the function
    - Reading and mutating memory explicitly passed in as a parameter

Disallowed:
    - Accessing files, printing, or performing any kind of IO
    - Accessing global variables, or any memory address not passed in to the function (excluding positive integer offsets from pointers passed in)
    - Allocating or freeing memory


To make memory allocation clear, any procedure that allocates memory is suffixed `$`, and declared with `proc$`.

```citrus
Vec: struct {
    // ... internals
}

Vec::new: proc$() -> Vec {
    // allocate memory
    let a = malloc$(69);
    // other stuff
}

main: proc$() -> i32 {
    mut some_vec = Vec::new$();
}

foo: proc() {
    mut some_vec = Vec::new(); // ERROR! Vec::new allocates memory, must add $ suffix
    mut some_vec = Vec::new$(); // ERROR! Allocating memory in a procedure not marked proc$
}
```