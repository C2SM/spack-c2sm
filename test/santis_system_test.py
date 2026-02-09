from spack_commands import spack_install


def test_install_icon_conditional_dependencies():
    # +coupling triggers libfyaml, libxml2, netcdf-c
    # +emvorado triggers eccodes, hdf5, zlib
    # +eccodes-definitions triggers cosmo-eccodes-definitions
    # +mpi triggers mpi
    # gpu=nvidia-90 triggers cuda

    # serialization=create omitted because compilation fails

    # WORKAROUND: A build and link dependency should imply that the same compiler is used. ^cray-mpich%nvhpc enforces it.
    spack_install(
        "icon-nwp @2024.10-mch-1.0 %nvhpc +coupling +emvorado +mpi gpu=nvidia-90 ^cray-mpich%nvhpc"
    )
