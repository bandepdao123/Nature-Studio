"""Declarative, conservative stage routing. No model calls or source summaries.

The old mode recipe is the coverage floor. New/unassigned sources are included
at every stage until explicitly classified; unknown effects use the full mode.
"""
import hashlib
import json
from pathlib import Path, PureWindowsPath
import re

STAGES = ('orient', 'concept', 'write', 'review', 'save', 'all')


def local(root, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ValueError('Use a workspace-relative path with forward slashes')
    path = Path(relative)
    if path.is_absolute() or PureWindowsPath(relative).drive or '..' in path.parts:
        raise ValueError('Path outside workspace')
    target = (root / path).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError('Path outside workspace')
    return target


def mode_sources(recipe, mode):
    seen = set()
    while True:
        if mode in seen:
            raise ValueError('Cyclic context-map alias')
        seen.add(mode)
        value = recipe.get(mode, 'new' if mode == 'reference' else None)
        if isinstance(value, str):
            mode = value
        elif isinstance(value, list) and all(isinstance(p, str) for p in value):
            return value
        else:
            raise ValueError('Missing/invalid task recipe: ' + mode)


def strings(value, label):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValueError('Expected string list: ' + label)
    return value


def route(root, slug, recipe, mode, stage, effects=()):
    """All path selection is data-driven; never interpret natural-language hints as exclusions."""
    baseline = list(dict.fromkeys(mode_sources(recipe, mode)))
    fallback = lambda reason: dict(stage=stage, effective_stage='all', effects=list(effects),
        files=baseline, tasks=[], include_species=True, include_angling=True,
        fallback=reason, unassigned=[], config=None, config_sha256=None)
    if stage not in STAGES:
        return fallback('Unknown stage; full mode sources required')
    config_path = recipe.get('routing')
    if not config_path:
        return fallback('No stage routing configured; full mode sources required')
    path = local(root, config_path)
    if not path.is_file():
        return fallback('Routing file unavailable; full mode sources required')
    raw = path.read_bytes()
    config = json.loads(raw.decode('utf-8-sig'))
    if config.get('schema') != 1 or not isinstance(config.get('modes'), dict):
        raise ValueError('Invalid context routing schema')
    active, seen = mode, set()
    while True:
        if active in seen:
            raise ValueError('Cyclic stage routing alias')
        seen.add(active)
        profile = config['modes'].get(active)
        if isinstance(profile, str):
            active = profile
        else:
            break
    if not isinstance(profile, dict):
        return fallback('No stage profile for mode; full mode sources required')
    stages = profile.get('stages')
    if not isinstance(stages, dict) or any(k not in STAGES[:-1] for k in stages):
        raise ValueError('Invalid stage profile')
    classified = set()
    for name, row in stages.items():
        if not isinstance(row, dict):
            raise ValueError('Invalid stage row: ' + name)
        classified.update(strings(row.get('sources', []), name + '.sources'))
        strings(row.get('tasks', []), name + '.tasks')
        for flag in ('species', 'angling'):
            if flag in row and type(row[flag]) is not bool:
                raise ValueError('Expected boolean: ' + name + '.' + flag)
    effects_config = config.get('effects', {})
    if not isinstance(effects_config, dict):
        raise ValueError('Invalid effects map')
    unknown = [e for e in effects if e not in effects_config]
    if unknown:
        result = fallback('Unknown effects: ' + ', '.join(unknown))
        result.update(config=config_path, config_sha256=hashlib.sha256(raw).hexdigest())
        return result
    if stage != 'all' and stage not in stages:
        result = fallback('Stage not configured for mode; full mode sources required')
        result.update(config=config_path, config_sha256=hashlib.sha256(raw).hexdigest())
        return result
    selected_stages = list(stages) if stage == 'all' else [stage]
    rows = [stages[name] for name in selected_stages]
    files = [p for row in rows for p in row.get('sources', [])]
    override_map = config.get('task_overrides', {})
    if not isinstance(override_map, dict):
        raise ValueError('Invalid mode task override map')
    overrides = override_map.get(mode, {})
    if not isinstance(overrides, dict):
        raise ValueError('Invalid mode task overrides')
    tasks = [t for name in selected_stages for t in
             strings(overrides.get(name, stages[name].get('tasks', [])), name + '.tasks')]
    unassigned = [p for p in baseline if p not in classified]
    files += unassigned
    # Effects add dependencies. They never subtract mandatory mode sources.
    queue, visited = list(effects), set()
    while queue:
        effect = queue.pop()
        if effect in visited:
            continue
        visited.add(effect)
        row = effects_config.get(effect)
        if not isinstance(row, dict):
            raise ValueError('Invalid/missing effect dependency: ' + effect)
        files += strings(row.get('sources', []), effect + '.sources')
        tasks += strings(row.get('tasks', []), effect + '.tasks')
        queue += strings(row.get('requires', []), effect + '.requires')
    return dict(stage=stage, effective_stage=stage, effects=sorted(visited),
        files=list(dict.fromkeys(files)), tasks=list(dict.fromkeys(tasks)),
        include_species=any(row.get('species', True) for row in rows) or bool(effects),
        include_angling=any(row.get('angling', True) for row in rows) or bool(effects),
        fallback=None, unassigned=unassigned, config=config_path,
        config_sha256=hashlib.sha256(raw).hexdigest())


def dependency_digest(packet):
    dependencies = {s['path']: s['sha256'] for s in packet.get('dependencies', [])}
    # context-map is a source, but changing its routing also invalidates reuse.
    dependencies.update({s['path']: s['sha256'] for s in packet['sources']
                         if s['path'].endswith('/context-map.json')})
    return hashlib.sha256(json.dumps(dependencies, sort_keys=True).encode()).hexdigest()


def pages(text, limit):
    """Split an oversized source at headings, then lines; joining the pages restores it exactly."""
    if len(text) <= limit:
        return [text]
    pieces = []
    for segment in re.split(r'(?m)^(?=#{1,6} )', text):
        if len(segment) <= limit:
            pieces.append(segment)
            continue
        buffer = ''
        for line in segment.splitlines(keepends=True):
            while len(line) > limit:
                if buffer:
                    pieces.append(buffer)
                    buffer = ''
                pieces.append(line[:limit])
                line = line[limit:]
            if buffer and len(buffer) + len(line) > limit:
                pieces.append(buffer)
                buffer = ''
            buffer += line
        pieces.append(buffer)
    result, current = [], ''
    for piece in filter(None, pieces):
        if current and len(current) + len(piece) > limit:
            result.append(current)
            current = ''
        current += piece
    return result + [current] if current else result


def render(packet, root, context_id=None, seen=(), retained=False, paths=(), max_chars=None, page_large=False):
    """Plaintext view plus a local display receipt, not proof of model comprehension.

    Reuse is an explicit assertion that FULL untruncated text remains in this
    exact context epoch. Compaction/unknown context must not pass retained=True.
    page_large splits a source longer than max_chars into pages; it counts as read
    only after every page was displayed in the same context.
    """
    if seen and (not retained or not context_id):
        raise ValueError('Reuse requires --retained and the same explicit --context-id')
    if page_large and not max_chars:
        raise ValueError('Paging requires --max-chars')
    current_digest = dependency_digest(packet)
    known, parts_known = set(), {}
    metadata_packets = set()
    for receipt in seen:
        if not isinstance(receipt, dict) or receipt.get('schema') != 1:
            raise ValueError('Invalid display receipt')
        if (receipt.get('context_id') == context_id and receipt.get('root') == str(root.resolve())
                and receipt.get('dependency_digest') == current_digest):
            for row in receipt.get('sources', []):
                if not isinstance(row, dict) or not isinstance(row.get('path'), str) or not isinstance(row.get('sha256'), str):
                    raise ValueError('Invalid receipt source')
                known.add((row['path'], row['sha256']))
            for row in receipt.get('partial_sources', []):
                key = (row['path'], row['sha256'], row['page_chars'])
                parts_known.setdefault(key, set()).update(row['pages_done'])
            metadata_packets.update(receipt.get('metadata_packets', []))
    offered = {s['path'] for s in packet['sources']}
    if set(paths) - offered:
        raise ValueError('Requested source not in packet')
    sources = [s for s in packet['sources'] if not paths or s['path'] in paths]
    remaining = [s for s in sources if (s['path'], s['sha256']) not in known]
    if max_chars is not None and (type(max_chars) is not int or max_chars < 1):
        raise ValueError('max_chars must be a positive integer')
    units = []
    for row in remaining:
        split = pages(row['text'], max_chars) if page_large else [row['text']]
        done = parts_known.get((row['path'], row['sha256'], max_chars), set()) if len(split) > 1 else set()
        units += [(row, index, len(split), text) for index, text in enumerate(split) if index not in done]
    chosen, length = [], 0
    for unit in units:
        if max_chars and chosen and length + len(unit[3]) > max_chars:
            break
        chosen.append(unit)
        length += len(unit[3])
    # Never chop a source to fit a display target unless paging was requested.
    next_sources = list(dict.fromkeys(unit[0]['path'] for unit in units[len(chosen):]))
    packet_digest = hashlib.sha256(json.dumps(packet, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    memory = {k: v for k, v in packet['memory'].items() if k != 'fingerprint'}
    for state in ('active', 'candidates', 'retired'):
        memory[state] = [{k: v for k, v in row.items() if k != 'sha256'}
                         for row in memory.get(state, [])]
    # Keep conditions, scope, status, errors and continuation cursors visible.
    header = {k: packet[k] for k in ('project', 'mode', 'species', 'interaction', 'pending')}
    if 'routing' in packet:
        header['routing'] = {k: packet['routing'][k] for k in
                             ('stage', 'effective_stage', 'effects', 'tasks', 'fallback', 'unassigned')}
    if packet.get('asset_selection') is not None:
        header['planned_asset_refs'] = [dict(asset_id=r['asset_id'], path=(r.get('file') or {}).get('path')) for r in packet['asset_selection']['records']]
        header['asset_review_pending'] = packet.get('asset_review_pending',[])
        header['asset_scope'] = 'Planned references; open actual files; not proof of model use or visual QA'
    header['memory'] = memory
    header['selected_lessons'] = [{k: v for k, v in r.items() if k != 'sha256'}
                                  for r in packet.get('selected_lessons', [])]
    if packet_digest in metadata_packets:
        # Identical verified packet, with its descriptor explicitly still retained.
        # Repeating all task/condition metadata at every file batch wastes context.
        header = dict(continued_retained_packet=True, project=packet['project'], mode=packet['mode'],
                      pending=packet['pending'], memory_remaining=memory['remaining'])
        if memory['next_cursor'] or memory['errors']:
            header.update(memory_next_cursor=memory['next_cursor'], memory_errors=memory['errors'])
    output = json.dumps(header, ensure_ascii=False, separators=(',', ':')) + '\n'
    displayed = set()
    reused = [row['path'] for row in sources if (row['path'], row['sha256']) in known]
    for row, index, total, text in chosen:
        if total == 1:
            output += '\nSOURCE ' + row['path'] + '\n' + text + '\nEND SOURCE\n'
            displayed.add((row['path'], row['sha256']))
            continue
        output += f"\nSOURCE {row['path']} PAGE {index + 1}/{total}\n" + text + '\nEND PAGE\n'
        key = (row['path'], row['sha256'], max_chars)
        parts_known.setdefault(key, set()).add(index)
        if len(parts_known[key]) == total:
            displayed.add((row['path'], row['sha256']))
    complete = known | displayed
    partial = [dict(path=p, sha256=h, page_chars=size, pages_done=sorted(done))
               for (p, h, size), done in sorted(parts_known.items()) if (p, h) not in complete]
    output += '\nREUSED IN ASSERTED CURRENT CONTEXT: ' + str(len(reused)) + ' sources (paths in local manifest)'
    output += '\nNEXT SOURCES: ' + json.dumps(dict(count=len(next_sources), next=next_sources[:1]), ensure_ascii=False)
    output += '\nEND VIEW — if truncated, do not reuse receipt; read missing sources with --source.\n'
    receipt = dict(schema=1, root=str(root.resolve()), context_id=context_id,
        dependency_digest=current_digest,
        metadata_packets=sorted(metadata_packets | {packet_digest}), remaining_sources=next_sources,
        sources=[dict(path=p, sha256=h) for p, h in sorted(complete)],
        note='Display receipt only. --retained asserts full text still present; not proof of reading or semantic QA.')
    if partial:
        receipt['partial_sources'] = partial
    return output, receipt
