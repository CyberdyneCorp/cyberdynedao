"""Molecular Docking & Virtual Screening track: Basics -> Intermediate -> Advanced.

A three-level track on predicting how small molecules bind protein targets and on
screening large libraries to find hits. It moves from binding intuition, poses and
conformational search; through scoring functions, search algorithms and pose
validation; to high-throughput virtual screening, consensus/rescoring and machine
-learning scoring. Lessons are `text` with LaTeX, interactive ```plot blocks
(binding curves, energy landscapes, enrichment) and ```mermaid pipeline diagrams.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Molecular Docking & Virtual Screening — Basics ───────────────────────────

_BASICS = SeedCourse(
    slug="docking-virtual-screening-basics",
    title="Molecular Docking & Virtual Screening — Basics",
    description=(
        "An intuitive introduction to how small molecules bind protein targets "
        "and how computers predict that binding. We build from the physics of "
        "molecular recognition and the meaning of binding affinity, through the "
        "idea of a docking pose and the binding site, to conformational "
        "flexibility and a first end-to-end docking run. Interactive plots and "
        "pipeline diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What molecular recognition means",
            "10 min",
            r"""
# What molecular recognition means

**Molecular docking** asks a concrete question: given a protein **target** and a
small-molecule **ligand**, how do they fit together, and how strongly do they
stick? The answer underpins most of modern drug discovery, because nearly all
drugs act by binding a protein and changing its behaviour.

Binding is driven by **non-covalent interactions**: hydrogen bonds, salt bridges
(electrostatics), van der Waals contacts and the **hydrophobic effect**, in which
non-polar surfaces associate to release ordered water into bulk solvent. A good
ligand is **complementary** to its pocket in shape *and* chemistry — the old
"lock and key" picture, refined by **induced fit**, where both partners adjust.

```mermaid
flowchart LR
  L["Ligand (small molecule)"] --> C["Complementarity:\nshape + chemistry"]
  P["Protein pocket"] --> C
  C --> B["Bound complex\n(low free energy)"]
```

The strength of binding is a **free energy**, $\Delta G_{bind}$. It balances
enthalpy (favourable contacts) against entropy (lost flexibility and freed water).
Affinity falls off steeply as contacts improve: a modest gain in $\Delta G$ buys a
large gain in occupancy.

```plot
{"title": "Fraction of protein bound vs ligand concentration", "xLabel": "ligand [L]", "yLabel": "fraction bound", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating binding", "color": "#2563eb"}]}
```

Docking tries to *predict* both the geometry (the **pose**) and a *score* that
ranks how good that binding is.

**Next:** turning binding strength into a number — affinity and $\Delta G$.
""",
        ),
        _t(
            "Binding affinity and free energy",
            "11 min",
            r"""
# Binding affinity and free energy

The equilibrium $P + L \rightleftharpoons PL$ is summarised by the **dissociation
constant** $K_d$:

$$K_d = \frac{[P][L]}{[PL]}$$

A *small* $K_d$ means *tight* binding. At a ligand concentration equal to $K_d$,
exactly half the protein is occupied, so $K_d$ has units of concentration (often
nM to µM for useful drugs). $K_d$ connects to free energy through

$$\Delta G_{bind} = R T \ln K_d$$

where $R$ is the gas constant and $T$ the temperature. Because of the logarithm,
each factor-of-ten improvement in $K_d$ is worth only about $1.4\,\text{kcal/mol}$
at room temperature — which is roughly one good hydrogen bond.

```plot
{"title": "Fraction bound for a tight vs weak binder", "xLabel": "ligand [L] (uM)", "yLabel": "fraction bound", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+0.5)", "label": "tight (Kd=0.5)", "color": "#16a34a"}, {"expr": "x/(x+4)", "label": "weak (Kd=4)", "color": "#dc2626"}]}
```

For inhibitors that compete with a substrate, experiments often report an **IC50**
(the concentration giving 50% inhibition) or a $K_i$. These are related but not
identical: IC50 depends on assay conditions, whereas $K_i$ and $K_d$ are intrinsic
constants. The goal of a scoring function (later) is to **estimate $\Delta G_{bind}$
from a structure alone**.

