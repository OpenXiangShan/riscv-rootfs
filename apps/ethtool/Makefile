NAME = ethtool

include $(RISCV_ROOTFS_HOME)/Makefile.app

REPO_PATH = repo
TARBALL = ethtool-5.19.tar.gz

CONFIG_FLAGS = CC=riscv64-unknown-linux-gnu-gcc \
			   CXX=riscv64-unknown-linux-gnu-g++ \
			   --host=riscv64 \
			   --prefix=$(shell realpath build)

$(REPO_PATH):
	mkdir -p build
	curl -O https://mirrors.edge.kernel.org/pub/software/network/ethtool/$(TARBALL)
	tar xf $(TARBALL)
	mv $(shell basename $(TARBALL) .tar.gz) repo
	cd $(REPO_PATH) && ./configure $(CONFIG_FLAGS)


$(APP): | $(REPO_PATH)
	$(MAKE) -C $(REPO_PATH)
	$(MAKE) -C $(REPO_PATH) install
	cd build && ln -sf sbin/ethtool ethtool
