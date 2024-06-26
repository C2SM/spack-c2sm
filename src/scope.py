import os

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

all_machines = ['balfrin', 'daint', 'tsa']
all_packages = [
    name for name in os.listdir(
        os.path.join(spack_c2sm_path, 'repos/c2sm/packages')) if os.path.isdir(
            os.path.join(spack_c2sm_path, 'repos/c2sm/packages', name))
]
all_packages_underscore = [p.replace('-', '_') for p in all_packages]


def explicit_scope(scope: str) -> list:
    "Adds all packages if none is listed, and all machines if none is listed."

    scope = scope.split(' ')

    if not any(x in scope for x in all_machines):
        scope.extend(all_machines)  #no machine means all machines
    if not any(x in scope for x in all_packages):
        scope.extend(all_packages)  #no package means all packages
    return scope


def package_triggers(scope: list) -> list:
    triggers = []
    for x, y in zip(all_packages, all_packages_underscore):
        if x in scope:
            triggers.append(x)
            triggers.append(y)

    return triggers
