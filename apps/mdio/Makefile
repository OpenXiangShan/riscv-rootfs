NAME = mdio

include $(RISCV_ROOTFS_HOME)/Makefile.app

REPO_PATH = repo

$(REPO_PATH):
	mkdir -p build
	git clone https://github.com/PieVo/mdio-tool.git repo

$(APP): | $(REPO_PATH)
	riscv64-unknown-linux-gnu-gcc -I repo $(wildcard repo/*.c) -o $@
