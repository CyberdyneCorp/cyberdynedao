"""Mathematics for Life Sciences track: Basics -> Intermediate -> Advanced.

A quantitative-biology track that builds from functions, rates of change and
basic calculus, through linear algebra, probability and differential equations,
to dynamical models of population growth, enzyme kinetics and pharmacokinetics.
Every lesson carries an interactive ```plot block (real biological curves) or a
```mermaid diagram (pathways, model structure, fitting pipelines).
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Mathematics for Life Sciences — Basics ───────────────────────────────────

_BASICS = SeedCourse(
    slug="math-life-sciences-basics",
    title="Mathematics for Life Sciences — Basics",
    description=(
        "Build the quantitative intuition every biologist needs: functions and "
        "units, exponential and logarithmic growth, rates of change, the "
        "derivative as an instantaneous rate, and the saturating curves that "
        "describe enzymes, binding and dose-response. Worked with interactive "
        "plots and pathway diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Functions, variables and units in biology",
            "10 min",
            r"""
# Functions, variables and units in biology

A **function** is a rule that assigns exactly one output to each input. In life
sciences we constantly relate one measured quantity to another: bacterial
density $N$ as a function of time $t$, reaction rate $v$ as a function of
substrate concentration $[S]$, or oxygen saturation as a function of partial
pressure. We write $N = f(t)$ and read it as "$N$ depends on $t$".

Two ideas matter from day one. First, the **domain** (allowed inputs) is set by
biology: time and concentration cannot be negative, so $t \geq 0$ and
$[S] \geq 0$. Second, every quantity carries **units**. A rate constant for
first-order decay has units of $1/\text{time}$ (e.g. $\text{h}^{-1}$); a
Michaelis constant $K_m$ has units of concentration (e.g. $\mu M$). Checking
that both sides of an equation share units — **dimensional analysis** — catches
many modelling errors before any data are touched.

The simplest model is **linear**, $y = a x + b$, where $a$ is the slope (change
in $y$ per unit $x$) and $b$ the intercept. A calibration curve relating
absorbance to protein concentration is often treated as linear over a working
range.

```plot
{"title": "Linear calibration: absorbance vs concentration", "xLabel": "concentration (uM)", "yLabel": "absorbance (AU)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.08*x + 0.05", "label": "A = 0.08[c] + 0.05", "color": "#2563eb"}]}
```

**Next:** exponential growth and the doubling time of populations.
""",
        ),
        _t(
            "Exponential growth and doubling time",
            "11 min",
            r"""
# Exponential growth and doubling time

When each individual reproduces at a constant per-capita rate and resources are
unlimited, a population grows **exponentially**: $N(t) = N_0 e^{r t}$, where
$N_0$ is the starting size and $r$ the intrinsic growth rate (units
$1/\text{time}$). The defining property is that the *rate of increase is
proportional to the current size* — twice as many bacteria divide twice as fast.

The **doubling time** is the time for $N$ to double. Setting
$2 N_0 = N_0 e^{r t_d}$ gives $t_d = \frac{\ln 2}{r} \approx \frac{0.693}{r}$.
For *E. coli* in rich medium with $t_d \approx 20$ min, $r \approx 2.1\,
\text{h}^{-1}$. Exponential growth is explosive: starting from one cell, after
just 10 doublings there are over 1000 cells, after 20 over a million.

The same maths runs in reverse for **exponential decay** (radioactive tracers,
drug clearance), $N(t) = N_0 e^{-k t}$, with **half-life**
$t_{1/2} = \frac{\ln 2}{k}$.

```plot
{"title": "Exponential population growth", "xLabel": "time (h)", "yLabel": "relative size N/N0", "xRange": [0, 6], "yRange": [0, 6], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "N = N0 e^(0.3 t)", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  A[1 cell] --> B[2 cells] --> C[4 cells] --> D[8 cells] --> E[... doubling each generation]
```

**Next:** taming explosive curves with logarithms.
""",
        ),
        _t(
            "Logarithms: pH, log scales and linearising data",
            "10 min",
            r"""
# Logarithms: pH, log scales and linearising data

The **logarithm** is the inverse of the exponential: if $y = e^x$ then
$x = \ln y$. Logs turn multiplication into addition
($\log(ab) = \log a + \log b$) and powers into products
($\log(a^n) = n \log a$). This is exactly what we need when quantities span
many orders of magnitude.

