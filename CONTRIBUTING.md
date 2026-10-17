# Contributing

Thanks for helping. The most useful contributions are small and concrete.

## Map a red-team test to a control

Tests that match no control are listed as *unmapped* and don't count as evidence. To map one, open a **Test mapping** issue, or add a rule to [`redteam_evidence/catalog.yaml`](redteam_evidence/catalog.yaml):

```yaml
garak:
  - {match: "probe_module.*", controls: [RT-01]}       # garak probe name, shell-style glob
promptfoo:
  plugins:
    - {match: "plugin-id", controls: [RT-05]}          # promptfoo plugin id
  strategies:
    - {match: "strategy-id*", controls: [RT-03]}       # promptfoo delivery strategy
```

Explain in the pull request what the test attacks and why it evidences that control.

## Support a new tool or output format

Add a parser in [`redteam_evidence/parsers.py`](redteam_evidence/parsers.py) that turns the tool's output into `Run` and `TestResult` objects, plus a small test file under `tests/` showing a passing and a failing attempt. Remove any real model output that contains harmful content or personal data.

## Code changes

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

- If your change alters the example data, rerun `python scripts/make_examples.py`. If it alters any output, regenerate the sample with `SOURCE_DATE_EPOCH=1791763200 python -m redteam_evidence demo --out sample-output`. CI fails if either is stale.
- Dependencies: edit `requirements.in`, then regenerate the hash-locked `requirements.txt` with the command at the top of `requirements.in`.
- Security issues: please follow [SECURITY.md](SECURITY.md) instead of opening a public issue.
