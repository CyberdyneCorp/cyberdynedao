"""Microbiology track: Basics -> Intermediate -> Advanced.

A university-level microbiology curriculum spanning microbial diversity,
cell structure and growth; through metabolism, genetics and physical/chemical
control; to pathogenesis, antimicrobial resistance and the microbiome. Lessons
use interactive ```plot blocks for quantitative relationships (growth curves,
kill kinetics, Monod and dose-response) and ```mermaid diagrams for pathways,
taxonomic classifications and laboratory/computational pipelines.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Microbiology -- Basics ----------------------------------------------------

_BASICS = SeedCourse(
    slug="microbiology-basics",
    title="Microbiology — Basics",
    description=(
        "The microbial world from the ground up: the three-domain tree and "
        "microbial diversity, the prokaryotic cell and its envelope, the Gram "
        "stain and microscopy, how microbes are grown and counted, and the "
        "exponential growth curve. Built on real molecular and laboratory "
        "detail with interactive plots and pathway diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The microbial world and the three domains",
            "10 min",
            r"""
# The microbial world and the three domains

**Microbiology** studies organisms too small to see unaided — bacteria,
archaea, fungi, protists and the acellular viruses. Microbes are the oldest,
most abundant and most metabolically diverse life on Earth, driving the carbon,
nitrogen and sulfur cycles and inhabiting every habitat from deep-sea vents to
the human gut.

Carl Woese's comparison of **small-subunit (16S/18S) ribosomal RNA** redrew the
tree of life into **three domains**: Bacteria, Archaea and Eukarya. Bacteria and
Archaea are both **prokaryotic** (no membrane-bound nucleus) but differ
profoundly — archaeal membranes use ether-linked isoprenoid lipids and many
thrive in extreme heat, salt or acidity.

```mermaid
flowchart TB
  LUCA["Last universal common ancestor"] --> BAC["Bacteria"]
  LUCA --> ARC["Archaea"]
  LUCA --> EUK["Eukarya (protists, fungi, plants, animals)"]
  ARC -.closer relatives.- EUK
```

Why is rRNA the molecular clock? It is universal, functionally constant and
changes slowly, so sequence differences scale with evolutionary distance — the
fraction of conserved positions falls as lineages diverge over time:

```plot
{"title": "Sequence identity vs evolutionary divergence", "xLabel": "divergence time (relative)", "yLabel": "fraction identical positions", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.3*x)", "label": "rRNA identity decay", "color": "#2563eb"}]}
```

**Next:** the architecture of the prokaryotic cell.
""",
        ),
        _t(
            "The prokaryotic cell and its envelope",
            "11 min",
            r"""
# The prokaryotic cell and its envelope

A bacterium packs life into ~1-5 um. Its **cytoplasm** holds the **nucleoid**
(a single supercoiled circular chromosome), 70S **ribosomes**, often **plasmids**
(small accessory DNA), and storage granules. There is no nucleus and no
membrane-bound organelles.

The **cell envelope** defines the cell and resists turgor pressure. Outside the
plasma membrane lies the **cell wall** built of **peptidoglycan** — glycan
chains of alternating NAG and NAM cross-linked by short peptides. Two major
plans exist:

| Feature | Gram-positive | Gram-negative |
|---------|---------------|---------------|
| Peptidoglycan | thick (many layers) | thin (1-2 layers) |
| Outer membrane | absent | present (LPS) |
| Periplasm | minimal | prominent |
| Teichoic acids | present | absent |

```mermaid
flowchart LR
  GP["Gram-positive"] --> PG["Thick peptidoglycan + teichoic acid"]
  GN["Gram-negative"] --> OM["Outer membrane (LPS) + thin peptidoglycan"]
  OM --> PERI["Periplasmic space"]
```

External structures add function: **flagella** for motility, **pili/fimbriae**
for adhesion and conjugation, and a **capsule** for immune evasion. The
peptidoglycan wall is the target of penicillin, which blocks the
transpeptidase that cross-links it.

**Next:** how we stain and see these cells.
""",
        ),
        _t(
            "Microscopy and the Gram stain",
            "11 min",
            r"""
