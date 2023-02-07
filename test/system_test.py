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
                           split_phases=True,
                           python_package=False):
    """
    Tests 'spack install' of the given spec and writes the output into the log file.
    If log_filename is None, spec is used to create one.
    """

    log_filename = sanitized_filename(log_filename or spec)

    if spec.startswith('cosmo '):
        command = 'installcosmo'
    else:
        command = 'install'

    if spec.startswith('py-'):
        python_package = True

    if python_package:
        # python packages don't necessarily have a build phase.
        # Thus splitting on build doesn't work in general
        split_phases = False
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
                            split_phases=True,
                            python_package=False):
    """
    Tests 'spack dev-build' of the given spec and writes the output into the log file.
    If log_filename is None, spec is used to create one.
    """
    log_filename = sanitized_filename(log_filename or spec)

    if spec.startswith('cosmo '):
        command = 'devbuildcosmo'
    else:
        command = 'dev-build'

    if python_package:
        # python packages don't necessarily have a build phase.
        # Thus splitting on build doesn't work in general
        split_phases = False
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
@pytest.mark.no_tsa  # irrelevant
class CosmoTest(unittest.TestCase):

    @pytest.mark.serial_only
    def test_install_version_6_0_gpu(self):
        spack_install_and_test(
            f'cosmo @6.0 %{nvidia_compiler} cosmo_target=gpu +cppdycore ^{mpi} %{nvidia_compiler}'
        )

    def test_install_version_6_0_cpu(self):
        spack_install_and_test(
            f'cosmo @6.0 %{nvidia_compiler} cosmo_target=cpu ~cppdycore ^{mpi} %{nvidia_compiler}'
        )

    def test_devbuildcosmo(self):
        subprocess.run(
            'git clone --depth 1 --branch 6.0 git@github.com:COSMO-ORG/cosmo.git',
            check=True,
            shell=True)
        spec = f'cosmo @6.0 %{nvidia_compiler} cosmo_target=gpu +cppdycore ^{mpi} %{nvidia_compiler}'
        spack_devbuild_and_test(
            spec,
            cwd='cosmo',
            log_filename=sanitized_filename('devbuildcosmo ' + spec))

    @pytest.mark.no_daint  # Testsuite fails
    def test_install_version_5_09_mch_1_2_p2_cpu(self):
        spack_install_and_test(
            f'cosmo @5.09a.mch1.2.p2 %{nvidia_compiler} cosmo_target=cpu ~cppdycore ^{mpi} %{nvidia_compiler}'
        )

    @pytest.mark.no_daint  # Unable to open MODULE file gt_gcl_bindings.mod
    def test_install_version_5_09_mch_1_2_p2_gpu(self):
        spack_install_and_test(
            f'cosmo @5.09a.mch1.2.p2 %{nvidia_compiler} cosmo_target=gpu +cppdycore ^{mpi} %{nvidia_compiler}'
        )

    def test_install_c2sm_features_cpu(self):
        spack_install_and_test(
            f'cosmo @c2sm-features %{nvidia_compiler} cosmo_target=cpu ~cppdycore ^{mpi} %{nvidia_compiler}'
        )

    @pytest.mark.serial_only
    def test_install_c2sm_features_gpu(self):
        spack_install_and_test(
            f'cosmo @c2sm-features %{nvidia_compiler} cosmo_target=gpu +cppdycore ^{mpi} %{nvidia_compiler}'
        )


@pytest.mark.no_balfrin  # cuda arch is not supported
class CosmoDycoreTest(unittest.TestCase):

    def test_install_version_6_0(self):
        spack_install_and_test('cosmo-dycore @6.0 +cuda')
        spack_install_and_test('cosmo-dycore @6.0 ~cuda')

    def test_install_c2sm_master_cuda(self):
        spack_install_and_test('cosmo-dycore @c2sm-master +cuda')

    def test_install_c2sm_master_no_cuda(self):
        spack_install_and_test('cosmo-dycore @c2sm-master ~cuda')


