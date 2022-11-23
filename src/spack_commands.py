import os
import subprocess
from pathlib import Path

spack_c2sm_path = os.path.dirname(os.path.realpath(__file__)) + '/..'


def with_spack(command: str, cwd=None, check=False):
    return subprocess.run(f'. {spack_c2sm_path}/setup-env.sh; {command}',
                          cwd=cwd,
                          check=check,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)


def log_with_spack(command: str, log_file: Path, cwd=None):
    log_file.parent.mkdir(exist_ok=True, parents=True)

    with log_file.open('w') as f:
        f.write(command)
        f.write('\n\n')

    ret = with_spack(f'{command} >> {log_file} 2>&1', cwd)

    with log_file.open('a') as f:
        f.write('\n\n')
        f.write('OK' if ret.returncode == 0 else 'FAILED')

    return ret
