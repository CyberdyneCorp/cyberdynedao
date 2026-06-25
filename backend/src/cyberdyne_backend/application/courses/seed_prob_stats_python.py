"""Probability & Statistics with Python track: Basics -> Intermediate -> Advanced.

A hands-on, code-first course track. Every lesson shows real, correct Python
using numpy, scipy (scipy.stats / scipy.optimize) and pandas inside ```python
fences, alongside interactive ```plot graphs and ```mermaid diagrams. All code
is illustrative (runnable in principle) — there is no code-runner lesson because
numpy/scipy/pandas are not available in the in-browser sandbox.
"""

# Lesson prose and code comments use typographic characters (×, →, ≈, σ, μ, …)
# and LaTeX — exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


# ── Probability & Statistics with Python — Basics ────────────────────────────

_PS_BASICS = SeedCourse(
    slug="prob-stats-python-basics",
    title="Probability & Statistics with Python — Basics",
    description=(
        "Get hands-on with data in Python: NumPy arrays and vectorised maths, "
        "descriptive statistics with NumPy and pandas, random sampling with the "
        "modern numpy.random.Generator, common distributions from scipy.stats, "
        "everyday data visualisation, and pandas DataFrames for tabular data — "
        "with interactive plots and diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "NumPy arrays for data",
            "10 min",
            r"""\
# NumPy arrays for data

Statistics in Python starts with **NumPy**. A NumPy array (`ndarray`) is a
fixed-type, contiguous block of numbers — far faster and more memory-efficient
than a Python list, and the foundation pandas and scipy are built on.

```python
import numpy as np

# Create arrays
a = np.array([4.1, 5.2, 3.8, 6.0, 4.7])   # from a list
zeros = np.zeros(5)                         # [0. 0. 0. 0. 0.]
grid = np.arange(0, 1, 0.25)               # [0.   0.25 0.5  0.75]
lin = np.linspace(0, 1, 5)                 # 5 evenly spaced points incl. ends

print(a.shape, a.dtype)                    # (5,) float64
```

**Indexing & slicing** look like lists but extend to *boolean masks* and
*fancy indexing* — the bread and butter of data filtering:

```python
a[0], a[-1]          # 4.1, 4.7  — first and last
a[1:3]               # array([5.2, 3.8])
mask = a > 4.5       # array([False,  True, False,  True,  True])
a[mask]              # array([5.2, 6. , 4.7]) — keep values above 4.5
a[[0, 2, 4]]         # fancy index: pick positions 0, 2, 4
```

**Vectorised operations** apply elementwise with no Python loop — this is why
NumPy is fast. The same code works on a 5-element array or a 5-million one:

```python
celsius = np.array([0.0, 20.0, 37.0, 100.0])
fahrenheit = celsius * 9 / 5 + 32          # array([ 32.,  68.,  98.6, 212.])
np.sqrt(a)                                 # elementwise square root
a + 1                                       # broadcasting a scalar over the array
```

A simple function plotted as data — the kind of relationship a vectorised
expression produces — looks like this:

```plot
{"title": "A vectorised transform: f(x) = sqrt(x)", "xLabel": "x", "yLabel": "f(x)", "xRange": [0, 9], "yRange": [0, 3.2], "functions": [{"expr": "sqrt(x)", "label": "sqrt(x)", "color": "#2563eb"}], "points": [{"x": 1, "y": 1, "color": "#dc2626", "size": 6}, {"x": 4, "y": 2, "color": "#dc2626", "size": 6}, {"x": 9, "y": 3, "label": "sqrt(9)=3", "color": "#dc2626", "size": 6}]}
```

The whole data-analysis workflow you will build in this course rests on arrays:

```mermaid
flowchart LR
    A[Raw data] --> B[NumPy array]
    B --> C[Vectorised ops & indexing]
    C --> D[Descriptive statistics]
    D --> E[Visualise & model]
```

**Next:** summarising an array with descriptive statistics.
""",
        ),
        _t(
            "Descriptive statistics with NumPy & pandas",
            "11 min",
            r"""\
# Descriptive statistics with NumPy & pandas

Once data is in an array, **summarise** it. The centre (mean, median) and the
spread (variance, standard deviation, quantiles) are the first numbers you
report.

```python
import numpy as np

x = np.array([4.1, 5.2, 3.8, 6.0, 4.7, 5.5, 4.9, 6.3, 5.1, 4.4])

x.mean()                 # 5.0   — arithmetic mean
np.median(x)             # 5.0   — middle value (robust to outliers)
x.std(ddof=1)            # sample standard deviation (ddof=1 → divide by n-1)
x.var(ddof=1)            # sample variance
np.percentile(x, [25, 50, 75])   # quartiles Q1, median, Q3
x.min(), x.max(), x.ptp()        # min, max, peak-to-peak range
```

> **ddof matters.** `np.var`/`np.std` default to `ddof=0` (population, divide by
> $n$). For a *sample* estimate, use `ddof=1` to divide by $n-1$. The formula is
> $s^2 = \frac{1}{n-1}\sum_i (x_i - \bar x)^2$.

**pandas** gives you the same statistics on labelled `Series`/`DataFrame`, plus
the one-call summary `describe()`:

```python
import pandas as pd

s = pd.Series(x, name="response_ms")
s.mean(), s.median(), s.std()    # std() uses ddof=1 by default in pandas
s.quantile([0.25, 0.5, 0.75])

df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [10, 20, 30, 40]})
df.describe()    # count, mean, std, min, 25%, 50%, 75%, max per column
```

For a Normal distribution the mean sits at the peak and about **68%** of the
data lies within one standard deviation, **95%** within two — drag the centre
$\mu$ and spread $\sigma$:

```plot
{"title": "Centre μ and spread σ summarised by a distribution", "xLabel": "x", "yLabel": "density", "xRange": [-6, 10], "yRange": [0, 0.85], "controls": [{"name": "mu", "range": [-2, 5], "value": 2, "label": "mean μ"}, {"name": "sg", "range": [0.5, 3], "value": 1.5, "label": "std dev σ"}], "functions": [{"expr": "exp(-(x-mu)^2/(2*sg^2))/(sg*sqrt(2*pi))", "label": "f(x)", "color": "#2563eb"}], "points": [{"xExpr": "mu", "y": 0, "label": "mean", "color": "#dc2626", "size": 7}, {"xExpr": "mu-sg", "y": 0, "color": "#16a34a", "size": 5}, {"xExpr": "mu+sg", "y": 0, "label": "±σ (68%)", "color": "#16a34a", "size": 5}]}
```

Mean vs median tells you about skew; the IQR ($Q_3 - Q_1$) and standard deviation
quantify spread. Always look at both centre and spread before going further.

**Next:** generating random data to experiment with.
""",
        ),
        _t(
            "Probability foundations & random sampling",
            "11 min",
            r"""\
# Probability foundations & random sampling

A **probability** is a number in $[0, 1]$ describing how likely an event is.
Over many independent trials, the observed frequency of an event converges to
its probability — the **law of large numbers**. We simulate this in Python with
**`numpy.random`**.

Modern NumPy uses an explicit **`Generator`** seeded for reproducibility — prefer
it over the legacy `np.random.seed` / `np.random.rand` functions:

```python
import numpy as np

rng = np.random.default_rng(seed=2024)   # reproducible Generator

rng.random(3)                # 3 floats uniform in [0, 1)
rng.integers(1, 7, size=10)  # 10 dice rolls in 1..6
rng.normal(loc=0, scale=1, size=5)       # 5 standard-Normal draws
rng.choice(["A", "B", "C"], size=4)      # sample categories (with replacement)
rng.choice(20, size=5, replace=False)    # sample 5 distinct positions
```

**Law of large numbers in code** — a fair coin's running proportion of heads
settles toward 0.5 as we flip more:

```python
rng = np.random.default_rng(0)
flips = rng.integers(0, 2, size=10_000)      # 0 = tails, 1 = heads
running_mean = np.cumsum(flips) / np.arange(1, flips.size + 1)
running_mean[-1]    # ≈ 0.5 once n is large
```

The running proportion wobbles a lot early on, then converges to the true
probability $p = 0.5$:

```plot
{"title": "Law of large numbers: 1/sqrt(n) envelope shrinks toward p = 0.5", "xLabel": "number of flips n", "yLabel": "proportion of heads", "xRange": [1, 200], "yRange": [0, 1], "functions": [{"expr": "0.5", "label": "true p = 0.5", "color": "#dc2626"}, {"expr": "0.5 + 1/sqrt(x)", "label": "0.5 + 1/sqrt(n)", "color": "#94a3b8"}, {"expr": "0.5 - 1/sqrt(x)", "label": "0.5 - 1/sqrt(n)", "color": "#94a3b8"}]}
```

> **Reproducibility rule.** Seed once per experiment with
> `np.random.default_rng(seed)` and reuse that `rng`. Same seed → same numbers,
> which is essential for debuggable, shareable analysis.

**Next:** the named distributions those samples come from.
""",
        ),
        _t(
            "Common distributions with scipy.stats",
            "11 min",
            r"""\
# Common distributions with scipy.stats

Most data is modelled with a handful of named **distributions**. `scipy.stats`
gives each one the same interface: `pmf`/`pdf` (probability), `cdf` (cumulative),
`ppf` (quantile/inverse-cdf), `rvs` (random draws), plus `mean`, `var`.

**Discrete** distributions use `pmf` (probability *mass*):

```python
from scipy import stats

# Binomial: number of successes in n=10 trials, success prob p=0.3
binom = stats.binom(n=10, p=0.3)
binom.pmf(3)        # P(exactly 3 successes)
binom.cdf(3)        # P(at most 3 successes)
binom.mean()        # n*p = 3.0
binom.rvs(size=5, random_state=0)   # 5 random counts

# Poisson: count of events with average rate lam=4
pois = stats.poisson(mu=4)
pois.pmf(2)         # P(exactly 2 events)
```

**Continuous** distributions use `pdf` (probability *density*):

```python
from scipy import stats

# Uniform on [0, 1] (loc=0, scale=1)
unif = stats.uniform(loc=0, scale=1)
unif.pdf(0.5)       # 1.0 — flat density

# Normal with mean 3, std 1
norm = stats.norm(loc=3, scale=1)
norm.pdf(3)         # density at the peak ≈ 0.399
norm.cdf(3)         # 0.5 — half the mass below the mean
norm.ppf(0.975)     # ≈ 1.96*scale + loc — the 97.5% quantile
norm.rvs(size=4, random_state=1)
```

Here is that Normal PDF, $f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/2\sigma^2}$,
with $\mu = 3,\ \sigma = 1$:

```plot
{"title": "Normal PDF from scipy.stats.norm(loc=3, scale=1)", "xLabel": "value", "yLabel": "density", "xRange": [-2, 8], "yRange": [0, 0.45], "functions": [{"expr": "exp(-(x-3)^2/2)/sqrt(2*pi)", "label": "Normal(3, 1)", "color": "#2563eb"}], "points": [{"x": 3, "y": 0, "label": "mean μ = 3", "color": "#dc2626", "size": 7}]}
```

The distribution families fall into a small map you will reuse constantly:

```mermaid
flowchart TD
    R[Random quantity] --> D{Discrete or continuous?}
    D -->|Discrete| DC{What kind?}
    DC -->|Yes/no count in n trials| BIN[Binomial]
    DC -->|Count of rare events| POIS[Poisson]
    D -->|Continuous| CC{Shape?}
    CC -->|Flat on an interval| UNI[Uniform]
    CC -->|Bell-shaped| NORM[Normal]
    CC -->|Time between events| EXP[Exponential]
```

**Next:** turning data into pictures.
""",
        ),
        _t(
            "Visualising data: histograms, box plots & scatter",
            "10 min",
            r"""\
# Visualising data: histograms, box plots & scatter

Numbers summarise; **pictures reveal**. Three plots cover most exploratory needs.

**Histogram** — the shape of one variable's distribution. `np.histogram` gives
you the raw counts; `matplotlib` draws them:

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)
data = rng.normal(loc=50, scale=8, size=1000)

counts, edges = np.histogram(data, bins=20)   # counts per bin, bin edges
plt.hist(data, bins=20, density=True)         # density=True → area sums to 1
plt.xlabel("value"); plt.ylabel("density")
```

**Box plot** — centre, spread and outliers at a glance (median line, the IQR
box from $Q_1$ to $Q_3$, whiskers, and outlier points):

```python
groups = [rng.normal(50, 8, 200), rng.normal(55, 12, 200)]
plt.boxplot(groups, labels=["A", "B"])
```

**Scatter** — the relationship between two variables:

```python
x = rng.uniform(0, 10, 100)
y = 2 * x + rng.normal(0, 2, 100)     # linear trend plus noise
plt.scatter(x, y, alpha=0.6)
plt.xlabel("x"); plt.ylabel("y")
```

A histogram of Normal data traces out the bell curve as the sample grows large —
the smooth density it approximates:

```plot
{"title": "Histogram of Normal data approaches its density", "xLabel": "value", "yLabel": "density", "xRange": [26, 74], "yRange": [0, 0.055], "functions": [{"expr": "exp(-(x-50)^2/(2*64))/(8*sqrt(2*pi))", "label": "Normal(50, 8) density", "color": "#2563eb"}], "points": [{"x": 50, "y": 0, "label": "mean = 50", "color": "#dc2626", "size": 7}, {"x": 42, "y": 0, "color": "#16a34a", "size": 5}, {"x": 58, "y": 0, "label": "±σ", "color": "#16a34a", "size": 5}]}
```

Choosing the right chart is a quick decision:

```mermaid
flowchart TD
    Q{What do you want to see?} -->|Distribution of one variable| H[Histogram]
    Q -->|Compare groups / spot outliers| B[Box plot]
    Q -->|Relationship between two variables| S[Scatter plot]
    Q -->|Trend over an ordered axis| L[Line plot]
```

**Next:** organising data into tables with pandas.
""",
        ),
        _t(
            "pandas DataFrames & Series for tabular data",
            "11 min",
            r"""\
# pandas DataFrames & Series for tabular data

Real data is **tabular**: rows of observations, columns of variables. **pandas**
gives you the `Series` (one labelled column) and the `DataFrame` (a whole table).

```python
import pandas as pd

# Build a DataFrame from a dict of columns
df = pd.DataFrame({
    "city": ["Rio", "Rio", "SP", "SP", "Rio"],
    "temp": [31.0, 28.5, 22.0, 24.5, 30.0],
    "humidity": [70, 65, 55, 60, 72],
})

# Or read from a file (CSV is the workhorse):
# df = pd.read_csv("weather.csv")

df.head()        # first rows
df.shape         # (5, 3) — rows, columns
df.dtypes        # type of each column
df.info()        # non-null counts and types
```

**Selecting** columns and rows:

```python
df["temp"]                 # a Series (one column)
df[["city", "temp"]]       # a DataFrame (several columns)
df.loc[0]                  # row by label
df.iloc[0:2]               # rows by integer position
```

**Filtering** with a boolean mask — the tabular version of NumPy masking:

```python
hot = df[df["temp"] > 29]          # rows where temp exceeds 29
df[(df["city"] == "Rio") & (df["humidity"] > 68)]   # combine conditions with &, |
```

**Group-by** — split the rows into groups, apply a statistic, combine the
results (the split-apply-combine pattern you will use everywhere):

```python
df.groupby("city")["temp"].mean()      # mean temperature per city
df.groupby("city").agg(
    avg_temp=("temp", "mean"),
    max_hum=("humidity", "max"),
)
```

A scatter of two numeric columns shows the kind of relationship a DataFrame
holds — here temperature vs humidity with a rising trend:

```plot
{"title": "Two DataFrame columns: temperature vs humidity", "xLabel": "temp", "yLabel": "humidity", "xRange": [20, 34], "yRange": [50, 78], "functions": [{"expr": "2.2*x", "label": "rough trend", "color": "#94a3b8"}], "points": [{"x": 31, "y": 70, "color": "#2563eb", "size": 6}, {"x": 28.5, "y": 65, "color": "#2563eb", "size": 6}, {"x": 22, "y": 55, "color": "#2563eb", "size": 6}, {"x": 24.5, "y": 60, "color": "#2563eb", "size": 6}, {"x": 30, "y": 72, "label": "Rio", "color": "#dc2626", "size": 6}]}
```

The pandas workflow you have now seen end to end:

```mermaid
flowchart LR
    A[read_csv / DataFrame] --> B[Inspect: head, info, describe]
    B --> C[Select & filter rows/columns]
    C --> D[groupby + agg]
    D --> E[Summary statistics & plots]
```

**Next:** test what you've learned.
""",
        ),
    ),
)

