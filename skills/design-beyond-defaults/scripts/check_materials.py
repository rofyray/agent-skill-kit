#!/usr/bin/env python3
"""Validate the optional material catalog and declared contrast pairs, not visual quality."""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path


class Specimens(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.materials = {}
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'section' and 'material' in attrs.get('class', '').split():
            self.materials[attrs.get('id')] = dict(
                item.split(':', 1) for item in attrs.get('style', '').split(';') if ':' in item
            )


def contrast(a, b):
    def luminance(value):
        channels = [int(value[i:i + 2], 16)/255 for i in (1, 3, 5)]
        linear = [c/12.92 if c <= 0.04045 else ((c + 0.055)/1.055)**2.4 for c in channels]
        return sum(c*w for c, w in zip(linear, (0.2126, 0.7152, 0.0722)))
    x, y = sorted((luminance(a), luminance(b)))
    return (y + 0.05)/(x + 0.05)


def validate(root):
    errors = []
    data = json.loads((root/'assets/materials.json').read_text())
    if not isinstance(data, dict) or type(data.get('version')) is not int or data['version'] != 1 or not isinstance(data.get('materials'), list):
        return ['Expected version 1 material catalog']
    ids = set()
    specimen = (root/'assets/material-specimens.html').read_text()
    specimens = Specimens(specimen).materials
    roles = {'ground', 'surface', 'ink', 'muted', 'accent', 'on_accent', 'focus'}
    for m in data['materials']:
        if not isinstance(m, dict):
            errors.append('Material must be an object')
            continue
        slug = m.get('id', '')
        if not isinstance(slug, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or slug in ids:
            errors.append('Invalid or duplicate material id')
            continue
        ids.add(slug)
        for key in ('name', 'font', 'radius', 'profile'):
            if not isinstance(m.get(key), str) or not m[key].strip():
                errors.append(f'{slug}: missing {key}')
        profile = m.get('profile')
        profile_text = ''
        if isinstance(profile, str):
            path = (root/profile).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                errors.append(f'{slug}: profile must be an existing bundled file')
            else:
                profile_text = path.read_text()
        jobs = m.get('jobs')
        if not isinstance(jobs, list) or len(jobs) < 2 or any(not isinstance(x, str) or not x.strip() for x in jobs) or len(set(jobs)) != len(jobs):
            errors.append(f'{slug}: two distinct job examples required')
        if f'id="{slug}"' not in specimen:
            errors.append(f'{slug}: missing specimen')
        tokens = m.get('tokens')
        if not isinstance(tokens, dict) or set(tokens) != roles or any(not isinstance(v, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', v) for v in tokens.values()):
            errors.append(f'{slug}: expected seven semantic hex color tokens')
            continue
        for role, value in tokens.items():
            if f'| {role} | `{value}` |' not in profile_text:
                errors.append(f'{slug}: profile token differs for {role}')
            if specimens.get(slug, {}).get(f'--{role}') != value:
                errors.append(f'{slug}: specimen token differs for {role}')
        pairs = [(fg, bg, 4.5) for fg in ('ink', 'muted') for bg in ('ground', 'surface')]
        pairs += [('on_accent', 'accent', 4.5), ('focus', 'ground', 3), ('focus', 'surface', 3)]
        for fg, bg, minimum in pairs:
            ratio = contrast(tokens[fg], tokens[bg])
            if ratio < minimum:
                errors.append(f'{slug}: {fg} on {bg} = {ratio:.2f}:1, needs {minimum}:1')
    if not ids:
        errors.append('Catalog is empty')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors = validate(args.root)
    except (OSError, ValueError, TypeError) as exc:
        errors = [str(exc)]
    print(json.dumps({'errors': errors, 'scope': 'catalog structure and declared contrast pairs only'}, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
