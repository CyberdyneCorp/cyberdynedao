"""Evolution & Ecology track: Basics -> Intermediate -> Advanced.

A university-level curriculum from variation and natural selection, through
phylogenetics, speciation, population genetics and molecular evolution, to
community ecology, population dynamics, coevolution and evolutionary medicine.
Lessons use interactive ```plot blocks for quantitative relationships (growth,
selection, decay, dose-response) and ```mermaid diagrams for processes,
classifications and analytical pipelines.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Evolution & Ecology -- Basics --------------------------------------------

_BASICS = SeedCourse(
    slug="evolution-ecology-basics",
    title="Evolution & Ecology — Basics",
    description=(
        "The core logic of evolution: where heritable variation comes from, how "
        "natural selection acts on it, the four forces of evolutionary change, "
        "the evidence for common descent, and the ecological stage on which it "
        "all plays out. Built on real biological detail with interactive plots "
        "and process diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Variation: the raw material of evolution",
            "10 min",
            r"""
# Variation: the raw material of evolution

Evolution acts only on **heritable variation**. Individuals in a population
differ in **phenotype** (observable traits) because they differ in **genotype**
(DNA sequence) and in environment. Only the genetic component is passed on, so
only it can fuel long-term change.

The ultimate source of new variation is **mutation**: errors in DNA replication,
plus damage from radiation and chemicals. Most point mutations are neutral or
mildly deleterious; rarely one is beneficial. **Recombination** during meiosis
then shuffles existing alleles into new combinations, and **gene flow** imports
alleles from other populations.

```mermaid
flowchart LR
  MUT["Mutation (new alleles)"] --> POOL["Gene pool: allele frequencies"]
  REC["Recombination (new combinations)"] --> POOL
  FLOW["Gene flow (migration)"] --> POOL
  POOL --> PHEN["Phenotypic variation"]
```

Many traits are **quantitative** — height, beak depth, growth rate — controlled
by many genes plus environment, and so are roughly normally distributed in a
population. The spread of that distribution, the **variance**, is what selection
has to work with: no variance, no response.

```plot
{"title": "Normal distribution of a quantitative trait", "xLabel": "trait value (standardized)", "yLabel": "frequency", "xRange": [-4, 4], "yRange": [0, 0.5], "grid": true, "functions": [{"expr": "exp(-(x*x)/2)/sqrt(2*3.14159)", "label": "trait frequency", "color": "#2563eb"}]}
```

**Next:** how natural selection turns variation into adaptation.
""",
        ),
        _t(
            "Natural selection and adaptation",
            "11 min",
            r"""
# Natural selection and adaptation

Darwin's argument is a logical syllogism. Given (1) heritable variation, (2) more
offspring than can survive, and (3) variation in **fitness** — the expected
number of surviving, reproducing offspring — then the alleles of the fitter
variants increase in frequency. This is **natural selection**.

Selection is the only evolutionary force that reliably builds **adaptation**:
traits that improve survival and reproduction in a given environment. It is not
random — but it has no foresight. It works on what is available, producing
"good enough" solutions full of historical constraints (the vertebrate eye's
blind spot, the recurrent laryngeal nerve).

```mermaid
flowchart LR
  VAR["Heritable variation"] --> COMP["Overproduction + competition"]
  COMP --> DIFF["Differential survival/reproduction (fitness)"]
  DIFF --> SHIFT["Allele frequency shift"]
  SHIFT --> ADAPT["Adaptation"]
```

Selection comes in modes. **Directional** selection favours one extreme (peppered
moths darkening with soot). **Stabilizing** selection favours the mean (human
birth weight). **Disruptive** selection favours both extremes. A simple way to
see directional selection on an allele is **logistic spread**: a favoured allele
rises slowly, accelerates, then saturates near fixation.

```plot
{"title": "Spread of a beneficial allele over time", "xLabel": "generations", "yLabel": "allele frequency", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "frequency of favoured allele", "color": "#16a34a"}]}
```

**Next:** the four forces that change allele frequencies.
""",
        ),
        _t(
            "The four forces of evolution",
            "12 min",
            r"""
# The four forces of evolution

Evolution is, mechanically, **change in allele frequencies** across generations.
Four processes drive it. Selection is only one of them.

