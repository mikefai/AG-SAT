---
domain: "SAT"
target_level: "Score 750 - 800"
topic: "Geometry, Trigonometry & Data Analysis Masterclass"
date_created: "2026-09-01"
content_type: "Question Bank / Drill"
---

# 📐 Digital SAT Math: Geometry, Trigonometry & Data Analysis Masterclass

## 📋 Module Overview
- **Domain**: Geometry & Trigonometry, Problem-Solving and Data Analysis
- **Target Skills**: Circle Equations & Completing the Square, Radian Arc Length & Sector Area, Complementary Angle Trigonometry $\sin(\theta) = \cos(90^\circ - \theta)$, Conditional Probability Tables, Margin of Error
- **Calculator Policy**: Desmos Graphing Calculator Permitted
- **Number of Items**: 5 Items (4 Multiple Choice, 1 Student-Produced Response)
- **Time Recommended**: ~80 seconds per item

---

## ❓ Math Problems

### Question 1 (Multiple Choice: Circle Equation & Completing the Square)
In the $xy$-plane, the equation of a circle is given by:

$$x^2 + y^2 - 8x + 10y + 5 = 0$$

What are the coordinates of the center $(h, k)$ and the radius $r$ of the circle?

- **A)** Center: $(4, -5)$, Radius: $r = 6$
- **B)** Center: $(-4, 5)$, Radius: $r = 6$
- **C)** Center: $(4, -5)$, Radius: $r = 36$
- **D)** Center: $(-8, 10)$, Radius: $r = \sqrt{5}$

---

### Question 2 (Multiple Choice: Right Triangle Trigonometric Identities)
In right triangle $\triangle ABC$, angle $C$ is a right angle ($90^\circ$). If $\sin(A) = \frac{7}{25}$, what is the value of $\cos(B)$?

- **A)** $\frac{7}{25}$
- **B)** $\frac{24}{25}$
- **C)** $\frac{25}{7}$
- **D)** $\frac{7}{24}$

---

### Question 3 (Multiple Choice: Arc Length & Radian Measure)
In a circle with center $O$, central angle $\angle AOB$ intercepts an arc $AB$ of length $14\pi\text{ cm}$. If the radius of the circle is $21\text{ cm}$, what is the radian measure of central angle $\angle AOB$?

- **A)** $\frac{\pi}{3}$
- **B)** $\frac{2\pi}{3}$
- **C)** $\frac{3\pi}{4}$
- **D)** $\frac{4\pi}{3}$

---

### Question 4 (Multiple Choice: Two-Way Frequency Table & Conditional Probability)
A clinical trial surveyed 200 participants across two age demographics regarding their response to a new allergy therapy.

| Demographics | Significant Symptom Relief | Moderate Relief | No Improvement | Total |
| :--- | :---: | :---: | :---: | :---: |
| **Adults (18–50)** | 64 | 36 | 20 | **120** |
| **Seniors (51+)** | 32 | 16 | 32 | **80** |
| **Total** | **96** | **52** | **52** | **200** |

If a participant who experienced "Significant Symptom Relief" is selected at random, what is the probability that this individual is in the "Adults (18–50)" demographic?

- **A)** $\frac{64}{120}$
- **B)** $\frac{64}{200}$
- **C)** $\frac{64}{96}$
- **D)** $\frac{96}{200}$

---

### Question 5 (Student-Produced Response: Special Right Triangles & 3D Geometry)
A right rectangular prism has a square base with side length $6\text{ cm}$ and a height of $7\text{ cm}$. What is the length, in centimeters, of the interior space diagonal that connects two opposite vertices of the prism?

*(Enter your exact integer answer if a whole number, or round to the nearest whole integer if applicable: here $\sqrt{6^2 + 6^2 + 7^2} = \sqrt{121} = 11$).*

---

## 🔑 Answer Key & Dual Solution Methods

| Question | Correct Answer | Domain / Sub-Topic | Difficulty Tier |
| :---: | :---: | :---: | :---: |
| **Q1** | **A (Center: $(4, -5)$, Radius: $6$)** | Geometry: Circle Standard Form | Hard |
| **Q2** | **A ($\frac{7}{25}$)** | Trigonometry: Complementary Angle Co-functions | Medium |
| **Q3** | **B ($\frac{2\pi}{3}$)** | Geometry: Radian Arc Length Formula | Medium |
| **Q4** | **C ($\frac{64}{96} = \frac{2}{3}$)** | Data Analysis: Conditional Probability | Medium-Hard |
| **Q5** | **11** | Geometry: 3D Space Diagonal Theorem | Medium-Hard |

