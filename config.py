#!/usr/bin/env python3

import argparse
import os
import sys
import shutil
import subprocess

dir_path = os.path.dirname(os.path.realpath(__file__))

spack_version = 'v0.17.0'
spack_repo = 'https://github.com/spack/spack.git'


def to_spack_abs_path(path: str) -> str:
    # Spack paths support environment variables and `~` in paths, so we need to handle them separately.
    # (see: https://spack.readthedocs.io/en/latest/configuration.html#config-file-variables )

    # It's enough to check only the start
    # (environment variables in the middle of a path are fine):
    if path.startswith(("$", "~")):
        # We assume environment variables to be absolute.
        # (we can't really fix them anyways, since they could change)
        return path

    # convert to absolute path
    return os.path.realpath(path)


def main():
    parser = argparse.ArgumentParser(
        description=
        'Small config script which can be used to install a spack instance with the correct configuration files and mch spack packages.'
    )
    parser.add_argument(
        '-i',
        '--idir',
        type=str,
        default=dir_path,
        required=True,
        help=
        'Where the Spack instance is installed or you want it to be installed')
    parser.add_argument('-m',
                        '--machine',
                        type=str,
                        required=True,
                        help='Required: machine name')
    parser.add_argument('-u',
                        '--upstreams',
                        type=str,
                        default='ON',
                        choices=('ON', 'OFF'),
                        help='ON or OFF, install upstreams.yaml file')
    parser.add_argument('-v',
                        '--version',
                        type=str,
                        default=spack_version,
                        help='Spack version, Default: ' + spack_version)
    parser.add_argument('-r',
                        '--reposdir',
                        type=str,
                        help='Deprecated and ignored')
    parser.add_argument(
        '-p',
        '--pckgidir',
        type=str,
        help=
        'Define spack package, modules installation directory. Default: admin; /project/g110, non-admin; $SCRATCH'
    )
    parser.add_argument(
        '-s',
        '--stgidir',
        type=str,
        default='$SCRATCH',
        help='Define spack stages directory. Default: $SCRATCH')
    parser.add_argument(
        '-c',
        '--cacheidir',
        type=str,
        default='~/.spack',
        help=
        'Define spack caches (source and misc)  directories. Default:  ~/.spack'
    )
    args = parser.parse_args()

    admin_and_machine = args.machine
    admin = ('admin' in admin_and_machine)
    machine = admin_and_machine.replace('admin-', '')
    spack_dir = args.idir + '/spack'
    spack_etc = args.idir + '/spack/etc/spack/'
    package_install_dir = to_spack_abs_path(
        args.pckgidir or ('/project/g110' if admin else '$SCRATCH'))
    build_stage_dir = to_spack_abs_path(
        args.stgidir) + '/spack-stages/' + admin_and_machine
    cache_dir = to_spack_abs_path(args.cacheidir)

    print("dir_path: " + dir_path)
    print("admin_and_machine: " + admin_and_machine)
    print("machine: " + machine)
    print("spack_dir: " + spack_dir)
    print("spack_etc: " + spack_etc)
    print("package_install_dir: " + package_install_dir)
    print("build_stage_dir: " + build_stage_dir)
    print("cache_dir: " + cache_dir)

    # clone spack
    if not os.path.isdir(spack_dir):
        print('Cloning spack instance to: ' + spack_dir)
        cmd = f'git clone {spack_repo} -b {args.version} {spack_dir}'
        subprocess.run(cmd.split(), check=True)

    print('Installing mch packages & ' + admin_and_machine + ' config files.')

    # install config files to spack_etc
    config_files = [
        'repos.yaml',
        'config.yml',
        machine + '/compilers.yaml',
        machine + '/modules.yaml',
        machine + '/packages.yaml',
    ]
    if args.upstreams == 'ON':
        config_files.append('upstreams.yaml')
    for cfile in config_files:
        shutil.copy(dir_path + '/sysconfigs/' + cfile, spack_etc)

    # install version_detection.py
    shutil.copy(dir_path + '/tools/version_detection.py',
                spack_dir + '/lib/spack/version_detection.py')
    sys.path.insert(1, os.path.join(spack_dir, '/lib/spack/external'))
    from ruamel import yaml

    print('Installing mch packages & ' + admin_and_machine + ' config files.')

    # Config overview:
    #   repos.yaml
    #     repos: $dir_path
    #   config.yaml
    #     config:
    #         install_tree:
    #             root: $package_install_dir/spack-install/$machine
    #         module_roots:
    #             tcl: $package_install_dir/modules/admin-$machine
    #         source_cache: $cache_dir/$machine/source_cache
    #         misc_cache: $cache_dir/$machine/cache
    #         build_stage: $build_stage_dir
    #         extensions: $dir_path/tools/spack-scripting
    #   upstream.yaml
    #     upstreams:
    #       spack-instance-1:
    #         install_tree: /project/g110/spack-install/$machine

    # configure repos.yaml
    file = spack_etc + 'repos.yaml'
    data = yaml.safe_load(open(file, 'r'))
    data['repos'] = [dir_path]
    yaml.safe_dump(data, open(file, 'w'), default_flow_style=False)

    # configure config.yaml
    file = spack_etc + 'config.yaml'
    data = yaml.safe_load(open(file, 'r'))
    data['config']['install_tree']['root'] = (package_install_dir +
                                              '/spack-install/' + machine)
    data['config']['module_roots']['tcl'] = (package_install_dir +
                                             '/modules/' + admin_and_machine)
    data['config']['source_cache'] = (cache_dir + '/' + machine +
                                      '/source_cache')
    data['config']['misc_cache'] = (cache_dir + '/' + machine + '/cache')
    data['config']['build_stage'] = [build_stage_dir]
    data['config']['extensions'] = [dir_path + '/tools/spack-scripting']
    yaml.safe_dump(data, open(file, 'w'), default_flow_style=False)

    # configure upstreams.yaml
    if args.upstreams == 'ON':
        file = spack_etc + 'upstreams.yaml'
        data = yaml.safe_load(open(file, 'r'))
        data['upstreams']['spack-instance-1'][
            'install_tree'] = '/project/g110/spack-install/' + machine
        yaml.safe_dump(data, open(file, 'w'), default_flow_style=False)

    print('Spack successfully installed. \nsource ' + spack_dir +
          '/share/spack/setup-env.sh for setting up the instance.')


if __name__ == "__main__":
    main()
