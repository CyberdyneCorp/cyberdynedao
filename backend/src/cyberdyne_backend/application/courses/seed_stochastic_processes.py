"""Random & Stochastic Processes track: Basics -> Intermediate -> Advanced.

From a review of probability and random variables to the theory of random
processes: stationarity, autocorrelation, power spectral density and the
Wiener-Khinchin theorem, LTI systems with random inputs, Gaussian processes and
ergodicity, then Poisson processes, Markov chains, thermal/electronic noise, the
matched filter, Wiener filtering and queueing. Lessons are `text` with LaTeX,
interactive ```plot blocks (PDFs, autocorrelation, power spectral density,
sample paths) and ```mermaid state/block diagrams.
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, μ, λ, τ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Random & Stochastic Processes — Basics ───────────────────────────────────

_SP_BASICS = SeedCourse(
    slug="stochastic-processes-basics",
    title="Random & Stochastic Processes — Basics",
    description=(
        "The probability groundwork for stochastic processes: random variables, "
        "expectation and moments, the workhorse distributions (Gaussian, uniform, "
        "exponential, Poisson), pairs of random variables with covariance and "
        "correlation, functions of random variables, and a first look at random "
        "processes as ensembles of realizations. Interactive distribution plots "
        "throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Probability & random variables review",
            "10 min",
            r"""\
# Probability & random variables review

A **random variable** (RV) maps the outcome of a random experiment to a number.
A *discrete* RV takes countably many values with a **probability mass function**
$P(X = x_k) = p_k$; a *continuous* RV is described by a **probability density
function (PDF)** $f_X(x) \ge 0$ with $\int_{-\infty}^{\infty} f_X(x)\,dx = 1$.

The **cumulative distribution function (CDF)** ties them together:

$$F_X(x) = P(X \le x) = \int_{-\infty}^{x} f_X(u)\,du, \qquad f_X(x) = \frac{dF_X}{dx}.$$

The probability of landing in an interval is the **area** under the PDF:

$$P(a < X \le b) = F_X(b) - F_X(a) = \int_a^b f_X(x)\,dx.$$

Here is a standard Gaussian PDF; the shaded idea is that area, not height, is
probability:

```plot
{"title": "A continuous PDF: area is probability", "xLabel": "x", "yLabel": "density f(x)", "xRange": [-4, 4], "yRange": [0, 0.45], "functions": [{"expr": "exp(-x^2/2)/sqrt(2*pi)", "label": "f(x)", "color": "#2563eb"}], "points": [{"x": 0, "y": 0, "label": "P(a<X≤b) = area", "color": "#dc2626", "size": 6}]}
```

Key axioms to keep handy: $0 \le P(A) \le 1$, $P(\text{certain}) = 1$, and for
disjoint events $P(A \cup B) = P(A) + P(B)$. Everything that follows is built on
these.

**Next:** how to summarise an RV with expectation, variance and moments.
""",
        ),
        _t(
            "Expectation, variance & moments",
            "11 min",
            r"""\
# Expectation, variance & moments

The **expectation** (mean) is the probability-weighted average:

$$\mu = E[X] = \int_{-\infty}^{\infty} x\, f_X(x)\,dx \quad\text{(continuous)}, \qquad E[X] = \sum_k x_k\, p_k \quad\text{(discrete)}.$$

Expectation is **linear**: $E[aX + b] = a\,E[X] + b$, regardless of the
distribution. The **variance** measures spread about the mean:

$$\sigma^2 = \operatorname{Var}(X) = E\!\big[(X-\mu)^2\big] = E[X^2] - \mu^2.$$

The **standard deviation** is $\sigma = \sqrt{\operatorname{Var}(X)}$. More
generally the **$n$-th moment** is $E[X^n]$ and the **$n$-th central moment** is
$E[(X-\mu)^n]$: the 2nd central moment is the variance, the (normalised) 3rd is
**skewness**, and the 4th is **kurtosis**.

Variance grows with the square of a scale factor: $\operatorname{Var}(aX) = a^2
\operatorname{Var}(X)$. Increasing $\sigma$ lowers and widens the Gaussian PDF
while preserving unit area:

```plot
{"title": "Variance controls width: f(x) for changing σ", "xLabel": "x", "yLabel": "density", "xRange": [-8, 8], "yRange": [0, 0.85], "controls": [{"name": "sg", "range": [0.5, 3], "value": 1, "label": "std dev σ"}], "functions": [{"expr": "exp(-x^2/(2*sg^2))/(sg*sqrt(2*pi))", "label": "f(x)", "color": "#2563eb"}], "points": [{"x": 0, "y": 0, "label": "mean μ = 0", "color": "#dc2626", "size": 6}]}
```

