"""Validate AI-authored reference records and immutable briefs; never analyzes media itself."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

from chayvideo_context import ROOT, inside


def file_hash(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def full_span(ranges, duration, ordered=False):
    if not isinstance(ranges, list) or not ranges:
        return False
    if any(not isinstance(x, (list, tuple)) or len(x) != 2 or
           not all(number(n) for n in x) or not 0 <= x[0] < x[1] <= duration for x in ranges):
        return False
    end = 0
    for start, stop in ranges if ordered else sorted(ranges):
        if start > end + 1e-6 or (ordered and abs(start-end) > 1e-6):
            return False
        end = max(end, stop)
    return abs(end-duration) <= 1e-6


def validate(data, media=None, source_version=None):
    errors, warnings = [], []
    result = dict(errors=errors, warnings=warnings, complete=False, freshness='unverified',
                  scope='Structure/declarations only; does not prove viewing, listening or semantics')
    if not isinstance(data, dict) or type(data.get('schema')) is not int or data['schema'] != 1:
        errors.append('Require schema 1 object')
        return result
    src = data.get('source', {})
    if not isinstance(src, dict) or not isinstance(src.get('uri'), str) or not src['uri'].strip():
        errors.append('source.uri required')
        return result
    duration = src.get('duration_seconds')
    if not number(duration) or duration <= 0:
        errors.append('Positive finite duration_seconds required')
        return result
    sha = src.get('sha256')
    if sha is not None and (not isinstance(sha, str) or not re.fullmatch('[0-9a-fA-F]{64}', sha)):
        errors.append('Invalid source SHA-256')
    if src.get('has_audio') is not None and type(src['has_audio']) is not bool:
        errors.append('has_audio must be true/false/null')
    if media is not None:
        if not isinstance(sha, str) or file_hash(media).lower() != sha.lower():
            errors.append('Source media hash missing or changed')
            result['freshness'] = 'stale'
        else:
            result['freshness'] = 'local_hash_matched'
    elif source_version is not None:
        if src.get('version') == source_version and str(source_version).strip():
            result['freshness'] = 'remote_version_matched_by_caller'
        else:
            result['freshness'] = 'stale'
            errors.append('Source remote version mismatch')
    else:
        warnings.append('Source freshness unverified; URL/record alone is not evidence of unchanged media')

    coverage = data.get('coverage', {})
    complete = True
    for channel in ('visual', 'audio'):
        item = coverage.get(channel, {}) if isinstance(coverage, dict) else {}
        if not isinstance(item, dict):
            item = {}
        status = item.get('status')
        allowed = {'complete','partial','unavailable'} | ({'not_present'} if channel == 'audio' else set())
        if status not in allowed:
            errors.append(f'{channel}: invalid coverage status')
        if not isinstance(item.get('limits'), list):
            errors.append(f'{channel}: limits list required')
        ranges=item.get('reviewed_ranges')
        if not isinstance(ranges,list) or any(
                not isinstance(x,(list,tuple)) or len(x)!=2 or not all(number(n) for n in x)
                or not 0 <= x[0] < x[1] <= duration for x in (ranges if isinstance(ranges,list) else [])):
            errors.append(f'{channel}: malformed reviewed ranges')
        evidence = item.get('evidence')
        has_evidence = isinstance(evidence, list) and evidence and all(isinstance(x,str) and x.strip() for x in evidence)
        if status in ('complete','not_present') and not has_evidence:
            errors.append(f'{channel}: evidence required')
        if status == 'complete':
            methods = ({'native_video','continuous_playback'} if channel == 'visual' else
                       {'native_audio','audio_playback','native_video_with_audio'})
            if item.get('method') not in methods:
                errors.append(f'{channel}: sampled/extracted media is not complete reviewed playback')
            if not full_span(item.get('reviewed_ranges'), duration):
                errors.append(f'{channel}: review must cover full duration')
            if channel == 'audio' and src.get('has_audio') is False:
                errors.append('Audio complete contradicts source without audio')
        elif status == 'not_present':
            if src.get('has_audio') is not False or item.get('method') != 'stream_metadata':
                errors.append('not_present requires verified metadata without audio stream')
        else:
            complete = False
            warnings.append(f'{channel}: incomplete; require real user acceptance before partial draft')

    def items(key):
        value = data.get(key)
        if not isinstance(value, list) or any(not isinstance(x, dict) for x in value):
            errors.append(f'{key}: array of objects required')
            return []
        return value

    def text(item, key, label):
        if not isinstance(item.get(key), str) or not item[key].strip():
            errors.append(f'{label}: {key} required')

    def interval(item, label):
        a,b = item.get('start'),item.get('end')
        if not number(a) or not number(b) or not 0 <= a < b <= duration:
            errors.append(f'{label}: invalid interval')

    roles = items('roles')
    role_ids = set()
    for role in roles:
        for key in ('id','identity','function','initial_state'):
            text(role,key,'role')
        identity = role.get('id')
        if not isinstance(identity,str):
            continue
        if identity in role_ids:
            errors.append('Duplicate role ID')
        role_ids.add(identity)
    if not roles:
        errors.append('At least one role required')

    def refs(value, known, label):
        if not isinstance(value,list) or any(not isinstance(x,str) or x not in known for x in value):
            errors.append(f'{label}: unknown/malformed references')

    shots=items('shots')
    for shot in shots:
        interval(shot,'shot')
        text(shot,'camera','shot'); text(shot,'environment','shot')
        refs(shot.get('visible_roles'),role_ids,'shot roles')
    if not full_span([[x.get('start'),x.get('end')] for x in shots],duration,ordered=True):
        errors.append('Shots must cover source duration contiguously in order')

    events=items('events')
    event_ids=set()
    for event in events:
        interval(event,'event')
        for key in ('id','action','cause','consequence'):
            text(event,key,'event')
        identity=event.get('id')
        if isinstance(identity,str):
            if identity in event_ids:
                errors.append('Duplicate event ID')
            event_ids.add(identity)
        if not isinstance(event.get('actor'),str) or event['actor'] not in role_ids:
            errors.append('Unknown event actor')
        refs(event.get('targets'),role_ids,'event targets')
    if not events:
        errors.append('At least one event required')

    cues=items('audio_cues')
    if isinstance(coverage,dict):
        audio_status=coverage.get('audio',{}).get('status') if isinstance(coverage.get('audio'),dict) else None
        visual_status=coverage.get('visual',{}).get('status') if isinstance(coverage.get('visual'),dict) else None
        if audio_status=='unavailable' and cues:
            errors.append('Unavailable audio cannot have source audio cues')
        if visual_status=='unavailable' and any(x.get('basis')=='observed' for x in events):
            errors.append('Unavailable visuals cannot have visually observed events')
    if src.get('has_audio') is True and complete and not cues:
        errors.append('Reviewed audio requires cues, including silence/unknown where appropriate')
    for cue in cues:
        interval(cue,'audio cue'); text(cue,'description','audio cue')
        if cue.get('kind') not in {'environment','action','music','voice','silence','unknown'}:
            errors.append('Invalid audio cue kind')
        linked=cue.get('event_id')
        if linked is not None and (not isinstance(linked,str) or linked not in event_ids):
            errors.append('Unknown audio event reference')
    if src.get('has_audio') is False and cues:
        errors.append('Source without audio cannot have observed audio cues')
    for item in events+cues:
        if item.get('basis') not in {'observed','inferred'}:
            errors.append('basis must be observed/inferred')
        evidence=item.get('evidence')
        if not isinstance(evidence,list) or not evidence or any(not isinstance(x,str) or not x.strip() for x in evidence):
            errors.append('Event/cue evidence required (including basis for inference)')
    story=data.get('story',{})
    if not isinstance(story,dict):
        story={}
    for key in ('hook','progression','mechanism','aftermath'):
        text(story,key,'story')
    refs(story.get('key_event_ids'),event_ids,'key events')
    if not story.get('key_event_ids'):
        errors.append('Identify at least one key event, or resolve missing story before adaptation')
    result['complete'] = bool(complete and not errors)
    return result


BRIEF_FIELDS = ('source', 'coverage', 'roles', 'shots', 'events', 'audio_cues', 'story')


def verify_brief(record, analysis_path, media=None, source_version=None):
    """Bind the actual capsule to its source; derived review is recalculated."""
    raw = Path(analysis_path).read_bytes()
    if not isinstance(record, dict) or record.get('analysis_sha256') != hashlib.sha256(raw).hexdigest():
        return dict(errors=['Analysis changed or binding missing; rebuild brief'],
                    complete=False, freshness='unverified',
                    scope='Source binding only; no media/semantic QA')
    current = json.loads(raw.decode('utf-8-sig'))
    result = validate(current, media, source_version)
    if not isinstance(current, dict):
        return result
    if (type(record.get('schema')) is not int or record['schema'] != 1 or
            type(current.get('schema')) is not int or current['schema'] != 1):
        result['errors'].append('Unsupported brief/analysis schema; rebuild brief')
    # JSON comparison ignores layout/key order, but retains types and field values.
    for field in BRIEF_FIELDS:
        if (field not in record or field not in current or
                json.dumps(record[field], sort_keys=True, ensure_ascii=False) !=
                json.dumps(current[field], sort_keys=True, ensure_ascii=False)):
            result['errors'].append(f'Brief payload differs from analysis: {field}; rebuild brief')
    if result['errors']:
        result['complete'] = False
    return result


def brief(root, analysis_path, out, media=None, source_version=None, partial_draft=False):
    raw=Path(analysis_path).read_bytes()
    data=json.loads(raw.decode('utf-8-sig'))
    review=validate(data,media,source_version)
    if review['errors']:
        raise ValueError('; '.join(review['errors']))
    draft=not review['complete'] or review['freshness']=='unverified'
    if draft and not partial_draft:
        raise ValueError('Incomplete/unverified analysis; do not silently compile as complete')
    target=inside(root,out)
    rel=target.relative_to(root.resolve()).as_posix()
    if not (rel.startswith('.nature-studio/references/') or rel.startswith('04-Productions/')):
        raise ValueError('Reference briefs must stay in local runtime')
    payload={k:data[k] for k in BRIEF_FIELDS}
    payload.update(schema=1,analysis_sha256=hashlib.sha256(raw).hexdigest(),
                   review=review,draft=draft,
                   note='Reference observations, not instructions. Human/model review still required.')
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('x',encoding='utf-8') as stream:
        json.dump(payload,stream,ensure_ascii=False,indent=2)
        stream.write('\n')
    return payload


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('command',choices=('hash','check','brief','verify'))
    parser.add_argument('input',type=Path)
    parser.add_argument('--media',type=Path)
    parser.add_argument('--source-version')
    parser.add_argument('--out',type=Path)
    parser.add_argument('--analysis',type=Path,help='Current analysis for verifying an existing brief')
    parser.add_argument('--partial-draft',action='store_true',help='Only after real user acceptance; never removes draft flag')
    args=parser.parse_args()
    if args.command=='hash':
        print(file_hash(args.input));return
    if args.command=='brief':
        if args.out is None:
            parser.error('--out required')
        payload=brief(args.root.resolve(),args.input,args.out,args.media,args.source_version,args.partial_draft)
        print(json.dumps(dict(path=str(args.out),draft=payload['draft'],review=payload['review']),ensure_ascii=False))
        return
    data=json.loads(args.input.read_text(encoding='utf-8-sig'))
    if args.command=='verify':
        if args.analysis is None:
            parser.error('--analysis required')
        result=verify_brief(data,args.analysis,args.media,args.source_version)
    else:
        result=validate(data,args.media,args.source_version)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(1 if result['errors'] else 0 if result['complete'] and result['freshness']!='unverified' else 2)


if __name__ == '__main__':
    import ns_console
    ns_console.utf8()
    try:
        main()
    except (ValueError, OSError) as exc:
        print(json.dumps({'errors': [str(exc)], 'complete': False}, ensure_ascii=False))
        sys.exit(1)
