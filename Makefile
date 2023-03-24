$(shell mkdir -p rootfsimg/build)

APPS = mdio ethtool hello stream busybox redis dwarf/md5 dwarf/sort dwarf/wordcount zlib stream ssh-dropbear tcpdump new_before_workload notip_before_workload after_workload
APPS_DIR = $(addprefix apps/, $(APPS))

.PHONY: rootfsimg $(APPS_DIR) clean

rootfsimg: $(APPS_DIR)

$(APPS_DIR): %:
	-$(MAKE) -s -C $@ install

clean:
	-$(foreach app, $(APPS_DIR), $(MAKE) -s -C $(app) clean ;)
	-rm -f rootfsimg/build/*
