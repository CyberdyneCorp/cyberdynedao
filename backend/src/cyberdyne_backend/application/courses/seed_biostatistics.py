"""Statistics & Biostatistics track: Basics -> Intermediate -> Advanced.

From data, distributions and descriptive statistics, through estimation,
hypothesis testing and regression, to experimental design, survival analysis and
multiple-testing correction in genomics. Lessons are ``text`` with LaTeX,
interactive ```plot blocks and ```mermaid pipeline diagrams.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Statistics & Biostatistics -- Basics -------------------------------------

_BASICS = SeedCourse(
    slug="biostatistics-basics",
    title="Statistics & Biostatistics — Basics",
    description=(
        "Build the foundations: kinds of data and study designs, summarising "
        "data with centre and spread, probability and the key distributions, "
        "the Normal curve and the Central Limit Theorem. The intuition every "
        "experiment, clinical trial and genomics analysis rests on, with "
        "interactive distribution plots."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Data types & study designs",
            "10 min",
            r"""
# Data types & study designs

Statistics begins by asking *what kind of data* you have and *how it was
collected*. The data type fixes which summaries and tests are legal.

- **Categorical (qualitative)**: nominal (blood type A/B/AB/O) or ordinal
  (tumour grade I–IV).
- **Numerical (quantitative)**: discrete counts (CFU per plate) or continuous
  measurements (serum glucose, mmHg).

Equally important is the **design**. An **observational** study merely watches
(cohort, case–control, cross-sectional) and is vulnerable to **confounding**; an
**experiment** (the randomised controlled trial, RCT) actively *intervenes* and
randomises, which is why it supports causal claims.

```mermaid
flowchart LR
  A[Research question] --> B{Intervene?}
  B -->|No| C[Observational]
  B -->|Yes| D[Experimental / RCT]
  C --> C1[Cohort]
  C --> C2[Case-control]
  C --> C3[Cross-sectional]
  D --> D1[Randomise + control]
```

A clean design beats any clever analysis: randomisation and blinding remove
biases that no statistical correction can fully repair afterwards.

**Next:** turning raw numbers into summaries.
""",
        ),
        _t(
            "Describing data: centre & spread",
            "11 min",
            r"""
# Describing data: centre & spread

Before any inference, summarise the sample.

**Centre**
- **Mean** $\bar x = \frac1n\sum x_i$ — the balance point, sensitive to outliers.
- **Median** — the middle value, robust to outliers and skew.
- **Mode** — the most frequent value.

**Spread**
- **Variance** $s^2 = \frac1{n-1}\sum (x_i-\bar x)^2$ and **standard deviation** $s$.
- **IQR** = $Q_3 - Q_1$, the middle-50% range, paired with the median.

Skewed biological data (incubation times, viral loads) pull the mean away from
the median, so report the median + IQR there. For a roughly Normal variable the
mean sits at the peak; drag $\sigma$ to see the spread widen:

```plot
{"title": "Centre and spread of a distribution", "xLabel": "value", "yLabel": "density", "xRange": [-6, 12], "yRange": [0, 0.85], "grid": true, "functions": [{"expr": "exp(-(x-3)^2/(2*1.5^2))/(1.5*sqrt(2*pi))", "label": "density", "color": "#2563eb"}]}
```

Always look at the data first: a histogram or boxplot reveals skew, outliers and
multiple peaks that a single number hides.

**Next:** the language of probability.
""",
        ),
        _t(
            "Probability essentials",
            "11 min",
            r"""
# Probability essentials

Probability is the engine of inference. A probability $P(A)\in[0,1]$ measures how
likely event $A$ is.

- **Complement**: $P(A^c) = 1 - P(A)$.
- **Addition**: $P(A\cup B) = P(A) + P(B) - P(A\cap B)$.
- **Conditional**: $P(A\mid B) = \dfrac{P(A\cap B)}{P(B)}$.
- **Independence**: $A,B$ independent $\iff P(A\cap B) = P(A)\,P(B)$.

