from spack import *
from spack.pkg.builtin.Claw import Claw as SpackClaw


class Claw(SpackClaw):
    version('2.1', tag='v2.1', submodules=True)
