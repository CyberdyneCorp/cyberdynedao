"""Machine Learning for Life Sciences track: Basics -> Intermediate -> Advanced.

A university-level path from biological data, features and the kinds of learning,
through the core quantitative methods (models, cross-validation, metrics), to
state-of-the-art and applied topics (imbalanced data, interpretability, deep
learning and the pitfalls of ML in biology). Lessons use interactive ```plot
blocks for quantitative relationships (loss curves, ROC, learning curves,
calibration) and ```mermaid diagrams for pipelines, data flows and taxonomies.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- ML for Life Sciences -- Basics --------------------------------------------

_BASICS = SeedCourse(
    slug="ml-life-sciences-basics",
    title="Machine Learning for Life Sciences — Basics",
    description=(
        "What machine learning is and how it applies to biology: examples, "
        "features and labels; supervised, unsupervised and reinforcement "
        "learning; the bias-variance trade-off and overfitting; how data is "
        "split for honest evaluation; and the first models (linear and logistic "
        "regression, k-NN). Grounded in real life-science examples with "
        "interactive plots and pipeline diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What machine learning is and why biology needs it",
            "10 min",
            r"""
# What machine learning is and why biology needs it

**Machine learning (ML)** builds models that learn patterns from data rather
than being explicitly programmed with rules. Formally, a model is a function
$f_\theta$ with parameters $\theta$ fitted to minimise a **loss** measuring the
gap between predictions and truth. Biology needs ML because modern assays —
genome sequencing, single-cell RNA-seq, mass spectrometry, microscopy — produce
high-dimensional data whose patterns no human can hand-code.

```mermaid
flowchart LR
  DATA["Biological data: omics, images, signals"] --> FEAT["Features"]
  FEAT --> MODEL["Model f_theta"]
  MODEL --> PRED["Predictions"]
  PRED --> LOSS["Loss vs truth"]
  LOSS -->|update theta| MODEL
```

Typical life-science tasks include predicting whether a tumour is malignant from
gene expression, classifying cell types from single-cell data, or predicting a
protein's function from sequence. Learning is iterative: as the model sees more
training data, its error on that data falls, but the *useful* gains plateau —
real skill is generalising to unseen samples.

```plot
{"title": "Training loss decreasing over iterations", "xLabel": "training iteration", "yLabel": "loss", "xRange": [0, 20], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.3*x)", "label": "loss decays as model fits", "color": "#2563eb"}]}
```

**Next:** the raw material of ML — examples, features and labels.
""",
        ),
        _t(
            "Examples, features and labels",
            "11 min",
            r"""
# Examples, features and labels

ML organises data as a **design matrix** $X$ of shape $n \times p$: $n$
**examples** (rows, e.g. patients or cells) each described by $p$ **features**
(columns, e.g. expression of $p$ genes). In **supervised** learning each example
also has a **label** $y$ — a class (malignant/benign) or a number (drug $IC_{50}$).

Choosing and preparing features is **feature engineering**. Biological features
are often on wildly different scales, so we **standardise** each to zero mean and
unit variance, $z = \frac{x - \mu}{\sigma}$, so that no single gene dominates by
magnitude alone.

```mermaid
flowchart LR
  RAW["Raw measurements"] --> CLEAN["Clean / normalize"]
  CLEAN --> ENC["Encode categorical, scale numeric"]
  ENC --> X["Design matrix X (n x p)"]
  X --> Y["Labels y"]
```

A defining feature of biology is that $p$ often greatly exceeds $n$ — thousands
of genes, dozens of samples (the "large $p$, small $n$" regime). This makes
models prone to fitting noise, so the number of features we can safely use grows
only slowly with sample size.

```plot
{"title": "Safe model capacity vs sample size", "xLabel": "number of samples n", "yLabel": "usable features (relative)", "xRange": [0, 100], "yRange": [0, 12], "grid": true, "functions": [{"expr": "sqrt(x)", "label": "capacity grows sub-linearly", "color": "#16a34a"}]}
```

**Next:** the three broad styles of learning.
""",
        ),
        _t(
            "Types of learning: supervised, unsupervised, reinforcement",
            "11 min",
            r"""
# Types of learning: supervised, unsupervised, reinforcement

ML problems fall into three broad families distinguished by what feedback the
model gets.

