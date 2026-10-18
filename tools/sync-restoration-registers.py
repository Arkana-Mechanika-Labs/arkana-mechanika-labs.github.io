"""Rebuild data/original_oddities.json for the Bugs & Oddities page from the restoration's faithfulness registers.

  python tools/sync-restoration-registers.py [--repo PATH_TO_darklands-restoration] [--previous data/original_oddities.json]

Reads docs/faithfulness/original_bugs.csv (the original bugs the game reproduces) and docs/faithfulness/dormant.csv (the
original's hidden branches) of a checkout of github.com/Arkana-Mechanika-Studios/darklands-restoration, and records its
commit. The curated hidden branches, the reported leads and the earlier development's findings are carried over from the
previous data file (schema v1 or v2); tools/carried-over-verdicts.json records how each of them was re-checked against
the restoration (already in a register, confirmed and proposed for one, not a bug of 483.07, or still open), and the
script links the register entries and source lines it cites at the synced commit.
"""
import argparse
import collections
import csv
import datetime
import json
import os
import re
import subprocess

AREAS = {
    'cards': 'Cards and encounters',
    'rules': 'Rules',
    'battles': 'Battles',
    'events': 'Events',
    'screens/presentation': 'Screens',
    'travel': 'Travel',
    'host/audio': 'Sound',
}

VERDICTS = {
    'covered': 'In the registers',
    'confirmed-missing': 'Confirmed in the code, register entry proposed',
    'not-in-483.07': 'Not a bug of 483.07',
    'open': 'Still open',
}

REASONS = {
    'fixed-before-483.07': 'fixed before 483.07',
    'documentation': 'documentation',
    'platform': 'platform or host',
    'third-party-tool': 'third-party tool',
    'mechanic': 'intended rule',
    'code-refutes': 'the code does not do it',
    'retracted': 'retracted',
}


