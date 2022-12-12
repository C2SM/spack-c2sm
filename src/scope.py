all_machines = [
    'tsa', 
    'daint', 
    'balfrin'
    ]
    
all_packages = [
    'cosmo',
    'cosmo-dycore',
    'cosmo-eccodes-definitions',
    'cosmo-grib-api',
    'cosmo-grib-api-definitions',
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
    'xcodeml-tools',
    'zlib_ng',
    ]

def explicit_scope(scope: str) -> list:
    scope = scope.split(' ')

    if not any(x in scope for x in all_machines): 
        scope.extend(all_machines) #no machine means all machines
    if not any(x in scope for x in all_packages):
        scope.extend(all_packages) #no package means all packages
    return scope


def package_triggers(scope: list) -> list:
    active_packages = [x for x in all_packages if x in scope] # intersection
    active_testcases = [x.replace('-', '').replace('_', '') + 'test' for x in active_packages]
    active_tests = ['test_' + x.replace('-', '_') for x in active_packages]
    return active_testcases + active_tests

    
def machine_skips(scope: list) -> list:
    inactive_machines = [x for x in all_machines if x not in scope] # all_machines - scope
    return ['no_' + x for x in inactive_machines]
