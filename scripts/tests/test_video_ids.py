"""Allocator invariants exercised on temporary workspaces only."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest
from contextlib import closing
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('video_ids', Path(__file__).resolve().parents[1] / 'video_ids.py')
ids = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ids)


class VideoIdTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for slug in ['one', 'two']:
            path = self.root / '03-Projects' / slug
            path.mkdir(parents=True)
            (path / 'PROJECT.md').write_text(f'ID: stable-{slug} | Status: configured\n', encoding='utf-8')

    def test_init_is_idempotent_and_does_not_create_video(self):
        first = ids.initialize(self.root, 'one')
        self.assertEqual(first, ids.initialize(self.root, 'one'))
        self.assertRegex(first['prefix'], r'^[A-Z]{3}$')
        self.assertFalse((self.root / '04-Productions').exists())

    def test_first_number_and_uuid_identity(self):
        ids.initialize(self.root, 'one', 'ABC')
        first = ids.reserve(self.root, 'one')
        second = ids.reserve(self.root, 'one')
        self.assertEqual(first['video_id'], 'ABC-00001')
        self.assertEqual(second['video_id'], 'ABC-00002')
        self.assertNotEqual(first['video_uuid'], second['video_uuid'])
        path = self.root / '04-Productions/one/ABC-00001/IDENTITY.json'
        self.assertEqual(json.loads(path.read_text()), first)

    def test_prefix_collision_and_change_are_rejected(self):
        ids.initialize(self.root, 'one', 'ABC')
        with self.assertRaises(ValueError):
            ids.initialize(self.root, 'two', 'ABC')
        with self.assertRaises(ValueError):
            ids.initialize(self.root, 'one', 'DEF')

    def test_invalid_prefix_and_slug_are_rejected(self):
        for prefix in ['AB', 'ABCD', 'abc', 'A01']:
            with self.assertRaises(ValueError):
                ids.initialize(self.root, 'one', prefix)
        with self.assertRaises(ValueError):
            ids.initialize(self.root, '../outside')

    def test_imported_prefix_is_not_claimed(self):
        (self.root / '04-Productions/two/ABC-00002').mkdir(parents=True)
        with self.assertRaises(ValueError):
            ids.initialize(self.root, 'one', 'ABC')

    def test_ledger_reservation_is_respected(self):
        ids.initialize(self.root, 'one', 'ABC')
        (self.root / '03-Projects/one/idea-ledger.md').write_text('ABC-00009 retired\n')
        self.assertEqual(ids.reserve(self.root, 'one')['video_id'], 'ABC-00010')

    def test_deleted_video_number_is_not_reused(self):
        first = ids.reserve(self.root, 'one')
        shutil.rmtree(self.root / '04-Productions/one' / first['video_id'])
        self.assertTrue(ids.reserve(self.root, 'one')['video_id'].endswith('-00002'))

    def test_project_rename_keeps_identity(self):
        before = ids.initialize(self.root, 'one')
        (self.root / '03-Projects/one').rename(self.root / '03-Projects/renamed')
        after = ids.initialize(self.root, 'renamed')
        self.assertEqual(before, after)

    def test_concurrent_reservations_are_unique_and_sequential(self):
        ids.initialize(self.root, 'one', 'ABC')
        with ThreadPoolExecutor(max_workers=5) as pool:
            results = list(pool.map(lambda _: ids.reserve(self.root, 'one'), range(10)))
        self.assertEqual(sorted(r['video_id'] for r in results), [f'ABC-{n:05d}' for n in range(1, 11)])
        self.assertEqual(len({r['video_uuid'] for r in results}), 10)

    def test_counter_exhaustion_does_not_wrap(self):
        ids.initialize(self.root, 'one', 'ABC')
        with closing(sqlite3.connect(self.root / '.nature-studio/video-ids.sqlite3')) as db:
            db.execute('UPDATE projects SET last_number=99999')
            db.commit()
        with self.assertRaises(ValueError):
            ids.reserve(self.root, 'one')

    def test_legacy_folder_is_untouched(self):
        folder = self.root / '04-Productions/one/UF-0001'
        folder.mkdir(parents=True)
        (folder / 'SUMMARY.md').write_bytes(b'legacy bytes')
        ids.initialize(self.root, 'one', 'ABC')
        self.assertEqual(ids.reserve(self.root, 'one')['video_id'], 'ABC-00001')
        self.assertEqual((folder / 'SUMMARY.md').read_bytes(), b'legacy bytes')

    def test_registry_is_excluded_from_distribution_package(self):
        spec = importlib.util.spec_from_file_location('packager', Path(__file__).resolve().parents[1] / 'package_workspace.py')
        package = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(package)
        self.assertFalse(package.included(package.ROOT / '.nature-studio/video-ids.sqlite3'))
        base = package.ROOT / '01-Knowledge/benchmarks/example'
        for rel in ['evidence/source.jpg', 'captions-raw.json', 'evidence-manifest.json']:
            self.assertFalse(package.included(base / rel))
        self.assertTrue(package.included(base / 'REPORT.md'))
        self.assertTrue(package.included(base / 'corpus.json'))

    def test_failed_identity_write_does_not_reuse_reservation(self):
        ids.initialize(self.root, 'one', 'ABC')
        original = Path.open
        def failing_open(path, *args, **kwargs):
            if path.name == 'IDENTITY.json':
                raise PermissionError('fixture identity write failure')
            return original(path, *args, **kwargs)
        with patch.object(Path, 'open', failing_open):
            with self.assertRaises(PermissionError):
                ids.reserve(self.root, 'one')
        self.assertEqual(ids.reserve(self.root, 'one')['video_id'], 'ABC-00002')


if __name__ == '__main__':
    unittest.main()
