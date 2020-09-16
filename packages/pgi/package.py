from spack import *
from spack.pkg.builtin.pgi import Pgi as SpackPgi

class Pgi(SpackPgi):
    """PGI optimizing multi-core x64 compilers for Linux, MacOS & Windows
    with support for debugging and profiling of local MPI processes.

    Note: This package cannot be installed, it can only wrap existing installations specified 
    in packages.yaml.
    """

    version('20.1.0', sha256='none')
    version('20.1.1', sha256='none')
