# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import os

import llnl.util.tty as tty

import spack.config
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.repo
from spack.stage import DIYStage
from spack.spec import Spec
from spack.cmd.dev_build import dev_build

description = "Dev-build cosmo and dycore with or without testing."
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['jobs'])
    subparser.add_argument(
        '-d', '--source-path', dest='source_path', default=None,
        help="path to source directory. defaults to the current directory")
    subparser.add_argument(
        '-i', '--ignore-dependencies', action='store_true', dest='ignore_deps',
        help="don't try to install dependencies of requested packages")
    arguments.add_common_arguments(subparser, ['no_checksum'])
    subparser.add_argument(
        '--keep-prefix', action='store_true',
        help="do not remove the install prefix if installation fails")
    subparser.add_argument(
        '--skip-patch', action='store_true',
        help="skip patching for the developer build")
    subparser.add_argument(
        '-q', '--quiet', action='store_true', dest='quiet',
        help="do not display verbose build output while installing")
    subparser.add_argument(
        '-u', '--until', type=str, dest='until', default=None,
        help="phase to stop after when installing (default None)")
    subparser.add_argument(
        '-t', '--test', action='store_true', help="Dev-build with testing")
    subparser.add_argument(
        '-c', '--clean_build', action='store_true', help="Clean dev-build")
    subparser.add_argument(
        '-w', '--without_dycore', action='store_true', help="Dev-build cosmo but not dycore")

    arguments.add_common_arguments(subparser, ['spec'])

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])


def dev_build_cosmo(self, args):
    # Extract and concretize cosmo_spec
    if not args.spec:
        tty.die("spack dev-build requires a package spec argument.")

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        tty.die("spack dev-build only takes one spec.")

    cosmo_spec = specs[0]
    cosmo_spec.concretize()

    # Set dycore_spec
    if not args.without_dycore:
        dycore_spec = 'cosmo-dycore@dev-build'
    else:
        dycore_spec = 'cosmo-dycore@master'
    dycore_spec += ' real_type=' + cosmo_spec.variants['real_type'].value

    cosmo_serialize_spec = 'cosmo@master%pgi cosmo_target=cpu +serialize ~cppdycore' + ' real_type=' + cosmo_spec.variants['real_type'].value

    base_directory = os.getcwd()
    
    # Clean if needed
    if args.clean_build:
        print('==> cosmo: Cleaning build directory')
        os.chdir(base_directory + '/cosmo/ACC')
        os.system('make clean')
        os.chdir(base_directory)

        if not args.without_dycore:
          print('==> dycore: Cleaning build directory')
          os.chdir(base_directory)
          os.system('rm -rf spack-build')

    if cosmo_spec.satisfies('+cppdycore') and not args.without_dycore:
        # Concretize dycore spec and cosmo_serialize spec
        dycore_spec = Spec(dycore_spec)
        dycore_spec.concretize()
        cosmo_serialize_spec = Spec(cosmo_serialize_spec)
        cosmo_serialize_spec.concretize()
        
        args.spec = str(dycore_spec)
        
        # Dev-build dycore
        os.chdir(base_directory)
        dev_build(self, args)

        serialization_data_path = cosmo_serialize_spec.prefix + '/data'
        
        # Launch dycore tests
        if args.test:
            print('==> cosmo-dycore: Launching dycore tests')

            # Source env
            os.system('source ' + base_directory +'/spack-build-env.txt')

            os.chdir(base_directory + '/spack-build/src/tests/unittests')
            os.system('srun -n 1 -p debug --gres=gpu:1 ./unittests  --gtest_filter=-TracerBindings.TracerVariable')

            os.chdir('gcl_fortran')
            os.system('srun -n 4 -p debug --gres=gpu:4 ./unittests_gcl_bindings')

            os.chdir(base_directory + '/spack-build/src/tests/regression')
            testlist=['cosmo1_cp_test1', 'cosmo-1e_test_1', 'cosmo-1e_test_1_all_off', 'cosmo-1e_test_1_coldpool_uv', 'cosmo-1e_test_1_non_default', 'cosmo-1e_test_1_vdiffm1', 'cosmo7_test_3', 'cosmo7_test_namelist_irunge_kutta2', 'cosmo-2e_test_1', 'cosmo-2e_test_1_coldpools', 'cosmo-2e_test_1_bechtold']
            for test in testlist:
                os.system('srun -n 1 -p debug --gres=gpu:1 ./regression_tests -p ' + serialization_data_path + '/' + dycore_spec.variants['slave'].value + '/' + test + ' --gtest_filter=-DycoreUnittest.Performance')

        args.spec = str(cosmo_spec)
    
    os.chdir(base_directory)
    # Dev-build cosmo
    dev_build(self, args)
    
    # Launch cosmo tests
    if args.test:
        print('==> cosmo: Launching cosmo tests')
        
        # Create data
        os.system(base_directory + '/cosmo/test/testsuite/data')
        os.system('./get_data.sh')
        
        # Source env test
        os.system('source ' + base_directory + '/spack-build-env.txt')

        if '~serialize' in cosmo_spec:
            os.chdir('cosmo/test/testsuite')

            run_testsuite = 'ASYNCIO=ON'
            if cosmo_spec.variants['cosmo_target'].value == 'gpu':
                run_testsuite += ' TARGET=GPU'
            else:
                run_testsuite += ' TARGET=CPU'
            if cosmo_spec.variants['real_type'].value == 'float':
                run_testsuite += ' REAL_TYPE=FLOAT'
            if '~cppdycore' in cosmo_spec:
                run_testsuite += 'JENKINS_NO_DYCORE=ON'
            if cosmo_spec.variants['slave'].value == 'tsa_rh7.7':
                run_testsuite = 'sbatch -W --reservation=rh77 submit.tsa.slurm'
            else:
                run_testsuite = 'sbatch -W submit.' + cosmo_spec.variants['slave'].value + '.slurm'
            
            os.system(run_testsuite)
            cat_testsuite = 'cat testsuite.out'
            os.system(cat_testsuite)
            check_testsuite = './testfail.sh'
            if os.system(check_testsuite) != 0:
                raise ValueError('Testsuite failed.')

        if '+serialize' in cosmo_spec:
            os.chdir('cosmo/ACC')
            get_serialization_data = 'python2 test/serialize/generateUnittestData.py -v -e cosmo_serialize --mpirun=srun >> serialize_log.txt; grep \'Generation failed\' serialize_log.txt | wc -l'
            cat_log = 'cat serialize_log.txt'
            if os.system(get_serialization_data) > 0:
                raise ValueError('Serialization failed.')
            os.system(cat_log)
