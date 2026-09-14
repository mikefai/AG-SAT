#!/usr/bin/env python3
"""Build SAT-first interactive drill pages from set .md sources.

Parses: frontmatter, Module Overview, Question Items (MCQ + SPR),
Answer-Key table (key / rule / tier), Solutions sections.
Emits self-contained HTML: dual-pane drill, Easy/Medium/Expert tiers,
timer, flags, instant feedback + solutions, scoring, localStorage,
KaTeX math, print CSS. No IELTS content of any kind.

Usage: python scripts/build_sat_modules.py   (rebuilds all 11 set pages)
"""
import html as htmllib
import io
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAT = os.path.join(BASE, 'SAT')

SETS = [
    'Reading_Writing/Craft_and_Structure/sat_craft_and_structure_cross_text_connections_set_02.md',
    'Reading_Writing/Craft_and_Structure/sat_craft_and_structure_words_in_context_set_01.md',
    'Reading_Writing/Expression_of_Ideas/sat_expression_of_ideas_transitions_rhetorical_synthesis_set_01.md',
    'Reading_Writing/Information_and_Ideas/sat_information_and_ideas_evidence_inference_set_01.md',
    'Reading_Writing/Information_and_Ideas/sat_information_and_ideas_scientific_tables_and_graphs_set_02.md',
    'Reading_Writing/Standard_English_Conventions/sat_standard_english_conventions_boundaries_and_modifiers_set_01.md',
    'Reading_Writing/Standard_English_Conventions/sat_standard_english_conventions_verbs_pronouns_parallelism_set_02.md',
    'Math/Advanced_Math/sat_math_advanced_math_polynomials_and_nonlinear_systems_set_02.md',
    'Math/Algebra/sat_math_algebra_and_advanced_functions_set_01.md',
    'Math/Geometry_and_Trigonometry/sat_math_geometry_trigonometry_and_data_set_01.md',
    'Math/Problem_Solving_and_Data_Analysis/sat_math_problem_solving_data_statistics_set_01.md',
]

TIER_BUCKET = {'easy': 'easy', 'easy-medium': 'easy', 'medium': 'medium',
               'medium-hard': 'medium', 'hard': 'expert'}
LETTERS = ['A', 'B', 'C', 'D']


def esc(t):
    return htmllib.escape(t, quote=False)


def inline_fmt(t):
    t = esc(t)
    t = re.sub(r'`([^`\n]+?)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\w)\*([^*\n]+?)\*(?!\w)', r'<em>\1</em>', t)
    return t


def md_lines_to_html(lines):
    """Indent-aware mini renderer for solution bullets."""
    out, stack = [], []

    def close_all():
        while stack:
            out.append('</ul>')
            stack.pop()

    for ln in lines:
        if not ln.strip() or ln.strip() == '---':
            continue
        m = re.match(r'^(\s*)(?:-\s+|\d+[.)]\s+)(.*)$', ln)
        if m:
            depth = len(m.group(1)) // 2
            while len(stack) > depth + 1:
                out.append('</ul>')
                stack.pop()
            while len(stack) < depth + 1:
                out.append('<ul class="sol-list">')
                stack.append(1)
            out.append('<li>%s</li>' % inline_fmt(m.group(2).strip()))
        else:
            close_all()
            out.append('<p>%s</p>' % inline_fmt(ln.strip()))
    close_all()
    return '\n'.join(out)


