#!/usr/bin/env spack-python

import sys
import os
import ast

from spack.spec import Spec
import spack.build_environment as build_environment

def main():  
    spack_spec = Spec(' '.join(sys.argv[1:]))
    spack_spec.concretize()

    build_environment.setup_package(spack_spec.package, False)
    
    env_file = open("env.txt","w+")

    env_file.write('export _LMFILES_=' + os.environ['_LMFILES_'] + '\n')
    env_file.write('export LOADEDMODULES=' + os.environ['LOADEDMODULES'] + '\n')

    run_env_variables = {}
    try: 
        run_env_variables = ast.literal_eval(os.environ['SPACK_RUN_ENV'])
        for key in run_env_variables:
            env_file.write('export ' + key + '=' + run_env_variables[key] + '\n')
    except:
        print('Warning: missing SPACK_RUN_ENV variable for this package')

    env_file.close()

if __name__ == "__main__":
      main()
