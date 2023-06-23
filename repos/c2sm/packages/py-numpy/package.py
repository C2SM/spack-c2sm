from spack.package import *
from spack.pkg.builtin.py_numpy import PyNumpy as SpackPyNumpy


class PyNumpy(SpackPyNumpy):
    """NumPy is the fundamental package for scientific computing with Python.
    It contains among other things: a powerful N-dimensional array object,
    sophisticated (broadcasting) functions, tools for integrating C/C++ and
    Fortran code, and useful linear algebra, Fourier transform, and random
    number capabilities"""

    version('1.24.2',
            sha256=
            '003a9f530e880cb2cd177cba1af7220b9aa42def9c4afc2a2fc3ee6be7eb2b22')

    conflicts("python@3.10.1", when="@1.24.2")  # metadata generation fails.

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/n/numpy/numpy-{}.{}"
        if version >= Version("1.23"):
            ext = "tar.gz"
        else:
            ext = "zip"
        return url.format(version, ext)
