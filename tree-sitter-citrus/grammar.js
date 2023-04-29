function delimited_list(a, delim, $, allow_trailing) {
    if (allow_trailing) {
        return seq(a($), repeat(seq(delim, a($))), optional(delim));
    } else {
        return seq(a($), repeat(seq(delim, a($))));
    }
}

module.exports = grammar({
    name: 'citrus',

    rules: {
        source_file: $ => repeat($.definition),
        definition: $ => choice($.func_def, $.struct_def),
        statement: $ => choice(seq($.expr, ";")),
        
        expr: $ => choice($.mathexpr),
        compound_expr: $ => seq("{", repeat($.statement), $.expr, "}"),
        int: $ => /\-?[0-9]+/,
        ident: $ => /[a-zA-Z_][a-zA-Z0-9_]*/,
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
        
        block: $ => seq("{", repeat($.statement), "}"),
        
        arg_list: $ => seq("(", optional(delimited_list(r => seq(r.ident, ":", r._type), ",", $)), ")"),
        template_list: $ => 
            seq("<",
                delimited_list(
                    $ => seq(
                        alias($.ident, $.template_type),
                        optional(
                            seq(
                                ":",
                                delimited_list($ => alias($._type, $.proto_type), "+", $, false)  
                            )
                        )
                    ),
                    ",",
                    $
                ),
                ">"
            ),
        
        func_def: $ => seq($.ident, ":", choice("fun", "proc"), optional($.template_list), $.arg_list, optional(seq("->", $._type)), "=", choice(seq($.expr, ";"), $.block, $.compound_expr)),
        
        struct_def: $ => seq($.ident, ":", "struct", "=", "{", repeat(seq($.ident, ":", $._type, ";")), "}"),
    }
});