# Microscopy and the Gram stain

Microbes are smaller than the eye's limit, so microscopy is foundational.
**Bright-field** light microscopy resolves down to about 200 nm, set by
diffraction; **phase-contrast** reveals living unstained cells; **fluorescence**
labels specific molecules; and **electron microscopy** reaches nanometre
detail for ultrastructure.

The **Gram stain** (1884) is the single most important differential stain. The
sequence is crystal violet, iodine mordant, alcohol decolourisation, then
safranin counterstain. The thick peptidoglycan of **Gram-positive** cells traps
the crystal violet-iodine complex and stays purple; the thin wall of
**Gram-negative** cells loses it and takes up the pink safranin.

```mermaid
flowchart LR
  CV["Crystal violet (all purple)"] --> IOD["Iodine mordant"]
  IOD --> DEC["Alcohol decolorize"]
  DEC --> GPOS["Gram+ stays purple"]
  DEC --> GNEG["Gram- becomes colorless"]
  GNEG --> SAF["Safranin -> pink"]
```

Microscope resolution follows Abbe's limit
$d = \frac{\lambda}{2\,\text{NA}}$: shorter wavelength or higher numerical
aperture gives finer detail. Resolving power (1/d) rises linearly with
numerical aperture:

```plot
{"title": "Resolving power vs numerical aperture", "xLabel": "numerical aperture NA", "yLabel": "resolving power (relative)", "xRange": [0.1, 1.4], "yRange": [0, 3], "grid": true, "functions": [{"expr": "2*x", "label": "1/d ~ 2NA/lambda", "color": "#16a34a"}]}
```

**Next:** how we cultivate microbes in the lab.
""",
        ),
        _t(
            "Culturing microbes: media and isolation",
            "11 min",
            r"""
# Culturing microbes: media and isolation

To study a microbe we usually grow a **pure culture** — a population descended
from one cell. **Culture media** supply carbon, nitrogen, energy and trace
nutrients. Media are classified by purpose:

- **Defined (synthetic)**: exact chemical composition, known concentrations.
- **Complex**: rich extracts (peptone, yeast extract) of unknown exact makeup.
- **Selective**: inhibit unwanted organisms (e.g. MacConkey with bile salts).
- **Differential**: reveal traits by colour (e.g. blood agar haemolysis).

```mermaid
flowchart LR
  SAMP["Mixed sample"] --> STREAK["Streak-plate dilution"]
  STREAK --> COL["Isolated colonies"]
  COL --> PICK["Pick single colony"]
  PICK --> PURE["Pure culture"]
```

The classic isolation method is the **streak plate**, which dilutes cells across
agar until individual cells are far enough apart to grow into discrete
**colonies** — each a clone of one founding cell (a CFU, colony-forming unit).
Robert Koch's solidification of media with **agar** made this routine.

Not every microbe grows on plates: the **great plate-count anomaly** notes that
microscopic counts vastly exceed culturable counts, because most environmental
microbes are not yet cultivable. The fraction recovered on standard media stays
low even as sampling effort rises:

```plot
{"title": "Culturable fraction vs sampling effort", "xLabel": "sampling effort (relative)", "yLabel": "fraction recovered on plates", "xRange": [0, 10], "yRange": [0, 0.1], "grid": true, "functions": [{"expr": "0.09*x/(2+x)", "label": "saturating recovery (~1%)", "color": "#dc2626"}]}
```

**Next:** how a population grows over time.
""",
        ),
        _t(
            "Microbial growth and the growth curve",
            "12 min",
            r"""
# Microbial growth and the growth curve

Bacteria reproduce by **binary fission**: one cell becomes two, two become four.
In rich medium the population **doubles** every **generation time** $g$. After
$n$ generations from $N_0$ cells, $N = N_0 \cdot 2^{n}$ — exponential growth.

A batch culture passes through four phases:

```mermaid
flowchart LR
  LAG["Lag: adapting, no division"] --> LOG["Log/exponential: max rate"]
  LOG --> STAT["Stationary: nutrients limit"]
  STAT --> DEATH["Death/decline"]
```

