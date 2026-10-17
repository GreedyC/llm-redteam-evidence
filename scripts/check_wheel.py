"""Build the wheel without pip and check it ships everything the CLI needs at runtime:
the control and test catalogs, the bundled examples, and the console script."""
import sys
import zipfile
from pathlib import Path

from setuptools import build_meta

dist = Path('dist')
dist.mkdir(exist_ok=True)
wheel = dist / build_meta.build_wheel(str(dist))
names = set(zipfile.ZipFile(wheel).namelist())
required = {
    'redteam_evidence/catalog.yaml',
    'redteam_evidence/controls.yaml',
    'redteam_evidence/examples/README.md',
    'redteam_evidence/examples/v1/garak.v1.report.jsonl',
    'redteam_evidence/examples/v1/promptfoo.v1.json',
    'redteam_evidence/examples/v2/garak.v2.report.jsonl',
    'redteam_evidence/examples/v2/promptfoo.v2.json',
}
missing = sorted(required - names)
entry_points = next((n for n in names if n.endswith('.dist-info/entry_points.txt')), None)
script_ok = entry_points and 'redteam-evidence = redteam_evidence.__main__:main' in \
    zipfile.ZipFile(wheel).read(entry_points).decode()
print(f'{wheel.name}: {len(names)} files')
if missing or not script_ok:
    sys.exit(f'missing from wheel: {missing or ""} {"" if script_ok else "console script"}')
print('wheel contains the catalogs, examples and console script')
