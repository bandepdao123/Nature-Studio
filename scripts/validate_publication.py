"""Read-only public-tree guard. Run before publishing through Git OR an API.

Checks scope and explicit sharing metadata, not the truth/privacy of prose.
"""
from pathlib import Path, PurePosixPath
import argparse
import json
import re
import subprocess


def forbidden(path):
    parts = PurePosixPath(path.replace('\\', '/')).parts
    # Installation receipts describe one machine, not a public release manifest.
    # This path rule is shared by the Git/API guard and the package selector.
    local_installation = (len(parts) >= 3 and parts[-3:-1] == ('07-Releases', 'manifests')
                          and bool(re.search(r'(?:^|-)installation(?:-|\.)', parts[-1], re.I))
                          and parts[-1].lower().endswith('.json'))
    return (('04-Productions' in parts and path != '04-Productions/README.md')
            or (bool(parts) and parts[0] == 'tmp')
            or local_installation
            or '.nature-studio' in parts
            or ('05-Memory' in parts and path.lower().endswith('.json'))
            or ('idea-ledger.md' in parts and path != '00-Standards/templates/idea-ledger.md')
            or ('benchmarks' in parts and ('evidence' in parts or parts[-1] in {'captions-raw.json', 'evidence-manifest.json'})))


def is_lesson(path):
    parts = PurePosixPath(path).parts
    return path.startswith('05-Memory/') and path.endswith('.md') and parts[-1] not in {'README.md', 'INDEX.md'}


def metadata(text):
    parts = text.split('---', 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError('Missing JSON lesson metadata')
    data = json.loads(parts[1])
    if not isinstance(data, dict):
        raise ValueError('Lesson metadata must be an object')
    return data


def shareable(text):
    try:
        value = metadata(text).get('publication', {})
        return isinstance(value, dict) and value.get('visibility') == 'public' and value.get('reviewed') is True
    except (ValueError, TypeError):
        return False


def validate_files(files, read):
    files = set(files)
    errors = [f'Private runtime path in public tree: {p}' for p in sorted(files) if forbidden(p)]
    for path in sorted(files):
        if not path.startswith('05-Memory/') or not path.endswith('.md'):
            continue
        try:
            text = read(path).decode('utf-8-sig')
            if is_lesson(path):
                data = metadata(text)
                if not shareable(text):
                    errors.append(f'Lesson not explicitly reviewed for public sharing: {path}')
                if data.get('production_ids'):
                    errors.append(f'Remove private production IDs from public lesson metadata: {path}')
                refs = data.get('evidence', []) + data.get('validation', {}).get('records', [])
                authority = data.get('activation', {}).get('authority')
                if authority:
                    refs.append(authority)
                for ref in refs:
                    target = ref.split('#', 1)[0] if isinstance(ref, str) else ''
                    if target not in files or forbidden(target):
                        errors.append(f'Public lesson requires included, public evidence: {path}: {ref}')
            # Public indexes cannot expose or point to omitted local lesson records.
            for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                if link.startswith(('https:', 'http:', '#', 'mailto:')):
                    continue
                import posixpath
                target = posixpath.normpath(posixpath.join(posixpath.dirname(path), link.split('#', 1)[0]))
                if target not in files or forbidden(target):
                    errors.append(f'Broken/private memory link: {path}: {link}')
        except (ValueError, TypeError, AttributeError, OSError) as exc:
            errors.append(f'{path}: {exc}')
    return {'valid': not errors, 'checked_files': len(files), 'errors': errors}


def validate_git(root, tree=None):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args])
    if tree:
        commit = git('rev-parse', '--verify', tree + '^{tree}').decode().strip()
        files = git('ls-tree', '-r', '--name-only', '-z', commit).decode().split('\0')
        read = lambda path: git('show', commit + ':' + path)
    else:
        files = git('ls-files', '-z').decode().split('\0')
        read = lambda path: git('show', ':' + path)
    return validate_files([p for p in files if p], read)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--tree', help='Validate a commit/tree; default validates the Git index')
    args = parser.parse_args()
    report = validate_git(args.root.resolve(), args.tree)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['valid'] else 1)
