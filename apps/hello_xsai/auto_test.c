#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "ame.h"
#include "mem.h"
// #include "bm_run.h"
// AME GEMM function
extern void ggml_ame_gemm_tile_i8_i32_bT(
    const int8_t * A,
    const int8_t * B,
    int32_t * C
);

// Scalar reference implementation
void reference_gemm_i8_i32_bT(
    const int8_t * A,      // M x K
    const int8_t * B,      // N x K (transposed)
    int32_t * C,           // M x N
    int M, int K, int N
) {
    for (int m = 0; m < M; m++) {
        for (int n = 0; n < N; n++) {
            int32_t sum = 0;
            for (int k = 0; k < K; k++) {
                sum += (int32_t)A[m * K + k] * (int32_t)B[n * K + k];
            }
            C[m * N + n] = sum;
        }
    }
}

int auto_test() {
    const int M = AME_TILE_M;  // 128
    const int K = AME_TILE_K;  // 64
    const int N = AME_TILE_N;  // 128
    // INIT();
    printf("Testing AME GEMM: C(%dx%d) = A(%dx%d) * B^T(%dx%d)\n", M, N, M, K, N, K);
    printf("Note: B is transposed, so B[n,k] is stored at B[n*K + k]\n\n");
    
    int8_t *A, *B;
    int32_t *C_ame, *C_ref;
    
    // Use custom memory allocator for reserved memory region
    A = (int8_t *)my_malloc(M * K * sizeof(int8_t));
    B = (int8_t *)my_malloc(N * K * sizeof(int8_t));
    C_ame = (int32_t *)my_malloc(M * N * sizeof(int32_t));
    C_ref = (int32_t *)my_malloc(M * N * sizeof(int32_t));

    if (!A || !B || !C_ame || !C_ref) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // --- RANDOMIZED TESTS LOOP ---
    // Seed the random number generator
    srand(12345);

    int num_tests = 50; 
    int total_failures = 0;

    printf("Starting Randomized Fuzzing Tests (%d iterations)\n", num_tests);

    for (int t = 0; t < num_tests; t++) {
        // Clear outputs
        memset(C_ame, 0, M * N * sizeof(int32_t));
        memset(C_ref, 0, M * N * sizeof(int32_t));
        
        // Generate random inputs
        // Case 0: All zeros
        // Case 1: All ones
        // Case 2: Max values
        // Case 3: Min values
        // Case 4+: Random values
        
        if (t == 0) {
            printf("  Test Case 0: All Zeros\n");
            memset(A, 0, M * K * sizeof(int8_t));
            memset(B, 0, N * K * sizeof(int8_t));
        } else if (t == 1) {
            printf("  Test Case 1: All Ones\n");
            memset(A, 1, M * K * sizeof(int8_t));
            memset(B, 1, N * K * sizeof(int8_t));
        } else if (t == 2) {
            printf("  Test Case 2: Max Values (127)\n");
            memset(A, 127, M * K * sizeof(int8_t));
            memset(B, 127, N * K * sizeof(int8_t));
        } else if (t == 3) {
            printf("  Test Case 3: Min Values (-128)\n");
            memset(A, -128, M * K * sizeof(int8_t));
            memset(B, -128, N * K * sizeof(int8_t));
        } else {
             // Random fill
             for (int i = 0; i < M * K; i++) A[i] = (int8_t)(rand() % 256);
             for (int i = 0; i < N * K; i++) B[i] = (int8_t)(rand() % 256);
        }

        // Compute reference result (scalar)
        reference_gemm_i8_i32_bT(A, B, C_ref, M, K, N);
        
        // Compute AME result
        // if(t==20){nemu_signal(NOTIFY_PROFILER);}
        ggml_ame_gemm_tile_i8_i32_bT(A, B, C_ame);
        // if(t==20){nemu_signal(NOTIFY_PROFILE_EXIT);}
        // Compare results
        int errors = 0;
        int first_err_idx = -1;
        for (int i=0; i < M*N; i++) {
             if (C_ame[i] != C_ref[i]) {
                 if (errors == 0) first_err_idx = i;
                 errors++;
             }
        }

        if (errors > 0) {
            printf("  [FAIL] Test iteration %d failed with %d errors.\n", t, errors);
            printf("         First mismatch at index %d: AME=%d, REF=%d\n", 
                   first_err_idx, C_ame[first_err_idx], C_ref[first_err_idx]);
            total_failures++;
            if (total_failures > 5) {
                printf("Too many failures, stopping fuzzing.\n");
                break;
            }
        } else {
            // Only print for special cases or every 10th random test
            if (t < 5 || t % 10 == 0) {
                printf("  [PASS] Test iteration %d passed.\n", t);
            }
        }
    }

    if (total_failures == 0) {
        printf("\nAll %d fuzzing tests PASSED.\n", num_tests);
    } else {
         printf("\n%d/%d fuzzing tests FAILED.\n", total_failures, num_tests);
         my_free(A); my_free(B); my_free(C_ame); my_free(C_ref);
         return 2;
    }
    
    // Cleanup
    my_free(A);
    my_free(B);
    my_free(C_ame);
    my_free(C_ref);
    
    return 0;
}
