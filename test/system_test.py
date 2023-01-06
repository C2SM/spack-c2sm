import unittest
import pytest
import subprocess
import sys
import os
import uuid
from pathlib import Path

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, log_with_spack, sanitized_filename


def spack_installcosmo_and_test(command: str, log_filename: str = None):
    """
    Tests 'spack installcosmo' of the given command and writes the output into the log file.
    If log_filename is None, command is used to create one.
    """
    log_filename = sanitized_filename(log_filename or command)
    log_with_spack(f'spack installcosmo --until build -n -v {command}',
                   'system_test',
                   log_filename,
                   srun=True)
    log_with_spack(
        f'spack installcosmo --dont-restage --test=root -n -v {command}',
        'system_test',
        log_filename,
        srun=False)


def spack_install_and_test(command: str, log_filename: str = None):
    """
    Tests 'spack install' of the given command and writes the output into the log file.
    If log_filename is None, command is used to create one.
    """
    log_filename = sanitized_filename(log_filename or command)
    log_with_spack(f'spack install --until build --test=root -n -v {command}',
                   'system_test',
                   log_filename,
                   srun=True)
    log_with_spack(f'spack install --dont-restage --test=root -n -v {command}',
                   'system_test',
                   log_filename,
                   srun=False)


def spack_install_and_test_no_phase_splitting(command: str,
                                              log_filename: str = None):
    """
    Tests 'spack install' of the given command and writes the output into the log file.
    If log_filename is None, command is used to create one.
    """
    log_filename = sanitized_filename(log_filename or command)
    log_with_spack(f'spack install --test=root -n -v {command}',
                   'system_test',
                   log_filename,
                   srun=True)


def spack_install_and_test_python_package(command: str,
                                          log_filename: str = None):
    """
    Tests 'spack install' of the given command and writes the output into the log file.
    If log_filename is None, command is used to create one.

    Special version for Python packages to run in a clean environment
    """

    # pytest is run from a virtual environment that breaks the
    # Python environment setup by Spack. Additionally "deactivate"
    # is not available here, therefore we manually unset paths like

    # - VIRTUAL_ENV
    # - PATH

    # set by the virtual environment

    virtual_env = os.path.join(os.environ['VIRTUAL_ENV'], 'bin')
    os.environ.pop('VIRTUAL_ENV')
    path = os.environ['PATH']
    path = path.replace(virtual_env, '')
    os.environ['PATH'] = path

    log_filename = sanitized_filename(log_filename or command)
    log_with_spack(f'spack install --test=root -n -v {command}',
                   'system_test',
                   log_filename,
                   srun=True)


def spack_devbuildcosmo_and_test(command: str,
                                 log_filename: str = None,
                                 cwd=None):
    """
    Tests 'spack devbuildcosmo' of the given command and writes the output into the log file.
    If log_filename is None, command is used to create one.
    """
    log_filename = sanitized_filename(log_filename or command)
    log_with_spack(
        f'spack devbuildcosmo --until build --test=root -n {command}',
        'system_test',
        log_filename,
        cwd=cwd,
        srun=True)
    log_with_spack(
        f'spack devbuildcosmo --dont-restage --test=root -n {command}',
        'system_test',
        log_filename,
        cwd=cwd,
        srun=False)


def spack_devbuild_and_test(command: str, log_filename: str = None, cwd=None):
    """
    Tests 'spack dev-build' of the given command and writes the output into the log file.
    If log_filename is None, command is used to create one.
    """
    log_filename = sanitized_filename(log_filename or command)
    log_with_spack(f'spack dev-build --until build --test=root -n {command}',
                   'system_test',
                   log_filename,
                   cwd=cwd,
                   srun=True)
    log_with_spack(f'spack dev-build --dont-restage --test=root -n {command}',
                   'system_test',
                   log_filename,
                   cwd=cwd,
                   srun=False)


mpi: str = {
    'daint': 'mpich',
    'tsa': 'openmpi',
    'balfrin': 'cray-mpich-binary',
}[machine_name()]

nvidia_compiler: str = {
    'daint': 'nvhpc',
    'tsa': 'pgi',
    'balfrin': 'nvhpc',
}[machine_name()]


