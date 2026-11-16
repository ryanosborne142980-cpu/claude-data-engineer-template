---
paths:
  - "**/*.sql"
  - "**/*.sqlproj"
---

# SQL Server rules

- Objects live in SQL projects as plain `CREATE`, one object per file named after it. Use `CREATE OR ALTER` only in bootstrap, post-deployment, and ad hoc scripts.
- Run a SqlPackage deploy report before every publish; a clean report is empty.
- Load procs: `<schema>.usp_<Verb><Object>`, take `@BatchId`, log to the batch table, `TRY/CATCH` with `THROW`.
- Dynamic SQL uses `sp_executesql` with parameters; object names come from a vetted list wrapped in `QUOTENAME`.
- Server name comes from `{{SQL_SERVER_ENV_VAR}}`. `sqlcmd` against a dev instance with a self-signed certificate needs `-C`.
