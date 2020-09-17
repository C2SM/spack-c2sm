from spack import *
from spack.util.prefix import Prefix
import os

class Pgi(Package):
    """PGI optimizing multi-core x64 compilers for Linux, MacOS & Windows
    with support for debugging and profiling of local MPI processes.

    Note: This package cannot be installed, it wraps existing installation, specified 
    in packages.yaml.
    """
    homepage = "http://www.pgroup.com/"

    version('20.1', sha256='none', url='http://fake-link.tgz')
    version('19.9', sha256='none', url='http://fake-link.tgz')