These two numbers — mean and variance — are the bread and butter of the whole
course: every stationary process is described first by its mean and its
second-order structure.

**Next:** the named distributions you will meet again and again.
""",
        ),
        _t(
            "Common distributions",
            "12 min",
            r"""\
# Common distributions

A handful of distributions cover most of engineering. Learn their PDF or PMF,
mean and variance.

**Gaussian (Normal)** $\mathcal{N}(\mu, \sigma^2)$ — the central-limit limit of
sums; mean $\mu$, variance $\sigma^2$:

$$f_X(x) = \frac{1}{\sigma\sqrt{2\pi}}\,e^{-(x-\mu)^2/(2\sigma^2)}.$$

**Uniform** $\mathcal{U}(a,b)$ — flat over $[a,b]$; mean $\tfrac{a+b}{2}$,
variance $\tfrac{(b-a)^2}{12}$.

**Exponential** (rate $\lambda$) — memoryless waiting time; mean $1/\lambda$,
variance $1/\lambda^2$:

$$f_X(x) = \lambda e^{-\lambda x}, \quad x \ge 0.$$

**Poisson** (rate $\lambda$) — counts of rare events; PMF
$P(X=k) = e^{-\lambda}\lambda^k/k!$, with **mean = variance = $\lambda$**.

Compare the two continuous shapes — symmetric Gaussian versus one-sided
exponential decay:

```plot
{"title": "Gaussian vs exponential PDFs", "xLabel": "x", "yLabel": "density", "xRange": [-3, 5], "yRange": [0, 1.1], "functions": [{"expr": "exp(-x^2/2)/sqrt(2*pi)", "label": "Gaussian N(0,1)", "color": "#2563eb"}, {"expr": "exp(-x)", "label": "exponential (λ=1, x≥0)", "color": "#dc2626"}]}
```

The exponential and Poisson are two faces of the same coin: if events arrive as
a **Poisson** count, the **gaps between them are exponential** — the link we
exploit later for Poisson processes and shot noise.

**Next:** what happens when two random variables interact.
""",
        ),
        _t(
            "Pairs of RVs: joint, conditional, covariance",
            "11 min",
            r"""\
# Pairs of RVs: joint, conditional, covariance

Two RVs $X$ and $Y$ are described jointly by $f_{X,Y}(x,y)$. **Marginals** come
from integrating out the other variable, and the **conditional** density is

$$f_{Y\mid X}(y\mid x) = \frac{f_{X,Y}(x,y)}{f_X(x)}.$$

$X$ and $Y$ are **independent** iff $f_{X,Y}(x,y) = f_X(x)\,f_Y(y)$ — the joint
factors into the marginals.

The **covariance** measures how they move together:

$$\operatorname{Cov}(X,Y) = E\!\big[(X-\mu_X)(Y-\mu_Y)\big] = E[XY] - \mu_X\mu_Y.$$

The **correlation coefficient** normalises it to $[-1, 1]$:

$$\rho_{XY} = \frac{\operatorname{Cov}(X,Y)}{\sigma_X\,\sigma_Y}.$$

$\rho = +1$ means a perfect rising line, $\rho = -1$ a perfect falling line,
$\rho = 0$ means **uncorrelated** (no *linear* relationship — they may still be
dependent). A picture of perfect positive vs perfect negative correlation:

```plot
{"title": "Correlation: the line Y relates to X", "xLabel": "x", "yLabel": "y", "xRange": [-3, 3], "yRange": [-3, 3], "functions": [{"expr": "x", "label": "ρ = +1", "color": "#2563eb"}, {"expr": "-x", "label": "ρ = -1", "color": "#dc2626"}, {"expr": "0", "label": "ρ = 0 (no linear trend)", "color": "#16a34a"}]}
```

A vital fact for the rest of the course: **independent ⇒ uncorrelated**, but the
converse is false in general. It *is* true for **jointly Gaussian** variables,
which is why Gaussian processes are so tractable.

**Next:** what happens to a distribution when you pass it through a function.
""",
        ),
        _t(
            "Functions of random variables",
            "11 min",
            r"""\
# Functions of random variables

Engineering constantly transforms signals: $Y = g(X)$. A deterministic block
maps each input value through $g(\cdot)$ to an output value:

```mermaid
flowchart LR
  X["Input RV X<br/>density f_X(x)"] --> G["Transform g(·)<br/>Y = g(X)"]
  G --> Y["Output RV Y<br/>density f_Y(y)"]
```

How is $Y$ distributed?

