# Example results (synthetic)

These files are **synthetic**. They follow the structure of real garak `report.jsonl` and promptfoo results JSON so the tool can be demonstrated without running attacks against a live model, but no model produced them:

- Every prompt and response is written in [`scripts/make_examples.py`](../../scripts/make_examples.py), and CI checks that the files match the generator exactly.
- Harmful content is replaced with placeholders such as `[harmful output withheld from this example]`.
- Names, emails and phone numbers are reserved example values (`example.com`, `555-01xx`).

The scenario is a fictional **Acme Support Assistant**:

| Folder | What it represents |
|---|---|
| [`v1/`](v1) | The approved release. Passes every control it was tested on, but bias (RT-10) was never tested. |
| [`v2/`](v2) | A cheaper model with a shortened system prompt. It leaks its system prompt and customer data, jailbreaks more easily, hallucinates less, and adds bias tests. Two promptfoo attempts timed out. |

To assess a real system, run garak or promptfoo against it and point `redteam-evidence assess` at their output instead.
