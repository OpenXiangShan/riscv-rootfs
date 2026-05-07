---
name: modelscope-download
description: 'Download full model repositories from ModelScope into ./models using the workspace virtual environment. Use when asked to download a model from ModelScope, pull a ModelScope repo locally, or prepare a full Hugging Face style model directory for later GGUF conversion.'
argument-hint: '<modelscope-repo> [local-name]'
---

# ModelScope Download

## When to Use
- Download a full model repository from ModelScope into `./models/`
- Mirror a ModelScope model locally before conversion
- Prepare tokenizer and weight files for GGUF export

## Procedure
1. Run commands from the workspace root.
2. Ensure the workspace venv contains `modelscope`. If not, install it with the Tsinghua mirror commands in [commands](./references/commands.md).
3. Download the full repository into `./models/<name>-hf`.
4. Do not restrict the download to `README.md` or any other partial file set if the next step is GGUF conversion.
5. Report the final local directory path.

## Output
- A local Hugging Face style model directory under `./models/`

## References
- [Command templates](./references/commands.md)
