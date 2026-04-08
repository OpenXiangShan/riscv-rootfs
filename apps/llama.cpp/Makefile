NAME = llama-simple

THIS_MAKEFILE := $(abspath $(lastword $(MAKEFILE_LIST)))
APP_DIR := $(patsubst %/,%,$(dir $(THIS_MAKEFILE)))
XSAI_ENV_ROOT := $(abspath $(APP_DIR)/../../../..)
XSAI_RESOLVE_RISCV_ENV := $(XSAI_ENV_ROOT)/scripts/resolve-riscv-env.sh
# Memory layout (QEMU size, kernel RAM, XSAI DMA pool)
include $(XSAI_ENV_ROOT)/mk/memory.mk

XS_PROJECT_ROOT ?= $(XSAI_ENV_ROOT)
RISCV_ROOTFS_HOME ?= $(XS_PROJECT_ROOT)/firmware/riscv-rootfs
ROOTFS_BUILD_DIR ?= $(RISCV_ROOTFS_HOME)/rootfsimg/build
ROOTFS_INTERPRETER ?= /lib/ld-linux-riscv64-lp64d.so.1
RISCV ?= /opt/riscv
export PATH := $(RISCV)/bin:$(PATH)

REPO_PATH := $(APP_DIR)/repo
LLAMA_CPP_DEFAULT_HOME := $(XS_PROJECT_ROOT)/software/llama.cpp
ifneq ($(wildcard $(LLAMA_CPP_DEFAULT_HOME)/CMakeLists.txt),)
LLAMA_CPP_HOME ?= $(LLAMA_CPP_DEFAULT_HOME)
else
LLAMA_CPP_HOME ?= $(REPO_PATH)
endif

CMAKE ?= cmake
NPROC ?= $(shell nproc 2>/dev/null || getconf _NPROCESSORS_ONLN 2>/dev/null || echo 8)
HOST_CC ?= cc
HOST_CXX ?= c++
HOST_NO_CET_FLAG ?= -fcf-protection=none
HOST_CFLAGS ?=
HOST_CXXFLAGS ?=
HOST_EFFECTIVE_CFLAGS := $(strip $(HOST_CFLAGS) $(HOST_NO_CET_FLAG))
HOST_EFFECTIVE_CXXFLAGS := $(strip $(HOST_CXXFLAGS) $(HOST_NO_CET_FLAG))
QEMU_HOME ?= $(XS_PROJECT_ROOT)/qemu
QEMU_USER_CPU_FLAGS ?= rv64,v=true,vlen=128,h=true,zvfh=true,zvfhmin=true,x-matrix=true,rlen=512,mlen=65536,melen=32

HOST_BUILD_DIR := $(APP_DIR)/build-host
TARGET_BUILD_DIR := $(APP_DIR)/build-riscv
HOST_TOOLS_STAMP := $(HOST_BUILD_DIR)/.tools-ready
TARGET_TOOLS_STAMP := $(TARGET_BUILD_DIR)/.tools-built
HOST_CONVERT_BIN := $(HOST_BUILD_DIR)/bin/llama-convert-llama2c-to-ggml
HOST_QUANTIZE_BIN := $(HOST_BUILD_DIR)/bin/llama-quantize
TARGET_SIMPLE_BIN      := $(TARGET_BUILD_DIR)/bin/llama-simple
ROOTFS_SIMPLE_BIN      := $(ROOTFS_BUILD_DIR)/llama-simple
TARGET_SIMPLE_XSAI_BIN := $(TARGET_BUILD_DIR)/bin/llama-simple-xsai
ROOTFS_SIMPLE_XSAI_BIN := $(ROOTFS_BUILD_DIR)/llama-simple-xsai
TARGET_BENCH_BIN       := $(TARGET_BUILD_DIR)/bin/llama-bench
ROOTFS_BENCH_BIN       := $(ROOTFS_BUILD_DIR)/llama-bench
TARGET_BATCHED_BENCH_BIN := $(TARGET_BUILD_DIR)/bin/llama-batched-bench
ROOTFS_BATCHED_BENCH_BIN := $(ROOTFS_BUILD_DIR)/llama-batched-bench
ROOTFS_WRAPPER := $(ROOTFS_BUILD_DIR)/llama-xsai
ROOTFS_WRAPPER_SRC := $(APP_DIR)/llama-xsai.sh
ROOTFS_MODEL_NAME ?= llama-model.gguf
ROOTFS_MODEL_FILE := $(ROOTFS_BUILD_DIR)/$(ROOTFS_MODEL_NAME)

