from __future__ import annotations

import argparse
from pathlib import Path

from .cli.compile import run_compile
from .cli.create import run_create
from .cli.update import run_update
from .cli.validate import run_validate
from .cli.utils import list_template_names


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="libgen",
        description="Generate and maintain Python bindings for C++ projects.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a new C++/Python project")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("--dir", default=".", help="Destination directory")

    update_parser = subparsers.add_parser("update", help="Update bindings and support files")
    update_parser.add_argument("project_path", help="Path to the project root")

    compile_parser = subparsers.add_parser("compile", help="Compile the Python extension")
    compile_parser.add_argument("project_path", help="Path to the project root")
    compile_parser.add_argument("--release", action="store_true", help="Build in release mode")

    validate_parser = subparsers.add_parser("validate", help="Validate binding consistency")
    validate_parser.add_argument("project_path", help="Path to the project root")

    subparsers.add_parser("list-templates", help="List available templates")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "create":
        run_create(args.name, Path(args.dir))
    elif args.command == "update":
        run_update(Path(args.project_path))
    elif args.command == "compile":
        run_compile(Path(args.project_path), release=args.release)
    elif args.command == "validate":
        run_validate(Path(args.project_path))
    elif args.command == "list-templates":
        for template_name in list_template_names():
            print(template_name)


if __name__ == "__main__":
    main()
