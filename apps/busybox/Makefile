NAME = busybox

include $(RISCV_ROOTFS_HOME)/Makefile.app

REPO_PATH = repo
$(REPO_PATH):
	mkdir -p $@
	git clone --depth 1 -b 1_32_stable https://github.com/mirror/busybox.git $@
	cp config $@/.config

$(APP): | $(REPO_PATH)
	$(MAKE) -C $(REPO_PATH)
	ln -sf $(abspath $(REPO_PATH)/busybox) $@