**Expectation without the PDF.** Often you only need a mean, and the **law of
the unconscious statistician** delivers it directly:

$$E[g(X)] = \int_{-\infty}^{\infty} g(x)\, f_X(x)\,dx.$$

No need to find $f_Y$ first. This is how we will compute signal **power**
$E[X^2]$ later.

**The full density.** For a smooth, monotonic $g$ with inverse $x = g^{-1}(y)$,

$$f_Y(y) = f_X\!\big(g^{-1}(y)\big)\,\left|\frac{dx}{dy}\right|.$$

The $|dx/dy|$ factor conserves probability mass as the axis stretches or
compresses. For a linear map $Y = aX + b$: $\mu_Y = a\mu_X + b$ and
$\sigma_Y^2 = a^2\sigma_X^2$.

A linear transform of a Gaussian stays Gaussian — only its centre and width
move. Slide the gain $a$ and offset $b$:

```plot
{"title": "Linear transform Y = aX + b of a Gaussian", "xLabel": "y", "yLabel": "density", "xRange": [-8, 12], "yRange": [0, 0.9], "controls": [{"name": "a", "range": [0.5, 3], "value": 1, "label": "gain a"}, {"name": "b", "range": [-2, 6], "value": 2, "label": "offset b"}], "functions": [{"expr": "exp(-(x-b)^2/(2*a^2))/(a*sqrt(2*pi))", "label": "f_Y(y)", "color": "#2563eb"}], "points": [{"xExpr": "b", "y": 0, "label": "new mean = b", "color": "#dc2626", "size": 6}]}
```

The takeaway: linear systems and Gaussian inputs are a closed, easy world — the
foundation of LTI-with-noise analysis in the Intermediate track.

**Next:** stitching RVs together over time into a random process.
""",
        ),
        _t(
            "Intro to random processes",
            "10 min",
            r"""\
# Intro to random processes

A **random (stochastic) process** $X(t)$ is a family of random variables indexed
by time. Fix the time $t$ and $X(t)$ is an ordinary RV; fix the outcome
$\omega$ (one run of the experiment) and $X(t, \omega)$ is a deterministic
**realization** or **sample path**. The collection of all sample paths is the
**ensemble**.

```mermaid
flowchart LR
  W["Random experiment outcome ω"] --> P["Stochastic process X(t, ω)"]
  P --> R1["Realization 1: sample path x1(t)"]
  P --> R2["Realization 2: sample path x2(t)"]
  P --> R3["Realization 3: sample path x3(t)"]
  R1 --> E["Ensemble = all sample paths"]
  R2 --> E
  R3 --> E
```

Two ways to average:
- **Ensemble average** — average across many sample paths *at a fixed time* $t$:
  the mean $m_X(t) = E[X(t)]$.
- **Time average** — average one sample path *over time*.

When the two agree, the process is **ergodic** (Intermediate track). The
first-order description is the time-varying mean and variance; the deeper
structure lives in how $X(t_1)$ and $X(t_2)$ relate — the **autocorrelation**.

Below: three example sample paths (here, sinusoids with random phase) drawn from
one ensemble:

```plot
{"title": "Three realizations of a random process", "xLabel": "time t", "yLabel": "x(t)", "xRange": [0, 12], "yRange": [-1.5, 1.5], "functions": [{"expr": "sin(x)", "label": "x1(t)", "color": "#2563eb"}, {"expr": "sin(x + 1.0)", "label": "x2(t)", "color": "#dc2626"}, {"expr": "sin(x + 2.2)", "label": "x3(t)", "color": "#16a34a"}]}
```

**Next course:** stationarity makes these averages independent of *when* you
look, unlocking the spectral tools.
""",
        ),
        _quiz(),
    ),
)


# ── Random & Stochastic Processes — Intermediate ─────────────────────────────

_SP_INTERMEDIATE = SeedCourse(
    slug="stochastic-processes-intermediate",
    title="Random & Stochastic Processes — Intermediate",
    description=(
        "The core theory of stationary processes: strict vs wide-sense "
        "stationarity, autocorrelation and autocovariance, power spectral "
        "density and the Wiener-Khinchin theorem, how LTI systems shape random "
        "inputs, Gaussian processes, and ergodicity linking time and ensemble "
        "averages. With autocorrelation and PSD plots and system block diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Stationarity: strict & wide-sense",
            "11 min",
            r"""\
# Stationarity: strict & wide-sense

A process is easier to analyse when its statistics do not drift with time.

**Strict-sense stationary (SSS).** Every finite-dimensional distribution is
invariant under a time shift $\tau$: the joint statistics of
$\{X(t_1), \dots, X(t_n)\}$ equal those of $\{X(t_1+\tau), \dots, X(t_n+\tau)\}$
for all $\tau$. A strong, often unverifiable condition.

