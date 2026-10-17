"""Deterministic text checks and append-only attempt writes; no semantic/media QA."""
import argparse
import hashlib
from decimal import Decimal
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

from chayvideo_context import ROOT, inside, slug_ok
from video_ids import project as project_id

FIELDS = ('idea', 'first_frame_prompt', 'video_prompt', 'caption')
FRAME_FIELDS = ('subjects', 'environment', 'composition', 'initial_state')


def frame_errors(state):
    if not isinstance(state, dict) or set(state) != set(FRAME_FIELDS):
        return ['frame_state: supply subjects, environment, composition, initial_state']
    return [f'frame_state.{key}: nonempty text required' for key in FRAME_FIELDS
            if not isinstance(state[key], str) or not state[key].strip()]


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def production(root, slug, production_id):
    slug_ok(slug)
    if not isinstance(production_id, str) or not re.fullmatch(r'(?:[A-Z]{3}-\d{5}|UF-\d{4})', production_id):
        raise ValueError('Invalid production ID')
    folder = inside(root, f'04-Productions/{slug}/{production_id}')
    if not folder.is_dir():
        raise ValueError('Existing production required; no ID is allocated')
    if re.fullmatch(r'[A-Z]{3}-\d{5}', production_id):
        identity = json.loads((folder / 'IDENTITY.json').read_text(encoding='utf-8-sig'))
        if identity.get('video_id') != production_id:
            raise ValueError('Reserved identity mismatch')
        if identity.get('project_id') not in (None, project_id(root, slug)):
            raise ValueError('Reserved Project identity mismatch')
    return folder


def local_file(folder, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ValueError('Use a production-relative path with forward slashes')
    rel = Path(relative)
    path = (folder / rel).resolve()
    if rel.is_absolute() or '..' in rel.parts or not path.is_relative_to(folder.resolve()):
        raise ValueError('Path outside production')
    if not path.is_file():
        raise ValueError(f'Missing file: {relative}')
    return path


def attempt_file(folder, ref):
    if not isinstance(ref, str) or not re.fullmatch(r'(?:attempts/)?A\d+', ref):
        raise ValueError('Explicit attempt required: A01 or attempts/A01; never latest')
    file = local_file(folder, ref + '/OUTPUT.json')
    if (file.parent / 'SAVE-INCOMPLETE.txt').exists():
        raise ValueError(f'Incomplete attempt: {ref}')
    return file


def resolve(root, slug, production_id, attempt):
    """Read an explicit revision chain, without selecting, approving or writing anything."""
    folder = production(root, slug, production_id)
    chain, seen = [], set()
    ref = attempt
    while True:
        file = attempt_file(folder, ref)
        if file in seen:
            raise ValueError('Revision cycle')
        if len(chain) >= 128:
            raise ValueError('Revision chain too deep; inspect sources')
        seen.add(file)
        data = json.loads(file.read_text(encoding='utf-8-sig'))
        if not isinstance(data, dict):
            raise ValueError(f'Invalid OUTPUT: {ref}')
        if 'state_schema' in data and data['state_schema'] != 1:
            raise ValueError(f'Unsupported state_schema: {ref}')
        for key in FIELDS:
            if key in data and (not isinstance(data[key], str) or not data[key].strip()):
                raise ValueError(f'Invalid {key}: {ref}')
        if 'frame_state' in data and frame_errors(data['frame_state']):
            raise ValueError(f'Invalid frame_state: {ref}')
        chain.append((ref, file, data))
        parent = data.get('base_attempt')
        if parent is None:
            if not all(key in data for key in FIELDS):
                raise ValueError(f'Legacy/partial attempt {ref} has no explicit base; inspect original sources')
            if data.get('mode') in {'revision', 'caption'}:
                raise ValueError(f'Missing revision base: {ref}')
            break
        base = attempt_file(folder, parent)
        if data.get('base_sha256') != sha256(base):
            raise ValueError(f'Base changed: {parent}; inspect sources before reuse')
        ref = parent
    values, sources, state = {}, {}, None
    for ref, file, data in reversed(chain):
        changed = set(FIELDS).intersection(data)
        if data.get('mode') == 'caption' and (changed != {'caption'} or 'frame_state' in data):
            raise ValueError('Caption attempt must not change story or frame state')
        if changed.intersection(FIELDS[:3]):
            # A semantic revision cannot silently certify unchanged t=0.
            state = data.get('frame_state')
        for key in changed:
            values[key] = data[key]
            sources[key] = dict(attempt=ref, sha256=sha256(file))
    result = dict(production_id=production_id, project=slug, attempt=attempt,
                attempt_sha256=sha256(chain[0][1]),
                output=values, sources=sources, frame_state=state,
                frame_state_status='recorded' if state else 'unverified',
                scope='Explicit inputs only; no selection, approval or semantic QA')
    if state:
        result['frame_inputs'] = frame_snapshot(result)
        result['frame_inputs_sha256'] = snapshot_hash(result['frame_inputs'])
    return result


def frame_snapshot(resolved):
    """Only opening-state inputs; caption and later motion do not invalidate an image."""
    state = resolved.get('frame_state')
    if frame_errors(state):
        raise ValueError('Opening state unverified; record/review frame_state first')
    return dict(frame_state=state, first_frame_prompt=resolved['output']['first_frame_prompt'])


def snapshot_hash(snapshot):
    return hashlib.sha256(json.dumps(snapshot, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':')).encode('utf-8')).hexdigest()


