import os
import sys
import pytest

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')
sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, explicit_scope, package_triggers, all_machines


def pytest_configure(config):
    for machine in all_machines:
        config.addinivalue_line(
            'markers', f'no_{machine}: mark test to not run on {machine}')


def pytest_addoption(parser):
    parser.addoption('--scope', action='store', default='')


def pytest_collection_modifyitems(config, items):
    scope = explicit_scope(config.getoption("--scope"))

    triggers = package_triggers(scope)

    for item in items:
        keywords = [k.lower() for k in item.keywords]
        if machine_name() not in scope:
            item.add_marker(pytest.mark.skip(reason="machine not in scope"))
        if f'no_{machine_name()}' in keywords:
            item.add_marker(
                pytest.mark.skip(
                    reason="test is marked to not run on this machine"))
        if not any(k in triggers for k in keywords):
            item.add_marker(pytest.mark.skip(reason="test not in scope"))
