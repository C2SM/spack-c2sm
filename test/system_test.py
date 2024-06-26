import unittest
import pytest
import subprocess
import sys
import os
import uuid
import shutil
from pathlib import Path
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


def compose_logfilename(spec, log_filename: str = None):
    func_name = inspect.currentframe().f_back.f_back.f_code.co_name.replace(
        'test_', '')
    if log_filename is None:
        log_filename = sanitized_filename(func_name + '-' + spec)
    return log_filename


def spack_install(spec: str, log_filename: str = None):
    """
    Tests 'spack install' of the given spec and writes the output into the log file.
    """

    log_filename = compose_logfilename(spec, log_filename)

    command = 'install'

    log_with_spack(f'spack spec {spec}',
                   'system_test',
                   log_filename,
                   srun=False)
    log_with_spack(f'spack {command} -n -v {spec}',
                   'system_test',
                   log_filename,
                   srun=True)


def spack_install_and_test(spec: str,
                           log_filename: str = None,
                           split_phases=False):
    """
    Tests 'spack install' of the given spec and writes the output into the log file.
    """

    log_filename = compose_logfilename(spec, log_filename)

    command = 'install'

    log_with_spack(f'spack spec {spec}',
                   'system_test',
                   log_filename,
                   srun=False)
    if split_phases:
        log_with_spack(
            f'spack {command} --until build --test=root -n -v {spec}',
            'system_test',
            log_filename,
            srun=True)
        log_with_spack(
            f'spack {command} --dont-restage --test=root -n -v {spec}',
            'system_test',
            log_filename,
            srun=False)
    else:
        log_with_spack(f'spack {command} --test=root -n -v {spec}',
                       'system_test',
                       log_filename,
                       srun=not spec.startswith('icon '))


def spack_devbuild_and_test(spec: str,
                            log_filename: str = None,
                            cwd=None,
                            split_phases=False):
    """
    Tests 'spack dev-build' of the given spec and writes the output into the log file.
    """

    log_filename = compose_logfilename(spec, log_filename)

    command = 'dev-build'

    if split_phases:
        log_with_spack(f'spack {command} --until build --test=root -n {spec}',
                       'system_test',
                       log_filename,
                       cwd=cwd,
                       srun=True)
        log_with_spack(f'spack {command} --dont-restage --test=root -n {spec}',
                       'system_test',
                       log_filename,
                       cwd=cwd,
                       srun=False)
    else:
        log_with_spack(f'spack {command} --test=root -n {spec}',
                       'system_test',
                       log_filename,
                       cwd=cwd,
                       srun=True)


def spack_env_dev_install_and_test(spack_env: str,
                                   url: str,
                                   branch: str,
                                   name: str,
                                   log_filename: str = None,
                                   out_of_source: bool = False,
                                   build_on_login_node: bool = False):
    """
    Clones repo with given branch into unique folder, activates the given spack
    environment, tests 'spack install' and writes the output into the log file.
    If log_filename is None, spack_env is used to create one.

    ICON specials:
    If out_of_source is True, create additional folder and build there, BUT skip testing!
    If build_on_login_node is True, do not run build-step on login node
    """

    if name != 'icon' and out_of_source:
        raise ValueError('out-of-source only possible with Icon')

    unique_folder = name + '_' + uuid.uuid4(
    ).hex  # to avoid cloning into the same folder and having race conditions
    subprocess.run(
        f'git clone --depth 1 --recurse-submodules -b {branch} {url} {unique_folder}',
        check=True,
        shell=True)

    log_filename = sanitized_filename(log_filename or spack_env)

    if out_of_source:
        build_dir = os.path.join(unique_folder, 'build')
        os.makedirs(build_dir, exist_ok=True)
        shutil.copytree(os.path.join(unique_folder, 'config'),
                        os.path.join(build_dir, 'config'))
        unique_folder = build_dir
        log_filename = f'{log_filename}_out_of_source'

    log_with_spack('spack install -n -v',
                   'system_test',
                   log_filename,
                   cwd=unique_folder,
                   env=spack_env,
                   srun=not build_on_login_node)

    # for out-of-source build we can't run tests because required files
    # like scripts/spack/test.py or scripts/buildbot_script are not synced
    # in our spack-recipe to the build-folder
    if not out_of_source:
        log_with_spack('spack install --test=root -n -v',
                       'system_test',
                       log_filename,
                       cwd=unique_folder,
                       env=spack_env,
                       srun=False)


