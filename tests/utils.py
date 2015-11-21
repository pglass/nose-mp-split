import logging
import os
import subprocess

TEST_DIR = os.path.join(os.path.dirname(__file__), 'sample')
LOG = logging.getLogger(__name__)


def indent(s):
    indent = "  "
    lines = s.split('\n')
    return indent + "\n{0}".format(indent).join(lines)


def run_cmd(*args):
    cmd = list(args)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    LOG.info('executed `%s`', " ".join(cmd))
    LOG.info(' - exit code %s', p.returncode)
    LOG.info('------- stdout -------\n%s', indent(out))
    LOG.info('------- stderr -------\n%s', indent(err))
    return (out.decode('utf-8'), err.decode('utf-8'), p.returncode)


def run_regex(text, regex):
    LOG.debug("----- scanning the following text -----\n%s", indent(text))
    m = regex.search(text)
    if not m:
        LOG.debug("  regex '%s' failed to match", regex.pattern)
    else:
        groups = m.groups()
        LOG.debug("  parsed %s", groups)
        return groups
