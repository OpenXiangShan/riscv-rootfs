NAME = lkvm-static

include $(RISCV_ROOTFS_HOME)/Makefile.app

LIBFDT_INSTALL_ROOT=$(RISCV_ROOTFS_HOME)/apps/dtc/build/dtc/usr
LIBFDT_INCLUDE_DIR=$(LIBFDT_INSTALL_ROOT)/include
LIBFDT_INCLUDE=$(LIBFDT_INCLUDE_DIR)/libfdt.h
LIBFDT_ARCHIVE=$(LIBFDT_INSTALL_ROOT)/lib64/lp64d/libfdt.a
LIBFDT_DIR=$(APP_DIR)/build/libfdt
LIBFDT=$(LIBFDT_DIR)/libfdt.a
LIBFDT_HEADERS=$(LIBFDT_DIR)/libfdt.h $(LIBFDT_DIR)/libfdt_env.h $(LIBFDT_DIR)/fdt.h

.PHONY: check-libfdt
check-libfdt:
	@if [ ! -f "$(LIBFDT_ARCHIVE)" ] || [ ! -f "$(LIBFDT_INCLUDE)" ]; then \
		echo "Error: libfdt is missing. Please build apps/dtc first."; \
		exit 1; \
	fi

$(LIBFDT): check-libfdt
	@mkdir -p $(LIBFDT_DIR)
	@cp $(LIBFDT_ARCHIVE) $(LIBFDT)
	@cp $(LIBFDT_INCLUDE_DIR)/libfdt.h $(LIBFDT_DIR)/libfdt.h
	@cp $(LIBFDT_INCLUDE_DIR)/libfdt_env.h $(LIBFDT_DIR)/libfdt_env.h
	@cp $(LIBFDT_INCLUDE_DIR)/fdt.h $(LIBFDT_DIR)/fdt.h

REPO_PATH = repo
$(REPO_PATH):
	git clone --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/will/kvmtool.git $@


$(APP): $(LIBFDT) | $(REPO_PATH)
	$(MAKE) LIBFDT_DIR=$(LIBFDT_DIR) -C $(REPO_PATH) lkvm-static
	$(CROSS_COMPILE)strip $(REPO_PATH)/lkvm-static
	ln -sf $(abspath $(REPO_PATH)/lkvm-static) $@

clean-repo:
	$(MAKE) -C $(REPO_PATH) clean
