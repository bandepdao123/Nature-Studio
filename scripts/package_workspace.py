"""Build a portable, verified Nature Studio ZIP using only the Python stdlib."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {'.git', '__pycache__', '.venv', 'node_modules', '.pytest_cache'}


def included(path):
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if rel.parts[:2] == ('07-Releases', 'packages'):
        return False
    name = path.name.lower()
    if name.startswith('.env') and name != '.env.example':
        return False
    if name.startswith(('credentials', 'secrets')) and path.suffix.lower() == '.json':
        return False
    return name not in {'thumbs.db', '.ds_store'} and path.suffix.lower() not in {
        '.pem', '.key', '.pyc', '.pyo', '.tmp', '.log'
    }


def build():
    files = sorted(p for p in ROOT.rglob('*') if p.is_file() and included(p))
    if any(p.is_symlink() for p in files):
        raise RuntimeError('Resolve symlinks explicitly before packaging.')
    records = [{'path': p.relative_to(ROOT).as_posix(), 'size': p.stat().st_size,
                'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
    manifest = {'format_version': 1, 'workspace': 'Nature-Studio',
                'created_at_utc': datetime.now(timezone.utc).isoformat(),
                'file_count': len(records), 'files': records}
    payload = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    output = ROOT / '07-Releases' / 'packages'
    output.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    archive = output / f'Nature-Studio-{stamp}.zip'
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
