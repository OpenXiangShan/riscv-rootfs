run_and_capture()
{
  if run_workload_cmd "$@"; then
    WORKLOAD_STATUS=0
  else
    WORKLOAD_STATUS=$?
  fi
}

run_llama_bench()
{
  run_workload_cmd /bin/llama-bench \
    -m "$LLAMA_MODEL" \
    -t 1 -p 512 -n 0 \
    --no-warmup --estimate-prompt 1
}

run_llama_simple()
{
  run_workload_cmd /bin/llama-simple-xsai -m "$LLAMA_MODEL" "$LLAMA_PROMPT"
}

run_llama_xsai()
{
  run_workload_cmd /bin/llama-xsai --model "$LLAMA_MODEL" --prompt "$LLAMA_PROMPT"
}

run_llama_fake_bench_suite()
{
  status=0
  bench_args="-t 1 -p 128 -n 0 -r 1 --estimate-prompt 1 --no-warmup"

  export GGML_AME_LOG="${GGML_AME_LOG:-0}"
  export GGML_AME_PACKED_Q8="${GGML_AME_PACKED_Q8:-1}"

  if [ "${TRACE_WORKLOAD:-1}" = 1 ]; then
    set -x
  fi

  for model in \
    /root/stories15M-q8_0.gguf.om \
    /root/qwen3_0.6b_q8.gguf.om \
    /root/llama3.2_1b_q8.gguf.om \
    /root/DeepSeek-R1-Distill-Qwen-1.5B-q8_0.gguf.om
  do
    if run_workload_cmd /bin/llama-bench --fake-like "$model" $bench_args; then
      :
    else
      rc=$?
      if [ "$status" = 0 ]; then
        status=$rc
      fi
    fi
  done

  if [ "${TRACE_WORKLOAD:-1}" = 1 ]; then
    set +x
  fi

  return "$status"
}

run_selected_workload()
{
  case "$WORKLOAD" in
    none)
      log "workload disabled"
      WORKLOAD_STATUS=0
      ;;
    shell)
      log "workload set to shell; skipping automatic execution"
      WORKLOAD_STATUS=0
      ;;
    hello_xsai)
      log "launching hello_xsai"
      run_and_capture /bin/hello_xsai
      ;;
    gemm_precomp)
      log "launching gemm_precomp"
      run_and_capture /bin/gemm_precomp
      ;;
    pmu_test)
      log "launching pmu_test"
      run_and_capture /bin/pmu_test
      ;;
    llama-bench)
      log "launching llama-bench"
      if run_llama_bench; then
        WORKLOAD_STATUS=0
      else
        WORKLOAD_STATUS=$?
      fi
      ;;
    llama-fake-bench-suite)
      log "launching llama fake-like bench suite"
      if run_llama_fake_bench_suite; then
        WORKLOAD_STATUS=0
      else
        WORKLOAD_STATUS=$?
      fi
      ;;
    llama-simple|llama-simple-xsai)
      log "launching llama-simple-xsai"
      if run_llama_simple; then
        WORKLOAD_STATUS=0
      else
        WORKLOAD_STATUS=$?
      fi
      ;;
    llama-xsai)
      log "launching llama-xsai"
      if run_llama_xsai; then
        WORKLOAD_STATUS=0
      else
        WORKLOAD_STATUS=$?
      fi
      ;;
    *)
      warn "unknown WORKLOAD: $WORKLOAD"
      WORKLOAD_STATUS=2
      ;;
  esac
}
