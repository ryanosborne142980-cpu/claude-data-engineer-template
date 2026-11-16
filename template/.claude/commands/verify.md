---
description: Run the project's checks and report honestly
---

1. Run every command in the **Verify** section of `AGENTS.md`, in order. If a command can't run (tool missing, needs a live environment), record it as not run instead of skipping it silently.
2. If loads or transforms changed and a dev environment is available, rerun the affected load once and confirm the row counts don't change (idempotency) and reconciliation still balances.
3. Do not fix anything yet. Report:
   - each check: **PASS**, **FAIL** (with the relevant output) or **NOT RUN** (with the reason)
   - whether anything ran against a live environment or only fixtures
   - the likely cause of each failure and a proposed fix

Ask before applying fixes.
