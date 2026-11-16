---
description: Record a lesson in the narrowest place it fits, without bloating AGENTS.md
argument-hint: "<what went wrong or what to remember>"
---

Lesson: $ARGUMENTS

If no lesson was given, use the most recent correction the user made in this conversation.

**1. Is it worth keeping?** Skip it, and say so, if it was a one-off, if Claude would do it right by default, or if it's already covered. If it's covered but was ignored, sharpen the existing line instead of adding a new one.

**2. Pick the narrowest home**, first match wins:

| If the lesson... | Put it in |
|---|---|
| can be enforced mechanically (a command pattern, formatting, a file that must not be read) | `.claude/hooks/hooks.py` or `.claude/settings.json`, not prose |
| applies to one stack or file type | the matching `.claude/rules/*.md` (create one with `paths:` frontmatter if none fits) |
| is a fact about the data (grain, a quirk, a key) | `docs/data_contracts.md` |
| is a design choice with trade-offs | `docs/decisions.md` |
| applies to all of the user's repos | `~/.claude/CLAUDE.md`: propose the line and ask first, since it's outside this repo |
| is a project-wide rule | one line in `## Lessons` in `AGENTS.md` |

**3. Write it tight**: one line, imperative, with the reason in a few words. Example: `- Pad bank codes to 3 digits in silver, not bronze (bronze stays as received).`

**4. Respect the budget.** `AGENTS.md` under 100 lines, at most 15 lessons, each rules file under 40 lines. If the addition would exceed a budget, run the `/prune` steps first.

**5. Show the diff** and name the file you chose and why. Do not commit.
