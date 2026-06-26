"""Generative Models for Molecular Design track: Basics -> Intermediate -> Advanced.

A university-level path from molecular representations and what generative
design means, through the core deep generative methods (VAEs, GANs, normalizing
flows, autoregressive models and reinforcement learning), to state-of-the-art
diffusion and flow-matching models, structure-conditioned (pocket-aware) design
and multi-objective optimization. Lessons use interactive ```plot blocks for
quantitative relationships (loss landscapes, reward shaping, noise schedules,
property distributions) and ```mermaid diagrams for pipelines, model families
and design loops.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Generative Molecular Design -- Basics ------------------------------------

_BASICS = SeedCourse(
    slug="generative-molecular-design-basics",
    title="Generative Models for Molecular Design — Basics",
    description=(
        "What molecular generative design is and why it matters for drug "
        "discovery and materials. How molecules are represented for machine "
        "learning (SMILES, graphs, fingerprints), what makes chemical space so "
        "vast, how we score and validate generated molecules, and the intuition "
        "behind learning a distribution over molecules. Built on real "
        "cheminformatics detail with interactive plots and pipeline diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is generative molecular design",
            "10 min",
            r"""
# What is generative molecular design

**Generative molecular design** uses machine-learning models that *propose new
molecules* rather than only screen existing ones. Classical **virtual
screening** ranks a fixed library; a generative model instead learns a
distribution $p(x)$ over valid molecules and **samples** novel candidates,
optionally biased toward desired properties.

The motivation is the size of chemical space. The number of small,
drug-like organic molecules is estimated near $10^{60}$ — far beyond any
library we could enumerate or test. We need models that explore this space
intelligently.

```mermaid
flowchart LR
  DATA["Known molecules (ChEMBL, ZINC)"] --> MODEL["Generative model learns p(x)"]
  MODEL --> SAMPLE["Sample novel candidates"]
  SAMPLE --> SCORE["Score: validity, drug-likeness, activity"]
  SCORE -->|feedback| MODEL
  SCORE --> SYN["Synthesize & test best hits"]
```

A useful mental picture: the achievable goodness of a campaign rises steeply as
the model learns chemistry, then saturates once it captures the data
distribution — further gains require better objectives or data.

```plot
{"title": "Design quality vs model training", "xLabel": "training effort", "yLabel": "fraction useful candidates", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "useful fraction", "color": "#2563eb"}]}
```

The promise: faster hit discovery, novel scaffolds outside patented space, and
designs steered toward potency, solubility and synthesizability at once.

**Next:** how we turn a molecule into something a model can read.
""",
        ),
        _t(
            "Molecular representations: SMILES, graphs and fingerprints",
            "12 min",
            r"""
# Molecular representations: SMILES, graphs and fingerprints

A model cannot read a molecule directly — it needs a **representation**. Three
dominate generative chemistry.

**SMILES** (Simplified Molecular-Input Line-Entry System) encodes a molecule as
a string, e.g. ethanol is `CCO` and aspirin is
`CC(=O)Oc1ccccc1C(=O)O`. Strings let us reuse sequence models (RNNs,
Transformers), but most random strings are invalid, and one molecule has many
SMILES unless **canonicalized**. **SELFIES** is a newer string grammar where
*every* string decodes to a valid molecule.

**Molecular graphs** treat atoms as nodes and bonds as edges — the natural,
permutation-invariant structure handled by **graph neural networks (GNNs)**.

**Fingerprints** (e.g. ECFP/Morgan) are fixed-length bit vectors encoding
substructures; great for similarity and as fixed inputs, but not directly
generative.

```mermaid
flowchart TB
  MOL["Molecule"] --> S["SMILES / SELFIES string"]
  MOL --> G["Graph: atoms + bonds"]
  MOL --> F["Fingerprint: bit vector"]
  S --> SEQ["Sequence models"]
  G --> GNN["Graph models"]
  F --> SIM["Similarity & QSAR"]
```

Tools like **RDKit** parse, canonicalize and validate these representations and
compute the fingerprints used everywhere downstream.

```plot
{"title": "Tanimoto similarity vs shared substructures", "xLabel": "shared substructure features", "yLabel": "Tanimoto-like similarity", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "similarity", "color": "#16a34a"}]}
```

