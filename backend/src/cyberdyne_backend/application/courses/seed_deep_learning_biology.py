"""Deep Learning for Biology track: Basics -> Intermediate -> Advanced.

A university-level path from neural-network fundamentals and training, through
the core architectures (CNNs, RNNs, attention and transformers), to the modern
state of the art for biology (graph neural networks for molecules, protein and
nucleotide language models, and structure prediction). Lessons use interactive
```plot blocks for quantitative relationships (activations, losses, learning
curves) and ```mermaid diagrams for architectures, pipelines and data flow.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Deep Learning for Biology -- Basics ---------------------------------------

_BASICS = SeedCourse(
    slug="deep-learning-biology-basics",
    title="Deep Learning for Biology — Basics",
    description=(
        "Why deep learning matters for biology and how a neural network actually "
        "works: the artificial neuron, activation functions, forward propagation, "
        "loss functions, gradient descent and backpropagation. Built on concrete "
        "biological examples (gene expression, sequence classification) with "
        "interactive plots and architecture diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why deep learning for biology",
            "10 min",
            r"""
# Why deep learning for biology

Biology became a data science. A single experiment can yield millions of
sequencing reads, thousands of single-cell expression profiles or terabytes of
microscopy. **Deep learning** — neural networks with many layers — excels when
the mapping from raw data to the answer is complex, non-linear and hard to
hand-code, which describes most biological problems.

Classical methods need humans to design features (e.g. GC content, motif
counts). Deep networks instead **learn representations** directly from data: a
model trained on millions of protein sequences discovers contacts and folds no
one programmed in.

```mermaid
flowchart LR
  RAW["Raw biology: sequences, images, expression"] --> NET["Deep network: learned features"]
  NET --> TASK["Task: classify, predict, generate"]
  TASK --> BIO["Biological insight"]
```

Landmark results — AlphaFold for protein structure, deep variant callers,
single-cell embeddings — share one ingredient: large labelled or self-supervised
datasets feeding flexible models. The trade-off is that networks are
data-hungry and can overfit, so understanding training is essential.

A recurring theme is the **dose-response sigmoid**, which also describes a
neuron's saturating output:

```plot
{"title": "Sigmoid response", "xLabel": "input", "yLabel": "output", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "sigmoid", "color": "#2563eb"}]}
```

**Next:** the artificial neuron.
""",
        ),
        _t(
            "The artificial neuron",
            "11 min",
            r"""
# The artificial neuron

A neuron computes a weighted sum of its inputs, adds a bias, then applies a
non-linear **activation**. For inputs $x_1,\dots,x_n$ with weights $w_i$ and
bias $b$:

$$z=\sum_{i=1}^{n} w_i x_i + b, \qquad a=\sigma(z)$$

The weights are what the network learns. Loosely inspired by biological
neurons, the artificial neuron is a mathematical abstraction, not a faithful
model of a cell.

```mermaid
flowchart LR
  X1["x1"] --> S["sum w*x + b"]
  X2["x2"] --> S
  X3["x3"] --> S
  S --> A["activation sigma(z)"]
  A --> O["output a"]
```

Without the non-linearity, stacking neurons would collapse to a single linear
map — no matter how many layers. The activation gives the network its power to
approximate arbitrary functions (the universal approximation theorem). A common
choice is the sigmoid $\sigma(z)=\frac{1}{1+e^{-z}}$, which squashes any real
number into $(0,1)$ and is interpretable as a probability — useful when, say,
predicting whether a DNA window contains a promoter.

```plot
{"title": "Neuron activation (sigmoid)", "xLabel": "z", "yLabel": "a", "xRange": [-6,6], "yRange": [0,1], "grid": true, "functions": [{"expr": "1/(1+exp(-x))", "label": "sigma(z)", "color": "#2563eb"}]}
```

**Next:** stacking neurons into layers.
""",
        ),
        _t(
            "Layers, depth and forward propagation",
            "11 min",
            r"""
# Layers, depth and forward propagation

A **layer** is a set of neurons sharing the same inputs. Stack layers and the
output of one becomes the input of the next — a **multilayer perceptron**
(MLP). Computing the output for an input is **forward propagation**: each layer
applies a matrix multiply plus bias, then an activation.