- **Supervised learning** uses labelled examples to predict $y$ from $X$.
  *Classification* predicts a category (disease subtype); *regression* predicts a
  number (gene expression level, binding affinity).
- **Unsupervised learning** has no labels and finds structure: *clustering*
  groups similar cells (e.g. Leiden clustering of single-cell data) and
  *dimensionality reduction* (PCA, UMAP) compresses many genes into a few axes.
- **Reinforcement learning** learns a policy by trial and error against a reward,
  used for example in de novo molecule design and adaptive experiment selection.

```mermaid
flowchart TB
  ML["Machine learning"] --> SUP["Supervised: X -> y"]
  ML --> UNS["Unsupervised: structure in X"]
  ML --> RL["Reinforcement: actions -> reward"]
  SUP --> CLS["Classification"]
  SUP --> REG["Regression"]
  UNS --> CLU["Clustering"]
  UNS --> DR["Dimensionality reduction"]
```

In unsupervised analysis, adding clusters always fits training data better, but
the *gain* in explained variation diminishes — the basis for "elbow" heuristics
that pick a sensible number of groups.

```plot
{"title": "Explained variation vs number of clusters", "xLabel": "number of clusters k", "yLabel": "explained variation", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "diminishing returns (elbow)", "color": "#dc2626"}]}
```

**Next:** why fitting the training data perfectly is a trap.
""",
        ),
        _t(
            "Overfitting and the bias-variance trade-off",
            "12 min",
            r"""
# Overfitting and the bias-variance trade-off

A model that memorises the training set but fails on new data has **overfit**.
The expected test error decomposes into three parts:

$$\text{Error} = \text{Bias}^2 + \text{Variance} + \sigma^2$$

**Bias** is error from an over-simple model (underfitting); **variance** is
sensitivity to the particular training sample (overfitting); $\sigma^2$ is
irreducible noise. As model complexity rises, bias falls but variance grows, so
test error is U-shaped with a sweet spot in the middle.

```mermaid
flowchart LR
  SIMPLE["Too simple: high bias (underfit)"] --> GOOD["Right capacity"]
  GOOD --> COMPLEX["Too complex: high variance (overfit)"]
```

In biology, with few samples and many features, the variance term dominates, so
controlling complexity (regularisation, fewer features) is essential. The total
test error as a function of complexity captures the trade-off directly:

```plot
{"title": "Test error vs model complexity (U-shape)", "xLabel": "model complexity", "yLabel": "expected test error", "xRange": [0, 10], "yRange": [0, 6], "grid": true, "functions": [{"expr": "4/(x+1) + 0.4*x", "label": "bias^2 + variance", "color": "#2563eb"}]}
```

The remedy is honest evaluation on held-out data and methods that penalise
unnecessary complexity, covered next.

**Next:** splitting data so evaluation is honest.
""",
        ),
        _t(
            "Splitting data: train, validation and test",
            "11 min",
            r"""
# Splitting data: train, validation and test

To estimate how a model performs on *unseen* data, we split the dataset.
**Training** data fits parameters $\theta$; a **validation** set tunes
**hyperparameters** (model choices like regularisation strength); and a held-out
**test** set, touched only once, gives an unbiased performance estimate.

```mermaid
flowchart LR
  ALL["All data"] --> TR["Train: fit parameters"]
  ALL --> VAL["Validation: tune hyperparameters"]
  ALL --> TE["Test: final unbiased estimate"]
```

A subtle but critical biological pitfall is **data leakage**: information from
test examples sneaking into training. Common causes are scaling using the whole
dataset before splitting, or putting replicates of the *same* patient in both
train and test — which inflates apparent accuracy. Splits must respect biological
grouping (split by patient, batch or site).

As the training fraction grows, the held-out estimate becomes more stable, but
the gain in reliability saturates — beyond a point, more training data helps the
model more than it helps the estimate.

```plot
{"title": "Estimate stability vs training fraction", "xLabel": "fraction used for training (%)", "yLabel": "estimate reliability", "xRange": [0, 90], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+20)", "label": "reliability saturates", "color": "#16a34a"}]}
```

**Next:** your first predictive models.
""",
        ),
        _t(
            "First models: linear, logistic and k-NN",
            "12 min",
            r"""
# First models: linear, logistic and k-NN

Three simple models cover a lot of ground.