- **Mutation** introduces new alleles, but is too slow alone to shift frequencies
  much per generation (rates ~$10^{-8}$ per site).
- **Natural selection** systematically favours alleles by their fitness effects.
- **Genetic drift** is random change from finite sampling of gametes; it is
  strong in **small populations** and can fix or lose alleles by chance.
- **Gene flow** (migration) mixes populations, homogenising their gene pools and
  opposing divergence.

```mermaid
flowchart TB
  GP["Gene pool"] --> MUT["Mutation: + new alleles"]
  GP --> SEL["Selection: directional, non-random"]
  GP --> DRIFT["Drift: random, ~1/N strength"]
  GP --> FLOW["Gene flow: homogenising"]
```

Drift matters because its strength scales with **1/N** (N = population size).
In a small population, allele frequencies wander widely each generation; in a
large one they are stable. This is why bottlenecks and founder events erode
diversity. The expected loss of heterozygosity per generation is $1/(2N)$, so
the heterozygosity remaining falls geometrically with population size.

```plot
{"title": "Strength of genetic drift versus population size", "xLabel": "population size N", "yLabel": "drift variance ~ 1/(2N)", "xRange": [1, 20], "yRange": [0, 0.5], "grid": true, "functions": [{"expr": "1/(2*x)", "label": "drift per generation", "color": "#dc2626"}]}
```

**Next:** the lines of evidence that evolution has happened.
""",
        ),
        _t(
            "Evidence for common descent",
            "11 min",
            r"""
# Evidence for common descent

Evolution is supported by independent, converging lines of evidence. **Comparative
anatomy** reveals **homologous** structures — the same bones (humerus, radius,
ulna) repurposed in a human arm, a bat wing and a whale flipper — pointing to
shared ancestry, distinct from **analogous** structures (insect vs bird wings)
shaped by convergent selection.

```mermaid
flowchart LR
  ANC["Common ancestor"] --> H1["Human arm"]
  ANC --> H2["Bat wing"]
  ANC --> H3["Whale flipper"]
  H1 --> HOM["Homology: same bones, different use"]
  H2 --> HOM
  H3 --> HOM
```

**The fossil record** documents transitional forms (Tiktaalik between fish and
tetrapods; Archaeopteryx between dinosaurs and birds) and ordered appearance in
rock strata. **Biogeography** explains odd distributions — marsupials in
Australia — by isolation and descent. **Molecular biology** is the strongest
witness: the near-universal genetic code, and **sequence divergence** that
accumulates with time so that more distantly related species share fewer
identical residues. The fraction of conserved sites decays roughly exponentially
with divergence time.

```plot
{"title": "Sequence identity decaying with divergence time", "xLabel": "divergence time (relative)", "yLabel": "fraction identical sites", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "conserved fraction", "color": "#2563eb"}]}
```

**Next:** the ecological context where selection happens.
""",
        ),
        _t(
            "Ecology: the stage for selection",
            "11 min",
            r"""
# Ecology: the stage for selection

**Ecology** studies how organisms interact with each other and their environment.
It supplies the selective pressures that drive evolution, and evolution shapes
the players in ecology — the two are inseparable.

The hierarchy runs from **individual** to **population** (same species, one area),
**community** (all interacting species), **ecosystem** (community plus abiotic
environment), to **biosphere**. Each organism occupies an **ecological niche**:
the sum of resources and conditions it uses and tolerates.

```mermaid
flowchart TB
  IND["Individual"] --> POP["Population (one species)"]
  POP --> COM["Community (many species)"]
  COM --> ECO["Ecosystem (+ abiotic)"]
  ECO --> BIO["Biosphere"]
```

Interactions among species are the raw selective forces: **competition** (−/−),
**predation** and **parasitism** (+/−), **mutualism** (+/+) and **commensalism**
(+/0). A population growing in a finite environment cannot expand forever —
resources, predators and disease impose a **carrying capacity** ($K$). Growth is
fast when rare and slows as the population approaches $K$, the classic logistic
saturation seen everywhere in ecology.

```plot
{"title": "Logistic population growth toward carrying capacity", "xLabel": "time", "yLabel": "population size", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "N / K", "color": "#16a34a"}]}
```

