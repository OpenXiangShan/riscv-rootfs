---
name: build-host-binaries
description: 'Build common host-side llama.cpp binaries into ./build-host/bin. Use when asked to compile llama-bench, llama-cli, llama-convert-llama2c-to-ggml, llama-quantize, llama-simple, or other native host tools in this workspace.'
argument-hint: '[target|all]'
---

# Build Host Binaries

## When to Use
- Build or rebuild host-side executables under `./build-host/bin`
- Compile `llama-bench`, `llama-cli`, `llama-convert-llama2c-to-ggml`, `llama-quantize`, or `llama-simple`
- Repair a `build-host` tree that is missing one of the expected native tools

## Procedure
1. Run commands from the workspace root.
2. Treat `./repo` as the CMake source tree and `./build-host` as the native x86_64 build directory.
3. Reconfigure `build-host` before building `llama-cli`, because that target is only added when `LLAMA_BUILD_SERVER=ON`.
4. Build either the single requested target or the standard host tool set.
5. Confirm the expected binaries exist under `./build-host/bin`.

## Important Notes
- In this workspace, the top-level `Makefile` configures `build-host` with `LLAMA_BUILD_SERVER=OFF`, so `cmake --build build-host --target llama-cli` fails until the cache is reconfigured.
- `make host-tools` only guarantees `llama-convert-llama2c-to-ggml` and `llama-quantize`; it does not cover `llama-bench`, `llama-simple`, or `llama-cli`.
- Re-running `cmake -S repo -B build-host ...` is the safe way to update the existing `build-host` cache in place.

## Output
- Host binaries in `./build-host/bin`

## References
- [Command templates](./references/commands.md)