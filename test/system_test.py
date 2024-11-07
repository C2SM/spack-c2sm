import pytest
from spack_commands import spack_install


def test_install_libfyaml_default():
    spack_install('libfyaml', test_root=False)


def test_install_libtorch_default():
    spack_install('libtorch', test_root=False)


@pytest.mark.parametrize("version", ['2.25.0.1', '2.19.0.7'])
def test_install_cosmo_eccodes_definitions_version(version):
    spack_install(f'cosmo-eccodes-definitions @{version}', test_root=False)


def test_install_eccodes_2_19_0():
    spack_install('eccodes @2.19.0', test_root=False)


def test_install_flexpart_ifs(version):
    spack_install('flexpart-ifs', test_root=False)


def test_install_flexpart_cosmo():
    spack_install('flexpart-cosmo @V8C4.0')


def test_install_icon_mch_2_6_6_mch2b_gcc():
    spack_install('icon-mch @icon-2.6.6-mch2b %gcc')


def test_install_icon_mch_2_6_6_mch2b_nvhpc():
    spack_install('icon-mch @icon-2.6.6-mch2b %nvhpc')


def test_install_icon_mch_conditional_dependencies():
    # +coupling triggers libfyaml, libxml2, netcdf-c
    # serialization=create triggers serialbox
    # +emvorado triggers eccodes, hdf5, zlib
    # +eccodes-definitions triggers cosmo-eccodes-definitions
    # +mpi triggers mpi
    # gpu=nvidia-80 triggers cuda

    spack_install(
        'icon-mch @icon-2.6.6-mch2b %nvhpc +coupling serialization=create +emvorado +mpi gpu=nvidia-80'
    )


def test_install_icontools():
    spack_install('icontools @2.5.2')


def test_install_int2lm_3_00_nvhpc():
    spack_install('int2lm @int2lm-3.00 %nvhpc', test_root=False)


def test_install_libgrib1_22_01_2020_nvhpc():
    spack_install('libgrib1 @22-01-2020 %nvhpc')


def test_install_makedepf90():
    spack_install('makedepf90 @3.0.1', test_root=False)


def test_install_oasis_version_4_0_nvhpc():
    spack_install('oasis @4.0 %nvhpc')


def test_install_pytorch_fortran_version_0_4():
    spack_install(
        'pytorch-fortran@0.4%nvhpc ^pytorch-fortran-proxy@0.4%gcc ^python@3.10 ^gmake%gcc ^cmake%gcc',
        test_root=False)


def test_install_pytorch_fortran_proxy_version_0_4():
    spack_install('pytorch-fortran-proxy@0.4%gcc ^python@3.10',
                  test_root=False)


def test_install_py_cytoolz_install_default():
    spack_install('py-cytoolz')


def test_install_py_devtools_install_default():
    spack_install('py-devtools')


def test_install_py_factory_boy_install_default():
    spack_install('py-factory-boy')


def test_install_py_gridtools_cpp_install_default():
    spack_install('py-gridtools-cpp')


@pytest.mark.parametrize("version", ['1.0.3.7', '1.0.3.9'])
def test_install_py_gt4py_for_version(version):
    spack_install(f'py-gt4py @{version}')


def test_install_py_icon4py():
    spack_install('py-icon4py')


def test_install_py_hatchling_default():
    spack_install('py-hatchling')


def test_install_py_inflection_default():
    spack_install('py-inflection')


def test_install_py_pytest_factoryboy_default():
    spack_install('py-pytest-factoryboy')


def test_install_py_tabulate_default():
    spack_install('py-tabulate')


def test_install_py_typing_extensions_default():
    spack_install('py-typing-extensions')


def test_install_yaxt_default():
    spack_install('yaxt')
