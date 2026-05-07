# Command Templates

Run the following commands from the workspace root.

## Reconfigure `build-host` With `llama-cli` Enabled

```bash
cmake -S repo -B build-host -DLLAMA_BUILD_SERVER=ON
```

Use this before building `llama-cli`, or anytime the existing `build-host/CMakeCache.txt` still has `LLAMA_BUILD_SERVER=OFF`.

## Build The Standard Host Binary Set

```bash
cmake --build build-host \
  --target llama-bench llama-cli llama-convert-llama2c-to-ggml llama-quantize llama-simple \
  -j"$(nproc)"
```

This produces the common host binaries currently expected under `./build-host/bin`.

## Build A Single Host Target

```bash
cmake --build build-host --target llama-cli -j"$(nproc)"
cmake --build build-host --target llama-bench -j"$(nproc)"
cmake --build build-host --target llama-simple -j"$(nproc)"
cmake --build build-host --target llama-convert-llama2c-to-ggml -j"$(nproc)"
cmake --build build-host --target llama-quantize -j"$(nproc)"
```

## Verify The Outputs

```bash
ls -lh build-host/bin/llama-bench \
  build-host/bin/llama-cli \
  build-host/bin/llama-convert-llama2c-to-ggml \
  build-host/bin/llama-quantize \
  build-host/bin/llama-simple
```

## Common Pitfalls

- If `gmake: *** No rule to make target 'llama-cli'. Stop.` appears, re-run the `cmake -S repo -B build-host -DLLAMA_BUILD_SERVER=ON` configure step first.
- If you only run `make host-tools`, you will not get `llama-bench`, `llama-simple`, or `llama-cli`.
- Build commands here are for the native host directory `./build-host`, not the cross-compiled `./build-riscv` tree.