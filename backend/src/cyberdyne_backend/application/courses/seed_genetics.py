"""Genetics track: Basics -> Intermediate -> Advanced.

A university-level genetics curriculum from Mendelian inheritance, alleles and
the chromosome theory, through linkage and recombination, mutation, and
population genetics, to quantitative, medical and computational genetics
(GWAS, genomic prediction and deep-learning variant effect models). Lessons use
interactive ```plot blocks for quantitative relationships (allele-frequency
dynamics, recombination, mutation-selection balance, heritability) and
```mermaid diagrams for crosses, pathways and analysis pipelines.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Genetics -- Basics --------------------------------------------------------

_BASICS = SeedCourse(
    slug="genetics-basics",
    title="Genetics — Basics",
    description=(
        "The foundations of heredity: genes, alleles and the genotype-to-"
        "phenotype map; Mendel's laws of segregation and independent "
        "assortment; the monohybrid and dihybrid cross; dominance, codominance "
        "and multiple alleles; meiosis as the cellular basis of inheritance; "
        "and the chromosome theory. Built on real genetic detail with "
        "interactive plots and cross diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Genes, alleles and the language of heredity",
            "10 min",
            r"""
# Genes, alleles and the language of heredity

A **gene** is a unit of heredity: a stretch of DNA encoding a product (a protein
or functional RNA) at a fixed location, its **locus**. Most genes come in
alternative versions called **alleles** that differ in sequence. A diploid
organism carries two alleles per autosomal locus, one from each parent.

The two alleles together form the **genotype**; the observable trait they
produce is the **phenotype**. If the two alleles are identical the individual is
**homozygous**; if different, **heterozygous**. A **dominant** allele (written in
upper case, $A$) masks a **recessive** one ($a$) in the heterozygote $Aa$.

```mermaid
flowchart LR
  GENE["Gene (locus)"] --> ALL["Alleles: A, a"]
  ALL --> GEN["Genotype: AA, Aa, aa"]
  GEN --> PHE["Phenotype: dominant / recessive"]
```

Genotype does not map to phenotype perfectly. **Penetrance** is the fraction of
individuals with a genotype who show the expected phenotype; **expressivity** is
how strongly it shows. Penetrance often rises with allele dose or age, a
saturating relationship:

```plot
{"title": "Penetrance vs genetic/age load", "xLabel": "risk load (relative)", "yLabel": "fraction affected", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "penetrance", "color": "#2563eb"}]}
```

**Next:** how Mendel deduced these rules from peas.
""",
        ),
        _t(
            "Mendel's laws: segregation and independent assortment",
            "11 min",
            r"""
# Mendel's laws: segregation and independent assortment

Gregor Mendel crossed true-breeding pea lines and counted offspring ratios,
inferring discrete "factors" (genes) decades before DNA was known. Two laws
emerged.

The **law of segregation**: the two alleles of a gene separate during gamete
formation, so each gamete carries exactly one. A heterozygote $Aa$ produces $A$
and $a$ gametes in equal proportion.

The **law of independent assortment**: alleles of *different* genes segregate
independently (for genes on different chromosomes), so a dihybrid $AaBb$ makes
$AB$, $Ab$, $aB$, $ab$ gametes in equal 1:1:1:1 ratio.

```mermaid
flowchart TB
  P["Parent Aa"] --> G1["Gamete A (1/2)"]
  P --> G2["Gamete a (1/2)"]
  D["Dihybrid AaBb"] --> AB["AB"]
  D --> Ab["Ab"]
  D --> aB["aB"]
  D --> ab["ab"]
```

These rules are probabilistic. For $n$ independently assorting heterozygous loci,
the number of distinct gamete genotypes is $2^n$, which grows explosively — the
engine of genetic variety:

```plot
{"title": "Distinct gamete genotypes vs heterozygous loci", "xLabel": "number of loci n", "yLabel": "gamete types (2^n)", "xRange": [0, 8], "yRange": [0, 260], "grid": true, "functions": [{"expr": "2^x", "label": "2^n", "color": "#dc2626"}]}
```

**Next:** working the monohybrid and dihybrid crosses.
""",
        ),
        _t(
            "The monohybrid and dihybrid cross",
            "12 min",
            r"""
# The monohybrid and dihybrid cross

