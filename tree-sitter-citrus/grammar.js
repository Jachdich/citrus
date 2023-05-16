function delimited_list(a, delim, $, allow_trailing) {
    if (allow_trailing) {
        return seq(a($), repeat(seq(delim, a($))), optional(delim));
    } else {
        return seq(a($), repeat(seq(delim, a($))));
    }
}

module.exports = grammar({
    name: 'citrus',

    extras: $ => [
        /\s/,
        $.comment,
    ],

    word: $ => $.ident,

    rules: {
        source_file: $ => repeat(choice($.definition, $.import_smt)),
        definition: $ => choice($.func_def, $.struct_def, $.proto_def),
        statement: $ => choice(seq($.expr, ";"), $.let_smt, $.if_smt),
        comment_line: $ => token(seq("//", /.*/)),
        comment_block: $ => token(seq("/*", /.*/, "*/")),
        comment: $ => choice($.comment_line, $.comment_block),
        
        expr: $ => choice(
            $.binexpr,
            $.funccall,
            $.struct_init,
            $.if_expr,
            prec.left($.ident),
            $.int,
            seq("(", $.expr, ")")
        ),
        compound_expr: $ => seq("{", repeat($.statement), $.expr, "}"),
        int: $ => /\-?[0-9]+/,
        ident: $ => /[a-zA-Z_][a-zA-Z0-9_]*/,

        // stolen form rust
        string_literal: $ => seq(
            // alias(/b?"/, '"'),
            '"',
            repeat(choice(
                $.escape_sequence,
                /[^\"]/,
            )),
            token.immediate('"')
        ),

        escape_sequence: $ => token.immediate(
            seq('\\',
            choice(
                /[^xu]/,
                /u[0-9a-fA-F]{4}/,
                /u{[0-9a-fA-F]+}/,
                /x[0-9a-fA-F]{2}/
            )
        )),
        
        binexpr: $ => choice(
            choice(...[
                "+", "-", "*", "/", "%",
                ">", "<", ">=", "<=", "≥", "≤", "==",
                "&", "|", "^", "&&", "||"
            ].map(op => prec.left(1, seq($.expr, op, $.expr)))),
            prec.right(2, seq($.expr, "@")),
            prec.left(3, seq($.expr, ".", $.ident)),
            prec.left(3, seq($.ident, "::", $.ident)),
        ),

        struct_init: $ => seq(
            $.ident, "{", delimited_list($ => seq(
                $.ident, ":", $.expr
            ), ",", $), "}"
        ),

        funccall: $ => seq($.expr, $.arg_use_list),
        
        primitive_type: $ => choice("u8", "u16", "u32", "u64", "i8", "i16", "i32", "i64", "f32", "f64", "char", "bool"),
        type_ident: $ => $.ident,
        
        _type: $ => choice(seq(
            choice(
                $.primitive_type,
                seq($.type_ident, optional($.template_use_list))
            ),
            repeat("*")
        ), repeat1("*")),
        
        block: $ => seq("{", repeat($.statement), "}"),
        
        arg_def_list: $ => seq("(", optional(delimited_list(r => seq(r.ident, ":", r._type, optional(seq("=", $.expr))), ",", $)), ")"),
        arg_use_list: $ => seq("(", optional(delimited_list(r => r.expr, ",", $)), ")"),

        template_def_list: $ => 
            seq("<",
                delimited_list(
                    $ => seq(
                        alias($.ident, $.template_type),
                        optional(seq(
                            ":",
                            delimited_list(
                                $ => alias($._type, $.proto_type),
                                "+", $, false
                            )  
                        ))
                    ),
                    ",",
                    $
                ),
                ">"
            ),

        template_use_list: $ => 
            seq("<",
                delimited_list(
                    $ => alias($.ident, $.template_type),
                    ",",
                    $
                ),
                ">"
            ),
        
        func_def: $ => seq(
            optional(seq(alias($.ident, $.func_struct), "::")),
            alias($.ident, $.func_name),
            ":",
            choice("fun", "proc"),
            optional($.template_def_list),
            $.arg_def_list,
            optional(seq("->", $._type)),
            choice(
                seq("=", $.expr, ";"),
                $.block,
                $.compound_expr,
                ";", // forward decleration
            )
        ),
        
        struct_def: $ => seq(
            alias($.ident, $.struct_name),
            ":", "struct",
            optional(seq(
                "(",
                delimited_list(
                    $ => $._type,
                    "+", $, false
                ),
                ")")),
            choice(seq(
                "{",
                repeat(seq(
                    $.ident,
                    ":",
                    $._type,
                    ";"
                )),
                "}"
            ), ";"),
        ),

        proto_def: $ => seq(
            alias($.ident, $.proto_name),
            ":", "protocol", "{",
            repeat(seq(
                $.ident,
                ":",
                $._type,
                ";"
            )),
            "}"
        ),

        import_smt: $ => seq("import", $.string_literal, ";"),

        let_smt: $ => seq(
            choice("let", "mut"),
            $.ident,
            optional(seq(
               ":", $._type 
            )),
            optional(seq(
                "=", $.expr
            )),
            ";"
        ),

        if_smt: $ => seq(
            "if", $.expr, $.block,
            repeat(seq("elif", $.expr, $.block)),
            optional(seq("else", $.block))
        ),

        if_expr: $ => seq(
            "if", $.expr, $.compound_expr,
            repeat(seq("elif", $.expr, $.compound_expr)),
            seq("else", $.compound_expr)
        ),

    }
});

