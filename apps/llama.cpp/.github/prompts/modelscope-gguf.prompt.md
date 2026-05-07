---
name: "ModelScope GGUF"
description: "Run the workspace ModelScope download, q8_0 GGUF conversion, and metadata-only orchestration workflow using the split skills. Use for a shorter /modelscope-gguf entry."
argument-hint: "<modelscope-repo | model.gguf> [local-name]"
agent: "agent"
---

Use these workspace skills:
- [ModelScope Download](../skills/modelscope-download/SKILL.md)
- [HF To GGUF Q8](../skills/hf-to-gguf-q8/SKILL.md)
- [GGUF Metadata Only](../skills/gguf-metadata-only/SKILL.md)

Interpret the text I provide after this prompt as:
- either a ModelScope model id with an optional local model name override
- or an existing `.gguf` path that should be converted to `.gguf.om`

Execute the workflow from the workspace root:
1. If the input is an existing `.gguf`, use the metadata-only skill path only.
2. Otherwise, treat the input as a ModelScope model id and use the download skill, then the q8 GGUF conversion skill, then the metadata-only skill.
3. If a host smoke test is practical and a real `.gguf` file is available, build `llama-simple` if needed and run a short inference against that `.gguf` file.

Report back with:
- which workflow path was used
- the downloaded directory path, if one was created
- the source `.gguf` path
- the generated `.gguf.om` path
- the generated `.gguf` path, if one was created in this run
- whether inference validation was run and the key result

If neither a model id nor a `.gguf` path is provided, ask only for that missing value.