---
name: gguf-metadata-only
description: 'Generate metadata-only .gguf.om files from existing GGUF models with gguf-metadata-only.sh for llama-bench --fake-like. Use when asked to create .gguf.om, metadata-only GGUF, fake-like inputs, or convert an existing .gguf to .gguf.om in this workspace.'
argument-hint: '<model.gguf> [output-path]'
---

# GGUF Metadata Only

## When to Use
- Convert an existing `.gguf` into `.gguf.om`
- Prepare metadata-only model inputs for `llama-bench --fake-like`
- Avoid re-running ModelScope download or HF conversion when a real `.gguf` already exists

## Procedure
1. Run commands from the workspace root.
2. Ensure the input is a real `.gguf` file.
3. Run `gguf-metadata-only.sh` against that `.gguf` file.
4. Use the generated `.gguf.om` only for fake-like or metadata-only benchmarking workflows.

## Important Notes
- `.gguf.om` is not for normal inference.
- By default, the script writes `<input>.om` next to the source `.gguf`.

## References
- [Command templates](./references/commands.md)
