#include <tree_sitter/parser.h>

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 98
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 54
#define ALIAS_COUNT 2
#define TOKEN_COUNT 34
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 10
#define PRODUCTION_ID_COUNT 4

enum {
  anon_sym_SEMI = 1,
  anon_sym_LBRACE = 2,
  anon_sym_RBRACE = 3,
  sym_int = 4,
  sym_ident = 5,
  anon_sym_PLUS = 6,
  anon_sym_DASH = 7,
  anon_sym_STAR = 8,
  anon_sym_SLASH = 9,
  anon_sym_PERCENT = 10,
  anon_sym_LPAREN = 11,
  anon_sym_RPAREN = 12,
  anon_sym_u8 = 13,
  anon_sym_u16 = 14,
  anon_sym_u32 = 15,
  anon_sym_u64 = 16,
  anon_sym_i8 = 17,
  anon_sym_i16 = 18,
  anon_sym_i32 = 19,
  anon_sym_i64 = 20,
  anon_sym_f32 = 21,
  anon_sym_f64 = 22,
  anon_sym_char = 23,
  anon_sym_bool = 24,
  anon_sym_COLON = 25,
  anon_sym_COMMA = 26,
  anon_sym_LT = 27,
  anon_sym_GT = 28,
  anon_sym_fun = 29,
  anon_sym_proc = 30,
  anon_sym_DASH_GT = 31,
  anon_sym_EQ = 32,
  anon_sym_struct = 33,
  sym_source_file = 34,
  sym_definition = 35,
  sym_statement = 36,
  sym_expr = 37,
  sym_compound_expr = 38,
  sym_mathexpr = 39,
  sym_primitive_type = 40,
  sym_type_ident = 41,
  sym__type = 42,
  sym_block = 43,
  sym_arg_list = 44,
  sym_template_list = 45,
  sym_func_def = 46,
  sym_struct_def = 47,
  aux_sym_source_file_repeat1 = 48,
  aux_sym_compound_expr_repeat1 = 49,
  aux_sym_arg_list_repeat1 = 50,
  aux_sym_template_list_repeat1 = 51,
  aux_sym_template_list_repeat2 = 52,
  aux_sym_struct_def_repeat1 = 53,
  alias_sym_proto_type = 54,
  alias_sym_template_type = 55,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [anon_sym_SEMI] = ";",
  [anon_sym_LBRACE] = "{",
  [anon_sym_RBRACE] = "}",
  [sym_int] = "int",
  [sym_ident] = "ident",
  [anon_sym_PLUS] = "+",
  [anon_sym_DASH] = "-",
  [anon_sym_STAR] = "*",
  [anon_sym_SLASH] = "/",
  [anon_sym_PERCENT] = "%",
  [anon_sym_LPAREN] = "(",
  [anon_sym_RPAREN] = ")",
  [anon_sym_u8] = "u8",
  [anon_sym_u16] = "u16",
  [anon_sym_u32] = "u32",
  [anon_sym_u64] = "u64",
  [anon_sym_i8] = "i8",
  [anon_sym_i16] = "i16",
  [anon_sym_i32] = "i32",
  [anon_sym_i64] = "i64",
  [anon_sym_f32] = "f32",
  [anon_sym_f64] = "f64",
  [anon_sym_char] = "char",
  [anon_sym_bool] = "bool",
  [anon_sym_COLON] = ":",
  [anon_sym_COMMA] = ",",
  [anon_sym_LT] = "<",
  [anon_sym_GT] = ">",
  [anon_sym_fun] = "fun",
  [anon_sym_proc] = "proc",
  [anon_sym_DASH_GT] = "->",
  [anon_sym_EQ] = "=",
  [anon_sym_struct] = "struct",
  [sym_source_file] = "source_file",
  [sym_definition] = "definition",
  [sym_statement] = "statement",
  [sym_expr] = "expr",
  [sym_compound_expr] = "compound_expr",
  [sym_mathexpr] = "mathexpr",
  [sym_primitive_type] = "primitive_type",
  [sym_type_ident] = "type_ident",
  [sym__type] = "_type",
  [sym_block] = "block",
  [sym_arg_list] = "arg_list",
  [sym_template_list] = "template_list",
  [sym_func_def] = "func_def",
  [sym_struct_def] = "struct_def",
  [aux_sym_source_file_repeat1] = "source_file_repeat1",
  [aux_sym_compound_expr_repeat1] = "compound_expr_repeat1",
  [aux_sym_arg_list_repeat1] = "arg_list_repeat1",
  [aux_sym_template_list_repeat1] = "template_list_repeat1",
  [aux_sym_template_list_repeat2] = "template_list_repeat2",
  [aux_sym_struct_def_repeat1] = "struct_def_repeat1",
  [alias_sym_proto_type] = "proto_type",
  [alias_sym_template_type] = "template_type",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [anon_sym_SEMI] = anon_sym_SEMI,
  [anon_sym_LBRACE] = anon_sym_LBRACE,
  [anon_sym_RBRACE] = anon_sym_RBRACE,
  [sym_int] = sym_int,
  [sym_ident] = sym_ident,
  [anon_sym_PLUS] = anon_sym_PLUS,
  [anon_sym_DASH] = anon_sym_DASH,
  [anon_sym_STAR] = anon_sym_STAR,
  [anon_sym_SLASH] = anon_sym_SLASH,
  [anon_sym_PERCENT] = anon_sym_PERCENT,
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_RPAREN] = anon_sym_RPAREN,
  [anon_sym_u8] = anon_sym_u8,
  [anon_sym_u16] = anon_sym_u16,
  [anon_sym_u32] = anon_sym_u32,
  [anon_sym_u64] = anon_sym_u64,
  [anon_sym_i8] = anon_sym_i8,
  [anon_sym_i16] = anon_sym_i16,
  [anon_sym_i32] = anon_sym_i32,
  [anon_sym_i64] = anon_sym_i64,
  [anon_sym_f32] = anon_sym_f32,
  [anon_sym_f64] = anon_sym_f64,
  [anon_sym_char] = anon_sym_char,
  [anon_sym_bool] = anon_sym_bool,
  [anon_sym_COLON] = anon_sym_COLON,
  [anon_sym_COMMA] = anon_sym_COMMA,
  [anon_sym_LT] = anon_sym_LT,
  [anon_sym_GT] = anon_sym_GT,
  [anon_sym_fun] = anon_sym_fun,
  [anon_sym_proc] = anon_sym_proc,
  [anon_sym_DASH_GT] = anon_sym_DASH_GT,
  [anon_sym_EQ] = anon_sym_EQ,
  [anon_sym_struct] = anon_sym_struct,
  [sym_source_file] = sym_source_file,
  [sym_definition] = sym_definition,
  [sym_statement] = sym_statement,
  [sym_expr] = sym_expr,
  [sym_compound_expr] = sym_compound_expr,
  [sym_mathexpr] = sym_mathexpr,
  [sym_primitive_type] = sym_primitive_type,
  [sym_type_ident] = sym_type_ident,
  [sym__type] = sym__type,
  [sym_block] = sym_block,
  [sym_arg_list] = sym_arg_list,
  [sym_template_list] = sym_template_list,
  [sym_func_def] = sym_func_def,
  [sym_struct_def] = sym_struct_def,
  [aux_sym_source_file_repeat1] = aux_sym_source_file_repeat1,
  [aux_sym_compound_expr_repeat1] = aux_sym_compound_expr_repeat1,
  [aux_sym_arg_list_repeat1] = aux_sym_arg_list_repeat1,
  [aux_sym_template_list_repeat1] = aux_sym_template_list_repeat1,
  [aux_sym_template_list_repeat2] = aux_sym_template_list_repeat2,
  [aux_sym_struct_def_repeat1] = aux_sym_struct_def_repeat1,
  [alias_sym_proto_type] = alias_sym_proto_type,
  [alias_sym_template_type] = alias_sym_template_type,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [anon_sym_SEMI] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LBRACE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RBRACE] = {
    .visible = true,
    .named = false,
  },
  [sym_int] = {
    .visible = true,
    .named = true,
  },
  [sym_ident] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_PLUS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DASH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_STAR] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SLASH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_PERCENT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_u8] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_u16] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_u32] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_u64] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_i8] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_i16] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_i32] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_i64] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_f32] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_f64] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_char] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_bool] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COLON] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMMA] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_GT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_fun] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_proc] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DASH_GT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_struct] = {
    .visible = true,
    .named = false,
  },
  [sym_source_file] = {
    .visible = true,
    .named = true,
  },
  [sym_definition] = {
    .visible = true,
    .named = true,
  },
  [sym_statement] = {
    .visible = true,
    .named = true,
  },
  [sym_expr] = {
    .visible = true,
    .named = true,
  },
  [sym_compound_expr] = {
    .visible = true,
    .named = true,
  },
  [sym_mathexpr] = {
    .visible = true,
    .named = true,
  },
  [sym_primitive_type] = {
    .visible = true,
    .named = true,
  },
  [sym_type_ident] = {
    .visible = true,
    .named = true,
  },
  [sym__type] = {
    .visible = false,
    .named = true,
  },
  [sym_block] = {
    .visible = true,
    .named = true,
  },
  [sym_arg_list] = {
    .visible = true,
    .named = true,
  },
  [sym_template_list] = {
    .visible = true,
    .named = true,
  },
  [sym_func_def] = {
    .visible = true,
    .named = true,
  },
  [sym_struct_def] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_source_file_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_compound_expr_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_arg_list_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_template_list_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_template_list_repeat2] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_struct_def_repeat1] = {
    .visible = false,
    .named = false,
  },
  [alias_sym_proto_type] = {
    .visible = true,
    .named = true,
  },
  [alias_sym_template_type] = {
    .visible = true,
    .named = true,
  },
};

