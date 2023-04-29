[
  "fun"
  "struct"
  "proc"
] @keyword

(ident) @variable
(primitive_type) @type.builtin
(type_ident) @type
; (template_type) @

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
] @punctuation.delimiter

[
  (int)
] @number


[
  "("
  ")"
] @punctuation.bracket