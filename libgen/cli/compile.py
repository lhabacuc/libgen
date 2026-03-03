from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .utils import run_cmd


def run_compile(project_root: Path, release: bool = False) -> None:
    project_root = project_root.resolve()
    module_name = project_root.name

    cmd = [sys.executable, "-m", "pip", "wheel", ".", "-w", "dist"]
    if release:
        cmd.extend(["--no-deps"])

    result = run_cmd(cmd, cwd=project_root)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit("Build failed")

    install = run_cmd([sys.executable, "-m", "pip", "install", "-e", "."], cwd=project_root)
    if install.returncode != 0:
        print(install.stdout)
        print(install.stderr)
        raise SystemExit("Build succeeded but editable install failed")

    probe = subprocess.run(
        [sys.executable, "-c", f"import {module_name}; print({module_name}.__name__)"],
        cwd=str(project_root),
        text=True,
        capture_output=True,
        check=False,
    )
    if probe.returncode != 0:
        print(probe.stdout)
        print(probe.stderr)
        raise SystemExit("Module compiled but import test failed")

    print("Build completed and import test passed")
