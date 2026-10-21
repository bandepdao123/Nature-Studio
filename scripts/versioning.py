"""Read workspace version and propose the next release; never edits files."""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(root=ROOT):
    value = (root / 'VERSION').read_text(encoding='utf-8-sig').strip()
    if not re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', value):
        raise ValueError('VERSION must be MAJOR.MINOR.PATCH, without leading zeros')
    return value


def next_version(value, level='patch'):
    if not re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', value):
        raise ValueError('Invalid version')
    parts = list(map(int, value.split('.')))
    index = {'major': 0, 'minor': 1, 'patch': 2}[level]
    parts[index] += 1
    for i in range(index+1, 3):
        parts[i] = 0
    return '.'.join(map(str, parts))


def check(root=ROOT):
    value = read(root)
    for name in ('README.md', 'START-HERE.md', 'SYSTEM.md', 'CHANGELOG.md'):
        if not re.search(r'(?<![0-9])v' + re.escape(value) + r'(?![0-9.])', (root / name).read_text(encoding='utf-8-sig')):
            raise ValueError(f'{name}: missing current v{value}')
    if not (root / '07-Releases' / f'v{value}.md').is_file():
        raise ValueError('Missing current release notes')
    return value


if __name__ == '__main__':
    import ns_console
    ns_console.utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'next'])
    parser.add_argument('--level', choices=['patch', 'minor', 'major'], default='patch')
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        print(check(args.root) if args.action == 'check' else next_version(read(args.root), args.level))
    except (ValueError, OSError) as exc:
        parser.exit(1, f'{exc}\n')