**Wide-sense stationary (WSS).** Only the first two moments must be
shift-invariant — the practical workhorse:

1. The mean is constant: $m_X(t) = E[X(t)] = \mu_X$ for all $t$.
2. The autocorrelation depends only on the **lag** $\tau = t_2 - t_1$:

$$R_X(t_1, t_2) = R_X(\tau) = E\!\big[X(t)\,X(t+\tau)\big].$$

SSS $\Rightarrow$ WSS; the converse holds for **Gaussian** processes, where the
two notions coincide. WSS is exactly the assumption that makes the power
spectral density well defined.

A constant mean line versus a drifting (non-stationary) mean:

```plot
{"title": "Constant mean (WSS) vs drifting mean (non-stationary)", "xLabel": "time t", "yLabel": "mean m_X(t)", "xRange": [0, 10], "yRange": [-1, 4], "functions": [{"expr": "1", "label": "WSS: m_X = const", "color": "#2563eb"}, {"expr": "0.3*x", "label": "non-stationary mean", "color": "#dc2626"}]}
```

**Next:** the autocorrelation function, the heart of second-order theory.
""",
        ),
        _t(
            "Autocorrelation & autocovariance",
            "11 min",
            r"""\
# Autocorrelation & autocovariance

For a WSS process the **autocorrelation function** captures how a value relates
to itself $\tau$ seconds later:

$$R_X(\tau) = E\!\big[X(t)\,X(t+\tau)\big].$$

The **autocovariance** removes the mean:

$$C_X(\tau) = R_X(\tau) - \mu_X^2.$$

Essential properties:
- **Power at zero lag:** $R_X(0) = E[X^2(t)] \ge 0$ — the average power.
- **Even symmetry:** $R_X(-\tau) = R_X(\tau)$.
- **Maximum at the origin:** $|R_X(\tau)| \le R_X(0)$.
- It **decays** toward $\mu_X^2$ as $\tau \to \infty$ when distant samples
  decorrelate.

The *shape* tells you the bandwidth: a slowly decaying $R_X(\tau)$ means a
smooth, low-frequency (narrowband) process; a sharp spike means a fast,
broadband one. A classic example is $R_X(\tau) = e^{-|\tau|}$:

```plot
{"title": "Autocorrelation: slow vs fast decay", "xLabel": "lag τ", "yLabel": "R_X(τ)", "xRange": [-5, 5], "yRange": [0, 1.1], "functions": [{"expr": "exp(-abs(x))", "label": "slow decay (narrowband)", "color": "#2563eb"}, {"expr": "exp(-3*abs(x))", "label": "fast decay (broadband)", "color": "#dc2626"}], "points": [{"x": 0, "y": 1, "label": "R_X(0) = power", "color": "#16a34a", "size": 6}]}
```

This even, peaked-at-zero function is the bridge to the frequency domain — its
Fourier transform is the power spectral density.

**Next:** that transform, via the Wiener-Khinchin theorem.
""",
        ),
        _t(
            "Power spectral density & Wiener-Khinchin",
            "12 min",
            r"""\
# Power spectral density & Wiener-Khinchin

How is a random process's power spread across frequency? The **power spectral
density (PSD)** $S_X(f)$ answers this, and the **Wiener-Khinchin theorem** says
it is simply the Fourier transform of the autocorrelation:

$$S_X(f) = \int_{-\infty}^{\infty} R_X(\tau)\, e^{-j 2\pi f \tau}\,d\tau, \qquad R_X(\tau) = \int_{-\infty}^{\infty} S_X(f)\, e^{j 2\pi f \tau}\,df.$$

Consequences:
- $S_X(f) \ge 0$ for all $f$ (power cannot be negative).
- **Total average power** is the area under the PSD, which equals zero-lag
  autocorrelation:

$$E[X^2] = R_X(0) = \int_{-\infty}^{\infty} S_X(f)\,df.$$

- For real processes $S_X(f)$ is **even** in $f$.

Example: the autocorrelation $R_X(\tau) = e^{-|\tau|}$ transforms to the
**Lorentzian** PSD $S_X(f) = \dfrac{2}{1 + (2\pi f)^2}$ — a low-pass shape. **White
noise**, by contrast, has $S_X(f) = N_0/2$, flat for all $f$:

```plot
{"title": "Power spectral density: low-pass process vs white noise", "xLabel": "frequency f", "yLabel": "S_X(f)", "xRange": [-3, 3], "yRange": [0, 2.2], "functions": [{"expr": "2/(1 + (2*pi*x)^2)", "label": "Lorentzian (R=e^-|τ|)", "color": "#2563eb"}, {"expr": "0.5", "label": "white noise N0/2", "color": "#dc2626"}]}
```

