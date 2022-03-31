#include <stdio.h>

void nemu_signal(int op)
{
    asm volatile("mv a0, %0; .word 0x0000006b;"::"r"(op));
}


int main(int argc, char const *argv[])
{
    nemu_signal(0);
    return 0;
}
