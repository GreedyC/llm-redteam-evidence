from pathlib import Path

import pytest

from redteam_evidence.model import Run, TestResult

EXAMPLES = Path(__file__).resolve().parent.parent / 'redteam_evidence' / 'examples'


def make_run(results, tool='promptfoo'):
    return Run(tool=tool, tool_version='test', target='model-under-test', started='2026-10-01T00:00:00',
               source_file='results.json', source_sha256='0' * 64, results=results)


def attacks(test_id, n, failures=0, tool='promptfoo', strategy=None, errored=0):
    out = [TestResult(tool=tool, test_id=test_id, strategy=strategy, passed=i >= failures,
                      prompt=f'attack {i}', response=f'response {i}', attempt_id=f'{test_id}-{i}')
           for i in range(n)]
    out += [TestResult(tool=tool, test_id=test_id, strategy=strategy, passed=False, errored=True,
                       attempt_id=f'{test_id}-err-{i}') for i in range(errored)]
    return out


@pytest.fixture
def run_factory():
    return make_run


@pytest.fixture
def attack_factory():
    return attacks
