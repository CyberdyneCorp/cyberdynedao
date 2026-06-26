"""Molecular Biology track: Basics -> Intermediate -> Advanced.

A university-level molecular biology curriculum: from DNA/RNA structure and the
central dogma, through the quantitative methods of replication, transcription,
translation and PCR, to gene regulation, epigenetics, CRISPR and AI-driven
genomics. Lessons use interactive ```plot blocks for quantitative relationships
(melting curves, binding, kinetics, dose-response) and ```mermaid diagrams for
pathways, processes and experimental pipelines.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Molecular Biology -- Basics ----------------------------------------------

_BASICS = SeedCourse(
    slug="molecular-biology-basics",
    title="Molecular Biology — Basics",
    description=(
        "The molecules of heredity from first principles: the structure of DNA "
        "and RNA, base pairing and the double helix, the central dogma, the "
        "genetic code, and an overview of replication, transcription and "
        "translation. Built on real molecular detail with interactive plots and "
        "process diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "DNA structure and the double helix",
            "10 min",
            r"""
# DNA structure and the double helix

**Deoxyribonucleic acid (DNA)** stores genetic information as a polymer of four
**nucleotides**: adenine (A), thymine (T), guanine (G) and cytosine (C). Each
nucleotide is a **deoxyribose sugar**, a **phosphate** group and a **nitrogenous
base**. Sugars and phosphates link through **phosphodiester bonds** to form a
backbone with directionality: a free 5'-phosphate at one end and a 3'-hydroxyl at
the other.

In 1953 **Watson and Crick**, using **Rosalind Franklin's** X-ray diffraction,
described the **double helix**: two antiparallel strands wound around a common
axis. The bases face inward and pair by hydrogen bonds following **Chargaff's
rules** — A pairs with T (two H-bonds), G pairs with C (three H-bonds).

```mermaid
flowchart LR
  STRAND1["5' -> 3' strand"] -->|A=T, G≡C base pairs| STRAND2["3' <- 5' strand"]
  SUGAR["Deoxyribose + phosphate backbone"] --> STRAND1
  SUGAR --> STRAND2
```

Because G-C pairs share three hydrogen bonds and A-T only two, GC-rich DNA is
more thermally stable. The fraction of strands that stay paired falls
sigmoidally as temperature rises through the **melting temperature** $T_m$:

```plot
{"title": "DNA melting (denaturation) curve", "xLabel": "temperature (relative)", "yLabel": "fraction double-stranded", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-1/(1+exp(-(x-5)))", "label": "fraction paired", "color": "#2563eb"}]}
```

**Next:** how RNA differs and what it does.
""",
        ),
        _t(
            "RNA: types and differences from DNA",
            "10 min",
            r"""
# RNA: types and differences from DNA

