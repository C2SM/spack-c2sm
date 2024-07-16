import getpass
import os
import subprocess
import time
from pathlib import Path

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

from .machine import machine_name
from .format import time_format, sanitized_filename


def log_with_spack(command: str,
                   test_category: str,
                   log_filename: str = None,
                   cwd=None,
                   env=None,
                   allow_srun=False,
                   uenv=None) -> None:
    """
    Executes the given command while spack is loaded and writes the output into the log file.
    If log_filename is None, command is used to create one.
    """
    filename = sanitized_filename(log_filename or command) + '.log'
    log_file = Path(
        spack_c2sm_path) / 'log' / machine_name() / test_category / filename

    # Setup spack env
    spack_env = f'. {spack_c2sm_path}/setup-env.sh'
    if uenv:
        spack_env += ' /user-environment'

    # Only use srun as Jenkins user and on machines where it is available
    use_srun = allow_srun and getpass.getuser() == 'jenkins' and machine_name(
    ) in ['daint', 'tsa']

    uenv_args = ''
    if uenv:
        uenv_mount_point = f'{uenv}:/user-environment'
        if use_srun:
            uenv_args = '--uenv=' + uenv_mount_point
        else:
            uenv_args = 'squashfs-mount ' + uenv_mount_point + ' -- '

    # Distribute work with 'srun'
    if use_srun:
        # The '-c' argument should be in sync with
        # sysconfig/<machine>/config.yaml config:build_jobs for max efficiency

        srun = {
            'daint': 'srun -t 02:00:00 -C gpu -A g110 -c 12 -n 1',
            'tsa': 'srun -t 02:00:00 -c 6',
        }[machine_name()]
    else:
        srun = ''

    # Make Directory
    log_file.parent.mkdir(exist_ok=True, parents=True)

    # Log machine name and command
    with log_file.open('a') as f:
        f.write(machine_name())
        f.write('\n')
        if uenv:
            f.write(f'uenv: {uenv}')
            f.write('\n')
        f.write(command)
        f.write('\n\n')

    env_activate = f'spack env activate -d {env};' if env else ''
    start = time.time()
    # The output is streamed as directly as possible to the log_file to avoid buffering and potentially losing buffered content.
    # '2>&1' redirects stderr to stdout.
    ret = subprocess.run(
        f'({srun} {uenv_args} bash -c "{spack_env}; {env_activate} {command}") >> {log_file} 2>&1',
        cwd=cwd,
        check=False,
        shell=True)
    end = time.time()

    # Log time and success
    with log_file.open('a') as f:
        f.write('\n\n')
        f.write(time_format(end - start))
        f.write('\n')
        f.write('OK' if ret.returncode == 0 else 'FAILED')
        f.write('\n')

    ret.check_returncode()