The **Punnett square** turns Mendel's laws into predictions. Cross two
heterozygotes, $Aa \times Aa$. Each parent gives $A$ or $a$ with probability
$1/2$, so offspring are $1\,AA : 2\,Aa : 1\,aa$ — the classic **3:1** phenotypic
ratio when $A$ is dominant.

|        | A (1/2) | a (1/2) |
|--------|---------|---------|
| A (1/2)| AA      | Aa      |
| a (1/2)| Aa      | aa      |

A **dihybrid cross** $AaBb \times AaBb$, with independent assortment, multiplies
two 3:1 ratios to give the famous **9:3:3:1** phenotypic ratio among 16
genotype combinations.

```mermaid
flowchart LR
  CROSS["AaBb x AaBb"] --> R1["9 A_B_ (both dominant)"]
  CROSS --> R2["3 A_bb"]
  CROSS --> R3["3 aaB_"]
  CROSS --> R4["1 aabb"]
```

A **test cross** to a homozygous recessive ($A? \times aa$) reveals an unknown
genotype: all-dominant offspring imply $AA$, a 1:1 split implies $Aa$. Because
each offspring is an independent trial, observed ratios converge on the expected
only with large samples — sampling error shrinks roughly as $1/\sqrt{N}$:

```plot
{"title": "Sampling error of an observed ratio vs family size", "xLabel": "offspring N (relative)", "yLabel": "error in estimated ratio", "xRange": [1, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/sqrt(x)", "label": "error ~ 1/sqrt(N)", "color": "#2563eb"}]}
```

**Next:** when inheritance is not simply dominant or recessive.
""",
        ),
        _t(
            "Beyond simple dominance: codominance and multiple alleles",
            "11 min",
            r"""
# Beyond simple dominance: codominance and multiple alleles

Real traits often break the clean dominant/recessive dichotomy.

- **Incomplete dominance**: the heterozygote is intermediate (red x white
  snapdragons -> pink). Neither allele fully masks the other, giving a **1:2:1**
  phenotypic ratio that matches the genotype ratio.
- **Codominance**: both alleles are expressed fully and simultaneously, as in
  the **AB blood type**, where A and B antigens both appear.
- **Multiple alleles**: a gene can have more than two variants in a population.
  The **ABO** locus has alleles $I^A$, $I^B$ and $i$; A and B are codominant and
  both dominant over $i$.

```mermaid
flowchart TB
  ABO["ABO gene"] --> IA["I^A -> A antigen"]
  ABO --> IB["I^B -> B antigen"]
  ABO --> i["i -> no antigen"]
  IA --> AB["I^A I^B = type AB (codominant)"]
  IB --> AB
```

Other complications: **pleiotropy** (one gene affecting many traits),
**epistasis** (one gene masking another), and **polygenic** traits set by many
genes. With $k$ additive loci each adding a small effect, the phenotype
distribution approaches a smooth bell curve — a continuous, not discrete, trait:

```plot
{"title": "Polygenic trait approaches a normal distribution", "xLabel": "trait value", "yLabel": "frequency", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-((x-5)^2)/2)", "label": "phenotype density", "color": "#16a34a"}]}
```

**Next:** the cell division that makes inheritance possible.
""",
        ),
        _t(
            "Meiosis: the cellular basis of inheritance",
            "12 min",
            r"""
# Meiosis: the cellular basis of inheritance

Mendel's "factors" are carried on **chromosomes**, and **meiosis** is the
reduction division that explains his laws physically. Meiosis halves the
chromosome number, taking a diploid (2n) cell to haploid (n) gametes in two
rounds, **meiosis I** and **meiosis II**.

```mermaid
flowchart LR
  CELL["Diploid germ cell (2n)"] --> MI["Meiosis I: homologs separate"]
  MI --> CELL2["Two haploid cells (n, sister chromatids)"]
  CELL2 --> MII["Meiosis II: sister chromatids separate"]
  MII --> GAM["Four haploid gametes (n)"]
```

The key event is **prophase I**, where homologous chromosomes pair (synapsis)
and exchange segments by **crossing over**, then line up. The independent
orientation of each homolog pair at metaphase I is the physical basis of
**independent assortment**, while the separation of homologs is **segregation**.

Two mechanisms generate gamete diversity: **independent assortment** gives $2^n$
combinations ($n$ chromosome pairs), and **crossing over** recombines alleles
along chromosomes. The probability that at least one of several gametes is fully
recombinant rises and saturates with the number sampled:

