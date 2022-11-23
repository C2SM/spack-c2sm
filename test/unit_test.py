import unittest
import sys
import os
from pathlib import Path

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')
sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, Markdown


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
            Markdown.table([['title1', 'title2'], ['data1', 'data2'],
                            ['data3', 'data4']]),
            'title1 | title2\n--- | ---\ndata1 | data2\ndata3 | data4')

    def test_collapsible(self):
        self.assertEqual(
            Markdown.collapsible('summary', 'details'),
            '<details><summary>summary</summary>details</details>')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        machine_name_from_arg = sys.argv[-1]
        sys.argv = sys.argv[:-1]  # unittest needs this
    unittest.main(verbosity=2)
