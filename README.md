# LibGen CLI

LibGen is a CLI that scaffolds and maintains Python bindings for C++ modules using `pybind11`.

## Features

- `libgen create <name>`: create a Python + C++ project skeleton.
- `libgen update <path>`: regenerate `bindings.cpp`, `__init__.py`, README and basic tests from C++ sources.
- `libgen validate <path>`: validate that discovered C++ functions match exported bindings.
- `libgen compile <path> --release`: build wheel and verify Python import.
- `libgen list-templates`: show embedded templates.

## Installation

```bash
pip install sflibgen
```

## Usage

```bash
libgen create mylib
libgen update mylib
libgen validate mylib
libgen compile mylib --release
```

## PyPI Publishing (GitHub Actions)

This repository includes a workflow at `.github/workflows/publish.yml` that publishes to PyPI when a GitHub release is published.

Required setup on GitHub/PyPI:

1. In PyPI, create a Trusted Publisher for this repository.
2. In GitHub, ensure `main`/`pypi` branch protections and release permissions are configured.
3. Create a release in GitHub; the workflow builds and uploads `sdist` + `wheel` to PyPI.
