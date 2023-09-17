from spack.package import *
from spack.pkg.builtin.serialbox import Serialbox as SpackSerialbox


class Serialbox(SpackSerialbox):
    """See upstream package.
    Adding version to make compatible with numpy 1.24
    """
    git = 'https://github.com/GridTools/serialbox.git'
    maintainers = ['halungge', 'skosukhin']

    version('2.6.2',
            commit='88ac4e4dfc824953d068fe63c8e7b3dd9560a914',
            git=git,
            submodules=True)
