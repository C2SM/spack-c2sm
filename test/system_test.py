import unittest
import sys
import os
from pathlib import Path

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, log_with_spack


def test_with_spack(command: str, log_name: str = None):
    if log_name is None:
        log_name = command.replace(' ', '_').replace('%', '')

    log = Path(
        f'{spack_c2sm_path}/log/{machine_name()}/system_test/{log_name}.log')
    ret = log_with_spack(command, log)
    ret.check_returncode()


def spack_install(command: str, log_name: str = None):
    test_with_spack(f'spack install {command}', log_name)


class CosmoTest(unittest.TestCase):

    def test_install_version_6_0(self):
        spack_install('--test=root cosmo @6.0')

    def test_install_version_5_09_mch_1_2_p2(self):
        spack_install('--test=root cosmo @5.09a.mch1.2.p2')


class IconTest(unittest.TestCase):

    def setUp(self):
        if machine_name() in ['tsa']:
            self.skipTest()

    def test_install_version_2_6_5(self):
        spack_install('--test=root icon @2.6.5')

    def test_install_nwp_cpu(self):
        spack_install('icon @nwp %nvhpc icon_target=cpu')

    def test_install_nwp_gpu(self):
        spack_install('icon @nwp icon_target=gpu')

    def test_install_nwp_all_deps(self):
        """Triggers conditional dependencies"""

        spack_install(
            '--test=root icon @nwp icon_target=cpu serialize_mode=create +eccodes +claw'
        )


class Int2lmTest(unittest.TestCase):

    def test_install_gcc(self):
        spack_install('int2lm @c2sm-master %gcc')

    def test_install_nvhpc(self):
        if machine_name() in ['tsa']:
            return
        spack_install('int2lm @c2sm-master %nvhpc')


class IconToolsTest(unittest.TestCase):

    def test_install(self):
        spack_install('icontools @c2sm-master %gcc')


if __name__ == '__main__':
    unittest.main(verbosity=2)
