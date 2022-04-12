import os
import sys

# (filelist, arguments) information for each benchmark
# filelist[0] should always be the binary file

cross_compile = "riscv64-linux-gnu-gcc-9.3.0"
#cross_compile = "riscv64-unknown-linux-gnu-gcc-10.2.0"

spec_info = {
  "astar_biglakes": (
    [
      "${SPEC}/spec06_exe/astar_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/astar/BigLakes2048.bin",
      "${SPEC}/cpu2006_run_dir/astar/BigLakes2048.cfg"
    ],
    [ "BigLakes2048.cfg" ]
  ),
  "astar_rivers": (
    [
      "${SPEC}/spec06_exe/astar_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/astar/rivers.bin",
      "${SPEC}/cpu2006_run_dir/astar/rivers.cfg"
    ],
    [ "rivers.cfg" ]
  ),
  "bwaves": (
    [
      "${SPEC}/spec06_exe/bwaves_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/bwaves/bwaves.in"
    ],
    []
  ),
  "bzip2_chicken": (
    [
      "${SPEC}/spec06_exe/bzip2_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/bzip2/chicken.jpg"
    ],
    [ "chicken.jpg", "30" ]
  ),
  "bzip2_combined": (
    [
      "${SPEC}/spec06_exe/bzip2_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/bzip2/input.combined"
    ],
    [ "input.combined", "200" ]
  ),
  "bzip2_html": (
    [
      "${SPEC}/spec06_exe/bzip2_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/bzip2/text.html"
    ],
    [ "text.html", "280" ]
  ),
  "bzip2_liberty": (
    [
      "${SPEC}/spec06_exe/bzip2_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/bzip2/liberty.jpg"
    ],
    [ "liberty.jpg", "30" ]
  ),
  "bzip2_program": (
    [
      "${SPEC}/spec06_exe/bzip2_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/bzip2/input.program"
    ],
    [ "input.program", "280" ]
  ),
  "bzip2_source": (
    [
      "${SPEC}/spec06_exe/bzip2_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/bzip2/input.source"
    ],
    [ "input.source", "280" ]
  ),
  "cactusADM": (
    [
      "${SPEC}/spec06_exe/cactusADM_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/cactusADM/benchADM.par"
    ],
    [ "benchADM.par" ]
  ),
  "calculix": (
    [
      "${SPEC}/spec06_exe/calculix_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/calculix/hyperviscoplastic.dat",
      "${SPEC}/cpu2006_run_dir/calculix/hyperviscoplastic.frd",
      "${SPEC}/cpu2006_run_dir/calculix/hyperviscoplastic.inp",
      "${SPEC}/cpu2006_run_dir/calculix/hyperviscoplastic.sta"
    ],
    [ "-i", "hyperviscoplastic" ]
  ),
  "dealII": (
    [
      "${SPEC}/spec06_exe/dealII_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/dealII/DummyData"
    ],
    [ "23" ]
  ),
  "gamess_cytosine": (
    [
      "${SPEC}/spec06_exe/gamess_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gamess/cytosine.2.config",
      "${SPEC}/cpu2006_run_dir/gamess/cytosine.2.inp"
    ],
    [ "<", "cytosine.2.config" ]
  ),
  "gamess_gradient": (
    [
      "${SPEC}/spec06_exe/gamess_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gamess/h2ocu2+.gradient.config",
      "${SPEC}/cpu2006_run_dir/gamess/h2ocu2+.gradient.inp"
    ],
    [ "<", "h2ocu2+.gradient.config" ]
  ),
  "gamess_triazolium": (
    [
      "${SPEC}/spec06_exe/gamess_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gamess/triazolium.config",
      "${SPEC}/cpu2006_run_dir/gamess/triazolium.inp"
    ],
    [ "<", "triazolium.config" ]
  ),
  "gcc_166": (
    [
      "${SPEC}/spec06_exe/gcc_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gcc/166.i"
    ],
    [ "166.i", "-o", "166.s" ]
  ),
  "gcc_200": (
    [
      "${SPEC}/spec06_exe/gcc_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gcc/200.i"
    ],
    [ "200.i", "-o", "200.s" ]
  ),
  "gcc_cpdecl": (
    [
      "${SPEC}/spec06_exe/gcc_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gcc/cp-decl.i"
    ],
    [ "cp-decl.i", "-o", "cp-decl.s" ]
  ),
  "gcc_expr2": (
    [
      "${SPEC}/spec06_exe/gcc_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gcc/expr2.i"
    ],
    [ "expr2.i", "-o", "expr2.s" ]
  ),
  "gcc_expr": (
    [
      "${SPEC}/spec06_exe/gcc_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gcc/expr.i"
    ],
    [ "expr.i", "-o", "expr.s" ]
  ),
  "gcc_g23": (
    [
      "${SPEC}/spec06_exe/gcc_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gcc/g23.i"
    ],
    [ "g23.i", "-o", "g23.s" ]
  ),
  "gcc_s04": (
    [
      "${SPEC}/spec06_exe/gcc_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gcc/s04.i"
    ],
    [ "s04.i", "-o", "s04.s" ]
  ),
  "gcc_scilab": (
    [
      "${SPEC}/spec06_exe/gcc_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gcc/scilab.i"
    ],
    [ "scilab.i", "-o", "scilab.s" ]
  ),
  "gcc_typeck": (
    [
      "${SPEC}/spec06_exe/gcc_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gcc/c-typeck.i"
    ],
    [ "c-typeck.i", "-o", "c-typeck.s" ]
  ),
  "GemsFDTD": (
    [
      "${SPEC}/spec06_exe/GemsFDTD_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/GemsFDTD/ref.in",
      "${SPEC}/cpu2006_run_dir/GemsFDTD/sphere.pec",
      "${SPEC}/cpu2006_run_dir/GemsFDTD/yee.dat"
    ],
    []
  ),
  "gobmk_13x13": (
    [
      "${SPEC}/spec06_exe/gobmk_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gobmk/13x13.tst",
      "dir games ${SPEC}/cpu2006_run_dir/gobmk/games",
      "dir golois ${SPEC}/cpu2006_run_dir/gobmk/golois"
    ],
    [ "--quiet", "--mode", "gtp", "<", "13x13.tst" ]
  ),
  "gobmk_nngs": (
    [
      "${SPEC}/spec06_exe/gobmk_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gobmk/nngs.tst",
      "dir games ${SPEC}/cpu2006_run_dir/gobmk/games",
      "dir golois ${SPEC}/cpu2006_run_dir/gobmk/golois"
    ],
    [ "--quiet", "--mode", "gtp", "<", "nngs.tst" ]
  ),
  "gobmk_score2": (
    [
      "${SPEC}/spec06_exe/gobmk_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gobmk/score2.tst",
      "dir games ${SPEC}/cpu2006_run_dir/gobmk/games",
      "dir golois ${SPEC}/cpu2006_run_dir/gobmk/golois"
    ],
    [ "--quiet", "--mode", "gtp", "<", "score2.tst" ]
  ),
  "gobmk_trevorc": (
    [
      "${SPEC}/spec06_exe/gobmk_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gobmk/trevorc.tst",
      "dir games ${SPEC}/cpu2006_run_dir/gobmk/games",
      "dir golois ${SPEC}/cpu2006_run_dir/gobmk/golois"
    ],
    [ "--quiet", "--mode", "gtp", "<", "trevorc.tst" ]
  ),
  "gobmk_trevord": (
    [
      "${SPEC}/spec06_exe/gobmk_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gobmk/trevord.tst",
      "dir games ${SPEC}/cpu2006_run_dir/gobmk/games",
      "dir golois ${SPEC}/cpu2006_run_dir/gobmk/golois"
    ],
    [ "--quiet", "--mode", "gtp", "<", "trevord.tst" ]
  ),
  "gromacs": (
    [
      "${SPEC}/spec06_exe/gromacs_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gromacs/gromacs.tpr"
    ],
    [ "-silent", "-deffnm", "gromacs.tpr", "-nice", "0" ]
  ),
  "h264ref_foreman.baseline": (
    [
      "${SPEC}/spec06_exe/h264ref_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/h264ref/foreman_ref_encoder_baseline.cfg",
      "${SPEC}/cpu2006_run_dir/h264ref/foreman_qcif.yuv"
    ],
    [ "-d", "foreman_ref_encoder_baseline.cfg" ]
  ),
  "h264ref_foreman.main": (
    [
      "${SPEC}/spec06_exe/h264ref_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/h264ref/foreman_ref_encoder_main.cfg",
      "${SPEC}/cpu2006_run_dir/h264ref/foreman_qcif.yuv"
    ],
    [ "-d", "foreman_ref_encoder_main.cfg" ]
  ),
  "h264ref_sss": (
    [
      "${SPEC}/spec06_exe/h264ref_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/h264ref/sss_encoder_main.cfg",
      "${SPEC}/cpu2006_run_dir/h264ref/sss.yuv"
    ],
    [ "-d", "sss_encoder_main.cfg" ]
  ),
  "hmmer_nph3": (
    [
      "${SPEC}/spec06_exe/hmmer_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/hmmer/nph3.hmm",
      "${SPEC}/cpu2006_run_dir/hmmer/swiss41"
    ],
    [ "nph3.hmm", "swiss41" ]
  ),
  "hmmer_retro": (
    [
      "${SPEC}/spec06_exe/hmmer_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/hmmer/retro.hmm"
    ],
    [ "--fixed", "0", "--mean", "500", "--num", "500000", "--sd", "350", "--seed", "0", "retro.hmm" ]
  ),
  "lbm": (
    [
      "${SPEC}/spec06_exe/lbm_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/lbm/100_100_130_ldc.of",
      "${SPEC}/cpu2006_run_dir/lbm/lbm.in"
    ],
    [ "3000", "reference.dat", "0", "0", "100_100_130_ldc.of" ]
  ),
  "leslie3d": (
    [
      "${SPEC}/spec06_exe/leslie3d_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/leslie3d/leslie3d.in"
    ],
    [ "<", "leslie3d.in" ]
  ),
  "libquantum": (
    [
      "${SPEC}/spec06_exe/libquantum_base." + cross_compile
    ],
    [ "1397", "8" ]
  ),
  "mcf": (
    [
      "${SPEC}/spec06_exe/mcf_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/mcf/inp.in"
    ],
    [ "inp.in" ]
  ),
  "milc": (
    [
      "${SPEC}/spec06_exe/milc_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/milc/su3imp.in"
    ],
    [ "<", "su3imp.in" ]
  ),
  "namd": (
    [
      "${SPEC}/spec06_exe/namd_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/namd/namd.input"
    ],
    [ "--input", "namd.input", "--iterations", "38", "--output", "namd.out" ]
  ),
  "omnetpp": (
    [
      "${SPEC}/spec06_exe/omnetpp_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/omnetpp/omnetpp.ini"
    ],
    [ "omnetpp.ini" ]
  ),
  "perlbench_checkspam": (
    [
      "${SPEC}/spec06_exe/perlbench_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/perlbench/cpu2006_mhonarc.rc",
      "${SPEC}/cpu2006_run_dir/perlbench/checkspam.pl",
      "${SPEC}/cpu2006_run_dir/perlbench/checkspam.in",
      "dir lib ${SPEC}/cpu2006_run_dir/perlbench/lib",
      "dir rules ${SPEC}/cpu2006_run_dir/perlbench/rules"
    ],
    [ "-I./lib", "checkspam.pl", "2500", "5", "25", "11", "150", "1", "1", "1", "1" ]
  ),
  "perlbench_diffmail": (
    [
      "${SPEC}/spec06_exe/perlbench_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/perlbench/cpu2006_mhonarc.rc",
      "${SPEC}/cpu2006_run_dir/perlbench/diffmail.pl",
      "${SPEC}/cpu2006_run_dir/perlbench/diffmail.in",
      "dir lib ${SPEC}/cpu2006_run_dir/perlbench/lib",
      "dir rules ${SPEC}/cpu2006_run_dir/perlbench/rules"
    ],
    [ "-I./lib", "diffmail.pl", "4", "800", "10", "17", "19", "300" ]
  ),
  "perlbench_splitmail": (
    [
      "${SPEC}/spec06_exe/perlbench_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/perlbench/cpu2006_mhonarc.rc",
      "${SPEC}/cpu2006_run_dir/perlbench/splitmail.pl",
      "${SPEC}/cpu2006_run_dir/perlbench/splitmail.in",
      "dir lib ${SPEC}/cpu2006_run_dir/perlbench/lib",
      "dir rules ${SPEC}/cpu2006_run_dir/perlbench/rules"
    ],
    [ "-I./lib", "splitmail.pl", "1600", "12", "26", "16", "4500" ]
  ),
  "povray": (
    [
      "${SPEC}/spec06_exe/povray_base." + cross_compile,
      "dir . ${SPEC}/cpu2006_run_dir/povray"
    ],
    [ "SPEC-benchmark-ref.ini" ]
  ),
  "sjeng": (
    [
      "${SPEC}/spec06_exe/sjeng_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/sjeng/ref.txt"
    ],
    [ "ref.txt" ]
  ),
  "soplex_pds-50": (
    [
      "${SPEC}/spec06_exe/soplex_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/soplex/pds-50.mps"
    ],
    [ "-s1", "-e", "-m45000", "pds-50.mps" ]
  ),
  "soplex_ref": (
    [
      "${SPEC}/spec06_exe/soplex_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/soplex/ref.mps"
    ],
    [ "-m3500", "ref.mps" ]
  ),
  "sphinx3": (
    [
      "${SPEC}/spec06_exe/sphinx_livepretend_base." + cross_compile,
      "dir . ${SPEC}/cpu2006_run_dir/sphinx3"
    ],
    [ "ctlfile", ".", "args.an4" ]
  ),
  "tonto": (
    [
      "${SPEC}/spec06_exe/tonto_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/tonto/stdin"
    ],
    []
  ),
  "wrf": (
    [
      "${SPEC}/spec06_exe/wrf_base." + cross_compile,
      "dir . ${SPEC}/cpu2006_run_dir/wrf"
    ],
    []
  ),
  "xalancbmk": (
    [
      "${SPEC}/spec06_exe/Xalan_base." + cross_compile,
      "dir . ${SPEC}/cpu2006_run_dir/xalancbmk"
    ],
    [ "-v", "t5.xml", "xalanc.xsl" ]
  ),
  "zeusmp": (
    [
      "${SPEC}/spec06_exe/zeusmp_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/zeusmp/zmp_inp"
    ],
    []
  ),
  # WARNING: this is SPEC test
  "gamess_exam29": (
    [
      "${SPEC}/spec06_exe/gamess_base." + cross_compile,
      "${SPEC}/cpu2006_run_dir/gamess/exam29.config",
      "${SPEC}/cpu2006_run_dir/gamess/exam29.inp"
    ],
    [ "<", "exam29.config" ]
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
  "",
  "# memtester",
  "file /bin/memtester /nfs/home/xuyinan/nanshan/memtester/memtester 755 0 0",
  "",
  "# busybox",
  "file /bin/busybox ${RISCV_ROOTFS_HOME}/rootfsimg/build/busybox 755 0 0",
  # "file /etc/inittab ${RISCV_ROOTFS_HOME}/rootfsimg/inittab-spec 755 0 0",
  "file /etc/inittab ${RISCV_ROOTFS_HOME}/rootfsimg/inittab 755 0 0",
  "slink /init /bin/busybox 755 0 0",
  "",
  "# SPEC common",
  "dir /spec_common 755 0 0",
  "#file /spec_common/before_workload ${SPEC}/before_workload 755 0 0",
  "#file /spec_common/trap ${SPEC}/trap_new 755 0 0",
  "",
  "# SPEC",
  "dir /spec 755 0 0",
  "file /spec/run.sh ${RISCV_ROOTFS_HOME}/rootfsimg/run.sh 755 0 0",
  "file /spec/checkmd5.sh ${RISCV_ROOTFS_HOME}/rootfsimg/checkmd5.sh 755 0 0"
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
  print(f"Generating initramfs: {specs}")
  lines = default_files.copy()
  for spec in specs:
    spec_files = spec_info[spec][0]
    for i, filename in enumerate(spec_files):
      if len(filename.split()) == 1:
        # print(f"default {filename} to file 755 0 0")
        basename = filename.split("/")[-1]
        filename = f"file /spec/{basename} {filename} 755 0 0"
        lines.append(filename)
      elif len(filename.split()) == 3:
        node_type, name, path = filename.split()
        if node_type != "dir":
          print(f"unknown filename: {filename}")
          continue
        all_dirs, all_files = traverse_path(path)
        lines.append(f"dir /spec/{name} 755 0 0")
        for sub_dir in all_dirs:
          lines.append(f"dir /spec/{name}/{sub_dir} 755 0 0")
        for file in all_files:
          lines.append(f"file /spec/{name}/{file} {path}/{file} 755 0 0")
      else:
        print(f"unknown filename: {filename}")
  with open("initramfs-spec.txt", "w") as f:
    f.writelines(map(lambda x: x + "\n", lines))


def generate_run_sh(specs, withTrap=False):
  lines =[ ]
  lines.append("#!/bin/sh")
  lines.append("echo '===== Start running SPEC2006 ====='")
  for spec in specs:
    spec_bin = spec_info[spec][0][0].split("/")[-1]
    spec_cmd = " ".join(spec_info[spec][1])
    lines.append(f"echo '======== BEGIN {spec} ========'")
    # lines.append("set -x")
    lines.append(f"md5sum /spec/{spec_bin}")
    lines.append("date -R")
    lines.append(f"cd /spec && time ./{spec_bin} {spec_cmd} > {spec}_output.log 2>&1")
    lines.append(f"tail {spec}_output.log")
    lines.append("date -R")
    #lines.append("set +x")
    lines.append(f"echo '======== END   {spec} ========'")
  lines.append("echo '===== Finish running SPEC2006 ====='")
  if withTrap:
    #lines.append("/spec_common/trap")
    pass
  with open("run.sh", "w") as f:
    f.writelines(map(lambda x: x + "\n", lines))

def generate_checkmd5_sh(specs):
  lines =[ ]
  lines.append("#!/bin/sh")
  lines.append("while true")
  lines.append("do")
  for spec in specs:
    spec_bin = spec_info[spec][0][0].split("/")[-1]
    lines.append(f"md5sum /spec/{spec_bin}")
  lines.append("done")
  with open("checkmd5.sh", "w") as f:
    f.writelines(map(lambda x: x + "\n", lines))

if __name__ == "__main__":
  all_spec06_ref = list(spec_info.keys())[:-1]
  print(len(all_spec06_ref), all_spec06_ref)
  specs = sys.argv[1:]
  # specs = all_spec06_ref[:11]
  # specs = all_spec06_ref[11:24]
  # specs = all_spec06_ref[24:34]
  # specs = all_spec06_ref[34:43]
  # specs = all_spec06_ref[43:46]
  # specs = all_spec06_ref[46:50]
  # specs = all_spec06_ref[50:52]
  # specs = all_spec06_ref[52:]
  print(specs)
  generate_initramfs(specs)
  generate_run_sh(specs, True)
  generate_checkmd5_sh(specs)