def check_frame(root, slug, production_id, attempt, handoff='FIRST-FRAME.json'):
    """Verify recorded bindings, never infer image quality from metadata."""
    folder = production(root, slug, production_id)
    current = resolve(root, slug, production_id, attempt)
    record = json.loads(local_file(folder, handoff).read_text(encoding='utf-8-sig'))
    if not isinstance(record, dict):
        raise ValueError('Invalid handoff object')
    errors, review, unknown = [], [], []
    if record.get('production_id') != production_id or record.get('project_id') != project_id(root, slug):
        errors.append('Handoff production/Project mismatch')
    if record.get('qa_status') != 'qa_pass':
        review.append('No recorded qa_pass')
    for path_key, hash_key in [('image_path', 'sha256'), ('review_path', 'review_sha256')]:
        try:
            path = local_file(folder, record.get(path_key))
            expected = record.get(hash_key)
            if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
                unknown.append(f'Missing/invalid {hash_key}')
            elif sha256(path) != expected:
                errors.append(f'{path_key} hash changed')
        except ValueError as exc:
            errors.append(str(exc))
    snapshot = record.get('frame_inputs')
    if not isinstance(snapshot, dict) or set(snapshot) != {'frame_state', 'first_frame_prompt'}:
        unknown.append('Legacy/missing frame_inputs; review actual image against current opening state')
    elif frame_errors(snapshot['frame_state']) or not isinstance(snapshot['first_frame_prompt'], str) or not snapshot['first_frame_prompt'].strip():
        errors.append('Malformed frame_inputs')
    elif record.get('frame_inputs_sha256') != snapshot_hash(snapshot):
        errors.append('Recorded frame_inputs hash mismatch')
    else:
        try:
            if snapshot != frame_snapshot(current):
                review.append('Opening inputs changed; inspect actual image, do not automatically regenerate')
        except ValueError as exc:
            unknown.append(str(exc))
    # Bind the QA snapshot to the exact source attempt; do not require current==QA attempt.
    if record.get('schema') == 2:
        image_attempt = record.get('attempt_id')
        if not isinstance(image_attempt, str) or not re.fullmatch(r'(?:attempts/)?A\d+', image_attempt):
            errors.append('Explicit image attempt_id required')
        else:
            directory = (folder / image_attempt).resolve()
            if not directory.is_relative_to(folder.resolve()) or not directory.is_dir():
                errors.append('Image attempt missing/outside production')
            elif (directory / 'SAVE-INCOMPLETE.txt').exists():
                errors.append('Image attempt incomplete')
        try:
            reviewed = resolve(root, slug, production_id, record.get('source_attempt'))
            if record.get('source_attempt_sha256') != sha256(attempt_file(folder, record.get('source_attempt'))):
                errors.append('QA source attempt changed')
            if frame_snapshot(reviewed) != snapshot:
                errors.append('QA snapshot does not match its source attempt')
        except (ValueError, FileNotFoundError) as exc:
            unknown.append(str(exc))
    else:
        unknown.append('Legacy handoff needs explicit provenance review; never silently upgraded')
    criteria = record.get('qa_sources')
    if not isinstance(criteria, dict) or not criteria:
        unknown.append('Missing QA criteria hashes')
    else:
        required = {'00-Standards/first-frame.md', '00-Standards/quality-review.md',
                    f'03-Projects/{slug}/PROJECT.md'}
        if not required.issubset(criteria):
            unknown.append('Missing common/Project QA source bindings')
        for rel, expected in criteria.items():
            try:
                if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or '..' in Path(rel).parts:
                    raise ValueError('Use workspace-relative QA source paths')
                path = inside(root, rel)
                if not path.is_file() or sha256(path) != expected:
                    review.append(f'QA criteria missing/changed: {rel}')
            except (ValueError, TypeError):
                errors.append('Invalid QA criteria path')
    status = 'invalid' if errors else 'needs_review' if review else 'unverified' if unknown else 'matched'
    return dict(status=status, errors=errors, needs_review=review, unverified=unknown,
                scope='Recorded file/input bindings only; image QA and user approval remain independent')