A narrow autocorrelation ⇄ a wide spectrum, and vice versa: the same
time-frequency trade-off you know from deterministic Fourier analysis.

**Next:** sending such a process through a filter.
""",
        ),
        _t(
            "LTI systems with random inputs",
            "11 min",
            r"""\
# LTI systems with random inputs

Pass a WSS process $X(t)$ through a **linear time-invariant** system with impulse
response $h(t)$ and frequency response $H(f)$. The output $Y(t)$ is also WSS, and
the second-order statistics transform cleanly.

```mermaid
flowchart LR
  X["WSS input X(t)<br/>PSD S_X(f)"] --> H["LTI system<br/>H(f), h(t)"]
  H --> Y["Output Y(t)<br/>S_Y(f) = |H(f)|^2 S_X(f)"]
```

**Mean** scales by the DC gain:

$$\mu_Y = \mu_X \int_{-\infty}^{\infty} h(t)\,dt = \mu_X\, H(0).$$

**PSD** — the single most useful formula in the field:

$$\boxed{\,S_Y(f) = |H(f)|^2\, S_X(f)\,}$$

The system shapes the input spectrum by its **squared magnitude response**.
Output power follows by integrating:

$$E[Y^2] = \int_{-\infty}^{\infty} |H(f)|^2\, S_X(f)\,df.$$

Feed **white noise** ($S_X = N_0/2$) into a one-pole low-pass filter
$|H(f)|^2 = 1/(1 + (f/f_c)^2)$ and the output spectrum takes the filter's shape:

```plot
{"title": "White noise shaped by an LTI low-pass: S_Y(f) = |H(f)|^2 N0/2", "xLabel": "frequency f", "yLabel": "S_Y(f)", "xRange": [-4, 4], "yRange": [0, 0.6], "controls": [{"name": "fc", "range": [0.5, 3], "value": 1, "label": "cutoff f_c"}], "functions": [{"expr": "0.5/(1 + (x/fc)^2)", "label": "S_Y(f)", "color": "#2563eb"}, {"expr": "0.5", "label": "input white noise", "color": "#dc2626"}]}
```

This is why every receiver's noise bandwidth is set by its filters — the theme of
the Advanced track's noise and matched-filter lessons.

**Next:** the special, fully tractable family of Gaussian processes.
""",
        ),
        _t(
            "Gaussian processes",
            "11 min",
            r"""\
# Gaussian processes

A process $X(t)$ is **Gaussian** if every finite collection
$\{X(t_1), \dots, X(t_n)\}$ is **jointly Gaussian**. Jointly Gaussian RVs are
specified *entirely* by their mean vector and covariance matrix — so a Gaussian
process is fully described by just $m_X(t)$ and $R_X(t_1, t_2)$.

Three properties make them the cornerstone of the theory:

1. **WSS ⇔ SSS.** Because only first and second moments exist as free
   parameters, wide-sense stationarity implies strict-sense stationarity.
2. **Uncorrelated ⇒ independent.** For jointly Gaussian variables $\rho = 0$
   really does mean independence — the converse that fails in general.
3. **Closed under LTI filtering.** A linear system driven by a Gaussian process
   outputs a Gaussian process; only $m$ and $R$ change.

The marginal at any instant is the familiar bell curve; jointly, two instants
follow a 2-D Gaussian whose tilt is set by $\rho = R_X(\tau)/R_X(0)$:

```plot
{"title": "Marginal of a Gaussian process at one instant", "xLabel": "x", "yLabel": "density", "xRange": [-5, 5], "yRange": [0, 0.45], "functions": [{"expr": "exp(-x^2/2)/sqrt(2*pi)", "label": "f(x) = N(0, R_X(0))", "color": "#2563eb"}], "points": [{"x": 0, "y": 0, "label": "mean m_X", "color": "#dc2626", "size": 6}]}
```

Thermal noise is, to excellent approximation, a **Gaussian white** process — so
this family is not a mathematical convenience but the physics of real receivers.

**Next:** when can a single recording stand in for the whole ensemble?
""",
        ),
        _t(
            "Ergodicity & time averages",
            "10 min",
            r"""\
# Ergodicity & time averages

In practice you rarely have an ensemble of many recordings — you have **one long
sample path**. **Ergodicity** is the property that lets you replace ensemble
averages with **time averages** over that single realization.

The time average of a sample path $x(t)$ is

