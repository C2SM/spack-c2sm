import os
import sys

spack = set(os.listdir("./spack/var/spack/repos/builtin/packages"))
spack_c2sm = set(os.listdir("./repos/c2sm/packages"))

overlapping_packages = sorted(spack & spack_c2sm)

if not overlapping_packages:
    print("::notice::No overlapping packages!")
else:
    print("::error::Found overlapping packages between Spack-C2SM and Spack repos")

    print("::group::Overlapping packages")
    for package in overlapping_packages:
        print(package)
    print("::endgroup::")

    sys.exit(1)
