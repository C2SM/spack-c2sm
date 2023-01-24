all_machines = ['balfrin', 'daint', 'tsa']

all_packages = [
    'clang-format',
    'cosmo',
    'cosmo-dycore',
    'cosmo-eccodes-definitions',
    'dawn',
    'dawn4py',
    'dusk',
    'flexpart-ifs',
    'gridtools',
    'icon',
    'icontools',
    'int2lm',
    'libgrib1',
    'oasis',
    'omni-xmod-pool',
    'omnicompiler',
    'py-black',
    'py-boltons',
    'py-cytoolz',
    'py-devtools',
    'py-editables',
    'py-factory-boy',
    'py-fprettify',
    'py-frozendict',
    'py-gridtools-cpp',
    'py-gt4py',
    'py-hatchling',
    'py-icon4py',
    'py-inflection',
    'py-lark',
    'py-pathspec',
    'py-pytest-factoryboy',
    'py-toolz',
    'py-typing-extensions',
    'xcodeml-tools',
    'zlib_ng',
]


def explicit_scope(scope: str) -> list:
    "Adds all packages if none is listed, and all machines if none is listed."

    scope = scope.split(' ')

    if not any(x in scope for x in all_machines):
        scope.extend(all_machines)  #no machine means all machines
    if not any(x in scope for x in all_packages):
        scope.extend(all_packages)  #no package means all packages
    return scope


def package_triggers(scope: list) -> list:
    """
    Transforms ['package-name'] to ['packagenametest', 'test_package_name']
    so they match with the naming convenction of testcases and tests.
    """

    active_packages = [x for x in all_packages if x in scope]  # intersection
    active_testcases = [
        x.replace('-', '').replace('_', '') + 'test' for x in active_packages
    ]
    active_tests = ['test_' + x.replace('-', '_') for x in active_packages]
    return active_testcases + active_tests
