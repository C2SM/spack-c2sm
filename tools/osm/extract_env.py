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
    parser.add_argument('-idir', '--idir', type=str, help='Installation directory for the installation of cosmo & eccodes.')
    args=parser.parse_args()

    if not args.spec:
        print('Need a cosmo spack spec in order to extract the environement!')

    if not args.idir:
        print('Need an installation directory for installing cosmo and eccodes.')
    else:
        args.idir = os.path.abspath(args.idir)
    
    # Extract and concretize cosmo and eccodes
    cosmo_spec=Spec(args.spec).concretized()
    
    cosmo_dir = 'cosmo' + cosmo_spec.format('{@version}') + cosmo_spec.format('{%compiler}')  + '-' + cosmo_spec.format('{variants.real_type.value}') + '-' + cosmo_spec.format('{variants.cosmo_target.value}')
    eccodes_dir = 'eccodes' + cosmo_spec.format('{^eccodes.@version}') + cosmo_spec.format('{^eccodes.%compiler}')
    eccodes_definitions_dir = 'cosmo-eccodes-definitions' + cosmo_spec.format('{^cosmo-eccodes-definitions.version}') + cosmo_spec.format('{^cosmo-eccodes-definitions.%compiler}')
    
    print('Installing ' + cosmo_spec.format('{prefix}') + ' to: ' + os.path.join(args.idir, cosmo_dir))
    shutil.copytree(cosmo_spec.format('{prefix}'), os.path.join(args.idir, cosmo_dir))

    print('Installing ' + cosmo_spec.format('{^eccodes.prefix}') + ' to: ' + os.path.join(args.idir, eccodes_dir))
    shutil.copytree(cosmo_spec.format('{^eccodes.prefix}'), os.path.join(args.idir, eccodes_dir))

    print('Installing ' + cosmo_spec.format('{^cosmo-eccodes-definitions.prefix}') + ' to: ' + os.path.join(args.idir, eccodes_definitions_dir))
    #shutil.copytree(cosmo_spec.format('{^cosmo-eccodes-definitions.prefix}'), os.path.join(args.idir, eccodes_definitions_dir))
    
    with open(cosmo_dir + '_run-env', 'w') as outfile:
        subprocess.run(['spack', 'load', '--sh', args.spec], stdout=outfile)

    with open(cosmo_dir + '_run-env', 'r') as outfile:
        filedata = outfile.read()
        newdata = filedata.replace(cosmo_spec.format('{prefix}'), os.path.join(args.idir, cosmo_dir))
        newdata = newdata.replace(cosmo_spec.format('{^eccodes.prefix}'), os.path.join(args.idir, eccodes_dir))
        newdata = newdata.replace(cosmo_spec.format('{^cosmo-eccodes-definitions.prefix}'), os.path.join(args.idir, eccodes_definitions_dir))
        newdata = newdata.replace(bin_path + ':', '')

    with open(cosmo_dir + '_run-env', 'w') as outfile:
        outfile.write(newdata)

if __name__ == "__main__":
    main()
