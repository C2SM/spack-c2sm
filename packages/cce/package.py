from spack import *


class Cce(Package):
    """Cray compiler

    Note: This package cannot be installed, it wraps existing installation, specified 
    in packages.yaml.
    """

    version('10.0.2', sha256='none', url='http://fake-link.tgz')

