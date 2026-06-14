"""Academy seed content — the State Estimation & Sensor Fusion track (Beginner → Advanced).

* ``estimation-basics``        — why estimate, random variables & the Gaussian, least squares, recursive estimation, the measurement model
* ``estimation-intermediate``  — the Bayes filter, the Kalman filter (full derivation), tuning Q/R, the complementary filter
* ``estimation-advanced``      — the EKF, the UKF, the particle filter, factor-graph smoothing, multi-sensor fusion & consistency

Runnable ``code`` lessons use Python + numpy (validated inline) for least-squares
fits, recursive weighted means, a 2-state Kalman filter, a complementary filter,
an EKF for range-to-beacon localization, and a 1-D particle filter. The
**equivalent MATLAB** appears as read-only blocks (Kalman predict/update). Interactive
plots include a slider-driven Gaussian. Part of the Robotics & Controls curriculum.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, μ, σ, θ, ², ×, ∝, ⁻¹) in diagrams.
# ruff: noqa: RUF001, RUF003

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# estimation-basics
# ──────────────────────────────────────────────────────────────────────

_EST_BASICS = SeedCourse(
    slug="estimation-basics",
    title="State Estimation & Sensor Fusion — Basics",
    description=(
        "Why we estimate hidden state from noisy, partial measurements: random "
        "variables and the Gaussian, least squares and weighted least squares, "
        "recursive estimation (the running weighted mean as a precursor to the "
        "Kalman filter), and the linear measurement model y = Hx + noise. With "
        "runnable Python labs, MATLAB equivalents, and an interactive Gaussian."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why estimate? Noise, uncertainty & partial observability",
            "10 min",
            r"""# Why estimate? Noise, uncertainty & partial observability

A robot, a spacecraft, a phone, a self-driving car — none of them can ever directly
**see their own state**. They want to know where they are, how fast they're moving,
which way they're pointed. What they actually have is a stream of **noisy, partial,
indirect measurements** from imperfect sensors. **State estimation** is the
discipline of turning those measurements into the best possible guess of the hidden
**state**, together with an honest statement of **how uncertain** that guess is.

Three hard facts force us to estimate rather than simply read off the answer:

- **Noise.** Every sensor is corrupted by random error — thermal noise, vibration,
  quantization. A GPS fix jitters by metres; a gyro output trembles even when still.
  No single reading is the truth.
- **Partial observability.** You rarely measure the state you want. A wheel encoder
  measures rotation, not position; a camera measures pixels, not depth; a barometer
  measures pressure, not altitude. The state is **hidden behind** a measurement
  function.
- **Uncertainty.** Because of the above, the answer is never a single number — it's a
  **distribution**. Good estimators report not just a best guess (the **mean**) but a
  **covariance** that says how confident they are. An estimate without an uncertainty
  is dangerous: it tells a control system to trust a number it shouldn't.

The setup we'll use throughout: there's a true **state** `x` we cannot see, and we
collect **measurements** `z` related to it by a **measurement model**. We want the
estimate `x̂` (read "x-hat") that is, in a precise sense, **best** — and we want its
uncertainty so downstream decisions can weigh it correctly.

```
   hidden truth x ──►  sensor (model H + noise) ──►  measurement z
                                                       │
                            estimator  ◄───────────────┘
                                │
                                ▼
                    estimate  x̂  +  uncertainty (covariance P)
```

**Two regimes** organize the whole field. When you have a **batch** of data and want
one best fit, that's **least squares** (this course). When data arrives **one sample
at a time** and you want to update your estimate on the fly without re-processing
everything, that's **recursive estimation** — which culminates in the **Kalman
filter** (next course). Remarkably, the recursive form gives the *same* answer as the
batch form, just computed incrementally — a theme we'll make concrete.

**Fusion** is the payoff. When several sensors each see part of the truth — a GPS and
an accelerometer, a camera and a LIDAR — combining them yields an estimate **better
than any sensor alone**, because their errors are partly independent. The
mathematics of *how* to combine them optimally (weighting each by its reliability) is
exactly what we build here, starting from the humble idea that a measurement you
trust more should count for more.

The mindset shift: stop thinking of a sensor reading as **the answer**, and start
thinking of it as **evidence** that nudges a belief. Everything that follows —
weighting, recursion, the Kalman gain, Bayesian updates — is machinery for combining
evidence optimally. We begin with the language of uncertainty itself: the Gaussian.
""",
        ),
        _t(
            "Random variables & the Gaussian",
            "11 min",
            r"""# Random variables & the Gaussian

To reason about noisy quantities we model them as **random variables** — numbers
whose value we don't know exactly, described by a **probability distribution**. Two
numbers summarize a distribution and carry almost all the weight in estimation:

- The **mean** `μ` — the center of mass, our best single guess.
- The **variance** `σ²` (or its square root, the **standard deviation** `σ`) — the
  spread, i.e. how uncertain we are.

The star of the show is the **Gaussian** (normal) distribution:

$$ p(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \, \exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right) $$

the familiar bell curve, centered at μ with width set by σ. In the multivariate case
the variance becomes a **covariance matrix** `Σ` (or `P`), whose diagonal holds each
variable's variance and whose off-diagonals capture **correlation** between them.

Drag the slider to see how σ controls the bell's width (larger σ → flatter, more
uncertain; smaller σ → sharp, confident):

```plot
{"title": "The Gaussian — drag σ: larger variance ⇒ wider, less certain", "xLabel": "x", "yLabel": "p(x) (unnormalised)", "xRange": [-6, 6], "yRange": [0, 1.05], "controls": [{"name": "s", "label": "std dev σ", "range": [0.4, 3], "step": 0.1, "value": 1}], "functions": [{"expr": "exp(-(x*x)/(2*s*s))", "label": "exp(−x²/2σ²)", "color": "#2563eb"}]}
```

**Why do Gaussians dominate estimation?** Several deep reasons converge:

- **The Central Limit Theorem.** A quantity perturbed by *many* small independent
  effects (the way real sensor noise arises) tends toward a Gaussian — so it's an
  honest model of measurement noise.
- **Closed under linear operations.** A linear function of a Gaussian is Gaussian; the
  **sum** of independent Gaussians is Gaussian (means add, variances add). This is
  what lets a filter stay Gaussian step after step.
- **Closed under multiplication.** The **product** of two Gaussians is (up to scale)
  another Gaussian — and that product is exactly how Bayes' rule **fuses** two pieces
  of Gaussian evidence. The fused mean is the **precision-weighted average** of the
  two means, where precision = 1/σ². This single fact is the seed of the Kalman gain.
- **Only two numbers.** A Gaussian is fully described by (μ, Σ). Propagating a belief
  reduces to propagating a mean and a covariance — cheap and exact for linear systems.

A worked taste of fusion: two independent measurements of the same quantity,
`z₁ ± σ₁` and `z₂ ± σ₂`, combine into

$$ \hat{x} = \frac{\sigma_2^2\,z_1 + \sigma_1^2\,z_2}{\sigma_1^2 + \sigma_2^2}, \qquad \frac{1}{\sigma^2} = \frac{1}{\sigma_1^2} + \frac{1}{\sigma_2^2} $$

Read it: each measurement is weighted by the **other's** variance (so the *more
certain* one dominates), and the **precisions add** — fusing evidence always makes you
*more* certain than either source alone. Notice the fused variance is smaller than
either σ₁² or σ₂². That formula *is* a one-shot Kalman update, and we'll meet it again
dressed in matrices.

The lesson to carry forward: **uncertainty is a first-class quantity**, the Gaussian
is the workhorse for representing it, and combining Gaussians by their precision is
the atom of optimal fusion. Next we estimate from a whole batch of data at once:
least squares.
""",
        ),
        _t(
            "Least squares & weighted least squares",
            "11 min",
            r"""# Least squares & weighted least squares

The oldest and most useful estimator is **least squares**: given many noisy
observations of a model, choose the parameters that make the model fit the data **as
closely as possible**, where "close" means minimizing the **sum of squared errors**.
Gauss invented it to track asteroids; today it underlies regression, calibration,
SLAM back-ends, and the Kalman filter itself.

Write the **linear measurement model** stacking all observations:

$$ z = H x + v $$