**Bayes' theorem** updates beliefs with evidence and underlies diagnostic
testing: $P(D\mid +) = \dfrac{P(+\mid D)\,P(D)}{P(+)}$. With a rare disease, even
an accurate test gives many **false positives** — base rates matter.

```mermaid
flowchart LR
  P[Prior P D] --> B[Bayes rule]
  L[Likelihood P plus given D] --> B
  E[Evidence P plus] --> B
  B --> Post[Posterior P D given plus]
```

Sensitivity is $P(+\mid D)$ and specificity is $P(-\mid D^c)$; the **positive
predictive value** $P(D\mid +)$ also depends on prevalence, which is why
screening rare conditions is hard.

**Next:** named distributions for counts and rare events.
""",
        ),
        _t(
            "Discrete distributions: Binomial & Poisson",
            "11 min",
            r"""
# Discrete distributions: Binomial & Poisson

Counts of events follow a handful of canonical laws.

The **Binomial** $X\sim\text{Bin}(n,p)$ counts successes in $n$ independent trials
with success probability $p$:
$$P(X=k) = \binom{n}{k} p^k (1-p)^{n-k},\quad E[X]=np,\ \text{Var}=np(1-p).$$
Use it for "how many of 20 patients respond" when each responds independently with
probability $p$.

The **Poisson** $X\sim\text{Pois}(\lambda)$ counts rare events in a fixed
window — mutations per genome, colonies per plate, ER arrivals per hour:
$$P(X=k) = \frac{\lambda^k e^{-\lambda}}{k!},\quad E[X]=\text{Var}=\lambda.$$
It is the limit of the Binomial as $n\to\infty$, $p\to 0$ with $np=\lambda$ fixed.

The expected Poisson count grows linearly with the exposure window:

```plot
{"title": "Poisson mean λ vs exposure time", "xLabel": "exposure (hours)", "yLabel": "expected count", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "1*x", "label": "λ = rate × time", "color": "#16a34a"}]}
```

A telltale sign of Poisson data is mean ≈ variance; if variance is much larger
the data are **overdispersed** (often negative-binomial, common in RNA-seq).

**Next:** the Normal curve and the CLT.
""",
        ),
        _t(
            "The Normal distribution & the CLT",
            "11 min",
            r"""
# The Normal distribution & the CLT

The **Normal** (Gaussian) distribution $N(\mu,\sigma^2)$ is the bell curve that
dominates statistics:
$$f(x) = \frac{1}{\sigma\sqrt{2\pi}}\,e^{-(x-\mu)^2/(2\sigma^2)}.$$
About **68%** of mass lies within $\mu\pm\sigma$, **95%** within $\mu\pm2\sigma$.
Standardising gives the **z-score** $z = \dfrac{x-\mu}{\sigma}$, putting any
Normal on the same $N(0,1)$ scale.

The **Central Limit Theorem (CLT)** explains its ubiquity: for almost any
population, the sample mean $\bar X$ of $n$ observations is approximately Normal,
centred at $\mu$ with **standard error** $\sigma/\sqrt n$ — regardless of the
population's shape, once $n$ is moderately large.

```plot
{"title": "Standard Normal density N(0,1)", "xLabel": "z", "yLabel": "density", "xRange": [-4, 4], "yRange": [0, 0.45], "grid": true, "functions": [{"expr": "exp(-x^2/2)/sqrt(2*pi)", "label": "φ(z)", "color": "#2563eb"}]}
```

The CLT is why means, proportions and regression coefficients get Normal-based
confidence intervals and z/t tests even when raw data are not Normal.

**Next:** test your foundations.
""",
        ),
        _quiz(),
    ),
)


# -- Statistics & Biostatistics -- Intermediate -------------------------------

_INTERMEDIATE = SeedCourse(
    slug="biostatistics-intermediate",
    title="Statistics & Biostatistics — Intermediate",
    description=(
        "The quantitative core: point and interval estimation, the logic of "
        "hypothesis testing and p-values, t-tests and ANOVA, chi-square for "
        "categorical data, and linear and logistic regression. The toolkit for "
        "analysing real experiments and clinical data, with interactive "
        "power and dose-response plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Estimation & confidence intervals",
            "11 min",
            r"""
