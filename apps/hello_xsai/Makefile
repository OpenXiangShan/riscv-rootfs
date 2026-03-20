NAME = hello_xsai
SRCS = hello_xsai.c auto_test.c ggml_ame_gemm_tile_i8_i32_bT.c mem.c mem_test.c
STATIC_DEBUG ?= 1

THIS_MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
XSAI_ENV_ROOT_FALLBACK := $(abspath $(THIS_MAKEFILE_DIR)/../../../..)
AME_LLVM_BIN := $(LLVM_HOME)/bin
AME_CLANG_RESOLVED := $(AME_LLVM_BIN)/clang
AME_OBJDUMP := $(AME_LLVM_BIN)/llvm-objdump

ifeq ($(strip $(LLVM_HOME)),)
$(error LLVM_HOME is not set. Please export LLVM_HOME and use full path toolchain)
endif

ifeq ($(wildcard $(AME_CLANG_RESOLVED)),)
$(error clang not found at $(AME_CLANG_RESOLVED))
endif

ifeq ($(wildcard $(AME_OBJDUMP)),)
$(error llvm-objdump not found at $(AME_OBJDUMP))
endif

AME_TARGET = -target riscv64-unknown-linux-gnu
AME_ARCH = -march=rv64g_v_zvfh_zame_zvl128b_zicbop_zihintpause
AME_FEATURE = -Xclang -target-feature -Xclang +matrix-xuantie-0.6

RESERVED_PHYS_BASE_ADDR ?= 0x100000000UL
RESERVED_MEMORY_SIZE    ?= 0x180000000UL

CFLAGS += $(AME_TARGET) $(AME_ARCH) $(AME_FEATURE)
CFLAGS += -DRESERVED_PHYS_BASE_ADDR=$(RESERVED_PHYS_BASE_ADDR)
CFLAGS += -DRESERVED_MEMORY_SIZE=$(RESERVED_MEMORY_SIZE)
LDFLAGS += $(AME_TARGET) $(AME_ARCH) $(AME_FEATURE)

include $(RISCV_ROOTFS_HOME)/Makefile.compile
AME_OBJ ?= $(DST_DIR)/auto_test.o
AME_DISASM ?= $(DST_DIR)/auto_test.S
STATIC_DEBUG_CFLAGS ?= -O0 -g3 -fno-omit-frame-pointer -fno-inline -fno-inline-functions
STATIC_DEBUG_LDFLAGS ?= -static

ifeq ($(STATIC_DEBUG),1)
CFLAGS += $(STATIC_DEBUG_CFLAGS)
LDFLAGS += $(STATIC_DEBUG_LDFLAGS)
endif

override CC := $(AME_CLANG_RESOLVED)
override LD := $(AME_CLANG_RESOLVED)

.PHONY: disasm-ame static-debug
disasm-ame: $(AME_OBJ)
	$(AME_OBJDUMP) -d $(AME_OBJ) --mattr=+matrix-xuantie-0.6 > $(AME_DISASM)
	@echo "generated $(AME_DISASM)"

static-debug:
	@$(MAKE) --no-print-directory STATIC_DEBUG=1 clean install
