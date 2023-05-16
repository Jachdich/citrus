[
  "fun"
  "struct"
  "proc"
  "import"
  "protocol"
] @keyword

(ident) @variable
(primitive_type) @type.builtin
(type_ident) @type
(func_name) @function
[ (struct_name) (proto_name) ] @type
(template_type) @type ; TODO these two need unique thingies
(proto_type) @type
(string_literal) @string
(comment) @comment

[
  "+"
  "-"
  "*"
  "/"
  "%"
  "="
  "->"
] @operator

[
  ";"
  ":"
  ","
] @punctuation.delimiter

[
  (int)
] @number


[
  "(" ")"
  "{" "}"
  "<" ">"
] @punctuation.bracket