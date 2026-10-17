"""Public export safeguards, without publishing fixtures or touching runtime."""
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('public_guard', Path(__file__).resolve().parents[1] / 'validate_publication.py')
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


class PublicationTests(unittest.TestCase):
    def files(self, data=None):
        if data is None:
            data = {'publication': {'visibility': 'public', 'reviewed': True}, 'production_ids': [],
                    'evidence': ['01-Knowledge/source.md'], 'validation': {'records': []}, 'activation': {'authority': None}}
        return {'05-Memory/projects/test/candidates/L-test.md': ('---\n'+json.dumps(data)+'\n---\n# Safe summary').encode(),
                '05-Memory/projects/test/INDEX.md': b'[lesson](candidates/L-test.md)',
                '01-Knowledge/source.md': b'Public supporting evidence'}

    def check(self, files):
        return guard.validate_files(files, files.__getitem__)

    def test_runtime_and_snapshot_runtime_blocked(self):
        for path in ['04-Productions/a/X-0001/prompt.txt', '07-Releases/snapshots/old/04-Productions/a/clip.mp4', '03-Projects/a/idea-ledger.md', '.nature-studio/db']:
            with self.subTest(path=path):
                self.assertFalse(self.check({path: b'private'})['valid'])

    def test_template_and_runtime_readme_allowed(self):
        self.assertTrue(self.check({'04-Productions/README.md': b'Local only', '00-Standards/templates/idea-ledger.md': b'Empty template'})['valid'])

    def test_local_installation_manifests_blocked_in_public_tree(self):
        for path in ['07-Releases/manifests/story-development-installation-2026-10-16.json',
                     '07-Releases/manifests/taoanh-installation-2026-10-16.json',
                     '07-Releases/snapshots/old/07-Releases/manifests/tool-installation-2026-10-16.json']:
            with self.subTest(path=path):
                self.assertFalse(self.check({path: b'{"backup_root":"local-only"}'})['valid'])
        self.assertTrue(self.check({'07-Releases/manifests/public-baseline.json': b'{"source_version":"1.5"}'})['valid'])

    def test_packager_uses_same_installation_filter_and_preserves_original(self):
        spec = importlib.util.spec_from_file_location('packager_fixture', Path(__file__).resolve().parents[1] / 'package_workspace.py')
        package = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(package)
        with tempfile.TemporaryDirectory() as tmp:
            package.ROOT = Path(tmp)
            local = package.ROOT / '07-Releases/manifests/tool-installation-2026-10-17.json'
            local.parent.mkdir(parents=True)
            local.write_bytes(b'{"backup_root":"local-only"}')
            public = local.parent / 'public-baseline.json'
            public.write_bytes(b'{"source_version":"1.5"}')
            before = local.read_bytes()
            self.assertFalse(package.included(local))
            self.assertTrue(package.included(public))
            self.assertEqual(local.read_bytes(), before)

    def test_public_candidate_is_included_without_activation(self):
        files = self.files()
        self.assertTrue(self.check(files)['valid'])
        self.assertNotIn(b'active', next(iter(files.values())))

    def test_private_lesson_rejected(self):
        files = self.files({'publication': {'visibility': 'private', 'reviewed': False}})
        self.assertFalse(self.check(files)['valid'])

    def test_missing_sharing_review_rejected(self):
        self.assertFalse(self.check(self.files({}))['valid'])

    def test_private_evidence_cannot_be_hidden_by_missing_file(self):
        data = {'publication': {'visibility': 'public', 'reviewed': True}, 'production_ids': [],
                'evidence': ['04-Productions/test/private/review.md'], 'validation': {'records': []}}
        self.assertFalse(self.check(self.files(data))['valid'])

    def test_public_index_cannot_link_omitted_private_lesson(self):
        files = self.files()
        files['05-Memory/projects/test/INDEX.md'] += b'\n[private](candidates/L-private.md)'
        self.assertFalse(self.check(files)['valid'])

    def test_production_ids_must_be_cleaned(self):
        self.assertFalse(self.check(self.files({'publication': {'visibility': 'public', 'reviewed': True}, 'production_ids': ['PRIVATE-00001']}))['valid'])

    def test_browser_account_ui_evidence_blocked(self):
        self.assertFalse(self.check({'01-Knowledge/benchmarks/test/evidence/ui.jpg': b'UI'})['valid'])

    def test_public_knowledge_can_accompany_lessons(self):
        self.assertTrue(self.check(self.files())['valid'])


if __name__ == '__main__':
    unittest.main()
