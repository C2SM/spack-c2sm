import pytest
from spack_commands import spack_install


def test_install_icon_conditional_dependencies():
    # +coupling triggers libfyaml, libxml2, netcdf-c
    # serialization=create triggers serialbox
    # +emvorado triggers eccodes, hdf5, zlib
    # +eccodes-definitions triggers cosmo-eccodes-definitions
    # +mpi triggers mpi
    # gpu=nvidia-80 triggers cuda

    # WORKAROUND: A build and link dependency should imply that the same compiler is used. ^cray-mpich%nvhpc enforces it.
    spack_install(
        'icon @2024.10-mch-1.0 %nvhpc +coupling serialization=create +emvorado +mpi gpu=nvidia-80 ^cray-mpich%nvhpc'
    )


def test_install_yaxt():
    spack_install('yaxt')


def test_install_flexpart_cosmo_icon():
    spack_install('flexpart-cosmo-icon')


def test_install_flexpart_ifs():
    spack_install('flexpart-ifs')
