//slightly modified rust style struct declaration 
struct S {
    a: u32;
    b: u32*;
}



//modified rust style fn
fn do_nothing(a: u32) -> u32 = {
    a
}

//functions with a single expression can be written as such
fn add(x: i32, y: i32) -> i32 = x + y;
fn add(x: i32, y: i32) = x + y; //it can infer the return type

add = fn(x: i32, y: i32) = x + y;


//should I allow associated methods? or use c-style and pass pointers to functions
//  idea: assign anonymous function to function pointer field of struct
struct AssocMethod {
	some_fn: Fn(i32, i32) -> i32; //fn pointer syntax
	some_data: i32;
}

//perhaps need some way of marking some_fn as static or this line makes no sense
AssocMethod.some_fn = fn(x: i32, y: i32) = x + y;

//...or perhaps do it like this
fn AssocMethod::some_fn(x: i32, y: i32) = x + y;

//implicitly pass a self pointer when calling such associated methods
//e.g.
//let s = AssocMethod{...};
//s.can_access_self()
//same as
//AssocMethod::can_access_self(s&);
fn AssocMethod::can_access_self(self: AssocMethod*) = self.some_data;



//rust style error handling 
//not sure about this generic syntax, i want genetics to be as simple as possible though 
#[generic(T)]
union Option {
    Some: T;
    None;
}

//perhaps implicitly like ths
union Option<T> {
	Some: T;
	None;
}

fn can_fail() -> Option<i32> = None
fn can_fail() -> Option<i32> = {
	None
}

fn handle_fail() -> Option<i32> = {
	let res_a = can_fail()?; //rust style ? syntax
	let res_b = can_fail()?;
	Some(a + b)
}

main: fn() = {
	
}

fn main() -> i32 = {
    let a: u32 = 32;
    let b = &a; //b is pointer not reference because pointers are based
    let c: u8[4] /* is [u8; 4] better? */ = *b;

    //ifs are expressions
    let d = if c[0] { a * 2 } else { a / 2 };

    //optional parens?
    let d = do_nothing 15;
	
	//lambdas
	let a_fn: Fn() -> i32 = fn() = 32;
	//or just
	let a_fn = fn() = 32;
	//idk about the two =s though. they look a bit unclean;
	
	0 //success from main
}
