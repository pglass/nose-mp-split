import os
import unittest

from parse import NoseResults
from utils import run_cmd, TEST_DIR


class TestMeta(unittest.TestCase):

    def test_parse(self):
        test_small = os.path.join(TEST_DIR, 'test_small.py')
        out, err, ret = run_cmd('nosetests', test_small)
        results = NoseResults(err)

        self.assertEqual(results.n_tests, 2)
        self.assertEqual(len(results.failed_tests), 2)
        # we know each test takes at least 2 seconds
        self.assertGreaterEqual(results.test_time, 4)

        names = set([t.name for t in results.failed_tests])
        expected_names = set([
            'sample.test_small.SmallTest.test_small1',
            'sample.test_small.SmallTest.test_small2',
        ])
        self.assertEqual(names, expected_names)

        # all tests should have run in one process
        pids = set([t.pid for t in results.failed_tests])
        self.assertEqual(len(pids), 1)
        self.assertGreater(next(iter(pids)), 1023)
