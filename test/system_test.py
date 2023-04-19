import unittest
import pytest
import subprocess
import sys
import os
import uuid
from pathlib import Path
import inspect

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, log_with_spack, sanitized_filename


def devirtualize_env():
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


def spack_install_and_test(spec: str,
                           log_filename: str = None,
                           split_phases=False):
    """
    Tests 'spack install' of the given spec and writes the output into the log file.
    """

    func_name = inspect.currentframe().f_back.f_code.co_name.replace(
        'test_', '')
    class_name = inspect.currentframe().f_back.f_locals.get(
        'self', None).__class__.__name__.replace('Test', '')
    if log_filename is None:
        log_filename = sanitized_filename(class_name + '-' + func_name)

    if spec.startswith('cosmo '):
        command = 'installcosmo'
    else:
        command = 'install'

    if spec.startswith('py-'):
        devirtualize_env()

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
                       srun=True)


def spack_devbuild_and_test(spec: str,
                            log_filename: str = None,
                            cwd=None,
                            split_phases=False):
    """
    Tests 'spack dev-build' of the given spec and writes the output into the log file.
    """

    func_name = inspect.currentframe().f_back.f_code.co_name.replace(
        'test_', '')
    class_name = inspect.currentframe().f_back.f_locals.get(
        'self', None).__class__.__name__.replace('Test', '')
    if log_filename is None:
        log_filename = sanitized_filename(class_name + '-' + func_name)

    if spec.startswith('cosmo '):
        command = 'devbuildcosmo'
    else:
        command = 'dev-build'

    if spec.startswith('py-'):
        devirtualize_env()

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
                                   icon_branch: str,
                                   log_filename: str = None):
    """
    Clones ICON with given branch into unique folder, activates the given spack
    environment, tests 'spack install' and writes the output into the log file.
    If log_filename is None, spack_env is used to create one.
    """

    # in case we use serialbox or another python preprocessor
    devirtualize_env()

    unique_folder = 'icon_' + uuid.uuid4(
    ).hex  # to avoid cloning into the same folder and having race conditions
    subprocess.run(
        f'git clone --depth 1 --recurse-submodules -b {icon_branch} git@github.com:C2SM/icon.git {unique_folder}',
        check=True,
        shell=True)
    log_filename = sanitized_filename(log_filename or spack_env)

    # limit number of build-jobs to 4 because no srun used
    log_with_spack('spack install -j 4 --until build -n -v',
                   'system_test',
                   log_filename,
                   cwd=unique_folder,
                   env=spack_env,
                   srun=False)

    log_with_spack('spack install --test=root -n -v',
                   'system_test',
                   log_filename,
                   cwd=unique_folder,
                   env=spack_env,
                   srun=False)


mpi: str = {
    'daint': 'mpich',
    'tsa': 'openmpi',
    'balfrin': 'cray-mpich',
}[machine_name()]

nvidia_compiler: str = {
    'daint': 'nvhpc',
    'tsa': 'pgi',
    'balfrin': 'nvhpc',
}[machine_name()]


@pytest.mark.no_balfrin  # cosmo-dycore does not support the cuda arch of balfrin
@pytest.mark.no_tsa  # irrelevant
class CosmoTest(unittest.TestCase):

    def test_install_version_6_0_gpu(self):
        spack_install_and_test(
            f'cosmo @6.0 %{nvidia_compiler} cosmo_target=gpu +cppdycore ^{mpi} %{nvidia_compiler}',
            split_phases=True)

    def test_install_version_6_0_cpu(self):
        spack_install_and_test(
            f'cosmo @6.0 %{nvidia_compiler} cosmo_target=cpu ~cppdycore ^{mpi} %{nvidia_compiler}',
            split_phases=True)

    @pytest.mark.serial_only  # devbuildcosmo does a forced uninstall
    def test_devbuildcosmo(self):
        subprocess.run(
            'git clone --depth 1 --branch 6.0 git@github.com:COSMO-ORG/cosmo.git',
            check=True,
            shell=True)
        spec = f'cosmo @6.0 %{nvidia_compiler} cosmo_target=cpu ~cppdycore ^{mpi} %{nvidia_compiler}'
        spack_devbuild_and_test(
            spec,
            cwd='cosmo',
            log_filename=sanitized_filename('devbuildcosmo ' + spec),
            split_phases=True)


@pytest.mark.no_balfrin  # cuda arch is not supported
class CosmoDycoreTest(unittest.TestCase):

    def test_install_version_6_0(self):
        spack_install_and_test('cosmo-dycore @6.0 +cuda', split_phases=True)
        spack_install_and_test('cosmo-dycore @6.0 ~cuda', split_phases=True)

    def test_install_c2sm_master_cuda(self):
        spack_install_and_test('cosmo-dycore @c2sm-master +cuda',
                               split_phases=True)

    def test_install_c2sm_master_no_cuda(self):
        spack_install_and_test('cosmo-dycore @c2sm-master ~cuda',
                               split_phases=True)


class CosmoEccodesDefinitionsTest(unittest.TestCase):

    def test_install_version_2_19_0_7(self):
        spack_install_and_test('cosmo-eccodes-definitions @2.19.0.7')


class DawnTest(unittest.TestCase):
    pass


class Dawn4PyTest(unittest.TestCase):
    pass


class DuskTest(unittest.TestCase):
    pass


class FlexpartIfsTest(unittest.TestCase):

    def test_install(self):
        spack_install_and_test('flexpart-ifs')


