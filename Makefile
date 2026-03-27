$(shell mkdir -p rootfsimg/build)

APPS = hello_xsai after_workload gemm_precomp busybox before_workload llama.cpp
# trap qemu_trap dtc lkvm-static

APPS_DIR = $(addprefix apps/, $(APPS))

.PHONY: rootfsimg $(APPS_DIR) clean

rootfsimg: $(APPS_DIR)

$(APPS_DIR): %:
	$(MAKE) -s -C $@ install

clean:
	-$(foreach app, $(APPS_DIR), $(MAKE) -s -C $(app) clean ;)
	-rm -f rootfsimg/build/*

distclean:
	-$(foreach app, $(APPS_DIR), $(MAKE) -s -C $(app) distclean ;)
	-rm -f rootfsimg/build/*
	-rm -rf apps/busybox/repo
	-rm -rf apps/llama.cpp/repo
