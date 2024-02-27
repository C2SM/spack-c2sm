from spack.package import *
from spack.pkg.builtin.py_setuptools import PySetuptools as SpackPySetuptools


class PySetuptools(SpackPySetuptools):
    """A Python utility that aids in the process of downloading, building,
       upgrading, installing, and uninstalling Python packages."""

    version('65.5.0',
            sha256=
            '512e5536220e38146176efb833d4a62aa726b7bbff82cfbc8ba9eaa3996e0b17')
    version('60.6.0',
            sha256=
            'eb83b1012ae6bf436901c2a2cee35d45b7260f31fd4b65fd1e50a9f99c11d7f8')
