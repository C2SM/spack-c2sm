import pytest
from spack_commands import spack_install


def test_install_clang_format():
    spack_install('clang-format')


def test_install_cosmo_eccodes_definitions():
    spack_install('cosmo-eccodes-definitions')


def test_install_ecbuild():
    # Tests are disabled because they fail with:
    # The following tests FAILED:
    # 	  1 - ECBUILD-359 (Failed)
    # 	  2 - ECBUILD-401 (Failed)
    # 	  8 - ECBUILD-511 (Failed)
    # 	 11 - bundle-subdir-std (Failed)
    # 	 12 - bundle-subdir-ecbfind (Failed)
    # 	 17 - test_ecbuild_find_package (Failed)
    spack_install('ecbuild @3.7.2', test_root=False)


def test_install_flexpart_cosmo():
    spack_install('flexpart-cosmo')


def test_install_flexpart_ifs():
    spack_install('flexpart-ifs')


@pytest.mark.parametrize('version',
                         ['2024.01-1', '2.6.6-mch2a', '2.6.6-mch2b'])
def test_install_icon(version):
    # WORKAROUND: A build and link dependency should imply that the same compiler is used. ^cray-mpich%nvhpc enforces it.
    spack_install(f'icon @{version} %nvhpc ^cray-mpich%nvhpc')


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


def test_install_icontools():
    spack_install(
        'icontools%gcc ~mpi fflags="-fallow-argument-mismatch" ^netcdf-fortran%gcc'
    )


def test_install_libgrib1_nvhpc():
    spack_install('libgrib1 %nvhpc')


def test_install_makedepf90():
    # Tests are disabled because they fail with:
    # test1.sh: No such file or directory
    spack_install('makedepf90', test_root=False)


def test_install_py_cytoolz():
    spack_install('py-cytoolz')


def test_install_py_devtools():
    spack_install('py-devtools')


def test_install_py_factory_boy():
    spack_install('py-factory-boy')


def test_install_py_gridtools_cpp():
    spack_install('py-gridtools-cpp')


@pytest.mark.parametrize("version", ['1.0.3.9'])
def test_install_py_gt4py_for_version(version):
    spack_install(f'py-gt4py @{version}')


# fails due to sql error
def test_build_only_py_gt4py_for_1_0_3_10():
    spack_install('py-gt4py @1.0.3.10', test_root=False)


@pytest.mark.parametrize("version, gt4py_version", [('0.0.13', '1.0.3.9'),
                                                    ('0.0.14', '1.0.3.10')])
def test_install_py_icon4py(version, gt4py_version):
    spack_install(f'py-icon4py@{version} ^py-gt4py@{gt4py_version}')


def test_install_py_hatchling():
    spack_install('py-hatchling')


def test_install_py_inflection():
    spack_install('py-inflection')


def test_install_py_pytest_factoryboy():
    spack_install('py-pytest-factoryboy')


def test_install_py_tabulate():
    spack_install('py-tabulate')


def test_install_py_typing_extensions():
    spack_install('py-typing-extensions')


def test_install_yaxt():
    spack_install('yaxt')
