NAME = lkvm-static

include $(RISCV_ROOTFS_HOME)/Makefile.app

LIBFDT_DIR=$(RISCV_ROOTFS_HOME)/apps/dtc/build/dtc/usr/lib64/lp64d
LIBFDT=$(LIBFDT_DIR)/libfdt.a

.PHONY: check-libfdt
check-libfdt:
	@if [ ! -f "$(LIBFDT)" ]; then \
		echo "Error: Dependency file '$(LIBFDT)' is missing. Please build it first."; \
		exit 1; \
	fi

REPO_PATH = repo
$(REPO_PATH):
	git clone --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/will/kvmtool.git $@

$(APP): check-libfdt | $(REPO_PATH)
	$(MAKE) LIBFDT_DIR=$(LIBFDT_DIR) -C $(REPO_PATH) lkvm-static
	$(CROSS_COMPILE)strip $(REPO_PATH)/lkvm-static
	ln -sf $(abspath $(REPO_PATH)/lkvm-static) $@

clean-repo:
	$(MAKE) -C $(REPO_PATH) clean
