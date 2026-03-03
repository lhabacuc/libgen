from __future__ import annotations

from pathlib import Path

from .utils import render_template, write_text


def run_create(name: str, destination_root: Path) -> None:
    project_root = (destination_root / name).resolve()
    if project_root.exists():
        raise SystemExit(f"Project already exists: {project_root}")

    package_dir = project_root / name
    src_dir = project_root / "src"
    tests_dir = project_root / "tests"

    write_text(src_dir / f"{name}.cpp", render_template("cpp_module.cpp", module_name=name))
    write_text(
        project_root / "bindings.cpp",
        render_template(
            "pybind11_bindings.cpp",
            module_name=name,
            declarations="int sample_add(int a, int b);",
            defs='    m.def("sample_add", &sample_add, "A sample function");\n',
        ),
    )
    write_text(package_dir / "__init__.py", f"from .{name} import *\n")
    write_text(tests_dir / "test_smoke.py", render_template("test_module.py", module_name=name, function_name="sample_add"))
    write_text(project_root / "README.md", render_template("README.md", module_name=name, function_list="- sample_add"))
    write_text(project_root / "pyproject.toml", render_template("pyproject.toml", module_name=name))
    write_text(project_root / "setup.py", render_template("setup.py", module_name=name))
    write_text(project_root / ".libgen-project", "version=1\n")

    print(f"Created project: {project_root}")
