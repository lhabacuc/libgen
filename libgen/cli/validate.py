from __future__ import annotations

from pathlib import Path

from .utils import discover_bound_function_names, discover_cpp_functions, iter_cpp_sources


def run_validate(project_root: Path) -> None:
    project_root = project_root.resolve()
    src_dir = project_root / "src"
    bindings_path = project_root / "bindings.cpp"

    cpp_functions: set[str] = set()
    for cpp_file in iter_cpp_sources(src_dir):
        cpp_functions.update(fn.name for fn in discover_cpp_functions(cpp_file.read_text(encoding="utf-8")))

    if not bindings_path.exists():
        raise SystemExit(f"Missing bindings file: {bindings_path}")

    bound_functions = discover_bound_function_names(bindings_path.read_text(encoding="utf-8"))

    missing = sorted(cpp_functions - bound_functions)
    extra = sorted(bound_functions - cpp_functions)

    if not missing and not extra:
        print("Validation successful: C++ and bindings are consistent")
        return

    if missing:
        print("Missing bindings for:")
        for name in missing:
            print(f"  - {name}")

    if extra:
        print("Bindings without C++ implementation:")
        for name in extra:
            print(f"  - {name}")

    raise SystemExit("Validation failed")