def validate(data, mode='new', underwater=False):
    if not isinstance(data, dict):
        return ['Output must be a JSON object']
    errors = []
    if mode == 'caption' and (any(k in data for k in FIELDS[:3]) or 'frame_state' in data):
        errors.append('caption: only caption may change')
    if 'frame_state' in data:
        errors.extend(frame_errors(data['frame_state']))
    required = (('caption',) if mode == 'caption' else
                tuple(k for k in FIELDS if k in data) if mode == 'revision' else FIELDS)
    if not required:
        errors.append('revision: supply at least one output field')
    for key in required:
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f'Missing/non-string {key}')
    for key in FIELDS[1:]:
        if key in data and isinstance(data[key], str) and re.search(r'[\r\n]|\\[nr]', data[key]):
            errors.append(f'{key}: must be one paragraph')
    caption = data.get('caption')
    if underwater and isinstance(caption, str):
        tags = re.findall(r'#[\w]+', caption)
        if not 3 <= len(tags) <= 5 or len({x.casefold() for x in tags}) != len(tags):
            errors.append('caption: require 3–5 distinct hashtags')
        if not caption.split('#', 1)[0].strip():
            errors.append('caption: missing hook')
        if re.search(r'\bAI\b|\bAI[- ]generated\b', caption, re.I) or any(
                re.match(r'#(?:ai(?:generated|video|art|content)?|generativeai)$', t, re.I) for t in tags):
            errors.append('caption: AI mention/tag')
        if any(t.casefold() == '#underwater' for t in tags):
            errors.append('caption: #Underwater excluded')
    if underwater and mode != 'caption' and isinstance(data.get('video_prompt'), str):
        text = data['video_prompt']
        beats = re.findall(r'\[(\d+(?:\.\d+)?)\s*[–—-]\s*(\d+(?:\.\d+)?)s\]', text)
        beats = [(Decimal(a), Decimal(b)) for a, b in beats]
        if (not 5 <= len(beats) <= 8 or beats[0][0] != 0 or beats[-1][1] != 10
                or any(a >= b for a, b in beats)
                or any(beats[i][1] != beats[i+1][0] for i in range(len(beats)-1))):
            errors.append('video_prompt: 5–8 positive contiguous beats from 0 to 10s required')
        checks = data.get('checks', {})
        key = checks.get('key_onset') if isinstance(checks, dict) else None
        try:
            onset = Decimal(str(key))
            if not onset.is_finite() or not 5 < onset < 10:
                raise ValueError()
        except (ValueError, ArithmeticError):
            errors.append('checks.key_onset: provide actual intended onset >5 and <10')
    return errors


