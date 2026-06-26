"""Introduction to Bioinformatics track: Basics -> Intermediate -> Advanced.

A university-level path from biological data and the central problems, through
the core algorithms, databases and tools (sequence alignment, BLAST, HMMs,
phylogenetics, read mapping, variant calling), to reproducible pipelines, data
integration and modern AI methods (deep learning for variant effects and
protein structure). Lessons use interactive ```plot blocks for quantitative
relationships (scoring, growth, error rates, dynamics) and ```mermaid diagrams
for pipelines, data flows and classifications.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Bioinformatics -- Basics --------------------------------------------------

_BASICS = SeedCourse(
    slug="bioinformatics-basics",
    title="Introduction to Bioinformatics — Basics",
    description=(
        "What bioinformatics is and the biological data it works with: DNA, RNA "
        "and proteins as sequences; the central dogma; genomes and the cost of "
        "sequencing; the central computational problems (search, alignment, "
        "assembly, annotation); and the file formats and public databases that "
        "hold life-science data. Built on real biological detail with "
        "interactive plots and pipeline diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is bioinformatics and why it exists",
            "10 min",
            r"""
# What is bioinformatics and why it exists

**Bioinformatics** is the science of storing, searching and analysing
biological data with computers. It arose because biology became a data science:
DNA sequencing, mass spectrometry and high-throughput assays now produce
information faster than humans can read it, so algorithms and statistics are
required to extract biological meaning.

The discipline sits at the intersection of biology, computer science and
statistics. Typical questions include: *which gene does this sequence come
from?*, *how are two species related?*, *which mutation causes this disease?*
and *what does this protein do?*

```mermaid
flowchart LR
  BIO["Biology: cells, genomes, proteins"] --> DATA["Raw data: reads, spectra, images"]
  CS["Computer science: algorithms, data structures"] --> TOOLS["Tools & pipelines"]
  STAT["Statistics: inference, models"] --> TOOLS
  DATA --> TOOLS --> KNOW["Biological knowledge"]
```

A key driver is scale. Sequencing cost has fallen far faster than Moore's law:
the cost per genome dropped from roughly $100 million in 2001 to under $1000 by
the late 2010s. Falling cost means exponentially more data, which makes
computation the bottleneck rather than the lab bench.

```plot
{"title": "Sequencing data accumulation over time", "xLabel": "years since 2005", "yLabel": "relative data volume", "xRange": [0, 12], "yRange": [0, 30], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "data volume", "color": "#2563eb"}]}
```

**Next:** the molecules behind the data — DNA, RNA and protein.
""",
        ),
        _t(
            "Biological sequences: DNA, RNA and protein",
            "11 min",
            r"""
# Biological sequences: DNA, RNA and protein

The three core biological polymers are read as **strings** in bioinformatics.
**DNA** uses a 4-letter alphabet $\{A, C, G, T\}$; **RNA** replaces $T$ with $U$;
**proteins** use a 20-letter amino-acid alphabet. DNA is double-stranded, with
$A$ pairing $T$ and $C$ pairing $G$ — **complementary base pairing**, which lets
each strand template the other.

The **central dogma** describes information flow: DNA is **transcribed** into
mRNA, which is **translated** into protein. Translation reads mRNA in triplets
(**codons**); the 64 codons map to 20 amino acids plus stop signals via the
**genetic code**, which is redundant (degenerate).

```mermaid
flowchart LR
  DNA["DNA (A C G T)"] -->|transcription| RNA["mRNA (A C G U)"]
  RNA -->|translation| PROT["Protein (20 amino acids)"]
  DNA -->|replication| DNA
```

Because there are 4 DNA letters, a random $k$-mer (substring of length $k$)
has $4^k$ possible values, so the space of motifs grows explosively with length —
the reason specific sequences are informative.

```plot
{"title": "Number of distinct DNA k-mers", "xLabel": "k-mer length k", "yLabel": "4^k distinct k-mers", "xRange": [0, 6], "yRange": [0, 4200], "grid": true, "functions": [{"expr": "4^x", "label": "4^k", "color": "#dc2626"}]}
```

GC content (fraction of $G$+$C$) varies between organisms and genome regions and
is a simple but useful descriptor for classification and quality control.

