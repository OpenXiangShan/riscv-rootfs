$(shell mkdir -p rootfsimg/build)

APPS = hello stream busybox redis dwarf/md5 dwarf/sort dwarf/wordcount new_before_workload
APPS_DIR = $(addprefix apps/, $(APPS))

.PHONY: rootfsimg $(APPS_DIR) clean

rootfsimg: $(APPS_DIR)

$(APPS_DIR): %:
	-$(MAKE) -s -C $@ install

clean:
	-$(foreach app, $(APPS_DIR), $(MAKE) -s -C $(app) clean ;)
	-rm -f rootfsimg/build/*
