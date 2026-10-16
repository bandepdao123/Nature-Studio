"""Local Project prefix initialization and atomic video reservations (stdlib only)."""
import argparse
import json
from pathlib import Path
import re
import secrets
import sqlite3
import string
import uuid
from contextlib import contextmanager


def project(root, slug):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', slug):
        raise ValueError('Invalid Project slug')
    path = root / '03-Projects' / slug / 'PROJECT.md'
    match = re.search(r'^ID:\s*([^|\r\n]+)', path.read_text(encoding='utf-8'), re.M)
    if not match:
        raise ValueError('Missing stable Project ID')
    return match.group(1).strip()


@contextmanager
def registry(root):
    directory = root / '.nature-studio'
    directory.mkdir(exist_ok=True)
    db = sqlite3.connect(directory / 'video-ids.sqlite3', timeout=30, isolation_level=None)
    try:
        db.execute('BEGIN IMMEDIATE')
        db.execute('CREATE TABLE IF NOT EXISTS projects (source_id TEXT PRIMARY KEY, uid TEXT UNIQUE NOT NULL, prefix TEXT UNIQUE NOT NULL, last_number INTEGER NOT NULL DEFAULT 0)')
        db.execute('CREATE TABLE IF NOT EXISTS videos (uid TEXT PRIMARY KEY, project_uid TEXT NOT NULL, code TEXT UNIQUE NOT NULL, number INTEGER NOT NULL)')
        yield db
        db.commit()
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


def observed(root):
    """Include real folder names, saved identity files and ledgers across Projects."""
    codes = set()
    for folder in (root / '04-Productions').glob('*/*'):
        if folder.is_dir():
            codes.add(folder.name)
    for ledger in (root / '03-Projects').glob('*/idea-ledger.md'):
        codes.update(re.findall(r'\b[A-Z]{3}-\d{5}\b', ledger.read_text(encoding='utf-8')))
    return codes


def initialize(root, slug, prefix=None):
    pid = project(root, slug)
    if prefix is not None and not re.fullmatch('[A-Z]{3}', prefix):
        raise ValueError('Prefix must be exactly three uppercase ASCII letters')
    with registry(root) as db:
        row = db.execute('SELECT uid,prefix,last_number FROM projects WHERE source_id=?', (pid,)).fetchone()
        if row:
            if prefix and prefix != row[1]:
                raise ValueError('Project already initialized; changing its prefix is prohibited')
            return dict(project_id=pid, project_uuid=row[0], prefix=row[1], last_number=row[2])
        used = {row[0] for row in db.execute('SELECT prefix FROM projects')}
        used.update(code[:3] for code in observed(root) if re.fullmatch(r'[A-Z]{3}-\d{5}', code))
        if prefix and prefix in used:
            raise ValueError('Prefix already used; restore original registry to continue an existing Project')
        if len(used) >= 26 ** 3:
            raise ValueError('Three-letter prefix space exhausted')
        while prefix is None:
            candidate = ''.join(secrets.choice(string.ascii_uppercase) for _ in range(3))
            if candidate not in used:
                prefix = candidate
        uid = str(uuid.uuid4())
        db.execute('INSERT INTO projects(source_id,uid,prefix) VALUES(?,?,?)', (pid,uid,prefix))
        return dict(project_id=pid, project_uuid=uid, prefix=prefix, last_number=0)


def reserve(root, slug):
    info = initialize(root, slug)
    parent = root / '04-Productions' / slug
    parent.mkdir(parents=True, exist_ok=True)
    with registry(root) as db:
        last = db.execute('SELECT last_number FROM projects WHERE source_id=?', (info['project_id'],)).fetchone()[0]
        codes = observed(root)
        values = [int(c[-5:]) for c in codes if re.fullmatch(re.escape(info['prefix']) + r'-\d{5}', c)]
        number = max([last, *values]) + 1
        if number > 99999:
            raise ValueError('Project exhausted 99999 videos; do not wrap counter or change prefix silently')
        code = f"{info['prefix']}-{number:05d}"
        uid = str(uuid.uuid4())
        db.execute('INSERT INTO videos VALUES(?,?,?,?)', (uid,info['project_uuid'],code,number))
        db.execute('UPDATE projects SET last_number=? WHERE source_id=?', (number,info['project_id']))
    # Reservation is already durable. A filesystem failure burns the number; never reuse it.
    folder = parent / code
    folder.mkdir(exist_ok=False)
    identity = dict(video_id=code, video_uuid=uid, project_id=info['project_id'],
                    project_uuid=info['project_uuid'], status='reserved')
    with (folder / 'IDENTITY.json').open('x', encoding='utf-8', newline='\n') as out:
        json.dump(identity, out, ensure_ascii=False, indent=2)
        out.write('\n')
    return identity


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['init','reserve'])
    parser.add_argument('slug')
    parser.add_argument('--prefix')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    if args.action == 'reserve' and args.prefix:
        parser.error('--prefix is only valid for init')
    try:
        result = initialize(args.root.resolve(), args.slug, args.prefix) if args.action == 'init' else reserve(args.root.resolve(), args.slug)
        print(json.dumps(result, ensure_ascii=False))
    except (ValueError, OSError, sqlite3.Error) as exc:
        parser.exit(1, f'{exc}\n')
