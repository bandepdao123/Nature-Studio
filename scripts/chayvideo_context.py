"""Plan 01: exact-source task packets and rebuildable local history. Stdlib only.

No model calls, semantic novelty verdicts, ID reservations or media operations.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import memory_retrieval as memory

ROOT = Path(__file__).resolve().parents[1]
FINGERPRINT_FIELDS = ('opening', 'interaction', 'objects', 'terrain_role',
                      'trigger', 'key_action', 'consequence')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inside(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Path outside workspace: {relative}')
    return path


def slug_ok(slug):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', slug):
        raise ValueError('Invalid Project slug')


def source(root, relative):
    path = inside(root, relative)
    raw = path.read_bytes()
    return dict(path=path.relative_to(root.resolve()).as_posix(),
                sha256=digest(raw), text=raw.decode('utf-8-sig'))


def catalog(root):
    """Route using compact current metadata; no frozen species-to-project map."""
    rows = []
    for path in sorted((root / '03-Projects').glob('*/PROJECT.md')):
        item = source(root, path.relative_to(root))
        text = item.pop('text')
        metadata = [line for line in text.splitlines() if re.match(
            r'^(# |ID:|Slug:|Version:|Aliases:|Routing:|Model:)', line)]
        rows.append(dict(**item, metadata='\n'.join(metadata),
                         needs_full_read=not any(x.startswith('Routing:') for x in metadata)))
    return rows


def active_files(root, slug):
    # Check real files too; an empty/stale INDEX is not proof of no lessons.
    files = []
    for base in (f'05-Memory/projects/{slug}/active', '05-Memory/shared/active'):
        directory = inside(root, base)
        if directory.exists():
            files.extend(p.relative_to(root).as_posix() for p in directory.rglob('*.md'))
    return sorted(files)


def packet(root, slug, mode, species=(), interaction='unspecified',
           memory_selection=None, lesson_ids=(), topics=(), query_text=''):
    slug_ok(slug)
    recipe_path = f'03-Projects/{slug}/context-map.json'
    recipe_source = source(root, recipe_path)
    recipe = json.loads(recipe_source['text'])
    selection = mode
    seen = set()
    while True:
        if selection in seen:
            raise ValueError('Cyclic context-map alias')
        seen.add(selection)
        chosen = recipe.get(selection, 'new' if selection == 'reference' else None)
        if isinstance(chosen, str):
            selection = chosen
        elif isinstance(chosen, list):
            break
        else:
            raise ValueError(f'Missing task recipe: {mode}')
    files = [recipe_path] + recipe['common'] + chosen
    # Human-facing indexes can grow without bound; discovery returns paged descriptors.
    files = [p for p in files if not (p.startswith('05-Memory/') and p.endswith('/INDEX.md'))]
    missing = []
    if mode != 'caption':
        for name in species:
            profile = recipe.get('species', {}).get(name.lower())
            if profile:
                files.append(profile)
            else:
                missing.append(f'Research exact species/context: {name}; no substitute profile')
        # Underwater is the configured species-required workflow. Optional profiles
        # in another Project's map do not make species a mandatory input there.
        if slug == 'underwater' and not species:
            missing.append('Resolve species or granted choice before producing content')
        if interaction != 'natural':
            files += recipe.get('angling', [])
    selection = memory.query(root, slug, mode=mode, topics=topics, entities=species,
                             interactions=[] if interaction == 'unspecified' else [interaction],
                             text=query_text)
    if selection['errors']:
        missing.append('Memory discovery incomplete: inspect memory.errors before producing content')
    if lesson_ids:
        if memory_selection is None or memory_selection.get('request', {}).get('mode') != mode:
            raise ValueError('Supply a memory selection page for the same task mode')
        selected = memory.load_lessons(root, slug, memory_selection, list(lesson_ids))
        files += [row['path'] for row in selected]
    else:
        selected = []
    sources = [source(root, path) for path in dict.fromkeys(files)]
    dependencies = []
    for path in ['VERSION', 'START-HERE.md', 'SYSTEM.md', 'AGENTS.md',
                 '.agents/skills/chayvideo/SKILL.md',
                 '.agents/skills/chayvideo/references/workflow.md',
                 '00-Standards/video-prompt-workflow.md',
                 f'.agents/skills/chayvideo/references/{mode}.md']:
        item = source(root, path)
        item.pop('text')
        dependencies.append(item)
    for path in ['scripts/memory_retrieval.py', '00-Standards/memory-taxonomy.json']:
        if inside(root, path).is_file():
            item = source(root, path)
            item.pop('text')
            dependencies.append(item)
    if mode == 'reference':
        for path in ['00-Standards/reference-video-adaptation.md',
                     '.agents/skills/clonevideo/SKILL.md',
                     '.agents/skills/clonevideo/references/analysis.md',
                     '.agents/skills/clonevideo/references/schema.md',
                     'scripts/reference_video.py']:
            item = source(root, path)
            item.pop('text')
            dependencies.append(item)
    return dict(schema=2, project=slug, mode=mode, species=list(species),
                interaction=interaction, memory=selection,
                selected_lessons=[{k: r[k] for k in ('id', 'status', 'path', 'sha256')} for r in selected],
                sources=sources, dependencies=dependencies, pending=missing,
                note='Exact current sources, no token truncation. Read real production/attached media '
                     'separately. Active location is discovery, not permission: inspect status and '
                         'conditions before applying. Project decides required inputs; generic packet '
                         'does not certify completeness. New facts need external research.')


def verify(root, data):
    stale = []
    for item in data['sources'] + data.get('dependencies', []):
        path = inside(root, item['path'])
        if not path.is_file() or digest(path.read_bytes()) != item['sha256']:
            stale.append(item['path'])
    if 'memory' in data:
        current = memory.scan(root, data['project'])
        if current['fingerprint'] != data['memory']['fingerprint'] or current['errors']:
            stale.append('memory_inventory')
    elif active_files(root, data['project']) != data['active_inventory']:
        stale.append('active_inventory')
    return stale


def history(root, slug, query=''):
    """Inspect all text files, cache derived rows; never pretend lexical search is semantic QA."""
    slug_ok(slug)
    folder = inside(root, f'04-Productions/{slug}')
    rows, inventory = [], {}
    for production in sorted(folder.iterdir()) if folder.exists() else []:
        if not production.is_dir():
            continue
        # Every text record participates in freshness, including feedback and old attempts.
        files = sorted(p for p in production.rglob('*') if p.is_file()
                       and p.suffix.lower() in ('.md', '.json', '.txt'))
        current = {}
        texts = {}
        for path in files:
            rel = path.relative_to(root).as_posix()
            raw = inside(root, rel).read_bytes()
            current[rel] = digest(raw)
            if path.name != 'HISTORY-FINGERPRINT.json':
                texts[rel] = raw.decode('utf-8-sig', errors='replace')
        inventory.update(current)
        fp_path = production / 'HISTORY-FINGERPRINT.json'
        fp, valid = None, False
        if fp_path.exists():
            try:
                fp = json.loads(fp_path.read_text(encoding='utf-8-sig'))
                if not isinstance(fp, dict):
                    raise ValueError('Fingerprint must be an object')
                refs = fp.get('source_hashes', {})
                # Capsule must cover ALL text sources. A later attempt invalidates it.
                valid = (refs == {k: v for k, v in current.items()
                                  if not k.endswith('/HISTORY-FINGERPRINT.json')}
                         and all(isinstance(fp.get(k), str) and fp[k].strip()
                                 for k in FINGERPRINT_FIELDS))
            except (ValueError, TypeError):
                pass
        terms = set(re.findall(r'\w+', query.casefold()))
        matches = [rel for rel, text in texts.items()
                   if terms and any(term in text.casefold() for term in terms)]
        rows.append(dict(production=production.name,
                         fingerprint={k: fp[k] for k in FINGERPRINT_FIELDS} if valid else None,
                         needs_read=[] if valid else sorted(texts), lexical_matches=matches,
                         source_hashes=current))
    ledger = inside(root, f'03-Projects/{slug}/idea-ledger.md')
    ledger_source = source(root, ledger.relative_to(root)) if ledger.exists() else None
    if ledger_source:
        inventory[ledger_source['path']] = ledger_source['sha256']
    cache = inside(root, f'.nature-studio/history/{slug}.json')
    try:
        previous = json.loads(cache.read_text(encoding='utf-8')) if cache.exists() else {}
    except ValueError:
        previous = {}  # Derived cache can be rebuilt; production remains authoritative.
    if not isinstance(previous, dict):
        previous = {}
    result = dict(schema=1, project=slug, inventory=inventory, records=rows,
                  ledger=ledger_source, refreshed=previous.get('inventory') != inventory,
                  limits='All records listed; lexical matches only assist retrieval. Read uncovered '
                         'records and nearest originals before novelty verdict. Chat, examples, '
                         'rejected drafts and related other Projects still require inspection.')
    cache.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=cache.parent,
                                     suffix='.tmp', delete=False) as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        temp = Path(out.name)
    temp.replace(cache)
    return result


def fingerprint(root, slug, production_id, data):
    """Store an AI-authored capsule only against the exact history it actually reviewed."""
    if not all(isinstance(data.get(k), str) and data[k].strip() for k in FINGERPRINT_FIELDS):
        raise ValueError('Supply all causal fingerprint fields')
    records = history(root, slug)['records']
    record = next((r for r in records if r['production'] == production_id), None)
    if record is None:
        raise ValueError('Unknown production')
    current = {k: v for k, v in record['source_hashes'].items()
               if not k.endswith('/HISTORY-FINGERPRINT.json')}
    if not current or data.get('source_hashes') != current:
        raise ValueError('Read all source records first; supplied source_hashes must exactly match')
    payload = {k: data[k] for k in (*FINGERPRINT_FIELDS, 'source_hashes')}
    payload['schema'] = 1
    path = inside(root, f'04-Productions/{slug}/{production_id}/HISTORY-FINGERPRINT.json')
    # Derived metadata only; never modifies a source record or its status.
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return dict(path=path.relative_to(root).as_posix(), note='AI-authored capsule; semantic review still required')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    subs = parser.add_subparsers(dest='command', required=True)
    subs.add_parser('projects')
    p = subs.add_parser('packet')
    p.add_argument('project')
    p.add_argument('--mode', choices=('new', 'revision', 'caption', 'reference'), required=True)
    p.add_argument('--species', action='append', default=[])
    p.add_argument('--interaction', choices=('natural', 'angling', 'unspecified'), default='unspecified')
    p.add_argument('--out', type=Path)
    p.add_argument('--memory-selection', type=Path)
    p.add_argument('--lesson-id', action='append', default=[])
    p.add_argument('--topic', action='append', default=[])
    p.add_argument('--query', default='')
    p = subs.add_parser('verify')
    p.add_argument('packet', type=Path)
    p = subs.add_parser('history')
    p.add_argument('project')
    p.add_argument('--query', default='')
    p.add_argument('--full', action='store_true', help='Include hashes of every source file; default is compact')
    p = subs.add_parser('fingerprint')
    p.add_argument('project')
    p.add_argument('production')
    p.add_argument('input', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command == 'projects':
        result = catalog(root)
    elif args.command == 'packet':
        selection = (json.loads(inside(root, args.memory_selection.as_posix()).read_text(encoding='utf-8-sig'))
                     if args.memory_selection else None)
        result = packet(root, args.project, args.mode, args.species, args.interaction,
                        selection, args.lesson_id, args.topic, args.query)
        if args.out:
            path = inside(root, args.out)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
            print(path)
            return
    elif args.command == 'history':
        result = history(root, args.project, args.query)
        if not args.full:
            result['inventory_count'] = len(result.pop('inventory'))
            for row in result['records']:
                row.pop('source_hashes')
    elif args.command == 'fingerprint':
        result = fingerprint(root, args.project, args.production,
                             json.loads(args.input.read_text(encoding='utf-8-sig')))
    else:
        result = dict(stale=verify(root, json.loads(args.packet.read_text(encoding='utf-8-sig'))))
        if result['stale']:
            print(json.dumps(result, ensure_ascii=False))
            sys.exit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