Biology is full of log scales. **pH** is defined as
$\text{pH} = -\log_{10}[\text{H}^+]$, so a one-unit pH drop means a ten-fold
rise in hydrogen-ion concentration. Decibels, the Richter scale, and serial
dilutions are all logarithmic.

Logs also **linearise** exponential data. Take $N(t) = N_0 e^{r t}$ and apply
the natural log: $\ln N = \ln N_0 + r t$. Plotting $\ln N$ against $t$ gives a
straight line whose slope is the growth rate $r$ — the standard way to read a
growth rate off a bacterial growth curve, and far more robust than guessing
$r$ from the raw exponential.

```plot
{"title": "Semi-log: ln N is linear in time", "xLabel": "time (h)", "yLabel": "ln(N/N0)", "xRange": [0, 6], "yRange": [0, 2], "grid": true, "functions": [{"expr": "0.3*x", "label": "ln N = r t, slope = r", "color": "#dc2626"}]}
```

**Next:** the derivative — measuring instantaneous rates of change.
""",
        ),
        _t(
            "Rates of change and the derivative",
            "12 min",
            r"""
# Rates of change and the derivative

Biology cares about *rates*: how fast a tumour grows, how quickly a drug leaves
the blood, how steeply firing rate rises with stimulus. The **average rate of
change** of $y = f(x)$ between two points is the slope of the connecting line,
$\frac{\Delta y}{\Delta x} = \frac{f(x+h) - f(x)}{h}$.

Shrink the interval $h$ toward zero and this average becomes the
**instantaneous rate of change**, the **derivative**:
$$\frac{dy}{dx} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$
Geometrically it is the slope of the tangent line at a point. For population
size, $\frac{dN}{dt}$ is the instantaneous growth rate in cells per hour.

A few derivatives recur constantly: the derivative of $e^{rt}$ is $r e^{rt}$
(exponential growth: rate proportional to size), and the derivative of a
constant is zero (no change at a steady state). Where a curve **peaks or
troughs** the derivative is zero — useful for finding the substrate level that
maximises a yield, or the time of peak drug concentration.

```plot
{"title": "A curve and the points where its slope is zero", "xLabel": "x", "yLabel": "f(x)", "xRange": [-3, 3], "yRange": [-2, 6], "grid": true, "functions": [{"expr": "x^2 - 1", "label": "f(x) = x^2 - 1 (min where slope = 0)", "color": "#2563eb"}]}
```

**Next:** the saturating curves of enzymes and binding.
""",
        ),
        _t(
            "Saturation curves: Michaelis-Menten and binding",
            "12 min",
            r"""
# Saturation curves: Michaelis-Menten and binding

Many biological responses **saturate**: increasing the input keeps raising the
output, but with diminishing returns toward a ceiling. The archetype is enzyme
kinetics. The **Michaelis-Menten** equation relates reaction velocity $v$ to
substrate concentration $[S]$:
$$v = \frac{V_{max}[S]}{K_m + [S]}$$
Here $V_{max}$ is the maximum velocity (all enzyme saturated) and $K_m$ the
**Michaelis constant**: the substrate concentration at which $v = V_{max}/2$.
A small $K_m$ means the enzyme reaches half-speed at low substrate — high
apparent affinity.

The same hyperbola describes **ligand binding** to a receptor: the fraction of
sites bound is $\frac{[L]}{K_d + [L]}$, where $K_d$ is the dissociation
constant. At low input the curve is nearly linear; at high input it flattens
toward its maximum.

```plot
{"title": "Michaelis-Menten saturation (Vmax=8, Km=2)", "xLabel": "[S] (uM)", "yLabel": "v (uM/s)", "xRange": [0, 30], "yRange": [0, 8], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "v = Vmax[S]/(Km+[S])", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  E[Enzyme E] -->|+ S| ES[Complex ES] -->|catalysis| P[Product P]
  ES -->|release| E
```

**Next:** S-shaped dose-response and cooperative curves.
""",
        ),
        _t(
            "Dose-response and the sigmoid curve",
            "11 min",
            r"""
# Dose-response and the sigmoid curve