nvidia_compiler: str = {
    'daint': 'nvhpc',
    'tsa': 'pgi',
    'balfrin': 'nvhpc',
    'unknown': '',
}[machine_name()]


@pytest.mark.libfyaml
def test_install_libfyaml_default():
    spack_install('libfyaml')


@pytest.mark.libtorch
def test_install_libtorch_default():
    spack_install('libtorch')


@pytest.mark.no_balfrin  # cuda arch is not supported
@pytest.mark.no_tsa  # irrelevant
@pytest.mark.cosmo_dycore
@pytest.mark.parametrize("version,cuda_variant", [('6.0', '+cuda'),
                                                  ('6.0', '~cuda'),
                                                  ('6.1', '+cuda'),
                                                  ('6.1', '~cuda')])
def test_install_and_check_cosmo_dycore_for(version, cuda_variant):
    spack_install_and_test(f'cosmo-dycore @{version} {cuda_variant}',
                           split_phases=True)


@pytest.mark.cosmo_eccodes_definitions
@pytest.mark.parametrize("version", ['2.25.0.1', '2.19.0.7'])
def test_install_cosmo_eccodes_definitions_version(version):
    spack_install(f'cosmo-eccodes-definitions @{version}')


@pytest.mark.eccodes
def test_install_eccodes_2_19_0():
    spack_install('eccodes @2.19.0')


@pytest.mark.fckit
def test_install_and_check_fckit_0_9_0():
    spack_install_and_test('fckit@0.9.0')


@pytest.mark.fdb_fortran
def test_install_fdb_fortran():
    spack_install_and_test('fdb-fortran')


@pytest.mark.flexpart_ifs
@pytest.mark.parametrize("version", ['10.4.4', 'fdb'])
def test_install_flexpart_ifs_version(version):
    spack_install(f'flexpart-ifs @{version}')


@pytest.mark.no_tsa  # No one uses spack for flexpart-cosmo on Tsa
@pytest.mark.flexpart_cosmo
def test_install_flexpart_cosmo():
    spack_install_and_test('flexpart-cosmo @V8C4.0')


@pytest.mark.gridtools
def test_install_gridtools_version_1_1_3_gcc():
    spack_install_and_test(f'gridtools @1.1.3 %gcc')


@pytest.mark.no_tsa  # Only pgc++ 18 and 19 are supported! nvhpc doesn't work either.
@pytest.mark.gridtools
def test_install_version_1_1_3_nvhpc():
    spack_install_and_test(f'gridtools @1.1.3 %{nvidia_compiler}')


@pytest.mark.no_tsa  # FDB tests fail on tsa due to 'ucp_context'
@pytest.mark.fdb
def test_install_fdb_5_11_17_gcc():
    spack_install_and_test('fdb @5.11.17 %gcc')


@pytest.mark.no_tsa  # FDB tests fail on tsa due to 'ucp_context'
@pytest.mark.fdb
def test_install_fdb_5_11_17_nvhpc():
    # tests fail because compiler emitted warnings.
    spack_install(f'fdb @5.11.17 %{nvidia_compiler}')


@pytest.mark.no_tsa  # Icon does not run on Tsa
@pytest.mark.no_daint
@pytest.mark.icon
def test_install_icon_24_1_gcc():
    spack_install_and_test('icon @2024.1-1 %gcc')


