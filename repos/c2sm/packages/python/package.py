from spack.pkg.builtin.python import Python as SpackPython


class Python(SpackPython):
    variant("ssl", default=False, description="Build ssl module")