MODELS_DIR ?= $(APP_DIR)/models
MODEL_PRESET ?= stories15M
STORIES15M_URL ?= https://huggingface.co/karpathy/tinyllamas/resolve/main/stories15M.bin
STORIES110M_URL ?= https://huggingface.co/karpathy/tinyllamas/resolve/main/stories110M.bin
QWEN_CODER_URL ?= https://modelscope.cn/models/Qwen/Qwen2.5-Coder-0.5B-Instruct-GGUF/resolve/master/qwen2.5-coder-0.5b-instruct-q8_0.gguf

ifeq ($(MODEL_PRESET),stories15M)
MODEL_KIND ?= llama2c
MODEL_NAME ?= stories15M
MODEL_SOURCE_URL ?= $(STORIES15M_URL)
endif
ifeq ($(MODEL_PRESET),stories110M)
MODEL_KIND ?= llama2c
MODEL_NAME ?= stories110M
MODEL_SOURCE_URL ?= $(STORIES110M_URL)
endif
ifeq ($(MODEL_PRESET),qwen-coder-0.5b)
MODEL_KIND ?= gguf
MODEL_NAME ?= qwen-coder-0.5b
MODEL_SOURCE_PATH ?= $(MODELS_DIR)/qwen-coder-0.5b/qwen-coder-0.5b.gguf
MODEL_SOURCE_URL ?= $(QWEN_CODER_URL)
MODEL_QUANTIZE ?= 0
endif

MODEL_KIND ?= gguf
MODEL_NAME ?= custom-model
MODEL_SOURCE_URL ?=
MODEL_SOURCE_PATH ?=
QUANT_TYPE ?= q8_0
MODEL_QUANTIZE ?= 1
VOCAB_MODEL ?= $(LLAMA_CPP_HOME)/models/ggml-vocab-llama-spm.gguf

SUPPORTED_MODEL_KINDS := llama2c gguf
ifneq ($(filter $(MODEL_KIND),$(SUPPORTED_MODEL_KINDS)),$(MODEL_KIND))
$(error MODEL_KIND must be one of $(SUPPORTED_MODEL_KINDS))
endif

MODEL_DIR := $(MODELS_DIR)/$(MODEL_NAME)
MODEL_SOURCE_EXT := $(if $(filter llama2c,$(MODEL_KIND)),bin,gguf)
MODEL_SOURCE_BASENAME := $(strip $(if $(MODEL_SOURCE_PATH),$(notdir $(MODEL_SOURCE_PATH)),$(notdir $(MODEL_SOURCE_URL))))
MODEL_SOURCE_FILE := $(MODEL_DIR)/$(if $(MODEL_SOURCE_BASENAME),$(MODEL_SOURCE_BASENAME),$(MODEL_NAME).$(MODEL_SOURCE_EXT))
MODEL_GGUF := $(MODEL_DIR)/$(MODEL_NAME).gguf
MODEL_QUANTIZE_ENABLED := $(if $(filter 1 true TRUE yes YES,$(MODEL_QUANTIZE)),1,)
MODEL_FINAL_FILE := $(MODEL_DIR)/$(MODEL_NAME)-$(QUANT_TYPE).gguf
MODEL_READY_FILE := $(if $(MODEL_QUANTIZE_ENABLED),$(MODEL_FINAL_FILE),$(MODEL_GGUF))

RUN_MODEL ?= $(MODEL_READY_FILE)
RUN_PROMPT ?= Once
RUN_ARGS ?=

