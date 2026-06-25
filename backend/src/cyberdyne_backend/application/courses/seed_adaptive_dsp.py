"""Adaptive & Array Signal Processing track: Basics -> Intermediate -> Advanced.

Advanced DSP that *learns* and *steers*. From a recap of correlation, the FFT and
random signals, through optimal (Wiener) filtering and the mean-square-error
surface, into adaptive filters (LMS, NLMS, RLS) and their applications (noise /
echo cancellation, equalization), and finally to spatial processing with sensor
arrays: beamforming, MVDR/LCMV, MUSIC/ESPRIT and high-resolution spectral
estimation. Builds on the Digital Signal Processing and Statistical Inference
tracks. Lessons are `text` with LaTeX, interactive ```plot blocks and ```mermaid
block diagrams of the adaptive-filter loop and beamformer.
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, μ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Adaptive & Array Signal Processing — Basics ──────────────────────────────

_AD_BASICS = SeedCourse(
    slug="adaptive-dsp-basics",
    title="Adaptive & Array Signal Processing — Basics",
    description=(
        "The foundations of filters that learn. A focused recap of correlation, "
        "the FFT and random signals & power spectra, then optimal Wiener "
        "filtering via the normal equations, the mean-square-error surface and "
        "gradient descent, and finally why and where we make filters adaptive "
        "(noise / echo cancellation, equalization). Interactive error-surface and "
        "convergence plots plus an adaptive-loop block diagram."
    ),
    level="Beginner",
    lessons=(
        _t(
            "DSP, correlation & the FFT recap",
            "10 min",
            """\
# DSP, correlation & the FFT recap

Before a filter can *adapt*, we need the fixed tools it adapts. This course
assumes the [[Digital Signal Processing]] basics; here is the slice we lean on.

**Discrete signals & LTI filters.** A signal is a sequence $x[n]$. A linear
time-invariant filter is fully described by its impulse response $h[n]$, and its
output is the **convolution**

$$y[n] = \\sum_{k} h[k]\\,x[n-k].$$

An **FIR filter** of length $M$ just weights the last $M$ inputs:
$y[n] = \\sum_{k=0}^{M-1} w_k\\,x[n-k] = \\mathbf{w}^\\mathsf{T}\\mathbf{x}[n]$. Adaptive
filters are almost always FIR, because the weights $\\mathbf{w}$ are exactly what
we will *learn*.

**Correlation.** The **cross-correlation** $r_{xy}[\\ell]=\\mathbb{E}\\{x[n]\\,y[n-\\ell]\\}$
measures how much two signals line up at lag $\\ell$; the **autocorrelation**
$r_{xx}[\\ell]$ is a signal with itself. Correlation is the language of optimal
filtering — the normal equations are built entirely from $r_{xx}$ and $r_{xy}$.

**The FFT.** The Discrete Fourier Transform turns $N$ samples into $N$ frequency
bins, $X[k]=\\sum_n x[n]e^{-j2\\pi kn/N}$, and the **FFT** computes it in
$O(N\\log N)$. We use it to *look at* what a signal and a filter do in frequency —
e.g. the magnitude response of a length-$M$ moving-average filter, whose nulls
march across the band:

```plot
{"title": "Magnitude response of a length-M moving-average FIR filter", "xLabel": "normalized frequency (×π rad/sample)", "yLabel": "|H|", "xRange": [0.01, 3.14], "yRange": [0, 1.05], "controls": [{"name": "M", "range": [2, 12], "value": 5, "step": 1, "label": "filter length M"}], "functions": [{"expr": "abs(sin(M*x/2)/(M*sin(x/2)))", "label": "|H(ω)|", "color": "#2563eb"}]}
```

That $\\dfrac{\\sin(M\\omega/2)}{M\\sin(\\omega/2)}$ shape — a **Dirichlet kernel** —
reappears as an array beam pattern later in the course; spatial and temporal
processing share the same mathematics.

**Next:** random signals and their power spectra.
""",
        ),
        _t(
            "Random signals & power spectra recap",
            "10 min",
            """\
# Random signals & power spectra recap

Real inputs — speech, noise, interference — are **random signals**, so we describe
them statistically (building on [[Statistical Inference]] and probability).

**Stationarity & moments.** A signal is **wide-sense stationary (WSS)** if its
mean is constant and its autocorrelation $r_{xx}[\\ell]=\\mathbb{E}\\{x[n]x[n-\\ell]\\}$
depends only on the lag $\\ell$, not on absolute time. Then:

- $r_{xx}[0]=\\mathbb{E}\\{x^2[n]\\}$ is the **power** of the signal.
- $r_{xx}[\\ell]$ tells us how predictable the signal is from its past — the basis
  of every adaptive predictor.

**The power spectral density (PSD).** The Wiener–Khinchin theorem says the PSD is
the Fourier transform of the autocorrelation:

$$S_{xx}(\\omega)=\\sum_{\\ell} r_{xx}[\\ell]\\,e^{-j\\omega\\ell}.$$

**White noise** has $r_{xx}[\\ell]=\\sigma^2\\delta[\\ell]$ — flat PSD, no structure to
exploit. **Coloured** signals have peaked spectra: a narrowband interferer is a
spike, and a first-order AR process $x[n]=a\\,x[n-1]+e[n]$ has the smooth
low-pass PSD below. Slide the pole $a$ toward 1 and watch the spectrum sharpen:

```plot
{"title": "Power spectrum of an AR(1) signal x[n]=a·x[n−1]+e[n]", "xLabel": "frequency ω", "yLabel": "S(ω)", "xRange": [0.01, 3.14], "yRange": [0, 12], "controls": [{"name": "a", "range": [0, 0.9], "value": 0.6, "label": "pole a"}], "functions": [{"expr": "1/(1 - 2*a*cos(x) + a^2)", "label": "S(ω)", "color": "#2563eb"}]}
```

Adaptive filters exploit exactly this structure: the more coloured the input, the
more there is to predict — and, as we will see, the harder the error surface.

**Next:** the optimal filter for a known spectrum — the Wiener filter.
""",
        ),
        _t(
            "Optimal Wiener filtering & the normal equations",
            "11 min",
            """\
# Optimal Wiener filtering & the normal equations

