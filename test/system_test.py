import unittest
import pytest
import sys
import os
from pathlib import Path

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, log_with_spack


def spack_installcosmo_and_test(command: str, log_filename: str = None):
    """
    Tests 'spack installcosmo' of the given command and writes the output into the log file.
    If log_filename is None, command is used to create one.
    """
    ret = log_with_spack(f'spack installcosmo --test=root -n -v {command}',
                         'system_test', log_filename)
    ret.check_returncode()


def spack_install_and_test(command: str, log_filename: str = None):
    """
    Tests 'spack install' of the given command and writes the output into the log file.
    If log_filename is None, command is used to create one.
    """
    ret = log_with_spack(f'spack install --test=root -n -v {command}',
                         'system_test', log_filename)
    ret.check_returncode()


def spack_installcosmo_and_test(command: str, log_name: str = None):
    test_with_spack(f'spack installcosmo --test=root -n -v {command}',
                    log_name)


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
        #spack_installcosmo_and_test(f'cosmo @6.0 %{nvidia_compiler} cosmo_target=cpu ~cppdycore ^{mpi} %{nvidia_compiler}')
        pass  #TODO

    def test_devbuild_version_6_0_gpu(self):
        #spack_installcosmo_and_test(f'cosmo @6.0 %{nvidia_compiler} cosmo_target=gpu +cppdycore ^{mpi} %{nvidia_compiler}')
        pass  #TODO

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
        spack_install_and_test('cosmo-eccodes-definitions @2.19.0.7')


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

    def test_install_version_1_1_3(self):
        spack_install_and_test('gridtools @1.1.3')


@pytest.mark.no_tsa  # config file does not exist for these machines
class IconTest(unittest.TestCase):

    def test_install_nwp_gpu(self):
        spack_install_and_test(
            'icon @nwp %nvhpc icon_target=gpu +claw +eccodes +ocean')

    def test_install_nwp_cpu(self):
        spack_install_and_test(
            'icon @nwp %nvhpc icon_target=cpu serialize_mode=create +eccodes +ocean'
        )

    def test_devbuild_nwp_gpu(self):
        spack_install_and_test(
            'icon @develop %nvhpc config_dir=./.. icon_target=gpu')

    def test_devbuild_nwp_cpu(self):
        spack_install_and_test(
            'icon @develop %nvhpc config_dir=./.. icon_target=cpu')

    def test_install_exclaim_cpu(self):
        spack_install_and_test(
            'icon @exclaim-master %nvhpc icon_target=cpu +eccodes +ocean')

    def test_install_exclaim_cpu_gcc(self):
        spack_install_and_test(
            'icon @exclaim-master %gcc icon_target=gpu +eccodes +ocean +claw')

    def test_install_exclaim_gpu(self):
        spack_install_and_test(
            'icon @exclaim-master %nvhpc icon_target=gpu +eccodes +ocean +claw'
        )


class Int2lmTest(unittest.TestCase):

    def test_install_version_3_00_gcc(self):
        spack_install_and_test('int2lm @int2lm-3.00 %gcc')

    def test_install_version_3_00_nvhpc(self):
        spack_install_and_test(f'int2lm @int2lm-3.00 %{nvidia_compiler}')

    def test_install_c2sm_master_gcc(self):
        spack_install_and_test('int2lm @c2sm-master %gcc')

    def test_install_c2sm_master_nvhpc(self):
        spack_install_and_test(f'int2lm @c2sm-master %{nvidia_compiler}')


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
        spack_install_and_test('omni-xmod-pool @0.1')


class OmniCompilerTest(unittest.TestCase):

    def test_install_version_1_3_2(self):
        spack_install_and_test('omnicompiler @1.3.2')


class XcodeMLToolsTest(unittest.TestCase):

    def test_install_version_92a35f9(self):
        spack_install_and_test('xcodeml-tools @92a35f9')


class ZLibNGTest(unittest.TestCase):

    def test_install_version_2_0_0(self):
        spack_install_and_test('xcodeml-tools @2.0.0')


if __name__ == '__main__':
    unittest.main(verbosity=2)