Pharmacology and toxicology summarise the effect of a drug or toxin with a
**dose-response curve**. Plotted against the *logarithm* of dose, the response
is typically **sigmoidal** (S-shaped): little effect at low dose, a steep rise
through a transition region, and a plateau at maximal effect.

The key summary statistic is the **EC50** (or, for inhibition, IC50): the dose
giving 50% of the maximal response. A common model is the **Hill equation**,
$$E = \frac{E_{max}\,[D]^n}{EC_{50}^{\,n} + [D]^n}$$
where the **Hill coefficient** $n$ measures steepness and cooperativity. With
$n = 1$ the curve is a plain hyperbola; with $n > 1$ (positive cooperativity,
as in oxygen binding to haemoglobin) it becomes markedly S-shaped on a linear
axis. The logistic function $\frac{1}{1 + e^{-(x - x_0)}}$ is the same shape and
recurs in growth models and classifiers.

```plot
{"title": "Sigmoid dose-response (EC50 at x = 5)", "xLabel": "log dose", "yLabel": "fraction of max effect", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "logistic dose-response", "color": "#dc2626"}]}
```

**Next:** a short quiz to consolidate the Basics.
""",
        ),
        _quiz(),
    ),
)


# ── Mathematics for Life Sciences — Intermediate ─────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="math-life-sciences-intermediate",
    title="Mathematics for Life Sciences — Intermediate",
    description=(
        "The core quantitative toolkit: integration and accumulated change, "
        "vectors and matrices for stage-structured populations and compartment "
        "models, probability and the distributions behind biological data, "
        "linear regression and nonlinear curve fitting, and first-order "
        "differential equations. Plots and diagrams throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Integration: accumulating change",
            "12 min",
            r"""
# Integration: accumulating change

If the derivative answers "how fast?", the **integral** answers "how much in
total?". Integration is the inverse operation: it accumulates a rate over an
interval to give a net amount. The **definite integral**
$\int_a^b f(t)\,dt$ is the (signed) area under the curve $f$ between $t = a$ and
$t = b$.

This is everywhere in physiology and pharmacology. If $C(t)$ is the
concentration of a drug in plasma over time, the **AUC** (area under the curve),
$\int_0^\infty C(t)\,dt$, measures total systemic exposure and underpins
bioequivalence testing. If a population grows at rate $g(t)$, then
$\int_0^T g(t)\,dt$ is the total number added over $[0, T]$.

The **Fundamental Theorem of Calculus** ties the two operations together: if
$F'(t) = f(t)$, then $\int_a^b f(t)\,dt = F(b) - F(a)$. For example,
$\int_0^\infty C_0 e^{-k t}\,dt = \frac{C_0}{k}$ — the AUC of a single-dose,
first-order elimination curve is simply $C_0/k$.

```plot
{"title": "AUC: area under a drug concentration curve", "xLabel": "time (h)", "yLabel": "concentration", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "C(t) = C0 e^(-k t); AUC = C0/k", "color": "#2563eb"}]}
```

**Next:** vectors and matrices for structured populations.
""",
        ),
        _t(
            "Vectors and matrices for biological systems",
            "12 min",
            r"""
# Vectors and matrices for biological systems

A **vector** holds several numbers at once — for example the abundances of three
life stages, $\mathbf{n} = (n_{\text{egg}}, n_{\text{juv}}, n_{\text{adult}})$.
A **matrix** is a rectangular table of numbers that *transforms* one vector into
another. Matrix-vector multiplication applies a rule to every component at once.

In demography, the **Leslie / Lefkovitch matrix** $\mathbf{A}$ projects a
stage-structured population one time step forward: $\mathbf{n}_{t+1} =
\mathbf{A}\,\mathbf{n}_t$. The matrix entries encode survival probabilities
(sub-diagonal) and fecundities (top row). Iterating the projection forecasts
the population trajectory and its eventual stage distribution.

Matrices also describe **compartment models**: rates of flow between
compartments (blood, tissue, gut) become entries of a transition matrix that
drives a system of differential equations. Solving such systems and analysing
their long-term behaviour is the bread and butter of pharmacokinetics and
systems biology.

```mermaid
flowchart LR
  Egg -->|survival s1| Juv
  Juv -->|survival s2| Adult
  Adult -->|fecundity f| Egg
```

