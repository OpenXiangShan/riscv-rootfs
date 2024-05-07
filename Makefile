$(shell mkdir -p rootfsimg/build)

APPS = hello busybox before_workload trap qemu_trap
APPS_DIR = $(addprefix apps/, $(APPS))

.PHONY: rootfsimg $(APPS_DIR) clean

rootfsimg: $(APPS_DIR)

$(APPS_DIR): %:
	-$(MAKE) -s -C $@ install

clean:
	-$(foreach app, $(APPS_DIR), $(MAKE) -s -C $(app) clean ;)
	-rm -f rootfsimg/build/*
	-rm -rf apps/busybox/repo