**Next:** the central computational problems bioinformatics solves.
""",
        ),
        _t(
            "The central computational problems",
            "12 min",
            r"""
# The central computational problems

Most of bioinformatics reduces to a handful of recurring problems on sequences.
Understanding them as abstract tasks helps you pick the right tool.

- **Search**: find where a query sequence occurs in a large database (e.g.
  BLAST against GenBank).
- **Alignment**: line up two or more sequences to reveal conserved and divergent
  positions, scoring matches, mismatches and gaps.
- **Assembly**: reconstruct a genome from millions of short overlapping reads.
- **Annotation**: label a genome with genes, regulatory elements and function.
- **Phylogenetics**: infer evolutionary trees from sequence differences.

```mermaid
flowchart TB
  RAW["Sequencing reads"] --> ASM["Assembly"]
  ASM --> ANN["Annotation: genes, features"]
  Q["Query sequence"] --> SRCH["Search / BLAST"]
  ANN --> ALN["Multiple alignment"]
  ALN --> PHY["Phylogenetic tree"]
```

These problems are computationally hard because data is huge. A naive
all-against-all comparison of $n$ sequences scales as $n^2$, which becomes
infeasible quickly — motivating the indexing and heuristic methods covered
later.

```plot
{"title": "Cost of naive all-vs-all comparison", "xLabel": "number of sequences n", "yLabel": "pairwise comparisons (thousands)", "xRange": [0, 100], "yRange": [0, 5], "grid": true, "functions": [{"expr": "x^2/2000", "label": "n(n-1)/2 ~ n^2/2", "color": "#16a34a"}]}
```

**Next:** the file formats that carry biological data.
""",
        ),
        _t(
            "File formats: FASTA, FASTQ and beyond",
            "11 min",
            r"""
# File formats: FASTA, FASTQ and beyond

Bioinformatics runs on plain-text and binary file formats, each tuned to a kind
of data. Knowing them is half the daily work.

**FASTA** stores sequences: a header line starting with `>` followed by the
residues. **FASTQ** extends this for sequencing reads by adding a **quality
line** encoding a per-base **Phred score** $Q = -10\log_{10}(P_{error})$. So
$Q=20$ means a 1% error probability and $Q=30$ means 0.1%.

```
@read1
ACGTACGTACGT
+
IIIIIIIIIIII
```

Downstream formats include **SAM/BAM** (read alignments to a reference),
**VCF** (called variants), **GFF/GTF** (genome annotations) and **BED**
(genomic intervals).

```mermaid
flowchart LR
  FASTQ["FASTQ reads + quality"] --> BAM["BAM: aligned reads"]
  REF["FASTA reference"] --> BAM
  BAM --> VCF["VCF: variants"]
  GFF["GFF/GTF annotation"] --> VCF
```

The Phred scale is logarithmic, so error probability falls steeply as quality
rises — a few extra Phred points dramatically improves confidence.

```plot
{"title": "Phred quality vs base-error probability", "xLabel": "Phred score Q", "yLabel": "error probability P", "xRange": [0, 40], "yRange": [0, 1], "grid": true, "functions": [{"expr": "10^(-x/10)", "label": "P = 10^(-Q/10)", "color": "#2563eb"}]}
```

**Next:** the public databases that store the world's biological data.
""",
        ),
        _t(
            "Biological databases and resources",
            "11 min",
            r"""
# Biological databases and resources

A defining feature of bioinformatics is its reliance on **public databases**.
Most analyses begin or end with a lookup against a curated resource maintained
by international centres (NCBI, EMBL-EBI, DDBJ).

Key resources include:

- **GenBank / ENA / DDBJ** — the primary nucleotide sequence archives (mirrored).
- **RefSeq** — curated, non-redundant reference sequences.
- **UniProt** — protein sequences with functional annotation.
- **PDB** — experimentally determined 3D protein structures.
- **Ensembl / UCSC Genome Browser** — annotated genomes with visualisation.
- **SRA** — raw sequencing reads from experiments.

```mermaid
flowchart TB
  EXP["Experiment"] --> SRA["SRA: raw reads"]
  SRA --> GB["GenBank/ENA: assembled sequences"]
  GB --> REFSEQ["RefSeq: curated references"]
  GB --> UNIPROT["UniProt: proteins"]
  UNIPROT --> PDB["PDB: structures"]
```

