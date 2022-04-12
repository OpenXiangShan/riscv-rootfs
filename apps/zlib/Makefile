NAME = zlib

include $(RISCV_ROOTFS_HOME)/Makefile.app

REPO_PATH = repo
TARBALL = zlib-1.2.12.tar.gz
CONFIG_FLAGS = --prefix=$(shell realpath build)

$(TARBALL):
	curl -O https://www.zlib.net/$(TARBALL)

$(REPO_PATH): $(TARBALL)
	tar xf $(TARBALL)
	rm -rf $@
	mv $(shell basename $(TARBALL) .tar.gz) $@

$(APP): | $(REPO_PATH)
	cd $(REPO_PATH) && CHOST=riscv64-unknown-linux-gnu ./configure $(CONFIG_FLAGS)
	$(MAKE) -C $(REPO_PATH)
	$(MAKE) -C $(REPO_PATH) install
	cd build && ln -sf lib/libz.so.1 zlib
