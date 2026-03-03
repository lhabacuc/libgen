from __future__ import annotations

from pathlib import Path

from .utils import (
    discover_cpp_functions,
    iter_cpp_sources,
    render_template,
    require_libgen_project,
    write_text,
)


def run_update(project_root: Path) -> None:
    project_root = project_root.resolve()
    require_libgen_project(project_root)
    module_name = project_root.name
    src_dir = project_root / "src"

    functions = []
    for cpp_file in iter_cpp_sources(src_dir):
        functions.extend(discover_cpp_functions(cpp_file.read_text(encoding="utf-8")))

    unique_functions = []
    seen = set()
    for fn in functions:
        if fn.name in seen:
            continue
        seen.add(fn.name)
        unique_functions.append(fn)

    declarations = "\n".join(f"{fn.return_type} {fn.name}({fn.args});" for fn in unique_functions)
    defs = "".join(f'    m.def("{fn.name}", &{fn.name});\n' for fn in unique_functions)
    function_list = "\n".join(f"- {fn.name}" for fn in unique_functions) or "- (none found)"

    write_text(
        project_root / "bindings.cpp",
        render_template(
            "pybind11_bindings.cpp",
            module_name=module_name,
            declarations=declarations,
            defs=defs,
        ),
    )
    write_text(project_root / module_name / "__init__.py", f"from .{module_name} import *\n")
    write_text(project_root / "README.md", render_template("README.md", module_name=module_name, function_list=function_list))

    tests_body = "".join(
        f"def test_{fn.name}_exists():\n    assert hasattr({module_name}, \"{fn.name}\")\n\n"
        for fn in unique_functions
    )
    test_content = render_template("test_module.py", module_name=module_name, function_name="")
    test_content = test_content.replace("# AUTO_TESTS\n", tests_body)
    write_text(project_root / "tests" / "test_generated.py", test_content)

    print(f"Updated bindings for module '{module_name}' with {len(unique_functions)} functions")