# ── Probability & Statistics with Python — Intermediate ──────────────────────

_PS_INTERMEDIATE = SeedCourse(
    slug="prob-stats-python-intermediate",
    title="Probability & Statistics with Python — Intermediate",
    description=(
        "Put statistics to work in Python: the Central Limit Theorem by "
        "simulation, confidence intervals with numpy/scipy, hypothesis testing "
        "with scipy.stats (t-tests and chi-square), correlation and covariance, "
        "simple linear regression, and real-world data wrangling with pandas — "
        "with interactive plots and decision diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The Central Limit Theorem by simulation",
            "11 min",
            r"""\
# The Central Limit Theorem by simulation

The **Central Limit Theorem (CLT)** is why the Normal distribution is
everywhere: the **mean of many independent samples** is approximately Normal,
*no matter the shape of the original distribution*. We can watch this happen.

Take a heavily skewed source — say an Exponential distribution — and repeatedly
average $n$ draws. As $n$ grows, the distribution of those sample means turns
into a bell curve, centred on the true mean, with standard error
$\sigma/\sqrt{n}$:

```python
import numpy as np

rng = np.random.default_rng(2024)

n = 30            # samples per mean
reps = 20_000     # how many means to simulate

# Source is Exponential(scale=2): mean = 2, std = 2 — strongly right-skewed.
draws = rng.exponential(scale=2.0, size=(reps, n))
sample_means = draws.mean(axis=1)        # one mean per row → 20,000 means

print(sample_means.mean())               # ≈ 2.0 (the true mean)
print(sample_means.std(ddof=1))          # ≈ 2 / sqrt(30) ≈ 0.365 (the SE)
```

The standard error shrinks only as $\sqrt{n}$: to halve the spread of the sample
mean you need **four times** the data. Increase $n$ and watch the sampling
distribution of $\bar x$ concentrate on the truth:

```plot
{"title": "CLT: sampling distribution of x̄ becomes Normal and tightens as n grows", "xLabel": "sample mean x̄", "yLabel": "density", "xRange": [0, 4], "yRange": [0, 3], "controls": [{"name": "n", "range": [1, 50], "value": 5, "step": 1, "label": "samples per mean n"}], "functions": [{"expr": "exp(-(x-2)^2/(2*4/n))/sqrt(2*pi*4/n)", "label": "distribution of x̄", "color": "#2563eb"}], "points": [{"x": 2, "y": 0, "label": "true mean μ = 2", "color": "#dc2626", "size": 7}]}
```

> **Why it matters.** The CLT justifies using Normal-based confidence intervals
> and t-tests even when the raw data is not Normal — as long as $n$ is large
> enough. It is the engine under the next several lessons.

The simulation recipe is short:

```mermaid
flowchart LR
    A[Pick any source distribution] --> B[Draw n values, take the mean]
    B --> C[Repeat many times]
    C --> D[Histogram of means is approximately Normal]
    D --> E[Centred on μ, std = σ/√n]
```

**Next:** turning the standard error into a confidence interval.
""",
        ),
        _t(
            "Confidence intervals with numpy & scipy",
            "11 min",
            r"""\
# Confidence intervals with numpy & scipy

A point estimate ($\bar x = 5.0$) needs a **margin of error**. A confidence
interval is $\bar x \pm z^* \cdot \mathrm{SE}$, where $\mathrm{SE} = s/\sqrt{n}$
and $z^*$ is the Normal critical value (1.96 for 95%).

**By hand with numpy + scipy:**

```python
import numpy as np
from scipy import stats

x = np.array([4.1, 5.2, 3.8, 6.0, 4.7, 5.5, 4.9, 6.3, 5.1, 4.4])
n = x.size
mean = x.mean()
se = x.std(ddof=1) / np.sqrt(n)          # standard error of the mean

z = stats.norm.ppf(0.975)                # 1.959... — the 95% z critical value
ci_z = (mean - z * se, mean + z * se)    # large-sample (Normal) interval
```

**For small samples**, use the **t-distribution** (heavier tails) with $n-1$
degrees of freedom — or let scipy build the whole interval:

```python
tcrit = stats.t.ppf(0.975, df=n - 1)             # t critical value
ci_t = (mean - tcrit * se, mean + tcrit * se)

# One-call equivalent:
ci = stats.t.interval(0.95, df=n - 1, loc=mean, scale=se)
print(mean, ci)                                   # estimate and its 95% CI
```

The interval edges are $\bar x \pm 1.96\,\mathrm{SE}$ — increase $n$ and watch
them close in around the mean:

```plot
{"title": "95% confidence interval narrows with sample size", "xLabel": "x̄", "yLabel": "density", "xRange": [3, 7], "yRange": [0, 4], "controls": [{"name": "n", "range": [4, 80], "value": 10, "step": 1, "label": "sample size n"}], "functions": [{"expr": "exp(-(x-5)^2/(2*1/n))/sqrt(2*pi*1/n)", "label": "sampling distribution of x̄", "color": "#2563eb"}], "points": [{"xExpr": "5 - 1.96/sqrt(n)", "y": 0, "label": "lower 95%", "color": "#dc2626", "size": 7}, {"xExpr": "5 + 1.96/sqrt(n)", "y": 0, "label": "upper 95%", "color": "#dc2626", "size": 7}]}
```

> **Interpretation.** A 95% CI means: if you repeated the experiment many times,
> about 95% of the intervals you build would contain the true mean. It is *not*
> "95% probability the true mean is in this particular interval".

**Next:** deciding whether an effect is real — hypothesis testing.
""",
        ),
        _t(
            "Hypothesis testing with scipy.stats",
            "12 min",
            r"""\
# Hypothesis testing with scipy.stats

A **hypothesis test** asks whether the data is surprising under a default
assumption $H_0$. We compute a **test statistic** and its **p-value** — the
probability of a result at least this extreme if $H_0$ were true. Small p-value
($< \alpha$, typically 0.05) → reject $H_0$.

**One-sample t-test** — is the mean different from a target $\mu_0$?

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(0)
x = rng.normal(loc=5.3, scale=1.0, size=40)

t_stat, p = stats.ttest_1samp(x, popmean=5.0)   # H0: mean == 5.0
print(t_stat, p)                                 # reject H0 if p < 0.05
```

**Two-sample t-test** — do two groups have different means?

```python
a = rng.normal(50, 8, size=120)
b = rng.normal(54, 8, size=120)

# Welch's t-test does not assume equal variances (the safer default):
t_stat, p = stats.ttest_ind(a, b, equal_var=False)
print(p)                                          # p < 0.05 → means differ
```

**Chi-square test** — are two categorical variables independent?

```python
# Contingency table: rows = group, columns = outcome (clicked / not)
table = np.array([[30, 70],
                  [45, 55]])
chi2, p, dof, expected = stats.chi2_contingency(table)
print(chi2, p)                                    # p < 0.05 → not independent
```

Under $H_0$ the statistic follows a known null distribution; the p-value is the
tail area beyond the observed value. Slide the observed statistic into the tail
and watch the p-value shrink:

```plot
{"title": "Null distribution; the p-value is the tail beyond the statistic", "xLabel": "test statistic", "yLabel": "density", "xRange": [-4, 4], "yRange": [0, 0.45], "controls": [{"name": "z0", "range": [0, 3.5], "value": 1, "label": "observed statistic"}], "functions": [{"expr": "exp(-x^2/2)/sqrt(2*pi)", "label": "H₀ distribution", "color": "#2563eb"}], "points": [{"xExpr": "z0", "yExpr": "exp(-z0^2/2)/sqrt(2*pi)", "label": "observed", "color": "#dc2626", "size": 7}, {"x": 1.96, "y": 0, "label": "5% cutoff", "color": "#16a34a", "size": 6}]}
```

Pick the test from the data type:

```mermaid
flowchart TD
    Q{What are you comparing?} -->|One mean vs a target| T1[ttest_1samp]
    Q -->|Two group means| T2[ttest_ind]
    Q -->|Paired before/after| TP[ttest_rel]
    Q -->|Counts in categories| CHI[chi2_contingency]
```

> ⚠️ A p-value is **not** the probability $H_0$ is true, and "not significant"
> is not "no effect". Beware p-hacking and multiple comparisons.

**Next:** measuring how two variables move together.
""",
        ),
        _t(
            "Correlation & covariance",
            "10 min",
            r"""\
# Correlation & covariance

**Covariance** measures whether two variables move together: positive when they
rise together, negative when one rises as the other falls. Its scale depends on
the units, so we usually standardise it into the **correlation coefficient**
$r \in [-1, 1]$:

$$r = \frac{\operatorname{cov}(x, y)}{s_x\, s_y}.$$

```python
import numpy as np

rng = np.random.default_rng(0)
x = rng.uniform(0, 10, 200)
y = 2 * x + rng.normal(0, 3, 200)        # strong positive linear relation

# Covariance matrix (diagonal = variances, off-diagonal = covariance)
cov = np.cov(x, y)                        # shape (2, 2)

# Pearson correlation matrix (diagonal = 1)
corr = np.corrcoef(x, y)
r = corr[0, 1]                            # the correlation between x and y
print(round(r, 3))                        # ≈ 0.9
```

**With pandas**, `.corr()` builds the whole correlation matrix across columns —
ideal for spotting related features in a table:

```python
import pandas as pd

df = pd.DataFrame({"x": x, "y": y, "noise": rng.normal(0, 1, 200)})
df.corr()                # 3×3 matrix; x–y ≈ 0.9, anything with noise ≈ 0
df["x"].corr(df["y"])    # single pairwise correlation
```

> **Correlation ≠ causation,** and $r$ only captures *linear* association. A
> perfect parabola can have $r \approx 0$. Always look at the scatter plot.

A strong positive correlation looks like points hugging a rising line:

```plot
{"title": "Strong positive correlation (r ≈ 0.9)", "xLabel": "x", "yLabel": "y", "xRange": [0, 10], "yRange": [0, 22], "functions": [{"expr": "2*x", "label": "trend y ≈ 2x", "color": "#94a3b8"}], "points": [{"x": 1, "y": 2.5, "color": "#2563eb", "size": 6}, {"x": 2.5, "y": 4.0, "color": "#2563eb", "size": 6}, {"x": 4, "y": 8.5, "color": "#2563eb", "size": 6}, {"x": 5.5, "y": 10.5, "color": "#2563eb", "size": 6}, {"x": 7, "y": 15.0, "color": "#2563eb", "size": 6}, {"x": 8.5, "y": 16.5, "color": "#2563eb", "size": 6}, {"x": 9.5, "y": 20.0, "label": "data", "color": "#dc2626", "size": 6}]}
```

The correlation strength scale:

```mermaid
flowchart LR
    N["r ≈ -1: strong negative"] --> Z["r ≈ 0: no linear relation"]
    Z --> P["r ≈ +1: strong positive"]
```

**Next:** turning correlation into a predictive line — regression.
""",
        ),
        _t(
            "Simple linear regression",
            "11 min",
            r"""\
# Simple linear regression

**Linear regression** fits the best straight line $y = \beta_0 + \beta_1 x$
through a cloud of points by **least squares** — minimising the sum of squared
vertical residuals. scipy gives you the slope, intercept, and inference all at
once:

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(0)
x = rng.uniform(0, 10, 80)
y = 1.0 + 0.8 * x + rng.normal(0, 1.5, 80)       # true slope 0.8, intercept 1.0

res = stats.linregress(x, y)
res.slope, res.intercept      # estimated β₁, β₀
res.rvalue ** 2               # R² — fraction of variance explained
res.pvalue                    # p-value for H0: slope == 0
res.stderr                    # standard error of the slope

# Predict at new points:
y_hat = res.intercept + res.slope * x
```

`numpy.polyfit` gives the same coefficients (handy for higher-degree fits too):

```python
beta1, beta0 = np.polyfit(x, y, deg=1)   # returns [slope, intercept]
poly = np.poly1d([beta1, beta0])         # callable: poly(x) → predictions
```

> **Read the diagnostics.** A small slope p-value means the relationship is
> unlikely to be chance; $R^2$ near 1 means the line explains most of the
> variation. Always plot the **residuals** — they should look like
> structureless noise.

Adjust the intercept $\beta_0$ and slope $\beta_1$ to fit the line over the data:

```plot
{"title": "Least-squares fit: y = β₀ + β₁x over scatter points", "xLabel": "x", "yLabel": "y", "xRange": [-0.5, 10.5], "yRange": [0, 12], "controls": [{"name": "b0", "range": [-2, 4], "value": 1, "label": "intercept β₀"}, {"name": "b1", "range": [0, 1.5], "value": 0.8, "label": "slope β₁"}], "functions": [{"expr": "b0 + b1*x", "label": "fitted line", "color": "#dc2626"}], "points": [{"x": 1, "y": 1.9, "color": "#2563eb", "size": 6}, {"x": 2.5, "y": 3.2, "color": "#2563eb", "size": 6}, {"x": 4, "y": 4.1, "color": "#2563eb", "size": 6}, {"x": 5.5, "y": 5.6, "color": "#2563eb", "size": 6}, {"x": 7, "y": 6.4, "color": "#2563eb", "size": 6}, {"x": 8.5, "y": 8.0, "color": "#2563eb", "size": 6}, {"x": 10, "y": 8.9, "label": "data", "color": "#2563eb", "size": 6}]}
```

**Next:** wrangling messy real-world tables with pandas.
""",
        ),
        _t(
            "Real-world data wrangling with pandas",
            "12 min",
            r"""\
# Real-world data wrangling with pandas

Real datasets are messy: missing values, mixed groups, the wrong shape. pandas
turns wrangling into a few composable operations.

**Missing data** — detect, drop, or fill:

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "city": ["Rio", "Rio", "SP", "SP", "BH"],
    "sales": [100.0, np.nan, 80.0, 95.0, np.nan],
    "region": ["SE", "SE", "SE", "SE", "SE"],
})

df.isna().sum()                       # count missing per column
df.dropna(subset=["sales"])           # drop rows missing sales
df["sales"].fillna(df["sales"].mean())   # impute with the column mean
```

**Group-by + aggregation** — split-apply-combine, the heart of analysis:

```python
df.groupby("city")["sales"].agg(["mean", "sum", "count"])

# Several columns, named outputs:
df.groupby("region").agg(
    total_sales=("sales", "sum"),
    avg_sales=("sales", "mean"),
    n_cities=("city", "nunique"),
)
```

**Pivot tables** — reshape long data into a grid of one statistic:

```python
trips = pd.DataFrame({
    "city": ["Rio", "Rio", "SP", "SP"],
    "quarter": ["Q1", "Q2", "Q1", "Q2"],
    "revenue": [120, 150, 200, 180],
})
pivot = trips.pivot_table(
    values="revenue", index="city", columns="quarter", aggfunc="sum"
)
# city  Q1   Q2
# Rio  120  150
# SP   200  180
```

**Combining tables** with a join:

```python
prices = pd.DataFrame({"city": ["Rio", "SP"], "cost": [40, 55]})
merged = trips.merge(prices, on="city", how="left")   # add cost to each row
```

A pivot of per-quarter revenue per city makes the trend obvious at a glance:

```plot
{"title": "Quarterly revenue by city (pivoted)", "xLabel": "quarter (Q1=1, Q2=2)", "yLabel": "revenue", "xRange": [0.5, 2.5], "yRange": [0, 240], "points": [{"x": 1, "y": 120, "label": "Rio Q1", "color": "#2563eb", "size": 7}, {"x": 2, "y": 150, "label": "Rio Q2", "color": "#2563eb", "size": 7}, {"x": 1, "y": 200, "label": "SP Q1", "color": "#dc2626", "size": 7}, {"x": 2, "y": 180, "label": "SP Q2", "color": "#dc2626", "size": 7}]}
```

The full wrangling pipeline:

```mermaid
flowchart LR
    A[read_csv] --> B[Clean: dropna / fillna]
    B --> C[Filter & transform]
    C --> D[groupby + agg]
    D --> E[pivot_table / merge]
    E --> F[Analyse & visualise]
```

**Next:** test what you've learned.
""",
        ),
    ),
)