static const TSSymbol ts_alias_sequences[PRODUCTION_ID_COUNT][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
  [1] = {
    [1] = alias_sym_template_type,
  },
  [2] = {
    [1] = alias_sym_template_type,
    [3] = alias_sym_proto_type,
  },
  [3] = {
    [1] = alias_sym_proto_type,
  },
};

static const uint16_t ts_non_terminal_alias_map[] = {
  sym__type, 2,
    sym__type,
    alias_sym_proto_type,
  0,
};

static const TSStateId ts_primary_state_ids[STATE_COUNT] = {
  [0] = 0,
  [1] = 1,
  [2] = 2,
  [3] = 3,
  [4] = 4,
  [5] = 5,
  [6] = 6,
  [7] = 7,
  [8] = 8,
  [9] = 9,
  [10] = 10,
  [11] = 11,
  [12] = 12,
  [13] = 13,
  [14] = 14,
  [15] = 15,
  [16] = 16,
  [17] = 17,
  [18] = 18,
  [19] = 19,
  [20] = 20,
  [21] = 21,
  [22] = 22,
  [23] = 23,
  [24] = 24,
  [25] = 25,
  [26] = 26,
  [27] = 27,
  [28] = 28,
  [29] = 29,
  [30] = 30,
  [31] = 31,
  [32] = 32,
  [33] = 33,
  [34] = 34,
  [35] = 35,
  [36] = 36,
  [37] = 37,
  [38] = 38,
  [39] = 39,
  [40] = 40,
  [41] = 41,
  [42] = 42,
  [43] = 43,
  [44] = 44,
  [45] = 45,
  [46] = 46,
  [47] = 47,
  [48] = 48,
  [49] = 49,
  [50] = 50,
  [51] = 51,
  [52] = 52,
  [53] = 53,
  [54] = 54,
  [55] = 55,
  [56] = 56,
  [57] = 57,
  [58] = 58,
  [59] = 59,
  [60] = 60,
  [61] = 61,
  [62] = 62,
  [63] = 63,
  [64] = 64,
  [65] = 65,
  [66] = 66,
  [67] = 67,
  [68] = 68,
  [69] = 69,
  [70] = 70,
  [71] = 71,
  [72] = 72,
  [73] = 73,
  [74] = 74,
  [75] = 75,
  [76] = 76,
  [77] = 77,
  [78] = 78,
  [79] = 79,
  [80] = 80,
  [81] = 81,
  [82] = 82,
  [83] = 83,
  [84] = 84,
  [85] = 85,
  [86] = 86,
  [87] = 87,
  [88] = 88,
  [89] = 89,
  [90] = 90,
  [91] = 91,
  [92] = 92,
  [93] = 93,
  [94] = 94,
  [95] = 95,
  [96] = 96,
  [97] = 97,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(15);
      if (lookahead == '%') ADVANCE(53);
      if (lookahead == '(') ADVANCE(54);
      if (lookahead == ')') ADVANCE(55);
      if (lookahead == '*') ADVANCE(51);
      if (lookahead == '+') ADVANCE(48);
      if (lookahead == ',') ADVANCE(69);
      if (lookahead == '-') ADVANCE(50);
      if (lookahead == '/') ADVANCE(52);
      if (lookahead == ':') ADVANCE(68);
      if (lookahead == ';') ADVANCE(16);
      if (lookahead == '<') ADVANCE(70);
      if (lookahead == '=') ADVANCE(77);
      if (lookahead == '>') ADVANCE(71);
      if (lookahead == 'b') ADVANCE(40);
      if (lookahead == 'c') ADVANCE(35);
      if (lookahead == 'f') ADVANCE(25);
      if (lookahead == 'i') ADVANCE(20);
      if (lookahead == 'p') ADVANCE(43);
      if (lookahead == 's') ADVANCE(45);
      if (lookahead == 'u') ADVANCE(21);
      if (lookahead == '{') ADVANCE(17);
      if (lookahead == '}') ADVANCE(18);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(0)
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 1:
      if (lookahead == '%') ADVANCE(53);
      if (lookahead == ')') ADVANCE(55);
      if (lookahead == '*') ADVANCE(51);
      if (lookahead == '+') ADVANCE(48);
      if (lookahead == '-') ADVANCE(49);
      if (lookahead == '/') ADVANCE(52);
      if (lookahead == ';') ADVANCE(16);
      if (lookahead == 'b') ADVANCE(40);
      if (lookahead == 'c') ADVANCE(35);
      if (lookahead == 'f') ADVANCE(26);
      if (lookahead == 'i') ADVANCE(20);
      if (lookahead == 'u') ADVANCE(21);
      if (lookahead == '}') ADVANCE(18);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(1)
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 2:
      if (lookahead == '>') ADVANCE(76);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(19);
      END_STATE();
    case 3:
      if (lookahead == 'c') ADVANCE(74);
      END_STATE();
    case 4:
      if (lookahead == 'c') ADVANCE(10);
      END_STATE();
    case 5:
      if (lookahead == 'f') ADVANCE(12);
      if (lookahead == 'p') ADVANCE(8);
      if (lookahead == 's') ADVANCE(11);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(5)
      END_STATE();
    case 6:
      if (lookahead == 'n') ADVANCE(72);
      END_STATE();
    case 7:
      if (lookahead == 'o') ADVANCE(3);
      END_STATE();
    case 8:
      if (lookahead == 'r') ADVANCE(7);
      END_STATE();
    case 9:
      if (lookahead == 'r') ADVANCE(13);
      END_STATE();
    case 10:
      if (lookahead == 't') ADVANCE(78);
      END_STATE();
    case 11:
      if (lookahead == 't') ADVANCE(9);
      END_STATE();
    case 12:
      if (lookahead == 'u') ADVANCE(6);
      END_STATE();
    case 13:
      if (lookahead == 'u') ADVANCE(4);
      END_STATE();
    case 14:
      if (eof) ADVANCE(15);
      if (lookahead == '(') ADVANCE(54);
      if (lookahead == ')') ADVANCE(55);
      if (lookahead == '-') ADVANCE(2);
      if (lookahead == '=') ADVANCE(77);
      if (lookahead == '{') ADVANCE(17);
      if (lookahead == '}') ADVANCE(18);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(14)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(19);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 15:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 16:
      ACCEPT_TOKEN(anon_sym_SEMI);
      END_STATE();
    case 17:
      ACCEPT_TOKEN(anon_sym_LBRACE);
      END_STATE();
    case 18:
      ACCEPT_TOKEN(anon_sym_RBRACE);
      END_STATE();
    case 19:
      ACCEPT_TOKEN(sym_int);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(19);
      END_STATE();
    case 20:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '1') ADVANCE(30);
      if (lookahead == '3') ADVANCE(23);
      if (lookahead == '6') ADVANCE(28);
      if (lookahead == '8') ADVANCE(60);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 21:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '1') ADVANCE(31);
      if (lookahead == '3') ADVANCE(24);
      if (lookahead == '6') ADVANCE(29);
      if (lookahead == '8') ADVANCE(56);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 22:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '2') ADVANCE(64);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 23:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '2') ADVANCE(62);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 24:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '2') ADVANCE(58);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 25:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '3') ADVANCE(22);
      if (lookahead == '6') ADVANCE(27);
      if (lookahead == 'u') ADVANCE(37);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 26:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '3') ADVANCE(22);
      if (lookahead == '6') ADVANCE(27);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 27:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '4') ADVANCE(65);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 28:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '4') ADVANCE(63);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 29:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '4') ADVANCE(59);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 30:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '6') ADVANCE(61);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 31:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '6') ADVANCE(57);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 32:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'a') ADVANCE(42);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 33:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'c') ADVANCE(75);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 34:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'c') ADVANCE(44);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 35:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'h') ADVANCE(32);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 36:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'l') ADVANCE(67);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 37:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'n') ADVANCE(73);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 38:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'o') ADVANCE(36);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 39:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'o') ADVANCE(33);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 40:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'o') ADVANCE(38);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 41:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'r') ADVANCE(46);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 42:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'r') ADVANCE(66);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 43:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'r') ADVANCE(39);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 44:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 't') ADVANCE(79);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 45:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 't') ADVANCE(41);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 46:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'u') ADVANCE(34);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 47:
      ACCEPT_TOKEN(sym_ident);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 48:
      ACCEPT_TOKEN(anon_sym_PLUS);
      END_STATE();
    case 49:
      ACCEPT_TOKEN(anon_sym_DASH);
      END_STATE();
    case 50:
      ACCEPT_TOKEN(anon_sym_DASH);
      if (lookahead == '>') ADVANCE(76);
      END_STATE();
    case 51:
      ACCEPT_TOKEN(anon_sym_STAR);
      END_STATE();
    case 52:
      ACCEPT_TOKEN(anon_sym_SLASH);
      END_STATE();
    case 53:
      ACCEPT_TOKEN(anon_sym_PERCENT);
      END_STATE();
    case 54:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 55:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 56:
      ACCEPT_TOKEN(anon_sym_u8);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 57:
      ACCEPT_TOKEN(anon_sym_u16);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 58:
      ACCEPT_TOKEN(anon_sym_u32);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 59:
      ACCEPT_TOKEN(anon_sym_u64);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 60:
      ACCEPT_TOKEN(anon_sym_i8);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 61:
      ACCEPT_TOKEN(anon_sym_i16);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 62:
      ACCEPT_TOKEN(anon_sym_i32);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 63:
      ACCEPT_TOKEN(anon_sym_i64);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 64:
      ACCEPT_TOKEN(anon_sym_f32);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 65:
      ACCEPT_TOKEN(anon_sym_f64);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 66:
      ACCEPT_TOKEN(anon_sym_char);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 67:
      ACCEPT_TOKEN(anon_sym_bool);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 68:
      ACCEPT_TOKEN(anon_sym_COLON);
      END_STATE();
    case 69:
      ACCEPT_TOKEN(anon_sym_COMMA);
      END_STATE();
    case 70:
      ACCEPT_TOKEN(anon_sym_LT);
      END_STATE();
    case 71:
      ACCEPT_TOKEN(anon_sym_GT);
      END_STATE();
    case 72:
      ACCEPT_TOKEN(anon_sym_fun);
      END_STATE();
    case 73:
      ACCEPT_TOKEN(anon_sym_fun);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 74:
      ACCEPT_TOKEN(anon_sym_proc);
      END_STATE();
    case 75:
      ACCEPT_TOKEN(anon_sym_proc);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    case 76:
      ACCEPT_TOKEN(anon_sym_DASH_GT);
      END_STATE();
    case 77:
      ACCEPT_TOKEN(anon_sym_EQ);
      END_STATE();
    case 78:
      ACCEPT_TOKEN(anon_sym_struct);
      END_STATE();
    case 79:
      ACCEPT_TOKEN(anon_sym_struct);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(47);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 14},
  [2] = {.lex_state = 1},
  [3] = {.lex_state = 1},
  [4] = {.lex_state = 1},
  [5] = {.lex_state = 1},
  [6] = {.lex_state = 1},
  [7] = {.lex_state = 1},
  [8] = {.lex_state = 1},
  [9] = {.lex_state = 1},
  [10] = {.lex_state = 14},
  [11] = {.lex_state = 14},
  [12] = {.lex_state = 14},
  [13] = {.lex_state = 1},
  [14] = {.lex_state = 14},
  [15] = {.lex_state = 1},
  [16] = {.lex_state = 1},
  [17] = {.lex_state = 14},
  [18] = {.lex_state = 14},
  [19] = {.lex_state = 1},
  [20] = {.lex_state = 1},
  [21] = {.lex_state = 14},
  [22] = {.lex_state = 1},
  [23] = {.lex_state = 1},
  [24] = {.lex_state = 1},
  [25] = {.lex_state = 1},
  [26] = {.lex_state = 1},
  [27] = {.lex_state = 0},
  [28] = {.lex_state = 0},
  [29] = {.lex_state = 0},
  [30] = {.lex_state = 1},
  [31] = {.lex_state = 14},
  [32] = {.lex_state = 14},
  [33] = {.lex_state = 1},
  [34] = {.lex_state = 1},
  [35] = {.lex_state = 0},
  [36] = {.lex_state = 14},
  [37] = {.lex_state = 14},
  [38] = {.lex_state = 0},
  [39] = {.lex_state = 14},
  [40] = {.lex_state = 0},
  [41] = {.lex_state = 0},
  [42] = {.lex_state = 14},
  [43] = {.lex_state = 0},
  [44] = {.lex_state = 0},
  [45] = {.lex_state = 0},
  [46] = {.lex_state = 0},
  [47] = {.lex_state = 14},
  [48] = {.lex_state = 0},
  [49] = {.lex_state = 0},
  [50] = {.lex_state = 0},
  [51] = {.lex_state = 0},
  [52] = {.lex_state = 5},
  [53] = {.lex_state = 0},
  [54] = {.lex_state = 14},
  [55] = {.lex_state = 0},
  [56] = {.lex_state = 14},
  [57] = {.lex_state = 0},
  [58] = {.lex_state = 0},
  [59] = {.lex_state = 14},
  [60] = {.lex_state = 14},
  [61] = {.lex_state = 0},
  [62] = {.lex_state = 14},
  [63] = {.lex_state = 14},
  [64] = {.lex_state = 14},
  [65] = {.lex_state = 14},
  [66] = {.lex_state = 14},
  [67] = {.lex_state = 14},
  [68] = {.lex_state = 14},
  [69] = {.lex_state = 14},
  [70] = {.lex_state = 14},
  [71] = {.lex_state = 14},
  [72] = {.lex_state = 14},
  [73] = {.lex_state = 14},
  [74] = {.lex_state = 14},
  [75] = {.lex_state = 14},
  [76] = {.lex_state = 0},
  [77] = {.lex_state = 14},
  [78] = {.lex_state = 14},
  [79] = {.lex_state = 14},
  [80] = {.lex_state = 0},
  [81] = {.lex_state = 0},
  [82] = {.lex_state = 0},
  [83] = {.lex_state = 0},
  [84] = {.lex_state = 0},
  [85] = {.lex_state = 14},
  [86] = {.lex_state = 0},
  [87] = {.lex_state = 14},
  [88] = {.lex_state = 0},
  [89] = {.lex_state = 0},
  [90] = {.lex_state = 0},
  [91] = {.lex_state = 0},
  [92] = {.lex_state = 0},
  [93] = {.lex_state = 0},
  [94] = {.lex_state = 0},
  [95] = {.lex_state = 0},
  [96] = {.lex_state = 0},
  [97] = {.lex_state = 14},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [anon_sym_SEMI] = ACTIONS(1),
    [anon_sym_LBRACE] = ACTIONS(1),
    [anon_sym_RBRACE] = ACTIONS(1),
    [sym_ident] = ACTIONS(1),
    [anon_sym_PLUS] = ACTIONS(1),
    [anon_sym_DASH] = ACTIONS(1),
    [anon_sym_STAR] = ACTIONS(1),
    [anon_sym_SLASH] = ACTIONS(1),
    [anon_sym_PERCENT] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_RPAREN] = ACTIONS(1),
    [anon_sym_u8] = ACTIONS(1),
    [anon_sym_u16] = ACTIONS(1),
    [anon_sym_u32] = ACTIONS(1),
    [anon_sym_u64] = ACTIONS(1),
    [anon_sym_i8] = ACTIONS(1),
    [anon_sym_i16] = ACTIONS(1),
    [anon_sym_i32] = ACTIONS(1),
    [anon_sym_i64] = ACTIONS(1),
    [anon_sym_f32] = ACTIONS(1),
    [anon_sym_f64] = ACTIONS(1),
    [anon_sym_char] = ACTIONS(1),
    [anon_sym_bool] = ACTIONS(1),
    [anon_sym_COLON] = ACTIONS(1),
    [anon_sym_COMMA] = ACTIONS(1),
    [anon_sym_LT] = ACTIONS(1),
    [anon_sym_GT] = ACTIONS(1),
    [anon_sym_fun] = ACTIONS(1),
    [anon_sym_proc] = ACTIONS(1),
    [anon_sym_DASH_GT] = ACTIONS(1),
    [anon_sym_EQ] = ACTIONS(1),
    [anon_sym_struct] = ACTIONS(1),
  },
  [1] = {
    [sym_source_file] = STATE(95),
    [sym_definition] = STATE(31),
    [sym_func_def] = STATE(64),
    [sym_struct_def] = STATE(64),
    [aux_sym_source_file_repeat1] = STATE(31),
    [ts_builtin_sym_end] = ACTIONS(3),
    [sym_ident] = ACTIONS(5),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 4,
    ACTIONS(7), 1,
      sym_ident,
    STATE(50), 1,
      sym__type,
    STATE(29), 2,
      sym_primitive_type,
      sym_type_ident,
    ACTIONS(9), 12,
      anon_sym_u8,
      anon_sym_u16,
      anon_sym_u32,
      anon_sym_u64,
      anon_sym_i8,
      anon_sym_i16,
      anon_sym_i32,
      anon_sym_i64,
      anon_sym_f32,
      anon_sym_f64,
      anon_sym_char,
      anon_sym_bool,
  [25] = 4,
    ACTIONS(7), 1,
      sym_ident,
    STATE(61), 1,
      sym__type,
    STATE(29), 2,
      sym_primitive_type,
      sym_type_ident,
    ACTIONS(9), 12,
      anon_sym_u8,
      anon_sym_u16,
      anon_sym_u32,
      anon_sym_u64,
      anon_sym_i8,
      anon_sym_i16,
      anon_sym_i32,
      anon_sym_i64,
      anon_sym_f32,
      anon_sym_f64,
      anon_sym_char,
      anon_sym_bool,
  [50] = 4,
    ACTIONS(7), 1,
      sym_ident,
    STATE(88), 1,
      sym__type,
    STATE(29), 2,
      sym_primitive_type,
      sym_type_ident,
    ACTIONS(9), 12,
      anon_sym_u8,
      anon_sym_u16,
      anon_sym_u32,
      anon_sym_u64,
      anon_sym_i8,
      anon_sym_i16,
      anon_sym_i32,
      anon_sym_i64,
      anon_sym_f32,
      anon_sym_f64,
      anon_sym_char,
      anon_sym_bool,
  [75] = 4,
    ACTIONS(7), 1,
      sym_ident,
    STATE(96), 1,
      sym__type,
    STATE(29), 2,
      sym_primitive_type,
      sym_type_ident,
    ACTIONS(9), 12,
      anon_sym_u8,
      anon_sym_u16,
      anon_sym_u32,
      anon_sym_u64,
      anon_sym_i8,
      anon_sym_i16,
      anon_sym_i32,
      anon_sym_i64,
      anon_sym_f32,
      anon_sym_f64,
      anon_sym_char,
      anon_sym_bool,
  [100] = 4,
    ACTIONS(7), 1,
      sym_ident,
    STATE(46), 1,
      sym__type,
    STATE(29), 2,
      sym_primitive_type,
      sym_type_ident,
    ACTIONS(9), 12,
      anon_sym_u8,
      anon_sym_u16,
      anon_sym_u32,
      anon_sym_u64,
      anon_sym_i8,
      anon_sym_i16,
      anon_sym_i32,
      anon_sym_i64,
      anon_sym_f32,
      anon_sym_f64,
      anon_sym_char,
      anon_sym_bool,
  [125] = 4,
    ACTIONS(7), 1,
      sym_ident,
    STATE(38), 1,
      sym__type,
    STATE(29), 2,
      sym_primitive_type,
      sym_type_ident,
    ACTIONS(9), 12,
      anon_sym_u8,
      anon_sym_u16,
      anon_sym_u32,
      anon_sym_u64,
      anon_sym_i8,
      anon_sym_i16,
      anon_sym_i32,
      anon_sym_i64,
      anon_sym_f32,
      anon_sym_f64,
      anon_sym_char,
      anon_sym_bool,
  [150] = 4,
    ACTIONS(7), 1,
      sym_ident,
    STATE(45), 1,
      sym__type,
    STATE(29), 2,
      sym_primitive_type,
      sym_type_ident,
    ACTIONS(9), 12,
      anon_sym_u8,
      anon_sym_u16,
      anon_sym_u32,
      anon_sym_u64,
      anon_sym_i8,
      anon_sym_i16,
      anon_sym_i32,
      anon_sym_i64,
      anon_sym_f32,
      anon_sym_f64,
      anon_sym_char,
      anon_sym_bool,
  [175] = 4,
    ACTIONS(7), 1,
      sym_ident,
    STATE(81), 1,
      sym__type,
    STATE(29), 2,
      sym_primitive_type,
      sym_type_ident,
    ACTIONS(9), 12,
      anon_sym_u8,
      anon_sym_u16,
      anon_sym_u32,
      anon_sym_u64,
      anon_sym_i8,
      anon_sym_i16,
      anon_sym_i32,
      anon_sym_i64,
      anon_sym_f32,
      anon_sym_f64,
      anon_sym_char,
      anon_sym_bool,
  [200] = 6,
    ACTIONS(11), 1,
      anon_sym_LBRACE,
    ACTIONS(15), 1,
      anon_sym_LPAREN,
    STATE(13), 1,
      sym_mathexpr,
    STATE(33), 1,
      sym_expr,
    ACTIONS(13), 2,
      sym_int,
      sym_ident,
    STATE(73), 2,
      sym_compound_expr,
      sym_block,
  [221] = 6,
    ACTIONS(17), 1,
      anon_sym_RBRACE,
    ACTIONS(22), 1,
      anon_sym_LPAREN,
    STATE(13), 1,
      sym_mathexpr,
    STATE(30), 1,
      sym_expr,
    ACTIONS(19), 2,
      sym_int,
      sym_ident,
    STATE(11), 2,
      sym_statement,
      aux_sym_compound_expr_repeat1,
  [242] = 6,
    ACTIONS(11), 1,
      anon_sym_LBRACE,
    ACTIONS(15), 1,
      anon_sym_LPAREN,
    STATE(13), 1,
      sym_mathexpr,
    STATE(25), 1,
      sym_expr,
    ACTIONS(13), 2,
      sym_int,
      sym_ident,
    STATE(69), 2,
      sym_compound_expr,
      sym_block,
  [263] = 1,
    ACTIONS(25), 8,
      anon_sym_SEMI,
      anon_sym_RBRACE,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
  [274] = 6,
    ACTIONS(11), 1,
      anon_sym_LBRACE,
    ACTIONS(15), 1,
      anon_sym_LPAREN,
    STATE(13), 1,
      sym_mathexpr,
    STATE(34), 1,
      sym_expr,
    ACTIONS(13), 2,
      sym_int,
      sym_ident,
    STATE(74), 2,
      sym_compound_expr,
      sym_block,
  [295] = 1,
    ACTIONS(27), 8,
      anon_sym_SEMI,
      anon_sym_RBRACE,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
  [306] = 1,
    ACTIONS(29), 8,
      anon_sym_SEMI,
      anon_sym_RBRACE,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
  [317] = 6,
    ACTIONS(15), 1,
      anon_sym_LPAREN,
    ACTIONS(31), 1,
      anon_sym_RBRACE,
    STATE(13), 1,
      sym_mathexpr,
    STATE(23), 1,
      sym_expr,
    ACTIONS(13), 2,
      sym_int,
      sym_ident,
    STATE(11), 2,
      sym_statement,
      aux_sym_compound_expr_repeat1,
  [338] = 6,
    ACTIONS(15), 1,
      anon_sym_LPAREN,
    ACTIONS(33), 1,
      anon_sym_RBRACE,
    STATE(13), 1,
      sym_mathexpr,
    STATE(22), 1,
      sym_expr,
    ACTIONS(13), 2,
      sym_int,
      sym_ident,
    STATE(17), 2,
      sym_statement,
      aux_sym_compound_expr_repeat1,
  [359] = 2,
    ACTIONS(35), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
    ACTIONS(27), 5,
      anon_sym_SEMI,
      anon_sym_RBRACE,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_RPAREN,
  [372] = 1,
    ACTIONS(27), 8,
      anon_sym_SEMI,
      anon_sym_RBRACE,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
  [383] = 6,
    ACTIONS(11), 1,
      anon_sym_LBRACE,
    ACTIONS(15), 1,
      anon_sym_LPAREN,
    STATE(13), 1,
      sym_mathexpr,
    STATE(26), 1,
      sym_expr,
    ACTIONS(13), 2,
      sym_int,
      sym_ident,
    STATE(65), 2,
      sym_compound_expr,
      sym_block,
  [404] = 4,
    ACTIONS(37), 1,
      anon_sym_SEMI,
    ACTIONS(39), 1,
      anon_sym_RBRACE,
    ACTIONS(41), 2,
      anon_sym_PLUS,
      anon_sym_DASH,
    ACTIONS(35), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
  [420] = 4,
    ACTIONS(37), 1,
      anon_sym_SEMI,
    ACTIONS(43), 1,
      anon_sym_RBRACE,
    ACTIONS(41), 2,
      anon_sym_PLUS,
      anon_sym_DASH,
    ACTIONS(35), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
  [436] = 3,
    ACTIONS(45), 1,
      anon_sym_RPAREN,
    ACTIONS(41), 2,
      anon_sym_PLUS,
      anon_sym_DASH,
    ACTIONS(35), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
  [449] = 3,
    ACTIONS(47), 1,
      anon_sym_SEMI,
    ACTIONS(41), 2,
      anon_sym_PLUS,
      anon_sym_DASH,
    ACTIONS(35), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
  [462] = 3,
    ACTIONS(49), 1,
      anon_sym_SEMI,
    ACTIONS(41), 2,
      anon_sym_PLUS,
      anon_sym_DASH,
    ACTIONS(35), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
  [475] = 1,
    ACTIONS(51), 6,
      anon_sym_SEMI,
      anon_sym_PLUS,
      anon_sym_RPAREN,
      anon_sym_COMMA,
      anon_sym_GT,
      anon_sym_EQ,
  [484] = 1,
    ACTIONS(53), 6,
      anon_sym_SEMI,
      anon_sym_PLUS,
      anon_sym_RPAREN,
      anon_sym_COMMA,
      anon_sym_GT,
      anon_sym_EQ,
  [493] = 1,
    ACTIONS(55), 6,
      anon_sym_SEMI,
      anon_sym_PLUS,
      anon_sym_RPAREN,
      anon_sym_COMMA,
      anon_sym_GT,
      anon_sym_EQ,
  [502] = 3,
    ACTIONS(37), 1,
      anon_sym_SEMI,
    ACTIONS(41), 2,
      anon_sym_PLUS,
      anon_sym_DASH,
    ACTIONS(35), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
  [515] = 4,
    ACTIONS(5), 1,
      sym_ident,
    ACTIONS(57), 1,
      ts_builtin_sym_end,
    STATE(32), 2,
      sym_definition,
      aux_sym_source_file_repeat1,
    STATE(64), 2,
      sym_func_def,
      sym_struct_def,
  [530] = 4,
    ACTIONS(59), 1,
      ts_builtin_sym_end,
    ACTIONS(61), 1,
      sym_ident,
    STATE(32), 2,
      sym_definition,
      aux_sym_source_file_repeat1,
    STATE(64), 2,
      sym_func_def,
      sym_struct_def,
  [545] = 3,
    ACTIONS(64), 1,
      anon_sym_SEMI,
    ACTIONS(41), 2,
      anon_sym_PLUS,
      anon_sym_DASH,
    ACTIONS(35), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
  [558] = 3,
    ACTIONS(66), 1,
      anon_sym_SEMI,
    ACTIONS(41), 2,
      anon_sym_PLUS,
      anon_sym_DASH,
    ACTIONS(35), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
  [571] = 5,
    ACTIONS(68), 1,
      anon_sym_PLUS,
    ACTIONS(70), 1,
      anon_sym_COMMA,
    ACTIONS(72), 1,
      anon_sym_GT,
    STATE(44), 1,
      aux_sym_template_list_repeat1,
    STATE(58), 1,
      aux_sym_template_list_repeat2,
  [587] = 4,
    ACTIONS(15), 1,
      anon_sym_LPAREN,
    STATE(13), 1,
      sym_mathexpr,
    STATE(24), 1,
      sym_expr,
    ACTIONS(13), 2,
      sym_int,
      sym_ident,
  [601] = 4,
    ACTIONS(15), 1,
      anon_sym_LPAREN,
    STATE(13), 1,
      sym_mathexpr,
    STATE(19), 1,
      sym_expr,
    ACTIONS(13), 2,
      sym_int,
      sym_ident,
  [615] = 5,
    ACTIONS(68), 1,
      anon_sym_PLUS,
    ACTIONS(70), 1,
      anon_sym_COMMA,
    ACTIONS(74), 1,
      anon_sym_GT,
    STATE(35), 1,
      aux_sym_template_list_repeat1,
    STATE(48), 1,
      aux_sym_template_list_repeat2,
  [631] = 4,
    ACTIONS(15), 1,
      anon_sym_LPAREN,
    STATE(13), 1,
      sym_mathexpr,
    STATE(15), 1,
      sym_expr,
    ACTIONS(13), 2,
      sym_int,
      sym_ident,
  [645] = 3,
    ACTIONS(68), 1,
      anon_sym_PLUS,
    STATE(44), 1,
      aux_sym_template_list_repeat1,
    ACTIONS(76), 2,
      anon_sym_COMMA,
      anon_sym_GT,
  [656] = 4,
    ACTIONS(78), 1,
      anon_sym_LPAREN,
    ACTIONS(80), 1,
      anon_sym_LT,
    STATE(75), 1,
      sym_arg_list,
    STATE(76), 1,
      sym_template_list,
  [669] = 1,
    ACTIONS(82), 4,
      anon_sym_RBRACE,
      sym_int,
      sym_ident,
      anon_sym_LPAREN,
  [676] = 4,
    ACTIONS(70), 1,
      anon_sym_COMMA,
    ACTIONS(84), 1,
      anon_sym_COLON,
    ACTIONS(86), 1,
      anon_sym_GT,
    STATE(53), 1,
      aux_sym_template_list_repeat2,
  [689] = 3,
    ACTIONS(88), 1,
      anon_sym_PLUS,
    STATE(44), 1,
      aux_sym_template_list_repeat1,
    ACTIONS(91), 2,
      anon_sym_COMMA,
      anon_sym_GT,
  [700] = 3,
    ACTIONS(68), 1,
      anon_sym_PLUS,
    STATE(40), 1,
      aux_sym_template_list_repeat1,
    ACTIONS(93), 2,
      anon_sym_COMMA,
      anon_sym_GT,
  [711] = 1,
    ACTIONS(95), 3,
      anon_sym_PLUS,
      anon_sym_COMMA,
      anon_sym_GT,
  [717] = 3,
    ACTIONS(97), 1,
      anon_sym_RBRACE,
    ACTIONS(99), 1,
      sym_ident,
    STATE(56), 1,
      aux_sym_struct_def_repeat1,
  [727] = 3,
    ACTIONS(70), 1,
      anon_sym_COMMA,
    ACTIONS(72), 1,
      anon_sym_GT,
    STATE(51), 1,
      aux_sym_template_list_repeat2,
  [737] = 2,
    ACTIONS(101), 1,
      anon_sym_COLON,
    ACTIONS(103), 2,
      anon_sym_COMMA,
      anon_sym_GT,
  [745] = 3,
    ACTIONS(105), 1,
      anon_sym_RPAREN,
    ACTIONS(107), 1,
      anon_sym_COMMA,
    STATE(57), 1,
      aux_sym_arg_list_repeat1,
  [755] = 3,
    ACTIONS(109), 1,
      anon_sym_COMMA,
    ACTIONS(112), 1,
      anon_sym_GT,
    STATE(51), 1,
      aux_sym_template_list_repeat2,
  [765] = 2,
    ACTIONS(116), 1,
      anon_sym_struct,
    ACTIONS(114), 2,
      anon_sym_fun,
      anon_sym_proc,
  [773] = 3,
    ACTIONS(70), 1,
      anon_sym_COMMA,
    ACTIONS(118), 1,
      anon_sym_GT,
    STATE(51), 1,
      aux_sym_template_list_repeat2,
  [783] = 3,
    ACTIONS(99), 1,
      sym_ident,
    ACTIONS(120), 1,
      anon_sym_RBRACE,
    STATE(47), 1,
      aux_sym_struct_def_repeat1,
  [793] = 3,
    ACTIONS(122), 1,
      anon_sym_RPAREN,
    ACTIONS(124), 1,
      anon_sym_COMMA,
    STATE(55), 1,
      aux_sym_arg_list_repeat1,
  [803] = 3,
    ACTIONS(127), 1,
      anon_sym_RBRACE,
    ACTIONS(129), 1,
      sym_ident,
    STATE(56), 1,
      aux_sym_struct_def_repeat1,
  [813] = 3,
    ACTIONS(107), 1,
      anon_sym_COMMA,
    ACTIONS(132), 1,
      anon_sym_RPAREN,
    STATE(55), 1,
      aux_sym_arg_list_repeat1,
  [823] = 3,
    ACTIONS(70), 1,
      anon_sym_COMMA,
    ACTIONS(134), 1,
      anon_sym_GT,
    STATE(51), 1,
      aux_sym_template_list_repeat2,
  [833] = 1,
    ACTIONS(136), 2,
      ts_builtin_sym_end,
      sym_ident,
  [838] = 1,
    ACTIONS(138), 2,
      anon_sym_DASH_GT,
      anon_sym_EQ,
  [843] = 1,
    ACTIONS(140), 2,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [848] = 1,
    ACTIONS(142), 2,
      ts_builtin_sym_end,
      sym_ident,
  [853] = 1,
    ACTIONS(144), 2,
      ts_builtin_sym_end,
      sym_ident,
  [858] = 1,
    ACTIONS(146), 2,
      ts_builtin_sym_end,
      sym_ident,
  [863] = 1,
    ACTIONS(148), 2,
      ts_builtin_sym_end,
      sym_ident,
  [868] = 1,
    ACTIONS(150), 2,
      anon_sym_RBRACE,
      sym_ident,
  [873] = 1,
    ACTIONS(152), 2,
      ts_builtin_sym_end,
      sym_ident,
  [878] = 2,
    ACTIONS(154), 1,
      sym_ident,
    ACTIONS(156), 1,
      anon_sym_RPAREN,
  [885] = 1,
    ACTIONS(158), 2,
      ts_builtin_sym_end,
      sym_ident,
  [890] = 1,
    ACTIONS(160), 2,
      ts_builtin_sym_end,
      sym_ident,
  [895] = 1,
    ACTIONS(162), 2,
      ts_builtin_sym_end,
      sym_ident,
  [900] = 1,
    ACTIONS(164), 2,
      ts_builtin_sym_end,
      sym_ident,
  [905] = 1,
    ACTIONS(166), 2,
      ts_builtin_sym_end,
      sym_ident,
  [910] = 1,
    ACTIONS(168), 2,
      ts_builtin_sym_end,
      sym_ident,
  [915] = 2,
    ACTIONS(170), 1,
      anon_sym_DASH_GT,
    ACTIONS(172), 1,
      anon_sym_EQ,
  [922] = 2,
    ACTIONS(78), 1,
      anon_sym_LPAREN,
    STATE(77), 1,
      sym_arg_list,
  [929] = 2,
    ACTIONS(174), 1,
      anon_sym_DASH_GT,
    ACTIONS(176), 1,
      anon_sym_EQ,
  [936] = 1,
    ACTIONS(178), 2,
      anon_sym_DASH_GT,
      anon_sym_EQ,
  [941] = 1,
    ACTIONS(180), 2,
      anon_sym_DASH_GT,
      anon_sym_EQ,
  [946] = 1,
    ACTIONS(182), 1,
      anon_sym_COLON,
  [950] = 1,
    ACTIONS(184), 1,
      anon_sym_SEMI,
  [954] = 1,
    ACTIONS(186), 1,
      anon_sym_COLON,
  [958] = 1,
    ACTIONS(188), 1,
      anon_sym_LBRACE,
  [962] = 1,
    ACTIONS(190), 1,
      anon_sym_LPAREN,
  [966] = 1,
    ACTIONS(192), 1,
      sym_ident,
  [970] = 1,
    ACTIONS(194), 1,
      anon_sym_LPAREN,
  [974] = 1,
    ACTIONS(196), 1,
      sym_ident,
  [978] = 1,
    ACTIONS(198), 1,
      anon_sym_EQ,
  [982] = 1,
    ACTIONS(200), 1,
      anon_sym_COLON,
  [986] = 1,
    ACTIONS(202), 1,
      anon_sym_LPAREN,
  [990] = 1,
    ACTIONS(204), 1,
      anon_sym_EQ,
  [994] = 1,
    ACTIONS(206), 1,
      anon_sym_COLON,
  [998] = 1,
    ACTIONS(208), 1,
      anon_sym_LPAREN,
  [1002] = 1,
    ACTIONS(210), 1,
      anon_sym_LPAREN,
  [1006] = 1,
    ACTIONS(212), 1,
      ts_builtin_sym_end,
  [1010] = 1,
    ACTIONS(214), 1,
      anon_sym_EQ,
  [1014] = 1,
    ACTIONS(216), 1,
      sym_ident,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(2)] = 0,
  [SMALL_STATE(3)] = 25,
  [SMALL_STATE(4)] = 50,
  [SMALL_STATE(5)] = 75,
  [SMALL_STATE(6)] = 100,
  [SMALL_STATE(7)] = 125,
  [SMALL_STATE(8)] = 150,
  [SMALL_STATE(9)] = 175,
  [SMALL_STATE(10)] = 200,
  [SMALL_STATE(11)] = 221,
  [SMALL_STATE(12)] = 242,
  [SMALL_STATE(13)] = 263,
  [SMALL_STATE(14)] = 274,
  [SMALL_STATE(15)] = 295,
  [SMALL_STATE(16)] = 306,
  [SMALL_STATE(17)] = 317,
  [SMALL_STATE(18)] = 338,
  [SMALL_STATE(19)] = 359,
  [SMALL_STATE(20)] = 372,
  [SMALL_STATE(21)] = 383,
  [SMALL_STATE(22)] = 404,
  [SMALL_STATE(23)] = 420,
  [SMALL_STATE(24)] = 436,
  [SMALL_STATE(25)] = 449,
  [SMALL_STATE(26)] = 462,
  [SMALL_STATE(27)] = 475,
  [SMALL_STATE(28)] = 484,
  [SMALL_STATE(29)] = 493,
  [SMALL_STATE(30)] = 502,
  [SMALL_STATE(31)] = 515,
  [SMALL_STATE(32)] = 530,
  [SMALL_STATE(33)] = 545,
  [SMALL_STATE(34)] = 558,
  [SMALL_STATE(35)] = 571,
  [SMALL_STATE(36)] = 587,
  [SMALL_STATE(37)] = 601,
  [SMALL_STATE(38)] = 615,
  [SMALL_STATE(39)] = 631,
  [SMALL_STATE(40)] = 645,
  [SMALL_STATE(41)] = 656,
  [SMALL_STATE(42)] = 669,
  [SMALL_STATE(43)] = 676,
  [SMALL_STATE(44)] = 689,
  [SMALL_STATE(45)] = 700,
  [SMALL_STATE(46)] = 711,
  [SMALL_STATE(47)] = 717,
  [SMALL_STATE(48)] = 727,
  [SMALL_STATE(49)] = 737,
  [SMALL_STATE(50)] = 745,
  [SMALL_STATE(51)] = 755,
  [SMALL_STATE(52)] = 765,
  [SMALL_STATE(53)] = 773,
  [SMALL_STATE(54)] = 783,
  [SMALL_STATE(55)] = 793,
  [SMALL_STATE(56)] = 803,
  [SMALL_STATE(57)] = 813,
  [SMALL_STATE(58)] = 823,
  [SMALL_STATE(59)] = 833,
  [SMALL_STATE(60)] = 838,
  [SMALL_STATE(61)] = 843,
  [SMALL_STATE(62)] = 848,
  [SMALL_STATE(63)] = 853,
  [SMALL_STATE(64)] = 858,
  [SMALL_STATE(65)] = 863,
  [SMALL_STATE(66)] = 868,
  [SMALL_STATE(67)] = 873,
  [SMALL_STATE(68)] = 878,
  [SMALL_STATE(69)] = 885,
  [SMALL_STATE(70)] = 890,
  [SMALL_STATE(71)] = 895,
  [SMALL_STATE(72)] = 900,
  [SMALL_STATE(73)] = 905,
  [SMALL_STATE(74)] = 910,
  [SMALL_STATE(75)] = 915,
  [SMALL_STATE(76)] = 922,
  [SMALL_STATE(77)] = 929,
  [SMALL_STATE(78)] = 936,
  [SMALL_STATE(79)] = 941,
  [SMALL_STATE(80)] = 946,
  [SMALL_STATE(81)] = 950,
  [SMALL_STATE(82)] = 954,
  [SMALL_STATE(83)] = 958,
  [SMALL_STATE(84)] = 962,
  [SMALL_STATE(85)] = 966,
  [SMALL_STATE(86)] = 970,
  [SMALL_STATE(87)] = 974,
  [SMALL_STATE(88)] = 978,
  [SMALL_STATE(89)] = 982,
  [SMALL_STATE(90)] = 986,
  [SMALL_STATE(91)] = 990,
  [SMALL_STATE(92)] = 994,
  [SMALL_STATE(93)] = 998,
  [SMALL_STATE(94)] = 1002,
  [SMALL_STATE(95)] = 1006,
  [SMALL_STATE(96)] = 1010,
  [SMALL_STATE(97)] = 1014,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 0),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(92),
  [7] = {.entry = {.count = 1, .reusable = false}}, SHIFT(27),
  [9] = {.entry = {.count = 1, .reusable = false}}, SHIFT(28),
  [11] = {.entry = {.count = 1, .reusable = true}}, SHIFT(18),
  [13] = {.entry = {.count = 1, .reusable = true}}, SHIFT(16),
  [15] = {.entry = {.count = 1, .reusable = true}}, SHIFT(36),
  [17] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_compound_expr_repeat1, 2),
  [19] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_compound_expr_repeat1, 2), SHIFT_REPEAT(16),
  [22] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_compound_expr_repeat1, 2), SHIFT_REPEAT(36),
  [25] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_expr, 1),
  [27] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_mathexpr, 3),
  [29] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_mathexpr, 1),
  [31] = {.entry = {.count = 1, .reusable = true}}, SHIFT(72),
  [33] = {.entry = {.count = 1, .reusable = true}}, SHIFT(67),
  [35] = {.entry = {.count = 1, .reusable = true}}, SHIFT(39),
  [37] = {.entry = {.count = 1, .reusable = true}}, SHIFT(42),
  [39] = {.entry = {.count = 1, .reusable = true}}, SHIFT(59),
  [41] = {.entry = {.count = 1, .reusable = true}}, SHIFT(37),
  [43] = {.entry = {.count = 1, .reusable = true}}, SHIFT(70),
  [45] = {.entry = {.count = 1, .reusable = true}}, SHIFT(20),
  [47] = {.entry = {.count = 1, .reusable = true}}, SHIFT(74),
  [49] = {.entry = {.count = 1, .reusable = true}}, SHIFT(69),
  [51] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_ident, 1),
  [53] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_primitive_type, 1),
  [55] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym__type, 1),
  [57] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 1),
  [59] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2),
  [61] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2), SHIFT_REPEAT(92),
  [64] = {.entry = {.count = 1, .reusable = true}}, SHIFT(65),
  [66] = {.entry = {.count = 1, .reusable = true}}, SHIFT(62),
  [68] = {.entry = {.count = 1, .reusable = true}}, SHIFT(6),
  [70] = {.entry = {.count = 1, .reusable = true}}, SHIFT(85),
  [72] = {.entry = {.count = 1, .reusable = true}}, SHIFT(84),
  [74] = {.entry = {.count = 1, .reusable = true}}, SHIFT(93),
  [76] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_template_list_repeat2, 5, .production_id = 2),
  [78] = {.entry = {.count = 1, .reusable = true}}, SHIFT(68),
  [80] = {.entry = {.count = 1, .reusable = true}}, SHIFT(87),
  [82] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_statement, 2),
  [84] = {.entry = {.count = 1, .reusable = true}}, SHIFT(7),
  [86] = {.entry = {.count = 1, .reusable = true}}, SHIFT(86),
  [88] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_template_list_repeat1, 2), SHIFT_REPEAT(6),
  [91] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_template_list_repeat1, 2),
  [93] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_template_list_repeat2, 4, .production_id = 2),
  [95] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_template_list_repeat1, 2, .production_id = 3),
  [97] = {.entry = {.count = 1, .reusable = true}}, SHIFT(63),
  [99] = {.entry = {.count = 1, .reusable = true}}, SHIFT(89),
  [101] = {.entry = {.count = 1, .reusable = true}}, SHIFT(8),
  [103] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_template_list_repeat2, 2, .production_id = 1),
  [105] = {.entry = {.count = 1, .reusable = true}}, SHIFT(78),
  [107] = {.entry = {.count = 1, .reusable = true}}, SHIFT(97),
  [109] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_template_list_repeat2, 2), SHIFT_REPEAT(85),
  [112] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_template_list_repeat2, 2),
  [114] = {.entry = {.count = 1, .reusable = true}}, SHIFT(41),
  [116] = {.entry = {.count = 1, .reusable = true}}, SHIFT(91),
  [118] = {.entry = {.count = 1, .reusable = true}}, SHIFT(90),
  [120] = {.entry = {.count = 1, .reusable = true}}, SHIFT(71),
  [122] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_arg_list_repeat1, 2),
  [124] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_arg_list_repeat1, 2), SHIFT_REPEAT(97),
  [127] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_struct_def_repeat1, 2),
  [129] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_struct_def_repeat1, 2), SHIFT_REPEAT(89),
  [132] = {.entry = {.count = 1, .reusable = true}}, SHIFT(79),
  [134] = {.entry = {.count = 1, .reusable = true}}, SHIFT(94),
  [136] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_compound_expr, 3),
  [138] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_arg_list, 2),
  [140] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_arg_list_repeat1, 4),
  [142] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_func_def, 10),
  [144] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_struct_def, 7),
  [146] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_definition, 1),
  [148] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_func_def, 7),
  [150] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_struct_def_repeat1, 4),
  [152] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_block, 2),
  [154] = {.entry = {.count = 1, .reusable = true}}, SHIFT(82),
  [156] = {.entry = {.count = 1, .reusable = true}}, SHIFT(60),
  [158] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_func_def, 8),
  [160] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_compound_expr, 4),
  [162] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_struct_def, 6),
  [164] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_block, 3),
  [166] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_func_def, 6),
  [168] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_func_def, 9),
  [170] = {.entry = {.count = 1, .reusable = true}}, SHIFT(4),
  [172] = {.entry = {.count = 1, .reusable = true}}, SHIFT(10),
  [174] = {.entry = {.count = 1, .reusable = true}}, SHIFT(5),
  [176] = {.entry = {.count = 1, .reusable = true}}, SHIFT(21),
  [178] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_arg_list, 5),
  [180] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_arg_list, 6),
  [182] = {.entry = {.count = 1, .reusable = true}}, SHIFT(3),
  [184] = {.entry = {.count = 1, .reusable = true}}, SHIFT(66),
  [186] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [188] = {.entry = {.count = 1, .reusable = true}}, SHIFT(54),
  [190] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_template_list, 6, .production_id = 2),
  [192] = {.entry = {.count = 1, .reusable = true}}, SHIFT(49),
  [194] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_template_list, 3, .production_id = 1),
  [196] = {.entry = {.count = 1, .reusable = true}}, SHIFT(43),
  [198] = {.entry = {.count = 1, .reusable = true}}, SHIFT(12),
  [200] = {.entry = {.count = 1, .reusable = true}}, SHIFT(9),
  [202] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_template_list, 4, .production_id = 1),
  [204] = {.entry = {.count = 1, .reusable = true}}, SHIFT(83),
  [206] = {.entry = {.count = 1, .reusable = true}}, SHIFT(52),
  [208] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_template_list, 5, .production_id = 2),
  [210] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_template_list, 7, .production_id = 2),
  [212] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [214] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [216] = {.entry = {.count = 1, .reusable = true}}, SHIFT(80),
};

