"""Genomics track: Basics -> Intermediate -> Advanced.

A university-level genomics curriculum: from genome structure, chromosomes and
the chemistry of sequencing, through assembly, annotation, alignment and
variant calling, to comparative, functional and clinical genomics with modern
AI/deep-learning methods. Lessons use interactive ```plot blocks for
quantitative relationships (coverage, error models, read-length distributions,
selection) and ```mermaid diagrams for genome organization, pipelines and
workflows.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Genomics -- Basics -------------------------------------------------------

_BASICS = SeedCourse(
    slug="genomics-basics",
    title="Genomics — Basics",
    description=(
        "What a genome is and how we read it. The structure of genomes, "
        "chromosomes and gene content; the difference between genetics and "
        "genomics; the chemistry behind Sanger and next-generation sequencing; "
        "and the core ideas of coverage and read alignment. Built on real "
        "molecular detail with interactive plots and process diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is a genome?",
            "10 min",
            r"""
# What is a genome?

A **genome** is the complete set of genetic material in a cell — all of its DNA,
including coding genes, regulatory elements, and the large non-coding fraction.
**Genetics** studies single genes and their inheritance; **genomics** studies
the genome as a whole: its sequence, structure, function and evolution, usually
with high-throughput data and computation.

Genome sizes vary enormously. The human genome is about **3.2 billion base pairs
(3.2 Gb)** across 23 chromosome pairs, with roughly **20,000 protein-coding
genes** — under 2% of the sequence. *E. coli* has ~4.6 Mb; the wheat genome is
~16 Gb. Size does not track complexity (the **C-value paradox**), because much of
a large genome is repetitive and non-coding.

```mermaid
flowchart LR
  GENOME["Genome (all DNA)"] --> CODING["Coding genes (~2%)"]
  GENOME --> REG["Regulatory elements"]
  GENOME --> REPEAT["Repeats & transposons"]
  GENOME --> NC["Non-coding RNA & introns"]
```

Genome size in base pairs spans many orders of magnitude across the tree of
life, so we usually reason in log scale:

```plot
{"title": "Genome size grows steeply across organisms (log scale view)", "xLabel": "organism rank (simple to complex)", "yLabel": "log10 genome size (bp)", "xRange": [0, 10], "yRange": [6, 11], "grid": true, "functions": [{"expr": "6+0.5*x", "label": "log10 bp", "color": "#2563eb"}]}
```

**Next:** how DNA is packaged into chromosomes.
""",
        ),
        _t(
            "Chromosomes and genome organization",
            "10 min",
            r"""
# Chromosomes and genome organization

Genomic DNA is not naked: it is wrapped around **histone** octamers to form
**nucleosomes**, then coiled into **chromatin** and, during mitosis, condensed
into **chromosomes**. Eukaryotic chromosomes carry a **centromere** (for
spindle attachment) and **telomeres** (protective repeat caps, ...TTAGGG... in
humans) that shorten with each division.

Genomes mix **euchromatin** (open, gene-rich, transcribed) and
**heterochromatin** (condensed, repeat-rich, mostly silent). Beyond the nuclear
genome, eukaryotes carry small **organellar genomes**: the circular
**mitochondrial** genome (~16.6 kb in humans) and, in plants, the chloroplast
genome.

```mermaid
flowchart TB
  DNA["Double helix"] --> NUC["Nucleosome (DNA + histones)"]
  NUC --> FIBER["30 nm chromatin fiber"]
  FIBER --> CHR["Condensed chromosome"]
  CHR --> CEN["Centromere"]
  CHR --> TEL["Telomeres"]
```

Gene density is uneven along a chromosome: gene-rich euchromatic arms versus
gene-poor pericentromeric heterochromatin. A simplified density profile peaks
away from the centromere:

```plot
{"title": "Gene density varies along a chromosome", "xLabel": "position along arm (relative)", "yLabel": "relative gene density", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-((x-7)^2)/6)", "label": "gene density", "color": "#16a34a"}]}
```

**Next:** what genes and the non-coding genome actually contain.
""",
        ),
        _t(
            "Genes, non-coding DNA and repeats",
            "11 min",
            r"""
# Genes, non-coding DNA and repeats

A **gene** is a stretch of DNA transcribed into a functional product. In
eukaryotes a protein-coding gene has a **promoter**, **exons** (retained in
mature mRNA) and **introns** (spliced out), plus **untranslated regions** (UTRs)
that regulate translation and stability. **Alternative splicing** lets one gene
encode several proteins.