class CosmoEccodesDefinitionsTest(unittest.TestCase):

    def test_install_version_2_19_0_7(self):
        spack_install_and_test('cosmo-eccodes-definitions @2.19.0.7',
                               split_phases=False)


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

    @pytest.mark.no_daint  # cannot link to libxml2 library
    def test_install_nwp_gpu(self):
        spack_install_and_test(
            f'icon @nwp %nvhpc icon_target=gpu ^{mpi} %{nvidia_compiler}')

    @pytest.mark.no_daint  # cannot link to libxml2 library
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
    @pytest.mark.no_daint  # unable to link a test program using the Fortran 90 interface of NetCDF library
    def test_install_exclaim_cpu(self):
        spack_install_and_test(
            f'icon @exclaim-master %nvhpc icon_target=cpu +eccodes +ocean ^{mpi} %{nvidia_compiler}'
        )

    @pytest.mark.no_balfrin  # config file does not exist for this machines
    @pytest.mark.no_daint  # Cannot depend on 'cmake' twice
    def test_install_exclaim_cpu_gcc(self):
        spack_install_and_test(
            'icon @exclaim-master %gcc icon_target=cpu +eccodes +ocean')

    @pytest.mark.no_balfrin  # config file does not exist for this machines
    @pytest.mark.no_daint  # unable to link a test program using the Fortran 90 interface of NetCDF library
    def test_install_exclaim_gpu(self):
        spack_install_and_test(
            f'icon @exclaim-master %nvhpc icon_target=gpu +eccodes +ocean +claw ^{mpi} %{nvidia_compiler}'
        )


@pytest.mark.no_balfrin  # int2lm depends on 'libgrib1 @22-01-2020', which fails.
class Int2lmTest(unittest.TestCase):

    def test_install_version_3_00_gcc(self):
        spack_install_and_test('int2lm @int2lm-3.00 %gcc')

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


@pytest.mark.no_balfrin  # This fails with "undefined reference to symbol".
class IconToolsTest(unittest.TestCase):

    def test_install(self):
        spack_install_and_test('icontools @c2sm-master %gcc')


@pytest.mark.no_balfrin  # This fails with "BOZ literal constant at (1) cannot appear in an array constructor". https://gcc.gnu.org/onlinedocs/gfortran/BOZ-literal-constants.html
class LibGrib1Test(unittest.TestCase):

    @pytest.mark.serial_only  # locking problem on Tsa in combination with int2lm
    def test_install_version_22_01_2020(self):
        spack_install_and_test('libgrib1 @22-01-2020')


@pytest.mark.no_balfrin  # Coupling only needed on Daint
@pytest.mark.no_tsa  # Coupling only needed on Daint
class OasisTest(unittest.TestCase):

    def test_install_master_nvhpc(self):
        spack_install_and_test('oasis@master%nvhpc', split_phases=False)


class OmniXmodPoolTest(unittest.TestCase):

    def test_install_version_0_1(self):
        spack_install_and_test('omni-xmod-pool @0.1', split_phases=False)


@pytest.mark.no_balfrin  # Irrelevant
@pytest.mark.no_daint  # py-isort install fails with: No module named 'poetry'.
@pytest.mark.no_tsa  # Irrelevant
class PyGt4pyTest(unittest.TestCase):

    def test_install_version_functional(self):
        spack_install_and_test('py-gt4py %gcc')


@pytest.mark.no_balfrin  # py-isort install fails with: No module named 'poetry'.
@pytest.mark.no_daint  # py-isort install fails
@pytest.mark.no_tsa  # py-isort install fails with: No module named 'poetry'.
class PyIcon4pyTest(unittest.TestCase):

    def test_install_version_main(self):
        spack_install_and_test('py-icon4py @main %gcc')


class ZLibNGTest(unittest.TestCase):

    def test_install_version_2_0_0(self):
        spack_install_and_test('zlib_ng @2.0.0')


if __name__ == '__main__':
    unittest.main(verbosity=2)
