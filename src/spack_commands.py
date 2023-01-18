import getpass
import os
import subprocess
import time
from pathlib import Path
from random import randint

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

from .machine import machine_name
from .format import time_format, sanitized_filename


def with_srun(command: str) -> str:
    "Wraps command in 'srun' with machine specific arguments."

    # '-c' should be in sync with sysconfig/<machine>/config.yaml config:build_jobs
    cmd = {
        'balfrin': 'srun -t 02:00:00 -c 12 --partition=normal,postproc',
        'daint': 'srun -t 02:00:00 -C gpu -A g110',
        'tsa': 'srun -t 02:00:00 -c 6',
    }[machine_name()]
    return f'{cmd} sh -c"{command}"'


def rnd_delay(command: str):
    "Delays execution of command."
    # Randomly delay
    time = randint(0, 30)
    return f'sleep {time}; {command}'


def with_spack(command: str, cwd=None, check=False):
    return subprocess.run(f'. {spack_c2sm_path}/setup-env.sh; {command}',
                          cwd=cwd,
                          check=check,
                          shell=True)


def log_with_spack(command: str,
                   test_category: str,
                   log_filename: str = None,
                   cwd=None,
                   srun=False) -> None:
    """
    Executes the given command while spack is loaded and writes the output into the log file.
    If log_filename is None, command is used to create one.
    """
    log_file = Path(spack_c2sm_path) / 'log' / machine_name() / test_category / (sanitized_filename(log_filename or command) + '.log')

    # WORKAROUND: To avoid race conditions on spack locks.
    command = rnd_delay(command)
    
    # Only jenkins starts sruns
    if srun and getpass.getuser() == 'jenkins':
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
    ret = with_spack(f'({command}) >> {log_file} 2>&1', cwd)
    end = time.time()

    with log_file.open('a') as f:
        f.write('\n\n')
        f.write(time_format(end - start))
        f.write('\n')
        f.write('OK' if ret.returncode == 0 else 'FAILED')
        f.write('\n')

    ret.check_returncode()