where `x` is the unknown parameter vector (e.g. a line's slope and intercept), each
row of the **measurement matrix** `H` maps `x` to one prediction, `z` is the stacked
measurements, and `v` is noise. We have **more equations than unknowns**
(over-determined), so no exact solution exists — instead we minimize the residual:

$$ J(x) = \sum_i (z_i - H_i x)^2 = \lVert z - Hx \rVert^2 $$

Setting the gradient to zero gives the famous **normal equations** and their solution:

$$ H^\top H\,\hat{x} = H^\top z \quad\Longrightarrow\quad \hat{x} = (H^\top H)^{-1} H^\top z $$

That matrix `(HᵀH)⁻¹Hᵀ` is the **pseudo-inverse**. Geometrically, least squares
**projects** the measurement vector onto the column space of `H` — the residual is
made orthogonal to every model direction, which is why no further reduction is
possible.

**A picture for a straight-line fit** `y = a + b·t`:

```
 y │        ●            each ● is a noisy sample (t_i, z_i);
   │     ●  ╱  ●         least squares slides the line to
   │   ● ╱●               minimise the total squared vertical
   │  ╱●   ●              gap (the residuals).
   │ ╱  ●
   └──────────────► t      rows of H are [1, t_i]; x = [a, b].
```

**Weighted least squares (WLS)** fixes a blind spot: plain LS trusts every
measurement equally, but some sensors are noisier than others. Weight each residual by
its reliability — ideally the **inverse of its noise variance** (`wᵢ = 1/σᵢ²`):

$$ \hat{x} = (H^\top W H)^{-1} H^\top W z, \qquad W = \operatorname{diag}(1/\sigma_i^2) $$

Now a precise measurement (small σ) pulls the fit harder than a sloppy one — exactly
the **precision-weighting** we saw fusing two Gaussians, generalized to many. When the
noise is zero-mean Gaussian, WLS is not just intuitive but **optimal**: it coincides
with the **maximum-likelihood** estimate (minimizing squared error = maximizing
Gaussian likelihood, because the log of a Gaussian *is* a negative quadratic). And if
you carry the noise covariance through, WLS even hands you the **covariance of the
estimate**, `(HᵀWH)⁻¹` — your uncertainty, for free.

The conceptual bridge to filtering: least squares answers "given **all** the data,
what's the best fit?" But data arrives over time, and re-solving the whole batch on
every new sample is wasteful. The next lesson shows how to get the *same* answer
**recursively**, one measurement at a time — the doorway to the Kalman filter. You'll
fit a line to noisy data in the lab that follows.
""",
        ),
        _code(
            "Least-squares fit to noisy data",
            "13 min",
            r"""# Least squares fits a model to over-determined noisy data by minimising squared
# error: solve the normal equations xhat = (H'H)^-1 H'z, or use np.linalg.lstsq.
# Here we fit a straight line y = a + b*t to noisy samples. Noise is DETERMINISTIC
# (a normalised sum of sinusoids), so the result is reproducible. Uses numpy.

import numpy as np

# True line we will try to recover.
a_true = 2.0
b_true = 0.5
t = np.linspace(0.0, 10.0, 60)

# Deterministic "noise": a sum of incommensurate sinusoids, normalised to unit std,
# then scaled. (No random module in the sandbox -> we synthesise repeatable noise.)
raw = np.sin(3.0 * t) + np.sin(7.3 * t + 1.0) + np.sin(13.1 * t + 2.0)
noise = 0.8 * (raw - raw.mean()) / raw.std()
z = a_true + b_true * t + noise

# Build the measurement matrix H (each row [1, t_i]) and solve least squares.
H = np.column_stack([np.ones_like(t), t])
xhat = np.linalg.lstsq(H, z, rcond=None)[0]          # [a_hat, b_hat]

# The normal equations give the SAME answer (and the estimate covariance ~ (H'H)^-1).
xhat_normal = np.linalg.inv(H.T @ H) @ (H.T @ z)
residual = z - H @ xhat
rms = float(np.sqrt(np.mean(residual ** 2)))

print("true:      a=%.3f  b=%.3f" % (a_true, b_true))
print("lstsq:     a=%.3f  b=%.3f" % (xhat[0], xhat[1]))
print("normal eq: a=%.3f  b=%.3f  (matches lstsq)" % (xhat_normal[0], xhat_normal[1]))
print("residual RMS = %.3f (~ the injected noise level)" % rms)
print()
print("least squares recovers the underlying line despite per-sample noise;")
print("weighting rows by 1/sigma^2 (WLS) would trust the cleaner samples more.")
""",
        ),
        _t(
            "Recursive estimation & the measurement model",
            "11 min",
            r"""# Recursive estimation & the measurement model

Least squares is a **batch** method: it waits for all the data, then solves once. But
a robot gets measurements **one at a time, forever**. Re-solving the entire history on
every new sample is wasteful and eventually impossible. **Recursive estimation**
updates the current estimate using **only the new measurement and a compact summary**
of everything seen so far — and, beautifully, lands on the *same* answer as the batch
solution.

The clearest instance is the **running mean**. To average N numbers you could store
them all and divide. Recursively, keep just the current mean `x̂ₙ₋₁` and count, and fold
in each new sample `zₙ`:

$$ \hat{x}_n = \hat{x}_{n-1} + \frac{1}{n}\,\bigl(z_n - \hat{x}_{n-1}\bigr) $$

Look closely — this is the **shape of every filter we will build**:

```
 new estimate = old estimate  +  gain × ( measurement − prediction )
   x̂ₙ          =     x̂ₙ₋₁     +  Kₙ   × (    zₙ        −   x̂ₙ₋₁    )
                                  └────────────┬───────────────┘
                                          the "innovation":
                                       how surprising the new data is
```

The bracket is the **innovation** (or residual) — the part of the measurement the
estimate did **not** predict. The **gain** `Kₙ = 1/n` decides how much to trust that
surprise. Early on (`n` small) the gain is large and each sample moves the estimate a
lot; later it shrinks, so once you're confident, new data barely budges you. That
gain-shrinking-as-confidence-grows behaviour is the Kalman filter in miniature.

**Recursive *weighted* mean.** If samples have different reliabilities, weight by
precision (`wᵢ = 1/σᵢ²`) and track the **accumulated precision** `Wₙ = Σ wᵢ`:

$$ \hat{x}_n = \hat{x}_{n-1} + \frac{w_n}{W_n}\,\bigl(z_n - \hat{x}_{n-1}\bigr), \qquad \frac{1}{\sigma_n^2} = W_n $$

The gain `wₙ/Wₙ` is large when the *new* sample is precise relative to what you've
accumulated, and the estimate's variance `1/Wₙ` **shrinks monotonically** as precision
piles up — fusion always sharpens the belief. This is literally a scalar Kalman filter
for a constant state.

**The measurement model**, made general. Throughout estimation we relate the hidden
state to what a sensor reports by:

$$ z = H x + v, \qquad v \sim \mathcal{N}(0, R) $$

- `x` — the hidden state we want (position, velocity, …).
- `H` — the **observation matrix**: how the state maps into the measurement. It
  encodes *partial observability* — a position sensor has `H = [1\ 0]`, seeing
  position but **not** velocity. A row of zeros means a state component is invisible to
  that sensor.
- `v` — zero-mean noise with **covariance R**: how much to distrust the sensor. Big R →
  noisy sensor → small gain → the filter leans on its prediction instead.

When `H` is nonlinear (e.g. a range or bearing), we **linearize** it — the leap to the
Extended Kalman Filter (advanced course). For now, `z = Hx + v` plus the recursive
"estimate += gain × innovation" update are the two ideas the entire Kalman machinery is
built from. You'll implement the recursive weighted mean next and watch its variance
collapse as evidence accumulates.
""",
        ),
        _code(
            "Recursive weighted mean (a scalar filter)",
            "13 min",
            r"""# A recursive estimator folds in one sample at a time:
#   xhat += (w_n / W_n) * (z_n - xhat),   variance = 1/W_n  (W = accumulated precision).
# This is a scalar Kalman filter for a constant state. We estimate a constant signal
# from measurements of MIXED reliability and watch the variance shrink. numpy.

import numpy as np

x_true = 5.0

# Twelve measurements with DETERMINISTIC offsets (no random module) and a per-sample
# stated noise std sigma_i. Precise samples (small sigma) should pull the estimate more.
sigma = np.array([2.0, 2.0, 0.5, 2.0, 1.0, 2.0, 0.3, 1.0, 2.0, 0.5, 1.5, 2.0])
offset = np.array([1.4, -1.7, 0.2, 1.9, -0.6, -2.1, 0.1, 0.7, -1.5, -0.2, 1.1, 1.8])
z = x_true + offset

# Run the recursive weighted mean. Straight-line module-level loop (no helper fn).
xhat = 0.0
accum_precision = 0.0
print(" step   z_n    sigma_n    gain     xhat     est.std")
for i in range(z.shape[0]):
    w = 1.0 / (sigma[i] * sigma[i])              # precision of this sample
    accum_precision = accum_precision + w
    gain = w / accum_precision                   # recursive-mean gain
    xhat = xhat + gain * (z[i] - xhat)           # estimate += gain * innovation
    est_std = float(np.sqrt(1.0 / accum_precision))
    print("  %2d   %5.2f   %5.2f    %5.3f   %6.3f   %6.3f"
          % (i + 1, z[i], sigma[i], gain, xhat, est_std))

print()
print("final estimate %.3f (true %.1f); estimate std shrank monotonically." % (xhat, x_true))
print("precise samples (small sigma) carry a bigger gain -> precision-weighted fusion.")
""",
        ),
        quiz_lesson(
            "Quiz: Estimation Fundamentals",
            (
                q(
                    "Why must we estimate state rather than read it directly?",
                    (
                        opt(
                            "Sensors are noisy, observe state only partially/indirectly, so the answer is a distribution (mean + uncertainty), not a single number",
                            correct=True,
                        ),
                        opt("Sensors are always exact but slow"),
                        opt("State is always directly measured"),
                        opt("Estimation removes the need for sensors"),
                    ),
                    "Noise, partial observability, and uncertainty force us to fuse measurements into a best guess plus a covariance; a reading is evidence, not the truth.",
                ),
                q(
                    "Why does the Gaussian dominate estimation?",
                    (
                        opt(
                            "It's fully described by (mean, covariance), and is closed under linear maps, sums, and products — so beliefs stay Gaussian and fuse by precision",
                            correct=True,
                        ),
                        opt("It is the only distribution that exists"),
                        opt("It has infinite variance"),
                        opt("It cannot be added to another Gaussian"),
                    ),
                    "Central Limit Theorem + closure under linear ops and multiplication (Bayes fusion) + only two parameters make Gaussians the workhorse of filtering.",
                ),
                q(
                    "What does the least-squares solution x̂ = (HᵀH)⁻¹Hᵀz do?",
                    (
                        opt(
                            "Minimises the sum of squared residuals ‖z − Hx‖² — projecting z onto H's column space; with Gaussian noise it equals the maximum-likelihood estimate",
                            correct=True,
                        ),
                        opt("Maximises the residual error"),
                        opt("Requires exactly as many equations as unknowns"),
                        opt("Ignores the measurements entirely"),
                    ),
                    "LS solves the over-determined normal equations; WLS weights each row by 1/σ² (precision), which is optimal for zero-mean Gaussian noise.",
                ),
                q(
                    "In weighted least squares / fusion, how should each measurement be weighted?",
                    (
                        opt(
                            "By its precision, the inverse of its noise variance (1/σ²) — more certain measurements count more",
                            correct=True,
                        ),
                        opt("Equally, regardless of noise"),
                        opt("By its variance σ² directly"),
                        opt("By how recent it is only"),
                    ),
                    "Precision-weighting (1/σ²) lets a clean sensor dominate a noisy one; the fused precision is the SUM of precisions, so fusion always sharpens the estimate.",
                ),
                q(
                    "The recursive update x̂ₙ = x̂ₙ₋₁ + Kₙ(zₙ − x̂ₙ₋₁) — what is the bracketed term and what does Kₙ do?",
                    (
                        opt(
                            "The bracket is the innovation (measurement minus prediction); the gain Kₙ sets how much that surprise moves the estimate, shrinking as confidence grows",
                            correct=True,
                        ),
                        opt("The bracket is the transmit power; Kₙ is the frequency"),
                        opt("The bracket is always zero"),
                        opt("Kₙ grows without bound over time"),
                    ),
                    "estimate += gain × innovation is the shape of every filter; for a running mean Kₙ = 1/n shrinks as evidence accumulates — a scalar Kalman filter.",
                ),
                q(
                    "In the measurement model z = Hx + v, what do H and R represent?",
                    (
                        opt(
                            "H maps hidden state into the measurement (encoding partial observability); R is the measurement-noise covariance (how much to distrust the sensor)",
                            correct=True,
                        ),
                        opt("H is the state and R is the time step"),
                        opt("H is noise and R is the true state"),
                        opt("Both are always the identity"),
                    ),
                    "H = [1 0] sees position but not velocity (partial observability); a large R yields a small gain so the filter trusts its prediction over the sensor.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# estimation-intermediate
# ──────────────────────────────────────────────────────────────────────

_EST_INTERMEDIATE = SeedCourse(
    slug="estimation-intermediate",
    title="State Estimation & Sensor Fusion — Intermediate",
    description=(
        "The recursive Bayesian core of estimation: the Bayes filter "
        "(predict/update), the Kalman filter derived in full (predict and update "
        "equations, the Kalman gain), the intuition that it is optimal for "
        "linear-Gaussian systems, tuning the process and measurement covariances "
        "Q and R, and the lightweight complementary filter. With a runnable 2-state "
        "Kalman filter, a complementary-filter fusion lab, and an estimate plot."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The Bayes filter — the recursive belief",
            "11 min",
            r"""# The Bayes filter — the recursive belief

Every recursive estimator — Kalman, EKF, particle filter — is a special case of one
master algorithm: the **Bayes filter**. It maintains a **belief**, a probability
distribution `bel(x)` over the state, and updates it as the world evolves and new
measurements arrive. Understand this loop once and you understand the family.

Two ingredients drive a dynamic system:

- A **motion (process) model** `p(xₜ | xₜ₋₁, uₜ)` — how the state evolves over one
  step given any control input `u`. (A car's next position depends on its speed.)
- A **measurement model** `p(zₜ | xₜ)` — how likely a sensor reading is, given a state.

The Bayes filter alternates **two steps** forever:

```
        ┌──────────────── PREDICT ─────────────────┐
 bel(xₜ₋₁) ──move via motion model──►  bel̄(xₜ)   (belief BEFORE the measurement)
        └────────────────────────────────────────┘
        ┌──────────────── UPDATE ──────────────────┐
   bel̄(xₜ) ──weight by measurement likelihood──►  bel(xₜ)  (belief AFTER)
        └────────────────────────────────────────┘
```

**Predict** (time update): push the belief forward through the motion model. The
state moves, and because motion is uncertain (the control isn't perfect, the world is
noisy), the belief **spreads out** — uncertainty *grows*:

$$ \overline{bel}(x_t) = \int p(x_t \mid x_{t-1}, u_t)\, bel(x_{t-1})\, dx_{t-1} $$

**Update** (measurement update): fold in the new measurement via **Bayes' rule**,
multiplying the predicted belief by the **likelihood** of the data and renormalizing.
The belief **sharpens** — uncertainty *shrinks* — toward states consistent with what
was observed:

$$ bel(x_t) = \eta\; p(z_t \mid x_t)\; \overline{bel}(x_t) $$

(`η` is just the normalizer that makes it a valid distribution.)

The rhythm is the heartbeat of estimation: **predict spreads, measure sharpens**,
predict spreads, measure sharpens. Without measurements the belief diffuses into
ignorance (dead-reckoning drift); without motion it would freeze. The two steps
balance a **model you trust** against **data you trust**.

Why does this matter? The integral in the predict step and the product in the update
step are, in general, **intractable** — you can't represent arbitrary distributions on
a computer. The whole zoo of filters is **different ways to make the Bayes filter
computable** by restricting the form of the belief:

- Assume everything **linear and Gaussian** → the integral and product have a
  **closed form** → the **Kalman filter** (next lesson). Just track (mean, covariance).
- Allow **nonlinear** models, linearize them → the **Extended/Unscented KF**.
- Represent the belief by **samples** → the **particle filter** (advanced course).

So the Bayes filter is the **theory**; the Kalman filter is its exact, efficient
solution in the friendly linear-Gaussian world — where "multiply two Gaussians" (from
the Basics course) becomes the update, and "sum of Gaussians" becomes the predict.
That is exactly what we derive next.
""",
        ),
        _t(
            "The Kalman filter — full derivation",
            "13 min",
            r"""# The Kalman filter — full derivation

The **Kalman filter (KF)** is the Bayes filter made concrete for **linear systems with
Gaussian noise**. Because Gaussians are closed under the linear predict and the
multiplicative update, the belief stays Gaussian forever, so the filter only ever
tracks a **mean `x`** and a **covariance `P`**. It is the most-used estimator in
engineering — guidance, navigation, tracking, sensor fusion.

**The model.** A linear discrete-time system:

$$ x_t = F\,x_{t-1} + B\,u_t + w, \qquad w \sim \mathcal{N}(0, Q) $$
$$ z_t = H\,x_t + v, \qquad v \sim \mathcal{N}(0, R) $$

- `F` — **state-transition matrix** (the dynamics; e.g. position += velocity·dt).
- `B`, `u` — control input (optional).
- `Q` — **process-noise covariance**: how much we distrust the motion model.
- `H` — **measurement matrix**; `R` — **measurement-noise covariance**.

**PREDICT (time update)** — push the Gaussian through the dynamics. The mean follows
`F`; the covariance is transformed by `F` and **grows** by the process noise `Q`:

$$ \hat{x}^- = F\,\hat{x} + B\,u $$
$$ P^- = F\,P\,F^\top + Q $$

(The `FPFᵀ` is how a linear map transforms a covariance; `+ Q` is the spreading.)

**UPDATE (measurement update)** — fuse the measurement. First the **innovation** (the
surprise) and its covariance:

$$ y = z - H\,\hat{x}^- \qquad\text{(innovation)} $$
$$ S = H\,P^-\,H^\top + R \qquad\text{(innovation covariance)} $$

Then the star of the show, the **Kalman gain** — how much to trust the innovation:

$$ K = P^-\,H^\top\,S^{-1} = P^-\,H^\top\,(H\,P^-\,H^\top + R)^{-1} $$

and finally correct the mean and **shrink** the covariance:

$$ \hat{x} = \hat{x}^- + K\,y $$
$$ P = (I - K\,H)\,P^- $$

That's the entire filter — five lines, run in a loop:

```
 PREDICT:   x⁻ = F x ;            P⁻ = F P Fᵀ + Q          (belief spreads)
 UPDATE:    y  = z − H x⁻         (innovation: data minus prediction)
            S  = H P⁻ Hᵀ + R      (its covariance)
            K  = P⁻ Hᵀ S⁻¹        (Kalman gain)
            x  = x⁻ + K y         (correct the estimate)
            P  = (I − K H) P⁻     (belief sharpens)
```

**Read the gain.** `K` balances the predicted uncertainty `P⁻` against the measurement
noise `R`. In scalar form `K = P⁻ / (P⁻ + R)`:

- **Trustworthy sensor** (`R` small) → `K → 1` → snap the estimate to the measurement.
- **Noisy sensor** (`R` large) → `K → 0` → ignore the measurement, coast on the model.
- It's the **precision-weighted blend** from the Basics course (`σ₂²z₁+σ₁²z₂` over
  `σ₁²+σ₂²`), promoted to matrices. The KF is recursive weighted least squares.

**Why it's special.** Among *all* estimators (not just linear ones), for a
linear-Gaussian system the Kalman filter is the **optimal** estimator — it is
simultaneously the minimum-mean-square-error estimator, the maximum-likelihood
estimate, and the exact Bayes posterior. No method can do better given the same model.
It also runs in **constant memory and time per step**, which is why it flew Apollo and
runs in your phone's GPS. Next: how `Q` and `R` — the only real knobs — shape its
behaviour, and a lightweight cousin, the complementary filter. The standard predict/
update in **MATLAB**:

```matlab
% one Kalman step (constant-velocity, position measurement)
F = [1 dt; 0 1];  H = [1 0];
xpred = F*x;                  Ppred = F*P*F' + Q;     % PREDICT
y = z - H*xpred;              S = H*Ppred*H' + R;     % innovation
K = Ppred*H'*inv(S);                                  % Kalman gain
x = xpred + K*y;              P = (eye(2) - K*H)*Ppred;% UPDATE
disp('updated state estimate:'); disp(x)
```
""",
        ),
        _code(
            "A 2-state Kalman filter (position + velocity)",
            "14 min",
            r"""# A constant-velocity Kalman filter estimates position AND velocity from noisy
# position-only measurements. State x = [pos, vel]; F advances it; H = [1, 0] sees
# only position. All matrix algebra (F P F', K = P H' inv(S), ...) runs at MODULE
# LEVEL (the sandbox hides numpy inside functions). Deterministic noise. numpy.

import numpy as np

dt = 1.0
steps = 40

# Model matrices.
F = np.array([[1.0, dt], [0.0, 1.0]])      # constant-velocity dynamics
H = np.array([[1.0, 0.0]])                 # measure position only
Q = np.array([[0.01, 0.0], [0.0, 0.01]])   # process-noise covariance
R = np.array([[4.0]])                      # measurement-noise variance (noisy GPS)
I2 = np.eye(2)

# Ground truth: constant velocity 1.0; deterministic measurement noise (sinusoids).
t = np.arange(steps, dtype=float)
true_pos = 1.0 * t
k = np.arange(steps)
raw = np.sin(2.1 * k) + np.sin(5.7 * k + 1.0) + np.sin(11.3 * k + 2.0)
meas_noise = 2.0 * (raw - raw.mean()) / raw.std()
z_all = true_pos + meas_noise

# Initial belief: position/velocity unknown, large covariance.
x = np.array([[0.0], [0.0]])
P = np.array([[10.0, 0.0], [0.0, 10.0]])

est_pos = np.zeros(steps)
for i in range(steps):
    # PREDICT (module-level matrix ops).
    x = F @ x
    P = F @ P @ F.T + Q
    # UPDATE.
    z = np.array([[z_all[i]]])
    y = z - H @ x                          # innovation
    S = H @ P @ H.T + R                    # innovation covariance
    Kgain = P @ H.T @ np.linalg.inv(S)     # Kalman gain
    x = x + Kgain @ y
    P = (I2 - Kgain @ H) @ P
    est_pos[i] = float(x[0, 0])

meas_err = float(np.sqrt(np.mean((z_all - true_pos) ** 2)))
est_err = float(np.sqrt(np.mean((est_pos - true_pos) ** 2)))
print("final estimate: pos=%.2f vel=%.2f (truth pos=%.1f vel=1.0)" % (x[0, 0], x[1, 0], true_pos[-1]))
print("RMS error  raw measurements = %.3f" % meas_err)
print("RMS error  Kalman estimate  = %.3f" % est_err)
print("the filter recovered velocity it never measured, and beats the raw sensor.")
""",
        ),
        _t(
            "Tuning Q and R, and filter behaviour",
            "11 min",
            r"""# Tuning Q and R, and filter behaviour

The Kalman equations are fixed; what you actually *design* is the pair of covariances
**Q** (process noise) and **R** (measurement noise). They are the only real knobs, and
they encode a single judgement: **how much do I trust my motion model versus my
sensor?** Getting them right is most of the practical work of filtering.

**What each one means:**

- **R — measurement-noise covariance.** How noisy is the sensor? Often you can measure
  it directly: log a stationary sensor and compute the variance of its output. R is the
  most *physically grounded* parameter.
- **Q — process-noise covariance.** How wrong is the motion model? It accounts for
  unmodeled dynamics — accelerations you didn't model, wind, slip. Q is harder to pin
  down; it's effectively "how much reality deviates from `x = Fx`," and is usually
  **tuned**.

**Their ratio sets the gain**, hence the filter's whole personality. In scalar terms
`K = P⁻/(P⁻ + R)`, with `P⁻` driven up by `Q`:

```
 LARGE Q / small R  →  high gain  →  trust the SENSOR
    fast, responsive, tracks maneuvers — but noisy/jittery output
 small Q / LARGE R  →  low gain   →  trust the MODEL
    smooth, heavily filtered output — but laggy, slow to react,
    and DANGEROUS if the model is wrong (the filter ignores reality)
```

So tuning is a **responsiveness vs smoothness** trade-off, exactly like a low-pass
filter's cutoff — because a steady-state Kalman filter *is* one, with the bandwidth set
by the Q/R ratio.

**Failure modes to recognize:**

- **Too small Q** (over-confident model) → the filter becomes **over-confident**: `P`
  collapses, the gain goes to zero, and it **stops listening** to measurements. If the
  true state then maneuvers, the estimate **diverges** while *claiming* tiny
  uncertainty — the classic, dangerous KF failure. A floor on Q (or fading-memory)
  keeps it alive.
- **Too large Q** → the estimate is jittery and barely better than the raw sensor.
- **Wrong R** → mis-weighted fusion; an over-small R makes the filter chase noise.

**How to tune in practice:**

- Measure **R** from sensor data; start there.
- Set **Q** from physical reasoning (expected unmodeled acceleration × dt), then adjust.
- **Validate with the innovations** (next course's *consistency* idea): if the filter's
  assumptions are right, the innovation sequence `y = z − Hx⁻` should be **zero-mean,
  white** (uncorrelated), and have the covariance `S` the filter predicts. Innovations
  that are biased, correlated, or larger/smaller than `S` say Q/R are mistuned — a
  rigorous, data-driven way to tune rather than eyeballing.

The takeaway: the matrices `F, H` describe **physics**; `Q, R` describe **trust**. Most
real filter problems are not "wrong equations" but "wrong trust" — mistuned Q/R. Treat
them as the design surface, ground R in measurement, reason about Q, and check the
innovations. Next, a lightweight fusion scheme that captures the same trust trade-off
with almost no math: the complementary filter.
""",
        ),
        _t(
            "The complementary filter",
            "10 min",
            r"""# The complementary filter

Not every system can afford a full Kalman filter — a tiny microcontroller on a drone
running an attitude loop at 1 kHz may have no room for matrix inverses. The
**complementary filter** is the lightweight cousin: a clever way to **fuse two sensors
with complementary error characteristics** using a single constant and almost no
computation. It's everywhere in drones, IMUs, and balancing robots.

**The classic problem: estimate tilt angle from an IMU.** You have two sensors, each
flawed in an *opposite* way:

- A **gyroscope** measures angular **rate**. Integrate it to get angle — accurate over
  the **short term**, but it **drifts** without bound over the long term as tiny bias
  errors accumulate. Good high-frequency, bad low-frequency.
- An **accelerometer** can infer the tilt angle from gravity — accurate over the **long
  term** (no drift, it always sees "down"), but **noisy** and corrupted by the
  vehicle's own acceleration in the short term. Good low-frequency, bad high-frequency.

Their error spectra are **complementary**: one is trustworthy exactly where the other
isn't. So **high-pass** the gyro estimate and **low-pass** the accel estimate and add
them — together they cover all frequencies:

$$ \theta_t = \alpha\,\bigl(\theta_{t-1} + \omega_{\text{gyro}}\,\Delta t\bigr) + (1-\alpha)\,\theta_{\text{accel}} $$

```
   gyro rate ─►[ integrate ]─►[ HIGH-PASS (α) ]─┐
                                                ├─(+)─► fused angle θ
   accel ───────────────────►[ LOW-PASS (1−α) ]─┘
```

One parameter, **α** (typically 0.95–0.99), sets the **crossover**: close to 1 leans on
the gyro (smooth, fast, but drifts if too high); lower leans on the accel (drift-free
but noisier). The two weights always **sum to one**, which is why it's "complementary"
— it's a weighted average that trusts each source in its good band.

**Relationship to the Kalman filter.** The complementary filter is essentially a
**steady-state, hand-tuned Kalman filter** for this 1-D fusion problem: α plays the
role of (one minus) the Kalman gain, fixed instead of computed online from covariances.
You give up the KF's adaptivity (a real KF would estimate and *remove* the gyro bias,
and adjust its gain as conditions change) and its uncertainty output, in exchange for
**trivial cost and rock-solid simplicity** — no matrices, no tuning of Q/R, just one α.

When to reach for which:

```
 complementary filter:  cheap, 1-2 signals, fixed trust, no covariance output
                        -> microcontrollers, attitude estimation, quick fusion
 Kalman filter:         optimal, multi-state, adapts gain, gives uncertainty,
                        estimates biases -> navigation, tracking, serious fusion
```

The unifying lesson of this course: **fusion is weighting sources by trust.** The
Kalman filter computes that weight optimally from Q and R; the complementary filter
fixes it with a single α. Both implement the same idea — combine a model/prediction
with a measurement, each in proportion to how much you believe it. You'll fuse a
drifting and a noisy signal with a complementary filter next.
""",
        ),
        _code(
            "Complementary filter: fusing drift and noise",
            "13 min",
            r"""# A complementary filter fuses two sensors with OPPOSITE flaws:
#   theta = alpha*(theta + rate*dt) + (1-alpha)*absolute_measurement
# the integrated rate is smooth but DRIFTS; the absolute reading is noisy but
# drift-free. alpha high-passes the first and low-passes the second. Deterministic. numpy.

import numpy as np

dt = 0.02
steps = 400
t = np.arange(steps) * dt

# Ground-truth angle: a smooth maneuver.
truth = 30.0 * np.sin(0.5 * t)
true_rate = 15.0 * np.cos(0.5 * t)            # exact derivative (deg/s)

# Sensor 1: a gyro rate with a constant BIAS -> integrating it DRIFTS.
gyro_bias = 4.0                               # deg/s of bias
gyro_rate = true_rate + gyro_bias

# Sensor 2: an absolute angle reading, drift-free but NOISY (deterministic noise).
raw = np.sin(7.0 * t) + np.sin(17.0 * t + 1.0) + np.sin(29.0 * t + 2.0)
accel_angle = truth + 3.0 * (raw - raw.mean()) / raw.std()

# Pure gyro integration (shows the drift) and the complementary fusion, side by side.
alpha = 0.98
gyro_only = np.zeros(steps)
fused = np.zeros(steps)
g = 0.0
f = 0.0
for i in range(steps):
    g = g + gyro_rate[i] * dt                                 # integrate -> drifts
    f = alpha * (f + gyro_rate[i] * dt) + (1.0 - alpha) * accel_angle[i]
    gyro_only[i] = g
    fused[i] = f

err_gyro = float(np.sqrt(np.mean((gyro_only - truth) ** 2)))
err_accel = float(np.sqrt(np.mean((accel_angle - truth) ** 2)))
err_fused = float(np.sqrt(np.mean((fused - truth) ** 2)))
print("RMS angle error (deg):")
print("  gyro-only (drifts):      %.2f" % err_gyro)
print("  accel-only (noisy):      %.2f" % err_accel)
print("  complementary (alpha=%.2f): %.2f" % (alpha, err_fused))
print("fusion beats BOTH: alpha low-passes the noisy accel and high-passes the gyro,")
print("rejecting drift AND noise with one constant.")
""",
        ),
        quiz_lesson(
            "Quiz: Bayes & Kalman Filtering",
            (
                q(
                    "What are the two steps of the Bayes filter and what does each do to the belief?",
                    (
                        opt(
                            "Predict (push through the motion model — uncertainty grows/spreads) and Update (fold in the measurement via Bayes — uncertainty shrinks/sharpens)",
                            correct=True,
                        ),
                        opt("Encode and decode"),
                        opt("Both steps shrink the uncertainty"),
                        opt("Amplify and attenuate the signal"),
                    ),
                    "Predict spreads the belief; update sharpens it. The Kalman filter is this loop made closed-form for linear-Gaussian systems.",
                ),
                q(
                    "Which equation is the Kalman gain?",
                    (
                        opt(
                            "K = P⁻Hᵀ(HP⁻Hᵀ + R)⁻¹ — it weights the innovation by predicted uncertainty vs measurement noise",
                            correct=True,
                        ),
                        opt("K = F P Fᵀ + Q"),
                        opt("K = z − Hx⁻"),
                        opt("K = (I − KH)P⁻"),
                    ),
                    "K = P⁻HᵀS⁻¹ with S = HP⁻Hᵀ + R. Scalar form K = P⁻/(P⁻+R): K→1 trusts the sensor, K→0 trusts the model.",
                ),
                q(
                    "In the Kalman predict step, what happens to the covariance P?",
                    (
                        opt(
                            "P⁻ = FPFᵀ + Q — it is transformed by the dynamics and GROWS by the process noise Q (the belief spreads)",
                            correct=True,
                        ),
                        opt("P stays exactly constant"),
                        opt("P shrinks during predict"),
                        opt("P becomes the identity"),
                    ),
                    "Predict spreads uncertainty: FPFᵀ propagates it through the dynamics and +Q adds process noise. The update step then shrinks P via (I−KH)P⁻.",
                ),
                q(
                    "Why is the Kalman filter considered optimal?",
                    (
                        opt(
                            "For a linear-Gaussian system it is the exact Bayes posterior — simultaneously the MMSE, ML, and minimum-variance estimate; no estimator does better",
                            correct=True,
                        ),
                        opt("Because it ignores the measurements"),
                        opt("Because it uses the most memory"),
                        opt("Only because it is fast"),
                    ),
                    "Closed under linear maps and Gaussian products, the KF keeps the belief exactly Gaussian, making it optimal for linear-Gaussian models in constant time/memory.",
                ),
                q(
                    "What is the danger of setting the process noise Q too small?",
                    (
                        opt(
                            "P collapses and the gain → 0, so the filter stops listening to measurements and can diverge from a maneuvering truth while claiming tiny uncertainty",
                            correct=True,
                        ),
                        opt("The filter becomes too noisy"),
                        opt("It has no effect at all"),
                        opt("Measurements are weighted too heavily"),
                    ),
                    "Over-small Q makes the filter over-confident in its model; it ignores the sensor and diverges. Innovations checks (zero-mean, white, covariance S) catch mistuned Q/R.",
                ),
                q(
                    "How does a complementary filter fuse a gyro and an accelerometer for tilt?",
                    (
                        opt(
                            "θ = α(θ + ω·dt) + (1−α)·θ_accel — high-passes the drift-prone gyro and low-passes the noisy accel; α sets the crossover (≈ a fixed-gain Kalman filter)",
                            correct=True,
                        ),
                        opt("It averages the two sensors with equal weight always"),
                        opt("It uses only the gyroscope"),
                        opt("It requires inverting a covariance matrix each step"),
                    ),
                    "Each sensor is trusted in its good frequency band; the weights α and (1−α) sum to one. It's a steady-state, hand-tuned scalar Kalman filter.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# estimation-advanced
# ──────────────────────────────────────────────────────────────────────

_EST_ADVANCED = SeedCourse(
    slug="estimation-advanced",
    title="State Estimation & Sensor Fusion — Advanced",
    description=(
        "Nonlinear and modern estimation: the Extended Kalman Filter (Jacobian "
        "linearization), the Unscented Kalman Filter (sigma points), the particle "
        "filter (importance sampling, weighting, resampling, degeneracy), an intro "
        "to factor-graph / MAP smoothing, and multi-sensor fusion with consistency "
        "checks (innovations, NEES/NIS). With a runnable EKF range-to-beacon lab, a "
        "1-D particle filter, and an estimation-error plot."
    ),
    level="Advanced",
    lessons=(
        _t(
            "The Extended Kalman Filter (EKF)",
            "11 min",
            r"""# The Extended Kalman Filter (EKF)

The Kalman filter is exact — but only for **linear** systems. Reality is rarely
linear: a robot's heading enters its motion through sines and cosines; a radar measures
**range** `√(x²+y²)` and **bearing** `atan2(y,x)`, both nonlinear in position. The
**Extended Kalman Filter (EKF)** extends the KF to nonlinear models by **linearizing
them locally** at each step, and for decades it was *the* workhorse of navigation
(it flew on Apollo and runs in countless GPS/INS systems).

**The nonlinear model.** Replace the matrices `F` and `H` with nonlinear functions:

$$ x_t = f(x_{t-1}, u_t) + w, \qquad z_t = h(x_t) + v $$

`f` is the motion model, `h` the measurement model. The trouble: pushing a Gaussian
through a nonlinear function does **not** yield a Gaussian, so the exact Bayes update is
intractable. The EKF's answer: **approximate `f` and `h` by their tangent (first-order
Taylor) linearization** around the current estimate, then run the ordinary Kalman
equations on those local linear models.

