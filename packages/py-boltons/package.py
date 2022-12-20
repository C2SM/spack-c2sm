from spack.package import *
from spack.pkg.builtin.py_boltons import PyBoltons as SpackPyBoltons


class PyBoltons(SpackPyBoltons):
    """Functionality that should be in the standard library. 
    Like builtins, but Boltons."""

    version('21.0.0',
            sha256=
            '65e70a79a731a7fe6e98592ecfb5ccf2115873d01dbc576079874629e5c90f13')
