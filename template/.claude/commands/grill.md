---
description: Adversarial data-engineering review of the branch; no SHIP IT until every issue is fixed
argument-hint: "[base branch, default main]"
---

Review the current branch as a skeptical senior data engineer whose job is to stop bad data from reaching production.

1. Find the base (`$ARGUMENTS`, else `main`) and read `git diff <base>...HEAD` and `git status` (include untracked files). Read whole changed files where the diff alone lacks context, and the relevant `docs/data_contracts.md` entries.
2. Check each area and cite evidence (file:line) for every finding:
   - **Rerun safety**: does running each load twice create duplicates or drift? Are watermarks updated only after success? What happens after a partial failure?
   - **Grain and keys**: did any table's grain change? Can joins fan out? Are business keys really unique?
   - **Data quality and reconciliation**: are bad rows quarantined, not dropped? Does source = loaded + quarantined still hold? Nulls, empty strings, and type coercion?
   - **Schema and contracts**: breaking changes to downstream consumers? Contracts and decisions docs updated?
   - **Time**: time zones, late-arriving data, SCD effective dates, boundaries (`<` vs `<=`)?
   - **Destructive or environment risk**: `DROP`/`TRUNCATE`/unbounded `DELETE`, hardcoded hosts, catalogs, or prod targets?
   - **Secrets and PII**: credentials, raw data, or personal data in code, fixtures, logs, or notebook outputs?
   - **Tests**: is new behavior tested, including the failure path and a rerun?
   - **Performance**: full scans, row-by-row work, or missing partition filters on large tables?
3. Verdict: **SHIP IT**, **NEEDS WORK**, or **BLOCK**. List issues by severity (blocker, major, minor) with file:line, what goes wrong with concrete data, and the fix.

Never give SHIP IT while a blocker or major issue remains, or when a check you needed could not be run. Do not edit files; report only. After the user fixes issues, re-review from step 1.