```mermaid
flowchart LR
  KD["Kd (concentration)"] --> DG["ΔG = RT ln Kd"]
  DG --> RANK["Rank ligands\nby predicted ΔG"]
```

**Next:** the binding site — where on the protein this all happens.
""",
        ),
        _t(
            "The binding site and the pose",
            "10 min",
            r"""
# The binding site and the pose

Docking happens inside a defined region of the protein, the **binding site** (or
**pocket**), usually a concave cavity lined with residues that contact the ligand.
For an enzyme this is often the **active site**; for a receptor it may be an
**orthosteric** site (where the natural ligand binds) or an **allosteric** site
elsewhere on the protein.

A **pose** is one candidate placement of the ligand in the pocket: its position,
orientation and internal conformation. Docking generates many poses and tries to
identify the one closest to reality — the **binding mode**. We measure how close a
predicted pose is to a known crystal pose with the **root-mean-square deviation**
of atomic positions:

$$\text{RMSD} = \sqrt{\frac{1}{N}\sum_{i=1}^{N}\,\lVert \mathbf{r}_i - \mathbf{r}_i^{ref}\rVert^2}$$

A pose with $\text{RMSD} < 2\,\text{Å}$ from the experimental structure is the usual
threshold for "correct".

```mermaid
flowchart LR
  POCKET["Binding pocket\n(cavity + residues)"] --> POSE["Pose:\nposition + orientation + conf."]
  POSE --> RMSD["RMSD vs crystal pose"]
  RMSD --> OK["< 2 Å = correct"]
```

Where is the pocket? Sometimes it is obvious from a bound ligand in the crystal
structure; otherwise **pocket-detection** tools (geometry- or energy-based) propose
candidate cavities. Defining the search region — a box or sphere around the site —
is the first practical step of any docking run.

```plot
{"title": "Pose 'quality' falls with RMSD from the true pose", "xLabel": "RMSD (Angstrom)", "yLabel": "relative quality", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "quality ~ exp(-RMSD)", "color": "#2563eb"}]}
```

**Next:** why ligands are flexible and what that does to the search.
""",
        ),
        _t(
            "Conformational flexibility",
            "11 min",
            r"""
# Conformational flexibility

A small molecule is not rigid. Single bonds rotate, so the same molecule can adopt
many three-dimensional shapes, or **conformers**. Each **rotatable bond** adds a
**torsion** (dihedral) degree of freedom. If each torsion has roughly $k$
preferred values, a ligand with $n$ rotatable bonds has on the order of $k^n$
conformers — the combinatorics explode quickly.

```plot
{"title": "Conformers grow exponentially with rotatable bonds", "xLabel": "rotatable bonds n", "yLabel": "approx. conformers (3^n)", "xRange": [0, 8], "yRange": [0, 600], "grid": true, "functions": [{"expr": "3^x", "label": "~3 states per torsion", "color": "#dc2626"}]}
```

Each torsion has its own energy profile. Rotating about an ethane-like bond gives a
periodic potential with minima at staggered angles and maxima at eclipsed ones —
the **torsional potential** that force fields encode.

```plot
{"title": "A torsional potential vs dihedral angle", "xLabel": "dihedral (rad)", "yLabel": "energy (a.u.)", "xRange": [0, 6.3], "yRange": [0, 2], "grid": true, "functions": [{"expr": "1-cos(3*x)", "label": "3-fold torsion", "color": "#16a34a"}]}
```

Docking must explore this flexibility. **Rigid docking** keeps the ligand fixed and
only searches its placement; **flexible-ligand docking** also samples torsions,
which is now standard. Some methods even allow **flexible receptor** side chains.
More flexibility means a more realistic model but a far larger search space — the
core tension we manage with search algorithms and scoring.

```mermaid
flowchart LR
  RB["Rotatable bonds"] --> CONF["Many conformers"]
  CONF --> SEARCH["Search: rigid vs\nflexible ligand/receptor"]
  SEARCH --> COST["More DOF = harder search"]
```

