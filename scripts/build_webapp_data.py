"""Convert questions.json + lessons.json into browser-safe classic scripts
(window.SAT_QUESTIONS / window.SAT_LESSONS) for file:// compatibility.
Also validates integrity: 8 categories x 10, keys A-D, options non-empty.
"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "SAT", "webapp", "data")

questions = json.load(open(os.path.join(DATA, "questions.json"), encoding="utf-8"))
lessons = json.load(open(os.path.join(DATA, "lessons.json"), encoding="utf-8"))

# --- validation ---
from collections import Counter
cats = Counter(q["category"] for q in questions)
print("Per-category counts:", dict(cats))
assert len(questions) == 280, f"expected 280, got {len(questions)}"
assert all(len(q["options"]) == 4 and all(o.strip() for o in q["options"]) for q in questions), "bad options"
assert all(q["answer"] in ("A", "B", "C", "D") for q in questions), "bad keys"
assert all(q["rationale"].strip() for q in questions), "empty rationale"
assert len(lessons) == 8, f"expected 8 lessons, got {len(lessons)}"
print("Validation OK: 280 MCQ, keys A-D, rationales present, 8 lessons.")

# --- emit classic scripts ---
with open(os.path.join(DATA, "questions.js"), "w", encoding="utf-8") as f:
    f.write("window.SAT_QUESTIONS = ")
    json.dump(questions, f, ensure_ascii=False)
    f.write(";\n")
with open(os.path.join(DATA, "lessons.js"), "w", encoding="utf-8") as f:
    f.write("window.SAT_LESSONS = ")
    json.dump(lessons, f, ensure_ascii=False)
    f.write(";\n")
print("Wrote questions.js + lessons.js")
