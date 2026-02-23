from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "fast_search",
        ["fast_search.cpp"],
        # Example: passing in the version to the compiled module
        define_macros=[('VERSION_INFO', '"0.1"')],
    ),
]

setup(
    name="fast_search",
    version="0.1",
    author="Jules",
    author_email="jules@example.com",
    description="A fast C++ search backend for Media Stats Viewer",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.7",
)
