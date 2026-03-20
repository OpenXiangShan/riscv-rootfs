/*
 * mem_test.c - Unit tests for the custom memory allocator in mem.c
 *
 * Tests:
 *   0. Basic alloc/free
 *   1. Multiple allocs, then free in order
 *   2. Free in reverse order (coalesce right-then-left)
 *   3. Free in middle, check fragmentation then refill
 *   4. Alignment check (all returned pointers must be 64-byte aligned)
 *   5. Write & read back (basic memory integrity)
 *   6. Alloc all, free all, re-alloc one large block (full coalesce)
 *   7. Zero-size alloc returns NULL (no crash)
 */

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "mem.h"

#define N_PTRS  16
#define CHUNK   (4096)          /* 4 KB each */
#define PASS    "[PASS]"
#define FAIL    "[FAIL]"

static int total_pass = 0;
static int total_fail = 0;

#define CHECK(cond, msg) \
    do { \
        if (cond) { printf("  " PASS " %s\n", msg); total_pass++; } \
        else       { printf("  " FAIL " %s\n", msg); total_fail++; } \
    } while (0)

/* ------------------------------------------------------------------ */
/* Test 0: basic single alloc/free                                      */
/* ------------------------------------------------------------------ */
static void test_basic(void) {
    printf("Test 0: Basic alloc/free\n");
    void *p = my_malloc(128);
    CHECK(p != NULL, "alloc 128 bytes returns non-NULL");
    my_free(p);
    /* After free, allocate again – should succeed */
    void *p2 = my_malloc(128);
    CHECK(p2 != NULL, "alloc 128 bytes again after free returns non-NULL");
    my_free(p2);
}

/* ------------------------------------------------------------------ */
/* Test 1: multiple allocs freed in order                               */
/* ------------------------------------------------------------------ */
static void test_multi_alloc_free_forward(void) {
    printf("Test 1: Multiple allocs, free in order\n");
    void *ptrs[N_PTRS];
    int ok = 1;
    for (int i = 0; i < N_PTRS; i++) {
        ptrs[i] = my_malloc(CHUNK);
        if (!ptrs[i]) { ok = 0; break; }
    }
    CHECK(ok, "all 16 allocs succeed");
    for (int i = 0; i < N_PTRS; i++)
        my_free(ptrs[i]);
    /* Pool should be fully coalesced – one big alloc should work */
    void *big = my_malloc(CHUNK * N_PTRS);
    CHECK(big != NULL, "large alloc succeeds after full coalesce");
    my_free(big);
}

/* ------------------------------------------------------------------ */
/* Test 2: free in reverse order                                        */
/* ------------------------------------------------------------------ */
static void test_multi_alloc_free_reverse(void) {
    printf("Test 2: Multiple allocs, free in reverse order\n");
    void *ptrs[N_PTRS];
    int ok = 1;
    for (int i = 0; i < N_PTRS; i++) {
        ptrs[i] = my_malloc(CHUNK);
        if (!ptrs[i]) { ok = 0; break; }
    }
    CHECK(ok, "all 16 allocs succeed");
    for (int i = N_PTRS - 1; i >= 0; i--)
        my_free(ptrs[i]);
    void *big = my_malloc(CHUNK * N_PTRS);
    CHECK(big != NULL, "large alloc succeeds after reverse-order free coalesce");
    my_free(big);
}

/* ------------------------------------------------------------------ */
/* Test 3: free middle block, check fragmentation, then free rest       */
/* ------------------------------------------------------------------ */
static void test_fragmentation(void) {
    printf("Test 3: Fragmentation / hole in middle\n");
    void *a = my_malloc(CHUNK);
    void *b = my_malloc(CHUNK);
    void *c = my_malloc(CHUNK);
    CHECK(a && b && c, "three allocs succeed");
    my_free(b);   /* hole in the middle */
    /* Allocate something that fits in the hole */
    void *b2 = my_malloc(CHUNK / 2);
    CHECK(b2 != NULL, "alloc in freed hole succeeds");
    my_free(a);
    my_free(b2);
    my_free(c);
    /* Everything freed – big alloc should work */
    void *big = my_malloc(CHUNK * 3);
    CHECK(big != NULL, "large alloc after defrag succeeds");
    my_free(big);
}