Databases grow roughly exponentially as sequencing scales, so search and
indexing must keep pace. Identifiers (accession numbers) and cross-references
let tools navigate between resources programmatically via APIs.

```plot
{"title": "Database entry growth over time", "xLabel": "years", "yLabel": "relative number of entries", "xRange": [0, 15], "yRange": [0, 25], "grid": true, "functions": [{"expr": "exp(0.22*x)", "label": "entries", "color": "#dc2626"}]}
```

**Next:** test your grasp of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- Bioinformatics -- Intermediate --------------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="bioinformatics-intermediate",
    title="Introduction to Bioinformatics — Intermediate",
    description=(
        "The core quantitative methods of sequence analysis: dynamic-programming "
        "alignment (Needleman-Wunsch and Smith-Waterman), substitution matrices "
        "and gap penalties, heuristic database search with BLAST and its E-value "
        "statistics, hidden Markov models for sequence families, multiple "
        "sequence alignment, and distance- and likelihood-based phylogenetics. "
        "Includes interactive plots of scoring and tree dynamics."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Pairwise alignment by dynamic programming",
            "13 min",
            r"""
# Pairwise alignment by dynamic programming

**Pairwise alignment** finds the best correspondence between two sequences.
Brute force is exponential, but **dynamic programming** (DP) solves it in
$O(mn)$ time by filling a scoring matrix.

**Needleman-Wunsch** computes a **global** alignment (end to end). Each cell
$F(i,j)$ holds the best score aligning the first $i$ and $j$ residues:

$$F(i,j) = \max\begin{cases} F(i-1,j-1) + s(x_i,y_j) \\ F(i-1,j) - d \\ F(i,j-1) - d \end{cases}$$

where $s$ is the substitution score and $d$ the gap penalty. **Smith-Waterman**
gives a **local** alignment by adding a 0 option, so the score never goes
negative and the best subsegment is found.

```mermaid
flowchart LR
  X["Sequence X"] --> M["Fill DP matrix F(i,j)"]
  Y["Sequence Y"] --> M
  M --> TB["Traceback from best cell"]
  TB --> A["Optimal alignment"]
```

Alignment score grows with sequence length when sequences are related, and the
relationship is roughly linear in the aligned length once a fixed identity is
assumed.

```plot
{"title": "Alignment score vs aligned length", "xLabel": "aligned length", "yLabel": "raw score", "xRange": [0, 100], "yRange": [0, 200], "grid": true, "functions": [{"expr": "2*x", "label": "score ~ 2 * length", "color": "#2563eb"}]}
```

**Next:** the matrices and penalties that make scores biologically meaningful.
""",
        ),
        _t(
            "Substitution matrices and gap penalties",
            "12 min",
            r"""
# Substitution matrices and gap penalties

Alignment quality depends on the **scoring scheme**. For proteins, a
**substitution matrix** gives a log-odds score for each amino-acid pair:

$$s(a,b) = \frac{1}{\lambda} \log \frac{p_{ab}}{q_a q_b}$$

where $p_{ab}$ is the observed substitution frequency in related sequences and
$q_a q_b$ the chance expectation. **PAM** matrices are derived from closely
related sequences and extrapolated; **BLOSUM** matrices (e.g. BLOSUM62) are
derived directly from conserved blocks at a given identity threshold.

```mermaid
flowchart LR
  ALN["Trusted alignments"] --> FREQ["Substitution frequencies p_ab"]
  FREQ --> LOGODDS["Log-odds scores"]
  LOGODDS --> MAT["BLOSUM / PAM matrix"]
```

**Gap penalties** model insertions/deletions. An **affine** model charges a
large gap-opening cost plus a small per-residue extension cost:
$\gamma(g) = -(o + e \cdot g)$. This favours a few long gaps over many short
ones, matching how indels actually occur.

```plot
{"title": "Affine gap penalty vs gap length", "xLabel": "gap length g", "yLabel": "penalty magnitude", "xRange": [0, 20], "yRange": [0, 30], "grid": true, "functions": [{"expr": "10 + 1*x", "label": "open + extend*g", "color": "#dc2626"}]}
```

Choosing a matrix matched to expected divergence (e.g. BLOSUM45 for distant,
BLOSUM80 for close) materially changes which alignments are found.

**Next:** searching huge databases quickly with BLAST.
""",
        ),
        _t(
            "BLAST and the statistics of search",
            "13 min",
            r"""
# BLAST and the statistics of search

Full DP against an entire database is too slow, so **BLAST** (Basic Local
Alignment Search Tool) uses a **seed-and-extend** heuristic: it finds short
exact or near-exact **words** shared by query and database, then extends them
into local alignments only where seeds hit.

```mermaid
flowchart LR
  Q["Query"] --> W["Break into words (k-mers)"]
  W --> HIT["Find word hits in DB index"]
  HIT --> EXT["Ungapped/gapped extension"]
  EXT --> HSP["High-scoring pairs (HSPs)"]
  HSP --> EVAL["E-value & ranking"]
```

The key output is the **E-value**: the expected number of alignments scoring at
least as high *by chance* in a database of that size. It follows the
Karlin-Altschul model:

$$E = K\,m\,n\,e^{-\lambda S}$$

where $m,n$ are query and database lengths, $S$ the score, and $K,\lambda$
parameters of the scoring system. Because $E$ decays **exponentially** with
score, a small score increase makes a hit far more significant.

```plot
{"title": "BLAST E-value vs alignment score", "xLabel": "bit score S", "yLabel": "E-value", "xRange": [0, 40], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.3*x)", "label": "E ~ exp(-lambda*S)", "color": "#2563eb"}]}
```

A common threshold is $E < 10^{-5}$ for confident homology. Lower E-values mean
fewer chance hits expected, hence stronger evidence of true relationship.

**Next:** modelling whole sequence families with HMMs.
""",
        ),
        _t(
            "Hidden Markov models for sequences",
            "13 min",
            r"""
# Hidden Markov models for sequences

A **hidden Markov model (HMM)** models a sequence as generated by hidden states
that emit symbols. In bioinformatics, **profile HMMs** represent a sequence
family with per-position **match**, **insert** and **delete** states, capturing
position-specific conservation far better than a single matrix.

```mermaid
flowchart LR
  BEGIN["Begin"] --> M1["Match 1"]
  M1 --> M2["Match 2"]
  M1 --> I1["Insert"]
  M1 --> D2["Delete"]
  M2 --> END["End"]
```

Three algorithms power HMMs: **Viterbi** finds the most likely state path
(decoding), **forward** computes the total probability of a sequence, and
**Baum-Welch** (EM) trains parameters from data. Tools like **HMMER** use
profile HMMs to detect remote homologs and to build domain databases (e.g.
**Pfam**).

The probability of a state path is a product of transition and emission
probabilities; in log space these become sums, so log-likelihood grows
approximately linearly with sequence length for a well-matched model.

```plot
{"title": "Log-likelihood accumulation along a sequence", "xLabel": "position in sequence", "yLabel": "negative log-likelihood", "xRange": [0, 50], "yRange": [0, 100], "grid": true, "functions": [{"expr": "2*x", "label": "-log P (sums per position)", "color": "#16a34a"}]}
```

Profile HMMs detect distant relationships that pairwise BLAST misses, because
they pool information across many family members.

**Next:** aligning many sequences at once.
""",
        ),
        _t(
            "Multiple sequence alignment",
            "12 min",
            r"""
# Multiple sequence alignment

A **multiple sequence alignment (MSA)** aligns three or more sequences
simultaneously, exposing conserved columns, motifs and the input for
phylogenetics. Optimal MSA by DP is NP-hard (cost scales as $L^N$ for $N$
sequences of length $L$), so practical tools use heuristics.

The dominant heuristic is **progressive alignment**: build a rough guide tree,
then align sequences/profiles from most to least similar. **Clustal Omega**,
**MUSCLE** and **MAFFT** refine this with iterative methods and consistency
scoring.

```mermaid
flowchart TB
  SEQ["Input sequences"] --> DIST["Pairwise distances"]
  DIST --> TREE["Guide tree"]
  TREE --> PROG["Progressive alignment"]
  PROG --> REFINE["Iterative refinement"]
  REFINE --> MSA["Final MSA"]
```

Conservation per column is often summarised by **information content** (in bits),
visualised as a **sequence logo** where taller letters mark more conserved
positions. The exact-DP cost explodes with the number of sequences, justifying
the heuristics:

```plot
{"title": "Exact MSA cost vs number of sequences", "xLabel": "number of sequences N", "yLabel": "relative cost", "xRange": [0, 8], "yRange": [0, 260], "grid": true, "functions": [{"expr": "2^x", "label": "grows like L^N", "color": "#dc2626"}]}
```

**Next:** turning alignments into evolutionary trees.
""",
        ),
        _t(
            "Phylogenetics: trees from sequences",
            "13 min",
            r"""
# Phylogenetics: trees from sequences

**Phylogenetics** infers evolutionary relationships as a **tree** whose leaves
are taxa and whose internal nodes are common ancestors. The input is usually an
MSA; the output is a tree with branch lengths proportional to evolutionary
change.

Three method families dominate:

- **Distance-based** (e.g. neighbor-joining): convert the MSA to a pairwise
  distance matrix, then build a tree that fits it.
- **Maximum parsimony**: prefer the tree requiring the fewest mutations.
- **Maximum likelihood / Bayesian** (RAxML, IQ-TREE, MrBayes): score trees under
  an explicit substitution model (e.g. Jukes-Cantor, GTR).

```mermaid
flowchart LR
  MSA["Multiple alignment"] --> MODEL["Substitution model"]
  MODEL --> SEARCH["Tree search"]
  SEARCH --> SUPPORT["Bootstrap support"]
  SUPPORT --> TREE["Phylogenetic tree"]
```

Observed differences saturate over time: as positions mutate repeatedly,
apparent distance plateaus below the true number of substitutions. Correction
models (e.g. Jukes-Cantor) recover true distance from a saturating observed
curve:

```plot
{"title": "Observed vs true evolutionary distance (saturation)", "xLabel": "true substitutions per site", "yLabel": "observed fraction different", "xRange": [0, 5], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.75*(1 - exp(-x))", "label": "Jukes-Cantor curve", "color": "#2563eb"}]}
```

**Bootstrapping** resamples alignment columns to estimate branch support.

**Next:** check your understanding of the core methods.
""",
        ),
        _quiz(),
    ),
)


