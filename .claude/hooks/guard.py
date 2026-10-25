"""Hook PreToolUse : bloque les actions interdites par CLAUDE.md.

Code de sortie 2 = action refusée, le message sur stderr est renvoyé à l'IA.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

PROTECTED_BRANCHES = {"main", "master"}
FILE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def current_branch() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def check_file(file_path: str) -> str | None:
    if Path(file_path).name.lower() == "config.toml":
        return (
            "config.toml est le fichier personnel de l'utilisateur : ne pas le modifier. "
            "Modifier config_template.toml à la place."
        )
    return None


def check_command(command: str) -> str | None:
    # Analyse chaque sous-commande séparément, pour ne pas réagir au texte d'un message de commit.
    for segment in re.split(r"&&|\|\||[;|\n]", command):
        segment = segment.strip()
        if re.search(r">\s*\S*config\.toml\b", segment):
            return "Écrire dans config.toml est interdit. Modifier config_template.toml."
        if re.match(r"git\s+push\b", segment):
            if re.search(r"(--force|\s-f\b|\s\+\S)", segment):
                return "git push --force est interdit : ne jamais réécrire l'historique distant."
            if re.search(r"\b(main|master)\b", segment) or current_branch() in PROTECTED_BRANCHES:
                return "Pousser sur main est interdit : travailler sur une branche dédiée."
        if re.match(r"git\s+commit\b", segment) and current_branch() in PROTECTED_BRANCHES:
            return "Committer sur main est interdit : créer une branche dédiée d'abord."
    return None


def main() -> int:
    payload = json.load(sys.stdin)
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})

    reason = None
    if tool_name in FILE_TOOLS:
        reason = check_file(tool_input.get("file_path") or tool_input.get("notebook_path", ""))
    elif tool_name == "Bash":
        reason = check_command(tool_input.get("command", ""))

    if reason:
        print(f"Bloqué par .claude/hooks/guard.py : {reason}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
