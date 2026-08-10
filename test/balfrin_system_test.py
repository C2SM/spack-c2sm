import re

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


def test_icon_fflags_reach_fortran_compiler():
    # Regression test for `fflags="..."` set on the icon spec (e.g. via
    # spack.yaml) being silently dropped instead of reaching the Fortran
    # compiler: icon's configure_args() hardcodes FCFLAGS per compiler
    # vendor and forces FC to the MPI compiler wrapper, which bypasses
    # spack's own SPACK_FFLAGS compiler-wrapper injection. --until=configure
    # keeps this cheap: it stops right after configure, before any of
    # icon's sources are actually compiled.
    #
    # WORKAROUND: A build and link dependency should imply that the same compiler is used. ^cray-mpich%nvhpc enforces it.
    spec = 'icon @2.6.6-mch2b %nvhpc +mpi gpu=nvidia-80 fflags=-traceback ^cray-mpich%nvhpc'
    log = spack_install(spec, test_root=False, extra_args=["--until=configure"])

    content = log.read_text()
    assert re.search(r"FCFLAGS=[^\n]*-traceback", content), (
        f"-traceback missing from the FCFLAGS configure argument; see {log}")


def test_install_yaxt():
    spack_install('yaxt')


def test_install_flexpart_cosmo_icon():
    spack_install('flexpart-cosmo-icon')


def test_install_flexpart_ifs():
    spack_install('flexpart-ifs')
