from spack.package import *
from spack.pkg.builtin.pyblack import PyBlack as SpackPyBlack


class PyBlack(SpackPyBlack):

    version("22.3.0",
            sha256=
            "35020b8886c022ced9282b51b5a875b6d1ab0c387b31a065b84db7c33085ca79")
