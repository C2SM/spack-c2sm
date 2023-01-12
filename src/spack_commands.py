import getpass
import os
import subprocess
import time
from pathlib import Path

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

from .machine import machine_name
from .format import time_format, sanitized_filename


def with_srun(command: str) -> str:
    "Wraps command in 'srun' with machine specific arguments."

    cmd = {
        'balfrin': 'srun -t 02:00:00',
        'daint': 'srun -C gpu -A g110 -t 02:00:00',
        'tsa': 'srun -c 16 -t 02:00:00',
    }[machine_name()]
    return f'{cmd} {command}'


def with_spack_env_dev(command: str, env: str, cwd=None, check=False):
    return subprocess.run(
        f'. {spack_c2sm_path}/setup-env.sh; spack env activate -d {env}; spack develop; {command}',
        cwd=cwd,
        check=check,
        shell=True)


def with_spack(command: str, cwd=None, check=False):
    return subprocess.run(f'. {spack_c2sm_path}/setup-env.sh; {command}',
                          cwd=cwd,
                          check=check,
                          shell=True)


def log_with_spack(command: str,
                   test_category: str,
                   log_filename: str = None,
                   cwd=None,
                   env=None,
                   srun=False) -> None:
    """
    Executes the given command while spack is loaded and writes the output into the log file.
    If log_filename is None, command is used to create one.
    """
    log_file = Path(spack_c2sm_path) / 'log' / machine_name(
    ) / test_category / (sanitized_filename(log_filename or command) + '.log')

    if srun and getpass.getuser(
    ) == 'jenkins':  #  only jenkins should start sruns
        command = with_srun(command)

    # Make Directory
    log_file.parent.mkdir(exist_ok=True, parents=True)

    with log_file.open('a') as f:
        f.write(machine_name())
        f.write('\n')
        f.write(command)
        f.write('\n\n')

    start = time.time()
    # The output of the command is streamed as directly as possible to the log_file to avoid buffering and potentially losing buffered content.
    # '2>&1' redirects stderr to stdout.
    if env:
        ret = with_spack_env_dev(f'({command}) >> {log_file} 2>&1', env, cwd)
    else:
        ret = with_spack(f'({command}) >> {log_file} 2>&1', cwd)
    end = time.time()

    with log_file.open('a') as f:
        f.write('\n\n')
        f.write(time_format(end - start))
        f.write('\n')
        f.write('OK' if ret.returncode == 0 else 'FAILED')
        f.write('\n')

    ret.check_returncode()