```plot
{"title": "Projected total population size over time", "xLabel": "generation", "yLabel": "total N", "xRange": [0, 10], "yRange": [0, 100], "grid": true, "functions": [{"expr": "10*exp(0.2*x)", "label": "growth set by dominant eigenvalue", "color": "#16a34a"}]}
```

**Next:** eigenvalues and the long-run growth rate.
""",
        ),
        _t(
            "Eigenvalues and long-run population growth",
            "12 min",
            r"""
# Eigenvalues and long-run population growth

When a projection matrix $\mathbf{A}$ acts on most vectors it both rotates and
rescales them. But some special directions are only *stretched*, not turned:
for an **eigenvector** $\mathbf{v}$, $\mathbf{A}\mathbf{v} = \lambda \mathbf{v}$,
where the scalar $\lambda$ is its **eigenvalue**. Eigenvalues capture the
intrinsic behaviour of a linear system independent of starting conditions.

For a Leslie matrix the **dominant eigenvalue** $\lambda_1$ (the largest in
magnitude) is the **asymptotic growth rate** per time step: $\lambda_1 > 1$
means long-run growth, $\lambda_1 < 1$ decline, $\lambda_1 = 1$ a stationary
population. Its eigenvector gives the **stable stage distribution** — the fixed
proportions of eggs, juveniles and adults the population settles into,
whatever its initial composition.

The same idea governs stability of equilibria in differential-equation models:
eigenvalues of the system's **Jacobian** at a steady state determine whether
small perturbations decay (stable) or grow (unstable).

```plot
{"title": "Long-run growth set by the dominant eigenvalue", "xLabel": "time step", "yLabel": "log total N", "xRange": [0, 10], "yRange": [0, 5], "grid": true, "functions": [{"expr": "0.4*x", "label": "slope = ln(lambda1)", "color": "#dc2626"}]}
```

**Next:** probability and the randomness in biological data.
""",
        ),
        _t(
            "Probability and distributions in biology",
            "12 min",
            r"""
# Probability and distributions in biology

Biological measurements are noisy, so we model them with **probability
distributions**. A distribution assigns probabilities to outcomes; its **mean**
$\mu$ is the long-run average and its **variance** $\sigma^2$ the spread.

Three distributions cover most cases. The **binomial** counts successes in $n$
independent yes/no trials (e.g. number of seeds that germinate) with mean $np$.
The **Poisson** models counts of rare independent events in a fixed window
(mutations per genome, colonies per plate, spikes per second); its mean equals
its variance, $\lambda$. The **normal** (Gaussian) — the familiar bell curve —
describes continuous traits like height or blood pressure and arises naturally
whenever many small effects add up (the **Central Limit Theorem**).

Knowing the right distribution matters: count data are better analysed with
Poisson or negative-binomial models than by forcing them into a normal
framework, and this choice drives which statistical test or regression you use.

```plot
{"title": "Normal (Gaussian) density, mean 0", "xLabel": "value", "yLabel": "probability density", "xRange": [-4, 4], "yRange": [0, 0.45], "grid": true, "functions": [{"expr": "exp(-x^2/2)/sqrt(6.283)", "label": "standard normal N(0,1)", "color": "#2563eb"}]}
```

**Next:** fitting models to data with regression.
""",
        ),
        _t(
            "Linear regression and curve fitting",
            "12 min",
            r"""
# Linear regression and curve fitting

To extract parameters from data we **fit a model**. **Linear regression** finds
the line $y = a x + b$ that best predicts $y$ from $x$ by minimising the sum of
squared residuals, $\sum_i (y_i - (a x_i + b))^2$ — the **least-squares**
criterion. The slope $a$ estimates how much $y$ changes per unit $x$; the
coefficient of determination $R^2$ reports the fraction of variance explained.

Many biological relationships are **nonlinear** (Michaelis-Menten, sigmoid
dose-response, exponential growth). Two routes exist. You can **linearise** —
e.g. the Lineweaver-Burk double-reciprocal plot turns Michaelis-Menten into a
straight line $1/v$ vs $1/[S]$ — but this distorts the error structure and is
now discouraged. The modern approach is **nonlinear least squares**, fitting the
curve directly (e.g. `scipy.optimize.curve_fit`) to estimate $V_{max}$ and
$K_m$ with proper confidence intervals.