RISCV_TRIPLE ?= riscv64-unknown-linux-gnu
RISCV_MARCH ?= rv64gc_zba_zicbop
RISCV_MABI ?= lp64d
# cmake cross-compile sysroot: prefer the active env/toolchain sysroot and
# fall back only if nothing else is available.
LLAMA_RISCV_SYSROOT ?= $(strip $(or $(RISCV_SYSROOT),$(QEMU_LD_PREFIX),$(shell [ -x "$(XSAI_RESOLVE_RISCV_ENV)" ] && "$(XSAI_RESOLVE_RISCV_ENV)" sysroot 2>/dev/null || true),$(shell $(RISCV_TRIPLE)-gcc -print-sysroot 2>/dev/null),$(RISCV)/sysroot,/opt/riscv/sysroot))
RISCV_SYSROOT_RESOLVED := $(strip $(or $(RISCV_SYSROOT),$(QEMU_LD_PREFIX),$(shell [ -x "$(XSAI_RESOLVE_RISCV_ENV)" ] && "$(XSAI_RESOLVE_RISCV_ENV)" sysroot 2>/dev/null || true),$(shell $(RISCV_TRIPLE)-gcc -print-sysroot 2>/dev/null),$(RISCV)/sysroot))
ifeq ($(strip $(RISCV_SYSROOT)),)
RISCV_SYSROOT := $(RISCV_SYSROOT_RESOLVED)
endif

HOST_CMAKE_ARGS = \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_C_COMPILER=$(HOST_CC) \
	-DCMAKE_CXX_COMPILER=$(HOST_CXX) \
	-DCMAKE_C_FLAGS="$(HOST_EFFECTIVE_CFLAGS)" \
	-DCMAKE_CXX_FLAGS="$(HOST_EFFECTIVE_CXXFLAGS)" \
	-DGGML_CCACHE=OFF \
	-DGGML_OPENMP=OFF \
	-DLLAMA_CURL=OFF \
	-DBUILD_SHARED_LIBS=OFF \
	-DLLAMA_BUILD_TESTS=OFF \
	-DLLAMA_BUILD_SERVER=OFF \
	-DLLAMA_BUILD_TOOLS=ON \
	-DLLAMA_BUILD_EXAMPLES=ON

TARGET_CMAKE_ARGS = \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_TOOLCHAIN_FILE=$(LLAMA_CPP_HOME)/cmake/riscv64-toolchain.cmake \
	-DRISCV_ROOT_PATH=$(LLVM_HOME) \
	-DRISCV_TRIPLE=$(RISCV_TRIPLE) \
	-DRISCV_MARCH=$(RISCV_MARCH) \
	-DRISCV_MABI=$(RISCV_MABI) \
	-DRISCV_USE_LLVM=ON \
	-DGGML_CCACHE=OFF \
	-DGGML_OPENMP=OFF \
	-DLLAMA_CURL=OFF \
	-DLLAMA_OPENSSL=OFF \
	-DBUILD_SHARED_LIBS=OFF \
	-DLLAMA_BUILD_TESTS=OFF \
	-DLLAMA_BUILD_SERVER=OFF \
	-DLLAMA_BUILD_TOOLS=ON \
	-DLLAMA_BUILD_EXAMPLES=ON \
	-DGGML_RV_AME=ON \
	-DGGML_RV_ZFH=ON \
	-DGGML_RV_ZVFH=ON \
	-DGGML_RVV=ON \
	-DCMAKE_EXE_LINKER_FLAGS="$(ROOTFS_LINKER_FLAGS)" \
	-DRISCV_SYSROOT=$(LLAMA_RISCV_SYSROOT)

# Custom allocator: route llama.cpp tensor memory into the DMA-coherent
# reserved physical region (same region as XSAI_DIRECT_MAP_MEM_*).
# Override LLAMA_DIRECT_MAP_MEM_SIZE for a larger pool than the XSAI default.
# Defaults come from mk/memory.mk (included above).
LLAMA_DIRECT_MAP_MEM_START ?= $(XSAI_DIRECT_MAP_MEM_START)
LLAMA_DIRECT_MAP_MEM_SIZE  ?= $(XSAI_DIRECT_MAP_MEM_SIZE)