#ifdef __cplusplus
extern "C" {
#endif
#ifdef _WIN32
#define extern __declspec(dllexport)
#endif

extern const TSLanguage *tree_sitter_citrus(void) {
  static const TSLanguage language = {
    .version = LANGUAGE_VERSION,
    .symbol_count = SYMBOL_COUNT,
    .alias_count = ALIAS_COUNT,
    .token_count = TOKEN_COUNT,
    .external_token_count = EXTERNAL_TOKEN_COUNT,
    .state_count = STATE_COUNT,
    .large_state_count = LARGE_STATE_COUNT,
    .production_id_count = PRODUCTION_ID_COUNT,
    .field_count = FIELD_COUNT,
    .max_alias_sequence_length = MAX_ALIAS_SEQUENCE_LENGTH,
    .parse_table = &ts_parse_table[0][0],
    .small_parse_table = ts_small_parse_table,
    .small_parse_table_map = ts_small_parse_table_map,
    .parse_actions = ts_parse_actions,
    .symbol_names = ts_symbol_names,
    .symbol_metadata = ts_symbol_metadata,
    .public_symbol_map = ts_symbol_map,
    .alias_map = ts_non_terminal_alias_map,
    .alias_sequences = &ts_alias_sequences[0][0],
    .lex_modes = ts_lex_modes,
    .lex_fn = ts_lex,
    .primary_state_ids = ts_primary_state_ids,
  };
  return &language;
}
#ifdef __cplusplus
}
#endif