```plot
{"title": "Least-squares line through noisy data", "xLabel": "x", "yLabel": "y", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "1.1*x + 0.5", "label": "best-fit line (minimises sum of squares)", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  D[Data points] --> M[Model y = f(x; params)]
  M --> L[Loss = sum of squared residuals]
  L --> O[Optimise params to minimise loss]
  O --> F[Fitted parameters + CIs]
```

**Next:** differential equations and rates that drive change.
""",
        ),
        _t(
            "First-order differential equations",
            "12 min",
            r"""
# First-order differential equations

A **differential equation** specifies the *rate* of change of a quantity rather
than the quantity itself, and is the natural language of dynamic biology. The
simplest, $\frac{dN}{dt} = r N$, says the growth rate is proportional to the
current size; its solution is exponential, $N(t) = N_0 e^{r t}$.

A more realistic model adds a ceiling. The **logistic equation**
$$\frac{dN}{dt} = r N \left(1 - \frac{N}{K}\right)$$
introduces a **carrying capacity** $K$: growth is near-exponential when $N$ is
small but slows to zero as $N \to K$. Its solution is the S-shaped logistic
curve, widely used for resource-limited population and tumour growth.

A first-order decay model, $\frac{dC}{dt} = -k C$, gives $C(t) = C_0 e^{-k t}$
and is the foundation of single-compartment **pharmacokinetics**. The general
skill is reading a model's qualitative behaviour from its equation: where
$\frac{dN}{dt} = 0$ are the **steady states**, and the sign of the rate either
side tells you whether they are stable.

```plot
{"title": "Logistic growth toward carrying capacity K=10", "xLabel": "time", "yLabel": "population N", "xRange": [0, 12], "yRange": [0, 11], "grid": true, "functions": [{"expr": "10/(1+9*exp(-0.8*x))", "label": "N(t), logistic with K = 10", "color": "#dc2626"}]}
```

**Next:** a quiz on the intermediate toolkit.
""",
        ),
        _quiz(),
    ),
)


# ── Mathematics for Life Sciences — Advanced ─────────────────────────────────

_ADVANCED = SeedCourse(
    slug="math-life-sciences-advanced",
    title="Mathematics for Life Sciences — Advanced",
    description=(
        "State-of-the-art quantitative biology: nonlinear dynamics and stability "
        "analysis, predator-prey and epidemic (SIR) systems, enzyme-kinetics "
        "parameter estimation, multi-compartment pharmacokinetics, stochastic "
        "modelling of molecular noise, and machine-learning / scientific-computing "
        "methods for fitting and simulating biological models."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Nonlinear dynamics, equilibria and stability",
            "13 min",
            r"""
# Nonlinear dynamics, equilibria and stability

Most real biological systems are **nonlinear**, and their interesting behaviour
lives at and around **equilibria** (steady states) where all rates vanish,
$\frac{dx}{dt} = 0$. The central question is **stability**: if the system is
nudged, does it return to equilibrium or run away?

For a one-variable system $\frac{dx}{dt} = f(x)$, linearise near an equilibrium
$x^*$: stability is decided by the sign of $f'(x^*)$. If $f'(x^*) < 0$ the
perturbation decays (stable); if $f'(x^*) > 0$ it grows (unstable). For systems
of several variables, compute the **Jacobian matrix** of partial derivatives and
examine its **eigenvalues** — all with negative real part means a stable
equilibrium. As a parameter changes, equilibria can appear, vanish or swap
stability: a **bifurcation**, the mathematical signature of a biological switch
or tipping point.

```plot
{"title": "Phase line: dx/dt vs x (stable root where slope < 0)", "xLabel": "x", "yLabel": "dx/dt = r x (1 - x/K)", "xRange": [0, 12], "yRange": [-3, 3], "grid": true, "functions": [{"expr": "0.5*x*(1 - x/10)", "label": "logistic rate; x*=10 stable, x*=0 unstable", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  P[Perturbation] --> J[Linearise: Jacobian at x*]
  J --> E{Re of all eigenvalues < 0?}
  E -->|yes| S[Stable: returns]
  E -->|no| U[Unstable: diverges]
```

**Next:** predator-prey and competition dynamics.
""",
        ),
        _t(
            "Predator-prey and interacting populations",
            "13 min",
            r"""
