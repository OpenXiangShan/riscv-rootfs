/*
 * pmu_test.c — bare-metal RISC-V PMU sanity check
 *
 * Tests that rdcycle / rdtime / rdinstret CSRs are accessible from user mode
 * and that their values advance as expected.
 *
 * Exit codes:
 *   0  all counters working
 *   1  rdcycle stuck at 0 (mcountinhibit.CY set or scounteren.CY clear)
 *   2  rdtime  stuck at 0
 *   3  rdinstret stuck at 0
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static inline uint64_t rdcycle(void)
{
#if defined(__riscv)
    uint64_t v;
    asm volatile("rdcycle %0" : "=r"(v));
    return v;
#else
    return 0;
#endif
}

static inline uint64_t rdtime(void)
{
#if defined(__riscv)
    uint64_t v;
    asm volatile("rdtime %0" : "=r"(v));
    return v;
#else
    return 0;
#endif
}

static inline uint64_t rdinstret(void)
{
#if defined(__riscv)
    uint64_t v;
    asm volatile("rdinstret %0" : "=r"(v));
    return v;
#else
    return 0;
#endif
}

/* Prevent the compiler from optimising the spin away */
static volatile uint64_t sink;

static void spin(unsigned n)
{
    for (unsigned i = 0; i < n; i++)
        sink += i;
}

int main(void)
{
    printf("=== RISC-V PMU user-mode access test ===\n");

    /* ---------- rdcycle ---------- */
    uint64_t cy0 = rdcycle();
    spin(100000);
    uint64_t cy1 = rdcycle();
    uint64_t dcy = cy1 - cy0;
    printf("rdcycle  : before=%llu  after=%llu  delta=%llu  %s\n",
           (unsigned long long)cy0,
           (unsigned long long)cy1,
           (unsigned long long)dcy,
           dcy > 0 ? "OK" : "FAIL (stuck at 0)");

    /* ---------- rdtime ---------- */
    uint64_t tm0 = rdtime();
    spin(100000);
    uint64_t tm1 = rdtime();
    uint64_t dtm = tm1 - tm0;
    printf("rdtime   : before=%llu  after=%llu  delta=%llu  %s\n",
           (unsigned long long)tm0,
           (unsigned long long)tm1,
           (unsigned long long)dtm,
           dtm > 0 ? "OK" : "FAIL (stuck at 0)");

    /* ---------- rdinstret ---------- */
    uint64_t ir0 = rdinstret();
    spin(100000);
    uint64_t ir1 = rdinstret();
    uint64_t dir = ir1 - ir0;
    printf("rdinstret: before=%llu  after=%llu  delta=%llu  %s\n",
           (unsigned long long)ir0,
           (unsigned long long)ir1,
           (unsigned long long)dir,
           dir > 0 ? "OK" : "FAIL (stuck at 0)");

    /* ---------- IPC estimate ---------- */
    if (dcy > 0 && dir > 0) {
        printf("IPC (spin workload): %.3f\n", (double)dir / (double)dcy);
    }

    printf("=========================================\n");

    if (dcy == 0) { fprintf(stderr, "[pmu_test] FAIL: rdcycle did not advance\n"); return 1; }
    if (dtm == 0) { fprintf(stderr, "[pmu_test] FAIL: rdtime did not advance\n");  return 2; }
    if (dir == 0) { fprintf(stderr, "[pmu_test] FAIL: rdinstret did not advance\n"); return 3; }

    printf("[pmu_test] PASS\n");
    return 0;
}
