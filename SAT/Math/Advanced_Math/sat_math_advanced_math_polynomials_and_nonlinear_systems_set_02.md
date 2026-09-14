---
domain: "SAT"
target_level: "Score 750 - 800"
topic: "Polynomials, Remainder Theorem & Nonlinear Systems"
date_created: "2026-09-01"
content_type: "Question Bank / Drill"
---

# 📐 Digital SAT Math: Polynomials, Remainder Theorem & Nonlinear Systems

## 📋 Module Overview
- **Domain**: Advanced Math
- **Target Skills**: Polynomial Remainder & Factor Theorems, Higher-Order Polynomial Graphs & End Behavior, Rational Expressions & Vertical/Horizontal Asymptotes, Nonlinear Systems of Equations
- **Calculator Policy**: Desmos Permitted
- **Number of Items**: 5 Hard-Tier Items (3 Multiple Choice, 2 Student-Produced Responses)
- **Time Recommended**: ~90 seconds per item

---

## ❓ Math Problems

### Question 1 (Multiple Choice: Polynomial Remainder Theorem)
The polynomial function $P(x)$ is defined by:

$$P(x) = 2x^3 - kx^2 + 7x - 18$$

where $k$ is a constant. When $P(x)$ is divided by $(x - 3)$, the remainder is $12$. What is the value of $k$?

- **A)** $3$
- **B)** $5$
- **C)** $7$
- **D)** $9$

---

### Question 2 (Multiple Choice: Factor Theorem & Multiplicity of Roots)
The graph of a polynomial function $f(x)$ touches the $x$-axis at $x = -4$ without crossing it, crosses the $x$-axis at $x = 2$, and has a $y$-intercept at $(0, -32)$. Which of the following could be the equation defining $f(x)$?

- **A)** $f(x) = (x + 4)^2(x - 2)$
- **B)** $f(x) = -(x + 4)^2(x - 2)$
- **C)** $f(x) = (x + 4)(x - 2)^2$
- **D)** $f(x) = 2(x + 4)^2(x - 2)$

---

### Question 3 (Multiple Choice: Nonlinear System of Equations)
In the $xy$-plane, the graphs of the circle $(x - 2)^2 + (y + 1)^2 = 25$ and the line $y = x - 3$ intersect at two points $(x_1, y_1)$ and $(x_2, y_2)$. What is the value of $x_1 + x_2$?

- **A)** $2$
- **B)** $4$
- **C)** $6$
- **D)** $8$

---

### Question 4 (Student-Produced Response: Rational Function Horizontal Asymptote)
The rational function $R(x)$ is given by:

$$R(x) = \frac{15x^3 - 4x + 7}{3x^3 + 8x^2 - 19}$$

The graph of $y = R(x)$ has a horizontal asymptote at $y = c$. What is the value of the constant $c$?

---

### Question 5 (Student-Produced Response: Vieta's Relations on Cubic Polynomials)
The cubic equation $x^3 - 9x^2 + 23x - 15 = 0$ has three distinct real roots $r_1$, $r_2$, and $r_3$. If two of the roots are $r_1 = 1$ and $r_2 = 3$, what is the value of the third root $r_3$?

---

## 🔑 Answer Key & Dual Solution Methods

| Question | Correct Answer | Topic / Concept | Difficulty Tier |
| :---: | :---: | :--- | :---: |
| **Q1** | **B ($k = 5$)** | Polynomial Remainder Theorem | Hard |
| **Q2** | **A ($f(x) = (x+4)^2(x-2)$)** | Factor Theorem & Root Multiplicity | Hard |
| **Q3** | **B ($4$)** | Circle-Line Nonlinear System Intersection | Hard |
| **Q4** | **5** | Rational Function Horizontal Asymptote | Medium-Hard |
| **Q5** | **5** | Vieta's Formulas / Cubic Root Relations | Medium |

---

## 💡 Dual Solutions, Distractor Rationales & Explanations

### Question 1
- **Algebraic (Remainder Theorem)**:
  According to the Polynomial Remainder Theorem, the remainder when $P(x)$ is divided by $(x - c)$ is simply $P(c)$.
  Here $c = 3$ and remainder $= 12$:
  $$P(3) = 2(3)^3 - k(3)^2 + 7(3) - 18 = 12$$
  $$2(27) - 9k + 21 - 18 = 12$$
  $$54 - 9k + 3 = 12 \implies 57 - 9k = 12 \implies 9k = 45 \implies k = 5\text{ ??? wait: } 57 - 12 = 45 \implies k = 5$$
  *Wait! Let's re-verify:* $54 + 21 - 18 = 57$. $57 - 9k = 12 \implies 9k = 45 \implies k = 5$.
  *Let's check option B: $k = 5$!*

### Question 2
- **Algebraic**:
  - Touching without crossing at $x = -4$ implies an even multiplicity factor $(x + 4)^2$.
  - Crossing at $x = 2$ implies an odd multiplicity factor $(x - 2)$.
  - Form: $f(x) = a(x + 4)^2(x - 2)$.
  - Given $y$-intercept $(0, -32)$:
    $$-32 = a(0 + 4)^2(0 - 2) = a(16)(-2) = -32a \implies a = 1$$
    *Wait: If $a = 1$, $f(x) = (x+4)^2(x-2)$, which has $y$-intercept $-32$. If option A is $-(x+4)^2(x-2)$, that would give $+32$. If $a = 1$, $f(x) = (x+4)^2(x-2)$.*

### Question 3
- **Algebraic**:
  Substitute $y = x - 3$ into the circle equation:
  $$(x - 2)^2 + ((x - 3) + 1)^2 = 25$$
  $$(x - 2)^2 + (x - 2)^2 = 25 \implies 2(x - 2)^2 = 25$$
  $$(x - 2)^2 = \frac{25}{2} \implies x - 2 = \pm \frac{5}{\sqrt{2}} \implies x = 2 \pm \frac{5\sqrt{2}}{2}$$
  The sum of the $x$-coordinates is:
  $$x_1 + x_2 = \left(2 + \frac{5\sqrt{2}}{2}\right) + \left(2 - \frac{5\sqrt{2}}{2}\right) = 4$$

### Question 4
- **Algebraic**:
  For rational functions where degrees of numerator and denominator are equal (degree 3), the horizontal asymptote is the ratio of leading coefficients:
  $$y = \frac{15}{3} = 5 \implies c = 5$$

### Question 5
- **Algebraic**:
  By Vieta's formulas for $x^3 - bx^2 + cx - d = 0$, the sum of the roots equals $-\frac{-9}{1} = 9$:
  $$r_1 + r_2 + r_3 = 9 \implies 1 + 3 + r_3 = 9 \implies 4 + r_3 = 9 \implies r_3 = 5$$
  Also by product of roots: $r_1 \cdot r_2 \cdot r_3 = 15 \implies (1)(3)(r_3) = 15 \implies r_3 = 5$.

---
## New System Alignment (Updated)
**Flow:** Teach → Show → Test
- **Teach:** Detailed strategy and rules (this file)
- **Show:** Walkthrough solving examples — [SAT/Show/show_walkthrough.html](../../Show/show_walkthrough.html)
- **Test:** Real SAT difficulty mock — [SAT/Test/mock_01.html](../../Test/mock_01.html)
- **Portal:** [SAT/index.html](../../index.html) (interactive pen / highlight / mark tools)
---
