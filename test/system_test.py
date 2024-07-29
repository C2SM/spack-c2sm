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


nvidia_compiler: str = {
    'daint': 'nvhpc',
    'tsa': 'pgi',
    'balfrin': 'nvhpc',
    'unknown': '',
}[machine_name()]


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


@pytest.mark.no_tsa
@pytest.mark.cosmo
def test_install_cosmo_6_0():
    spack_install(f'cosmo@6.0%nvhpc', test_root=False)


@pytest.mark.eccodes
def test_install_eccodes_2_19_0():
    spack_install('eccodes @2.19.0', test_root=False)


@pytest.mark.fckit
def test_install_and_check_fckit_0_9_0():
    spack_install('fckit@0.9.0')


@pytest.mark.fdb_fortran
def test_install_fdb_fortran():
    spack_install('fdb-fortran')


@pytest.mark.flexpart_ifs
@pytest.mark.parametrize("version", ['10.4.4', 'fdb'])
def test_install_flexpart_ifs_version(version):
    spack_install(f'flexpart-ifs @{version}', test_root=False)


@pytest.mark.no_tsa  # No one uses spack for flexpart-cosmo on Tsa
@pytest.mark.flexpart_cosmo
def test_install_flexpart_cosmo():
    spack_install('flexpart-cosmo @V8C4.0')


@pytest.mark.no_tsa  # FDB tests fail on tsa due to 'ucp_context'
@pytest.mark.fdb
def test_install_fdb_5_11_17_gcc():
    spack_install('fdb @5.11.17 %gcc')


@pytest.mark.no_tsa  # FDB tests fail on tsa due to 'ucp_context'
@pytest.mark.fdb
def test_install_fdb_5_11_17_nvhpc():
    # tests fail because compiler emitted warnings.
    spack_install(f'fdb @5.11.17 %{nvidia_compiler}', test_root=False)


@pytest.mark.no_tsa  # Icon does not run on Tsa
@pytest.mark.no_daint
@pytest.mark.icon
def test_install_icon_24_1_gcc():
    spack_install('icon @2024.1-1 %gcc')


@pytest.mark.icon
@pytest.mark.no_daint
@pytest.mark.no_tsa  # Icon does not run on Tsa
def test_install_2024_1_nvhpc():
    #WORKAROUND: ^libxml2%gcc works around a problem in the concretizer of spack v0.21.1 and /mch-environment/v6
    spack_install('icon @2024.1-1 %nvhpc ^libxml2%gcc')


@pytest.mark.no_daint  # libxml2 %nvhpc fails to build
@pytest.mark.no_tsa  # Icon does not run on Tsa
@pytest.mark.icon
def test_install_conditional_dependencies():
    # +coupling triggers libfyaml, libxml2, netcdf-c
    # +rttov triggers rttov
    # serialization=create triggers serialbox
    # +cdi-pio triggers libcdi-pio, yaxt                   (but unfortunately this is broken)
    # +emvorado triggers eccodes, hdf5, zlib
    # +eccodes-definitions triggers cosmo-eccodes-definitions
    # +mpi triggers mpi
    # gpu=openacc+cuda triggers cuda

    #WORKAROUND: ^libxml2%gcc works around a problem in the concretizer of spack v0.21.1 and /mch-environment/v6
    spack_install(
        'icon @2024.1-1 %nvhpc +coupling +rttov serialization=create +emvorado +mpi gpu=openacc+cuda ^libxml2%gcc'
    )


def icon_env_test(spack_env: str, out_of_source: bool = False):
    # avoids race conditions on the same folder
    unique_folder = 'icon_' + uuid.uuid4().hex
    subprocess.run(
        f'git clone --depth 1 --recurse-submodules -b 2024.01.1 git@github.com:C2SM/icon.git {unique_folder}',
        check=True,
        shell=True)

    if out_of_source:
        build_dir = os.path.join(unique_folder, 'build')
        os.makedirs(build_dir, exist_ok=True)
        shutil.copytree(os.path.join(unique_folder, 'config'),
                        os.path.join(build_dir, 'config'))
        unique_folder = build_dir

    log_filename = sanitized_filename(spack_env) + '_out_of_source'
    log_with_spack('spack install -n -v',
                   'system_test',
                   log_filename,
                   cwd=unique_folder,
                   env=spack_env,
                   srun=True)

    # for out-of-source build we can't run tests because required files
    # like scripts/spack/test.py or scripts/buildbot_script are not synced
    # in our spack-recipe to the build-folder
    if out_of_source:
        return

    log_with_spack('spack install --test=root -n -v',
                   'system_test',
                   log_filename,
                   cwd=unique_folder,
                   env=spack_env,
                   srun=False)


@pytest.mark.no_balfrin  # config file does not exist for this machine
@pytest.mark.no_tsa  # Icon does not run on Tsa
@pytest.mark.icon
def test_install_c2sm_test_cpu_nvhpc_out_of_source():
    icon_env_test('config/cscs/spack/v0.21.1.0/daint_cpu_nvhpc',
                  out_of_source=True)


@pytest.mark.no_balfrin  # config file does not exist for this machine
@pytest.mark.no_tsa  # Icon does not run on Tsa
@pytest.mark.icon
def test_install_c2sm_test_cpu():
    icon_env_test('config/cscs/spack/v0.21.1.0/daint_cpu_nvhpc')


