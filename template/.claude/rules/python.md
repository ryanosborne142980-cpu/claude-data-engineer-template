---
paths:
  - "**/*.py"
  - "pyproject.toml"
---

# Python rules

- Read config through the single config module; secrets come from environment variables.
- Load data in bulk (`BULK INSERT`, `COPY INTO`, Spark writes), never row by row.
- Pipeline code logs with `logging`, not `print`, and exits non-zero on failure.
- Run scripts that read downloaded files with `python -I`, from a separate directory.
- Say why before adding a dependency.
