
#include <stdint.h>
#define i8  int8_t
#define i16 int16_t
#define i32 int32_t
#define i64 int64_t
#define u8  uint8_t
#define u16 uint16_t
#define u32 uint32_t
#define u64 uint64_t
#define f32 float
#define f64 double

typedef struct {
    u32 length;
    char* data;
} String;

void* malloc(u64);
void* memcpy(void*, void*, u64);
void* memset(void*, i32, u64);
void free(void*);
u64 strlen(char*);
u64 len(String* self) {
    return (self)->length;
}

