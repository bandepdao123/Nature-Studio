"""Build a portable, verified Nature Studio ZIP using only the Python stdlib."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
import zipfile
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {'.nature-studio', '.git', '__pycache__', '.venv', 'node_modules', '.pytest_cache'}
_GUARD_SPEC = importlib.util.spec_from_file_location('publication_guard', ROOT / 'scripts' / 'validate_publication.py')
_GUARD = importlib.util.module_from_spec(_GUARD_SPEC)
_GUARD_SPEC.loader.exec_module(_GUARD)


def included(path):
    rel = path.relative_to(ROOT)
    if _GUARD.forbidden(rel.as_posix()):
        return False
    if _GUARD.is_lesson(rel.as_posix()) and not _GUARD.shareable(path.read_text(encoding='utf-8-sig')):
        return False
    if rel.as_posix() == 'PACKAGE-MANIFEST.json':
        return False  # Replace an extracted package's old manifest with a fresh one.
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if rel.parts[:2] == ('07-Releases', 'packages'):
        return False
    if rel.parts[:2] == ('01-Knowledge', 'benchmarks') and (
            'evidence' in rel.parts[2:] or path.name in {'captions-raw.json', 'evidence-manifest.json'}):
        return False  # Browser UI evidence stays local, outside public distribution.
    name = path.name.lower()
    if name.startswith('.env') and name != '.env.example':
        return False
    if name.startswith(('credentials', 'secrets')) and path.suffix.lower() == '.json':
        return False
    return name not in {'thumbs.db', '.ds_store'} and path.suffix.lower() not in {
        '.pem', '.key', '.pyc', '.pyo', '.tmp', '.log'
    }


def source_git():
    """Record provenance without treating a dirty working tree as a Git snapshot."""
    def git(*args):
        result = subprocess.run(['git', '-C', str(ROOT), *args],
                                capture_output=True, text=True, encoding='utf-8')
        return result.stdout.strip() if result.returncode == 0 else None
    try:
        top = git('rev-parse', '--show-toplevel')
        if not top or Path(top).resolve() != ROOT:
            return {'head': None, 'has_local_changes': None, 'exact_git_snapshot': False}
        head = git('rev-parse', 'HEAD')
        status = git('status', '--porcelain', '--untracked-files=normal')
        dirty = bool(status) if status is not None else None
        return {'head': head, 'has_local_changes': dirty,
                'exact_git_snapshot': bool(head) and dirty is False}
    except FileNotFoundError:
        return {'head': None, 'has_local_changes': None, 'exact_git_snapshot': False}


def build():
    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'\d+\.\d+(?:\.\d+)?', version):
        raise ValueError('VERSION must contain a numeric workspace version such as 1.0.')
    repository = json.loads((ROOT / 'REPOSITORY.json').read_text(encoding='utf-8'))
    expected_url = f"https://github.com/{repository['owner']}/{repository['name']}"
    if repository.get('name_policy') != 'stable' or repository['url'] != expected_url:
        raise ValueError('REPOSITORY.json must describe the stable repository URL.')
    files = sorted(p for p in ROOT.rglob('*') if p.is_file() and included(p))
    by_path = {p.relative_to(ROOT).as_posix(): p for p in files}
    public_check = _GUARD.validate_files(by_path, lambda rel: by_path[rel].read_bytes())
    if not public_check['valid']:
        raise ValueError('Public package rejected: ' + '; '.join(public_check['errors']))
    if any(p.is_symlink() for p in files):
        raise RuntimeError('Resolve symlinks explicitly before packaging.')
    records = [{'path': p.relative_to(ROOT).as_posix(), 'size': p.stat().st_size,
                'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
    manifest = {'format_version': 2, 'workspace': 'Nature-Studio',
                'workspace_version': version,
                'source_repository': repository['url'],
                'source_repository_id': repository['repository_id'],
                'source_git': source_git(),
                'created_at_utc': datetime.now(timezone.utc).isoformat(),
                'file_count': len(records), 'files': records}
    payload = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    output = ROOT / '07-Releases' / 'packages'
    output.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    archive = output / f'Nature-Studio-v{version}-{stamp}.zip'
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as bundle:
        for path in files:
            bundle.write(path, 'Nature-Studio/' + path.relative_to(ROOT).as_posix())
        bundle.writestr('Nature-Studio/PACKAGE-MANIFEST.json', payload)
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None, 'ZIP integrity check failed'
        for record in records:
            data = bundle.read('Nature-Studio/' + record['path'])
            assert hashlib.sha256(data).hexdigest() == record['sha256'], record['path']
    archive.with_suffix('.manifest.json').write_bytes(payload)
    archive.with_suffix('.sha256').write_text(
        hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name + '\n',
        encoding='utf-8')
    print(json.dumps({'archive': str(archive), 'file_count': len(files),
                      'bytes': archive.stat().st_size, 'verified': True}))


if __name__ == '__main__':
    build()