**Ribonucleic acid (RNA)** is chemically close to DNA but with three key
differences: it uses **ribose** (a 2'-OH sugar) instead of deoxyribose, it
substitutes **uracil (U)** for thymine, and it is usually **single-stranded**.
The extra 2'-hydroxyl makes RNA more reactive and less stable — useful for a
short-lived working copy of the genome.

RNA comes in functional classes:

| RNA | Role |
|-----|------|
| mRNA | messenger; carries the coding sequence to ribosomes |
| tRNA | adaptor; matches codons to amino acids |
| rRNA | structural and catalytic core of the ribosome |
| miRNA / siRNA | regulatory; silence target mRNAs |

```mermaid
flowchart TB
  RNA["RNA"] --> CODING["Coding: mRNA"]
  RNA --> NONCODING["Non-coding RNA"]
  NONCODING --> TRNA["tRNA (adaptor)"]
  NONCODING --> RRNA["rRNA (ribosome)"]
  NONCODING --> REG["miRNA / siRNA / lncRNA"]
```

The single-stranded, reactive nature of RNA means it degrades faster than DNA.
A typical mRNA decays with **first-order kinetics**, $m(t) = m_0 e^{-k t}$, so a
cell can rapidly change which proteins it makes:

```plot
{"title": "First-order RNA decay", "xLabel": "time (relative)", "yLabel": "RNA level", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "m(t) = m0 e^{-kt}", "color": "#dc2626"}]}
```

**Next:** the rule that links DNA, RNA and protein.
""",
        ),
        _t(
            "The central dogma of molecular biology",
            "11 min",
            r"""
# The central dogma of molecular biology

The **central dogma**, stated by **Francis Crick** in 1958, describes the
directional flow of sequence information in the cell: DNA is **replicated** into
DNA, **transcribed** into RNA, and RNA is **translated** into protein. Crucially,
information does not flow from protein back into nucleic acid.

```mermaid
flowchart LR
  DNA["DNA"] -->|replication| DNA2["DNA"]
  DNA -->|transcription| RNA["RNA (mRNA)"]
  RNA -->|translation| PROT["Protein"]
  RNA -.->|reverse transcription| DNA
```

The dashed arrow marks **reverse transcription** (RNA -> DNA), discovered in
retroviruses such as HIV and used by the enzyme **reverse transcriptase**. It is
a real but special-case route, not the default direction.

The dogma is about **sequence information**, not a ban on feedback: proteins
heavily regulate when and how much DNA is transcribed. Each step amplifies — one
gene can yield many mRNA copies, and each mRNA can be translated many times, so
protein output can rise far above the gene-copy number with saturating gain:

```plot
{"title": "Amplification across the central dogma", "xLabel": "transcription/translation activity", "yLabel": "protein output (relative)", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "saturating output", "color": "#16a34a"}]}
```

**Next:** how DNA is copied before a cell divides.
""",
        ),
        _t(
            "DNA replication overview",
            "11 min",
            r"""
# DNA replication overview

Before a cell divides it must copy its genome. Replication is
**semiconservative** (proved by **Meselson and Stahl**): each daughter duplex
keeps one parental strand as a template and gains one new strand. Synthesis
starts at **origins of replication** and proceeds bidirectionally at
**replication forks**.

```mermaid
flowchart LR
  ORI["Origin"] --> HEL["Helicase unwinds duplex"]
  HEL --> PRIM["Primase lays RNA primers"]
  PRIM --> POL["DNA polymerase extends 5' -> 3'"]
  POL --> LEAD["Leading strand (continuous)"]
  POL --> LAG["Lagging strand (Okazaki fragments)"]
  LAG --> LIG["Ligase seals nicks"]
```

**DNA polymerase** adds nucleotides only in the **5' -> 3'** direction, so the
two antiparallel strands are made differently: the **leading strand** is
continuous, while the **lagging strand** is built in short **Okazaki fragments**
later joined by **DNA ligase**. Polymerase **proofreading** (3'->5' exonuclease)
keeps the error rate extremely low.

Replication is fast and roughly constant-rate, so the amount of newly synthesised
DNA grows nearly linearly with time once forks are running:

```plot
{"title": "DNA synthesized during replication", "xLabel": "time (relative)", "yLabel": "DNA copied (relative)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "near-linear synthesis", "color": "#2563eb"}]}
```

**Next:** turning genes into RNA.
""",
        ),
        _t(
            "Transcription and translation overview",
            "12 min",
            r"""
# Transcription and translation overview

**Transcription** copies a gene into RNA. **RNA polymerase** binds a **promoter**,
unwinds the DNA, and synthesises an RNA strand complementary to the template,
reading 3'->5' and building RNA 5'->3'. In eukaryotes the **pre-mRNA** is then
**capped** (5' 7-methylguanosine), **spliced** (introns removed) and
**polyadenylated** (poly-A tail) before export.

**Translation** decodes the mRNA into protein at the **ribosome**. The mRNA is
read in three-base **codons**; **tRNAs** carrying amino acids match their
**anticodon** to each codon. Synthesis begins at the **start codon (AUG)** and
ends at a **stop codon**.

```mermaid
flowchart LR
  GENE["Gene (DNA)"] -->|RNA polymerase| PRE["pre-mRNA"]
  PRE -->|cap, splice, poly-A| MRNA["mature mRNA"]
  MRNA -->|export| RIB["Ribosome"]
  RIB -->|tRNA reads codons| PROT["Polypeptide"]
```

A ribosome elongates a chain at a roughly steady rate (a few to ~20 amino acids
per second), so protein length grows nearly linearly with elongation time until
the stop codon:

```plot
{"title": "Polypeptide elongation over time", "xLabel": "time (relative)", "yLabel": "amino acids added", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "steady elongation", "color": "#16a34a"}]}
```

**Next:** how codons map to amino acids.
""",
        ),
        _t(
            "The genetic code",
            "11 min",
            r"""
# The genetic code

The **genetic code** maps each three-base **codon** to an amino acid (or a stop
signal). With 4 bases read in triplets there are $4^3 = 64$ codons specifying 20
amino acids plus 3 stop signals — so the code is **degenerate** (redundant):
most amino acids have several codons.

Key properties:

- **Triplet**: codons are three bases, read without gaps.
- **Non-overlapping**: each base belongs to one codon.
- **Degenerate**: many amino acids have multiple codons, often differing only at
  the third "wobble" position.
- **Nearly universal**: almost all organisms share the same code (minor
  mitochondrial exceptions exist).

```mermaid
flowchart LR
  MRNA["mRNA codon (e.g. AUG)"] --> TRNA["tRNA anticodon"]
  TRNA --> AA["Amino acid (Met)"]
  AUG["AUG = start / Met"] --> STARTS["Initiation"]
  STOP["UAA, UAG, UGA = stop"] --> ENDS["Termination"]
```

Degeneracy buffers against mutation: many single-base changes are **synonymous**
(silent). As the number of synonymous codons per amino acid rises, the chance
that a random point mutation is silent increases, but with diminishing returns:

```plot
{"title": "Chance a point mutation is silent vs codon redundancy", "xLabel": "synonymous codons per amino acid", "yLabel": "fraction of changes that are silent", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "silent fraction", "color": "#2563eb"}]}
```

**Next:** test your grasp of the molecular basics.
""",
        ),
        _quiz(),
    ),
)


# -- Molecular Biology -- Intermediate ----------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="molecular-biology-intermediate",
    title="Molecular Biology — Intermediate",
    description=(
        "Quantitative molecular biology: the enzymology and fidelity of "
        "replication, the kinetics of transcription and RNA processing, the "
        "mechanics of translation, the thermodynamics of hybridization and PCR, "
        "and mutation and DNA repair. Emphasis on the core equations and methods "
        "— melting temperature, exponential PCR amplification, error rates — with "
        "interactive plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Replication enzymology and fidelity",
            "12 min",
            r"""
# Replication enzymology and fidelity

Replication is carried out by a coordinated machine, the **replisome**.
**Helicase** unwinds the duplex; **single-strand binding (SSB) proteins** keep
strands apart; **topoisomerase** relieves the torsional strain ahead of the fork;
**primase** lays short RNA primers; and **DNA polymerase** (Pol III in *E. coli*,
Pol $\delta$/$\epsilon$ in eukaryotes) extends them 5'->3'.

```mermaid
flowchart LR
  TOPO["Topoisomerase relieves supercoils"] --> HEL["Helicase"]
  HEL --> SSB["SSB proteins"]
  SSB --> PRIM["Primase"]
  PRIM --> POL["DNA polymerase + clamp"]
  POL --> EXO["3'->5' proofreading exonuclease"]
```

**Fidelity** comes from three layers: base-pairing geometry (~$10^{-5}$ errors),
**proofreading** by the polymerase's 3'->5' exonuclease (another ~$10^{2}$), and
**mismatch repair** afterward (another ~$10^{2}$–$10^{3}$), giving an overall
error rate near $10^{-9}$–$10^{-10}$ per base.

Because each layer multiplies the accuracy, the residual error per base falls
steeply (roughly exponentially) as proofreading and repair are added:

```plot
{"title": "Residual error rate vs fidelity layers", "xLabel": "fidelity stages applied", "yLabel": "relative error rate", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-1*x)", "label": "compounding accuracy", "color": "#dc2626"}]}
```

**Next:** the kinetics of making RNA.
""",
        ),
        _t(
            "Transcription kinetics and RNA processing",
            "12 min",
            r"""
# Transcription kinetics and RNA processing

Transcription has three phases. In **initiation**, RNA polymerase (Pol II for
mRNA in eukaryotes) and **general transcription factors** assemble at the
promoter (e.g. the **TATA box**) and form the pre-initiation complex. In
**elongation** the polymerase moves along the template at ~20–80 nt/s. In
**termination** the transcript is released.

```mermaid
flowchart LR
  PROM["Promoter + TFs"] --> INIT["Initiation: PIC assembly"]
  INIT --> ELONG["Elongation (Pol II)"]
  ELONG --> TERM["Termination + release"]
  ELONG --> CAP["5' cap"]
  ELONG --> SPL["Splicing (spliceosome)"]
  ELONG --> POLYA["3' cleavage + poly-A"]
```

Eukaryotic **pre-mRNA processing** happens co-transcriptionally: a 5' cap aids
stability and ribosome loading; the **spliceosome** removes introns at GU...AG
boundaries; and cleavage plus **polyadenylation** define the 3' end.
**Alternative splicing** lets one gene encode many protein isoforms.

If transcript synthesis runs at a constant rate $k_s$ while the mRNA degrades at
rate $k_d$, the steady-state level rises and saturates toward $k_s/k_d$:

```plot
{"title": "mRNA accumulation to steady state", "xLabel": "time (relative)", "yLabel": "mRNA level (relative)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.6*x)", "label": "approach to k_s/k_d", "color": "#2563eb"}]}
```

**Next:** the mechanics of the ribosome.
""",
        ),
        _t(
            "Translation mechanics and the ribosome",
            "12 min",
            r"""
# Translation mechanics and the ribosome

The **ribosome** is a ribonucleoprotein machine (a **ribozyme** — its catalytic
peptidyl-transferase centre is RNA). It has a **small subunit** that reads the
mRNA and a **large subunit** that catalyses peptide-bond formation, with three
tRNA sites: **A** (aminoacyl), **P** (peptidyl) and **E** (exit).

```mermaid
flowchart LR
  INIT["Initiation: start codon AUG, initiator tRNA"] --> ELONG["Elongation cycle"]
  ELONG --> A["A site: incoming aminoacyl-tRNA"]
  A --> P["Peptide bond, P site"]
  P --> TRANS["Translocation (EF-G / eEF2)"]
  TRANS --> ELONG
  ELONG --> TERM["Stop codon -> release factor"]
```

Each elongation cycle costs GTP (delivery by EF-Tu/eEF1, translocation by
EF-G/eEF2). Accuracy comes from **kinetic proofreading**: correct codon-anticodon
pairing slows GTP hydrolysis enough to reject most mismatches before commitment.

Translation rate rises with available **aminoacyl-tRNA / ternary complex** and
then saturates as the ribosome's catalytic cycle becomes rate-limiting — a
hyperbolic, Michaelis-Menten-shaped response:

```plot
{"title": "Translation rate vs tRNA availability", "xLabel": "[charged tRNA] (relative)", "yLabel": "elongation rate", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "saturating rate", "color": "#16a34a"}]}
```

**Next:** the thermodynamics behind hybridization.
""",
        ),
        _t(
            "Hybridization thermodynamics and Tm",
            "12 min",
            r"""
# Hybridization thermodynamics and Tm

Two complementary strands anneal when base pairing and stacking lower the free
energy: $\Delta G = \Delta H - T\Delta S$. Duplex formation is enthalpically
favourable ($\Delta H < 0$) but entropically costly, so it is favoured at low
temperature. The **melting temperature** $T_m$ is where half the strands are
paired ($\Delta G = 0$, i.e. $T_m = \Delta H / \Delta S$).

```mermaid
flowchart LR
  SS["Single strands"] -->|cool / anneal| DS["Duplex (lower G)"]
  DS -->|heat / denature| SS
  GC["High GC content"] --> HIGH["Higher Tm"]
  SALT["Higher salt"] --> HIGH
```

For short oligonucleotides a useful rule of thumb is the **Wallace rule**,
$T_m \approx 2(A+T) + 4(G+C)$ in °C, reflecting the extra hydrogen bond in G-C
pairs. $T_m$ also rises with **salt concentration** (screening backbone charge)
and with sequence length. The fraction of duplex versus temperature is a sharp
sigmoid centred on $T_m$:

```plot
{"title": "Hybridization melting profile", "xLabel": "temperature (relative)", "yLabel": "fraction duplex", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp((x-5)))", "label": "fraction paired", "color": "#2563eb"}]}
```

Designing primers and probes means tuning length and GC to hit a target $T_m$ —
the foundation of PCR, microarrays and FISH.

**Next:** amplifying DNA with PCR.
""",
        ),
        _t(
            "PCR and exponential amplification",
            "12 min",
            r"""
# PCR and exponential amplification

**Polymerase chain reaction (PCR)**, invented by **Kary Mullis**, amplifies a
chosen DNA region through repeated thermal cycles. Each cycle has three steps:
**denaturation** (~95 °C, melt strands), **annealing** (~50–65 °C, primers bind),
and **extension** (~72 °C, a thermostable **Taq polymerase** copies each
template).

```mermaid
flowchart LR
  DENAT["Denature (95C)"] --> ANNEAL["Anneal primers (~60C)"]
  ANNEAL --> EXTEND["Extend (72C, Taq)"]
  EXTEND --> DENAT
  EXTEND --> PROD["Doubled target copies"]
```

If every template is copied each cycle, copy number doubles: after $n$ cycles
$N = N_0 (1+E)^n$, with efficiency $E \approx 1$ for ideal doubling. The
amplification is **exponential** in cycle number:

```plot
{"title": "Exponential PCR amplification", "xLabel": "cycle number", "yLabel": "copies (relative)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "N = N0 (1+E)^n", "color": "#dc2626"}]}
```

In real reactions the curve eventually **plateaus** as reagents deplete. In
**quantitative PCR (qPCR)** a fluorescent signal is tracked each cycle; the
**cycle threshold ($C_t$)** — when signal crosses a threshold — is lower for
samples with more starting template, giving quantitation. **Reverse-transcription
PCR (RT-PCR)** first copies RNA to cDNA to measure gene expression.

**Next:** how mutations arise and get repaired.
""",
        ),
        _t(
            "Mutation and DNA repair",
            "12 min",
            r"""
# Mutation and DNA repair

A **mutation** is a heritable change in DNA sequence. **Point mutations** swap
one base (**transitions** within purines/pyrimidines, **transversions** across);
**insertions/deletions (indels)** can cause **frameshifts**. By effect on coding,
substitutions are **silent**, **missense** or **nonsense**.

Mutations come from replication errors, **deamination**, **oxidation** (8-oxoG),
UV-induced **pyrimidine dimers**, and chemical mutagens. Cells defend with
dedicated repair pathways:

```mermaid
flowchart TB
  DAMAGE["DNA damage"] --> MMR["Mismatch repair (replication errors)"]
  DAMAGE --> BER["Base excision repair (small lesions)"]
  DAMAGE --> NER["Nucleotide excision repair (bulky/UV)"]
  DAMAGE --> DSB["Double-strand breaks"]
  DSB --> NHEJ["NHEJ (error-prone)"]
  DSB --> HR["Homologous recombination (accurate)"]
```

Repair efficiency matters: defects cause disease (xeroderma pigmentosum from NER
loss; Lynch syndrome from MMR loss; BRCA-related cancers from HR loss). With
functioning repair, the fraction of lesions remaining falls exponentially over
time as repair enzymes act, $f(t) = e^{-k t}$:

```plot
{"title": "Lesion removal by DNA repair over time", "xLabel": "time (relative)", "yLabel": "fraction of lesions remaining", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "first-order repair", "color": "#2563eb"}]}
```

**Next:** test the quantitative core.
""",
        ),
        _quiz(),
    ),
)


# -- Molecular Biology -- Advanced --------------------------------------------

_ADVANCED = SeedCourse(
    slug="molecular-biology-advanced",
    title="Molecular Biology — Advanced",
    description=(
        "State-of-the-art and applied molecular biology: transcriptional gene "
        "regulation and operons, epigenetics and chromatin, RNA interference and "
        "non-coding RNA, CRISPR-Cas genome editing, next-generation sequencing, "
        "and AI/deep-learning models of the genome. Connects mechanism to modern "
        "computational methods with interactive plots."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Gene regulation: operons and transcription factors",
            "13 min",
            r"""
# Gene regulation: operons and transcription factors

Cells control **which** genes are expressed and **how much**. In bacteria, the
classic **lac operon** bundles co-regulated genes under one promoter. A
**repressor** blocks transcription unless lactose (allolactose) inactivates it
(**negative control**); the **CAP-cAMP** complex boosts transcription when
glucose is scarce (**positive control**) — together a logic gate for nutrient
sensing.

```mermaid
flowchart LR
  GLUC["Low glucose -> high cAMP"] --> CAP["CAP-cAMP activates"]
  LAC["Lactose present"] --> REP["Repressor released from operator"]
  CAP --> ON["lac genes transcribed"]
  REP --> ON
```

In eukaryotes, regulation is combinatorial: **transcription factors** bind
**enhancers** and **silencers** that can act over long distances via DNA looping
to the promoter and **Mediator** complex. **Cooperative** TF binding makes
expression **switch-like** — a steep sigmoid in output versus activator
concentration, described by a high **Hill coefficient**:

```plot
{"title": "Cooperative (switch-like) gene activation", "xLabel": "activator concentration (relative)", "yLabel": "expression (fraction max)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^4)", "label": "Hill, n=4", "color": "#2563eb"}]}
```

**Next:** regulation written above the sequence — epigenetics.
""",
        ),
        _t(
            "Epigenetics and chromatin regulation",
            "13 min",
            r"""
# Epigenetics and chromatin regulation

**Epigenetics** is heritable change in gene activity without changing the DNA
sequence. Two main layers: **DNA methylation** (a methyl group on cytosine in
**CpG** islands, generally silencing) and **histone modifications** (acetylation,
methylation, etc.) that loosen or tighten chromatin.

```mermaid
flowchart TB
  CHROM["Chromatin state"] --> METH["DNA methylation (CpG)"]
  CHROM --> HIST["Histone marks"]
  HIST --> ACT["H3K4me3 / H3K27ac -> active (euchromatin)"]
  HIST --> REP["H3K9me3 / H3K27me3 -> repressed (heterochromatin)"]
  METH --> REP
```

A useful mental model is **writers** (e.g. DNMTs, HATs, HMTs add marks),
**erasers** (HDACs, demethylases remove them) and **readers** (bromo-/chromo-
domain proteins interpret them). These marks drive **X-inactivation**,
**imprinting** and cell-type identity, and are reprogrammable — the basis of
induced pluripotent stem cells.

Marks can be **bistable** and self-reinforcing: above a threshold of repressive
modification, a locus flips to a stably silenced state, giving a sharp switch
rather than a gradual dial:

```plot
{"title": "Bistable chromatin silencing switch", "xLabel": "repressive mark density (relative)", "yLabel": "probability silenced", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "silencing probability", "color": "#dc2626"}]}
```

**Next:** RNA that regulates other RNA.
""",
        ),
        _t(
            "RNA interference and non-coding RNA",
            "12 min",
            r"""
# RNA interference and non-coding RNA

Much of the genome is transcribed into **non-coding RNA** that regulates rather
than encodes protein. **RNA interference (RNAi)** uses small RNAs to silence
genes sequence-specifically. **microRNAs (miRNAs)** are processed by **Drosha**
and **Dicer**, loaded into the **RISC** complex (with **Argonaute**), and guide
it to complementary mRNAs to block translation or trigger degradation.

```mermaid
flowchart LR
  PRI["pri-miRNA"] -->|Drosha| PRE["pre-miRNA"]
  PRE -->|Dicer| DUP["miRNA duplex"]
  DUP -->|load into RISC/Argonaute| RISC["RISC"]
  RISC --> TARGET["Target mRNA: cleavage / repression"]
```

**siRNAs** (often exogenous, e.g. from dsRNA) drive sequence-perfect cleavage and
are a workhorse for **gene knockdown** and a therapeutic modality (siRNA drugs
like patisiran). Other classes include **lncRNAs** (scaffolds, e.g. XIST in
X-inactivation) and **piRNAs** (transposon defence).

Knockdown is dose-dependent: as siRNA/miRNA concentration rises, target protein
falls along a sigmoidal **dose-response** toward a residual floor:

```plot
{"title": "Target knockdown vs small-RNA dose", "xLabel": "log siRNA dose", "yLabel": "remaining target protein", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-1/(1+exp(-(x-5)))", "label": "knockdown", "color": "#16a34a"}]}
```

**Next:** rewriting the genome with CRISPR.
""",
        ),
        _t(
            "CRISPR-Cas genome editing",
            "13 min",
            r"""
# CRISPR-Cas genome editing

**CRISPR-Cas** repurposes a bacterial adaptive immune system for programmable
genome editing. A **guide RNA (gRNA)** directs the **Cas9** nuclease to a
20-nucleotide target adjacent to a **PAM** (e.g. NGG), where Cas9 makes a
**double-strand break**. Repair determines the outcome.

```mermaid
flowchart LR
  GRNA["Guide RNA"] --> CAS9["Cas9 + PAM recognition"]
  CAS9 --> DSB["Double-strand break"]
  DSB --> NHEJ["NHEJ -> indels (knockout)"]
  DSB --> HDR["HDR + donor -> precise knock-in"]
```

Beyond cutting, the toolbox has grown: **CRISPRi/a** (catalytically dead dCas9
fused to repressors/activators) tunes expression; **base editors** convert one
base to another without a double-strand break; and **prime editing** writes
small edits using a reverse transcriptase and an extended **pegRNA**.

A central practical concern is **specificity**: gRNAs can cut **off-target**
sites with mismatches. Cleavage efficiency falls steeply as the number of guide-
target mismatches grows, which is what makes high-fidelity design possible:

```plot
{"title": "Cas9 cleavage vs guide-target mismatches", "xLabel": "number of mismatches", "yLabel": "relative cleavage efficiency", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.8*x)", "label": "off-target falloff", "color": "#dc2626"}]}
```

Machine-learning models (e.g. for on-/off-target scoring) now help design guides
that maximise on-target activity while minimising off-target risk.

**Next:** reading genomes at scale.
""",
        ),
        _t(
            "Next-generation sequencing",
            "13 min",
            r"""
# Next-generation sequencing

**Next-generation sequencing (NGS)** reads DNA massively in parallel. The
dominant **Illumina** chemistry fragments DNA, ligates adapters, clusters
fragments by bridge amplification, and reads sequence by **sequencing-by-
synthesis** with reversible fluorescent terminators. **Long-read** platforms
(**PacBio** SMRT, **Oxford Nanopore**) read single molecules of tens of kilobases.

```mermaid
flowchart LR
  DNA["Genomic DNA"] --> FRAG["Fragment + adapters"]
  FRAG --> CLUST["Cluster / amplify"]
  CLUST --> SEQ["Sequencing by synthesis"]
  SEQ --> READS["Short / long reads + quality"]
  READS --> ALIGN["Align / assemble"]
  ALIGN --> VAR["Variant calling / quantification"]
```

Bioinformatics turns reads into biology: alignment (BWA, minimap2), assembly,
**variant calling** (GATK), and quantification (RNA-seq). Read quality is scored
on the **Phred** scale, $Q = -10\log_{10} P_{error}$, so error probability drops
exponentially as $Q$ rises (Q30 = 1 error in 1000):

```plot
{"title": "Phred quality vs error probability", "xLabel": "Phred Q (relative, tens)", "yLabel": "error probability", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.7*x)", "label": "P_error = 10^(-Q/10)", "color": "#2563eb"}]}
```

**Coverage** (mean reads per base) governs confidence; variant-detection
sensitivity rises with coverage and then saturates, so studies pick depth to hit
a target without wasteful over-sequencing.

**Next:** AI models that read the genome.
""",
        ),
        _t(
            "AI and deep learning in genomics",
            "13 min",
            r"""
# AI and deep learning in genomics

**Deep learning** now predicts function directly from sequence. Convolutional and
transformer models learn the regulatory grammar of DNA: tools like **DeepBind**
and **Basset** predict transcription-factor binding and chromatin accessibility,
while **Enformer** uses long-range attention to predict gene expression from
sequence over ~100 kb. **AlphaFold** revolutionised the related problem of
predicting protein structure from sequence.

```mermaid
flowchart LR
  SEQ["DNA / protein sequence"] --> ENC["Encode (one-hot / tokens)"]
  ENC --> NET["CNN / transformer"]
  NET --> PRED["Predict: binding, expression, structure, variant effect"]
  PRED --> INTERP["Interpretation / attribution maps"]
```

Applications span **variant-effect prediction** (which mutations are
pathogenic), **splice prediction** (SpliceAI), **regulatory element** discovery,
and guide-RNA design for CRISPR. Models are increasingly **interpretable** via
attribution (saliency, in-silico mutagenesis) that recovers known motifs.

As with most learned models, accuracy improves with **training data** but shows
**diminishing returns** — a saturating learning curve that motivates
self-supervised pretraining on large unlabelled genomes (e.g. DNA language
models):

```plot
{"title": "Genomic model accuracy vs training data", "xLabel": "labeled examples (relative)", "yLabel": "validation accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "learning curve", "color": "#2563eb"}]}
```

Caveats remain: **distribution shift** across cell types and species, the need
for careful held-out evaluation, and correlation-versus-causation in regulatory
predictions.

**Next:** the capstone quiz.
""",
        ),
        _quiz(),
    ),
)


MOLECULAR_BIOLOGY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["MOLECULAR_BIOLOGY_COURSES"]