**Linear regression** predicts a number as a weighted sum of features,
$\hat{y} = w_0 + \sum_j w_j x_j$, fitting weights by least squares. It is the
baseline for any regression task (e.g. predicting a continuous biomarker).

**Logistic regression** predicts a probability for classification by squashing
the linear score through a **sigmoid**, $p = \frac{1}{1 + e^{-z}}$, where
$z = w_0 + \sum_j w_j x_j$. Despite its name it is a classifier and is the
workhorse for disease-risk modelling.

**k-nearest neighbours (k-NN)** makes no equation: it labels a new example by the
majority vote of its $k$ closest training examples, relying purely on a distance.

```mermaid
flowchart TB
  X["Features x"] --> LIN["Linear: weighted sum"]
  X --> LOG["Logistic: sigmoid of weighted sum"]
  X --> KNN["k-NN: vote of nearest neighbours"]
  LIN --> NUM["Number"]
  LOG --> PROB["Probability / class"]
  KNN --> CLS["Class"]
```

The sigmoid maps any real score to a probability in $(0,1)$, giving logistic
regression its smooth, interpretable decision curve:

```plot
{"title": "Logistic sigmoid: score to probability", "xLabel": "linear score z", "yLabel": "predicted probability", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "p = 1/(1+e^-z)", "color": "#2563eb"}]}
```

