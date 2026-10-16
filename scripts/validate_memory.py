"""Validate portable memory records, scope boundaries and activation metadata.

This is a structural check, not proof that evidence or a lesson is true.
Only Python's standard library is required. Never mutates the workspace.
"""
from pathlib import Path, PureWindowsPath
from datetime import date
import argparse
import json
import re

STATUS_DIRS = {'candidate': 'candidates', 'active': 'active', 'retired': 'retired'}


def project_map(root):
    projects = {}
    for path in (root / '03-Projects').glob('*/PROJECT.md'):
        match = re.search(r'^ID:\s*([^|\r\n]+)', path.read_text(encoding='utf-8'), re.M)
        if not match:
            raise ValueError(f'Missing Project ID: {path.relative_to(root)}')
        pid = match.group(1).strip()
        if pid in projects:
            raise ValueError(f'Duplicate Project ID: {pid}')
        projects[pid] = path.parent.name
    return projects


def read_metadata(path):
    text = path.read_text(encoding='utf-8-sig')
    parts = text.split('---', 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError('Expected JSON metadata between opening --- delimiters')
    data = json.loads(parts[1])
    if not isinstance(data, dict):
        raise ValueError('Metadata must be an object')
    return data


def valid_ref(root, value):
    if not isinstance(value, str) or not value.strip():
        return False
    raw = value.split('#', 1)[0]
    if not raw or '\\' in raw or PureWindowsPath(raw).is_absolute() or ':' in raw:
        return False
    path = Path(raw)
    if path.is_absolute() or '..' in path.parts:
        return False
    resolved = (root / path).resolve()
    return resolved.is_relative_to(root.resolve()) and resolved.is_file()


def validate_record(root, path, projects):
    errors = []
    try:
        data = read_metadata(path)
    except (ValueError, OSError) as exc:
        return None, [str(exc)]

    def need(condition, message):
        if not condition:
            errors.append(message)

    lid = data.get('id')
    need(isinstance(lid, str) and bool(re.fullmatch(r'L-[A-Za-z0-9][A-Za-z0-9-]*', lid)),
         'Invalid or placeholder lesson ID')
    need(isinstance(data.get('version'), str) and bool(re.fullmatch(r'\d+\.\d+(?:\.\d+)?', data['version'])), 'Invalid version')
    need(data.get('kind') in ('procedural', 'empirical'), 'Invalid kind')
    need(isinstance(data.get('action'), str) and bool(data['action'].strip()), 'Missing actionable instruction')
    status = data.get('status')
    valid_status = isinstance(status, str) and status in STATUS_DIRS
    need(valid_status, 'Invalid status')
    scope = data.get('scope')
    need(scope in ('project', 'shared'), 'Invalid scope')
    pid = data.get('project_id')
    namespace = None
    if scope == 'project':
        valid_pid = isinstance(pid, str) and pid in projects
        need(valid_pid, 'Unknown stable Project ID')
        if valid_pid:
            namespace = root / '05-Memory' / 'projects' / projects[pid]
    elif scope == 'shared':
        need(pid is None, 'Shared lesson must use project_id null')
        need(isinstance(data.get('transfer_rationale'), str) and bool(data['transfer_rationale'].strip()), 'Shared lesson needs transfer rationale')
        namespace = root / '05-Memory' / 'shared'
    origins = data.get('origin_project_ids')
    need(isinstance(origins, list) and bool(origins) and all(isinstance(x, str) and x in projects for x in origins), 'Missing/unknown origin Project IDs')
    productions = data.get('production_ids')
    need(isinstance(productions, list) and all(isinstance(x, str) for x in productions), 'Invalid production_ids')
    conditions = data.get('conditions')
    need(isinstance(conditions, dict), 'Missing conditions')
    if isinstance(conditions, dict):
        for key in ('tasks', 'models', 'interfaces', 'formats'):
            values = conditions.get(key)
            need(isinstance(values, list) and all(isinstance(x, str) and x.strip() for x in values), f'Invalid condition {key}')
        need(bool(conditions.get('tasks')), 'At least one applicable task is required')
    evidence = data.get('evidence')
    need(isinstance(evidence, list) and bool(evidence) and all(valid_ref(root, x) for x in evidence), 'Missing/nonportable/broken evidence')
    validation = data.get('validation')
    activation = data.get('activation')
    need(isinstance(validation, dict), 'Missing validation')
    need(isinstance(activation, dict), 'Missing activation')
    if isinstance(validation, dict):
        need(validation.get('result') in ('not_checked', 'pass', 'fail'), 'Invalid validation result')
        need(validation.get('method') in ('not_checked', 'objective', 'empirical'), 'Invalid validation method')
        records = validation.get('records')
        need(isinstance(records, list) and all(valid_ref(root, x) for x in records), 'Broken validation records')
        need(type(validation.get('regression_checked')) is bool, 'regression_checked must be boolean')
        need(type(validation.get('changes_policy')) is bool, 'changes_policy must be boolean')
        need(isinstance(validation.get('unresolved_conflicts'), list), 'Invalid conflicts')
    if status == 'active' and isinstance(validation, dict) and isinstance(activation, dict):
        need(validation.get('unresolved_conflicts') == [], 'Active lesson has unresolved conflicts')
        need(validation.get('changes_policy') is False, 'Policy changes belong in decisions, not active lessons')
        method = activation.get('method')
        need(method in ('automatic', 'user'), 'Active lesson needs activation authority')
        need(valid_ref(root, activation.get('authority')), 'Missing activation authority file')
        try:
            date.fromisoformat(activation.get('date', ''))
        except (ValueError, TypeError):
            errors.append('Missing/invalid activation date')
        if method == 'automatic':
            need(data.get('kind') == 'procedural', 'Automatic empirical activation is prohibited')
            need(validation.get('result') == 'pass' and validation.get('method') == 'objective', 'Automatic activation requires objective pass')
            need(validation.get('regression_checked') is True, 'Automatic activation requires regression/exception checks')
            records = validation.get('records', [])
            need(isinstance(records, list) and bool(records) and all(isinstance(x, str) and x.startswith('06-Evaluation/results/') for x in records), 'Automatic activation needs evaluation results')
            need(activation.get('authority') == '00-Standards/memory-policy.md', 'Automatic authority must reference memory policy')
        elif method == 'user':
            need(activation.get('authority') != '00-Standards/memory-policy.md', 'Policy approval is not user approval of a lesson')
    if namespace is not None and valid_status:
        expected = namespace / STATUS_DIRS[status]
        need(path.parent.resolve() == expected.resolve(), 'Directory does not match Project/scope/status')
        index = namespace / 'INDEX.md'
        need(index.is_file(), 'Missing namespace INDEX')
        if index.is_file():
            link = f'{STATUS_DIRS[status]}/{path.name}'
            need(f']({link})' in index.read_text(encoding='utf-8'), 'Lesson missing from namespace INDEX')
    return data, errors


def validate(root):
    errors = []
    try:
        projects = project_map(root)
    except ValueError as exc:
        return {'valid': False, 'lesson_count': 0, 'errors': [str(exc)]}
    namespaces = [root / '05-Memory' / 'shared']
    namespaces += [root / '05-Memory' / 'projects' / slug for slug in projects.values()]
    for namespace in namespaces:
        for child in ['INDEX.md', *STATUS_DIRS.values()]:
            if not (namespace / child).exists():
                errors.append(f'Missing {namespace.relative_to(root)}/{child}')
    top = root / '05-Memory' / 'INDEX.md'
    if not top.is_file():
        errors.append('Missing root memory INDEX')
    else:
        text = top.read_text(encoding='utf-8')
        for namespace in namespaces:
            link = (namespace / 'INDEX.md').relative_to(top.parent).as_posix()
            if f']({link})' not in text:
                errors.append(f'Namespace not linked in root INDEX: {link}')
    seen = {}
    count = 0
    for path in sorted((root / '05-Memory').rglob('*.md')):
        if path.name in {'README.md', 'INDEX.md'}:
            continue
        count += 1
        data, issues = validate_record(root, path, projects)
        label = path.relative_to(root).as_posix()
        errors.extend(f'{label}: {issue}' for issue in issues)
        if data and isinstance(data.get('id'), str):
            lid = data['id']
            if lid in seen:
                errors.append(f'Duplicate lesson ID {lid}: {seen[lid]}, {label}')
            seen[lid] = label
    return {'valid': not errors, 'lesson_count': count, 'errors': errors}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = validate(args.root.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['valid'] else 1)