**The Jacobians.** Linearizing means taking the matrix of partial derivatives —
the **Jacobian** — evaluated at the current state estimate:

$$ F = \left.\frac{\partial f}{\partial x}\right|_{\hat{x}}, \qquad H = \left.\frac{\partial h}{\partial x}\right|_{\hat{x}} $$

These play exactly the roles `F` and `H` did before, but they're **recomputed every
step** at the latest estimate (the linearization point moves with the filter).

**The EKF loop** — KF equations, with `f`/`h` for the means and the Jacobians for the
covariances:

```
 PREDICT:  x⁻ = f(x, u)              (nonlinear motion for the mean)
           P⁻ = F P Fᵀ + Q           (Jacobian F transforms the covariance)
 UPDATE:   y  = z − h(x⁻)            (innovation uses the nonlinear h)
           S  = H P⁻ Hᵀ + R
           K  = P⁻ Hᵀ S⁻¹
           x  = x⁻ + K y
           P  = (I − K H) P⁻
```

**Example — range to a beacon.** A robot at `(x, y)` measures its distance to a known
beacon at `(bx, by)`: `h(x) = √((x−bx)² + (y−by)²)`. Its Jacobian (a 1×2 row) is the
**unit vector from beacon to robot**:

$$ H = \left[\frac{x-b_x}{r}, \; \frac{y-b_y}{r}\right], \qquad r = \sqrt{(x-b_x)^2 + (y-b_y)^2} $$

