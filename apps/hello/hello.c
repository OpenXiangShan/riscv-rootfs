#include <stdio.h>
#include <sys/syscall.h>
#include "events.h"
#include <stdint.h>

#define SET_PERF_EXPECT 1
#define SET_PERF 294
#define GET_PERF_EXPECT 2
#define GET_PERF 295

#define MODE_OFFSET 59
#define MODE_MASK 0x1F
#define MODE_M 0x10
#define MODE_H 0x08
#define MODE_S 0x04
#define MODE_U 0x02
#define MODE_D 0x01

#define OPTYPE2_OFFSET 50
#define OPTYPE2_MASK 0x1F
#define OPTYPE1_OFFSET 45
#define OPTYPE1_MASK 0x1F
#define OPTYPE0_OFFSET 40
#define OPTYPE0_MASK 0x1F
#define OPTYPE_OR 0x0
#define OPTYPE_AND 0x1
#define OPTYPE_XOR 0x2
#define OPTYPE_ADD 0x4
// Operations
// Event0 <Optype0> Event1 = T1
// Event2 <Optype1> Event3 = T2
// T1 <Optype2> T2 = Result

#define EVENT3_OFFSET 30
#define EVENT3_MASK 0x3FF
#define EVENT2_OFFSET 20
#define EVENT2_MASK 0x3FF
#define EVENT1_OFFSET 10
#define EVENT1_MASK 0x3FF
#define EVENT0_OFFSET 0
#define EVENT0_MASK 0x3FF

#define SET(reg, field, value) (reg) = ((reg) & ~((uint64_t)(field##_MASK) << (field##_OFFSET))) | ((uint64_t)(value) << (field##_OFFSET));

#define EVENT_BASE 0x320
#define COUNTER_BASE 0xb00

#define clear_counter(id) syscall(SET_PERF, COUNTER_BASE + id, 0x0UL)
#define clear_event(id) syscall(SET_PERF, EVENT_BASE + id, 0x0UL)

#define print_event(id) printf("mhpmevent%d: %lx\n", id, syscall(GET_PERF, EVENT_BASE + id))
#define print_counter(id) printf("mhpmcounter%d: %lu\n", id, syscall(GET_PERF, COUNTER_BASE + id))
#define printd_csr(csr) printf(#csr": %ld\n", syscall(GET_PERF, csr))
#define printu_csr(csr) printf(#csr": %lu\n", syscall(GET_PERF, csr))
#define printx_csr(csr) printf(#csr": %lx\n", syscall(GET_PERF, csr))

#define set_event_quad(csr_id, mode, optype2, optype1, optype0, event3, event2, event1, event0) \
    {   \
        uint64_t value = syscall(GET_PERF, EVENT_BASE + csr_id); \
        SET(value, MODE, mode); \
        SET(value, OPTYPE2, optype2); \
        SET(value, OPTYPE1, optype1); \
        SET(value, OPTYPE0, optype0); \
        SET(value, EVENT3, event3); \
        SET(value, EVENT2, event2); \
        SET(value, EVENT1, event1); \
        SET(value, EVENT0, event0); \
        syscall(SET_PERF, EVENT_BASE + csr_id, value); \
    }

#define set_event_double(csr_id, mode, optype0, event1, event0) \
    set_event_quad(csr_id, mode, OPTYPE_OR, OPTYPE_OR, optype0, noEvent, noEvent, event1, event0)

#define set_event_single(csr_id, mode, event)\
    set_event_quad(csr_id, mode, OPTYPE_OR, OPTYPE_OR, OPTYPE_OR, noEvent, noEvent, noEvent, event)

// set event and clear counter
#define se_cc_quad(csr_id, mode, optype2, optype1, optype0, event3, event2, event1, event0) \
    {set_event_quad(csr_id, mode, optype2, optype1, optype0, event3, event2, event1, event0);clear_counter(csr_id);}
#define se_cc_double(csr_id, mode, optype0, event1, event0) \
    {set_event_double(csr_id, mode, optype0, event1, event0);clear_counter(csr_id);}
#define se_cc_single(csr_id, mode, event) \
    {set_event_single(csr_id, mode, event);clear_counter(csr_id);}


int main() {
	printf("Hello, RISC-V World!\n");
	
    se_cc_single(3, MODE_M, Frontend_frontendFlush);
    se_cc_single(11, MODE_M, CtrlBlock_decoder_waitInstr);
    se_cc_double(19, MODE_M, OPTYPE_ADD, MemBlock_loadpipe0_load_req, MemBlock_loadpipe1_load_req);

    // === tmp workload ===
    volatile uint64_t a = 0;
    for(uint64_t i = 0; i < 100; i++) {
        a += a + i;
    }
    printf("%lu\n",a);

    print_event(3);
    print_counter(3);
    print_event(11);
    print_counter(11);
    print_event(19);
    print_counter(19);

	printf("hanging\n");
	while(1);
}
