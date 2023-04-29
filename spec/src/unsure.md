# Things I'm not certain on

## `proc` and `fn`

An idea I had was to separate "pure" functions from "impure" procedures. Procedures could call other procedures or functions, and would be defined with `proc`; whereas functions could only call other functions and could not have side effects. The problem is defining what a side effect is in this context - is having internal mutable state (e.g. a temp vector) a side effect? If we're too strict on this, then having any pure functions would be rare; however if we're not strict enough it isn't useful. It might also just not be useful at all.

## Protocols

Should citrus even have protocols? Should they allow fields to be specified as well as methods? I feel like they should to avoid getters/setters which are annoying, but it also makes it harder to refactor. And I think anonymous protocols are really cool but I don't think they're *actually useful*.

Also I am not sure as to the syntax of:
- Anonymous protocols: Should it be `where T has (whatever)` or `T with (whatever)`?
- Implementing a protocol on a type: `Thing: struct(Protocol, ...) {}`? Standalone `Thing implemets Protocol`, or similar? idk.

## Definition syntax

Currently the `name: thing(other stuff)` syntax is *alright*, but a bit annoying. Maybe I should stick with `thing name(other stuff)` (e.g. `fn main` rather than `main: fn`)? The current syntax is nice for keeping things the same, as the syntax for declaring a function is the same as for a lambda, for example.

Additionally, what about associated functions? So far I've been doing it like this: `Struct::method: fn() = {}`, but that's a lot of ::s, so maybe it should be done differently.

Should the `=` be optional in function definitions to allow `thing: fn() {}` rather than reequiring `thing: fn() = {}`?

## It's too much like rust

How do I make it less like rust?

## Oh my, *lifetimes*

So I was wanting to do some rusty-c++y-(probably other languages)y stuff but it is *hard*. I want to not require any kind of explicit memory management if possible, but not entirely hide it like rust does. So `malloc`ing should be *possible* but absolutely not *necessary*.

Here's the thing: How do I keep track of who owns data? And what does it really *mean* for something to be owned? Rust solves this by saying that a reference isn't owned, but a not-reference is owned and therefore can be moved or dropped. The issue is, citrus doesn't *have* references, only pointers. Here's an example to illustrate the issue:

```citrus
String: struct {
    data: char*;
    length: u64;
}

String::split: fn(self: String*, delim: char) -> Vec<String*> = {
    // logic
}
```

In that example, if `split` simply returns a Vec of strings that reference the data from the original string, then they must not be owned otherwise when the `Vec` is dropped, its contents will be dropped too, and the same bit of data will be freed many times. So that means there must be a Vec of String*s, but what are the pointers to? I can't `malloc` them, because they would never be freed, and they can't be pointers to local variables because they would go out of scope. So I can't really use pointers to denote ownership, because it wouldn't allow the creation of non-owned objects in certain situations. idk it's hard to explain.

So the solution so far is to give up and just do manual memory management for now. this is hard. maybe I need a borrow checker....


## Algebraic effects???

"It's just rewriting the stack at runtime, how hard can it be?"

## Loops

Maybe `while` on its own could be an infinite loop? Trying so hard not to copy rust's `loop` rn.

```citrus
while {
    // loop until break
}
```

## Import/include/use/...

What word should I use? Also should it be a path or a namespace? dot seperated or colon seprated? semicolon at the end or not?

```citrus
// currently, it's like this
import "liblemon/vec.lime"

// other options
import "liblemon/vec.lime";
import liblemon.vec;
import liblemon::vec;
// additionally the above but replace "import" with any other suitable word
```

## Namespaces

Maybe I should implement namespaces... that might be good... and perhaps enforce a new namespace for each new file.

## Minor syntax decision paralysis

- Dedicated range syntax (`a..b`, `a:b`, etc.) or function `range(a, b)`?
- `with` in while loop to declare a scoped iteration variable? Could be annoying if I use `with` in the protocol syntax, or might not be, idk.

