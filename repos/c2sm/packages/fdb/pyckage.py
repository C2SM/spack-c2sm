from spack.package import *
from spack.pkg.builtin.fdb import Fdb as SpackFdb


class Fdb(SpackFdb):

    version("5.10.8", sha256="6a0db8f98e13c035098dd6ea2d7559f883664cbf9cba8143749539122ac46099")
