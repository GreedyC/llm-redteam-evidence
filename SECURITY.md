# Security policy

## Supported versions

Only the latest release receives fixes.

## Reporting a vulnerability

Please **don't open a public issue** for security problems. Report them privately through GitHub: on this repository go to **Security → Report a vulnerability**. I'll acknowledge the report within 5 business days and agree a disclosure date with you once a fix is ready.

Useful things to include: the version or commit, the result file that triggers the problem (with any sensitive model output removed), and what you expected to happen.

## Scope

This tool reads red-team results, which contain attack prompts and model responses that may include harmful text, personal data or leaked secrets. Especially relevant reports:

- Text that appears in an output after `--no-excerpts` was used.
- A crafted garak or promptfoo file that causes code execution, writes outside the `--out` folder, or hangs the tool.
- A way to change an evidence file or the summary without breaking its SHA-256 hash.
- A result counted as resisted when the tool's own output marks it as a successful attack.

A red-team test that should map to a control but doesn't is a normal bug: please open an issue.

## Design notes

- Result files are only read, never executed. YAML catalogs are loaded with `yaml.safe_load`.
- Failing prompts and responses are always stored as SHA-256 hashes; text excerpts are optional and truncated.
- The tool makes no network calls and never contacts the model under test.
