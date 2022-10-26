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

def spack_dev_build(package):
    spack(f'dev-build --show-log-on-error {package}')


class IconTest(unittest.TestCase):

    def test_dev_build_benchmark_4_cpu(self):
        subprocess.run('git clone --branch icon22_benchmark_4 --recursive ssh://git@gitlab.dkrz.de/icon/icon-nwp.git', check=True, shell=True)
        subprocess.run('mkdir -p icon-nwp/cpu', check=True, shell=True)
        subprocess.run('touch .dummy_file', cwd='icon-nwp/cpu', check=True, shell=True)
        try:
            spack_dev_build('icon @cpu config_dir=./.. icon_target=cpu', cwd='icon-nwp/cpu')
        finally:
            subprocess.run('rm -rf icon-nwp', check=True, shell=True)

    def test_dev_build_benchmark_4_gpu(self):
        subprocess.run('git clone --branch icon22_benchmark_4 --recursive ssh://git@gitlab.dkrz.de/icon/icon-nwp.git', check=True, shell=True)
        subprocess.run('mkdir -p icon-nwp/gpu', check=True, shell=True)
        subprocess.run('touch .dummy_file', cwd='icon-nwp/gpu', check=True, shell=True)
        try:
            spack_dev_build('icon @gpu config_dir=./.. icon_target=gpu', cwd='icon-nwp/gpu')
        finally:
            subprocess.run('rm -rf icon-nwp', check=True, shell=True)

    # def test_install_nwp_cpu(self):
    #     spack_install('icon @nwp icon_target=cpu')

    # def test_install_nwp_gpu(self):
    #     spack_install('icon @nwp icon_target=gpu')

    # def test_install_nwp_all_deps(self):
    #     "Triggers conditional dependencies"
    #     spack_install(
    #         '--test=root icon @nwp icon_target=gpu serialize_mode=create +eccodes +claw'
    #     )


if __name__ == '__main__':
    unittest.main()