@pytest.mark.icon
@pytest.mark.no_daint
@pytest.mark.no_tsa  # Icon does not run on Tsa
def test_install_2024_1_nvhpc():
    #WORKAROUND: ^libxml2%gcc works around a problem in the concretizer of spack v0.21.1 and /mch-environment/v6
    spack_install_and_test('icon @2024.1-1 %nvhpc ^libxml2%gcc')


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
    spack_install_and_test(
        'icon @2024.1-1 %nvhpc +coupling +rttov serialization=create +emvorado +mpi gpu=openacc+cuda ^libxml2%gcc'
    )


@pytest.mark.no_balfrin  # config file does not exist for this machine
@pytest.mark.no_tsa  # Icon does not run on Tsa
@pytest.mark.icon
def test_install_c2sm_test_cpu_nvhpc_out_of_source():
    spack_env_dev_install_and_test(
        'config/cscs/spack/v0.21.1.0/daint_cpu_nvhpc',
        'git@github.com:C2SM/icon.git',
        '2024.01.1',
        'icon',
        out_of_source=True,
        build_on_login_node=False)


@pytest.mark.no_balfrin  # config file does not exist for this machine
@pytest.mark.no_tsa  # Icon does not run on Tsa
@pytest.mark.icon
def test_install_c2sm_test_cpu():
    spack_env_dev_install_and_test(
        'config/cscs/spack/v0.21.1.0/daint_cpu_nvhpc',
        'git@github.com:C2SM/icon.git',
        '2024.01.1',
        'icon',
        build_on_login_node=False)


@pytest.mark.no_balfrin  # config file does not exist for this machine
@pytest.mark.no_tsa  # Icon does not run on Tsa
@pytest.mark.icon
def test_install_c2sm_test_gpu():
    spack_env_dev_install_and_test(
        'config/cscs/spack/v0.21.1.0/daint_gpu_nvhpc',
        'git@github.com:C2SM/icon.git',
        '2024.01.1',
        'icon',
        build_on_login_node=False)


@pytest.mark.no_tsa  # This test is flaky and sometimes fails with: icondelaunay.cpp:29:10: fatal error: version.c: No such file or directory. See issue #781.
@pytest.mark.icontools
def test_install_icontools():
    spack_install_and_test('icontools @2.5.2')


@pytest.mark.no_tsa  # Not supported on Tsa
@pytest.mark.no_balfrin  # Not supported on Balfrin
@pytest.mark.infero
def test_install_infero_tf_c():
    spack_install_and_test(
        'infero @0.1.2 %gcc +onnx +tf_c fflags="-ffree-line-length-1024"')


@pytest.mark.no_balfrin  # int2lm depends on 'libgrib1 @22-01-2020', which fails.
@pytest.mark.int2lm
def test_install_int2ml_version_3_00_gcc():
    spack_install('int2lm @int2lm-3.00 %gcc')


@pytest.mark.int2lm
@pytest.mark.serial_only
@pytest.mark.no_balfrin  # fails because libgrib1 master fails
def test_install_int2lm_version_3_00_nvhpc():
    spack_install_and_test(f'int2lm @int2lm-3.00 %{nvidia_compiler}')


@pytest.mark.int2lm
@pytest.mark.no_balfrin  # fails because libgrib1 master fails
def test_install_int2lm_version_3_00_nvhpc_fixed_definitions():
    spack_install_and_test(
        f'int2lm @int2lm-3.00 %{nvidia_compiler} ^cosmo-eccodes-definitions@2.19.0.7%{nvidia_compiler}'
    )


@pytest.mark.int2lm
@pytest.mark.no_balfrin  # fails because libgrib1 master fails
def test_install_int2lm_c2sm_master_gcc():
    spack_install('int2lm @v2.8.4 %gcc ^eccodes %gcc ^libgrib1 %gcc')