**Next:** test your grasp of variation, selection and ecology.
""",
        ),
        _quiz(),
    ),
)


# -- Evolution & Ecology -- Intermediate --------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="evolution-ecology-intermediate",
    title="Evolution & Ecology — Intermediate",
    description=(
        "The quantitative core: Hardy-Weinberg equilibrium and tests for "
        "evolution, phylogenetic inference, the genetics of speciation, "
        "quantitative-genetic prediction of selection response, and the "
        "mathematics of population growth and species interactions. Worked "
        "equations, plots and analytical pipelines throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Hardy-Weinberg equilibrium",
            "12 min",
            r"""
# Hardy-Weinberg equilibrium

The **Hardy-Weinberg (HW) principle** is the null model of population genetics.
For one locus with two alleles at frequencies $p$ and $q$ ($p+q=1$), the
genotype frequencies in the next generation are $p^2$ (homozygote A), $2pq$
(heterozygote) and $q^2$ (homozygote a) — provided five conditions hold: no
mutation, no migration, no selection, random mating, and infinite population
size (no drift).

```mermaid
flowchart LR
  P["Allele freqs p, q"] --> SQ["p^2 + 2pq + q^2 = 1"]
  SQ --> EQ{Match observed?}
  EQ -->|yes| NULL["No evolution at this locus"]
  EQ -->|no| EVO["Some force acting"]
```

HW is powerful precisely because it is the **no-evolution baseline**: deviations
flag a force at work. With observed genotype counts you compute expected counts
under HW and test with a chi-square statistic, $\chi^2 = \sum (O-E)^2/E$. The
heterozygote frequency $2pq$ is maximised at $p=q=0.5$, reaching 0.5, and
vanishes as either allele becomes rare — a curve worth knowing by heart.

```plot
{"title": "Heterozygote frequency 2pq versus allele frequency", "xLabel": "allele frequency p", "yLabel": "2pq (heterozygotes)", "xRange": [0, 1], "yRange": [0, 0.6], "grid": true, "functions": [{"expr": "2*x*(1-x)", "label": "2pq", "color": "#2563eb"}]}
```

**Next:** reconstructing the tree of life from data.
""",
        ),
        _t(
            "Phylogenetics: reading the tree of life",
            "13 min",
            r"""
# Phylogenetics: reading the tree of life

A **phylogeny** is a hypothesis of evolutionary relationships, drawn as a tree
whose tips are taxa, internal nodes are common ancestors, and branch lengths can
encode time or change. Groups are defined by **shared derived characters**
(synapomorphies); a valid **clade** (monophyletic group) contains an ancestor and
all its descendants.

```mermaid
flowchart LR
  ROOT["Root: common ancestor"] --> N1["Node A"]
  ROOT --> OUT["Outgroup"]
  N1 --> T1["Taxon 1"]
  N1 --> N2["Node B"]
  N2 --> T2["Taxon 2"]
  N2 --> T3["Taxon 3"]
```

Trees are inferred from aligned molecular sequences by several criteria.
**Maximum parsimony** picks the tree needing the fewest changes. **Distance**
methods (neighbour-joining) cluster by pairwise divergence. **Maximum likelihood**
and **Bayesian** methods evaluate trees under an explicit substitution model
(e.g. Jukes-Cantor, GTR). **Bootstrapping** resamples sites to attach support
values to branches. Because multiple substitutions hide at the same site,
observed differences saturate: the true number of substitutions grows while
observed identity plateaus, the central correction all models apply.

```plot
{"title": "Observed vs true substitutions (multiple-hit saturation)", "xLabel": "true substitutions per site", "yLabel": "observed differences", "xRange": [0, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "(3/4)*(1-exp(-x))", "label": "observed (Jukes-Cantor)", "color": "#dc2626"}]}
```

**Next:** how one species becomes two.
""",
        ),
        _t(
            "Speciation and reproductive isolation",
            "12 min",
            r"""
# Speciation and reproductive isolation

Under the **biological species concept**, species are groups that actually or
potentially interbreed and are **reproductively isolated** from other such
groups. **Speciation** is the evolution of that isolation, built from
**prezygotic barriers** (habitat, temporal, behavioural, mechanical, gametic) and
**postzygotic barriers** (hybrid inviability, sterility, breakdown).

