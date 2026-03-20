/*
 * mem.c - Pure C custom memory allocator using a reserved memory region.
 *
 * Uses a simple free-list with first-fit allocation and block coalescing.
 * All allocations are padded to 64-byte alignment (suitable for AME).
 *
 * Replaces the C++ std::map/std::set based allocator to avoid linking
 * against libstdc++.
 */

#include "mem.h"
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#ifndef RESERVED_MEMORY_SIZE
#define RESERVED_MEMORY_SIZE (1024L * 1024L * 1024L) /* 1 GB */
#endif

/* Each free block is stored as an intrusive linked list node at the
 * start of the free region. */
typedef struct free_block {
    size_t size;              /* usable bytes following this header */
    struct free_block *next;
    /* pad to ALIGN so that the payload after an alloc header is aligned */
    char _pad[64 - sizeof(size_t) - sizeof(void *)];
} free_block_t;

/* Each allocated block has a small header stored just before the
 * pointer returned to the caller.
 * Padded to exactly ALIGN bytes so the payload is always ALIGN-aligned. */
typedef struct alloc_header {
    size_t size;              /* usable bytes following this header */
    char _pad[64 - sizeof(size_t)];
} alloc_header_t;

#define ALLOC_HDR_SIZE  (sizeof(alloc_header_t))   /* == ALIGN == 64 */
#define FREE_HDR_SIZE   (sizeof(free_block_t))      /* == ALIGN == 64 */
/* Minimum block alignment – must equal header sizes */
#define ALIGN           64

static void   *pool_base  = NULL;
static size_t  pool_size  = 0;
static free_block_t *free_list = NULL;  /* sorted by address */

static size_t align_up(size_t v, size_t a) {
    return (v + a - 1) & ~(a - 1);
}

static int pool_init(void) {
    pool_size = RESERVED_MEMORY_SIZE;
#ifdef RESERVED_PHYS_BASE_ADDR
    fprintf(stderr, "[mem] mode=phys  phys_base=0x%lx  size=%zu MB\n",
            (unsigned long)RESERVED_PHYS_BASE_ADDR, pool_size >> 20);
    int fd = open("/dev/mem", O_RDWR);
    if (fd < 0) {
        fprintf(stderr, "[mem] open /dev/mem failed (need root?)\n");
        return -1;
    }
    pool_base = mmap(NULL, pool_size, PROT_READ | PROT_WRITE,
                     MAP_SHARED, fd, RESERVED_PHYS_BASE_ADDR);
    close(fd);
#else
    fprintf(stderr, "[mem] mode=anon  size=%zu MB\n", pool_size >> 20);
    pool_base = mmap(NULL, pool_size, PROT_READ | PROT_WRITE,
                     MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    fprintf(stderr, "[mem] pool_base = %p\n", pool_base);
#endif
    if (pool_base == MAP_FAILED) {
        fprintf(stderr, "[mem] mmap failed\n");
        pool_base = NULL;
        return -1;
    }

    /* Initialise the single free block covering the whole pool */
    free_list = (free_block_t *)pool_base;
    free_list->size = pool_size - FREE_HDR_SIZE;
    free_list->next = NULL;
    return 0;
}

void *my_malloc(size_t size) {
    if (size == 0) return NULL;

    if (pool_base == NULL) {
        if (pool_init() != 0) return NULL;
    }

    /* Round up to alignment and reserve space for the alloc header */
    size_t need = align_up(size + ALLOC_HDR_SIZE, ALIGN);

    free_block_t *prev = NULL;
    free_block_t *cur  = free_list;
    while (cur) {
        if (cur->size + FREE_HDR_SIZE >= need) {
            /* Split the block if there is enough room for a new free node */
            size_t leftover = (cur->size + FREE_HDR_SIZE) - need;
            if (leftover >= FREE_HDR_SIZE + ALIGN) {
                free_block_t *split = (free_block_t *)((char *)cur + need);
                split->size = leftover - FREE_HDR_SIZE;
                split->next = cur->next;
                cur->next   = split;         /* temporary, removed below */
            }

            /* Unlink cur from the free list */
            if (prev) prev->next = cur->next;
            else       free_list = cur->next;

            /* Write alloc header at cur, return payload after it */
            alloc_header_t *hdr = (alloc_header_t *)cur;
            hdr->size = need - ALLOC_HDR_SIZE;
            return (char *)hdr + ALLOC_HDR_SIZE;
        }
        prev = cur;
        cur  = cur->next;
    }

    fprintf(stderr, "[mem] out of memory (requested %zu bytes)\n", size);
    return NULL;
}

void my_free(void *ptr) {
    if (!ptr) return;

    alloc_header_t *hdr  = (alloc_header_t *)((char *)ptr - ALLOC_HDR_SIZE);
    free_block_t   *blk  = (free_block_t *)hdr;
    blk->size = hdr->size + ALLOC_HDR_SIZE - FREE_HDR_SIZE;

    /* Insert into free list sorted by address */
    free_block_t *prev = NULL;
    free_block_t *cur  = free_list;
    while (cur && (char *)cur < (char *)blk) {
        prev = cur;
        cur  = cur->next;
    }
    blk->next = cur;
    if (prev) prev->next = blk;
    else       free_list = blk;

    /* Coalesce with next block */
    if (blk->next &&
        (char *)blk + FREE_HDR_SIZE + blk->size == (char *)blk->next) {
        blk->size += FREE_HDR_SIZE + blk->next->size;
        blk->next  = blk->next->next;
    }

    /* Coalesce with previous block */
    if (prev &&
        (char *)prev + FREE_HDR_SIZE + prev->size == (char *)blk) {
        prev->size += FREE_HDR_SIZE + blk->size;
        prev->next  = blk->next;
    }
}