# ── Probability & Statistics with Python — Advanced ──────────────────────────

_PS_ADVANCED = SeedCourse(
    slug="prob-stats-python-advanced",
    title="Probability & Statistics with Python — Advanced",
    description=(
        "The modern statistical toolkit in Python: Bayesian inference with a "
        "conjugate Beta-Binomial model, the bootstrap and resampling, Monte "
        "Carlo simulation, multivariate statistics and PCA, maximum likelihood "
        "with scipy.optimize, and a complete end-to-end analysis combining "
        "pandas and scipy.stats — with interactive plots and diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Bayesian inference basics",
            "12 min",
            r"""\
# Bayesian inference basics

**Bayesian inference** keeps a whole *distribution* of belief and updates it
with data via Bayes' rule:

$$\underbrace{P(\theta\mid \text{data})}_{\text{posterior}} \;\propto\;
\underbrace{P(\text{data}\mid\theta)}_{\text{likelihood}}\;
\underbrace{P(\theta)}_{\text{prior}}.$$

For estimating a probability $p$ (a coin's bias, a conversion rate) the
**Beta** distribution is *conjugate* to the **Binomial** likelihood: a
$\text{Beta}(\alpha, \beta)$ prior, after observing $h$ successes and $t$
failures, becomes a $\text{Beta}(\alpha + h,\ \beta + t)$ posterior — no
integration needed.

```python
import numpy as np
from scipy import stats

# Prior belief about a conversion rate: Beta(2, 2) — symmetric, mild.
alpha0, beta0 = 2, 2

# Observed data: 14 conversions out of 20 visitors.
heads, tails = 14, 6

# Conjugate update — the posterior is just Beta with bumped parameters.
alpha_post = alpha0 + heads
beta_post = beta0 + tails
post = stats.beta(alpha_post, beta_post)

post.mean()                         # posterior mean estimate of p
post.ppf([0.025, 0.975])            # 95% credible interval for p
post.pdf(np.linspace(0, 1, 5))      # posterior density at a few points
```

The prior is broad; the posterior is sharper and shifted toward the data. Adjust
the observed successes $h$ and failures $t$ and watch the posterior concentrate:

```plot
{"title": "Bayesian updating: Beta prior → posterior over a rate p", "xLabel": "p", "yLabel": "belief density", "xRange": [0, 1], "yRange": [0, 5], "controls": [{"name": "h", "range": [0, 30], "value": 14, "step": 1, "label": "successes h"}, {"name": "t", "range": [0, 30], "value": 6, "step": 1, "label": "failures t"}], "functions": [{"expr": "x^(2-1)*(1-x)^(2-1)", "label": "prior Beta(2,2)", "color": "#94a3b8"}, {"expr": "x^(2+h-1)*(1-x)^(2+t-1)", "label": "posterior (unnormalised)", "color": "#2563eb"}]}
```

> A **credible interval** ("95% probability the rate is in here") is the answer
> people actually want — unlike a frequentist confidence interval. Bayesian
> methods shine with small data and real prior knowledge.

```mermaid
flowchart LR
    P[Prior Beta α, β] --> U[Observe h successes, t failures]
    U --> Q[Posterior Beta α+h, β+t]
    Q --> R[Mean estimate & credible interval]
```

**Next:** when there is no neat formula — the bootstrap.
""",
        ),
        _t(
            "Bootstrap & resampling",
            "11 min",
            r"""\
# Bootstrap & resampling

When a closed-form standard error is hard (the median, a correlation, a ratio),
the **bootstrap** estimates uncertainty by **resampling the data itself**: draw
many samples *with replacement* from your sample, recompute the statistic each
time, and read the spread of those values.

```python
import numpy as np

rng = np.random.default_rng(2024)
data = np.array([4.1, 5.2, 3.8, 6.0, 4.7, 5.5, 4.9, 6.3, 5.1, 4.4])
n = data.size

B = 10_000
# Each row is one bootstrap resample (with replacement), shape (B, n).
idx = rng.integers(0, n, size=(B, n))
resamples = data[idx]

boot_means = resamples.mean(axis=1)     # the statistic on each resample
se = boot_means.std(ddof=1)             # bootstrap standard error
print(round(se, 4))
```

The **percentile confidence interval** is just the empirical quantiles of the
bootstrap distribution — and it works for *any* statistic, not only the mean:

```python
ci = np.percentile(boot_means, [2.5, 97.5])   # 95% bootstrap CI
print(ci)

# Same recipe for the median — no formula exists, but the bootstrap still works:
boot_medians = np.median(resamples, axis=1)
np.percentile(boot_medians, [2.5, 97.5])
```

The bootstrap distribution of the mean is approximately Normal, centred on the
sample mean, with spread equal to the standard error:

```plot
{"title": "Bootstrap distribution of the mean (≈ Normal, SE-wide)", "xLabel": "bootstrap mean", "yLabel": "density", "xRange": [4.2, 5.8], "yRange": [0, 3], "functions": [{"expr": "exp(-(x-5)^2/(2*0.04))/sqrt(2*pi*0.04)", "label": "bootstrap means", "color": "#2563eb"}], "points": [{"x": 5, "y": 0, "label": "sample mean", "color": "#dc2626", "size": 7}, {"x": 4.6, "y": 0, "color": "#16a34a", "size": 5}, {"x": 5.4, "y": 0, "label": "≈ 95% CI edges", "color": "#16a34a", "size": 5}]}
```

```mermaid
flowchart LR
    A[Original sample] --> B[Resample with replacement]
    B --> C[Recompute statistic]
    C --> D[Repeat B times]
    D --> E[Spread = SE; percentiles = CI]
```

> The bootstrap is astonishingly general: no distributional assumption, just
> resampling. Use it whenever the formula is missing or doubtful.

**Next:** estimating quantities by random simulation — Monte Carlo.
""",
        ),
        _t(
            "Monte Carlo methods",
            "11 min",
            r"""\
# Monte Carlo methods

**Monte Carlo** methods answer hard questions by **simulating randomness** and
averaging. If you can sample it, you can estimate it.

**Estimate $\pi$** by throwing random darts at a unit square and counting how
many land inside the quarter circle (area $\pi/4$):

```python
import numpy as np

rng = np.random.default_rng(0)
N = 1_000_000
x = rng.random(N)
y = rng.random(N)
inside = (x**2 + y**2) <= 1.0          # boolean mask
pi_est = 4 * inside.mean()             # fraction inside × 4
print(pi_est)                          # ≈ 3.1416
```

**Estimate an integral** $\int_0^1 e^{-x^2}\,dx$ as the average of the
integrand at random points (the law of large numbers in action):

```python
u = rng.random(500_000)
integral = np.exp(-u**2).mean()        # ≈ 0.7468
```

**Estimate risk / a tail probability** — e.g. the chance a portfolio loses more
than a threshold, by simulating many scenarios:

```python
returns = rng.normal(loc=0.01, scale=0.05, size=200_000)   # daily returns
prob_loss = (returns < -0.05).mean()   # P(loss worse than 5%)
value_at_risk = np.percentile(returns, 5)   # 5% Value-at-Risk
```

Monte Carlo error falls as $1/\sqrt{N}$ — like every sample estimate, four times
the simulations halves the error:

```plot
{"title": "Monte Carlo error shrinks like 1/√N", "xLabel": "simulations N", "yLabel": "estimation error", "xRange": [1, 1000], "yRange": [0, 1.1], "functions": [{"expr": "1/sqrt(x)", "label": "error ∝ 1/√N", "color": "#2563eb"}], "points": [{"x": 100, "y": 0.1, "label": "N=100 → 0.10", "color": "#dc2626", "size": 6}, {"x": 400, "y": 0.05, "label": "N=400 → 0.05", "color": "#16a34a", "size": 6}]}
```

```mermaid
flowchart LR
    A[Define a random model] --> B[Sample N scenarios]
    B --> C[Compute the quantity per scenario]
    C --> D[Average → estimate]
    D --> E[Error ∝ 1/√N]
```

**Next:** statistics in many dimensions at once.
""",
        ),
        _t(
            "Multivariate statistics & PCA",
            "12 min",
            r"""\
# Multivariate statistics & PCA

With several variables, the **covariance matrix** $\Sigma$ captures every
pairwise relationship: variances on the diagonal, covariances off it.

```python
import numpy as np

rng = np.random.default_rng(0)
# Three correlated features stacked as columns of an (n, 3) matrix.
X = rng.multivariate_normal(
    mean=[0, 0, 0],
    cov=[[3, 2, 0.5],
         [2, 2, 0.3],
         [0.5, 0.3, 1]],
    size=500,
)

# np.cov expects variables in ROWS, so transpose:
Sigma = np.cov(X, rowvar=False)        # 3×3 sample covariance matrix
corr = np.corrcoef(X, rowvar=False)    # 3×3 correlation matrix
```

**Principal Component Analysis (PCA)** finds the directions of greatest variance
by **eigen-decomposing** the covariance matrix. The eigenvectors are the
principal axes; the eigenvalues are the variance along each:

```python
# 1. Centre the data (PCA needs zero-mean columns).
Xc = X - X.mean(axis=0)

# 2. Covariance, then eigen-decomposition (eigh: symmetric matrices).
cov = np.cov(Xc, rowvar=False)
eigvals, eigvecs = np.linalg.eigh(cov)        # ascending eigenvalues

# 3. Sort descending → principal components first.
order = np.argsort(eigvals)[::-1]
eigvals, eigvecs = eigvals[order], eigvecs[:, order]

# 4. Variance explained by each component.
explained = eigvals / eigvals.sum()
print(np.round(explained, 3))                 # e.g. [0.78 0.16 0.06]

# 5. Project onto the top 2 components (dimensionality reduction).
scores = Xc @ eigvecs[:, :2]                  # shape (500, 2)
```

The cumulative variance explained typically rises steeply, then flattens — a
"scree" shape that tells you how many components to keep:

```plot
{"title": "PCA scree: cumulative variance explained vs components kept", "xLabel": "components kept", "yLabel": "cumulative variance", "xRange": [0, 3.2], "yRange": [0, 1.05], "functions": [{"expr": "1", "label": "100%", "color": "#94a3b8"}], "points": [{"x": 1, "y": 0.78, "label": "1 comp: 78%", "color": "#2563eb", "size": 7}, {"x": 2, "y": 0.94, "label": "2 comps: 94%", "color": "#2563eb", "size": 7}, {"x": 3, "y": 1.0, "label": "3 comps: 100%", "color": "#dc2626", "size": 7}]}
```

```mermaid
flowchart LR
    A[Centre the data] --> B[Covariance matrix Σ]
    B --> C[Eigen-decompose Σ]
    C --> D[Sort by eigenvalue]
    D --> E[Project onto top components]
```

**Next:** fitting parameters by maximising likelihood.
""",
        ),
        _t(
            "Maximum likelihood with scipy.optimize",
            "12 min",
            r"""\
# Maximum likelihood with scipy.optimize

**Maximum likelihood estimation (MLE)** picks the parameters that make the
observed data most probable. We maximise the **log-likelihood**
$\ell(\theta) = \sum_i \log f(x_i \mid \theta)$ — equivalently, **minimise** the
*negative* log-likelihood with `scipy.optimize.minimize`.

```python
import numpy as np
from scipy import optimize, stats

rng = np.random.default_rng(0)
data = rng.normal(loc=3.0, scale=2.0, size=500)   # true μ=3, σ=2

def neg_log_likelihood(params, x):
    mu, sigma = params
    if sigma <= 0:                       # σ must be positive
        return np.inf
    # scipy gives the log-pdf directly; sum it and negate.
    return -np.sum(stats.norm.logpdf(x, loc=mu, scale=sigma))

result = optimize.minimize(
    neg_log_likelihood,
    x0=[0.0, 1.0],                       # initial guess for (μ, σ)
    args=(data,),
    method="Nelder-Mead",
)
mu_hat, sigma_hat = result.x
print(round(mu_hat, 3), round(sigma_hat, 3))   # ≈ sample mean and std
```

> **Sanity check.** For a Normal, the MLE of $\mu$ is exactly the sample mean and
> the MLE of $\sigma$ is the (population) sample standard deviation — the
> optimiser should land there.

MLE is not limited to Normals. Here it fits an **exponential** rate $\lambda$ to
waiting-time data:

```python
wait = rng.exponential(scale=1 / 0.7, size=400)   # true rate λ = 0.7

def neg_ll_exp(params, x):
    lam = params[0]
    if lam <= 0:
        return np.inf
    return -np.sum(stats.expon.logpdf(x, scale=1 / lam))

res = optimize.minimize(neg_ll_exp, x0=[1.0], args=(wait,), method="Nelder-Mead")
print(round(res.x[0], 3))               # ≈ 0.7  (MLE: λ̂ = 1 / mean)
```

The log-likelihood as a function of the candidate mean is a smooth hill; the
optimiser climbs to its peak — the MLE:

```plot
{"title": "Log-likelihood of μ: the optimiser finds the peak (MLE)", "xLabel": "candidate mean μ", "yLabel": "log-likelihood (shifted)", "xRange": [0, 6], "yRange": [-9, 0.5], "controls": [{"name": "mu", "range": [0, 6], "value": 1.5, "label": "candidate μ"}], "functions": [{"expr": "-(x-3)^2", "label": "ℓ(μ)", "color": "#2563eb"}], "points": [{"xExpr": "mu", "yExpr": "-(mu-3)^2", "color": "#dc2626", "size": 7}, {"x": 3, "y": 0, "label": "MLE μ̂ = 3", "color": "#16a34a", "size": 6}]}
```

```mermaid
flowchart LR
    A[Write the likelihood f x | θ] --> B[Take the log, sum over data]
    B --> C[Negate → loss to minimise]
    C --> D[scipy.optimize.minimize]
    D --> E[θ̂ = argmax likelihood]
```

**Next:** put it all together in one analysis.
""",
        ),
        _t(
            "End-to-end analysis: load, explore, test, model, conclude",
            "12 min",
            r"""\
# End-to-end analysis: load, explore, test, model, conclude

A real analysis chains everything you have learned. Here we compare two store
layouts (A vs B) on daily sales, then model the trend over time.

**1 — Load & inspect (pandas):**

```python
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(7)
days = np.arange(60)
sales_a = 100 + 0.5 * days + rng.normal(0, 10, 60)
sales_b = 110 + 0.5 * days + rng.normal(0, 10, 60)

df = pd.DataFrame({
    "day": np.r_[days, days],
    "layout": ["A"] * 60 + ["B"] * 60,
    "sales": np.r_[sales_a, sales_b],
})
df.head()
df.groupby("layout")["sales"].describe()   # explore each group
```

**2 — Explore (descriptive + correlation):**

```python
df.groupby("layout")["sales"].agg(["mean", "std", "count"])
df[df.layout == "B"][["day", "sales"]].corr()   # does sales trend with day?
```

**3 — Test (scipy.stats): is B really better than A?**

```python
a = df.loc[df.layout == "A", "sales"]
b = df.loc[df.layout == "B", "sales"]
t_stat, p = stats.ttest_ind(b, a, equal_var=False)
print(round(t_stat, 2), round(p, 4))     # p < 0.05 → B's mean is higher
```

**4 — Model (linear regression on the trend):**

```python
reg = stats.linregress(df.loc[df.layout == "B", "day"],
                       df.loc[df.layout == "B", "sales"])
print(round(reg.slope, 3), round(reg.rvalue**2, 3))   # daily growth and R²
```

**5 — Conclude.** Report the effect size, its confidence interval, and the
p-value together — never a bare "significant":

```python
diff = b.mean() - a.mean()
se = np.sqrt(b.var(ddof=1) / b.size + a.var(ddof=1) / a.size)
ci = (diff - 1.96 * se, diff + 1.96 * se)
print(f"B beats A by {diff:.1f} units, 95% CI {ci[0]:.1f}..{ci[1]:.1f}, p={p:.4f}")
```

The two groups separate, and each rises along its regression line — the picture
that backs the conclusion:

```plot
{"title": "Layout B (red) sits above A (blue), both trending up with day", "xLabel": "day", "yLabel": "sales", "xRange": [0, 60], "yRange": [90, 150], "functions": [{"expr": "100 + 0.5*x", "label": "A trend", "color": "#2563eb"}, {"expr": "110 + 0.5*x", "label": "B trend", "color": "#dc2626"}], "points": [{"x": 0, "y": 100, "label": "A start", "color": "#2563eb", "size": 6}, {"x": 60, "y": 130, "color": "#2563eb", "size": 6}, {"x": 0, "y": 110, "label": "B start", "color": "#dc2626", "size": 6}, {"x": 60, "y": 140, "label": "B end", "color": "#dc2626", "size": 6}]}
```

The complete pipeline, start to finish:

```mermaid
flowchart LR
    A[Load with pandas] --> B[Explore: describe, corr]
    B --> C[Test: scipy.stats]
    C --> D[Model: linregress]
    D --> E[Conclude: effect + CI + p]
```

**Next:** test what you've learned.
""",
        ),
    ),
)


PROB_STATS_PYTHON_COURSES = (_PS_BASICS, _PS_INTERMEDIATE, _PS_ADVANCED)

__all__ = ["PROB_STATS_PYTHON_COURSES"]
