from spack.package import *
from spack.pkg.builtin.py_typing_extensions import PyTypingExtensions as SpackPyTypingExtensions


class PyTypingExtensions(SpackPyTypingExtensions):

    version("4.2.0",
            sha256=
            "f1c24655a0da0d1b67f07e17a5e6b2a105894e6824b92096378bb3668ef02376")
