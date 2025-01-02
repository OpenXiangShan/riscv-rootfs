NAME = CPU2006LiteWrapper

include $(RISCV_ROOTFS_HOME)/Makefile.app

REPO_PATH = repo
$(REPO_PATH):
	git clone --depth 1 https://github.com/OpenXiangShan/CPU2006LiteWrapper.git $@

$(APP): $(REPO_PATH)
	@echo "Please build CPU2006LiteWrapper manually"
