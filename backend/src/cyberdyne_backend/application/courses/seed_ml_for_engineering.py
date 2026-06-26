"""Machine Learning for Engineering & Simulation track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on data-driven modelling: from regression
on experimental data, through surrogate and reduced-order models for expensive
simulations, to physics-informed neural networks and ML-accelerated solvers. Lessons
are `text` with LaTeX, interactive ```plot blocks (loss curves, regression fits,
ROM energy decay), ```mermaid workflow/classification diagrams and runnable
```python (NumPy/scikit-learn/PyTorch) and ```matlab code.
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, ε, ∇, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Machine Learning for Engineering & Simulation — Basics ────────────────────

_BASICS = SeedCourse(
    slug="ml-for-engineering-basics",
    title="Machine Learning for Engineering & Simulation — Basics",
    description=(
        "The intuition and fundamentals of machine learning for engineers: what "
        "data-driven modelling is and when to use it, the supervised learning "
        "workflow, linear and polynomial regression on experimental data, how to "
        "split data and avoid overfitting, and how to read a model with simple "
        "error metrics. Interactive plots, diagrams and Python throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What machine learning is for engineers",
            "10 min",
            r"""
# What machine learning is for engineers

Classical engineering builds **mechanistic models** from first principles —
Newton's laws, conservation of energy, constitutive laws like $\sigma = E\varepsilon$.
**Machine learning (ML)** instead *learns a mapping* $y = f(\mathbf{x})$ directly
from measured data, without writing the governing equations by hand. It earns its
place when the physics is unknown, too expensive to evaluate, or noisy — for
example predicting fatigue life from load history, or a turbine's efficiency from
operating conditions.

The two paradigms are complementary. A good engineer uses ML where data is
plentiful and mechanism is murky, and keeps physics where it is cheap and exact.

```mermaid
flowchart LR
  P["Physics: equations from first principles"] --> H["Hybrid model"]
  D["Data: experiments / simulations"] --> ML["ML: learn f(x) from data"]
  ML --> H
  H --> U["Prediction / control / design"]
```

Most engineering ML is **supervised**: we have inputs $\mathbf{x}$ and known
targets $y$, and we fit parameters that minimise prediction error. A typical
training curve falls quickly then flattens:

```plot
{"title": "Training loss vs epochs", "xLabel": "epoch", "yLabel": "loss", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "loss ~ exp(-0.4 epoch)", "color": "#2563eb"}]}
```

**Next:** the supervised learning workflow end to end.
""",
        ),
        _t(
            "The supervised learning workflow",
            "11 min",
            r"""
# The supervised learning workflow

Every supervised project follows the same loop: collect labelled data, split it,
choose a model, fit by minimising a **loss**, then evaluate on data the model has
never seen. The objective for regression is usually the mean squared error

$$\text{MSE} = \frac{1}{n}\sum_{i=1}^{n}\bigl(y_i - \hat{y}_i\bigr)^2,$$

where $\hat{y}_i = f(\mathbf{x}_i;\boldsymbol{\theta})$ is the prediction and
$\boldsymbol{\theta}$ the parameters tuned during training.

```mermaid
flowchart LR
  C["Collect data (x, y)"] --> S["Split: train / val / test"]
  S --> M["Choose model + loss"]
  M --> F["Fit theta on train"]
  F --> V["Tune on validation"]
  V --> E["Report on held-out test"]
```

