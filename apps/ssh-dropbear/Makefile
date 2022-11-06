NAME = ssh-dropbear

include $(RISCV_ROOTFS_HOME)/Makefile.app

REPO_PATH = repo
TARBALL = dropbear-2019.78.tar.bz2
CONFIG_FLAGS = CC=riscv64-unknown-linux-gnu-gcc \
			   CXX=riscv64-unknown-linux-gnu-g++ \
			   --host=riscv64 \
			   --with-zlib=$(RISCV_ROOTFS_HOME)/apps/zlib/build \
			   --prefix=$(shell realpath build)

$(TARBALL):
	curl -O https://matt.ucc.asn.au/dropbear/releases/$(TARBALL)

$(REPO_PATH): $(TARBALL)
	tar xf $(TARBALL)
	rm -rf $@
	mv $(shell basename $(TARBALL) .tar.bz2) $@

$(APP): | $(REPO_PATH)
	make -s -C ../zlib install
	cd $(REPO_PATH) && ./configure $(CONFIG_FLAGS)
	$(MAKE) -C $(REPO_PATH)
	$(MAKE) -C $(REPO_PATH) install
	cd build && ln -sf sbin/dropbear ssh-dropbear
	ln -sf $(abspath build/bin/dbclient) ${RISCV_ROOTFS_HOME}/rootfsimg/build/
	ln -sf $(abspath build/bin/dropbearkey) ${RISCV_ROOTFS_HOME}/rootfsimg/build/