```plot
{"title": "Chance of a recombinant gamete vs gametes sampled", "xLabel": "gametes sampled (relative)", "yLabel": "P(at least one recombinant)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.5*x)", "label": "cumulative probability", "color": "#2563eb"}]}
```

Errors in this process — **nondisjunction** — cause **aneuploidy** such as
trisomy 21.

**Next:** tying genes to chromosomes and to sex.
""",
        ),
        _t(
            "The chromosome theory and sex linkage",
            "11 min",
            r"""
# The chromosome theory and sex linkage

The **chromosome theory of inheritance** (Sutton and Boveri, confirmed by
Morgan) states that genes reside on chromosomes, whose behaviour in meiosis
exactly parallels Mendel's laws. Morgan's work on *Drosophila* white-eyed flies
gave the decisive proof through **sex linkage**.

In humans the **sex chromosomes** are X and Y: XX females, XY males. The X
carries many genes; the Y carries few (notably *SRY*, the male-determining
switch). A gene on the X is **X-linked**.

```mermaid
flowchart TB
  CROSS["Carrier mother X^H X^h  x  healthy father X^H Y"] --> D["Daughters: 1/2 carriers, 0 affected"]
  CROSS --> S["Sons: 1/2 affected (X^h Y), 1/2 healthy"]
```

Because males are **hemizygous** (one X), a recessive X-linked allele such as
those for **haemophilia** or red-green **colour blindness** is expressed in any
male who inherits it, making these conditions far more common in males. The
expected affected fraction among sons of a carrier mother is $1/2$, independent
of the father.

For an X-linked recessive at allele frequency $q$, the affected fraction is $q$
in males but only $q^2$ in females, so the male-to-female ratio of affected
individuals is $1/q$ — large for rare alleles:

```plot
{"title": "Male:female ratio of X-linked recessive cases", "xLabel": "allele frequency q (x100, relative)", "yLabel": "ratio affected males:females", "xRange": [0.2, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "10/x", "label": "ratio ~ 1/q", "color": "#dc2626"}]}
```

