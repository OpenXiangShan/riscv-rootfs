#ifndef MEM_H
#define MEM_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// Custom memory allocator using reserved memory region
// These functions provide aligned allocation suitable for AME operations
void* my_malloc(size_t size);
void my_free(void *ptr);

#ifdef __cplusplus
}
#endif

#endif // MEM_H
