import re

from utils import run_regex

THICK_DIVIDER = \
    '======================================================================'
THIN_DIVIDER = \
    '----------------------------------------------------------------------'


class FailedTestResult(object):

    def __init__(self, raw):
        self.raw = raw
        self.name = None
        self.pid = None
        self.parse()

    def parse(self):
        if not self.raw.strip().startswith(THICK_DIVIDER):
            raise Exception(
                "Received bad test failure text:\n{0}".format(self.raw)
            )
        self.parse_name()
        self.parse_pid()

    def parse_name(self):
        regex = re.compile("FAIL: (\w+) \((.+)\)")
        groups = run_regex(self.raw, regex)
        self.name = "{1}.{0}".format(*groups)

    def parse_pid(self):
        regex = re.compile("Current PID: (\w+)")
        groups = run_regex(self.raw, regex)
        self.pid = groups[0]


class NoseResults(object):
    """
    This parses non-verbose test output from nose, with log capturing on.

    It expects all tests to have failed.
    It expects each test logs its current pid.
    """

    def __init__(self, raw):
        self.raw = raw
        self.n_tests = -1
        self.test_time = -1
        self.failed_tests = []
        self.parse()

    def parse(self):
        head, tail = self.raw.split('\n', 1)
        self.dot_output = head.strip()

        while THICK_DIVIDER in tail:
            head, tail = tail.strip().split('\n\n', 1)
            self.add_failed_test_case(head.strip())

        if not tail.strip().startswith(THIN_DIVIDER):
            raise Exception("Failed to parse nose output")
        self.parse_footer(tail)

    def add_failed_test_case(self, text):
        self.failed_tests.append(FailedTestResult(text))

    def parse_footer(self, footer):
        # parse the "Ran N tests in Xs" portion
        regex = re.compile("Ran (\d+) tests in (.+)s")
        groups = run_regex(footer, regex)
        self.n_tests = int(groups[0])
        self.test_time = float(groups[1])
