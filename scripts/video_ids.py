"""Atomic local XX-YYYY reservations; historical IDs and UUIDs remain immutable."""
import argparse
from contextlib import contextmanager
import json
from pathlib import Path
import re
import secrets
import sqlite3
import string
import uuid

FORMAT = 'XX-YYYY'
CODE = r'(?:[A-Z]{2}-[0-9]{4}|[A-Z]{3}-[0-9]{5})'


def project(root, slug):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', slug):
        raise ValueError('Invalid Project slug')
    path = root / '03-Projects' / slug / 'PROJECT.md'
    match = re.search(r'^ID:\s*([^|\r\n]+)', path.read_text(encoding='utf-8'), re.M)
    if not match:
        raise ValueError('Missing stable Project ID')
    return match.group(1).strip()


def valid_prefix(prefix):
    return isinstance(prefix, str) and re.fullmatch(r'[A-Z]{2}', prefix) and prefix != 'UF'


@contextmanager
def registry(root):
    directory = root / '.nature-studio'
    directory.mkdir(exist_ok=True)
    db = sqlite3.connect(directory / 'video-ids.sqlite3', timeout=30, isolation_level=None)
    try:
        db.execute('BEGIN IMMEDIATE')
        if db.execute('PRAGMA user_version').fetchone()[0] > 2:
            raise ValueError('Registry schema newer than this allocator; use matching source version')
        db.execute('CREATE TABLE IF NOT EXISTS projects (source_id TEXT PRIMARY KEY, uid TEXT UNIQUE NOT NULL, prefix TEXT UNIQUE NOT NULL, last_number INTEGER NOT NULL DEFAULT 0)')
        db.execute('CREATE TABLE IF NOT EXISTS videos (uid TEXT PRIMARY KEY, project_uid TEXT NOT NULL, code TEXT UNIQUE NOT NULL, number INTEGER NOT NULL)')
        db.execute('CREATE TABLE IF NOT EXISTS series (project_uid TEXT NOT NULL, scheme TEXT NOT NULL, prefix TEXT UNIQUE NOT NULL, last_number INTEGER NOT NULL, PRIMARY KEY(project_uid,scheme))')
        # Old binaries must fail rather than emit five-digit IDs under an active v2 prefix.
        condition = "NEW.prefix NOT GLOB '[A-Z][A-Z]' OR NEW.prefix='UF'"
        for name, event in [('v2_project_insert', 'INSERT'), ('v2_project_prefix', 'UPDATE OF prefix')]:
            db.execute(f"CREATE TRIGGER IF NOT EXISTS {name} BEFORE {event} ON projects WHEN {condition} BEGIN SELECT RAISE(ABORT,'v2 requires a two-letter prefix; UF is legacy'); END")
        db.execute("""CREATE TRIGGER IF NOT EXISTS v2_video_insert BEFORE INSERT ON videos
            WHEN NEW.number NOT BETWEEN 1 AND 9999 OR NOT EXISTS (
              SELECT 1 FROM projects p WHERE p.uid=NEW.project_uid
                AND p.prefix GLOB '[A-Z][A-Z]' AND p.prefix!='UF'
                AND NEW.code=p.prefix || '-' || printf('%04d',NEW.number))
            BEGIN SELECT RAISE(ABORT,'v2 allocator required'); END""")
        db.execute('PRAGMA user_version=2')
        yield db
        db.commit()
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


def observed(root):
    codes = set()
    for folder in (root / '04-Productions').glob('*/*'):
        if folder.is_dir() and re.fullmatch(CODE, folder.name):
            codes.add(folder.name)
    for ledger in (root / '03-Projects').glob('*/idea-ledger.md'):
        codes.update(re.findall(r'\b' + CODE + r'\b', ledger.read_text(encoding='utf-8')))
    for identity in (root / '04-Productions').glob('*/*/IDENTITY.json'):
        data = json.loads(identity.read_text(encoding='utf-8-sig'))
        code = data.get('video_id')
        if isinstance(code, str) and re.fullmatch(CODE, code):
            codes.add(code)
    return codes


