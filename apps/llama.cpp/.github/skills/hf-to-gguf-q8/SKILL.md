---
name: hf-to-gguf-q8
description: 'Convert a local Hugging Face model directory to q8_0 GGUF with repo/convert_hf_to_gguf.py. Use when asked to export q8_0 GGUF, convert a local HF checkpoint to .gguf, or prepare a llama.cpp model file from an already-downloaded model directory.'
argument-hint: '<model-dir> [output-name]'
---

# HF To GGUF Q8

## When to Use
- Convert a local Hugging Face style model directory into GGUF
- Export directly to `q8_0`
- Prepare a `.gguf` file for llama.cpp inference or later `.gguf.om` generation

## Procedure
1. Run commands from the workspace root.
2. Ensure the workspace venv contains the conversion dependencies listed in [commands](./references/commands.md).
3. Use `repo/convert_hf_to_gguf.py --outtype q8_0` against the local model directory.
4. Write the output into `./models/` unless the user requested another path.
5. If the user wants a smoke test, build `llama-simple` and run a short prompt against the generated `.gguf` file.

## Important Notes
- In this workspace, `repo/convert_hf_to_gguf.py` can emit `q8_0` directly, so a separate `llama-quantize` step is not required.
- The input for this skill is a local model directory, not a ModelScope repo id.

## References
- [Command templates](./references/commands.md)
