from __future__ import annotations

import sys
from pathlib import Path

from .utils import require_libgen_project, run_cmd


def run_install(project_root: Path) -> None:
    project_root = project_root.resolve()
    require_libgen_project(project_root)

    result = run_cmd([sys.executable, "-m", "pip", "install", "-e", "."], cwd=project_root)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit("Install failed")

    print("Install completed")
