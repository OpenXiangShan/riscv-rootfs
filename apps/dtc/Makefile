NAME = dtc

include $(RISCV_ROOTFS_HOME)/Makefile.app

ARCH ?= riscv
CROSS_COMPILE ?= riscv64-unknown-linux-gnu-
CC := $(CROSS_COMPILE)gcc -mabi=lp64d -march=rv64gc
TRIPLET := $(shell $(CC) -dumpmachine)

REPO_PATH = repo
$(REPO_PATH):
	git clone --depth 1 -b v1.7.2 https://git.kernel.org/pub/scm/utils/dtc/dtc.git $@

$(APP): | $(REPO_PATH)
	$(MAKE) -C $(REPO_PATH) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) CC="$(CC)" NO_PYTHON=1 NO_YAML=1 DESTDIR=$(APP) PREFIX=/usr LIBDIR=/usr/lib64/lp64d  install-lib install-includes

clean-repo:
	$(MAKE) -C $(REPO_PATH) clean
