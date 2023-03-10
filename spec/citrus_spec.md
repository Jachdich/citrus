
# Protocols

A protocol is a set of features that a struct must have. This can include associated functions and members. Here is an example of a protocol definition:

```
Add: protocol {
    __add__: fn(self: Self*, other: Self*) -> Self;
}
```

The special value `Self` refers to whichever type the protocol is being implemented on. Here's an example of implementing a protocol:

```
MyNumber: struct(Add) {
    inner: i32;
}

// if we don't implement this function, the compiler will complain!
MyNumber::__add__: fn(self: MyNumber*, other: MyNumber*) -> MyNumber =
    MyNumber { inner: self.inner + other.inner };
```
