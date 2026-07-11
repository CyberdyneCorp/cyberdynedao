"""Academy seed content - AI, Digital Twins and Molecular Discovery for Chemical Engineering.

The flagship new-technology course of the Chemical Engineering track: how
artificial intelligence and data science are reshaping the discipline.
It moves from data science and machine learning for process modeling,
soft sensors and optimization, through digital twins and Industry 4.0,
into the molecular frontier - cheminformatics, ML property and reaction
prediction, generative models for molecules and materials, and
AlphaFold-style protein structure prediction driving AI drug discovery.
Every lesson is a direct explanation with a mermaid diagram and a concrete
example (a Python snippet, a data pipeline, or a design formula), followed
by a checkpoint quiz; the course closes with a comprehensive final quiz.
"""

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


_AI_DIGITAL_CHEMICAL_ENGINEERING = SeedCourse(
    slug="ai-digital-chemical-engineering",
    title="AI, Digital Twins & Molecular Discovery for Chemical Engineering",
    description=(
        "How AI is transforming chemical engineering: machine learning for "
        "process modeling, soft sensors and optimization; digital twins and "
        "Industry 4.0; and AI-driven molecular and drug discovery - "
        "cheminformatics, generative models, and AlphaFold-style protein "
        "structure prediction. Every lesson pairs a clear explanation with a "
        "mermaid diagram and a concrete Python, data-pipeline or formula example."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# AI, Digital Twins and Molecular Discovery

Chemical engineering runs on data - temperatures, flows, compositions,
spectra, and now billions of molecular structures. **Artificial
intelligence** turns that data into models that predict, optimize, and
even invent. This course connects two worlds: the **process plant**
(where machine learning tunes columns, reactors and utilities in real
time) and the **molecule** (where AI discovers new drugs, catalysts and
materials).

The approach is **concrete**: every lesson explains one idea directly,
shows it in a short real example - a Python snippet, a data pipeline, or
a design equation - and draws it as a diagram. After each lesson there is
a short quiz; a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Data science for process engineering** - the data lifecycle
2. **Machine learning for process modeling and soft sensors**
3. **Process optimization and reinforcement learning**
4. **Digital twins and Industry 4.0**
5. **Cheminformatics and molecular representations** - SMILES, fingerprints
6. **Machine learning for property and reaction prediction**
7. **Generative AI for molecular and materials discovery**
8. **Protein structure prediction (AlphaFold) and AI-driven drug discovery**

You do not need to be a data scientist to start - just a chemical
engineer curious about where the field is going. The tools you will meet
(scikit-learn, RDKit, PyTorch, AlphaFold) are the modern working set, and
knowing where each fits makes the whole picture click.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What two worlds does this course connect?",
                    (
                        opt("Accounting and marketing"),
                        opt(
                            "The process plant (ML for units in real time) and the "
                            "molecule (AI for discovering drugs, catalysts and materials)",
                            correct=True,
                        ),
                        opt("Only web development and databases"),
                        opt("Mechanical CAD and civil engineering"),
                    ),
                    "AI reshapes both process operations and molecular design - the "
                    "course spans process ML and molecular AI.",
                ),
                q(
                    "How is each lesson structured?",
                    (
                        opt("A long lecture with no examples"),
                        opt(
                            "A direct explanation, a mermaid diagram, and a concrete "
                            "example (Python, pipeline, or formula), then a quiz",
                            correct=True,
                        ),
                        opt("Only multiple-choice questions"),
                        opt("Video only, no text"),
                    ),
                ),
            ),
        ),
        # -- 1. Data science for process engineering -------------------
        _t(
            "Data science for process engineering",
            "10 min",
            """# Data science for process engineering

Before any model, there is **data**. A modern plant streams thousands of
tags from its **DCS** (distributed control system) and **historian** (for
example OSIsoft PI or Aspen IP.21): temperatures, pressures, flows,
levels, valve positions, and lab analyses. Machine learning is only as
good as the pipeline that turns those raw tags into clean, aligned,
trustworthy features.

The **data lifecycle** for process data:

- **Ingest** - pull time series from the historian and lab (LIMS).
- **Clean** - remove sensor spikes, frozen values, and out-of-range
  points; flag periods when the unit was down.
- **Align and resample** - process tags arrive at different rates; put
  them on a common time base and handle **lab delay** (an assay may report
  an hour after the sample was taken).
- **Feature engineering** - derive rates, ratios, rolling averages, and
  known engineering quantities (for example a heat-exchanger duty).
- **Split** - separate train and test **by time**, never randomly, so you
  do not leak the future into the past.

A minimal cleaning and alignment step in Python:

```python
import pandas as pd

# raw historian export: irregular timestamps, some bad values
df = pd.read_parquet("unit42_tags.parquet")

# 1. drop physically impossible readings (sensor faults)
df.loc[(df["reactor_T"] < 0) | (df["reactor_T"] > 600), "reactor_T"] = pd.NA

# 2. put every tag on a common 1-minute grid, forward-fill short gaps
df = df.set_index("ts").resample("1min").mean().ffill(limit=5)

# 3. engineer a feature: exchanger duty  Q = m * cp * dT
df["duty_kW"] = df["feed_flow"] * 4.18 * (df["out_T"] - df["in_T"])
```

Two ideas dominate process data quality. **Steady-state detection**:
models trained on transients (startups, grade changes) behave differently
from steady operation - you often filter to steady windows. **Data
leakage**: any feature that secretly contains the answer (or future
information) inflates offline scores and fails online.

```mermaid
graph LR
    HIST["Historian and LIMS"] --> INGEST["Ingest time series"]
    INGEST --> CLEAN["Clean and flag faults"]
    CLEAN --> ALIGN["Align and resample"]
    ALIGN --> FEAT["Feature engineering"]
    FEAT --> SPLIT["Split by time"]
    SPLIT --> MODEL["Ready for modeling"]
```

Remember: in process data science, the historian is the mine, but the
pipeline - cleaning, alignment, honest time-based splits - is what makes
the ore usable.
""",
        ),
        quiz_lesson(
            "Quiz: Data science for process engineering",
            (
                q(
                    "Where does most process time-series data live in a plant?",
                    (
                        opt("In printed logbooks only"),
                        opt(
                            "In the DCS and a historian (for example OSIsoft PI or "
                            "Aspen IP.21), with lab results in a LIMS",
                            correct=True,
                        ),
                        opt("In the operators' memory"),
                        opt("Nowhere - it is not recorded"),
                    ),
                ),
                q(
                    "Why split process data by time rather than randomly?",
                    (
                        opt("Random splits are illegal"),
                        opt(
                            "A random split leaks future information into training, "
                            "inflating offline scores and failing online",
                            correct=True,
                        ),
                        opt("Time-based splits are faster to compute"),
                        opt("It makes no difference"),
                    ),
                    "Random shuffling mixes future and past; a chronological split "
                    "tests the model the way it will actually be used.",
                ),
                q(
                    "What is 'data leakage'?",
                    (
                        opt("A physical leak of process fluid"),
                        opt(
                            "A feature that secretly contains the answer or future "
                            "information, inflating offline scores",
                            correct=True,
                        ),
                        opt("Losing historian data to disk failure"),
                        opt("Sharing data between departments"),
                    ),
                ),
            ),
        ),
        # -- 2. ML for process modeling and soft sensors ---------------
        _t(
            "Machine learning for process modeling and soft sensors",
            "11 min",
            """# Machine learning for process modeling and soft sensors

Chemical engineers have always built models. **First-principles** (or
**white-box**) models come from mass and energy balances, thermodynamics
and kinetics - the equations in Aspen Plus or a reactor design. **Data-
driven** (**black-box**) models learn input-output relationships from
historian data. **Hybrid** (**grey-box**) models combine the two: physics
where you trust it, ML for the messy residual.

A flagship application is the **soft sensor** (or **inferential
sensor**). Some quality variables - product composition, a polymer's melt
index, an impurity in ppm - are measured only by a slow, expensive lab
assay or an unreliable online analyzer. A soft sensor **predicts** that
hard-to-measure variable in real time from easy-to-measure ones
(temperatures, pressures, flows), so control can act every second instead
of every hour.

A soft sensor with a gradient-boosted model:

```python
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit
import numpy as np

# X: fast process tags (T, P, flows, reflux ...); y: lab product purity
model = GradientBoostingRegressor(n_estimators=300, max_depth=3)

# honest validation: expanding time-ordered folds, never a random shuffle
cv = TimeSeriesSplit(n_splits=5)
scores = []
for tr, te in cv.split(X):
    model.fit(X[tr], y[tr])
    pred = model.predict(X[te])
    scores.append(np.sqrt(np.mean((pred - y[te]) ** 2)))   # RMSE
print("cross-validated RMSE:", np.mean(scores))
```

Classic process choices: **PLS** (partial least squares) and **PCR** for
correlated spectral or many-tag data; tree ensembles (**random forest**,
**gradient boosting**) for tabular nonlinearity; neural nets when data is
plentiful. Beyond accuracy, an industrial soft sensor needs:

- **Robustness to drift** - fouling, catalyst aging and sensor drift move
  the process; models need monitoring and periodic retraining.
- **Extrapolation awareness** - warn when inputs fall outside the training
  region instead of guessing confidently.
- **Interpretability** - engineers must trust it; feature importance and
  physical sanity matter for acceptance.

```mermaid
graph LR
    PHYS["First principles physics"] --> HYB["Hybrid grey box model"]
    DATA["Historian data"] --> HYB
    HYB --> SS["Soft sensor prediction"]
    SS --> CTRL["Real time control and monitoring"]
    DRIFT["Process drift"] --> RETRAIN["Monitor and retrain"]
    RETRAIN --> HYB
```

Remember: ML does not replace the engineering model - it fills the gaps.
Soft sensors turn a slow lab number into a live signal you can control on.
""",
        ),
        quiz_lesson(
            "Quiz: Machine learning for process modeling and soft sensors",
            (
                q(
                    "What is a soft sensor?",
                    (
                        opt("A physically soft, flexible temperature probe"),
                        opt(
                            "A model that predicts a hard-to-measure variable (for "
                            "example product purity) in real time from easy-to-measure tags",
                            correct=True,
                        ),
                        opt("A backup for the historian database"),
                        opt("A cushioned mounting for a pressure gauge"),
                    ),
                    "Inferential sensors infer a slow or expensive quality variable "
                    "from fast process measurements, enabling second-by-second control.",
                ),
                q(
                    "What is a hybrid (grey-box) model?",
                    (
                        opt("A model that uses only neural networks"),
                        opt(
                            "A combination of first-principles physics and data-driven "
                            "ML - physics where trusted, ML for the residual",
                            correct=True,
                        ),
                        opt("A model painted grey in the P and ID"),
                        opt("A model with no equations at all"),
                    ),
                ),
                q(
                    "Why must an industrial soft sensor be monitored and retrained?",
                    (
                        opt("To use more CPU"),
                        opt(
                            "Fouling, catalyst aging and sensor drift move the process "
                            "away from the training data over time",
                            correct=True,
                        ),
                        opt("Because scikit-learn models expire"),
                        opt("It never needs retraining once deployed"),
                    ),
                ),
            ),
        ),
        # -- 3. Optimization and RL ------------------------------------
        _t(
            "Process optimization and reinforcement learning",
            "11 min",
            """# Process optimization and reinforcement learning

A model that predicts is useful; a model that **decides** is
transformative. **Optimization** finds the operating point that maximizes
an objective (yield, profit, energy efficiency) subject to constraints
(safety limits, purity specs, equipment capacity).

The classic layered scheme in a plant:

- **RTO** - real-time optimization sets the best steady-state targets
  (setpoints) from a rigorous economic model, minutes to hours.
- **APC / MPC** - model predictive control drives the process to those
  setpoints, respecting constraints, seconds to minutes.
- **Regulatory control** - PID loops act instant to instant.

A general nonlinear program for an operating point:

```text
maximize    profit(x)  =  revenue(products) - cost(feed, energy)
subject to  g(x) <= 0    safety and quality constraints
            h(x)  = 0    mass and energy balances
            xL <= x <= xU   valve, flow and temperature bounds
```

**Machine learning** enters in two ways. A trained model can be the fast
**surrogate** that replaces a slow rigorous simulation inside the
optimizer (thousands of evaluations become milliseconds). And
**reinforcement learning (RL)** learns a control **policy** by trial and
error against a simulator: an **agent** observes the process **state**,
takes an **action** (adjust setpoints), and receives a **reward** (profit
minus constraint penalties), improving over many episodes.

```python
# reward shaping for an RL controller of a distillation column
def reward(state, action, next_state):
    profit = value(next_state["distillate"]) - energy_cost(action["reboiler_Q"])
    penalty = 0.0
    if next_state["impurity_ppm"] > 50:      # off-spec product
        penalty += 100.0
    if next_state["flooding_margin"] < 0:    # unsafe hydraulics
        penalty += 500.0
    return profit - penalty
```

RL is powerful but demanding: it needs a **faithful simulator** (you do
not explore on the real plant), careful reward design, and guardrails so
the learned policy never proposes an unsafe action. In practice RL and MPC
increasingly blend - RL for hard nonlinear or economic trade-offs, MPC's
constraint handling for safety.

```mermaid
graph TD
    RTO["RTO economic setpoints"] --> MPC["MPC drives to setpoints"]
    MPC --> PID["PID regulatory loops"]
    PID --> PLANT["Plant"]
    PLANT --> STATE["State measurements"]
    STATE --> AGENT["RL agent"]
    AGENT --> REWARD["Reward profit minus penalties"]
    REWARD --> AGENT
```

Remember: prediction tells you what will happen; optimization and RL
decide what to do about it - always inside hard safety constraints.
""",
        ),
        quiz_lesson(
            "Quiz: Process optimization and reinforcement learning",
            (
                q(
                    "In the layered control scheme, what does RTO do?",
                    (
                        opt("Acts instant to instant like a PID loop"),
                        opt(
                            "Sets the best steady-state setpoints from an economic model, "
                            "over minutes to hours",
                            correct=True,
                        ),
                        opt("Cleans the historian data"),
                        opt("Trains the soft sensor"),
                    ),
                    "RTO sets economic targets; MPC drives to them under constraints; "
                    "PID acts moment to moment.",
                ),
                q(
                    "In reinforcement learning terms, what is the 'reward'?",
                    (
                        opt("The training dataset"),
                        opt(
                            "A scalar signal (for example profit minus constraint "
                            "penalties) the agent tries to maximize over episodes",
                            correct=True,
                        ),
                        opt("The neural network's weights"),
                        opt("The number of sensors"),
                    ),
                ),
                q(
                    "Why is RL usually trained against a simulator, not the live plant?",
                    (
                        opt("Simulators are cheaper to license"),
                        opt(
                            "Trial-and-error exploration on a real plant would risk "
                            "unsafe or off-spec operation",
                            correct=True,
                        ),
                        opt("The real plant has no sensors"),
                        opt("RL cannot read real data"),
                    ),
                ),
            ),
        ),
        # -- 4. Digital twins and Industry 4.0 -------------------------
        _t(
            "Digital twins and Industry 4.0",
            "11 min",
            """# Digital twins and Industry 4.0

A **digital twin** is a living, data-connected virtual replica of a
physical asset - a reactor, a compressor, a whole plant - kept in sync
with reality by a continuous stream of sensor data. Unlike a one-off
design simulation, a twin **updates as the asset changes**: it reflects
today's fouling, catalyst activity and equipment health, not the
brand-new design case.

Digital twins sit at the heart of **Industry 4.0** - the convergence of
**IIoT** (industrial internet of things sensors), cloud and edge
computing, big-data historians, and AI. The pattern:

- **Instrument** - IIoT sensors and the DCS stream live data.
- **Model** - a first-principles simulator (Aspen HYSYS, gPROMS, DWSIM)
  and/or ML surrogates form the twin.
- **Sync** - the twin's parameters are continuously updated (data
  assimilation) so it tracks the real asset.
- **Act** - the twin enables what-if studies, predictive maintenance,
  operator training, and optimization - safely, in silico.

A twin unlocks capabilities that are impractical on the real plant:

- **Predictive maintenance** - detect a compressor bearing degrading or a
  heat exchanger fouling before it trips, and schedule the fix.
- **What-if and soft commissioning** - test a new feed or setpoint on the
  twin before touching the plant.
- **Operator training simulators** - practice startups and upsets with no
  real risk.

```python
# data assimilation: nudge the twin's fouling parameter toward reality
def update_twin(twin_state, measured, learning_rate=0.1):
    predicted = twin_state.simulate()          # model's current guess
    error = measured["outlet_T"] - predicted["outlet_T"]
    # correct the fouling resistance so the twin tracks the real exchanger
    twin_state.fouling_R += learning_rate * error * twin_state.sensitivity
    return twin_state
```

The twin's value grows with **fidelity** and **freshness**: a model that
lags reality misleads. Good twins pair rigorous physics with ML surrogates
for speed and with anomaly detection on the model-vs-measurement residual.

```mermaid
graph LR
    ASSET["Physical asset"] --> IIOT["IIoT sensors and DCS"]
    IIOT --> TWIN["Digital twin model"]
    TWIN --> SYNC["Data assimilation sync"]
    SYNC --> TWIN
    TWIN --> MAINT["Predictive maintenance"]
    TWIN --> WHATIF["What if and optimization"]
    TWIN --> TRAIN["Operator training"]
```

Remember: a digital twin is not a static model - it is a virtual asset
that learns from its physical counterpart in real time and lets you test
the future before you live it.
""",
        ),
        quiz_lesson(
            "Quiz: Digital twins and Industry 4.0",
            (
                q(
                    "How does a digital twin differ from a one-off design simulation?",
                    (
                        opt("It runs on paper instead of a computer"),
                        opt(
                            "It stays continuously synced with live sensor data, "
                            "reflecting the asset's current condition, not the design case",
                            correct=True,
                        ),
                        opt("It cannot use first-principles physics"),
                        opt("It is only a 3D rendering with no data"),
                    ),
                    "A twin is a living replica updated by streaming data; a design sim "
                    "is a static snapshot of the new-equipment case.",
                ),
                q(
                    "Which is a core Industry 4.0 enabler for digital twins?",
                    (
                        opt("Fax machines"),
                        opt(
                            "IIoT sensors streaming live data into cloud or edge compute "
                            "and AI models",
                            correct=True,
                        ),
                        opt("Manual daily logbook entries only"),
                        opt("Disconnecting the plant from any network"),
                    ),
                ),
                q(
                    "Which is a classic digital-twin use case?",
                    (
                        opt(
                            "Predictive maintenance - catch fouling or a bearing "
                            "degrading before it trips",
                            correct=True,
                        ),
                        opt("Printing invoices"),
                        opt("Replacing the plant's steel with plastic"),
                        opt("Deleting the historian"),
                    ),
                ),
            ),
        ),
        # -- 5. Cheminformatics and molecular representations ----------
        _t(
            "Cheminformatics and molecular representations",
            "11 min",
            """# Cheminformatics and molecular representations

To let a computer reason about **molecules**, you must represent them as
data. **Cheminformatics** is the discipline of encoding, storing,
searching and computing over chemical structures - the bridge between
chemistry and machine learning.

The most common text representation is **SMILES** (Simplified Molecular
Input Line Entry System): a compact ASCII string for a molecule's graph.

```text
Ethanol         CCO
Benzene         c1ccccc1
Acetic acid     CC(=O)O
Aspirin         CC(=O)Oc1ccccc1C(=O)O
Caffeine        Cn1cnc2c1c(=O)n(C)c(=O)n2C
```

Atoms are letters; lowercase means aromatic; branches use parentheses;
ring-closure digits pair bonded atoms. Because one molecule can have many
valid SMILES, a **canonical SMILES** algorithm gives each structure a
single unique string. Related formats: **InChI** (a standardized IUPAC
identifier) and **InChIKey** (a fixed-length hash for database lookup).

For machine learning, molecules become fixed-length **descriptors** or
**fingerprints**:

- **Descriptors** - computed physicochemical numbers: molecular weight,
  **logP** (lipophilicity), topological polar surface area (**TPSA**),
  hydrogen-bond donors and acceptors, rotatable bonds. These underlie
  rules of thumb like **Lipinski's rule of five** for oral drugs.
- **Fingerprints** - bit vectors encoding which substructures are present.
  **Morgan / ECFP** fingerprints hash circular atom neighborhoods into a
  binary vector; molecular similarity is then the **Tanimoto** coefficient
  between two bit vectors.

Using **RDKit**, the standard open-source cheminformatics toolkit:

```python
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem, DataStructs

mol = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")   # aspirin
print("MW   :", round(Descriptors.MolWt(mol), 1))    # 180.2
print("logP :", round(Descriptors.MolLogP(mol), 2))  # ~1.31
print("HBD  :", Descriptors.NumHDonors(mol))         # 1

# ECFP4 fingerprint and Tanimoto similarity to another molecule
fp1 = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)
fp2 = AllChem.GetMorganFingerprintAsBitVect(
    Chem.MolFromSmiles("CC(=O)Oc1ccccc1"), 2, 2048)
print("Tanimoto:", round(DataStructs.TanimotoSimilarity(fp1, fp2), 3))
```

More expressive still, a **molecular graph** (atoms as nodes, bonds as
edges) feeds a **graph neural network** that learns its own
representation - the frontier we build on in later lessons.

```mermaid
graph LR
    MOL["Molecule structure"] --> SMILES["SMILES string"]
    SMILES --> CANON["Canonical SMILES or InChI"]
    MOL --> DESC["Descriptors MW logP TPSA"]
    MOL --> FP["Morgan ECFP fingerprint"]
    MOL --> GRAPH["Molecular graph"]
    FP --> TANI["Tanimoto similarity"]
    GRAPH --> GNN["Graph neural network"]
```

Remember: a molecule is a graph. SMILES writes it as text, descriptors and
fingerprints turn it into a vector, and graph learning lets the model
build its own - all so machines can search and predict chemistry.
""",
        ),
        quiz_lesson(
            "Quiz: Cheminformatics and molecular representations",
            (
                q(
                    "What is a SMILES string?",
                    (
                        opt("A photograph of a molecule"),
                        opt(
                            "A compact ASCII text encoding of a molecule's graph "
                            "(atoms, bonds, rings, branches)",
                            correct=True,
                        ),
                        opt("A 3D crystal structure file"),
                        opt("A spectroscopy measurement"),
                    ),
                    "SMILES writes the molecular graph as a line of text; canonical "
                    "SMILES gives each structure one unique string.",
                ),
                q(
                    "What does a Morgan / ECFP fingerprint encode?",
                    (
                        opt("The molecule's price"),
                        opt(
                            "A bit vector of which circular substructures are present, "
                            "used for similarity search",
                            correct=True,
                        ),
                        opt("The exact 3D coordinates of every atom"),
                        opt("The synthesis cost in dollars"),
                    ),
                ),
                q(
                    "How is similarity between two fingerprints commonly measured?",
                    (
                        opt("Euclidean distance in kilograms"),
                        opt("The Tanimoto coefficient between the bit vectors", correct=True),
                        opt("The difference in boiling points"),
                        opt("Their alphabetical order"),
                    ),
                ),
            ),
        ),
        # -- 6. ML for property and reaction prediction ----------------
        _t(
            "Machine learning for property and reaction prediction",
            "11 min",
            """# Machine learning for property and reaction prediction

Once molecules are vectors or graphs, machine learning can **predict what
they will do** - long before you synthesize or test them. This is the
engine of modern discovery: score millions of candidates in silico, then
make only the promising few.

**Property prediction** (a **QSAR/QSPR** task - quantitative structure-
activity/property relationship) maps a structure to a number or class:

- **Physicochemical** - solubility, logP, melting point, boiling point.
- **ADMET** - absorption, distribution, metabolism, excretion, toxicity;
  the drug-likeness properties that decide whether a molecule can be a
  medicine.
- **Bioactivity** - binding affinity or inhibition against a target.

Two modeling families dominate. **Descriptor/fingerprint models** feed the
fixed vectors of the previous lesson into gradient boosting or a random
forest - fast, strong baselines. **Graph neural networks (GNNs)** operate
directly on the molecular graph, learning features by **message passing**:
each atom repeatedly aggregates information from its bonded neighbors, so
the network discovers the relevant substructures itself.

```python
import torch, torch.nn as nn
from torch_geometric.nn import GCNConv, global_mean_pool

class MolGNN(nn.Module):
    "Predict a molecular property from the atom-bond graph."
    def __init__(self, in_dim, hidden=64):
        super().__init__()
        self.c1 = GCNConv(in_dim, hidden)   # message passing layer 1
        self.c2 = GCNConv(hidden, hidden)   # message passing layer 2
        self.head = nn.Linear(hidden, 1)    # regress one property

    def forward(self, x, edge_index, batch):
        x = torch.relu(self.c1(x, edge_index))
        x = torch.relu(self.c2(x, edge_index))
        x = global_mean_pool(x, batch)      # graph-level readout
        return self.head(x)                 # e.g. predicted solubility
```

**Reaction prediction** turns ML toward synthesis. **Forward prediction**
asks "given these reactants and conditions, what product forms?"
**Retrosynthesis** runs it backward: "given a target molecule, what
reactions could make it?" Modern systems (for example transformer models
trained on reaction SMILES, as in IBM RXN) treat reactions like a
translation problem, and **synthesizability** scoring keeps generated
ideas realistic.

A recurring pitfall is **applicability domain**: a QSAR model is reliable
only for molecules resembling its training set. Predicting far outside
that chemical space is extrapolation, and honest pipelines flag it and
report **uncertainty**, not just a point estimate.

```mermaid
graph TD
    STRUCT["Molecular structure"] --> FEAT["Fingerprint or graph"]
    FEAT --> QSAR["QSAR property model"]
    FEAT --> GNN["Graph neural network"]
    QSAR --> PROP["Predicted property or ADMET"]
    GNN --> PROP
    STRUCT --> RXN["Reaction and retrosynthesis model"]
    RXN --> ROUTE["Predicted product or synthesis route"]
```

Remember: property and reaction models let you triage chemistry
computationally - but only within the applicability domain they were
trained on. Trust with uncertainty, then validate in the lab.
""",
        ),
        quiz_lesson(
            "Quiz: Machine learning for property and reaction prediction",
            (
                q(
                    "What does a QSAR/QSPR model do?",
                    (
                        opt("Draws the molecule in 3D"),
                        opt(
                            "Maps a molecular structure to a predicted property or "
                            "activity (for example solubility, toxicity, binding)",
                            correct=True,
                        ),
                        opt("Measures the boiling point in a lab"),
                        opt("Prices the molecule for sale"),
                    ),
                    "Quantitative structure-activity/property relationships predict "
                    "behavior from structure, enabling in-silico triage.",
                ),
                q(
                    "How does a graph neural network learn molecular features?",
                    (
                        opt("By reading the SMILES letter by letter as English"),
                        opt(
                            "By message passing - each atom repeatedly aggregates "
                            "information from its bonded neighbors",
                            correct=True,
                        ),
                        opt("By memorizing molecular weights only"),
                        opt("By random guessing with no training"),
                    ),
                ),
                q(
                    "What is retrosynthesis prediction?",
                    (
                        opt("Predicting a molecule's color"),
                        opt(
                            "Working backward from a target molecule to reactions that "
                            "could make it",
                            correct=True,
                        ),
                        opt("Predicting the reactor temperature"),
                        opt("Reversing a distillation column"),
                    ),
                ),
                q(
                    "What does the 'applicability domain' caveat mean?",
                    (
                        opt("The model can predict any molecule perfectly"),
                        opt(
                            "The model is reliable only for molecules resembling its "
                            "training set; far outside is extrapolation",
                            correct=True,
                        ),
                        opt("The model only works on weekdays"),
                        opt("The model needs no validation"),
                    ),
                ),
            ),
        ),
        # -- 7. Generative AI for molecules and materials --------------
        _t(
            "Generative AI for molecular and materials discovery",
            "11 min",
            """# Generative AI for molecular and materials discovery

Prediction scores molecules that already exist. **Generative AI** does
something bolder: it **invents new ones**. Instead of searching a
catalogue, a generative model proposes novel structures optimized toward a
goal - high potency, low toxicity, a target band gap, an easier synthesis.
This is **inverse design**: specify the properties you want, and let the
model design molecules to match.

The main model families:

- **Variational autoencoders (VAEs)** - learn a continuous **latent
  space** of molecules; you optimize a property by moving through that
  space and decoding back to a structure.
- **Generative adversarial networks (GANs)** - a generator invents
  molecules while a discriminator judges realism.
- **Autoregressive and transformer models** - generate SMILES or graphs
  token by token, like a language model for chemistry.
- **Diffusion models** - increasingly used to generate 3D structures by
  denoising, including molecules directly in a protein pocket.

Generation is steered by **optimization**: reinforcement learning or
Bayesian optimization pushes the generator toward a **multi-objective**
target (potency AND solubility AND synthesizability), and a **scoring
function** (often the QSAR/property models from the previous lesson)
grades every proposal.

```python
# a design-make-test loop for generative molecular discovery
def optimize(generator, score_fn, steps=1000):
    best = []
    for _ in range(steps):
        candidates = generator.sample(batch=128)       # invent molecules
        scored = [(m, score_fn(m)) for m in candidates] # multi-objective score
        elite = top_k(scored, k=16)                     # keep the best
        generator.reinforce(elite)                      # bias toward them
        best = merge_best(best, elite)
    return dedupe_valid(best)                           # novel, valid, high-scoring
```

The same idea extends beyond drugs to **materials discovery** - proposing
polymers, catalysts, battery electrolytes and metal-organic frameworks
with target properties, a core method in the **Materials Genome** effort.

Two guardrails separate hype from value. **Validity and novelty**: a good
generator produces chemically valid, genuinely new structures, not
duplicates or nonsense. **Synthesizability**: a molecule you cannot make
is useless, so scores include a synthetic-accessibility term, and the loop
closes with real lab synthesis and testing - the **design-make-test**
cycle, now accelerated by self-driving labs.

```mermaid
graph LR
    GOAL["Target properties"] --> GEN["Generative model"]
    GEN --> CAND["Candidate molecules"]
    CAND --> SCORE["Multi objective scoring"]
    SCORE --> OPT["Optimize and reinforce"]
    OPT --> GEN
    SCORE --> LAB["Design make test in lab"]
    LAB --> GOAL
```

Remember: generative AI turns discovery from search into design - you
state the properties you want and the model invents candidates, but only
valid, novel and makeable molecules count.
""",
        ),
        quiz_lesson(
            "Quiz: Generative AI for molecular and materials discovery",
            (
                q(
                    "What is 'inverse design' in generative molecular discovery?",
                    (
                        opt("Designing a molecule backward alphabetically"),
                        opt(
                            "Specifying the properties you want and letting a model "
                            "design molecules to match",
                            correct=True,
                        ),
                        opt("Only screening an existing catalogue"),
                        opt("Reversing a chemical reaction physically"),
                    ),
                    "Instead of searching known molecules, inverse design generates new "
                    "ones optimized toward target properties.",
                ),
                q(
                    "Why include a synthesizability (synthetic-accessibility) term in the score?",
                    (
                        opt("To make the model run slower"),
                        opt(
                            "A molecule you cannot actually make is useless, however good "
                            "its predicted properties",
                            correct=True,
                        ),
                        opt("Because SMILES require it"),
                        opt("To increase the molecular weight"),
                    ),
                ),
                q(
                    "Beyond drugs, generative models are used for what?",
                    (
                        opt("Only for writing marketing copy"),
                        opt(
                            "Materials discovery - polymers, catalysts, battery "
                            "electrolytes and MOFs with target properties",
                            correct=True,
                        ),
                        opt("Predicting the weather"),
                        opt("Nothing else"),
                    ),
                ),
            ),
        ),
        # -- 8. AlphaFold and AI drug discovery ------------------------
        _t(
            "Protein structure prediction and AI-driven drug discovery",
            "12 min",
            """# Protein structure prediction and AI-driven drug discovery

Most drugs work by binding a **protein target** - an enzyme or receptor -
and a protein's **3D shape** determines what binds it. For fifty years,
predicting that shape from the amino-acid sequence was biology's grand
challenge (the **protein folding problem**). Experimental structures come
from slow X-ray crystallography or cryo-EM; most proteins had none.

In 2020, **DeepMind's AlphaFold 2** effectively solved single-chain
prediction at the CASP14 assessment, reaching near-experimental accuracy
from sequence alone. It combines a **multiple sequence alignment** (which
co-evolving residues reveal contacts) with an attention-based
**Evoformer** and a structure module that outputs 3D coordinates, plus a
per-residue confidence score (**pLDDT**). The **AlphaFold Protein
Structure Database** then released predicted structures for over 200
million proteins - nearly every known protein. **AlphaFold 3** (2024)
extended this to complexes of proteins with ligands, nucleic acids and
ions - directly relevant to drug binding.

Why this matters for a chemical engineer in drug discovery: a reliable
structure unlocks **structure-based drug design**.

```mermaid
graph TD
    SEQ["Protein sequence"] --> MSA["Multiple sequence alignment"]
    MSA --> AF["AlphaFold Evoformer"]
    AF --> STRUCT["Predicted 3D structure"]
    STRUCT --> DOCK["Molecular docking"]
    LIB["Molecule library"] --> DOCK
    DOCK --> HITS["Ranked binders"]
    HITS --> GEN["Generative design in pocket"]
    GEN --> DMT["Design make test"]
    DMT --> LIB
```

The AI-driven discovery pipeline chains everything in this course:

- **Target structure** - AlphaFold (or experiment) gives the binding site.
- **Virtual screening / docking** - **molecular docking** poses each
  candidate in the pocket and scores the fit, ranking millions in silico.
- **Property and ADMET filtering** - the QSAR/GNN models predict potency,
  solubility and toxicity to triage hits.
- **Generative design** - generative models grow or optimize molecules
  directly for that pocket (structure-based generation).
- **Design-make-test** - the best candidates are synthesized and assayed;
  results retrain the models. Increasingly this loop runs in **self-
  driving labs** with robotic synthesis.

A simple hit-triage rule combining docking with drug-likeness:

```python
def is_promising(mol):
    dock = docking_score(mol, pocket="target.pdb")   # more negative = tighter
    tox  = admet_model.predict_toxicity(mol)         # 0..1 risk
    return dock < -8.0 and tox < 0.3 and lipinski_ok(mol)
```

None of this replaces the wet lab - predictions still need experimental
validation, and biology is full of surprises. But the shift is real: AI
compresses discovery from years of blind screening to a guided, in-silico-
first search. Companies from Isomorphic Labs to Recursion now build drug
pipelines around exactly this stack.

Remember: AlphaFold turned "we cannot see the target" into "here is its
structure", and that unlocks a computational discovery loop - predict the
structure, dock and screen, generate and optimize, then make and test.
""",
        ),
        quiz_lesson(
            "Quiz: Protein structure prediction and AI-driven drug discovery",
            (
                q(
                    "What problem did AlphaFold 2 (2020) largely solve?",
                    (
                        opt("Predicting the stock market"),
                        opt(
                            "Predicting a protein's 3D structure from its amino-acid "
                            "sequence at near-experimental accuracy",
                            correct=True,
                        ),
                        opt("Synthesizing proteins in a reactor"),
                        opt("Measuring reaction kinetics"),
                    ),
                    "AlphaFold cracked single-chain structure prediction at CASP14 and "
                    "released structures for over 200 million proteins.",
                ),
                q(
                    "Why does a protein's 3D structure matter for drug discovery?",
                    (
                        opt("It sets the drug's price"),
                        opt(
                            "The binding-site shape determines what molecules bind, "
                            "enabling structure-based drug design and docking",
                            correct=True,
                        ),
                        opt("It has no relevance to binding"),
                        opt("It only matters for cosmetics"),
                    ),
                ),
                q(
                    "What does molecular docking do in the pipeline?",
                    (
                        opt("Physically synthesizes the molecule"),
                        opt(
                            "Poses each candidate molecule in the target's pocket and "
                            "scores the fit, ranking many in silico",
                            correct=True,
                        ),
                        opt("Measures toxicity in animals"),
                        opt("Prints the protein on paper"),
                    ),
                ),
                q(
                    "What still remains essential despite AI-driven discovery?",
                    (
                        opt("Nothing - AI removes all experiments"),
                        opt(
                            "Experimental validation in the wet lab - predictions must be "
                            "synthesized and tested",
                            correct=True,
                        ),
                        opt("Ignoring the predictions entirely"),
                        opt("Only manual literature reading"),
                    ),
                    "AI compresses and guides discovery, but the design-make-test loop "
                    "still closes with real synthesis and assay.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Before any model, what makes process machine learning succeed or fail?",
                    (
                        opt("The color of the dashboard"),
                        opt(
                            "The data pipeline - cleaning, aligning, and splitting "
                            "historian and lab data honestly by time",
                            correct=True,
                        ),
                        opt("The number of monitors in the control room"),
                        opt("The brand of the sensors only"),
                    ),
                    "Garbage in, garbage out: a trustworthy pipeline with time-based "
                    "splits is the foundation.",
                ),
                q(
                    "A soft sensor is best described as:",
                    (
                        opt("A physically flexible probe"),
                        opt(
                            "A model predicting a hard-to-measure quality variable in "
                            "real time from easy-to-measure tags",
                            correct=True,
                        ),
                        opt("A backup power supply"),
                        opt("A type of distillation tray"),
                    ),
                ),
                q(
                    "In the layered scheme, which layer sets economic steady-state setpoints?",
                    (
                        opt("PID regulatory control"),
                        opt("RTO real-time optimization", correct=True),
                        opt("The historian"),
                        opt("The soft sensor"),
                    ),
                    "RTO sets targets, MPC drives to them under constraints, PID acts "
                    "moment to moment.",
                ),
                q(
                    "What distinguishes a digital twin from a static design simulation?",
                    (
                        opt("It is drawn in 2D"),
                        opt(
                            "It stays continuously synced with live sensor data and "
                            "reflects the asset's current condition",
                            correct=True,
                        ),
                        opt("It uses no physics"),
                        opt("It runs only once at design time"),
                    ),
                ),
                q(
                    "What does a SMILES string represent?",
                    (
                        opt("A spectrum"),
                        opt(
                            "A molecule's graph encoded as a compact ASCII text string",
                            correct=True,
                        ),
                        opt("A reactor's P and ID"),
                        opt("A price quote"),
                    ),
                ),
                q(
                    "Morgan/ECFP fingerprints plus the Tanimoto coefficient are used to:",
                    (
                        opt("Measure temperature"),
                        opt(
                            "Encode substructures as a bit vector and compute molecular similarity",
                            correct=True,
                        ),
                        opt("Balance a mass balance"),
                        opt("Size a pump"),
                    ),
                ),
                q(
                    "A graph neural network learns molecular features by:",
                    (
                        opt("Reading SMILES as English sentences"),
                        opt(
                            "Message passing - atoms aggregate information from bonded "
                            "neighbors across layers",
                            correct=True,
                        ),
                        opt("Weighing the sample"),
                        opt("Guessing randomly"),
                    ),
                ),
                q(
                    "Generative molecular AI differs from property prediction because it:",
                    (
                        opt("Only screens existing molecules"),
                        opt(
                            "Invents novel candidate structures optimized toward target "
                            "properties (inverse design)",
                            correct=True,
                        ),
                        opt("Cannot produce new molecules"),
                        opt("Measures boiling points"),
                    ),
                ),
                q(
                    "What did AlphaFold achieve, and why does it matter for drug discovery?",
                    (
                        opt("It synthesizes drugs automatically in a reactor"),
                        opt(
                            "It predicts protein 3D structure from sequence, unlocking "
                            "structure-based design and docking against the target",
                            correct=True,
                        ),
                        opt("It sets drug prices"),
                        opt("It has no role in drug discovery"),
                    ),
                    "A predicted binding-site structure lets you dock, screen and "
                    "generate molecules for that pocket.",
                ),
                q(
                    "Across process AI and molecular AI, what remains essential?",
                    (
                        opt("Trusting every prediction blindly"),
                        opt(
                            "Validation - monitoring and retraining process models, and "
                            "synthesizing and testing generated molecules in the lab",
                            correct=True,
                        ),
                        opt("Never measuring anything again"),
                        opt("Removing all human engineers"),
                    ),
                    "AI guides and accelerates, but honest validation - online for "
                    "process models, wet-lab for molecules - closes the loop.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

AI_DIGITAL_CHEMICAL_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (
    _AI_DIGITAL_CHEMICAL_ENGINEERING,
)
