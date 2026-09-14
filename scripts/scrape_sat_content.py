"""Scrape SAT question banks from markdown into structured JSON for the web service.
Handles: full MCQ format, inline-option format, and open/fix format.
"""
import json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QB = os.path.join(BASE, "SAT", "Question_Banks")
OUT = os.path.join(BASE, "SAT", "webapp", "data")
os.makedirs(OUT, exist_ok=True)

FILES = {
    "Craft & Structure": "sat_craft_structure_10_items.md",
    "Information & Ideas": "sat_information_ideas_10_items.md",
    "Expression of Ideas": "sat_expression_ideas_10_items.md",
    "Standard English Conventions": "sat_standard_conventions_10_items.md",
    "Algebra": "sat_algebra_10_items.md",
    "Advanced Math": "sat_advanced_math_10_items.md",
    "Problem Solving & Data Analysis": "sat_problem_solving_10_items.md",
    "Geometry & Trigonometry": "sat_geometry_10_items.md",
}

def clean_md(s):
    s = re.sub(r"\*\*(.*?)\*\*", r"\1", s)
    return s.strip()

def parse_bank(path, category):
    text = open(path, encoding="utf-8").read()
    chunks = re.split(r"\n## Q(?=\d)", text)
    items = []
    for chunk in chunks[1:]:
        lines = [l.rstrip() for l in chunk.splitlines()]
        header = lines[0].strip()
        qnum_m = re.match(r"(\d+)", header)
        if not qnum_m:
            continue
        qnum = int(qnum_m.group(1))
        m = re.match(r"\d+\s*[—–-]\s*(.+?)\s*\((Easy|Medium|Hard)\)", header)
        skill = clean_md(m.group(1)).strip() if m else "Mixed"
        difficulty = m.group(2).lower() if m else "medium"
        body = "\n".join(lines[1:])

        passage = None
        pm = re.search(r"\*\*(Passage[^:]*):\*\*\s*(.+)", body)
        if pm:
            passage = clean_md(pm.group(2))

        question = None
        qm = re.search(r"\*\*Question:\*\*\s*(.+)", body)
        if qm:
            question = clean_md(qm.group(1))
        else:
            # Fallback: Q: / Fix: / Best... lines
            qm2 = re.search(r"^(?:Q|Fix|Best[^:]*):\s*(.+)$", body, re.M)
            if qm2:
                question = clean_md(qm2.group(0))

        options = {}
        # Format A: "- A. text" lines
        for lm in re.finditer(r"^\s*-\s*([A-D])[.:)]\s+(.+)$", body, re.M):
            options[lm.group(1)] = clean_md(lm.group(2))
        # Format B: "A) opt / B) opt / C) opt / D) opt" on one line
        if len(options) < 4:
            for ln in body.splitlines():
                if sum(1 for t in ("A)", "B)", "C)", "D)") if t in ln) >= 2:
                    parts = re.split(r"\s*/\s*", ln.strip())
                    for part in parts:
                        pm2 = re.match(r"^([A-D])[).]\s*(.+)$", part.strip())
                        if pm2 and pm2.group(1) not in options:
                            options[pm2.group(1)] = clean_md(pm2.group(2))
                    if len(options) >= 4:
                        break

        answer_key, rationale = None, ""
        am = re.search(r"\*\*Answer:\*\*\s*(.+)", body, re.S)
        if not am:
            am = re.search(r"^Answer:\s*(.+)", body, re.M | re.S)
        if am:
            ans_full = clean_md(am.group(1).strip().splitlines()[0])
            # Answer may be "B. rationale" or free text (open format)
            km = re.match(r"^([A-D])(?:[.)]\s*|\s+\()(.*)$", ans_full)
            if km and len(options) == 4:
                answer_key = km.group(1)
                rationale = km.group(2).strip()
            else:
                rationale = ans_full

        # Stimulus: first non-empty line that isn't Q/Fix/Answer/option
        stimulus = None
        for ln in lines[1:]:
            s = ln.strip()
            if not s or s in ("---", "***") or s.startswith(("**Question", "**Answer", "Answer:", "Q:", "Fix:", "- A", "- B", "- C", "- D", "A)", "**Portal", "**Study")):
                continue
            if s.startswith("**Passage"):
                continue
            stimulus = clean_md(s)
            break

        if len(options) == 4 and answer_key:
            qtype = "mcq"
            opts = [options.get("A", ""), options.get("B", ""), options.get("C", ""), options.get("D", "")]
        else:
            qtype = "open"
            opts = []

        if question or stimulus or passage:
            items.append({
                "id": f"{category}-Q{qnum}",
                "category": category,
                "skill": skill,
                "difficulty": difficulty,
                "type": qtype,
                "passage": passage,
                "stimulus": stimulus,
                "question": question,
                "options": opts,
                "answer": answer_key,
                "rationale": rationale or "See study notes.",
            })
    return items

all_questions = []
for cat, fname in FILES.items():
    p = os.path.join(QB, fname)
    if not os.path.exists(p):
        print(f"MISSING: {p}")
        continue
    items = parse_bank(p, cat)
    mcq = sum(1 for i in items if i["type"] == "mcq")
    print(f"{cat}: {len(items)} items ({mcq} mcq)")
    all_questions.extend(items)

json.dump(all_questions, open(os.path.join(OUT, "questions.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"TOTAL: {len(all_questions)} questions -> SAT/webapp/data/questions.json")
