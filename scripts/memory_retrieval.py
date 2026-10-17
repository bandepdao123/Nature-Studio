"""Local, metadata-first lesson discovery. Ranking is not semantic coverage or authority."""
import argparse
import base64
import hashlib
import json
from pathlib import Path, PureWindowsPath
import re
import unicodedata

from validate_memory import read_metadata

ROOT = Path(__file__).resolve().parents[1]
ENGINE = 1
STATUSES = {'active': 'active', 'candidate': 'candidates', 'retired': 'retired'}


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def digest(value):
    return hashlib.sha256(value).hexdigest()


def local(root, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ValueError('Use a workspace-relative path with forward slashes')
    rel = Path(relative)
    path = (root / rel).resolve()
    if rel.is_absolute() or PureWindowsPath(relative).drive or '..' in rel.parts or not path.is_relative_to(root.resolve()):
        raise ValueError('Path outside workspace')
    return path


def fold(value):
    value = unicodedata.normalize('NFKD', value.casefold().replace('đ', 'd'))
    return re.sub(r'[^\w]+', ' ', ''.join(c for c in value if not unicodedata.combining(c))).strip()


def retrieval_errors(value):
    if not isinstance(value, dict) or type(value.get('schema')) is not int or value['schema'] != 1:
        return ['retrieval: require schema 1 object']
    errors = []
    if not isinstance(value.get('summary'), str) or not value['summary'].strip():
        errors.append('retrieval.summary: nonempty text required')
    for key in ('topics', 'entities', 'interactions'):
        if not isinstance(value.get(key), list) or any(not isinstance(x, str) or not x.strip() for x in value[key]):
            errors.append(f'retrieval.{key}: require a list of nonempty strings')
    return errors


def taxonomy(root):
    path = local(root, '00-Standards/memory-taxonomy.json')
    # Isolated legacy fixtures/workspaces may not have the taxonomy yet.
    data = json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else {
        'schema': 1, 'tasks': {}, 'modes': {}, 'topics': {}, 'entities': {}, 'interactions': {}}
    if data.get('schema') != 1:
        raise ValueError('Unsupported memory taxonomy')
    for group in ('tasks', 'modes', 'topics', 'entities', 'interactions'):
        if not isinstance(data.get(group), dict) or any(
                not isinstance(k, str) or not isinstance(v, list) or
                any(not isinstance(x, str) or not x.strip() for x in v)
                for k, v in data[group].items()):
            raise ValueError('Invalid taxonomy group: ' + group)
    return data


def canonical(value, group, tax):
    word = fold(value)
    for key, aliases in tax[group].items():
        if word in [fold(x) for x in (key, *aliases)]:
            return key
    return value.casefold().strip()


def scan(root, slug, persist=True):
    """Read source files locally, never inject their bodies into model discovery output."""
    root = Path(root).resolve()
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', slug):
        raise ValueError('Invalid Project slug')
    project = local(root, f'03-Projects/{slug}/PROJECT.md')
    match = re.search(r'^ID:\s*([^|\r\n]+)', project.read_text(encoding='utf-8-sig'), re.M)
    if not match:
        raise ValueError('Project ID missing')
    pid = match.group(1).strip()
    tax = taxonomy(root)
    inventory, records, errors, ids = {}, [], [], set()
    for prefix, scope in ((f'05-Memory/projects/{slug}', 'project'), ('05-Memory/shared', 'shared')):
        folder = local(root, prefix)
        for path in sorted(folder.rglob('*.md')) if folder.exists() else []:
            if path.name in ('README.md', 'INDEX.md'):
                continue
            rel = path.relative_to(root).as_posix()
            try:
                path = local(root, rel)
                raw = path.read_bytes()
                inventory[rel] = digest(raw)
                m = read_metadata(path)
                lid, status = m.get('id'), m.get('status')
                if not isinstance(lid, str) or not re.fullmatch(r'L-[A-Za-z0-9][A-Za-z0-9-]*', lid):
                    raise ValueError('Invalid lesson ID')
                if lid in ids:
                    raise ValueError('Duplicate lesson ID: ' + lid)
                ids.add(lid)
                if status not in STATUSES or path.parent != local(root, prefix + '/' + STATUSES[status]):
                    raise ValueError('Status/directory mismatch')
                if m.get('scope') != scope or m.get('project_id') != (pid if scope == 'project' else None):
                    raise ValueError('Scope/Project mismatch')
                if not isinstance(m.get('version'), str) or not isinstance(m.get('action'), str) or not m['action'].strip():
                    raise ValueError('Missing version/action')
                conditions = m.get('conditions')
                if not isinstance(conditions, dict) or any(
                        not isinstance(conditions.get(k), list) or
                        any(not isinstance(x, str) or not x.strip() for x in conditions[k])
                        for k in ('tasks', 'models', 'interfaces', 'formats')) or not conditions['tasks']:
                    raise ValueError('Invalid conditions')
                retrieval = m.get('retrieval')
                if retrieval is not None and retrieval_errors(retrieval):
                    raise ValueError('; '.join(retrieval_errors(retrieval)))
                records.append(dict(id=lid, path=rel, sha256=inventory[rel], version=m['version'],
                                    status=status, scope=scope, conditions=conditions,
                                    summary=retrieval['summary'] if retrieval else m['action'],
                                    retrieval=retrieval, action=m['action']))
            except (ValueError, TypeError, OSError, KeyError) as exc:
                errors.append(dict(path=rel, error=str(exc)))
    stamp = digest(encoded(dict(engine=ENGINE, engine_source=digest(Path(__file__).read_bytes()),
                                project=digest(project.read_bytes()),
                                taxonomy=tax, inventory=inventory, errors=errors)))
    catalog = dict(schema=1, engine=ENGINE, project=slug, fingerprint=stamp,
                   inventory=inventory, records=records, errors=errors, taxonomy=tax)
    if persist:
        cache = local(root, f'.nature-studio/memory/{slug}/catalog.json')
        cache.parent.mkdir(parents=True, exist_ok=True)
        payload = encoded(catalog)
        if not cache.exists() or cache.read_bytes() != payload:
            cache.write_bytes(payload)
    return catalog


def dimensions(record, request, tax):
    unknown = []
    for key in ('tasks', 'models', 'interfaces', 'formats'):
        wanted, actual = record['conditions'][key], request.get(key, [])
        if not wanted:
            continue
        if not actual:
            unknown.append(key)
            continue
        if key == 'tasks':
            wanted = [canonical(x, 'tasks', tax) for x in wanted]
            actual = [canonical(x, 'tasks', tax) for x in actual]
            if set(wanted) & set(actual):
                continue
            if any(x not in tax['tasks'] for x in wanted + actual):
                unknown.append(key)
                continue
        elif {fold(x) for x in wanted} & {fold(x) for x in actual}:
            continue
        return 'excluded', [key + ': explicit mismatch']
    return ('unknown' if unknown else 'match'), unknown


def query(root, slug, *, mode=None, tasks=(), topics=(), entities=(), interactions=(),
          models=(), interfaces=(), formats=(), text='', candidates=False, retired=False,
          broad=False, page_size=12, cursor=None):
    if not 1 <= page_size <= 100:
        raise ValueError('page_size must be between 1 and 100')
    catalog = scan(root, slug)
    tax = catalog['taxonomy']
    request = dict(mode=mode, tasks=list(tasks) if tasks else tax['modes'].get(mode, []),
                   topics=list(topics), entities=list(entities), interactions=list(interactions),
                   models=list(models), interfaces=list(interfaces), formats=list(formats), text=text,
                   candidates=candidates, retired=retired, broad=broad)
    signature = digest(encoded(dict(fingerprint=catalog['fingerprint'], request=request, page_size=page_size)))
    offset = 0
    if cursor:
        try:
            token = json.loads(base64.urlsafe_b64decode(cursor.encode()))
            if token['signature'] != signature or type(token['offset']) is not int or token['offset'] < 0:
                raise ValueError()
            offset = token['offset']
        except (ValueError, KeyError, TypeError):
            raise ValueError('Stale or invalid memory cursor; restart query') from None
    rows, excluded = [], 0
    for record in catalog['records']:
        if record['status'] == 'candidate' and not candidates or record['status'] == 'retired' and not retired:
            continue
        state, reasons = dimensions(record, request, tax)
        if state == 'excluded':
            excluded += 1
            continue
        retrieval, hits = record['retrieval'], []
        if retrieval:
            for group in ('topics', 'entities', 'interactions'):
                wanted = {canonical(x, group, tax) for x in request[group]}
                for label in retrieval[group]:
                    canon = canonical(label, group, tax)
                    aliases = [canon, *tax[group].get(canon, [])]
                    if canon in wanted or any(fold(a) and fold(a) in fold(text) for a in aliases):
                        hits.append(group + ':' + canon)
        # Action/summary terms assist retrieval, never serve as hard conditions.
        words = set(fold(text).split()) - {'the', 'and', 'video', 'prompt', 'cua', 'cho', 'with'}
        lexical = words & set(fold(record['summary'] + ' ' + record['action']).split())
        score = 0 if broad else len(set(hits)) * 10 + min(len(lexical), 5)
        relation = 'related' if score else ('needs_review' if broad or not retrieval or state == 'unknown' else 'deferred')
        row = {k: record[k] for k in ('id', 'path', 'sha256', 'version', 'status', 'scope', 'summary', 'conditions')}
        row.update(condition_match=state, relation=relation,
                   reasons=reasons + sorted(set(hits)), score=score,
                   legacy=retrieval is None)
        rows.append(row)
    rows.sort(key=lambda r: (r['status'] != 'active', -r['score'], r['relation'] != 'needs_review', r['id']))
    page = rows[offset:offset + page_size]
    next_offset = offset + len(page)
    next_cursor = base64.urlsafe_b64encode(encoded(dict(signature=signature, offset=next_offset))).decode() if next_offset < len(rows) else None
    return dict(schema=1, project=slug, fingerprint=catalog['fingerprint'], request=request,
                active=[r for r in page if r['status'] == 'active'],
                candidates=[r for r in page if r['status'] == 'candidate'],
                retired=[r for r in page if r['status'] == 'retired'],
                total=len(rows), remaining=len(rows)-next_offset, excluded_conditions=excluded,
                next_cursor=next_cursor, errors=catalog['errors'],
                discovery_complete=not catalog['errors'] and next_cursor is None,
                semantic_coverage='not_certified',
                note='Read full originals before use. Topics rank, not exclude. Candidates are not rules. '
                     'Unknown/legacy require review; deferred rows remain available via pagination. '
                     'An empty page or exhausted cursor does not certify semantic coverage.')


def load_lessons(root, slug, selection, ids):
    """Explicit hash-bound reading; rejects unreviewed states as automatic rules."""
    catalog = scan(root, slug)
    if selection.get('project') != slug or selection.get('fingerprint') != catalog['fingerprint'] or catalog['errors']:
        raise ValueError('Memory selection stale/incomplete; query again')
    offered = {r['id']: r for k in ('active', 'candidates', 'retired') for r in selection.get(k, [])}
    originals = {r['id']: r for r in catalog['records']}
    if not ids or len(ids) != len(set(ids)):
        raise ValueError('Supply distinct lesson IDs from this query page')
    result = []
    for lid in ids:
        if lid not in offered:
            raise ValueError('Lesson not offered on this query page: ' + lid)
        row = offered[lid]
        original = originals.get(lid)
        if not original or any(row.get(k) != original[k] for k in ('path', 'sha256', 'version', 'status')):
            raise ValueError('Selection does not match original lesson')
        if dimensions(original, selection.get('request', {}), catalog['taxonomy'])[0] == 'excluded':
            raise ValueError('Lesson contradicts selected conditions')
        raw = local(root, row['path']).read_bytes()
        if digest(raw) != row['sha256']:
            raise ValueError('Lesson hash changed')
        result.append(dict(id=lid, status=row['status'], path=row['path'], sha256=row['sha256'],
                           text=raw.decode('utf-8-sig'), authority='inspect_original_not_automatic'))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('query'); p.add_argument('project')
    p.add_argument('--mode', choices=('new', 'revision', 'caption', 'reference'))
    for field in ('task', 'topic', 'entity', 'interaction', 'model', 'interface', 'format'):
        p.add_argument('--'+field, action='append', default=[])
    p.add_argument('--text', default='')
    p.add_argument('--candidates', action='store_true'); p.add_argument('--retired', action='store_true')
    p.add_argument('--broad', action='store_true'); p.add_argument('--page-size', type=int, default=12)
    p.add_argument('--cursor'); p.add_argument('--out', type=Path)
    p = sub.add_parser('read'); p.add_argument('project'); p.add_argument('selection', type=Path)
    p.add_argument('--id', action='append', required=True)
    args = parser.parse_args(); root = args.root.resolve()
    if args.command == 'read':
        selection = json.loads(local(root, args.selection.as_posix()).read_text(encoding='utf-8-sig'))
        result = load_lessons(root, args.project, selection, args.id)
    else:
        result = query(root, args.project, mode=args.mode, tasks=args.task, topics=args.topic,
                       entities=args.entity, interactions=args.interaction, models=args.model,
                       interfaces=args.interface, formats=args.format, text=args.text,
                       candidates=args.candidates, retired=args.retired, broad=args.broad,
                       page_size=args.page_size, cursor=args.cursor)
        if args.out:
            dest = local(root, args.out.as_posix()); dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(encoded(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if isinstance(result, dict) and result.get('errors') else 0


if __name__ == '__main__':
    raise SystemExit(main())
