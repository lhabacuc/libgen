from __future__ import annotations

import os
import sys
from pathlib import Path

from .utils import require_libgen_project, run_cmd


def _resolve_pypi_token() -> str | None:
    return os.getenv("PYPI_API_TOKEN") or os.getenv("TWINE_PASSWORD")


def run_push(project_root: Path, repository: str = "pypi", skip_build: bool = False) -> None:
    project_root = project_root.resolve()
    require_libgen_project(project_root)

    token = _resolve_pypi_token()
    if not token:
        raise SystemExit(
            "No PyPI credential found. Define PYPI_API_TOKEN or TWINE_PASSWORD in the environment."
        )

    if not skip_build:
        prep = run_cmd([sys.executable, "-m", "pip", "install", "--upgrade", "build", "twine"], cwd=project_root)
        if prep.returncode != 0:
            print(prep.stdout)
            print(prep.stderr)
            raise SystemExit("Failed to install build/publish tools")

        build = run_cmd([sys.executable, "-m", "build"], cwd=project_root)
        if build.returncode != 0:
            print(build.stdout)
            print(build.stderr)
            raise SystemExit("Build failed")

    dist_dir = project_root / "dist"
    artifacts = sorted(dist_dir.glob("*"))
    if not artifacts:
        raise SystemExit("No artifacts found in dist/. Run without --skip-build or build first.")

    cmd = [
        sys.executable,
        "-m",
        "twine",
        "upload",
        "--non-interactive",
        "--username",
        "__token__",
        "--password",
        token,
    ]
    if repository != "pypi":
        cmd.extend(["--repository", repository])
    cmd.extend(str(path) for path in artifacts)

    upload = run_cmd(cmd, cwd=project_root)
    if upload.returncode != 0:
        print(upload.stdout)
        print(upload.stderr)
        raise SystemExit("PyPI upload failed")

    print(f"Upload completed to '{repository}'")
