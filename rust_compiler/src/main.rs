use tree_sitter::Tree;

#[repr(C)]
struct ParseTree {
    children: *mut ParseTree,
    num_children: usize,
    ty: *const u8,
    val: *const u8,
}

fn traverse(tree: &Tree) -> ParseTree {
    ParseTree {
        num_children: tree.child_count(),
        ty: tree.kind().as_bytes(),
    }
}

fn main() {
    let code = "main: proc() -> i32 {}";
    let mut parser = tree_sitter::Parser::new();
    parser
        .set_language(tree_sitter_citrus::language())
        .expect("Error loading citrus grammar");
    let tree = parser.parse(code, None).unwrap();
    // let mut cursor = tree.walk();
    let tree = traverse(&tree);
}
