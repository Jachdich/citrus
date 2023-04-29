module.exports = grammar({
    name: 'citrus',

    rules: {
        source_file: $ => repeat($.definition),
        definition: $ => choice($.fndef),
        expr: $ => choice($.mathexpr),
        int: $ => /\-?[0-9]+/,
        ident: $ => /[a-zA-Z_][a-zA-Z0-9_]+/,
        mathexpr: $ => choice(
            $.int, $.ident,
            prec.left(1, seq($.expr, "+", $.expr)),
            prec.left(1, seq($.expr, "-", $.expr)),
            prec.left(2, seq($.expr, "*", $.expr)),
            prec.left(2, seq($.expr, "/", $.expr)),
            prec.left(2, seq($.expr, "%", $.expr)),
            seq("(", $.expr, ")")
        ),
        
        primitive_type: $ => choice("u8", "u16", "u32", "u64", "i8", "i16", "i32", "i64", "f32", "f64", "char", "bool"),
        type_ident: $ => $.ident,
        
        _type: $ => choice($.primitive_type, $.type_ident),
        arg_list: $ => seq("(", repeat(seq($.ident, ":", $._type)), ")"),
        
        fndef: $ => seq($.ident, ":", "fun", $.arg_list, optional(seq("->", $._type)), "=", $.expr, ";"),
    }
});

