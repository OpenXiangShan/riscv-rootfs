#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <getopt.h>
#include <sys/mman.h>


void nemu_signal(int op)
{
    asm volatile("mv a0, %0; .word 0x0000006b;"::"r"(op));
}


int main(int argc, char const *argv[])
{
    nemu_signal(0x100);//close timer intr
    nemu_signal(0x101);
    uint64_t *arr = mmap(NULL, 64*0x1000,PROT_READ, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    printf("arr addr:%p\n",arr);
    asm volatile(
        "mv a0,%0 \n\t"
        "li t3,0x1000 \n\t"
        "li t2, 16 \n\t"
        "myloop: \n\t"
        "li t0, 1 \n\t"
        "again:\n\t"
        "lw t1, (a0) \n\t"
        "bnez t1, again \n\t"
        "amoswap.w.aq t1, t0, (a0) \n\t"
        "bnez t1, again \n\t"
        "addi t2,t2,-1 \n\t"
        "fence iorw,or \n\t"
        "amoswap.w.rl t5, t2, (a0) \n\t"
        "add a0,a0,t3 \n\t"
        "bnez t2,myloop\n\t"
    :
    :"r"(arr)
    :"memory");
    printf("arr addr:%p\n",arr);
    printf("arr out:%x\n",arr[0x1000/8]);
    return 0;
}
