#!/usr/bin/env python3
"""Generic Markdown -> styled HTML compiler for SAT workspace content.

Usage:
    python scripts/md_to_html.py [file_or_dir ...]
    (default: all *.md under SAT/ that have no same-name .html yet)

Renders: YAML frontmatter (as info card), headings, paragraphs, bold/italic/
inline code, unordered + ordered lists, horizontal rules, blockquotes, tables,
fenced code blocks, markdown links (rewrites *.md targets to *.html).
Zero dependencies. Output is self-contained (inline CSS, no external assets
except an optional Google font with system fallback).
"""
import os
import re
import sys
import html as htmllib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAT = os.path.join(BASE, 'SAT')

CSS = """
:root{--bg:#f8fafc;--surface:#fff;--text:#0f172a;--muted:#64748b;
--primary:#2b7fff;--border:#e2e8f0;--radius:12px;
--font:'Plus Jakarta Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
--mono:'JetBrains Mono',Consolas,monospace}
*{box-sizing:border-box}body{font-family:var(--font);background:var(--bg);
color:var(--text);line-height:1.7;margin:0;padding:2rem 1rem 4rem}
.wrap{max-width:900px;margin:0 auto}.crumbs{font-size:.82rem;color:var(--muted);
margin-bottom:1rem}.crumbs a{color:var(--primary);text-decoration:none}
h1{font-size:1.9rem;border-left:6px solid var(--primary);padding-left:1rem;
line-height:1.3}h2{font-size:1.35rem;margin-top:2rem;border-bottom:2px solid
var(--border);padding-bottom:.3rem}h3{font-size:1.1rem;margin-top:1.5rem}
.meta{background:var(--surface);border:1px solid var(--border);
border-radius:var(--radius);padding:.8rem 1.1rem;margin:1rem 0;font-size:.86rem;
color:var(--muted);display:flex;flex-wrap:wrap;gap:.4rem 1.2rem}
.meta b{color:var(--text)}p{margin:.7rem 0}
ul,ol{margin:.5rem 0 .9rem;padding-left:1.4rem}li{margin:.28rem 0}
hr{border:none;border-top:2px solid var(--border);margin:1.6rem 0}
blockquote{border-left:4px solid var(--primary);margin:1rem 0;padding:.4rem 1rem;
background:var(--surface);border-radius:0 var(--radius) var(--radius) 0}
code{font-family:var(--mono);font-size:.85em;background:#eef2ff;padding:.1rem .35rem;
border-radius:6px}pre{background:#0f172a;color:#e2e8f0;padding:1rem;
border-radius:var(--radius);overflow:auto}pre code{background:none;color:inherit;
padding:0}table{border-collapse:collapse;width:100%;margin:1rem 0;font-size:.9rem;
background:var(--surface)}th,td{border:1px solid var(--border);padding:.5rem .7rem;
text-align:left}th{background:#eff6ff}a{color:var(--primary)}
.answer{background:#f0fdf4;border-left:4px solid #16a34a;padding:.7rem 1rem;
border-radius:8px;margin:.7rem 0}.card{background:var(--surface);
border:1px solid var(--border);border-radius:var(--radius);padding:1.2rem 1.4rem;
margin:1rem 0;box-shadow:0 4px 6px -1px rgb(0 0 0/.05)}
"""

def esc(t):
    return htmllib.escape(t, quote=False)

