import os

from Cython.Build import cythonize
from setuptools import Extension


def build(setup_kwargs: dict):
    cython_dir = os.path.join("trie_again", "_ext")
    extension = Extension(
        "trie_again.cytrie",
        [
            os.path.join(cython_dir, "cytrie.pyx"),
        ],
        extra_compile_args=["-march=native", "-O3"],
    )

    ext_modules = cythonize([extension], include_path=[cython_dir])
    setup_kwargs.update(ext_modules=ext_modules)
