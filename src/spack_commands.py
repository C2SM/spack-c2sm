import os
import subprocess
from pathlib import Path

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

from .machine import machine_name


def with_spack(command: str, cwd=None, check=False):
    return subprocess.run(f'. {spack_c2sm_path}/setup-env.sh; {command}',
                          cwd=cwd,
                          check=check,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)


def log_with_spack(command: str, log_file: Path, cwd=None):
    log_file.parent.mkdir(exist_ok=True, parents=True)
    log_file.write_text(f'{machine_name()}: {command}\n\n')

    ret = with_spack(f'{command} >> {log_file} 2>&1', cwd)

    with log_file.open('a') as f:
        f.write('\n\n')
        f.write('OK' if ret.returncode == 0 else 'FAILED')

    return ret
