# llama.cpp Benchmark Notes

This directory contains two different benchmark tools from llama.cpp:

- `llama-bench`
- `llama-batched-bench`

They answer different questions. Use the tool that matches the workload you want to measure.

## Which Tool To Use

Use `llama-bench` when you want to measure single-request inference performance.

Typical questions:

- How fast is prompt processing on this model?
- How fast is token generation on one request?
- How does throughput scale with thread count?
- What is the single-core or single-socket CPU performance?
- What happens if I change `n_batch`, `n_ubatch`, KV cache type, or context depth?

Use `llama-batched-bench` when you want to measure batched serving performance.

Typical questions:

- If I decode 2, 4, 8, or 32 sequences together, what total throughput do I get?
- How does shared prompt vs non-shared prompt change KV usage?
- What batch size gives the best aggregate serving throughput?
- How much KV cache is required for a serving-style workload?

Short rule:

- Single prompt / single stream / CPU core scaling: `llama-bench`
- Multi-sequence serving / batch scheduling / KV capacity planning: `llama-batched-bench`

## Main Difference

`llama-bench` measures one logical request at a time. It can run three styles of test:

- prompt processing only (`pp`, set by `-p`)
- text generation only (`tg`, set by `-n`)
- prompt processing plus generation (`pg`, set by `-pg`)

It is the right tool for measuring the raw latency/throughput behavior of a single inference stream.

`llama-batched-bench` measures multiple sequences decoded together in one batch. Its core knobs are:

- `PP`: prompt tokens per sequence
- `TG`: generated tokens per sequence
- `B`: number of parallel sequences
- prompt shared vs prompt not shared

It is the right tool for measuring server-style throughput and KV-cache pressure.

## Batch Size Does Not Mean The Same Thing

Yes, `llama-bench` also has `-b, --batch-size`, but here `batch-size` means the
decode chunk size used inside one logical request.

In practice, for `llama-bench`:

- `-b` controls how many prompt tokens are processed per decode call
- `-ub` controls the micro-batch size used by the backend
- it still measures one request stream at a time
- it does not turn one test into multi-sequence concurrent serving

So in `llama-bench`, increasing `-b` mainly changes the prompt-processing shape
of a single request.

For `llama-batched-bench`, the important extra dimension is not just `-b`, but
the number of parallel sequences being decoded together. That is the serving
workload dimension represented in its results as `B`, together with per-sequence
prompt length `PP`, generation length `TG`, and shared-prompt mode.

Short version:

- `llama-bench -b`: batch size inside one request
- `llama-batched-bench`: throughput of many sequences together

## Recommendation For This Repo

For the current XSAI workflow, start with `llama-bench`.

Reasons:

- Most of the recent work here has been around single-model loading and single-run execution.
- You were checking single-core CPU performance on the host.
- `llama-bench` directly exposes thread count, CPU mask, strict CPU affinity, batch size, and context depth.

Use `llama-batched-bench` only if you are moving to a serving-oriented question such as aggregate throughput under concurrent requests.

## Host Build Status In This Tree

The host build enables llama.cpp tools in [Makefile](Makefile).

- Host CMake sets `LLAMA_BUILD_TOOLS=ON`
- Target RISC-V CMake also sets `LLAMA_BUILD_TOOLS=ON`

That means:

- host benchmark binaries are expected under `build-host/bin/`
- guest-side benchmark binaries are expected under `build-riscv/bin/`
- `make -C firmware/riscv-rootfs/apps/llama.cpp install` copies the RISC-V benchmarks into `rootfsimg/build/`
- the initramfs manifest includes both benchmark binaries under `/bin/`

## Command Templates

Keep shared notes and committed docs free of machine-specific absolute paths.
Use shell variables or repo-relative paths in examples, and pass your local
model location at runtime.

From this directory, set a reusable model path once:

```bash
HOST_BIN="build-host/bin"
MODEL_PATH="path/to/model.gguf"
```

If your model is not stored under this repo, export `MODEL_PATH` in your shell
before running the examples instead of hardcoding a personal filesystem path in
the document.

Run `llama-bench` on the host for a normal single-request benchmark:

```bash
$HOST_BIN/llama-bench \
  -m "$MODEL_PATH"
```

Run a strict single-core benchmark on CPU0:

```bash
$HOST_BIN/llama-bench \
  -m "$MODEL_PATH" \
  -t 1 -C 0x1 --cpu-strict 1
```

Sweep CPU thread count for a single model:

```bash
$HOST_BIN/llama-bench \
  -m "$MODEL_PATH" \
  -t 1,2,4,8,16 \
  -p 512 -n 128 \
  -r 3
```

Measure prompt processing only:

```bash
$HOST_BIN/llama-bench \
  -m "$MODEL_PATH" \
  -p 512 -n 0
```

Measure generation only:

```bash
$HOST_BIN/llama-bench \
  -m "$MODEL_PATH" \
  -p 0 -n 128
```

Sweep prefilled context depth:

```bash
$HOST_BIN/llama-bench \
  -m "$MODEL_PATH" \
  -d 0,512,1024 \
  -p 512 -n 128
```

Run `llama-batched-bench` for serving-style aggregate throughput:

```bash
$HOST_BIN/llama-batched-bench \
  -m "$MODEL_PATH" \
  -c 2048 -b 2048 -ub 512 \
  -npp 128,256 \
  -ntg 128 \
  -npl 1,2,4,8
```

Run `llama-batched-bench` with shared prompt mode:

```bash
$HOST_BIN/llama-batched-bench \
  -m "$MODEL_PATH" \
  -c 2048 -b 2048 -ub 512 \
  -npp 128 \
  -ntg 128 \
  -npl 1,2,4,8 \
  -pps
```

Sweep parallel sequence count for batched serving:

```bash
$HOST_BIN/llama-batched-bench \
  -m "$MODEL_PATH" \
  -c 4096 -b 2048 -ub 512 \
  -npp 128 \
  -ntg 128 \
  -npl 1,2,4,8,16,32
```

## How To Interpret Results

For `llama-bench`:

- `pp512` means prompt processing throughput for 512 prompt tokens
- `tg128` means generation throughput for 128 generated tokens
- if you use `-pg pp,tg`, the reported throughput is over the combined token count

For `llama-batched-bench`:

- `S_PP` is prompt throughput
- `S_TG` is generation throughput
- `S` is total throughput over the whole batched run
- `N_KV` is the required KV-cache footprint for that workload shape

The biggest practical difference is that `llama-batched-bench` makes KV growth explicit, while `llama-bench` is better for isolated per-request performance.

## Practical Choice

If you are asking one of these questions, use `llama-bench`:

- How fast is this model on one CPU core?
- How fast is one request on this machine?
- How do threads, batch size, or depth affect one inference stream?

If you are asking one of these questions, use `llama-batched-bench`:

- How many concurrent sequences can I serve efficiently?
- What total throughput do I get at batch size `B`?
- How much KV cache is needed when prompts are shared or not shared?

For your current use case, the default answer is: use `llama-bench` first.