```mermaid
flowchart TB
  POP["Ancestral population"] --> ALLO["Allopatric: geographic split"]
  POP --> SYM["Sympatric: same area, niche/host shift"]
  ALLO --> DIV["Divergence by drift + selection"]
  SYM --> DIV
  DIV --> ISO["Reproductive isolation -> two species"]
```

**Allopatric** speciation, the commonest mode, begins with a geographic barrier;
isolated populations diverge by drift and divergent selection until isolation is
complete even on secondary contact. **Sympatric** speciation occurs without
geographic separation — via polyploidy (instant in plants) or host shifts.
Reinforcement can then strengthen prezygotic isolation. As lineages diverge, the
probability that hybrids are viable and fertile declines with genetic distance,
producing the empirical rise of reproductive isolation with divergence time.

```plot
{"title": "Reproductive isolation accumulating with divergence", "xLabel": "genetic distance (relative)", "yLabel": "reproductive isolation", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.4*x)", "label": "isolation index", "color": "#16a34a"}]}
```

**Next:** predicting the response to selection quantitatively.
""",
        ),
        _t(
            "Quantitative genetics and the breeder's equation",
            "13 min",
            r"""
# Quantitative genetics and the breeder's equation

Most ecologically important traits are **quantitative**, shaped by many loci plus
environment. We partition phenotypic variance: $V_P = V_G + V_E$, where genetic
variance splits further into additive, dominance and epistatic parts. The key
quantity is **narrow-sense heritability**, $h^2 = V_A / V_P$ — the fraction of
variance due to additively transmitted genes.

```mermaid
flowchart LR
  VP["V_P (phenotype)"] --> VG["V_G (genetic)"]
  VP --> VE["V_E (environment)"]
  VG --> VA["V_A additive"]
  VG --> VD["V_D dominance"]
  VG --> VI["V_I epistasis"]
```

The **breeder's equation** predicts one generation of response:
$$R = h^2 S$$
where $S$ is the **selection differential** (how far the breeding parents' mean
trait departs from the population mean) and $R$ is the **response** (the shift in
the offspring mean). High heritability converts selection into rapid change; low
heritability blunts it. For a fixed selection differential, response rises
linearly with heritability — the line breeders and field biologists live by.

```plot
{"title": "Response to selection versus heritability (fixed S)", "xLabel": "heritability h^2", "yLabel": "response R (units of S)", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x", "label": "R = h^2 * S", "color": "#2563eb"}]}
```

**Next:** the dynamics of populations and their interactions.
""",
        ),
        _t(
            "Population dynamics and species interactions",
            "13 min",
            r"""
# Population dynamics and species interactions

Populations change through births, deaths, immigration and emigration. With
unlimited resources growth is **exponential**, $\frac{dN}{dt} = rN$, giving
$N(t) = N_0 e^{rt}$ and a fixed doubling time $\ln 2 / r$. Real environments
impose a **carrying capacity** $K$, yielding the **logistic** model
$\frac{dN}{dt} = rN(1 - N/K)$ that decelerates as $N \to K$.

```mermaid
flowchart LR
  EXP["Exponential: dN/dt = rN"] --> LIM["Add resource limit"]
  LIM --> LOG["Logistic: dN/dt = rN(1 - N/K)"]
  LOG --> EQ["Equilibrium at N = K"]
```

Interactions couple populations. The **Lotka-Volterra** predator-prey equations
produce out-of-phase oscillations; **competition** models predict coexistence or
exclusion depending on competition coefficients. **Density dependence** is the
engine: per-capita growth declines as the population fills its niche. Plotting
per-capita growth rate $r(1 - N/K)$ against $N$ gives a straight line falling to
zero exactly at $K$ — the signature of logistic regulation.

```plot
{"title": "Per-capita growth rate versus population size (logistic)", "xLabel": "population N (units of K)", "yLabel": "per-capita growth rate", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-x", "label": "r(1 - N/K)", "color": "#dc2626"}]}
```

