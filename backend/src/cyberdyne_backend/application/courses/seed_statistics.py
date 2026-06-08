"""Statistical Inference track: Basics -> Intermediate -> Advanced.

From samples and sampling distributions to hypothesis testing, confidence
intervals, A/B testing, maximum likelihood, Bayesian inference, regression and
the bootstrap. Builds on the Probability & Statistics course. Lessons are `text`
with LaTeX and interactive ```plot blocks; the Advanced track ends with a
runnable Monte-Carlo / bootstrap lab.
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, μ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Statistical Inference — Basics ───────────────────────────────────────────

_BASICS = SeedCourse(
    slug="statinf-basics",
    title="Statistical Inference — Basics",
    description=(
        "From data to conclusions: populations vs samples, summarising data "
        "(mean, variance, quantiles), sampling distributions and the standard "
        "error, and confidence intervals. The groundwork for every experiment, "
        "poll and A/B test, with interactive distribution plots."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Populations, samples & statistics",
            "11 min",
            """\
# Populations, samples & statistics

Statistics is the science of drawing conclusions about a **population** (everyone
/ everything we care about) from a **sample** (the few we actually measure).

- A **parameter** describes the population — the true mean $\\mu$, true proportion
  $p$. Usually unknown.
- A **statistic** is computed from the sample — the sample mean $\\bar x$, sample
  proportion $\\hat p$. We use it to **estimate** the parameter.

The catch: a sample is random, so a statistic is random too. Below is a
population (a Normal with mean $\\mu = 3$); any one sample's mean lands *near* 3
but rarely exactly on it — quantifying that wobble is the whole game:

```plot
{"title": "Population distribution (true mean μ = 3)", "xLabel": "value", "yLabel": "density", "xRange": [-2, 8], "yRange": [0, 0.45], "functions": [{"expr": "exp(-(x-3)^2/2)/sqrt(2*pi)", "label": "population", "color": "#2563eb"}], "points": [{"x": 3, "y": 0, "label": "μ = 3 (unknown in practice)", "color": "#dc2626", "size": 7}]}
```

Good sampling must be **representative** (ideally random) — biased samples break
everything downstream, no matter how much data you collect.

**Next:** summarising a sample.
""",
        ),
        _t(
            "Describing data: centre & spread",
            "11 min",
            """\
# Describing data: centre & spread

Before inferring anything, summarise the data.

**Centre**
- **Mean** $\\bar x = \\frac1n\\sum x_i$ — the balance point (sensitive to outliers).
- **Median** — the middle value (robust to outliers).
- **Mode** — the most common value.

**Spread**
- **Variance** $s^2 = \\frac1{n-1}\\sum (x_i-\\bar x)^2$ and **standard deviation** $s$.
- **Quantiles / IQR** — percentiles and the middle-50% range.

For a Normal, the mean sits at the peak and about **68%** of the data lies within
one standard deviation, **95%** within two. Drag $\\mu$ (centre) and $\\sigma$
(spread):

```plot
{"title": "Centre μ and spread σ of a distribution", "xLabel": "x", "yLabel": "density", "xRange": [-6, 10], "yRange": [0, 0.85], "controls": [{"name": "mu", "range": [-2, 5], "value": 2, "label": "mean μ"}, {"name": "sg", "range": [0.5, 3], "value": 1.5, "label": "std dev σ"}], "functions": [{"expr": "exp(-(x-mu)^2/(2*sg^2))/(sg*sqrt(2*pi))", "label": "f(x)", "color": "#2563eb"}], "points": [{"xExpr": "mu", "y": 0, "label": "mean", "color": "#dc2626", "size": 7}, {"xExpr": "mu-sg", "y": 0, "color": "#16a34a", "size": 5}, {"xExpr": "mu+sg", "y": 0, "label": "±σ (68%)", "color": "#16a34a", "size": 5}]}
```

Skew, outliers and the mean-vs-median gap are the first things to check in any
dataset.

**Next:** how the sample mean itself is distributed.
""",
        ),
        _t(
            "Sampling distributions & standard error",
            "11 min",
            """\
# Sampling distributions & standard error

Take many samples of size $n$ and compute $\\bar x$ each time — those means have
their own distribution, the **sampling distribution**. Two facts (from the CLT)
make inference possible:

- It is centred on the true mean $\\mu$ (the estimate is **unbiased**).
- Its spread — the **standard error** — is $\\mathrm{SE} = \\dfrac{\\sigma}{\\sqrt n}$.