**Next:** what we even mean by "good" molecules and how we measure them.
""",
        ),
        _t(
            "Scoring molecules: validity, drug-likeness and properties",
            "12 min",
            r"""
# Scoring molecules: validity, drug-likeness and properties

A generator is only useful if we can judge its output. Four levels of scoring
matter.

**Validity** — does the SMILES parse into a real molecule with sensible
valences (checked by RDKit)? **Uniqueness** and **novelty** — are samples
distinct from each other and from the training set? Together these guard
against memorization and mode collapse.

**Drug-likeness** uses interpretable rules and scores. **Lipinski's Rule of
Five** flags poor oral absorption when, e.g., molecular weight $> 500$, $\log P
> 5$, H-bond donors $> 5$ or acceptors $> 10$. The **QED** (Quantitative
Estimate of Drug-likeness) collapses several descriptors into a single
$0$–$1$ score.

**Target properties** — predicted potency, solubility ($\log S$),
synthesizability (**SA score**) or binding affinity, often from a separate
**QSAR / ML predictor**.

```mermaid
flowchart LR
  GEN["Generated SMILES"] --> V["Valid? (RDKit)"]
  V --> U["Unique & novel?"]
  U --> D["Drug-like? (QED, Ro5)"]
  D --> P["Property predictors (logP, SA, activity)"]
  P --> KEEP["Keep top candidates"]
```

Lipophilicity ($\log P$) illustrates a typical sweet spot: too low and the
molecule won't cross membranes, too high and it is insoluble and promiscuous —
so good scores peak in a middle band rather than rising monotonically.

```plot
{"title": "Desirability vs lipophilicity (logP)", "xLabel": "logP", "yLabel": "desirability", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-((x-3)/2)^2)", "label": "desirability", "color": "#dc2626"}]}
```

**Next:** the idea of learning a distribution over molecules.
""",
        ),
        _t(
            "Learning a distribution over molecules",
            "11 min",
            r"""
# Learning a distribution over molecules

The core idea of a generative model is to learn the **probability
distribution** $p(x)$ of molecules in a dataset, so that new samples
$x \sim p(x)$ look like real chemistry. Training typically **maximizes the
likelihood** of the observed molecules, equivalently minimizing the negative
log-likelihood

$$\mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N} \log p(x_i).$$

For a SMILES model, $p(x)$ factorizes over tokens autoregressively:
$p(x) = \prod_t p(x_t \mid x_{<t})$, so the model predicts each next character
given the prefix — exactly like a language model trained on chemistry.

```mermaid
flowchart LR
  TRAIN["Training molecules"] --> FIT["Fit p(x): maximize likelihood"]
  FIT --> LATENT["Learned distribution"]
  LATENT --> SAMPLE["Sample new molecules"]
  SAMPLE --> EVAL["Validity / novelty checks"]
```

As training proceeds the loss (negative log-likelihood) falls and then
flattens; the gap to its floor reflects what the model still cannot capture.

```plot
{"title": "Negative log-likelihood during training", "xLabel": "training epochs", "yLabel": "NLL loss", "xRange": [0, 10], "yRange": [0, 5], "grid": true, "functions": [{"expr": "0.5 + 4*exp(-0.5*x)", "label": "NLL", "color": "#2563eb"}]}
```

Once trained, **conditional** generation $p(x \mid c)$ lets us bias samples on a
property $c$ (e.g. high solubility) — the bridge from "make any molecule" to
"make a useful molecule."

**Next:** the family tree of generative models you'll meet.
""",
        ),
        _t(
            "A map of generative model families",
            "10 min",
            r"""
# A map of generative model families

Several model families learn $p(x)$ in different ways; each trades off sample
quality, diversity, training stability and likelihood access.

- **Autoregressive models** (RNNs, Transformers over SMILES/SELFIES): generate
  token by token; stable, exact likelihood, but sequential.
- **Variational autoencoders (VAEs)**: encode molecules into a smooth
  **latent space** you can optimize in; enable interpolation.
- **Generative adversarial networks (GANs)**: a generator vs a discriminator;
  sharp samples but no likelihood and tricky training.