— intuitive: a range measurement only constrains position *along the line of sight*,
which is exactly what that gradient encodes.

**Caveats — the EKF is an approximation, and it can bite:**

- **Linearization error.** If `f`/`h` are strongly nonlinear over the span of the
  uncertainty, the tangent is a poor fit and the filter can be **inconsistent** or
  **diverge**. Smaller uncertainty / milder nonlinearity → better.
- **The Jacobians must be derived** (by hand or autodiff) and be correct — a frequent
  source of bugs.
- **It's not optimal**, only a good local approximation — which motivates the
  derivative-free **Unscented** filter next.

Still, when nonlinearity is mild the EKF is cheap, fast, and excellent — which is why
it remains ubiquitous. You'll build the range-to-beacon EKF in the lab.
""",
        ),
        _t(
            "The Unscented Kalman Filter (UKF)",
            "10 min",
            r"""# The Unscented Kalman Filter (UKF)

The EKF linearizes by **differentiating** — it approximates a nonlinear *function* by
its tangent. The **Unscented Kalman Filter (UKF)** takes a smarter route, captured by a
memorable principle: *it is easier to approximate a probability distribution than an
arbitrary nonlinear function.* Instead of a Jacobian, it propagates a small, carefully
chosen set of **sample points** through the **exact** nonlinear function and rebuilds a
Gaussian from where they land. No derivatives required.

