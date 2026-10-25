"""Hook Stop : empêche l'IA de rendre la main tant que le projet n'est pas vert.

Ne s'exécute que si du code a changé : modifications non commitées, ou commits pas encore poussés.
"""

import json
import subprocess
import sys

CHECKS = [
    ["ruff", "format", "--check", "."],
    ["ruff", "check", "."],
    ["mypy"],
    ["pytest", "-q"],
]
WATCHED_SUFFIXES = (".py", ".toml", ".txt")


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    return result.stdout if result.returncode == 0 else ""


def code_changed() -> bool:
    for line in git("status", "--porcelain").splitlines():
        if line.rstrip().endswith(WATCHED_SUFFIXES):
            return True
    return bool(git("log", "--oneline", "@{upstream}..HEAD").strip())


def main() -> int:
    payload = json.load(sys.stdin)
    # Deuxième passage après un blocage : on laisse la main pour éviter une boucle infinie.
    if payload.get("stop_hook_active") or not code_changed():
        return 0

    failures = []
    for check in CHECKS:
        result = subprocess.run(
            [sys.executable, "-m", *check],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            output = (result.stdout + result.stderr).strip()[-2000:]
            failures.append(f"$ {' '.join(check)}\n{output}")

    if failures:
        reason = (
            "Le projet n'est pas vert. Corriger avant de rendre la main "
            "(skill verifier) :\n\n" + "\n\n".join(failures)
        )
        print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
