from spack.package import *
from spack.pkg.builtin.pyboltons import PyBoltons as SpackPyBoltons


class PyBoltons(SpackPyBoltons):

    version('21.0.0',
            sha256=
            '65e70a79a731a7fe6e98592ecfb5ccf2115873d01dbc576079874629e5c90f13')