Suppose we want an FIR filter $\\mathbf{w}$ whose output $y[n]=\\mathbf{w}^\\mathsf{T}\\mathbf{x}[n]$
best matches a **desired signal** $d[n]$. "Best" means minimum **mean-square
error** (MSE):

$$J(\\mathbf{w}) = \\mathbb{E}\\{e^2[n]\\}, \\qquad e[n] = d[n] - \\mathbf{w}^\\mathsf{T}\\mathbf{x}[n].$$

Expanding the square gives a clean quadratic in $\\mathbf{w}$:

$$J(\\mathbf{w}) = \\sigma_d^2 - 2\\,\\mathbf{w}^\\mathsf{T}\\mathbf{p} + \\mathbf{w}^\\mathsf{T}\\mathbf{R}\\,\\mathbf{w},$$

where $\\mathbf{R}=\\mathbb{E}\\{\\mathbf{x}\\mathbf{x}^\\mathsf{T}\\}$ is the input
**autocorrelation matrix** (built from $r_{xx}$) and
$\\mathbf{p}=\\mathbb{E}\\{d\\,\\mathbf{x}\\}$ is the **cross-correlation vector**
(built from $r_{dx}$).

**The normal equations.** Setting the gradient to zero, $\\nabla J = -2\\mathbf{p} + 2\\mathbf{R}\\mathbf{w}=0$,
gives the **Wiener–Hopf** solution:

$$\\boxed{\\;\\mathbf{R}\\,\\mathbf{w}_{\\!o} = \\mathbf{p} \\quad\\Longrightarrow\\quad \\mathbf{w}_{\\!o}=\\mathbf{R}^{-1}\\mathbf{p}.\\;}$$

This is the gold standard: the single best linear filter, expressed purely in
correlations. The minimum error is $J_{\\min}=\\sigma_d^2-\\mathbf{p}^\\mathsf{T}\\mathbf{w}_{\\!o}$.

**Why we still need to adapt.** Computing $\\mathbf{w}_{\\!o}$ needs $\\mathbf{R}$ and
$\\mathbf{p}$ in advance — i.e. the statistics — and inverting $\\mathbf{R}$. In the
real world the statistics are unknown and *changing*. Adaptive algorithms find
$\\mathbf{w}_{\\!o}$ **from data, online, without inverting anything** — they are
iterative solvers for the normal equations.

**Next:** picture the cost we are minimising — the MSE surface.
""",
        ),
        _t(
            "The mean-square-error surface & gradient descent",
            "11 min",
            """\
# The mean-square-error surface & gradient descent

Because $J(\\mathbf{w})$ is a **quadratic** in the weights, its graph is a
**bowl** (a paraboloid). With one weight it is a parabola; with two it is an
elliptical bowl whose single minimum is the Wiener solution $\\mathbf{w}_{\\!o}$.
The bowl's shape is set entirely by $\\mathbf{R}$: its **eigenvalues** are the
curvatures along the principal axes.

Here is a 1-D slice of the bowl. The minimum sits at $w_o$; the curvature is the
input power. Slide the candidate weight and read off the error:

```plot
{"title": "MSE surface J(w): a quadratic bowl with minimum at the Wiener weight", "xLabel": "filter weight w", "yLabel": "J(w) = mean-square error", "xRange": [-3, 5], "yRange": [0, 12], "controls": [{"name": "w", "range": [-3, 5], "value": -2, "label": "candidate weight w"}], "functions": [{"expr": "1 + 1.5*(x-1)^2", "label": "J(w)", "color": "#2563eb"}], "points": [{"xExpr": "w", "yExpr": "1 + 1.5*(w-1)^2", "label": "current weight", "color": "#dc2626", "size": 7}, {"x": 1, "y": 1, "label": "minimum: Wiener w_o, J_min", "color": "#16a34a", "size": 6}]}
```

**Steepest descent.** To reach the bottom without inverting $\\mathbf{R}$, step
**downhill** — opposite the gradient — at each iteration:

$$\\mathbf{w}_{k+1} = \\mathbf{w}_k - \\mu\\,\\nabla J(\\mathbf{w}_k) = \\mathbf{w}_k + 2\\mu\\big(\\mathbf{p}-\\mathbf{R}\\mathbf{w}_k\\big).$$

The **step size** $\\mu$ is the whole story: too small and convergence crawls; too
large and the iterates overshoot and **diverge**. Stability requires
$0<\\mu<\\dfrac{1}{\\lambda_{\\max}}$ (with $\\lambda_{\\max}$ the largest eigenvalue of
$\\mathbf{R}$), and the *slowest* mode converges at a rate set by the
**eigenvalue spread** $\\lambda_{\\max}/\\lambda_{\\min}$ — i.e. by how coloured the
input is. The error falls geometrically toward $J_{\\min}$:

```plot
{"title": "Steepest descent: error decays toward J_min each iteration", "xLabel": "iteration k", "yLabel": "excess MSE J(k) − J_min", "xRange": [0, 40], "yRange": [0, 10], "controls": [{"name": "rate", "range": [0.05, 0.6], "value": 0.2, "label": "convergence rate (∝ μ)"}], "functions": [{"expr": "10*exp(-rate*x)", "label": "J(k) − J_min", "color": "#2563eb"}]}
```

Steepest descent still needs $\\mathbf{R}$ and $\\mathbf{p}$. The **adaptive** trick
of the next course is to replace them with cheap *instantaneous* estimates from
the live data.

**Next:** what "adaptive" actually buys us.
""",
        ),
        _t(
            "Introduction to adaptive filtering",
            "10 min",
            """\
# Introduction to adaptive filtering

An **adaptive filter** adjusts its own weights, sample by sample, to minimise an
error — *without anyone supplying the statistics in advance*. It is the union of a
filter and a feedback loop.

**Why adapt at all?**

- **Unknown statistics.** We rarely know $\\mathbf{R}$ and $\\mathbf{p}$ ahead of
  time. The filter estimates them implicitly from the data.
- **Non-stationarity.** Channels, rooms and interference *change*. A fixed
  optimal filter goes stale; an adaptive one **tracks** the moving optimum.
- **Simplicity.** No matrix inversion, no offline training pass — just an update
  rule running in real time on a DSP or microcontroller.

**The canonical loop.** Every adaptive filter wires up the same four blocks: take
an input $\\mathbf{x}[n]$, filter it to get $y[n]$, compare to the desired $d[n]$
to form the error $e[n]=d[n]-y[n]$, and feed $e[n]$ back to nudge the weights:

