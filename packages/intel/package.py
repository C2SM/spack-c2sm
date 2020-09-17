from spack import *

class Intel(IntelPackage):
    """Intel Compilers.
       Note: This package cannot be installed, it wraps existing installation, specified 
       in packages.yaml.
    """

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    # Same as in ../intel-parallel-studio/package.py, Composer Edition,
    # but the version numbering in Spack differs.
    version('19.0.1.144', sha256='none', url='http://fake-link.tgz')
    version('19.1.1.217', sha256='none', url='http://fake-link.tgz')