ifneq ($(LLAMA_DIRECT_MAP_MEM_START),)
TARGET_CMAKE_ARGS += \
	-DGGML_XSAI_ALLOC=ON \
	-DRESERVED_PHYS_BASE_ADDR=$(LLAMA_DIRECT_MAP_MEM_START)ul \
	-DRESERVED_MEMORY_SIZE=$(LLAMA_DIRECT_MAP_MEM_SIZE)ul
endif

.DEFAULT_GOAL := $(TARGET_SIMPLE_BIN)

.PHONY: repo source-ready host-tools riscv fetch-model convert-model quantize-model \
	prepare-model prepare-stories15m prepare-stories110M install install-model rootfs \
	run-user print-config clean distclean help

help:
	@echo "llama.cpp xsai wrapper"
	@echo "  make -C firmware/riscv-rootfs/apps/llama.cpp print-config"
	@echo "  make -C firmware/riscv-rootfs/apps/llama.cpp prepare-model"
	@echo "  make -C firmware/riscv-rootfs/apps/llama.cpp prepare-stories110M"
	@echo "  make -C firmware/riscv-rootfs/apps/llama.cpp MODEL_PRESET=custom MODEL_KIND=gguf MODEL_SOURCE_PATH=/path/to/model.gguf MODEL_QUANTIZE=0 install"
	@echo "  make firmware MODEL_PRESET=stories110M"

print-config:
	@echo "MODEL_PRESET=$(MODEL_PRESET)"
	@echo "MODEL_KIND=$(MODEL_KIND)"
	@echo "MODEL_NAME=$(MODEL_NAME)"
	@echo "MODEL_SOURCE_URL=$(MODEL_SOURCE_URL)"
	@echo "MODEL_SOURCE_PATH=$(MODEL_SOURCE_PATH)"
	@echo "MODEL_SOURCE_FILE=$(MODEL_SOURCE_FILE)"
	@echo "MODEL_GGUF=$(MODEL_GGUF)"
	@echo "MODEL_FINAL_FILE=$(MODEL_FINAL_FILE)"
	@echo "MODEL_READY_FILE=$(MODEL_READY_FILE)"
	@echo "ROOTFS_MODEL_FILE=$(ROOTFS_MODEL_FILE)"
	@echo "MODEL_QUANTIZE=$(MODEL_QUANTIZE)"
	@echo "QUANT_TYPE=$(QUANT_TYPE)"
	@echo "RISCV_SYSROOT=$(RISCV_SYSROOT)"
	@echo "LLAMA_RISCV_SYSROOT=$(LLAMA_RISCV_SYSROOT)"
	@echo "LLAMA_DIRECT_MAP_MEM_START=$(LLAMA_DIRECT_MAP_MEM_START)"
	@echo "LLAMA_DIRECT_MAP_MEM_SIZE=$(LLAMA_DIRECT_MAP_MEM_SIZE)"

repo: $(REPO_PATH)/CMakeLists.txt

source-ready: $(if $(filter $(REPO_PATH),$(LLAMA_CPP_HOME)),$(REPO_PATH)/CMakeLists.txt,)
	@if [ ! -f "$(LLAMA_CPP_HOME)/CMakeLists.txt" ]; then \
		echo "error: llama.cpp source not found at $(LLAMA_CPP_HOME)" >&2; \
		echo "hint: clone to $(LLAMA_CPP_DEFAULT_HOME) or run 'make repo' in this directory" >&2; \
		exit 1; \
	fi

$(REPO_PATH)/CMakeLists.txt:
	git clone --depth 1 https://github.com/OurCompArchGroup/llama.cpp.git $(REPO_PATH)

$(MODELS_DIR):
	mkdir -p $@

$(MODEL_DIR): | $(MODELS_DIR)
	mkdir -p $@

$(ROOTFS_BUILD_DIR):
	mkdir -p $@

.PHONY: host-configure target-configure host-tools