@pytest.mark.int2lm
@pytest.mark.no_balfrin  # fails because libgrib1 master fails
@pytest.mark.no_tsa  # An error occurred in MPI_Bcast
def test_install_int2lm_c2sm_master_nvhpc():
    spack_install_and_test(
        f'int2lm @v2.8.4 %{nvidia_compiler} ^cosmo-eccodes-definitions@2.19.0.7%{nvidia_compiler} ^libgrib1 %{nvidia_compiler}'
    )


@pytest.mark.no_tsa  # Test is too expensive. It takes over 5h.
@pytest.mark.libcdi_pio
def test_install_libcdi_pio_default():
    spack_install_and_test('libcdi-pio')


@pytest.mark.no_balfrin  # This fails with "BOZ literal constant at (1) cannot appear in an array constructor". https://gcc.gnu.org/onlinedocs/gfortran/BOZ-literal-constants.html
@pytest.mark.libgrib1
@pytest.mark.serial_only  # locking problem on Tsa in combination with int2lm
def test_install_libgrib1_22_01_2020():
    spack_install_and_test('libgrib1 @22-01-2020')


@pytest.mark.makedepf90
def test_install_makedepf90():
    spack_install('makedepf90 @3.0.1')


@pytest.mark.no_balfrin  # Package is a workaround, only needed on Daint.
@pytest.mark.no_tsa  # Package is a workaround, only needed on Daint.
@pytest.mark.nvidia_blas
def test_install_default_nvidia_blas():
    spack_install_and_test('nvidia-blas')


@pytest.mark.no_balfrin  # Package is a workaround, only needed on Daint.
@pytest.mark.no_tsa  # Package is a workaround, only needed on Daint.
@pytest.mark.nvidia_lapack
def test_install_default_nvidia_lapack():
    spack_install_and_test('nvidia-lapack')


@pytest.mark.onnx_runtime
def test_install_default_onnx_runtime():
    spack_install_and_test('onnx-runtime')


@pytest.mark.no_balfrin  # Coupling only needed on Daint
@pytest.mark.no_tsa  # Coupling only needed on Daint
@pytest.mark.oasis
def test_install_oasis_version_4_0_nvhpc():
    spack_install_and_test('oasis @4.0 %nvhpc')


@pytest.mark.no_tsa
@pytest.mark.pytorch_fortran
def test_install_pytorch_fortran_version_0_4(devirt_env):
    spack_install(
        'pytorch-fortran@0.4%nvhpc ^pytorch-fortran-proxy@0.4%gcc ^python@3.10 ^gmake%gcc ^cmake%gcc'
    )


@pytest.mark.no_tsa
@pytest.mark.pytorch_fortran_proxy
def test_install_pytorch_fortran_proxy_version_0_4(devirt_env):
    spack_install('pytorch-fortran-proxy@0.4%gcc ^python@3.10')


@pytest.mark.py_asttokens
def test_py_asttokens_install_default(devirt_env):
    spack_install_and_test('py-asttokens')


@pytest.mark.py_black
def test_py_black_install_default(devirt_env):
    spack_install_and_test('py-black')


@pytest.mark.py_boltons
def test_py_boltons_install_default(devirt_env):
    spack_install_and_test('py-boltons')


@pytest.mark.no_balfrin  # Preparing metadata (pyproject.toml): finished with status 'error: metadata-generation-failed'.
@pytest.mark.py_cytoolz
def test_py_cytoolz_install_default(devirt_env):
    spack_install_and_test('py-cytoolz')


@pytest.mark.py_devtools
def test_py_devtools_install_default(devirt_env):
    spack_install_and_test('py-devtools')


@pytest.mark.py_editables
def test_py_editables_install_default(devirt_env):
    spack_install_and_test('py-editables')


@pytest.mark.py_executing
def test_py_executing_install_default(devirt_env):
    spack_install_and_test('py-executing')


@pytest.mark.py_factory_boy
def test_py_factory_boy_install_default(devirt_env):
    spack_install_and_test('py-factory-boy')


@pytest.mark.py_fprettify
def test_py_fprettify_install_default(devirt_env):
    spack_install_and_test('py-fprettify')