```mermaid
flowchart LR
    X["input x[n]"] --> F["adaptive FIR filter w[n]"]
    F --> Y["output y[n]"]
    D["desired d[n]"] --> SUM(("Σ −"))
    Y --> SUM
    SUM --> E["error e[n]"]
    E --> ADAPT["adaptation rule: update w[n] from x[n], e[n]"]
    ADAPT -. "adjust weights" .-> F
```

The genius is in choosing $d[n]$. There is no labelled "truth" lying around — yet
in each application we can *construct* a desired signal from the wiring of the
problem (a reference microphone, a known training symbol, a delayed copy of the
input). Pick $d[n]$ well and the same loop solves wildly different problems.

**Two regimes.** A filter is in **acquisition** while it converges from scratch,
then in **tracking** as it follows slow changes. Step size trades the two:
big $\\mu$ acquires and tracks fast but leaves more residual error
(**misadjustment**); small $\\mu$ is precise but sluggish.

**Next:** the map of where this loop gets used.
""",
        ),
        _t(
            "Applications map: where adaptive filters live",
            "10 min",
            """\
# Applications map: where adaptive filters live

The same loop, rewired four ways. The art is always: *what plays the role of the
desired signal $d[n]$?*

**1. System identification.** Drive an unknown system and the adaptive filter in
parallel with the same input; let the system's output be $d[n]$. The filter
**converges to a model** of the unknown system — the basis of echo-path modelling
and plant identification in control.

**2. Adaptive noise cancellation.** A primary mic hears *signal + noise*; a
reference mic hears a *correlated copy of the noise alone*. Use the noisy mix as
$d[n]$ and the reference as the input. The filter learns to predict the noise
component and subtracts it, leaving the signal — used in headsets, fetal-ECG
extraction and engine-cabin noise control.

**3. Echo cancellation.** In a phone or conference call, your speaker leaks into
your mic (acoustic echo) or hybrids reflect the line (line echo). Feed the
*outgoing* signal through an adaptive filter that models the echo path; subtract
its output from the mic. The far end stops hearing themselves.

**4. Channel equalization.** A communication channel smears symbols together
(**inter-symbol interference**). An adaptive **equalizer** at the receiver inverts
the channel; during a known **training** sequence the transmitted symbols are
$d[n]$, after which it switches to **decision-directed** mode and tracks drift.

A compact taxonomy by what supplies $d[n]$:

| Application | Input $\\mathbf{x}[n]$ | Desired $d[n]$ | Filter learns |
|---|---|---|---|
| System ID | probe signal | unknown system's output | the system |
| Noise cancellation | reference noise | signal + noise | the noise path |
| Echo cancellation | outgoing signal | mic (echo + near speech) | the echo path |
| Equalization | received samples | training / decisions | the channel inverse |

All four are revisited in depth in the Intermediate course. They all reduce to:
**minimise $\\mathbb{E}\\{e^2[n]\\}$ online.**

**Next:** check what you've learned, then on to the LMS algorithm.
""",
        ),
        _quiz(),
    ),
)

# ── Adaptive & Array Signal Processing — Intermediate ────────────────────────

_AD_INTERMEDIATE = SeedCourse(
    slug="adaptive-dsp-intermediate",
    title="Adaptive & Array Signal Processing — Intermediate",
    description=(
        "The adaptive-filter algorithms, in depth. The LMS update and its step-"
        "size / convergence trade-offs, normalized LMS and robust variants, and "
        "the fast-converging RLS algorithm with its cost. Then the three classic "
        "applications worked end to end: adaptive noise cancellation, acoustic "
        "echo cancellation, and adaptive equalization with channel tracking. "
        "Interactive convergence plots and a noise-canceller block diagram."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The LMS algorithm",
            "12 min",
            """\
# The LMS algorithm

**Least Mean Squares** (Widrow–Hoff, 1960) is the workhorse adaptive algorithm. It
is steepest descent with the cheapest possible gradient estimate: replace the
*expected* gradient $-2(\\mathbf{p}-\\mathbf{R}\\mathbf{w})$ with its **instantaneous**
value at this one sample, $-2\\,e[n]\\,\\mathbf{x}[n]$. The update is three lines:

$$y[n] = \\mathbf{w}^\\mathsf{T}[n]\\,\\mathbf{x}[n], \\qquad e[n]=d[n]-y[n],$$
$$\\boxed{\\;\\mathbf{w}[n+1] = \\mathbf{w}[n] + \\mu\\,e[n]\\,\\mathbf{x}[n].\\;}$$

That is the whole algorithm: $O(M)$ multiplies per sample, no matrix anywhere. It
is a stochastic-gradient method — the same idea that trains neural nets — and the
direct ancestor of the LMS used in millions of modems and headsets.

**Step size & convergence.** $\\mu$ governs everything. For the mean weight to
converge, $0<\\mu<\\dfrac{2}{\\lambda_{\\max}}$, and a safe practical bound is
$0<\\mu<\\dfrac{2}{M\\,\\mathbb{E}\\{x^2\\}}$ (inversely proportional to input power and
filter length). The catch with the noisy gradient is **misadjustment**: the
weights never quite settle, they jitter around $\\mathbf{w}_{\\!o}$, leaving an excess
MSE $\\approx \\mu M \\sigma_x^2 J_{\\min}/2$. So:

- **Large $\\mu$** → fast convergence, but more misadjustment (noisier solution).
- **Small $\\mu$** → low residual error, but slow convergence and slow tracking.

Watch the learning curve trade speed against the noise floor — bigger $\\mu$ drops
faster but settles higher:

```plot
{"title": "LMS learning curve: large μ converges fast but to a higher error floor", "xLabel": "iteration n", "yLabel": "mean-square error J(n)", "xRange": [0, 120], "yRange": [0, 10], "controls": [{"name": "mu", "range": [0.02, 0.4], "value": 0.12, "label": "step size μ"}], "functions": [{"expr": "9*exp(-mu*x) + 12*mu", "label": "J(n)", "color": "#2563eb"}], "points": [{"x": 0, "y": 9, "label": "start", "color": "#dc2626", "size": 6}]}
```

The notch in the curve at the right is the misadjustment floor $\\propto \\mu$ — you
can see it rise as you push $\\mu$ up. Eigenvalue spread (coloured input) stretches
the curve out further. The next lesson fixes the most fragile part: the
dependence on input power.

