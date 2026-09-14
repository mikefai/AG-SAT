---
domain: "SAT"
target_level: "Score 750 - 800"
topic: "Statistics, Probability, Data Distributions & Margin of Error"
date_created: "2026-09-01"
content_type: "Question Bank / Drill"
---

# 📐 Digital SAT Math: Statistics, Probability & Data Distributions

## 📋 Module Overview
- **Domain**: Problem-Solving and Data Analysis
- **Target Skills**: Mean, Median, Mode & Outlier Effects, Standard Deviation & Spread, Box-and-Whisker Plots & Interquartile Range (IQR), Margin of Error & Confidence Intervals, Conditional Probability
- **Calculator Policy**: Desmos Permitted
- **Number of Items**: 5 Items (4 Multiple Choice, 1 Student-Produced Response)
- **Time Recommended**: ~80 seconds per item

---

## ❓ Math Problems

### Question 1 (Multiple Choice: Margin of Error & Sample Size)
A polling organization surveyed a representative random sample of $1{,}200$ registered voters in a city regarding a proposed public transit bond. The survey found that $58\%$ of respondents supported the bond with a margin of error of $\pm 2.8\%$ at a $95\%$ confidence level. Which of the following modifications would result in a **smaller margin of error** while maintaining the same $95\%$ confidence level?

- **A)** Surveying a random sample of $2{,}400$ registered voters in the same city.
- **B)** Surveying a random sample of $600$ registered voters in the same city.
- **C)** Increasing the confidence level from $95\%$ to $99\%$ with the original $1{,}200$ sample.
- **D)** Surveying only voters who regularly commute using public transit.

---

### Question 2 (Multiple Choice: Outlier Impact on Mean vs Median)
A small software startup has 8 employees with the following annual salaries (in thousands of dollars):

$$\{65, 70, 72, 75, 80, 82, 85, 90\}$$

The company hires a new Chief Technology Officer (CTO) with an annual salary of $\$350{,}000$ ($350$ thousand dollars). How does adding this new salary affect the mean and median of the employee salary distribution?

- **A)** The mean increases significantly, while the median increases by a relatively small amount.
- **B)** The median increases significantly, while the mean remains unchanged.
- **C)** Both the mean and the median increase by exactly the same amount.
- **D)** Neither the mean nor the median changes because the sample size is under 30.

---

### Question 3 (Multiple Choice: Box Plots & Interquartile Range)
The box plots below summarize the distribution of test scores for two classes, Class A and Class B, each containing 30 students.

```
Class A:  |----[   |   ]----|
Score:   40   60  75  85   98

Class B:      |--[     |     ]--|
Score:        55 70   82    92  100
```

- **Class A**: Minimum = $40$, $Q_1 = 60$, Median = $75$, $Q_3 = 85$, Maximum = $98$
- **Class B**: Minimum = $55$, $Q_1 = 70$, Median = $82$, $Q_3 = 92$, Maximum = $100$

Which of the following statements must be true based on the data?

- **A)** The Interquartile Range (IQR) of Class A is greater than the IQR of Class B.
- **B)** The range of scores in Class B is greater than the range of scores in Class A.
- **C)** The IQR of Class A is $25$ and the IQR of Class B is $22$.
- **D)** At least $50\%$ of the students in Class A scored higher than the median score of Class B.

---

### Question 4 (Multiple Choice: Two-Way Relative Frequency & Conditional Probability)
A marine biology laboratory tested the effectiveness of two water purification filters against microplastic contamination in water samples.

| Filter Type | High Microplastic Retention (>95%) | Moderate Retention (75–95%) | Low Retention (<75%) | Total Samples |
| :--- | :---: | :---: | :---: | :---: |
| **Graphene Filter (G-1)** | 144 | 36 | 20 | **200** |
| **Cellulose Filter (C-2)** | 84 | 56 | 60 | **200** |
| **Total** | **228** | **92** | **80** | **400** |

Given that a randomly selected water sample had "High Microplastic Retention (>95%)", what is the probability that it was processed by the Graphene Filter (G-1)?

