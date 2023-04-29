#include <tree_sitter/parser.h>

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 37
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 38
#define ALIAS_COUNT 0
#define TOKEN_COUNT 27
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 9
#define PRODUCTION_ID_COUNT 1

enum {
  sym_int = 1,
  sym_ident = 2,
  anon_sym_PLUS = 3,
  anon_sym_DASH = 4,
  anon_sym_STAR = 5,
  anon_sym_SLASH = 6,
  anon_sym_PERCENT = 7,
  anon_sym_LPAREN = 8,
  anon_sym_RPAREN = 9,
  anon_sym_u8 = 10,
  anon_sym_u16 = 11,
  anon_sym_u32 = 12,
  anon_sym_u64 = 13,
  anon_sym_i8 = 14,
  anon_sym_i16 = 15,
  anon_sym_i32 = 16,
  anon_sym_i64 = 17,
  anon_sym_f32 = 18,
  anon_sym_f64 = 19,
  anon_sym_char = 20,
  anon_sym_bool = 21,
  anon_sym_COLON = 22,
  anon_sym_fun = 23,
  anon_sym_DASH_GT = 24,
  anon_sym_EQ = 25,
  anon_sym_SEMI = 26,
  sym_source_file = 27,
  sym_definition = 28,
  sym_expr = 29,
  sym_mathexpr = 30,
  sym_primitive_type = 31,
  sym_type_ident = 32,
  sym__type = 33,
  sym_arg_list = 34,
  sym_fndef = 35,
  aux_sym_source_file_repeat1 = 36,
  aux_sym_arg_list_repeat1 = 37,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
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
  [anon_sym_fun] = "fun",
  [anon_sym_DASH_GT] = "->",
  [anon_sym_EQ] = "=",
  [anon_sym_SEMI] = ";",
  [sym_source_file] = "source_file",
  [sym_definition] = "definition",
  [sym_expr] = "expr",
  [sym_mathexpr] = "mathexpr",
  [sym_primitive_type] = "primitive_type",
  [sym_type_ident] = "type_ident",
  [sym__type] = "_type",
  [sym_arg_list] = "arg_list",
  [sym_fndef] = "fndef",
  [aux_sym_source_file_repeat1] = "source_file_repeat1",
  [aux_sym_arg_list_repeat1] = "arg_list_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
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
  [anon_sym_fun] = anon_sym_fun,
  [anon_sym_DASH_GT] = anon_sym_DASH_GT,
  [anon_sym_EQ] = anon_sym_EQ,
  [anon_sym_SEMI] = anon_sym_SEMI,
  [sym_source_file] = sym_source_file,
  [sym_definition] = sym_definition,
  [sym_expr] = sym_expr,
  [sym_mathexpr] = sym_mathexpr,
  [sym_primitive_type] = sym_primitive_type,
  [sym_type_ident] = sym_type_ident,
  [sym__type] = sym__type,
  [sym_arg_list] = sym_arg_list,
  [sym_fndef] = sym_fndef,
  [aux_sym_source_file_repeat1] = aux_sym_source_file_repeat1,
  [aux_sym_arg_list_repeat1] = aux_sym_arg_list_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
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
  [anon_sym_fun] = {
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
  [anon_sym_SEMI] = {
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
  [sym_expr] = {
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
  [sym_arg_list] = {
    .visible = true,
    .named = true,
  },
  [sym_fndef] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_source_file_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_arg_list_repeat1] = {
    .visible = false,
    .named = false,
  },
};

static const TSSymbol ts_alias_sequences[PRODUCTION_ID_COUNT][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
};

static const uint16_t ts_non_terminal_alias_map[] = {
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
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(16);
      if (lookahead == '%') ADVANCE(37);
      if (lookahead == '(') ADVANCE(38);
      if (lookahead == ')') ADVANCE(39);
      if (lookahead == '*') ADVANCE(35);
      if (lookahead == '+') ADVANCE(32);
      if (lookahead == '-') ADVANCE(34);
      if (lookahead == '/') ADVANCE(36);
      if (lookahead == ':') ADVANCE(52);
      if (lookahead == ';') ADVANCE(57);
      if (lookahead == '=') ADVANCE(56);
      if (lookahead == 'b') ADVANCE(11);
      if (lookahead == 'c') ADVANCE(9);
      if (lookahead == 'f') ADVANCE(5);
      if (lookahead == 'i') ADVANCE(3);
      if (lookahead == 'u') ADVANCE(4);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(0)
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(14);
      END_STATE();
    case 1:
      if (lookahead == '(') ADVANCE(38);
      if (lookahead == '-') ADVANCE(13);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(1)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(17);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(14);
      END_STATE();
    case 2:
      if (lookahead == '-') ADVANCE(7);
      if (lookahead == '=') ADVANCE(56);
      if (lookahead == 'b') ADVANCE(11);
      if (lookahead == 'c') ADVANCE(9);
      if (lookahead == 'f') ADVANCE(6);
      if (lookahead == 'i') ADVANCE(3);
      if (lookahead == 'u') ADVANCE(4);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(2)
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(14);
      END_STATE();
    case 3:
      if (lookahead == '1') ADVANCE(24);
      if (lookahead == '3') ADVANCE(19);
      if (lookahead == '6') ADVANCE(22);
      if (lookahead == '8') ADVANCE(44);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 4:
      if (lookahead == '1') ADVANCE(25);
      if (lookahead == '3') ADVANCE(20);
      if (lookahead == '6') ADVANCE(23);
      if (lookahead == '8') ADVANCE(40);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 5:
      if (lookahead == '3') ADVANCE(18);
      if (lookahead == '6') ADVANCE(21);
      if (lookahead == 'u') ADVANCE(28);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 6:
      if (lookahead == '3') ADVANCE(18);
      if (lookahead == '6') ADVANCE(21);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 7:
      if (lookahead == '>') ADVANCE(55);
      END_STATE();
    case 8:
      if (lookahead == 'f') ADVANCE(12);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(8)
      END_STATE();
    case 9:
      if (lookahead == 'h') ADVANCE(26);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 10:
      if (lookahead == 'n') ADVANCE(53);
      END_STATE();
    case 11:
      if (lookahead == 'o') ADVANCE(29);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 12:
      if (lookahead == 'u') ADVANCE(10);
      END_STATE();
    case 13:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(17);
      END_STATE();
    case 14:
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 15:
      if (eof) ADVANCE(16);
      if (lookahead == '%') ADVANCE(37);
      if (lookahead == ')') ADVANCE(39);
      if (lookahead == '*') ADVANCE(35);
      if (lookahead == '+') ADVANCE(32);
      if (lookahead == '-') ADVANCE(33);
      if (lookahead == '/') ADVANCE(36);
      if (lookahead == ';') ADVANCE(57);
      if (lookahead == '=') ADVANCE(56);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(15)
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(14);
      END_STATE();
    case 16:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 17:
      ACCEPT_TOKEN(sym_int);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(17);
      END_STATE();
    case 18:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '2') ADVANCE(48);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 19:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '2') ADVANCE(46);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 20:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '2') ADVANCE(42);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 21:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '4') ADVANCE(49);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 22:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '4') ADVANCE(47);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 23:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '4') ADVANCE(43);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 24:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '6') ADVANCE(45);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 25:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == '6') ADVANCE(41);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 26:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'a') ADVANCE(30);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 27:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'l') ADVANCE(51);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 28:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'n') ADVANCE(54);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 29:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'o') ADVANCE(27);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 30:
      ACCEPT_TOKEN(sym_ident);
      if (lookahead == 'r') ADVANCE(50);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 31:
      ACCEPT_TOKEN(sym_ident);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 32:
      ACCEPT_TOKEN(anon_sym_PLUS);
      END_STATE();
    case 33:
      ACCEPT_TOKEN(anon_sym_DASH);
      END_STATE();
    case 34:
      ACCEPT_TOKEN(anon_sym_DASH);
      if (lookahead == '>') ADVANCE(55);
      END_STATE();
    case 35:
      ACCEPT_TOKEN(anon_sym_STAR);
      END_STATE();
    case 36:
      ACCEPT_TOKEN(anon_sym_SLASH);
      END_STATE();
    case 37:
      ACCEPT_TOKEN(anon_sym_PERCENT);
      END_STATE();
    case 38:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 39:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 40:
      ACCEPT_TOKEN(anon_sym_u8);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 41:
      ACCEPT_TOKEN(anon_sym_u16);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 42:
      ACCEPT_TOKEN(anon_sym_u32);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 43:
      ACCEPT_TOKEN(anon_sym_u64);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 44:
      ACCEPT_TOKEN(anon_sym_i8);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 45:
      ACCEPT_TOKEN(anon_sym_i16);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 46:
      ACCEPT_TOKEN(anon_sym_i32);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 47:
      ACCEPT_TOKEN(anon_sym_i64);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 48:
      ACCEPT_TOKEN(anon_sym_f32);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 49:
      ACCEPT_TOKEN(anon_sym_f64);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 50:
      ACCEPT_TOKEN(anon_sym_char);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 51:
      ACCEPT_TOKEN(anon_sym_bool);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 52:
      ACCEPT_TOKEN(anon_sym_COLON);
      END_STATE();
    case 53:
      ACCEPT_TOKEN(anon_sym_fun);
      END_STATE();
    case 54:
      ACCEPT_TOKEN(anon_sym_fun);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(31);
      END_STATE();
    case 55:
      ACCEPT_TOKEN(anon_sym_DASH_GT);
      END_STATE();
    case 56:
      ACCEPT_TOKEN(anon_sym_EQ);
      END_STATE();
    case 57:
      ACCEPT_TOKEN(anon_sym_SEMI);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 15},
  [2] = {.lex_state = 2},
  [3] = {.lex_state = 2},
  [4] = {.lex_state = 15},
  [5] = {.lex_state = 15},
  [6] = {.lex_state = 15},
  [7] = {.lex_state = 15},
  [8] = {.lex_state = 15},
  [9] = {.lex_state = 15},
  [10] = {.lex_state = 15},
  [11] = {.lex_state = 15},
  [12] = {.lex_state = 15},
  [13] = {.lex_state = 15},
  [14] = {.lex_state = 1},
  [15] = {.lex_state = 1},
  [16] = {.lex_state = 1},
  [17] = {.lex_state = 1},
  [18] = {.lex_state = 1},
  [19] = {.lex_state = 15},
  [20] = {.lex_state = 15},
  [21] = {.lex_state = 15},
  [22] = {.lex_state = 15},
  [23] = {.lex_state = 15},
  [24] = {.lex_state = 2},
  [25] = {.lex_state = 15},
  [26] = {.lex_state = 2},
  [27] = {.lex_state = 2},
  [28] = {.lex_state = 15},
  [29] = {.lex_state = 0},
  [30] = {.lex_state = 15},
  [31] = {.lex_state = 15},
  [32] = {.lex_state = 0},
  [33] = {.lex_state = 0},
  [34] = {.lex_state = 0},
  [35] = {.lex_state = 8},
  [36] = {.lex_state = 0},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
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
    [anon_sym_fun] = ACTIONS(1),
    [anon_sym_DASH_GT] = ACTIONS(1),
    [anon_sym_EQ] = ACTIONS(1),
    [anon_sym_SEMI] = ACTIONS(1),
  },
  [1] = {
    [sym_source_file] = STATE(36),
    [sym_definition] = STATE(12),
    [sym_fndef] = STATE(30),
    [aux_sym_source_file_repeat1] = STATE(12),
    [ts_builtin_sym_end] = ACTIONS(3),
    [sym_ident] = ACTIONS(5),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 3,
    ACTIONS(7), 1,
      sym_ident,
    STATE(32), 3,
      sym_primitive_type,
      sym_type_ident,
      sym__type,
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
  [23] = 3,
    ACTIONS(7), 1,
      sym_ident,
    STATE(25), 3,
      sym_primitive_type,
      sym_type_ident,
      sym__type,
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
  [46] = 1,
    ACTIONS(11), 7,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_SEMI,
  [56] = 1,
    ACTIONS(13), 7,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_SEMI,
  [66] = 2,
    ACTIONS(15), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
    ACTIONS(13), 4,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_RPAREN,
      anon_sym_SEMI,
  [78] = 1,
    ACTIONS(13), 7,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_SEMI,
  [88] = 1,
    ACTIONS(17), 7,
      anon_sym_PLUS,
      anon_sym_DASH,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
      anon_sym_RPAREN,
      anon_sym_SEMI,
  [98] = 3,
    ACTIONS(21), 1,
      anon_sym_SEMI,
    ACTIONS(19), 2,
      anon_sym_PLUS,
      anon_sym_DASH,
    ACTIONS(15), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
  [111] = 3,
    ACTIONS(23), 1,
      anon_sym_RPAREN,
    ACTIONS(19), 2,
      anon_sym_PLUS,
      anon_sym_DASH,
    ACTIONS(15), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
  [124] = 3,
    ACTIONS(25), 1,
      anon_sym_SEMI,
    ACTIONS(19), 2,
      anon_sym_PLUS,
      anon_sym_DASH,
    ACTIONS(15), 3,
      anon_sym_STAR,
      anon_sym_SLASH,
      anon_sym_PERCENT,
  [137] = 4,
    ACTIONS(5), 1,
      sym_ident,
    ACTIONS(27), 1,
      ts_builtin_sym_end,
    STATE(30), 1,
      sym_fndef,
    STATE(13), 2,
      sym_definition,
      aux_sym_source_file_repeat1,
  [151] = 4,
    ACTIONS(29), 1,
      ts_builtin_sym_end,
    ACTIONS(31), 1,
      sym_ident,
    STATE(30), 1,
      sym_fndef,
    STATE(13), 2,
      sym_definition,
      aux_sym_source_file_repeat1,
  [165] = 4,
    ACTIONS(36), 1,
      anon_sym_LPAREN,
    STATE(5), 1,
      sym_expr,
    STATE(8), 1,
      sym_mathexpr,
    ACTIONS(34), 2,
      sym_int,
      sym_ident,
  [179] = 4,
    ACTIONS(36), 1,
      anon_sym_LPAREN,
    STATE(6), 1,
      sym_expr,
    STATE(8), 1,
      sym_mathexpr,
    ACTIONS(34), 2,
      sym_int,
      sym_ident,
  [193] = 4,
    ACTIONS(36), 1,
      anon_sym_LPAREN,
    STATE(8), 1,
      sym_mathexpr,
    STATE(9), 1,
      sym_expr,
    ACTIONS(34), 2,
      sym_int,
      sym_ident,
  [207] = 4,
    ACTIONS(36), 1,
      anon_sym_LPAREN,
    STATE(8), 1,
      sym_mathexpr,
    STATE(11), 1,
      sym_expr,
    ACTIONS(34), 2,
      sym_int,
      sym_ident,
  [221] = 4,
    ACTIONS(36), 1,
      anon_sym_LPAREN,
    STATE(8), 1,
      sym_mathexpr,
    STATE(10), 1,
      sym_expr,
    ACTIONS(34), 2,
      sym_int,
      sym_ident,
  [235] = 3,
    ACTIONS(38), 1,
      sym_ident,
    ACTIONS(40), 1,
      anon_sym_RPAREN,
    STATE(23), 1,
      aux_sym_arg_list_repeat1,
  [245] = 1,
    ACTIONS(42), 3,
      sym_ident,
      anon_sym_RPAREN,
      anon_sym_EQ,
  [251] = 1,
    ACTIONS(44), 3,
      sym_ident,
      anon_sym_RPAREN,
      anon_sym_EQ,
  [257] = 3,
    ACTIONS(46), 1,
      sym_ident,
    ACTIONS(49), 1,
      anon_sym_RPAREN,
    STATE(22), 1,
      aux_sym_arg_list_repeat1,
  [267] = 3,
    ACTIONS(38), 1,
      sym_ident,
    ACTIONS(51), 1,
      anon_sym_RPAREN,
    STATE(22), 1,
      aux_sym_arg_list_repeat1,
  [277] = 1,
    ACTIONS(53), 2,
      anon_sym_DASH_GT,
      anon_sym_EQ,
  [282] = 1,
    ACTIONS(55), 2,
      sym_ident,
      anon_sym_RPAREN,
  [287] = 1,
    ACTIONS(57), 2,
      anon_sym_DASH_GT,
      anon_sym_EQ,
  [292] = 2,
    ACTIONS(59), 1,
      anon_sym_DASH_GT,
    ACTIONS(61), 1,
      anon_sym_EQ,
  [299] = 1,
    ACTIONS(63), 2,
      ts_builtin_sym_end,
      sym_ident,
  [304] = 2,
    ACTIONS(65), 1,
      anon_sym_LPAREN,
    STATE(27), 1,
      sym_arg_list,
  [311] = 1,
    ACTIONS(67), 2,
      ts_builtin_sym_end,
      sym_ident,
  [316] = 1,
    ACTIONS(69), 2,
      ts_builtin_sym_end,
      sym_ident,
  [321] = 1,
    ACTIONS(71), 1,
      anon_sym_EQ,
  [325] = 1,
    ACTIONS(73), 1,
      anon_sym_COLON,
  [329] = 1,
    ACTIONS(75), 1,
      anon_sym_COLON,
  [333] = 1,
    ACTIONS(77), 1,
      anon_sym_fun,
  [337] = 1,
    ACTIONS(79), 1,
      ts_builtin_sym_end,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(2)] = 0,
  [SMALL_STATE(3)] = 23,
  [SMALL_STATE(4)] = 46,
  [SMALL_STATE(5)] = 56,
  [SMALL_STATE(6)] = 66,
  [SMALL_STATE(7)] = 78,
  [SMALL_STATE(8)] = 88,
  [SMALL_STATE(9)] = 98,
  [SMALL_STATE(10)] = 111,
  [SMALL_STATE(11)] = 124,
  [SMALL_STATE(12)] = 137,
  [SMALL_STATE(13)] = 151,
  [SMALL_STATE(14)] = 165,
  [SMALL_STATE(15)] = 179,
  [SMALL_STATE(16)] = 193,
  [SMALL_STATE(17)] = 207,
  [SMALL_STATE(18)] = 221,
  [SMALL_STATE(19)] = 235,
  [SMALL_STATE(20)] = 245,
  [SMALL_STATE(21)] = 251,
  [SMALL_STATE(22)] = 257,
  [SMALL_STATE(23)] = 267,
  [SMALL_STATE(24)] = 277,
  [SMALL_STATE(25)] = 282,
  [SMALL_STATE(26)] = 287,
  [SMALL_STATE(27)] = 292,
  [SMALL_STATE(28)] = 299,
  [SMALL_STATE(29)] = 304,
  [SMALL_STATE(30)] = 311,
  [SMALL_STATE(31)] = 316,
  [SMALL_STATE(32)] = 321,
  [SMALL_STATE(33)] = 325,
  [SMALL_STATE(34)] = 329,
  [SMALL_STATE(35)] = 333,
  [SMALL_STATE(36)] = 337,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 0),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(33),
  [7] = {.entry = {.count = 1, .reusable = false}}, SHIFT(21),
  [9] = {.entry = {.count = 1, .reusable = false}}, SHIFT(20),
  [11] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_mathexpr, 1),
  [13] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_mathexpr, 3),
  [15] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [17] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_expr, 1),
  [19] = {.entry = {.count = 1, .reusable = true}}, SHIFT(15),
  [21] = {.entry = {.count = 1, .reusable = true}}, SHIFT(31),
  [23] = {.entry = {.count = 1, .reusable = true}}, SHIFT(7),
  [25] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [27] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 1),
  [29] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2),
  [31] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2), SHIFT_REPEAT(33),
  [34] = {.entry = {.count = 1, .reusable = true}}, SHIFT(4),
  [36] = {.entry = {.count = 1, .reusable = true}}, SHIFT(18),
  [38] = {.entry = {.count = 1, .reusable = true}}, SHIFT(34),
  [40] = {.entry = {.count = 1, .reusable = true}}, SHIFT(26),
  [42] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_primitive_type, 1),
  [44] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_ident, 1),
  [46] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_arg_list_repeat1, 2), SHIFT_REPEAT(34),
  [49] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_arg_list_repeat1, 2),
  [51] = {.entry = {.count = 1, .reusable = true}}, SHIFT(24),
  [53] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_arg_list, 3),
  [55] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_arg_list_repeat1, 3),
  [57] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_arg_list, 2),
  [59] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [61] = {.entry = {.count = 1, .reusable = true}}, SHIFT(17),
  [63] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_fndef, 7),
  [65] = {.entry = {.count = 1, .reusable = true}}, SHIFT(19),
  [67] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_definition, 1),
  [69] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_fndef, 9),
  [71] = {.entry = {.count = 1, .reusable = true}}, SHIFT(16),
  [73] = {.entry = {.count = 1, .reusable = true}}, SHIFT(35),
  [75] = {.entry = {.count = 1, .reusable = true}}, SHIFT(3),
  [77] = {.entry = {.count = 1, .reusable = true}}, SHIFT(29),
  [79] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
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
