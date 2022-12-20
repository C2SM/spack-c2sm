import os
import sys
import pytest

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')
sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, explicit_scope, package_triggers, machine_skips, all_machines


def pytest_configure(config):
    for machine in all_machines:
        config.addinivalue_line(
            'markers', f'no_{machine}: mark test to not run on {machine}')


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
    scope = explicit_scope(config.getoption("--scope"))
    
    skips = machine_skips(scope)
    triggers = package_triggers(scope)

    for item in items:
        if machine_name() not in scope:
            item.add_marker(pytest.mark.skip(reason="machine not in scope"))
        if not any(k.lower() in triggers for k in item.keywords):
            item.add_marker(pytest.mark.skip(reason="test not in scope"))
        if any(k.lower() in skips for k in item.keywords):
            item.add_marker(pytest.mark.skip(reason="test is marked to not run on this machine"))
