#!/bin/sh

set -eu

runner=${LLAMA_RUNNER:-/bin/llama-simple}
model=${LLAMA_MODEL:-/root/llama-model.gguf}
prompt=${LLAMA_PROMPT:-Once}
model_set=0

usage() {
  cat <<'USAGE'
usage: llama-xsai [--model PATH] [--prompt TEXT] [MODEL.gguf] [PROMPT...]
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --model)
      model=$2
      model_set=1
      shift 2
      ;;
    --prompt)
      prompt=$2
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    *)
      break
      ;;
  esac
done

if [ "$#" -gt 0 ] && [ "$model_set" -eq 0 ] && [ -f "$1" ]; then
  model=$1
  shift
fi

if [ "$#" -gt 0 ]; then
  prompt="$*"
fi

if [ ! -f "$model" ]; then
  echo "llama-xsai: model not found: $model" >&2
  exit 1
fi

exec "$runner" -m "$model" "$prompt"
