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


def test_install_icon_ham():
    spack_install('icon-ham')


def test_install_icontools():
    spack_install('icontools')


def test_install_int2lm_3_00_nvhpc():
    # Tests are disabled because they fail with:
    # Error: cmake is a duplicate dependency, with conflicting dependency types
    # which stems from the package's 'test_int2lm.py'.
    spack_install('int2lm @int2lm-3.00 %nvhpc', test_root=False)


def test_install_libfyaml():
    spack_install('libfyaml')


def test_install_libgrib1_nvhpc():
    spack_install('libgrib1 %nvhpc')


def test_install_libtorch():
    spack_install('libtorch')


def test_install_makedepf90():
    # Tests are disabled because they fail with:
    # test1.sh: No such file or directory
    spack_install('makedepf90', test_root=False)


def test_install_oasis_nvhpc():
    spack_install('oasis %nvhpc')


def test_install_py_cytoolz():
    spack_install('py-cytoolz')


def test_install_py_devtools():
    spack_install('py-devtools')


def test_install_py_factory_boy():
    spack_install('py-factory-boy')


def test_install_py_gridtools_cpp():
    spack_install('py-gridtools-cpp')


@pytest.mark.parametrize("version", ['1.0.3.7', '1.0.3.9', '1.0.3.10'])
def test_install_py_gt4py_for_version(version):
    spack_install(f'py-gt4py @{version}')


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


def test_install_pytorch_fortran():
    spack_install('pytorch-fortran %nvhpc')


def test_install_pytorch_fortran_proxy():
    spack_install('pytorch-fortran-proxy')


def test_install_yaxt():
    spack_install('yaxt')
