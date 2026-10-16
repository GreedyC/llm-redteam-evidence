"""Normalized red-team results. garak and promptfoo outputs are parsed into these
classes so mapping and scoring never depend on which tool produced a result."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TestResult:
    """One attack attempt against the model and whether the model withstood it."""
    __test__ = False                 # not a pytest test class, despite the name
    tool: str                     # garak | promptfoo
    test_id: str                  # garak probe ("promptinject.HijackHateHumans") or promptfoo plugin ("pii:direct")
    passed: bool                  # True = the model resisted the attack
    strategy: str | None = None   # promptfoo delivery strategy (jailbreak, base64, crescendo, ...)
    detector: str | None = None   # what judged the output (garak detector, promptfoo grader)
    prompt: str = ''
    response: str = ''
    reason: str = ''              # grader's explanation, when the tool gives one
    attempt_id: str = ''
    errored: bool = False         # the attempt never got a scorable answer; excluded from rates


@dataclass
class Run:
    """One tool output file."""
    tool: str
    tool_version: str
    target: str                   # model / application under test, as the tool recorded it
    started: str
    source_file: str
    source_sha256: str            # hash of the raw file bytes, so the evidence ties to the exact tool output
    results: list[TestResult] = field(default_factory=list)


@dataclass
class ControlResult:
    control_id: str
    title: str
    status: str                   # PASS | FAIL | INCONCLUSIVE | NOT_TESTED
    tests: int
    failures: int
    errors: int
    attack_success_rate: float    # failures / tests
    upper_bound_95: float         # Wilson 95% upper bound on the true attack success rate
    max_attack_success_rate: float
    min_tests: int
    by_test: dict[str, dict] = field(default_factory=dict)   # test_id -> {tests, failures}
    failing: list[TestResult] = field(default_factory=list)
