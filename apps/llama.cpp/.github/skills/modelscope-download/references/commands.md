# Command Templates

Run the following commands from the workspace root.

## Install Dependencies With Tsinghua Mirror

```bash
./.venv/bin/python -m pip install \
  -i https://pypi.tuna.tsinghua.edu.cn/simple \
  -r repo/requirements/requirements-convert_hf_to_gguf.txt \
  modelscope safetensors tiktoken
```

## Download The Full Model Repository

```bash
MODEL_ID="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
MODEL_NAME="DeepSeek-R1-Distill-Qwen-1.5B"

./.venv/bin/modelscope download \
  --model "$MODEL_ID" \
  --local_dir "./models/${MODEL_NAME}-hf"
```

## Quick Check

```bash
ls -lh "./models/${MODEL_NAME}-hf"
```

## Common Pitfalls

- If `modelscope` is missing, the workspace venv is missing dependencies.
- If the user wants later conversion, do not download only `README.md`.
