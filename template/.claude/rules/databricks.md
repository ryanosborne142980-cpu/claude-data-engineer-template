---
paths:
  - "databricks.yml"
  - "resources/**"
  - "notebooks/**"
  - "**/*.ipynb"
---

# Databricks rules

- Use three-part names (`catalog.schema.table`). Catalog per environment: `{{dev_catalog / prod_catalog}}`.
- Deploy with bundles: `databricks bundle validate`, then deploy to the `dev` target only unless told otherwise.
- Never pick a CLI profile automatically; pass `--profile <name>` chosen by the user.
- Prefer serverless; say why if a workload needs classic compute.
- Upserts use Delta `MERGE`. No hardcoded workspace URLs, tokens, or storage keys.
- Clear notebook outputs before committing.
