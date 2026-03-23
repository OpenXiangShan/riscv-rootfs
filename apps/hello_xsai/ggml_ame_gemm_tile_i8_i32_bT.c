#include "ame.h"
#include <stddef.h>
#include <stdio.h>
// #include "bm_run.h"

// Zicbop prefetch hint — reads the cache line containing addr into dcache.
// No exception is raised if addr is invalid; purely a performance hint.
#define PREFETCH_R(addr) \
    asm volatile("prefetch.r 0(%0)" :: "r"(addr) : )

// INT8 GEMM using RISC-V AME instructions
// Tile size: M=AME_TILE_M, K=AME_TILE_K, N=AME_TILE_N (atomic AME variant)
// C(MxN) = A(MxK) × B^T(NxK), where B is transposed in memory
// This function computes a single MxN tile output
void ggml_ame_gemm_tile_i8_i32_bT(
    const int8_t * A,      // Input matrix A: MxK
    const int8_t * B,      // Input matrix B (transposed): NxK
    int32_t * C            // Output matrix C: MxN
) {
    asm volatile("msyncreset tok0" ::: "memory");

    // ----------------------------------------------------------------
    // Prefetch A, B, C tiles into dcache before issuing AME loads.
    //
    // A: AME_TILE_M x AME_TILE_K  int8  = 128 x 64  =  8 KB
    //    row stride = AME_TILE_K = 64 B = 1 cache line (64 B)
    //    -> 128 rows x 1 line/row = 128 prefetches
    //
    // B^T: AME_TILE_N x AME_TILE_K int8  = 128 x 64  =  8 KB
    //    same layout, same count
    //
    // C: AME_TILE_M x AME_TILE_N  int32 = 128 x 128  = 64 KB
    //    row stride = AME_TILE_N * 4 = 512 B = 8 cache lines (64 B each)
    //    -> 128 rows x 8 lines/row = 1024 prefetches
    // ----------------------------------------------------------------
   
#ifdef AME_PREFETCH
    const int CL = 64; /* cache line size in bytes */

    /* Prefetch A: 128 rows, each 64 B = 1 cache line */
    for (int i = 0; i < AME_TILE_M; i++) {
        PREFETCH_R(A + i * AME_TILE_K);
    }

    /* Prefetch B^T: 128 rows, each 64 B = 1 cache line */
    for (int i = 0; i < AME_TILE_N; i++) {
        PREFETCH_R(B + i * AME_TILE_K);
    }

    /* Prefetch C: 128 rows x 512 B/row = 8 cache lines per row */
    {
        const int stride_c_bytes = AME_TILE_N * (int)sizeof(int32_t); /* 512 B */
        const int lines_per_row  = stride_c_bytes / CL;               /* 8 */
        for (int i = 0; i < AME_TILE_M; i++) {
            for (int j = 0; j < lines_per_row; j++) {
                PREFETCH_R((const char*)C + i * stride_c_bytes + j * CL);
            }
        }
    }
#endif /* AME_PREFETCH */
    /* Fixed tile dimensions */
    const int TILE_M = AME_TILE_M;
    const int TILE_K = AME_TILE_K;
    const int TILE_N = AME_TILE_N;

    /* Configure matrix dimensions */
    int tmp;
    MSETTILEM(tmp, TILE_M);
    MSETTILEK(tmp, TILE_K);
    MSETTILEN(tmp, TILE_N);

    /* Preload C matrix to initialize accumulator */
    int32_t *addr_c = C;
    int stride_c = TILE_N; /* Row stride (in elements) */

    MZERO_ACC(acc0);
    printf("addr_c: %p, stride_c: %d\n", (void*)addr_c, stride_c);
    MLCE32(acc0, addr_c, stride_c * 4);

    /* Load left matrix A tile: MxK */
    const int8_t *addr_a = A;
    MLAE8(tr0, addr_a, TILE_K);

    /* Load right matrix B tile (transposed): NxK */
    const int8_t *addr_b = B;
    MLBE8(tr1, addr_b, TILE_K);

    /* INT8 matrix multiply-accumulate: C(MxN) = A(MxK) x B^T(NxK) */
    MQMA(acc0, tr0, tr1);

    /* Store INT32 result to C (MxN) */
    MSCE32(acc0, addr_c, stride_c * 4);

    asm volatile("mrelease tok0" ::: "memory");
    int acquire_target = 1;
    asm volatile("macquire %0,tok0" :: "r"(acquire_target) : "memory");
}