host-configure: | source-ready
	@if [ -f "$(HOST_BUILD_DIR)/CMakeCache.txt" ]; then \
		cached_c_flags=$$(grep '^CMAKE_C_FLAGS:STRING=' "$(HOST_BUILD_DIR)/CMakeCache.txt" | head -n1 | cut -d= -f2-); \
		cached_cxx_flags=$$(grep '^CMAKE_CXX_FLAGS:STRING=' "$(HOST_BUILD_DIR)/CMakeCache.txt" | head -n1 | cut -d= -f2-); \
		expected_c_flags='$(HOST_EFFECTIVE_CFLAGS)'; \
		expected_cxx_flags='$(HOST_EFFECTIVE_CXXFLAGS)'; \
		if grep -Eq 'CMAKE_(C|CXX)_COMPILER:FILEPATH=.*/riscv64-.*-(gcc|g\+\+)' "$(HOST_BUILD_DIR)/CMakeCache.txt" || \
		   [ "$$cached_c_flags" != "$$expected_c_flags" ] || \
		   [ "$$cached_cxx_flags" != "$$expected_cxx_flags" ]; then \
			echo "Reconfiguring llama.cpp host build with native compilers and host flags..."; \
			rm -rf "$(HOST_BUILD_DIR)"; \
		fi; \
	fi
	@if [ ! -f "$(HOST_BUILD_DIR)/Makefile" ]; then \
		$(CMAKE) -S $(LLAMA_CPP_HOME) -B $(HOST_BUILD_DIR) $(HOST_CMAKE_ARGS); \
	fi


$(HOST_CONVERT_BIN): $(THIS_MAKEFILE) $(LLAMA_CPP_HOME)/CMakeLists.txt | source-ready
	@$(MAKE) --no-print-directory host-configure
	@if [ ! -f "$(HOST_TOOLS_STAMP)" ] || \
	   [ "$(HOST_TOOLS_STAMP)" -ot "$(THIS_MAKEFILE)" ] || \
	   [ "$(HOST_TOOLS_STAMP)" -ot "$(LLAMA_CPP_HOME)/CMakeLists.txt" ] || \
	   [ ! -x "$(HOST_CONVERT_BIN)" ] || \
	   [ ! -x "$(HOST_QUANTIZE_BIN)" ]; then \
		$(CMAKE) --build $(HOST_BUILD_DIR) --target llama-convert-llama2c-to-ggml llama-quantize -j$(NPROC); \
		touch "$(HOST_TOOLS_STAMP)"; \
	fi
	@test -x "$@"

$(HOST_QUANTIZE_BIN): $(HOST_CONVERT_BIN)
	@test -x "$@"

host-tools: $(HOST_CONVERT_BIN) $(HOST_QUANTIZE_BIN)

$(TARGET_TOOLS_STAMP): target-configure
	@needs_build=0; \
	if [ ! -f "$@" ] || \
	   [ "$@" -ot "$(THIS_MAKEFILE)" ] || \
	   [ "$@" -ot "$(LLAMA_CPP_HOME)/CMakeLists.txt" ] || \
	   [ ! -x "$(TARGET_SIMPLE_BIN)" ] || \
	   [ ! -x "$(TARGET_SIMPLE_XSAI_BIN)" ] || \
	   [ ! -x "$(TARGET_BENCH_BIN)" ] || \
	   [ ! -x "$(TARGET_BATCHED_BENCH_BIN)" ]; then \
		needs_build=1; \
	elif find "$(LLAMA_CPP_HOME)/cmake" "$(LLAMA_CPP_HOME)/common" "$(LLAMA_CPP_HOME)/examples" "$(LLAMA_CPP_HOME)/ggml" "$(LLAMA_CPP_HOME)/include" "$(LLAMA_CPP_HOME)/src" "$(LLAMA_CPP_HOME)/tools" \
		-type f \( -name 'CMakeLists.txt' -o -name '*.cmake' -o -name '*.c' -o -name '*.cc' -o -name '*.cpp' -o -name '*.h' -o -name '*.hpp' \) \
		-newer "$@" -print -quit 2>/dev/null | grep -q .; then \
		needs_build=1; \
	fi; \
	if [ $$needs_build -eq 1 ]; then \
		$(CMAKE) --build $(TARGET_BUILD_DIR) --target llama-simple llama-simple-xsai llama-bench llama-batched-bench -j$(NPROC); \
		touch $@; \
	fi

