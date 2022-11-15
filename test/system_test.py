import unittest
import os
import subprocess
from ..src import machine_name, spack_install

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


if __name__ == '__main__':
    unittest.main()
