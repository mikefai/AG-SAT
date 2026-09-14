"""Strip IELTS Task-1 blocks from the 4 SAT guide/mock pages.

Removes (HTML): teacher-drawer Lesson Flow + CCQ blocks (keeps Printing).
Removes (JS): insertSentenceStarter fn, Writing Arena block, Speaking Arena block.
Dead code has no live callers (verified). Idempotent: re-run is a no-op.
"""
import io
import os
import re

BASE = 'C:/Users/micha/OneDrive/Desktop/AG TEACHING/SAT'
FILES = ['Question_Banks/sat_desmos_calculator_mastery_guide_and_hacks.html',
         'Question_Banks/sat_digital_rw_distractor_trap_radar_and_cheat_sheet.html',
         'Practice_Modules/sat_digital_full_practice_test_01_math_module.html',
         'Practice_Modules/sat_digital_full_practice_test_01_rw_module.html']


def drop_divs(html, fingerprints):
    """Remove top-level <div class="teacher-block"> whose text matches fingerprints."""
    out, i, removed = [], 0, 0
    while True:
        start = html.find('<div class="teacher-block">', i)
        if start < 0:
            out.append(html[i:])
            break
        # balance divs from start
        depth, j = 0, start
        while True:
            m = re.search(r'</?div\b[^>]*>', html[j:])
            assert m, 'unbalanced div'
            tag = m.group(0)
            depth += -1 if tag.startswith('</') else 1
            j += m.end()
            if depth == 0:
                break
        block = html[start:j]
        if any(fp in block for fp in fingerprints):
            removed += 1
            out.append(html[i:start])
        else:
            out.append(html[i:j])
        i = j
    return ''.join(out), removed


def drop_range(lines, start_pat, end_pat):
    """Drop lines from start_pat (inclusive) to end_pat (exclusive). Returns new lines + count."""
    s = next((k for k, ln in enumerate(lines) if re.search(start_pat, ln)), None)
    if s is None:
        return lines, 0
    e = next((k for k, ln in enumerate(lines) if k > s and re.search(end_pat, ln)), len(lines))
    return lines[:s] + lines[e:], e - s


for f in FILES:
    p = os.path.join(BASE, f)
    c = io.open(p, encoding='utf-8').read()
    c, n_blocks = drop_divs(c, ['Suggested Lesson Flow', 'Concept Checking'])
    lines = c.split('\n')
    lines, n1 = drop_range(lines, r'function insertSentenceStarter\(type\)', r'function updateAudioSpeed\(')
    lines, n2 = drop_range(lines, r'// Writing Arena Logic', r'// Speaking Arena Logic')
    lines, n3 = drop_range(lines, r'// Speaking Arena Logic', r'// Mastery Checklist Logic')
    io.open(p, 'w', encoding='utf-8').write('\n'.join(lines))
    print('%s: teacher-blocks=%d js-lines=%d' % (os.path.basename(f)[:45], n_blocks, n1 + n2 + n3))
