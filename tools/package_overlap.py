import os

spack = set(os.listdir("./spack/var/spack/repos/builtin/packages"))
spack_c2sm = set(os.listdir("./repos/c2sm/packages"))

for folder in sorted(spack & spack_c2sm):
    print(folder)
