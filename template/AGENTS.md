# Agent guidance

{{PROJECT_ONE_LINE_PURPOSE}}

Single source of truth for every agent (Claude Code, Copilot, others). Budget: this file stays under 100 lines.

## Project facts

- **Sources:** {{SOURCE_SYSTEMS_AND_FORMATS}}
- **Platform:** {{e.g. SQL Server 2025 / Databricks Unity Catalog / Azure Synapse}}
- **Environments:** {{dev / test / prod}}. Agents work in **{{dev}}** only unless told otherwise.
- **Hard constraints:** {{in/out of scope, e.g. "pure T-SQL transforms, no dbt"}}
- **Layout:** {{src/ Python, sql/<layer>/ SQL, tests/, infra/, docs/}}
- **Raw data:** `{{raw_files/}}` (never committed). Test fixtures: `tests/fixtures/` (small, sanitized).

## Verify

Run these to check work. Do not report success for a check that was not run.

```
{{python -m pytest}}
{{ruff check .}}
```

Say whether a change was validated against a live environment or only with fixtures.

## Ask first

Get an explicit request in the current conversation before you:
- commit, push, open or merge a PR, tag, or delete a branch (preparing a PR is not permission to merge it)
- run destructive DDL (`DROP`, `TRUNCATE`, unbounded `DELETE`, dropping columns) or write outside dev
- deploy anything (bundles, Bicep, SqlPackage)

Never force-push `main` or rewrite published history. Check `git status` before editing, and never discard or stash the user's changes.

## How we work

- Build one module or layer at a time, then stop for review.
- Ask, do not guess, on grain, keys, SCD type, dedup rules, and business definitions.
- Explain non-obvious design choices in a sentence or two.
- Record decisions in `docs/decisions.md`. Record table grain, keys, and load pattern in `docs/data_contracts.md`.

## Data rules

- Loads are idempotent: rerunning gives the same result with no duplicates. Stamp rows with `batch_id` and `loaded_at`.
- Raw/bronze keeps data as received. Conform in silver; business logic in gold.
- Failing rows go to quarantine with the rule and batch ID, never silently dropped. Reconcile: source = loaded + quarantined.
- Never present inferred or derived values as source facts; keep an inference flag and method.
- Schema changes are additive by default; breaking changes need a decision record.
- Timestamps are UTC unless a contract says otherwise.

## Secrets and private data

- Credentials come only from environment variables or a secret store, never config files, notebooks, or code.
- No PII in fixtures, logs, or responses.
- If you find a secret, stop any commit or push and name the file without repeating the value.

## Area rules

Rules for a specific stack or file type live in `.claude/rules/`. Claude Code loads them automatically; other agents should read the matching file before editing that area.

## Lessons

<!-- One line per lesson: imperative rule + short reason. Max 15. Add with /learn, consolidate with /prune. -->
