NAME = redis-server

include $(RISCV_ROOTFS_HOME)/Makefile.app

REPO_PATH = repo
$(REPO_PATH):
	mkdir -p $@
	git clone -b 6.2.6 --depth 1 git@github.com:redis/redis.git $@
	cd $@ && git apply ../riscv-cross-compile.patch

$(APP): | $(REPO_PATH)
	$(MAKE) -C $(REPO_PATH)
	ln -sf $(abspath $(REPO_PATH)/src/$(NAME)) $@
	riscv64-unknown-linux-gnu-strip $(abspath $(REPO_PATH)/src/$(NAME))
