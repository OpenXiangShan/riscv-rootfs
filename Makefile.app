ifeq ($(RISCV_ROOTFS_HOME),)
	$(error RISCV_ROOTFS_HOME is not defined)
endif

ifeq (run, $(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

APP_DIR ?= $(shell pwd)
INC_DIR += $(APP_DIR)/include/
DST_DIR ?= $(APP_DIR)/build/
APP ?= $(APP_DIR)/build/$(NAME)
ROOTFS_BUILD_DIR ?= $(RISCV_ROOTFS_HOME)/rootfsimg/build
ROOTFS_INTERPRETER ?= /lib/ld-linux-riscv64-lp64d.so.1
ROOTFS_RPATH ?= /lib
ROOTFS_LINKER_FLAGS ?= -Wl,--dynamic-linker=$(ROOTFS_INTERPRETER) -Wl,-rpath,$(ROOTFS_RPATH)
ROOTFS_LINK_FLAGS_STAMP ?= $(APP_DIR)/.rootfs-link-flags

.DEFAULT_GOAL = $(APP)

$(shell mkdir -p $(DST_DIR) $(ROOTFS_BUILD_DIR))

.PHONY: install clean

$(ROOTFS_LINK_FLAGS_STAMP):
	@tmp="$@.tmp"; \
	printf '%s\n' '$(ROOTFS_LINKER_FLAGS)' > "$$tmp"; \
	if [ ! -f "$@" ] || ! cmp -s "$$tmp" "$@"; then \
		mv "$$tmp" "$@"; \
	else \
		rm -f "$$tmp"; \
	fi

install: $(APP)
	@target="$(ROOTFS_BUILD_DIR)/$(NAME)"; \
	rm -rf "$$target"; \
	if [ -f "$(APP)" ]; then \
		cp -Lf "$(APP)" "$$target"; \
		interp=$$(readelf -l "$$target" 2>/dev/null | sed -n 's/.*Requesting program interpreter: \(.*\)]/\1/p'); \
		if [ -n "$$interp" ] && [ "$$interp" != "$(ROOTFS_INTERPRETER)" ]; then \
			if ! command -v patchelf >/dev/null 2>&1; then \
				echo "error: patchelf is required to rewrite interpreter $$interp -> $(ROOTFS_INTERPRETER)" >&2; \
				echo "hint: prefer building with ROOTFS_LINKER_FLAGS='$(ROOTFS_LINKER_FLAGS)' so patching is unnecessary" >&2; \
				exit 1; \
			fi; \
			patchelf --set-interpreter "$(ROOTFS_INTERPRETER)" --set-rpath "$(ROOTFS_RPATH)" "$$target"; \
		fi; \
	else \
		ln -sfn "$(APP)" "$$target"; \
	fi

clean:
	rm -rf $(APP_DIR)/build/
	rm -f $(ROOTFS_LINK_FLAGS_STAMP)
