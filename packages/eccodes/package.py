from spack.pkg.builtin.eccodes import Eccodes as SpackEccodes


class Eccodes(SpackEccodes):
    version('2.19.0',
            sha256=
            'a1d080aed1b17a9d4e3aecccc5a328c057830cd4d54f451f5498b80b24c46404')
    version('2.14.1',
            sha256=
            '16da742691c0ac81ccc378ae3f97311ef0dfdc82505aa4c652eb773e911cc9d6')

    variant('fortran', default=True, description='Enable the Fortran support')
