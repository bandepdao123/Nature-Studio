from concurrent.futures import ThreadPoolExecutor
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('image_budget',Path(__file__).resolve().parents[1]/'image_budget.py')
budget = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(budget)


class ImageBudgetTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.rel = '04-Productions/project/ABC-00001'
        self.folder = self.root / self.rel
        self.folder.mkdir(parents=True)
        (self.folder/'feedback.md').write_text('Fixture: explicit approval for two additional calls.')

    def call(self, action, **kwargs):
        return budget.run(self.root,self.rel,action,**kwargs)

    def exhaust(self):
        self.call('init')
        for _ in range(5):
            self.call('reserve')

    def test_sixth_request_rejected_and_init_does_not_reset(self):
        self.exhaust()
        with self.assertRaises(ValueError):
            self.call('reserve')
        self.assertEqual(self.call('init')['used'],5)

    def test_errors_and_cancellations_still_consume_calls(self):
        self.call('init')
        for outcome in ['error','cancelled','unknown']:
            call=self.call('reserve',operation='edit')
            self.call('finish',call_id=call['call_id'],outcome=outcome)
        self.assertEqual(self.call('status')['remaining'],2)

    def test_grant_requires_evidence_and_keeps_counter(self):
        self.exhaust()
        with self.assertRaises(ValueError):
            self.call('grant',extra=2)
        result=self.call('grant',extra=2,approval_file='feedback.md')
        self.assertEqual(result['authorized'],7)
        self.assertEqual(self.call('reserve')['call_number'],6)

    def test_concurrent_calls_cannot_exceed_five(self):
        self.call('init')
        def attempt(_):
            try:
                return self.call('reserve')['call_id']
            except ValueError:
                return None
        with ThreadPoolExecutor(max_workers=6) as pool:
            ids=list(pool.map(attempt,range(10)))
        self.assertEqual(len({x for x in ids if x}),5)
        self.assertEqual(self.call('status')['used'],5)

    def test_new_cycle_requires_explicit_saved_request(self):
        first=self.call('init')
        with self.assertRaises(ValueError):
            self.call('new-cycle')
        second=self.call('new-cycle',approval_file='feedback.md')
        self.assertNotEqual(first['cycle_id'],second['cycle_id'])

    def test_path_escape_and_outside_runtime_rejected(self):
        for path in ['../outside','03-Projects/project','04-Productions/project','E:/outside']:
            with self.assertRaises(ValueError):
                budget.run(self.root,path,'init')

    def test_uninitialized_reserve_is_rejected(self):
        with self.assertRaises(ValueError):
            self.call('reserve')

    def test_no_early_or_negative_grant(self):
        self.call('init')
        with self.assertRaises(ValueError):
            self.call('grant',extra=2,approval_file='feedback.md')
        self.exhaust()
        with self.assertRaises(ValueError):
            self.call('grant',extra=-1,approval_file='feedback.md')

    def test_other_production_has_separate_budget(self):
        self.exhaust()
        other='04-Productions/project/ABC-00002'
        (self.root/other).mkdir()
        self.assertEqual(budget.run(self.root,other,'init')['remaining'],5)

    def test_foreign_call_cannot_be_finished(self):
        self.call('init')
        with self.assertRaises(ValueError):
            self.call('finish',call_id='not-a-call',outcome='success')


if __name__=='__main__':
    unittest.main()
