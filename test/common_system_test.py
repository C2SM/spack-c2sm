import pytest
from spack_commands import spack_install


def test_install_clang_format():
    spack_install("clang-format")


def test_install_cosmo_eccodes_definitions():
    spack_install("cosmo-eccodes-definitions")


def test_install_ecbuild():
    # Tests are disabled because they fail with:
    # The following tests FAILED:
    # 	  1 - ECBUILD-359 (Failed)
    # 	  2 - ECBUILD-401 (Failed)
    # 	  8 - ECBUILD-511 (Failed)
    # 	 11 - bundle-subdir-std (Failed)
    # 	 12 - bundle-subdir-ecbfind (Failed)
    # 	 17 - test_ecbuild_find_package (Failed)
    spack_install("ecbuild @3.7.2", test_root=False)


def test_install_makedepf90():
    # Tests are disabled because they fail with:
    # test1.sh: No such file or directory
    spack_install("makedepf90", test_root=False)


@pytest.mark.parametrize("version", ["2024.10", "2024.10-mch-1.0", "2.6.6-mch2b"])
def test_install_icon(version):
    # WORKAROUND: A build and link dependency should imply that the same compiler is used. ^cray-mpich%nvhpc enforces it.
    spack_install(f"icon @{version} %nvhpc ^cray-mpich%nvhpc")


# make check of external cdi fails with
# Error: Type mismatch in argument 'size_dummy' at (1); passed INTEGER(8) to INTEGER(4) cdi_write_f2003.f90:31:37
def test_install_icontools():
    spack_install(
        "icontools @c2sm-master %gcc ~mpi ^netcdf-fortran%gcc", test_root=False
    )


def test_install_py_cytoolz():
    spack_install("py-cytoolz")


def test_install_py_devtools():
    spack_install("py-devtools")


def test_install_py_factory_boy():
    spack_install("py-factory-boy")


def test_install_py_gridtools_cpp():
    spack_install("py-gridtools-cpp")


def test_install_py_hatchling():
    spack_install("py-hatchling")


def test_install_py_inflection():
    spack_install("py-inflection")


def test_install_py_pytest_factoryboy():
    spack_install("py-pytest-factoryboy")


def test_install_py_tabulate():
    spack_install("py-tabulate")


def test_install_py_typing_extensions():
    spack_install("py-typing-extensions")
