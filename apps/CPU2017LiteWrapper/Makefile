NAME = CPU2017LiteWrapper

include $(RISCV_ROOTFS_HOME)/Makefile.app

REPO_PATH = repo
$(REPO_PATH):
	git clone --depth 1 https://github.com/OpenXiangShan/CPU2017LiteWrapper.git $@

$(APP): $(REPO_PATH)
	@echo "Please build CPU2017LiteWrapper manually"
