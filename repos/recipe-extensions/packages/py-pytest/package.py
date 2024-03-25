from spack.package import *
from spack.pkg.builtin.py_pytest import PyPytest as SpackPyPytest


class PyPytest(SpackPyPytest):
    """pytest: simple powerful testing with Python."""

    version('7.0.0',
            sha256=
            'dad48ffda394e5ad9aa3b7d7ddf339ed502e5e365b1350e0af65f4a602344b11')
