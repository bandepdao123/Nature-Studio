"""Read-only production state bindings; QA, selection and human approval stay separate."""
import argparse
import hashlib
import json
from pathlib import Path, PureWindowsPath

DOMAINS = ('visual', 'motion', 'anatomy', 'audio', 'format')
STATUSES = ('pass', 'fail', 'not_checked', 'not_applicable')


def validate(state, base):
    errors, unknown = [], []
    base = Path(base).resolve()
    if not isinstance(state, dict):
        return dict(valid=False, errors=['State must be an object'], qa_pass=False, approval='none', unverified=[])
    schema = state.get('schema')
    if type(schema) is not int or schema not in (1, 2):
        errors.append('Unsupported schema')

    def binding(value, label, required=False):
        if value is None:
            if required: errors.append(label + ': binding required')
            return False
        if not isinstance(value, dict):
            errors.append(label + ': expected path/sha256 binding')
            return False
        rel = value.get('path')
        if not isinstance(rel, str) or not rel or '\\' in rel or PureWindowsPath(rel).drive:
            errors.append(label + ': invalid relative path')
            return False
        path = (base / rel).resolve()
        if Path(rel).is_absolute() or '..' in Path(rel).parts or not path.is_relative_to(base) or not path.is_file():
            errors.append(label + ': missing or outside production')
            return False
        if hashlib.sha256(path.read_bytes()).hexdigest() != value.get('sha256'):
            errors.append(label + ': hash mismatch')
            return False
        return True

    binding(state.get('current_text'), 'current_text', True)
    selected_ok = binding(state.get('selected_render'), 'selected_render')
    reviewed_ok = binding(state.get('reviewed_render'), 'reviewed_render')
    for field in ('first_frame', 'first_frame_handoff', 'actual_inputs_evidence'):
        if field in state: binding(state[field], field)
    qa = state.get('qa')
    if not isinstance(qa, dict):
        qa = {}
        errors.append('QA must be an object')
    if any(qa.get(key) not in STATUSES for key in DOMAINS):
        errors.append('QA must record each domain explicitly')
    passes = [key for key in DOMAINS if qa.get(key) == 'pass']
    all_pass = bool(passes) and all(qa.get(key) in ('pass', 'not_applicable') for key in DOMAINS)
    evidence_ok = binding(state.get('qa_evidence'), 'qa_evidence', schema == 2 and bool(passes))
    coverage = state.get('qa_coverage', {})
    if not isinstance(coverage, dict):
        coverage = {}
        errors.append('qa_coverage must be an object')
    for key in passes:
        row = coverage.get(key)
        if not isinstance(row, dict) or row.get('status') != 'complete' or not isinstance(row.get('method'), str) or not row['method'].strip():
            unknown.append('QA coverage incomplete: ' + key)
    if passes and not reviewed_ok:
        unknown.append('QA is not bound to a reviewed render')
        if schema == 2: errors.append('Pass domains require reviewed_render')
    if schema == 1:
        unknown.append('Legacy schema1: QA evidence/coverage not certified; preserve record and review explicitly')
    approval = state.get('approval')
    if approval not in ('none', 'provisional', 'final'):
        errors.append('Unknown approval')
    elif approval != 'none':
        if not selected_ok: errors.append('Render approval requires selected_render')
        record = state.get('approval_evidence')
        if schema == 1 and isinstance(record, str) and record:
            path = (base / record).resolve()
            if Path(record).is_absolute() or PureWindowsPath(record).drive or '..' in Path(record).parts or not path.is_relative_to(base) or not path.is_file():
                errors.append('Approval requires saved human evidence within production')
        else:
            binding(record, 'approval_evidence', True)
    return dict(valid=not errors, errors=errors, qa_pass=bool(schema == 2 and not errors and all_pass and reviewed_ok and evidence_ok and not unknown),
                approval=approval, unverified=unknown, qa_asset=state.get('reviewed_render'), selected_render=state.get('selected_render'),
                note='File bindings and declared coverage do not prove perception, actual generation inputs or human authorship. QA concerns reviewed_render; approval concerns selected_render.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('state', type=Path)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.state.read_text(encoding='utf-8-sig')), args.state.parent)
    except (ValueError, OSError) as exc:
        result = dict(valid=False, qa_pass=False, errors=[str(exc)])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['valid'] else 2)


if __name__ == '__main__': main()