# Predator-prey and interacting populations

Coupled species are modelled with **systems** of differential equations. The
classic **Lotka-Volterra** predator-prey model is
$$\frac{dN}{dt} = \alpha N - \beta N P, \qquad
\frac{dP}{dt} = \delta N P - \gamma P$$
where $N$ is prey, $P$ predators. Prey grow exponentially but are eaten at a
rate proportional to encounters $NP$; predators die off but reproduce on the
prey they consume. The result is **sustained oscillations**: prey rise,
predators follow, prey crash, predators starve, and the cycle repeats — seen in
the lynx-hare records.

The basic model is idealised (neutral cycles, no prey ceiling). Realistic
variants add **logistic prey growth** and a saturating **Holling type-II
functional response** (predators saturate at high prey density, just like
Michaelis-Menten). Analysing the equilibria and their Jacobian eigenvalues
reveals whether the coexistence point is a stable spiral, a centre, or a stable
limit cycle.

```plot
{"title": "Predator-prey oscillation (prey abundance over time)", "xLabel": "time", "yLabel": "prey density N", "xRange": [0, 18], "yRange": [-1.5, 1.5], "grid": true, "functions": [{"expr": "sin(x)", "label": "cyclic prey dynamics (schematic)", "color": "#16a34a"}]}
```

**Next:** epidemic dynamics with the SIR model.
""",
        ),
        _t(
            "Epidemic modelling: the SIR system and R0",
            "13 min",
            r"""
# Epidemic modelling: the SIR system and R0

Infectious-disease dynamics are captured by **compartmental models**. The
**SIR** model splits a population into **S**usceptible, **I**nfectious and
**R**ecovered:
$$\frac{dS}{dt} = -\beta S I, \quad
\frac{dI}{dt} = \beta S I - \gamma I, \quad
\frac{dR}{dt} = \gamma I$$
Here $\beta$ is the transmission rate and $\gamma$ the recovery rate
(so $1/\gamma$ is the mean infectious period). The pivotal quantity is the
**basic reproduction number** $R_0 = \frac{\beta}{\gamma} S_0$: the expected
number of secondary cases from one infected individual in a fully susceptible
population.

The threshold theorem is sharp: if $R_0 > 1$ an epidemic takes off; if
$R_0 < 1$ it dies out. This also gives the **herd-immunity threshold**: an
epidemic is prevented once a fraction $1 - 1/R_0$ is immune. The infectious
curve typically rises, peaks when $S$ falls to $\gamma/\beta$, then declines —
the "flatten the curve" picture.

```plot
{"title": "Epidemic infectious curve I(t) (schematic)", "xLabel": "time (days)", "yLabel": "infectious fraction I", "xRange": [0, 10], "yRange": [0, 0.5], "grid": true, "functions": [{"expr": "0.5*exp(-(x-5)^2/2)", "label": "epidemic peak then decline", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  S[Susceptible] -->|beta S I| I[Infectious] -->|gamma I| R[Recovered]
```

**Next:** estimating enzyme-kinetics parameters from data.
""",
        ),
        _t(
            "Enzyme kinetics: parameter estimation",
            "13 min",
            r"""
# Enzyme kinetics: parameter estimation

Turning the Michaelis-Menten model into numbers means estimating $V_{max}$ and
$K_m$ from initial-velocity data $\{[S]_i, v_i\}$. Historically this was done by
**linearisation** — Lineweaver-Burk ($1/v$ vs $1/[S]$), Eadie-Hofstee, or
Hanes-Woolf plots. These are pedagogically neat but statistically biased: the
reciprocal transform inflates the influence of low-substrate points where noise
is largest, distorting the estimates.

The accepted modern method is **nonlinear least squares**: fit
$v = \frac{V_{max}[S]}{K_m + [S]}$ directly by minimising
$\sum_i (v_i - \hat v_i)^2$, using an optimiser such as Levenberg-Marquardt
(`scipy.optimize.curve_fit`) with sensible initial guesses. This yields unbiased
estimates and proper standard errors. For cooperative enzymes, fit the Hill
equation and report the Hill coefficient. **Weighted** fitting accounts for
heteroscedastic noise, and a **global fit** across inhibitor concentrations can
distinguish competitive from non-competitive inhibition by sharing parameters.

