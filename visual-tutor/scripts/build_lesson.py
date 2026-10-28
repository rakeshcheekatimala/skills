#!/usr/bin/env python3
"""Validate lesson data and embed it in the offline visual-tutor shell."""
import argparse
import json
import math
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlparse


class LessonError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise LessonError(message)


def text(value, where):
    require(isinstance(value, str) and bool(value.strip()), f'{where}: expected nonempty text')


def strings(value, where, nonempty=True):
    require(isinstance(value, list) and (bool(value) or not nonempty), f'{where}: expected a list')
    for i, item in enumerate(value):
        text(item, f'{where}[{i}]')


def local_path(value, where):
    text(value, where)
    p = PurePosixPath(value)
    require(not p.is_absolute() and '..' not in p.parts and '\\' not in value
            and ':' not in value and not value.startswith(('#', '?')),
            f'{where}: use a relative path within the lesson directory')


def example(value, where):
    require(isinstance(value, dict), f'{where}: expected an object')
    for key in ('label', 'language', 'code'):
        text(value.get(key), f'{where}.{key}')
    if 'file' in value:
        local_path(value['file'], f'{where}.file')
    evidence = value.get('evidence', {})
    require(evidence.get('kind') in ('executed', 'model', 'sourced'), f'{where}.evidence.kind: executed, model, or sourced')
    text(evidence.get('note'), f'{where}.evidence.note')
    if evidence['kind'] == 'executed':
        for key in ('command', 'output'):
            text(evidence.get(key), f'{where}.evidence.{key}')


