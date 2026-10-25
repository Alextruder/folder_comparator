"""Hook SessionStart : installe les outils de développement dans les sessions cloud.

En local, l'installation se fait à la main dans un environnement virtuel (voir CLAUDE.md).
"""

import os
import subprocess
import sys


def main() -> int:
    if os.environ.get("CLAUDE_CODE_REMOTE") != "true":
        return 0
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-dev.txt"],
        check=False,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
