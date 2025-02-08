import argparse
import os
import sys
import json
import yaml

elf_suffix = "_base.riscv64-linux-gnu-gcc-9.3.0"

# (filelist, arguments) information for each benchmark
# filelist[0] should always be the binary file

json_data = {}
default_initramfs_data = []

def load_json(json_path):
    with open(json_path, "r") as f:
        global json_data
        json_data = json.load(f)

def load_yaml(yaml_path):
    with open(yaml_path, "r") as f:
        global default_initramfs_data
        default_initramfs_data = yaml.safe_load(f)["default_files"]

def get_spec_info():
    spec_info = {}
    for spec_name, spec_details in json_data.items():
        base_name = spec_details["base_name"]
        files = [
            f"${{SPEC}}/spec06_exe/{base_name}" + elf_suffix
        ] + [
            f"${{SPEC}}/cpu2006_run_dir/{file}" for file in spec_details["files"]
        ]
        args = spec_details["args"]
        spec_type = spec_details["type"]
        spec_info[spec_name] = (files, args, spec_type)
    return spec_info

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

def generate_initramfs(initramfs_file, specs):
  lines = default_initramfs_data.copy()
  for spec in specs:
    spec_files = get_spec_info()[spec][0]
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
  with open(initramfs_file, "w") as f:
    f.writelines(map(lambda x: x + "\n", lines))


def generate_run_sh(run_sh, specs, withTrap=False):
  lines =[ ]
  lines.append("#!/bin/sh")
  lines.append("echo '===== Start running SPEC2006 ====='")
  for spec in specs:
    spec_bin = get_spec_info()[spec][0][0].split("/")[-1]
    spec_cmd = " ".join(get_spec_info()[spec][1])
    lines.append(f"echo '======== BEGIN {spec} ========'")
    lines.append("set -x")
    lines.append(f"md5sum /spec/{spec_bin}")
    lines.append("date -R")
    if withTrap:
      lines.append("/spec_common/before_workload")
    lines.append(f"cd /spec && ./{spec_bin} {spec_cmd}")
    if withTrap:
      lines.append("/spec_common/trap")
    lines.append("date -R")
    lines.append("set +x")
    lines.append(f"echo '======== END   {spec} ========'")
  lines.append("echo '===== Finish running SPEC2006 ====='")
  with open(run_sh, "w") as f:
    f.writelines(map(lambda x: x + "\n", lines))

def generate_build_scripts(build_sh, specs, withTrap=False, spec_gen=__file__):
  lines = []
  lines.append("#!/bin/sh")
  lines.append("set -x")
  lines.append("set -e")
  spike_dir, linux_dir = "../../riscv-pk", "../../riscv-linux"
  lines.append("mkdir -p spec_images")
  for spec in specs:
    target_dir = f"spec_images/{spec}"
    lines.append(f"mkdir -p {target_dir}")
    extra_args = ""
    if withTrap:
      extra_args += " --checkpoints"
    extra_args += f" --elf-suffix {elf_suffix}"
    lines.append(f"python3 {spec_gen} {spec}{extra_args}")
    lines.append(f"make -s -C {spike_dir} clean && make -s -C {spike_dir} -j100")
    bbl_elf = f"{spike_dir}/build/bbl"
    linux_elf = f"{linux_dir}/vmlinux"
    spec_elf = get_spec_info()[spec][0][0]
    bbl_bin = f"{spike_dir}/build/bbl.bin"
    for f in [bbl_elf, linux_elf, spec_elf]:
      filename = os.path.basename(f)
      lines.append(f"riscv64-unknown-linux-gnu-objdump -d {f} > {target_dir}/{filename}.txt")
    for f in [bbl_elf, linux_elf, spec_elf, bbl_bin]:
      lines.append(f"cp {f} {target_dir}")
  with open(build_sh, "w") as f:
    f.writelines(map(lambda x: x + "\n", lines))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='CPU CPU2006 ramfs scripts')
  parser.add_argument('benchspec', nargs='*', help='selected benchmarks')
  parser.add_argument('--json', required=True, help='select config json')
  parser.add_argument('--elf-suffix', '-s',
                      help='elf suffix (default: _base.riscv64-linux-gnu-gcc-9.3.0)')
  parser.add_argument('--checkpoints', action='store_true',
                      help='checkpoints mode (with before_workload and trap)')
  parser.add_argument('--scripts', action='store_true',
                      help='generate build scripts for spec ramfs')
  parser.add_argument('--initramfs-file', help="specify output initramfs file name")
  parser.add_argument('--run-sh-file', help="specify output run.sh file name")
  parser.add_argument('--build-sh-file', help="specify output build.sh file name")

  args = parser.parse_args()

  if args.elf_suffix is not None:
    elf_suffix = args.elf_suffix

  initramfs_file_name = "initramfs-spec.txt" if args.initramfs_file is None else args.initramfs_file
  run_sh_file_name = "run.sh" if args.run_sh_file is None else args.run_sh_file
  build_sh_file_name = "build.sh" if args.build_sh_file is None else args.build_sh_file

  load_json(args.json)
  load_yaml("initramfs_yaml/default_files.yaml")

  # parse benchspec
  benchspec = []
  spec_info = get_spec_info()
  for s in args.benchspec:
    if s in spec_info:
      benchspec.append(s)
    else:
      benchspec += [k for k in spec_info.keys() if set(s.split(",")) <= set(spec_info[k][2])]
  benchspec = sorted(set(benchspec))
  print(f"All {len(benchspec)} selected benchspec: {' '.join(benchspec)}")

  if args.scripts:
    generate_build_scripts(build_sh_file_name, benchspec, args.checkpoints)
  else:
    generate_initramfs(initramfs_file_name, benchspec)
    generate_run_sh(run_sh_file_name, benchspec, args.checkpoints)
