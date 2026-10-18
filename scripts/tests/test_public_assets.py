"""Portable public assets and non-destructive import; synthetic bytes only."""
import copy
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import asset_catalog as a
import validate_publication as publication


class BundleTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name)
        for rel,data in [('08-Assets/images/ref.bin',b'synthetic image bytes'),('08-Assets/reviews/ref.md',b'synthetic static declaration'),('08-Assets/README.md',b'fixture')]:
            p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        def binding(rel):return dict(path=rel,sha256=a.file_hash(self.root/rel))
        self.record=dict(asset_id='AI-DEMO',entity_id='DEMO',kind='equipment',stage=None,variant='standard',view='side',roles=['anatomy'],origin='generated',source=dict(url=None,rights='synthetic fixture'),requires=[],applicability=dict(scope='shared',project_ids=[]),publication=dict(visibility='public',reviewed=True),file=binding('08-Assets/images/ref.bin'),review=dict(status='pass',roles=['anatomy'],evidence=binding('08-Assets/reviews/ref.md')))
        self.bundle=dict(schema=1,reviewed_for_publication=True,assets=[self.record]);self.write()
    def write(self):
        (self.root/'08-Assets/reference-library.json').write_text(json.dumps(self.bundle),encoding='utf-8')
    def install(self):return a.import_bundle(self.root,'08-Assets/reference-library.json')
    def guard(self):
        files=[p.relative_to(self.root).as_posix() for p in (self.root/'08-Assets').rglob('*') if p.is_file()]
        return publication.validate_files(files,lambda p:(self.root/p).read_bytes())

    def test_clean_machine_import_and_query(self):
        result=self.install();self.assertEqual(result['imported'],1)
        rec=a.selection(self.root,[dict(entity_id='DEMO',role='anatomy')],['AI-DEMO'],'new-project')
        self.assertEqual(a.verify(self.root,rec,'new-project')['status'],'matched');self.assertTrue(self.guard()['valid'])

    def test_repeat_import_keeps_private_local_provenance(self):
        self.install()
        row=a.details(self.root,['AI-DEMO'])['assets'][0]
        updated=row['record'];updated['publication']=dict(visibility='private',reviewed=False);updated['generation']={'private_notes':'keep private'}
        a.register(self.root,updated,row['record_sha256'])
        before=(self.root/a.CATALOG).read_bytes();result=self.install()
        self.assertEqual(result['kept_existing'],1);self.assertEqual(before,(self.root/a.CATALOG).read_bytes())

    def test_conflict_rejected_before_write(self):
        self.install();before=(self.root/a.CATALOG).read_bytes()
        self.record['variant']='different';self.write()
        with self.assertRaisesRegex(ValueError,'conflict'):self.install()
        self.assertEqual(before,(self.root/a.CATALOG).read_bytes())

    def test_corrupt_image_never_imported_or_published(self):
        (self.root/self.record['file']['path']).write_bytes(b'changed')
        with self.assertRaises(ValueError):self.install()
        self.assertFalse((self.root/a.CATALOG).exists());self.assertFalse(self.guard()['valid'])

    def test_unreviewed_export_rejected(self):
        self.record['publication']['reviewed']=False;self.write()
        with self.assertRaises(ValueError):self.install()
        self.assertFalse(self.guard()['valid'])

    def test_outside_path_rejected(self):
        self.record['file']['path']='../private.bin';self.write()
        with self.assertRaises(ValueError):self.install()
        self.assertFalse(self.guard()['valid'])

    def test_dependency_and_derivation_rebound_on_new_machine(self):
        child=copy.deepcopy(self.record);child['asset_id']='AI-CHILD';child['requires']=['AI-DEMO'];child['derived_from']=dict(parent_id='AI-DEMO',operation='Synthetic alternate view')
        self.bundle['assets']=[child,self.record];self.write();self.assertEqual(self.install()['imported'],2)
        rec=a.selection(self.root,[dict(entity_id='DEMO',role='anatomy')],['AI-CHILD'],'new-project')
        self.assertEqual(rec['status'],'matched');self.assertEqual(len(rec['records']),2)

    def test_cycle_or_missing_dependency_rejected_before_write(self):
        for dep in ('AI-DEMO','MISSING'):
            self.record['requires']=[dep];self.write()
            with self.assertRaises(ValueError):self.install()
            self.assertFalse((self.root/a.CATALOG).exists())

    def test_unlisted_files_not_published(self):
        (self.root/'08-Assets/extra.bin').write_bytes(b'unreviewed')
        self.assertFalse(self.guard()['valid'])


if __name__=='__main__':unittest.main()