During exponential phase the count rises steeply; plotted on a linear axis the
curve is a sharp upward sweep before nutrients run out:

```plot
{"title": "Exponential phase of bacterial growth", "xLabel": "time (generations)", "yLabel": "cell number (relative)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "N = N0 e^(mu t)", "color": "#2563eb"}]}
```

The **specific growth rate** $\mu$ links to generation time by
$g = \frac{\ln 2}{\mu}$. Environmental factors set the ceiling: temperature
(psychrophiles, mesophiles, thermophiles), pH, oxygen (obligate aerobes vs
anaerobes vs facultative), and water/solute activity. Each organism has a
cardinal temperature triplet — minimum, optimum and maximum — beyond which
proteins denature and growth stops.

**Next:** test your grasp of microbial fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- Microbiology -- Intermediate ---------------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="microbiology-intermediate",
    title="Microbiology — Intermediate",
    description=(
        "Quantitative and mechanistic microbiology: chemostat and Monod growth "
        "kinetics, microbial metabolism and respiration, regulation of gene "
        "expression, horizontal gene transfer and mutation, and the kinetics of "
        "sterilisation and disinfection. Emphasis on the core equations and "
        "methods — Monod, the decimal reduction time D, mutation rates — with "
        "interactive plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Growth kinetics: Monod and the chemostat",
            "12 min",
            r"""
# Growth kinetics: Monod and the chemostat

In a closed batch culture growth is transient. A **chemostat** sustains steady
growth by continuously feeding fresh medium and removing culture at the same
**dilution rate** $D = F/V$ (flow over volume). At steady state the specific
growth rate equals the dilution rate, $\mu = D$.

Growth rate depends on the limiting nutrient through the **Monod equation**,
the microbial analogue of Michaelis-Menten:

$$\mu = \mu_{max}\frac{S}{K_s + S},$$

where $K_s$ is the substrate concentration at half-maximal growth. The
saturating hyperbola:

```plot
{"title": "Monod growth kinetics", "xLabel": "[S] (relative to Ks)", "yLabel": "mu (fraction of mu_max)", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "mu = mu_max S/(Ks+S)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  IN["Fresh medium in (F)"] --> VESSEL["Stirred vessel (V), mu = D"]
  VESSEL --> OUT["Culture out (F)"]
  VESSEL --> SS["Steady state: dX/dt = 0"]
```

The **yield coefficient** $Y_{X/S}$ relates biomass made to substrate consumed.
Raising $D$ above $\mu_{max}$ causes **washout**: cells leave faster than they
divide and the culture collapses. The chemostat lets microbiologists hold cells
in a defined physiological state — invaluable for studying metabolism and
evolution.

**Next:** how microbes harvest energy.
""",
        ),
        _t(
            "Microbial metabolism and respiration",
            "12 min",
            r"""
# Microbial metabolism and respiration

Microbes show unmatched metabolic versatility. Energy comes from light
(**phototrophs**) or chemicals (**chemotrophs**); electrons from organic
(**organotrophs**) or inorganic (**lithotrophs**) donors; carbon from CO2
(**autotrophs**) or organics (**heterotrophs**). Combinations define lifestyles
like the chemolithoautotroph.

```mermaid
flowchart LR
  GLU["Glucose"] -->|glycolysis| PYR["Pyruvate + ATP + NADH"]
  PYR -->|aerobic| TCA["TCA cycle + ETC + O2"]
  PYR -->|anaerobic| FERM["Fermentation (lactate / ethanol)"]
  TCA --> ATPH["High ATP yield"]
  FERM --> ATPL["Low ATP yield, regenerates NAD+"]
```

In **aerobic respiration** electrons flow down the chain to O2, the terminal
acceptor, building a proton-motive force for ATP synthase — high yield.
**Anaerobic respiration** uses alternative acceptors (nitrate, sulfate, Fe(III),
fumarate) with progressively lower energy. **Fermentation** uses no chain at
all: it regenerates NAD+ by reducing an organic intermediate, yielding only
substrate-level ATP.

ATP yield rises with the **redox potential gap** between donor and acceptor;
more positive acceptors release more energy, with diminishing returns:

```plot
{"title": "Energy yield vs terminal acceptor potential", "xLabel": "acceptor redox potential (relative)", "yLabel": "ATP yield (relative)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.5*x)", "label": "energy from electron drop", "color": "#16a34a"}]}
```

This ordering explains the **redox tower** and why microbes use the best
available acceptor first.

**Next:** how microbes control which genes they express.
""",
        ),
        _t(
            "Regulation of gene expression",
            "12 min",
            r"""
# Regulation of gene expression

Bacteria tune their proteome to the environment, mostly at **transcription
initiation**. The classic model is the **lac operon**: a cluster of genes for
lactose use under one promoter, controlled by a repressor and an activator.

```mermaid
flowchart LR
  REP["LacI repressor"] -->|no lactose| BLOCK["Blocks operator -> off"]
  IND["Allolactose (inducer)"] -->|binds LacI| ON["Operon ON"]
  GLU["Glucose low -> cAMP high"] --> CAP["CAP-cAMP activates"]
  CAP --> ON
```

Two logics combine: **negative control** (LacI repressor blocks the operator
until the inducer allolactose binds it) and **positive control** (CAP-cAMP
boosts transcription only when glucose is scarce). The result is
**catabolite repression** — glucose is used preferentially.

Beyond operons, bacteria use **sigma factors** to switch whole regulons (e.g.
heat-shock, sporulation), **two-component systems** (a sensor kinase plus a
response regulator) for signal transduction, **riboswitches** that sense
metabolites in the mRNA itself, and **quorum sensing** to count their own
density. Quorum-regulated genes switch on sharply above a threshold cell
density — a cooperative, sigmoidal response:

```plot
{"title": "Quorum-sensing response vs cell density", "xLabel": "autoinducer (relative)", "yLabel": "fraction of cells activated", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(4/x)^4)", "label": "cooperative switch", "color": "#dc2626"}]}
```

**Next:** how genes move and change.
""",
        ),
        _t(
            "Mutation and horizontal gene transfer",
            "12 min",
            r"""
# Mutation and horizontal gene transfer

Genetic variation arises by **mutation** and is shuffled by **recombination**.
Point mutations (substitutions, frameshifts) occur spontaneously from
replication errors and damage; the **mutation rate** is roughly constant per
base per replication, so mutants accumulate in proportion to population size and
generations.

```mermaid
flowchart TB
  HGT["Horizontal gene transfer"] --> TRANS["Transformation: free DNA uptake"]
  HGT --> TDUCT["Transduction: phage-mediated"]
  HGT --> CONJ["Conjugation: plasmid via pilus"]
```

What makes bacteria evolve fast is **horizontal gene transfer (HGT)** — moving
DNA between cells, even across species:

- **Transformation**: competent cells take up free environmental DNA.
- **Transduction**: a bacteriophage accidentally packages and delivers host DNA.
- **Conjugation**: a donor transfers a plasmid (e.g. the F plasmid) through a
  pilus-mediated mating bridge.

HGT spreads antibiotic-resistance and virulence genes rapidly. The expected
number of resistant mutants in a culture scales with population size; on a log
scale the count of pre-existing resistant cells rises with the total cells
screened:

```plot
{"title": "Expected resistant mutants vs population size", "xLabel": "population size (relative)", "yLabel": "resistant cells (relative)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "0.9*x", "label": "mutants ~ mutation rate x N", "color": "#2563eb"}]}
```

The **Luria-Delbruck** fluctuation test showed such mutations arise *before*
selection, not in response to it — a landmark for Darwinian evolution in
microbes.

**Next:** how we kill microbes.
""",
        ),
        _t(
            "Sterilisation and disinfection kinetics",
            "12 min",
            r"""
# Sterilisation and disinfection kinetics

Controlling microbes means removing or killing them. **Sterilisation** destroys
all life (including spores); **disinfection** reduces vegetative pathogens on
surfaces; **antisepsis** does so on living tissue. Methods are physical (heat,
filtration, radiation) or chemical (alcohols, aldehydes, oxidisers).

Killing by heat or chemical follows **first-order (exponential) kinetics**: a
constant fraction of survivors dies per unit time, so the survivor count falls
exponentially, $N = N_0 e^{-kt}$.

```plot
{"title": "Exponential microbial kill curve", "xLabel": "exposure time (relative)", "yLabel": "surviving fraction", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "N/N0 = e^(-kt)", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  HEAT["Moist heat (autoclave 121C)"] --> KILL["Denature proteins / nucleic acids"]
  CHEM["Chemical agent"] --> KILL
  KILL --> LOG["Log-linear survivor decline"]
  LOG --> DVAL["Defined by D and z values"]
```

Two parameters quantify resistance: the **decimal reduction time D** is the time
to kill 90% (one log) of the population at a given temperature; the **z value**
is the temperature rise needed to cut D tenfold. The **autoclave** (saturated
steam at 121 C, 15 psi, ~15 min) is the workhorse, achieving a wide safety
margin (the 12-D concept for spore-formers). Filtration (0.22 um membranes)
sterilises heat-sensitive fluids without killing.

**Next:** test the quantitative core.
""",
        ),
        _quiz(),
    ),
)


