import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT/'skills/design-beyond-defaults'


def module(name):
    spec = importlib.util.spec_from_file_location(name, SKILL/'scripts'/f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


record = module('design_record')
materials = module('check_materials')


def valid():
    return {'version': 1, 'target': 'settings', 'revision': 'abc', 'complete': True,
            'contracts': [{'id': 'save', 'requirement': 'Timezone persists after reload'}], 'changes': [],
            'checks': [{'id': 'save-reload', 'contract': 'save', 'target': 'settings', 'viewport': '390x844',
                        'state': 'changed timezone', 'revision': 'abc', 'status': 'pass', 'method': 'browser save and reload',
                        'evidence': [{'location': 'journey.log', 'observation': 'Timezone remains selected after reload'}]}]}


class DesignRecordTests(unittest.TestCase):
    def test_valid_record_and_current_revision(self):
        self.assertEqual(record.validate(valid(), 'abc'), [])
        self.assertTrue(record.validate(valid(), 'def'))

    def test_stale_check_rejected_even_if_record_updated(self):
        data = valid(); data['revision'] = 'def'
        self.assertTrue(record.validate(data))

    def test_success_needs_evidence(self):
        data = valid(); data['checks'][0]['evidence'] = []
        self.assertTrue(record.validate(data))

    def test_screenshot_path_without_observation_is_insufficient(self):
        data = valid(); data['checks'][0]['evidence'] = ['screen.png']
        self.assertTrue(record.validate(data))

    def test_budget_exhaustion_cannot_complete(self):
        for status in ('not run', 'unsupported', 'needs review', 'fail'):
            data = valid(); data['checks'][0].update(status=status, note='Budget exhausted')
            self.assertTrue(record.validate(data))
            data['complete'] = False
            self.assertEqual(record.validate(data), [])

    def test_unexplained_missing_capability_rejected(self):
        data = valid(); data['complete'] = False
        data['checks'][0].update(status='unsupported', evidence=[])
        self.assertTrue(record.validate(data))

    def test_every_contract_needs_coverage(self):
        data = valid(); data['contracts'].append({'id': 'invalid', 'requirement': 'Invalid input is rejected'})
        self.assertTrue(record.validate(data))

    def test_duplicate_and_unknown_ids(self):
        data = valid(); data['checks'].append(copy.deepcopy(data['checks'][0]))
        self.assertTrue(record.validate(data))
        data = valid(); data['checks'][0]['contract'] = 'invented'
        self.assertTrue(record.validate(data))
        data = valid(); data['contracts'].append(copy.deepcopy(data['contracts'][0]))
        self.assertTrue(record.validate(data))

    def test_malformed_values_fail_without_crashing(self):
        for data in (None, [], {}, {'version': 1}, {'version': True}, valid() | {'checks': 'x'}):
            self.assertTrue(record.validate(data))
        for field, value in [('status', []), ('evidence', 1), ('id', {}), ('revision', False)]:
            data = valid(); data['checks'][0][field] = value
            self.assertTrue(record.validate(data))

    def test_inventory_removal_requires_declaration(self):
        before = valid(); after = valid()
        after.update(complete=False, contracts=[], checks=[])
        self.assertEqual(record.compare(before, after)['unexplained'], ['save'])
        after['changes'] = [{'contract': 'save', 'reason': 'User removed persistence from scope', 'authorization': 'Explicit request in task'}]
        result = record.compare(before, after)
        self.assertEqual(result['errors'], [])
        self.assertIn('execute required journeys', result['limitation'])

    def test_changed_requirement_not_hidden_by_stable_id(self):
        before = valid(); after = valid(); after['contracts'][0]['requirement'] = 'Display a saved message'
        self.assertEqual(record.compare(before, after)['changed'], ['save'])
        self.assertTrue(record.compare(before, after)['errors'])

    def test_unknown_authorization_cannot_mask_omission(self):
        before = valid(); after = valid(); after.update(complete=False, contracts=[], checks=[])
        after['changes'] = [{'contract': 'other', 'reason': 'Not relevant', 'authorization': 'Claimed'}]
        self.assertTrue(record.compare(before, after)['errors'])

    def test_compare_targets_must_match(self):
        data = valid(); data['target'] = 'billing'
        self.assertTrue(record.compare(valid(), data)['errors'])

    def test_empty_record_not_complete(self):
        data = valid(); data.update(contracts=[], checks=[])
        self.assertTrue(record.validate(data))

    def test_cli_initializes_without_overwriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'record.json'
            args = [sys.executable, str(SKILL/'scripts/design_record.py'), 'init', '--target', 'settings', '--revision', 'abc', '--output', str(target)]
            self.assertEqual(subprocess.run(args, capture_output=True).returncode, 0)
            original = target.read_bytes()
            self.assertFalse(json.loads(original)['complete'])
            self.assertNotEqual(subprocess.run(args, capture_output=True).returncode, 0)
            self.assertEqual(target.read_bytes(), original)

    def test_cli_bad_json_is_structured_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'bad.json'; path.write_text('{broken')
            result = subprocess.run([sys.executable, str(SKILL/'scripts/design_record.py'), 'validate', str(path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(json.loads(result.stdout)['errors'])


class MaterialTests(unittest.TestCase):
    def test_declared_catalog_pairs(self):
        self.assertEqual(materials.validate(SKILL), [])
        catalog = json.loads((SKILL/'assets/materials.json').read_text())
        self.assertEqual(len(catalog['materials']), 12)

    def test_known_contrast_extremes(self):
        self.assertAlmostEqual(materials.contrast('#000000', '#ffffff'), 21)
        self.assertEqual(materials.contrast('#112233', '#112233'), 1)

    def test_bad_palette_rejected(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'skill'; shutil.copytree(SKILL, root)
            path = root/'assets/materials.json'; data = json.loads(path.read_text())
            data['materials'][0]['tokens']['muted'] = data['materials'][0]['tokens']['ground']
            path.write_text(json.dumps(data))
            self.assertTrue(materials.validate(root))

    def test_profile_and_specimen_cannot_silently_drift(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'skill'; shutil.copytree(SKILL, root)
            p = root/'assets/material-specimens.html'
            p.write_text(p.read_text().replace('--ground:#f5f6f7', '--ground:#eeeeee'))
            self.assertTrue(materials.validate(root))
            p = root/'references/materials/quiet-utility.md'
            p.write_text(p.read_text().replace('#182128', '#202020'))
            self.assertTrue(materials.validate(root))

    def test_catalog_path_escape_rejected(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'skill'; shutil.copytree(SKILL, root)
            path = root/'assets/materials.json'; data = json.loads(path.read_text())
            data['materials'][0]['profile'] = '../outside.md'; (root.parent/'outside.md').write_text('outside')
            path.write_text(json.dumps(data))
            self.assertTrue(materials.validate(root))


if __name__ == '__main__':
    unittest.main()