**Next:** test your grasp of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- Genetics -- Intermediate -------------------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="genetics-intermediate",
    title="Genetics — Intermediate",
    description=(
        "The quantitative core of genetics: linkage, recombination frequency "
        "and genetic mapping; mutation types and rates; the Hardy-Weinberg "
        "equilibrium and its tests; the forces of evolution — selection, drift, "
        "migration and mutation; and an introduction to quantitative genetics "
        "and heritability. Emphasis on the equations and methods, with "
        "interactive plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Linkage, recombination and genetic mapping",
            "12 min",
            r"""
# Linkage, recombination and genetic mapping

Genes close together on the same chromosome are **linked**: they violate
independent assortment because crossing over rarely separates them. The
**recombination frequency** (RF) between two loci is the fraction of gametes
that are recombinant:

$$\text{RF} = \frac{\text{recombinant offspring}}{\text{total offspring}}.$$

RF ranges from 0 (perfectly linked) to a maximum of 0.5 (unlinked, indistinguishable
from independent assortment). One **map unit** (centiMorgan, cM) equals 1%
recombination, so RF approximately gives map distance for nearby loci.

```mermaid
flowchart LR
  A["Locus A"] --- B["Locus B (near)"]
  B --- C["Locus C (far)"]
  A -->|low RF| B
  A -->|high RF, RF<=0.5| C
```

Because double crossovers between distant loci go undetected, RF underestimates
true distance for far-apart genes. **Mapping functions** (Haldane, Kosambi)
correct this. The observed RF rises with true map distance but plateaus toward
0.5 — exactly the saturation a mapping function describes:

```plot
{"title": "Observed recombination frequency vs map distance", "xLabel": "true map distance (Morgans, relative)", "yLabel": "observed RF", "xRange": [0, 10], "yRange": [0, 0.5], "grid": true, "functions": [{"expr": "0.5*(1-exp(-0.5*x))", "label": "Haldane RF = 1/2(1-e^-2d)", "color": "#2563eb"}]}
```

**Three-point crosses** order three loci and detect double crossovers, giving
the **interference** that real chromosomes show.

**Next:** the source of all genetic variation.
""",
        ),
        _t(
            "Mutation: types, rates and consequences",
            "12 min",
            r"""
# Mutation: types, rates and consequences

**Mutation** is any heritable change in DNA sequence — the ultimate source of
new alleles. Mutations are classified by scale and effect.

```mermaid
flowchart TB
  MUT["Mutation"] --> POINT["Point: substitution / indel"]
  MUT --> CHROM["Chromosomal: deletion, duplication, inversion, translocation"]
  POINT --> SYN["Silent (synonymous)"]
  POINT --> MIS["Missense"]
  POINT --> NON["Nonsense (stop)"]
  POINT --> FS["Frameshift (indel not x3)"]
```

A **point mutation** swaps one base; **transitions** (purine<->purine) outnumber
**transversions**. In a coding region the consequence depends on the genetic
code's redundancy: **synonymous** (no amino-acid change), **missense** (one
residue changed), **nonsense** (premature stop), or **frameshift** (an indel
not a multiple of three, scrambling all downstream codons).

Mutations accumulate over time. Under a constant per-generation rate $\mu$, the
expected number of new mutations grows linearly, while the probability that a
given site is still unmutated decays exponentially as $e^{-\mu t}$:

```plot
{"title": "Probability a site remains unmutated over time", "xLabel": "generations (relative)", "yLabel": "P(no mutation)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "P = e^{-mu t}", "color": "#dc2626"}]}
```

Human germline rates are about $10^{-8}$ per base per generation. Mutations arise
from replication errors, deamination, oxidation and radiation; **DNA repair**
(mismatch repair, base/nucleotide excision) keeps rates low, and its failure
drives mutator phenotypes and cancer.

**Next:** describing allele frequencies in whole populations.
""",
        ),
        _t(
            "Hardy-Weinberg equilibrium",
            "12 min",
            r"""
# Hardy-Weinberg equilibrium

**Population genetics** tracks allele and genotype frequencies. For a locus with
alleles $A$ (frequency $p$) and $a$ (frequency $q = 1-p$), random mating predicts
the **Hardy-Weinberg** genotype frequencies in one generation:

$$p^2 + 2pq + q^2 = 1,$$

with $p^2$ homozygous $AA$, $2pq$ heterozygous $Aa$, and $q^2$ homozygous $aa$.
The frequencies are then stable across generations — *if* the assumptions hold:
no selection, no mutation, no migration, infinite population (no drift), and
random mating.

```mermaid
flowchart LR
  ALLELE["Allele freqs p, q"] --> RAND["Random mating"]
  RAND --> GENO["Genotypes p^2 : 2pq : q^2"]
  GENO --> STABLE["Stable next generation (if assumptions hold)"]
```

HWE is the **null model**: a deviation flags one of these forces at work, or
nonrandom mating. A practical use is estimating carrier frequency for a recessive
disease from incidence: if $q^2$ is the affected fraction, the carrier frequency
$2pq \approx 2q$ for rare alleles is much larger.

Heterozygotes are most abundant at intermediate $p$, peaking at $p = 0.5$ where
$2pq = 0.5$ — and the curve is symmetric:

```plot
{"title": "Heterozygote frequency 2pq vs allele frequency", "xLabel": "allele frequency p (x10)", "yLabel": "2pq", "xRange": [0, 10], "yRange": [0, 0.6], "grid": true, "functions": [{"expr": "2*(x/10)*(1-x/10)", "label": "2pq", "color": "#16a34a"}]}
```

A **chi-square** goodness-of-fit test compares observed genotype counts to the
$p^2:2pq:q^2$ expectation.

**Next:** the forces that move allele frequencies.
""",
        ),
        _t(
            "Forces of evolution: selection, drift and migration",
            "13 min",
            r"""
# Forces of evolution: selection, drift and migration

When Hardy-Weinberg assumptions fail, allele frequencies change — evolution. Four
forces dominate.

```mermaid
flowchart TB
  EVO["Allele-frequency change"] --> SEL["Selection (fitness differences)"]
  EVO --> DRIFT["Genetic drift (sampling, small N)"]
  EVO --> MIG["Migration / gene flow"]
  EVO --> MUTF["Mutation (new alleles)"]
```

**Selection** acts on **fitness** ($w$): the relative reproductive success of
each genotype. The **selection coefficient** $s = 1 - w$ measures the
disadvantage of a genotype. Directional selection against a recessive allele
drives its frequency down, but slowly when rare because deleterious alleles hide
in heterozygotes.

**Genetic drift** is random change from finite sampling; its strength scales as
$1/(2N)$, so small populations lose variation fast. The expected heterozygosity
decays each generation by a factor $(1 - 1/(2N))$, an exponential loss:

```plot
{"title": "Loss of heterozygosity by drift (small population)", "xLabel": "generations (relative)", "yLabel": "heterozygosity remaining", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.3*x)", "label": "H_t = H_0 (1-1/2N)^t", "color": "#dc2626"}]}
```

**Migration** (gene flow) homogenises populations, opposing the differentiation
caused by drift and local selection. **Balancing selection** — as in
**heterozygote advantage** at the sickle-cell locus, where $HbA/HbS$ resists
malaria — maintains polymorphism rather than fixing one allele.

**Next:** measuring traits set by many genes.
""",
        ),
        _t(
            "Quantitative genetics and heritability",
            "13 min",
            r"""
# Quantitative genetics and heritability

Many traits — height, blood pressure, yield — are **quantitative**: continuous,
shaped by many genes plus environment. Their study partitions the **phenotypic
variance**:

$$V_P = V_G + V_E,$$

genetic plus environmental variance (ignoring interaction). The genetic part
splits further into **additive** ($V_A$), **dominance** ($V_D$) and **epistatic**
components.

```mermaid
flowchart LR
  VP["Phenotypic variance V_P"] --> VG["Genetic V_G"]
  VP --> VE["Environmental V_E"]
  VG --> VA["Additive V_A"]
  VG --> VD["Dominance V_D"]
```

Two heritabilities matter. **Broad-sense** $H^2 = V_G/V_P$; **narrow-sense**
$h^2 = V_A/V_P$, the fraction of variance that responds predictably to selection.
Narrow-sense heritability drives the **breeder's equation**:

$$R = h^2 S,$$

the response to selection $R$ equals $h^2$ times the selection differential $S$.

```plot
{"title": "Response to selection vs heritability (fixed S)", "xLabel": "narrow-sense heritability h^2 (x10)", "yLabel": "response R (relative)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "R = h^2 S", "color": "#2563eb"}]}
```

Heritability is **population- and environment-specific**, not a fixed property of
a trait, and says nothing about differences *between* groups. It is estimated
from resemblance among relatives (twin studies, parent-offspring regression) or,
modernly, from genome-wide marker data (GREML).

**Next:** test the quantitative core.
""",
        ),
        _quiz(),
    ),
)


