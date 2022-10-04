#!/usr/bin/python3

# Tests that the command 'SPACK SPEC ...' work.

import os
import unittest

repo_path = os.path.dirname(os.path.realpath(__file__)) + '/../..'


class TestCosmo(unittest.TestCase):

    def test_name(self):
        pass


if __name__ == '__main__':
    unittest.main()
