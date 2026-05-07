#!/usr/bin/env bash

set -euo pipefail

# Convert one or more GGUF files into metadata-only `.gguf.om` files.
#
# What this script does:
# - builds a tiny helper against this repo's GGUF library
# - loads the source GGUF metadata and tensor descriptors
# - writes a new GGUF with `gguf_write_to_file(..., only_meta = true)`
#
# What the output is for:
# - `llama-bench --fake-like <model.gguf.om>`
# - benchmarking shape/graph/memory behavior without tensor payload I/O
#
# What the output is not for:
# - normal `llama-bench -m`
# - normal inference or correctness checks

script_dir=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo_dir="${LLAMA_REPO_DIR:-$script_dir/repo}"
build_dir="${LLAMA_BUILD_DIR:-$script_dir/build-host}"
tmp_dir="${TMPDIR:-/tmp}"
helper_src="$tmp_dir/gguf_meta_only_helper.cpp"
helper_bin="$tmp_dir/gguf_meta_only_helper"

suffix=".om"
force=0
output_path=""
input_dir=""
declare -a inputs=()

usage() {
  cat <<'USAGE'
usage:
  gguf-metadata-only.sh [options] FILE.gguf [FILE2.gguf ...]
  gguf-metadata-only.sh [options] --dir DIR

options:
  -o, --output PATH   output path for a single input file
  -s, --suffix TEXT   suffix appended to each input path (default: .om)
  -f, --force         overwrite existing outputs
  --dir DIR           convert all *.gguf files in DIR
  -h, --help          show this help

examples:
  gguf-metadata-only.sh /path/model.gguf
  gguf-metadata-only.sh --dir /path/to/models
  gguf-metadata-only.sh -o /tmp/model.gguf.om /path/model.gguf

notes:
  - outputs are intended for `llama-bench --fake-like`
  - outputs are metadata-only and will fail with normal `-m`
USAGE
}

die() {
  echo "gguf-metadata-only: $*" >&2
  exit 1
}

build_helper() {
  [[ -d "$repo_dir/ggml/include" ]] || die "repo headers not found under $repo_dir"
  [[ -f "$build_dir/ggml/src/libggml.a" ]] || die "missing $build_dir/ggml/src/libggml.a; build-host is required"
  [[ -f "$build_dir/ggml/src/libggml-base.a" ]] || die "missing $build_dir/ggml/src/libggml-base.a; build-host is required"
  [[ -f "$build_dir/ggml/src/libggml-cpu.a" ]] || die "missing $build_dir/ggml/src/libggml-cpu.a; build-host is required"

  cat > "$helper_src" <<'CPP'
#include "gguf.h"

#include <cstdio>

int main(int argc, char ** argv) {
    if (argc != 3) {
        std::fprintf(stderr, "usage: %s <input.gguf> <output.gguf.om>\n", argv[0]);
        return 1;
    }

    ggml_context * ctx_data = nullptr;
    gguf_init_params params = {
        /*.no_alloc = */ true,
        /*.ctx      = */ &ctx_data,
    };

    gguf_context * ctx = gguf_init_from_file(argv[1], params);
    if (ctx == nullptr) {
        std::fprintf(stderr, "failed to load %s\n", argv[1]);
        return 2;
    }

    if (!gguf_write_to_file(ctx, argv[2], /*only_meta =*/ true)) {
        std::fprintf(stderr, "failed to write %s\n", argv[2]);
        gguf_free(ctx);
        return 3;
    }

    gguf_free(ctx);
    return 0;
}
CPP

  "${CXX:-c++}" \
    -std=c++17 \
    -I"$repo_dir/ggml/include" \
    -I"$repo_dir/ggml/src" \
    "$helper_src" \
    "$build_dir/ggml/src/libggml.a" \
    "$build_dir/ggml/src/libggml-base.a" \
    "$build_dir/ggml/src/libggml-cpu.a" \
    -lpthread -ldl \
    -o "$helper_bin"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output)
      [[ $# -ge 2 ]] || die "missing value for $1"
      output_path="$2"
      shift 2
      ;;
    -s|--suffix)
      [[ $# -ge 2 ]] || die "missing value for $1"
      suffix="$2"
      shift 2
      ;;
    -f|--force)
      force=1
      shift
      ;;
    --dir)
      [[ $# -ge 2 ]] || die "missing value for $1"
      input_dir="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      while [[ $# -gt 0 ]]; do
        inputs+=("$1")
        shift
      done
      ;;
    -*)
      die "unknown option: $1"
      ;;
    *)
      inputs+=("$1")
      shift
      ;;
  esac
done

if [[ -n "$input_dir" && ${#inputs[@]} -gt 0 ]]; then
  die "use either explicit files or --dir, not both"
fi

if [[ -n "$input_dir" ]]; then
  shopt -s nullglob
  for file in "$input_dir"/*.gguf; do
    inputs+=("$file")
  done
  shopt -u nullglob
fi

[[ ${#inputs[@]} -gt 0 ]] || die "no input GGUF files provided"

if [[ -n "$output_path" && ${#inputs[@]} -ne 1 ]]; then
  die "--output can only be used with a single input file"
fi

build_helper

for input_path in "${inputs[@]}"; do
  [[ -f "$input_path" ]] || die "input not found: $input_path"

  if [[ -n "$output_path" ]]; then
    current_output="$output_path"
  else
    current_output="$input_path$suffix"
  fi

  if [[ -e "$current_output" && $force -ne 1 ]]; then
    die "output already exists: $current_output (use --force to overwrite)"
  fi

  "$helper_bin" "$input_path" "$current_output"
  ls -lh "$current_output"
done
