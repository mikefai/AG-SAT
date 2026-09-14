# 🏛️ SAT (Digital SAT) Workspace

Welcome to the **Digital SAT** dedicated workspace and standalone web platform.

- 🌐 **Independent Web Portal**: [`index.html`](index.html) *(Open locally or publish via GitHub Pages)*
- 🔗 **GitHub Repository**: [`https://github.com/mikefai/AG-SAT`](https://github.com/mikefai/AG-SAT)
- 🏠 **Master Workspace Hub**: [`./index.html`](./index.html)

---

## 📁 Directory Structure

```
SAT/
├── index.html                           # Standalone Digital SAT web portal connecting all creations
├── Reading_Writing/
│   ├── Craft_and_Structure/             # Words in context, Text structure and purpose, Cross-text connections
│   ├── Information_and_Ideas/           # Central ideas, Command of evidence (textual & quantitative), Inferences
│   ├── Standard_English_Conventions/    # Boundaries (semicolons, periods, comma splices), Form, structure, and sense
│   └── Expression_of_Ideas/             # Rhetorical synthesis (bullet point notes), Transitions
├── Math/
│   ├── Algebra/                         # Linear equations, systems, inequalities
│   ├── Advanced_Math/                   # Quadratics, polynomials, exponential functions
│   ├── Problem_Solving_and_Data_Analysis/ # Ratios, percentages, probability, statistics
│   └── Geometry_and_Trigonometry/       # Angles, triangles, circles, trigonometric ratios
├── Question_Banks/                      # High-yield discrete drills by difficulty (Easy, Medium, Hard)
├── Practice_Modules/                    # 27-question Reading/Writing & 22-question Math adaptive modules
└── README.md                            # This document
```

---

## 🎯 Digital SAT Domain Breakdown (Reading & Writing)

| Domain | Approximate Question Count per Module | Content Focus |
| :--- | :--- | :--- |
| **Craft and Structure** | ~28% (13–15 Qs total) | High-utility academic vocabulary, tone, rhetorical craft, author's perspective |
| **Information and Ideas** | ~26% (12–14 Qs total) | Finding main claims, scientific and humanities evidence graphs/tables, logical deductions |
| **Standard English Conventions** | ~26% (11–15 Qs total) | Sentence boundaries, subject-verb agreement, modifier placement, verb tense/aspect |
| **Expression of Ideas** | ~20% (8–12 Qs total) | Transition words (*consequently, conversely, moreover*), synthesizing research notes |

---

## 📋 Content Creation Standard

When generating SAT content:
1. **Accurate Item Design**: Follow College Board single-passage prompt formats (25–150 words per stimulus).
2. **Four-Option Multiple Choice**: Provide exactly 4 options (`A`, `B`, `C`, `D`) for Reading/Writing.
3. **Comprehensive Rationales**:
   - Explicitly detail why the correct answer is logically/grammatically sound.
   - Provide precise error breakdown for each of the 3 distractors.
4. **Synchronization**: After creating new items, execute `python scripts/build_workspace_index.py` to update the connected portal.

---
## New System Alignment (Updated)
**Flow:** Teach → Show → Test
- **Teach:** Detailed strategy and rules (this file)
- **Show:** Walkthrough solving examples — [SAT/Show/show_walkthrough.html](./Show/show_walkthrough.html)
- **Test:** Real SAT difficulty mock — [SAT/Test/mock_01.html](./Test/mock_01.html)
- **Portal:** [SAT/index.html](./index.html) (interactive pen / highlight / mark tools)
---
