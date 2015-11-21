import unittest

from parse import NoseResults
from utils import run_cmd, TEST_DIR


def run_nose(*args):
    """Run nose against our sample dir of tests."""
    cmd = ['nosetests'] + list(args) + [TEST_DIR]
    _, err, _ = run_cmd(*cmd)
    return NoseResults(err)


class TestSplit(unittest.TestCase):

    TEST_LIST = set([
        'sample.test_large.LargeTest.test_large1',
        'sample.test_large.LargeTest.test_large2',
        'sample.test_large.LargeTest.test_large3',
        'sample.test_large.LargeTest.test_large4',
        'sample.test_large.LargeTest.test_large5',
        'sample.test_large.LargeTest.test_large6',
        'sample.test_small.SmallTest.test_small1',
        'sample.test_small.SmallTest.test_small2',
    ])

    def test_processes_without_split(self):
        results = run_nose('--processes=8', '--process-timeout=60')

        names = set([t.name for t in results.failed_tests])
        self.assertEqual(names, self.TEST_LIST)

        # each test takes 2 seconds. the largest module (test_large) is run
        # entirely in one process and has 6 test cases. So we can't take less
        # time than 2 * 6 = 12 seconds
        self.assertGreater(results.test_time, 12)

        # even though we specified more processes, nose only uses 2 (the total
        # number of classes we have)
        pids = set([t.pid for t in results.failed_tests])
        self.assertEqual(len(pids), 2)

    def test_processes_with_split(self):
        results = run_nose(
            '--processes=8', '--process-timeout=60', '--mp-split-all',
        )

        names = set([t.name for t in results.failed_tests])
        self.assertEqual(names, self.TEST_LIST)

        # we gave the same number of processes as tests.
        # each test takes 2 seconds, so we expect this to finish in about
        # 2 seconds + overhead
        self.assertLess(results.test_time, 3)

        pids = set([t.pid for t in results.failed_tests])
        self.assertEqual(len(pids), 8)