**Next:** check your grasp of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- ML for Life Sciences -- Intermediate --------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="ml-life-sciences-intermediate",
    title="Machine Learning for Life Sciences — Intermediate",
    description=(
        "The core quantitative toolkit: cross-validation for small biological "
        "datasets, regularisation (ridge, lasso, elastic net) for high-"
        "dimensional omics, classification metrics and ROC/PR curves, "
        "tree ensembles (random forests, gradient boosting), unsupervised "
        "structure with PCA and clustering, and feature selection without "
        "leakage. Includes interactive plots of ROC, regularisation paths and "
        "variance explained."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Cross-validation for small biological datasets",
            "12 min",
            r"""
# Cross-validation for small biological datasets

A single train/test split wastes scarce biological samples and gives a noisy
estimate. **k-fold cross-validation (CV)** splits the data into $k$ folds, trains
on $k-1$ and tests on the held-out fold, rotating so every example is tested
once; the $k$ scores are averaged.

```mermaid
flowchart LR
  DATA["Dataset"] --> F["Split into k folds"]
  F --> R1["Round 1: fold 1 test"]
  F --> R2["Round 2: fold 2 test"]
  F --> RK["Round k: fold k test"]
  R1 --> AVG["Average score +/- SD"]
  R2 --> AVG
  RK --> AVG
```

For class imbalance, use **stratified** CV so each fold preserves class
proportions. Critically, all preprocessing (scaling, feature selection) must be
fit **inside** each training fold — fitting on the full dataset leaks test
information and inflates scores. **Nested CV** adds an inner loop for
hyperparameter tuning so the outer estimate stays unbiased.

Increasing $k$ reduces the bias of the error estimate but raises compute cost and
variance; the marginal benefit beyond $k=10$ is small, which is why 5- or 10-fold
CV is standard:

```plot
{"title": "Estimate bias vs number of folds k", "xLabel": "number of folds k", "yLabel": "estimate bias (relative)", "xRange": [2, 20], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(x-1)", "label": "bias falls then plateaus", "color": "#2563eb"}]}
```

**Next:** taming high-dimensional omics with regularisation.
""",
        ),
        _t(
            "Regularisation: ridge, lasso and elastic net",
            "13 min",
            r"""
# Regularisation: ridge, lasso and elastic net

When features outnumber samples, unregularised models overfit. **Regularisation**
adds a penalty on weight size to the loss, shrinking weights toward zero.

**Ridge** ($L_2$) minimises $\sum (y_i - \hat{y}_i)^2 + \lambda \sum_j w_j^2$;
it shrinks all weights smoothly and handles correlated genes well. **Lasso**
($L_1$) penalises $\lambda \sum_j |w_j|$, driving some weights *exactly* to zero
and so performing automatic **feature selection** — invaluable for finding a
small panel of predictive genes. **Elastic net** mixes both, keeping sparsity
while sharing weight across correlated features.

```mermaid
flowchart LR
  LOSS["Fit term + penalty"] --> RIDGE["Ridge L2: shrink all"]
  LOSS --> LASSO["Lasso L1: sparse, selects features"]
  LOSS --> EN["Elastic net: L1 + L2"]
```

The penalty strength $\lambda$ is a hyperparameter chosen by CV. As $\lambda$
grows, coefficient magnitudes shrink toward zero — the **regularisation path**:

```plot
{"title": "Coefficient magnitude vs regularisation strength", "xLabel": "regularisation strength lambda", "yLabel": "coefficient magnitude", "xRange": [0, 10], "yRange": [0, 5], "grid": true, "functions": [{"expr": "5*exp(-0.5*x)", "label": "weights shrink toward 0", "color": "#dc2626"}]}
```

Too little $\lambda$ overfits; too much underfits — so the optimal value is found
by minimising cross-validated error.

**Next:** measuring classifier performance honestly.
""",
        ),
        _t(
            "Classification metrics and ROC/PR curves",
            "13 min",
            r"""
# Classification metrics and ROC/PR curves

**Accuracy** alone is misleading, especially with imbalanced classes. From the
**confusion matrix** (TP, FP, TN, FN) we derive richer metrics:
**sensitivity** (recall) $= \frac{TP}{TP+FN}$, **specificity**
$= \frac{TN}{TN+FP}$, **precision** $= \frac{TP}{TP+FP}$, and their harmonic mean
the **F1 score**.

```mermaid
flowchart LR
  PRED["Predicted vs actual"] --> CM["Confusion matrix: TP FP TN FN"]
  CM --> SENS["Sensitivity / recall"]
  CM --> SPEC["Specificity"]
  CM --> PREC["Precision"]
  PREC --> F1["F1 score"]
  SENS --> F1
```

A classifier outputs a score; sweeping the **threshold** trades sensitivity
against specificity. The **ROC curve** plots true-positive rate vs false-positive
rate; its area (**AUROC**) summarises ranking quality (0.5 = random, 1.0 =
perfect). For rare positives, the **precision-recall (PR) curve** and its area
(AUPRC) are more informative because they ignore the abundant true negatives.

```plot
{"title": "ROC curve: a good classifier bows toward top-left", "xLabel": "false-positive rate", "yLabel": "true-positive rate", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "sqrt(x)", "label": "ROC (AUROC ~ 0.67)", "color": "#2563eb"}]}
```

The diagonal $TPR = FPR$ is chance; the further the curve bows above it, the
better the model separates classes.

**Next:** powerful off-the-shelf models — tree ensembles.
""",
        ),
        _t(
            "Tree ensembles: random forests and gradient boosting",
            "12 min",
            r"""
# Tree ensembles: random forests and gradient boosting

A single **decision tree** splits feature space by recursive yes/no questions; it
is interpretable but unstable. **Ensembles** combine many trees for far better
accuracy and are the default strong baseline on tabular biological data.

**Random forests** train many trees on bootstrap samples with random feature
subsets, then average them — reducing variance through decorrelation. **Gradient
boosting** (XGBoost, LightGBM) instead adds trees **sequentially**, each fitting
the residual errors of the current ensemble, reducing bias.

```mermaid
flowchart TB
  DATA["Training data"] --> RF["Random forest: parallel, bagged trees"]
  DATA --> GB["Gradient boosting: sequential residual trees"]
  RF --> AVG["Average / vote (variance down)"]
  GB --> ADD["Additive correction (bias down)"]
```

Both report **feature importance**, useful for nominating candidate biomarkers
(but not causal proof). Ensemble error falls as trees are added, with strongly
diminishing returns — more trees never overfit a random forest but stop helping:

```plot
{"title": "Ensemble error vs number of trees", "xLabel": "number of trees", "yLabel": "test error", "xRange": [1, 100], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.2 + 0.6/sqrt(x)", "label": "error plateaus", "color": "#dc2626"}]}
```

**Next:** finding structure without labels.
""",
        ),
        _t(
            "Unsupervised structure: PCA and clustering",
            "12 min",
            r"""
# Unsupervised structure: PCA and clustering

When no labels exist, **unsupervised** methods reveal structure.
**Principal component analysis (PCA)** finds orthogonal directions (principal
components) capturing maximal variance, projecting thousands of genes onto a few
axes. The first components often correspond to dominant biological or technical
signals (cell type, batch).

```mermaid
flowchart LR
  X["High-dim expression"] --> CENTER["Center / scale"]
  CENTER --> COV["Covariance structure"]
  COV --> PC["Principal components"]
  PC --> VIS["2D/3D visualization & clustering"]
```

**Clustering** then groups samples: **k-means** partitions into $k$ spherical
clusters by minimising within-cluster variance; **hierarchical** clustering
builds a dendrogram; **graph-based** methods (Louvain, Leiden) dominate
single-cell analysis. Non-linear embeddings (**UMAP**, **t-SNE**) are used for
visualisation but distort global distances, so cluster on the data, not the
embedding.

The variance explained accumulates across components and saturates — a **scree
plot** shows how few components capture most signal:

```plot
{"title": "Cumulative variance explained vs components", "xLabel": "number of components", "yLabel": "cumulative variance explained", "xRange": [0, 20], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1 - exp(-0.3*x)", "label": "first PCs capture most variance", "color": "#2563eb"}]}
```

**Next:** selecting features without fooling yourself.
""",
        ),
        _t(
            "Feature selection without leakage",
            "11 min",
            r"""
# Feature selection without leakage

With thousands of genes, reducing to a predictive subset improves
interpretability and generalisation. Three strategies exist: **filter** methods
rank features by a univariate statistic (e.g. t-test, mutual information);
**wrapper** methods (recursive feature elimination) search subsets by model
performance; and **embedded** methods (lasso, tree importance) select during
fitting.

```mermaid
flowchart LR
  GENES["All features"] --> FILTER["Filter: univariate stats"]
  GENES --> WRAP["Wrapper: search with model"]
  GENES --> EMB["Embedded: lasso / tree importance"]
  FILTER --> PANEL["Selected panel"]
  WRAP --> PANEL
  EMB --> PANEL
```

The cardinal sin is **selection leakage**: choosing features using the whole
dataset (including test samples) before cross-validation. This can make pure
noise look highly predictive. Feature selection must sit **inside** the CV loop,
re-run on each training fold. As the number of features screened grows, the
expected best-by-chance correlation rises, so without correction false discovery
is almost guaranteed:

```plot
{"title": "Best chance correlation vs features screened", "xLabel": "features screened (thousands)", "yLabel": "max spurious correlation", "xRange": [0, 20], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+4)", "label": "rises with screening", "color": "#dc2626"}]}
```

Always validate a selected panel on truly independent data.

**Next:** test your command of the core methods.
""",
        ),
        _quiz(),
    ),
)


