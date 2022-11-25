import sys
import os

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name


def needs_testing(package: str) -> bool:
    if 'jenkins' in sys.argv:
        if 'all' in sys.argv:
            return True
        package_match: bool = (package in sys.argv) or ('all_packages' in sys.argv)
        machine_match: bool = (machine_name() in sys.argv) or ('all_machines' in sys.argv)
        return package_match and machine_match
    return True
