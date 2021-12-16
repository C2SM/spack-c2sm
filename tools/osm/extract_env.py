#!/usr/bin/env spack-python

import argparse
import os
import shutil
import subprocess
import sys

from spack.spec import Spec
from spack.paths import bin_path


def main():
    parser = argparse.ArgumentParser(
        description=
        '''Deployement script which can be used to install a package that 
                                   depends on cosmo-eccodes-defintions at run time, e.g. cosmo or int2lm.
                                   The spack instance from which the package should be found needs to be sourced first'''
    )
    parser.add_argument(
        '-s',
        '--spec',
        type=str,
        help='Spack spec from which you want to extract the run environement.')
    parser.add_argument('-i',
                        '--idir',
                        type=str,
                        help='Package installation directory')
    parser.add_argument(
        '-j',
        '--idireccodes',
        type=str,
        help='Eccodes installation directory. Default : same locatino as idir')
    parser.add_argument('-f',
                        '--force',
                        action='store_true',
                        help='Overwritte package installation if exists')

    args = parser.parse_args()

    if not args.spec:
        sys.exit(
            'Error: missing -s package spack spec in order to extract the environement!'
        )

    if not args.idir:
        sys.exit(
            'Error: missing -i installation directory for installing the package and eccodes.'
        )
    else:
        args.idir = os.path.abspath(args.idir)

    if not args.idireccodes:
        args.idireccodes = args.idir

    # Extract and concretize cosmo and eccodes
    package_spec = Spec(args.spec).concretized()
    print(package_spec.format('{prefix}'))

    package_name = package_spec.format('{name}')
    package_dir = package_name + package_spec.format(
        '{@version}') + package_spec.format('{%compiler}')
    if package_name == 'cosmo':
        package_dir = package_dir + '-' + package_spec.format(
            '{variants.real_type.value}') + '-' + package_spec.format(
                '{variants.cosmo_target.value}')
    eccodes_dir = 'eccodes' + package_spec.format('{^eccodes.@version}')
    eccodes_definitions_dir = 'cosmo-eccodes-definitions' + package_spec.format(
        '{^cosmo-eccodes-definitions.@version}')

    if os.path.exists(os.path.join(args.idir, package_dir)):
        if args.force:
            # Remove if force cosmo installation already exists
            print('Force : removing existing installation ' +
                  os.path.join(args.idir, package_dir))
            os.system('rm -r ' + os.path.join(args.idir, package_dir))
        else:
            # Exit if cosmo installation already exists
            sys.exit('Error: The installation path: ' +
                     os.path.join(args.idir, package_dir) +
                     ' already exists, use -f to overwrite')
    print('Installing ' + package_spec.format('{prefix}') + ' to: ' +
          os.path.join(args.idir, package_dir))
    print(package_name.upper() + '_INSTALLATION_FULL_PATH=' +
          os.path.join(args.idir, package_dir))
    os.system('cp -rf ' + package_spec.format('{prefix}') + ' ' +
              os.path.join(args.idir, package_dir))

    # Warning if eccodes installation already exists
    if os.path.exists(os.path.join(args.idireccodes, eccodes_dir)):
        print('Warning: The eccodes installation path: ' +
              os.path.join(args.idireccodes, eccodes_dir) +
              ' already exists, keep existing')
    else:
        print('Installing ' + package_spec.format('{^eccodes.prefix}') +
              ' to: ' + os.path.join(args.idireccodes, eccodes_dir))
        print('ECCODES_INSTALLATION_FULL_PATH=' +
              os.path.join(args.idireccodes, eccodes_dir))
        os.system('cp -rf ' + package_spec.format('{^eccodes.prefix}') + ' ' +
                  os.path.join(args.idireccodes, eccodes_dir))

    # Warning if eccodes definitions installation already exists
    if os.path.exists(os.path.join(args.idireccodes, eccodes_definitions_dir)):
        print('Warning: The eccodes-definitions installation path: ' +
              os.path.join(args.idireccodes, eccodes_definitions_dir) +
              ' already exists, keep existing')
    else:
        print('Installing ' +
              package_spec.format('{^cosmo-eccodes-definitions.prefix}') +
              ' to: ' +
              os.path.join(args.idireccodes, eccodes_definitions_dir))
        print('ECCODES_DEFINITIONS_INSTALLATION_FULL_PATH=' +
              os.path.join(args.idireccodes, eccodes_definitions_dir))
        os.system('cp -rf ' +
                  package_spec.format('{^cosmo-eccodes-definitions.prefix}') +
                  ' ' +
                  os.path.join(args.idireccodes, eccodes_definitions_dir))

    with open('run-env', 'w') as outfile:
        subprocess.run(['spack load --sh ' + args.spec],
                       shell=True,
                       stdout=outfile)

    with open('run-env', 'r') as outfile:
        filedata = outfile.read()
        newdata = filedata.replace(package_spec.format('{prefix}'),
                                   os.path.join(args.idir, package_dir))
        newdata = newdata.replace(package_spec.format('{^eccodes.prefix}'),
                                  os.path.join(args.idireccodes, eccodes_dir))
        newdata = newdata.replace(
            package_spec.format('{^cosmo-eccodes-definitions.prefix}'),
            os.path.join(args.idireccodes, eccodes_definitions_dir))
        newdata = newdata.replace(bin_path + ':', '')

    with open('run-env', 'w') as outfile:
        outfile.write(newdata)

    print('Installing run-env file to: ' +
          os.path.join(args.idir, package_dir))
    os.system('mv run-env ' + os.path.join(args.idir, package_dir))


if __name__ == "__main__":
    main()
