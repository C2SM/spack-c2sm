import pytest
import subprocess
import sys
import os
import uuid
import shutil
import inspect

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, log_with_spack, sanitized_filename


@pytest.fixture(scope='function')
def devirt_env():
    # pytest is run from a virtual environment that breaks the
    # Python environment setup by Spack. Additionally "deactivate"
    # is not available here, therefore we manually unset
    # VIRTUAL_ENV and PATH

    # Remove 'VIRTUAL_ENV/bin'
    try:
        virtual_env_bin = os.path.join(os.environ['VIRTUAL_ENV'], 'bin')
        os.environ.pop('VIRTUAL_ENV')
        os.environ['PATH'] = os.environ['PATH'].replace(virtual_env_bin, '')

    # happens if test are run in serial-mode because cannot unset var twice
    except KeyError:
        pass


def compose_logfilename(spec):
    func_name = inspect.currentframe().f_back.f_back.f_code.co_name.replace(
        'test_', '')
    return sanitized_filename(func_name + '-' + spec)


def spack_install(spec: str, test_root: bool = True):
    """
    Tests 'spack install' of the given spec and writes the output into the log file.
    """

    log_filename = compose_logfilename(spec)

    # A spec at the top of a log helps debugging.
    log_with_spack(f'spack spec {spec}',
                   'system_test',
                   log_filename,
                   srun=False)

    test_arg = "--test=root" if test_root else ""
    log_with_spack(f'spack install -n -v {test_arg} {spec}',
                   'system_test',
                   log_filename,
                   srun=not spec.startswith('icon '))


@pytest.mark.libfyaml
def test_install_libfyaml_default():
    spack_install('libfyaml', test_root=False)


@pytest.mark.libtorch
def test_install_libtorch_default():
    spack_install('libtorch', test_root=False)


@pytest.mark.cosmo_eccodes_definitions
@pytest.mark.parametrize("version", ['2.25.0.1', '2.19.0.7'])
def test_install_cosmo_eccodes_definitions_version(version):
    spack_install(f'cosmo-eccodes-definitions @{version}', test_root=False)


@pytest.mark.cosmo
def test_install_cosmo_6_0():
    spack_install('cosmo@6.0%nvhpc', test_root=False)


@pytest.mark.eccodes
def test_install_eccodes_2_19_0():
    spack_install('eccodes @2.19.0', test_root=False)


@pytest.mark.fdb_fortran
def test_install_fdb_fortran():
    spack_install('fdb-fortran')


@pytest.mark.flexpart_ifs
@pytest.mark.parametrize("version", ['10.4.4', 'fdb'])
def test_install_flexpart_ifs_version(version):
    spack_install(f'flexpart-ifs @{version}', test_root=False)


@pytest.mark.flexpart_cosmo
def test_install_flexpart_cosmo():
    spack_install('flexpart-cosmo @V8C4.0')


@pytest.mark.fdb
def test_install_fdb_5_11_17_gcc():
    spack_install('fdb @5.11.17 %gcc')


@pytest.mark.fdb
def test_install_fdb_5_11_17_nvhpc():
    # tests fail because compiler emitted warnings.
    spack_install('fdb @5.11.17 %nvhpc', test_root=False)


@pytest.mark.icon
def test_install_icon_24_1_gcc():
    spack_install('icon @2024.1-1 %gcc')


@pytest.mark.icon
def test_install_2024_1_nvhpc():
    spack_install('icon @2024.1-1 %nvhpc')


@pytest.mark.icon
def test_install_conditional_dependencies():
    # +coupling triggers libfyaml, libxml2, netcdf-c
    # serialization=create triggers serialbox
    # +cdi-pio triggers libcdi-pio, yaxt                   (but unfortunately this is broken)
    # +emvorado triggers eccodes, hdf5, zlib
    # +eccodes-definitions triggers cosmo-eccodes-definitions
    # +mpi triggers mpi
    # gpu=openacc+cuda triggers cuda

    spack_install(
        'icon @2024.1-1 %nvhpc +coupling serialization=create +emvorado +mpi gpu=openacc+cuda cuda_arch=80'
    )


@pytest.mark.icontools
def test_install_icontools():
    spack_install('icontools @2.5.2')


