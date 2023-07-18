from spack.package import *
from spack.pkg.builtin.ecbuild import Ecbuild as SpackEcbuild


class Ecbuild(SpackEcbuild):

    version('3.7.2',
            sha256=
            '7a2d192cef1e53dc5431a688b2e316251b017d25808190faed485903594a3fb9')