$$h^{(1)}=\sigma(W^{(1)}x+b^{(1)}), \quad h^{(2)}=\sigma(W^{(2)}h^{(1)}+b^{(2)})$$

```mermaid
flowchart LR
  IN["Input layer"] --> H1["Hidden layer 1"]
  H1 --> H2["Hidden layer 2"]
  H2 --> OUT["Output layer"]
```

**Depth** (number of layers) lets the network build features hierarchically:
early layers detect simple patterns (a single nucleotide motif), later layers
combine them (a regulatory element). For a gene-expression classifier, the
input might be 20000 gene values and the output a tissue-type probability.

The modern default activation is **ReLU**, $\max(0,z)$, which is cheap and
avoids the vanishing gradients that plague saturating sigmoids in deep stacks.
Its positive branch grows linearly:

```plot
{"title": "ReLU activation", "xLabel": "z", "yLabel": "output", "xRange": [-4,4], "yRange": [0,4], "grid": true, "functions": [{"expr": "(abs(x)+x)/2", "label": "ReLU(z)", "color": "#16a34a"}]}
```

**Next:** measuring error with a loss function.
""",
        ),
        _t(
            "Loss functions and what we optimise",
            "10 min",
            r"""
# Loss functions and what we optimise

Training means adjusting weights to make predictions match labels. A **loss
function** quantifies the mismatch on a given example; we minimise its average
over the dataset.

For regression (e.g. predicting a continuous expression level), the **mean
squared error** is standard:

$$L=\frac{1}{N}\sum_{i=1}^{N}(y_i-\hat y_i)^2$$

For classification (e.g. pathogenic vs benign variant), we use **cross-entropy**.
For a binary label with predicted probability $\hat y$:

$$L=-\big[y\log \hat y + (1-y)\log(1-\hat y)\big]$$

Cross-entropy punishes confident wrong predictions sharply: as $\hat y \to 0$
while the truth is 1, the loss diverges.

```mermaid
flowchart LR
  PRED["Prediction y_hat"] --> LOSS["Loss L(y, y_hat)"]
  TRUE["Label y"] --> LOSS
  LOSS --> OPT["Minimise over weights"]
```

The shape of the loss as a prediction deviates from the truth shows why errors
are penalised non-linearly:

```plot
{"title": "Squared-error loss", "xLabel": "prediction", "yLabel": "loss", "xRange": [-3,3], "yRange": [0,9], "grid": true, "functions": [{"expr": "x^2", "label": "(y - y_hat)^2 at y=0", "color": "#dc2626"}]}
```

**Next:** how gradient descent moves downhill.
""",
        ),
        _t(
            "Gradient descent and learning rate",
            "11 min",
            r"""
# Gradient descent and learning rate

We minimise the loss by **gradient descent**: compute the gradient (slope) of
the loss with respect to each weight, then step in the opposite direction.

$$w \leftarrow w - \eta \frac{\partial L}{\partial w}$$

The **learning rate** $\eta$ controls step size. Too small and training crawls;
too large and it overshoots or diverges. In practice we use **mini-batch
stochastic gradient descent**: estimate the gradient on a small random batch,
which is faster and adds helpful noise that can escape poor minima.

```mermaid
flowchart LR
  BATCH["Sample mini-batch"] --> GRAD["Compute gradient"]
  GRAD --> STEP["Update weights w - eta*grad"]
  STEP --> BATCH
```

Think of the loss surface as a valley: descent rolls a ball toward the bottom.
A simple convex bowl shows the idea — the gradient is large far from the minimum
and vanishes at it:

```plot
{"title": "Loss landscape (1D)", "xLabel": "weight", "yLabel": "loss", "xRange": [-4,4], "yRange": [0,8], "grid": true, "functions": [{"expr": "0.5*x^2", "label": "loss", "color": "#2563eb"}]}
```

Optimisers like **Adam** improve on plain SGD by adapting per-parameter step
sizes and using momentum, which speeds convergence on the noisy, high-curvature
landscapes typical of biological data.

**Next:** backpropagation, the engine behind the gradients.
""",
        ),
        _t(
            "Backpropagation and overfitting",
            "11 min",
            r"""