Most of the human genome is **non-coding**. Major classes include regulatory
elements (**enhancers, silencers, insulators**), genes for **non-coding RNAs**
(rRNA, tRNA, miRNA, lncRNA), and vast amounts of **repetitive DNA** — tandem
repeats (microsatellites) and interspersed **transposable elements** such as
**LINEs, SINEs (e.g. Alu)** and LTR retrotransposons. Repeats make assembly and
alignment hard because identical copies are ambiguous to place.

```mermaid
flowchart LR
  GENE["Protein-coding gene"] --> PROM["Promoter"]
  GENE --> UTR5["5' UTR"]
  GENE --> EXON["Exons"]
  GENE --> INTRON["Introns"]
  GENE --> UTR3["3' UTR"]
```

Repeat families differ in copy number; abundance falls off steeply from the
most common families, a roughly exponential decay:

```plot
{"title": "Repeat family abundance falls off (schematic)", "xLabel": "repeat family rank", "yLabel": "relative copy number", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "copy number", "color": "#dc2626"}]}
```

**Next:** the original way we read DNA — Sanger sequencing.
""",
        ),
        _t(
            "Sanger sequencing",
            "10 min",
            r"""
# Sanger sequencing

**Sanger (chain-termination) sequencing**, developed by Frederick Sanger in
1977, dominated for three decades and still anchors many validation workflows.
A single-stranded template is copied by **DNA polymerase** from a primer in the
presence of normal **dNTPs** plus a small fraction of fluorescently labelled
**dideoxynucleotides (ddNTPs)**. A ddNTP lacks the 3'-OH needed to add the next
base, so incorporation **terminates the chain**.

The result is a population of fragments of every possible length, each ending in
a labelled base. **Capillary electrophoresis** separates them by size to
single-base resolution; the colour at each position reads off the sequence as a
**chromatogram**. Read lengths reach ~**500-1000 bp** with very high per-base
accuracy.

```mermaid
flowchart LR
  TEMPLATE["ssDNA template + primer"] --> POL["Polymerase + dNTPs + ddNTPs"]
  POL --> FRAG["Length-terminated fragments"]
  FRAG --> CE["Capillary electrophoresis"]
  CE --> READ["Chromatogram -> sequence"]
```

Sanger is accurate but **low-throughput and costly per base**, which is why the
field moved to massively parallel methods. Its accuracy still makes it the gold
standard for confirming individual variants. Per-base quality is reported as a
**Phred score** $Q = -10 \log_{10}(P_{error})$:

```plot
{"title": "Phred quality maps error probability to a score", "xLabel": "Phred Q score", "yLabel": "error probability", "xRange": [0, 50], "yRange": [0, 1], "grid": true, "functions": [{"expr": "10^(-x/10)", "label": "P(error)", "color": "#2563eb"}]}
```

**Next:** how next-generation sequencing reads millions of fragments at once.
""",
        ),
        _t(
            "Next-generation sequencing",
            "11 min",
            r"""
# Next-generation sequencing

**Next-generation sequencing (NGS)** reads millions to billions of fragments in
parallel, collapsing the cost per base by orders of magnitude. The dominant
platform, **Illumina**, uses **sequencing by synthesis**: fragmented DNA is
ligated to adapters, **clonally amplified** into clusters by bridge
amplification on a flow cell, then sequenced one base per cycle using
**reversible-terminator** fluorescent nucleotides imaged each round.

Illumina reads are short (~**100-300 bp**) but extremely numerous and accurate.
**Long-read** platforms complement them: **Oxford Nanopore** measures ionic
current as DNA threads through a protein pore, and **PacBio HiFi** reads a
circular template many times for high-accuracy long reads. Long reads span
repeats and structural variants that short reads cannot resolve.

```mermaid
flowchart LR
  LIB["Library: fragment + adapters"] --> CLUST["Cluster amplification"]
  CLUST --> SBS["Sequencing by synthesis"]
  SBS --> IMG["Per-cycle imaging"]
  IMG --> READS["Millions of short reads"]
```

Cost per genome has fallen faster than Moore's law — an exponential decline that
made population-scale genomics feasible:

```plot
{"title": "Sequencing cost per genome (schematic decline)", "xLabel": "years since 2008", "yLabel": "relative cost", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.6*x)", "label": "relative cost", "color": "#dc2626"}]}
```

