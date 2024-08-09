from spack.package import *

from spack.pkg.builtin.eccodes import Eccodes as SpackEccodes


class Eccodes(SpackEccodes):

    version('2.19.0',
            sha256=
            'a1d080aed1b17a9d4e3aecccc5a328c057830cd4d54f451f5498b80b24c46404')
