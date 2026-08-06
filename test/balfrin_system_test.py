import re

from spack_commands import spack_install


def test_icon_nwp_fflags_reach_fortran_compiler():
    # Regression test for `fflags="..."` set on the icon-nwp spec (e.g. via
    # spack.yaml) being silently dropped instead of reaching the Fortran
    # compiler: icon's set_configure_args() (upstream, in the builtin icon
    # package) hardcodes FCFLAGS per compiler vendor and forces FC to the
    # MPI compiler wrapper, which bypasses spack's own SPACK_FFLAGS
    # compiler-wrapper injection. --until=configure keeps this cheap: it
    # stops right after configure, before any of icon's sources are
    # actually compiled.
    #
    # WORKAROUND: A build and link dependency should imply that the same compiler is used. ^cray-mpich%nvhpc enforces it.
    spec = 'icon-nwp @2024.10-mch-1.0 +mpi gpu=nvidia-80 fflags="-traceback" %c,cxx,fortran=nvhpc ^cray-mpich %c,cxx,fortran=nvhpc'
    log = spack_install(spec, test_root=False, extra_args="--until=configure")

    content = log.read_text()
    assert re.search(r"FCFLAGS=[^\n]*-traceback", content), (
        f"-traceback missing from the FCFLAGS configure argument; see {log}"
    )


def test_install_icon_conditional_dependencies():
    # +coupling triggers libfyaml, libxml2, netcdf-c
    # serialization=create triggers serialbox
    # +emvorado triggers eccodes, hdf5, zlib
    # +eccodes-definitions triggers cosmo-eccodes-definitions
    # +mpi triggers mpi
    # gpu=nvidia-80 triggers cuda

    # WORKAROUND: A build and link dependency should imply that the same compiler is used. ^cray-mpich%nvhpc enforces it.
    spack_install(
        "icon-nwp @2024.10-mch-1.0 +coupling serialization=create +emvorado +mpi gpu=nvidia-80 %c,cxx,fortran=nvhpc ^cray-mpich %c,cxx,fortran=nvhpc"
    )


def test_install_yaxt():
    spack_install("yaxt")


def test_install_flexpart_cosmo_icon():
    spack_install("flexpart-cosmo-icon")


def test_install_flexpart_ifs():
    spack_install("flexpart-ifs")
