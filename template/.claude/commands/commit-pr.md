---
description: Verify, commit on a feature branch, push, and open a PR (never merges)
argument-hint: "[optional PR title or scope]"
---

Running this command is the user's explicit request to commit, push the current feature branch, and open a pull request. It is **not** permission to merge, tag, or push to `main`.

Use the `git-workflow` agent and follow its rules. Steps:

1. Check `git status --short --branch`. If on `main`, create a `type/short-description` branch first.
2. Run `/verify`. Stop if any check fails.
3. Review staged, unstaged, and untracked files separately. Stage only files in scope, by name (no `git add -A`). Stop if anything looks like a secret, raw data, or PII.
4. Commit with a Conventional Commit message.
5. Push with `-u origin <branch>`.
6. Open the PR with `gh pr create`, filling in `.github/pull_request_template.md`. $ARGUMENTS
7. Report the PR URL, the checks run, and anything not verified.