# Estimation & confidence intervals

A **point estimate** is a single best guess (the sample mean $\bar x$ for $\mu$),
but it never lands exactly on the truth. A **confidence interval (CI)** reports a
plausible range plus its reliability.

For a mean with known-ish spread, the 95% CI is
$$\bar x \pm z_{0.975}\,\frac{s}{\sqrt n} = \bar x \pm 1.96\,\frac{s}{\sqrt n}.$$
With small $n$ and unknown $\sigma$ you swap $z$ for the **Student-t** critical
value $t_{n-1}$, which is slightly wider.

**Correct interpretation**: over many repeated samples, 95% of such intervals
contain $\mu$. It is *not* "95% probability $\mu$ is in this one interval". The
width shrinks only as $\sqrt n$ — quadrupling the sample halves the margin:

```plot
{"title": "Margin of error shrinks as 1/√n", "xLabel": "sample size n", "yLabel": "margin (× s)", "xRange": [1, 100], "yRange": [0, 2], "grid": true, "functions": [{"expr": "1.96/sqrt(x)", "label": "1.96 / √n", "color": "#2563eb"}]}
```

Reporting an estimate **with its CI** is far more informative than a bare number
or a lone p-value.

**Next:** the formal logic of hypothesis testing.
""",
        ),
        _t(
            "Hypothesis testing & p-values",
            "12 min",
            r"""
# Hypothesis testing & p-values

A hypothesis test pits a **null** $H_0$ (no effect) against an **alternative**
$H_1$. You compute a **test statistic**, then a **p-value**: the probability of a
result at least this extreme *if $H_0$ were true*.

```mermaid
flowchart LR
  A[State H0 and H1] --> B[Pick alpha]
  B --> C[Compute test statistic]
  C --> D[Get p-value]
  D --> E{p < alpha?}
  E -->|Yes| F[Reject H0]
  E -->|No| G[Fail to reject H0]
```

Two error types govern everything:
- **Type I (α)**: rejecting a true $H_0$ — a false positive (often α = 0.05).
- **Type II (β)**: failing to reject a false $H_0$. **Power** = $1-\beta$.

A small p-value means the data are surprising under $H_0$; it does **not** measure
effect size or the probability $H_0$ is true. Power rises with sample size — the
detection rate of a real effect climbs and saturates toward 1:

```plot
{"title": "Statistical power vs sample size", "xLabel": "sample size", "yLabel": "power (1 − β)", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "power", "color": "#16a34a"}]}
```

Always pair a p-value with an effect size and CI; "statistically significant" and
"clinically important" are different claims.

**Next:** comparing means.
""",
        ),
        _t(
            "t-tests & ANOVA",
            "11 min",
            r"""
# t-tests & ANOVA

To compare **means**, use the t-test family. The two-sample t-statistic is
$$t = \frac{\bar x_1 - \bar x_2}{\text{SE}_{\text{diff}}},$$
referred to a Student-t distribution with the appropriate degrees of freedom.
Variants: **one-sample** (vs a reference), **paired** (before/after on the same
subject, removing between-subject variation), and **Welch's** (unequal variances —
a safer default than the classic pooled test).

