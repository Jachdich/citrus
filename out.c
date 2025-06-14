#include "citrus.h"
// const TypeIdent(GenericIdent(printf)) = func((Ident(_), TypeIdent(GenericIdent(char)))): None, None;
// const TypeIdent(GenericIdent(main)) = func((Ident(argc), TypeIdent(GenericIdent(i32))), (Ident(argv), TypeIdent(GenericIdent(char)))): TypeIdent(GenericIdent(i32)), { FuncCall(Ident(printf)([NumLit(3)])); 0 };
i32 main(i32 argc, char** argv) {
    printf(3);
    return 0;
}

