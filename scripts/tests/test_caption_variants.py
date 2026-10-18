"""Caption structure, revisions and frame compatibility; no language/performance claims."""
import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import chayvideo_output as out
import test_revision_frame as frames


def sample():
    return json.loads((Path(out.ROOT)/'00-Standards/templates/caption-variants.json').read_text(encoding='utf-8'))


class CaptionChecks(unittest.TestCase):
    def test_all_three_validate_with_existing_project_rules(self):
        self.assertEqual(out.validate(sample(),'caption',underwater=True),[])

    def test_hook_one_to_nine_words_and_contractions(self):
        for text in ('Nope.',"I don't think that's going to work out here."):
            data=sample();data['caption_variants']['variants']['standard']['hook_text']=text
            self.assertFalse(out.validate(data,'caption',underwater=True))
        for text in ('...', 'One two three four five six seven eight nine ten', 'one-two-three-four-five-six-seven-eight-nine-ten'):
            data=sample();data['caption_variants']['variants']['standard']['hook_text']=text
            self.assertTrue(out.validate(data,'caption',underwater=True))
        self.assertEqual(out.hook_words('Don’t miss that last-second turn.'),['Don’t','miss','that','last','second','turn'])

    def test_every_variant_hashtag_rules_checked(self):
        for style in out.CAPTION_STYLES:
            for tags in ('#Muskie #Fish','#Muskie #muskie #Fish','#Muskie #Fish #UnderWater','#Muskie #Fish #AIGenerated'):
                data=sample();item=data['caption_variants']['variants'][style];item['caption']='Watch. '+tags
                if style=='standard':data['caption']=item['caption']
                self.assertTrue(out.validate(data,'caption',underwater=True),(style,tags))

    def test_hook_hashtag_ai_or_newline_rejected(self):
        for field,text in [('hook_text','Watch #Muskie'),('hook_text','AI made this.'),('hook_text','Watch\nclosely'),('caption_vi','Dòng một\\nDòng hai')]:
            data=sample();data['caption_variants']['variants']['humor'][field]=text
            self.assertTrue(out.validate(data,'caption',underwater=True))

    def test_schema_types_and_empty_translations_report_errors(self):
        for replacement in (None,[],dict(schema=True,variants={}),dict(schema=1,variants={})):
            data=sample();data['caption_variants']=replacement;self.assertTrue(out.validate(data,'caption',underwater=True))
        for replacement in (None,[],{},'missing'):
            data=sample();data['caption_variant']=replacement;self.assertTrue(out.validate(data,'caption',underwater=True))
        for field in out.CAPTION_VARIANT_FIELDS:
            data=sample();data['caption_variants']['variants']['humor'][field]='';self.assertTrue(out.validate(data,'caption',underwater=True))

    def test_selected_caption_must_match_and_not_be_user_approval(self):
        data=sample();data['caption_variant']='humor';self.assertTrue(out.validate(data,'caption',underwater=True))
        data['caption']=data['caption_variants']['variants']['humor']['caption'];self.assertFalse(out.validate(data,'caption',underwater=True))
        self.assertNotIn('user_approved',data)

    def test_duplicate_wording_rejected_but_shared_hashtags_allowed(self):
        data=sample();self.assertFalse(out.validate(data,'caption',underwater=True))
        data['caption_variants']['variants']['humor']['caption']=data['caption'];self.assertTrue(out.validate(data,'caption',underwater=True))
        data=sample();data['caption_variants']['variants']['humor']['hook_text']=data['caption_variants']['variants']['standard']['hook_text'];self.assertTrue(out.validate(data,'caption',underwater=True))
        data=sample();data['caption_variants']['variants']['standard']['hook_text']='Passed on that lure!';self.assertTrue(out.validate(data,'caption',underwater=True))

    def test_project_specific_hashtags_not_forced_on_other_projects(self):
        data=sample();data['caption_variants']['variants']['humor']['caption']='Different audience. #Underwater'
        self.assertFalse(out.validate(data,'caption',underwater=False))

    def test_variant_metadata_requires_caption_and_bundle(self):
        data=sample();data.pop('caption');self.assertTrue(out.validate(data,'revision'))
        self.assertTrue(out.validate(dict(caption='Legacy.',caption_variant='standard'),'caption'))

    def test_render_order_exactly_caption_translation_hook_translation(self):
        rendered=out.render_caption_variants(sample()['caption_variants'])
        self.assertLess(rendered.index('## Chuẩn'),rendered.index('## Hài hước'))
        self.assertLess(rendered.index('## Hài hước'),rendered.index('## Tò mò'))
        for section in rendered.split('## ')[1:]:
            fields=['**Caption:**','**Lược dịch caption:**','**Hook text:**','**Lược dịch hook:**']
            self.assertEqual(sorted(section.index(x) for x in fields),[section.index(x) for x in fields])


