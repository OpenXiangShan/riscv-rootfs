/*
 * main.c — entry point for gemm_precomp app
 */
#include <stdio.h>
#include <stdlib.h>
#include "ame.h"

extern int precomp_test(void);

int main(void)
{
    int ret = precomp_test();
    if (ret == 0)
        nemu_signal(GOOD_TRAP);
    return ret;
}