/* ------------------------------------------------------------------ */
/* Test 4: alignment                                                    */
/* ------------------------------------------------------------------ */
static void test_alignment(void) {
    printf("Test 4: 64-byte alignment\n");
    void *ptrs[8];
    int ok = 1;
    for (int i = 0; i < 8; i++) {
        ptrs[i] = my_malloc(1 + i * 13);   /* odd sizes */
        if (!ptrs[i] || ((uintptr_t)ptrs[i] & 63) != 0) {
            ok = 0;
        }
    }
    CHECK(ok, "all pointers are 64-byte aligned");
    for (int i = 0; i < 8; i++) my_free(ptrs[i]);
}

/* ------------------------------------------------------------------ */
/* Test 5: write and read back                                          */
/* ------------------------------------------------------------------ */
static void test_write_read(void) {
    printf("Test 5: Write / read-back integrity\n");
    const size_t SZ = 1024;
    uint8_t *buf = (uint8_t *)my_malloc(SZ);
    CHECK(buf != NULL, "alloc 1024 bytes");
    if (buf) {
        for (size_t i = 0; i < SZ; i++) buf[i] = (uint8_t)(i & 0xFF);
        int ok = 1;
        for (size_t i = 0; i < SZ; i++) {
            if (buf[i] != (uint8_t)(i & 0xFF)) { ok = 0; break; }
        }
        CHECK(ok, "data read back matches written pattern");
        my_free(buf);
    }
}

/* ------------------------------------------------------------------ */
/* Test 6: alloc all → free all → one giant re-alloc                   */
/* ------------------------------------------------------------------ */
static void test_full_coalesce(void) {
    printf("Test 6: Alloc all, free all, re-alloc single large block\n");
    /* Allocate many small chunks */
    const int M = 64;
    void *ptrs[64];
    int ok = 1;
    for (int i = 0; i < M; i++) {
        ptrs[i] = my_malloc(512);
        if (!ptrs[i]) { ok = 0; break; }
    }
    CHECK(ok, "64 x 512-byte allocs succeed");
    /* Free all in random-ish order (interleaved) */
    for (int i = 0; i < M; i += 2) my_free(ptrs[i]);
    for (int i = 1; i < M; i += 2) my_free(ptrs[i]);
    /* Now one large alloc should fit */
    void *big = my_malloc(512 * M);
    CHECK(big != NULL, "single large re-alloc after full coalesce succeeds");
    if (big) my_free(big);
}

/* ------------------------------------------------------------------ */
/* Test 7: zero-size alloc                                              */
/* ------------------------------------------------------------------ */
static void test_zero_alloc(void) {
    printf("Test 7: Zero-size alloc returns NULL\n");
    void *p = my_malloc(0);
    CHECK(p == NULL, "my_malloc(0) == NULL");
    /* Calling free(NULL) must not crash */
    my_free(NULL);
    CHECK(1, "my_free(NULL) does not crash");
}

/* ------------------------------------------------------------------ */
/* Entry point                                                          */
/* ------------------------------------------------------------------ */
int mem_test(void) {
    printf("\n=== mem_test: custom allocator unit tests ===\n");
    test_basic();
    test_multi_alloc_free_forward();
    test_multi_alloc_free_reverse();
    test_fragmentation();
    test_alignment();
    test_write_read();
    test_full_coalesce();
    test_zero_alloc();

    printf("\n=== Results: %d passed, %d failed ===\n", total_pass, total_fail);
    return total_fail == 0 ? 0 : 1;
}