- **Normalizing flows**: invertible maps giving *exact* likelihood.
- **Diffusion / score-based models**: iteratively denoise; current
  state-of-the-art for 3D structures.
- **Reinforcement learning**: not a density model but a way to *steer* any
  generator toward a reward.

```mermaid
flowchart TB
  GEN["Generative models for molecules"] --> AR["Autoregressive (SMILES)"]
  GEN --> VAE["VAE: latent space"]
  GEN --> GAN["GAN: adversarial"]
  GEN --> FLOW["Normalizing flows"]
  GEN --> DIFF["Diffusion / score-based"]
  GEN --> RL["Reinforcement learning (steering)"]
```

There is a rough trade-off: methods with sharper, more diverse samples often
sacrifice tractable likelihood, while likelihood-based methods can be blurrier
or slower. No single model wins on every axis.

```plot
{"title": "Sample quality vs likelihood tractability (illustrative)", "xLabel": "sample sharpness", "yLabel": "likelihood tractability", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "9/(x+1)", "label": "trade-off frontier", "color": "#16a34a"}]}
```

**Next:** test your grasp of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- Generative Molecular Design -- Intermediate ------------------------------

_INTERMEDIATE = SeedCourse(
    slug="generative-molecular-design-intermediate",
    title="Generative Models for Molecular Design — Intermediate",
    description=(
        "The core quantitative methods of molecular generation: variational "
        "autoencoders and the ELBO, adversarial training and its objectives, "
        "graph-based generation, and reinforcement learning to optimize "
        "molecules toward a reward. Includes the math of latent-space "
        "optimization and reward shaping, with interactive plots and model "
        "diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Variational autoencoders and the ELBO",
            "13 min",
            r"""
# Variational autoencoders and the ELBO

A **variational autoencoder (VAE)** learns an **encoder** $q_\phi(z \mid x)$ that
maps a molecule to a distribution over a latent vector $z$, and a **decoder**
$p_\theta(x \mid z)$ that reconstructs molecules from $z$. Because the true
likelihood is intractable, we maximize the **evidence lower bound (ELBO)**:

$$\mathcal{L}_{ELBO} = \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{KL}\!\big(q_\phi(z|x)\,\|\,p(z)\big).$$

The first term is **reconstruction**; the second is a **KL regularizer**
pulling the posterior toward a prior $p(z)=\mathcal{N}(0,I)$. The
**reparameterization trick**, $z = \mu + \sigma \odot \epsilon$ with
$\epsilon \sim \mathcal{N}(0,I)$, makes sampling differentiable.

The payoff for chemistry is a **smooth, continuous latent space**: nearby points
decode to similar molecules, so we can interpolate and run gradient-based
property optimization (as in the ChemVAE / JT-VAE line of work).

```mermaid
flowchart LR
  X["Molecule x"] --> ENC["Encoder q(z|x)"]
  ENC --> Z["Latent z ~ N(mu, sigma)"]
  Z --> DEC["Decoder p(x|z)"]
  DEC --> XR["Reconstruction x'"]
  PRIOR["Prior N(0, I)"] -.KL.-> ENC
```

Tuning the KL weight $\beta$ (the **beta-VAE** idea) trades reconstruction for a
more disentangled, well-behaved latent space — too much KL and the decoder
ignores $z$ (**posterior collapse**).

```plot
{"title": "Reconstruction error vs KL weight beta", "xLabel": "KL weight beta", "yLabel": "reconstruction error", "xRange": [0, 10], "yRange": [0, 6], "grid": true, "functions": [{"expr": "0.5 + 0.5*exp(0.4*x)", "label": "recon error", "color": "#dc2626"}]}
```

**Next:** generating with adversaries — GANs for molecules.
""",
        ),
        _t(
            "GANs for molecular generation",
            "12 min",
            r"""
# GANs for molecular generation

A **generative adversarial network (GAN)** pits a **generator** $G$ against a
**discriminator** $D$ in a minimax game:

$$\min_G \max_D \; \mathbb{E}_{x\sim p_{data}}[\log D(x)] + \mathbb{E}_{z\sim p_z}[\log(1 - D(G(z)))].$$

$D$ learns to tell real molecules from fakes; $G$ learns to fool $D$. At the
ideal equilibrium $G$ reproduces the data distribution. GANs give **no explicit
likelihood**, which is why validity/novelty metrics matter so much here.

For molecules, **ORGAN/MolGAN** combine the adversarial loss with a **reward**
(a property score) — often via reinforcement learning because discrete
SMILES/graph outputs are not directly differentiable through sampling.
**MolGAN** generates graphs directly and is fast (one shot) but prone to
**mode collapse** (low uniqueness).

```mermaid
flowchart LR
  Z["Noise z"] --> G["Generator"]
  G --> FAKE["Fake molecule"]
  DATA["Real molecules"] --> D["Discriminator"]
  FAKE --> D
  D --> LOSS["Real vs fake signal"]
  LOSS -->|update| G
  LOSS -->|update| D
```

Training is delicate: if $D$ wins too fast, gradients to $G$ vanish.
**Wasserstein GANs (WGAN-GP)** replace the loss with an Earth-Mover distance and
a gradient penalty to stabilize this. A healthy run keeps generator and
discriminator losses in a balanced, oscillating regime rather than one
collapsing.

```plot
{"title": "Generator loss in an unstable vs stable GAN", "xLabel": "training steps", "yLabel": "generator loss", "xRange": [0, 10], "yRange": [0, 6], "grid": true, "functions": [{"expr": "2 + sin(2*x)", "label": "stable (balanced)", "color": "#16a34a"}, {"expr": "5*exp(-0.5*x)", "label": "vanishing gradient", "color": "#dc2626"}]}
```

**Next:** building molecules as graphs.
""",
        ),
        _t(
            "Graph-based molecular generation",
            "12 min",
            r"""
# Graph-based molecular generation

Strings can produce chemically odd intermediates; **graph generation** works on
the molecule's native structure, guaranteeing valences are respected at each
step. A molecule is a graph $G=(V,E)$ with atom features on nodes and bond types
on edges, processed by **message-passing GNNs** that update each atom from its
neighbors.

Two generation strategies dominate:

- **Autoregressive graph models** (e.g. **GraphAF**, **MolecularRNN**) add atoms
  and bonds one at a time, applying valence masks so every partial graph stays
  valid.
- **One-shot models** (e.g. **MolGAN**, graph VAEs) emit the whole
  adjacency/feature tensor at once — fast, but must reconcile a permutation
  problem and often score lower on validity.

```mermaid
flowchart LR
  START["Empty / seed graph"] --> ADDA["Add atom"]
  ADDA --> ADDB["Add bond (valence-masked)"]
  ADDB --> STOP{"Terminate?"}
  STOP -->|no| ADDA
  STOP -->|yes| MOL["Final molecular graph"]
```

A key advantage: enforcing valence rules at each step lets autoregressive graph
models reach near-100% validity without a post-hoc filter, whereas raw SMILES
models lose many samples to parse errors. The trade-off is more steps per
molecule and a more complex decoder.

```plot
{"title": "Validity vs valence masking strength", "xLabel": "constraint strictness", "yLabel": "fraction valid", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-3)))", "label": "valid fraction", "color": "#2563eb"}]}
```

**Next:** steering generators with reinforcement learning.
""",
        ),
        _t(
            "Reinforcement learning for property optimization",
            "13 min",
            r"""
# Reinforcement learning for property optimization

Likelihood training reproduces the data; **reinforcement learning (RL)** pushes
a generator toward molecules with *better* properties than the data. The
generator is a **policy** $\pi_\theta$ that builds a molecule as a sequence of
actions (tokens or graph edits); a **reward** $R$ scores the finished molecule
(e.g. predicted potency, QED, docking score).

The **REINFORCE** policy-gradient update maximizes expected reward:

$$\nabla_\theta J(\theta) = \mathbb{E}_{x\sim\pi_\theta}\big[(R(x) - b)\,\nabla_\theta \log \pi_\theta(x)\big],$$

where the baseline $b$ reduces variance. The influential **REINVENT** approach
adds a KL-style penalty to a fixed **prior** policy so the agent earns reward
*without drifting into invalid or bizarre chemistry*:

$$R_{aug} = R(x) - \lambda\, [\log \pi_\theta(x) - \log \pi_{prior}(x)].$$

```mermaid
flowchart LR
  PRIOR["Pretrained prior policy"] --> AGENT["Agent policy pi_theta"]
  AGENT --> MOL["Sampled molecule"]
  MOL --> SCORE["Reward R(x): activity, QED, docking"]
  SCORE -->|policy gradient| AGENT
  PRIOR -.KL penalty.-> AGENT
```

A central danger is **reward hacking**: the agent exploits flaws in the scoring
function (e.g. a QSAR model's blind spot) to score high while being useless.
Mitigations include multi-objective rewards, diversity bonuses and
experience replay. Average reward typically climbs and saturates as the policy
specializes.

```plot
{"title": "Average reward during RL fine-tuning", "xLabel": "training steps", "yLabel": "mean reward", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-4)))", "label": "mean reward", "color": "#16a34a"}]}
```

**Next:** searching latent spaces with Bayesian optimization.
""",
        ),
        _t(
            "Latent-space optimization and Bayesian search",
            "12 min",
            r"""
# Latent-space optimization and Bayesian search

A VAE's continuous latent space turns molecular design into **continuous
optimization**: instead of editing discrete molecules, we move a vector $z$ to
improve a property, then decode. If a property predictor $f(z)$ is differentiable
we can do **gradient ascent**; otherwise we use **Bayesian optimization (BO)**.

BO fits a **surrogate** (typically a **Gaussian process**) to observed
$(z, \text{property})$ pairs and picks the next $z$ to evaluate by maximizing an
**acquisition function** such as **Expected Improvement** — balancing
**exploitation** (high predicted value) against **exploration** (high
uncertainty). This is sample-efficient, crucial when each evaluation means a
docking run or an assay.

```mermaid
flowchart LR
  Z["Latent points z"] --> GP["Gaussian-process surrogate"]
  GP --> ACQ["Acquisition (Expected Improvement)"]
  ACQ --> NEXT["Pick next z"]
  NEXT --> DEC["Decode to molecule"]
  DEC --> EVAL["Evaluate property"]
  EVAL -->|augment data| GP
```

A practical caveat: optimizing too aggressively pushes $z$ into **low-density,
poorly-trained regions** of the latent space, where the decoder produces invalid
or unrealistic molecules. **Jointly trained** property predictors and trust
regions keep the search in the well-modeled "valid manifold." The acquisition
value is high where the GP mean is good *and* uncertainty is informative,
peaking away from already-sampled points.

```plot
{"title": "Expected-improvement acquisition over latent coordinate", "xLabel": "latent coordinate z", "yLabel": "acquisition value", "xRange": [0, 10], "yRange": [0, 1.6], "grid": true, "functions": [{"expr": "exp(-((x-3)/1.2)^2) + 0.7*exp(-((x-7)/1)^2)", "label": "acquisition", "color": "#2563eb"}]}
```

**Next:** check your understanding of the core methods.
""",
        ),
        _quiz(),
    ),
)