**Next:** normalize the step size.
""",
        ),
        _t(
            "Normalized LMS & variants",
            "10 min",
            """\
# Normalized LMS & variants

Plain LMS has a flaw: the stable range of $\\mu$ depends on the **input power**,
which we may not know and which changes (think speech — loud then quiet). Pick
$\\mu$ for loud passages and it crawls on quiet ones; pick it for quiet and it
**diverges** when the input gets loud.

**Normalized LMS (NLMS).** Divide the step by the current input energy so the
*effective* step is power-independent:

$$\\mathbf{w}[n+1] = \\mathbf{w}[n] + \\frac{\\tilde\\mu}{\\;\\varepsilon + \\|\\mathbf{x}[n]\\|^2\\;}\\;e[n]\\,\\mathbf{x}[n].$$

Now $\\tilde\\mu$ is **dimensionless** and stability is simply $0<\\tilde\\mu<2$
(with $\\tilde\\mu\\approx 1$ a good default). The small constant $\\varepsilon$ guards
against dividing by zero during silence. NLMS converges faster than LMS for
non-stationary, time-varying-power inputs and is the version actually deployed in
most echo cancellers.

**Other useful variants:**

- **Sign-LMS / sign-error / sign-sign** — replace $e$ or $\\mathbf{x}$ by their sign.
  Cheaper (no multiplies) and more robust to impulsive noise; used in
  ultra-low-power hardware.
- **Leaky LMS** — add a tiny decay, $\\mathbf{w}[n+1]=(1-\\mu\\gamma)\\mathbf{w}[n]+\\mu e\\mathbf{x}$.
  Prevents weight drift when the input lacks excitation.
- **Variable step size** — start big to acquire, shrink to refine; a scheduled or
  error-driven $\\mu$ gets the best of both worlds.
- **Block / frequency-domain LMS** — process a block via the FFT, slashing cost
  for long filters (room echo paths can be thousands of taps).

NLMS curing the power sensitivity is shown below — the same effective rate at two
very different input levels:

```plot
{"title": "NLMS: same effective convergence at very different input powers", "xLabel": "iteration n", "yLabel": "mean-square error J(n)", "xRange": [0, 80], "yRange": [0, 10], "functions": [{"expr": "9*exp(-0.09*x) + 0.4", "label": "loud input (NLMS)", "color": "#2563eb"}, {"expr": "9*exp(-0.085*x) + 0.4", "label": "quiet input (NLMS)", "color": "#16a34a"}]}
```

NLMS is the safe default. When you need the *fastest possible* convergence
regardless of cost, you reach for RLS.

**Next:** the RLS algorithm.
""",
        ),
        _t(
            "The RLS algorithm",
            "12 min",
            """\
# The RLS algorithm

**Recursive Least Squares** takes a different stance from LMS. Instead of chasing
the *expected* error with a noisy gradient, it **exactly** minimises the
accumulated weighted least-squares error at every step:

$$J[n] = \\sum_{i=0}^{n} \\lambda^{\\,n-i}\\,\\big(d[i]-\\mathbf{w}^\\mathsf{T}[n]\\mathbf{x}[i]\\big)^2,$$

where $0<\\lambda\\le 1$ is the **forgetting factor** that down-weights old data
(a memory of $\\approx 1/(1-\\lambda)$ samples). RLS keeps a running inverse of the
correlation matrix, $\\mathbf{P}[n]\\approx\\mathbf{R}^{-1}$, and updates it via the
matrix-inversion lemma — effectively solving the normal equations recursively:

$$\\mathbf{k}[n]=\\frac{\\mathbf{P}[n-1]\\mathbf{x}[n]}{\\lambda+\\mathbf{x}^\\mathsf{T}[n]\\mathbf{P}[n-1]\\mathbf{x}[n]},\\quad
\\mathbf{w}[n]=\\mathbf{w}[n-1]+\\mathbf{k}[n]\\,e[n].$$

**The pay-off: speed.** RLS converges in roughly $2M$ iterations — essentially
*independent of the eigenvalue spread* that cripples LMS on coloured inputs.
Where LMS crawls, RLS snaps to the optimum:

```plot
{"title": "RLS converges in ~2M iterations vs LMS's eigenvalue-limited crawl", "xLabel": "iteration n", "yLabel": "mean-square error J(n)", "xRange": [0, 120], "yRange": [0, 10], "functions": [{"expr": "9*exp(-0.06*x) + 0.3", "label": "LMS (slow on coloured input)", "color": "#94a3b8"}, {"expr": "9*exp(-0.45*x) + 0.3", "label": "RLS (fast, spread-insensitive)", "color": "#2563eb"}]}
```

**The cost.** Nothing is free:

- **Computation** — $O(M^2)$ per sample versus LMS's $O(M)$. For long filters this
  is the difference between feasible and not.
- **Numerical stability** — the $\\mathbf{P}$ recursion can lose symmetry / positive-
  definiteness and blow up; production code uses **square-root / QR-RLS** forms.
- **Memory** — the $M\\times M$ matrix $\\mathbf{P}$.

**Rule of thumb:** LMS/NLMS for cheap, long, well-behaved problems; RLS when fast
convergence or tracking of fast changes justifies the quadratic cost.

**Next:** put LMS to work cancelling noise.
""",
        ),
        _t(
            "Adaptive noise cancellation",
            "11 min",
            """\
# Adaptive noise cancellation

The classic Widrow application. We want a clean signal $s[n]$ but only ever
measure it **corrupted by noise** $v_0[n]$. The trick: get a second sensor near
the noise source that picks up a *correlated* version $v_1[n]$ of the noise but
(ideally) none of the signal.

- **Primary input** $d[n] = s[n] + v_0[n]$ — signal plus noise.
- **Reference input** $x[n] = v_1[n]$ — noise only, correlated with $v_0$.

The adaptive filter learns the transfer path from $v_1$ to $v_0$, so its output
$y[n]\\approx v_0[n]$. The **error** $e[n]=d[n]-y[n]\\approx s[n]$ is the cleaned
signal — and, beautifully, the error *is* the output we keep:

```mermaid
flowchart LR
    S["signal source s[n]"] --> PRIM(("Σ +"))
    N["noise source"] --> V0["noise path → v0[n]"]
    V0 --> PRIM
    PRIM --> D["primary d[n] = s[n] + v0[n]"]
    N --> V1["reference sensor → v1[n]"]
    V1 --> W["adaptive filter w[n]"]
    W --> Y["y[n] ≈ v0[n]"]
    D --> SUB(("Σ −"))
    Y --> SUB
    SUB --> E["e[n] ≈ s[n]  (clean output)"]
    E -. "error drives adaptation" .-> W
```

**Why minimising $e^2$ cleans the signal.** Since $s$ is uncorrelated with the
noise, the filter cannot reduce $\\mathbb{E}\\{e^2\\}$ by touching $s$; the only way
down is to cancel $v_0$ using $v_1$. At the optimum the residual noise is driven to
its floor and the signal passes through untouched.

**Real uses:** noise-cancelling headsets (reference = external mic), fetal-ECG
recovery (reference = maternal-ECG lead), 50/60 Hz hum removal (reference = a tap
off the mains), and cancelling engine noise in a cockpit.

**Pitfalls:** if the reference also contains *signal* leakage, the filter cancels
part of the signal too (signal distortion); and the reference must genuinely be
correlated with the noise — an uncorrelated reference does nothing.

**Next:** the same idea against acoustic echo.
""",
        ),
        _t(
            "Adaptive echo cancellation",
            "11 min",
            """\
# Adaptive echo cancellation

In hands-free calling, your loudspeaker plays the *far-end* speech and your
microphone picks it back up after bouncing around the room — the far end hears
themselves a fraction of a second later. **Acoustic echo cancellation (AEC)** kills
this without muting anyone.

**The setup.** We *know* the loudspeaker signal $x[n]$ (it is the far-end signal
we are playing). The room turns it into an echo via an unknown impulse response
$h[n]$ — the **echo path**. The mic captures echo + near-end speech:

$$d[n] = \\underbrace{(h * x)[n]}_{\\text{echo}} + \\underbrace{s[n]}_{\\text{near-end speech}} + \\text{noise}.$$

An adaptive filter $\\hat{h}[n]$, driven by the known $x[n]$, **models the echo
path** and synthesises an echo replica $y[n]=\\hat h^\\mathsf{T}\\mathbf{x}[n]$. Subtract:
$e[n]=d[n]-y[n]\\to s[n]$. This is **system identification** — the filter literally
estimates the room's response.

**What makes AEC hard:**

- **Long echo paths.** A reverberant room is hundreds of milliseconds — at 16 kHz
  that is thousands of taps. Hence frequency-domain / block NLMS for efficiency.
- **Double-talk.** When the near-end speaks ($s[n]\\neq 0$) *while* echo is present,
  the near-end speech looks like a huge error and corrupts the weights. A
  **double-talk detector (DTD)** freezes adaptation during double-talk.
- **Time variation.** Someone moves, a door closes — the echo path shifts and the
  filter must re-track. NLMS handles the changing input power.
- **Residual echo.** A nonlinear **post-filter / residual echo suppressor** mops up
  what the linear filter cannot model (loudspeaker nonlinearity).

NLMS with a robust DTD is the standard recipe; the same architecture handles
**line echo** in the telephone network (the echo path is the 2-to-4-wire hybrid).

**Next:** invert the channel instead of modelling it — equalization.
""",
        ),
        _t(
            "Adaptive equalization & channel tracking",
            "12 min",
            """\
# Adaptive equalization & channel tracking

A communication channel (a copper pair, a radio link, a disk read head) spreads
each transmitted symbol over time, so symbols collide — **inter-symbol
interference (ISI)**. An **equalizer** is an adaptive filter at the receiver that
*inverts* the channel and reopens the eye.

**Two phases.**

1. **Training.** The transmitter sends a sequence both ends know. The receiver
   uses those known symbols as the desired $d[n]$ and runs LMS/RLS until the
   equalizer $\\approx C^{-1}(z)$, the channel inverse.
2. **Decision-directed tracking.** Once the eye is open, error rates are low, so
   the receiver trusts its own **hard decisions** $\\hat d[n]$ as the desired signal
   and keeps adapting — following slow channel drift (temperature, motion) with no
   further training overhead.

For higher-order constellations, **blind** equalizers (e.g. the constant-modulus
algorithm, CMA) open the eye with *no* training at all, exploiting only a known
property of the signal.

**The trade-off equalizers can't escape.** A pure inverse $1/C(z)$ does kill ISI —
but where the channel has a deep null (large attenuation), the inverse has a huge
gain, **amplifying noise** at that frequency. So the equalizer balances ISI
against noise enhancement; the **MMSE equalizer** (the Wiener solution again)
explicitly minimises their sum rather than forcing ISI to exactly zero
(**zero-forcing**). Below, the inverse's gain spikes wherever the channel dips —
slide the null depth and watch the noise-enhancement spike grow:

```plot
{"title": "Equalizer gain |1/C| spikes where the channel C has a null (noise enhancement)", "xLabel": "frequency ω", "yLabel": "magnitude", "xRange": [0.01, 3.14], "yRange": [0, 8], "controls": [{"name": "d", "range": [0.3, 0.95], "value": 0.7, "label": "channel null depth"}], "functions": [{"expr": "abs(1 - d*cos(x))", "label": "channel |C(ω)|", "color": "#94a3b8"}, {"expr": "1/abs(1 - d*cos(x))", "label": "equalizer |1/C(ω)|", "color": "#2563eb"}]}
```

**Tracking** is where adaptive equalizers earn their keep: RLS for fast-fading
links, NLMS where cost matters, DFE (decision-feedback) structures for severe ISI.

**Next:** check your knowledge, then move from time to space — sensor arrays.
""",
        ),
        _quiz(),
    ),
)

# ── Adaptive & Array Signal Processing — Advanced ────────────────────────────

_AD_ADVANCED = SeedCourse(
    slug="adaptive-dsp-advanced",
    title="Adaptive & Array Signal Processing — Advanced",
    description=(
        "Processing in space: sensor arrays. The spatial signal model and "
        "steering vectors, delay-and-sum beamforming and the array beam pattern, "
        "optimal & adaptive beamforming (MVDR / Capon and LCMV), super-resolution "
        "direction-of-arrival estimation (MUSIC, ESPRIT), high-resolution "
        "parametric / AR spectral estimation, and a capstone case study on "
        "interference nulling and source localization. Interactive beam-pattern "
        "and pseudo-spectrum plots plus a beamformer block diagram."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Sensor arrays & the spatial signal model",
            "11 min",
            """\
