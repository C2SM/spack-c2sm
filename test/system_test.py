import unittest
import pytest
import subprocess
import sys
import os
import uuid
import shutil
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


def spack_install(spec: str, log_filename: str = None):
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

    log_with_spack(f'spack {command} -n -v {spec}',
                   'system_test',
                   log_filename,
                   srun=True)


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
                                   log_filename: str = None,
                                   out_of_source: bool = False):
    """
    Clones ICON with given branch into unique folder, activates the given spack
    environment, tests 'spack install' and writes the output into the log file.
    If log_filename is None, spack_env is used to create one.
    If out_of_source is True, create additional folder and build there, BUT skip testing!
    """

    # in case we use serialbox or another python preprocessor
    devirtualize_env()

    unique_folder = 'icon_' + uuid.uuid4(
    ).hex  # to avoid cloning into the same folder and having race conditions
    subprocess.run(
        f'git clone --depth 1 --recurse-submodules -b {icon_branch} git@github.com:C2SM/icon.git {unique_folder}',
        check=True,
        shell=True)

    # patch spack env
    filename = f'{unique_folder}/{spack_env}/spack.yaml'
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines = [
        line.rstrip() + ' +grib2\n' if 'icon@develop' in line else line
        for line in lines
    ]
    with open(filename, 'w') as file:
        file.writelines(lines)

    log_filename = sanitized_filename(log_filename or spack_env)

    if out_of_source:
        build_dir = os.path.join(unique_folder, 'build')
        os.makedirs(build_dir, exist_ok=True)
        shutil.copytree(os.path.join(unique_folder, 'config'),
                        os.path.join(build_dir, 'config'))
        unique_folder = build_dir
        log_filename = f'{log_filename}_out_of_source'

    # limit number of build-jobs to 4 because no srun used
    log_with_spack('spack install -j 4 --until build -n -v',
                   'system_test',
                   log_filename,
                   cwd=unique_folder,
                   env=spack_env,
                   srun=False)

    # for out-of-source build we can't run tests because required files
    # like scripts/spack/test.py or scripts/buildbot_script are not synced
    # in our spack-recipe to the build-folder
    if not out_of_source:
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


@pytest.mark.no_tsa  # proj-8.2.1 fails with "./.libs/libproj.so: error: undefined reference to 'curl_easy_setopt'"
class CdoTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('cdo')


class ClangFormatTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('clang-format')


class ClawTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('claw')


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
    # TODO: Add the other versions!

    def test_install_version_2_25_0_1(self):
        spack_install_and_test('cosmo-eccodes-definitions @2.25.0.1')

    def test_install_version_2_19_0_7(self):
        spack_install_and_test('cosmo-eccodes-definitions @2.19.0.7')


class DawnTest(unittest.TestCase):
    pass


class Dawn4PyTest(unittest.TestCase):
    pass


class DuskTest(unittest.TestCase):
    pass


class EccodesTest(unittest.TestCase):
    # All the other versions are not the responsibility of spack-c2sm

    def test_install_2_19_0(self):
        spack_install_and_test('eccodes @2.19.0')


@pytest.mark.no_tsa  # Fails with "The C compiler "/scratch-shared/meteoswiss/scratch/jenkins/workspace/Spack/spack_PR/spack/lib/spack/env/nvhpc/nvc" is not able to compile a simple test program."
@pytest.mark.no_daint  # Tests are flaky https://github.com/C2SM/spack-c2sm/issues/779
@pytest.mark.no_balfrin  # Tests are flaky https://github.com/C2SM/spack-c2sm/issues/779
class EckitTest(unittest.TestCase):
    # All the other versions are not the responsibility of spack-c2sm

    def test_install_1_20_0(self):
        spack_install_and_test('eckit @1.20.0')


class FckitTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('fckit')


class FlexpartIfsTest(unittest.TestCase):

    def test_install_latest(self):
        spack_install_and_test('flexpart-ifs @meteoswiss-10')


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
        spack_install_and_test(f'icon @nwp-master %nvhpc +cuda')

    @pytest.mark.no_daint  # libxml2 %nvhpc fails to build
    def test_install_nwp_cpu(self):
        spack_install_and_test(f'icon @nwp-master %nvhpc ~cuda')

    @pytest.mark.no_balfrin  # config file does not exist for this machine
    def test_install_c2sm_test_cpu_gcc(self):
        spack_env_dev_install_and_test(
            'config/cscs/spack/v0.18.1.7/daint_cpu_gcc', 'icon-2.6.6.1')

    @pytest.mark.no_balfrin  # config file does not exist for this machine
    def test_install_c2sm_test_cpu_nvhpc_out_of_source(self):
        spack_env_dev_install_and_test(
            'config/cscs/spack/v0.18.1.7/daint_cpu_nvhpc',
            'icon-2.6.6.1',
            out_of_source=True)

    @pytest.mark.no_balfrin  # config file does not exist for this machine
    def test_install_c2sm_test_cpu(self):
        spack_env_dev_install_and_test(
            'config/cscs/spack/v0.18.1.7/daint_cpu_nvhpc', 'icon-2.6.6.1')

    @pytest.mark.no_balfrin  # config file does not exist for this machine
    def test_install_c2sm_test_gpu(self):
        spack_env_dev_install_and_test(
            'config/cscs/spack/v0.18.1.7/daint_gpu_nvhpc', 'icon-2.6.6.1')

    @pytest.mark.no_balfrin  # config file does not exist for this machine
    def test_install_nwp_test_cpu_cce(self):
        spack_env_dev_install_and_test(
            'config/cscs/spack/v0.18.1.7/daint_cpu_cce', 'cce')


