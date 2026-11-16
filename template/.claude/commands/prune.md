---
description: Shrink AGENTS.md and .claude/rules back under budget without losing what matters
---

Budgets: `AGENTS.md` under 100 lines, at most 15 entries in `## Lessons`, each `.claude/rules/*.md` under 40 lines.

1. Report the current line counts and number of lessons.
2. For each line in `AGENTS.md` and `.claude/rules/`, decide:
   - **Delete**: Claude follows it by default, it's obsolete (the code or tool changed), or it duplicates another line.
   - **Merge**: several lessons share one root cause; replace them with one general rule.
   - **Move**: it only applies to one stack or file type (to `.claude/rules/`), it's a data fact (to `docs/data_contracts.md`), or it can be enforced by a hook (to `.claude/hooks/hooks.py`).
   - **Promote**: a lesson that has proved important becomes a line in the matching section above `## Lessons`.
   - **Keep**.
3. Present a table of proposed changes (line, action, reason) and **wait for approval**. Never drop a safety rule (the "Ask first" and "Secrets" sections) without explicit approval.
4. Apply the approved changes, show the diff and the new counts. Do not commit.
