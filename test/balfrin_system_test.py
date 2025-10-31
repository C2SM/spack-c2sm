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
        'icon @2.6.6-mch2b %nvhpc +coupling serialization=create +emvorado +mpi gpu=nvidia-80 ^cray-mpich%nvhpc'
    )


# fails due to sql error
def test_build_only_py_gt4py_for_1_0_3_10():
    spack_install('py-gt4py @1.0.3.10', test_root=False)


# fails due to sql error
def test_build_only_py_icon4py_for_0_0_14():
    spack_install('py-icon4py@ 0.0.14 ^py-gt4py @1.0.3.10', test_root=False)


def test_install_yaxt():
    spack_install('yaxt')


def test_install_flexpart_cosmo_icon():
    spack_install('flexpart-cosmo-icon')


def test_install_flexpart_ifs():
    spack_install('flexpart-ifs')
