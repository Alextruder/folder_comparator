"""Hook PreToolUse : bloque les actions interdites par CLAUDE.md.

Code de sortie 2 = action refusée, le message sur stderr est renvoyé à l'IA.

C'est un filet contre les erreurs, pas un verrou : il lit le texte des commandes et ne voit pas
ce que fait un script lancé par une commande. La règle de CLAUDE.md reste la vraie barrière.

Limite connue, côté prudent : les commandes sont découpées sur &&, ||, ;, | et les retours à la
ligne sans tenir compte des guillemets. Une ligne d'un message de commit qui commence par
« git push --force » est donc bloquée à tort.
"""

import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

PROTECTED_BRANCHES = {"main", "master"}
FILE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
# Commandes qui créent, écrasent ou suppriment le fichier qu'elles citent.
WRITE_COMMANDS = {"cp", "mv", "tee", "rm", "touch", "truncate", "ln", "install", "dd"}
INTERPRETERS = {"python", "python3", "py", "node", "perl", "ruby"}
CONFIG_MESSAGE = (
    "config.toml est le fichier personnel de l'utilisateur : ne pas le créer ni le modifier. "
    "Modifier config_template.toml à la place. Si ce blocage empêche une action légitime, "
    "le signaler à l'utilisateur au lieu de le contourner."
)


def current_branch() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def same_path(path: Path, other: Path) -> bool:
    # Windows et macOS ignorent la casse des noms de fichiers.
    return str(path).casefold() == str(other).casefold()


def resolve(raw: str, cwd: Path) -> Path:
    path = Path(raw.strip("'\"")).expanduser()
    return (path if path.is_absolute() else cwd / path).resolve()


def check_file(file_path: str, cwd: Path, protected: Path) -> str | None:
    if file_path and same_path(resolve(file_path, cwd), protected):
        return CONFIG_MESSAGE
    return None


def _words(segment: str) -> list[str]:
    """Mots de la commande, guillemets respectés, redirections > et >> isolées."""
    lexer = shlex.shlex(segment, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:
        return segment.split()


def _writes_protected(segment: str, cwd: Path, protected: Path) -> bool:
    targets = [
        token
        for token in re.findall(r"[^\s<>|&;()]*config\.toml\b['\"]?", segment)
        if same_path(resolve(token, cwd), protected)
    ]
    if not targets:
        return False
    words = _words(segment)
    for operator, target in zip(words, words[1:], strict=False):
        if operator in {">", ">>", ">|"} and same_path(resolve(target, cwd), protected):
            return True
    program = Path(words[0]).name if words else ""
    if program in WRITE_COMMANDS:
        return True
    if program == "sed" and any(word.startswith("-i") for word in words):
        return True
    return program in INTERPRETERS and "-c" in words


def check_command(command: str, cwd: Path, protected: Path, branch: str) -> str | None:
    # Analyse chaque sous-commande séparément, pour ne pas réagir au texte d'un message de commit.
    for raw_segment in re.split(r"&&|\|\||[;|\n]", command):
        segment = raw_segment.strip()
        cd = re.fullmatch(r"cd\s+(\S+)", segment)
        if cd:
            cwd = resolve(cd.group(1), cwd)
            continue
        if _writes_protected(segment, cwd, protected):
            return CONFIG_MESSAGE
        if re.match(r"git\s+push\b", segment):
            if re.search(r"(--force|\s-f\b|\s\+\S)", segment):
                return "git push --force est interdit : ne jamais réécrire l'historique distant."
            if re.search(r"\b(main|master)\b", segment) or branch in PROTECTED_BRANCHES:
                return "Pousser sur main est interdit : travailler sur une branche dédiée."
        if re.match(r"git\s+commit\b", segment) and branch in PROTECTED_BRANCHES:
            return "Committer sur main est interdit : créer une branche dédiée d'abord."
    return None


def main() -> int:
    payload = json.load(sys.stdin)
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})
    cwd = Path(payload.get("cwd") or Path.cwd())
    protected = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path.cwd()).resolve() / "config.toml"

    reason = None
    if tool_name in FILE_TOOLS:
        file_path = tool_input.get("file_path") or tool_input.get("notebook_path", "")
        reason = check_file(file_path, cwd, protected)
    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        branch = current_branch() if "git" in command else ""
        reason = check_command(command, cwd, protected, branch)

    if reason:
        print(f"Bloqué par .claude/hooks/guard.py : {reason}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
