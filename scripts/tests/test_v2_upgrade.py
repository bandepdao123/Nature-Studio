"""v2 migration, backward readers and patch policy on temporary data only."""
from pathlib import Path
from contextlib import closing
import sqlite3
import tempfile
import unittest
import uuid
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import video_ids as ids
import versioning
from chayvideo_output import production, resolve


class V2Tests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / '03-Projects/one').mkdir(parents=True)
        (self.root / '03-Projects/one/PROJECT.md').write_text('ID: stable-one\n', encoding='utf-8')

    def legacy(self):
        (self.root / '.nature-studio').mkdir()
        db = sqlite3.connect(self.root / '.nature-studio/video-ids.sqlite3')
        db.execute('CREATE TABLE projects(source_id TEXT PRIMARY KEY,uid TEXT UNIQUE NOT NULL,prefix TEXT UNIQUE NOT NULL,last_number INTEGER NOT NULL DEFAULT 0)')
        db.execute('CREATE TABLE videos(uid TEXT PRIMARY KEY,project_uid TEXT NOT NULL,code TEXT UNIQUE NOT NULL,number INTEGER NOT NULL)')
        uid, vid = str(uuid.uuid4()), str(uuid.uuid4())
        db.execute('INSERT INTO projects VALUES(?,?,?,?)',('stable-one',uid,'ABC',19))
        db.execute('INSERT INTO videos VALUES(?,?,?,?)',(vid,uid,'ABC-00019',19))
        db.commit(); db.close()
        return uid, vid

    def test_legacy_migration_preserves_identity_and_history(self):
        uid, vid = self.legacy()
        info = ids.initialize(self.root,'one','AB')
        self.assertEqual(info['project_uuid'],uid)
        self.assertEqual(ids.reserve(self.root,'one')['video_id'],'AB-0001')
        with closing(sqlite3.connect(self.root / '.nature-studio/video-ids.sqlite3')) as db:
            self.assertEqual(db.execute('SELECT code FROM videos WHERE uid=?',(vid,)).fetchone()[0],'ABC-00019')
            self.assertEqual(db.execute("SELECT prefix,last_number FROM series WHERE scheme='XXX-YYYYY'").fetchone(),('ABC',19))
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],2)

    def test_status_never_migrates_or_initializes(self):
        self.assertFalse(ids.status(self.root,'one')['initialized'])
        self.assertFalse((self.root / '.nature-studio').exists())
        self.legacy()
        path = self.root / '.nature-studio/video-ids.sqlite3'
        before = path.read_bytes()
        self.assertTrue(ids.status(self.root,'one')['migration_pending'])
        self.assertEqual(path.read_bytes(),before)

    def test_future_registry_is_not_downgraded(self):
        self.legacy()
        with closing(sqlite3.connect(self.root / '.nature-studio/video-ids.sqlite3')) as db:
            db.execute('PRAGMA user_version=3'); db.commit()
        path=self.root / '.nature-studio/video-ids.sqlite3'; before=path.read_bytes()
        with self.assertRaisesRegex(ValueError,'newer'): ids.initialize(self.root,'one','AB')
        self.assertEqual(path.read_bytes(),before)

    def test_old_binary_insert_is_blocked(self):
        uid, _ = self.legacy()
        ids.initialize(self.root,'one','AB')
        with closing(sqlite3.connect(self.root / '.nature-studio/video-ids.sqlite3')) as db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute('INSERT INTO videos VALUES(?,?,?,?)',(str(uuid.uuid4()),uid,'AB-00001',1))
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute('INSERT INTO projects VALUES(?,?,?,0)',('new',str(uuid.uuid4()),'DEF'))

    def test_failed_migration_rolls_back_legacy(self):
        uid, _ = self.legacy()
        folder=self.root/'04-Productions/other/AB-0001'; folder.mkdir(parents=True)
        with self.assertRaises(ValueError): ids.initialize(self.root,'one','AB')
        self.assertEqual(ids.status(self.root,'one')['current']['prefix'],'ABC')
        self.assertEqual(ids.status(self.root,'one')['current']['project_uuid'],uid)

    def test_reader_accepts_new_identity_and_rejects_mismatch(self):
        ids.initialize(self.root,'one','AB'); identity=ids.reserve(self.root,'one')
        folder=production(self.root,'one','AB-0001')
        for key, value in [('schema',1),('project_id','other'),('video_uuid','bad'),('id_format','wrong')]:
            bad=dict(identity); bad[key]=value
            (folder/'IDENTITY.json').write_text(json.dumps(bad),encoding='utf-8')
            with self.assertRaises(ValueError): production(self.root,'one','AB-0001')
        (folder/'IDENTITY.json').write_text(json.dumps(identity),encoding='utf-8')
        self.assertEqual(production(self.root,'one','AB-0001'),folder)

    def test_new_identity_resolves_attempt_without_reallocation(self):
        ids.initialize(self.root,'one','AB'); identity=ids.reserve(self.root,'one')
        folder=production(self.root,'one',identity['video_id'])
        attempt=folder/'attempts/A01'; attempt.mkdir(parents=True)
        data=dict(idea='test idea',first_frame_prompt='frame',video_prompt='video',caption='caption')
        (attempt/'OUTPUT.json').write_text(json.dumps(data),encoding='utf-8')
        self.assertEqual(resolve(self.root,'one','AB-0001','attempts/A01')['output']['idea'],'test idea')
        self.assertEqual(ids.status(self.root,'one')['current']['last_number'],1)

    def test_v2_requires_uuids_and_nonzero_number(self):
        ids.initialize(self.root,'one','AB'); identity=ids.reserve(self.root,'one')
        folder=production(self.root,'one','AB-0001')
        missing=dict(identity); del missing['video_uuid']
        (folder/'IDENTITY.json').write_text(json.dumps(missing),encoding='utf-8')
        with self.assertRaises(ValueError): production(self.root,'one','AB-0001')
        zero=folder.parent/'AB-0000'; zero.mkdir()
        identity['video_id']='AB-0000'
        (zero/'IDENTITY.json').write_text(json.dumps(identity),encoding='utf-8')
        with self.assertRaises(ValueError): production(self.root,'one','AB-0000')

    def test_reader_keeps_both_legacy_formats(self):
        for code in ('UF-0001','ABC-00001'):
            folder=self.root/'04-Productions/one'/code; folder.mkdir(parents=True)
            if code.startswith('ABC'): (folder/'IDENTITY.json').write_text(json.dumps({'video_id':code}),encoding='utf-8')
            self.assertEqual(production(self.root,'one',code),folder)

    def test_unicode_digits_are_rejected(self):
        with self.assertRaises(ValueError): production(self.root,'one','AB-０００１')

    def test_identity_and_registry_codes_reserve_prefixes(self):
        folder=self.root/'04-Productions/one/imported'; folder.mkdir(parents=True)
        (folder/'IDENTITY.json').write_text(json.dumps({'video_id':'AB-0009'}),encoding='utf-8')
        with self.assertRaises(ValueError): ids.initialize(self.root,'one','AB')

    def test_counter_exhaustion_does_not_wrap(self):
        ids.initialize(self.root,'one','AB')
        with closing(sqlite3.connect(self.root / '.nature-studio/video-ids.sqlite3')) as db:
            db.execute('UPDATE projects SET last_number=9999')
            db.execute('UPDATE series SET last_number=9999')
            db.commit()
        with self.assertRaisesRegex(ValueError,'9999'): ids.reserve(self.root,'one')

    def test_patch_policy_and_strict_version(self):
        self.assertEqual(versioning.next_version('2.0.0'),'2.0.1')
        self.assertEqual(versioning.next_version('2.0.9'),'2.0.10')
        self.assertEqual(versioning.next_version('2.0.9','minor'),'2.1.0')
        self.assertEqual(versioning.next_version('2.1.9','major'),'3.0.0')
        for bad in ('2.0','v2.0.0','2.00.1','2.0.1x'):
            with self.assertRaises(ValueError): versioning.next_version(bad)

    def test_version_check_requires_notes_and_current_markers(self):
        (self.root/'VERSION').write_text('2.0.0\n')
        for name in ('README.md','START-HERE.md','SYSTEM.md','CHANGELOG.md'):
            (self.root/name).write_text('v2.0.0\n')
        with self.assertRaises(ValueError): versioning.check(self.root)
        (self.root/'07-Releases').mkdir(); (self.root/'07-Releases/v2.0.0.md').write_text('notes')
        self.assertEqual(versioning.check(self.root),'2.0.0')
        (self.root/'README.md').write_text('v2.0.01')
        with self.assertRaises(ValueError): versioning.check(self.root)


if __name__ == '__main__': unittest.main()
