#!/bin/busybox sh

set -eu

/bin/busybox --install -s

mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev

LLAMA_MODEL=/root/llama-model.gguf
MODEL_MNT=/models

mkdir -p "$MODEL_MNT"
if [ -b /dev/vda ]; then
  echo "[xsai-init] trying to mount /dev/vda"
  if mount -o ro,noload /dev/vda "$MODEL_MNT" 2>/dev/null || \
     mount -o ro /dev/vda "$MODEL_MNT" 2>/dev/null || \
     mount /dev/vda "$MODEL_MNT" 2>/dev/null; then
    if [ -f "$MODEL_MNT/model.gguf" ]; then
      LLAMA_MODEL="$MODEL_MNT/model.gguf"
    else
      set -- "$MODEL_MNT"/*.gguf
      if [ "$1" != "$MODEL_MNT/*.gguf" ] && [ -f "$1" ]; then
        LLAMA_MODEL="$1"
      fi
    fi
  else
    echo "[xsai-init] warning: failed to mount /dev/vda; using initramfs model"
  fi
else
  echo "[xsai-init] no /dev/vda; using initramfs model"
fi

echo "[xsai-init] model path: $LLAMA_MODEL"
# /bin/hello_xsai || true
# /bin/gemm_precomp || true
/bin/llama-bench -m $LLAMA_MODEL -t 1 -p 512 -n 0 --no-warmup || true
/bin/after_workload || true
# Enable user-mode access to hardware performance counters (rdcycle / rdinstret).
# The riscv_pmu_sbi driver exposes this via perf_user_access sysctl:
#   0 = no user access (scounteren = 0x0)
#   1 = user access via perf only (scounteren = 0x2, TIME only) -- default
#   2 = legacy: rdcycle/rdinstret directly accessible (scounteren = 0x7, CY+TM+IR)
# We need 2 so that unprivileged rdcycle / rdinstret CSR reads don't SIGILL.
if [ -f /proc/sys/kernel/perf_user_access ]; then
  echo 2 > /proc/sys/kernel/perf_user_access
fi

# Enable transparent huge pages (madvise mode) for large model weight mappings
if [ -f /sys/kernel/mm/transparent_hugepage/enabled ]; then
  echo madvise > /sys/kernel/mm/transparent_hugepage/enabled
fi
# initramfs is tmpfs (shmem); shmem THP has its own knob separate from the
# anonymous-THP "enabled" setting above.  Must be set to "advise" so that
# madvise(MADV_HUGEPAGE) on shmem-backed mmaps (the model file) is honoured.
if [ -f /sys/kernel/mm/transparent_hugepage/shmem_enabled ]; then
  echo advise > /sys/kernel/mm/transparent_hugepage/shmem_enabled
fi
hello_status=0
# 128 PROMPT TOKENS (arbitrary test value to check THP handling with large model mappings)
LLAMA_PROMPT="once upon a time, in a forest where the trees never lost their leaves, a young woodcutter discovered a door hidden beneath an ancient oak. the door was no taller than his knee and sealed with a lock shaped like a crescent moon. he had passed this way a hundred times but never noticed it before. that morning, something made him kneel in the soft earth and press his ear against the weathered wood. a voice from inside whispered his name. he reached into his coat pocket and found, to his astonishment, a silver key he had never seen before. with trembling "
# LLAMA_PROMPT="<|im_start|>system
# You are an expert embedded systems C programmer with 20 years of experience writing high-performance code for RISC-V architectures. Follow these strict guidelines:

# 1. CODE STYLE: Adhere to Linux kernel coding style (K&R braces, 8-space tabs, 80-col limit)
# 2. NAMING: Use descriptive lowercase_with_underscores; prefix constants with uppercase
# 3. TYPES: Prefer explicit sized types (uint32_t, size_t) from stdint.h/stddef.h
# 4. SAFETY: Always validate pointer arguments and array bounds with early returns
# 5. OPTIMIZATION: Use const for read-only pointers, restrict for aliasing hints, inline for small hot functions
# 6. DOCUMENTATION: Add kernel-style doc comments explaining @param, @return, and algorithm complexity
# 7. PRECISION: For float operations, consider accumulation order and numerical stability
# 8. ATTRIBUTES: Use __attribute__((aligned)) and compiler hints where beneficial

# Generate production-ready, MISRA-C compliant code suitable for bare-metal environments.<|im_end|>
# <|im_start|>user
# Write a short C function that computes the dot product of two float arrays.<|im_end|>
# <|im_start|>assistant
# "
echo "[xsai-init] launching llama-xsai"
/bin/llama-simple-xsai -m "$LLAMA_MODEL" "$LLAMA_PROMPT" || hello_status=$?
/bin/after_workload "$hello_status"
echo "[xsai-init] THP counters before llama:"
grep -E 'AnonHugePages|FileHugePages|ShmemHugePages' /proc/meminfo || true
grep 'thp_fault_alloc\|thp_collapse_alloc\|thp_file_mapped\|thp_file_alloc' /proc/vmstat || true

if [ -x /bin/llama-xsai ]; then
  /bin/llama-xsai --model "$LLAMA_MODEL" --prompt "${LLAMA_PROMPT:-Once}" || true
fi

echo "[xsai-init] THP counters after llama:"
grep -E 'AnonHugePages|FileHugePages|ShmemHugePages' /proc/meminfo || true
grep 'thp_fault_alloc\|thp_collapse_alloc\|thp_file_mapped\|thp_file_alloc' /proc/vmstat || true

# /bin/before_workload
# echo "[xsai-init] launching hello_xsai"
# /bin/gemm_precomp
# /bin/after_workload
# if [ -x /bin/hello_xsai ]; then
#   if /bin/hello_xsai; then
#     hello_status=0
#   else
#     hello_status=$?
#   fi
# fi

echo "[xsai-init] launching after_workload"
if [ -x /bin/after_workload ]; then
  /bin/after_workload "$hello_status" || true
fi

echo "[xsai-init] trying DSID cgroup setup"
if [ -d /sys/fs/cgroup ]; then
  CGROUP_ROOT=/sys/fs/cgroup
else
  CGROUP_ROOT=/cgroup
  mkdir -p "$CGROUP_ROOT"
  mount -t tmpfs cgroup_root "$CGROUP_ROOT" || true
fi

mkdir -p "$CGROUP_ROOT"/dsid/test-1 "$CGROUP_ROOT"/dsid/test-2
mount -t cgroup -o dsid dsid "$CGROUP_ROOT"/dsid || true
echo 1 > "$CGROUP_ROOT"/dsid/test-1/dsid.dsid-set || true
echo 2 > "$CGROUP_ROOT"/dsid/test-2/dsid.dsid-set || true

echo "[xsai-init] done; entering shell"
exec /bin/sh