@pytest.mark.py_frozendict
def test_py_frozendict_install_default(devirt_env):
    spack_install_and_test('py-frozendict')


@pytest.mark.py_gridtools_cpp
def test_py_gridtools_cpp_install_default(devirt_env):
    spack_install_and_test('py-gridtools-cpp')


@pytest.mark.py_gt4py
@pytest.mark.no_tsa  # Irrelevant
@pytest.mark.parametrize("version", ['1.0.3.3', '1.0.3.6', '1.0.3.7'])
def test_install_py_gt4py_for_version(version, devirt_env):
    spack_install_and_test(f'py-gt4py @{version}')


@pytest.mark.no_tsa  # py-isort install fails with: No module named 'poetry'.
@pytest.mark.py_icon4py
def test_install_py_icon4py_version_0_0_10(devirt_env):
    spack_install_and_test('py-icon4py @ 0.0.10 %gcc ^py-gt4py@1.0.3.3')


@pytest.mark.py_icon4py
@pytest.mark.no_tsa  # py-isort install fails with: No module named 'poetry'.
def test_install_py_icon4py_version_0_0_11(devirt_env):
    spack_install_and_test('py-icon4py @ 0.0.11 %gcc ^py-gt4py@1.0.3.7')


@pytest.mark.py_hatchling
def test_install_py_hatchling_default(devirt_env):
    spack_install_and_test('py-hatchling')


@pytest.mark.py_inflection
def test_install_py_inflection_default(devirt_env):
    spack_install_and_test('py-inflection')


@pytest.mark.py_isort
def test_install_py_isort_default(devirt_env):
    spack_install_and_test('py-isort')


@pytest.mark.py_lark
def test_install_py_lark_default(devirt_env):
    spack_install_and_test('py-lark')


@pytest.mark.py_nanobind
def test_install_py_nanobind_default(devirt_env):
    spack_install_and_test('py-nanobind')


@pytest.mark.py_pathspec
def test_install_py_pathspec_default(devirt_env):
    spack_install_and_test('py-pathspec')


@pytest.mark.py_pytest
def test_install_py_pytest_default(devirt_env):
    spack_install_and_test('py-pytest')


@pytest.mark.py_pytest_factoryboy
def test_install_py_pytest_factoryboy_default(devirt_env):
    spack_install_and_test('py-pytest-factoryboy')


@pytest.mark.py_setuptools
def test_install_py_setuptools_default(devirt_env):
    spack_install_and_test('py-setuptools')


@pytest.mark.py_sphinxcontrib_jquery
def test_install_py_sphinxcontrib_jquery_default(devirt_env):
    spack_install_and_test('py-sphinxcontrib-jquery')


@pytest.mark.py_tabulate
def test_install_py_tabulate_default(devirt_env):
    spack_install_and_test('py-tabulate')


@pytest.mark.py_typing_extensions
def test_install_py_typing_extensions_default(devirt_env):
    spack_install_and_test('py-typing-extensions')


@pytest.mark.no_tsa  # Irrelevant
@pytest.mark.no_balfrin  #Irrelevant
@pytest.mark.rttov
@pytest.mark.parametrize("compiler", ['gcc', 'nvhpc'])
def test_install_rttov(compiler):
    spack_install_and_test(f'rttov @13.1 %{compiler}')


@pytest.mark.no_tsa  # Fails with "C compiler cannot create executables"
@pytest.mark.scales_ppm
def test_install_default():
    spack_install_and_test('scales-ppm')


@pytest.mark.tensorflowc
def test_install_2_6_0():
    spack_install_and_test('tensorflowc @2.6.0')


@pytest.mark.no_tsa  # Fails with "C compiler cannot create executables"
@pytest.mark.yaxt
def test_install_yaxt_default():
    spack_install_and_test('yaxt')


@pytest.mark.zlib_ng
def test_install_zlib_ng_version_2_0_0():
    spack_install_and_test('zlib_ng @2.0.0')
