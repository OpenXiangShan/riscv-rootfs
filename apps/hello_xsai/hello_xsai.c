#include <stdio.h>
#include <unistd.h>
#include "ame.h"

extern int auto_test();
extern int mem_test();
#ifdef __linux__
#define INIT() do { } while (0)
#else
#define INIT()                                                                 \
  do {                                                                         \
    const uint64_t mstatus_mask = (uint64_t)0x2002200;                         \
    asm volatile ("csrs mstatus, %0" :: "r"(mstatus_mask));                    \
    asm volatile("csrwi vcsr,0" ::);                                           \
  } while (0)
#endif

    //   asm volatile("csrw mtvec, %0" : : "r"(__am_asm_trap));                     
int main(void) {
    // INIT();
    puts("Hello, XiangShan AI!");
    puts("hello_xsai is running from XSAI init flow.");
    // nemu_signal(NOTIFY_PROFILE_EXIT);
    int ret = mem_test();
    if (ret != 0) {
        nemu_signal(ret);
        return ret;
    }
    nemu_signal(DISABLE_TIME_INTR);
    ret = auto_test();
    nemu_signal(ret);
    return 0;
}