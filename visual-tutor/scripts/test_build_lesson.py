"""Behavioral checks for lesson validation and safe standalone generation."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from build_lesson import LessonError, validate


def fixture():
    chapter = {
        'id': 'first', 'level': 'Foundations', 'title': 'A concept', 'why': 'A concrete problem',
        'explanation': ['A causal explanation'],
        'example': {'label': 'Input', 'language': 'text', 'code': 'one\ntwo',
                    'evidence': {'kind': 'model', 'note': 'Illustration'}},
        'diagram': {'label': 'A mechanism', 'note': 'Simplified model',
                    'nodes': [{'id': 'a', 'label': 'A', 'detail': 'Input', 'x': 20, 'y': 50},
                              {'id': 'b', 'label': 'B', 'detail': 'Result', 'x': 80, 'y': 50}],
                    'edges': [{'id': 'ab', 'from': 'a', 'to': 'b'}]},
        'steps': [{'title': 'Input', 'text': 'Inspect the input', 'active': ['a'], 'lines': [1]},
                  {'title': 'Result', 'text': 'Explain the result', 'active': ['b'], 'edges': ['ab'], 'lines': [2]}],
        'exercise': {'prompt': 'Change the input', 'hint': 'Use the rule', 'solution': 'Explain the consequence'},
        'sources': ['primary']}
    chapters = []
    for index, level in enumerate(('Foundations', 'Intermediate', 'Advanced')):
        item = copy.deepcopy(chapter)
        item.update(id=f'concept-{index}', level=level)
        chapters.append(item)
    return {'version': 1, 'title': 'Test lesson', 'subtitle': 'A learning path', 'outcome': 'Apply the rule',
            'research_date': '2026-10-23', 'scope': {'prerequisites': ['None'], 'includes': ['The rule'], 'boundaries': ['Other rules']},
            'sources': [{'id': 'primary', 'title': 'Primary source', 'url': 'https://example.org/docs'}],
            'chapters': chapters}


class LessonTests(unittest.TestCase):
    def test_valid_lesson(self):
        self.assertEqual(len(validate(fixture())['chapters']), 3)

    def test_broken_cross_references_and_lines(self):
        mutations = [
            lambda c: c['steps'][0].update(active=['missing']),
            lambda c: c['steps'][0].update(edges=['missing']),
            lambda c: c['steps'][0].update(lines=[3]),
            lambda c: c['steps'][0].update(values={'missing': 'value'}),
            lambda c: c.update(sources=['missing']),
            lambda c: c['diagram']['edges'][0].update(to='missing')]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                data = fixture()
                mutate(data['chapters'][0])
                with self.assertRaises(LessonError):
                    validate(data)

    def test_execution_claim_requires_evidence(self):
        data = fixture()
        data['chapters'][0]['example']['evidence']['kind'] = 'executed'
        with self.assertRaises(LessonError):
            validate(data)

    def test_variant_uses_its_own_line_count(self):
        data = fixture()
        chapter = data['chapters'][0]
        variant = {'name': 'Shorter example', 'example': copy.deepcopy(chapter['example']), 'steps': copy.deepcopy(chapter['steps'])}
        variant['example']['code'] = 'one'
        chapter['variants'] = [variant]
        with self.assertRaises(LessonError):
            validate(data)

    def test_resource_paths_stay_local(self):
        for path in ('../secret', '/etc/passwd', 'javascript:alert(1)', 'https://example.org/file', 'x\\y'):
            with self.subTest(path=path):
                data = fixture()
                data['resources'] = [{'label': 'Source', 'path': path}]
                with self.assertRaises(LessonError):
                    validate(data)

    def test_script_closing_text_is_data_and_round_trips(self):
        data = fixture()
        payload = '</script><script>throw new Error("not data")</script> & < >'
        data['chapters'][0]['example']['code'] = payload+'\nsecond line'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root/'lesson.json', root/'index.html'
            source.write_text(json.dumps(data))
            run = subprocess.run([sys.executable, str(Path(__file__).with_name('build_lesson.py')), str(source), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            html = output.read_text()
            embedded = html.split('<script type="application/json" id="lesson-data">', 1)[1].split('</script>', 1)[0]
            self.assertNotIn('<script>', embedded)
            self.assertEqual(json.loads(embedded)['chapters'][0]['example']['code'], payload+'\nsecond line')

    def test_missing_resource_is_reported(self):
        data = fixture()
        data['resources'] = [{'label': 'Missing source', 'path': 'missing.py'}]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root/'lesson.json'
            source.write_text(json.dumps(data))
            run = subprocess.run([sys.executable, str(Path(__file__).with_name('build_lesson.py')), str(source), '--output', str(root/'index.html')], capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)
            self.assertIn('missing resource', run.stderr)
            self.assertFalse((root/'index.html').exists())


if __name__ == '__main__':
    unittest.main()