The cardinal rule: **never report performance on data used to fit or tune.** The
held-out test set is your only honest estimate of how the model generalises.

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
model = LinearRegression().fit(X_tr, y_tr)
print("test MSE:", mean_squared_error(y_te, model.predict(X_te)))
```

**Next:** the simplest learner — linear regression.
""",
        ),
        _t(
            "Linear regression on engineering data",
            "12 min",
            r"""
# Linear regression on engineering data

Linear regression fits $\hat{y} = \theta_0 + \theta_1 x$ (or
$\hat{y} = \mathbf{X}\boldsymbol{\theta}$ in matrix form) by minimising squared
error. It has a closed-form **normal-equation** solution

$$\boldsymbol{\theta} = (\mathbf{X}^{\top}\mathbf{X})^{-1}\mathbf{X}^{\top}\mathbf{y},$$

which is exactly how the elastic region of a stress-strain test recovers Young's
modulus $E$ as the slope. Below, a material with $E$-like slope of 200 (units
scaled) gives a straight line until yielding:

```plot
{"title": "Linear fit of elastic stress-strain", "xLabel": "strain x", "yLabel": "stress y", "xRange": [0, 2], "yRange": [0, 400], "grid": true, "functions": [{"expr": "200*x", "label": "fit: y = 200 x", "color": "#2563eb"}]}
```

Compute the fit directly with NumPy:

```python
import numpy as np
X = np.column_stack([np.ones_like(x), x])      # design matrix [1, x]
theta = np.linalg.lstsq(X, y, rcond=None)[0]    # solves normal equations
slope = theta[1]                                # ~ Young's modulus
```

Linear models are interpretable — each coefficient is a sensitivity — and a strong
baseline. If a straight line is good enough, prefer it over anything fancier.

**Next:** when straight lines fail and we go polynomial.
""",
        ),
        _t(
            "Polynomial features and nonlinearity",
            "11 min",
            r"""
# Polynomial features and nonlinearity

Many engineering relationships curve: drag rises with the square of velocity, a
beam's deflection scales with $L^3$. We keep the *linear* machinery but enrich the
inputs with **polynomial features** $[1, x, x^2, x^3, \dots]$. The model stays
linear in its parameters, so the same least-squares solver applies.

A cubic deflection curve $\delta = \tfrac{FL^3}{3EI}$ in $x$ (length) bends upward:

```plot
{"title": "Cantilever tip deflection vs length", "xLabel": "length x", "yLabel": "deflection", "xRange": [0, 3], "yRange": [0, 10], "grid": true, "functions": [{"expr": "0.37*x^3", "label": "delta ~ x^3", "color": "#16a34a"}]}
```

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression

model = make_pipeline(PolynomialFeatures(degree=3), LinearRegression())
model.fit(x.reshape(-1, 1), y)
```

The danger: raise the degree too far and the curve wiggles through every noisy
point. Choosing the right complexity is the central tension of ML — the next
lesson on overfitting.

**Next:** the bias-variance trade-off and overfitting.
""",
        ),
        _t(
            "Overfitting, bias and variance",
            "12 min",
            r"""
# Overfitting, bias and variance

A model that is too simple **underfits** (high bias): it misses real structure. A
model that is too flexible **overfits** (high variance): it memorises noise and
fails on new data. Total expected error decomposes as

$$\mathbb{E}[(y-\hat{y})^2] = \text{bias}^2 + \text{variance} + \sigma^2_{\text{noise}},$$

and the sweet spot minimises the sum. Plotting error against model complexity, the
training error keeps falling while the validation error turns back up:

```plot
{"title": "Validation error vs model complexity", "xLabel": "complexity (poly degree)", "yLabel": "error", "xRange": [1, 10], "yRange": [0, 5], "grid": true, "functions": [{"expr": "0.3*(x-5)^2 + 0.5", "label": "validation error (U-shape)", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  L["Too simple"] --> B["High bias - underfit"]
  R["Too complex"] --> V["High variance - overfit"]
  B --> S["Sweet spot: tune on validation"]
  V --> S
```

Defences: hold out a validation set, use **cross-validation**, add
**regularisation** (penalise large coefficients), and prefer the simplest model
that explains the data — Occam's razor for engineers.

**Next:** measuring how good a model really is.
""",
        ),
        _t(
            "Evaluating models: metrics and residuals",
            "10 min",
            r"""
# Evaluating models: metrics and residuals

A single number rarely tells the whole story, so engineers report several. For
regression the staples are **RMSE** (in the units of $y$), **MAE** (robust to
outliers), and the **coefficient of determination**

$$R^2 = 1 - \frac{\sum_i (y_i-\hat{y}_i)^2}{\sum_i (y_i-\bar{y})^2},$$

which is the fraction of variance explained ($1.0$ is perfect, $0$ is no better
than predicting the mean).

Just as important is the **residual plot** $r_i = y_i - \hat{y}_i$. Healthy
residuals scatter randomly around zero; a curved or fanning pattern signals a
missing feature or non-constant variance.

```python
from sklearn.metrics import r2_score, mean_absolute_error
import numpy as np

resid = y_te - model.predict(X_te)
print("RMSE:", np.sqrt(np.mean(resid**2)))
print("MAE :", mean_absolute_error(y_te, model.predict(X_te)))
print("R2  :", r2_score(y_te, model.predict(X_te)))
```