def parse_frontmatter(text):
    meta, body = {}, text
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            for ln in parts[1].strip().splitlines():
                if ':' in ln:
                    k, v = ln.split(':', 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
            body = parts[2]
    return meta, body


def parse_overview(body):
    info = {}
    m = re.search(r'##\s+[^\n]*Module Overview[^\n]*\n(.*?)(?=\n##\s|\n---\s*\n##|\Z)', body, re.S)
    if not m:
        return info
    for ln in m.group(1).splitlines():
        mm = re.match(r'\s*-\s*\*\*(.+?)\*\*\s*:\s*(.+)$', ln.strip())
        if mm:
            info[mm.group(1).strip()] = mm.group(2).strip()
    return info


def split_questions(body):
    """Return list of (num, header_skill, block_lines) for Question Items."""
    start = re.search(r'##\s+[^\n]*(?:Question Items|Math Problems)[^\n]*\n', body)
    if not start:
        return []
    region = body[start.end():]
    end = re.search(r'\n##\s+(?!###)', region)
    if end:
        region = region[:end.start()]
    chunks = re.split(r'(?m)^###\s+Question\s+(\d+)([^\n]*)$', region)
    out = []
    # chunks[0] is preamble; then groups of (num, rest-of-line, block)
    for i in range(1, len(chunks), 3):
        if i + 1 >= len(chunks):
            break
        rest = chunks[i + 1].strip()
        skill = re.sub(r'^[:(\[]\s*', '', rest)
        skill = re.sub(r'\s*[)\]]$', '', skill).strip()
        out.append((int(chunks[i]), skill, chunks[i + 2].splitlines()))
    return out


def parse_options(block_lines):
    opts = {}
    for ln in block_lines:
        m = re.match(r'^\s*-\s*\*\*([A-D])\)\*\*\s*(.*)$', ln.strip())
        if m:
            opts[m.group(1)] = m.group(2).strip()
    return opts


def parse_key_table(body):
    """Map qnum -> (key_raw, rule, tier_raw)."""
    m = re.search(r'\|[^\n]*Question[^\n]*\|[^\n]*(?:Correct|Key)[^\n]*\|\n((?:\|[^\n]*\n)+)', body)
    keys = {}
    if not m:
        return keys
    for row in m.group(1).splitlines():
        cells = [c.strip() for c in row.strip().strip('|').split('|')]
        if len(cells) < 4:
            continue
        qm = re.search(r'Q\s*(\d+)', cells[0])
        if not qm:
            continue
        keys[int(qm.group(1))] = (cells[1], cells[2], cells[3])
    return keys


def clean_key(raw):
    t = raw.replace('*', '').strip()
    m = re.match(r'^([A-D])\b', t)
    if m:
        return ('mcq', m.group(1))
    t = t.replace('$', '').replace(',', '').replace('{,}', '').strip()
    return ('spr', t)


def spr_expected(key):
    """Return (accepted_strings, expected_float_or_None)."""
    k = key
    acc = set()
    m = re.search(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', k)
    if m:
        try:
            a, b = float(m.group(1)), float(m.group(2))
            import math
            g = math.gcd(int(a), int(b))
            acc.add('%d/%d' % (int(a), int(b)))
            acc.add('%d/%d' % (int(a // g), int(b // g)))
            return sorted(acc), a / b
        except (ValueError, ZeroDivisionError):
            pass
    k2 = re.sub(r'\\[a-zA-Z]+\{?', '', k).replace('{', '').replace('}', '').strip()
    try:
        return sorted({k2}), float(k2)
    except ValueError:
        return sorted({k2}), None


def parse_solutions(body):
    """Map qnum -> html rationale from Solutions/Distractor sections."""
    sols = {}
    # sections after the answer-key table headed '### Question N'
    key_pos = re.search(r'\|[^\n]*Question[^\n]*\|[^\n]*(?:Correct|Key)', body)
    region = body[key_pos.end():] if key_pos else body
    chunks = re.split(r'(?m)^###\s+Question\s+(\d+)\s*$', region)
    for i in range(1, len(chunks), 2):
        if i + 1 >= len(chunks):
            break
        num = int(chunks[i])
        lines = chunks[i + 1].splitlines()
        # stop at next ## heading or alignment footer
        cut = []
        for ln in lines:
            if re.match(r'^##\s+', ln) or 'New System Alignment' in ln:
                break
            cut.append(ln)
        sols[num] = md_lines_to_html(cut)
    return sols


def pacing_seconds(info, n):
    txt = info.get('Pacing Guideline', '') + ' ' + info.get('Time Recommended', '')
    nums = []
    for a, b in re.findall(r'(\d+)\s*(?:[–-]\s*(\d+))?\s*seconds', txt):
        nums.append(int(a))
        if b:
            nums.append(int(b))
    per = max(nums) if nums else 75
    return per * n, per


CSS = """
:root{--bg:#e9f1fd;--surface:#fff;--surface2:#f4f8ff;--text:#0a1a3c;--muted:#5b6b8c;
--primary:#2b7fff;--primary-dark:#1a5fd0;--soft:#e3efff;--ok:#16a34a;--okbg:#f0fdf4;
--bad:#dc2626;--badbg:#fef2f2;--border:#d7e3f7;--radius:14px;
--font:'Segoe UI',system-ui,-apple-system,sans-serif;--mono:Consolas,monospace}
[data-theme=dark]{--bg:#0a1428;--surface:#12203c;--surface2:#0e1a32;--text:#eaf1ff;
--muted:#93a4c4;--primary:#5b97ff;--primary-dark:#3f7bf0;--soft:#1b2c52;
--okbg:#052e16;--badbg:#450a0a;--border:#243a63}
*{box-sizing:border-box}body{margin:0;font-family:var(--font);background:var(--bg);
color:var(--text);line-height:1.65;padding-bottom:4rem}
.topbar{background:var(--surface);border-bottom:1px solid var(--border);
position:sticky;top:0;z-index:50}.topbar-in{max-width:1180px;margin:0 auto;
padding:.6rem 1.2rem;display:flex;align-items:center;gap:.8rem;flex-wrap:wrap}
.brand{font-weight:800;text-decoration:none;color:var(--text)}
.badge{background:var(--soft);color:var(--primary);font-weight:800;font-size:.72rem;
border-radius:6px;padding:.15rem .5rem;text-transform:uppercase;letter-spacing:.05em}
.chips{display:flex;gap:.4rem;flex-wrap:wrap;margin-left:auto}
.chip{background:var(--surface2);border:1px solid var(--border);color:var(--muted);
border-radius:99px;padding:.2rem .7rem;font-size:.78rem;font-weight:600}
.wrap{max-width:1180px;margin:0 auto;padding:1.2rem}
.toolbar{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
padding:.7rem 1rem;display:flex;gap:.6rem;align-items:center;flex-wrap:wrap;
position:sticky;top:57px;z-index:40;box-shadow:0 4px 12px rgba(15,40,100,.07)}
.timer{font-family:var(--mono);font-weight:700;font-size:1.05rem}
.toolbtn{border:1.5px solid var(--border);background:var(--surface);color:var(--text);
border-radius:99px;padding:.32rem .85rem;cursor:pointer;font-weight:700;font-size:.82rem}
.toolbtn.on,.toolbtn.active{background:var(--primary);border-color:var(--primary);color:#fff}
.pill{border:1.5px solid var(--border);background:var(--surface);color:var(--muted);
border-radius:99px;padding:.3rem .9rem;cursor:pointer;font-weight:700;font-size:.82rem}
.pill.active{background:var(--primary);border-color:var(--primary);color:#fff}
.teach{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
margin:1rem 0;overflow:hidden}
.teach summary{cursor:pointer;font-weight:800;padding:.9rem 1.2rem;list-style:none}
.teach summary::-webkit-details-marker{display:none}
.teach summary::before{content:'\\25B6  ';color:var(--primary);font-size:.8rem}
.teach[open] summary::before{content:'\\25BC  '}
.teach-body{padding:0 1.2rem 1.2rem}
table.rules{width:100%;border-collapse:collapse;font-size:.86rem}
table.rules th,table.rules td{border-bottom:1px solid var(--border);padding:.45rem;text-align:left}
.diff{font-size:.7rem;font-weight:800;text-transform:uppercase;border-radius:6px;padding:.12rem .45rem;white-space:nowrap}
.diff-easy{background:#dcfce7;color:#166534}.diff-medium{background:#fef3c7;color:#92400e}
.diff-expert{background:#fee2e2;color:#991b1b}
.layout{display:grid;grid-template-columns:300px 1fr;gap:1rem;align-items:start;margin-top:1rem}
@media(max-width:900px){.layout{grid-template-columns:1fr}.stimulus{position:static!important;max-height:none!important}}
.stimulus{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
padding:1.1rem;position:sticky;top:140px;max-height:70vh;overflow:auto}
.qnav{display:flex;flex-wrap:wrap;gap:.35rem;margin:.6rem 0}
.qpill{width:36px;height:36px;border-radius:9px;border:1.5px solid var(--border);
background:var(--surface);color:var(--text);font-weight:800;cursor:pointer}
.qpill.cur{border-color:var(--primary);background:var(--soft)}
.qpill.ok{background:#dcfce7;border-color:var(--ok);color:#166534}
.qpill.no{background:#fee2e2;border-color:var(--bad);color:#991b1b}
.qpill.flag::after{content:' \\2691';font-size:.7rem}
.qcard{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.3rem}
.opt{display:block;width:100%;text-align:left;margin:.45rem 0;padding:.7rem .9rem;
border:1.5px solid var(--border);border-radius:10px;background:var(--surface);
color:var(--text);cursor:pointer;font-size:.95rem;font-family:var(--font)}
.opt:hover:not(:disabled){border-color:var(--primary)}
.opt.right{border-color:var(--ok);background:var(--okbg)}
.opt.wrong{border-color:var(--bad);background:var(--badbg)}
.opt.dim{opacity:.8}.opt:disabled{cursor:default}
.spr-row{display:flex;gap:.5rem;margin:.6rem 0}
.spr-row input{flex:1;font:inherit;color:var(--text);background:var(--surface2);
border:1.5px solid var(--border);border-radius:10px;padding:.6rem .8rem;font-family:var(--mono)}
.feedback{border-radius:10px;padding:.8rem 1rem;margin-top:.7rem;font-size:.92rem}
.feedback.good{background:var(--okbg);border:1.5px solid var(--ok)}
.feedback.bad{background:var(--badbg);border:1.5px solid var(--bad)}
details.sol{margin-top:.7rem}details.sol summary{cursor:pointer;font-weight:800;color:var(--primary)}
.sol-list{margin:.4rem 0}code{font-family:var(--mono);font-size:.85em;background:var(--surface2);
padding:.1rem .35rem;border-radius:6px}
.navrow{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1rem}
.btn{display:inline-block;border:none;cursor:pointer;font-weight:800;border-radius:99px;
padding:.55rem 1.3rem;font-size:.9rem;text-decoration:none}
.btn-p{background:var(--primary);color:#fff}.btn-g{background:var(--soft);color:var(--primary)}
.results{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
padding:1.3rem;margin-top:1rem}
.bar{height:9px;background:var(--surface2);border:1px solid var(--border);border-radius:99px;overflow:hidden}
.bar>span{display:block;height:100%;background:var(--primary)}
.foot{max-width:1180px;margin:2rem auto 0;padding:0 1.2rem;color:var(--muted);font-size:.85rem}
.foot a{color:var(--primary)}
@media print{.topbar,.toolbar,.navrow,.no-print{display:none!important}body{background:#fff}}
"""

JS_TEMPLATE = """
const QD = __DATA__;
const LSKEY = '__LSKEY__';
let state = {answers:{}, flags:[], idx:0, tier:'all', flagOnly:false, left:__SECS__, timerOn:false, timerId:null, done:false};
try{const s = JSON.parse(localStorage.getItem(LSKEY)); if(s && s.answers) state.answers=s.answers; if(s&&s.flags) state.flags=s.flags;}catch(e){}
function save(){try{localStorage.setItem(LSKEY, JSON.stringify({answers:state.answers,flags:state.flags}));}catch(e){}}
const LET=['A','B','C','D'];
function list(){return QD.filter(q=>(state.tier==='all'||q.tier===state.tier)&&(!state.flagOnly||state.flags.includes(q.id)));}
function fmt(s){s=Math.max(0,s);const m=Math.floor(s/60),r=s%60;return String(m).padStart(2,'0')+':'+String(r).padStart(2,'0');}
function tick(){document.getElementById('clock').textContent=fmt(state.left);}
function startTimer(){if(state.timerId)return;state.timerOn=true;state.timerId=setInterval(()=>{if(!state.timerOn)return;state.left--;tick();if(state.left<=0){clearInterval(state.timerId);state.timerId=null;finish();}},1000);}
function pauseTimer(){state.timerOn=!state.timerOn;document.getElementById('pauseBtn').textContent=state.timerOn?'Pause':'Resume';}
function resetTimer(){clearInterval(state.timerId);state.timerId=null;state.left=__SECS__;state.timerOn=false;document.getElementById('pauseBtn').textContent='Pause';tick();}
function renderNav(){const L=list();document.getElementById('qnav').innerHTML=L.map((q,i)=>{const a=state.answers[q.id];let c='qpill'+(i===state.idx?' cur':'')+(a?(a.ok?' ok':' no'):'')+(state.flags.includes(q.id)?' flag':'');return `<button class="${c}" data-i="${i}">${i+1}</button>`;}).join('');
document.querySelectorAll('#qnav .qpill').forEach(b=>b.onclick=()=>{state.idx=+b.dataset.i;renderQ();});}
function renderQ(){const L=list();const box=document.getElementById('qbox');
if(!L.length){box.innerHTML='<div class="qcard"><p>No questions match this filter.</p></div>';document.getElementById('stim').innerHTML='';renderNav();return;}
if(state.idx>=L.length)state.idx=0;
const q=L[state.idx],a=state.answers[q.id],flagged=state.flags.includes(q.id);
let stimHtml=`<span class="badge">${q.cat}</span> <span class="diff diff-${q.tier}">${q.tier}</span><p style="color:var(--muted);font-size:.82rem"><strong>${q.skill}</strong> &middot; source tier: ${q.tierRaw}</p>`;
if(q.passage)stimHtml+=`<h3>Passage</h3><p>${q.passage}</p>`;
document.getElementById('stim').innerHTML=stimHtml;
let inner=`<p><strong>Q${state.idx+1} of ${L.length}.</strong> ${q.stem}</p>`;
if(q.type==='mcq'){
inner+='<div>'+q.options.map((o,i)=>{let c='opt';if(a){c+=' dim';if(LET[i]===q.key)c+=' right';else if(LET[i]===a.pick)c+=' wrong';}return `<button class="${c}" data-p="${LET[i]}" ${a?'disabled':''}><strong>${LET[i]}.</strong> ${o}</button>`;}).join('')+'</div>';
}else{
inner+=`<div class="spr-row"><input id="sprIn" inputmode="decimal" placeholder="Enter your answer" value="${a?a.pick:''}" ${a?'disabled':''}><button class="btn btn-p" id="sprGo" ${a?'disabled':''}>Check</button></div><p style="color:var(--muted);font-size:.82rem">Student-produced response: equivalent fractions and decimals accepted.</p>`;
}
if(a){inner+=`<div class="feedback ${a.ok?'good':'bad'}">${a.ok?'&#10003; Correct.':'&#10007; Correct answer: <strong>${q.keyDisplay}</strong>.'}<details class="sol"><summary>Why? Show solution</summary>${q.sol}</details></div>`;}
inner+=`<div class="navrow"><button class="btn btn-g" id="prevB">&larr; Prev</button><button class="btn btn-g" id="nextB">Next &rarr;</button><button class="btn btn-g" id="flagB">${flagged?'&#9873; Flagged':'&#9872; Flag'}</button>${a?'<button class="btn btn-g" id="retryB">Retry</button>':''}<button class="btn btn-p" id="finB">Finish drill</button></div><div class="navrow"><span id="scoreLine" style="color:var(--muted);font-size:.85rem"></span></div>`;
box.innerHTML='<div class="qcard">'+inner+'</div>';
if(q.type==='mcq'&&!a){box.querySelectorAll('.opt').forEach(b=>b.onclick=()=>answer(q,b.dataset.p));}
if(q.type==='spr'&&!a){const go=()=>{const v=document.getElementById('sprIn').value;if(v.trim()==='')return;answer(q,v.trim());};document.getElementById('sprGo').onclick=go;document.getElementById('sprIn').addEventListener('keydown',e=>{if(e.key==='Enter')go();});}
document.getElementById('prevB').onclick=()=>{state.idx=(state.idx-1+L.length)%L.length;renderQ();};
document.getElementById('nextB').onclick=()=>{state.idx=(state.idx+1)%L.length;renderQ();};
document.getElementById('flagB').onclick=function(){const i=state.flags.indexOf(q.id);if(i>=0)state.flags.splice(i,1);else state.flags.push(q.id);save();renderQ();};
const rt=document.getElementById('retryB');if(rt)rt.onclick=()=>{delete state.answers[q.id];save();renderQ();};
document.getElementById('finB').onclick=finish;
if(window.renderMathInElement)try{renderMathInElement(box,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]});}catch(e){}
updateScore();renderNav();}
function sprOk(q,v){const s=v.replace(/[\\s,]/g,'');if(q.accept.includes(s))return true;if(q.expFloat===null||q.expFloat===undefined)return false;let n=null;const fr=s.match(/^(-?\\d+(?:\\.\\d+)?)\\/(-?\\d+(?:\\.\\d+)?)$/);if(fr&&parseFloat(fr[2])!==0)n=parseFloat(fr[1])/parseFloat(fr[2]);else if(/^-?\\d+(?:\\.\\d+)?$/.test(s))n=parseFloat(s);if(n===null||!isFinite(n))return false;const tol=Math.max(0.005,Math.abs(q.expFloat)*0.002);return Math.abs(n-q.expFloat)<=tol;}
function answer(q,pick){let ok;if(q.type==='mcq')ok=(pick===q.key);else ok=sprOk(q,pick);state.answers[q.id]={pick:pick,ok:ok};save();renderQ();}
function updateScore(){const ids=Object.keys(state.answers);const ok=ids.filter(k=>state.answers[k].ok).length;const el=document.getElementById('scoreLine');if(el)el.textContent=ids.length?`Score this device: ${ok}/${ids.length} (${Math.round(ok/ids.length*100)}%) — saved automatically`:'Answer to begin — progress saves on this device.';const g=document.getElementById('progFill');if(g){g.style.width=Math.min(100,Math.round(ids.length/QD.length*100))+'%';}}
function finish(){const L=list();let tot=0,ok=0;const byTier={};L.forEach(q=>{const a=state.answers[q.id];byTier[q.tier]=byTier[q.tier]||{t:0,o:0};byTier[q.tier].t++;if(a){tot++;if(a.ok){ok++;byTier[q.tier].o++;}}});
let rows=Object.keys(byTier).map(t=>{const b=byTier[t];const p=b.t?Math.round(b.o/b.t*100):0;return `<div><strong style="text-transform:capitalize">${t}</strong> — ${b.o}/${b.t} (${p}%)<div class="bar"><span style="width:${p}%"></span></div></div>`;}).join('');
const un=L.length-tot;
document.getElementById('results').innerHTML=`<div class="results"><h2>Drill complete: ${ok}/${L.length}</h2>${un?`<p>${un} unanswered.</p>`:''}${rows}<div class="navrow"><button class="btn btn-g" id="revMiss">Review misses in drill &uarr;</button></div></div>`;
document.getElementById('revMiss').onclick=()=>{document.getElementById('results').innerHTML='';window.scrollTo(0,0);};
document.getElementById('results').scrollIntoView({behavior:'smooth'});}
document.addEventListener('keydown',e=>{if(/INPUT|TEXTAREA|SELECT/.test((document.activeElement||{}).tagName))return;const m={'1':0,'2':1,'3':2,'4':3,a:0,b:1,c:2,d:3,A:0,B:1,C:2,D:3};if(e.key in m){const b=document.querySelectorAll('#qbox .opt');if(b[m[e.key]])b[m[e.key]].click();}if(e.key==='ArrowRight'){const n=document.getElementById('nextB');if(n)n.click();}if(e.key==='ArrowLeft'){const p=document.getElementById('prevB');if(p)p.click();}});
document.querySelectorAll('#tierRow .pill').forEach(p=>p.onclick=()=>{document.querySelectorAll('#tierRow .pill').forEach(x=>x.classList.remove('active'));p.classList.add('active');state.tier=p.dataset.t;state.idx=0;renderQ();});
document.getElementById('flagOnly').onclick=function(){state.flagOnly=!state.flagOnly;this.classList.toggle('on',state.flagOnly);state.idx=0;renderQ();};
document.getElementById('pauseBtn').onclick=pauseTimer;
document.getElementById('resetBtn').onclick=resetTimer;
document.getElementById('restartBtn').onclick=()=>{if(confirm('Clear saved answers for this drill?')){state.answers={};state.flags=[];state.idx=0;save();renderQ();}};
document.getElementById('themeBtn').onclick=()=>{const h=document.documentElement;const n=h.getAttribute('data-theme')==='dark'?'light':'dark';h.setAttribute('data-theme',n);try{localStorage.setItem('satdrill_theme',n);}catch(e){}};
try{if(localStorage.getItem('satdrill_theme')==='dark')document.documentElement.setAttribute('data-theme','dark');}catch(e){}
tick();startTimer();renderQ();
"""


def build_module(rel_path):
    src = os.path.join(SAT, *rel_path.split('/'))
    text = io.open(src, encoding='utf-8').read()
    meta, body = parse_frontmatter(text)
    info = parse_overview(body)
    questions = split_questions(body)
    keys = parse_key_table(body)
    sols = parse_solutions(body)

    domain = info.get('Domain', meta.get('domain', 'SAT'))
    skills = info.get('Target Skills', '')
    score = info.get('Target Score', meta.get('target_level', ''))
    pacing_info = info.get('Pacing Guideline', info.get('Time Recommended', ''))

    items = []
    for num, skill, block in questions:
        stem_lines, opts = [], {}
        for ln in block:
            s = ln.strip()
            if not s or s == '---':
                continue
            m = re.match(r'^-\s*\*\*([A-D])\)\*\*\s*(.*)$', s)
            if m:
                opts[m.group(1)] = m.group(2).strip()
            else:
                stem_lines.append(ln.rstrip())
        key_raw, rule, tier_raw = keys.get(num, ('', '', 'medium'))
        kind, kval = clean_key(key_raw)
        tier = TIER_BUCKET.get(tier_raw.strip().lower(), 'medium')
        if kind == 'mcq' and len(opts) == 4:
            qtype, key, accept, expf, key_display = 'mcq', kval, [], None, kval
        else:
            # SPR (or degraded): numeric answer from key table
            accept, expf = spr_expected(kval if kind == 'spr' else '')
            qtype, key, key_display = 'spr', '', (accept[0] if accept else kval)
        # group consecutive non-option lines into paragraphs
        paras, buf = [], []
        for ln in stem_lines:
            if ln.strip():
                buf.append(ln.strip())
            elif buf:
                paras.append(' '.join(buf))
                buf = []
        if buf:
            paras.append(' '.join(buf))
        stem = ''.join(('<p class="hint">%s</p>' if p.startswith('*(') else '<p>%s</p>') % inline_fmt(p) for p in paras)
        sol_html = sols.get(num, '<p>See worked solution in the study notes.</p>')
        items.append({'id': '%s-q%d' % (os.path.basename(src)[:-3], num), 'n': num,
                      'skill': skill or 'Mixed', 'tier': tier, 'tierRaw': tier_raw.strip() or 'Medium',
                      'type': qtype, 'stem': stem,
                      'passage': '', 'options': [opts.get(L, '') for L in LETTERS],
                      'key': key, 'keyDisplay': key_display, 'accept': accept,
                      'expFloat': expf, 'sol': sol_html, 'cat': domain})

    total_secs, per_item = pacing_seconds(info, max(len(items), 1))
    slug = os.path.basename(src)[:-3]
    depth = len(rel_path.split('/')) - 1
    up = '../' * depth
    title = re.sub(r'^[^\w\s"\']+', '', (re.search(r'^#\s+(.+)$', body, re.M).group(1)
                                         if re.search(r'^#\s+(.+)$', body, re.M) else meta.get('topic', slug))).strip()
    rules_rows = ''.join(
        '<tr><td>Q' + str(it['n']) + '</td><td>' + esc(it['skill']) + '</td><td>'
        + esc({'easy': 'Easy', 'medium': 'Medium', 'expert': 'Expert'}[it['tier']])
        + ' <span class="diff diff-' + it['tier'] + '">' + esc(it['tierRaw']) + '</span></td></tr>'
        for it in items)
    data_json = json.dumps([{'id': it['id'], 'tier': it['tier'], 'tierRaw': it['tierRaw'],
                             'skill': it['skill'], 'cat': it['cat'], 'type': it['type'],
                             'stem': it['stem'], 'passage': it['passage'], 'options': it['options'],
                             'key': it['key'], 'keyDisplay': it['keyDisplay'],
                             'accept': it['accept'], 'expFloat': it['expFloat'], 'sol': it['sol']}
                            for it in items], ensure_ascii=False)
    js = JS_TEMPLATE.replace('__DATA__', data_json).replace('__LSKEY__', 'satdrill_' + slug).replace('__SECS__', str(total_secs))
    counts = {t: sum(1 for it in items if it['tier'] == t) for t in ('easy', 'medium', 'expert')}
    html = ('<!DOCTYPE html><html lang="en" data-theme="light"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<title>@@TITLE@@ | SAT Drill</title>'
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">'
            '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>'
            '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" '
            'onload="renderMathInElement(document.body,{delimiters:[{left:\'$$\',right:\'$$\',display:true},{left:'
            '\'$\',right:\'$\',display:false}]});"></script>'
            '<style>@@CSS@@</style></head><body>'
            '<div class="topbar"><div class="topbar-in">'
            '<a class="brand" href="@@UP@@index.html">&larr; SAT Portal</a>'
            '<span class="badge">SAT drill</span>'
            '<div class="chips"><span class="chip">@@DOMAIN@@</span><span class="chip">Target @@SCORE@@</span>'
            '<span class="chip">@@N@@ questions</span><span class="chip">~@@PER@@s each</span></div>'
            '</div></div>'
            '<div class="wrap">'
            '<h1>@@TITLE@@</h1>'
            '<div class="toolbar"><span class="timer" id="clock">--:--</span>'
            '<button class="toolbtn" id="pauseBtn">Pause</button>'
            '<button class="toolbtn" id="resetBtn">Reset timer</button>'
            '<span id="tierRow"><button class="pill active" data-t="all">All</button>'
            '<button class="pill" data-t="easy">Easy (@@CE@@)</button>'
            '<button class="pill" data-t="medium">Medium (@@CM@@)</button>'
            '<button class="pill" data-t="expert">Expert (@@CX@@)</button></span>'
            '<button class="toolbtn" id="flagOnly">\u2691 Flagged</button>'
            '<button class="toolbtn" id="themeBtn">Theme</button>'
            '<button class="toolbtn" id="restartBtn">Restart</button></div>'
            '<details class="teach"><summary>What this drill trains &amp; how to use it</summary>'
            '<div class="teach-body"><p><strong>Skills:</strong> @@SKILLS@@</p>'
            '<table class="rules"><tr><th>#</th><th>Skill tested</th><th>Tier</th></tr>@@RULES@@</table>'
            '<p><strong>How to use:</strong> 1) Read the stem. 2) Answer (keys 1\u20134, arrows move). '
            '3) Open the solution to study the rule. Filter by tier to train easy, medium, or expert items.</p>'
            '</div></details>'
            '<div class="layout"><div class="stimulus"><strong>Navigator</strong><div class="qnav" id="qnav"></div>'
            '<div class="bar"><span id="progFill" style="width:0%"></span></div><div id="stim"></div></div>'
            '<div><div id="qbox"></div><div id="results"></div></div></div>'
            '</div>'
            '<div class="foot"><a href="@@UP@@index.html">&larr; SAT Portal</a> &middot; '
            '<a href="@@UP@@Show/show_walkthrough.html">Show walkthrough</a> &middot; '
            '<a href="@@UP@@Test/mock_01.html">Test mock</a> &middot; '
            '<a href="@@UP@@webapp/index.html#/practice">More practice in SATPrep Studio</a></div>'
            '<script>@@JS@@</script></body></html>')
    for tok, val in [('@@TITLE@@', esc(title)), ('@@CSS@@', CSS), ('@@UP@@', up),
                     ('@@DOMAIN@@', esc(domain)), ('@@SCORE@@', esc(score)),
                     ('@@N@@', str(len(items))), ('@@PER@@', str(per_item)),
                     ('@@CE@@', str(counts['easy'])), ('@@CM@@', str(counts['medium'])),
                     ('@@CX@@', str(counts['expert'])), ('@@SKILLS@@', esc(skills)),
                     ('@@RULES@@', rules_rows), ('@@JS@@', js)]:
        html = html.replace(tok, val)
    out = src[:-3] + '.html'
    io.open(out, 'w', encoding='utf-8').write(html)
    return out, len(items)


if __name__ == '__main__':
    total = 0
    for rel in SETS:
        out, n = build_module(rel)
        total += n
        print('rebuilt %s (%d items)' % (os.path.relpath(out, BASE), n))
    print('TOTAL ITEMS:', total)
