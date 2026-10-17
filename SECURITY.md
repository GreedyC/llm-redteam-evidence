# Security policy

## Supported versions

Only the latest release receives fixes.

## Reporting a vulnerability

Please **don't open a public issue** for security problems. Report them privately through GitHub's private vulnerability reporting:

**https://github.com/Mihirajmera/llm-redteam-evidence/security/advisories/new**

What to expect:

- **Acknowledgement within 5 business days.**
- **An assessment within 14 days**: whether it's accepted as a vulnerability, its severity, and a planned fix.
- **Coordinated disclosure**: a fix is released and the advisory published together, normally within 90 days of the report. You'll be credited in the advisory unless you'd rather not be.

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
- Dependencies are pinned by hash, GitHub Actions are pinned to commit SHAs, and CodeQL and OpenSSF Scorecard run on every push.
