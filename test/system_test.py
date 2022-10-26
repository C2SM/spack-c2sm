import unittest
import os
import subprocess

spack_c2sm_path = os.path.dirname(os.path.realpath(__file__)) + '/..'


def spack(command):
    subprocess.run(f'. {spack_c2sm_path}/setup-env.sh; spack {command}',
                   check=True,
                   shell=True)


def spack_install(package):
    spack(f'install --show-log-on-error {package}')


class IconTest(unittest.TestCase):

    def test_install_nwp_cpu(self):
        spack_install('icon @nwp icon_target=cpu')

    def test_install_nwp_gpu(self):
        spack_install('icon @nwp icon_target=gpu')

    def test_install_nwp_all_deps(self):
        "Triggers conditional dependencies"
        spack_install(
            '--test=root icon @nwp icon_target=gpu serialize_mode=create +eccodes +claw'
        )


if __name__ == '__main__':
    unittest.main()