# Sensor arrays & the spatial signal model

So far the filter combined a signal with *past samples of itself* (taps in time).
A **sensor array** combines the *same instant across many sensors in space* — and
the maths is identical, with spatial position playing the role of time delay.

**The geometry.** Take a **uniform linear array (ULA)** of $N$ sensors spaced $d$
apart. A plane wave from angle $\\theta$ (off broadside) reaches each sensor a
little later: sensor $m$ sees an extra path $m\\,d\\sin\\theta$, i.e. a phase shift
$m\\,\\dfrac{2\\pi d}{\\lambda}\\sin\\theta$. Collect these into the **steering vector**:

$$\\mathbf{a}(\\theta) = \\big[\\,1,\\; e^{j\\phi},\\; e^{j2\\phi},\\;\\dots,\\; e^{j(N-1)\\phi}\\,\\big]^\\mathsf{T},\\qquad \\phi = \\tfrac{2\\pi d}{\\lambda}\\sin\\theta.$$

The steering vector is the spatial signature of a direction — the array's analogue
of a complex exponential in frequency.

**The data model.** With $K$ sources $s_k[n]$ arriving from angles $\\theta_k$ plus
sensor noise $\\mathbf{n}[n]$, the $N$-vector of sensor outputs is

$$\\mathbf{x}[n] = \\sum_{k=1}^{K}\\mathbf{a}(\\theta_k)\\,s_k[n] + \\mathbf{n}[n] = \\mathbf{A}\\,\\mathbf{s}[n] + \\mathbf{n}[n].$$

Everything downstream is built from the **spatial covariance matrix**
$\\mathbf{R}=\\mathbb{E}\\{\\mathbf{x}\\mathbf{x}^\\mathsf{H}\\}=\\mathbf{A}\\mathbf{R}_s\\mathbf{A}^\\mathsf{H}+\\sigma^2\\mathbf{I}$,
estimated in practice by $\\hat{\\mathbf{R}}=\\frac1L\\sum_n\\mathbf{x}[n]\\mathbf{x}^\\mathsf{H}[n]$.

**The half-wavelength rule.** Choose $d=\\lambda/2$. Larger spacing causes
**spatial aliasing** — distinct directions share a steering vector, the spatial
twin of temporal aliasing from the FFT recap. Smaller spacing wastes aperture and
worsens resolution.

The **aperture** $Nd$ sets resolution exactly as observation time sets frequency
resolution: more sensors, finer angular detail.

**Next:** the simplest way to point an array — delay-and-sum.
""",
        ),
        _t(
            "Beamforming: delay-and-sum & the beam pattern",
            "12 min",
            """\
# Beamforming: delay-and-sum & the beam pattern

A **beamformer** weights and sums the sensor outputs, $y[n]=\\mathbf{w}^\\mathsf{H}\\mathbf{x}[n]$,
to listen preferentially in one direction. The simplest choice — **delay-and-sum
(DAS)** — aligns the sensors for a **look direction** $\\theta_0$ by setting
$\\mathbf{w}=\\mathbf{a}(\\theta_0)/N$. Signals from $\\theta_0$ add coherently;
everything else partially cancels.

**The beam pattern.** Steer to broadside ($\\theta_0=0$) and the array response
versus angle is the familiar **array factor** — the spatial Dirichlet kernel from
the FFT recap:

$$\\big|B(\\theta)\\big| = \\frac1N\\left|\\frac{\\sin(N\\psi/2)}{\\sin(\\psi/2)}\\right|,\\qquad \\psi=\\tfrac{2\\pi d}{\\lambda}\\sin\\theta.$$

It has a **mainlobe** pointing at the look direction, **nulls**, and **sidelobes**.
Add sensors ($N$) and the mainlobe narrows — sharper spatial focus and finer
resolution. Slide $N$:

```plot
{"title": "Delay-and-sum beam pattern |B|: more sensors N ⇒ narrower mainlobe", "xLabel": "spatial angle variable ψ", "yLabel": "|array factor|", "xRange": [-3.14, 3.14], "yRange": [0, 1.05], "controls": [{"name": "N", "range": [2, 12], "value": 6, "step": 1, "label": "number of sensors N"}], "functions": [{"expr": "abs(sin(N*x/2)/(N*sin(x/2)))", "label": "|B(ψ)|", "color": "#2563eb"}]}
```

**Mainlobe vs sidelobes.** Narrow mainlobe = good resolution; low sidelobes = good
rejection of off-axis interference. Uniform weights give the narrowest mainlobe but
high (−13 dB) sidelobes. **Tapering / windowing** the weights (Hamming, Chebyshev —
the same windows used on the FFT) trades a slightly wider mainlobe for *much* lower
sidelobes.

**Steering.** To look at $\\theta_0$, multiply each weight by the steering vector
$\\mathbf{a}(\\theta_0)$ — this **electronically steers** the beam with no moving
parts (phased-array radar, 5G beamforming, ultrasound, sonar).

DAS is robust and cheap but **data-independent**: its sidelobes sit wherever the
geometry puts them, even if a strong interferer happens to land on one. The fix is
to let the *data* shape the pattern.

**Next:** optimal and adaptive beamforming.
""",
        ),
        _t(
            "Optimal & adaptive beamforming (MVDR / LCMV)",
            "12 min",
            """\
# Optimal & adaptive beamforming (MVDR / LCMV)

Delay-and-sum ignores the actual interference. **Adaptive beamforming** shapes the
weights from the measured covariance $\\mathbf{R}$ to *place nulls on interferers*
while keeping the look direction intact.

**MVDR / Capon.** The **Minimum Variance Distortionless Response** beamformer
minimises total output power subject to **unit gain** toward the look direction
$\\theta_0$ — so it suppresses everything *except* the signal of interest:

$$\\min_{\\mathbf{w}}\\;\\mathbf{w}^\\mathsf{H}\\mathbf{R}\\,\\mathbf{w}\\quad\\text{s.t.}\\quad \\mathbf{w}^\\mathsf{H}\\mathbf{a}(\\theta_0)=1\\;\\;\\Longrightarrow\\;\\; \\boxed{\\;\\mathbf{w}_{\\text{MVDR}}=\\frac{\\mathbf{R}^{-1}\\mathbf{a}(\\theta_0)}{\\mathbf{a}^\\mathsf{H}(\\theta_0)\\mathbf{R}^{-1}\\mathbf{a}(\\theta_0)}.\\;}$$