**Next:** coverage and how we line reads up to a reference.
""",
        ),
        _t(
            "Coverage and read alignment",
            "10 min",
            r"""
# Coverage and read alignment

**Coverage (depth)** is how many reads overlap a given position. The **Lander-
Waterman** expectation is $C = \frac{N L}{G}$, where $N$ reads of length $L$ map
to a genome of size $G$. Higher depth raises confidence: random sequencing
errors at one base are outvoted by many overlapping reads, so 30x is a common
target for human whole-genome variant calling.

Reads are placed against a **reference genome** by **alignment (mapping)**.
Short-read aligners such as **BWA-MEM** and **Bowtie2** use a
**Burrows-Wheeler Transform / FM-index** to find seed matches fast, then extend
them allowing mismatches and gaps. The output is a **SAM/BAM** file recording
each read's position, orientation, **mapping quality (MAPQ)** and a **CIGAR**
string describing matches, insertions and deletions.

```mermaid
flowchart LR
  READS["FASTQ reads"] --> ALIGN["Aligner (BWA-MEM, BWT/FM-index)"]
  REF["Reference genome"] --> ALIGN
  ALIGN --> BAM["SAM/BAM: position + MAPQ + CIGAR"]
  BAM --> PILEUP["Per-base pileup"]
```

The chance a position is missed falls as expected depth rises (Poisson zero
term, $P_{0} = e^{-C}$):

```plot
{"title": "Probability a base is left uncovered vs depth", "xLabel": "expected coverage C", "yLabel": "P(0 reads)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-x)", "label": "P(uncovered)", "color": "#16a34a"}]}
```

**Next:** test what you learned.
""",
        ),
        _quiz(),
    ),
)


# -- Genomics -- Intermediate -------------------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="genomics-intermediate",
    title="Genomics — Intermediate",
    description=(
        "The quantitative core of turning reads into biology: genome assembly "
        "with de Bruijn and overlap graphs, structural and functional "
        "annotation, sequence alignment algorithms, variant calling and "
        "filtering, and the statistics of GWAS. Worked equations, real tools, "
        "interactive plots and pipeline diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Genome assembly: de Bruijn and overlap graphs",
            "12 min",
            r"""
# Genome assembly: de Bruijn and overlap graphs

**De novo assembly** reconstructs a genome from reads with no reference. Two
graph paradigms dominate. **Overlap-Layout-Consensus (OLC)**, used by long-read
assemblers (e.g. **Canu**, **hifiasm**), builds an **overlap graph** where nodes
are reads and edges are detected overlaps, then finds a path through them. OLC
suits long, noisier reads but is computationally heavy on many short reads.

**De Bruijn graphs (DBG)**, used by short-read assemblers (**SPAdes**,
**Velvet**), break reads into overlapping **k-mers**: nodes are length-$(k-1)$
words and edges are k-mers. A genome traversal becomes an **Eulerian path**.
Choosing $k$ trades off: small $k$ collapses repeats into tangles; large $k$
fragments coverage. Output **contigs** are ordered and oriented into
**scaffolds** using paired-end or long-read links.

```mermaid
flowchart LR
  READS["Reads"] --> KMERS["k-mers"]
  KMERS --> DBG["De Bruijn graph"]
  DBG --> CONTIG["Contigs (Eulerian path)"]
  CONTIG --> SCAF["Scaffolds (paired links)"]
```

Assembly contiguity is summarized by **N50**: the contig length such that 50% of
the assembly sits in contigs that long or longer. Distinct k values give
different N50, peaking at an intermediate value:

```plot
{"title": "Assembly N50 vs k-mer size (schematic)", "xLabel": "k-mer size (relative)", "yLabel": "relative N50", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-((x-5)^2)/5)", "label": "N50", "color": "#2563eb"}]}
```

**Next:** finding the genes and features in an assembled genome.
""",
        ),
        _t(
            "Genome annotation",
            "11 min",
            r"""
# Genome annotation

**Annotation** assigns biological meaning to sequence. **Structural annotation**
locates features — genes, exons/introns, UTRs, ncRNAs, repeats; **functional
annotation** attaches identities and roles (gene names, **GO terms**, pathways).

