import pytest
from spack_commands import spack_install


def test_install_py_tabulate_0_8_10():
    spack_install('py-tabulate@0.8.10')


def test_install_icon_conditional_dependencies():
    # +coupling triggers libfyaml, libxml2, netcdf-c
    # serialization=create triggers serialbox
    # +emvorado triggers eccodes, hdf5, zlib
    # +eccodes-definitions triggers cosmo-eccodes-definitions
    # +mpi triggers mpi
    # gpu=nvidia-90 triggers cuda

    # WORKAROUND: A build and link dependency should imply that the same compiler is used. ^cray-mpich%nvhpc enforces it.
    spack_install(
        'icon @2.6.6-mch2b %nvhpc +coupling +emvorado +mpi gpu=nvidia-90 ^cray-mpich%nvhpc'
    )
