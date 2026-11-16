# Data-engineering agent template

A starter kit of agent instructions, commands, and safety hooks for data-engineering repos. It follows Boris Cherny's approach: a short shared instruction file that grows from real mistakes, a way for Claude to check its own work, and hooks for anything that must be enforced. It adds firm limits on how large the guidance can grow.

## Use it

```powershell
C:\dev\claude-de-template\new-de-repo.ps1 -Target C:\dev\my-new-repo -Stack sqlserver,python
C:\dev\claude-de-template\new-de-repo.ps1 -Target C:\dev\my-new-repo -Stack all
# Existing repo: never overwrites; -Force writes <file>.template-new copies to merge by hand
C:\dev\claude-de-template\new-de-repo.ps1 -Target C:\dev\existing-repo -Stack databricks -Force
```

Stacks: `sqlserver`, `databricks`, `azure`, `python`, `all`, `none` (default `python`). Then fill in the `{{PLACEHOLDER}}` lines the script prints. The hooks need `python` on PATH; formatting also uses `ruff` if it's installed.

## How the guidance stays small

| Layer | Loaded | Budget |
|---|---|---|
| `AGENTS.md` (imported by `CLAUDE.md`) | every session | under 100 lines, at most 15 Lessons |
| `.claude/rules/<stack>.md` | only when Claude touches matching paths (`paths:` frontmatter) | under 40 lines each |
| `docs/decisions.md`, `docs/data_contracts.md` | only when read | none |
| `.claude/hooks/hooks.py` | never (it's code, not context) | none |

- `/learn` sends each lesson to the narrowest home it fits. Rules that can be enforced mechanically become hooks, stack-specific ones go to rules files, data facts go to the docs, and only rules that apply to the whole project become a one-line Lesson.
- `/prune` deletes, merges, moves, or promotes lines to get back under budget, and asks for approval first.
- A SessionStart hook warns Claude when a file is over budget, so the overrun is noticed instead of growing quietly.

## What's in a generated repo

| Path | Purpose |
|---|---|
| `AGENTS.md` | Shared rules: project facts, verify commands, what to ask before doing, how we work, data rules, secrets, Lessons |
| `CLAUDE.md` | `@AGENTS.md` plus notes for Claude Code (plan review, commands) |
| `.claude/rules/*.md` | Rules for each stack, loaded only for matching paths |
| `.claude/commands/` | `/verify`, `/grill` (adversarial review of the branch), `/commit-pr`, `/learn`, `/prune` |
| `.claude/agents/` | `plan-reviewer` (staff-level review of a plan), `git-workflow` (safe commits and PRs) |
| `.claude/hooks/hooks.py` | **guard**: denies force-push, `reset --hard`, `clean -f`, and reading `.env`/key files; asks before commit, push, merge, tag, destructive DDL, and deploys. Covers both Bash and PowerShell. **format**: runs `ruff format` on the edited `.py` file. **budget**: the size warning described above |
| `.claude/settings.json` | Hook wiring, a small allowlist, and Read deny rules |
| `.github/` | Copilot pointer and PR checklist |
| `docs/` | Decisions log and data contracts |

## Editing the template

- Edit files under `template/`. Existing repos are not updated; to pull changes into one, rerun the script with `-Force` and merge the `.template-new` files.
- To add a stack, add `template/.claude/rules/<name>.md` with `paths:` frontmatter, then add `<name>` to `ValidateSet` and `$allStacks` in `new-de-repo.ps1`.
- Budgets are defined in `hooks.py` and repeated in `AGENTS.md`, `/learn`, and `/prune`. Change all four together.
- The guard uses regex and can be fooled; it's a safety net, not a security boundary. `.claude/settings.local.json` (gitignored) is for personal permission tweaks.
