#!/bin/busybox sh

set -eu

/bin/busybox --install -s

mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev

hello_status=0

# /bin/before_workload
echo "[xsai-init] launching hello_xsai"
/bin/gemm_precomp
/bin/after_workload
if [ -x /bin/hello_xsai ]; then
  if /bin/hello_xsai; then
    hello_status=0
  else
    hello_status=$?
  fi
fi

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