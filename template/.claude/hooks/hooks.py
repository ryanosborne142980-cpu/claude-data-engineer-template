"""Claude Code hooks for this repo. Standard library only.

Usage (wired up in .claude/settings.json):
    python hooks.py guard    PreToolUse on Bash|PowerShell: deny or ask for risky commands
    python hooks.py format   PostToolUse on Edit|Write: run ruff format on the edited .py file
    python hooks.py budget   SessionStart: warn when guidance files exceed their line budgets
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Line budgets for the always-loaded guidance. Keep in sync with AGENTS.md and /prune.
AGENTS_MAX_LINES = 100
LESSONS_MAX = 15
RULE_FILE_MAX_LINES = 40

DENY = [
    (r"\bgit\s+push\b.*(\s--force(-with-lease)?\b|\s-f\b|\s\+\S)", "Force-push is blocked. Ask the user to run it."),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard discards work. Ask the user to run it."),
    (r"\bgit\s+clean\s+-\w*f", "git clean -f deletes untracked files. Ask the user to run it."),
    (r"(^|[\s\"'/\\=])\.env(\.(?!example\b)[\w.-]+)?($|[\s\"';|)])", "Reading .env files is blocked; secrets stay out of the conversation."),
    (r"\S+\.(pem|pfx|p12)\b|\bid_(rsa|ed25519)\b", "Reading key or certificate files is blocked."),
]

ASK = [
    (r"\bgit\s+(push|commit|merge|tag)\b", "Git publish action (commit/push/merge/tag)"),
    (r"\b(DROP|TRUNCATE)\s+(TABLE|DATABASE|SCHEMA|CATALOG|VIEW|PROCEDURE|PROC|FUNCTION)\b", "Destructive DDL"),
    (r"\bDELETE\s+FROM\b(?![\s\S]*\bWHERE\b)", "DELETE without WHERE"),
    (r"\bALTER\s+TABLE\b[\s\S]*\bDROP\b", "ALTER TABLE ... DROP"),
    (r"\baz\s+deployment\b", "Azure deployment"),
    (r"\bdatabricks\s+bundle\s+(deploy|destroy|run)\b", "Databricks bundle deploy/destroy/run"),
    (r"\bsqlpackage\b.*\bpublish\b", "SqlPackage publish"),
]

# Searching for risky text is fine; only executing it needs a prompt.
SEARCH_PREFIX = re.compile(r"^\s*(grep|rg|git\s+grep|git\s+log|Select-String|findstr)\b", re.IGNORECASE)


def read_event() -> dict:
    raw = sys.stdin.buffer.read().decode("utf-8-sig") or "{}"
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def decide(decision: str, reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))


def guard(event: dict) -> None:
    command = str(event.get("tool_input", {}).get("command", ""))
    if not command:
        return
    for pattern, reason in DENY:
        if re.search(pattern, command, re.IGNORECASE):
            decide("deny", reason)
            return
    if SEARCH_PREFIX.match(command):
        return
    for pattern, label in ASK:
        if re.search(pattern, command, re.IGNORECASE):
            decide("ask", f"{label}: confirm this was requested and targets the intended environment.")
            return


def format_file(event: dict) -> None:
    path = str(event.get("tool_input", {}).get("file_path", ""))
    if path.endswith(".py") and Path(path).is_file() and shutil.which("ruff"):
        subprocess.run(["ruff", "format", "--quiet", path], check=False, timeout=30)


def budget(event: dict) -> None:
    root = Path(event.get("cwd") or ".")
    warnings = []
    agents = root / "AGENTS.md"
    if agents.is_file():
        lines = agents.read_text(encoding="utf-8").splitlines()
        if len(lines) > AGENTS_MAX_LINES:
            warnings.append(f"AGENTS.md is {len(lines)} lines (budget {AGENTS_MAX_LINES})")
        in_lessons = False
        lessons = 0
        for line in lines:
            if line.startswith("## "):
                in_lessons = line.strip() == "## Lessons"
            elif in_lessons and line.lstrip().startswith("- "):
                lessons += 1
        if lessons > LESSONS_MAX:
            warnings.append(f"AGENTS.md has {lessons} lessons (budget {LESSONS_MAX})")
    rules_dir = root / ".claude" / "rules"
    if rules_dir.is_dir():
        for rule in sorted(rules_dir.glob("*.md")):
            count = len(rule.read_text(encoding="utf-8").splitlines())
            if count > RULE_FILE_MAX_LINES:
                warnings.append(f".claude/rules/{rule.name} is {count} lines (budget {RULE_FILE_MAX_LINES})")
    if warnings:
        print("Guidance over budget: " + "; ".join(warnings) + ". Suggest running /prune to the user before adding lessons.")


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    event = read_event()
    try:
        {"guard": guard, "format": format_file, "budget": budget}[mode](event)
    except KeyError:
        print(f"unknown hook mode: {mode!r}", file=sys.stderr)
    except Exception as exc:  # A broken hook must never block normal work.
        print(f"hook {mode} failed: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