@pytest.mark.no_balfrin  # int2lm depends on 'libgrib1 @22-01-2020', which fails.
@pytest.mark.int2lm
def test_install_int2ml_version_3_00_gcc():
    spack_install('int2lm @int2lm-3.00 %gcc', test_root=False)


@pytest.mark.int2lm
def test_install_int2lm_version_3_00_nvhpc_fixed_definitions():
    spack_install(
        'int2lm @int2lm-3.00 %nvhpc ^cosmo-eccodes-definitions@2.19.0.7%nvhpc',
        test_root='balfrin' not in machine_name())


@pytest.mark.libcdi_pio
def test_install_libcdi_pio_default():
    spack_install('libcdi-pio')


@pytest.mark.libgrib1
def test_install_libgrib1_22_01_2020_nvhpc():
    spack_install('libgrib1 @22-01-2020%nvhpc')


@pytest.mark.makedepf90
def test_install_makedepf90():
    spack_install('makedepf90 @3.0.1', test_root=False)


@pytest.mark.oasis
def test_install_oasis_version_4_0_nvhpc():
    spack_install('oasis @4.0 %nvhpc')


@pytest.mark.pytorch_fortran
def test_install_pytorch_fortran_version_0_4(devirt_env):
    spack_install(
        'pytorch-fortran@0.4%nvhpc ^pytorch-fortran-proxy@0.4%gcc ^python@3.10 ^gmake%gcc ^cmake%gcc',
        test_root=False)


@pytest.mark.pytorch_fortran_proxy
def test_install_pytorch_fortran_proxy_version_0_4(devirt_env):
    spack_install('pytorch-fortran-proxy@0.4%gcc ^python@3.10',
                  test_root=False)


@pytest.mark.py_cytoolz
def test_py_cytoolz_install_default(devirt_env):
    spack_install('py-cytoolz')


@pytest.mark.py_devtools
def test_py_devtools_install_default(devirt_env):
    spack_install('py-devtools')


@pytest.mark.py_factory_boy
def test_py_factory_boy_install_default(devirt_env):
    spack_install('py-factory-boy')


@pytest.mark.py_frozendict
def test_py_frozendict_install_default(devirt_env):
    spack_install('py-frozendict')


@pytest.mark.py_gridtools_cpp
def test_py_gridtools_cpp_install_default(devirt_env):
    spack_install('py-gridtools-cpp')


@pytest.mark.py_gt4py
@pytest.mark.parametrize("version", ['1.0.3.3', '1.0.3.7', '1.0.3.8'])
def test_install_py_gt4py_for_version(version, devirt_env):
    spack_install(f'py-gt4py @{version}')


@pytest.mark.py_icon4py
def test_install_py_icon4py_version_0_0_10(devirt_env):
    spack_install('py-icon4py @ 0.0.10 %gcc ^py-gt4py@1.0.3.3')


@pytest.mark.py_icon4py
def test_install_py_icon4py_version_0_0_11(devirt_env):
    spack_install('py-icon4py @ 0.0.11 %gcc ^py-gt4py@1.0.3.7')


@pytest.mark.py_icon4py
def test_install_py_icon4py_version_0_0_12(devirt_env):
    spack_install('py-icon4py @ 0.0.12 %gcc ^py-gt4py@1.0.3.8')


@pytest.mark.py_hatchling
def test_install_py_hatchling_default(devirt_env):
    spack_install('py-hatchling')


@pytest.mark.py_inflection
def test_install_py_inflection_default(devirt_env):
    spack_install('py-inflection')


@pytest.mark.py_pytest_factoryboy
def test_install_py_pytest_factoryboy_default(devirt_env):
    spack_install('py-pytest-factoryboy')


@pytest.mark.py_tabulate
def test_install_py_tabulate_default(devirt_env):
    spack_install('py-tabulate')


@pytest.mark.py_typing_extensions
def test_install_py_typing_extensions_default(devirt_env):
    spack_install('py-typing-extensions')


@pytest.mark.scales_ppm
def test_install_default():
    spack_install('scales-ppm')


@pytest.mark.yaxt
def test_install_yaxt_default():
    spack_install('yaxt')