- **A)** $\frac{144}{200}$
- **B)** $\frac{144}{228}$
- **C)** $\frac{144}{400}$
- **D)** $\frac{228}{400}$

---

### Question 5 (Student-Produced Response: Standard Deviation & Variance)
A quality control inspector measures the diameter (in millimeters) of five precision ball bearings from Machine 1:

$$\{25.0, 25.0, 25.0, 25.0, 25.0\}$$

What is the sample standard deviation, in millimeters, of this measurement set?

---

## 🔑 Answer Key & Dual Solution Methods

| Question | Correct Answer | Topic / Concept | Difficulty Tier |
| :---: | :---: | :--- | :---: |
| **Q1** | **A (2,400 sample)** | Margin of Error & Sample Size Law | Medium-Hard |
| **Q2** | **A (Mean rises much more)** | Outlier Sensitivity: Mean vs. Median | Medium |
| **Q3** | **C ($\text{IQR}_A = 25, \text{IQR}_B = 22$)** | Box Plots & Interquartile Range (IQR) | Hard |
| **Q4** | **B ($\frac{144}{228}$)** | Two-Way Conditional Probability | Medium-Hard |
| **Q5** | **0** | Standard Deviation of Identical Dataset | Easy-Medium |

---

## 💡 In-Depth Solution Rationales

### Question 1
- **Correct Answer: A**:
  - The margin of error formula is $\text{MOE} = z^* \cdot \sqrt{\frac{p(1-p)}{n}}$. Because sample size $n$ is in the denominator under the square root, **increasing sample size** (e.g., from 1,200 to 2,400) decreases standard error and reduces the margin of error.
  - Choice C increases MOE; Choice B decreases sample size (increasing MOE); Choice D introduces selection bias.

### Question 2
- **Correct Answer: A**:
  - **Mean**: The extreme outlier of $\$350\text{k}$ dramatically pulls the arithmetic sum and mean upward (initial mean $= 76.75\text{k} \rightarrow$ new mean $= 107.1\text{k}$, an increase of over $\$30\text{k}$).
  - **Median**: The median shifts only from the average of the 4th and 5th numbers ($\frac{75+80}{2} = 77.5$) to the 5th number ($80$), an increase of just $\$2.5\text{k}$.
  - The median is *resistant* to extreme outliers, whereas the mean is *highly sensitive*.

### Question 3
- **Correct Answer: C**:
  - $\text{IQR}_A = Q_3 - Q_1 = 85 - 60 = 25$.
  - $\text{IQR}_B = Q_3 - Q_1 = 92 - 70 = 22$.
  - Thus, $\text{IQR}_A = 25$ and $\text{IQR}_B = 22$. Choice C is exactly correct (which also means $\text{IQR}_A > \text{IQR}_B$, but C provides the exact numerical proof).

### Question 4
- **Correct Answer: B ($\frac{144}{228} = \frac{12}{19} \approx 0.6316$)**:
  - Condition: "High Microplastic Retention (>95%)" restricts our denominator strictly to that column's total: $228$.
  - Numerator: Graphene Filter samples within that column: $144$.
  - Probability $= \frac{144}{228}$.

### Question 5
- **Correct Answer: 0**:
  - Standard deviation measures the dispersion or spread of data points around the arithmetic mean.
  - Because all 5 ball bearings have the identical diameter ($25.0\text{ mm}$), the mean is $25.0\text{ mm}$ and every deviation $(x_i - \bar{x}) = 0$.
  - The variance and sample standard deviation are strictly $0$.

---
## New System Alignment (Updated)
**Flow:** Teach → Show → Test
- **Teach:** Detailed strategy and rules (this file)
- **Show:** Walkthrough solving examples — [SAT/Show/show_walkthrough.html](../../Show/show_walkthrough.html)
- **Test:** Real SAT difficulty mock — [SAT/Test/mock_01.html](../../Test/mock_01.html)
- **Portal:** [SAT/index.html](../../index.html) (interactive pen / highlight / mark tools)
---