# -- ML for Life Sciences -- Advanced ------------------------------------------

_ADVANCED = SeedCourse(
    slug="ml-life-sciences-advanced",
    title="Machine Learning for Life Sciences — Advanced",
    description=(
        "State-of-the-art and applied ML in biology: handling imbalanced and "
        "noisy clinical data, deep learning for sequences and images, transfer "
        "learning and foundation models (ESM, scGPT, AlphaFold), model "
        "interpretability (SHAP, attention, saliency), calibration and "
        "uncertainty for clinical decisions, and the reproducibility and bias "
        "pitfalls that undermine ML in the life sciences. Includes interactive "
        "plots of class imbalance, learning curves and calibration."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Imbalanced and noisy data in biology",
            "13 min",
            r"""
# Imbalanced and noisy data in biology

Biological labels are often **imbalanced** (rare disease, few responders) and
**noisy** (ambiguous diagnoses, label errors). A model that always predicts the
majority class can score 99% accuracy yet be useless — so accuracy is the wrong
metric and AUPRC, recall and balanced accuracy are preferred.

Remedies operate at the data or loss level: **resampling** (SMOTE oversamples the
minority by interpolation; random undersampling thins the majority),
**class-weighting** the loss so minority errors cost more, and **threshold
tuning** to the operating point that matters clinically.

```mermaid
flowchart LR
  IMB["Imbalanced labels"] --> RES["Resample: SMOTE / undersample"]
  IMB --> WEIGHT["Class-weighted loss"]
  IMB --> THRESH["Tune decision threshold"]
  RES --> EVAL["Evaluate with AUPRC / recall"]
  WEIGHT --> EVAL
  THRESH --> EVAL
```

The danger of relying on accuracy grows with imbalance: as the minority fraction
shrinks, a trivial majority classifier's accuracy climbs toward 1, masking total
failure on the class of interest.

```plot
{"title": "Majority-class accuracy vs minority fraction", "xLabel": "minority fraction (%)", "yLabel": "trivial-classifier accuracy", "xRange": [0, 50], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1 - x/100", "label": "accuracy misleads when rare", "color": "#dc2626"}]}
```

Resampling must be done **inside** CV folds to avoid leakage.

**Next:** deep learning for sequences and images.
""",
        ),
        _t(
            "Deep learning for sequences and images",
            "13 min",
            r"""
# Deep learning for sequences and images

When features are hard to hand-craft, **deep neural networks** learn them.
**Convolutional neural networks (CNNs)** excel on regular grids — histopathology
slides, microscopy, and DNA read as a 1D sequence (DeepBind, Basset predict
transcription-factor binding). **Recurrent networks and transformers** model
order in sequences; **transformers** with self-attention now dominate protein and
genomic modelling (Enformer for regulatory activity).

```mermaid
flowchart LR
  INPUT["Sequence / image"] --> LAYERS["Stacked layers learn features"]
  LAYERS --> REP["Learned representation"]
  REP --> HEAD["Task head"]
  HEAD --> OUT["Prediction"]
  OUT --> BP["Backprop updates weights"]
  BP --> LAYERS
```

Training minimises a loss by **stochastic gradient descent** with
backpropagation. Deep models are data-hungry and prone to overfitting, mitigated
by **dropout**, **batch normalisation**, weight decay and **data augmentation**
(rotations/flips for images). Validation loss typically falls then rises as the
network starts memorising — **early stopping** halts at the minimum:

```plot
{"title": "Validation loss vs training epochs (early stopping)", "xLabel": "training epoch", "yLabel": "validation loss", "xRange": [0, 20], "yRange": [0, 2], "grid": true, "functions": [{"expr": "0.3 + 0.05*(x-8)^2/3", "label": "stop at the minimum", "color": "#2563eb"}]}
```

**Next:** reusing pretrained knowledge with transfer learning.
""",
        ),
        _t(
            "Transfer learning and foundation models",
            "12 min",
            r"""
# Transfer learning and foundation models

Labelled biological data is scarce, but unlabelled data (billions of protein
sequences, millions of cells) is abundant. **Self-supervised** pretraining learns
general representations from unlabelled data; **transfer learning** then
fine-tunes them on a small labelled task.

**Foundation models** scale this idea: **ESM** and protein language models learn
from sequence databases and predict structure, function and the effect of
mutations; **scGPT** and **Geneformer** pretrain on tens of millions of single
cells; **AlphaFold** leverages evolutionary couplings for structure. Downstream,
a tiny labelled set can reach high accuracy by standing on these representations.

```mermaid
flowchart LR
  BIG["Massive unlabelled data"] --> PRE["Self-supervised pretraining"]
  PRE --> FM["Foundation model (ESM / scGPT)"]
  FM --> FT["Fine-tune on small labelled task"]
  FT --> APP["Application: function, effect, cell type"]
```

The payoff is sample efficiency: a fine-tuned foundation model reaches good
accuracy with far fewer labels than training from scratch, with accuracy rising
steeply at first then saturating as labels accumulate:

```plot
{"title": "Accuracy vs labelled examples (fine-tuning)", "xLabel": "labelled examples (relative)", "yLabel": "accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "high accuracy from few labels", "color": "#16a34a"}]}
```

Still, distribution shift between pretraining and clinical data demands careful
validation.

**Next:** opening the black box with interpretability.
""",
        ),
        _t(
            "Interpretability: SHAP, attention and saliency",
            "12 min",
            r"""
# Interpretability: SHAP, attention and saliency

In biology a prediction is rarely enough — we must know *why*, both for trust and
to generate hypotheses. **Interpretability** methods explain model behaviour.

**Global** methods describe the whole model (permutation importance, partial
dependence). **Local** methods explain one prediction: **LIME** fits a simple
surrogate around an example, and **SHAP** assigns each feature a contribution
based on cooperative game theory (Shapley values), with the appealing property
that contributions sum to the prediction. For deep models, **saliency maps** and
**Grad-CAM** highlight influential pixels or bases, and **attention** weights
suggest which positions a transformer focused on.

```mermaid
flowchart TB
  MODEL["Trained model"] --> GLOBAL["Global: permutation importance, PDP"]
  MODEL --> LOCAL["Local: SHAP, LIME"]
  MODEL --> DEEP["Deep: saliency, Grad-CAM, attention"]
  GLOBAL --> HYP["Hypotheses & trust"]
  LOCAL --> HYP
  DEEP --> HYP
```

A caution: feature importance signals **association, not causation**, and
attention is not a faithful explanation. As a model grows more complex,
faithfully explaining it gets harder — the interpretability-accuracy tension:

```plot
{"title": "Explanation fidelity vs model complexity", "xLabel": "model complexity", "yLabel": "explanation fidelity", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.25*x)", "label": "harder to explain as it grows", "color": "#dc2626"}]}
```

**Next:** calibration and uncertainty for decisions.
""",
        ),
        _t(
            "Calibration and uncertainty for clinical decisions",
            "12 min",
            r"""
# Calibration and uncertainty for clinical decisions

A clinical model's probabilities must be **calibrated**: among patients given a
risk of 0.8, about 80% should truly have the outcome. A model can rank well
(high AUROC) yet be badly calibrated and so dangerous for decisions.

Calibration is assessed with a **reliability diagram** (predicted vs observed
frequency) and summarised by the **Brier score**, the mean squared error of
probabilities. Miscalibration is corrected post hoc by **Platt scaling**
(logistic) or **isotonic regression**. Modern deep nets are often overconfident,
fixed cheaply by **temperature scaling**.

```mermaid
flowchart LR
  SCORES["Model probabilities"] --> REL["Reliability diagram"]
  REL --> BRIER["Brier score"]
  BRIER --> CAL["Recalibrate: Platt / isotonic / temperature"]
  CAL --> DECIDE["Trustworthy clinical decision"]
```

A perfectly calibrated model lies on the diagonal (predicted = observed);
overconfident models bow below it. Beyond point predictions, **uncertainty
quantification** (Bayesian methods, deep ensembles, **conformal prediction**)
gives prediction *intervals* and flags out-of-distribution inputs where the model
should abstain.

```plot
{"title": "Reliability diagram: perfect calibration is the diagonal", "xLabel": "predicted probability", "yLabel": "observed frequency", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x", "label": "ideal: observed = predicted", "color": "#2563eb"}]}
```

**Next:** the reproducibility and bias pitfalls of ML in biology.
""",
        ),
        _t(
            "Pitfalls: reproducibility, bias and validation",
            "13 min",
            r"""
# Pitfalls: reproducibility, bias and validation

Many published biomedical ML results fail to replicate. The recurring causes are
avoidable. **Data leakage** — features that encode the label, or preprocessing
before splitting — is the most common and inflates accuracy spectacularly.
**Batch effects** let a model learn the scanner or sequencing centre instead of
biology; the fix is to split by **batch/site** and adjust for confounders.

```mermaid
flowchart TB
  PIT["ML pitfalls in biology"] --> LEAK["Data leakage"]
  PIT --> BATCH["Batch / site confounding"]
  PIT --> SMALL["Tiny samples, no external test"]
  PIT --> SUBGROUP["Unequal subgroup performance"]
  LEAK --> FIX["External validation, leakage audits"]
  BATCH --> FIX
  SMALL --> FIX
  SUBGROUP --> FIX
```

**Dataset bias** harms fairness: a model trained on one population may
underperform on under-represented groups, so report **subgroup metrics**.
Reproducibility demands versioned data and code, fixed random seeds, reporting
checklists (TRIPOD-AI, CLAIM) and, above all, **external validation** on an
independent cohort. Optimistic single-cohort estimates regress toward reality
when tested externally — the gap is the price of every shortcut taken:

```plot
{"title": "Performance gap grows with shortcuts taken", "xLabel": "number of methodological shortcuts", "yLabel": "internal-minus-external AUROC gap", "xRange": [0, 6], "yRange": [0, 0.5], "grid": true, "functions": [{"expr": "0.45*(1 - exp(-0.6*x))", "label": "optimism vs reality", "color": "#dc2626"}]}
```

**Next:** test your command of state-of-the-art ML in biology.
""",
        ),
        _quiz(),
    ),
)


ML_LIFE_SCIENCES_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["ML_LIFE_SCIENCES_COURSES"]