**Next:** putting it together in a first docking run.
""",
        ),
        _t(
            "Your first docking run",
            "12 min",
            r"""
# Your first docking run

A basic docking workflow has a few well-defined stages. **Prepare the receptor**:
remove crystallographic water (unless functionally important), add hydrogens,
assign protonation states and partial charges. **Prepare the ligand**: build a
sensible 3D conformer, set protonation and tautomer states, and mark rotatable
bonds. **Define the search box** around the binding site. **Dock**: the engine
samples poses and scores them. **Inspect**: look at the top-ranked poses and the
interactions they make.

```mermaid
flowchart LR
  REC["Prepare receptor"] --> BOX["Define search box"]
  LIG["Prepare ligand"] --> DOCK["Dock: sample + score"]
  BOX --> DOCK
  DOCK --> POSES["Ranked poses"]
  POSES --> INSPECT["Inspect interactions"]
```

Popular open tools illustrate the field: **AutoDock** and **AutoDock Vina** are
widely used and free; **DOCK**, **rDock**, **Glide** (commercial) and **GOLD** are
other established engines. They differ in their search algorithm and scoring
function, but share this overall shape.

A key habit from day one is **validation by re-docking**: take a ligand whose bound
structure is known, remove it, dock it back, and check the RMSD of the top pose. If
the engine cannot reproduce a known binding mode, you cannot trust its predictions
for unknown ligands.

```plot
{"title": "Re-docking success vs RMSD cutoff (illustrative)", "xLabel": "RMSD cutoff (Angstrom)", "yLabel": "fraction recovered", "xRange": [0, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(1.5/x)^4)", "label": "cumulative success", "color": "#2563eb"}]}
```

**Next:** the Intermediate course — scoring functions and search algorithms in
depth.
""",
        ),
        _quiz(),
    ),
)


# ── Molecular Docking & Virtual Screening — Intermediate ─────────────────────

_INTERMEDIATE = SeedCourse(
    slug="docking-virtual-screening-intermediate",
    title="Molecular Docking & Virtual Screening — Intermediate",
    description=(
        "The quantitative core of docking. We cover the families of scoring "
        "functions and what they approximate, the search algorithms that explore "
        "pose space, how flexibility is sampled, how poses are validated, and how "
        "single-target docking scales up toward screening. Includes binding-energy "
        "plots, search-convergence curves and pipeline diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Scoring functions: families and form",
            "12 min",
            r"""
# Scoring functions: families and form

A **scoring function** estimates how good a pose is, ideally approximating
$\Delta G_{bind}$. There are four classical families. **Force-field-based** scores
sum physics terms — van der Waals (Lennard-Jones), electrostatics (Coulomb) and
sometimes explicit hydrogen bonds. **Empirical** scores (e.g. Glide, ChemScore)
fit weighted terms — H-bonds, hydrophobic contact, rotatable-bond penalty — to
experimental affinities. **Knowledge-based** (statistical-potential) scores derive
pairwise atom-type potentials from observed distances in the PDB. **Machine
-learning** scores (covered in Advanced) learn the mapping from descriptors.

```mermaid
flowchart TB
  SF["Scoring function"] --> FF["Force-field based"]
  SF --> EMP["Empirical / regression"]
  SF --> KB["Knowledge-based\n(PDB statistics)"]
  SF --> ML["Machine learning"]
```

The van der Waals term is the familiar **Lennard-Jones** potential, attractive at
medium range and steeply repulsive when atoms clash:

$$V_{LJ}(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right]$$

```plot
{"title": "Lennard-Jones interaction vs distance", "xLabel": "distance r (sigma units)", "yLabel": "energy / epsilon", "xRange": [0.9, 3], "yRange": [-1.2, 2], "grid": true, "functions": [{"expr": "4*((1/x)^12-(1/x)^6)", "label": "V_LJ", "color": "#2563eb"}]}
```

No scoring function is perfect. They trade speed against accuracy and are tuned for
either **pose prediction** (geometry) or **affinity ranking** — rarely both well.

**Next:** how engines search the vast space of poses.
""",
        ),
        _t(
            "Search algorithms for pose space",
            "12 min",
            r"""