It is the spatial Wiener filter — same $\\mathbf{R}^{-1}(\\cdot)$ structure as the
normal equations. The result: the mainlobe stays on $\\theta_0$ but a **deep null**
is steered onto each interferer automatically. Slide the interferer angle and watch
the adaptive pattern's null lock onto it (DAS, grey, cannot):

```plot
{"title": "Adaptive (MVDR) pattern steers a deep null onto the interferer; DAS cannot", "xLabel": "angle variable ψ", "yLabel": "|response|", "xRange": [-3.14, 3.14], "yRange": [0, 1.05], "controls": [{"name": "ji", "range": [-2.5, 2.5], "value": 1.4, "label": "interferer angle ψ_i"}], "functions": [{"expr": "abs(sin(6*x/2)/(6*sin(x/2)))", "label": "delay-and-sum (fixed)", "color": "#94a3b8"}, {"expr": "abs(sin(6*x/2)/(6*sin(x/2))) * abs(sin((x-ji)/2))", "label": "adaptive: null at interferer", "color": "#2563eb"}], "points": [{"xExpr": "ji", "y": 0, "label": "interferer", "color": "#dc2626", "size": 7}]}
```

**LCMV.** **Linearly Constrained Minimum Variance** generalises MVDR to *several*
linear constraints $\\mathbf{C}^\\mathsf{H}\\mathbf{w}=\\mathbf{f}$ — e.g. hold gain on
two friendly directions, or force exact nulls on known jammers:

$$\\mathbf{w}_{\\text{LCMV}}=\\mathbf{R}^{-1}\\mathbf{C}\\big(\\mathbf{C}^\\mathsf{H}\\mathbf{R}^{-1}\\mathbf{C}\\big)^{-1}\\mathbf{f}.$$

The **generalized sidelobe canceller (GSC)** reformulates LCMV as an *unconstrained*
adaptive filter — letting LMS/RLS from the Intermediate course run the array online.

**The catch — robustness.** MVDR is brutal when the look-direction steering vector
is even slightly wrong (array calibration error, look-angle mismatch): it can
**self-null the desired signal**. **Diagonal loading** ($\\mathbf{R}+\\gamma\\mathbf{I}$)
and robust-Capon variants tame this and are essential in practice.

**Next:** instead of steering, *estimate* the angles — DOA.
""",
        ),
        _t(
            "Direction-of-arrival estimation (MUSIC, ESPRIT)",
            "12 min",
            """\
# Direction-of-arrival estimation (MUSIC, ESPRIT)

A beamformer's angular resolution is capped by its aperture (the
**Rayleigh limit**). **Subspace methods** shatter that limit, resolving sources far
closer than a beamwidth apart — *super-resolution* DOA.

**The subspace idea.** Eigen-decompose the spatial covariance
$\\mathbf{R}=\\mathbf{A}\\mathbf{R}_s\\mathbf{A}^\\mathsf{H}+\\sigma^2\\mathbf{I}$. Its $N$
eigenvectors split into two orthogonal groups:

- a **signal subspace** — the $K$ largest eigenvalues, spanned by the source
  steering vectors $\\mathbf{a}(\\theta_k)$;
- a **noise subspace** $\\mathbf{E}_n$ — the remaining $N-K$, **orthogonal** to every
  true steering vector.

**MUSIC.** MUltiple SIgnal Classification exploits that orthogonality: a steering
vector pointing at a true source is orthogonal to $\\mathbf{E}_n$, so the
**pseudo-spectrum**

$$P_{\\text{MUSIC}}(\\theta)=\\frac{1}{\\mathbf{a}^\\mathsf{H}(\\theta)\\,\\mathbf{E}_n\\mathbf{E}_n^\\mathsf{H}\\,\\mathbf{a}(\\theta)}$$

**spikes** (denominator → 0) at each true angle. Two closely spaced sources show
two sharp peaks where a beamformer would show one blur. Slide the source
separation and watch the two MUSIC peaks resolve:

```plot
{"title": "MUSIC pseudo-spectrum: two sharp peaks resolve closely spaced sources", "xLabel": "angle θ", "yLabel": "P_MUSIC(θ)", "xRange": [-2, 2], "yRange": [0, 12], "controls": [{"name": "sep", "range": [0.15, 1.2], "value": 0.5, "label": "source separation"}], "functions": [{"expr": "1/((x-sep)^2 + 0.01) * 0.1 + 1/((x+sep)^2 + 0.01) * 0.1", "label": "P_MUSIC(θ)", "color": "#2563eb"}], "points": [{"xExpr": "sep", "y": 0, "label": "source 1", "color": "#dc2626", "size": 6}, {"xExpr": "0-sep", "y": 0, "label": "source 2", "color": "#dc2626", "size": 6}]}
```

**ESPRIT.** Estimation of Signal Parameters via Rotational Invariance Techniques
avoids the spectral *search* entirely. Split the ULA into two identical subarrays
shifted by one element; the signal subspaces of the two are related by a diagonal
matrix $\\boldsymbol{\\Phi}$ whose phases are *exactly* the DOAs. Solving a small
eigenvalue problem yields the angles in **closed form** — cheaper than MUSIC's grid
search and with no need for a calibrated array manifold.

**Caveats:** both need the **number of sources $K$** (estimated by AIC/MDL on the
eigenvalues), enough **snapshots** to estimate $\\mathbf{R}$ well, and **uncorrelated**
sources — coherent multipath collapses the signal subspace and needs *spatial
smoothing* to repair.

**Next:** the same subspace/parametric thinking, applied to frequency.
""",
        ),
        _t(
            "High-resolution spectral estimation (parametric, AR)",
            "11 min",
            """\
# High-resolution spectral estimation (parametric, AR)

