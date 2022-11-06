NAME = tcpdump

include $(RISCV_ROOTFS_HOME)/Makefile.app

REPO_PATH = repo
TARBALL = tcpdump-4.99.0.tar.gz
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
	make -s -C ../libpcap install
	-ln -sf ../libpcap/repo libpcap
	cd $(REPO_PATH) && ./configure $(CONFIG_FLAGS)
	$(MAKE) -C $(REPO_PATH)
	-ln -sf $(abspath build/bin/tcpdump) $(APP)
	$(MAKE) -C $(REPO_PATH) install