# Search algorithms for pose space

Even rigid placement of a ligand is a 6-dimensional problem (3 translations, 3
rotations); flexible ligands add one dimension per rotatable torsion. Exhaustive
enumeration is impossible, so docking uses **search (sampling) algorithms** to find
low-score poses.

**Systematic / incremental-construction** methods build the ligand fragment by
fragment inside the pocket (e.g. DOCK's anchor-and-grow, FlexX). **Stochastic**
methods sample randomly with a bias toward better scores: **Monte Carlo** with
Metropolis acceptance, **simulated annealing**, **genetic algorithms** (GOLD,
AutoDock) and the **Lamarckian genetic algorithm**. AutoDock Vina uses an efficient
gradient-guided Monte Carlo variant.

```mermaid
flowchart LR
  SEARCH["Pose search"] --> SYS["Systematic\n(fragment build-up)"]
  SEARCH --> STO["Stochastic\nMC / SA / GA"]
  STO --> ANNEAL["Bias toward low score"]
```

Stochastic searches accept worse poses with a temperature-dependent probability so
they can escape local minima — the Metropolis criterion $p = \exp(-\Delta E / k_B
T)$:

```plot
{"title": "Metropolis acceptance probability vs energy increase", "xLabel": "energy increase (kT units)", "yLabel": "acceptance probability", "xRange": [0, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-x)", "label": "p = exp(-dE/kT)", "color": "#dc2626"}]}
```

More search effort (more runs, more evaluations) improves the chance of finding the
global minimum but costs time. In practice we run several independent searches and
cluster the results, trusting a pose that recurs.

```plot
{"title": "Best score found improves with search effort", "xLabel": "evaluations (x1000)", "yLabel": "score gap to optimum", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "convergence", "color": "#16a34a"}]}
```

**Next:** modelling flexibility in ligand and receptor.
""",
        ),
        _t(
            "Modelling flexibility",
            "11 min",
            r"""
# Modelling flexibility

Real binding involves motion. **Ligand flexibility** is now routine: torsions are
sampled during the search. **Receptor flexibility** is harder because the protein
has thousands of degrees of freedom. Several strategies exist.

**Soft docking** slightly softens the repulsive wall of the van der Waals term so
small clashes are tolerated, mimicking minor side-chain give. **Side-chain
flexibility** lets selected pocket residues sample **rotamers** from a library.
**Ensemble docking** docks against several receptor conformations — from crystal
structures, NMR models, or molecular-dynamics snapshots — and keeps the best result,
approximating **conformational selection**.

```mermaid
flowchart TB
  FLEX["Receptor flexibility"] --> SOFT["Soft docking\n(softened vdW)"]
  FLEX --> ROT["Side-chain rotamers"]
  FLEX --> ENS["Ensemble docking\n(MD/NMR snapshots)"]
```

Softening the wall changes the energy landscape: clashes that were forbidden become
merely costly, which can rescue near-correct poses but also admits false ones.

```plot
{"title": "Soft vs hard repulsive wall", "xLabel": "overlap distance", "yLabel": "repulsion energy", "xRange": [0.6, 2], "yRange": [0, 4], "grid": true, "functions": [{"expr": "(1/x)^12", "label": "hard wall", "color": "#dc2626"}, {"expr": "(1/x)^6", "label": "softened", "color": "#16a34a"}]}
```

The cost of flexibility is combinatorial: every flexible residue multiplies the
search space. Ensemble docking trades one big flexible search for several cheaper
rigid-receptor searches — often the most practical compromise.

**Next:** deciding which poses to believe.
""",
        ),
        _t(
            "Pose validation and metrics",
            "11 min",
            r"""
# Pose validation and metrics

A docking engine returns many scored poses; deciding which to trust requires
**validation metrics** beyond the raw score. The workhorse is **re-docking**: dock
a ligand whose bound structure is known and measure the **RMSD** of the top pose to
the crystal pose. Success is usually $\text{RMSD} < 2\,\text{Å}$.

For benchmarking across a target, the **success rate** is the fraction of cases
where a near-native pose appears at rank 1 (pose-prediction power), or anywhere in
the top $N$ (sampling power). Beyond geometry, **interaction fingerprints** encode
which contacts a pose makes (H-bonds, hydrophobic, ionic) as a bit vector, letting
you compare a pose to a known binding mode by similarity.

```mermaid
flowchart LR
  POSES["Scored poses"] --> CLUST["Cluster by RMSD"]
  CLUST --> REDOCK["Re-dock validation"]
  REDOCK --> IFP["Interaction fingerprint match"]
  IFP --> TRUST["Trust a recurring,\ncontact-consistent pose"]
```

A recurring trap is **score-RMSD discordance**: the best-scoring pose is not always
the most native-like. Clustering poses and inspecting the most populated cluster
often beats taking the single top score.

```plot
{"title": "Top-pose success vs RMSD cutoff (benchmark)", "xLabel": "RMSD cutoff (Angstrom)", "yLabel": "success rate", "xRange": [0, 5], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(1.8/x)^4)", "label": "cumulative success", "color": "#2563eb"}]}
```

**Next:** scaling a single target up toward screening.
""",
        ),
        _t(
            "From single docking to screening",
            "12 min",
            r"""
# From single docking to screening

**Virtual screening (VS)** applies docking (or faster filters) to a **library** of
many candidate molecules to prioritise a few for experimental testing. The aim is
not perfect affinity prediction but **enrichment** — getting true binders to float
to the top of the ranked list.

```mermaid
flowchart LR
  LIB["Compound library"] --> FILT["Filters:\nLipinski, PAINS, ADMET"]
  FILT --> PREP["3D prep + tautomers"]
  PREP --> DOCK["Dock + score"]
  DOCK --> RANK["Rank + select top k"]
  RANK --> ASSAY["Experimental assay"]
```

Before docking, cheap **filters** prune the library: physicochemical rules such as
**Lipinski's rule of five**, removal of reactive or promiscuous **PAINS**
substructures, and rough ADMET checks. This both saves compute and removes
implausible chemistry.

We judge a screen by how much it **enriches** actives near the top of the list. The
**enrichment factor** at the top $x\%$ compares the hit rate there to random
selection:

$$\text{EF}_{x\%} = \frac{\text{actives in top } x\% / \text{compounds in top } x\%}{\text{total actives}/\text{total compounds}}$$

```plot
{"title": "Cumulative actives found vs library fraction screened", "xLabel": "fraction of library screened", "yLabel": "fraction of actives found", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-4*x)", "label": "good screen (enriched)", "color": "#16a34a"}, {"expr": "x", "label": "random", "color": "#dc2626"}]}
```

A perfect screen finds all actives in a tiny fraction of the library; a useless one
follows the diagonal. The Advanced course makes this rigorous with ROC/AUC and
covers high-throughput and AI methods.

**Next:** the Advanced course — high-throughput screening, consensus and ML scoring.
""",
        ),
        _quiz(),
    ),
)


# ── Molecular Docking & Virtual Screening — Advanced ─────────────────────────

_ADVANCED = SeedCourse(
    slug="docking-virtual-screening-advanced",
    title="Molecular Docking & Virtual Screening — Advanced",
    description=(
        "State-of-the-art and applied virtual screening. We cover rigorous "
        "enrichment metrics, ultra-large library and structure-based screening, "
        "consensus scoring and rescoring with physics-based free-energy methods, "
        "machine-learning and deep-learning scoring, and how to avoid bias and "
        "validate honestly. Includes ROC/enrichment plots and screening pipelines."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Enrichment, ROC and screening metrics",
            "12 min",
            r"""
# Enrichment, ROC and screening metrics

A virtual screen is a **ranking** problem: we want actives near the top. The
**enrichment factor** $\text{EF}_{x\%}$ measures the hit rate in the top fraction
relative to random, but it depends on the chosen cutoff and on the active/decoy
ratio. The **ROC curve** plots true-positive rate against false-positive rate
across all thresholds; its area, **AUC**, is threshold-free (0.5 = random, 1.0 =
perfect).

```plot
{"title": "ROC curves: good screen vs random", "xLabel": "false positive rate", "yLabel": "true positive rate", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "sqrt(x)*(2-x)/1.0", "label": "good (high AUC)", "color": "#16a34a"}, {"expr": "x", "label": "random (AUC 0.5)", "color": "#dc2626"}]}
```

Because hits are usually wanted from the *very top* of the list, **early
-recognition** metrics matter more than global AUC. The **BEDROC** and **RIE**
metrics weight early ranks exponentially; the **log-AUC** emphasises the
small-false-positive region.

```mermaid
flowchart LR
  RANK["Ranked screen output"] --> EF["EF at top x%"]
  RANK --> ROC["ROC / AUC"]
  RANK --> EARLY["Early recognition:\nBEDROC, RIE, logAUC"]
```

Decoys must be chosen carefully: property-matched but topologically distinct
decoys (as in **DUD-E** / **DEKOIS**) avoid trivial separation by molecular weight
and inflate-then-deflate the apparent performance honestly.

**Next:** screening libraries that reach into the billions.
""",
        ),
        _t(
            "Ultra-large library screening",
            "12 min",
            r"""
# Ultra-large library screening

Make-on-demand chemical spaces such as **Enamine REAL** now exceed tens of billions
of synthesisable molecules — far more than can be docked one by one. Two ideas make
this tractable. First, **massive parallelism**: docking embarrassingly parallel
campaigns on HPC/GPU (e.g. VirtualFlow, the 2019 docking of ~1 billion molecules)
to find chemotypes that classic million-compound screens miss.

```plot
{"title": "Brute-force docking cost grows linearly with library size", "xLabel": "library size (billions)", "yLabel": "compute (arbitrary)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "dock every molecule", "color": "#dc2626"}, {"expr": "log(1+x)*2", "label": "active-learning subset", "color": "#16a34a"}]}
```

Second, **active-learning / surrogate** strategies (e.g. **MolPAL**, deep docking)
dock a small sample, train a fast ML model to predict docking score from structure,
use it to triage the full space, and dock only the most promising — cutting cost by
orders of magnitude while recovering most top hits.

```mermaid
flowchart LR
  SPACE["10^9-10^11 molecules"] --> SAMP["Dock a sample"]
  SAMP --> MODEL["Train surrogate model"]
  MODEL --> PRED["Predict scores for all"]
  PRED --> SEL["Dock only top candidates"]
  SEL --> SAMP
```

Scale also amplifies error: with billions of compounds, even a tiny false-positive
rate yields many garbage top hits, so **rescoring** and careful pose inspection of
the final shortlist are essential.

**Next:** combining and re-ranking scores for reliability.
""",
        ),
        _t(
            "Consensus scoring and rescoring",
            "12 min",
            r"""
# Consensus scoring and rescoring

No single scoring function is reliably best across targets, so practitioners
combine them. **Consensus scoring** runs several functions and merges their verdicts
— by rank, by vote, or by averaging normalised scores. The intuition: independent
errors partly cancel, and a compound ranked highly by *several* functions is a
safer bet.

```mermaid
flowchart LR
  POSES["Docked poses"] --> S1["Score A"]
  POSES --> S2["Score B"]
  POSES --> S3["Score C"]
  S1 --> CONS["Consensus:\nrank/vote/average"]
  S2 --> CONS
  S3 --> CONS
  CONS --> SHORT["Refined shortlist"]
```

**Rescoring** instead re-evaluates poses with a *more expensive, more accurate*
method than the fast docking score. The gold standard is **physics-based
free-energy** estimation: **MM/PBSA** and **MM/GBSA** add implicit-solvent terms to
a molecular-mechanics energy, while rigorous **FEP** (free-energy perturbation) and
**thermodynamic integration** compute relative binding free energies via alchemical
transformations along a coupling parameter $\lambda$.

```plot
{"title": "Accuracy vs cost across scoring tiers", "xLabel": "method cost (log scale)", "yLabel": "ranking accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "docking -> MMGBSA -> FEP", "color": "#2563eb"}]}
```

The usual pipeline is a **funnel**: fast docking on the whole library, MM/GBSA
rescoring on the top thousands, and FEP on the final tens — spending accuracy where
it matters most.

**Next:** machine-learning and deep-learning scoring.
""",
        ),
        _t(
            "Machine-learning scoring functions",
            "12 min",
            r"""
# Machine-learning scoring functions

**Machine-learning scoring functions (MLSFs)** replace a fixed functional form with
a model trained on data. Early MLSFs such as **RF-Score** used random forests on
interaction-count descriptors and beat classical scores on the PDBbind affinity
benchmark. Modern approaches use **deep learning**: 3D-CNNs over voxelised
complexes, and **graph neural networks** that treat the protein-ligand complex as a
graph of atoms and bonds.

```mermaid
flowchart LR
  CPLX["Protein-ligand complex"] --> FEAT["Features:\ngrids / graphs / fingerprints"]
  FEAT --> MODEL["RF / CNN / GNN"]
  MODEL --> PRED["Predicted affinity\nor binary active"]
```

The headline risk is **dataset bias**. Many MLSFs achieve high benchmark scores by
exploiting **ligand-only** or protein-family memorisation rather than learning
genuine interaction physics — they perform well on similar training data but
generalise poorly. Honest evaluation needs **scaffold/target splits** so the test
set is dissimilar to training.

```plot
{"title": "Generalisation gap as test set diverges from training", "xLabel": "test-train dissimilarity", "yLabel": "model performance", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.3*x)", "label": "memorising model", "color": "#dc2626"}, {"expr": "0.7-0.02*x", "label": "generalising model", "color": "#16a34a"}]}
```

Newer **structure-prediction-aware** tools (e.g. diffusion-based pose generators
like DiffDock, and co-folding methods extending AlphaFold-style models to ligands)
predict poses directly. They are promising but still validated against the same
physics-based and experimental yardsticks.

**Next:** validating honestly and avoiding the classic traps.
""",
        ),
        _t(
            "Bias, validation and applied pipelines",
            "13 min",
            r"""
# Bias, validation and applied pipelines

Virtual screening is easy to fool yourself with. **Analogue/decoy bias**: if decoys
differ from actives in trivial properties (size, charge), any method "works".
**Y-randomisation** and property-matched decoys (DUD-E, DEKOIS, MUV) guard against
this. **Data leakage**: overlapping train/test targets inflate ML metrics; use
**time-split** or **target-clustered** splits. **Pose vs affinity**: a method good
at geometry need not rank affinities, so validate the property you actually care
about.

```mermaid
flowchart TB
  VS["Virtual screen"] --> PROSP["Prospective validation\n(experimental hit rate)"]
  VS --> CTRL["Controls:\nDUD-E, y-randomisation"]
  VS --> SPLIT["Honest splits:\ntime / target clusters"]
  PROSP --> DECISION["Trust pipeline?"]
  CTRL --> DECISION
  SPLIT --> DECISION
```

The decisive test is **prospective**: predictions made *before* experiments, then
the predicted top compounds assayed. A realistic structure-based screen might lift
the experimental hit rate from a baseline of ~1% to 5-20% — a large practical gain
even if absolute accuracy is modest.

```plot
{"title": "Experimental hit rate: random vs enriched screen", "xLabel": "compounds tested (top k)", "yLabel": "cumulative hit rate", "xRange": [0, 10], "yRange": [0, 0.3], "grid": true, "functions": [{"expr": "0.2*exp(-0.3*x)", "label": "enriched screen", "color": "#16a34a"}, {"expr": "0.01+0*x", "label": "random baseline", "color": "#dc2626"}]}
```

A mature applied pipeline therefore funnels: filter, dock, consensus/rescore,
cluster by chemotype, expert-inspect interactions, and order a chemically diverse
shortlist for assay — feeding confirmed hits back into model retraining.

**Next:** you have completed the Molecular Docking & Virtual Screening track.
""",
        ),
        _quiz(),
    ),
)


DOCKING_VIRTUAL_SCREENING_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["DOCKING_VIRTUAL_SCREENING_COURSES"]
