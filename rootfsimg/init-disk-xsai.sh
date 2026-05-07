#!/bin/busybox sh

set -eu

XSAI_MODE="${XSAI_MODE:-manual}"
WORKLOAD="${WORKLOAD:-llama-fake-bench-suite}"
AUTO_EXIT="${AUTO_EXIT:-0}"
DROP_SHELL="${DROP_SHELL:-1}"
RUN_AFTER_WORKLOAD="${RUN_AFTER_WORKLOAD:-1}"
DUMP_THP="${DUMP_THP:-1}"
WORKLOAD_STATUS=0

if [ -f /etc/xsai-init.conf ]; then
  . /etc/xsai-init.conf
fi

. /etc/xsai-init-common.sh
. /etc/xsai-workloads.sh

finish_init()
{
  if [ "$DROP_SHELL" = 1 ]; then
    log "done; entering shell"
    exec /bin/sh
  fi

  if [ "$AUTO_EXIT" = 1 ]; then
    log "done; auto-exit requested, status $WORKLOAD_STATUS"
    /bin/busybox poweroff -f 2>/dev/null || /bin/busybox halt -f 2>/dev/null || exit "$WORKLOAD_STATUS"
  fi

  log "done; no auto-exit requested, entering shell"
  exec /bin/sh
}

main()
{
  env_init

  log "init mode: $XSAI_MODE"
  log "selected workload: $WORKLOAD"

  case "$XSAI_MODE" in
    shell)
      WORKLOAD_STATUS=0
      ;;
    ci|manual)
      run_workload
      ;;
    none)
      log "init workload disabled"
      WORKLOAD_STATUS=0
      ;;
    *)
      warn "unknown XSAI_MODE: $XSAI_MODE"
      WORKLOAD_STATUS=2
      ;;
  esac

  finish_init
}

main "$@"
