"""Hook PostToolUse : formate et corrige automatiquement chaque fichier .py modifié.

Code de sortie 2 = il reste des erreurs de lint, renvoyées à l'IA sur stderr.
"""

import json
import subprocess
import sys
from pathlib import Path


def ruff(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "ruff", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    payload = json.load(sys.stdin)
    file_path = payload.get("tool_input", {}).get("file_path", "")
    if not file_path.endswith(".py") or not Path(file_path).is_file():
        return 0

    if ruff("--version").returncode != 0:
        print("ruff est absent : pip install -r requirements-dev.txt", file=sys.stderr)
        return 0

    check = ruff("check", "--fix", file_path)
    ruff("format", file_path)
    if check.returncode != 0:
        print(f"ruff signale des erreurs dans {file_path} :\n{check.stdout}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