# Backpropagation and overfitting

**Backpropagation** computes every weight's gradient efficiently using the
chain rule, propagating the error from the output back through each layer. It
reuses intermediate results from the forward pass, so the cost is comparable to
one forward pass rather than separately perturbing each weight.

```mermaid
flowchart LR
  FWD["Forward pass: compute output & loss"] --> BWD["Backward pass: chain-rule gradients"]
  BWD --> UPD["Update all weights"]
```

A trained network must **generalise** to new data, not memorise the training
set. **Overfitting** — low training loss but high validation loss — is the
central danger, especially with the small, noisy datasets common in biology.

Defences include holding out a **validation set**, **early stopping**,
**dropout** (randomly zeroing units during training), **weight decay** (L2
regularisation) and data augmentation. The hallmark of overfitting is the gap
that opens between training and validation error as training continues:

```plot
{"title": "Overfitting: validation error rebounds", "xLabel": "training epoch", "yLabel": "validation error", "xRange": [0,10], "yRange": [0,2], "grid": true, "functions": [{"expr": "exp(-0.5*x) + 0.05*x^2", "label": "val error", "color": "#dc2626"}]}
```

Watch this curve: the minimum marks where to stop. Together, backpropagation
plus regularisation are the foundation every architecture in the next courses
builds on.

**Next:** convolutional networks for sequence and image data.
""",
        ),
        _quiz(),
    ),
)


# -- Deep Learning for Biology -- Intermediate ---------------------------------

_INTERMEDIATE = SeedCourse(
    slug="deep-learning-biology-intermediate",
    title="Deep Learning for Biology — Intermediate",
    description=(
        "The core architectures that power biological deep learning: "
        "convolutional networks for sequences and images, recurrent networks for "
        "ordered data, the attention mechanism, the transformer, and embeddings "
        "for representing biological tokens. Quantitative and practical, with "
        "interactive plots and architecture diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Convolutional networks for sequences and images",
            "12 min",
            r"""
# Convolutional networks for sequences and images

A **convolutional neural network** (CNN) slides small learnable filters across
the input, detecting local patterns regardless of position — **translation
invariance**. In genomics, a 1D convolution over a one-hot encoded DNA sequence
learns motifs (e.g. transcription-factor binding sites); in microscopy, 2D
convolutions learn edges then textures then structures.

A convolution computes, for each position, a dot product between the filter and
the local window, producing a **feature map**. **Pooling** then downsamples,
giving robustness and reducing computation.

```mermaid
flowchart LR
  SEQ["One-hot DNA / image"] --> CONV["Conv filters -> feature maps"]
  CONV --> POOL["Pooling"]
  POOL --> CONV2["More conv layers"]
  CONV2 --> FC["Dense layers -> prediction"]
```

CNNs are parameter-efficient: a filter of width 12 over a 4-channel DNA input
has only 48 weights yet scans the whole sequence. Tools like **DeepBind** and
**Basset** used CNNs to predict protein-DNA binding and chromatin
accessibility, often recovering known motifs in their first-layer filters.

A learned motif acts like a saturating detector — once a strong match is found,
the activation plateaus:

```plot
{"title": "Motif detector saturation", "xLabel": "match strength", "yLabel": "activation", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "activation", "color": "#16a34a"}]}
```

**Next:** recurrent networks for ordered data.
""",
        ),
        _t(
            "Recurrent networks and sequence memory",
            "12 min",
            r"""
# Recurrent networks and sequence memory

A **recurrent neural network** (RNN) processes a sequence one element at a time,
maintaining a **hidden state** that carries information forward:

$$h_t=\sigma(W_x x_t + W_h h_{t-1} + b)$$

This makes RNNs natural for ordered biological data — nucleotide or amino-acid
sequences, time-course expression, or electrophysiology traces — where context
from earlier positions matters.

```mermaid
flowchart LR
  X1["x_t-1"] --> H1["h_t-1"]
  H1 --> H2["h_t"]
  X2["x_t"] --> H2
  H2 --> H3["h_t+1"]
  X3["x_t+1"] --> H3
```