class CaptionRevisionChecks(unittest.TestCase):
    def setUp(self):
        self.f=frames.RevisionFrameTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
    def add_bundle(self):return self.f.revise(self.f.a,mode='caption',**sample())

    def test_save_resolve_and_written_artifact(self):
        ref=self.add_bundle();result=self.f.resolved(ref)
        self.assertEqual(result['caption_variants'],sample()['caption_variants']);self.assertEqual(result['caption_variant'],'standard')
        self.assertEqual(result['output']['caption'],sample()['caption'])
        text=(self.f.base/ref/'caption-variants.md').read_text(encoding='utf-8');self.assertIn('**Lược dịch hook:**',text)
        self.assertEqual(out.frame_snapshot(result),out.frame_snapshot(self.f.resolved()))

    def test_targeted_revision_merges_without_losing_other_two(self):
        ref=self.add_bundle();item=copy.deepcopy(sample()['caption_variants']['variants']['humor'])
        item.update(caption='Not on the menu. #Muskie #MuskyFishing #FreshwaterFishing',caption_vi='Không phải món nó thích.')
        patch=dict(caption=item['caption'],caption_variant='humor',caption_variants=dict(schema=1,variants={'humor':item}))
        revised=self.f.revise(ref,mode='caption',**patch);resolved=self.f.resolved(revised)
        self.assertEqual(resolved['caption_variants']['variants']['standard'],sample()['caption_variants']['variants']['standard'])
        self.assertEqual(resolved['caption_variants']['variants']['humor'],item)
        stored=json.loads((self.f.base/revised/'OUTPUT.json').read_text(encoding='utf-8'))
        self.assertEqual(set(stored['caption_variants']['variants']),set(out.CAPTION_STYLES))
        self.assertNotIn('frame_state',stored);self.assertNotIn('asset_selection',stored)

    def test_caption_variants_do_not_invalidate_qa_image(self):
        self.f.record();ref=self.add_bundle();self.assertEqual(self.f.check(ref)['status'],'matched')

    def test_legacy_single_caption_does_not_certify_old_variants(self):
        ref=self.add_bundle();revised=self.f.revise(ref,mode='caption',caption='Legacy replacement.')
        self.assertIsNone(self.f.resolved(revised)['caption_variants']);self.assertEqual(self.f.resolved(revised)['caption_variants_status'],'unverified')
        self.assertIsNone(self.f.resolved()['caption_variants'])

    def test_story_change_requires_reviewed_bundle_again(self):
        ref=self.add_bundle();revised=self.f.revise(ref,video_prompt='Different outcome.',frame_state=self.f.state)
        self.assertIsNone(self.f.resolved(revised)['caption_variants'])

    def test_bad_patch_no_attempt_created_or_silent_collision(self):
        ref=self.add_bundle();before={p.name for p in self.f.base.iterdir()}
        item=copy.deepcopy(sample()['caption_variants']['variants']['humor']);item['caption']=sample()['caption']
        with self.assertRaises(ValueError):self.f.revise(ref,mode='caption',caption=item['caption'],caption_variant='humor',caption_variants=dict(schema=1,variants={'humor':item}))
        self.assertEqual(before,{p.name for p in self.f.base.iterdir()})

    def test_edit_another_style_keeps_existing_selection_with_full_snapshot(self):
        data=sample();data['caption_variant']='humor';data['caption']=data['caption_variants']['variants']['humor']['caption']
        ref=self.f.revise(self.f.a,mode='caption',**data)
        updated=copy.deepcopy(data)
        updated['caption_variants']['variants']['curiosity']['hook_text']='Watch it close in.'
        revised=self.f.revise(ref,mode='caption',**updated);resolved=self.f.resolved(revised)
        self.assertEqual(resolved['caption_variant'],'humor');self.assertEqual(resolved['output']['caption'],data['caption'])


if __name__=='__main__':unittest.main()