# -- Microbiology -- Advanced -------------------------------------------------

_ADVANCED = SeedCourse(
    slug="microbiology-advanced",
    title="Microbiology — Advanced",
    description=(
        "State-of-the-art and applied microbiology: molecular pathogenesis and "
        "toxins, antimicrobial action and pharmacodynamics, the mechanisms and "
        "evolution of antibiotic resistance, the human microbiome and "
        "metagenomics, biofilms and persistence, and AI/computational methods "
        "for pathogen genomics. Connects mechanism to modern sequencing and "
        "machine-learning methods with interactive plots."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Molecular pathogenesis and virulence",
            "13 min",
            r"""
# Molecular pathogenesis and virulence

A **pathogen** causes disease; **virulence** measures how severely. Infection is
a multistep program: adhere, invade or colonise, evade host defences, acquire
nutrients (notably iron via **siderophores**), and damage the host. The genes
encoding these traits often cluster in **pathogenicity islands** acquired by
horizontal transfer.

```mermaid
flowchart LR
  ADH["Adhesion (pili, adhesins)"] --> COL["Colonization / invasion"]
  COL --> EVA["Immune evasion (capsule, antigenic variation)"]
  EVA --> DAM["Damage (toxins, secretion systems)"]
  DAM --> DIS["Disease"]
```

**Toxins** are key weapons. **Exotoxins** are secreted proteins, classically
**AB toxins** (a B subunit binds the host receptor; an A subunit is the enzyme),
such as diphtheria, cholera and botulinum toxin. **Endotoxin** is
lipopolysaccharide (LPS), released from Gram-negative walls, triggering
inflammation and septic shock. **Secretion systems** (Type III/IV) inject
effectors directly into host cells.

Virulence is quantified by the **LD50** (dose lethal to 50% of hosts) or
**ID50** (infectious dose); the dose-response is sigmoidal on a log-dose axis:

```plot
{"title": "Dose-response: probability of infection", "xLabel": "log dose of pathogen", "yLabel": "fraction infected", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "ID50 at half-maximal", "color": "#2563eb"}]}
```

A lower LD50/ID50 means a more virulent organism — fewer cells needed to cause
disease.

**Next:** how antimicrobials act.
""",
        ),
        _t(
            "Antimicrobial action and pharmacodynamics",
            "13 min",
            r"""
# Antimicrobial action and pharmacodynamics

Antibiotics exploit targets present in microbes but absent (or different) in
us — **selective toxicity**. Major classes attack distinct processes:

| Target | Class (example) | Effect |
|--------|-----------------|--------|
| Cell wall | beta-lactams, vancomycin | bactericidal |
| 30S ribosome | aminoglycosides, tetracyclines | varies |
| 50S ribosome | macrolides, chloramphenicol | bacteriostatic |
| DNA gyrase | fluoroquinolones | bactericidal |
| Folate synthesis | sulfonamides, trimethoprim | bacteriostatic |

```mermaid
flowchart LR
  AB["Antibiotic"] --> WALL["Wall synthesis (beta-lactams)"]
  AB --> PROT["Protein synthesis (ribosome)"]
  AB --> DNA["DNA replication (quinolones)"]
  AB --> FOL["Folate pathway (sulfa)"]
```

Potency is summarised by the **minimum inhibitory concentration (MIC)** — the
lowest drug concentration that prevents visible growth. **Pharmacodynamics**
asks how killing depends on concentration: beta-lactams are
**time-dependent** (kill scales with time above MIC), while aminoglycosides and
fluoroquinolones are **concentration-dependent** (higher peaks kill faster).

Bacterial killing rate rises steeply with drug concentration around the MIC
then saturates at a maximum kill rate — a sigmoidal pharmacodynamic (Emax)
curve:

```plot
{"title": "Kill rate vs drug concentration (relative to MIC)", "xLabel": "concentration / MIC", "yLabel": "kill rate (relative)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(2/x)^2)", "label": "Emax pharmacodynamics", "color": "#dc2626"}]}
```

The **mutant prevention concentration** sits above the MIC, where even
single-step resistant mutants cannot grow — dosing strategy aims to stay there.

**Next:** how resistance arises and spreads.
""",
        ),
        _t(
            "Antibiotic resistance: mechanisms and evolution",
            "13 min",
            r"""
# Antibiotic resistance: mechanisms and evolution

Resistance is biochemistry plus evolution. The biochemical strategies are few
but powerful:

```mermaid
flowchart TB
  RES["Resistance mechanisms"] --> ENZ["Enzymatic destruction (beta-lactamases)"]
  RES --> EFF["Efflux pumps export the drug"]
  RES --> TGT["Target modification (PBP2a, ribosomal methylation)"]
  RES --> PERM["Reduced permeability (porin loss)"]
```

**Enzymatic inactivation** (beta-lactamases, including ESBLs and carbapenemases
like NDM-1), **efflux pumps**, **target alteration** (MRSA's altered PBP2a;
methylation of rRNA), and **decreased uptake** each blunt a drug. Genes spread
on **plasmids, transposons and integrons** by horizontal transfer.

Evolution does the rest. Under drug pressure, resistant clones are selected;
the **selection window** between the MIC of susceptible and resistant cells is
where resistance enriches fastest. Resistance often carries a **fitness cost**,
so the resistant fraction grows logistically toward fixation once selection
begins, but compensatory mutations can erase the cost:

```plot
{"title": "Resistant fraction under selection over time", "xLabel": "generations under drug (relative)", "yLabel": "fraction resistant", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-4)))", "label": "logistic enrichment", "color": "#2563eb"}]}
```

Stewardship — combination therapy, cycling, dose optimisation and rapid
diagnostics — slows resistance. **WGS-based surveillance** now tracks resistance
genes globally in near real time.

**Next:** the microbiome and metagenomics.
""",
        ),
        _t(
            "The human microbiome and metagenomics",
            "13 min",
            r"""
# The human microbiome and metagenomics

The **microbiome** is the community of microbes (and their genes) living in and
on us — densest in the gut, where ~10^13-10^14 cells rival our own. It aids
digestion (short-chain fatty acids from fibre), trains immunity, excludes
pathogens (**colonisation resistance**) and synthesises vitamins.

Because most members are unculturable, we study them by **sequencing** DNA
directly:

```mermaid
flowchart LR
  SAMP["Stool / swab sample"] --> EXT["DNA extraction"]
  EXT --> AMP["16S rRNA amplicon  OR  shotgun metagenome"]
  AMP --> SEQ["High-throughput sequencing"]
  SEQ --> BIN["ASVs / MAGs, taxonomy"]
  BIN --> FUNC["Diversity + functional profiling"]
```

**16S rRNA amplicon** sequencing identifies *who is there*; **shotgun
metagenomics** sequences all DNA to recover *what they can do* (functional
genes) and assemble **metagenome-assembled genomes (MAGs)**. **Alpha diversity**
measures richness within a sample; **beta diversity** compares samples.

As sequencing depth grows, more species are detected, but the **rarefaction
curve** saturates as rare taxa are exhausted — a key check that a sample was
sampled deeply enough:

```plot
{"title": "Rarefaction: species detected vs sequencing depth", "xLabel": "reads sampled (relative)", "yLabel": "fraction of species detected", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1.5)", "label": "saturating richness", "color": "#16a34a"}]}
```

**Dysbiosis** is linked to IBD, obesity and infection; **faecal microbiota
transplant** treats recurrent *C. difficile*, and engineered consortia are an
active therapeutic frontier.

**Next:** how communities resist treatment.
""",
        ),
        _t(
            "Biofilms, persistence and tolerance",
            "12 min",
            r"""
# Biofilms, persistence and tolerance

Most microbes in nature and disease live not as free **planktonic** cells but in
**biofilms** — surface-attached communities encased in a self-produced
**extracellular polymeric substance (EPS)** of polysaccharide, protein and
extracellular DNA. Biofilms foul catheters, implants and pipes.

```mermaid
flowchart LR
  ATT["Reversible attachment"] --> IRR["Irreversible adhesion"]
  IRR --> MAT["Matrix (EPS) production"]
  MAT --> MAT2["Maturation, 3D architecture"]
  MAT2 --> DISP["Dispersal -> new sites"]
```

Biofilms are dramatically harder to eradicate — often 100-1000x more tolerant
to antibiotics. The reasons differ from genetic **resistance**: the matrix
slows drug penetration, deep cells are nutrient-starved and slow-growing (many
antibiotics need active growth), and a sub-population of dormant **persister
cells** survives lethal doses without any resistance mutation. After treatment,
persisters regrow, giving the **biphasic kill curve** — a fast initial kill,
then a tolerant plateau:

```plot
{"title": "Biphasic kill: bulk vs persisters", "xLabel": "antibiotic exposure (relative)", "yLabel": "surviving fraction", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-2*x)", "label": "bulk population", "color": "#dc2626"}, {"expr": "0.05+0.0*x", "label": "persister plateau", "color": "#2563eb"}]}
```

**Tolerance** (survive longer at the same MIC) and **persistence** (a dormant
subpopulation) are distinct from resistance and increasingly recognised as
drivers of chronic, relapsing infection. Anti-biofilm strategies target the
matrix, quorum sensing, or persister metabolism.

**Next:** computational and AI methods in microbiology.
""",
        ),
        _t(
            "AI and computational genomics for pathogens",
            "13 min",
            r"""
# AI and computational genomics for pathogens

Sequencing has made microbiology a data science. **Whole-genome sequencing
(WGS)** of a clinical isolate now informs species ID, resistance prediction,
virulence profiling and outbreak tracing within hours.

```mermaid
flowchart LR
  ISO["Clinical isolate"] --> WGS["Whole-genome sequencing"]
  WGS --> ASM["Assembly + QC"]
  ASM --> AMR["Resistance gene calling (CARD / ResFinder)"]
  ASM --> TYPE["cgMLST / SNP phylogeny"]
  TYPE --> EPI["Outbreak transmission clustering"]
```

**Machine learning** now predicts antibiotic resistance phenotypes directly from
genotype — models trained on labelled genome-MIC pairs map resistance genes and
SNPs to susceptibility, often outperforming rule-based catalogues for novel
variants. Deep learning also powers **MALDI-TOF** species identification,
metagenomic read classification (Kraken2), and protein-structure-based target
discovery (AlphaFold-guided drug design).

Prediction accuracy improves with the number of labelled genomes but with
diminishing returns — a saturating learning curve that motivates sharing global
surveillance data:

```plot
{"title": "Resistance prediction accuracy vs training genomes", "xLabel": "labeled genomes (relative)", "yLabel": "validation accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "learning curve", "color": "#2563eb"}]}
```

Care is needed: **population structure** confounds genotype-phenotype models
(lineage acts as a hidden variable), databases are biased toward well-studied
pathogens, and proper validation needs held-out lineages, not just held-out
isolates. Genomic epidemiology (Nextstrain-style phylodynamics) closed the loop
during recent pandemics, tracking spread in near real time.

**Next:** the capstone quiz.
""",
        ),
        _quiz(),
    ),
)


MICROBIOLOGY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["MICROBIOLOGY_COURSES"]
