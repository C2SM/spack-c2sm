#!/usr/bin/env python3

import argparse
import os
import sys
import shutil
import subprocess

spack_c2sm_path = os.path.dirname(os.path.realpath(__file__))

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
        default=spack_c2sm_path,
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
                        help='repos.yaml install directory')
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
    spack_etc = args.idir + '/spack/etc/spack'
    package_install_dir = to_spack_abs_path(
        args.pckgidir or ('/project/g110' if admin else '$SCRATCH'))
    build_stage_dir = to_spack_abs_path(
        args.stgidir) + '/spack-stages/' + admin_and_machine
    cache_dir = to_spack_abs_path(args.cacheidir)

    print("spack_c2sm_path: " + spack_c2sm_path)
    print("admin_and_machine: " + admin_and_machine)
    print("machine: " + machine)
    print("spack_dir: " + spack_dir)
    print("spack_etc: " + spack_etc)
    print("package_install_dir: " + package_install_dir)
    print("build_stage_dir: " + build_stage_dir)
    print("cache_dir: " + cache_dir)

    if not os.path.isdir(spack_dir):
        print('Cloning spack instance to: ' + spack_dir)
        cmd = 'git clone {repo} -b {branch} {dest_dir}'.format(
            repo=spack_repo, branch=args.version, dest_dir=spack_dir)
        subprocess.run(cmd.split(), check=True)

    shutil.copy('./tools/version_detection.py',
                spack_dir + '/lib/spack/version_detection.py')
    sys.path.insert(1, os.path.join(spack_dir, 'lib/spack/external'))
    from ruamel import yaml

    print('Installing mch packages & ' + admin_and_machine + ' config files.')

    if not args.reposdir:
        args.reposdir = spack_etc

    # installing repos.yaml
    if not os.path.isdir(args.reposdir):
        raise OSError(
            "repository directory requested with -r does not exists: " +
            args.reposdir)

    print('Installing repos.yaml on ' + args.reposdir)
    shutil.copy(spack_c2sm_path + '/sysconfigs/repos.yaml', args.reposdir)
    reposfile = os.path.join(args.reposdir, 'repos.yaml')
    repos_data = yaml.safe_load(open(reposfile, 'r'))
    repos_data['repos'] = [spack_c2sm_path]
    yaml.safe_dump(repos_data, open(reposfile, 'w'), default_flow_style=False)

    # configure config.yaml

    # copy config.yaml file in site scope of spack instance
    configfile = spack_etc + '/config.yaml'

    shutil.copy('sysconfigs/' + machine + '/config.yaml', configfile)

    config_data = yaml.safe_load(open(configfile, 'r'))

    config_data['config']['install_tree']['root'] = (package_install_dir +
                                                     '/spack-install/' +
                                                     machine)
    config_data['config']['source_cache'] = (cache_dir + '/' + machine +
                                             '/source_cache')
    config_data['config']['misc_cache'] = (cache_dir + '/' + machine +
                                           '/cache')
    config_data['config']['build_stage'] = [
        build_stage_dir + '/spack-stages/' + admin_and_machine
    ]
    config_data['config']['module_roots']['tcl'] = (package_install_dir +
                                                    '/modules/' +
                                                    admin_and_machine)
    config_data['config']['extensions'] = [
        spack_c2sm_path + '/tools/spack-scripting'
    ]
    yaml.safe_dump(config_data,
                   open(configfile, 'w'),
                   default_flow_style=False)

    # copy modified upstreams.yaml if not admin
    if args.upstreams == 'ON':
        upstreamfile = spack_etc + '/upstreams.yaml'
        shutil.copy('sysconfigs/upstreams.yaml', upstreamfile)

        upstreams_data = yaml.safe_load(open(upstreamfile, 'r'))
        upstreams_data['upstreams']['spack-instance-1']['install_tree'] = '/project/g110/spack-install/' + \
            machine
        yaml.safe_dump(upstreams_data,
                       open(upstreamfile, 'w'),
                       default_flow_style=False)

    # copy modules.yaml, packages.yaml and compiles.yaml files in site scope of spack instance
    config_files = ["compilers.yaml", "modules.yaml", "packages.yaml"]
    for afile in config_files:
        cmd = 'cp ' + spack_c2sm_path + '/sysconfigs/' + machine + '/' + afile + ' ' + spack_etc + '/'
        subprocess.run(cmd.split(), check=True)

    print('Spack successfully installed. \nsource ' + spack_dir +
          '/share/spack/setup-env.sh for setting up the instance.')


if __name__ == "__main__":
    main()
