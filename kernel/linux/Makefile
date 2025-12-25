NAME = linux
ARCH ?= riscv
CROSS_COMPILE ?= riscv64-unknown-linux-gnu-

include $(RISCV_ROOTFS_HOME)/Makefile.app
include $(RISCV_ROOTFS_HOME)/Makefile.get

URL = https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.13.tar.xz
KERNEL_HOME = $(EXTRACT_DOWNLOAD_TARGET)

HOST_BUILD = $(DST_DIR)/host_build
GUEST_BUILD = $(DST_DIR)/guest_build

HOST_CONFIG = $(HOST_BUILD)/.config
GUEST_CONFIG = $(GUEST_BUILD)/.config

HOST_IMAGE = $(HOST_BUILD)/arch/$(ARCH)/boot/Image
GUEST_IMAGE = $(GUEST_BUILD)/arch/$(ARCH)/boot/Image

KVM_SO = $(HOST_BUILD)/arch/

.PHONY: $(APP)
$(APP): | unpack

.PHONY: set_initramfs
set_initramfs:
	sed -i '/^CONFIG_INITRAMFS_SOURCE=/c CONFIG_INITRAMFS_SOURCE="$(INITRAMFS_TXT)"' $(BUILD)/.config

.PHONY: install_defconfig
install_defconfig: | $(KERNEL_HOME)
	@cp $(DEFCONFIG) $(KERNEL_HOME)/arch/$(ARCH)/configs/

$(HOST_CONFIG):
	@CROSS_COMPILE=$(CROSS_COMPILE) ARCH=$(ARCH) make -C $(KERNEL_HOME) O=$(HOST_BUILD) xiangshanhost_defconfig

$(HOST_IMAGE): $(HOST_CONFIG)
	@$(MAKE) BUILD=$(HOST_BUILD) set_initramfs
	@CROSS_COMPILE=$(CROSS_COMPILE) ARCH=$(ARCH) make -C $(KERNEL_HOME) O=$(HOST_BUILD) -j `nproc`

$(GUEST_CONFIG):
	@CROSS_COMPILE=$(CROSS_COMPILE) ARCH=$(ARCH) make -C $(KERNEL_HOME) O=$(GUEST_BUILD) xiangshan_defconfig

$(GUEST_IMAGE): $(GUEST_CONFIG)
	@$(MAKE) BUILD=$(GUEST_BUILD) set_initramfs
	@CROSS_COMPILE=$(CROSS_COMPILE) ARCH=$(ARCH) make -C $(KERNEL_HOME) O=$(GUEST_BUILD) -j `nproc`

$(DST_DIR)/host_Image: $(HOST_IMAGE)
	@ln -sf $(HOST_IMAGE) $(DST_DIR)/host_Image

$(DST_DIR)/guest_Image: $(GUEST_IMAGE)
	@ln -sf $(GUEST_IMAGE) $(DST_DIR)/guest_Image

.PHONY: _install_host_image
_install_host_image: $(DST_DIR)/host_Image

.PHONY: _install_guest_image
_install_guest_image: $(DST_DIR)/guest_Image

.PHONY: host_image
host_image: $(HOST_IMAGE)

.PHONY: guest_image
guest_image: $(GUEST_IMAGE)

.PHONY: clean_host
clean_host:
	@rm -rf $(HOST_BUILD)
	@rm -rf $(DST_DIR)/host_Image

.PHONY: clean_guest
clean_guest:
	@rm -rf $(GUEST_BUILD)
	@rm -rf $(DST_DIR)/guest_Image

.PHONY: clean_download
clean_download:
	@rm -rf $(DOWNLOAD_PATH)

.PHONY: clean
clean: clean_host clean_guest clean_download
	@rm -rf $(DST_DIR)