# -- Bioinformatics -- Advanced ------------------------------------------------

_ADVANCED = SeedCourse(
    slug="bioinformatics-advanced",
    title="Introduction to Bioinformatics — Advanced",
    description=(
        "State-of-the-art and applied bioinformatics: next-generation sequencing "
        "and read mapping with the Burrows-Wheeler transform, variant calling and "
        "the GATK best practices, RNA-seq and differential expression, "
        "reproducible workflows with Nextflow/Snakemake and containers, "
        "multi-omics data integration, and deep learning for genomics and protein "
        "structure (AlphaFold). Includes interactive plots of coverage, "
        "dispersion and model behaviour."
    ),
    level="Advanced",
    lessons=(
        _t(
            "NGS read mapping and the Burrows-Wheeler transform",
            "13 min",
            r"""
# NGS read mapping and the Burrows-Wheeler transform

**Next-generation sequencing (NGS)** produces hundreds of millions of short
reads. **Read mapping** aligns each read to a reference genome — but full
DP per read against 3 billion bases is hopeless. Modern mappers (**BWA**,
**Bowtie2**) use the **Burrows-Wheeler transform (BWT)** and the **FM-index** to
search in time roughly proportional to read length, independent of genome size.

The BWT reversibly permutes the reference so that exact substring search
becomes a fast backward-extension over a compact index. Inexact matching
(allowing mismatches/indels) is layered on top with seed-and-extend.

```mermaid
flowchart LR
  REF["Reference genome"] --> BWT["BWT + FM-index"]
  READS["Short reads"] --> ALIGN["Backward search + extension"]
  BWT --> ALIGN
  ALIGN --> BAM["Sorted BAM"]
```

**Coverage** (mean reads per base) governs sensitivity. Under a Poisson model,
the probability a base is missed falls exponentially with mean coverage
$\lambda$ as $e^{-\lambda}$, so 30x coverage leaves a negligible fraction
uncovered.

```plot
{"title": "Fraction of genome uncovered vs mean coverage", "xLabel": "mean coverage (x)", "yLabel": "fraction uncovered", "xRange": [0, 15], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "e^(-lambda)", "color": "#dc2626"}]}
```

**Next:** turning aligned reads into confident variant calls.
""",
        ),
        _t(
            "Variant calling and best practices",
            "13 min",
            r"""
# Variant calling and best practices

**Variant calling** identifies where a sample differs from the reference: SNPs,
insertions/deletions (indels) and larger structural variants. The de-facto
standard is the **GATK best-practices** workflow.

Steps include marking PCR duplicates, **base quality score recalibration
(BQSR)**, and probabilistic genotype calling with **HaplotypeCaller**, which
locally reassembles reads into candidate haplotypes rather than calling per
base. Calls are emitted as **VCF** and then **filtered** (hard filters or
variant quality score recalibration, VQSR).

```mermaid
flowchart TB
  BAM["Aligned BAM"] --> DUP["Mark duplicates"]
  DUP --> BQSR["Base recalibration"]
  BQSR --> CALL["HaplotypeCaller"]
  CALL --> VCF["Raw VCF"]
  VCF --> FILT["Filtering / VQSR"]
  FILT --> ANN["Annotation (VEP/SnpEff)"]
```

Call confidence is reported as a Phred-scaled quality $QUAL$, where the
probability the call is wrong is $10^{-QUAL/10}$ — so higher QUAL means
exponentially fewer false positives.

```plot
{"title": "Variant false-call probability vs QUAL", "xLabel": "QUAL (Phred)", "yLabel": "P(call is wrong)", "xRange": [0, 50], "yRange": [0, 1], "grid": true, "functions": [{"expr": "10^(-x/10)", "label": "10^(-QUAL/10)", "color": "#2563eb"}]}
```

Functional annotation (VEP, SnpEff) then predicts each variant's effect on
genes and proteins.

**Next:** measuring gene expression with RNA-seq.
""",
        ),
        _t(
            "RNA-seq and differential expression",
            "13 min",
            r"""
# RNA-seq and differential expression

**RNA-seq** measures gene expression by sequencing the transcriptome. Reads are
either aligned (STAR, HISAT2) or pseudo-aligned (**Salmon**, **kallisto**) to
quantify per-gene or per-transcript counts. The central question is
**differential expression**: which genes change between conditions?

Counts are **over-dispersed** (variance exceeds the mean), so a simple Poisson
model fails. **DESeq2** and **edgeR** use the **negative binomial**
distribution, with $\text{Var} = \mu + \alpha\mu^2$ where $\alpha$ is the
dispersion, estimated robustly by shrinking gene-wise estimates toward a fitted
trend.

```mermaid
flowchart LR
  FASTQ["RNA-seq reads"] --> QUANT["Quantify (Salmon/STAR)"]
  QUANT --> COUNTS["Count matrix"]
  COUNTS --> NORM["Normalize (size factors)"]
  NORM --> NB["Negative binomial model"]
  NB --> DE["DE genes + adjusted p-values"]
```

Variance rising faster than the mean is exactly the over-dispersion that
motivates the negative binomial:

```plot
{"title": "Count variance vs mean (over-dispersion)", "xLabel": "mean expression mu", "yLabel": "variance", "xRange": [0, 10], "yRange": [0, 60], "grid": true, "functions": [{"expr": "x + 0.5*x^2", "label": "mu + alpha*mu^2", "color": "#dc2626"}]}
```

Thousands of simultaneous tests demand **multiple-testing correction**
(Benjamini-Hochberg FDR) to control false discoveries.

**Next:** making analyses reproducible with workflow managers.
""",
        ),
        _t(
            "Reproducible pipelines and workflows",
            "12 min",
            r"""
# Reproducible pipelines and workflows

A real analysis chains many tools; reproducing it months later, or on another
machine, is hard unless the pipeline is explicit and versioned.
**Reproducibility** rests on three pillars: a **workflow manager**, pinned
**environments**, and tracked **provenance**.

**Workflow managers** like **Nextflow** and **Snakemake** describe steps as a
**directed acyclic graph (DAG)** of tasks with declared inputs/outputs, enabling
automatic parallelism, resume-on-failure, and portability across HPC and cloud.
**Containers** (Docker, Singularity) and environment files (Conda) pin exact tool
versions so results do not drift.

```mermaid
flowchart LR
  RAW["Raw data"] --> QC["QC (FastQC)"]
  QC --> MAP["Mapping"]
  MAP --> CALL["Calling / quantify"]
  CALL --> REPORT["Report (MultiQC)"]
  ENV["Containers + pinned versions"] -.-> MAP
  ENV -.-> CALL
```

Workflow managers also cache completed steps, so re-running after a change only
recomputes affected tasks — runtime grows with the *changed* fraction, not the
whole pipeline, saving large amounts of compute on iterative work.

```plot
{"title": "Re-run cost vs fraction of pipeline changed", "xLabel": "fraction of steps changed (%)", "yLabel": "recompute cost (%)", "xRange": [0, 100], "yRange": [0, 100], "grid": true, "functions": [{"expr": "x", "label": "only changed steps rerun", "color": "#16a34a"}]}
```

Standards like **FAIR** (Findable, Accessible, Interoperable, Reusable) and
recorded random seeds complete reproducible practice.

**Next:** integrating many data types into one picture.
""",
        ),
        _t(
            "Multi-omics data integration",
            "12 min",
            r"""
# Multi-omics data integration

Biology is governed by interacting layers — genome, epigenome, transcriptome,
proteome, metabolome. **Multi-omics integration** combines these to explain
phenotypes that any single layer cannot. The challenge is heterogeneity:
different scales, noise models, dimensionality and missingness.

```mermaid
flowchart TB
  GEN["Genomics"] --> INT["Integration"]
  EPI["Epigenomics"] --> INT
  TRANS["Transcriptomics"] --> INT
  PROT["Proteomics"] --> INT
  INT --> MODEL["Joint model / network"]
  MODEL --> PHENO["Phenotype / mechanism"]
```

Common strategies: **early integration** (concatenate features), **late
integration** (combine per-omics models), and **intermediate** methods that
learn a shared latent space — e.g. **MOFA** (multi-omics factor analysis),
similarity network fusion, and joint matrix factorization.

A core obstacle is the **curse of dimensionality**: features vastly outnumber
samples, so model complexity must be controlled. The risk of spurious
correlations rises sharply as dimensionality grows relative to sample size,
motivating regularization and dimensionality reduction:

```plot
{"title": "Spurious-association risk vs feature/sample ratio", "xLabel": "features per sample", "yLabel": "relative false-discovery risk", "xRange": [0, 20], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+3)", "label": "risk saturates high", "color": "#2563eb"}]}
```

**Next:** deep learning for genomics and protein structure.
""",
        ),
        _t(
            "Deep learning in genomics and structure",
            "13 min",
            r"""
# Deep learning in genomics and structure

Deep learning now leads several bioinformatics tasks where features are hard to
hand-engineer. **Convolutional neural networks** read raw DNA to predict
regulatory activity (DeepSEA, Basenji); **transformers** model long-range
genomic context (Enformer) and protein language (ESM). The landmark result is
**AlphaFold**, which predicts 3D protein structure from sequence at near-
experimental accuracy by learning from MSAs and structural data.

```mermaid
flowchart LR
  SEQ["Protein sequence"] --> MSA["MSA / embeddings"]
  MSA --> NET["Deep network (Evoformer)"]
  NET --> STR["3D structure prediction"]
  STR --> CONF["Per-residue confidence (pLDDT)"]
```

These models are powerful but need care: they can learn dataset biases, and
**confidence calibration** matters — AlphaFold's per-residue **pLDDT** flags
unreliable regions. As with any model, performance improves with data but with
**diminishing returns**, so curated, diverse training data beats raw volume.

```plot
{"title": "Model accuracy vs training data (diminishing returns)", "xLabel": "relative training data", "yLabel": "accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating accuracy", "color": "#16a34a"}]}
```

Interpretability (saliency, attention) and rigorous held-out evaluation remain
essential before clinical or experimental use.

**Next:** test your command of state-of-the-art bioinformatics.
""",
        ),
        _quiz(),
    ),
)


BIOINFORMATICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["BIOINFORMATICS_COURSES"]