$$\langle x(t)\rangle = \lim_{T\to\infty} \frac{1}{2T}\int_{-T}^{T} x(t)\,dt.$$

A WSS process is **ergodic in the mean** if this time average equals the ensemble
mean $\mu_X$ for (almost) every realization:

$$\langle x(t)\rangle = E[X(t)] = \mu_X.$$

Similarly **ergodic in autocorrelation** if the time-lagged product average
recovers $R_X(\tau)$. Practically this needs the process to *mix* — distant
samples must decorrelate, i.e. $C_X(\tau) \to 0$ as $\tau \to \infty$.

```mermaid
flowchart LR
  A["One sample path x(t)"] --> B["Time average over t"]
  C["Ensemble of paths"] --> D["Ensemble average over ω"]
  B -->|"ergodic ⇒ equal"| E["μ_X, R_X(τ)"]
  D --> E
```

Ergodicity is the **bridge from theory to measurement**: it is why estimating a
spectrum from a single oscilloscope trace is legitimate. A non-ergodic
counterexample: a process with a random-but-fixed DC offset per realization —
each path's time average reports its own offset, never the ensemble mean.

**Next course:** the Advanced track applies all of this to Poisson noise, Markov
chains, physical noise, matched filters and Wiener filtering.
""",
        ),
        _quiz(),
    ),
)


# ── Random & Stochastic Processes — Advanced ─────────────────────────────────

_SP_ADVANCED = SeedCourse(
    slug="stochastic-processes-advanced",
    title="Random & Stochastic Processes — Advanced",
    description=(
        "Stochastic processes applied: Poisson processes and shot noise, Markov "
        "chains and their steady state, thermal and electronic (Johnson-Nyquist) "
        "noise with the noise-figure link, the matched filter and optimal "
        "detection, an introduction to Wiener filtering, and birth-death / "
        "queueing models. State diagrams, PSD plots and detection geometry."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Poisson processes & shot noise",
            "12 min",
            r"""\
# Poisson processes & shot noise

A **Poisson process** counts random arrivals (photons, electrons, packets) with
rate $\lambda$. The number $N(t)$ in an interval of length $t$ is Poisson:

$$P\{N(t) = k\} = \frac{(\lambda t)^k}{k!}\,e^{-\lambda t}, \qquad E[N(t)] = \operatorname{Var}[N(t)] = \lambda t.$$

Two defining features: **independent increments** (disjoint intervals are
independent) and **exponential inter-arrival times** with mean $1/\lambda$ —
memoryless waiting.

**Shot noise** is the current produced when discrete charges arrive as a Poisson
process: $i(t) = \sum_k q\, h(t - t_k)$. **Campbell's theorem** gives its mean and
variance, and the key engineering result is the **flat (white) low-frequency
PSD**:

$$S_i(f) = q\, I_{\text{dc}} \quad\text{(one-sided)}, \qquad \overline{i_n^2} = 2 q\, I_{\text{dc}}\, B,$$

where $I_{\text{dc}} = q\lambda$ is the average current and $B$ the bandwidth.
Shot noise scales with the DC current — fewer, larger charge packets are noisier
per amp.

The Poisson PMF for a few rates (drawn as a smooth envelope here):

```plot
{"title": "Poisson arrival statistics: spread grows with rate λt", "xLabel": "count k", "yLabel": "P(N=k) envelope", "xRange": [0, 16], "yRange": [0, 0.45], "controls": [{"name": "lt", "range": [1, 9], "value": 3, "label": "λt"}], "functions": [{"expr": "exp(-(x-lt)^2/(2*lt))/sqrt(2*pi*lt)", "label": "Poisson(λt) envelope", "color": "#2563eb"}], "points": [{"xExpr": "lt", "y": 0, "label": "mean = variance = λt", "color": "#dc2626", "size": 6}]}
```

**Next:** processes with memory of one step — Markov chains.
""",
        ),
        _t(
            "Markov chains & steady state",
            "12 min",
            r"""\
# Markov chains & steady state

A **Markov chain** is a process whose future depends on the present state only,
not the full history — the **Markov property**:

$$P\{X_{n+1} = j \mid X_n = i, \dots, X_0\} = P\{X_{n+1} = j \mid X_n = i\} = P_{ij}.$$

The one-step **transition matrix** $P = [P_{ij}]$ has nonnegative rows summing to
1. A two-state chain (think a channel that is *Good* or *Bad*):

```mermaid
stateDiagram-v2
  [*] --> Good
  Good --> Good: 0.8
  Good --> Bad: 0.2
  Bad --> Bad: 0.6
  Bad --> Good: 0.4
```

