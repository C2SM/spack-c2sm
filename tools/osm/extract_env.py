#!/usr/bin/env spack-python

import argparse
import os
import shutil
import subprocess
import sys

from spack.spec import Spec
from spack.paths import bin_path

def main():  
    parser=argparse.ArgumentParser(description='Small config script which can be used to install a spack instance with the correct configuration files and mch spack packages.')
    parser.add_argument('-s', '--spec', type=str, help='Spack spec from which you want to extract the run environement.')
    parser.add_argument('-i', '--idircosmo', type=str, help='Cosmo installation directory.')
    parser.add_argument('-j', '--idireccodes', type=str, help='Eccodes installation directory.')
    
    args=parser.parse_args()

    if not args.spec:
        print('Need a cosmo spack spec in order to extract the environement!')

    if not args.idircosmo:
        print('Need an installation directory for installing cosmo and eccodes.')
    else:
        args.idircosmo = os.path.abspath(args.idircosmo)

    # Extract and concretize cosmo and eccodes
    cosmo_spec=Spec(args.spec).concretized()

    cosmo_dir = 'cosmo' + cosmo_spec.format('{@version}') + cosmo_spec.format('{%compiler}')  + '-' + cosmo_spec.format('{variants.real_type.value}') + '-' + cosmo_spec.format('{variants.cosmo_target.value}')
    eccodes_dir = 'eccodes' + cosmo_spec.format('{^eccodes.@version}')
    eccodes_definitions_dir = 'cosmo-eccodes-definitions' + cosmo_spec.format('{^cosmo-eccodes-definitions.@version}')
    
    # Warning if eccodes installation already exists
    if os.path.exists(os.path.join(args.idircosmo, cosmo_dir)):
        print('Warning: The cosmo installation path: ' + os.path.join(args.idircosmo, cosmo_dir) + ' already exists!')
    print('Installing ' + cosmo_spec.format('{prefix}') + ' to: ' + os.path.join(args.idircosmo, cosmo_dir))
    os.system('cp -rf ' + cosmo_spec.format('{prefix}') + ' ' + os.path.join(args.idircosmo, cosmo_dir))

    # Warning if eccodes installation already exists
    if os.path.exists(os.path.join(args.idireccodes, eccodes_dir)):
        print('Warning: The eccodes installation path: ' + os.path.join(args.idireccodes, eccodes_dir) + ' already exists!')

    print('Installing ' + cosmo_spec.format('{^eccodes.prefix}') + ' to: ' + os.path.join(args.idireccodes, eccodes_dir))
    os.system('cp -rf ' + cosmo_spec.format('{^eccodes.prefix}') + ' ' + os.path.join(args.idireccodes, eccodes_dir))

    # Warning if path is already used
    if os.path.exists(os.path.join(args.idireccodes, eccodes_definitions_dir)):
        print('Warning: The eccodes-definitions installation path: ' +  os.path.join(args.idireccodes, eccodes_definitions_dir) + ' already exists!')

    print('Installing ' + cosmo_spec.format('{^cosmo-eccodes-definitions.prefix}') + ' to: ' + os.path.join(args.idireccodes, eccodes_definitions_dir))
    os.system('cp -rf ' + cosmo_spec.format('{^cosmo-eccodes-definitions.prefix}') + ' ' + os.path.join(args.idireccodes, eccodes_definitions_dir))

    with open(cosmo_dir + '_run-env', 'w') as outfile:
        subprocess.run(['spack', 'load', '--sh', args.spec], stdout=outfile)

    with open(cosmo_dir + '_run-env', 'r') as outfile:
        filedata = outfile.read()
        newdata = filedata.replace(cosmo_spec.format('{prefix}'), os.path.join(args.idircosmo, cosmo_dir))
        newdata = newdata.replace(cosmo_spec.format('{^eccodes.prefix}'), os.path.join(args.idireccodes, eccodes_dir))
        newdata = newdata.replace(cosmo_spec.format('{^cosmo-eccodes-definitions.prefix}'), os.path.join(args.idireccodes, eccodes_definitions_dir))
        newdata = newdata.replace(bin_path + ':', '')

    with open(cosmo_dir + '_run-env', 'w') as outfile:
        outfile.write(newdata)

if __name__ == "__main__":
    main()