**Next:** consolidate the quantitative methods.
""",
        ),
        _quiz(),
    ),
)


# -- Evolution & Ecology -- Advanced ------------------------------------------

_ADVANCED = SeedCourse(
    slug="evolution-ecology-advanced",
    title="Evolution & Ecology — Advanced",
    description=(
        "State-of-the-art and applied evolutionary biology: the molecular clock "
        "and tests for selection from genomes, coalescent and demographic "
        "inference, coevolution and the Red Queen, evolutionary medicine and "
        "antibiotic resistance, and machine-learning approaches to ecological "
        "and evolutionary genomics. Real tools, equations and pipelines."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Molecular evolution and detecting selection",
            "13 min",
            r"""
# Molecular evolution and detecting selection

At the sequence level, the **neutral theory** (Kimura) holds that most fixed
substitutions are selectively neutral, fixed by drift at a rate equal to the
mutation rate — the basis of the **molecular clock**, which makes substitutions
accumulate roughly linearly with time. Selection appears as departures from this
neutral expectation.

The workhorse test compares **nonsynonymous** ($d_N$, amino-acid-changing) and
**synonymous** ($d_S$, silent) substitution rates. The ratio
$$\omega = \frac{d_N}{d_S}$$
distinguishes regimes: $\omega < 1$ purifying selection, $\omega = 1$ neutrality,
$\omega > 1$ positive (diversifying) selection. Codon models in **PAML** and
**HyPhy** estimate $\omega$ per site or per branch; the **McDonald-Kreitman**
test and **dN/dS** scans flag adaptively evolving genes genome-wide.

```mermaid
flowchart LR
  ALN["Codon alignment"] --> COUNT["Count dN, dS"]
  COUNT --> RATIO["omega = dN/dS"]
  RATIO --> PUR["omega < 1: purifying"]
  RATIO --> NEU["omega = 1: neutral"]
  RATIO --> POS["omega > 1: positive"]
```

Under a strict clock, substitutions are Poisson in time, so divergence grows
linearly — the line whose slope calibrates dates from fossils or sampling times.

```plot
{"title": "Molecular clock: substitutions accumulate with time", "xLabel": "time since divergence", "yLabel": "substitutions per site", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.08*x", "label": "neutral substitutions", "color": "#2563eb"}]}
```

**Next:** inferring history from gene genealogies.
""",
        ),
        _t(
            "Coalescent theory and demographic inference",
            "13 min",
            r"""
# Coalescent theory and demographic inference

The **coalescent** runs evolution backward: trace sampled lineages until they
merge (coalesce) into common ancestors. For a sample of $k$ lineages in a
Wright-Fisher population of effective size $N_e$, the expected time to the next
coalescence is $\frac{2N_e}{\binom{k}{2}}$ — fast when many lineages remain,
slow as few are left. This gives a powerful, computationally cheap framework for
simulation (msprime) and inference.

```mermaid
flowchart TB
  SAMP["k sampled lineages today"] --> C1["Pairs coalesce (rate ~ k^2)"]
  C1 --> C2["Fewer lineages, slower coalescence"]
  C2 --> MRCA["Most recent common ancestor"]
  MRCA --> INFER["Infer Ne, growth, migration, selection"]
```

Because coalescence rate scales with **1/N_e**, the genealogy encodes
demographic history: bottlenecks compress coalescences, expansions stretch them.
Methods such as **PSMC/MSMC**, **dadi** and **SMC++** read the site-frequency
spectrum or pairwise heterozygosity to reconstruct ancestral population sizes
through time. The expected pairwise coalescence time scales directly with $N_e$,
so estimated diversity rises with the effective population size you infer.

```plot
{"title": "Expected pairwise coalescence time versus effective size", "xLabel": "effective population size Ne (relative)", "yLabel": "expected coalescence time", "xRange": [0, 10], "yRange": [0, 20], "grid": true, "functions": [{"expr": "2*x", "label": "E[T2] = 2 Ne", "color": "#16a34a"}]}
```

**Next:** the evolutionary arms races between species.
""",
        ),
        _t(
            "Coevolution and the Red Queen",
            "12 min",
            r"""
# Coevolution and the Red Queen

**Coevolution** is reciprocal evolutionary change between interacting species:
each is a selective pressure on the other. It generates exquisite matches
(flowers and pollinators, plants and herbivore detoxification) and relentless
arms races (host immunity vs parasite evasion).

