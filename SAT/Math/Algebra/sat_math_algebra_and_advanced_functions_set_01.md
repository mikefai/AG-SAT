---
domain: "SAT"
target_level: "Score 750 - 800"
topic: "Algebra & Advanced Math High-Yield Problem Set"
date_created: "2026-09-01"
content_type: "Question Bank / Drill"
---

# 📐 Digital SAT Math: Algebra & Advanced Math Masterclass

## 📋 Module Overview
- **Domain**: Algebra & Advanced Math
- **Target Skills**: Systems of Linear Equations (Constants for No/Infinite Solutions), Quadratic Functions & Vertex Form, Discriminant $\Delta = b^2 - 4ac$, Radical & Rational Equations, Exponential Modeling
- **Calculator Policy**: Desmos Graphing Calculator Permitted (Embedded shortcuts included)
- **Number of Items**: 5 Items (4 Multiple Choice, 1 Student-Produced Response)
- **Time Recommended**: ~80 seconds per item

---

## ❓ Math Problems

### Question 1 (Multiple Choice: Systems of Linear Equations with Constants)
In the system of equations below, $k$ is a constant.

$$\begin{cases} 
3x - 5y = 14 \\ 
kx + 15y = -42 
\end{cases}$$

If the system has infinitely many solutions, what is the value of $k$?

- **A)** $-9$
- **B)** $-3$
- **C)** $3$
- **D)** $9$

---

### Question 2 (Multiple Choice: Quadratic Vertex Form & Transformations)
A quadratic function $f(x)$ has its vertex at $(4, -18)$ and passes through the point $(1, 0)$. Which of the following defines $f(x)$ in standard form?

- **A)** $f(x) = 2x^2 - 16x + 14$
- **B)** $f(x) = 2x^2 - 8x - 10$
- **C)** $f(x) = -2x^2 + 16x - 14$
- **D)** $f(x) = x^2 - 8x + 7$

---

### Question 3 (Multiple Choice: Discriminant & Number of Real Solutions)
For what value of the constant $c$ does the equation $4x^2 - 12x + c = 0$ have exactly one distinct real solution?

- **A)** $-9$
- **B)** $3$
- **C)** $9$
- **D)** $36$

---

### Question 4 (Multiple Choice: Rational Expressions & Asymptotes)
The function $g$ is defined by:

$$g(x) = \frac{3x^2 - 12}{x^2 - 5x + 6}$$

For what value of $x$ does the graph of $y = g(x)$ have a removable discontinuity (a hole) rather than a vertical asymptote?

- **A)** $x = -2$
- **B)** $x = 2$
- **C)** $x = 3$
- **D)** $x = 6$

---

### Question 5 (Student-Produced Response: Exponential Growth & Modeling)
A microbiological culture initially contains $450$ bacterial cells. Under optimal laboratory conditions, the population doubles every $18$ hours according to the function:

$$P(t) = 450 \cdot 2^{\frac{t}{k}}$$

where $t$ represents time in hours. If after $72$ hours the population reaches $7{,}200$ cells, what is the value of the constant $k$?

*(Enter your numerical answer as an integer).*

---

## 🔑 Answer Key & Dual Solution Methods

| Question | Correct Answer | Domain / Sub-Topic | Difficulty Tier |
| :---: | :---: | :---: | :---: |
| **Q1** | **A ($-9$)** | Algebra: Systems with Infinite Solutions | Medium-Hard |
| **Q2** | **A ($f(x) = 2x^2 - 16x + 14$)** | Advanced Math: Quadratic Vertex Form | Hard |
| **Q3** | **C ($9$)** | Advanced Math: Discriminant Condition | Medium |
| **Q4** | **B ($x = 2$)** | Advanced Math: Rational Functions & Discontinuity | Hard |
| **Q5** | **18** | Advanced Math: Exponential Growth Models | Medium-Hard |

---

## 💡 In-Depth Solutions & Desmos Shortcuts

### Question 1
- **Correct Answer: A ($-9$)**
- **Method 1 (Algebraic Ratio Method)**:
  For a linear system $a_1 x + b_1 y = c_1$ and $a_2 x + b_2 y = c_2$ to have infinitely many solutions, the two equations must be linearly dependent (identical lines):
  $$\frac{a_1}{a_2} = \frac{b_1}{b_2} = \frac{c_1}{c_2}$$
  Comparing the coefficients of $y$ and the constants:
  $$\frac{-5}{15} = \frac{14}{-42} = -\frac{1}{3}$$
  Therefore:
  $$\frac{3}{k} = -\frac{1}{3} \implies k = 3 \cdot (-3) = -9$$