def title_of(note: str) -> str:
    """The first clause of a register note, as a short title."""
    first = re.split(r'(?<=[a-z0-9)])[.;:](\s|$)', note.strip(), maxsplit=1)[0].strip()
    first = re.sub(r'^\(-?\d+\)\s*', '', first)
    if len(first) > 110:
        first = first[:107].rsplit(' ', 1)[0] + '...'
    return first[:1].upper() + first[1:]


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=os.environ.get('DARKLANDS_RESTORATION', r'E:\Projects\darklands-clean'))
    ap.add_argument('--previous', default=os.path.join(here, 'data', 'original_oddities.json'))
    ap.add_argument('--out', default=os.path.join(here, 'data', 'original_oddities.json'))
    ap.add_argument('--verdicts', default=os.path.join(here, 'tools', 'carried-over-verdicts.json'))
    args = ap.parse_args()

    registers = os.path.join(args.repo, 'docs', 'faithfulness')
    commit = subprocess.run(['git', '-C', args.repo, 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    date = subprocess.run(['git', '-C', args.repo, 'log', '-1', '--format=%cs'], capture_output=True, text=True, check=True).stdout.strip()
    version = subprocess.run(['git', '-C', args.repo, 'describe', '--tags', '--abbrev=0'], capture_output=True, text=True).stdout.strip()

    with open(os.path.join(registers, 'original_bugs.csv'), encoding='utf-8') as f:
        bug_rows = list(csv.DictReader(f))
    with open(os.path.join(registers, 'dormant.csv'), encoding='utf-8') as f:
        dormant_rows = list(csv.DictReader(f))
    with open(args.previous, encoding='utf-8') as f:
        previous = json.load(f)

    reproduced = []
    for r in sorted(bug_rows, key=lambda r: (r['area'], r['type'], r['member'])):
        where = '.'.join(x for x in (r['type'], r['member']) if x)
        reproduced.append({
            'id': r['id'],
            'title': title_of(r['note']),
            'area': AREAS.get(r['area'], r['area']),
            'original': r['original'],
            'code': f"{r['file']}:{r['line']}" + (f" ({where})" if where else ''),
            'fix': '' if r['fix_flag'] in ('', 'none') else r['fix_flag'],
            'summary': r['note'],
        })

    dormant_counts = [{'area': AREAS.get(a, a), 'count': n}
                      for a, n in collections.Counter(r['area'] for r in dormant_rows).most_common()]

    old = previous
    curated = old.get('dormant_curated') or old.get('dormant') or []
    earlier = old.get('earlier_findings') or old.get('known') or []
    reported = old.get('reported_groups') or []

    # The re-check of the carried-over entries against this version (tools/carried-over-verdicts.json).
    with open(args.verdicts, encoding='utf-8') as f:
        verdicts = json.load(f)['entries']
    repo_url = 'https://github.com/Arkana-Mechanika-Studios/darklands-restoration'
    register_lines = {}
    for name in ('original_bugs', 'dormant', 'divergences', 'uncertain', 'unreachable', 'exclusions'):
        path = os.path.join(registers, name + '.csv')
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                for n, line in enumerate(f, 1):
                    register_lines.setdefault(line.split(',', 1)[0], (name, n))
    reproduced_ids = {b['id'] for b in reproduced}

    def register_link(rid):
        if rid in reproduced_ids:
            return {'id': rid, 'href': '#' + rid}
        if rid not in register_lines:
            raise SystemExit(f'verdict cites {rid}, which is in no register of {version or commit[:7]}')
        name, n = register_lines[rid]
        return {'id': rid, 'href': f'{repo_url}/blob/{commit}/docs/faithfulness/{name}.csv#L{n}'}

    def source_link(code):
        path, _, line = code.partition(':')
        if not os.path.exists(os.path.join(args.repo, path)):
            raise SystemExit(f'verdict cites {path}, which is not in {version or commit[:7]}')
        return {'code': code, 'href': f'{repo_url}/blob/{commit}/{path}' + (f'#L{line}' if line else '')}

    def checked(entry, key):
        entry = {k: v for k, v in entry.items() if k != 'check'}
        v = verdicts.get(key)
        if v is None:
            raise SystemExit(f'no verdict for carried-over entry {key!r}')
        if v['verdict'] not in VERDICTS:
            raise SystemExit(f'{key}: unknown verdict {v["verdict"]!r}')
        label = VERDICTS[v['verdict']]
        if v['verdict'] == 'not-in-483.07':
            label += ' (' + REASONS[v['reason_kind']] + ')'
        elif v['verdict'] == 'covered' and not v.get('register'):
            label = 'Reproduced, noted in the code'
        entry['check'] = {
            'verdict': v['verdict'],
            'label': label,
            'register': [register_link(r) for r in v.get('register', [])],
            'source': [source_link(s) for s in v.get('source', [])],
            'original': v.get('original', ''),
            'note': v['note'],
        }
        return entry

    reported = [dict(g, entries=[checked(e, e['id'] or e['report']) for e in g.get('entries', [])]) for g in reported]
    earlier = [checked(e, e['id']) for e in earlier]
    known = {e['id'] or e['report'] for g in reported for e in g['entries']} | {e['id'] for e in earlier}
    stale = sorted(set(verdicts) - known)
    if stale:
        raise SystemExit(f'verdicts for entries that are no longer carried over: {stale}')
    verdict_counts = collections.Counter(e['check']['verdict'] for e in earlier + [e for g in reported for e in g['entries']])

    data = {
        'schema': 'darklands.original-oddities.public.v2',
        'source_repository': 'https://github.com/Arkana-Mechanika-Studios/darklands-restoration',
        'source_commit': commit,
        'source_commit_date': date,
        'source_version': version,
        'generated': datetime.date.today().isoformat(),
        'counts': {
            'reproduced': len(reproduced),
            'reproduced_with_fix': sum(1 for b in reproduced if b['fix']),
            'dormant_total': len(dormant_rows),
            'dormant_curated': len(curated),
            'reported_leads': sum(len(g.get('entries', [])) for g in reported),
            'earlier_findings': len(earlier),
            'carried_over': {k: verdict_counts.get(k, 0) for k in VERDICTS},
        },
        'checked_against': version or commit[:7],
        'reproduced': reproduced,
        'dormant_counts': dormant_counts,
        'dormant_curated': curated,
        'reported_groups': reported,
        'earlier_findings': earlier,
        'earlier_source': {k: old[k] for k in ('source_commit', 'source_commit_date') if k in old and old.get('schema', '').endswith('v1')}
                          or old.get('earlier_source', {}),
    }
    with open(args.out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f"wrote {args.out}: {data['counts']} from {version or commit[:7]} ({date})")


if __name__ == '__main__':
    main()