So bigger samples give a *tighter* estimate, but only as $\\sqrt n$: to halve the
error you need **four times** the data. Increase $n$ and watch the sampling
distribution of $\\bar x$ concentrate on the truth:

```plot
{"title": "Sampling distribution of x̄ tightens as n grows", "xLabel": "sample mean x̄", "yLabel": "density", "xRange": [0, 6], "yRange": [0, 3], "controls": [{"name": "n", "range": [1, 50], "value": 1, "step": 1, "label": "sample size n"}], "functions": [{"expr": "exp(-(x-3)^2/(2/n))/sqrt(2*pi/n)", "label": "distribution of x̄", "color": "#2563eb"}], "points": [{"x": 3, "y": 0, "label": "true mean μ = 3", "color": "#dc2626", "size": 7}]}
```

The standard error is the single most important quantity in applied statistics —
it's the ± on every estimate.

**Next:** turning the standard error into a confidence interval.
""",
        ),
        _t(
            "Confidence intervals",
            "12 min",
            """\
# Confidence intervals

A point estimate ($\\bar x = 3.2$) is never the whole story — we report a range
that plausibly contains the true value. A **95% confidence interval** is

$$\\bar x \\;\\pm\\; 1.96\\,\\frac{\\sigma}{\\sqrt n}.$$