**Sigma points.** From the current mean `x` and covariance `P`, deterministically pick
`2n + 1` **sigma points** that exactly capture the distribution's mean and covariance —
the center point plus pairs spread symmetrically along the covariance ellipse's axes
(via a matrix square root of `P`):

$$ \mathcal{X}_0 = \hat{x}, \qquad \mathcal{X}_i = \hat{x} \pm \left(\sqrt{(n+\lambda)\,P}\right)_i $$

```
       sigma points placed on the covariance ellipse:
                    χ₂
                    ●
            χ₃ ●   (x̂)   ● χ₁       (center + symmetric pairs;
                    ●                  weights wᵢ recombine them)
                    χ₄
```

**The unscented transform** — the engine of the UKF:

1. **Pick** sigma points from `(x, P)`.
2. **Propagate** each one through the true nonlinear `f` (or `h`) — no linearization.
3. **Recombine** the transformed points with their weights into a new mean and
   covariance: `x' = Σ wᵢ f(χᵢ)`, and similarly for `P'`.

Slot the unscented transform into the predict (through `f`) and update (through `h`)
and you have the UKF — the same Bayes-filter skeleton, with sigma points where the EKF
had Jacobians.

**UKF vs EKF:**

```
 EKF: linearize via Jacobian (1st-order Taylor); needs derivatives;
      accurate only if nonlinearity is mild over the uncertainty span
 UKF: propagate sigma points through the EXACT function; derivative-FREE;
      captures the mean to 2nd/3rd order -> more accurate for strong nonlinearity
```