- **Method 2 (Desmos Graphing Shortcut)**:
  1. Type `3x - 5y = 14` into line 1.
  2. Type `kx + 15y = -42` into line 2 and add a slider for `k`.
  3. Adjust `k` until line 2 overlaps line 1 completely across all points. The slider lands exactly on $k = -9$.
- **Distractor Analysis**:
  - **D ($9$)**: Result if the student forgets the sign inversion between $-5$ and $+15$.
  - **B ($-3$)**: Result of an inverted ratio error ($\frac{k}{3} = -1$).

---

### Question 2
- **Correct Answer: A ($f(x) = 2x^2 - 16x + 14$)**
- **Method 1 (Vertex Form to Standard Form)**:
  The vertex form of a parabola is:
  $$f(x) = a(x - h)^2 + k$$
  Given vertex $(h, k) = (4, -18)$:
  $$f(x) = a(x - 4)^2 - 18$$
  Substitute the point $(1, 0)$ where $f(1) = 0$:
  $$0 = a(1 - 4)^2 - 18 \implies 0 = 9a - 18 \implies 9a = 18 \implies a = 2$$
  Now expand into standard form:
  $$f(x) = 2(x^2 - 8x + 16) - 18 = 2x^2 - 16x + 32 - 18 = 2x^2 - 16x + 14$$
- **Method 2 (Desmos Graphing Shortcut)**:
  1. Plot the points $(4, -18)$ and $(1, 0)$ in Desmos.
  2. Type each multiple choice option into Desmos.
  3. Option A is the only parabola whose minimum vertex touches $(4, -18)$ and crosses the x-axis at $(1, 0)$.

---

### Question 3
- **Correct Answer: C ($9$)**
- **Method 1 (Discriminant Analysis)**:
  A quadratic equation $ax^2 + bx + c = 0$ has exactly one real solution (a double root) when the discriminant equals zero:
  $$\Delta = b^2 - 4ac = 0$$
  Here $a = 4$, $b = -12$, and $c$ is unknown:
  $$(-12)^2 - 4(4)(c) = 0$$
  $$144 - 16c = 0 \implies 16c = 144 \implies c = \frac{144}{16} = 9$$
- **Method 2 (Perfect Square Trinomial)**:
  $$4x^2 - 12x + c = (2x - 3)^2 = 4x^2 - 12x + 9 \implies c = 9$$
- **Desmos Shortcut**:
  Type `y = 4x^2 - 12x + c` with a slider for `c`. The graph touches the x-axis at exactly one tangent point when $c = 9$.

---

### Question 4
- **Correct Answer: B ($x = 2$)**
- **Method 1 (Factoring & Discontinuity Analysis)**:
  Factor both numerator and denominator completely:
  $$\text{Numerator: } 3(x^2 - 4) = 3(x - 2)(x + 2)$$
  $$\text{Denominator: } (x - 2)(x - 3)$$
  Thus:
  $$g(x) = \frac{3(x - 2)(x + 2)}{(x - 2)(x - 3)}$$
  - The common factor $(x - 2)$ cancels out, indicating a **removable discontinuity (hole)** at $x = 2$.
  - The non-canceling factor in the denominator $(x - 3)$ produces a **vertical asymptote** at $x = 3$.
- **Desmos Shortcut**:
  Graph `y = (3x^2 - 12)/(x^2 - 5x + 6)`. Click and drag along the curve to $x = 2$; Desmos displays `(2, undefined)` as a hollow circle, confirming a hole at $x = 2$.

---

### Question 5
- **Correct Answer: 18**
- **Method 1 (Direct Problem Definition & Algebraic Verification)**:
  The problem stem states that the bacterial population doubles every $18$ hours. In the standard exponential doubling formula $P(t) = P_0 \cdot 2^{\frac{t}{k}}$, the denominator $k$ represents the exact doubling period in hours. Hence $k = 18$.
- **Verification via Given Data Point**:
  After $t = 72$ hours, $P(72) = 7{,}200$:
  $$7200 = 450 \cdot 2^{\frac{72}{k}}$$
  $$\frac{7200}{450} = 16 = 2^4$$
  $$2^4 = 2^{\frac{72}{k}} \implies 4 = \frac{72}{k} \implies k = \frac{72}{4} = 18$$

---
## New System Alignment (Updated)
**Flow:** Teach → Show → Test
- **Teach:** Detailed strategy and rules (this file)
- **Show:** Walkthrough solving examples — [SAT/Show/show_walkthrough.html](../../Show/show_walkthrough.html)
- **Test:** Real SAT difficulty mock — [SAT/Test/mock_01.html](../../Test/mock_01.html)
- **Portal:** [SAT/index.html](../../index.html) (interactive pen / highlight / mark tools)
---
