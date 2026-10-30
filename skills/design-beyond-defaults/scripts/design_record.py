#!/usr/bin/env python3
"""Validate declared interface evidence and compare contracts; never prove behavior or authority."""
import argparse
import json
from pathlib import Path

STATUSES = {'pass', 'fail', 'not run', 'unsupported', 'needs review'}


def text(value):
    return isinstance(value, str) and bool(value.strip())


def validate(record, revision=None):
    errors = []
    if not isinstance(record, dict):
        return ['Record must be an object']
    if type(record.get('version')) is not int or record['version'] != 1:
        errors.append('version must be 1')
    for field in ('target', 'revision'):
        if not text(record.get(field)):
            errors.append(f'{field} must be nonempty text')
    if revision is not None and record.get('revision') != revision:
        errors.append('Record revision does not match current revision')
    if type(record.get('complete')) is not bool:
        errors.append('complete must be boolean')
    for field in ('contracts', 'changes', 'checks'):
        if not isinstance(record.get(field), list):
            errors.append(f'{field} must be a list')
    if errors:
        return errors
    contracts = {}
    for c in record['contracts']:
        if not isinstance(c, dict) or not text(c.get('id')) or not text(c.get('requirement')):
            errors.append('Each contract needs id and requirement')
            continue
        if c['id'] in contracts:
            errors.append(f'Duplicate contract: {c["id"]}')
        contracts[c['id']] = c['requirement']
    changes = set()
    for c in record['changes']:
        if not isinstance(c, dict) or any(not text(c.get(k)) for k in ('contract', 'reason', 'authorization')):
            errors.append('Each change needs contract, reason, and authorization declaration')
            continue
        if c['contract'] in changes:
            errors.append(f'Duplicate change: {c["contract"]}')
        changes.add(c['contract'])
    ids, covered = set(), set()
    all_pass = bool(record['checks'])
    for c in record['checks']:
        if not isinstance(c, dict):
            errors.append('Each check must be an object')
            all_pass = False
            continue
        required = ('id', 'contract', 'target', 'viewport', 'state', 'revision', 'method')
        if any(not text(c.get(k)) for k in required):
            errors.append('Each check needs id, contract, target, viewport, state, revision, and method')
            all_pass = False
            continue
        label = c['id']
        if label in ids:
            errors.append(f'Duplicate check: {label}')
        ids.add(label)
        if c['contract'] not in contracts:
            errors.append(f'{label}: unknown contract')
        status = c.get('status')
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f'{label}: unknown status')
        if c['revision'] != record['revision']:
            errors.append(f'{label}: stale revision')
        evidence = c.get('evidence')
        if not isinstance(evidence, list) or any(not isinstance(e, dict) or not text(e.get('location')) or not text(e.get('observation')) for e in evidence):
            errors.append(f'{label}: evidence must contain location and observation objects')
        if status in ('pass', 'fail') and not evidence:
            errors.append(f'{label}: pass/fail requires evidence')
        if status not in ('pass', 'fail') and not text(c.get('note')):
            errors.append(f'{label}: unexplained untested or unresolved check')
        if status == 'pass':
            covered.add(c['contract'])
        else:
            all_pass = False
    if record['complete'] and (not contracts or not all_pass or set(contracts) != covered):
        errors.append('Complete requires contracts and passing coverage for every contract with no unresolved checks')
    return errors


def compare(before, after):
    errors = [f'before: {x}' for x in validate(before)] + [f'after: {x}' for x in validate(after)]
    if errors:
        return {'errors': errors}
    if before['target'] != after['target']:
        return {'errors': ['Targets differ; compare records for the same artifact']}
    old = {c['id']: c['requirement'] for c in before['contracts']}
    new = {c['id']: c['requirement'] for c in after['contracts']}
    changed = sorted(k for k in old.keys() & new.keys() if old[k] != new[k])
    removed = sorted(old.keys() - new.keys())
    declared = {c['contract']: c for c in after['changes']}
    differences = set(changed + removed)
    unexplained = sorted(differences - declared.keys())
    unused = sorted(declared.keys() - differences)
    return {'removed': removed, 'changed': changed, 'added': sorted(new.keys() - old.keys()),
            'declared_changes': [declared[k] for k in sorted(differences & declared.keys())],
            'unexplained': unexplained, 'unused_declarations': unused,
            'errors': [f'Unexplained contract difference: {k}' for k in unexplained] + [f'Change declaration matches no difference: {k}' for k in unused],
            'limitation': 'Inventory comparison only; verify declared authority and execute required journeys independently'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('--target', required=True)
    init.add_argument('--revision', required=True)
    init.add_argument('--output', required=True, type=Path)
    val = sub.add_parser('validate')
    val.add_argument('record', type=Path)
    val.add_argument('--revision')
    diff = sub.add_parser('compare')
    diff.add_argument('before', type=Path)
    diff.add_argument('after', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'init':
            record = {'version': 1, 'target': args.target, 'revision': args.revision, 'complete': False, 'contracts': [], 'changes': [], 'checks': []}
            errors = validate(record)
            if errors:
                raise ValueError('; '.join(errors))
            with args.output.open('x') as handle:
                handle.write(json.dumps(record, indent=2) + '\n')
            result = {'created': str(args.output), 'complete': False, 'errors': []}
        elif args.command == 'validate':
            record = json.loads(args.record.read_text())
            result = {'errors': validate(record, args.revision),
                      'declared_complete': record.get('complete') if isinstance(record, dict) else None,
                      'limitation': 'Consistency of declared evidence only; not proof of behavior'}
        else:
            result = compare(json.loads(args.before.read_text()), json.loads(args.after.read_text()))
    except (OSError, ValueError, TypeError) as exc:
        result = {'errors': [str(exc)]}
    print(json.dumps(result, indent=2))
    return bool(result['errors'])


if __name__ == '__main__':
    raise SystemExit(main())
