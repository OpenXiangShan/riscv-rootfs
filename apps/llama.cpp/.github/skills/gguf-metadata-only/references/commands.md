# Command Templates

Run the following commands from the workspace root.

## Generate Metadata-Only GGUF

```bash
bash ./gguf-metadata-only.sh "./models/model.gguf"
```

This produces:

```text
./models/model.gguf.om
```

## Generate Metadata-Only GGUF With An Explicit Output Path

```bash
bash ./gguf-metadata-only.sh \
  --output "./models/model-custom.gguf.om" \
  "./models/model.gguf"
```

## Common Pitfalls

- If `gguf-metadata-only.sh` complains about missing static libraries, build `build-host` first.
- Do not point normal inference tools at `.gguf.om`.
