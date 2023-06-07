import os
import sys
import shutil

# (filelist, arguments) information for each benchmark
# filelist[0] should always be the binary file
mybench_info = {
  "branchopt_dijkstra_opt": (
    [
      "/nfs/home/zhangchuanqi/lvna/benchmarks/branch-opt/dijkstra/dijkstra.opt",
    ],
    [ ],
    [ ]
  ),
  "branchopt_dijkstra_ori": (
    [
      "/nfs/home/zhangchuanqi/lvna/benchmarks/branch-opt/dijkstra/build/dijkstra",
    ],
    [ ],
    [ ]
  ),
  "branchopt_905_ori": (
    [
      "/nfs/home/zhangchuanqi/lvna/benchmarks/branch-opt/sortArrayByParity/build/905.sortArrayByParity",
    ],
    [ ],
    [ ]
  ),
  "branchopt_905_opt": (
    [
      "/nfs/home/zhangchuanqi/lvna/benchmarks/branch-opt/sortArrayByParity/905.opt",
    ],
    [ ],
    [ ]
  ),

}

default_files = [
  "dir /bin 755 0 0",
  "dir /etc 755 0 0",
  "dir /dev 755 0 0",
  "dir /lib 755 0 0",
  "dir /proc 755 0 0",
  "dir /sbin 755 0 0",
  "dir /sys 755 0 0",
  "dir /tmp 755 0 0",
  "dir /usr 755 0 0",
  "dir /mnt 755 0 0",
  "dir /usr/bin 755 0 0",
  "dir /usr/lib 755 0 0",
  "dir /usr/sbin 755 0 0",
  "dir /var 755 0 0",
  "dir /var/tmp 755 0 0",
  "dir /root 755 0 0",
  "dir /var/log 755 0 0",
  "",
  "nod /dev/console 644 0 0 c 5 1",
  "nod /dev/null 644 0 0 c 1 3",
  "",
  "# libraries",
  "file /lib/ld-linux-riscv64-lp64d.so.1 ${RISCV}/sysroot/lib/ld-linux-riscv64-lp64d.so.1 755 0 0",
  "file /lib/libc.so.6 ${RISCV}/sysroot/lib/libc.so.6 755 0 0",
  "file /lib/libresolv.so.2 ${RISCV}/sysroot/lib/libresolv.so.2 755 0 0",
  "file /lib/libm.so.6 ${RISCV}/sysroot/lib/libm.so.6 755 0 0",
  "file /lib/libdl.so.2 ${RISCV}/sysroot/lib/libdl.so.2 755 0 0",
  "file /lib/libpthread.so.0 ${RISCV}/sysroot/lib/libpthread.so.0 755 0 0",
  "file /lib/ld-linux-riscv64-lp64d.so.1 ${RISCV}/sysroot/lib/ld-linux-riscv64-lp64d.so.1 755 0 0",
  "file /lib/libc.so.6 ${RISCV}/sysroot/lib/libc.so.6 755 0 0",
  "file /lib/libresolv.so.2 ${RISCV}/sysroot/lib/libresolv.so.2 755 0 0",
  "file /lib/libm.so.6 ${RISCV}/sysroot/lib/libm.so.6 755 0 0",
  "file /lib/libdl.so.2 ${RISCV}/sysroot/lib/libdl.so.2 755 0 0",
  "file /lib/libpthread.so.0 ${RISCV}/sysroot/lib/libpthread.so.0 755 0 0",
  "file /lib/libgfortran.so.5.0.0 ${RISCV}/sysroot/lib/libgfortran.so.5.0.0 755 0 0",
  "slink /lib/libgfortran.so.5 /lib/libgfortran.so.5.0.0 755 0 0",
  "slink /lib/libgfortran.so /lib/libgfortran.so.5.0.0 755 0 0",
  "file /lib/libgomp.so.1.0.0 ${RISCV}/sysroot/lib/libgomp.so.1.0.0 755 0 0",
  "slink /lib/libgomp.so.1 /lib/libgomp.so.1.0.0 755 0 0",
  "slink /lib/libgomp.so /lib/libgomp.so.1.0.0 755 0 0",
  "file /lib/libgcc_s.so.1 ${RISCV}/sysroot/lib/libgcc_s.so.1 755 0 0",
  "file /lib/libstdc++.so.6 ${RISCV}/sysroot/lib/libstdc++.so.6 755 0 0",
  "file /lib/librt.so.1 ${RISCV}/sysroot/lib/librt.so.1 755 0 0",
  "file /lib/libz.so.1.2.11 ${MYRVLIB_PATH}/lib/libz.so.1.2.11 755 0 0",
  "slink /lib/libz.so /lib/libz.so.1.2.11 755 0 0",
  "slink /lib/libz.so.1 /lib/libz.so.1.2.11 755 0 0",
  "file /lib/libuuid.so.1.3.0 ${MYRVLIB_PATH}/lib/libuuid.so.1.3.0 755 0 0",
  "slink /lib/libuuid.so /lib/libuuid.so.1.3.0 755 0 0",
  "slink /lib/libuuid.so.1 /lib/libuuid.so.1.3.0 755 0 0",
  "",
  "# busybox",
  "file /bin/busybox ${RISCV_ROOTFS_HOME}/rootfsimg/build/busybox 755 0 0",
  "file /etc/inittab ${RISCV_ROOTFS_HOME}/rootfsimg/inittab-autorun-mybench 755 0 0",
  "slink /init /bin/busybox 755 0 0",
  "",
  "# cpt common",
  "dir /cpt_common 755 0 0",
  "file /cpt_common/new_before_workload ${RISCV_ROOTFS_HOME}/rootfsimg/build/new_before_workload 755 0 0",
  "file /cpt_common/notip_before_workload ${RISCV_ROOTFS_HOME}/rootfsimg/build/notip_before_workload 755 0 0",
  "file /cpt_common/after_workload ${RISCV_ROOTFS_HOME}/rootfsimg/build/after_workload 755 0 0",
  "",
  "# run script",
  "dir /mybench 755 0 0",
  "file /mybench/run.sh ${RISCV_ROOTFS_HOME}/rootfsimg/run.sh 755 0 0"
]