Plain RNNs struggle with **long-range dependencies**: gradients shrink (or
explode) as they propagate back through many time steps. The **LSTM** and
**GRU** add gates that learn what to keep, forget and output, preserving signal
across long sequences — essential for proteins where distant residues interact.

The vanishing-gradient problem means influence of an early input decays with
distance, motivating gated memory:

```plot
{"title": "Vanishing gradient with sequence length", "xLabel": "steps back in time", "yLabel": "gradient magnitude", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "|gradient|", "color": "#dc2626"}]}
```

**Next:** attention, which lets a model look anywhere at once.
""",
        ),
        _t(
            "The attention mechanism",
            "12 min",
            r"""
# The attention mechanism

**Attention** lets a model weigh all positions of a sequence directly, rather
than passing information step by step. Each position emits a **query**, **key**
and **value**; the output at a position is a weighted average of all values,
where the weights come from how well its query matches each key.

$$\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V$$

The $\sqrt{d_k}$ scaling keeps the dot products from growing too large and
saturating the softmax. Attention solves the long-range problem cheaply in
sequence length per layer: any two residues can interact in a single step.

```mermaid
flowchart LR
  Q["Query"] --> SCORE["Q . K scores"]
  K["Keys"] --> SCORE
  SCORE --> SM["softmax weights"]
  V["Values"] --> OUT["weighted sum"]
  SM --> OUT
```

In proteins, attention maps often align with **residue contacts** in the folded
structure — the model learns which positions co-vary. The softmax that produces
attention weights sharpens differences between scores:

```plot
{"title": "Softmax weight vs relative score", "xLabel": "score gap", "yLabel": "attention weight", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "weight", "color": "#2563eb"}]}
```

**Next:** assembling attention into the transformer.
""",
        ),
        _t(
            "Transformers and self-attention blocks",
            "12 min",
            r"""
# Transformers and self-attention blocks

The **transformer** stacks blocks of **multi-head self-attention** and
position-wise feed-forward layers, glued by residual connections and layer
normalisation. Multiple heads let the model attend to different relationships
simultaneously (e.g. one head tracks secondary structure, another tracks
hydrophobic contacts).

```mermaid
flowchart TB
  IN["Token + positional embeddings"] --> MHA["Multi-head self-attention"]
  MHA --> ADD1["Add & norm"]
  ADD1 --> FF["Feed-forward"]
  FF --> ADD2["Add & norm"]
  ADD2 --> OUT["Block output (repeat N times)"]
```

Because attention is order-agnostic, transformers add **positional encodings**
so the model knows residue order. Residual connections let gradients flow
through deep stacks, enabling models with dozens of layers and billions of
parameters.

Transformers underpin modern biology: protein language models (ESM, ProtTrans),
nucleotide models (DNABERT, the Nucleotide Transformer) and the Evoformer in
AlphaFold2. Their compute per layer scales with the **square** of sequence
length, which motivates efficient-attention variants for long genomes:

```plot
{"title": "Self-attention cost vs sequence length", "xLabel": "sequence length", "yLabel": "relative compute", "xRange": [0,10], "yRange": [0,100], "grid": true, "functions": [{"expr": "x^2", "label": "O(L^2)", "color": "#dc2626"}]}
```

**Next:** turning biological tokens into embeddings.
""",
        ),
        _t(
            "Embeddings and representing biology as vectors",
            "11 min",
            r"""
# Embeddings and representing biology as vectors

Networks operate on numbers, so we must encode biology. **One-hot** encoding
maps each of the 4 nucleotides or 20 amino acids to a sparse vector — simple but
high-dimensional and ignorant of similarity. An **embedding** layer instead maps
each token to a learned dense vector, so chemically similar amino acids end up
near each other in vector space.

```mermaid
flowchart LR
  TOK["Token: amino acid"] --> LOOKUP["Embedding lookup table"]
  LOOKUP --> VEC["Dense vector (e.g. 128-d)"]
  VEC --> NET["Downstream network"]
```

Embeddings are central to representation learning: a protein language model
produces a per-residue embedding that encodes structure and function, usable for
contact prediction, mutation-effect scoring or as features for a small
classifier — **transfer learning**. Single-cell methods embed cells so that
cell types cluster.

