import unittest
import pytest
import sys
import os
from pathlib import Path

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')
sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, Markdown, HTML, time_format, sanitized_filename, all_machines, all_packages, explicit_scope, package_triggers

from src.upstream import *


class MachineDetection(unittest.TestCase):

    @unittest.skipUnless(__name__ == '__main__' and len(sys.argv) > 1,
                         'needs machine_name_from_arg')
    def test_machine_name(self):
        self.assertEqual(machine_name(), machine_name_from_arg)


class MarkDownTest(unittest.TestCase):

    def test_ordered_list(self):
        self.assertEqual(Markdown.ordered_list(['a', 'b']), '1. a\n2. b')

    def test_unordered_list(self):
        self.assertEqual(Markdown.unordered_list(['a', 'b']), '* a\n* b')

    def test_link(self):
        self.assertEqual(Markdown.link('text', 'url'), '[text](url)')

    def test_image(self):
        self.assertEqual(Markdown.image('text', 'url'), '![text](url)')

    def test_inline_code(self):
        self.assertEqual(Markdown.inline_code('code'), '`code`')

    def test_code(self):
        self.assertEqual(Markdown.code('code'), '```\ncode\n```')
        self.assertEqual(Markdown.code('code', 'language'),
                         '```language\ncode\n```')

    def test_table(self):
        self.assertEqual(
            Markdown.table(['title1', 'title2'],
                           [['data1', 'data2'], ['data3', 'data4']]),
            'title1 | title2\n--- | ---\ndata1 | data2\ndata3 | data4')


class HTMLTest(unittest.TestCase):

    def test_link(self):
        self.assertEqual(HTML.link('text', 'url'), '<a href="url">text</a>')

    def test_table(self):
        self.assertEqual(
            HTML.table(['title1', 'title2'],
                       [['data1', 'data2'], ['data3', 'data4']]),
            '<table><thead><tr><th>title1</th><th>title2</th></tr></thead><tbody><tr><td>data1</td><td>data2</td></tr><tr><td>data3</td><td>data4</td></tr></tbody></table>'
        )

    def test_collapsible(self):
        self.assertEqual(
            HTML.collapsible('summary', 'details'),
            '<details><summary>summary</summary>details</details>')


class TimeFormatTest(unittest.TestCase):

    def test_seconds_only(self):
        self.assertEqual(time_format(1), '1.00s')

    def test_minutes_only(self):
        self.assertEqual(time_format(60), '1m')

    def test_hours_only(self):
        self.assertEqual(time_format(3600), '1h')

    def test_full_combo(self):
        self.assertEqual(time_format(3600 + 23 * 60 + 45.67), '1h 23m 45.67s')


class FilenameSanitizerTest(unittest.TestCase):

    def test_example(self):
        example = 'spack installcosmo --until build --dont-restage --test=root --show-log-on-error -n -v cosmo @6.0 %nvhpc cosmo_target=cpu ~cppdycore ^mpich %nvhpc'

        sanitized = sanitized_filename(example)

        self.assertFalse(' ' in sanitized)
        self.assertFalse('%' in sanitized)
        self.assertEqual(
            sanitized,
            'spack_installcosmo_cosmo_@6.0_nvhpc_cosmo_target=cpu_~cppdycore_^mpich_nvhpc'
        )


class ScopeTest(unittest.TestCase):

    def test_all_packages(self):
        self.assertTrue('icon' in all_packages)

    def test_explicit_scope_1_machine_1_package(self):
        scope = explicit_scope('tsa cosmo')
        self.assertEqual(sorted(scope), sorted(['tsa', 'cosmo']))

    def test_explicit_scope_2_machines_2_packages(self):
        scope = explicit_scope('tsa cosmo daint icon')
        self.assertEqual(sorted(scope),
                         sorted(['tsa', 'daint', 'cosmo', 'icon']))

    def test_explicit_scope_0_machines_1_package(self):
        scope = explicit_scope('cosmo')
        self.assertEqual(sorted(scope), sorted(all_machines + ['cosmo']))

    def test_explicit_scope_0_machines_0_packages(self):
        scope = explicit_scope('launch jenkins')
        self.assertEqual(
            sorted(scope),
            sorted(['launch', 'jenkins'] + all_machines + all_packages))

    def test_explicit_scope_allows_unknowns(self):
        scope = explicit_scope('launch jenkins tsa cosmo')
        self.assertEqual(sorted(scope),
                         sorted(['launch', 'jenkins', 'tsa', 'cosmo']))

    def test_package_triggers(self):
        triggers = package_triggers(['cosmo-dycore'])
        self.assertTrue('CosmoDycoreTest'.lower()
                        in triggers)  # Name of TestCase included
        self.assertTrue('test_cosmo_dycore'.lower()
                        in triggers)  # Name of Test included


class UpstreamTest(unittest.TestCase):

    @unittest.expectedFailure
    def test_non_existent_spack_yaml(self):
        read_upstream_from_spack_yaml('/inexistent_path/to_yaml')

    def test_upstream_from_config(self):
        upstream_base = read_upstream_from_spack_yaml(
            os.path.join(os.path.normpath(spack_c2sm_path),
                         'upstreams/daint/base'))
        self.assertEqual('/project/g110/spack/upstream/daint_v0.18.1.5/base',
                         upstream_base)

    def test_upstream_from_another_tag(self):
        upstream_base = os.path.join(os.path.normpath(spack_c2sm_path),
                                     'upstreams/daint/base')
        self.assertEqual('/project/g110/spack/upstream/daint_v0.18.1.4/base',
                         upstream_from_another_tag(upstream_base, 'v0.18.1.4'))

    def test_current_tag(self):
        current_tag()

    def test_git_version(self):
        git_version()

    def test_current_commit(self):
        current_commit()

    @unittest.skipUnless(2000 <= git_version(), 'needs git version > 2.0.0')
    def test_newer_tags(self):
        self.assertGreater(len(newer_tags('v0.18.1.0')), 5)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        machine_name_from_arg = sys.argv[-1]
        sys.argv = sys.argv[:-1]  # unittest needs this
    unittest.main(verbosity=2)