@pytest.mark.no_balfrin  # cosmo-dycore does not support the cuda arch of balfrin
class CosmoTest(unittest.TestCase):

    def test_install_version_6_0_cpu(self):
        spack_installcosmo_and_test(
            f'cosmo @6.0 %{nvidia_compiler} cosmo_target=cpu ~cppdycore ^{mpi} %{nvidia_compiler}'
        )

    def test_install_version_6_0_gpu(self):
        spack_installcosmo_and_test(
            f'cosmo @6.0 %{nvidia_compiler} cosmo_target=gpu +cppdycore ^{mpi} %{nvidia_compiler}'
        )

    def test_devbuild_version_6_0_cpu(self):
        unique_folder = uuid.uuid4().hex  # for multiprocessing-safety reasons
        subprocess.run(
            f'git clone --depth 1 --branch 6.0 git@github.com:COSMO-ORG/cosmo.git {unique_folder}',
            check=True,
            shell=True)
        try:
            spack_devbuildcosmo_and_test(
                f'cosmo @6.0_cpu %{nvidia_compiler} cosmo_target=cpu ~cppdycore ^{mpi} %{nvidia_compiler}',
                cwd=unique_folder)
        finally:
            subprocess.run(f'rm -rf {unique_folder}', shell=True)

    def test_devbuild_version_6_0_gpu(self):
        unique_folder = uuid.uuid4().hex  # for multiprocessing-safety reasons
        subprocess.run(
            f'git clone --depth 1 --branch 6.0 git@github.com:COSMO-ORG/cosmo.git {unique_folder}',
            check=True,
            shell=True)
        try:
            spack_devbuildcosmo_and_test(
                f'cosmo @6.0_gpu %{nvidia_compiler} cosmo_target=gpu +cppdycore ^{mpi} %{nvidia_compiler}',
                cwd='cosmo')
        finally:
            subprocess.run(f'rm -rf {unique_folder}', shell=True)

    def test_install_version_5_09_mch_1_2_p2_cpu(self):
        spack_installcosmo_and_test(
            f'cosmo @5.09a.mch1.2.p2 %{nvidia_compiler} cosmo_target=cpu ~cppdycore ^{mpi} %{nvidia_compiler}'
        )

    def test_install_version_5_09_mch_1_2_p2_gpu(self):
        spack_installcosmo_and_test(
            f'cosmo @5.09a.mch1.2.p2 %{nvidia_compiler} cosmo_target=gpu +cppdycore ^{mpi} %{nvidia_compiler}'
        )

    def test_install_c2sm_master_cpu(self):
        spack_installcosmo_and_test(
            f'cosmo @c2sm-master %{nvidia_compiler} cosmo_target=cpu ~cppdycore ^{mpi} %{nvidia_compiler}'
        )

    def test_install_c2sm_master_gpu(self):
        spack_installcosmo_and_test(
            f'cosmo @c2sm-master %{nvidia_compiler} cosmo_target=gpu +cppdycore ^{mpi} %{nvidia_compiler}'
        )


@pytest.mark.no_balfrin  # cuda arch is not supported
class CosmoDycoreTest(unittest.TestCase):

    def test_install_version_6_0_cuda(self):
        spack_install_and_test('cosmo-dycore @6.0 +cuda')

    def test_install_version_6_0_no_cuda(self):
        spack_install_and_test('cosmo-dycore @6.0 ~cuda')

    def test_install_c2sm_master_cuda(self):
        spack_install_and_test('cosmo-dycore @c2sm-master +cuda')

    def test_install_c2sm_master_no_cuda(self):
        spack_install_and_test('cosmo-dycore @c2sm-master ~cuda')


class CosmoEccodesDefinitionsTest(unittest.TestCase):

    def test_install_version_2_19_0_7(self):
        spack_install_and_test_no_phase_splitting(
            'cosmo-eccodes-definitions @2.19.0.7')


@pytest.mark.no_tsa  # It fails with: "This is libtool 2.4.7, but the libtool: definition of this LT_INIT comes from libtool 2.4.2".
@pytest.mark.no_balfrin  # It fails with: "This is libtool 2.4.7, but the libtool: definition of this LT_INIT comes from libtool 2.4.2".
class CosmoGribApiTest(unittest.TestCase):

    def test_install_version_1_20_0_3(self):
        spack_install_and_test('cosmo-grib-api @1.20.0.2')


class CosmoGribApiDefinitionsTest(unittest.TestCase):
    pass


class DawnTest(unittest.TestCase):
    pass


class Dawn4PyTest(unittest.TestCase):
    pass


class DuskTest(unittest.TestCase):
    pass


class GridToolsTest(unittest.TestCase):

    def test_install_version_1_1_3_gcc(self):
        spack_install_and_test(f'gridtools @1.1.3 %gcc')

    @pytest.mark.no_tsa  # Only pgc++ 18 and 19 are supported! nvhpc doesn't work either.
    def test_install_version_1_1_3_nvhpc(self):
        spack_install_and_test(f'gridtools @1.1.3 %{nvidia_compiler}')


