generate_config:
	@make -C nemu_board config

install_defconfig: generate_config
	@make -C linux install_defconfig DEFCONFIG=$(RISCV_ROOTFS_HOME)/kernel/nemu_board/build/xiangshanhost_defconfig
	@make -C linux install_defconfig DEFCONFIG=$(RISCV_ROOTFS_HOME)/kernel/nemu_board/build/xiangshan_defconfig

host_kernel: install_defconfig
	@make -C linux _install_host_image INITRAMFS_TXT=$(realpath $(INITRAMFS_TXT))

guest_kernel: install_defconfig
	@make -C linux _install_guest_image INITRAMFS_TXT=$(realpath $(INITRAMFS_TXT))

