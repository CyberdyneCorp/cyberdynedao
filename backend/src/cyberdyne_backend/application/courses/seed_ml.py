"""Academy seed content — the AI / Machine Learning track.

Four courses, Beginner → Advanced plus a dedicated Transformers/LLMs course:

* ``ml-basics``        — what ML is, regression, gradient descent, classification
* ``ml-intermediate``  — core algorithms + a neural net & backprop from scratch
* ``ml-advanced``      — deep learning, PyTorch & TensorFlow, CNNs/RNNs
* ``transformers``     — attention, the Transformer architecture, GPT/LLMs

Authoring notes (kept in sync with the platform):
- Lesson bodies are raw triple-quoted Markdown so LaTeX (``$...$`` / ``$$...$$``)
  reads naturally. Interactive ```plot blocks hold JSON (see ``lessonPlot.ts``).
- ``code`` lessons run in the Python sandbox, which has numpy/scipy/sklearn/
  pandas/matplotlib but NOT torch/tensorflow, and runs under RestrictedPython
  (no leading-underscore names, no dunder attributes, plain ``import``). So
  hands-on code is NumPy/sklearn; PyTorch & TensorFlow are shown as read-only
  fenced ```python in ``text`` lessons.
"""
# Lesson content legitimately uses math Unicode (σ, ω, ², ·, →) in strings,
# comments and labels — same convention as the other content modules.
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
# 1. ml-basics — Machine Learning: Basics (Beginner)
# ──────────────────────────────────────────────────────────────────────