Gene prediction blends two lines of evidence. **Ab initio** predictors
(**AUGUSTUS**, **GeneMark**) model statistical signals: splice sites, start/stop
codons and codon-usage bias captured by **Hidden Markov Models**. **Evidence-
based** methods align **RNA-seq** reads and known proteins to anchor real exons.
Pipelines such as **MAKER** and **BRAKER** combine both. **Repeats** are first
masked (**RepeatMasker**) so they do not generate spurious genes.

```mermaid
flowchart TB
  GENOME["Assembled genome"] --> MASK["Repeat masking"]
  MASK --> ABINITIO["Ab initio prediction (HMM)"]
  MASK --> EVIDENCE["RNA-seq + protein alignment"]
  ABINITIO --> MERGE["Consensus gene models"]
  EVIDENCE --> MERGE
  MERGE --> FUNC["Functional annotation (GO, pathways)"]
```

Coding regions show a strong **3-base periodicity** in nucleotide composition
from codon structure — a signal predictors exploit:

```plot
{"title": "Codon periodicity signal in coding DNA (schematic)", "xLabel": "position (bp)", "yLabel": "composition bias", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.5+0.4*cos(2*x)", "label": "periodic bias", "color": "#16a34a"}]}
```

**Next:** the algorithms that align sequences.
""",
        ),
        _t(
            "Sequence alignment algorithms",
            "12 min",
            r"""
# Sequence alignment algorithms

Alignment quantifies similarity by inserting **gaps** to maximize matches.
**Global alignment** (**Needleman-Wunsch**) aligns two sequences end to end;
**local alignment** (**Smith-Waterman**) finds the best matching subsequence —
ideal for domains embedded in larger sequences. Both are **dynamic programming**:
fill a scoring matrix where each cell is the best of match/mismatch, insertion or
deletion, then trace back the optimal path. Cost is $O(mn)$ in time and space.

Scores use **substitution matrices** (**BLOSUM**, **PAM**) for proteins and an
**affine gap penalty** $w(g) = o + e \cdot g$, charging a larger gap-opening cost
$o$ and a smaller per-base extension $e$ so one long indel is favoured over many
short ones. For database search at scale, **BLAST** uses a fast **seed-and-
extend** heuristic instead of full DP.

```mermaid
flowchart LR
  SEQ["Two sequences"] --> DP["DP scoring matrix"]
  DP --> NW["Needleman-Wunsch (global)"]
  DP --> SW["Smith-Waterman (local)"]
  NW --> ALN["Optimal alignment"]
  SW --> ALN
```

Affine gaps make total penalty grow linearly with gap length, but with a fixed
opening offset:

```plot
{"title": "Affine gap penalty vs gap length", "xLabel": "gap length g", "yLabel": "penalty w(g)", "xRange": [0, 10], "yRange": [0, 14], "grid": true, "functions": [{"expr": "4+1*x", "label": "o + e*g", "color": "#dc2626"}]}
```

**Next:** detecting how a genome differs from the reference.
""",
        ),
        _t(
            "Variant calling and filtering",
            "12 min",
            r"""
# Variant calling and filtering

**Variant calling** identifies where a sample differs from the reference:
**SNPs** (single-base substitutions), small **indels**, and larger **structural
variants**. From an aligned BAM, callers build a per-base **pileup** and apply a
**probabilistic genotype model**. The **GATK HaplotypeCaller** locally
reassembles reads into candidate haplotypes and computes genotype likelihoods;
**bcftools** and **DeepVariant** are widely used alternatives. Results are stored
in **VCF** with **QUAL**, **DP** (depth) and genotype fields.

Raw calls contain false positives from mapping errors and strand bias, so they
are **filtered**. Approaches include hard thresholds on depth, quality and
**strand-odds-ratio**, and GATK's **VQSR**, which models true vs artifactual
variants. The genotype posterior follows from Bayes: $P(G\mid D) \propto P(D\mid
G)\,P(G)$, combining the read likelihood with a prior.

```mermaid
flowchart LR
  BAM["Aligned BAM"] --> PILEUP["Pileup / local reassembly"]
  PILEUP --> LIK["Genotype likelihoods"]
  LIK --> VCF["VCF variant calls"]
  VCF --> FILTER["Filtering (VQSR / hard)"]
  FILTER --> HQ["High-confidence variants"]
```

Variant-calling sensitivity rises with depth and saturates — diminishing returns
past ~30x for SNPs:

