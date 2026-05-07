# Command Templates

Run the following commands from the workspace root.

## Convert A Local HF Directory To q8_0 GGUF

```bash
MODEL_NAME="DeepSeek-R1-Distill-Qwen-1.5B"
PY="./.venv/bin/python"

"$PY" repo/convert_hf_to_gguf.py \
  --outtype q8_0 \
  --outfile "./models/${MODEL_NAME}-q8_0.gguf" \
  "./models/${MODEL_NAME}-hf"
```

## Build A Host Smoke-Test Runner

```bash
cmake --build build-host --target llama-simple -j4
```

## Run A Short Inference Check

```bash
./build-host/bin/llama-simple \
  -m "./models/${MODEL_NAME}-q8_0.gguf" \
  -n 32 \
  "你好，请用一句话介绍你自己。"
```

## Quick Checks

```bash
ls -lh "./models/${MODEL_NAME}-q8_0.gguf"
```

## Common Pitfalls

- If the input path is only a partial download, conversion will fail because tokenizer or weight files are missing.
- If the user wants only `.gguf.om`, conversion may be unnecessary if a real `.gguf` already exists.
