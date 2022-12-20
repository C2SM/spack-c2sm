import os
import subprocess


def machine_name() -> str:
    """Returns the name of the machine this code runs on, or 'unknown'."""

    # Implemented as a wrapper around 'machine.sh'.
    file_dirname = os.path.dirname(os.path.realpath(__file__))
    return subprocess.run(
        f'. {file_dirname}/machine.sh',
        check=True,
        shell=True,
        stdout=subprocess.PIPE).stdout.decode("utf-8").strip()


if __name__ == '__main__':
    print(machine_name())
