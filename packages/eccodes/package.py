from spack import *
from glob import glob
from llnl.util.filesystem import LibraryList
import os
import platform
import llnl.util.tty as tty
from spack.pkg.builtin.eccodes import Eccodes as SpackEccodes

# Extend the official spack of eccodes in order to add build_shared_libs and change default of variants
class Eccodes(SpackEccodes):

    variant('build_shared_libs', default=True, description="Select the type of library built")
    variant('jp2k', default='jasper', values=('openjpeg', 'jasper', 'none'), description='Specify JPEG2000 decoding/encoding backend')
    variant('fortran', default=True, description='Enable the Fortran support')

    def cmake_args(self):
        args = super().cmake_args()

        if self.spec.variants['build_shared_libs'].value:
            args.append('-DBUILD_SHARED_LIBS=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS=OFF')

        return args