(The $1.96$ is the Normal's 95% cutoff; other confidence levels change it.) Its
**meaning**: if you repeated the whole experiment many times, about 95% of the
intervals you build would cover the true $\\mu$. The red markers are the interval
edges — increase $n$ and watch the interval **shrink** around the mean:

```plot
{"title": "95% confidence interval narrows with sample size", "xLabel": "x̄", "yLabel": "density", "xRange": [0, 6], "yRange": [0, 3], "controls": [{"name": "n", "range": [1, 50], "value": 4, "step": 1, "label": "sample size n"}], "functions": [{"expr": "exp(-(x-3)^2/(2/n))/sqrt(2*pi/n)", "label": "sampling distribution", "color": "#2563eb"}], "points": [{"xExpr": "3 - 1.96/sqrt(n)", "y": 0, "label": "lower 95%", "color": "#dc2626", "size": 7}, {"xExpr": "3 + 1.96/sqrt(n)", "y": 0, "label": "upper 95%", "color": "#dc2626", "size": 7}]}
```

A wider interval = more confidence but less precision; tightening it (more data)
is exactly the margin-of-error reported in every poll.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Statistical Inference — Intermediate ─────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="statinf-intermediate",
    title="Statistical Inference — Intermediate",
    description=(
        "Testing claims with data: hypothesis tests and p-values, Type I/II "
        "errors and power, t-tests for comparing groups, and a full A/B-testing "
        "workflow. The decision-making core of experiments and data science, with "
        "interactive plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Hypothesis testing & p-values",
            "13 min",
            """\
# Hypothesis testing & p-values

A **hypothesis test** asks whether the data is surprising under a default
assumption.

1. **Null hypothesis** $H_0$ — "nothing is going on" (no effect, no difference).
2. **Alternative** $H_1$ — what you suspect instead.
3. Compute a **test statistic** (e.g. how many standard errors the result is from
   the null).
4. The **p-value** is the probability of a result *at least this extreme* if $H_0$
   were true.

Small p-value → the data is unlikely under $H_0$, so we **reject** it (typically
at $\\alpha = 0.05$). Below is the null distribution; slide the observed statistic
outward — as it moves into the tail, the p-value (the area beyond it) shrinks:

```plot
{"title": "Null distribution; the p-value is the tail beyond the statistic", "xLabel": "test statistic z", "yLabel": "density", "xRange": [-4, 4], "yRange": [0, 0.45], "controls": [{"name": "z0", "range": [0, 3.5], "value": 1, "label": "observed statistic z"}], "functions": [{"expr": "exp(-x^2/2)/sqrt(2*pi)", "label": "H₀ distribution", "color": "#2563eb"}], "points": [{"xExpr": "z0", "yExpr": "exp(-z0^2/2)/sqrt(2*pi)", "label": "observed", "color": "#dc2626", "size": 7}, {"x": 1.96, "y": 0, "label": "5% cutoff (z=1.96)", "color": "#16a34a", "size": 6}]}
```

⚠️ A p-value is **not** the probability the null is true, and "not significant"
isn't "no effect". p-hacking and multiple comparisons inflate false positives.

**Next:** the two ways a test can be wrong.
""",
        ),
        _t(
            "Errors, power & sample size",
            "12 min",
            """\
# Errors, power & sample size

A test can be wrong two ways:

- **Type I error** (false positive, rate $\\alpha$): reject $H_0$ when it's true.
- **Type II error** (false negative, rate $\\beta$): fail to reject when $H_1$ is true.

**Power** $= 1-\\beta$ is the chance of detecting a real effect. It grows with the
**effect size**, the **sample size**, and a larger $\\alpha$. Below, the blue curve
is the world under $H_0$ and the red curve under a real effect of size $d$; the
green line is the decision cutoff. Slide the effect size and watch the curves
separate — the more they overlap, the more errors you make:

```plot
{"title": "H₀ vs a real effect of size d (overlap = errors)", "xLabel": "test statistic", "yLabel": "density", "xRange": [-4, 7], "yRange": [0, 0.45], "controls": [{"name": "d", "range": [0, 5], "value": 2.5, "label": "effect size d"}], "functions": [{"expr": "exp(-x^2/2)/sqrt(2*pi)", "label": "H₀ (no effect)", "color": "#2563eb"}, {"expr": "exp(-(x-d)^2/2)/sqrt(2*pi)", "label": "H₁ (effect = d)", "color": "#dc2626"}], "points": [{"x": 1.96, "y": 0, "label": "decision cutoff", "color": "#16a34a", "size": 6}]}
```

This is why studies do a **power analysis** up front: to pick a sample size big
enough to catch an effect worth catching.

**Next:** the workhorse test for means — the t-test.
""",
        ),
        _t(
            "t-tests: comparing groups",
            "12 min",
            """\
# t-tests: comparing groups

To compare a mean against a value, or two group means against each other, we use
a **t-test**. The **t-statistic** is the difference measured in standard errors:

$$t = \\frac{\\bar x_A - \\bar x_B}{\\mathrm{SE}_{\\text{diff}}}.$$

When the sample is small and $\\sigma$ is estimated from the data, the right
reference is the **Student's t-distribution** (heavier tails than the Normal),
converging to the Normal as $n$ grows. Two groups are "significantly different"
when their distributions separate relative to their spread — slide the gap:

```plot
{"title": "Two groups: significant when they separate vs their spread", "xLabel": "measurement", "yLabel": "density", "xRange": [-4, 8], "yRange": [0, 0.45], "controls": [{"name": "sep", "range": [0, 5], "value": 2, "label": "difference in means"}], "functions": [{"expr": "exp(-x^2/2)/sqrt(2*pi)", "label": "group A", "color": "#2563eb"}, {"expr": "exp(-(x-sep)^2/2)/sqrt(2*pi)", "label": "group B", "color": "#dc2626"}]}
```

Paired vs unpaired, equal vs unequal variances pick the exact variant — but the
idea is always *signal (difference) over noise (standard error)*.

**Next:** the most common real test — A/B testing.
""",
        ),
        _t(
            "A/B testing end to end",
            "12 min",
            """\
# A/B testing end to end

An **A/B test** is a randomised experiment comparing two variants (a button
colour, a model, a price). Usually we compare **conversion rates** (proportions):

1. Randomly split users into A and B.
2. Measure $\\hat p_A$, $\\hat p_B$ (e.g. click-through).
3. Test whether the difference is real or just noise.

Each rate has a confidence interval of half-width $\\approx 1.96\\sqrt{\\hat p(1-\\hat p)/n}$.
With little data the intervals overlap (inconclusive); as $n$ grows they shrink
and separate (a real winner). The bars are the 95% intervals — increase $n$:

```plot
{"title": "A/B test: 95% intervals separate as data grows", "xLabel": "variant", "yLabel": "conversion rate", "xRange": [0, 3], "yRange": [0, 0.3], "controls": [{"name": "n", "range": [50, 5000], "value": 400, "label": "users per variant"}], "points": [{"x": 1, "y": 0.1, "label": "A: 10%", "color": "#2563eb", "size": 7}, {"x": 2, "y": 0.13, "label": "B: 13%", "color": "#dc2626", "size": 7}], "vectors": [{"x": 1, "yExpr": "0.1 + 1.96*sqrt(0.1*0.9/n)", "fromExpr": ["1", "0.1 - 1.96*sqrt(0.1*0.9/n)"], "color": "#2563eb", "label": "A 95% CI"}, {"x": 2, "yExpr": "0.13 + 1.96*sqrt(0.13*0.87/n)", "fromExpr": ["2", "0.13 - 1.96*sqrt(0.13*0.87/n)"], "color": "#dc2626", "label": "B 95% CI"}]}
```

Watch for pitfalls: **peeking** (stopping early when it looks significant inflates
false positives), too-small samples, and the **multiple-comparisons** trap.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Statistical Inference — Advanced ─────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="statinf-advanced",
    title="Statistical Inference — Advanced",
    description=(
        "The modern inference toolkit: maximum likelihood estimation, Bayesian "
        "inference, regression as inference, and resampling (bootstrap & the "
        "bias-variance trade-off). The statistical core of machine learning, with "
        "a runnable bootstrap lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Maximum likelihood estimation",
            "13 min",
            """\
# Maximum likelihood estimation

**Maximum likelihood** picks the parameter that makes the observed data *most
probable*. Write the **likelihood** $L(\\theta) = P(\\text{data}\\mid\\theta)$, then
maximise it (usually its log, the **log-likelihood**, which turns products into
sums).

For a Normal with known variance, the likelihood of the mean $\\mu$ given the data
peaks exactly at the sample mean $\\bar x$ — drag the candidate mean and watch the
likelihood; the top is the MLE:

```plot
{"title": "Likelihood of the mean μ (peak = MLE = x̄)", "xLabel": "candidate mean μ", "yLabel": "likelihood", "xRange": [0, 6], "yRange": [0, 1.1], "controls": [{"name": "mu", "range": [0, 6], "value": 2, "label": "candidate μ"}], "functions": [{"expr": "exp(-3*(x-3.2)^2)", "label": "L(μ)", "color": "#2563eb"}], "points": [{"xExpr": "mu", "yExpr": "exp(-3*(mu-3.2)^2)", "color": "#dc2626", "size": 7}, {"x": 3.2, "y": 1, "label": "MLE x̄ = 3.2", "color": "#16a34a", "size": 6}]}
```

MLE underlies most fitted models: logistic regression, Gaussian fits, and — since
minimising **cross-entropy loss** is maximising likelihood — the training of
neural-network classifiers (see [[backpropagation]]).

**Next:** the Bayesian alternative.
""",
        ),
        _t(
            "Bayesian inference",
            "13 min",
            """\
# Bayesian inference

Instead of a single estimate, **Bayesian inference** keeps a whole *distribution*
of belief and updates it with data:

$$\\underbrace{P(\\theta\\mid\\text{data})}_{\\text{posterior}} \\;\\propto\\; \\underbrace{P(\\text{data}\\mid\\theta)}_{\\text{likelihood}}\\;\\underbrace{P(\\theta)}_{\\text{prior}}.$$

Start from a **prior** (what you believed before), multiply by the **likelihood**
(what the data says), get the **posterior** (updated belief). For estimating a
probability $p$ (a coin's bias, a conversion rate), observe heads and tails and
watch the posterior sharpen and shift:

```plot
{"title": "Bayesian updating: posterior over a probability p", "xLabel": "p", "yLabel": "belief density", "xRange": [0, 1], "yRange": [0, 4], "controls": [{"name": "h", "range": [0, 20], "value": 4, "step": 1, "label": "heads observed"}, {"name": "t", "range": [0, 20], "value": 2, "step": 1, "label": "tails observed"}], "functions": [{"expr": "x^h*(1-x)^t", "label": "posterior ∝ p^H (1−p)^T", "color": "#2563eb"}]}
```

A **credible interval** ("95% probability the rate is in here") is the Bayesian
analogue of a confidence interval — and the interpretation people *actually want*.
Bayesian methods shine with small data and prior knowledge, and power Bayesian
A/B testing and probabilistic ML.

**Next:** regression as inference.
""",
        ),
        _t(
            "Regression as inference",
            "12 min",
            """\
# Regression as inference

**Linear regression** fits $y = \\beta_0 + \\beta_1 x$ by least squares — but it is
also *inference*: each coefficient $\\beta$ comes with a standard error, a
confidence interval and a p-value (is this slope really non-zero?). $R^2$ reports
the fraction of variance explained, and the **residuals** should look like
structureless noise. Fit the line to the data:

```plot
{"title": "Regression: fit y = β₀ + β₁x, then judge the residuals", "xLabel": "x", "yLabel": "y", "xRange": [-0.5, 5.5], "yRange": [0, 8], "controls": [{"name": "b0", "range": [-1, 3], "value": 1, "label": "intercept β₀"}, {"name": "b1", "range": [0, 2], "value": 1, "label": "slope β₁"}], "functions": [{"expr": "b0 + b1*x", "label": "fit", "color": "#dc2626"}], "series": [{"points": [[0, 1.1], [1, 1.9], [2, 3.2], [3, 3.8], [4, 5.3], [5, 5.9]], "label": "data", "color": "#2563eb"}], "points": [{"x": 0, "y": 1.1, "color": "#2563eb", "size": 6}, {"x": 1, "y": 1.9, "color": "#2563eb", "size": 6}, {"x": 2, "y": 3.2, "color": "#2563eb", "size": 6}, {"x": 3, "y": 3.8, "color": "#2563eb", "size": 6}, {"x": 4, "y": 5.3, "color": "#2563eb", "size": 6}, {"x": 5, "y": 5.9, "color": "#2563eb", "size": 6}]}
```

Multiple regression, logistic regression (for yes/no outcomes) and regularised
variants (ridge/lasso) extend this — the boundary where classical statistics
becomes machine learning.

**Next:** resampling and the bias-variance trade-off.
""",
        ),
        _t(
            "Bootstrap & the bias-variance trade-off",
            "12 min",
            """\
# Bootstrap & the bias-variance trade-off

## The bootstrap

When a formula for the standard error is hard, **resample the data itself**: draw
many samples *with replacement* from your sample, recompute the statistic each
time, and use the spread of those values as the standard error / confidence
interval. It's astonishingly general — and the code lab builds one.

## Bias vs variance

Every fitted model balances two errors. A too-simple model **underfits** (high
**bias**); a too-complex one **overfits** the noise (high **variance**). Total
error is their sum — a U-curve with a sweet spot:

```plot
{"title": "Bias-variance trade-off: total error is U-shaped", "xLabel": "model complexity", "yLabel": "error", "xRange": [0.3, 6], "yRange": [0, 4], "functions": [{"expr": "1/x", "label": "bias² (falls)", "color": "#94a3b8"}, {"expr": "0.18*x", "label": "variance (rises)", "color": "#cbd5e1"}, {"expr": "1/x + 0.18*x", "label": "total error", "color": "#2563eb"}]}
```

**Cross-validation** estimates that total error honestly (train on part, test on
the rest) and is how you pick the sweet spot. This trade-off is the central
tension of all machine learning.

**Next:** run a bootstrap in code.
""",
        ),
        _code(
            "Lab: bootstrap confidence interval by simulation",
            "12 min",
            """\
# Statistical inference by simulation — the bootstrap, no libraries.

# A linear-congruential generator for repeatable 'random' numbers in [0, 1).
seed = 2024
rnd = []
for i in range(80000):
    seed = (1103515245 * seed + 12345) % 2147483648
    rnd.append(seed / 2147483648.0)

# A small sample of measurements (e.g. response times in ms).
data = [4.1, 5.2, 3.8, 6.0, 4.7, 5.5, 4.9, 6.3, 5.1, 4.4]
n = 10

total = 0.0
for v in data:
    total = total + v
mean = total / n
print("sample mean =", round(mean, 3))

# BOOTSTRAP: resample WITH REPLACEMENT B times, recompute the mean each time.
B = 3000
means = []
pos = 0
for b in range(B):
    s = 0.0
    for k in range(n):
        idx = int(rnd[pos] * n)
        if idx >= n:
            idx = n - 1
        s = s + data[idx]
        pos = pos + 1
    means.append(s / n)

# The spread of the bootstrap means estimates the standard error; a 95% interval
# is roughly mean +/- 1.96 * SE  (no formula for SE was needed!).
bm = 0.0
for v in means:
    bm = bm + v
bm = bm / B
bv = 0.0
for v in means:
    d = v - bm
    bv = bv + d * d
se = (bv / B) ** 0.5
print("bootstrap standard error =", round(se, 4))
print("95% bootstrap CI for the mean: [", round(bm - 1.96 * se, 3), ",", round(bm + 1.96 * se, 3), "]")

# Try it:
#   - Raise B for a smoother estimate; the interval itself barely moves.
#   - Add more data points: the interval shrinks like 1/sqrt(n).
""",
        ),
        _quiz(),
    ),
)


STATISTICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)

__all__ = ["STATISTICS_COURSES"]