def validate(data):
    require(isinstance(data, dict), 'lesson: expected an object')
    require(data.get('version') == 1, 'version: expected 1')
    for key in ('title', 'subtitle', 'outcome', 'research_date'):
        text(data.get(key), key)
    require(re.fullmatch(r'\d{4}-\d{2}-\d{2}', data['research_date']), 'research_date: use YYYY-MM-DD')
    scope = data.get('scope', {})
    for key in ('prerequisites', 'includes', 'boundaries'):
        strings(scope.get(key), f'scope.{key}')
    sources = data.get('sources')
    require(isinstance(sources, list), 'sources: expected a list, possibly empty if research was unavailable')
    source_ids = set()
    for src in sources:
        for key in ('id', 'title', 'url'):
            text(src.get(key), f'sources.{key}')
        require(src['id'] not in source_ids, f'duplicate source: {src["id"]}')
        url = urlparse(src['url'])
        require(url.scheme in ('http', 'https') and bool(url.netloc), 'sources.url: expected an HTTP(S) URL')
        source_ids.add(src['id'])
    chapters = data.get('chapters')
    require(isinstance(chapters, list) and bool(chapters), 'chapters: expected a nonempty list')
    chapter_ids = set()
    levels = set()
    for chapter in chapters:
        where = f'chapter {chapter.get("id", "?")}'
        for key in ('id', 'title', 'why'):
            text(chapter.get(key), f'{where}.{key}')
        require(chapter['id'] not in chapter_ids, f'{where}: duplicate id')
        require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', chapter['id']), f'{where}.id: use lowercase words separated by hyphens')
        chapter_ids.add(chapter['id'])
        require(chapter.get('level') in ('Foundations', 'Intermediate', 'Advanced'), f'{where}.level: invalid level')
        levels.add(chapter['level'])
        strings(chapter.get('explanation'), f'{where}.explanation')
        example(chapter.get('example'), f'{where}.example')
        diagram = chapter.get('diagram', {})
        for key in ('label', 'note'):
            text(diagram.get(key), f'{where}.diagram.{key}')
        nodes = diagram.get('nodes', [])
        require(isinstance(nodes, list) and bool(nodes), f'{where}: diagram needs nodes')
        ids = set()
        for node in nodes:
            for key in ('id', 'label', 'detail'):
                text(node.get(key), f'{where}.node.{key}')
            require(node['id'] not in ids, f'{where}: duplicate node id')
            ids.add(node['id'])
            for key in ('x', 'y'):
                val = node.get(key)
                require(isinstance(val, (float, int)) and not isinstance(val, bool) and math.isfinite(val) and 15 <= val <= 85,
                        f'{where}.node.{key}: use a finite position between 15 and 85 percent')
        edges = diagram.get('edges', [])
        require(isinstance(edges, list), f'{where}.edges: expected list')
        edge_ids = set()
        for edge in edges:
            text(edge.get('id'), f'{where}.edge.id')
            require(edge['id'] not in edge_ids, f'{where}: duplicate edge id')
            require(edge.get('from') in ids and edge.get('to') in ids, f'{where}: edge references missing node')
            require(edge['from'] != edge['to'], f'{where}: self edges require a custom renderer')
            edge_ids.add(edge['id'])
        variants = chapter.get('variants', [])
        require(isinstance(variants, list), f'{where}.variants: expected a list')
        for variant in variants:
            text(variant.get('name'), f'{where}.variant.name')
            if 'example' in variant:
                example(variant['example'], f'{where}.variant.example')
        for mode in [chapter] + variants:
            steps = mode.get('steps', [])
            require(isinstance(steps, list) and len(steps) >= 2, f'{where}: each scenario needs at least two causal steps')
            selected = mode.get('example', chapter['example'])
            line_count = len(selected['code'].split('\n'))
            for step in steps:
                for key in ('title', 'text'):
                    text(step.get(key), f'{where}.step.{key}')
                require(isinstance(step.get('active'), list) and bool(step['active']) and set(step['active']) <= ids,
                        f'{where}: active nodes must exist')
                require(isinstance(step.get('edges', []), list) and set(step.get('edges', [])) <= edge_ids,
                        f'{where}: active edges must exist')
                require(isinstance(step.get('lines', []), list) and all(type(n) is int and 1 <= n <= line_count for n in step.get('lines', [])),
                        f'{where}: code line outside example')
                require(isinstance(step.get('values', {}), dict) and set(step.get('values', {})) <= ids,
                        f'{where}: value references missing node')
                for value in step.get('values', {}).values():
                    text(value, f'{where}.step.value')
        for item in chapter.get('deep_dive', []):
            text(item.get('title'), f'{where}.deep_dive.title')
            text(item.get('text'), f'{where}.deep_dive.text')
        for key in ('prompt', 'hint', 'solution'):
            text(chapter.get('exercise', {}).get(key), f'{where}.exercise.{key}')
        refs = chapter.get('sources', [])
        require(isinstance(refs, list) and set(refs) <= source_ids, f'{where}: source id not found')
    require(levels == {'Foundations', 'Intermediate', 'Advanced'}, 'lesson must include all three levels')
    for resource in data.get('resources', []):
        text(resource.get('label'), 'resource.label')
        local_path(resource.get('path'), 'resource.path')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lesson', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--check', action='store_true', help='Validate data and local example/resource paths without writing HTML')
    args = parser.parse_args()
    try:
        data = validate(json.loads(args.lesson.read_text(encoding='utf-8')))
        paths = [r['path'] for r in data.get('resources', [])]
        for chapter in data['chapters']:
            for item in [chapter] + chapter.get('variants', []):
                if item.get('example', {}).get('file'):
                    paths.append(item['example']['file'])
        for path in paths:
            require((args.output.parent / path).is_file(), f'missing resource beside output: {path}')
        if args.check:
            print(f'Valid lesson: {len(data["chapters"])} concepts, {len(data["sources"])} sources, {len(set(paths))} local resources')
            return
        shell = (Path(__file__).resolve().parent.parent / 'assets/lesson-shell.html').read_text(encoding='utf-8')
        require(shell.count('__LESSON_JSON__') == 1, 'shell must contain exactly one data placeholder')
        encoded = json.dumps(data, ensure_ascii=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(shell.replace('__LESSON_JSON__', encoded), encoding='utf-8')
        print(f'Built {args.output} ({len(data["chapters"])} concepts)')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Lesson error: {exc}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