def traverse_path(path, stack=""):
  all_dirs, all_files = [], []
  for item in os.listdir(path):
    item_path = os.path.join(path, item)
    item_stack = os.path.join(stack, item)
    if os.path.isfile(item_path):
      all_files.append(item_stack)
    else:
      all_dirs.append(item_stack)
      sub_dirs, sub_files = traverse_path(item_path, item_stack)
      all_dirs.extend(sub_dirs)
      all_files.extend(sub_files)
  return (all_dirs, all_files)

def generate_initramfs(specs):
  lines = default_files.copy()
  for spec in specs:
    spec_files = mybench_info[spec][0]
    for i, filename in enumerate(spec_files):
      if len(filename.split()) == 1:
        # print(f"default {filename} to file 755 0 0")
        basename = filename.split("/")[-1]
        filename = f"file /mybench/{basename} {filename} 755 0 0"
        lines.append(filename)
      elif len(filename.split()) == 3:
        node_type, name, path = filename.split()
        if node_type != "dir":
          print(f"unknown filename: {filename}")
          continue
        all_dirs, all_files = traverse_path(path)
        lines.append(f"dir /mybench/{name} 755 0 0")
        for sub_dir in all_dirs:
          lines.append(f"dir /mybench/{name}/{sub_dir} 755 0 0")
        for file in all_files:
          lines.append(f"file /mybench/{name}/{file} {path}/{file} 755 0 0")
      else:
        print(f"unknown filename: {filename}")
  with open("initramfs-mybench.txt", "w") as f:
    f.writelines(map(lambda x: x + "\n", lines))


def generate_run_sh(specs, withTrap=False):
  lines =[ ]
  lines.append("#!/bin/sh")
  lines.append("echo '===== Start running mybench ====='")
  for spec in specs:
    spec_bin = mybench_info[spec][0][0].split("/")[-1]
    spec_cmd = " ".join(mybench_info[spec][1])
    lines.append(f"echo '======== BEGIN {spec} ========'")
    lines.append("set -x")
    # lines.append(f"md5sum /spec/{spec_bin}")
    # lines.append("date -R")
    # spec_check = " ".join(spec_info[spec][2])
    if withTrap:
      lines.append("/cpt_common/notip_before_workload")
    lines.append(f"cd /mybench && ./{spec_bin} {spec_cmd}")
    # lines.append("date -R")
    lines.append("set +x")
    lines.append(f"echo '======== END   {spec} ========'")
    # lines.append(f"md5sum {spec_check}")
  lines.append("echo '===== Finish running mybench ====='")
  if withTrap:
    lines.append("/cpt_common/after_workload")
  with open("run.sh", "w") as f:
    f.writelines(map(lambda x: x + "\n", lines))

if __name__ == "__main__":
  all_bms = list(mybench_info.keys())
  bin_dir_path = '/nfs/home/zhangchuanqi/lvna/for_xs/xs-env/sw/riscv-pk/out_bins/branchopt'
  for bm in all_bms:
    tmp_bm = [bm]
    generate_initramfs(tmp_bm)
    generate_run_sh(tmp_bm, True)
    os.system("make -j 16 -C /nfs/home/zhangchuanqi/lvna/for_xs/xs-env/sw/riscv-pk")
    os.makedirs(bin_dir_path, exist_ok=True)
    shutil.copy("/nfs/home/zhangchuanqi/lvna/for_xs/xs-env/sw/riscv-pk/build/bbl.bin",
                 os.path.join(bin_dir_path,f"{bm}.bin"))

