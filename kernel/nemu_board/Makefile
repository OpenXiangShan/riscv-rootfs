NAME = nemu_board
ARCH = riscv
CROSS_COMPILE =

include $(RISCV_ROOTFS_HOME)/Makefile.app
include $(RISCV_ROOTFS_HOME)/Makefile.get

REPO = https://github.com/OpenXiangShan/nemu_board.git

.PHONY: $(APP)
$(APP): | clone

.PHONY: config
config: | clone
	@ln -sf $(abspath $(CLONE_TARGET_REPO)/configs/xiangshan_defconfig) $(DST_DIR)/xiangshan_defconfig
	@ln -sf $(abspath $(CLONE_TARGET_REPO)/configs/xiangshanhost_defconfig) $(DST_DIR)/xiangshanhost_defconfig

.PHONY: dts
dts: | clone
	@cd $(CLONE_TARGET_REPO)/dts && bash build_single_core_for_nemu.sh && cd -
	@cd $(CLONE_TARGET_REPO)/dts && bash build_dual_core_for_qemu.sh   && cd -
	@cd $(CLONE_TARGET_REPO)/dts && bash build_four_core_for_qemu.sh   && cd -
	@cd $(CLONE_TARGET_REPO)/dts && bash build_eight_core_for_qemu.sh  && cd -
	@ln -sf $(abspath $(CLONE_TARGET_REPO)/dts/build/xiangshan.dtb)           $(DST_DIR)/
	@ln -sf $(abspath $(CLONE_TARGET_REPO)/dts/build/xiangshan_dualcore.dtb)  $(DST_DIR)/
	@ln -sf $(abspath $(CLONE_TARGET_REPO)/dts/build/xiangshan_fourcore.dtb)  $(DST_DIR)/
	@ln -sf $(abspath $(CLONE_TARGET_REPO)/dts/build/xiangshan_eightcore.dtb) $(DST_DIR)/

.PHONY: clean
clean:
	@rm -rf build
