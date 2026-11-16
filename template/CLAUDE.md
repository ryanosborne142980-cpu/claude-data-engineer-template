@AGENTS.md

## Claude Code

- Put project rules in `AGENTS.md`, not here, so other agents see them too.
- Start multi-step, schema-changing, or infrastructure work in plan mode. Before asking the user to approve a plan, have the `plan-reviewer` agent review it and address its blocking issues.
- Commands: `/verify` runs checks, `/grill` reviews the branch before a PR, `/commit-pr` commits and opens a PR, `/learn` records a lesson, `/prune` shrinks the guidance.
- When the user corrects you, offer to run `/learn` so the mistake is not repeated.