target-configure: | source-ready
	@if [ -z "$(LLVM_HOME)" ]; then \
		echo "error: LLVM_HOME is not set" >&2; \
		exit 1; \
	fi
	@if [ ! -x "$(LLVM_HOME)/bin/clang" ]; then \
		echo "error: clang not found at $(LLVM_HOME)/bin/clang" >&2; \
		exit 1; \
	fi
	@if [ -f "$(TARGET_BUILD_DIR)/CMakeCache.txt" ] && [ ! -f "$(TARGET_BUILD_DIR)/Makefile" ]; then \
		echo "Reconfiguring incomplete llama.cpp RISC-V build directory..."; \
		rm -rf "$(TARGET_BUILD_DIR)"; \
	fi
	@if [ -f "$(TARGET_BUILD_DIR)/CMakeCache.txt" ]; then \
		cached_sysroot=$$(grep '^RISCV_SYSROOT:PATH=' "$(TARGET_BUILD_DIR)/CMakeCache.txt" | head -n1 | cut -d= -f2-); \
		cached_phys_base=$$(grep '^RESERVED_PHYS_BASE_ADDR:' "$(TARGET_BUILD_DIR)/CMakeCache.txt" | head -n1 | cut -d= -f2-); \
		cached_mem_size=$$(grep '^RESERVED_MEMORY_SIZE:' "$(TARGET_BUILD_DIR)/CMakeCache.txt" | head -n1 | cut -d= -f2-); \
		cached_build_tools=$$(grep '^LLAMA_BUILD_TOOLS:BOOL=' "$(TARGET_BUILD_DIR)/CMakeCache.txt" | head -n1 | cut -d= -f2-); \
		cached_openssl=$$(grep '^LLAMA_OPENSSL:BOOL=' "$(TARGET_BUILD_DIR)/CMakeCache.txt" | head -n1 | cut -d= -f2-); \
		expected_phys_base='$(LLAMA_DIRECT_MAP_MEM_START)ul'; \
		expected_mem_size='$(LLAMA_DIRECT_MAP_MEM_SIZE)ul'; \
		expected_build_tools='ON'; \
		expected_openssl='OFF'; \
		if [ "$$cached_sysroot" != "$(LLAMA_RISCV_SYSROOT)" ] || \
		   [ "$$cached_phys_base" != "$$expected_phys_base" ] || \
		   [ "$$cached_mem_size" != "$$expected_mem_size" ] || \
		   [ "$$cached_build_tools" != "$$expected_build_tools" ] || \
		   [ "$$cached_openssl" != "$$expected_openssl" ]; then \
			echo "Reconfiguring llama.cpp RISC-V build due to cache mismatch..."; \
			rm -rf "$(TARGET_BUILD_DIR)"; \
		fi; \
	fi
	@if [ ! -f "$(TARGET_BUILD_DIR)/Makefile" ]; then \
		$(CMAKE) -S $(LLAMA_CPP_HOME) -B $(TARGET_BUILD_DIR) $(TARGET_CMAKE_ARGS); \
	fi

$(TARGET_SIMPLE_BIN) $(TARGET_SIMPLE_XSAI_BIN) $(TARGET_BENCH_BIN) $(TARGET_BATCHED_BENCH_BIN): $(TARGET_TOOLS_STAMP)
	@test -x "$@"

riscv: $(TARGET_SIMPLE_BIN) $(TARGET_SIMPLE_XSAI_BIN) $(TARGET_BENCH_BIN) $(TARGET_BATCHED_BENCH_BIN)