@pytest.mark.no_tsa  # config file does not exist for this machine
class IconTest(unittest.TestCase):

    def test_install_nwp_gpu(self):
        spack_install_and_test(
            f'icon @nwp %nvhpc icon_target=gpu ^{mpi} %{nvidia_compiler}')

    def test_install_nwp_cpu(self):
        spack_install_and_test(
            f'icon @nwp %nvhpc icon_target=cpu ^{mpi} %{nvidia_compiler}')

    # def test_devbuild_nwp_gpu(self):
    #     spack_install_and_test(
    #         f'icon @develop %nvhpc config_dir=./.. icon_target=gpu ^{mpi} %{nvidia_compiler}')

    # def test_devbuild_nwp_cpu(self):
    #     spack_install_and_test(
    #         f'icon @develop %nvhpc config_dir=./.. icon_target=cpu ^{mpi} %{nvidia_compiler}')

    @pytest.mark.no_balfrin  # config file does not exist for this machines
    def test_install_exclaim_cpu(self):
        spack_install_and_test(
            f'icon @exclaim-master %nvhpc icon_target=cpu +eccodes +ocean ^{mpi} %{nvidia_compiler}'
        )

    @pytest.mark.no_balfrin  # config file does not exist for this machines
    def test_install_exclaim_cpu_gcc(self):
        spack_install_and_test(
            'icon @exclaim-master %gcc icon_target=cpu +eccodes +ocean')

    @pytest.mark.no_balfrin  # config file does not exist for this machines
    def test_install_exclaim_gpu(self):
        spack_install_and_test(
            f'icon @exclaim-master %nvhpc icon_target=gpu +eccodes +ocean +claw ^{mpi} %{nvidia_compiler}'
        )


class Int2lmTest(unittest.TestCase):

    def test_install_version_3_00_gcc(self):
        spack_install_and_test('int2lm @int2lm-3.00 %gcc')

    def test_install_version_3_00_nvhpc(self):
        spack_install_and_test(f'int2lm @int2lm-3.00 %{nvidia_compiler}')

    def test_install_c2sm_master_gcc(self):
        spack_install_and_test(
            'int2lm @c2sm-master %gcc ^eccodes %gcc ^libgrib1 %gcc')

    def test_install_c2sm_master_nvhpc(self):
        spack_install_and_test(
            f'int2lm @c2sm-master %{nvidia_compiler} ^eccodes %{nvidia_compiler} ^libgrib1 %{nvidia_compiler}'
        )


@pytest.mark.no_balfrin  # This fails with "undefined reference to symbol".
@pytest.mark.no_daint  # This fails with: "C compiler cannot create executables".
@pytest.mark.no_tsa  # This fails with: "C compiler cannot create executables".
class IconToolsTest(unittest.TestCase):

    def test_install(self):
        spack_install_and_test('icontools @c2sm-master %gcc')


class LibGrib1Test(unittest.TestCase):

    def test_install_version_22_01_2020(self):
        spack_install_and_test('libgrib1 @22-01-2020')


class OasisTest(unittest.TestCase):
    pass  #TODO


class OmniXmodPoolTest(unittest.TestCase):

    def test_install_version_0_1(self):
        spack_install_and_test_no_phase_splitting('omni-xmod-pool @0.1')


@pytest.mark.no_balfrin  # This fails with: "multiple definition of symbols"
@pytest.mark.no_tsa  # This fails with: "multiple definition of symbols"
class OmniCompilerTest(unittest.TestCase):

    def test_install_version_1_3_2(self):
        spack_install_and_test('omnicompiler @1.3.2')


@pytest.mark.no_balfrin
@pytest.mark.no_tsa
class PyGt4pyTest(unittest.TestCase):

    def test_install_version_functional(self):
        spack_install_and_test_python_package('py-gt4py %gcc')


@pytest.mark.no_balfrin  # py-isort install fails with: No module named 'poetry'.
@pytest.mark.no_tsa # py-isort install fails with: No module named 'poetry'.
class PyIcon4pyTest(unittest.TestCase):

    def test_install_version_main(self):
        spack_install_and_test_python_package('py-icon4py @main %gcc')


class XcodeMLToolsTest(unittest.TestCase):

    def test_install_version_92a35f9(self):
        spack_install_and_test('xcodeml-tools @92a35f9')


class ZLibNGTest(unittest.TestCase):

    def test_install_version_2_0_0(self):
        spack_install_and_test('zlib_ng @2.0.0')


if __name__ == '__main__':
    unittest.main(verbosity=2)
