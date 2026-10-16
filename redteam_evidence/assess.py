"""Map test results to controls and decide each control's status against its risk tolerance."""
from __future__ import annotations

import math
from collections import Counter, defaultdict
from fnmatch import fnmatchcase
from pathlib import Path

import yaml

from .model import ControlResult, Run, TestResult

_HERE = Path(__file__).parent
CONTROLS: dict = yaml.safe_load((_HERE / 'controls.yaml').read_text(encoding='utf-8'))['controls']
CATALOG: dict = yaml.safe_load((_HERE / 'catalog.yaml').read_text(encoding='utf-8'))


def _matches(rules: list[dict], value: str | None) -> set[str]:
    if not value:
        return set()
    out = set()
    for rule in rules:
        if fnmatchcase(value, rule['match']) and value not in rule.get('unless', []):
            out.update(rule['controls'])
    return out


def controls_for(result: TestResult) -> set[str]:
    if result.tool == 'garak':
        return _matches(CATALOG['garak'], result.test_id)
    if result.tool == 'promptfoo':
        return (_matches(CATALOG['promptfoo']['plugins'], result.test_id)
                | _matches(CATALOG['promptfoo']['strategies'], result.strategy))
    return set()


def wilson_upper(failures: int, n: int, z: float = 1.96) -> float:
    """Upper end of the 95% Wilson interval for the true attack success rate.
    0 failures in 20 attempts still leaves an upper bound of about 16%: a small clean
    sample is weak evidence, and this number says how weak."""
    if n == 0:
        return 1.0
    p = failures / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return min(1.0, (centre + margin) / denom)


def assess(runs: list[Run]) -> tuple[list[ControlResult], Counter]:
    """Returns one result per control (in catalog order) and a count of unmapped test ids."""
    buckets: dict[str, list[TestResult]] = defaultdict(list)
    unmapped: Counter = Counter()
    for run in runs:
        for r in run.results:
            ids = controls_for(r)
            if not ids:
                unmapped[f'{r.tool}:{r.test_id}'] += 1
            for cid in ids:
                buckets[cid].append(r)

    out = []
    for cid, c in CONTROLS.items():
        results = buckets.get(cid, [])
        scored = [r for r in results if not r.errored]
        failing = [r for r in scored if not r.passed]
        n, f = len(scored), len(failing)
        asr = f / n if n else 0.0
        tolerance, min_tests = float(c['max_attack_success_rate']), int(c['min_tests'])
        if n == 0:
            status = 'NOT_TESTED'
        elif asr > tolerance:
            status = 'FAIL'
        elif n < min_tests:
            status = 'INCONCLUSIVE'
        else:
            status = 'PASS'
        by_test: dict[str, dict] = defaultdict(lambda: {'tests': 0, 'failures': 0})
        for r in scored:
            key = f'{r.tool}:{r.test_id}' + (f' [{r.strategy}]' if r.strategy else '')
            by_test[key]['tests'] += 1
            by_test[key]['failures'] += 0 if r.passed else 1
        out.append(ControlResult(
            control_id=cid, title=c['title'], status=status, tests=n, failures=f,
            errors=len(results) - n, attack_success_rate=asr, upper_bound_95=wilson_upper(f, n),
            max_attack_success_rate=tolerance, min_tests=min_tests,
            by_test=dict(sorted(by_test.items())), failing=failing,
        ))
    return out, unmapped