def save(root, slug, production_id, data, mode='new'):
    """Only an existing reserved/legacy production; the ID allocator remains authoritative.

    Data.files supplies AI-authored attempt documents, not fake generated metadata.
    Root brief/concept/ledger updates remain explicit workflow steps, never overwritten here.
    """
    base = production(root, slug, production_id)
    errors = validate(data, mode, underwater=(slug == 'underwater'))
    if errors:
        raise ValueError('; '.join(errors))
    provenance = dict(state_schema=1, mode=mode)
    if mode in {'revision', 'caption'}:
        ref = data.get('base_attempt')
        resolve(root, slug, production_id, ref)
        base_file = attempt_file(base, ref)
        expected = data.get('base_sha256')
        if expected != sha256(base_file):
            raise ValueError('Supply current base_sha256 from resolve; base missing or changed')
        provenance.update(base_attempt=ref, base_sha256=expected)
    docs = data.get('files', {})
    required = ('INPUTS.md', 'settings.md', 'review.md')
    if not isinstance(docs, dict) or any(not isinstance(docs.get(k), str) or not docs[k].strip() for k in required):
        raise ValueError('Supply INPUTS.md, settings.md, review.md with true prompt-only provenance')
    allowed = set(required) | {'revision.md'}
    if set(docs) - allowed:
        raise ValueError('Unexpected attempt document/path')
    # Respect actual local layout, do not relocate legacy attempts.
    parent = inside(root, (base / 'attempts').relative_to(root)) if (base / 'attempts').is_dir() else base
    stage = Path(tempfile.mkdtemp(prefix='.chayvideo-', dir=parent))
    try:
        payload = dict(docs)
        for key, name in [('first_frame_prompt', 'first-frame-prompt.md'),
                          ('video_prompt', 'video-prompt.md'), ('caption', 'caption.md')]:
            if key in data:
                payload[name] = data[key]
        payload['OUTPUT.json'] = json.dumps({**{k: data[k] for k in (*FIELDS, 'frame_state') if k in data}, **provenance},
                                          ensure_ascii=False, indent=2)
        for name, text in payload.items():
            (stage / name).write_text(text.rstrip() + '\n', encoding='utf-8')
        numbers = [int(p.name[1:]) for p in parent.iterdir()
                   if p.is_dir() and re.fullmatch(r'A\d+', p.name)]
        number = max(numbers, default=0) + 1
        while True:
            dest = parent / f'A{number:02d}'
            # mkdir(exist_ok=False) reserves the destination without replacing old attempts.
            try:
                dest.mkdir()
                break
            except FileExistsError:
                number += 1
        try:
            for path in stage.iterdir():
                path.rename(dest / path.name)
        except BaseException:
            # Keep incomplete attempt visible for recovery; never overwrite a prior attempt.
            (dest / 'SAVE-INCOMPLETE.txt').write_text('Inspect interrupted save before reuse.', encoding='utf-8')
            raise
        return dest
    finally:
        shutil.rmtree(stage)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('command', choices=('check', 'save', 'resolve', 'check-frame'))
    parser.add_argument('input', type=Path)
    parser.add_argument('--mode', choices=('new', 'revision', 'caption', 'reference'), default='new')
    parser.add_argument('--project', required=True)
    parser.add_argument('--production')
    parser.add_argument('--handoff', default='FIRST-FRAME.json')
    parser.add_argument('--frame-inputs', action='store_true', help='Include QA snapshot only when preparing a handoff')
    args = parser.parse_args()
    if args.command in {'resolve', 'check-frame'}:
        if not args.production:
            parser.error('--production required')
        if args.command == 'resolve':
            result = resolve(args.root.resolve(), args.project, args.production, args.input.as_posix())
            if not args.frame_inputs:
                result.pop('frame_inputs', None)
                result.pop('frame_inputs_sha256', None)
        else:
            result = check_frame(args.root.resolve(), args.project, args.production, args.input.as_posix(), args.handoff)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if args.command == 'resolve' or result['status'] == 'matched' else 2)
    data = json.loads(args.input.read_text(encoding='utf-8-sig'))
    if args.command == 'check':
        errors = validate(data, args.mode, args.project == 'underwater')
        scope = ('Syntax and declared Underwater gates; no semantic/media QA' if args.project == 'underwater'
                 else 'Common syntax only; AI must review the actual Project contract')
        print(json.dumps(dict(errors=errors, scope=scope), ensure_ascii=False))
        sys.exit(bool(errors))
    if not args.production:
        parser.error('--production required for save')
    print(save(args.root.resolve(), args.project, args.production, data, args.mode))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        print(json.dumps({'errors': [str(exc)], 'scope': 'No automatic source repair'}, ensure_ascii=False))
        sys.exit(1)