Distances in embedding space carry meaning; similarity between two vectors
typically rises smoothly as they align (e.g. cosine similarity), behaving like a
saturating curve as overlap grows:

```plot
{"title": "Embedding similarity vs overlap", "xLabel": "shared features", "yLabel": "similarity", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "similarity", "color": "#16a34a"}]}
```

**Next:** graph neural networks and biological language models.
""",
        ),
        _quiz(),
    ),
)


# -- Deep Learning for Biology -- Advanced -------------------------------------

_ADVANCED = SeedCourse(
    slug="deep-learning-biology-advanced",
    title="Deep Learning for Biology — Advanced",
    description=(
        "The state of the art applied to biology: graph neural networks for "
        "molecules and interaction networks, protein and nucleotide language "
        "models, structure prediction with AlphaFold, generative models for "
        "molecular design, and the practicalities of training, evaluating and "
        "trusting these models. Interactive plots and architecture diagrams "
        "throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Graph neural networks for molecules",
            "13 min",
            r"""
# Graph neural networks for molecules

Many biological objects are naturally **graphs**: a molecule is atoms (nodes)
joined by bonds (edges); a protein-protein interaction network and a metabolic
pathway are graphs too. A **graph neural network** (GNN) learns by **message
passing** — each node updates its representation by aggregating messages from
its neighbours:

$$h_v^{(k+1)}=\phi\!\Big(h_v^{(k)},\ \textstyle\sum_{u\in N(v)} \psi(h_u^{(k)})\Big)$$

After $k$ rounds, a node "sees" its $k$-hop neighbourhood. GNNs respect
**permutation invariance**: the prediction does not depend on arbitrary atom
ordering.

```mermaid
flowchart LR
  GRAPH["Molecular graph: atoms + bonds"] --> MP["Message passing layers"]
  MP --> POOL["Readout / pooling"]
  POOL --> PRED["Property: solubility, toxicity, binding"]
```

GNNs power molecular property prediction (MoleculeNet), drug-target interaction
and the antibiotic discovery work that found halicin. Adding more message-passing
layers grows the receptive field but risks **over-smoothing**, where node
representations converge and become indistinguishable:

```plot
{"title": "Over-smoothing with depth", "xLabel": "message-passing layers", "yLabel": "node distinctiveness", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "distinctiveness", "color": "#dc2626"}]}
```

**Next:** protein language models.
""",
        ),
        _t(
            "Protein language models",
            "13 min",
            r"""
# Protein language models

A **protein language model** (pLM) treats amino-acid sequences like text and
trains on hundreds of millions of natural proteins with a self-supervised
objective: **masked language modelling**, hiding residues and predicting them
from context. To do this well, the model must internalise the constraints of
evolution and biophysics.

```mermaid
flowchart LR
  SEQ["Protein sequences (UniProt)"] --> MASK["Mask residues"]
  MASK --> TF["Transformer encoder"]
  TF --> PRED["Predict masked residues"]
  TF --> EMB["Reusable embeddings"]
```

Models such as **ESM-2** and **ProtTrans** yield embeddings that, with little or
no fine-tuning, predict secondary structure, residue contacts, subcellular
localisation and **variant effects**. ESMFold even predicts 3D structure from a
single sequence using the language model alone — fast, though less accurate than
MSA-based methods.

A key empirical finding is **scaling**: prediction quality improves smoothly
(roughly log-linearly) as model size and data grow, mirroring scaling laws in
NLP. Performance rises with scale but with diminishing returns:

```plot
{"title": "Scaling: capability vs model size", "xLabel": "log model size", "yLabel": "capability", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "capability", "color": "#2563eb"}]}
```

**Next:** predicting 3D structure with AlphaFold.
""",
        ),
        _t(
            "Structure prediction with AlphaFold",
            "13 min",
            r"""
# Structure prediction with AlphaFold

**AlphaFold2** solved a 50-year grand challenge: predicting a protein's 3D fold
from its sequence at near-experimental accuracy. It combines a **multiple
sequence alignment** (capturing evolutionary co-variation that signals contacts)
with the **Evoformer**, a transformer that jointly reasons over the MSA and a
pairwise residue representation, then a **structure module** that outputs 3D
coordinates end to end.

