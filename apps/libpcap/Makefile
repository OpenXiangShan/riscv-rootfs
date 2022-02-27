NAME = libpcap

include $(RISCV_ROOTFS_HOME)/Makefile.app

REPO_PATH = repo
TARBALL = libpcap-1.10.0.tar.gz
CONFIG_FLAGS = CC=riscv64-unknown-linux-gnu-gcc \
			   CXX=riscv64-unknown-linux-gnu-g++ \
			   --host=riscv64 \
			   --prefix=$(shell realpath build)

$(TARBALL):
	curl -O https://www.tcpdump.org/release/$(TARBALL)

$(REPO_PATH): $(TARBALL)
	tar xf $(TARBALL)
	rm -rf $@
	mv $(shell basename $(TARBALL) .tar.gz) $@

$(APP): | $(REPO_PATH)
	cd $(REPO_PATH) && ./configure $(CONFIG_FLAGS)
	$(MAKE) -C $(REPO_PATH)
	$(MAKE) -C $(REPO_PATH) install