The FFT periodogram from the Basics recap is simple but **resolution-limited**
(by the window length) and **noisy** (its variance doesn't shrink with more data).
**Parametric** methods do better by *assuming a model* for the signal and fitting
its few parameters — trading a modelling assumption for sharp, low-variance peaks.

**Autoregressive (AR) modelling.** Model the signal as the output of an all-pole
filter driven by white noise:

$$x[n]=-\\sum_{k=1}^{p} a_k\\,x[n-k] + e[n]\\;\\;\\Longrightarrow\\;\\; S_{\\text{AR}}(\\omega)=\\frac{\\sigma_e^2}{\\big|1+\\sum_k a_k e^{-j\\omega k}\\big|^2}.$$

Fit the coefficients $a_k$ by solving the **Yule–Walker (normal!) equations**
$\\mathbf{R}\\mathbf{a}=-\\mathbf{r}$ — the *same* autocorrelation-matrix solve as Wiener
filtering, computed fast by the **Levinson–Durbin recursion**. AR estimation is
**linear prediction**: $a_k$ are the coefficients that best predict $x[n]$ from its
past, and the poles of the resulting filter sit under the spectral peaks. With a
short data record, AR resolves two close tones the periodogram merges into one hump:

```plot
{"title": "AR (all-pole) spectrum: sharp peaks where the periodogram blurs", "xLabel": "frequency ω", "yLabel": "S(ω)", "xRange": [0.01, 3.14], "yRange": [0, 14], "controls": [{"name": "r", "range": [0.7, 0.97], "value": 0.9, "label": "pole radius (sharpness)"}], "functions": [{"expr": "1/(1 - 2*r*cos(x-1.0) + r^2) + 1/(1 - 2*r*cos(x-1.5) + r^2)", "label": "S_AR(ω): two close tones", "color": "#2563eb"}]}
```

**The family.**

- **AR (all-pole)** — best for spectra with sharp peaks (sinusoids, resonances);
  the dominant choice (speech LPC, radar).
- **MA (all-zero)** — for spectra with deep nulls.
- **ARMA** — both; most general, harder to fit.

**Pisarenko / MUSIC for line spectra.** When the signal is *pure sinusoids in
noise*, the **subspace** estimators from the DOA lesson port directly to frequency:
eigen-decompose the autocorrelation matrix and read peaks off the noise subspace —
super-resolution in frequency, exactly mirroring super-resolution in angle.

**Trade-off:** parametric power depends on the **model order** $p$. Too small under-
fits (merged peaks); too large invents spurious peaks. Order-selection (AIC/MDL)
chooses it — the spectral cousin of estimating $K$ in MUSIC.

**Next:** put it all together in a case study.
""",
        ),
        _t(
            "Case study: interference nulling & source localization",
            "12 min",
            """\
# Case study: interference nulling & source localization

A capstone tying every thread together. Scenario: an $N=8$ element ULA
($d=\\lambda/2$) on a radio receiver must (a) **find** where signals are coming from,
(b) **lock onto** the wanted one, and (c) **null** a strong jammer — all online,
all from the array data.

**Step 1 — estimate the covariance.** Collect $L$ snapshots and form
$\\hat{\\mathbf{R}}=\\frac1L\\sum_n\\mathbf{x}[n]\\mathbf{x}^\\mathsf{H}[n]$. Everything below is a
function of $\\hat{\\mathbf{R}}$ — the spatial analogue of the time-domain $\\mathbf{R}$
that built the Wiener filter.

**Step 2 — localize the sources (DOA).** Eigen-decompose $\\hat{\\mathbf{R}}$; use
AIC/MDL on the eigenvalues to decide there are $K=2$ sources. Run **MUSIC** to get
two sharp peaks: the **signal of interest** at $\\theta_s$ and a **jammer** at
$\\theta_j$. (ESPRIT would give the same angles in closed form, cheaper.)

**Step 3 — beamform with a null on the jammer.** Build the **MVDR** weights toward
$\\theta_s$:

$$\\mathbf{w}=\\frac{\\hat{\\mathbf{R}}^{-1}\\mathbf{a}(\\theta_s)}{\\mathbf{a}^\\mathsf{H}(\\theta_s)\\hat{\\mathbf{R}}^{-1}\\mathbf{a}(\\theta_s)}.$$

Because the jammer dominates $\\hat{\\mathbf{R}}$, minimising output power *forces a
deep null* onto $\\theta_j$ while the constraint holds unit gain on $\\theta_s$. Add
**diagonal loading** $\\hat{\\mathbf{R}}+\\gamma\\mathbf{I}$ so a small steering-vector error
doesn't self-null the wanted signal. The resulting pattern: mainlobe on the signal,
deep notch on the jammer — slide the jammer angle and watch the null track it:

```plot
{"title": "Final pattern: mainlobe on signal (ψ=0), deep adaptive null on the jammer", "xLabel": "angle variable ψ", "yLabel": "|array response|", "xRange": [-3.14, 3.14], "yRange": [0, 1.05], "controls": [{"name": "jam", "range": [-2.5, 2.5], "value": 1.6, "label": "jammer angle ψ_j"}], "functions": [{"expr": "abs(sin(8*x/2)/(8*sin(x/2))) * abs(sin((x-jam)/2))/abs(sin(jam/2) + 0.05)", "label": "MVDR pattern", "color": "#2563eb"}], "points": [{"x": 0, "y": 1, "label": "signal of interest", "color": "#16a34a", "size": 7}, {"xExpr": "jam", "y": 0, "label": "jammer (nulled)", "color": "#dc2626", "size": 7}]}
```

**Step 4 — track.** Sources move, so re-estimate $\\hat{\\mathbf{R}}$ over a sliding
window (or update it with a forgetting factor — exactly the **RLS** mechanism) and
recompute. The array continuously re-points and re-nulls.

**The big picture.** Spatial processing is temporal adaptive filtering with
geometry: $\\mathbf{R}^{-1}\\mathbf{p}$ becomes $\\mathbf{R}^{-1}\\mathbf{a}(\\theta)$, taps in
time become sensors in space, frequency becomes angle, and the periodogram-vs-AR
resolution story repeats as beamforming-vs-MUSIC. Master one and you have the
other. This is the engine behind phased-array radar, 5G massive MIMO, GPS
anti-jam, sonar, ultrasound and radio astronomy.

**Next:** the final quiz.
""",
        ),
        _quiz(),
    ),
)


ADAPTIVE_DSP_COURSES: tuple[SeedCourse, ...] = (_AD_BASICS, _AD_INTERMEDIATE, _AD_ADVANCED)

__all__ = ["ADAPTIVE_DSP_COURSES"]