```mermaid
flowchart LR
  P["Predictions"] --> R["Residuals r = y - yhat"]
  R --> D{"Pattern?"}
  D -->|random scatter| OK["Model OK"]
  D -->|curve / funnel| FIX["Add feature / transform"]
```

**Next:** check your understanding of ML fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── Machine Learning for Engineering & Simulation — Intermediate ──────────────

_INTERMEDIATE = SeedCourse(
    slug="ml-for-engineering-intermediate",
    title="Machine Learning for Engineering & Simulation — Intermediate",
    description=(
        "Core quantitative methods for engineering ML: regularised regression, "
        "feature engineering and dimensionality reduction with PCA, Gaussian "
        "process surrogates with uncertainty, neural networks trained by "
        "gradient descent, and surrogate models that replace expensive "
        "simulations. Hands-on Python and MATLAB, with plots and diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Regularisation: ridge and lasso",
            "12 min",
            r"""
# Regularisation: ridge and lasso

When features are many or correlated, ordinary least squares overfits and produces
huge, unstable coefficients. **Regularisation** adds a penalty on coefficient size.
**Ridge** ($L_2$) shrinks coefficients smoothly:

$$\min_{\boldsymbol{\theta}} \; \|\mathbf{y}-\mathbf{X}\boldsymbol{\theta}\|^2 + \lambda\|\boldsymbol{\theta}\|_2^2,$$

while **lasso** ($L_1$) drives some coefficients to exactly zero, performing
feature selection. The strength $\lambda$ trades fit against simplicity; as
$\lambda$ grows, validation error first improves then worsens:

```plot
{"title": "Validation error vs regularisation strength", "xLabel": "log10 lambda", "yLabel": "validation error", "xRange": [-3, 3], "yRange": [0, 4], "grid": true, "functions": [{"expr": "0.4*(x+0.5)^2 + 0.6", "label": "error vs log lambda", "color": "#dc2626"}]}
```

```python
from sklearn.linear_model import RidgeCV, LassoCV
import numpy as np

alphas = np.logspace(-3, 3, 50)
ridge = RidgeCV(alphas=alphas).fit(X_tr, y_tr)
lasso = LassoCV(alphas=alphas, max_iter=10000).fit(X_tr, y_tr)
print("ridge alpha:", ridge.alpha_, " lasso nonzeros:", (lasso.coef_ != 0).sum())
```

Pick $\lambda$ by cross-validation, never by eye on the training fit.

**Next:** building informative features and reducing dimensions.
""",
        ),
        _t(
            "Feature engineering and PCA",
            "12 min",
            r"""
# Feature engineering and PCA

Models are only as good as their inputs. **Feature engineering** crafts physically
meaningful inputs — dimensionless groups like Reynolds number $Re=\rho V L/\mu$,
ratios, logs of skewed quantities — and **standardises** them so no feature
dominates by scale alone.

When inputs are high-dimensional and correlated, **principal component analysis
(PCA)** finds an orthogonal basis ordered by variance. Keeping the top components
that capture, say, 95% of variance compresses the data with little loss. The
cumulative explained-variance curve saturates fast for correlated data:

```plot
{"title": "Cumulative variance explained vs components", "xLabel": "number of components", "yLabel": "cumulative variance", "xRange": [1, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1 - exp(-0.7*x)", "label": "cumulative variance", "color": "#16a34a"}]}
```

```python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

Xs = StandardScaler().fit_transform(X)
pca = PCA(n_components=0.95).fit(Xs)   # keep 95% of variance
Xr = pca.transform(Xs)
print("kept", pca.n_components_, "components")
```

PCA is mathematically the singular value decomposition (SVD) of the centred data —
the same tool we will reuse for reduced-order models.

**Next:** surrogates that also tell you their uncertainty.
""",
        ),
        _t(
            "Gaussian process surrogates",
            "13 min",
            r"""
# Gaussian process surrogates

A **Gaussian process (GP)** treats the unknown function as a distribution over
functions, defined by a mean and a covariance **kernel** $k(\mathbf{x},\mathbf{x}')$.
After conditioning on data it returns not just a prediction but a **variance** —
priceless in engineering, where you must know *how much to trust* a surrogate. A
common choice is the squared-exponential kernel

$$k(\mathbf{x},\mathbf{x}') = \sigma_f^2 \exp\!\left(-\frac{\|\mathbf{x}-\mathbf{x}'\|^2}{2\ell^2}\right).$$

Predictive uncertainty grows away from the training points; here the standard
deviation widens like a bell as you move from a sampled location:

```plot
{"title": "GP predictive uncertainty vs distance from data", "xLabel": "distance from nearest sample", "yLabel": "predictive std", "xRange": [0, 5], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "1 - exp(-0.6*x)", "label": "std grows with distance", "color": "#2563eb"}]}
```

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

kernel = C(1.0) * RBF(length_scale=1.0)
gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True).fit(X_tr, y_tr)
mean, std = gp.predict(X_te, return_std=True)   # mean AND uncertainty
```

GPs shine with small, expensive datasets and underpin Bayesian optimization.

**Next:** neural networks and gradient descent.
""",
        ),
        _t(
            "Neural networks and gradient descent",
            "13 min",
            r"""
# Neural networks and gradient descent

A **feedforward neural network** stacks affine maps and nonlinear activations:
$\mathbf{h} = \phi(\mathbf{W}\mathbf{x}+\mathbf{b})$, repeated across layers, to
approximate arbitrarily complex functions (the universal approximation theorem).
Parameters are learned by **gradient descent**: compute the loss gradient via
**backpropagation** and step downhill,

$$\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \eta\,\nabla_{\boldsymbol{\theta}} L.$$

The learning rate $\eta$ is critical: too large diverges, too small crawls. A
well-tuned run shows the loss decaying smoothly toward a floor:

```plot
{"title": "Training loss vs iteration", "xLabel": "iteration (x100)", "yLabel": "loss", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x) + 0.05", "label": "loss decay", "color": "#2563eb"}]}
```

```python
import torch, torch.nn as nn

net = nn.Sequential(nn.Linear(d, 32), nn.Tanh(), nn.Linear(32, 1))
opt = torch.optim.Adam(net.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()
for _ in range(2000):
    opt.zero_grad()
    loss = loss_fn(net(Xt), yt)
    loss.backward()        # backprop
    opt.step()
```

Use **tanh** or **ReLU** activations, **Adam** for optimisation, and watch the
validation loss for early stopping.

**Next:** using these models as surrogates for simulation.
""",
        ),
        _t(
            "Surrogate models for simulation",
            "12 min",
            r"""
# Surrogate models for simulation

A high-fidelity CFD or FEA run can take hours. A **surrogate** (metamodel) learns
the simulator's input-output map from a modest set of runs, then answers new
queries in milliseconds — enabling design exploration, optimization and
uncertainty quantification that would otherwise be infeasible. The recipe:
sample the design space well (e.g. **Latin hypercube sampling**), run the
expensive model at those points, fit a surrogate (polynomial, GP, or NN), and
validate.

```mermaid
flowchart LR
  D["Design of experiments (LHS)"] --> S["Run expensive simulator"]
  S --> F["Fit surrogate model"]
  F --> V{"Accurate enough?"}
  V -->|no| A["Add samples (adaptive)"]
  A --> S
  V -->|yes| U["Optimize / explore in ms"]
```

Surrogate accuracy improves as more training samples are added, with diminishing
returns:

```plot
{"title": "Surrogate error vs number of simulation samples", "xLabel": "samples", "yLabel": "relative error", "xRange": [5, 50], "yRange": [0, 0.5], "grid": true, "functions": [{"expr": "2/x", "label": "error ~ 1/n", "color": "#dc2626"}]}
```

```matlab
% Latin hypercube design + GP surrogate (MATLAB)
X = lhsdesign(30, 3);                 % 30 samples in 3D unit cube
Y = arrayfun(@(i) expensive_sim(X(i,:)), 1:30)';
gpr = fitrgp(X, Y, 'KernelFunction', 'ardsquaredexponential');
yhat = predict(gpr, Xnew);            % instant evaluation
```

**Next:** check your understanding of intermediate methods.
""",
        ),
        _quiz(),
    ),
)