class IconHamTest(unittest.TestCase):
    pass


@pytest.mark.no_tsa  # This test is flaky and sometimes fails with: icondelaunay.cpp:29:10: fatal error: version.c: No such file or directory. See issue #781.
class IconToolsTest(unittest.TestCase):

    def test_install_2_5_2(self):
        spack_install_and_test('icontools @2.5.2')


@pytest.mark.no_tsa  # Not supported on Tsa
@pytest.mark.no_balfrin  # Not supported on Balfrin
class InferoTest(unittest.TestCase):

    def test_install(self):
        spack_install_and_test('infero @0.1.2 %gcc')


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


@pytest.mark.no_tsa  # Test is too expensive. It takes over 5h.
class LibCdiPioTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('libcdi-pio')


@pytest.mark.no_tsa  # Fails "make check"
class LibfyamlTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('libfyaml')


@pytest.mark.no_balfrin  # This fails with "BOZ literal constant at (1) cannot appear in an array constructor". https://gcc.gnu.org/onlinedocs/gfortran/BOZ-literal-constants.html
class LibGrib1Test(unittest.TestCase):

    @pytest.mark.serial_only  # locking problem on Tsa in combination with int2lm
    def test_install_version_22_01_2020(self):
        spack_install_and_test('libgrib1 @22-01-2020')


class LibXml2Test(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('libxml2')


@pytest.mark.no_balfrin  # Package is a workaround, only needed on Daint.
@pytest.mark.no_tsa  # Package is a workaround, only needed on Daint.
class NvidiaBlasTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('nvidia-blas')


@pytest.mark.no_balfrin  # Package is a workaround, only needed on Daint.
@pytest.mark.no_tsa  # Package is a workaround, only needed on Daint.
class NvidiaLapackTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('nvidia-lapack')


@pytest.mark.no_balfrin  # Coupling only needed on Daint
@pytest.mark.no_tsa  # Coupling only needed on Daint
class OasisTest(unittest.TestCase):

    def test_install_master_nvhpc(self):
        spack_install_and_test('oasis @master %nvhpc')


class OmniXmodPoolTest(unittest.TestCase):

    def test_install_version_0_1(self):
        spack_install_and_test('omni-xmod-pool @0.1')


class PyBlackTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-black')


class PyBoltonsTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-boltons')


@pytest.mark.no_balfrin  # Preparing metadata (pyproject.toml): finished with status 'error: metadata-generation-failed'.
class PyCytoolzTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-cytoolz')


class PyDevtoolsTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-devtools')


class PyEditablesTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-editables')


class PyFactoryBoyTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-factory-boy')


class PyFprettifyTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-fprettify')


class PyFrozendictTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-frozendict')


class PyGridtoolsCppTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-gridtools-cpp')


@pytest.mark.no_tsa  # Irrelevant
class PyGt4pyTest(unittest.TestCase):

    def test_install_version_1_1_1(self):
        spack_install_and_test('py-gt4py @1.1.1')


class PyHatchlingTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-hatchling')


@pytest.mark.no_tsa  # py-isort install fails with: No module named 'poetry'.
class PyIcon4pyTest(unittest.TestCase):

    def test_install_0_0_4(self):
        spack_install_and_test('py-icon4py @0.0.4')

    def test_install_version_0_0_3(self):
        spack_install_and_test(
            'py-icon4py @ 0.0.3 %gcc ^py-gt4py@1.1.1 ^python@3.10.4')

    def test_install_version_0_0_4(self):
        spack_install_and_test(
            'py-icon4py @ 0.0.4 %gcc ^py-gt4py@1.1.1 ^python@3.10.4')


class PyInflectionTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-inflection')


class PyLarkTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-lark')


class PyNumpyTest(unittest.TestCase):

    def test_install_default(self):
        spack_install('py-numpy')


class PyPathspecTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-pathspec')


class PyPoetryCoreTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-poetry-core')


class PyPytestTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-pytest')


class PyPytestFactoryboyTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-pytest-factoryboy')


class PySetuptoolsTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-setuptools')


class PyToolzTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-toolz')


class PyTypingExtensionsTest(unittest.TestCase):

    def test_install_default(self):
        spack_install_and_test('py-typing-extensions')


@pytest.mark.no_tsa  # Irrelevant
@pytest.mark.no_balfrin  #Irrelevant
class RttovTest(unittest.TestCase):

    def test_install_version_13_1_gcc(self):
        spack_install_and_test('rttov @13.1 %gcc')

    def test_install_version_13_1_nvhpc(self):
        spack_install_and_test('rttov @13.1 %nvhpc')


@pytest.mark.no_tsa  # Fails with "C compiler cannot create executables"
class ScalesPPMTest(unittest.TestCase):
    # TODO: Add other versions and compilers!

    def test_install_default(self):
        spack_install_and_test('scales-ppm')


class TensorflowCTest(unittest.TestCase):

    def test_install_2_6_0(self):
        spack_install_and_test('tensorflowc @2.6.0')


@pytest.mark.no_tsa  # Fails with "C compiler cannot create executables"
class YaxtTest(unittest.TestCase):
    # TODO: Add other versions and compilers!

    def test_install_default(self):
        spack_install_and_test('yaxt')


class ZLibNGTest(unittest.TestCase):
    # TODO: Add other compilers!

    def test_install_version_2_0_0(self):
        spack_install_and_test('zlib_ng @2.0.0')


if __name__ == '__main__':
    unittest.main(verbosity=2)
