from spack.package import *
from spack.pkg.builtin.py_typing_extensions import PyTypingExtensions as SpackPyTypingExtensions


class PyTypingExtensions(SpackPyTypingExtensions):
    """Backported and Experimental Type Hints for Python 3.7+"""

    version("4.5.0",
            sha256=
            "5cb5f4a79139d699607b3ef622a1dedafa84e115ab0024e0d9c044a9479ca7cb")
    version("4.2.0",
            sha256=
            "f1c24655a0da0d1b67f07e17a5e6b2a105894e6824b92096378bb3668ef02376")