```plot
{"title": "Variant detection sensitivity vs depth", "xLabel": "sequencing depth (x)", "yLabel": "sensitivity", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.5*x)", "label": "sensitivity", "color": "#2563eb"}]}
```

**Next:** linking variants to traits with GWAS.
""",
        ),
        _t(
            "Genome-wide association studies",
            "12 min",
            r"""
# Genome-wide association studies

A **genome-wide association study (GWAS)** tests millions of common variants for
statistical association with a trait or disease across many individuals. For each
**SNP**, a regression — linear for quantitative traits, logistic for case/control
— estimates an **effect size** (a **beta** or **odds ratio**) and a p-value,
while adjusting for **covariates** and **population structure** (via principal
components or mixed models) to avoid spurious associations.

Because so many tests run, the **multiple-testing** burden is severe. The
**genome-wide significance** threshold is conventionally $p < 5 \times 10^{-8}$
(Bonferroni for ~1 million independent tests). Results are visualized in a
**Manhattan plot** ($-\log_{10} p$ along the genome) and checked for inflation
with a **QQ plot**. Associated SNPs usually tag a region via **linkage
disequilibrium** rather than being causal themselves.

```mermaid
flowchart LR
  GENO["Genotypes (SNP array / WGS)"] --> QC["QC + imputation"]
  PHENO["Phenotype + covariates"] --> ASSOC["Per-SNP regression"]
  QC --> ASSOC
  ASSOC --> MANH["Manhattan / QQ plots"]
  MANH --> HITS["Significant loci"]
```

On a Manhattan plot, a true locus appears as a peak rising above the genome-wide
threshold line:

```plot
{"title": "Association peak at a trait locus (Manhattan view)", "xLabel": "genomic position (relative)", "yLabel": "-log10 p", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "10*exp(-((x-5)^2)/0.5)", "label": "-log10 p", "color": "#dc2626"}]}
```

**Next:** test what you learned.
""",
        ),
        _quiz(),
    ),
)


# -- Genomics -- Advanced -----------------------------------------------------

_ADVANCED = SeedCourse(
    slug="genomics-advanced",
    title="Genomics — Advanced",
    description=(
        "State-of-the-art and applied genomics: comparative and evolutionary "
        "genomics, functional genomics with RNA-seq and ATAC-seq, single-cell "
        "and spatial methods, pangenomes and graph references, clinical "
        "genomics, and deep-learning models that predict function from "
        "sequence. Quantitative, current and tool-grounded."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Comparative and evolutionary genomics",
            "12 min",
            r"""
# Comparative and evolutionary genomics

**Comparative genomics** aligns genomes across species to find what is conserved
(and therefore functional) and what has changed. **Orthologs** (genes separated
by speciation) and **paralogs** (separated by duplication) are distinguished by
phylogeny; tools like **OrthoFinder** infer orthogroups. **Whole-genome
alignment** (e.g. **Cactus**, **LASTZ**) reveals **synteny** — conserved gene
order — and rearrangements such as inversions and translocations.

Selection is read from substitution patterns in coding DNA. The ratio of
non-synonymous to synonymous changes, **dN/dS** (omega), classifies pressure:
$\omega < 1$ purifying (constraint), $\omega = 1$ neutral, $\omega > 1$ positive
selection. **Phylogenetic models** (**PAML**, **HyPhy**) estimate omega per
branch or per site to localize adaptive evolution.

```mermaid
flowchart LR
  GENOMES["Multiple genomes"] --> WGA["Whole-genome alignment"]
  WGA --> SYNTENY["Synteny / rearrangements"]
  GENOMES --> ORTHO["Orthology inference"]
  ORTHO --> DNDS["dN/dS selection test"]
  DNDS --> SEL["Constraint vs adaptation"]
```

Conserved sites accumulate fewer substitutions over evolutionary time than
neutral sites — the basis of conservation scores like phyloP:

```plot
{"title": "Substitutions accumulate slower under constraint", "xLabel": "divergence time (relative)", "yLabel": "substitutions per site", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.5*(1-exp(-0.2*x))", "label": "constrained site", "color": "#2563eb"}]}
```

**Next:** measuring genome activity with functional genomics.
""",
        ),
        _t(
            "Functional genomics: RNA-seq and ATAC-seq",
            "12 min",
            r"""
# Functional genomics: RNA-seq and ATAC-seq