def initialize(root, slug, prefix=None):
    pid = project(root, slug)
    if prefix is not None and not valid_prefix(prefix):
        raise ValueError('Prefix must be two uppercase ASCII letters; UF is reserved for legacy')
    with registry(root) as db:
        row = db.execute('SELECT uid,prefix,last_number FROM projects WHERE source_id=?', (pid,)).fetchone()
        if row and valid_prefix(row[1]):
            if prefix and prefix != row[1]:
                raise ValueError('Project already initialized; changing its prefix is prohibited')
            series = db.execute('SELECT prefix,last_number FROM series WHERE project_uid=? AND scheme=?', (row[0], FORMAT)).fetchone()
            if not series or series != (row[1], row[2]):
                raise ValueError('Inconsistent active series; restore or repair registry before allocating')
            return dict(project_id=pid, project_uuid=row[0], prefix=row[1], last_number=row[2])
        if row and not re.fullmatch('[A-Z]{3}', row[1]):
            raise ValueError('Unsupported legacy registry prefix')
        used = {r[0] for r in db.execute('SELECT prefix FROM projects UNION SELECT prefix FROM series')}
        used.update(c.split('-')[0] for c in observed(root))
        used.update(code.split('-')[0] for (code,) in db.execute('SELECT code FROM videos'))
        used.add('UF')
        candidates = [a+b for a in string.ascii_uppercase for b in string.ascii_uppercase if a+b not in used]
        if prefix and prefix in used:
            raise ValueError('Prefix already used; restore original registry to continue an existing Project')
        if not candidates:
            raise ValueError('Two-letter prefix space exhausted')
        prefix = prefix or secrets.choice(candidates)
        uid = row[0] if row else str(uuid.uuid4())
        if row:
            db.execute('INSERT INTO series VALUES(?,?,?,?)', (uid,'XXX-YYYYY',row[1],row[2]))
            db.execute('UPDATE projects SET prefix=?,last_number=0 WHERE source_id=?', (prefix,pid))
        else:
            db.execute('INSERT INTO projects(source_id,uid,prefix) VALUES(?,?,?)', (pid,uid,prefix))
        db.execute('INSERT INTO series VALUES(?,?,?,0)', (uid,FORMAT,prefix))
        return dict(project_id=pid, project_uuid=uid, prefix=prefix, last_number=0)


def reserve(root, slug):
    info = initialize(root, slug)
    parent = root / '04-Productions' / slug
    parent.mkdir(parents=True, exist_ok=True)
    with registry(root) as db:
        row = db.execute('SELECT uid,prefix,last_number FROM projects WHERE source_id=?', (info['project_id'],)).fetchone()
        if row[:2] != (info['project_uuid'],info['prefix']):
            raise ValueError('Active Project identity changed during reservation')
        codes = observed(root)
        values = [int(c[-4:]) for c in codes if re.fullmatch(re.escape(info['prefix']) + r'-[0-9]{4}', c)]
        recorded = db.execute('SELECT MAX(number) FROM videos WHERE project_uid=? AND code GLOB ?', (info['project_uuid'],info['prefix']+'-[0-9][0-9][0-9][0-9]')).fetchone()[0] or 0
        number = max([row[2], recorded, *values]) + 1
        if number > 9999:
            raise ValueError('Project exhausted 9999 videos; do not wrap or change prefix silently')
        code = f"{info['prefix']}-{number:04d}"
        uid = str(uuid.uuid4())
        db.execute('INSERT INTO videos VALUES(?,?,?,?)', (uid,info['project_uuid'],code,number))
        db.execute('UPDATE projects SET last_number=? WHERE source_id=?', (number,info['project_id']))
        db.execute('UPDATE series SET last_number=? WHERE project_uid=? AND scheme=?', (number,info['project_uuid'],FORMAT))
    # Commit before filesystem writes: a failed write burns the number, never reuses it.
    folder = parent / code
    folder.mkdir(exist_ok=False)
    identity = dict(schema=2, id_format=FORMAT, video_id=code, video_uuid=uid,
                    project_id=info['project_id'], project_uuid=info['project_uuid'], status='reserved')
    with (folder / 'IDENTITY.json').open('x', encoding='utf-8', newline='\n') as out:
        json.dump(identity, out, ensure_ascii=False, indent=2)
        out.write('\n')
    return identity


def status(root, slug):
    """Read-only inspection: never creates or migrates a registry."""
    pid = project(root, slug)
    path = root / '.nature-studio/video-ids.sqlite3'
    if not path.is_file():
        return dict(project_id=pid, initialized=False, id_format=FORMAT)
    db = sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)
    try:
        row = db.execute('SELECT uid,prefix,last_number FROM projects WHERE source_id=?', (pid,)).fetchone()
        return dict(project_id=pid, initialized=bool(row), id_format=FORMAT,
                    current=dict(zip(('project_uuid','prefix','last_number'), row)) if row else None,
                    migration_pending=bool(row and not valid_prefix(row[1])))
    finally:
        db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['init','reserve','status'])
    parser.add_argument('slug')
    parser.add_argument('--prefix')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    if args.action != 'init' and args.prefix:
        parser.error('--prefix is only valid for init')
    try:
        result = initialize(args.root.resolve(), args.slug, args.prefix) if args.action == 'init' else globals()[args.action](args.root.resolve(), args.slug)
        print(json.dumps(result, ensure_ascii=False))
    except (ValueError, OSError, sqlite3.Error) as exc:
        parser.exit(1, f'{exc}\n')
