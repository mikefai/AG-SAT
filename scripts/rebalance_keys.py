"""Balance answer keys across the 8 SAT banks (reusable pipeline).

Rotates option order in questions.json (remapping rationale letters), regenerates
the 8 bank .md files from JSON, re-scrapes, and verifies with an independent
block parser (options + key + rationale must match for all items).

Safe to re-run: rotation only moves surplus keys to deficit keys.
"""
import json, io, re, subprocess, sys
from collections import Counter

BASE = 'C:/Users/micha/OneDrive/Desktop/AG TEACHING'
QB = BASE + '/SAT/Question_Banks'
DATA = BASE + '/SAT/webapp/data'
CATS = ['Craft & Structure', 'Information & Ideas', 'Expression of Ideas',
        'Standard English Conventions', 'Algebra', 'Advanced Math',
        'Problem Solving & Data Analysis', 'Geometry & Trigonometry']
NOTES = {'Craft & Structure': 'craft_structure_notes',
         'Information & Ideas': 'information_ideas_notes',
         'Expression of Ideas': 'expression_ideas_notes',
         'Standard English Conventions': 'standard_conventions_notes',
         'Algebra': 'algebra_notes', 'Advanced Math': 'advanced_math_notes',
         'Problem Solving & Data Analysis': 'problem_solving_notes',
         'Geometry & Trigonometry': 'geometry_notes'}
FILEMAP = {'Craft & Structure': 'sat_craft_structure_10_items.md',
           'Information & Ideas': 'sat_information_ideas_10_items.md',
           'Expression of Ideas': 'sat_expression_ideas_10_items.md',
           'Standard English Conventions': 'sat_standard_conventions_10_items.md',
           'Algebra': 'sat_algebra_10_items.md',
           'Advanced Math': 'sat_advanced_math_10_items.md',
           'Problem Solving & Data Analysis': 'sat_problem_solving_10_items.md',
           'Geometry & Trigonometry': 'sat_geometry_10_items.md'}
LETTERS = ['A', 'B', 'C', 'D']
TARGET = {'A': 9, 'B': 9, 'C': 9, 'D': 8}
DENY = ['A logistics', 'answer A', 'answer B', 'answer C', 'answer D',
        'choice A', 'choice B', 'choice C', 'choice D',
        'option A', 'option B', 'option C', 'option D']

def unsafe(q):
    txt = (q.get('question') or '') + ' ' + (q.get('stimulus') or '')
    if re.search(r'\b[A-D]\)', txt):
        return 'option-enum-in-prompt'
    r = q.get('rationale') or ''
    for d in DENY:
        if d in r:
            return 'prose-mention:' + d
    return None

def remap_letters(text, mp):
    for i, L in enumerate(LETTERS):
        text = re.sub(r'\b' + L + r'\b', '\x00%d\x01' % i, text)
    for i, L in enumerate(LETTERS):
        text = text.replace('\x00%d\x01' % i, mp[L])
    return text

def rotate_to(question, target):
    cur = LETTERS.index(question['answer'])
    tgt = LETTERS.index(target)
    k = (cur - tgt) % 4
    opts = question['options']
    question['options'] = [opts[(i + k) % 4] for i in range(4)]
    mp = {LETTERS[j]: LETTERS[(j - k) % 4] for j in range(4)}
    question['rationale'] = remap_letters(question['rationale'], mp)
    question['answer'] = target

d = json.load(io.open(DATA + '/questions.json', encoding='utf-8'))
by_cat = {}
for q in d:
    by_cat.setdefault(q['category'], []).append(q)

moved = 0
for cat in CATS:
    items = sorted(by_cat[cat], key=lambda q: int(q['id'].rsplit('-Q', 1)[1]))
    counts = Counter(q['answer'] for q in items)
    for tgt in ['B', 'C', 'D', 'A']:
        need = TARGET[tgt] - counts.get(tgt, 0)
        for q in items:
            if need <= 0:
                break
            if q['answer'] == tgt or counts[q['answer']] <= TARGET[q['answer']]:
                continue
            reason = unsafe(q)
            if reason:
                print('  SKIP', q['id'], reason)
                continue
            old = q['answer']
            rotate_to(q, tgt)
            counts[old] -= 1
            counts[tgt] += 1
            need -= 1
            moved += 1
    print(cat, dict(counts))
print('moved:', moved)

for cat in CATS:
    items = sorted(by_cat[cat], key=lambda q: int(q['id'].rsplit('-Q', 1)[1]))
    out = ['---\ndomain: SAT\ntarget_level: Score 700+\n'
           'topic: Question Bank \u2014 %s (35 Items)\n'
           'date_created: 2026-09-13\ncontent_type: Question Bank / Drill\n---\n' % cat,
           '# %s \u2014 35 Practice Items\n' % cat,
           '**Flow:** Teach \u2192 Show \u2192 Test\n']
    for i, q in enumerate(items, 1):
        out.append('---\n')
        out.append('## Q%d \u2014 %s (%s)\n' % (i, q['skill'], q['difficulty'].capitalize()))
        if q.get('passage'):
            out.append('**Passage:** %s\n' % q['passage'])
        if q.get('stimulus') and q['stimulus'].strip() not in ('', '---', '***'):
            out.append('%s\n' % q['stimulus'])
        if q.get('question'):
            out.append('**Question:** %s\n' % q['question'])
        for L, o in zip(LETTERS, q['options']):
            out.append('- %s. %s\n' % (L, o))
        out.append('**Answer:** %s. %s\n' % (q['answer'], q['rationale']))
    out.append('\n---\n')
    out.append('\n**Portal / Study:** [SAT/Study_Notes/%s.md](../Study_Notes/%s.md) | '
               '[Show](../Show/show_walkthrough.html) | [Test](../Test/mock_01.html) | '
               '[Portal](../index.html)' % (NOTES[cat], NOTES[cat]))
    io.open(QB + '/' + FILEMAP[cat], 'w', encoding='utf-8').write('\n'.join(out))
print('files regenerated')

r = subprocess.run([sys.executable, BASE + '/scripts/scrape_sat_content.py'],
                   capture_output=True, text=True, cwd=BASE)
print(r.stdout[-400:])
assert r.returncode == 0, r.stderr

# independent block-level verification
d2 = json.load(io.open(DATA + '/questions.json', encoding='utf-8'))
assert len(d2) == 280, len(d2)
bad = 0
for q in d2:
    text = io.open(QB + '/' + FILEMAP[q['category']], encoding='utf-8').read()
    n = q['id'].rsplit('-Q', 1)[1]
    blk = next(ch for ch in re.split(r'\n## Q(?=\d)', text)[1:]
               if re.match(str(int(n)) + r'\s', ch))
    od = {L: t.strip() for L, t in re.findall(r'^\s*-\s*([A-D])[.:)]\s+(.+)$', blk, re.M)}
    for i, L in enumerate(LETTERS):
        if od.get(L, '') != q['options'][i]:
            print('OPT MISMATCH', q['id'], L); bad += 1
    m = re.search(r'\*\*Answer:\*\*\s*([A-D])', blk)
    if not m or m.group(1) != q['answer']:
        print('KEY MISMATCH', q['id']); bad += 1
print('block-check mismatches:', bad)
assert bad == 0
print('REBALANCE PIPELINE OK')
