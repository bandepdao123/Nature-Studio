"""Reference media protocol tests with declared fixtures; not actual video/audio analysis."""
import copy
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import reference_video as ref


def analysis():
    return dict(schema=1,
        source=dict(uri='user-file.mp4',sha256=None,version=None,duration_seconds=10,has_audio=True),
        coverage=dict(
            visual=dict(status='complete',method='native_video',reviewed_ranges=[[0,5],[5,10]],evidence=['tool visual observation 0–10'],limits=[]),
            audio=dict(status='complete',method='audio_playback',reviewed_ranges=[[0,10]],evidence=['tool audio observation 0–10'],limits=[])),
        roles=[dict(id='R1',identity='source animal',function='approacher',initial_state='left facing right'),
               dict(id='R2',identity='source prey',function='responder',initial_state='near cover')],
        shots=[dict(start=0,end=10,camera='fixed low angle',environment='source habitat',visible_roles=['R1','R2'])],
        events=[dict(id='E1',start=0,end=3,actor='R1',targets=['R2'],action='approach',cause='visible target',consequence='closer range',basis='observed',evidence=['visual 0–3']),
                dict(id='E2',start=2,end=4,actor='R2',targets=[],action='turn behind cover',cause='approach',consequence='miss',basis='observed',evidence=['visual 2–4'])],
        audio_cues=[dict(start=0,end=10,kind='environment',description='audible water texture',event_id=None,basis='observed',evidence=['audio 0–10']),
                    dict(start=2,end=4,kind='action',description='water movement, source uncertain',event_id='E2',basis='inferred',evidence=['audio and visual 2–4'])],
        story=dict(hook='approach toward cover',progression='approach then reversal',mechanism='direction change alters outcome',key_event_ids=['E2'],aftermath='target obscured'))


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.media=self.root/'input.mp4'
        self.media.write_bytes(b'fixture bytes, not playable media')
        self.data=analysis();self.data['source']['sha256']=ref.file_hash(self.media)
        self.path=self.root/'analysis.json'

    def write(self):
        self.path.write_text(json.dumps(self.data,ensure_ascii=False),encoding='utf-8')

    def test_declared_complete_is_only_structure_validation(self):
        result=ref.validate(self.data,self.media)
        self.assertFalse(result['errors'])
        self.assertTrue(result['complete'])
        self.assertIn('does not prove',result['scope'])

    def test_invalid_schema_types_rejected_before_brief_write(self):
        target = self.root / '.nature-studio/references/REF-test/brief.json'
        for schema in (True, 1.0, '1', 2):
            with self.subTest(schema=schema):
                self.data['schema'] = schema
                self.write()
                with self.assertRaises(ValueError):
                    ref.brief(self.root, self.path, target, self.media)
                self.assertFalse(target.exists())

    def test_sampled_frames_cannot_be_declared_complete(self):
        self.data['coverage']['visual']['method']='sampled_frames'
        self.assertTrue(ref.validate(self.data,self.media)['errors'])

    def test_extraction_is_not_listening(self):
        self.data['coverage']['audio']['method']='ffmpeg_extraction'
        self.assertTrue(ref.validate(self.data,self.media)['errors'])

    def test_visual_audio_gaps_both_rejected(self):
        for modality in ('visual','audio'):
            data=copy.deepcopy(self.data)
            data['coverage'][modality]['reviewed_ranges']=[[0,4],[5,10]]
            self.assertTrue(ref.validate(data,self.media)['errors'])

    def test_partial_audio_cannot_silently_become_full_brief(self):
        self.data['coverage']['audio'].update(status='unavailable',method='none',reviewed_ranges=[],evidence=[],limits=['audio inaccessible'])
        self.data['audio_cues']=[]
        self.write()
        with self.assertRaises(ValueError):
            ref.brief(self.root,self.path,'.nature-studio/references/REF-test/brief.json',self.media)
        result=ref.brief(self.root,self.path,'.nature-studio/references/REF-test/draft.json',self.media,partial_draft=True)
        self.assertTrue(result['draft'])
        self.assertEqual(result['coverage']['audio']['status'],'unavailable')

    def test_mute_requires_verified_no_audio_metadata(self):
        self.data['coverage']['audio'].update(status='not_present',method='stream_metadata')
        self.assertTrue(ref.validate(self.data,self.media)['errors'])
        self.data['source']['has_audio']=False
        self.data['audio_cues']=[]
        self.assertTrue(ref.validate(self.data,self.media)['complete'])

    def test_no_audio_contradiction_rejected(self):
        self.data['source']['has_audio']=False
        self.assertTrue(ref.validate(self.data,self.media)['errors'])

    def test_source_changed_same_length_invalidates_cache(self):
        old=self.media.read_bytes(); self.media.write_bytes(b'x'*len(old))
        result=ref.validate(self.data,self.media)
        self.assertTrue(result['errors']);self.assertEqual(result['freshness'],'stale')

    def test_url_alone_does_not_prove_freshness(self):
        self.data['source']['uri']='https://example.com/video'
        result=ref.validate(self.data)
        self.assertEqual(result['freshness'],'unverified')
        self.write()
        with self.assertRaises(ValueError):
            ref.brief(self.root,self.path,'.nature-studio/references/REF-test/brief.json')

    def test_remote_version_must_match_current_caller_value(self):
        self.data['source']['version']='version-1'
        self.assertTrue(ref.validate(self.data,source_version='version-2')['errors'])
        self.assertEqual(ref.validate(self.data,source_version='version-1')['freshness'],'remote_version_matched_by_caller')

    def test_role_and_key_and_audio_references_validated(self):
        for edit in ('actor','key','audio'):
            data=copy.deepcopy(self.data)
            if edit=='actor':data['events'][0]['actor']='missing'
            if edit=='key':data['story']['key_event_ids']=['missing']
            if edit=='audio':data['audio_cues'][0]['event_id']='missing'
            self.assertTrue(ref.validate(data,self.media)['errors'])

    def test_simultaneous_actions_are_allowed(self):
        self.assertFalse(ref.validate(self.data,self.media)['errors'])
        self.assertLess(self.data['events'][1]['start'],self.data['events'][0]['end'])

    def test_shot_gaps_and_overlap_rejected(self):
        for start in (4,6):
            data=copy.deepcopy(self.data)
            data['shots'][0]['end']=5
            shot=copy.deepcopy(data['shots'][0]);shot.update(start=start,end=10)
            data['shots'].append(shot)
            self.assertTrue(ref.validate(data,self.media)['errors'])

    def test_nan_negative_and_bool_duration_rejected(self):
        for value in (float('nan'),-1,0,True):
            data=copy.deepcopy(self.data);data['source']['duration_seconds']=value
            self.assertTrue(ref.validate(data,self.media)['errors'])

    def test_brief_preserves_events_audio_and_provenance_without_overwrite(self):
        self.write();out='.nature-studio/references/REF-test/brief-v001.json'
        value=ref.brief(self.root,self.path,out,self.media)
        self.assertEqual(value['events'],self.data['events'])
        self.assertEqual(value['audio_cues'],self.data['audio_cues'])
        self.assertEqual(value['analysis_sha256'],ref.file_hash(self.path))
        self.assertFalse(value['draft'])
        with self.assertRaises(FileExistsError):
            ref.brief(self.root,self.path,out,self.media)

    def test_brief_cannot_escape_or_write_system_source(self):
        self.write()
        for out in ('../outside.json','03-Projects/one/PROJECT.md'):
            with self.assertRaises(ValueError):
                ref.brief(self.root,self.path,out,self.media)

    def test_missing_evidence_is_not_complete(self):
        self.data['coverage']['visual']['evidence']=[]
        self.assertTrue(ref.validate(self.data,self.media)['errors'])

    def test_unavailable_audio_cannot_claim_source_cues(self):
        self.data['coverage']['audio'].update(status='unavailable',method='none',reviewed_ranges=[],evidence=[],limits=['not heard'])
        self.assertTrue(ref.validate(self.data,self.media)['errors'])

    def test_verify_cli_detects_analysis_changed_after_brief(self):
        self.write();out='.nature-studio/references/REF-test/brief.json'
        ref.brief(self.root,self.path,out,self.media)
        command=[sys.executable,'-X','utf8',str(Path(ref.__file__)),
                 '--root',str(self.root),'verify',str(self.root/out),
                 '--analysis',str(self.path),'--media',str(self.media)]
        good=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(good.returncode,0,good.stdout+good.stderr)
        self.data['story']['mechanism']='edited mechanism';self.write()
        stale=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(stale.returncode,1,stale.stdout+stale.stderr)
        self.assertIn('Analysis changed',stale.stdout)

    def verify_command(self, path):
        return [sys.executable, '-X', 'utf8', str(Path(ref.__file__)),
                '--root', str(self.root), 'verify', str(path),
                '--analysis', str(self.path), '--media', str(self.media)]

    def test_verify_cli_checks_the_brief_payload_and_schema(self):
        self.write()
        target = self.root / '.nature-studio/references/REF-test/brief.json'
        original = ref.brief(self.root, self.path, target, self.media)
        mutations = {'schema': 2, 'source': {**original['source'], 'uri': 'wrong.mp4'},
                     'coverage': {}, 'roles': [], 'shots': [], 'events': [],
                     'audio_cues': [], 'story': {**original['story'], 'mechanism': 'different'}}
        for field, value in mutations.items():
            with self.subTest(field=field):
                target.write_text(json.dumps({**original, field: value}), encoding='utf-8')
                result = subprocess.run(self.verify_command(target), capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertFalse(json.loads(result.stdout).get('complete', False))
        target.write_text(json.dumps(original), encoding='utf-8')
        result = subprocess.run(self.verify_command(target), capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_verify_missing_payload_field_is_rejected(self):
        self.write()
        target = self.root / '.nature-studio/references/REF-test/brief.json'
        record = ref.brief(self.root, self.path, target, self.media)
        record.pop('events')
        target.write_text(json.dumps(record), encoding='utf-8')
        result = subprocess.run(self.verify_command(target), capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_verify_recomputes_media_freshness_instead_of_trusting_saved_review(self):
        self.write()
        target = self.root / '.nature-studio/references/REF-test/brief.json'
        ref.brief(self.root, self.path, target, self.media)
        self.media.write_bytes(b'different fixture media')
        result = subprocess.run(self.verify_command(target), capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['freshness'], 'stale')

    def test_verify_cannot_promote_partial_by_editing_derived_flags(self):
        self.data['coverage']['audio'].update(status='unavailable', method='none',
                                              reviewed_ranges=[], evidence=[], limits=['fixture audio missing'])
        self.data['audio_cues'] = []
        self.write()
        target = self.root / '.nature-studio/references/REF-test/brief.json'
        record = ref.brief(self.root, self.path, target, self.media, partial_draft=True)
        record.update(draft=False, review={'complete': True, 'freshness': 'local_hash_matched'})
        target.write_text(json.dumps(record), encoding='utf-8')
        result = subprocess.run(self.verify_command(target), capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertFalse(json.loads(result.stdout)['complete'])

    def test_verify_accepts_formatting_changes_but_rejects_numeric_type_changes(self):
        self.write()
        target = self.root / '.nature-studio/references/REF-test/brief.json'
        record = ref.brief(self.root, self.path, target, self.media)
        target.write_text(json.dumps(record, indent=4, sort_keys=True), encoding='utf-8')
        result = subprocess.run(self.verify_command(target), capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        record['source']['has_audio'] = 1  # Python equality would incorrectly treat this as True.
        target.write_text(json.dumps(record), encoding='utf-8')
        result = subprocess.run(self.verify_command(target), capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)


if __name__=='__main__':
    unittest.main()
