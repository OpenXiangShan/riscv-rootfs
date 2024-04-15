NAME = zlib

include $(RISCV_ROOTFS_HOME)/Makefile.app

REPO_PATH = repo
TARBALL = zlib-1.3.1.tar.gz
CONFIG_FLAGS = --prefix=$(shell realpath build)

$(TARBALL):
	curl -O https://www.zlib.net/$(TARBALL)

$(REPO_PATH): $(TARBALL)
	if [ !`tar xf $(TARBALL)` ]; then echo "\033[1;31mUpdate zlib version in apps/zlib/Makefile\033[0m"; fi
	rm -rf $@
	mv $(shell basename $(TARBALL) .tar.gz) $@

$(APP): | $(REPO_PATH)
	cd $(REPO_PATH) && CHOST=riscv64-unknown-linux-gnu ./configure $(CONFIG_FLAGS)
	$(MAKE) -C $(REPO_PATH)
	$(MAKE) -C $(REPO_PATH) install
	cd build && ln -sf lib/libz.so.1 zlib