**Functional genomics** measures what the genome does. **RNA-seq** quantifies
transcription: reads are aligned (**STAR**, **HISAT2**) or pseudo-aligned
(**Salmon**, **kallisto**), counted per gene, and tested for **differential
expression** with negative-binomial models in **DESeq2** or **edgeR**. The
negative binomial captures **overdispersion** — biological variance exceeding a
Poisson model — and shrinkage stabilizes estimates at low counts.

**ATAC-seq** maps **open chromatin**: a hyperactive **Tn5 transposase** inserts
adapters only into accessible DNA, marking active promoters and enhancers.
**ChIP-seq** and **CUT&RUN** locate protein-DNA binding and histone marks. Peaks
are called with **MACS2**. Together these layers reconstruct the regulatory state
of a cell.

```mermaid
flowchart LR
  RNA["RNA-seq"] --> EXPR["Gene expression"]
  ATAC["ATAC-seq"] --> OPEN["Open chromatin"]
  CHIP["ChIP-seq"] --> BIND["TF / histone binding"]
  EXPR --> REG["Regulatory model of the cell"]
  OPEN --> REG
  BIND --> REG
```

RNA-seq counts are overdispersed: variance grows faster than the mean (negative
binomial, $\sigma^2 = \mu + \alpha\mu^2$), unlike the Poisson line:

```plot
{"title": "Negative-binomial variance exceeds Poisson (mean-variance)", "xLabel": "mean count mu", "yLabel": "variance", "xRange": [0, 10], "yRange": [0, 30], "grid": true, "functions": [{"expr": "x+0.2*x^2", "label": "negative binomial", "color": "#dc2626"}, {"expr": "x", "label": "Poisson", "color": "#2563eb"}]}
```

**Next:** resolving genomics one cell at a time.
""",
        ),
        _t(
            "Single-cell and spatial genomics",
            "12 min",
            r"""
# Single-cell and spatial genomics

Bulk assays average over millions of cells, hiding heterogeneity. **Single-cell
RNA-seq (scRNA-seq)** profiles each cell separately by tagging transcripts with a
**cell barcode** and a **unique molecular identifier (UMI)** that removes PCR
duplicates. Platforms like **10x Chromium** capture thousands of cells in
droplets. The data is a sparse cell-by-gene matrix analyzed in **Scanpy** or
**Seurat**.

The workflow normalizes counts, selects highly variable genes, reduces dimension
(**PCA -> UMAP**), and **clusters** cells into types; **trajectory inference**
orders cells along differentiation. **Spatial transcriptomics** (Visium, MERFISH)
adds back physical coordinates, mapping expression to tissue architecture.
**Multi-omics** (e.g. scRNA + scATAC) profiles several layers per cell.

```mermaid
flowchart LR
  CELLS["Single cells (barcode + UMI)"] --> MATRIX["Cell x gene matrix"]
  MATRIX --> NORM["Normalize + HVG"]
  NORM --> DR["PCA -> UMAP"]
  DR --> CLUST["Cluster -> cell types"]
  CLUST --> TRAJ["Trajectory inference"]
```

scRNA-seq matrices are extremely **sparse**: the fraction of nonzero entries
("dropout") drops as cell numbers and gene sparsity grow:

```plot
{"title": "Single-cell matrices are sparse (schematic)", "xLabel": "genes profiled (relative)", "yLabel": "fraction nonzero entries", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "fraction detected", "color": "#16a34a"}]}
```

**Next:** moving beyond a single linear reference genome.
""",
        ),
        _t(
            "Pangenomes and graph references",
            "11 min",
            r"""
# Pangenomes and graph references

A single **linear reference** (like GRCh38) carries one allele at each locus and
suffers **reference bias**: reads matching non-reference alleles map worse,
distorting variant calls. A **pangenome** represents many genomes together. The
**core genome** is shared by all individuals; the **accessory/dispensable
genome** is present in only some — a distinction first formalized in bacteria.

**Graph genomes** encode variation as a **sequence graph**: nodes are sequence
segments, and alternative alleles appear as parallel paths (bubbles). Tools like
**vg** and the **Human Pangenome Reference Consortium** (HPRC) build and align to
these graphs, reducing reference bias and capturing **structural variants** and
diverse haplotypes that a linear reference cannot.