---

## 💡 In-Depth Solutions & Desmos Shortcuts

### Question 1
- **Correct Answer: A (Center: $(4, -5)$, Radius: $r = 6$)**
- **Method 1 (Completing the Square)**:
  Group $x$ and $y$ terms:
  $$(x^2 - 8x) + (y^2 + 10y) = -5$$
  Complete square for $x$: $(\frac{-8}{2})^2 = (-4)^2 = 16$.
  Complete square for $y$: $(\frac{10}{2})^2 = 5^2 = 25$.
  Add both values to both sides of the equation:
  $$(x^2 - 8x + 16) + (y^2 + 10y + 25) = -5 + 16 + 25$$
  $$(x - 4)^2 + (y + 5)^2 = 36$$
  Comparing to the standard circle equation $(x - h)^2 + (y - k)^2 = r^2$:
  - Center $(h, k) = (4, -5)$
  - Radius $r = \sqrt{36} = 6$
- **Desmos Graphing Shortcut**:
  1. Type `x^2 + y^2 - 8x + 10y + 5 = 0` directly into Desmos.
  2. Click on the center point or find the leftmost and rightmost points ($x = -2$ to $x = 10 \implies \text{diameter} = 12 \implies r = 6$).
  3. Center is at $(4, -5)$.

---

### Question 2
- **Correct Answer: A ($\frac{7}{25}$)**
- **Method 1 (Cofunction Identity Theorem)**:
  In any right triangle where $\angle C = 90^\circ$, angles $A$ and $B$ are complementary ($\angle A + \angle B = 90^\circ$).
  The fundamental trigonometric cofunction identity states:
  $$\sin(A) = \cos(90^\circ - A) = \cos(B)$$
  Therefore, since $\sin(A) = \frac{7}{25}$, it immediately follows that $\cos(B) = \frac{7}{25}$.
- **Method 2 (Geometric Definition: SOH-CAH-TOA)**:
  - $\sin(A) = \frac{\text{Opposite to } A}{\text{Hypotenuse}} = \frac{a}{c} = \frac{7}{25}$
  - $\cos(B) = \frac{\text{Adjacent to } B}{\text{Hypotenuse}} = \frac{a}{c} = \frac{7}{25}$
  Both evaluate to the exact same side ratio $\frac{a}{c}$.

---

### Question 3
- **Correct Answer: B ($\frac{2\pi}{3}$)**
- **Method 1 (Radian Arc Length Formula)**:
  The formula relating arc length $s$, radius $r$, and radian angle $\theta$ is:
  $$s = r \cdot \theta$$
  Given $s = 14\pi$ and $r = 21$:
  $$14\pi = 21 \cdot \theta \implies \theta = \frac{14\pi}{21} = \frac{2\pi}{3}\text{ radians}$$

---

### Question 4
- **Correct Answer: C ($\frac{64}{96}$)**
- **Method 1 (Conditional Probability Formula)**:
  The condition given is: *"A participant who experienced Significant Symptom Relief is selected."*
  This restricts our sample space denominator strictly to the "Significant Symptom Relief" column total ($96$).
  The numerator is the number of adults within this specific group ($64$).
  $$P(\text{Adult} \mid \text{Significant Relief}) = \frac{64}{96} = \frac{2}{3}$$
- **Distractor Analysis**:
  - **A ($\frac{64}{120}$)**: The condition is inverted (calculating probability of relief given that the person is an adult).
  - **B ($\frac{64}{200}$)**: Failed to restrict the sample space; used the grand total 200 as denominator.

---

### Question 5
- **Correct Answer: 11**
- **Method 1 (3D Space Diagonal Distance Formula)**:
  For a rectangular prism with dimensions length $l$, width $w$, and height $h$, the interior 3D space diagonal $d$ is:
  $$d = \sqrt{l^2 + w^2 + h^2}$$
  Given $l = 6$, $w = 6$, and $h = 7$:
  $$d = \sqrt{6^2 + 6^2 + 7^2} = \sqrt{36 + 36 + 49} = \sqrt{121} = 11\text{ cm}$$

---
## New System Alignment (Updated)
**Flow:** Teach → Show → Test
- **Teach:** Detailed strategy and rules (this file)
- **Show:** Walkthrough solving examples — [SAT/Show/show_walkthrough.html](../../Show/show_walkthrough.html)
- **Test:** Real SAT difficulty mock — [SAT/Test/mock_01.html](../../Test/mock_01.html)
- **Portal:** [SAT/index.html](../../index.html) (interactive pen / highlight / mark tools)
---