def inline_md(t):
    """Inline formatting: code, bold, italic, links. Assumes input escaped."""
    t = re.sub(r'`([^`]+?)`', lambda m: '<code>%s</code>' % m.group(1), t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', t)

    def link_repl(m):
        label, href = m.group(1), m.group(2).strip()
        if href.lower().endswith('.md'):
            href = href[:-3] + '.html'
        return '<a href="%s">%s</a>' % (htmllib.escape(href, quote=True), label)

    t = re.sub(r'\[([^\]]+?)\]\(([^)]+?)\)', link_repl, t)
    return t

def render_body(lines):
    out = []
    i, n = 0, len(lines)
    in_ul = in_ol = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append('</ul>')
            in_ul = False
        if in_ol:
            out.append('</ol>')
            in_ol = False

    while i < n:
        line = lines[i]
        s = line.strip()
        if s.startswith('```'):
            close_lists()
            buf = []
            i += 1
            while i < n and not lines[i].strip().startswith('```'):
                buf.append(lines[i].rstrip('\n'))
                i += 1
            i += 1
            out.append('<pre><code>%s</code></pre>' % esc('\n'.join(buf)))
            continue
        if not s:
            close_lists()
            i += 1
            continue
        if re.match(r'^---+$', s) or re.match(r'^\*\*\*+$', s):
            close_lists()
            out.append('<hr>')
            i += 1
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', s)
        if m:
            close_lists()
            lvl = len(m.group(1))
            out.append('<h%d>%s</h%d>' % (lvl, inline_md(esc(m.group(2).strip())), lvl))
            i += 1
            continue
        if s.startswith('>'):
            close_lists()
            buf = []
            while i < n and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append('<blockquote>%s</blockquote>' % '<br>'.join(inline_md(esc(x)) for x in buf))
            continue
        # table: header row + delimiter row
        if '|' in s and i + 1 < n and re.match(r'^\s*\|?[\s:\-|]+\|?\s*$', lines[i + 1]):
            close_lists()
            headers = [c.strip() for c in s.strip('|').split('|')]
            i += 2
            rows = []
            while i < n and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            t = ['<table><tr>' + ''.join('<th>%s</th>' % inline_md(esc(c)) for c in headers) + '</tr>']
            for r in rows:
                t.append('<tr>' + ''.join('<td>%s</td>' % inline_md(esc(c)) for c in r) + '</tr>')
            t.append('</table>')
            out.append(''.join(t))
            continue
        m = re.match(r'^[-*+]\s+(.*)$', s)
        if m:
            if not in_ul:
                close_lists()
                out.append('<ul>')
                in_ul = True
            content = m.group(1)
            # Q&A answer lines get a highlight card
            if re.match(r'^\*\*Answer:\*\*', content):
                out.append('</ul>')
                in_ul = False
                out.append('<div class="answer">%s</div>' % inline_md(esc(content)))
            else:
                out.append('<li>%s</li>' % inline_md(esc(content)))
            i += 1
            continue
        m = re.match(r'^(\d+)[.)]\s+(.*)$', s)
        if m:
            if not in_ol:
                close_lists()
                out.append('<ol>')
                in_ol = True
            out.append('<li>%s</li>' % inline_md(esc(m.group(2))))
            i += 1
            continue
        close_lists()
        # standalone **Answer:** paragraph
        if s.startswith('**Answer:**'):
            out.append('<div class="answer">%s</div>' % inline_md(esc(s)))
        else:
            out.append('<p>%s</p>' % inline_md(esc(s)))
        i += 1
    close_lists()
    return '\n'.join(out)

def compile_file(md_path):
    with open(md_path, encoding='utf-8') as f:
        text = f.read()
    meta = {}
    body = text
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            for ln in parts[1].strip().splitlines():
                if ':' in ln:
                    k, v = ln.split(':', 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
            body = parts[2]
    title_m = re.search(r'^#\s+(.+)$', body, re.M)
    title = title_m.group(1).strip() if title_m else meta.get('topic', os.path.basename(md_path))
    title = re.sub(r'^[^\w\s"\']+', '', title).strip()
    # Drop the first H1 from the body — it is already shown in the title card
    body = re.sub(r'^#\s+.+$\n?', '', body, count=1, flags=re.M)
    meta_html = ''
    if meta:
        cells = ''.join('<span><b>%s:</b> %s</span>' % (esc(k), esc(v)) for k, v in meta.items())
        meta_html = '<div class="meta">%s</div>' % cells
    rel = os.path.relpath(os.path.dirname(os.path.abspath(md_path)), SAT).replace(os.sep, '/')
    depth = 0 if rel == '.' else rel.count('/') + 1
    up = '../' * depth
    crumbs = '<a href="%sindex.html">SAT Portal</a> &rsaquo; %s' % (up, esc(rel.replace('/', ' / ')) if rel != '.' else 'SAT')
    crumbs += ' &rsaquo; ' + esc(os.path.basename(md_path)[:-3] + '.html')
    html = ('<!DOCTYPE html><html lang="en"><!-- compiled by scripts/md_to_html.py --><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<title>%s | SATPrep</title><style>%s</style></head>'
            '<body><div class="wrap"><div class="crumbs">%s</div>'
            '<div class="card"><h1 style="border:none;padding:0;margin-top:0">%s</h1>%s</div>'
            '%s'
            '<p class="crumbs" style="margin-top:2rem"><a href="%sindex.html">&larr; SAT Portal</a></p>'
            '</div></body></html>' % (esc(title), CSS, crumbs, esc(title), meta_html, render_body(body.splitlines()), up))
    out_path = md_path[:-3] + '.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return out_path

def main(targets):
    force = False
    targets = [t for t in targets if not t.startswith('-')]
    if any(a == '--force' for a in sys.argv[1:]):
        force = True
    if not targets:
        targets = [SAT]
    made, skipped = 0, 0
    for t in targets:
        if os.path.isdir(t):
            files = []
            for root, _, fns in os.walk(t):
                for fn in sorted(fns):
                    if fn.lower().endswith('.md'):
                        files.append(os.path.join(root, fn))
        else:
            files = [t]
        for md in files:
            html_path = md[:-3] + '.html'
            if os.path.exists(html_path):
                if force and 'compiled by scripts/md_to_html.py' in open(html_path, encoding='utf-8').read():
                    pass  # regenerate below
                else:
                    skipped += 1
                    continue
            print('compiled', os.path.relpath(compile_file(md), BASE))
            made += 1
    print('done: %d compiled, %d skipped (html exists)' % (made, skipped))

if __name__ == '__main__':
    main(sys.argv[1:])