```mermaid
flowchart LR
  GENOMES["Many genomes"] --> GRAPH["Sequence graph (nodes + paths)"]
  GRAPH --> CORE["Core genome (shared)"]
  GRAPH --> ACC["Accessory genome (variable)"]
  GRAPH --> ALIGN["Graph alignment (vg)"]
  ALIGN --> NOBIAS["Reduced reference bias"]
```

As more genomes are added, the **pangenome** (union of genes) keeps growing while
the **core genome** (shared by all) shrinks toward a plateau:

```plot
{"title": "Pangenome grows as genomes are added (open pangenome)", "xLabel": "number of genomes", "yLabel": "gene families (relative)", "xRange": [1, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.4*x)", "label": "pangenome size", "color": "#2563eb"}, {"expr": "exp(-0.4*x)", "label": "core fraction", "color": "#16a34a"}]}
```

**Next:** turning genomes into clinical decisions.
""",
        ),
        _t(
            "Clinical genomics",
            "12 min",
            r"""
# Clinical genomics

**Clinical genomics** applies sequencing to diagnosis and treatment. **Whole-
exome (WES)** and **whole-genome sequencing (WGS)** diagnose rare Mendelian
disease by finding the causal variant among millions. Candidate variants are
**annotated** (**VEP**, **ANNOVAR**) for predicted effect, population frequency
(**gnomAD**) and disease databases (**ClinVar**), then classified by **ACMG/AMP**
criteria into **pathogenic, likely pathogenic, VUS, likely benign, benign**.

In oncology, **somatic** variant calling compares tumor to matched normal to find
driver mutations and inform **targeted therapy**; **tumor mutational burden** and
signatures guide immunotherapy. **Pharmacogenomics** uses germline variants
(e.g. *CYP2D6*) to dose drugs. **Liquid biopsy** detects circulating tumor DNA
for non-invasive monitoring. Throughout, **clinical-grade** pipelines demand
validated accuracy, reproducibility and reporting standards.

```mermaid
flowchart LR
  SAMPLE["Patient sample"] --> SEQ["WES / WGS"]
  SEQ --> VAR["Variant calling"]
  VAR --> ANNOT["Annotation: gnomAD, ClinVar, VEP"]
  ANNOT --> ACMG["ACMG classification"]
  ACMG --> REPORT["Clinical report"]
```

The **prior probability** a rare variant is causal climbs sharply as its
population frequency drops — rarity is strong evidence under ACMG:

```plot
{"title": "Variant rarity raises pathogenicity prior (schematic)", "xLabel": "-log10 population frequency", "yLabel": "relative pathogenicity prior", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-4)))", "label": "prior", "color": "#dc2626"}]}
```

**Next:** deep learning that predicts function from sequence.
""",
        ),
        _t(
            "Deep learning in genomics",
            "12 min",
            r"""
# Deep learning in genomics

Deep learning now reads the genome's "grammar" directly from sequence.
Convolutional models like **DeepSEA** and **Basset** predict chromatin
accessibility and transcription-factor binding from raw DNA. **Enformer**, a
transformer with a wide receptive field (~100 kb), predicts gene expression and
captures long-range enhancer-promoter effects. These models learn motifs as
filters and can score the **functional impact** of any variant *in silico*.

**AlphaFold** transformed structural genomics by predicting protein 3D structure
from sequence at near-experimental accuracy, enabling proteome-wide structure
prediction. For variant interpretation, **AlphaMissense** scores missense
pathogenicity, and **splicing** models (**SpliceAI**) flag variants that disrupt
splice sites. Generative and language-model approaches (e.g. **DNA/protein
language models** trained self-supervised on vast sequence corpora) increasingly
provide embeddings for downstream prediction.

```mermaid
flowchart LR
  SEQ["DNA / protein sequence"] --> CNN["CNN motif layers"]
  CNN --> TRANS["Transformer (long-range)"]
  TRANS --> PRED["Predict: expression, binding, structure"]
  PRED --> VAR["In-silico variant effect"]
  VAR --> INTERP["Interpretation / prioritization"]
```

Model accuracy improves with training data but shows **diminishing returns** —
each doubling of data yields a smaller gain (a saturating learning curve):

```plot
{"title": "Deep model accuracy vs training data (saturating)", "xLabel": "training data (relative, log)", "yLabel": "predictive accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.5*x)", "label": "accuracy", "color": "#2563eb"}]}
```

**Next:** test what you learned.
""",
        ),
        _quiz(),
    ),
)


GENOMICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["GENOMICS_COURSES"]