_ML_BASICS = SeedCourse(
    slug="ml-basics",
    title="Machine Learning — Basics",
    description=(
        "Start here. What machine learning actually is, the supervised vs "
        "unsupervised split, and the two ideas everything else is built on: a "
        "cost function and gradient descent. You'll fit a line by hand in NumPy, "
        "watch gradient descent roll downhill, and train your first classifier."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is machine learning?",
            "10 min",
            r"""# What is machine learning?

Traditional programming: you write **rules** and the computer applies them.
Machine learning flips this — you give the computer **examples** and it learns
the rule that fits them. Formally, we look for a function $f$ that maps inputs
$x$ to outputs $y$ so that $f(x)\approx y$ on data we've never seen.

## Three families

- **Supervised learning** — learn from *labelled* examples $(x, y)$. Predict a
  number (**regression**) or a category (**classification**). This is most of
  applied ML.
- **Unsupervised learning** — only inputs $x$, no labels. Find structure:
  clusters, lower-dimensional representations, anomalies.
- **Reinforcement learning** — an agent takes actions in an environment and
  learns from a **reward** signal (games, robotics, control).

## The workflow

1. **Data** → collect and clean examples.
2. **Split** → hold out a *test set* the model never trains on, so you can
   measure how it does on unseen data.
3. **Model** → pick a family of functions (a line, a tree, a neural net).
4. **Train** → tune the model's parameters to fit the training data.
5. **Evaluate** → measure error on the test set; iterate.

The golden rule: **the score that matters is on data the model has not seen.**
A model that memorises its training data but fails on new data has learned
nothing useful — we'll make that precise when we reach *overfitting*.
""",
        ),
        _t(
            "Regression vs classification",
            "9 min",
            r"""# Regression vs classification

Both are supervised — the difference is the **output**.

- **Regression** predicts a continuous number: house price, temperature,
  tomorrow's demand.
- **Classification** predicts a discrete label: spam / not-spam, which digit,
  which species.

The simplest model of all is a **straight line**, $\hat{y} = w x + b$, with a
**slope** $w$ and an **intercept** $b$. "Learning" here means choosing $w$ and
$b$ so the line passes as close as possible to the data. Drag the sliders and
try to fit the cloud of points by eye:

```plot
{"title": "Fit a line: ŷ = w·x + b", "xLabel": "x", "yLabel": "y", "xRange": [0, 10], "yRange": [0, 12], "controls": [{"name": "w", "range": [-1, 3], "value": 0.5, "label": "slope w"}, {"name": "b", "range": [-2, 6], "value": 1, "label": "intercept b"}], "functions": [{"expr": "w*x + b", "label": "ŷ = w·x + b", "color": "#2563eb"}], "points": [{"x": 1, "y": 2.1, "color": "#dc2626"}, {"x": 3, "y": 3.9, "color": "#dc2626"}, {"x": 5, "y": 6.2, "color": "#dc2626"}, {"x": 7, "y": 7.8, "color": "#dc2626"}, {"x": 9, "y": 10.1, "color": "#dc2626"}]}
```

Doing this by eye is fine for one line. With thousands of parameters we need a
way to **measure** how wrong a fit is, and an automatic way to improve it.
That's the next two lessons: the **cost function** and **gradient descent**.
""",
        ),
        _t(
            "The cost function (MSE)",
            "10 min",
            r"""# The cost function

To let a computer "fit" automatically, we need a single number that says how
bad the current parameters are. For regression the standard choice is
**Mean Squared Error**: average the squared gap between prediction and truth.

$$ J(w, b) = \frac{1}{n}\sum_{i=1}^{n}\bigl(\hat{y}_i - y_i\bigr)^2,\qquad \hat{y}_i = w x_i + b. $$

Squaring does two things: it makes every error positive (over- and
under-shooting both cost), and it punishes big misses much more than small
ones. Lower $J$ = better fit; **training = minimising $J$**.

Fix $b$ and vary a single weight $w$: the cost traces a **parabola** with one
lowest point — the best $w$. Slide $w$ and watch the cost (red dot) move:

```plot
{"title": "Cost J(w) is a bowl — find the bottom", "xLabel": "weight w", "yLabel": "cost J", "xRange": [-1, 5], "yRange": [0, 10], "controls": [{"name": "w", "range": [-1, 5], "value": 0, "label": "weight w"}], "functions": [{"expr": "(x - 2)^2 + 0.5", "label": "J(w)", "color": "#2563eb"}], "points": [{"xExpr": "w", "yExpr": "(w - 2)^2 + 0.5", "label": "current cost", "color": "#dc2626", "size": 7}]}
```

The minimum here is at $w = 2$. With one parameter you could just scan values.
With millions you can't — you need a method that *walks downhill* using only
the local slope. Enter gradient descent.
""",
        ),
        _code(
            "Fit a line in NumPy",
            "12 min",
            r"""# Linear regression in NumPy — compute the cost, then solve it exactly.
# Press Run. Then change the data or the guess and run again.
import numpy as np

# Five (x, y) points that roughly follow y = 1.2 x + 0.8
x = np.array([1.0, 3.0, 5.0, 7.0, 9.0])
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1])

# Mean squared error = mean((w*x + b - y)^2), computed inline for two guesses:
w, b = 0.5, 1.0
print("MSE at (w=0.5, b=1.0):", round(float(np.mean((w * x + b - y) ** 2)), 4))

w, b = 1.2, 0.8
print("MSE at (w=1.2, b=0.8):", round(float(np.mean((w * x + b - y) ** 2)), 4))

# The exact least-squares solution via the normal equation:
#   X = [x, 1],  theta = (X^T X)^-1 X^T y
X = np.column_stack([x, np.ones_like(x)])
theta = np.linalg.solve(X.T.dot(X), X.T.dot(y))
w_best, b_best = float(theta[0]), float(theta[1])
print("best fit: w =", round(w_best, 4), " b =", round(b_best, 4))
print("best MSE:", round(float(np.mean((w_best * x + b_best - y) ** 2)), 4))

# Try it: predict y at x = 11
print("prediction at x=11:", round(w_best * 11 + b_best, 2))
""",
        ),
        _t(
            "Gradient descent",
            "11 min",
            r"""# Gradient descent

The **gradient** is the slope of the cost surface — it points *uphill*. To
reduce cost we step in the **opposite** direction. For one weight:

$$ w \leftarrow w - \eta\,\frac{\partial J}{\partial w}. $$

$\eta$ (eta) is the **learning rate** — the step size. The derivative of our
parabola $J(w)=(w-2)^2$ is $J'(w)=2(w-2)$: positive to the right of the
minimum (step left), negative to the left (step right). Either way you roll
toward the bottom, taking smaller steps as the slope flattens. Watch the ball
descend:

```plot
{"title": "Gradient descent rolls downhill", "xLabel": "weight w", "yLabel": "cost J", "xRange": [-1, 5], "yRange": [0, 10], "animate": {"param": "t", "range": [0, 1], "label": "step"}, "functions": [{"expr": "(x - 2)^2 + 0.5", "label": "J(w)", "color": "#2563eb"}], "points": [{"xExpr": "2 - 2*exp(-3.5*t)", "yExpr": "4*exp(-7*t) + 0.5", "label": "w", "color": "#dc2626", "size": 8, "trail": true}]}
```

**Learning rate matters.** Too small → painfully slow. Too large → you
overshoot and can bounce or diverge. In higher dimensions the same rule
applies to every parameter at once: compute the gradient vector, step against
it, repeat. It scales to billions of parameters, which is why it powers all of
deep learning.
""",
        ),
        _code(
            "Gradient descent from scratch",
            "13 min",
            r"""# Fit y = w x + b by gradient descent — no solver, just the update rule.
import numpy as np

x = np.array([1.0, 3.0, 5.0, 7.0, 9.0])
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1])
n = len(x)

w, b = 0.0, 0.0      # start at zero
lr = 0.01            # learning rate (try 0.001 and 0.03 too)

for step in range(2001):
    y_hat = w * x + b
    err = y_hat - y
    # Gradients of MSE = mean(err^2):
    grad_w = (2.0 / n) * np.sum(err * x)
    grad_b = (2.0 / n) * np.sum(err)
    w = w - lr * grad_w
    b = b - lr * grad_b
    if step % 500 == 0:
        cost = np.mean(err * err)
        print("step", step, " w=", round(w, 3), " b=", round(b, 3), " cost=", round(cost, 4))

print("learned: y =", round(w, 3), "* x +", round(b, 3))
# Compare to the exact solution from the previous code lesson — they should match.
""",
        ),
        _t(
            "Classification & the sigmoid",
            "9 min",
            r"""# Classification & the sigmoid

For a yes/no question we want a probability in $[0, 1]$, not an unbounded line.
**Logistic regression** runs the linear score $z = w x + b$ through the
**sigmoid**:

$$ \sigma(z) = \frac{1}{1 + e^{-z}}. $$

It squashes any real number into $(0, 1)$: large positive $z\to 1$, large
negative $z\to 0$, and $\sigma(0)=0.5$ — the decision boundary. Slide $w$ to
see how the steepness (confidence) changes:

```plot
{"title": "The sigmoid: σ(w·x) maps scores to probabilities", "xLabel": "x", "yLabel": "P(class = 1)", "xRange": [-8, 8], "yRange": [-0.1, 1.1], "controls": [{"name": "w", "range": [0.2, 3], "value": 1, "label": "weight w"}], "functions": [{"expr": "1/(1 + exp(-w*x))", "label": "σ(w·x)", "color": "#2563eb"}, {"expr": "0.5", "label": "decision = 0.5", "color": "#9ca3af"}]}
```

We predict class 1 when $\sigma(z) > 0.5$ (i.e. $z>0$). Instead of MSE,
classification trains with **cross-entropy** (log loss), which heavily
penalises confident wrong answers — more on that in the Advanced course. The
optimiser is the same gradient descent you just wrote.
""",
        ),
        _code(
            "Train a classifier (scikit-learn)",
            "12 min",
            r"""# Your first real classifier: logistic regression on the Iris dataset.
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

data = load_iris()
X = data.data          # 150 flowers x 4 measurements
y = data.target        # species: 0, 1, 2
print("dataset:", X.shape[0], "samples,", X.shape[1], "features,", len(set(y)), "classes")

# Hold out 30% as a test set the model never sees during training.
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0
)

model = LogisticRegression(max_iter=500)
model.fit(x_train, y_train)

train_acc = model.score(x_train, y_train)
test_acc = model.score(x_test, y_test)
print("train accuracy:", round(train_acc, 3))
print("test  accuracy:", round(test_acc, 3))

# Predict the first 5 test flowers vs the truth:
pred = model.predict(x_test[:5])
print("predicted:", list(pred))
print("actual:   ", list(y_test[:5]))
""",
        ),
        _t(
            "Overfitting & generalisation",
            "10 min",
            r"""# Overfitting & generalisation

A model that nails the training data but flops on new data has **overfit** —
it memorised noise instead of learning the pattern. The opposite,
**underfitting**, is too simple to capture the trend at all. We want the
sweet spot in between.

The tell-tale picture: as model complexity grows, **training error** keeps
falling, but **validation error** (on held-out data) falls, bottoms out, then
rises. The gap between the two curves is overfitting:

```plot
{"title": "Training vs validation error", "xLabel": "model complexity", "yLabel": "error", "xRange": [0, 8], "yRange": [0, 1.2], "functions": [{"expr": "exp(-0.5*x) + 0.05", "label": "training error", "color": "#16a34a"}, {"expr": "exp(-0.5*x) + 0.05 + 0.03*(x - 3)^2", "label": "validation error", "color": "#dc2626"}]}
```

**How we control it**

- **Train/validation/test split** — tune on validation, report on test (used
  exactly once).
- **More data** — the most reliable cure.
- **Regularisation** — penalise large weights so the model stays simple.
- **Early stopping** — stop training when validation error starts rising.
- **Cross-validation** — average over several splits for a stabler estimate.

Keep this mantra: *we don't care about training accuracy; we care about
performance on data the model has never seen.*
""",
        ),
        quiz_lesson(
            "Quiz: Machine Learning Basics",
            (
                q(
                    "What distinguishes supervised from unsupervised learning?",
                    (
                        opt(
                            "Supervised learns from labelled (x, y) examples; unsupervised has only inputs x",
                            correct=True,
                        ),
                        opt(
                            "Supervised is always classification; unsupervised is always regression"
                        ),
                        opt("Supervised needs a GPU; unsupervised does not"),
                        opt("There is no real difference"),
                    ),
                    "Supervised learning fits a mapping from inputs to known labels; unsupervised finds structure with no labels.",
                ),
                q(
                    "Why do we square the errors in Mean Squared Error?",
                    (
                        opt(
                            "To make every error positive and penalise large misses more",
                            correct=True,
                        ),
                        opt("To make the cost negative"),
                        opt("Because squaring is faster to compute than absolute value"),
                        opt("To turn regression into classification"),
                    ),
                    "Squaring removes sign and grows quadratically, so big errors dominate the cost.",
                ),
                q(
                    "In the update w ← w − η·(∂J/∂w), what is η?",
                    (
                        opt("The learning rate — the size of each downhill step", correct=True),
                        opt("The number of training examples"),
                        opt("The final value of the weight"),
                        opt("The model's accuracy"),
                    ),
                    "η (eta) scales the step. Too small is slow; too large can overshoot or diverge.",
                ),
                q(
                    "What does the sigmoid σ(z) = 1/(1+e^−z) give you?",
                    (
                        opt("A value in (0, 1) usable as a probability", correct=True),
                        opt("A value in (−1, 1)"),
                        opt("An unbounded real number"),
                        opt("Always exactly 0 or 1"),
                    ),
                    "The sigmoid squashes any real score into (0, 1), with σ(0) = 0.5 as the decision boundary.",
                ),
                q(
                    "Training error is near zero but test error is high. What's happening?",
                    (
                        opt(
                            "Overfitting — the model memorised the training data, including noise",
                            correct=True,
                        ),
                        opt("Underfitting — the model is too simple"),
                        opt("The learning rate is too small"),
                        opt("The data has too many features removed"),
                    ),
                    "A large train/test gap is the signature of overfitting; regularisation, more data, or early stopping help.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# 2. ml-intermediate — core algorithms + neural net from scratch
# ──────────────────────────────────────────────────────────────────────

_ML_INTERMEDIATE = SeedCourse(
    slug="ml-intermediate",
    title="Machine Learning — Intermediate",
    description=(
        "The working ML toolkit: feature scaling, trees and forests, clustering, "
        "PCA, and evaluation done right. Then the heart of the course — you build "
        "a two-layer neural network and implement backpropagation from scratch in "
        "NumPy, training it to solve XOR."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Features & normalisation",
            "9 min",
            r"""# Features & normalisation

Models learn from **features** — the numeric columns you feed them. Two habits
make or break a project:

**Scale your features.** If one feature ranges 0–1 and another 0–100000,
distance- and gradient-based methods are dominated by the large one.
Standardise each feature to zero mean and unit variance:

$$ x' = \frac{x - \mu}{\sigma}. $$

**Encode categories.** Turn "red/green/blue" into numbers a model can use —
usually **one-hot** columns, not a single 1/2/3 (which would imply a false
ordering).

**Never leak the test set.** Compute $\mu$ and $\sigma$ on the *training* data
only, then apply them to validation and test. Fitting the scaler on all the
data lets information about the test set sneak into training — a subtle but
common bug that inflates your scores.

Good features beat fancy models more often than people expect. Time spent on
clean, well-scaled, well-encoded inputs pays off everywhere downstream.
""",
        ),
        _t(
            "Decision trees & random forests",
            "10 min",
            r"""# Decision trees & random forests

A **decision tree** asks a sequence of yes/no questions about the features
("petal length > 2.5?") and reads off a prediction at the leaf. It carves the
feature space into axis-aligned boxes:

```plot
{"title": "A tree splits the plane into boxes", "xLabel": "feature 1", "yLabel": "feature 2", "xRange": [0, 10], "yRange": [0, 10], "functions": [{"expr": "5", "label": "split: f2 = 5", "color": "#16a34a"}], "points": [{"x": 2, "y": 7, "color": "#2563eb", "label": "A"}, {"x": 3, "y": 8, "color": "#2563eb"}, {"x": 7, "y": 2, "color": "#dc2626", "label": "B"}, {"x": 8, "y": 3, "color": "#dc2626"}]}
```

A single deep tree overfits badly — it can grow a leaf for every point. The
fix is a **random forest**: train many trees, each on a random subset of rows
and features, and **average** their votes. Decorrelating the trees and
averaging slashes variance, giving a robust model that needs little tuning.
This *ensembling* idea (also: gradient-boosted trees) wins a huge share of
real-world tabular problems.
""",
        ),
        _code(
            "Train & evaluate a random forest",
            "12 min",
            r"""# A random forest on Iris, with a proper train/test split and metrics.
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

data = load_iris()
x_train, x_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.3, random_state=0
)

forest = RandomForestClassifier(n_estimators=100, random_state=0)
forest.fit(x_train, y_train)

pred = forest.predict(x_test)
print("test accuracy:", round(accuracy_score(y_test, pred), 3))
print("confusion matrix (rows = true, cols = predicted):")
print(confusion_matrix(y_test, pred))

# Which measurements mattered most?
names = data.feature_names
for name, score in sorted(zip(names, forest.feature_importances_), key=lambda p: -p[1]):
    print(round(score, 3), name)
""",
        ),
        _t(
            "Clustering: k-NN & k-means",
            "10 min",
            r"""# Clustering: k-NN & k-means

**k-Nearest Neighbours (k-NN)** is the laziest classifier: to label a new
point, look at its $k$ closest training points and take the majority vote.
There's no "training" — just storing the data and measuring distances.

**k-means** is the classic *unsupervised* method: split unlabelled data into
$k$ groups. It alternates two steps until stable:

1. **Assign** each point to the nearest cluster centre.
2. **Update** each centre to the mean of its assigned points.

```plot
{"title": "k-means: points snap to the nearest centre", "xLabel": "x", "yLabel": "y", "xRange": [0, 10], "yRange": [0, 10], "points": [{"x": 1.5, "y": 2, "color": "#2563eb"}, {"x": 2, "y": 1.5, "color": "#2563eb"}, {"x": 1, "y": 2.5, "color": "#2563eb"}, {"x": 8, "y": 8, "color": "#dc2626"}, {"x": 8.5, "y": 7.5, "color": "#dc2626"}, {"x": 7.5, "y": 8.5, "color": "#dc2626"}, {"x": 1.5, "y": 2, "color": "#1e3a8a", "size": 9, "label": "centre 1"}, {"x": 8, "y": 8, "color": "#7f1d1d", "size": 9, "label": "centre 2"}]}
```

Both rely on a notion of **distance**, so feature scaling (last-but-one lesson)
is essential — otherwise one large-range feature dictates every neighbour.
Pick $k$ with the "elbow" of the within-cluster error, or with domain
knowledge.
""",
        ),
        _code(
            "k-means from scratch",
            "13 min",
            r"""# k-means in plain NumPy: assign, update, repeat.
import numpy as np

np.random.seed(0)
# Two blobs of points:
blob_a = np.random.randn(30, 2) * 0.6 + np.array([2.0, 2.0])
blob_b = np.random.randn(30, 2) * 0.6 + np.array([7.0, 7.0])
points = np.vstack([blob_a, blob_b])

# Start with two random centres.
centres = points[np.random.choice(len(points), 2, replace=False)].copy()

for iteration in range(10):
    # Assign: distance from each point to each centre.
    d0 = np.sum((points - centres[0]) ** 2, axis=1)
    d1 = np.sum((points - centres[1]) ** 2, axis=1)
    labels = (d1 < d0).astype(int)   # 0 or 1
    # Update: move each centre to the mean of its members.
    new0 = points[labels == 0].mean(axis=0)
    new1 = points[labels == 1].mean(axis=0)
    centres = np.vstack([new0, new1])

print("final centres (should be near [2,2] and [7,7]):")
print(np.round(centres, 2))
print("cluster sizes:", int(np.sum(labels == 0)), int(np.sum(labels == 1)))
""",
        ),
        _t(
            "PCA & dimensionality reduction",
            "9 min",
            r"""# PCA & dimensionality reduction

High-dimensional data is hard to visualise and can drown models in noise.
**Principal Component Analysis (PCA)** finds new axes — *principal components*
— ordered by how much variance they capture, then keeps the first few. It's a
**rotation** of the data onto its most informative directions.

Geometrically: the first component is the line along which the data spreads the
most; the second is the next-best direction perpendicular to it, and so on.

$$ \text{maximise}\ \operatorname{Var}(Xv)\ \text{subject to}\ \lVert v\rVert = 1. $$

The solution comes from the **eigenvectors of the covariance matrix** (or an
SVD of the centred data). Project onto the top 2 components and you can plot
100-dimensional data on a screen, often revealing clusters that were invisible
before. PCA is also a denoiser and a speed-up: fewer features, less
overfitting, faster training — at the cost of some interpretability, since each
component mixes the originals.
""",
        ),
        _t(
            "Neural networks & activations",
            "11 min",
            r"""# Neural networks & activations

A **neuron** computes a weighted sum of its inputs plus a bias, then applies a
non-linear **activation**: $a = g(w\cdot x + b)$. Stack neurons into **layers**
and layers into a **network**, and you can approximate astonishingly complex
functions.

The activation is what makes it powerful — without a non-linearity, stacking
layers just gives another linear map. The three classics:

```plot
{"title": "Activation functions", "xLabel": "z", "yLabel": "g(z)", "xRange": [-5, 5], "yRange": [-1.2, 2], "functions": [{"expr": "1/(1 + exp(-z))", "label": "sigmoid", "color": "#2563eb"}, {"expr": "tanh(z)", "label": "tanh", "color": "#16a34a"}, {"expr": "if(z > 0, z, 0)", "label": "ReLU", "color": "#dc2626"}]}
```

- **Sigmoid** → $(0,1)$, smooth, but saturates and kills gradients at the ends.
- **tanh** → $(-1,1)$, zero-centred, still saturates.
- **ReLU** = $\max(0, z)$ → cheap, doesn't saturate for $z>0$; the default for
  hidden layers in modern deep nets.

A network with one hidden layer of enough neurons is already a *universal
approximator*. The open question: given a target, how do we find the millions
of weights? That's **backpropagation**, next.
""",
        ),
        _t(
            "Backpropagation",
            "13 min",
            r"""# Backpropagation

Backprop is just the **chain rule** applied efficiently to a network. Two
passes:

**Forward** — push inputs through to a prediction and a loss. For a 2-layer net
with hidden activation $g$ and a squared-error loss:

$$ z_1 = W_1 x + b_1,\quad a_1 = g(z_1),\quad \hat{y} = W_2 a_1 + b_2,\quad L = \tfrac{1}{2}(\hat{y}-y)^2. $$

**Backward** — propagate the error from the loss back to every parameter,
multiplying local derivatives along the way:

$$ \frac{\partial L}{\partial \hat{y}} = \hat{y} - y, \qquad \frac{\partial L}{\partial W_2} = \frac{\partial L}{\partial \hat{y}}\,a_1^{\top}, $$

$$ \delta_1 = \Bigl(W_2^{\top}\tfrac{\partial L}{\partial \hat{y}}\Bigr)\odot g'(z_1), \qquad \frac{\partial L}{\partial W_1} = \delta_1\,x^{\top}. $$

The key trick: reuse the downstream gradient ($\delta$) instead of recomputing
it for every weight. That makes the cost of all gradients about the same as one
forward pass — which is why training huge networks is feasible at all.

Each gradient then feeds the same update you already know:
$W \leftarrow W - \eta\,\partial L/\partial W$. In the next lesson you'll code
this end-to-end and watch a network *learn XOR* — a problem no single linear
model can solve.
""",
        ),
        _code(
            "A neural net + backprop from scratch",
            "16 min",
            r"""# A 2-layer neural network in pure NumPy, trained on XOR by backprop.
# XOR is NOT linearly separable — a hidden layer is essential.
import numpy as np

np.random.seed(1)

# XOR: inputs and targets
X = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
y = np.array([[0.0], [1.0], [1.0], [0.0]])

# Weights: 2 inputs -> 4 hidden -> 1 output
W1 = np.random.randn(2, 4)
b1 = np.zeros((1, 4))
W2 = np.random.randn(4, 1)
b2 = np.zeros((1, 1))
lr = 0.5

for epoch in range(4001):
    # ---- forward (sigmoid σ(z) = 1/(1+e^-z), inlined) ----
    z1 = X.dot(W1) + b1
    a1 = 1.0 / (1.0 + np.exp(-z1))
    y_hat = 1.0 / (1.0 + np.exp(-(a1.dot(W2) + b2)))

    # ---- backward (chain rule) ----
    d_out = (y_hat - y) * y_hat * (1.0 - y_hat)      # dL/dz_out
    dW2 = a1.T.dot(d_out)
    db2 = np.sum(d_out, axis=0, keepdims=True)
    d_hid = d_out.dot(W2.T) * a1 * (1.0 - a1)         # backprop into hidden
    dW1 = X.T.dot(d_hid)
    db1 = np.sum(d_hid, axis=0, keepdims=True)

    # ---- gradient-descent update ----
    W2 = W2 - lr * dW2
    b2 = b2 - lr * db2
    W1 = W1 - lr * dW1
    b1 = b1 - lr * db1

    if epoch % 1000 == 0:
        loss = np.mean((y_hat - y) ** 2)
        print("epoch", epoch, " loss", round(float(loss), 4))

print("predictions (want 0,1,1,0):")
print(np.round(y_hat.ravel(), 3))
""",
        ),
        _t(
            "Evaluating classifiers",
            "10 min",
            r"""# Evaluating classifiers

Accuracy alone lies. On a dataset that's 99% "negative", a model that always
says "negative" scores 99% — and is useless. Use the **confusion matrix** and
the metrics built on it:

- **Precision** = of the items flagged positive, how many really are?
  $\tfrac{TP}{TP+FP}$ — punishes false alarms.
- **Recall** = of the real positives, how many did we catch?
  $\tfrac{TP}{TP+FN}$ — punishes misses.
- **F1** = harmonic mean of precision and recall — one number when you need a
  balance.

There's a **trade-off**: lowering the decision threshold catches more
positives (recall ↑) but raises false alarms (precision ↓). The **ROC curve**
sweeps the threshold and plots true-positive vs false-positive rate; **AUC**
(area under it) summarises ranking quality — 0.5 is random, 1.0 is perfect.

```plot
{"title": "ROC curve: a good model bows toward the top-left", "xLabel": "false positive rate", "yLabel": "true positive rate", "xRange": [0, 1], "yRange": [0, 1], "functions": [{"expr": "x", "label": "random (AUC 0.5)", "color": "#9ca3af"}, {"expr": "x^(0.3)", "label": "good model", "color": "#2563eb"}]}
```

Choose the metric that matches the cost of mistakes: in cancer screening a
missed positive (recall) is far worse than a false alarm; in spam filtering the
reverse.
""",
        ),
        quiz_lesson(
            "Quiz: Core ML & Neural Networks",
            (
                q(
                    "Why must a scaler's mean and std be computed on the training set only?",
                    (
                        opt(
                            "Otherwise information about the test set leaks into training and inflates scores",
                            correct=True,
                        ),
                        opt("Because the test set has no variance"),
                        opt("To make training faster"),
                        opt("Scalers can only see one array at a time"),
                    ),
                    "Fitting the scaler on all data is data leakage; fit on train, then apply to val/test.",
                ),
                q(
                    "What makes a random forest more robust than a single deep tree?",
                    (
                        opt(
                            "It averages many decorrelated trees, which reduces variance",
                            correct=True,
                        ),
                        opt("It uses a single very deep tree with more splits"),
                        opt("It never looks at the training data"),
                        opt("It removes all randomness"),
                    ),
                    "Bagging rows/features decorrelates the trees; averaging their votes cuts variance.",
                ),
                q(
                    "Why can't a network without non-linear activations be deep in any useful sense?",
                    (
                        opt("Composing linear maps is still just one linear map", correct=True),
                        opt("Linear layers are too slow"),
                        opt("Gradients become exactly zero"),
                        opt("It would overfit instantly"),
                    ),
                    "Non-linearities (ReLU, tanh, sigmoid) are what let stacked layers represent complex functions.",
                ),
                q(
                    "What is backpropagation, in one sentence?",
                    (
                        opt(
                            "The chain rule applied efficiently to compute every parameter's gradient by reusing downstream gradients",
                            correct=True,
                        ),
                        opt("A way to randomly reinitialise weights"),
                        opt("A method to add more layers to a network"),
                        opt("The forward pass run twice"),
                    ),
                    "Backprop reuses the downstream error term (δ) so all gradients cost about one forward pass.",
                ),
                q(
                    "Why is XOR a classic test for a hidden layer?",
                    (
                        opt(
                            "XOR is not linearly separable, so a single linear model cannot solve it",
                            correct=True,
                        ),
                        opt("XOR has too many features"),
                        opt("XOR requires a GPU"),
                        opt("XOR has no labels"),
                    ),
                    "No straight line separates XOR's classes; a hidden layer creates the needed non-linear boundary.",
                ),
                q(
                    "On a 99%-negative dataset, why is accuracy a poor metric?",
                    (
                        opt(
                            "A model that always predicts 'negative' scores 99% yet is useless — use precision/recall/AUC",
                            correct=True,
                        ),
                        opt("Accuracy can exceed 100% on imbalanced data"),
                        opt("Accuracy only works for regression"),
                        opt("Accuracy ignores the training set"),
                    ),
                    "With class imbalance, accuracy is dominated by the majority class; precision, recall and AUC are informative.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# 3. ml-advanced — deep learning + PyTorch & TensorFlow
# ──────────────────────────────────────────────────────────────────────

_ML_ADVANCED = SeedCourse(
    slug="ml-advanced",
    title="Deep Learning — Advanced",
    description=(
        "Deep learning in practice: softmax & cross-entropy, the optimisers and "
        "regularisers that make training work, and the same network built in both "
        "PyTorch and TensorFlow/Keras side by side. Plus CNNs for images and RNNs "
        "for sequences. (PyTorch/TF lessons are read-along; the runnable hands-on "
        "uses scikit-learn.)"
    ),
    level="Advanced",
    lessons=(
        _t(
            "Why deep learning works",
            "9 min",
            r"""# Why deep learning works

Classical ML leans on hand-crafted features. **Deep learning** learns the
features too: each layer transforms the previous one into a more useful
representation — edges → textures → parts → objects, for vision. Three things
made it explode in the 2010s:

- **Data** — internet-scale labelled datasets.
- **Compute** — GPUs/TPUs do the dense matrix multiplies at the core of
  training in parallel, thousands of times faster than CPUs.
- **Algorithms** — ReLU, better initialisation, batch/layer norm, Adam, and
  architectures (CNNs, Transformers) that match the structure of the data.

Everything runs on **tensors** — n-dimensional arrays (a batch of images is a
4-D tensor: batch × height × width × channels). Frameworks like PyTorch and
TensorFlow give you tensors **on the GPU** plus **automatic differentiation**,
so you describe the forward computation and get backprop for free. The rest of
this course is about using them well.
""",
        ),
        _t(
            "Softmax, cross-entropy & optimisers",
            "12 min",
            r"""# Softmax, cross-entropy & optimisers

**Softmax** turns a vector of scores (logits) into a probability distribution
over $K$ classes:

$$ \text{softmax}(z)_k = \frac{e^{z_k}}{\sum_{j} e^{z_j}}. $$

Paired with it, **cross-entropy** is the classification loss — the negative
log-probability the model assigns to the true class:

$$ L = -\sum_k y_k \log \hat{y}_k. $$

It punishes confident wrong answers brutally (log of a tiny number is hugely
negative), which is exactly the gradient signal you want.

**Optimisers** decide how to use the gradient:

- **SGD** — plain gradient descent on mini-batches.
- **Momentum** — accumulate a velocity so you power through flat regions and
  dampen zig-zags.
- **Adam** — per-parameter adaptive step sizes; the robust default.

The **learning rate** is still the most important knob. Too high diverges; too
low crawls. Schedules that decay it over time (or warm up then decay) are
standard:

```plot
{"title": "Learning-rate decay over training", "xLabel": "training step", "yLabel": "learning rate", "xRange": [0, 10], "yRange": [0, 1.1], "functions": [{"expr": "exp(-0.3*x)", "label": "exponential decay", "color": "#2563eb"}, {"expr": "1/(1 + 0.5*x)", "label": "1/t decay", "color": "#16a34a"}]}
```
""",
        ),
        _t(
            "Regularisation that makes nets generalise",
            "10 min",
            r"""# Regularisation

Deep nets have millions of parameters and overfit eagerly. The standard
toolkit:

- **Weight decay (L2)** — add $\lambda\lVert W\rVert^2$ to the loss so the
  optimiser prefers small weights and smoother functions.
- **Dropout** — during training, randomly zero a fraction of activations each
  step. The network can't rely on any single unit, so it learns redundant,
  robust features. Turned off at test time.
- **Batch / layer normalisation** — normalise activations inside the network,
  which stabilises and speeds up training and has a mild regularising effect.
  (BatchNorm uses the batch's statistics; LayerNorm uses each sample's — the
  latter is what Transformers use.)
- **Early stopping** — watch validation loss and stop when it turns upward.
- **Data augmentation** — flips, crops, noise: free extra training data that
  teaches invariances.

These are usually combined. A typical recipe: Adam + weight decay + dropout +
early stopping + augmentation. None of them change *what* the network can
represent — they steer training toward solutions that generalise.
""",
        ),
        _t(
            "PyTorch fundamentals (read-along)",
            "12 min",
            r"""# PyTorch fundamentals

> These framework lessons are **read-along** — PyTorch isn't in the in-browser
> sandbox (it's a multi-GB GPU library). Run them in your own environment with
> `pip install torch`.

PyTorch feels like NumPy with two superpowers: tensors live on the **GPU**, and
every operation is recorded so gradients flow automatically (**autograd**).

```python
import torch

# A tensor that tracks gradients:
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x          # build a computation graph
y.backward()                # backprop
print(x.grad)               # dy/dx = 2x + 3 = 7.0
```

You define a model by subclassing `nn.Module` and writing `forward`:

```python
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 16), nn.ReLU(),
            nn.Linear(16, 3),          # 3-class logits
        )
    def forward(self, x):
        return self.net(x)
```

The pieces — `Linear`, `ReLU`, `Sequential`, autograd — compose into anything.
Next: the training loop that ties them together.
""",
        ),
        _t(
            "Training a net in PyTorch (read-along)",
            "12 min",
            r"""# Training a net in PyTorch

The canonical loop is five lines you'll write a thousand times: **forward →
loss → zero grads → backward → step.**

```python
import torch
import torch.nn as nn

model = MLP()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()          # softmax + cross-entropy in one

for epoch in range(100):
    for xb, yb in train_loader:          # mini-batches
        optimizer.zero_grad()            # clear last step's gradients
        logits = model(xb)               # forward
        loss = loss_fn(logits, yb)       # compare to labels
        loss.backward()                  # autograd computes all gradients
        optimizer.step()                 # update every parameter

# Evaluation: no gradients, model in eval mode
model.eval()
with torch.no_grad():
    preds = model(x_test).argmax(dim=1)
    acc = (preds == y_test).float().mean()
    print("test accuracy:", acc.item())
```

`zero_grad` matters: PyTorch **accumulates** gradients, so you must clear them
each step. `CrossEntropyLoss` expects raw logits (it applies softmax
internally). `no_grad` + `eval()` switch off gradient tracking and dropout for
inference. That's the whole game — every PyTorch project is a variation on this
loop.
""",
        ),
        _t(
            "TensorFlow / Keras fundamentals (read-along)",
            "11 min",
            r"""# TensorFlow / Keras fundamentals

> Read-along — TensorFlow isn't in the sandbox either. Install with
> `pip install tensorflow`.

Keras (TensorFlow's high-level API) trades some flexibility for brevity: you
declare the layers and call `.fit()`. The **Sequential** API stacks layers:

```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(16, activation="relu", input_shape=(4,)),
    keras.layers.Dense(3),                      # 3-class logits
])

model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"],
)
```

For graphs that branch or merge, the **functional** API wires layers like
functions:

```python
inputs = keras.Input(shape=(4,))
h = keras.layers.Dense(16, activation="relu")(inputs)
outputs = keras.layers.Dense(3)(h)
model = keras.Model(inputs, outputs)
```

Same math as PyTorch — `Dense` = `Linear`, the loss is softmax + cross-entropy.
The difference is style: Keras hides the training loop.
""",
        ),
        _t(
            "The same net: PyTorch vs Keras",
            "9 min",
            r"""# The same net: PyTorch vs Keras

Side by side, the training step makes the philosophies clear.

**PyTorch — you write the loop (full control):**

```python
for xb, yb in train_loader:
    optimizer.zero_grad()
    loss = loss_fn(model(xb), yb)
    loss.backward()
    optimizer.step()
```

**Keras — the loop is one call (brevity):**

```python
model.fit(x_train, y_train, epochs=100, batch_size=32,
          validation_data=(x_val, y_val))
preds = model.predict(x_test)
```

**Which to use?** Both are excellent and converging in features.

- **PyTorch** dominates research and is the default for custom architectures —
  the explicit loop makes unusual training schemes natural.
- **Keras/TF** shines for fast standard models and has a mature production/serving
  story (TF Serving, TFLite for mobile/edge).

Learn one deeply and the other is a weekend. The concepts you built from
scratch in the Intermediate course — layers, activations, loss, backprop,
gradient descent — are exactly what both frameworks automate.
""",
        ),
        _code(
            "Train a neural net (scikit-learn, runnable)",
            "12 min",
            r"""# A runnable neural network via scikit-learn's MLPClassifier
# (same idea as PyTorch/Keras, but it runs here in the sandbox).
import numpy as np
from sklearn.datasets import load_digits
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

digits = load_digits()          # 8x8 handwritten digits, 10 classes
X = digits.data
y = digits.target
print("data:", X.shape[0], "images,", X.shape[1], "pixels each")

x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0
)

# Scale features (fit on train only!)
scaler = StandardScaler().fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

# One hidden layer of 64 ReLU units, trained with Adam:
net = MLPClassifier(hidden_layer_sizes=(64,), activation="relu",
                    solver="adam", max_iter=300, random_state=0)
net.fit(x_train, y_train)

print("train accuracy:", round(net.score(x_train, y_train), 3))
print("test  accuracy:", round(net.score(x_test, y_test), 3))
print("final training loss:", round(net.loss_, 4))
""",
        ),
        _t(
            "Convolutional neural networks (CNNs)",
            "11 min",
            r"""# Convolutional neural networks

Images have structure: nearby pixels relate, and a cat is a cat wherever it
appears. A **convolution** exploits both. A small **kernel** (say 3×3) slides
over the image computing weighted sums, producing a **feature map** that lights
up where its pattern occurs. Crucially, the *same* kernel is reused everywhere
(**weight sharing**) — so a CNN has far fewer parameters than a dense net and
is **translation-invariant**.

```plot
{"title": "An edge-detector kernel responds at the boundary", "xLabel": "position", "yLabel": "response", "xRange": [-6, 6], "yRange": [-1.2, 1.2], "functions": [{"expr": "tanh(2*x)", "label": "image intensity (an edge)", "color": "#9ca3af"}, {"expr": "4*x*exp(-x*x)", "label": "kernel response (peaks at edge)", "color": "#dc2626"}]}
```

A CNN stacks **conv → ReLU → pooling** blocks. **Pooling** (e.g. max over 2×2)
shrinks the maps, building tolerance to small shifts and growing the *receptive
field* so deeper layers see more of the image. Early layers learn edges and
colours; deeper layers learn textures, parts, then whole objects. This
hierarchy is why CNNs revolutionised computer vision (and they remain strong
for images even in the Transformer era).
""",
        ),
        _t(
            "Sequences: RNNs & LSTMs",
            "9 min",
            r"""# Sequences: RNNs & LSTMs

Text, audio, and time series are **sequences** — order matters and length
varies. A **Recurrent Neural Network (RNN)** processes one element at a time,
carrying a **hidden state** $h_t$ that summarises everything seen so far:

$$ h_t = g(W_x x_t + W_h h_{t-1} + b). $$

In principle the state remembers the past; in practice plain RNNs forget
quickly because gradients **vanish** (or explode) when backpropagated through
many steps. **LSTMs** and **GRUs** fix this with **gates** — learned valves
that decide what to keep, forget, and output — letting them carry information
across long ranges.

RNNs ruled sequence modelling for years, but they have a fatal limit: they're
**inherently sequential**, so they can't be parallelised over the time
dimension, and very long-range dependencies remain hard. The fix — process the
whole sequence at once and let every position attend directly to every other —
is **attention**, and it's the subject of the dedicated *Transformers* course.
""",
        ),
        _t(
            "Practical deep learning",
            "10 min",
            r"""# Practical deep learning

Getting a model to work in the real world is mostly engineering:

- **Data is the model.** More, cleaner, better-labelled data beats architecture
  tweaks almost every time. Audit your labels; check class balance; look at the
  examples your model gets wrong.
- **Transfer learning.** Rarely train from scratch. Take a model pretrained on a
  huge dataset and **fine-tune** it on your (smaller) task — you inherit its
  learned features and need far less data and compute.
- **Start simple, then scale.** Get a tiny model overfitting a tiny dataset
  first (proves the pipeline works), then grow.
- **Track everything.** Log losses, metrics, hyperparameters, and random seeds
  so results are reproducible.
- **Watch the val curve.** Train and validation loss diverging = overfitting;
  both high = underfitting or a bug.
- **Deployment.** A trained model is an artefact you serve behind an API,
  quantise for **edge** devices, or batch offline. Latency, memory, and
  monitoring for drift matter as much as accuracy.

The frontier — and Cyberdyne's domain — is large models served as
infrastructure: retrieval-augmented generation, agents, and fine-tuned LLMs.
The next course builds the architecture behind all of them.
""",
        ),
        quiz_lesson(
            "Quiz: Deep Learning",
            (
                q(
                    "What does softmax produce from a vector of logits?",
                    (
                        opt(
                            "A probability distribution over the classes (positive, sums to 1)",
                            correct=True,
                        ),
                        opt("A single number in (0, 1)"),
                        opt("The index of the largest logit"),
                        opt("The gradient of the loss"),
                    ),
                    "Softmax exponentiates and normalises the logits into class probabilities.",
                ),
                q(
                    "What does dropout do, and when is it active?",
                    (
                        opt(
                            "Randomly zeroes activations during training only; off at test time",
                            correct=True,
                        ),
                        opt("Permanently removes neurons from the network"),
                        opt("Drops the learning rate each epoch"),
                        opt("Is active only during evaluation"),
                    ),
                    "Dropout forces redundancy during training and is disabled for inference.",
                ),
                q(
                    "In a PyTorch training loop, why call optimizer.zero_grad() each step?",
                    (
                        opt(
                            "PyTorch accumulates gradients; you must clear them before the next backward()",
                            correct=True,
                        ),
                        opt("It resets the model weights to zero"),
                        opt("It disables autograd"),
                        opt("It is optional and only cosmetic"),
                    ),
                    "Gradients add up across backward() calls, so each step starts by zeroing them.",
                ),
                q(
                    "What two properties make convolutions great for images?",
                    (
                        opt(
                            "Weight sharing (fewer parameters) and translation invariance",
                            correct=True,
                        ),
                        opt("They require no activation functions"),
                        opt("They process pixels in random order"),
                        opt("They only work on grayscale images"),
                    ),
                    "A shared kernel slid across the image detects a pattern anywhere with few parameters.",
                ),
                q(
                    "Why do plain RNNs struggle with long sequences?",
                    (
                        opt(
                            "Gradients vanish or explode through many time steps, so they forget the distant past",
                            correct=True,
                        ),
                        opt("They have too many parameters"),
                        opt("They can only read sequences backward"),
                        opt("They need labelled data for every step"),
                    ),
                    "Backpropagating through many steps shrinks/blows up gradients; LSTMs use gates to mitigate this.",
                ),
                q(
                    "What is transfer learning?",
                    (
                        opt(
                            "Fine-tuning a model pretrained on a large dataset for your smaller task",
                            correct=True,
                        ),
                        opt("Copying data between GPUs"),
                        opt("Training two models and averaging them"),
                        opt("Converting PyTorch code to TensorFlow"),
                    ),
                    "You reuse learned features from a big pretrained model, needing far less data and compute.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# 4. transformers — attention, the architecture, GPT/LLMs
# ──────────────────────────────────────────────────────────────────────

_TRANSFORMERS = SeedCourse(
    slug="transformers",
    title="Transformers & LLMs — Advanced",
    description=(
        "The architecture behind modern AI. Build intuition and the math for "
        "self-attention, implement scaled dot-product attention from scratch in "
        "NumPy, understand positional encodings and the full Transformer block, "
        "then see how GPT-style LLMs are trained and used (fine-tuning, RAG, "
        "agents)."
    ),
    level="Advanced",
    lessons=(
        _t(
            "From RNNs to attention",
            "9 min",
            r"""# From RNNs to attention

RNNs read a sequence one step at a time, squeezing the whole past into a single
hidden vector. Two problems: that bottleneck loses detail over long ranges, and
the step-by-step recurrence **can't be parallelised** — fatal when you want to
train on trillions of tokens.

**Attention** throws out recurrence. Process the whole sequence at once and let
every position look **directly** at every other position, pulling in whatever
is relevant — no matter how far away. "The animal didn't cross the street
because **it** was tired": to resolve *it*, the model attends straight to
*animal*, however many words back.

This gives three wins at once:

1. **Long-range** dependencies in a single hop.
2. **Full parallelism** — every position computed simultaneously (GPU-friendly).
3. **Interpretability** — the attention weights show what attended to what.

The 2017 paper that did this was literally titled *"Attention Is All You
Need"* — it dropped recurrence entirely. The rest of this course builds that
mechanism up from scratch.
""",
        ),
        _t(
            "Self-attention: Q, K, V",
            "13 min",
            r"""# Self-attention: queries, keys, values

Each token emits three vectors, all learned linear projections of its
embedding:

- **Query** $q$ — what this token is looking for.
- **Key** $k$ — what this token offers.
- **Value** $v$ — the information it passes on if attended to.

A token's query is compared against **every** token's key by dot product
(higher = more relevant). Those scores are scaled and softmax-ed into weights
that sum to 1, then used to take a weighted average of the **values**. In
matrix form, for the whole sequence at once:

$$ \text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{Q K^{\top}}{\sqrt{d_k}}\right) V. $$

Why divide by $\sqrt{d_k}$? With large key dimension $d_k$, the dot products
grow large, pushing softmax into saturated regions where gradients vanish.
Scaling keeps them well-behaved.

So each output is a **content-based blend** of the whole sequence's values,
weighted by relevance — computed for every position in parallel with two matrix
multiplies and a softmax. You'll code exactly this in two lessons.
""",
        ),
        _t(
            "Multi-head attention",
            "9 min",
            r"""# Multi-head attention

One attention pattern is limiting — a token may need to track several
relationships at once (syntax, coreference, topic). **Multi-head attention**
runs $h$ attention operations in parallel, each with its **own** learned
$Q,K,V$ projections into a smaller subspace:

$$ \text{head}_i = \text{Attention}(QW_i^Q,\, KW_i^K,\, VW_i^V), $$
$$ \text{MHA} = \text{Concat}(\text{head}_1,\dots,\text{head}_h)\,W^O. $$

Each head can specialise — one might attend to the previous word, another to
the verb a phrase depends on, another to matching brackets. Their outputs are
concatenated and mixed by a final projection $W^O$. Because each head works in
a $d/h$-dimensional subspace, multi-head costs about the same as one full-width
head but is far more expressive.

This is the core building block. Wrap it with a feed-forward network, residual
connections, and normalisation and you have a Transformer layer — next.
""",
        ),
        _code(
            "Self-attention from scratch (NumPy)",
            "15 min",
            r"""# Scaled dot-product self-attention in pure NumPy.
# softmax(Q K^T / sqrt(d)) V  — the heart of every Transformer.
import numpy as np

np.random.seed(0)

# A toy sequence: 3 tokens, each a 4-dimensional embedding.
tokens = np.array([
    [1.0, 0.0, 1.0, 0.0],
    [0.0, 2.0, 0.0, 2.0],
    [1.0, 1.0, 1.0, 1.0],
])
seq_len, d_model = tokens.shape
d_k = 4

# Learned projections (random here; trained in a real model).
Wq = np.random.randn(d_model, d_k)
Wk = np.random.randn(d_model, d_k)
Wv = np.random.randn(d_model, d_k)

Q = tokens.dot(Wq)
K = tokens.dot(Wk)
V = tokens.dot(Wv)

# scores -> scale -> row-wise softmax (inlined) -> weighted sum of values
scores = Q.dot(K.T) / np.sqrt(d_k)            # (seq, seq) relevance
scores = scores - scores.max(axis=1, keepdims=True)   # numerical stability
e = np.exp(scores)
weights = e / e.sum(axis=1, keepdims=True)    # each row sums to 1
output = weights.dot(V)                       # blended values

print("attention weights (rows sum to 1):")
print(np.round(weights, 3))
print("each weight row sums to:", np.round(weights.sum(axis=1), 3))
print("output shape:", output.shape, "(one context vector per token)")
print("output:")
print(np.round(output, 3))
""",
        ),
        _t(
            "Positional encoding",
            "10 min",
            r"""# Positional encoding

Attention is **permutation-invariant** — shuffle the tokens and the math is
unchanged, because it has no built-in notion of order. But "dog bites man" and
"man bites dog" are different! So we **add** position information to each token
embedding.

The original Transformer uses fixed **sinusoidal** encodings: each dimension is
a sine or cosine of the position at a different frequency.

$$ PE_{(pos,\,2i)} = \sin\!\left(\frac{pos}{10000^{2i/d}}\right),\quad PE_{(pos,\,2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/d}}\right). $$

Low dimensions oscillate fast, high dimensions slowly — together they give every
position a unique, smoothly varying fingerprint that the model can use to reason
about relative distances. Slide the dimension to see how the frequency changes:

```plot
{"title": "Sinusoidal positional encoding (one dimension)", "xLabel": "position", "yLabel": "PE value", "xRange": [0, 50], "yRange": [-1.2, 1.2], "controls": [{"name": "i", "range": [0, 6], "value": 1, "step": 1, "label": "dimension i"}], "functions": [{"expr": "sin(x / pow(10000, 2*i/16))", "label": "sin(pos / 10000^(2i/d))", "color": "#2563eb"}]}
```

Modern LLMs often swap this for **learned** or **rotary (RoPE)** encodings, but
the goal is identical: give attention a sense of where each token sits.
""",
        ),
        _t(
            "The Transformer block",
            "11 min",
            r"""# The Transformer block

A Transformer layer wraps multi-head attention in two more ideas that make deep
stacks trainable:

1. **Residual connections** — add the input back to each sublayer's output
   ($x + \text{Sublayer}(x)$). Gradients get a direct path, so you can stack
   dozens of layers without them vanishing.
2. **Layer normalisation** — normalise each token's vector (per sample, not per
   batch) to stabilise training.

A full block is two sublayers, each residual-and-normed:

$$ a = \text{LayerNorm}\big(x + \text{MultiHead}(x)\big), $$
$$ y = \text{LayerNorm}\big(a + \text{FFN}(a)\big). $$

The **feed-forward network (FFN)** is a small per-token MLP (expand to ~4× width
with a non-linearity, then project back). Intuition: attention **mixes
information across tokens**; the FFN **processes each token's gathered
information**. Alternating them, layer after layer, is the whole recipe.

Stack $N$ identical blocks and you have a Transformer encoder (or, with masking,
a decoder).
""",
        ),
        _t(
            "The original architecture",
            "9 min",
            r"""# The original architecture (2017)

The first Transformer was an **encoder–decoder** for translation:

- The **encoder** (a stack of blocks) reads the source sentence and produces a
  context-rich representation of every token. Its attention is
  **bidirectional** — each token sees the whole input.
- The **decoder** generates the translation one token at a time. It uses
  **masked** self-attention (a token may only attend to earlier positions, so
  it can't peek at the future it's trying to predict) plus **cross-attention**
  into the encoder's output.

Three attention flavours, then:

- **Encoder self-attention** — input attends to input (bidirectional).
- **Masked decoder self-attention** — output attends to earlier output only.
- **Cross-attention** — decoder queries attend to encoder keys/values.

From this base, two families split off: **encoder-only** models (BERT) great at
understanding/classification, and **decoder-only** models (GPT) great at
generation. The latter took over large language modelling — next.
""",
        ),
        _t(
            "A minimal block in PyTorch (read-along)",
            "9 min",
            r"""# A minimal Transformer block in PyTorch

> Read-along (PyTorch isn't in the sandbox). PyTorch even ships the whole block
> as `nn.TransformerEncoderLayer`, but here's the anatomy spelled out.

```python
import torch
import torch.nn as nn

class Block(nn.Module):
    def __init__(self, d_model, n_heads, d_ff):
        super().__init__()
        self.attn = nn.MultiheadAttention(d_model, n_heads, batch_first=True)
        self.norm1 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_ff), nn.GELU(),
            nn.Linear(d_ff, d_model),
        )
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x, mask=None):
        # Residual + norm around attention:
        a, _ = self.attn(x, x, x, attn_mask=mask)
        x = self.norm1(x + a)
        # Residual + norm around the feed-forward net:
        x = self.norm2(x + self.ff(x))
        return x
```

Note the shape: `x` is `(batch, seq_len, d_model)` throughout — the block maps a
sequence of vectors to a same-shaped sequence, so you can stack `Block`s
arbitrarily deep. Everything you implemented in NumPy (Q/K/V, scaled softmax,
multi-head) lives inside `nn.MultiheadAttention`.
""",
        ),
        _t(
            "GPT & large language models",
            "11 min",
            r"""# GPT & large language models

GPT-style models are **decoder-only** Transformers trained on one
breathtakingly simple objective: **predict the next token**. Feed in a stretch
of text with masked self-attention (each position sees only what came before)
and ask, at every position, "what comes next?" — billions of times over the
internet.

Pipeline:

1. **Tokenisation** — text is split into subword **tokens** (e.g. byte-pair
   encoding); each maps to an embedding.
2. **Forward pass** — stacked decoder blocks produce, at the last position, a
   distribution over the vocabulary.
3. **Sampling** — pick the next token (greedy, or with **temperature**/top-p
   randomness), append it, and repeat **autoregressively** to generate text.

That's it — no task-specific labels, just next-token prediction at scale. The
striking result is **emergence**: a model trained only to continue text turns
out to translate, summarise, write code, and reason, because doing those well
helps predict the next token. Scale (parameters × data × compute) reliably
improves capability, which is why these models — and the infrastructure to
serve them — became the centre of modern AI.
""",
        ),
        _t(
            "Using LLMs: fine-tuning, RAG & agents",
            "11 min",
            r"""# Using LLMs in practice

You rarely train an LLM from scratch (that costs millions). Instead:

- **Prompting** — the base skill. Give clear instructions, examples
  (*few-shot*), and ask the model to reason step by step. Often enough on its
  own.
- **Fine-tuning** — continue training a pretrained model on your own examples to
  specialise tone, format, or domain. **Instruction tuning** and **RLHF**
  (learning from human preference feedback) are what turn a raw next-token
  predictor into a helpful assistant. Parameter-efficient methods (**LoRA**)
  make this cheap.
- **Retrieval-Augmented Generation (RAG)** — the model's weights are frozen and
  out of date, so **retrieve** relevant documents (via embedding/vector search)
  and put them in the prompt. The model answers grounded in *your* data, with
  citations, and updates the moment your documents do — no retraining.
- **Agents** — give the model **tools** (search, code execution, APIs) and let
  it decide when to call them, observe results, and loop. This turns a text
  generator into a system that can take actions.

This is exactly Cyberdyne's domain — RAG, agents, and fine-tuned models served
as **infrastructure**. You now have the full stack: from a line fit by gradient
descent, through backprop and neural nets, to the Transformer and the LLMs
built on it.
""",
        ),
        quiz_lesson(
            "Quiz: Transformers & LLMs",
            (
                q(
                    "What is the scaled dot-product attention formula?",
                    (
                        opt("softmax(Q·Kᵀ / √dₖ) · V", correct=True),
                        opt("softmax(Q + K + V)"),
                        opt("Q · K · V"),
                        opt("σ(Q·Kᵀ) − V"),
                    ),
                    "Query–key dot products are scaled by √dₖ, softmaxed into weights, then used to average the values.",
                ),
                q(
                    "Why divide the attention scores by √dₖ?",
                    (
                        opt(
                            "Large dₖ makes dot products big, saturating softmax and killing gradients; scaling fixes it",
                            correct=True,
                        ),
                        opt("To make the weights negative"),
                        opt("To reduce the number of parameters"),
                        opt("To convert values into queries"),
                    ),
                    "Scaling keeps the logits in a range where softmax has useful gradients.",
                ),
                q(
                    "Why do Transformers need positional encodings?",
                    (
                        opt(
                            "Self-attention is permutation-invariant, so order must be added explicitly",
                            correct=True,
                        ),
                        opt("To reduce memory usage"),
                        opt("Because tokens have no embeddings otherwise"),
                        opt("To replace the softmax"),
                    ),
                    "Attention has no inherent sense of order; positional encodings inject it.",
                ),
                q(
                    "What do residual connections + LayerNorm enable in a Transformer block?",
                    (
                        opt(
                            "Training very deep stacks by giving gradients a direct path and stabilising activations",
                            correct=True,
                        ),
                        opt("Removing the need for attention"),
                        opt("Turning the decoder into an encoder"),
                        opt("Eliminating the feed-forward network"),
                    ),
                    "Residuals prevent vanishing gradients across depth; LayerNorm keeps activations stable.",
                ),
                q(
                    "What objective is a GPT-style model trained on?",
                    (
                        opt(
                            "Predicting the next token, autoregressively, with masked self-attention",
                            correct=True,
                        ),
                        opt("Classifying sentences into topics"),
                        opt("Reconstructing shuffled pixels"),
                        opt("Minimising the distance between two images"),
                    ),
                    "Decoder-only LLMs are trained to predict the next token given all previous ones.",
                ),
                q(
                    "What problem does Retrieval-Augmented Generation (RAG) solve?",
                    (
                        opt(
                            "It grounds answers in your own/up-to-date documents without retraining the model",
                            correct=True,
                        ),
                        opt("It makes the model train faster on GPUs"),
                        opt("It removes the need for tokenisation"),
                        opt("It converts an encoder into a decoder"),
                    ),
                    "RAG retrieves relevant documents into the prompt, so frozen-weight models answer from current, private data.",
                ),
            ),
        ),
    ),
)


ML_COURSES = (_ML_BASICS, _ML_INTERMEDIATE, _ML_ADVANCED, _TRANSFORMERS)
