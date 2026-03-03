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