$(MODEL_SOURCE_FILE): | $(MODEL_DIR)
	@if [ -n "$(MODEL_SOURCE_URL)" ]; then \
		if command -v curl >/dev/null 2>&1; then \
			curl -L --fail -o "$@" "$(MODEL_SOURCE_URL)"; \
		elif command -v wget >/dev/null 2>&1; then \
			wget -O "$@" "$(MODEL_SOURCE_URL)"; \
		else \
			echo "error: neither curl nor wget is available" >&2; \
			exit 1; \
		fi; \
	elif [ -n "$(MODEL_SOURCE_PATH)" ]; then \
		src="$(abspath $(MODEL_SOURCE_PATH))"; \
		dst="$(abspath $@)"; \
		if [ ! -f "$$src" ]; then \
			echo "error: model source path not found: $$src" >&2; \
			exit 1; \
		fi; \
		if [ "$$src" != "$$dst" ] && { [ ! -f "$@" ] || ! cmp -s "$$src" "$@"; }; then \
			cp -Lf "$$src" "$@"; \
		fi; \
	else \
		echo "error: set MODEL_SOURCE_URL or MODEL_SOURCE_PATH" >&2; \
		exit 1; \
	fi

ifeq ($(MODEL_KIND),llama2c)
$(MODEL_GGUF): $(MODEL_SOURCE_FILE) $(HOST_CONVERT_BIN)
	@if [ ! -f "$(VOCAB_MODEL)" ]; then \
		echo "error: vocab model not found at $(VOCAB_MODEL)" >&2; \
		exit 1; \
	fi
	@if [ ! -f "$@" ] || [ "$@" -ot "$(MODEL_SOURCE_FILE)" ] || [ "$@" -ot "$(VOCAB_MODEL)" ] || [ "$@" -ot "$(HOST_CONVERT_BIN)" ]; then \
		$(HOST_CONVERT_BIN) \
			--copy-vocab-from-model $(VOCAB_MODEL) \
			--llama2c-model $(MODEL_SOURCE_FILE) \
			--llama2c-output-model $(MODEL_GGUF); \
	fi
else
$(MODEL_GGUF): $(MODEL_SOURCE_FILE)
	@if [ "$(abspath $(MODEL_SOURCE_FILE))" != "$(abspath $(MODEL_GGUF))" ] && { [ ! -f "$@" ] || ! cmp -s "$(MODEL_SOURCE_FILE)" "$@"; }; then \
		cp -Lf $(MODEL_SOURCE_FILE) $(MODEL_GGUF); \
	fi
endif

ifeq ($(MODEL_QUANTIZE_ENABLED),1)
$(MODEL_FINAL_FILE): $(MODEL_GGUF) $(HOST_QUANTIZE_BIN)
	@if [ ! -f "$@" ] || [ "$@" -ot "$(MODEL_GGUF)" ] || [ "$@" -ot "$(HOST_QUANTIZE_BIN)" ]; then \
		$(HOST_QUANTIZE_BIN) $(MODEL_GGUF) $(MODEL_FINAL_FILE) $(QUANT_TYPE); \
	fi
endif

fetch-model: $(MODEL_SOURCE_FILE)
convert-model: $(MODEL_GGUF)
quantize-model: $(MODEL_FINAL_FILE)
prepare-model: $(MODEL_READY_FILE)

prepare-stories15m: MODEL_PRESET = stories15M
prepare-stories15m: prepare-model

prepare-stories110M: MODEL_PRESET = stories110M
prepare-stories110M: prepare-model

define install_rootfs_bin
@mkdir -p $(ROOTFS_BUILD_DIR)
@if [ ! -f "$(2)" ] || ! cmp -s "$(1)" "$(2)"; then \
	cp -Lf $(1) $(2); \
