#include <stdio.h>

int main() {
	asm("li a0, 0\n");
    asm(".word 0x0000006b\n");
}
