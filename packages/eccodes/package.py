from spack import *
from glob import glob
from llnl.util.filesystem import LibraryList
import os
import platform
import llnl.util.tty as tty
from spack.pkg.builtin.eccodes import Eccodes as SpackEccodes

# Extend the official spack of eccodes in order to add build_shared_libs and change default of variants
class Eccodes(SpackEccodes):

    version('2.21.0', sha256='da0a0bf184bb436052e3eae582defafecdb7c08cdaab7216780476e49b509755')
    version('2.20.0', sha256='207a3d7966e75d85920569b55a19824673e8cd0b50db4c4dac2d3d52eacd7985')
    version('2.19.1', sha256='9964bed5058e873d514bd4920951122a95963128b12f55aa199d9afbafdd5d4b')
    version('2.19.0', sha256='a1d080aed1b17a9d4e3aecccc5a328c057830cd4d54f451f5498b80b24c46404')
    version('2.18.0', sha256='d88943df0f246843a1a062796edbf709ef911de7269648eef864be259e9704e3')
    version('2.13.0', sha256='c5ce1183b5257929fc1f1c8496239e52650707cfab24f4e0e1f1a471135b8272')
    version('2.5.0', sha256='18ab44bc444168fd324d07f7dea94f89e056f5c5cd973e818c8783f952702e4e')
    version('2.2.0', sha256='1a4112196497b8421480e2a0a1164071221e467853486577c4f07627a702f4c3')

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