fi
@interp=$$(readelf -l "$(2)" 2>/dev/null | sed -n 's/.*Requesting program interpreter: \(.*\)]/\1/p'); \
if [ -n "$$interp" ] && [ "$$interp" != "$(ROOTFS_INTERPRETER)" ]; then \
	if ! command -v patchelf >/dev/null 2>&1; then \
		echo "error: patchelf is required to rewrite interpreter $$interp -> $(ROOTFS_INTERPRETER)" >&2; \
		echo "hint: prefer building with ROOTFS_LINKER_FLAGS='$(ROOTFS_LINKER_FLAGS)' so patching is unnecessary" >&2; \
		exit 1; \
	fi; \
	patchelf --set-interpreter $(ROOTFS_INTERPRETER) --set-rpath "$(ROOTFS_RPATH)" "$(2)"; \
fi
endef

$(ROOTFS_SIMPLE_BIN): $(TARGET_SIMPLE_BIN)
	$(call install_rootfs_bin,$(TARGET_SIMPLE_BIN),$(ROOTFS_SIMPLE_BIN))

$(ROOTFS_SIMPLE_XSAI_BIN): $(TARGET_SIMPLE_XSAI_BIN)
	$(call install_rootfs_bin,$(TARGET_SIMPLE_XSAI_BIN),$(ROOTFS_SIMPLE_XSAI_BIN))

$(ROOTFS_BENCH_BIN): $(TARGET_BENCH_BIN)
	$(call install_rootfs_bin,$(TARGET_BENCH_BIN),$(ROOTFS_BENCH_BIN))

$(ROOTFS_BATCHED_BENCH_BIN): $(TARGET_BATCHED_BENCH_BIN)
	$(call install_rootfs_bin,$(TARGET_BATCHED_BENCH_BIN),$(ROOTFS_BATCHED_BENCH_BIN))

$(ROOTFS_WRAPPER): $(ROOTFS_WRAPPER_SRC)
	@mkdir -p $(ROOTFS_BUILD_DIR)
	install -m 755 $(ROOTFS_WRAPPER_SRC) $@

$(ROOTFS_MODEL_FILE): $(MODEL_READY_FILE) | $(ROOTFS_BUILD_DIR)
	@if [ ! -f "$@" ] || ! cmp -s "$(MODEL_READY_FILE)" "$@"; then \
		install -m 644 $(MODEL_READY_FILE) $(ROOTFS_MODEL_FILE); \
	fi

install-model: $(ROOTFS_MODEL_FILE)

install: $(ROOTFS_SIMPLE_BIN) $(ROOTFS_SIMPLE_XSAI_BIN) $(ROOTFS_BENCH_BIN) $(ROOTFS_BATCHED_BENCH_BIN) $(ROOTFS_WRAPPER) install-model

rootfs: install

run-user: $(TARGET_SIMPLE_BIN) $(MODEL_READY_FILE)
	@if [ ! -x "$(QEMU_HOME)/build/qemu-riscv64" ]; then \
		echo "error: qemu-riscv64 not found at $(QEMU_HOME)/build/qemu-riscv64" >&2; \
		exit 1; \
	fi
	@if [ ! -f "$(RUN_MODEL)" ]; then \
		echo "error: model not found at $(RUN_MODEL)" >&2; \
		exit 1; \
	fi
	@if [ -z "$(RISCV_SYSROOT)" ]; then \
		echo "error: RISCV_SYSROOT is empty; ensure riscv64-unknown-linux-gnu-gcc -print-sysroot works" >&2; \
		exit 1; \
	fi
	$(QEMU_HOME)/build/qemu-riscv64 -cpu $(QEMU_USER_CPU_FLAGS) -L $(RISCV_SYSROOT) $(TARGET_SIMPLE_BIN) -m $(RUN_MODEL) "$(RUN_PROMPT)" $(RUN_ARGS)

clean:
	rm -rf $(HOST_BUILD_DIR) $(TARGET_BUILD_DIR)
	rm -f $(ROOTFS_SIMPLE_BIN) $(ROOTFS_SIMPLE_XSAI_BIN) $(ROOTFS_BENCH_BIN) $(ROOTFS_BATCHED_BENCH_BIN) $(ROOTFS_WRAPPER) $(ROOTFS_MODEL_FILE)

distclean: clean
	rm -rf $(MODELS_DIR)
	rm -rf $(REPO_PATH)