For **three or more groups**, repeated t-tests inflate the false-positive rate, so
use **ANOVA**, which partitions variance and computes
$$F = \frac{\text{between-group variance}}{\text{within-group variance}}.$$
A large $F$ says groups differ; **post-hoc** tests (Tukey's HSD) then locate
*which* pairs, with multiplicity controlled.

```mermaid
flowchart LR
  A[Compare means] --> B{How many groups?}
  B -->|Two| C[t-test]
  B -->|Three plus| D[ANOVA]
  C --> C1[paired or Welch]
  D --> E{F significant?}
  E -->|Yes| F[Tukey post-hoc]
```

Check assumptions — approximate Normality of residuals and (for classic ANOVA)
equal variances; otherwise use Welch ANOVA or non-parametric Kruskal–Wallis.

**Next:** categorical associations.
""",
        ),
        _t(
            "Categorical data & the chi-square test",
            "10 min",
            r"""
# Categorical data & the chi-square test

When both variables are categorical — treatment vs outcome, genotype vs
phenotype — cross-tabulate into a **contingency table** and test for association
with the **chi-square test**:
$$\chi^2 = \sum \frac{(O - E)^2}{E},$$
where $O$ are observed counts and $E = \dfrac{(\text{row total})(\text{col total})}{n}$
are the counts expected under independence. Large $\chi^2$ (small p) means the
variables are associated.

The reference $\chi^2$ density shifts right as degrees of freedom grow:

```plot
{"title": "Chi-square density (df = 4)", "xLabel": "χ²", "yLabel": "density", "xRange": [0, 16], "yRange": [0, 0.2], "grid": true, "functions": [{"expr": "x*exp(-x/2)/4", "label": "df = 4", "color": "#dc2626"}]}
```

Caveats: the approximation needs **expected counts ≥ 5**; for sparse $2\times2$
tables use **Fisher's exact test**. Effect sizes for tables include the **odds
ratio** and **relative risk**, central to epidemiology.

**Next:** modelling relationships with regression.
""",
        ),
        _t(
            "Linear & logistic regression",
            "12 min",
            r"""
# Linear & logistic regression

Regression models how an outcome depends on predictors.

**Linear regression** fits a continuous outcome:
$$y = \beta_0 + \beta_1 x_1 + \dots + \beta_k x_k + \varepsilon,$$
estimating $\beta$ by **least squares**. Each $\beta_j$ is the change in $y$ per
unit of $x_j$ holding the others fixed — this **adjustment** is how we control for
confounders. $R^2$ reports the fraction of variance explained.

**Logistic regression** handles a binary outcome (disease yes/no) by modelling
the **log-odds** linearly:
$$\log\frac{p}{1-p} = \beta_0 + \beta_1 x,\qquad p = \frac{1}{1+e^{-(\beta_0+\beta_1 x)}}.$$
The predicted probability follows an S-curve, and $e^{\beta_j}$ is an **odds
ratio** — the workhorse of clinical risk modelling:

```plot
{"title": "Logistic dose-response curve", "xLabel": "predictor x", "yLabel": "probability", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "P(outcome)", "color": "#2563eb"}]}
```

Always check assumptions (linearity, independence, residual behaviour) and beware
**collinearity**, which destabilises individual coefficients.

**Next:** test your core methods.
""",
        ),
        _quiz(),
    ),
)


# -- Statistics & Biostatistics -- Advanced -----------------------------------

_ADVANCED = SeedCourse(
    slug="biostatistics-advanced",
    title="Statistics & Biostatistics — Advanced",
    description=(
        "State-of-the-art and applied biostatistics: experimental design and "
        "power, survival analysis with Kaplan–Meier and Cox models, the "
        "multiple-testing problem and FDR control in genomics, generalised "
        "mixed models, and Bayesian and machine-learning approaches to "
        "high-dimensional biological data, with interactive survival and "
        "dose-response plots."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Experimental design & power analysis",
            "12 min",
            r"""
# Experimental design & power analysis

Good design is decided **before** data collection. Core principles
(Fisher): **randomisation** (breaks confounding), **replication** (estimates
error), **blocking** (removes nuisance variation), and **blinding** (removes bias).

A **power analysis** sizes the study so a real effect is likely detected. Power
depends on the effect size $\delta$, the variability $\sigma$, the significance
level $\alpha$, and the sample size $n$. For two means,
$$n \approx \frac{2\,(z_{1-\alpha/2}+z_{1-\beta})^2\,\sigma^2}{\delta^2}.$$
Smaller effects and noisier measurements demand dramatically larger $n$.

```mermaid
flowchart LR
  A[Effect size delta] --> P[Power calc]
  B[Variance sigma sq] --> P
  C[Alpha] --> P
  D[Target power] --> P
  P --> N[Required sample size n]
```

Required $n$ falls off steeply as the detectable effect grows — designing for an
implausibly tiny effect is what makes studies infeasible:

```plot
{"title": "Required n vs effect size (illustrative)", "xLabel": "effect size δ", "yLabel": "required n", "xRange": [0.2, 3], "yRange": [0, 50], "grid": true, "functions": [{"expr": "16/x^2", "label": "n ∝ 1/δ²", "color": "#dc2626"}]}
```

Underpowered studies waste resources and produce noisy, irreproducible findings.

**Next:** analysing time-to-event data.
""",
        ),
        _t(
            "Survival analysis: Kaplan–Meier & Cox",
            "12 min",
            r"""
# Survival analysis: Kaplan–Meier & Cox

**Survival analysis** models **time-to-event** data (death, relapse, device
failure) where some subjects are **censored** — followed without the event yet.
Censoring is information that standard regression cannot handle.

The **survival function** $S(t)=P(T>t)$ is estimated non-parametrically by the
**Kaplan–Meier** estimator, a step curve that drops at each event time. The
**log-rank test** compares survival curves between groups. A smooth exponential
survival curve illustrates the shape:

```plot
{"title": "Survival function S(t) = exp(−λt)", "xLabel": "time", "yLabel": "S(t)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "S(t)", "color": "#2563eb"}]}
```

To adjust for covariates, the **Cox proportional-hazards model** specifies the
hazard as
$$h(t\mid x) = h_0(t)\,\exp(\beta_1 x_1 + \dots + \beta_k x_k),$$
leaving the baseline hazard $h_0(t)$ unspecified (semi-parametric). Then
$e^{\beta_j}$ is a **hazard ratio**. Its key assumption — **proportional
hazards** — must be checked (e.g. Schoenfeld residuals).

```mermaid
flowchart LR
  A[Time-to-event + censoring] --> B[Kaplan-Meier curve]
  B --> C[Log-rank test]
  A --> D[Cox PH model]
  D --> E[Hazard ratios]
```

**Next:** the multiple-testing problem in genomics.
""",
        ),
        _t(
            "Multiple testing & FDR in genomics",
            "12 min",
            r"""
# Multiple testing & FDR in genomics

A microarray or RNA-seq experiment tests thousands of genes at once. At α = 0.05,
testing 20,000 null genes yields ~1,000 **false positives** by chance alone — the
**multiple-comparisons problem**.

Two control philosophies:
- **Family-wise error rate (FWER)**: probability of *any* false positive.
  **Bonferroni** uses threshold $\alpha/m$ — strict, low power for large $m$.
- **False discovery rate (FDR)**: expected *proportion* of false positives among
  the calls. **Benjamini–Hochberg (BH)** sorts p-values $p_{(1)}\le\dots\le p_{(m)}$
  and finds the largest $k$ with $p_{(k)} \le \frac{k}{m}\,q$.

```mermaid
flowchart LR
  A[m p-values] --> B[Sort ascending]
  B --> C[BH threshold k over m times q]
  C --> D[Call discoveries]
  D --> E[Report q-values]
```

FDR is the right currency for discovery science: tolerating a small, known false
fraction recovers far more true signals than Bonferroni. The BH cutoff line rises
linearly with rank — points below it are declared significant:

```plot
{"title": "Benjamini–Hochberg threshold (q = 0.1)", "xLabel": "rank k / m", "yLabel": "p-value cutoff", "xRange": [0, 1], "yRange": [0, 0.1], "grid": true, "functions": [{"expr": "0.1*x", "label": "(k/m)·q", "color": "#16a34a"}]}
```

Report **q-values** (the minimum FDR at which a gene is called) alongside raw
p-values.

**Next:** models for clustered and hierarchical data.
""",
        ),
        _t(
            "Mixed models & generalised linear models",
            "12 min",
            r"""
# Mixed models & generalised linear models

Real biological data violate the independence assumption: repeated measures on a
patient, cells within a mouse, mice within a litter. **Mixed-effects models** add
**random effects** to capture this grouping:
$$y_{ij} = \beta_0 + \beta_1 x_{ij} + u_i + \varepsilon_{ij},\qquad u_i \sim N(0,\sigma_u^2),$$
where $u_i$ is a per-group offset. **Fixed effects** estimate population trends;
**random effects** absorb correlation within clusters, giving honest standard
errors.

**Generalised linear models (GLMs)** extend regression to non-Normal outcomes via
a **link function** and a distribution: logistic (binomial, logit link), Poisson
(log link) for counts, and **negative binomial** for overdispersed counts — the
default for RNA-seq differential expression (DESeq2, edgeR).

```mermaid
flowchart LR
  A[Outcome type] --> B{Distribution}
  B -->|Binary| C[Logistic - logit]
  B -->|Count| D[Poisson - log]
  B -->|Overdispersed count| E[Negative binomial]
  A --> F{Clustered?}
  F -->|Yes| G[Add random effects -> GLMM]
```

For counts, the **log link** means effects are multiplicative — the expected count
grows exponentially in the linear predictor:

```plot
{"title": "Log-link mean: E[y] = exp(βx)", "xLabel": "linear predictor", "yLabel": "expected count", "xRange": [0, 8], "yRange": [0, 12], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "exp(βx)", "color": "#2563eb"}]}
```

GLMMs (GLM + random effects) are the modern default for clustered, non-Normal
biological data.

**Next:** Bayesian and ML approaches to high-dimensional data.
""",
        ),
        _t(
            "Bayesian & machine-learning methods",
            "12 min",
            r"""
# Bayesian & machine-learning methods

Modern biostatistics blends **Bayesian** reasoning and **machine learning** for
high-dimensional, complex data.

**Bayesian inference** updates a prior into a **posterior** via Bayes' rule,
$p(\theta\mid \text{data}) \propto p(\text{data}\mid\theta)\,p(\theta)$, computed
with **MCMC** (Stan, PyMC) or variational methods. It yields full **credible
intervals** and **shrinks** noisy gene-level estimates toward a shared
distribution — exactly what `limma` and DESeq2 do empirically to stabilise small
samples.

**Machine learning** tackles $p \gg n$ problems (thousands of genes, few samples):
- **Penalised regression** — LASSO ($\ell_1$) drives coefficients to zero for
  biomarker selection; ridge ($\ell_2$) and elastic net handle collinearity.
- **Random forests / gradient boosting** for non-linear prediction.
- **Cross-validation** to estimate out-of-sample error and avoid overfitting.

```mermaid
flowchart LR
  A[High-dim omics data] --> B[Feature selection - LASSO]
  A --> C[Bayesian shrinkage]
  B --> D[Model]
  C --> D
  D --> E[Cross-validate]
  E --> F[Validate on held-out cohort]
```

Penalty strength trades fit against simplicity; the effective number of selected
features falls as the penalty $\lambda$ rises:

```plot
{"title": "LASSO: effective coefficients vs penalty λ", "xLabel": "penalty λ", "yLabel": "nonzero coefficients", "xRange": [0, 10], "yRange": [0, 20], "grid": true, "functions": [{"expr": "20*exp(-0.5*x)", "label": "selected features", "color": "#dc2626"}]}
```

The constant theme: borrow strength across features, regularise hard, and
**validate on an independent cohort** before any biological claim.

**Next:** test your advanced mastery.
""",
        ),
        _quiz(),
    ),
)


BIOSTATISTICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["BIOSTATISTICS_COURSES"]
