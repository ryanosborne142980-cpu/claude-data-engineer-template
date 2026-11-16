---
paths:
  - "infra/**"
  - "**/*.bicep"
  - "**/*.bicepparam"
---

# Azure infrastructure rules

- All infrastructure is Bicep under `infra/`; document any manual portal change in `docs/decisions.md`.
- Run `az bicep build` and `az deployment group what-if` before deploying, and show the what-if output.
- No secrets in parameter files; use Key Vault references and managed identities.
- Naming: `{{<type>-<workload>-<env>-<region>}}`. Tags on every resource: `{{env, owner, project}}`.
- Synapse: serverless SQL for exploration; pause dedicated pools when idle.
