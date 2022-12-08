from spack.package import *

from spack.pkg.builtin.pytoolz import PyToolz as SpackPyToolz


class PyToolz(SpackPyToolz):

    version("0.12.0",
            sha256=
            "88c570861c440ee3f2f6037c4654613228ff40c93a6c25e0eba70d17282c6194")
