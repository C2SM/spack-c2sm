from spack.package import *
from spack.pkg.builtin.metkit import Metkit as SpackMetkit


class Metkit(SpackMetkit):

    version("1.9.2",
            sha256=
            "35d5f67196197cc06e5c2afc6d1354981e7c85a441df79a2fbd774e0c343b0b4")
