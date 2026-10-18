"""Rebuild data/original_oddities.json for the Bugs & Oddities page from the restoration's faithfulness registers.

  python tools/sync-restoration-registers.py [--repo PATH_TO_darklands-restoration] [--previous data/original_oddities.json]

Reads docs/faithfulness/original_bugs.csv (the original bugs the game reproduces) and docs/faithfulness/dormant.csv (the
original's hidden branches) of a checkout of github.com/Arkana-Mechanika-Studios/darklands-restoration, and records its
commit. The curated hidden branches, the reported leads and the earlier development's findings are carried over from the
previous data file (schema v1 or v2) until they are reconciled with the registers.
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
        },
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
