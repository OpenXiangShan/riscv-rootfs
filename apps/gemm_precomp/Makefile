# gemm_precomp — AME GEMM test using precomputed golden data (no runtime reference)
#
# Shares source files from hello_xsai (ggml kernel, mem allocator, ame.h).
# Regenerate test_data.h:
#   python3 gen_test_data.py [--num-rand N] [--seed S]

NAME = gemm_precomp

HELLO_XSAI_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))../hello_xsai

SRCS  = main.c
SRCS += precomp_test.c
SRCS += $(HELLO_XSAI_DIR)/ggml_ame_gemm_tile_i8_i32_bT.c
SRCS += $(HELLO_XSAI_DIR)/mem.c

STATIC_DEBUG ?= 1

THIS_MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

ifeq ($(strip $(LLVM_HOME)),)
$(error LLVM_HOME is not set. Please export LLVM_HOME and use the full-path toolchain)
endif

AME_LLVM_BIN  := $(LLVM_HOME)/bin
AME_CLANG     := $(AME_LLVM_BIN)/clang
AME_OBJDUMP   := $(AME_LLVM_BIN)/llvm-objdump

ifeq ($(wildcard $(AME_CLANG)),)
$(error clang not found at $(AME_CLANG))
endif

AME_TARGET  = -target riscv64-unknown-linux-gnu
AME_ARCH    = -march=rv64g_v_zvfh_zame_zvl128b_zicbop_zihintpause
AME_FEATURE = -Xclang -target-feature -Xclang +matrix-xuantie-0.6

RESERVED_PHYS_BASE_ADDR ?= 0x100000000UL
RESERVED_MEMORY_SIZE    ?= 0x180000000UL

CFLAGS  += $(AME_TARGET) $(AME_ARCH) $(AME_FEATURE)
CFLAGS  += -DRESERVED_PHYS_BASE_ADDR=$(RESERVED_PHYS_BASE_ADDR)
CFLAGS  += -DRESERVED_MEMORY_SIZE=$(RESERVED_MEMORY_SIZE)
# Include dirs: this app dir (for test_data.h) + hello_xsai dir (for ame.h, mem.h)
CFLAGS  += -I$(THIS_MAKEFILE_DIR) -I$(HELLO_XSAI_DIR)
LDFLAGS += $(AME_TARGET) $(AME_ARCH) $(AME_FEATURE)

STATIC_DEBUG_CFLAGS  ?= -O0 -g3 -fno-omit-frame-pointer -fno-inline -fno-inline-functions
STATIC_DEBUG_LDFLAGS ?= -static

ifeq ($(STATIC_DEBUG),1)
CFLAGS  += $(STATIC_DEBUG_CFLAGS)
LDFLAGS += $(STATIC_DEBUG_LDFLAGS)
endif

override CC := $(AME_CLANG)
override LD := $(AME_CLANG)

include $(RISCV_ROOTFS_HOME)/Makefile.compile

# Regenerate test_data.h
.PHONY: gen
gen:
	python3 $(THIS_MAKEFILE_DIR)/gen_test_data.py

.PHONY: static-debug
static-debug:
	@$(MAKE) --no-print-directory STATIC_DEBUG=1 clean install
