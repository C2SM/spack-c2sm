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


def spack_install_and_test(command: str, log_name: str = None):
    if 'cosmo' in command and 'cosmo-dycore' not in command:
        test_with_spack(f'spack installcosmo -v {command}', log_name)
    else:
        test_with_spack(f'spack install --show-log-on-error --test=root {command}', log_name)


def needs_testing(package: str) -> bool:
    if 'all' in sys.argv:
        return True
    if 'jenkins' in sys.argv:
        return machine_name() in sys.argv and package in sys.argv
    return True


@unittest.skipUnless(needs_testing('cosmo'), 'irrelevant')
class CosmoTest(unittest.TestCase):
    package_name = 'cosmo'

    def test_install_version_6_0(self):
        spack_install_and_test('cosmo @6.0')

    def test_install_version_5_09_mch_1_2_p2(self):
        spack_install_and_test('cosmo @5.09a.mch1.2.p2')


@unittest.skipUnless(needs_testing('cosmo-dycore'), 'irrelevant')
class CosmoDycoreTest(unittest.TestCase):
    package_name = 'cosmo-dycore'

    def test_install_version_6_0(self):
        spack_install_and_test('cosmo-dycore @6.0')

    def test_install_version_6_0_no_cuda(self):
        spack_install_and_test('cosmo-dycore @6.0 ~cuda')

    def test_install_version_5_09_mch_1_2_p2(self):
        spack_install_and_test('cosmo-dycore @5.09a.mch1.2.p2')


class CosmoEccodesDefinitionsTest(unittest.TestCase):
    package_name = 'cosmo-eccodes-definitions'


class CosmoGribApiTest(unittest.TestCase):
    package_name = 'cosmo-grib-api'


class CosmoGribApiDefinitionsTest(unittest.TestCase):
    package_name = 'cosmo-grib-api-definitions'
    

class DawnTest(unittest.TestCase):
    package_name = 'dawn'
    

class Dawn4PyTest(unittest.TestCase):
    package_name = 'dawn4py'


class DuskTest(unittest.TestCase):
    package_name = 'dusk'


class GridToolsTest(unittest.TestCase):
    package_name = 'gridtools'


@unittest.skipUnless(needs_testing('icon'), 'irrelevant')
@unittest.skipIf(machine_name() in ['tsa', 'manali'], 'config file does not exist for these machines')
class IconTest(unittest.TestCase):
    package_name = 'icon'

    def test_install_version_2_6_5(self):
        spack_install_and_test('icon @2.6.5')

    def test_install_nwp_cpu(self):
        spack_install_and_test('icon @nwp %nvhpc icon_target=cpu')

    def test_install_nwp_gpu(self):
        spack_install_and_test('icon @nwp icon_target=gpu')

    def test_install_nwp_all_deps(self):
        """Triggers conditional dependencies"""

        spack_install_and_test('icon @nwp icon_target=gpu serialize_mode=create +eccodes +claw')


@unittest.skipUnless(needs_testing('int2lm'), 'irrelevant')
class Int2lmTest(unittest.TestCase):
    package_name = 'int2lm'

    def test_install_gcc(self):
        spack_install_and_test('int2lm @c2sm-master %gcc')

    def test_install_nvhpc(self):
        spack_install_and_test('int2lm @c2sm-master %nvhpc')


@unittest.skipUnless(needs_testing('icontools'), 'irrelevant')
class IconToolsTest(unittest.TestCase):
    package_name = 'icontools'

    def test_install(self):
        spack_install_and_test('icontools @c2sm-master %gcc')


class LibGrib1Test(unittest.TestCase):
    package_name = 'libgrib1'


class OasisTest(unittest.TestCase):
    package_name = 'oasis'


class OmniXmodPoolTest(unittest.TestCase):
    package_name = 'omni-xmod-pool'


class OmniCompilerTest(unittest.TestCase):
    package_name = 'omnicompiler'


class XcodeMLToolsTest(unittest.TestCase):
    package_name = 'xcodeml-tools'


class ZLibNGTest(unittest.TestCase):
    package_name = 'zlib_ng'


if __name__ == '__main__':
    commands = sys.argv[1:]
    sys.argv = [sys.argv[0]]  # unittest needs this
    unittest.main(verbosity=2)
