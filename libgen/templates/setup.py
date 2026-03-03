from setuptools import Extension, setup
import pybind11

module_name = "$module_name"

ext_modules = [
    Extension(
        f"{module_name}.{module_name}",
        [f"src/{module_name}.cpp", "bindings.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++",
    )
]

setup(
    name=module_name,
    version="0.1.0",
    packages=[module_name],
    ext_modules=ext_modules,
)
