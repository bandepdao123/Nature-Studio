"""Safety invariants for memory records; fixtures never enter real memory."""
from pathlib import Path
import copy
import importlib.util
import json
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('memory_validator', Path(__file__).resolve().parents[1] / 'validate_memory.py')
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class MemoryValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.projects = {'one-id': 'one', 'two-id': 'two'}
        for pid, slug in self.projects.items():
            self.write(f'03-Projects/{slug}/PROJECT.md', f'ID: {pid} | Status: configured\n')
        namespaces = ['shared', 'projects/one', 'projects/two']
        for namespace in namespaces:
            self.write(f'05-Memory/{namespace}/INDEX.md', '')
            for status in validator.STATUS_DIRS.values():
                (self.root / '05-Memory' / namespace / status).mkdir()
        self.write('05-Memory/INDEX.md', '\n'.join(f'[namespace]({ns}/INDEX.md)' for ns in namespaces))
        self.write('04-Productions/one/T-001/review.md', 'Observed input/output discrepancy; no claims about media quality.')
        self.write('06-Evaluation/results/objective-check.md', 'Fixture only: controlled result record, not a real model run.')
        self.write('00-Standards/memory-policy.md', 'Fixture authorization for objective procedural activation.')
        self.data = {
            'id': 'L-test-unique', 'version': '0.1', 'status': 'candidate',
            'kind': 'procedural', 'action': 'Compare input/output identifiers before handoff.',
            'transfer_rationale': None, 'scope': 'project', 'project_id': 'one-id',
            'origin_project_ids': ['one-id'], 'production_ids': ['T-001'],
            'conditions': {'tasks': ['handoff'], 'models': [], 'interfaces': [], 'formats': []},
            'evidence': ['04-Productions/one/T-001/review.md'],
            'validation': {'result': 'not_checked', 'method': 'not_checked', 'records': [],
                           'regression_checked': False, 'unresolved_conflicts': [], 'changes_policy': False},
            'activation': {'method': 'none', 'date': None, 'authority': None}
        }

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def save(self, data, namespace=None, filename='lesson.md'):
        if namespace is None:
            namespace = 'shared' if data['scope'] == 'shared' else 'projects/' + self.projects[data['project_id']]
        status = validator.STATUS_DIRS[data['status']]
        rel = f'05-Memory/{namespace}/{status}/{filename}'
        path = self.write(rel, '---\n' + json.dumps(data) + '\n---\n# Actual lesson fixture\n')
        index = self.root / '05-Memory' / namespace / 'INDEX.md'
        index.write_text(index.read_text(encoding='utf-8') + f'\n[lesson]({status}/{filename})\n', encoding='utf-8')
        return path

    def active(self):
        data = copy.deepcopy(self.data)
        data.update(status='active', version='1.0')
        data['validation'].update(result='pass', method='objective',
                                  records=['06-Evaluation/results/objective-check.md'], regression_checked=True)
        data['activation'].update(method='automatic', date='2026-10-16', authority='00-Standards/memory-policy.md')
        return data

    def report(self):
        return validator.validate(self.root)

    def test_empty_namespaces_are_valid(self):
        self.assertTrue(self.report()['valid'])

    def test_candidate_with_evidence_is_valid(self):
        self.save(self.data)
        self.assertTrue(self.report()['valid'])

    def test_project_cannot_live_in_other_project_namespace(self):
        self.save(self.data, namespace='projects/two')
        self.assertFalse(self.report()['valid'])

    def test_shared_requires_transfer_rationale(self):
        self.data.update(scope='shared', project_id=None)
        self.save(self.data)
        self.assertFalse(self.report()['valid'])

    def test_shared_may_originate_in_one_project(self):
        self.data.update(scope='shared', project_id=None,
                         transfer_rationale='Identifier consistency is independent of subject matter; only handoff tasks apply.')
        self.save(self.data)
        self.assertTrue(self.report()['valid'])

    def test_missing_evidence_fails(self):
        self.data['evidence'] = ['missing.md']
        self.save(self.data)
        self.assertFalse(self.report()['valid'])

    def test_absolute_and_traversing_evidence_fails(self):
        for ref in ['C:/secret.md', '../outside.md', '/etc/passwd', 'https://example.com']:
            with self.subTest(ref=ref):
                self.assertFalse(validator.valid_ref(self.root, ref))

    def test_automatic_active_requires_real_result_references(self):
        data = self.active()
        data['validation']['records'] = []
        self.save(data)
        self.assertFalse(self.report()['valid'])

    def test_automatic_active_requires_regression(self):
        data = self.active()
        data['validation']['regression_checked'] = False
        self.save(data)
        self.assertFalse(self.report()['valid'])

    def test_automatic_empirical_activation_is_rejected(self):
        data = self.active()
        data['kind'] = 'empirical'
        self.save(data)
        self.assertFalse(self.report()['valid'])

    def test_conflicted_active_is_rejected(self):
        data = self.active()
        data['validation']['unresolved_conflicts'] = ['new contradictory result']
        self.save(data)
        self.assertFalse(self.report()['valid'])

    def test_policy_change_cannot_be_activated_as_lesson(self):
        data = self.active()
        data['validation']['changes_policy'] = True
        self.save(data)
        self.assertFalse(self.report()['valid'])

    def test_objective_procedural_active_is_structurally_valid(self):
        self.save(self.active())
        self.assertTrue(self.report()['valid'])

    def test_duplicate_ids_are_rejected(self):
        self.save(self.data, filename='first.md')
        self.save(self.data, filename='second.md')
        self.assertFalse(self.report()['valid'])

    def test_wrong_status_directory_is_rejected(self):
        path = self.save(self.data)
        path.rename(path.parent.parent / 'active' / path.name)
        self.assertFalse(self.report()['valid'])

    def test_user_activation_cannot_cite_blanket_policy_approval(self):
        data = self.active()
        data['activation']['method'] = 'user'
        self.save(data)
        self.assertFalse(self.report()['valid'])

    def test_repeat_validation_has_no_side_effects(self):
        self.save(self.data)
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.report()
        self.report()
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_malformed_field_types_fail_without_crashing(self):
        for field, value in [('status', []), ('project_id', {}), ('kind', []), ('scope', {})]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data[field] = value
                path = self.write('05-Memory/projects/one/candidates/malformed.md',
                                  '---\n' + json.dumps(data) + '\n---\n# malformed fixture\n')
                _, errors = validator.validate_record(self.root, path, self.projects)
                self.assertTrue(errors)

    def test_invalid_json_reports_error(self):
        self.write('05-Memory/projects/one/candidates/bad.md', '---\n{invalid}\n---\n')
        self.assertFalse(self.report()['valid'])


if __name__ == '__main__':
    unittest.main()
