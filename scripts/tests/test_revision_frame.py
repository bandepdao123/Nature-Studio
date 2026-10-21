"""Revision binding and frame freshness on temporary productions; no model calls."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import chayvideo_output as out


class RevisionFrameTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.base = self.root / '04-Productions/one/UF-0001'
        self.base.mkdir(parents=True)
        self.docs = {'INPUTS.md': 'Real fixture source bindings.',
                     'settings.md': 'Prompt only; not generated.',
                     'review.md': 'Syntax only; no image QA.'}
        self.state = dict(subjects='One fish and one lure.', environment='Clear lake.',
                          composition='Fixed camera facing bottom.', initial_state='Fish away from lure.')
        self.full = dict(idea='Fixture story', first_frame_prompt='Fish approaches a lure.',
                         video_prompt='Fish misses the lure.', caption='Watch. #Fish #Lake #Fishing',
                         frame_state=self.state, files=self.docs)
        self.a = out.save(self.root, 'one', 'UF-0001', self.full).relative_to(self.base).as_posix()
        for rel, text in [('03-Projects/one/PROJECT.md', 'ID: stable-one\nSlug: one\n'),
                          ('00-Standards/first-frame.md', 'Frame criteria.'),
                          ('00-Standards/quality-review.md', 'Review policy.')]:
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding='utf-8')

    def resolved(self, attempt=None):
        return out.resolve(self.root, 'one', 'UF-0001', attempt or self.a)

    def revise(self, base, mode='revision', **fields):
        data = dict(base_attempt=base, base_sha256=self.resolved(base)['attempt_sha256'],
                    files=self.docs, **fields)
        return out.save(self.root, 'one', 'UF-0001', data, mode).relative_to(self.base).as_posix()

    def record(self):
        r = self.resolved()
        image = self.base / 'image.png'
        image.write_bytes(b'Fixture bytes, not an actual QA image')
        review = self.base / 'image-review.md'
        review.write_text('Fixture QA record; not a real image verdict.')
        refs = ['00-Standards/first-frame.md', '00-Standards/quality-review.md',
                '03-Projects/one/PROJECT.md']
        record = dict(schema=2, production_id='UF-0001', project_id='stable-one',
                      attempt_id=self.a, source_attempt=self.a, source_attempt_sha256=r['attempt_sha256'],
                      qa_status='qa_pass', image_path='image.png', sha256=out.sha256(image),
                      review_path='image-review.md', review_sha256=out.sha256(review),
                      frame_inputs=r['frame_inputs'], frame_inputs_sha256=r['frame_inputs_sha256'],
                      qa_sources={rel: out.sha256(self.root / rel) for rel in refs}, user_approved=False)
        self.write_record(record)
        return record

    def write_record(self, record):
        (self.base / 'FIRST-FRAME.json').write_text(json.dumps(record), encoding='utf-8')

    def check(self, attempt=None):
        return out.check_frame(self.root, 'one', 'UF-0001', attempt or self.a)

    def test_chain_keeps_field_sources_without_selecting_latest(self):
        b = self.revise(self.a, video_prompt='Changed motion.', frame_state=self.state)
        c = self.revise(b, mode='caption', caption='Again. #Fish #Lake #Fishing')
        self.revise(self.a, idea='Unselected branch.', frame_state=self.state)
        result = self.resolved(c)
        self.assertEqual(result['output']['video_prompt'], 'Changed motion.')
        self.assertEqual(result['sources']['first_frame_prompt']['attempt'], self.a)
        self.assertEqual(result['sources']['video_prompt']['attempt'], b)
        self.assertEqual(result['sources']['caption']['attempt'], c)
        self.assertNotIn('selected', result)
        self.assertNotIn('user_approved', result)

    def test_revision_save_requires_pinned_explicit_base(self):
        data = dict(caption='Watch. #Fish #Lake #Fishing', files=self.docs)
        with self.assertRaises(ValueError):
            out.save(self.root, 'one', 'UF-0001', data, 'caption')
        data.update(base_attempt=self.a, base_sha256='0' * 64)
        with self.assertRaises(ValueError):
            out.save(self.root, 'one', 'UF-0001', data, 'caption')

    def test_resolve_checks_reserved_identity_without_allocating(self):
        modern = self.base.parent / 'ABC-00001'
        modern.mkdir()
        (modern / 'A01').mkdir()
        (modern / 'A01/OUTPUT.json').write_bytes((self.base / self.a / 'OUTPUT.json').read_bytes())
        identity = modern / 'IDENTITY.json'
        identity.write_text(json.dumps(dict(video_id='ABC-00001', project_id='stable-one')))
        self.assertEqual(out.resolve(self.root, 'one', 'ABC-00001', 'A01')['output']['idea'], self.full['idea'])
        identity.write_text(json.dumps(dict(video_id='ABC-00001', project_id='other')))
        with self.assertRaisesRegex(ValueError, 'Project identity'):
            out.resolve(self.root, 'one', 'ABC-00001', 'A01')
        self.assertFalse((self.root / '.nature-studio').exists())

    def test_save_rejects_wrong_project_before_any_attempt_or_stage(self):
        for mode, code in [('new', 'ABC-00001'), ('reference', 'DEF-00001')]:
            with self.subTest(mode=mode):
                folder = self.base.parent / code
                folder.mkdir()
                identity = folder / 'IDENTITY.json'
                identity.write_text(json.dumps(dict(video_id=code, project_id='wrong-project')))
                before = identity.read_bytes()
                with self.assertRaisesRegex(ValueError, 'Project identity'):
                    out.save(self.root, 'one', code, self.full, mode)
                self.assertEqual(list(folder.iterdir()), [identity])
                self.assertEqual(identity.read_bytes(), before)

    def test_save_and_resolve_agree_for_owned_modern_and_legacy(self):
        modern = self.base.parent / 'ABC-00001'
        modern.mkdir()
        (modern / 'IDENTITY.json').write_text(json.dumps(dict(video_id='ABC-00001', project_id='stable-one')))
        for code, folder in [('ABC-00001', modern), ('UF-0001', self.base)]:
            saved = out.save(self.root, 'one', code, self.full, 'reference')
            result = out.resolve(self.root, 'one', code, saved.relative_to(folder).as_posix())
            self.assertEqual(result['output']['idea'], self.full['idea'])

    def test_changed_ancestor_is_not_silently_reused(self):
        b = self.revise(self.a, mode='caption', caption='Again. #Fish #Lake #Fishing')
        file = self.base / self.a / 'OUTPUT.json'
        file.write_bytes(file.read_bytes() + b' ')
        with self.assertRaisesRegex(ValueError, 'Base changed'):
            self.resolved(b)

    def test_legacy_full_is_readable_partial_requires_manual_binding(self):
        legacy = self.base / 'A20'
        legacy.mkdir()
        fields = {k: self.full[k] for k in out.FIELDS}
        file = legacy / 'OUTPUT.json'
        file.write_text(json.dumps(fields))
        self.assertEqual(self.resolved('A20')['frame_state_status'], 'unverified')
        file.write_text(json.dumps({'caption': self.full['caption']}))
        with self.assertRaisesRegex(ValueError, 'no explicit base'):
            self.resolved('A20')

    def test_incomplete_cycle_missing_and_escape_rejected(self):
        for ref in ('latest', '../UF-0002/A01', 'A999', '/A01'):
            with self.assertRaises(ValueError):
                self.resolved(ref)
        marker = self.base / self.a / 'SAVE-INCOMPLETE.txt'
        marker.write_text('Interrupted save')
        with self.assertRaisesRegex(ValueError, 'Incomplete'):
            self.resolved()
        marker.unlink()
        file = self.base / self.a / 'OUTPUT.json'
        data = json.loads(file.read_text())
        data.update(base_attempt=self.a, base_sha256='0' * 64)
        file.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            self.resolved()

    def test_nested_attempt_layout(self):
        (self.base / 'attempts').mkdir()
        b = self.revise(self.a, mode='caption', caption='Again. #Fish #Lake #Fishing')
        self.assertEqual(b, 'attempts/A01')
        self.assertEqual(self.resolved(b)['sources']['idea']['attempt'], self.a)

    def test_caption_cannot_smuggle_story_changes(self):
        for change in ({'idea': 'Another story'}, {'frame_state': self.state}):
            data = dict(caption=self.full['caption'], **change)
            self.assertTrue(out.validate(data, 'caption'))

    def test_caption_keeps_frame_binding_and_commands_are_read_only(self):
        self.record()
        b = self.revise(self.a, mode='caption', caption='Again. #Fish #Lake #Fishing')
        before = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        result = self.check(b)
        self.assertEqual(result['status'], 'matched')
        after = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertFalse((self.base / '.image-qa.sqlite3').exists())

    def test_motion_revision_with_confirmed_same_opening_stays_matched(self):
        self.record()
        b = self.revise(self.a, video_prompt='Different action after t=0.', frame_state=self.state)
        self.assertEqual(self.check(b)['status'], 'matched')

    def test_image_attempt_and_content_source_are_distinct(self):
        record = self.record()
        (self.base / 'A08').mkdir()
        record['attempt_id'] = 'A08'
        self.write_record(record)
        self.assertEqual(self.check()['status'], 'matched')
        record['attempt_id'] = 'A09'
        self.write_record(record)
        self.assertEqual(self.check()['status'], 'invalid')

    def test_missing_review_binding_and_nonpass_qa_never_match(self):
        record = self.record()
        record.pop('qa_sources')
        self.write_record(record)
        self.assertEqual(self.check()['status'], 'unverified')
        record = self.record()
        record['qa_status'] = 'qa_incomplete'
        self.write_record(record)
        self.assertEqual(self.check()['status'], 'needs_review')

    def test_semantic_revision_without_state_is_unverified(self):
        self.record()
        b = self.revise(self.a, idea='Story changed; opening not assessed.')
        self.assertEqual(self.check(b)['status'], 'unverified')

    def test_changed_subjects_or_prompt_requests_review_without_deleting_pass(self):
        self.record()
        saved = (self.base / 'FIRST-FRAME.json').read_bytes()
        for fields in [dict(frame_state={**self.state, 'subjects': 'Two fish and no lure.'}, idea='New setup.'),
                       dict(first_frame_prompt='Changed camera description.', frame_state=self.state)]:
            b = self.revise(self.a, **fields)
            self.assertEqual(self.check(b)['status'], 'needs_review')
        self.assertEqual((self.base / 'FIRST-FRAME.json').read_bytes(), saved)

    def test_changed_image_or_review_hash_is_invalid(self):
        for name in ('image.png', 'image-review.md'):
            self.record()
            (self.base / name).write_bytes(b'changed')
            self.assertEqual(self.check()['status'], 'invalid')

    def test_legacy_handoff_is_unverified_not_upgraded(self):
        record = self.record()
        for key in ('schema', 'frame_inputs', 'frame_inputs_sha256', 'review_sha256'):
            record.pop(key)
        self.write_record(record)
        before = (self.base / 'FIRST-FRAME.json').read_bytes()
        self.assertEqual(self.check()['status'], 'unverified')
        self.assertEqual((self.base / 'FIRST-FRAME.json').read_bytes(), before)

    def test_source_criteria_changed_require_review(self):
        self.record()
        (self.root / '00-Standards/first-frame.md').write_text('Revised criteria.')
        self.assertEqual(self.check()['status'], 'needs_review')

    def test_qa_snapshot_tampering_wrong_owner_and_path_escape(self):
        original = self.record()
        for patch in [dict(project_id='other'), dict(image_path='../other/image.png'),
                      dict(frame_inputs_sha256='0' * 64),
                      dict(source_attempt_sha256='0' * 64)]:
            self.write_record({**original, **patch})
            self.assertEqual(self.check()['status'], 'invalid')
        altered = copy.deepcopy(original)
        altered['frame_inputs']['frame_state']['subjects'] = 'Different subject.'
        altered['frame_inputs_sha256'] = out.snapshot_hash(altered['frame_inputs'])
        self.write_record(altered)
        self.assertEqual(self.check()['status'], 'invalid')

    def test_cli_resolution_and_review_exit_codes(self):
        script = str(Path(out.__file__).resolve())
        args = [sys.executable, script, '--root', str(self.root)]
        scope = ['--project', 'one', '--production', 'UF-0001']
        self.record()
        for command in ('resolve', 'check-frame'):
            result = subprocess.run(args + [command, self.a] + scope, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIsInstance(json.loads(result.stdout), dict)
            if command == 'resolve':
                self.assertNotIn('frame_inputs', json.loads(result.stdout))
        result = subprocess.run(args + ['resolve', self.a, '--frame-inputs'] + scope, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('frame_inputs', json.loads(result.stdout))
        b = self.revise(self.a, first_frame_prompt='New opening.', frame_state=self.state)
        result = subprocess.run(args + ['check-frame', b] + scope, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