# -- Genetics -- Advanced -----------------------------------------------------

_ADVANCED = SeedCourse(
    slug="genetics-advanced",
    title="Genetics — Advanced",
    description=(
        "State-of-the-art and applied genetics: genome-wide association studies "
        "and the missing-heritability problem, linkage disequilibrium and fine-"
        "mapping, polygenic risk scores and genomic prediction, the clinical "
        "genetics of disease and pharmacogenomics, CRISPR genome editing and "
        "gene therapy, and deep-learning models of variant effect and gene "
        "regulation. Connects mechanism to modern computational methods with "
        "interactive plots."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Genome-wide association studies (GWAS)",
            "13 min",
            r"""
# Genome-wide association studies (GWAS)

A **GWAS** scans millions of common variants (**SNPs**) genotyped across many
individuals to find alleles statistically associated with a trait or disease. For
each SNP it regresses phenotype on genotype (linear for quantitative traits,
logistic for case-control) and tests the effect.

```mermaid
flowchart LR
  COHORT["Genotyped cohort (cases/controls)"] --> QC["QC + imputation"]
  QC --> ASSOC["Per-SNP association test"]
  ASSOC --> CORR["Correct for structure (PCs, mixed models)"]
  CORR --> MAN["Manhattan plot, hits"]
  MAN --> REP["Replication + fine-mapping"]
```

Because millions of tests run, the **genome-wide significance** threshold is
stringent, $p < 5 \times 10^{-8}$ (Bonferroni for ~1 million independent tests).
**Population stratification** is corrected with principal components or
**linear mixed models** (e.g. BOLT-LMM, GCTA). Results are summarised in a
**Manhattan plot** of $-\log_{10} p$ against genomic position.

Statistical **power** to detect a variant rises with sample size and effect size
and saturates toward 1 — explaining the huge biobank cohorts now used:

```plot
{"title": "GWAS power vs sample size", "xLabel": "sample size (relative)", "yLabel": "power to detect locus", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "power", "color": "#2563eb"}]}
```

Most associated variants are **non-coding** and of small effect, leaving the
**missing heritability** gap that polygenic and rare-variant work addresses.

**Next:** the correlation structure that GWAS exploits and must untangle.
""",
        ),
        _t(
            "Linkage disequilibrium and fine-mapping",
            "12 min",
            r"""
# Linkage disequilibrium and fine-mapping

**Linkage disequilibrium (LD)** is the non-random association of alleles at
nearby loci — the reason a genotyped "tag" SNP can stand in for many unmeasured
neighbours. LD is quantified by $D' $ and the squared correlation $r^2$.

```mermaid
flowchart LR
  CAUSAL["Causal variant"] --- TAG1["Tag SNP 1 (high r^2)"]
  CAUSAL --- TAG2["Tag SNP 2"]
  TAG1 --> SIG["GWAS signal at whole LD block"]
  TAG2 --> SIG
```

LD arises because variants on the same haplotype are inherited together; it
**decays with distance** as recombination breaks haplotypes over generations.
Within an LD block, dozens of correlated SNPs all show association, so the lead
SNP is rarely causal. Average $r^2$ falls roughly exponentially with genomic
separation:

```plot
{"title": "LD decay with distance", "xLabel": "distance between SNPs (kb, relative)", "yLabel": "average r^2", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "r^2 decay", "color": "#dc2626"}]}
```

**Fine-mapping** narrows an associated region to likely causal variants.
Bayesian methods (FINEMAP, SuSiE) compute **posterior inclusion probabilities**
and a **credible set** of variants that contain the causal one with, say, 95%
probability. Integrating functional annotations and **eQTL/colocalisation**
data (does the variant also control a gene's expression?) links statistical
hits to mechanism.

**Next:** turning many small effects into a prediction.
""",
        ),
        _t(
            "Polygenic risk scores and genomic prediction",
            "13 min",
            r"""
# Polygenic risk scores and genomic prediction

A **polygenic (risk) score (PRS/PGS)** aggregates the effects of many variants
into one number predicting an individual's genetic liability:

$$\text{PRS}_i = \sum_j \hat\beta_j\, x_{ij},$$

the sum over SNPs $j$ of the estimated effect $\hat\beta_j$ times the genotype
$x_{ij}$ (0/1/2 copies). Effects come from GWAS summary statistics.

```mermaid
flowchart LR
  GWAS["GWAS summary stats (betas)"] --> ADJ["LD adjustment (clumping / LDpred / PRS-CS)"]
  ADJ --> SCORE["Weighted sum over genotype"]
  SCORE --> RISK["Individual risk distribution"]
  RISK --> STRAT["Risk stratification / screening"]
```

Naive scores double-count correlated SNPs, so methods **adjust for LD**:
clumping + thresholding, or Bayesian shrinkage (**LDpred2**, **PRS-CS**). The
same machinery in animal and plant breeding is **genomic prediction**
(GBLUP, Bayesian alphabet), now also tackled with deep learning.

Prediction accuracy ($R^2$ or AUC) rises with **training GWAS sample size** but
plateaus at a ceiling set by the trait's $h^2$ and the SNP panel — diminishing
returns that motivate ever-larger biobanks:

```plot
{"title": "PRS accuracy vs training sample size", "xLabel": "training N (relative)", "yLabel": "prediction accuracy (R^2)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "accuracy", "color": "#2563eb"}]}
```

A critical caveat: scores trained in one ancestry **transfer poorly** to others
because LD and allele frequencies differ — a major equity problem in genomic
medicine.

**Next:** genetics in the clinic.
""",
        ),
        _t(
            "Medical genetics and pharmacogenomics",
            "13 min",
            r"""
# Medical genetics and pharmacogenomics

**Medical genetics** spans the disease architecture from single-gene to complex.
**Monogenic (Mendelian)** disorders — cystic fibrosis (*CFTR*), Huntington
disease (*HTT* CAG repeat), sickle-cell anaemia (*HBB*) — follow clear
inheritance and are diagnosed by sequencing. **Complex** diseases (type 2
diabetes, coronary disease) are polygenic plus environmental.

```mermaid
flowchart TB
  DIS["Genetic disease"] --> MONO["Monogenic: high penetrance, rare"]
  DIS --> COMPLEX["Complex: many small effects, common"]
  MONO --> DIAG["Diagnostic sequencing (panels, WES, WGS)"]
  COMPLEX --> PRS["Polygenic risk + lifestyle"]
```

Variants are interpreted against the **ACMG** criteria into classes from benign
to pathogenic, using population frequency (gnomAD), computational predictors and
segregation. **Genetic counselling** translates risk for families.

**Pharmacogenomics** matches drug to genotype: *CYP2D6* and *CYP2C19* metaboliser
status guides dosing; *TPMT* variants flag thiopurine toxicity; *HLA-B\*57:01*
predicts abacavir hypersensitivity. As more risk alleles are catalogued, the
fraction of patients with at least one actionable pharmacogenomic variant rises
and saturates near one:

```plot
{"title": "Patients with an actionable variant vs genes screened", "xLabel": "pharmacogenes screened (relative)", "yLabel": "fraction actionable", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.4*x)", "label": "cumulative coverage", "color": "#16a34a"}]}
```

**Next:** rewriting the genome itself.
""",
        ),
        _t(
            "CRISPR genome editing and gene therapy",
            "13 min",
            r"""
# CRISPR genome editing and gene therapy

**CRISPR-Cas9** programs a nuclease with a **guide RNA** to cut a chosen genomic
site; cellular repair then edits it. **Non-homologous end joining (NHEJ)**
produces indels that knock out a gene, while **homology-directed repair (HDR)**
with a template installs a precise edit.

```mermaid
flowchart LR
  GRNA["Guide RNA + Cas9"] --> CUT["Double-strand break at target"]
  CUT --> NHEJ["NHEJ -> indels (knockout)"]
  CUT --> HDR["HDR + template -> precise edit"]
  GRNA --> BASE["Base / prime editing (no DSB)"]
```

Newer tools avoid double-strand breaks: **base editors** chemically convert one
base to another, and **prime editors** ("search-and-replace") write new sequence
via a reverse transcriptase fused to a nicking Cas9. **Off-target** cutting is
the main safety concern, mitigated by high-fidelity Cas variants and careful
guide design.

**Gene therapy** delivers or corrects genes — **AAV** and lentiviral vectors,
or ex vivo edited cells. Approved successes include **CAR-T** cancer therapy and
**Casgevy**, a CRISPR therapy for sickle-cell disease. Editing efficiency rises
with vector dose but saturates as target cells are exhausted, while off-target
risk keeps climbing — the therapeutic-window trade-off:

```plot
{"title": "On-target editing efficiency vs delivered dose", "xLabel": "vector dose (relative)", "yLabel": "fraction of cells edited", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "editing efficiency", "color": "#2563eb"}]}
```

**Next:** predicting variant effects with machine learning.
""",
        ),
        _t(
            "Deep learning for variant effect and gene regulation",
            "13 min",
            r"""
# Deep learning for variant effect and gene regulation

Most disease variants are **non-coding** and hard to interpret. **Deep learning**
now predicts molecular consequences directly from DNA sequence, filling the
annotation gap.

```mermaid
flowchart LR
  SEQ["DNA sequence window"] --> NET["Deep model (CNN / Transformer)"]
  NET --> EPI["Predicted chromatin / expression tracks"]
  EPI --> VEP["Variant effect = predicted change (ref vs alt)"]
  VEP --> PRIOR["Prioritised causal variants"]
```

Sequence-to-function models — **DeepSEA**, **Basenji/Enformer** — read long
windows and predict chromatin accessibility, transcription-factor binding and
expression; scoring a variant means comparing predictions for the reference and
alternate alleles. For protein-coding variants, **AlphaMissense** and language
models (**ESM**) classify missense variants as benign or pathogenic, and
**AlphaFold** structures inform effect.

These are trained on huge functional-genomics corpora; accuracy improves with
training data and model scale but with diminishing returns, a familiar
saturating learning curve:

```plot
{"title": "Variant-effect prediction accuracy vs training data", "xLabel": "labeled data / model scale (relative)", "yLabel": "validation accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1.5)", "label": "learning curve", "color": "#2563eb"}]}
```

Caveats mirror all of genomic ML: **distribution shift** across ancestries and
cell types, the gap between predicting a molecular readout and proving causal
disease relevance, and the need for experimental validation (**MPRAs**,
saturation editing) before clinical use.

**Next:** the capstone quiz.
""",
        ),
        _quiz(),
    ),
)


GENETICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["GENETICS_COURSES"]