# ── Machine Learning for Engineering & Simulation — Advanced ──────────────────

_ADVANCED = SeedCourse(
    slug="ml-for-engineering-advanced",
    title="Machine Learning for Engineering & Simulation — Advanced",
    description=(
        "State-of-the-art data-driven simulation: reduced-order models via POD, "
        "physics-informed neural networks that embed PDE residuals in the loss, "
        "neural-operator surrogates that learn solution maps, Bayesian "
        "optimization for design, and ML-accelerated solvers. Research-grade "
        "Python (PyTorch) and MATLAB, with plots and architecture diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Reduced-order models with POD",
            "13 min",
            r"""
# Reduced-order models with POD

Full simulations live in spaces of millions of degrees of freedom, yet the
solution often evolves on a low-dimensional manifold. **Proper orthogonal
decomposition (POD)** — the SVD applied to a matrix of solution **snapshots** —
extracts an optimal orthonormal basis $\{\boldsymbol{\phi}_k\}$ that captures the
most energy in the fewest modes:

$$\mathbf{u}(t) \approx \sum_{k=1}^{r} a_k(t)\,\boldsymbol{\phi}_k, \qquad r \ll N.$$

The singular values decay fast for many engineering flows, so a handful of modes
hold almost all the energy:

```plot
{"title": "POD singular-value (energy) decay", "xLabel": "mode index", "yLabel": "normalised singular value", "xRange": [1, 20], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "sigma_k ~ exp(-0.5 k)", "color": "#16a34a"}]}
```

Projecting the governing equations onto this basis (Galerkin projection) yields a
tiny ODE system — a **reduced-order model (ROM)** that runs orders of magnitude
faster.

```python
import numpy as np
# snapshots: columns are solution states at sampled times
U, S, Vt = np.linalg.svd(snapshots, full_matrices=False)
energy = np.cumsum(S**2) / np.sum(S**2)
r = np.searchsorted(energy, 0.999) + 1     # modes for 99.9% energy
Phi = U[:, :r]                             # POD basis
a = Phi.T @ snapshots                       # reduced coordinates
```

**Next:** baking physics into neural networks (PINNs).
""",
        ),
        _t(
            "Physics-informed neural networks",
            "14 min",
            r"""
# Physics-informed neural networks

A **physics-informed neural network (PINN)** represents the solution
$u(\mathbf{x},t)$ as a neural network and trains it so that the **PDE residual**
is driven to zero — derivatives come for free from automatic differentiation. For
a PDE $\mathcal{N}[u]=0$, the loss combines data, boundary/initial conditions, and
the residual at collocation points:

$$L = L_{\text{data}} + L_{\text{BC}} + \lambda\,\frac{1}{M}\sum_{j=1}^{M}\bigl|\mathcal{N}[u_\theta](\mathbf{x}_j,t_j)\bigr|^2.$$

This lets PINNs solve forward and inverse problems with little or no labelled data,
and naturally handles irregular domains. The combined residual loss decays during
training:

```plot
{"title": "PINN residual loss vs epoch", "xLabel": "epoch (x1000)", "yLabel": "residual loss", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.45*x) + 0.02", "label": "PDE residual loss", "color": "#dc2626"}]}
```

```python
import torch
def pde_residual(net, x, t):
    x.requires_grad_(True); t.requires_grad_(True)
    u = net(torch.cat([x, t], 1))
    u_t = torch.autograd.grad(u, t, torch.ones_like(u), create_graph=True)[0]
    u_x = torch.autograd.grad(u, x, torch.ones_like(u), create_graph=True)[0]
    u_xx = torch.autograd.grad(u_x, x, torch.ones_like(u_x), create_graph=True)[0]
    return u_t - nu * u_xx          # heat/diffusion residual = 0
```

```mermaid
flowchart LR
  N["Neural net u_theta(x,t)"] --> AD["Autodiff: u_t, u_x, u_xx"]
  AD --> R["PDE residual N[u]"]
  R --> L["Loss = data + BC + residual"]
  L --> O["Optimise theta"]
  O --> N
```

**Next:** learning the solution operator itself.
""",
        ),
        _t(
            "Neural operators and solution maps",
            "13 min",
            r"""
# Neural operators and solution maps

A PINN solves one problem instance. A **neural operator** learns the *mapping
between function spaces* — e.g. from a coefficient field or boundary condition to
the full solution field — so a trained model generalises across many instances in
a single forward pass. The **Fourier Neural Operator (FNO)** parameterises a
global convolution in the spectral domain, making it discretisation-invariant and
remarkably efficient on parametric PDEs.

```mermaid
flowchart LR
  A["Input function a(x): e.g. permeability"] --> P["Lift to channels"]
  P --> FL["Fourier layers: FFT - linear - iFFT + local conv"]
  FL --> Q["Project"]
  Q --> U["Output function u(x): solution field"]
```

Once trained, a neural operator evaluates a new case far faster than a solver, and
test error falls as the training set of solved instances grows:

```plot
{"title": "Neural-operator test error vs training instances", "xLabel": "training PDE instances (x100)", "yLabel": "relative L2 error", "xRange": [1, 20], "yRange": [0, 0.3], "grid": true, "functions": [{"expr": "0.4/sqrt(x)", "label": "error ~ 1/sqrt(N)", "color": "#dc2626"}]}
```

```python
import torch.nn as nn
class SpectralConv1d(nn.Module):
    def __init__(self, cin, cout, modes):
        super().__init__()
        self.modes = modes
        self.w = nn.Parameter(torch.randn(cin, cout, modes, dtype=torch.cfloat))
    def forward(self, x):
        xf = torch.fft.rfft(x)                       # to spectral domain
        out = torch.zeros_like(xf)
        out[..., :self.modes] = torch.einsum(
            "bix,iox->box", xf[..., :self.modes], self.w)
        return torch.fft.irfft(out, n=x.size(-1))    # back to physical
```

**Next:** optimising designs with a budget — Bayesian optimization.
""",
        ),
        _t(
            "Bayesian optimization for design",
            "13 min",
            r"""
# Bayesian optimization for design

When each design evaluation is expensive (a wind-tunnel test, a full CFD run),
brute-force search is hopeless. **Bayesian optimization (BO)** builds a GP
surrogate of the objective and uses an **acquisition function** to pick the next
point that best balances **exploration** (high uncertainty) and **exploitation**
(good predicted value). A popular choice is **Expected Improvement (EI)**:

$$\text{EI}(\mathbf{x}) = \mathbb{E}\bigl[\max(0,\; f_{\text{best}} - f(\mathbf{x}))\bigr].$$

BO typically finds near-optimal designs in tens of evaluations, where grid search
needs thousands. Best-found value improves rapidly then plateaus:

```plot
{"title": "Best objective found vs evaluations", "xLabel": "evaluations", "yLabel": "best objective (minimise)", "xRange": [1, 30], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.2*x)", "label": "convergence", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  S["Initial samples"] --> G["Fit GP surrogate"]
  G --> A["Maximise acquisition (EI)"]
  A --> E["Evaluate expensive objective"]
  E --> G
  G --> R["Return best design"]
```

```python
from skopt import gp_minimize
res = gp_minimize(expensive_objective, dimensions=bounds,
                  acq_func="EI", n_calls=30, random_state=0)
print("best design:", res.x, " value:", res.fun)
```

**Next:** ML-accelerated solvers and hybrid pipelines.
""",
        ),
        _t(
            "ML-accelerated solvers and hybrid models",
            "13 min",
            r"""
# ML-accelerated solvers and hybrid models

The frontier is **hybrid** modelling: keep a trusted numerical solver but let ML
do the expensive or uncertain parts. Examples include learned **closure models**
for turbulence (replacing RANS/LES sub-grid terms), ML **preconditioners** that
accelerate linear solves, learned **time-steppers** that take larger stable steps,
and **multi-fidelity** schemes that fuse cheap low-fidelity runs with a few
high-fidelity ones.

```mermaid
flowchart LR
  LF["Low-fidelity model (cheap)"] --> MF["Multi-fidelity fusion"]
  HF["High-fidelity runs (few)"] --> MF
  MF --> C["Corrected prediction"]
  S["Numerical solver"] --> ML["Learned closure / step"]
  ML --> S
```

A learned time-stepper can take a coarser step at fixed accuracy, cutting wall-clock
cost; error grows with step size but far slower than an unaided scheme:

```plot
{"title": "Solver error vs time-step size", "xLabel": "time step dt", "yLabel": "global error", "xRange": [0, 2], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.25*x^2", "label": "learned stepper error ~ dt^2", "color": "#dc2626"}]}
```

```python
# Multi-fidelity correction: y_hf ~ rho * y_lf + delta(x)
import numpy as np
rho = np.linalg.lstsq(y_lf[:, None], y_hf, rcond=None)[0][0]
delta = GaussianProcessRegressor().fit(X, y_hf - rho * y_lf)  # learn discrepancy
y_pred = rho * y_lf_new + delta.predict(X_new)
```

Always **validate hybrid models against held-out high-fidelity data** and respect
known conservation laws — ML speed must never cost physical correctness.

**Next:** check your understanding of advanced methods.
""",
        ),
        _quiz(),
    ),
)


ML_FOR_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["ML_FOR_ENGINEERING_COURSES"]
