import pytest

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')
sys.path.append(os.path.normpath(spack_c2sm_path))
from src import explicit_scope, package_triggers, machine_skips


def pytest_addoption(parser):
    parser.addoption('--machinename', action='store', default='')
    parser.addoption('--scope', action='store', default='')


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.machinename
    if 'machinename' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize('machinename', [option_value])


def pytest_collection_modifyitems(config, items):
    scope = config.getoption("--scope")
    scope = explicit_scope(scope)
    triggers = package_triggers(scope)
    skips = machine_skips(scope)

    out_of_scope_skip = pytest.mark.skip(reason="not in scope")
    for item in items:
        package_inactive = not any(k.lower() in triggers
                                   for k in item.keywords)
        machine_inactive = any(k.lower() in skips for k in item.keywords)
        if package_inactive or machine_inactive:
            item.add_marker(out_of_scope_skip)