The state distribution evolves as $\boldsymbol\pi_{n+1} = \boldsymbol\pi_n P$.
For an irreducible, aperiodic chain it converges to a unique **stationary
distribution** $\boldsymbol\pi$ satisfying

$$\boldsymbol\pi = \boldsymbol\pi P, \qquad \sum_i \pi_i = 1.$$

For the chain above, balance gives $\pi_{\text{Good}} = 0.4/(0.2 + 0.4) = 2/3$
and $\pi_{\text{Bad}} = 1/3$: in the long run the channel is Good two-thirds of
the time, regardless of where it started. The convergence of the Good-state
probability from two different starts:

```plot
{"title": "Markov chain converges to steady state π_Good = 2/3", "xLabel": "step n", "yLabel": "P(Good at step n)", "xRange": [0, 12], "yRange": [0, 1.1], "functions": [{"expr": "0.6667 + 0.3333*(0.4)^x", "label": "start in Good", "color": "#2563eb"}, {"expr": "0.6667 - 0.6667*(0.4)^x", "label": "start in Bad", "color": "#dc2626"}, {"expr": "0.6667", "label": "steady state 2/3", "color": "#16a34a"}]}
```

**Next:** the physical noise that real circuits inject.
""",
        ),
        _t(
            "Thermal & electronic noise",
            "12 min",
            r"""\
# Thermal & electronic noise

Real devices add noise from physics, not bad design. **Thermal
(Johnson-Nyquist) noise** comes from the random thermal motion of charge carriers
in any resistor at temperature $T$. Its open-circuit voltage PSD is essentially
white over all useful frequencies:

$$\overline{v_n^2} = 4 k_B T R\, B, \qquad \overline{i_n^2} = \frac{4 k_B T B}{R},$$

with $k_B = 1.38\times10^{-23}\,\text{J/K}$, $R$ the resistance and $B$ the
bandwidth. The **available noise power** is beautifully simple — independent of
$R$:

$$P_{\text{avail}} = k_B T B.$$

At room temperature this is $-174\ \text{dBm/Hz}$, the noise floor every RF
engineer memorises. Thermal noise is **Gaussian and white**, so the
Intermediate-track LTI tools apply directly: a filter of noise bandwidth $B$
passes power $k_B T B$.

**Noise figure** measures how much a stage degrades the signal-to-noise ratio:

$$F = \frac{\mathrm{SNR}_{\text{in}}}{\mathrm{SNR}_{\text{out}}}, \qquad NF = 10\log_{10} F \ \text{dB}.$$

A noiseless stage has $F = 1$ (0 dB); any real amplifier adds its own
$\overline{v_n^2}$ and so $F > 1$. Cascaded stages follow **Friis' formula**, where
the first stage dominates — hence the low-noise amplifier comes first.

Noise power grows linearly with bandwidth (and with temperature):

```plot
{"title": "Thermal noise power P = kT·B grows with bandwidth", "xLabel": "bandwidth B (arb. units)", "yLabel": "noise power (arb.)", "xRange": [0, 10], "yRange": [0, 12], "controls": [{"name": "T", "range": [0.5, 2], "value": 1, "label": "temperature factor"}], "functions": [{"expr": "T*x", "label": "P = kT·B", "color": "#2563eb"}]}
```

**Next:** how to pull a known signal out of this white noise optimally.
""",
        ),
        _t(
            "The matched filter & optimal detection",
            "12 min",
            r"""\
# The matched filter & optimal detection

Given a known pulse $s(t)$ buried in additive **white** Gaussian noise of PSD
$N_0/2$, which linear filter maximises the output **signal-to-noise ratio** at
the sampling instant? The answer is the **matched filter**:

$$h(t) = s(T - t), \qquad H(f) = S^*(f)\,e^{-j 2\pi f T}.$$

It is the time-reversed, delayed copy of the signal. The peak SNR it achieves
depends only on the signal **energy** $E = \int s^2(t)\,dt$, not the pulse shape:

$$\left(\frac{S}{N}\right)_{\max} = \frac{2E}{N_0}.$$

Equivalently the matched filter **correlates** the received waveform against the
known template. This sets up **optimal detection**: with two equally likely
signals $s_0, s_1$ in Gaussian noise, the minimum-error rule compares against a
threshold midway between them, and the bit-error probability is

$$P_e = Q\!\left(\frac{d}{2\sigma}\right),$$

a $Q$-function of the distance $d$ between the signal points over the noise
$\sigma$. More separation or less noise drives $P_e$ down fast:

