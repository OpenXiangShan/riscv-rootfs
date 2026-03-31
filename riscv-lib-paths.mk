XSAI_RESOLVE_RISCV_ENV ?= $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/../../scripts/resolve-riscv-env.sh)
RISCV_SYSROOT_RESOLVED := $(strip $(or $(RISCV_SYSROOT),$(QEMU_LD_PREFIX),$(shell [ -x "$(XSAI_RESOLVE_RISCV_ENV)" ] && "$(XSAI_RESOLVE_RISCV_ENV)" sysroot 2>/dev/null || true),$(RISCV)/sysroot))
ifeq ($(strip $(RISCV_SYSROOT)),)
RISCV_SYSROOT := $(RISCV_SYSROOT_RESOLVED)
endif
RISCV_FALLBACK_LIB_DIRS := \
	$(if $(RISCV_SYSROOT),$(RISCV_SYSROOT)/lib) \
	$(if $(RISCV_SYSROOT),$(RISCV_SYSROOT)/usr/lib) \
	$(if $(RISCV_SYSROOT),$(RISCV_SYSROOT)/lib64) \
	$(if $(RISCV_SYSROOT),$(RISCV_SYSROOT)/usr/lib64) \
	$(if $(QEMU_LD_PREFIX),$(QEMU_LD_PREFIX)/lib) \
	$(if $(QEMU_LD_PREFIX),$(QEMU_LD_PREFIX)/usr/lib) \
	$(RISCV)/sysroot/lib \
	$(RISCV)/sysroot/usr/lib

gcc_print_file = $(strip $(shell $(CROSS_COMPILE)gcc -print-file-name=$(1) 2>/dev/null))
resolve_riscv_lib = $(strip $(if $(filter /%,$(call gcc_print_file,$(1))),$(call gcc_print_file,$(1)),$(firstword $(wildcard $(addsuffix /$(1),$(RISCV_FALLBACK_LIB_DIRS))))))

export RISCV_LD_SO := $(call resolve_riscv_lib,ld-linux-riscv64-lp64d.so.1)
export RISCV_LIBC_SO := $(call resolve_riscv_lib,libc.so.6)
export RISCV_LIBRESOLV_SO := $(call resolve_riscv_lib,libresolv.so.2)
export RISCV_LIBM_SO := $(call resolve_riscv_lib,libm.so.6)
export RISCV_LIBDL_SO := $(call resolve_riscv_lib,libdl.so.2)
export RISCV_LIBPTHREAD_SO := $(call resolve_riscv_lib,libpthread.so.0)
export RISCV_LIBCRYPT_SO := $(call resolve_riscv_lib,libcrypt.so.1)
export RISCV_LIBNSS_FILES_SO := $(call resolve_riscv_lib,libnss_files.so.2)
export RISCV_LIBUTIL_SO := $(call resolve_riscv_lib,libutil.so.1)
export RISCV_LIBRT_SO := $(call resolve_riscv_lib,librt.so.1)
export RISCV_LIBATOMIC_SO := $(call resolve_riscv_lib,libatomic.so.1)
