#!/usr/bin/env python3

import argparse
import os
import yaml
import shutil
import subprocess

dir_path = os.path.dirname(os.path.realpath(__file__))

spack_version = 'v0.15.4'
spack_repo = 'git@github.com:spack/spack.git'


def main():
    parser = argparse.ArgumentParser(
        description='Small config script which can be used to install a spack instance with the correct configuration files and mch spack packages.')
    parser.add_argument('-i', '--idir', type=str, default=dir_path,
                        help='Where the Spack instance is installed or you want it to be installed')
    parser.add_argument('-m', '--machine', type=str,
                        help='Required: machine name')
    parser.add_argument('-u', '--upstreams', type=str, default='ON',
                        help='ON or OFF, install upstreams.yaml file')
    parser.add_argument('-v', '--version', type=str, default=spack_version,
                        help='Spack version, Default: ' + spack_version)
    parser.add_argument('-r', '--reposdir', type=str,
                        help='repos.yaml install directory')
    parser.add_argument('-p', '--pckgidir', type=str,
                        help='Define spack package, modules installation directory. Default: tsa; /scratch/$USER/spack, daint; /scratch/snx3000/$USER/spack')
    parser.add_argument('-s', '--stgidir', type=str,
                        help='Define spack stages directory. Default: tsa; /scratch/$USER/spack, daint; /scratch/snx3000/$USER/spack')
    parser.add_argument('-c', '--cacheidir', type=str,
                        help='Define spack caches (source and misc)  directories. Default:  ~/.spack/machine/source_cache and ~/.spack/machine/cache')
    args = parser.parse_args()

    if args.upstreams != 'OFF' and args.upstreams != 'ON':
        print('Upstreams must be set to ON or OFF!')
        exit()

    if not args.machine:
        print('Error: machine name required!')
        exit()

    if args.idir:
        if not os.path.isdir(args.idir + '/spack'):
            print('Cloning spack instance to: ' + args.idir)
            if args.version is None:
                args.version = spack_version
            os.system('git clone {repo} -b {branch} {dest_dir}'.format(
                repo=spack_repo, branch=args.version, dest_dir=os.path.join(args.idir, 'spack')))
            print('Installing custom dev-build command')
            shutil.copy('./tools/spack-scripting/scripting/cmd/dev_build.py',
                        args.idir + '/spack/lib/spack/spack/cmd/')
    print('Installing mch packages & ' + args.machine + ' config files')

    if not args.reposdir:
        args.reposdir = args.idir + '/spack/etc/spack'

    # installing repos.yaml
    if not os.path.isdir(args.reposdir):
        raise OSError(
            "repository directory requested with -r does not exists: "+args.reposdir)

    print('Installing repos.yaml on ' + args.reposdir)
    shutil.copy(dir_path + '/sysconfigs/repos.yaml', args.reposdir)
    reposfile = os.path.join(args.reposdir, 'repos.yaml')
    repos_data = yaml.safe_load(open(reposfile, 'r'))
    repos_data['repos'] = [dir_path]
    yaml.safe_dump(repos_data, open(reposfile, 'w'), default_flow_style=False)

    # configure config.yaml

    # copy config.yaml file in site scope of spack instance
    configfile = args.idir + '/spack/etc/spack' + '/config.yaml'

    shutil.copy('sysconfigs/' + args.machine.replace('admin-', '') +
                '/config.yaml', configfile)

    config_data = yaml.safe_load(open(configfile, 'r'))

    if not args.pckgidir:
        if 'admin' in args.machine:
            args.pckgidir = '/project/g110'
        else:
            args.pckgidir = '$SCRATCH'

    if not args.stgidir:
        args.stgidir = '$SCRATCH'

    if not args.cacheidir:
        args.cacheidir = '~/.spack'
    config_data['config']['install_tree'] = args.pckgidir + \
        '/spack-install/' + args.machine.replace('admin-', '')
    config_data['config']['source_cache'] = args.cacheidir + \
        '/' + args.machine.replace('admin-', '') + '/source_cache'
    config_data['config']['misc_cache'] = args.cacheidir + \
        '/' + args.machine.replace('admin-', '') + '/cache'
    config_data['config']['build_stage'] = [
        args.stgidir + '/spack-stages/' + args.machine]
    config_data['config']['module_roots']['tcl'] = args.pckgidir + \
        '/modules/' + args.machine
    config_data['config']['extensions'] = [dir_path + '/tools/spack-scripting']
    yaml.safe_dump(config_data, open(configfile, 'w'),
                   default_flow_style=False)

    # copy modified upstreams.yaml if not admin
    if args.upstreams == 'ON':
        upstreamfile = args.idir + '/spack/etc/spack' + '/upstreams.yaml'
        shutil.copy('sysconfigs/upstreams.yaml', upstreamfile)

        upstreams_data = yaml.safe_load(
            open(upstreamfile, 'r'))
        upstreams_data['upstreams']['spack-instance-1']['install_tree'] = '/project/g110/spack-install/' + \
            args.machine.replace('admin-', '')
        yaml.safe_dump(upstreams_data, open(
            upstreamfile, 'w'), default_flow_style=False)

    # copy modules.yaml, packages.yaml and compiles.yaml files in site scope of spack instance
    config_files = ["compilers.yaml", "modules.yaml", "packages.yaml"]
    for afile in config_files:
        cmd='cp '+dir_path+'/sysconfigs/' + args.machine.replace('admin-',
                                                               '') + '/' + afile+' ' + args.idir + '/spack/etc/spack/'
        subprocess.run(cmd.split(), check=True)

    print('Spack successfully installed. \n source '+args.idir +
          '/spack/share/spack/setup-env.sh for setting up the instance')


if __name__ == "__main__":
    main()