```mermaid
flowchart LR
  SEQ["Query sequence"] --> MSA["MSA + templates"]
  MSA --> EVO["Evoformer (attention over MSA & pairs)"]
  EVO --> STRUCT["Structure module -> 3D coords"]
  STRUCT --> PLDDT["Per-residue confidence (pLDDT)"]
```

AlphaFold reports a per-residue confidence, **pLDDT** (0–100); high values mark
well-determined regions, low values often flag intrinsic disorder. The AlphaFold
DB released predicted structures for nearly all known proteins, transforming
structural biology. **AlphaFold-Multimer** and **AlphaFold3** extend this to
complexes and to ligands, nucleic acids and modified residues.

Prediction accuracy climbs steeply with the depth of the evolutionary alignment,
then saturates — more homologues help, up to a point:

```plot
{"title": "Accuracy vs MSA depth", "xLabel": "number of homologues (log)", "yLabel": "structure accuracy", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "accuracy", "color": "#16a34a"}]}
```

**Next:** generative models for molecular design.
""",
        ),
        _t(
            "Generative models for molecular design",
            "13 min",
            r"""
# Generative models for molecular design

**Generative models** create new biological entities rather than just classify
them. Variational autoencoders (VAEs) and, more recently, **diffusion models**
learn the distribution of valid molecules or protein structures, then sample
novel candidates with desired properties — accelerating drug and enzyme design.

A diffusion model learns to **denoise**: it is trained to reverse a process that
gradually adds Gaussian noise, so at inference it turns noise into a structured
sample step by step.

```mermaid
flowchart LR
  NOISE["Random noise"] --> DENOISE["Iterative denoising network"]
  DENOISE --> MOL["Generated molecule / structure"]
  MOL --> SCORE["Score: validity, affinity, novelty"]
  SCORE --> DENOISE
```

**RFdiffusion** designs proteins by diffusion over backbone coordinates, and
**ProteinMPNN** then designs sequences that fold to a target backbone — together
producing novel binders validated in the lab. For small molecules, generative
models paired with property predictors enable goal-directed design.

The denoising trajectory removes noise progressively across sampling steps, so
sample quality improves as noise decays:

```plot
{"title": "Diffusion: noise removed over steps", "xLabel": "denoising step", "yLabel": "remaining noise", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "noise level", "color": "#dc2626"}]}
```

**Next:** training, evaluating and trusting models on biological data.
""",
        ),
        _t(
            "Training, evaluation and trust in biological models",
            "12 min",
            r"""
# Training, evaluation and trust in biological models

State-of-the-art models are only useful if rigorously trained and honestly
evaluated. Biological data has pitfalls: **data leakage** (highly similar
sequences in train and test inflate scores), severe class imbalance (few
pathogenic variants), and batch effects.

The fix is principled splitting. For proteins, cluster by sequence identity and
split **between** clusters; for variants, split by gene or genomic region. Report
metrics matched to the task: **AUROC** and **AUPRC** for imbalanced
classification, Spearman correlation for effect prediction, and report
confidence intervals.

```mermaid
flowchart LR
  DATA["Biological dataset"] --> CLUST["Cluster by similarity"]
  CLUST --> SPLIT["Leakage-free train / val / test"]
  SPLIT --> TRAIN["Train + tune"]
  TRAIN --> EVAL["Task-matched metrics + calibration"]
```

**Calibration** matters in biology: a model that says "90% pathogenic" should be
right about 90% of the time, since clinicians may act on it. **Interpretability**
tools (attention maps, saliency, integrated gradients) help connect predictions
to mechanism. A reliable model's confidence tracks its accuracy — a calibration
curve should hug the diagonal:

```plot
{"title": "Calibration: predicted vs observed", "xLabel": "predicted probability", "yLabel": "observed frequency", "xRange": [0,1], "yRange": [0,1], "grid": true, "functions": [{"expr": "x", "label": "perfectly calibrated", "color": "#2563eb"}]}
```

**Next:** apply these methods to your own biological problem.
""",
        ),
        _quiz(),
    ),
)


DEEP_LEARNING_BIOLOGY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["DEEP_LEARNING_BIOLOGY_COURSES"]
