#include "ame.h"
#include <stddef.h>
// #include <stdio.h>
// #include "bm_run.h"

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
    // Fixed tile dimensions
    const int TILE_M = AME_TILE_M;
    const int TILE_K = AME_TILE_K;
    const int TILE_N = AME_TILE_N;
    
    // Configure matrix dimensions
    int tmp;
    MSETTILEM(tmp, TILE_M);
    MSETTILEK(tmp, TILE_K);
    MSETTILEN(tmp, TILE_N);

    // Preload C matrix to initialize accumulator 
    // MLCE32 will zero accumulator if C is zero, or add to it if non-zero
    int32_t *addr_c = C;
    int stride_c = TILE_N; // Row stride (in elements)

    MZERO_ACC(acc0);
    MLCE32(acc0, addr_c, stride_c * 4);

    // Load left matrix A tile: MxK
    const int8_t *addr_a = A;
    MLAE8(tr0, addr_a, TILE_K);

    // Load right matrix B tile (transposed): NxK
    const int8_t *addr_b = B;
    MLBE8(tr1, addr_b, TILE_K);

    // INT8 matrix multiply-accumulate: C(MxN) = A(MxK) × B^T(NxK)
    MQMA(acc0, tr0, tr1);

    // Store INT32 result to C (MxN)
    MSCE32(acc0, addr_c, stride_c * 4);

    asm volatile("mrelease tok0" ::: "memory");
    // 期望 tok0 >= 1，使用一个整型输入寄存器传入比较值
    int acquire_target = 1;
    asm volatile("macquire %0,tok0" :: "r"(acquire_target) : "memory"); // 等待 tok0 >= 1
}
