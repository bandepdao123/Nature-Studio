import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import media_review as media
import production_state


class ReviewTests(unittest.TestCase):
    def test_ratio_rounding_and_export_are_distinct(self):
        result = media.aspect(941, 1672)
        self.assertTrue(result['input_ratio_pass'])
        self.assertFalse(result['exact_export'])
        self.assertAlmostEqual(result['relative_error'], .0005316321105795)
        self.assertFalse(media.aspect(940, 1600)['input_ratio_pass'])
        self.assertTrue(media.aspect(1080, 1920)['exact_export'])

    def test_duration_and_unknown(self):
        self.assertEqual(media.duration_check(8, 10, 24)['status'], 'fail')
        self.assertEqual(media.duration_check(10.005, 10, 24)['status'], 'pass')
        self.assertEqual(media.duration_check(None, 10)['status'], 'not_checked')

    def test_binaries_do_not_prove_perception(self):
        with patch.object(shutil, 'which', return_value='installed'):
            result = media.capabilities()
        self.assertEqual(result['continuous_visual_understanding'], 'not_verified')
        self.assertEqual(result['environment_audio_understanding'], 'not_verified')

    def test_audio_classification(self):
        self.assertEqual(media.audio_status({'input_i': None, 'input_tp': None}, -16, -1), 'silent_or_unmeasurable')
        self.assertEqual(media.audio_status({'input_i': -16, 'input_tp': -.5}, -16, -1), 'peak_exceeded')
        self.assertEqual(media.audio_status({'input_i': -38, 'input_tp': -20}, -16, -1), 'level_outside_target')
        self.assertEqual(media.audio_status({'input_i': -16, 'input_tp': -2}, -16, -1), 'within_target')

    def test_provisional_does_not_pass_qa(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            (base/'text.md').write_text('fixture')
            (base/'render.mp4').write_text('fixture only')
            (base/'approval.md').write_text('Synthetic test: provisional acceptance')
            state = dict(schema=1, current_text={'path':'text.md','sha256':media.sha(base/'text.md')},
                         selected_render={'path':'render.mp4','sha256':media.sha(base/'render.mp4')},
                         approval='provisional', approval_evidence='approval.md',
                         qa=dict(visual='pass',motion='not_checked',anatomy='fail',audio='fail',format='pass'))
            result = production_state.validate(state,base)
            self.assertTrue(result['valid'])
            self.assertFalse(result['qa_pass'])
            self.assertEqual(result['approval'],'provisional')
            state['current_text']['sha256'] = 'bad'
            self.assertFalse(production_state.validate(state,base)['valid'])
            state['current_text']['path']='../outside.md'
            self.assertFalse(production_state.validate(state,base)['valid'])


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'Requires FFmpeg and FFprobe')
class SignalIntegrationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()

    def fixture(self, name, signal, duration=8, gain=None):
        path = self.base/name
        command=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-n',
                 '-f','lavfi','-i',f'color=c=black:s=90x160:r=24:d={duration}',
                 '-f','lavfi','-i',signal,'-t',str(duration),'-c:v','mpeg4','-c:a','aac']
        if gain:
            command += ['-af',gain]
        subprocess.run(command+[str(path)],check=True,capture_output=True)
        return path

    def test_short_video_quiet_mix_and_normalization(self):
        source=self.fixture('quiet.mp4','sine=frequency=1000:sample_rate=48000', gain='volume=0.04')
        before=media.inspect(source,10,-16,-1)
        self.assertEqual(before['duration']['status'],'fail')
        self.assertLess(before['audio']['whole']['input_i'],-35)
        self.assertEqual(set(before['audio']['windows']),{'head','middle','tail'})
        auth=self.base/'authorization.md'
        auth.write_text('Synthetic fixture processing authorized by test, not human production approval.')
        listening=self.base/'listening.md'
        listening.write_text('Known generated sine fixture only; no claim of human listening.')
        output=self.base/'normalized-v002.mp4'
        result=media.normalize(source,output,-16,-1,auth,listening)
        self.assertEqual(media.sha(source),before['sha256'])
        self.assertLess(abs(result['after']['audio']['whole']['input_i']+16),1)
        self.assertLessEqual(result['after']['audio']['whole']['input_tp'],-.8)
        self.assertEqual(result['post_processing_listening'],'not_checked')
        self.assertTrue(Path(str(output)+'.review.json').is_file())
        with self.assertRaises(ValueError):
            media.normalize(source,output,-16,-1,auth,listening)

    def test_silent_no_audio_and_codec_tail(self):
        silent=self.fixture('silent.mp4','anullsrc=r=48000:cl=mono',10)
        report=media.inspect(silent,10,-16,-1)
        self.assertEqual(report['duration']['status'],'pass')
        self.assertEqual(report['audio']['status'],'silent_or_unmeasurable')
        no_audio=self.base/'no-audio.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(silent),
                        '-an','-c:v','copy',str(no_audio)],check=True,capture_output=True)
        self.assertEqual(media.inspect(no_audio,10)['audio']['status'],'no_audio')
        # Container/audio duration may exceed video; only stream duration can pass.
        fake={'streams':[{'codec_type':'video','duration':'8','avg_frame_rate':'24/1','width':90,'height':160}],
              'format':{'duration':'10.005'}}
        with patch.object(media,'probe',return_value=fake):
            self.assertEqual(media.inspect(no_audio,10)['duration']['status'],'fail')


if __name__ == '__main__':
    unittest.main()
