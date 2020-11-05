# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Icon(AutotoolsPackage):
    """The ICON modelling framework is a joint project between the
    German Weather Service and the
    Max Planck Institute for Meteorology for
    developing a unified next-generation global numerical weather prediction and
    climate modelling system. The ICON model has been introduced into DWD's
    operational forecast system in January 2015."""

    homepage = 'https://software.ecmwf.int/wiki/display/GRIB/Home'
    url = 'https://gitlab.dkrz.de/icon/icon-cscs/-/archive/mc10_for_icon-2.6.x-rc/icon-cscs-mc10_for_icon-2.6.x-rc.tar.gz'
    git = 'git@gitlab.dkrz.de:icon/icon-cscs.git'

    maintainers = ['egermann']
    
    version('master', branch='master', submodules=True)
    version('2.6.x-rc', commit='040de650', submodules=True)
    version('2.0.17', commit='39ed04ad', submodules=True)
    
    depends_on('m4')
    depends_on('autoconf%gcc')
    depends_on('automake%gcc')
    depends_on('libtool%gcc')
    depends_on('jasper@1.900.1%gcc ~shared')
    depends_on('libxml2@2.9.7')
    depends_on('serialbox@2.6.0')
    depends_on('claw@2.0.1', when='+claw', type='build')
    depends_on('netcdf-c +mpi', type=('build', 'link'))
   
    variant('target', default='gpu', description='Build with target gpu or cpu', values=('gpu', 'cpu'), multi=False)
    variant('host', default='daint', description='Build on host daint', multi=False)
    variant('cuda_arch', default='none', description='Build with cuda_arch', values=('70', '60', '37'), multi=False)
    variant('claw', default=True, description='Build with claw directories enabled')

    config_args.extend(self.enable_or_disable('claw'))

    def configure_args(self):
        args = []
        return args                                   
