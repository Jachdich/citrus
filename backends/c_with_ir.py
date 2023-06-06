from enum import StrEnum, unique


# TODO
# ok what actually *is* a type? should it store the whole struct(for example) or just the name? what does it do? ?????????
@unique
class Primitive(StrEnum):
    I8 = "i8"
    I16 = "i16"
    I32 = "i32"
    I64 = "i64"
    U8 = "u8"
    U16 = "u16"
    U32 = "u32"
    U64 = "u64"
    F32 = "f32"
    F64 = "f64"
    CHAR = "char"
    VOID = "void"
    STRUCT = "struct"
    FUNCTION = "fn"

class Type:
    def __init__(self, primitive, name=None, generics=None):
        if primitive == Primitive.STRUCT or primitive == Primitive.FUNCTION:
            assert name is not None, "Structs must have a name"
            self.name = name

            if generics is not None:
                self.generics = generics
            else:
                self.generics = []

            self.complex = True # dealing with a complex type
        else:
            self.complex = False # just the primitive

        self.primitive = primitive

    def get_mangled_name(self, resolved_generics: dict=None):
        if not self.complex:
            # just a primitive
            return self.primitive
        else:
            if resolved_generics is None and len(self.generics) > 0:
                raise RuntimeException("Cannot get mangled name without knowing the generic resolutions!")
            return self.name + "".join(["_" + resolved_generics[g].get_mangled_name() for g in self.generics])

class CG:
    def __init__(self, fname):
        self.fname = fname
    # TODO figure out IR, should import statements modify first IR? maybe