```plot
{"title": "Detection error vs signal separation d/(2σ)", "xLabel": "d/(2σ)", "yLabel": "error probability P_e", "xRange": [0, 5], "yRange": [0, 0.55], "functions": [{"expr": "0.5*exp(-x^2/2)", "label": "P_e ≈ Q(d/2σ)", "color": "#dc2626"}], "points": [{"x": 0, "y": 0.5, "label": "no separation: P_e = 0.5", "color": "#2563eb", "size": 6}]}
```

```mermaid
flowchart LR
  R["Received r(t) = s(t) + noise"] --> M["Matched filter h(t)=s(T-t)"]
  M --> S["Sample at t = T"]
  S --> D["Compare to threshold"]
  D --> O["Decision"]
```

**Next:** estimating a signal, not just detecting it — Wiener filtering.
""",
        ),
        _t(
            "Wiener filtering intro",
            "11 min",
            r"""\
# Wiener filtering intro

The matched filter *detects* a known pulse; the **Wiener filter** *estimates* a
random signal $X(t)$ from a noisy observation $Y(t) = X(t) + N(t)$, minimising
the **mean-squared error** $E[(X - \hat X)^2]$.

For WSS signal and noise that are uncorrelated, the optimal (non-causal)
frequency response is a ratio of power spectral densities:

$$H(f) = \frac{S_X(f)}{S_X(f) + S_N(f)}.$$

Read it as a **frequency-by-frequency trust gauge**:
- Where the signal dominates ($S_X \gg S_N$), $H \approx 1$ — pass it through.
- Where noise dominates ($S_X \ll S_N$), $H \approx 0$ — suppress it.

It is the optimal smoother and the ancestor of the Kalman filter (its causal,
state-space recursive cousin). With a low-pass signal spectrum and white noise,
the Wiener filter naturally becomes a low-pass that follows the signal's
own band — vary the noise level and watch it tighten:

```plot
{"title": "Wiener filter gain H(f) = S_X / (S_X + S_N)", "xLabel": "frequency f", "yLabel": "|H(f)|", "xRange": [-4, 4], "yRange": [0, 1.1], "controls": [{"name": "sn", "range": [0.1, 2], "value": 0.3, "label": "noise PSD level S_N"}], "functions": [{"expr": "(1/(1+x^2))/((1/(1+x^2)) + sn)", "label": "|H(f)|", "color": "#2563eb"}], "points": [{"x": 0, "y": 1, "label": "passband: signal trusted", "color": "#16a34a", "size": 6}]}
```

**Next:** processes that grow and shrink — birth-death and queues.
""",
        ),
        _t(
            "Queueing & birth-death processes",
            "11 min",
            r"""\
# Queueing & birth-death processes

A **birth-death process** is a continuous-time Markov chain on the integers
$0, 1, 2, \dots$ where the state (a population, or queue length) moves only to a
neighbour: up by a **birth** at rate $\lambda$, down by a **death** at rate
$\mu$.

```mermaid
stateDiagram-v2
  [*] --> S0
  S0 --> S1: λ
  S1 --> S0: μ
  S1 --> S2: λ
  S2 --> S1: μ
  S2 --> S3: λ
  S3 --> S2: μ
```

The classic **M/M/1 queue** — Poisson (Markov) arrivals at rate $\lambda$,
exponential service at rate $\mu$, one server — is exactly this with constant
rates. Define the **utilisation** $\rho = \lambda/\mu$. For stability we need
$\rho < 1$, and the steady-state queue-length distribution is geometric:

$$\pi_n = (1 - \rho)\,\rho^n, \qquad L = E[\text{in system}] = \frac{\rho}{1 - \rho}.$$

**Little's law** ties average number to average delay: $L = \lambda W$, where $W$
is the mean time in system. The headline behaviour: as $\rho \to 1$ the queue
**blows up** — delay grows without bound long before the server is fully busy:

```plot
{"title": "M/M/1 mean number in system L = ρ/(1-ρ)", "xLabel": "utilisation ρ", "yLabel": "L (jobs in system)", "xRange": [0, 0.95], "yRange": [0, 20], "functions": [{"expr": "x/(1-x)", "label": "L = ρ/(1-ρ)", "color": "#2563eb"}], "points": [{"x": 0.9, "y": 9, "label": "ρ=0.9 ⇒ L=9", "color": "#dc2626", "size": 6}]}
```

This is why systems are sized for headroom: the cost of the last few percent of
utilisation is paid in unbounded delay.

**This completes the track** — from a single random variable to Poisson noise,
Markov queues, physical noise floors and optimal filters.
""",
        ),
        _quiz(),
    ),
)


STOCHASTIC_PROCESSES_COURSES = (_SP_BASICS, _SP_INTERMEDIATE, _SP_ADVANCED)