# -- Generative Molecular Design -- Advanced ----------------------------------

_ADVANCED = SeedCourse(
    slug="generative-molecular-design-advanced",
    title="Generative Models for Molecular Design — Advanced",
    description=(
        "State-of-the-art and applied molecular generation: denoising diffusion "
        "and score-based models, equivariant 3D generation, structure-based "
        "(pocket-conditioned) design and docking, multi-objective and "
        "synthesis-aware optimization, and rigorous benchmarking and "
        "deployment. Combines the latest AI methods with practical evaluation, "
        "using interactive plots and pipeline diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Denoising diffusion and score-based models",
            "14 min",
            r"""
# Denoising diffusion and score-based models

**Diffusion models** are the current frontier for molecular generation. A
**forward process** gradually adds Gaussian noise to data over $T$ steps until
it becomes pure noise; a neural network learns the **reverse process** that
denoises step by step, turning noise into molecules.

The forward step is
$x_t = \sqrt{\alpha_t}\,x_{t-1} + \sqrt{1-\alpha_t}\,\epsilon$, and the network
$\epsilon_\theta(x_t, t)$ is trained to predict the added noise with the simple
objective

$$\mathcal{L} = \mathbb{E}_{t,x_0,\epsilon}\big[\|\epsilon - \epsilon_\theta(x_t,t)\|^2\big].$$

This is equivalent to **score matching**: learning $\nabla_x \log p(x)$, the
direction toward higher data density. Diffusion sidesteps GAN instability and
VAE blur, giving high-quality, diverse samples.

```mermaid
flowchart LR
  X0["Molecule x0"] -->|add noise| XT["Noisy x_T (~ pure noise)"]
  XT -->|learned denoiser eps_theta| XR["Denoised x0'"]
  XR --> SAMPLE["New molecule"]
```

The **noise schedule** $\alpha_t$ controls how fast information is destroyed; a
common choice keeps the signal-to-noise ratio decaying smoothly so each reverse
step is learnable. Too-fast schedules destroy structure before the network can
learn to invert them.

```plot
{"title": "Signal retained vs diffusion timestep", "xLabel": "timestep t", "yLabel": "signal level (sqrt alpha-bar)", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.3*x)", "label": "retained signal", "color": "#2563eb"}]}
```

**Next:** generating molecules in 3D with the right symmetries.
""",
        ),
        _t(
            "Equivariant 3D generation",
            "13 min",
            r"""
# Equivariant 3D generation

Many properties (binding, energy) depend on **3D geometry**, so we generate
atomic coordinates, not just connectivity. The physics is invariant to
**rotations, translations and reflections** ($E(3)$/$SE(3)$): a rotated molecule
is the same molecule. A naive coordinate network would have to *learn* this
symmetry from data; **equivariant networks** build it in.

**E(3)-equivariant GNNs** (e.g. **EGNN**) update coordinates using only
distances and relative vectors, so the output rotates exactly as the input does.
Combined with diffusion this gives **E(3)-equivariant diffusion models** like
**EDM**, which diffuse atom types and 3D positions jointly to generate valid 3D
molecules.

```mermaid
flowchart TB
  NOISE["Noisy atoms (types + 3D coords)"] --> EGNN["E(3)-equivariant denoiser"]
  EGNN --> STEP["Reverse diffusion step"]
  STEP --> CHECK{"t = 0?"}
  CHECK -->|no| EGNN
  CHECK -->|yes| MOL3D["3D molecule (coords + bonds)"]
```

Equivariance is a strong **inductive bias**: by not wasting capacity learning
symmetry, these models reach good geometry with far less data and generalize to
unseen orientations. Empirically, sample quality (e.g. fraction with valid,
stable geometry) climbs much faster per training example than for non-equivariant
baselines.

```plot
{"title": "Stable-geometry rate vs training data (equivariant vs not)", "xLabel": "training data (relative)", "yLabel": "fraction stable", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-2)))", "label": "equivariant", "color": "#16a34a"}, {"expr": "1/(1+exp(-(x-6)))", "label": "non-equivariant", "color": "#dc2626"}]}
```

**Next:** designing molecules for a specific protein pocket.
""",
        ),
        _t(
            "Structure-based (pocket-conditioned) design",
            "13 min",
            r"""
# Structure-based (pocket-conditioned) design

**Structure-based drug design (SBDD)** conditions generation on a **protein
binding pocket**: given the 3D pocket, generate ligands that fit and bind it.
The model learns $p(\text{ligand} \mid \text{pocket})$, placing atoms inside the
cavity with favorable interactions (H-bonds, hydrophobic contacts, shape
complementarity).

Modern approaches (e.g. **Pocket2Mol**, **TargetDiff**, **DiffSBDD**) use
3D equivariant diffusion conditioned on pocket atoms, growing a ligand
atom-by-atom or denoising it inside the pocket. The conditioning is what turns a
general generator into a target-specific one.

```mermaid
flowchart LR
  POCKET["Protein pocket (3D atoms)"] --> COND["Condition the generator"]
  COND --> GEN["Pocket-conditioned diffusion"]
  GEN --> LIG["Candidate ligand in pocket"]
  LIG --> DOCK["Docking / scoring (Vina, Gnina)"]
  DOCK --> RANK["Rank by predicted affinity"]
```

Generated poses are validated by **molecular docking** (AutoDock Vina, Gnina)
and ideally by physics-based **free-energy** estimates. A core challenge is that
docking scores correlate only loosely with true binding, so high scores must be
treated as enrichment, not proof — affinity rises with good complementarity but
plateaus and is noisy, demanding wet-lab confirmation.

```plot
{"title": "Predicted binding gain vs pocket shape complementarity", "xLabel": "shape complementarity", "yLabel": "relative predicted affinity", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "predicted affinity", "color": "#2563eb"}]}
```

**Next:** optimizing many objectives at once.
""",
        ),
        _t(
            "Multi-objective and synthesis-aware optimization",
            "13 min",
            r"""
# Multi-objective and synthesis-aware optimization

Real drug design balances **competing objectives**: potency, selectivity,
solubility, metabolic stability, toxicity and **synthesizability**. Optimizing
one alone yields useless molecules, so we treat design as **multi-objective
optimization (MOO)**.

There is rarely a single best molecule; instead a **Pareto front** of
non-dominated trade-offs. A molecule is **Pareto-optimal** if no other improves
one objective without worsening another. Methods: scalarize objectives into one
reward (weighted sum, **Chebyshev**), use **Pareto-aware** acquisition in BO
(e.g. **qEHVI**, maximizing hypervolume), or **MOO genetic algorithms** like
**NSGA-II** over generated candidates.

Crucially, a beautiful molecule no chemist can make is worthless, so
**synthesis-aware** design adds **retrosynthesis** feasibility (e.g.
**SA score**, **SCScore**, or template/transformer retrosynthesis models) as a
hard objective.

```mermaid
flowchart TB
  GEN["Generator"] --> CAND["Candidate molecules"]
  CAND --> OBJ["Score objectives: potency, ADMET, SA"]
  OBJ --> PARETO["Pareto / hypervolume selection"]
  PARETO --> RETRO["Retrosynthesis feasibility"]
  RETRO --> NEXT["Steer / propose next batch"]
  NEXT --> GEN
```

The Pareto front shows the trade-off directly: pushing potency higher forces
solubility down past a point. Designers pick operating points on this curve
rather than a single optimum.

```plot
{"title": "Potency vs solubility Pareto front", "xLabel": "potency (relative)", "yLabel": "achievable solubility", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "9/(x+1)", "label": "Pareto front", "color": "#dc2626"}]}
```

**Next:** how we benchmark and deploy these models honestly.
""",
        ),
        _t(
            "Benchmarking, validation and deployment",
            "12 min",
            r"""
# Benchmarking, validation and deployment

Generative chemistry is littered with impressive-looking but unverifiable
claims, so **rigorous benchmarking** is essential. Standard suites —
**GuacaMol** and **MOSES** — report **validity**, **uniqueness**, **novelty**,
**Fréchet ChemNet Distance (FCD)** (distributional similarity to real
molecules), **scaffold diversity** and goal-directed optimization scores.

Beyond metrics, watch for failure modes: **mode collapse** (low uniqueness),
**memorization** (low novelty), and **reward hacking** (high in-silico score,
nonsense chemistry). The only decisive validation is the **make–test loop** —
synthesizing and assaying top candidates, ideally in a **closed-loop /
self-driving lab** where results feed back into the model.

```mermaid
flowchart LR
  MODEL["Generative model"] --> METRICS["Benchmarks: validity, FCD, novelty"]
  METRICS --> FILTER["Filter & prioritize"]
  FILTER --> MAKE["Synthesize"]
  MAKE --> TEST["Assay / measure"]
  TEST -->|active-learning feedback| MODEL
```

Honest reporting also means **proper baselines** (a tuned random/enumeration
baseline often beats flashy models) and **held-out** novelty checks against the
training set. As candidates pass each filter the count drops sharply — the
funnel from millions generated to a handful synthesized is steep, which is
exactly why upstream model quality matters.

```plot
{"title": "Candidate attrition through the design funnel", "xLabel": "filter stage", "yLabel": "fraction surviving", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "surviving fraction", "color": "#16a34a"}]}
```

**Next:** prove your mastery of the state of the art.
""",
        ),
        _quiz(),
    ),
)


GENERATIVE_MOLECULAR_DESIGN_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["GENERATIVE_MOLECULAR_DESIGN_COURSES"]
