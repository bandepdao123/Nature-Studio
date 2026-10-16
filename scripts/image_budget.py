"""Durable first-frame call budget. Records usage; never calls an image model."""
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import sqlite3
import uuid


def production_path(root, production):
    rel = Path(production)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('Use a workspace-relative production directory')
    path = (root / rel).resolve()
    boundary = (root / '04-Productions').resolve()
    if not path.is_relative_to(boundary) or len(path.relative_to(boundary).parts) != 2 or not path.is_dir():
        raise ValueError('Existing 04-Productions/<slug>/<video-id> required')
    return path


def approval_ref(folder, ref):
    if not isinstance(ref, str) or not ref:
        raise ValueError('Saved explicit approval/request file required')
    rel = Path(ref)
    if rel.is_absolute() or '..' in rel.parts or not (folder / rel).resolve().is_relative_to(folder):
        raise ValueError('Approval must be inside production')
    if not (folder / rel).is_file():
        raise ValueError('Approval file does not exist')
    return rel.as_posix()


@contextmanager
def database(folder):
    db = sqlite3.connect(folder / '.image-qa.sqlite3', timeout=30, isolation_level=None)
    try:
        db.execute('BEGIN IMMEDIATE')
        db.execute('CREATE TABLE IF NOT EXISTS cycles (id TEXT PRIMARY KEY, allowance INTEGER NOT NULL, used INTEGER NOT NULL DEFAULT 0, created TEXT NOT NULL, request_ref TEXT)')
        db.execute('CREATE TABLE IF NOT EXISTS calls (id TEXT PRIMARY KEY, cycle_id TEXT NOT NULL, number INTEGER NOT NULL, operation TEXT NOT NULL, outcome TEXT NOT NULL DEFAULT \'pending\', UNIQUE(cycle_id,number))')
        db.execute('CREATE TABLE IF NOT EXISTS grants (id TEXT PRIMARY KEY, cycle_id TEXT NOT NULL, extra INTEGER NOT NULL, approval_ref TEXT NOT NULL)')
        yield db
        db.commit()
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


def latest(db):
    return db.execute('SELECT id,allowance,used FROM cycles ORDER BY rowid DESC LIMIT 1').fetchone()


def info(row):
    return {'cycle_id': row[0], 'authorized': row[1], 'used': row[2], 'remaining': row[1] - row[2]}


def run(root, production, action, *, extra=None, approval_file=None, operation='generate', call_id=None, outcome=None):
    folder = production_path(root.resolve(), production)
    with database(folder) as db:
        row = latest(db)
        if action in {'init', 'new-cycle'}:
            if action == 'new-cycle':
                approval_ref(folder, approval_file)
            if row is None or action == 'new-cycle':
                cid = str(uuid.uuid4())
                db.execute('INSERT INTO cycles(id,allowance,created,request_ref) VALUES(?,?,?,?)',
                           (cid, 5, datetime.now(timezone.utc).isoformat(), approval_file))
                row = latest(db)
            return info(row)
        if row is None:
            raise ValueError('Initialize a cycle first; no implicit reset')
        if action == 'status':
            return info(row)
        if action == 'grant':
            if type(extra) is not int or extra < 1:
                raise ValueError('Extra calls must be a positive integer')
            if row[2] < row[1]:
                raise ValueError('Current budget not exhausted; use remaining calls first')
            ref = approval_ref(folder, approval_file)
            db.execute('INSERT INTO grants VALUES(?,?,?,?)', (str(uuid.uuid4()), row[0], extra, ref))
            db.execute('UPDATE cycles SET allowance=allowance+? WHERE id=?', (extra,row[0]))
            return info(latest(db))
        if action == 'reserve':
            if operation not in {'generate','edit','regenerate'}:
                raise ValueError('Invalid operation')
            if row[2] >= row[1]:
                raise ValueError('Budget exhausted; stop and obtain explicit approval for extra calls')
            cid = str(uuid.uuid4())
            db.execute('UPDATE cycles SET used=used+1 WHERE id=?', (row[0],))
            db.execute('INSERT INTO calls(id,cycle_id,number,operation) VALUES(?,?,?,?)', (cid,row[0],row[2]+1,operation))
            return {**info(latest(db)), 'call_id':cid, 'call_number':row[2]+1, 'outcome':'pending'}
        if action == 'finish':
            if outcome not in {'success','error','cancelled','unknown'}:
                raise ValueError('Invalid outcome')
            record = db.execute('SELECT cycle_id,outcome FROM calls WHERE id=?', (call_id,)).fetchone()
            if record is None or record[0] != row[0]:
                raise ValueError('Call does not belong to current cycle')
            if record[1] not in {'pending',outcome}:
                raise ValueError('Outcome already recorded; preserve history')
            db.execute('UPDATE calls SET outcome=? WHERE id=?', (outcome,call_id))
            return {**info(row), 'call_id':call_id, 'outcome':outcome}
        raise ValueError('Unknown action')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['init','status','reserve','finish','grant','new-cycle'])
    parser.add_argument('--production', required=True)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--operation', choices=['generate','edit','regenerate'], default='generate')
    parser.add_argument('--extra', type=int)
    parser.add_argument('--approval-file')
    parser.add_argument('--call-id')
    parser.add_argument('--outcome', choices=['success','error','cancelled','unknown'])
    args = parser.parse_args()
    try:
        result = run(args.root,args.production,args.action,extra=args.extra,approval_file=args.approval_file,
                     operation=args.operation,call_id=args.call_id,outcome=args.outcome)
        print(json.dumps(result, ensure_ascii=False))
    except (ValueError, OSError, sqlite3.Error) as exc:
        parser.exit(1, f'{exc}\n')