```mermaid
flowchart LR
  HOST["Host: resistance evolves"] --> PAR["Parasite: counter-adapts"]
  PAR --> HOST2["Host: new resistance"]
  HOST2 --> PAR2["Parasite: new evasion"]
  PAR2 --> RQ["Red Queen: running to stay in place"]
```

The **Red Queen hypothesis** (Van Valen) holds that species must constantly
evolve just to maintain relative fitness against coevolving antagonists — a major
explanation for the maintenance of **sexual reproduction**, which generates the
genotypic novelty needed to escape adapting parasites. Coevolution often shows
**negative frequency-dependent selection**: a host genotype is favoured only
while rare, because common genotypes are tracked by parasites. Fitness therefore
declines as a genotype becomes common, the hallmark signature.

```plot
{"title": "Negative frequency-dependent selection on a host genotype", "xLabel": "frequency of host genotype", "yLabel": "relative fitness", "xRange": [0, 1], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1-x", "label": "fitness falls as genotype spreads", "color": "#dc2626"}]}
```

**Next:** evolution at the bedside.
""",
        ),
        _t(
            "Evolutionary medicine and antibiotic resistance",
            "13 min",
            r"""
# Evolutionary medicine and antibiotic resistance

**Evolutionary medicine** applies selection thinking to health: pathogens evolve
within and between hosts, and our own bodies bear evolutionary trade-offs.
Antibiotic resistance is the clearest, most urgent case — a real-time experiment
in natural selection driven by the strong selective pressure of the drug.

```mermaid
flowchart LR
  POP["Bacterial population (variation)"] --> DRUG["Antibiotic applied"]
  DRUG --> KILL["Susceptible cells die"]
  DRUG --> SURV["Resistant mutants survive"]
  SURV --> GROW["Resistant clone expands"]
  GROW --> HGT["Horizontal gene transfer spreads resistance"]
```

Resistance arises by mutation (target alteration, efflux pumps, enzymatic
inactivation such as beta-lactamases) and spreads by **horizontal gene transfer**
on plasmids. Clinical strategy is shaped by evolution: complete dosing to clear
intermediate variants, **combination therapy** to make simultaneous resistance
improbable, and **cycling** to exploit fitness costs of resistance. Under a fixed
selection coefficient, the resistant fraction follows logistic sweep kinetics —
slow, then explosive, then saturating — which is why monitoring early matters.

```plot
{"title": "Rise of a resistant strain under antibiotic selection", "xLabel": "time (generations)", "yLabel": "fraction resistant", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "resistant fraction", "color": "#dc2626"}]}
```

**Next:** machine learning for evolution and ecology.
""",
        ),
        _t(
            "Machine learning in evolution and ecology",
            "13 min",
            r"""
# Machine learning in evolution and ecology

Genomic and ecological data have outgrown classical likelihood. **Machine
learning** now powers inference where likelihoods are intractable.
**Simulation-based inference (SBI)** trains models on data simulated under
population-genetic models (via msprime/SLiM), bypassing analytic likelihoods to
estimate demography and selection — the core of **approximate Bayesian
computation (ABC)** and modern neural posterior estimation.

```mermaid
flowchart LR
  SIM["Coalescent/forward simulations (msprime, SLiM)"] --> FEAT["Summary stats / raw genotype matrices"]
  FEAT --> ML["CNN / random forest / neural density estimator"]
  ML --> INFER["Demography, selection scans, recombination"]
  INFER --> VALID["Validate on held-out simulations"]
```

**Convolutional networks** read alignments directly to localise selective sweeps
and recombination hotspots (diploS/HIC, ReLERNN). In ecology, **species
distribution models** and deep classifiers map biodiversity from remote sensing
and camera-trap images, and **protein language models** (ESM) and structure
predictors (AlphaFold) inform molecular-evolution analyses of fitness effects.
Performance must be judged on held-out simulations: as training data grow, a
well-specified model's accuracy climbs and then plateaus, the familiar learning
curve that signals diminishing returns.

```plot
{"title": "Learning curve: inference accuracy versus training data", "xLabel": "training simulations (relative)", "yLabel": "accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.5*x)", "label": "validation accuracy", "color": "#2563eb"}]}
```

**Next:** test your command of the state of the art.
""",
        ),
        _quiz(),
    ),
)


EVOLUTION_ECOLOGY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["EVOLUTION_ECOLOGY_COURSES"]