```plot
{"title": "Michaelis-Menten fit to initial-velocity data", "xLabel": "[S] (uM)", "yLabel": "v (uM/s)", "xRange": [0, 30], "yRange": [0, 8], "grid": true, "functions": [{"expr": "8*x/(4+x)", "label": "fitted v = Vmax[S]/(Km+[S]), Km=4", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  Assay[Initial-rate assay] --> Pts[v vs S data]
  Pts --> NLS[Nonlinear least squares]
  NLS --> Est[Vmax, Km plus standard errors]
```

**Next:** multi-compartment pharmacokinetics.
""",
        ),
        _t(
            "Pharmacokinetics: compartment models",
            "13 min",
            r"""
# Pharmacokinetics: compartment models

**Pharmacokinetics** (PK) describes what the body does to a drug — absorption,
distribution, metabolism, excretion (ADME) — using compartment models. The
**one-compartment** model treats the body as a single well-mixed volume $V_d$
with first-order elimination: $\frac{dC}{dt} = -k_e C$, so
$C(t) = C_0 e^{-k_e t}$, with half-life $t_{1/2} = \frac{\ln 2}{k_e}$ and
**clearance** $CL = k_e V_d$. The total exposure is
$\text{AUC} = \frac{\text{dose}}{CL}$.

Many drugs need a **two-compartment** model — a central (blood) and a peripheral
(tissue) compartment with exchange rate constants — giving a bi-exponential
decay: a fast **distribution** phase then a slower **elimination** phase. Oral
dosing adds an **absorption** rate $k_a$, producing the rise-then-fall plasma
profile. These models drive dosing-regimen design: loading and maintenance
doses are chosen so steady-state concentrations stay in the therapeutic window.
**Population PK** (nonlinear mixed-effects models, e.g. NONMEM/nlmixr) extends
this to whole patient populations with covariates like weight and renal
function.

```plot
{"title": "Oral PK profile: absorption then elimination", "xLabel": "time (h)", "yLabel": "plasma concentration", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x) - exp(-1.5*x)", "label": "C(t): ka absorption, ke elimination", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  Gut -->|ka| Central[Central blood]
  Central -->|k12| Peripheral[Tissue]
  Peripheral -->|k21| Central
  Central -->|ke| Out[Eliminated]
```

**Next:** stochastic models and computational methods.
""",
        ),
        _t(
            "Stochastic models and computational methods",
            "13 min",
            r"""
# Stochastic models and computational methods

When molecule numbers are small — a handful of mRNA copies, a few transcription
factors — randomness is not noise to be averaged away but a driver of biology.
Deterministic ODEs assume large, continuous concentrations; at low copy number
we need **stochastic models** where reactions fire as discrete random events. The
**Gillespie algorithm** (the stochastic simulation algorithm, SSA) generates
exact sample trajectories of such a chemical reaction network, capturing
intrinsic noise in gene expression and the bursty, switch-like behaviour ODEs
miss.

Modern quantitative biology leans heavily on **scientific computing and machine
learning**. Hard models are calibrated by **Bayesian inference** — MCMC or, when
the likelihood is intractable, **approximate Bayesian computation (ABC)** — to
get full posterior distributions over parameters rather than point estimates.
**Universal differential equations** and **physics-informed neural networks**
embed neural networks inside mechanistic ODEs to learn unknown terms from data.
**Surrogate / emulator** models (Gaussian processes, neural nets) replace
expensive simulators for fast inference and design, and deep learning now
predicts structure and dynamics across biology.

```plot
{"title": "Stochastic vs deterministic trajectory (schematic mean)", "xLabel": "time", "yLabel": "molecule count", "xRange": [0, 10], "yRange": [0, 20], "grid": true, "functions": [{"expr": "20*(1 - exp(-0.5*x))", "label": "ODE mean; SSA fluctuates around it", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  Data[Biological data] --> Inf[Bayesian inference / ABC / MCMC]
  Model[Mechanistic ODE plus neural term] --> Inf
  Inf --> Post[Posterior over parameters]
  Post --> Sim[Simulate and predict]
```

**Next:** a final quiz on advanced quantitative biology.
""",
        ),
        _quiz(),
    ),
)


MATH_LIFE_SCIENCES_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["MATH_LIFE_SCIENCES_COURSES"]
