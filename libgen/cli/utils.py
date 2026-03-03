from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Iterable


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def templates_dir() -> Path:
    return package_root() / "templates"


def render_template(name: str, **context: str) -> str:
    template_path = templates_dir() / name
    content = template_path.read_text(encoding="utf-8")
    return Template(content).safe_substitute(**context)


def list_template_names() -> list[str]:
    return sorted(path.name for path in templates_dir().iterdir() if path.is_file())


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_cmd(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=str(cwd), check=False, text=True, capture_output=True)


def is_libgen_project(project_root: Path) -> tuple[bool, str]:
    root = project_root.resolve()
    marker = root / ".libgen-project"
    if marker.exists():
        return True, ""

    module_name = root.name
    required = [
        root / "src",
        root / "bindings.cpp",
        root / "pyproject.toml",
        root / "setup.py",
        root / module_name / "__init__.py",
    ]
    missing = [str(path.relative_to(root)) for path in required if not path.exists()]
    if missing:
        return False, f"missing required files: {', '.join(missing)}"
    return True, ""


def require_libgen_project(project_root: Path) -> None:
    ok, reason = is_libgen_project(project_root)
    if ok:
        return
    root = project_root.resolve()
    raise SystemExit(
        "Invalid LibGen project: "
        f"'{root}'. This command only works inside a LibGen-generated project ({reason})."
    )


@dataclass(frozen=True)
class CppFunction:
    return_type: str
    name: str
    args: str


_FUNC_RE = re.compile(
    r"""(?mx)
    ^\s*
    (?P<rtype>[A-Za-z_][\w:\<\>\s\*&]*)
    \s+
    (?P<name>[A-Za-z_]\w*)
    \s*\(
    (?P<args>[^\)]*)
    \)
    \s*\{
    """
)


_DEF_RE = re.compile(r"m\.def\(\"([^\"]+)\"")


def discover_cpp_functions(source_text: str) -> list[CppFunction]:
    functions: list[CppFunction] = []
    for match in _FUNC_RE.finditer(source_text):
        name = match.group("name")
        if name in {"if", "for", "while", "switch"}:
            continue
        functions.append(
            CppFunction(
                return_type=" ".join(match.group("rtype").split()),
                name=name,
                args=" ".join(match.group("args").split()),
            )
        )
    return functions


def discover_bound_function_names(bindings_text: str) -> set[str]:
    return set(_DEF_RE.findall(bindings_text))


def iter_cpp_sources(src_dir: Path) -> Iterable[Path]:
    if not src_dir.exists():
        return []
    return sorted(src_dir.glob("*.cpp"))
