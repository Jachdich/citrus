
fn test(a: i32) -> i32 {
    if a % 2 == 0 {
        a / 2
    } else {
        a * 3 + 1
    }
}

fn main() {
    println!("{}", test(34 + 35));
}