class GridToolsTest(unittest.TestCase):

    def test_install_version_1_1_3_gcc(self):
        spack_install_and_test(f'gridtools @1.1.3 %gcc')

    @pytest.mark.no_tsa  # Only pgc++ 18 and 19 are supported! nvhpc doesn't work either.
    def test_install_version_1_1_3_nvhpc(self):
        spack_install_and_test(f'gridtools @1.1.3 %{nvidia_compiler}')


@pytest.mark.no_tsa  # Icon does not run on Tsa
class IconTest(unittest.TestCase):

    @pytest.mark.no_daint  # libxml2 %nvhpc fails to build
    def test_install_nwp_gpu(self):
        spack_install_and_test(f'icon @nwp-master %nvhpc gpu=80')

    @pytest.mark.no_daint  # libxml2 %nvhpc fails to build
    def test_install_nwp_cpu(self):
        spack_install_and_test(f'icon @nwp-master %nvhpc')

    @pytest.mark.no_balfrin  # config file does not exist for this machine
    def test_install_c2sm_test_cpu_gcc(self):
        spack_env_dev_install_and_test(
            'config/cscs/spack/v0.18.1.1/daint_cpu_gcc', 'icon-2.6.6')

    @pytest.mark.no_balfrin  # config file does not exist for this machine
    def test_install_c2sm_test_cpu(self):
        spack_env_dev_install_and_test(
            'config/cscs/spack/v0.18.1.1/daint_cpu_nvhpc', 'icon-2.6.6')

    @pytest.mark.no_balfrin  # config file does not exist for this machine
    def test_install_c2sm_test_gpu(self):
        spack_env_dev_install_and_test(
            'config/cscs/spack/v0.18.1.1/daint_gpu_nvhpc', 'icon-2.6.6')


@pytest.mark.no_balfrin  # int2lm depends on 'libgrib1 @22-01-2020', which fails.
class Int2lmTest(unittest.TestCase):

    def test_install_version_3_00_gcc(self):
        spack_install_and_test('int2lm @int2lm-3.00 %gcc')

    @pytest.mark.serial_only
    @pytest.mark.no_balfrin  # fails because libgrib1 master fails
    def test_install_version_3_00_nvhpc(self):
        spack_install_and_test(f'int2lm @int2lm-3.00 %{nvidia_compiler}')

    @pytest.mark.no_balfrin  # fails because libgrib1 master fails
    def test_install_version_3_00_nvhpc_fixed_definitions(self):
        spack_install_and_test(
            f'int2lm @int2lm-3.00 %{nvidia_compiler} ^cosmo-eccodes-definitions@2.19.0.7%{nvidia_compiler}'
        )

    def test_install_c2sm_master_gcc(self):
        spack_install_and_test(
            'int2lm @c2sm-master %gcc ^eccodes %gcc ^libgrib1 %gcc')

    @pytest.mark.no_balfrin  # fails because libgrib1 master fails
    @pytest.mark.no_tsa  # An error occurred in MPI_Bcast
    def test_install_c2sm_master_nvhpc(self):
        spack_install_and_test(
            f'int2lm @c2sm-master %{nvidia_compiler} ^cosmo-eccodes-definitions@2.19.0.7%{nvidia_compiler} ^libgrib1 %{nvidia_compiler}'
        )


class IconToolsTest(unittest.TestCase):

    def test_install(self):
        spack_install_and_test('icontools @2.5.2')


@pytest.mark.no_tsa  # Not supported on Tsa
@pytest.mark.no_balfrin  # Not supported on Balfrin
class InferoTest(unittest.TestCase):

    def test_install(self):
        spack_install_and_test('infero@0.1.2 %gcc')


@pytest.mark.no_balfrin  # This fails with "BOZ literal constant at (1) cannot appear in an array constructor". https://gcc.gnu.org/onlinedocs/gfortran/BOZ-literal-constants.html
class LibGrib1Test(unittest.TestCase):

    @pytest.mark.serial_only  # locking problem on Tsa in combination with int2lm
    def test_install_version_22_01_2020(self):
        spack_install_and_test('libgrib1 @22-01-2020')


@pytest.mark.no_balfrin  # Coupling only needed on Daint
@pytest.mark.no_tsa  # Coupling only needed on Daint
class OasisTest(unittest.TestCase):

    def test_install_master_nvhpc(self):
        spack_install_and_test('oasis @master %nvhpc')


class OmniXmodPoolTest(unittest.TestCase):

    def test_install_version_0_1(self):
        spack_install_and_test('omni-xmod-pool @0.1')


@pytest.mark.no_tsa  # Irrelevant
class PyGt4pyTest(unittest.TestCase):

    def test_install_version_1_1_1(self):
        spack_install_and_test('py-gt4py @ 1.1.1 %gcc ^python@3.10.4')


@pytest.mark.no_tsa  # py-isort install fails with: No module named 'poetry'.
class PyIcon4pyTest(unittest.TestCase):

    def test_install_version_0_0_3(self):
        spack_install_and_test(
            'py-icon4py @ 0.0.3 %gcc ^py-gt4py@1.1.1 ^python@3.10.4')

@pytest.mark.no_tsa
@pytest.mark.no_balfrin
class RttovTest(unittest.TestCase):

    def Rttov_install_version_13_1(self):
        spack_install_and_test(
            'rttov @ 13.1  %nvhpc')


class ZLibNGTest(unittest.TestCase):

    def test_install_version_2_0_0(self):
        spack_install_and_test('zlib_ng @2.0.0')


if __name__ == '__main__':
    unittest.main(verbosity=2)
