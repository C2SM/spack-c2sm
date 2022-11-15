import unittest
from src import machine_name, spack_install


class CosmoTest(unittest.TestCase):

    def test_install_5_08_mch_1_0_p3(self):
        spack_install('cosmo @apn_5.08.mch.1.0.p3')


class IconTest(unittest.TestCase):

    def setUp(self):
        if machine_name() in ['tsa']:
            self.skipTest()
    
    def test_install_nwp_cpu(self):
        spack_install('icon @nwp %nvhpc icon_target=cpu')

    def test_install_nwp_gpu(self):
        spack_install('icon @nwp icon_target=gpu')

    def test_install_nwp_all_deps(self):
        """Triggers conditional dependencies"""

        spack_install('--test=root icon @nwp icon_target=gpu serialize_mode=create +eccodes +claw')


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
    unittest.main()
