#!/usr/bin/env python3

import argparse
import os
import shutil
import socket

spack_c2sm_path = os.path.dirname(os.path.abspath(__file__))
known_systems = [
    f.name for f in os.scandir(f'{spack_c2sm_path}/sysconfigs') if f.is_dir()
]


def get_name():
    """The name of the system, that currently executes this code."""
    try:
        # '/etc/xthostname' exists on all CSCS machines, except for Tsa and Arolla.
        # It contains the machine's name as a string.
        with open('/etc/xthostname') as f:
            return f.readline().strip()
    except Exception:
        pass

    hostname = socket.gethostname()
    for name in known_systems:
        if name in hostname:
            return name

    return 'unknown'


def main():
    parser = argparse.ArgumentParser(description='Installs sysconfigs.')
    name = get_name()
    parser.add_argument('-s',
                        '--system',
                        type=str,
                        default=name,
                        help=f'System name. Default: {name} (auto detected)')
    args = parser.parse_args()

    if args.system not in known_systems:
        print(
            f"ERROR: No compatible sysconfig available. Detected system '{args.system}'."
        )
        return -1

    files = [
        'compilers.yaml',
        'config.yaml',
        'modules.yaml',
        'packages.yaml',
        'upstreams.yaml',
        'repos.yaml',
    ]
    for file in files:
        source = f'{spack_c2sm_path}/sysconfigs/{args.system}/{file}'
        destination = f'{spack_c2sm_path}/spack/etc/spack/{file}'

        # Remove old file
        try:
            os.remove(destination)
        except Exception:
            pass

        # Add new file
        try:
            shutil.copy(source, destination)
        except Exception:
            pass

    # Install version detection
    shutil.copy(f'{spack_c2sm_path}/tools/version_detection.py',
                f'{spack_c2sm_path}/spack/lib/spack/version_detection.py')

    print(f'Spack configured for {args.system}.')


if __name__ == "__main__":
    main()