The UKF is typically **more accurate** (it captures curvature the EKF's tangent
misses), **derivative-free** (no error-prone Jacobians to hand-derive — great when `f`
is a complex simulator), and **comparable in cost** (O(n³), dominated by the matrix
square root, like the EKF's matrix ops). Its main subtleties are choosing the spread
parameters (`α, β, κ`) and keeping `P` positive-definite.

The UKF belongs to the broader family of **Gaussian/sigma-point filters** (with the
cubature Kalman filter a close relative). The mental model: **EKF approximates the
function; UKF approximates the distribution** — and approximating the distribution with
a few well-placed points usually wins. Both still assume the posterior is roughly
**Gaussian and unimodal**, though. When the truth is multi-modal or the nonlinearity is
severe, we abandon the Gaussian entirely and represent the belief with **particles** —
next.
""",
        ),
        _t(
            "The particle filter",
            "12 min",
            r"""# The particle filter

The Kalman family — KF, EKF, UKF — all assume the belief is a single **Gaussian**. But
many real problems are **multi-modal**: a robot in a symmetric building could be in
several places at once; a tracked object might be "here *or* there." When the
distribution is non-Gaussian or multi-modal, we need a representation that can be **any
shape at all**. The **particle filter** (a *sequential Monte Carlo* method) provides it
by representing the belief with a **swarm of weighted samples — particles**.

Each particle is one hypothesis "the state is *here*," and its **weight** is "how
plausible." Together they approximate the full posterior; more particles cluster where
the state probably is. It's a direct, sampled implementation of the Bayes filter.

**The three-step loop:**

1. **Predict (sample the motion model).** Move every particle forward through the
   motion model, adding process noise — each particle takes its own noisy step. The
   cloud **spreads**, mirroring growing uncertainty.

2. **Update (weight by likelihood).** For each particle, score how well it explains the
   new measurement using the measurement likelihood — for Gaussian sensor noise,

   $$ w_i \;\propto\; \exp\!\left(-\frac{(z - h(x_i))^2}{2\sigma^2}\right) $$

   then normalize so the weights sum to 1. Particles consistent with the data get heavy
   weights; inconsistent ones get crushed. This is **importance sampling**.

3. **Resample.** Over time a few particles hog all the weight and the rest become
   useless — **degeneracy**. Resampling **draws a new set**, picking particles with
   probability ∝ their weight (so heavy particles spawn copies, light ones die), then
   resets weights to equal. The swarm **concentrates** on the plausible region.

```
 PREDICT  ●  ● ● ●  ●  ●     spread the cloud via the motion model
 UPDATE   ·  ● O ●  ·  ·     weight by measurement likelihood (O = heaviest)
 RESAMPLE    ●●●● ●          redraw ∝ weight: keep the good, drop the bad
```

**Degeneracy and resampling quality.** The **effective sample size**
`N_eff ≈ 1 / Σ wᵢ²` measures how many particles really "count"; when it drops too low,
resample. The naive multinomial draw adds variance, so practical filters use
**low-variance (systematic) resampling** — one random offset, then evenly spaced
pointers along the cumulative-weight line — which is cheaper and adds less noise (you'll
implement it deterministically in the lab). Resample *too* eagerly and you cause
**sample impoverishment** (all particles collapse to a few duplicates, losing
diversity); a little process noise and resampling only when `N_eff` is low keeps the
swarm healthy.

**Strengths and costs:**

```
 + handles ARBITRARY distributions: nonlinear, non-Gaussian, MULTI-MODAL
 + simple to implement; no Jacobians, no Gaussian assumption
 − cost grows with particle count; the curse of dimensionality
   (high-dimensional states need exponentially many particles)
 − must manage degeneracy / impoverishment (N_eff, resampling, jitter)
```

Particle filters shine in **robot localization** (Monte Carlo Localization recovers
from the "kidnapped robot" because multi-modal beliefs are natural), tracking, and
non-Gaussian problems — wherever a single bell curve simply can't describe where you
might be. The lab builds a 1-D localization particle filter end to end: predict, weight
by a Gaussian likelihood, and low-variance resample.
""",
        ),
        _code(
            "EKF: estimating position from range to a beacon",
            "14 min",
            r"""# An EKF localizes a robot from a NONLINEAR measurement: the range to a known
# beacon, h(x,y) = sqrt((x-bx)^2 + (y-by)^2). We linearize h each step via its
# Jacobian H = [(x-bx)/r, (y-by)/r] and run the Kalman update. All matrix algebra
# is at MODULE LEVEL inside a straight-line loop. Deterministic noise. numpy.

import numpy as np

dt = 1.0
steps = 30
bx = 10.0          # beacon position
by = 0.0

# State x = [px, py]. Robot moves with (almost) constant velocity; we model it as a
# random-walk position (F = I) with process noise Q absorbing the motion.
F = np.eye(2)
Q = np.array([[0.5, 0.0], [0.0, 0.5]])
R = np.array([[0.5]])           # range-measurement variance
I2 = np.eye(2)

# Ground truth: robot drives in +x. Deterministic range-measurement noise.
k = np.arange(steps)
true_px = 0.5 * k
true_py = 2.0 + 0.0 * k
raw = np.sin(2.3 * k) + np.sin(6.1 * k + 1.0) + np.sin(12.7 * k + 2.0)
range_noise = 0.5 * (raw - raw.mean()) / raw.std()
true_range = np.sqrt((true_px - bx) ** 2 + (true_py - by) ** 2)
z_all = true_range + range_noise

# Initial belief: a poor guess with large covariance.
x = np.array([[0.0], [0.0]])
P = np.array([[5.0, 0.0], [0.0, 5.0]])

errs = np.zeros(steps)
for i in range(steps):
    # PREDICT (random-walk model -> mean unchanged, covariance grows by Q).
    x = F @ x
    P = F @ P @ F.T + Q
    # Linearize the nonlinear range measurement at the predicted state (MODULE level).
    dx = float(x[0, 0]) - bx
    dy = float(x[1, 0]) - by
    r = np.sqrt(dx * dx + dy * dy) + 1e-9
    Hjac = np.array([[dx / r, dy / r]])         # Jacobian of h
    # UPDATE with the nonlinear innovation z - h(x).
    y = np.array([[z_all[i] - r]])
    S = Hjac @ P @ Hjac.T + R
    Kgain = P @ Hjac.T @ np.linalg.inv(S)
    x = x + Kgain @ y
    P = (I2 - Kgain @ Hjac) @ P
    errs[i] = float(np.sqrt((x[0, 0] - true_px[i]) ** 2 + (x[1, 0] - true_py[i]) ** 2))

print("beacon at (%.0f, %.0f); EKF estimates 2-D position from 1-D range." % (bx, by))
print("final estimate (%.2f, %.2f), truth (%.2f, %.2f)"
      % (x[0, 0], x[1, 0], true_px[-1], true_py[-1]))
print("position error: start %.2f -> end %.2f" % (errs[0], errs[-1]))
print("the Jacobian (unit line-of-sight vector) lets the linear KF handle a nonlinear sensor.")
""",
        ),
        _code(
            "A 1-D particle filter with low-variance resampling",
            "14 min",
            r"""# A particle filter localizes a 1-D robot from noisy position measurements, with NO
# Gaussian assumption. Loop: predict (move + process noise), weight by a Gaussian
# likelihood, then LOW-VARIANCE resample. Randomness comes from a hand-rolled LCG
# (no random module). All numpy at MODULE level, straight-line. Deterministic.

import numpy as np

steps = 40
npart = 400

# Deterministic pseudo-random stream via a linear congruential generator (LCG),
# mapped to U(0,1). (The sandbox has no random module.)
count = npart + steps * (2 * npart + 1) + 10
state = 12345
lcg = np.zeros(count)
for i in range(count):
    state = (1103515245 * state + 12345) % 2147483648
    lcg[i] = state / 2147483648.0
cursor = 0

# Ground truth: robot drifts right at 1.0 unit/step. Deterministic measurement noise.
k = np.arange(steps)
truth = 1.0 * k
raw = np.sin(2.7 * k) + np.sin(6.3 * k + 1.0) + np.sin(13.9 * k + 2.0)
z_all = truth + 1.5 * (raw - raw.mean()) / raw.std()

move = 1.0          # known control (step size)
proc_std = 0.4      # process-noise std
meas_var = 2.25     # measurement-noise variance (sensor sigma^2 = 1.5^2)

# Initial particles spread uniformly over [-5, 5]; equal weights.
particles = -5.0 + 10.0 * lcg[cursor:cursor + npart]
cursor = cursor + npart
weights = np.ones(npart) / npart

est = np.zeros(steps)
for t in range(steps):
    # PREDICT: move every particle and add Gaussian-ish process noise.
    # Box-Muller turns two uniforms into a standard normal (module-level numpy).
    u1 = lcg[cursor:cursor + npart]
    u2 = lcg[cursor + npart:cursor + 2 * npart]
    cursor = cursor + 2 * npart
    gauss = np.sqrt(-2.0 * np.log(u1 + 1e-12)) * np.cos(2.0 * np.pi * u2)
    particles = particles + move + proc_std * gauss

    # UPDATE: weight by the Gaussian measurement likelihood, then normalise.
    diff = z_all[t] - particles
    weights = np.exp(-(diff * diff) / (2.0 * meas_var))
    weights = weights / weights.sum()
    est[t] = float(np.sum(weights * particles))

    # LOW-VARIANCE (systematic) resampling: one offset, evenly spaced pointers.
    positions = (np.arange(npart) + lcg[cursor]) / npart
    cursor = cursor + 1
    cumsum = np.cumsum(weights)
    idx = np.searchsorted(cumsum, positions)
    idx = np.clip(idx, 0, npart - 1)
    particles = particles[idx]
    weights = np.ones(npart) / npart

err = float(np.sqrt(np.mean((est - truth) ** 2)))
print("particle filter: %d particles, %d steps" % (npart, steps))
print("final estimate %.2f (truth %.1f)" % (est[-1], truth[-1]))
print("RMS tracking error = %.3f" % err)
print("the weighted swarm tracks the robot with no Gaussian/linearity assumption;")
print("low-variance resampling fights degeneracy while keeping particle diversity.")
""",
        ),
        _t(
            "Smoothing (MAP / factor graphs), fusion & consistency",
            "12 min",
            r"""# Smoothing (MAP / factor graphs), fusion & consistency

Three threads tie the whole track together: estimating over a **whole trajectory** (not
just the latest state), **fusing many sensors**, and **checking** that an estimator is
actually telling the truth about its own uncertainty.

**Filtering vs smoothing.** A filter estimates `x_t` from measurements **up to now** —
ideal for real-time control. A **smoother** estimates each `x_t` using **all** the data,
including the **future**, so later observations correct earlier states. Smoothing is
strictly more accurate (more evidence per state) but needs the data after the fact —
perfect for **offline** mapping, calibration, and trajectory reconstruction.

**The MAP / factor-graph view.** Modern estimation (especially SLAM) reframes the whole
trajectory as one big **optimization**: find the trajectory `X = (x₀, …, x_T)` that is
**most probable given all measurements** — the **Maximum A Posteriori (MAP)** estimate:

$$ \hat{X} = \arg\max_X \; p(X \mid Z) = \arg\min_X \sum_k \lVert r_k(X) \rVert^2_{\Sigma_k} $$

Because the noises are Gaussian, maximizing probability becomes **minimizing a sum of
squared, covariance-weighted residuals** — a giant **(weighted) nonlinear least
squares** problem (the Basics course, grown up). A **factor graph** is its natural
picture:

```
   (x₀)──■──(x₁)──■──(x₂)──■──(x₃)      ○ variable nodes  = states/poses
          │       │       │            ■ factor nodes    = constraints
          ◆       ◆       ◆               (motion ■, measurement ◆),
        measurement / landmark factors    each a squared residual term
```

Variable nodes are unknown states; **factor nodes are constraints** (a motion model
between consecutive states, a measurement tying a state to data/a landmark), each
contributing one weighted-squared-error term. Solving = least squares over the graph
(Gauss-Newton / Levenberg-Marquardt). The graph is **sparse** (each factor touches few
variables), and exploiting that sparsity (e.g. iSAM) makes huge SLAM problems tractable
and **incremental**. This is the backbone of modern SLAM (GTSAM, g2o, Ceres).

**Multi-sensor fusion.** With many sensors, two patterns recur. **Centralized**: stack
all measurements into one filter / one factor graph (optimal, but couples everything).
**Decentralized**: each sensor produces a local estimate, then combine them (modular,
robust, but must avoid **double-counting** shared information). Either way, two
practical must-dos: **time-synchronize** measurements (timestamps, interpolation — a
late or mis-stamped reading poisons the fusion) and **handle frames/calibration**
(extrinsics between sensors). Sensors with **complementary** error characteristics
(camera + IMU = visual-inertial, LIDAR + wheel odometry) fuse best — each covers the
other's blind spots, just as in the complementary filter.

**Consistency — does the filter believe the right amount?** An estimate is only useful
if its **covariance is honest**. A filter is **inconsistent** if it's
**over-confident** (P too small — it ignores data and diverges, the killer failure) or
under-confident (P too large — sluggish). Check it with the **innovations**:

- **NIS (Normalized Innovation Squared)**, `yᵀS⁻¹y`, tests the measurements: if the
  filter is consistent it follows a **chi-squared** distribution with `dim(z)` degrees
  of freedom; averaged over time it should sit inside the chi-squared confidence bounds.
  Persistently **above** → over-confident (R or P too small); **below** → pessimistic.
- **NEES (Normalized Estimation Error Squared)**, `(x−x̂)ᵀP⁻¹(x−x̂)`, needs ground truth
  (simulation) and tests the **state** error against `P` the same way.
- The innovation sequence should also be **zero-mean and white** (uncorrelated) — bias
  or correlation flags a wrong model or mistuned Q/R (the tuning hook from the
  Intermediate course).

The grand summary of the track: estimation is **recursive Bayesian inference** —
predict with a model, update with data, each weighted by trust. The Kalman filter
solves it exactly when linear-Gaussian; the EKF/UKF stretch it to nonlinear; the
particle filter abandons Gaussians for arbitrary beliefs; factor-graph smoothing
optimizes the whole trajectory at once. And across all of them, **consistency checks**
keep the reported uncertainty honest — because in estimation, *knowing how much you
don't know* is just as important as the estimate itself.
""",
        ),
        quiz_lesson(
            "Quiz: Nonlinear & Modern Estimation",
            (
                q(
                    "How does the Extended Kalman Filter handle nonlinear models?",
                    (
                        opt(
                            "It linearizes f and h via their Jacobians (first-order Taylor) at the current estimate each step, then runs the ordinary Kalman equations",
                            correct=True,
                        ),
                        opt("It ignores the nonlinearity entirely"),
                        opt("It uses sigma points instead of derivatives"),
                        opt("It only works if the system is already linear"),
                    ),
                    "The EKF recomputes Jacobians F = ∂f/∂x and H = ∂h/∂x at the latest estimate. It can diverge if the nonlinearity is strong over the uncertainty span.",
                ),
                q(
                    "What is the core idea of the Unscented Kalman Filter (UKF)?",
                    (
                        opt(
                            "Propagate a deterministic set of sigma points through the EXACT nonlinear function (the unscented transform) — derivative-free, more accurate than the EKF's tangent",
                            correct=True,
                        ),
                        opt("Use random particles weighted by likelihood"),
                        opt("Differentiate the model to second order"),
                        opt("Assume the system is linear"),
                    ),
                    "The UKF approximates the distribution (sigma points) rather than the function (Jacobian); it's derivative-free and captures more curvature, at similar O(n³) cost.",
                ),
                q(
                    "What are the three steps of a particle filter?",
                    (
                        opt(
                            "Predict (move particles via the motion model + noise), update (weight by measurement likelihood), and resample (redraw ∝ weight to fight degeneracy)",
                            correct=True,
                        ),
                        opt("Linearize, invert, integrate"),
                        opt("Encode, transmit, decode"),
                        opt("Sort, filter, average — with no weighting"),
                    ),
                    "Particles = weighted samples of an arbitrary belief; importance weighting + resampling implement the Bayes filter for non-Gaussian, multi-modal problems.",
                ),
                q(
                    "What problem does resampling in a particle filter solve, and what risk does over-resampling create?",
                    (
                        opt(
                            "It fixes degeneracy (a few particles hogging all the weight); resampling too eagerly causes sample impoverishment (loss of diversity). Watch N_eff",
                            correct=True,
                        ),
                        opt("It adds new sensors to the system"),
                        opt("It makes the filter linear"),
                        opt("It has no downside and should be done every step regardless"),
                    ),
                    "Resample ∝ weight when the effective sample size N_eff ≈ 1/Σwᵢ² drops; low-variance resampling adds less noise, and a little jitter preserves diversity.",
                ),
                q(
                    "How does a factor-graph / MAP formulation cast trajectory estimation?",
                    (
                        opt(
                            "As one big (weighted) nonlinear least-squares problem — minimise the sum of covariance-weighted squared residuals from motion and measurement factors over the whole trajectory",
                            correct=True,
                        ),
                        opt("As a single Kalman update with no past states"),
                        opt("As a linear program with no noise model"),
                        opt("By ignoring all but the latest measurement"),
                    ),
                    "Gaussian noise turns MAP into least squares; factor nodes are constraints, variable nodes are states, and exploiting sparsity (iSAM) scales modern SLAM.",
                ),
                q(
                    "What does a NIS/NEES consistency check tell you about a filter?",
                    (
                        opt(
                            "Whether its reported covariance is honest — NIS/NEES should follow a chi-squared distribution; persistently too high means over-confident, too low means pessimistic",
                            correct=True,
                        ),
                        opt("How fast the filter runs"),
                        opt("The number of sensors used"),
                        opt("Nothing about uncertainty, only the mean"),
                    ),
                    "Innovations should be zero-mean, white, and consistent with S; NIS = yᵀS⁻¹y and NEES = (x−x̂)ᵀP⁻¹(x−x̂) test that the filter neither over- nor under-states its uncertainty.",
                ),
            ),
        ),
    ),
)


ESTIMATION_COURSES = (_EST_BASICS, _EST_INTERMEDIATE, _EST_ADVANCED)
