from spack.pkg.builtin.eccodes import Eccodes as SpackEccodes

class Eccodes(SpackEccodes):
    variant('fortran', default=True, description='Enable the Fortran support')