@pytest.mark.no_balfrin  # config file does not exist for this machine
@pytest.mark.no_tsa  # Icon does not run on Tsa
@pytest.mark.icon
def test_install_c2sm_test_gpu():
    icon_env_test('config/cscs/spack/v0.21.1.0/daint_gpu_nvhpc')


@pytest.mark.no_tsa  # This test is flaky and sometimes fails with: icondelaunay.cpp:29:10: fatal error: version.c: No such file or directory. See issue #781.
@pytest.mark.icontools
def test_install_icontools():
    spack_install('icontools @2.5.2')


@pytest.mark.no_tsa  # Not supported on Tsa
@pytest.mark.no_balfrin  # Not supported on Balfrin
@pytest.mark.infero
def test_install_infero_tf_c():
    spack_install(
        'infero @0.1.2 %gcc +onnx +tf_c fflags="-ffree-line-length-1024"')


@pytest.mark.no_balfrin  # int2lm depends on 'libgrib1 @22-01-2020', which fails.
@pytest.mark.int2lm
def test_install_int2ml_version_3_00_gcc():
    spack_install('int2lm @int2lm-3.00 %gcc', test_root=False)


@pytest.mark.no_balfrin  # ld undefined reference to mpi_recv_
@pytest.mark.int2lm
def test_install_int2lm_version_3_00_nvhpc_fixed_definitions():
    spack_install(
        f'int2lm @int2lm-3.00 %{nvidia_compiler} ^cosmo-eccodes-definitions@2.19.0.7%{nvidia_compiler}'
    )


@pytest.mark.int2lm
def test_install_int2lm_version_3_00_nvhpc_fixed_definitions_serial():
    spack_install(
        f'int2lm @int2lm-3.00 %{nvidia_compiler} ^cosmo-eccodes-definitions@2.19.0.7%{nvidia_compiler} ~parallel',
        test_root=False)


@pytest.mark.no_tsa  # Test is too expensive. It takes over 5h.
@pytest.mark.libcdi_pio
def test_install_libcdi_pio_default():
    spack_install('libcdi-pio')


@pytest.mark.libgrib1
def test_install_libgrib1_22_01_2020_nvhpc():
    spack_install(f'libgrib1 @22-01-2020%{nvidia_compiler}')


@pytest.mark.makedepf90
def test_install_makedepf90():
    spack_install('makedepf90 @3.0.1', test_root=False)


@pytest.mark.no_balfrin  # Package is a workaround, only needed on Daint.
@pytest.mark.no_tsa  # Package is a workaround, only needed on Daint.
@pytest.mark.nvidia_blas
def test_install_default_nvidia_blas():
    spack_install('nvidia-blas')


@pytest.mark.no_balfrin  # Package is a workaround, only needed on Daint.
@pytest.mark.no_tsa  # Package is a workaround, only needed on Daint.
@pytest.mark.nvidia_lapack
def test_install_default_nvidia_lapack():
    spack_install('nvidia-lapack')


@pytest.mark.onnx_runtime
def test_install_default_onnx_runtime():
    spack_install('onnx-runtime')


@pytest.mark.no_tsa  # Coupling not needed on Tsa
@pytest.mark.oasis
def test_install_oasis_version_4_0_nvhpc():
    spack_install('oasis @4.0 %nvhpc')


@pytest.mark.no_tsa
@pytest.mark.pytorch_fortran
def test_install_pytorch_fortran_version_0_4(devirt_env):
    spack_install(
        'pytorch-fortran@0.4%nvhpc ^pytorch-fortran-proxy@0.4%gcc ^python@3.10 ^gmake%gcc ^cmake%gcc',
        test_root=False)


@pytest.mark.no_tsa
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
@pytest.mark.no_tsa  # Irrelevant
@pytest.mark.parametrize("version", ['1.0.3.3', '1.0.3.7', '1.0.3.8'])
def test_install_py_gt4py_for_version(version, devirt_env):
    spack_install(f'py-gt4py @{version}')


@pytest.mark.no_tsa  # py-isort install fails with: No module named 'poetry'.
@pytest.mark.py_icon4py
def test_install_py_icon4py_version_0_0_10(devirt_env):
    spack_install('py-icon4py @ 0.0.10 %gcc ^py-gt4py@1.0.3.3')


@pytest.mark.py_icon4py
@pytest.mark.no_tsa  # py-isort install fails with: No module named 'poetry'.
def test_install_py_icon4py_version_0_0_11(devirt_env):
    spack_install('py-icon4py @ 0.0.11 %gcc ^py-gt4py@1.0.3.7')


@pytest.mark.py_icon4py
@pytest.mark.no_tsa  # py-isort install fails with: No module named 'poetry'.
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


@pytest.mark.no_tsa  # Irrelevant
@pytest.mark.no_balfrin  #Irrelevant
@pytest.mark.rttov
@pytest.mark.parametrize("compiler", ['gcc', 'nvhpc'])
def test_install_rttov(compiler):
    spack_install(f'rttov @13.1 %{compiler}')


@pytest.mark.no_tsa  # Fails with "C compiler cannot create executables"
@pytest.mark.scales_ppm
def test_install_default():
    spack_install('scales-ppm')


@pytest.mark.tensorflowc
def test_install_2_6_0():
    spack_install('tensorflowc @2.6.0')


@pytest.mark.no_tsa  # Fails with "C compiler cannot create executables"
@pytest.mark.yaxt
def test_install_yaxt_default():
    spack_install('yaxt')
