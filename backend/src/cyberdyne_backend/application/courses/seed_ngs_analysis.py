"""Next-Generation Sequencing Analysis track: Basics -> Intermediate -> Advanced.

A university-level NGS data-analysis curriculum: from sequencing chemistries,
read formats and quality control, through alignment, variant calling and the
core file formats (FASTQ/SAM/BAM/VCF), to structural variants, reproducible
pipelines, deep-learning callers and best practices. Lessons use interactive
```plot blocks for quantitative relationships (Phred error, coverage, GC bias,
allele balance) and ```mermaid diagrams for chemistries, pipelines and workflows.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- NGS Analysis -- Basics ---------------------------------------------------

_BASICS = SeedCourse(
    slug="ngs-analysis-basics",
    title="Next-Generation Sequencing Analysis — Basics",
    description=(
        "How modern sequencers turn DNA into data, and how to judge that data. "
        "Sequencing chemistries (Illumina, PacBio, Nanopore), the FASTQ format "
        "and Phred quality scores, read QC and trimming, coverage and depth, and "
        "the difference between short and long reads. Built on real molecular and "
        "computational detail with interactive plots and process diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "From DNA to reads: sequencing technologies",
            "11 min",
            r"""
# From DNA to reads: sequencing technologies

**Next-generation sequencing (NGS)** reads millions of DNA fragments in
parallel. The workflow is always the same shape: extract DNA, build a
**library** (fragment, then add platform-specific **adapters**), amplify or
load it, and sequence. What differs is the **chemistry**.

**Illumina** dominates short reads: fragments form clonal clusters by **bridge
amplification** on a flow cell, then **sequencing-by-synthesis** images one
**reversible-terminator** base per cycle (reads of ~100–300 bp, error
<0.1%, mostly substitutions). **PacBio HiFi** circularizes a fragment and reads
it many times (**circular consensus**), giving long (~15 kb), highly accurate
reads. **Oxford Nanopore** threads single strands through a protein pore and
measures the **ionic current**, giving very long reads (10 kb–1 Mb) at higher
but improving error rates, with no amplification.

```mermaid
flowchart LR
  DNA["Genomic DNA"] --> LIB["Library prep + adapters"]
  LIB --> ILL["Illumina: SBS, short reads"]
  LIB --> PB["PacBio HiFi: CCS, long+accurate"]
  LIB --> ONT["Nanopore: current signal, ultra-long"]
```

Read length trades off against per-base accuracy and cost; platform choice
follows the biological question:

```plot
{"title": "Read length vs platform (illustrative)", "xLabel": "platform index", "yLabel": "log10 read length (bp)", "xRange": [0, 6], "yRange": [2, 6], "grid": true, "functions": [{"expr": "2+0.6*x", "label": "log10 read length", "color": "#2563eb"}]}
```

**Next:** the FASTQ format and Phred quality scores.
""",
        ),
        _t(
            "FASTQ and Phred quality scores",
            "11 min",
            r"""
# FASTQ and Phred quality scores

A sequencer emits reads as **FASTQ**: four lines per read — an `@`-prefixed
**identifier**, the **sequence**, a `+` separator, and a **quality** string of
the same length. Each quality character encodes a **Phred score** $Q$ via
ASCII offset 33 (Phred+33): the character value minus 33 gives $Q$.

The Phred score links to the probability $P$ that the base call is wrong:

$$Q = -10 \log_{10}(P) \qquad\Longleftrightarrow\qquad P = 10^{-Q/10}$$

So $Q20$ means a 1-in-100 error, $Q30$ means 1-in-1000, and $Q40$ means
1-in-10,000. Most analyses treat $Q\ge30$ as high confidence. Paired-end
sequencing produces two FASTQ files (R1, R2) whose reads share an identifier;
the **insert size** is the distance spanned by the pair.

```mermaid
flowchart TB
  L1["@read_id  (identifier)"] --> L2["ACGTACGTACGT  (sequence)"]
  L2 --> L3["+  (separator)"]
  L3 --> L4["IIIIFFFF####  (Phred+33 quality)"]
```

Error probability falls exponentially as $Q$ rises — a small Phred gain is a
large reliability gain:

```plot
{"title": "Phred score vs error probability", "xLabel": "Phred Q score", "yLabel": "error probability P", "xRange": [0, 40], "yRange": [0, 1], "grid": true, "functions": [{"expr": "10^(-x/10)", "label": "P = 10^(-Q/10)", "color": "#dc2626"}]}
```

**Next:** running QC on raw reads.
""",
        ),
        _t(
            "Read quality control",
            "11 min",
            r"""
# Read quality control

Before any analysis, you must **inspect read quality**. The standard tool is
**FastQC**, which summarizes a FASTQ file into per-module reports;
**MultiQC** aggregates many samples into one view. Key things to read:

- **Per-base quality** typically falls toward the 3' end of Illumina reads, as
  phasing and signal decay accumulate over cycles.
- **Per-base sequence content** should be roughly flat; a skew in the first few
  bases often reflects **adapter** or random-hexamer priming bias.
- **Overrepresented sequences / adapter content** flag library contamination.
- **Duplication level** hints at PCR over-amplification.
- **GC content** should match the expected organism; a second peak suggests
  contamination.

A failing module is a signal, not a verdict — RNA-seq, for instance,
legitimately shows non-flat sequence content at read starts.

```mermaid
flowchart LR
  FQ["Raw FASTQ"] --> FQC["FastQC per-sample"]
  FQC --> MQC["MultiQC aggregate"]
  MQC --> DEC{"QC pass?"}
  DEC -->|yes| DOWN["Proceed"]
  DEC -->|no| TRIM["Trim / re-prep"]
```

Mean per-base quality usually declines along the read, motivating 3'
trimming:

```plot
{"title": "Per-base quality decays along an Illumina read", "xLabel": "cycle (base position)", "yLabel": "mean Phred Q", "xRange": [0, 10], "yRange": [20, 40], "grid": true, "functions": [{"expr": "38-1.4*x", "label": "mean Q", "color": "#2563eb"}]}
```

**Next:** trimming adapters and low-quality bases.
""",
        ),
        _t(
            "Trimming and filtering reads",
            "10 min",
            r"""
# Trimming and filtering reads

QC findings drive **read processing**. Tools such as **Trimmomatic**,
**cutadapt** and **fastp** perform three jobs: remove **adapter** sequence,
trim **low-quality** bases (often from the 3' end), and **discard** reads that
become too short or too poor. fastp is popular because it also does adapter
auto-detection and emits its own QC report in one pass.

A common quality-trim rule uses a **sliding window**: scan a window (e.g. 4 bp)
and cut once its mean Phred falls below a threshold (e.g. Q20). For paired-end
data, keep R1 and R2 **synchronized** — if one mate is dropped, its partner
becomes an unpaired "orphan." Over-trimming is a real risk: aggressive cuts
shorten reads, hurt mappability, and can bias coverage, so trim only as much as
the QC report justifies.

```mermaid
flowchart LR
  RAW["Raw reads"] --> AD["Remove adapters"]
  AD --> QT["Quality trim (sliding window)"]
  QT --> LEN["Drop too-short reads"]
  LEN --> CLEAN["Cleaned, paired reads"]
```

There is a sweet spot: as you raise the quality threshold, mean retained
quality rises but the fraction of bases kept falls — yield and quality trade
off:

```plot
{"title": "Fraction of bases retained vs trim stringency", "xLabel": "quality threshold Q", "yLabel": "fraction of bases kept", "xRange": [0, 40], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(x/28)^6)", "label": "bases kept", "color": "#16a34a"}]}
```

**Next:** coverage and sequencing depth.
""",
        ),
        _t(
            "Coverage and sequencing depth",
            "11 min",
            r"""
# Coverage and sequencing depth

**Coverage** (or **depth**) at a position is the number of reads overlapping
it. The expected genome-wide depth follows **Lander–Waterman**:

$$C = \frac{N \cdot L}{G}$$

where $N$ is the number of reads, $L$ the read length, and $G$ the genome size.
For human WGS, $30\times$ is a common target; clinical WES often aims for
$100\times$ over the exome because capture is uneven. Higher depth lets random
errors be **outvoted** by consensus, raising variant-calling sensitivity —
especially for heterozygous and low-frequency variants.

Reads land roughly at random, so per-base depth is approximately **Poisson**
with mean $C$. The probability a base is **missed entirely** (zero reads) is
$e^{-C}$, which shrinks fast with depth — the basis for choosing a target.

```mermaid
flowchart LR
  READS["N reads of length L"] --> MAP["Map to genome (size G)"]
  MAP --> DEPTH["Per-base depth ~ Poisson(C)"]
  DEPTH --> CALL["Confidence in calls grows with C"]
```

The chance of leaving a base uncovered falls exponentially with mean depth:

```plot
{"title": "Probability a base is uncovered vs mean depth", "xLabel": "mean coverage C", "yLabel": "P(zero reads) = exp(-C)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-x)", "label": "P(uncovered)", "color": "#dc2626"}]}
```

**Next:** what short vs long reads are good for.
""",
        ),
        _t(
            "Short reads vs long reads",
            "10 min",
            r"""
# Short reads vs long reads

The single biggest analysis decision is **read length**. **Short reads**
(Illumina) are cheap, abundant and very accurate per base, making them ideal
for **SNV/indel calling**, gene-expression counting (RNA-seq) and any task that
maps confidently to a reference. Their weakness is **repeats and structural
variants**: a 150 bp read often cannot span a repeat, so its placement is
ambiguous and large rearrangements are hard to reconstruct.

**Long reads** (PacBio HiFi, Nanopore) span repeats, resolve **structural
variants**, phase **haplotypes**, enable near-complete **de novo assembly**,
and — with Nanopore — read **base modifications** (e.g. 5mC methylation)
directly. The trade-offs are higher per-base error (shrinking with HiFi and
newer chemistries) and higher cost per gigabase. Many modern projects are
**hybrid**: long reads for the scaffold and SVs, short reads to polish base
accuracy.

```mermaid
flowchart TB
  Q{"Analysis goal?"} --> SNV["SNVs, expression, depth"]
  Q --> SV["SVs, repeats, phasing, assembly"]
  SNV --> SHORT["Short reads (Illumina)"]
  SV --> LONG["Long reads (PacBio / Nanopore)"]
  LONG --> HYB["Hybrid: long + short polish"]
```

As reads lengthen, the fraction of repeats they can fully span rises toward 1:

```plot
{"title": "Fraction of repeats spanned vs read length", "xLabel": "read length (kb)", "yLabel": "fraction of repeats spanned", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "repeats spanned", "color": "#16a34a"}]}
```

**Next:** test your grasp of the NGS basics.
""",
        ),
        _quiz(),
    ),
)


# -- NGS Analysis -- Intermediate ---------------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="ngs-analysis-intermediate",
    title="Next-Generation Sequencing Analysis — Intermediate",
    description=(
        "The quantitative core of resequencing analysis. Read alignment and the "
        "SAM/BAM format, the alignment-cleanup steps before calling, probabilistic "
        "variant calling and genotype likelihoods, the VCF format and variant "
        "filtering, plus annotation. Real tools (BWA-MEM, minimap2, samtools, "
        "GATK, bcftools) with interactive plots and pipeline diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Read alignment and the SAM/BAM format",
            "12 min",
            r"""
# Read alignment and the SAM/BAM format

**Resequencing** maps reads back to a **reference genome**. Short-read
aligners (**BWA-MEM**, **Bowtie2**) index the reference with a
**Burrows–Wheeler Transform / FM-index** to find exact-match **seeds** in
$O(\text{read length})$ time, then extend them with banded
**Smith–Waterman**. Long-read aligners (**minimap2**) use **minimizer**
seeding and chaining to tolerate higher error and large indels.

Output is **SAM** (text) or its compressed binary form **BAM**. Each line is one
alignment with 11 mandatory fields: read name, **FLAG** (bitwise: paired,
mapped, reverse-strand, duplicate…), reference name, **POS**, **MAPQ** (mapping
confidence, Phred-scaled), **CIGAR** (e.g. `100M`, `5S95M`, `50M2D48M`
encoding match/insert/delete/clip), mate fields, and the **SEQ**/**QUAL**.
`samtools sort` and `index` produce a coordinate-sorted, randomly accessible
BAM.

```mermaid
flowchart LR
  FQ["Cleaned FASTQ"] --> ALN["BWA-MEM / minimap2"]
  ALN --> SAM["SAM (text)"]
  SAM --> SORT["samtools sort"]
  SORT --> BAM["Indexed BAM"]
```

**MAPQ** is Phred-scaled like base quality — the probability the read is
mis-placed falls exponentially as MAPQ rises:

```plot
{"title": "Mapping confidence: P(wrong placement) vs MAPQ", "xLabel": "MAPQ", "yLabel": "P(misplaced)", "xRange": [0, 40], "yRange": [0, 1], "grid": true, "functions": [{"expr": "10^(-x/10)", "label": "P = 10^(-MAPQ/10)", "color": "#dc2626"}]}
```

**Next:** cleaning up alignments before variant calling.
""",
        ),
        _t(
            "Alignment cleanup: duplicates and recalibration",
            "11 min",
            r"""
# Alignment cleanup: duplicates and recalibration

A raw BAM is not ready for calling. The **GATK Best Practices** pre-processing
removes two systematic biases.

**Duplicate marking** (`MarkDuplicates`, Picard/GATK) flags reads that share
the same fragment start/end as **PCR or optical duplicates**. They are not
independent evidence, so they would falsely inflate confidence in whatever base
they carry; they are marked (FLAG bit set), not deleted, and excluded from
calling.

**Base Quality Score Recalibration (BQSR)** corrects the sequencer's reported
Phred scores, which are often miscalibrated and context-dependent. GATK builds
an empirical model from mismatches at non-variant sites (using a known-variant
mask such as dbSNP) keyed on cycle, sequence context and original quality, then
adjusts each base's $Q$ toward its true error rate. The goal is **calibration**:
bases reported at $Q30$ should actually err 1 in 1000.

```mermaid
flowchart LR
  BAM["Sorted BAM"] --> DUP["MarkDuplicates"]
  DUP --> BQSR["BQSR (model from known sites)"]
  BQSR --> READY["Analysis-ready BAM"]
```

A well-calibrated caller's reported quality matches its observed error rate —
the recalibration target is the diagonal:

```plot
{"title": "Calibration: reported vs empirical quality", "xLabel": "reported Q", "yLabel": "empirical Q", "xRange": [0, 40], "yRange": [0, 40], "grid": true, "functions": [{"expr": "x", "label": "perfect calibration", "color": "#16a34a"}]}
```

**Next:** how variants are actually called.
""",
        ),
        _t(
            "Variant calling and genotype likelihoods",
            "12 min",
            r"""
# Variant calling and genotype likelihoods

Calling asks, at each site: which **genotype** best explains the pile of read
bases and their qualities? Callers compute a **genotype likelihood**
$P(\text{reads}\mid G)$ for each candidate $G$ (homozygous reference `0/0`,
heterozygous `0/1`, homozygous alternate `1/1`) by treating each base as an
independent Bernoulli trial whose error probability comes from its Phred score.
Bayes' rule then combines this with a **prior** to give a posterior; the call's
confidence is the Phred-scaled **QUAL**.

For SNVs and short indels, **GATK HaplotypeCaller** and **DeepVariant** go
further: they **locally reassemble** each active region into candidate
haplotypes and realign reads to them, which fixes alignment artifacts around
indels. **bcftools call** offers a faster pileup model. For a heterozygous site
at depth $C$, the expected **allele balance** is ~0.5; large deviations flag
errors or copy-number effects.

```mermaid
flowchart LR
  BAM["Analysis-ready BAM"] --> AR["Find active regions"]
  AR --> HAP["Local reassembly -> haplotypes"]
  HAP --> GL["Genotype likelihoods P(reads|G)"]
  GL --> CALL["Call + QUAL"]
```

At a true heterozygous site the alt-allele fraction concentrates near 0.5; the
spread narrows as depth grows (illustrative density):

```plot
{"title": "Allele-balance density at a het site", "xLabel": "alt fraction x10 (0..10 = 0.0..1.0)", "yLabel": "relative density", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-((x-5)^2)/2)", "label": "het ~ 0.5", "color": "#2563eb"}]}
```

**Next:** the VCF format that stores variants.
""",
        ),
        _t(
            "The VCF format",
            "11 min",
            r"""
# The VCF format

Variants are stored in **VCF (Variant Call Format)**: a header of `##` meta
lines defining INFO/FORMAT fields, then one record per variant site. The eight
fixed columns are **CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO**, followed by
a **FORMAT** column and one column per **sample**.

Read a record like a sentence: at `CHROM:POS`, the reference allele `REF` may be
replaced by `ALT`, called with confidence `QUAL`, passing or failing `FILTER`.
The **INFO** field carries site-level annotations (e.g. `DP` total depth, `AF`
allele frequency, `MQ` mapping quality). The per-sample fields follow FORMAT
keys: **GT** (genotype, `0/1`), **DP** (depth), **AD** (allelic depths), **GQ**
(genotype quality), **PL** (Phred-scaled likelihoods). Compress with `bgzip` and
index with `tabix` for random access; **gVCF** additionally records confidence
in **non-variant** blocks, enabling joint genotyping across cohorts.

```mermaid
flowchart LR
  HDR["##header (INFO/FORMAT defs)"] --> REC["Variant records"]
  REC --> FIX["CHROM POS ID REF ALT QUAL FILTER INFO"]
  REC --> SAMP["FORMAT + per-sample GT:DP:AD:GQ:PL"]
```

GT-likelihood (PL) values are Phred-scaled relative to the best genotype, so the
non-best genotypes become exponentially less probable:

```plot
{"title": "Relative genotype probability vs PL", "xLabel": "PL (Phred-scaled)", "yLabel": "relative probability", "xRange": [0, 40], "yRange": [0, 1], "grid": true, "functions": [{"expr": "10^(-x/10)", "label": "10^(-PL/10)", "color": "#dc2626"}]}
```

**Next:** filtering raw calls down to trustworthy ones.
""",
        ),
        _t(
            "Variant filtering",
            "11 min",
            r"""
# Variant filtering

Raw call sets contain many false positives; **filtering** marks or removes them.
Two strategies dominate.

**Hard filtering** applies fixed thresholds on INFO annotations — e.g. for SNVs
GATK suggests `QD < 2.0`, `FS > 60.0`, `MQ < 40.0`, `MQRankSum < -12.5`,
`ReadPosRankSum < -8.0`. It is simple and works for small cohorts, but the
cutoffs are blunt. **Variant Quality Score Recalibration (VQSR)** instead fits a
**Gaussian mixture model** to the annotation cloud of **known true** variants,
then assigns each call a **VQSLOD** (log-odds of being real) and sets a
sensitivity tranche (e.g. keep 99.5% of known true sites). Modern callers like
DeepVariant fold much of this into the model itself.

A good filter maximizes the area under the **precision–recall** curve: it should
keep recall high while precision stays near 1. Note that FILTER `PASS` is the
keep flag; anything else names the filter that failed.

```mermaid
flowchart LR
  RAW["Raw VCF"] --> CHOICE{"Cohort size?"}
  CHOICE -->|small| HARD["Hard filters (QD, FS, MQ...)"]
  CHOICE -->|large| VQSR["VQSR / ML (VQSLOD)"]
  HARD --> PASS["Filtered VCF (PASS)"]
  VQSR --> PASS
```

Filtering trades precision against recall; a good filter holds precision high
until recall is pushed near its limit:

```plot
{"title": "Precision-recall trade-off in variant filtering", "xLabel": "recall x10 (0..10 = 0..1)", "yLabel": "precision", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(x/8)^8)", "label": "precision", "color": "#16a34a"}]}
```

**Next:** annotating variants with biological meaning.
""",
        ),
        _t(
            "Variant annotation",
            "10 min",
            r"""
# Variant annotation

A PASS variant is still just a coordinate change; **annotation** attaches
biological and clinical meaning. Tools like **VEP (Ensembl)**, **SnpEff** and
**ANNOVAR** intersect each variant with gene models and databases to predict its
**consequence**: synonymous, missense, nonsense (stop-gained), frameshift,
splice-site, or non-coding/regulatory. They also pull **population frequency**
(gnomAD), **clinical significance** (ClinVar), and **deleteriousness scores**
(SIFT, PolyPhen-2, CADD, REVEL).

Annotation enables **prioritization**: a rare (low gnomAD AF), protein-truncating
variant in a disease gene with a high CADD score deserves attention; a common
synonymous change usually does not. For clinical reporting, variants are graded
against **ACMG/AMP** criteria into five tiers (benign to pathogenic). Garbage in,
garbage out: annotation only matters if the upstream calls and filters are sound.

```mermaid
flowchart LR
  VCF["Filtered VCF"] --> CONS["Consequence (VEP/SnpEff)"]
  VCF --> FREQ["Population AF (gnomAD)"]
  VCF --> CLIN["ClinVar / CADD / REVEL"]
  CONS --> PRIO["Prioritize candidates"]
  FREQ --> PRIO
  CLIN --> PRIO
```

Predicted deleteriousness scores (e.g. CADD-like) rise sigmoidally with
functional impact, separating likely-benign from likely-damaging variants:

```plot
{"title": "Deleteriousness score vs functional impact", "xLabel": "predicted impact", "yLabel": "scaled score", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "deleteriousness", "color": "#2563eb"}]}
```

**Next:** test your grasp of alignment, calling and VCF.
""",
        ),
        _quiz(),
    ),
)


# -- NGS Analysis -- Advanced -------------------------------------------------

_ADVANCED = SeedCourse(
    slug="ngs-analysis-advanced",
    title="Next-Generation Sequencing Analysis — Advanced",
    description=(
        "State-of-the-art and applied NGS analysis. Structural-variant and "
        "copy-number detection, somatic calling and tumor purity, deep-learning "
        "callers (DeepVariant) and pangenome graph references, reproducible "
        "workflows (Nextflow/Snakemake, nf-core), and benchmarking against truth "
        "sets. Modern tools and methods with interactive plots and diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Structural variants and copy number",
            "12 min",
            r"""
# Structural variants and copy number

**Structural variants (SVs)** are large (≥50 bp) genome changes — deletions,
duplications, insertions, inversions and translocations — plus **copy-number
variants (CNVs)** that change dosage. They drive much disease and evolution but
are the hardest class to call from short reads, because a 150 bp read rarely
spans a breakpoint.

Short-read callers (**Manta**, **DELLY**, **GRIDSS**, **Lumpy**) triangulate
**three signals**: **discordant read pairs** (mates mapping too far apart or in
the wrong orientation), **split reads** (one read straddling a breakpoint, seen
as a clipped CIGAR), and **read-depth** changes (a deletion halves depth, a
duplication raises it). **CNV** callers add **read-depth binning** and
segmentation. Long reads transform SV calling: a single read can span an entire
event, so **Sniffles** and **cuteSV** on PacBio/Nanopore achieve far higher
sensitivity and precise breakpoints.

```mermaid
flowchart LR
  BAM["Aligned reads"] --> DISC["Discordant pairs"]
  BAM --> SPLIT["Split reads"]
  BAM --> DEPTH["Read-depth change"]
  DISC --> SV["SV / CNV call"]
  SPLIT --> SV
  DEPTH --> SV
```

Copy number maps to normalized read depth: a heterozygous deletion drops depth
to ~0.5x, a duplication raises it to ~1.5x of the diploid baseline:

```plot
{"title": "Normalized read depth vs copy number", "xLabel": "copy number", "yLabel": "normalized depth", "xRange": [0, 4], "yRange": [0, 2], "grid": true, "functions": [{"expr": "x/2", "label": "depth ~ CN/2", "color": "#2563eb"}]}
```

**Next:** somatic variants and tumor analysis.
""",
        ),
        _t(
            "Somatic variant calling and tumor purity",
            "12 min",
            r"""
# Somatic variant calling and tumor purity

**Somatic** mutations arise in tissue (notably tumors) and are absent from the
germline, so they are called by **subtracting** a matched **normal**.
**Mutect2 (GATK)**, **Strelka2** and **VarScan2** contrast tumor and normal
pileups to find variants present only in the tumor, then filter sequencing
artifacts with **panels of normals** and read-orientation models (e.g. FFPE
oxidation).

The central difficulty is the **variant allele fraction (VAF)**. A germline het
sits near 0.5, but a somatic VAF reflects **tumor purity** $\rho$, **copy
number**, and **clonality**: a heterozygous mutation in a diploid clonal region
shows $\text{VAF}=\rho/2$. **Subclonal** mutations and low-purity samples push
VAF toward the noise floor, so somatic calling demands **higher depth** (often
$\ge200\times$, or thousands of $\times$ for liquid-biopsy ctDNA with UMIs to
suppress error). VAF distributions also reveal **clonal architecture** and
mutational **signatures** (e.g. SBS context spectra).

```mermaid
flowchart LR
  T["Tumor BAM"] --> M["Mutect2 / Strelka2"]
  N["Matched normal BAM"] --> M
  PON["Panel of normals"] --> M
  M --> FILT["Filter artifacts"]
  FILT --> SOM["Somatic VCF + VAF"]
```

Detectable VAF scales with tumor purity for a clonal diploid het mutation;
sensitivity falls as purity drops:

```plot
{"title": "Somatic VAF vs tumor purity (clonal diploid het)", "xLabel": "tumor purity (x10 = 0..1)", "yLabel": "expected VAF", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/20", "label": "VAF = purity/2", "color": "#dc2626"}]}
```

**Next:** deep-learning callers and pangenome references.
""",
        ),
        _t(
            "Deep learning and pangenome references",
            "12 min",
            r"""
# Deep learning and pangenome references

Two advances reshaped accuracy. **DeepVariant** (Google) reframes variant
calling as **image classification**: it renders the read pileup at each
candidate site as a multi-channel tensor (base, base quality, mapping quality,
strand, support) and a **convolutional neural network** classifies the genotype
(`0/0`, `0/1`, `1/1`). Trained on truth sets, it learns platform error patterns
implicitly and tops short- and long-read benchmarks; **PEPPER-Margin-DeepVariant**
extends this to Nanopore.

The second is the **pangenome graph reference**. A single linear reference
(GRCh38) carries **reference bias**: reads bearing non-reference alleles map
worse, hurting calls in diverse or highly variable regions. A **graph genome**
(the **Human Pangenome Reference Consortium**'s draft, tools **vg giraffe**,
**minigraph-cactus**) encodes many haplotypes as nodes and edges, so reads align
to the closest path. This reduces reference bias and improves variant recall,
especially for indels and the MHC.

```mermaid
flowchart LR
  PILE["Pileup at site"] --> IMG["Render to tensor"]
  IMG --> CNN["CNN genotype classifier"]
  CNN --> GT["0/0 | 0/1 | 1/1"]
  REFG["Pangenome graph"] --> GIR["vg giraffe align"]
  GIR --> CALL["Reduced reference bias"]
```

Adding haplotypes to the graph reference cuts reference bias, with diminishing
returns as the panel saturates the common variation:

```plot
{"title": "Reference-bias reduction vs haplotypes in graph", "xLabel": "haplotypes added", "yLabel": "fraction of bias removed", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "bias removed", "color": "#16a34a"}]}
```

**Next:** building reproducible pipelines.
""",
        ),
        _t(
            "Reproducible NGS pipelines",
            "11 min",
            r"""
# Reproducible NGS pipelines

Real analyses chain dozens of steps over many samples; doing this by hand is
unreproducible. **Workflow managers** — **Nextflow** and **Snakemake** — express
the pipeline as a **directed acyclic graph (DAG)** of tasks with declared
inputs/outputs, so the engine resolves dependencies, runs independent steps in
**parallel**, resumes from cached results after failure, and scales the same
code from a laptop to HPC/SLURM and cloud.

**Reproducibility** rests on three pillars: **containers** (Docker/Singularity)
or **conda** to pin every tool version; **version control** of the workflow code;
and **parameter/config** capture so a run is fully described. The
**nf-core** project provides community-curated, peer-reviewed Nextflow pipelines
(`nf-core/sarek` for germline+somatic, `nf-core/rnaseq`) that bake in best
practices and testing. The payoff is determinism: the same inputs and container
hashes yield the same VCF.

```mermaid
flowchart LR
  CFG["Pinned config + containers"] --> WF["Nextflow / Snakemake DAG"]
  WF --> QC["QC + trim"]
  QC --> ALN["Align"]
  ALN --> CALL["Call + filter"]
  CALL --> OUT["Versioned outputs + reports"]
```

Wall-clock time falls with parallel workers but plateaus (Amdahl's law) once the
serial fraction dominates:

```plot
{"title": "Pipeline runtime vs parallel workers (Amdahl)", "xLabel": "workers", "yLabel": "relative runtime", "xRange": [1, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.2+0.8/x", "label": "runtime", "color": "#dc2626"}]}
```

**Next:** benchmarking against truth sets.
""",
        ),
        _t(
            "Benchmarking and best practices",
            "11 min",
            r"""
# Benchmarking and best practices

You cannot trust a caller you have not **benchmarked**. The community standard is
the **Genome in a Bottle (GIAB)** reference samples (e.g. **HG002**), which ship
a **high-confidence truth VCF** plus **confident-region BED**. Compare your calls
to truth **inside** the confident regions with **hap.py / vcfeval (RTG Tools)**,
which do **haplotype-aware** matching so equivalent representations of the same
indel are not counted as errors.

Report the standard metrics: **recall (sensitivity)** = TP/(TP+FN),
**precision** = TP/(TP+FP), and their harmonic mean the **F1 score**, broken out
**by variant type** (SNV vs indel) because indel performance is usually lower.
**Best practices** to internalize: stratify by region (homopolymers, low
mappability, segmental duplications) where errors concentrate; never tune
filters on the same sample you report on; track depth and contamination
(verifyBamID); and keep the whole pipeline versioned and containerized so a
result is auditable years later.

```mermaid
flowchart LR
  CALLS["Your VCF"] --> CMP["hap.py / vcfeval"]
  TRUTH["GIAB truth VCF + BED"] --> CMP
  CMP --> M["TP / FP / FN"]
  M --> F1["Recall, Precision, F1 by type"]
```

F1 is the harmonic mean of precision and recall, so it stays low unless **both**
are high — punishing a caller that trades one for the other:

```plot
{"title": "F1 vs recall at fixed precision = 0.9", "xLabel": "recall x10 (0..10 = 0..1)", "yLabel": "F1 score", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "2*0.9*(x/10)/(0.9+(x/10))", "label": "F1", "color": "#16a34a"}]}
```

**Next:** test your grasp of advanced NGS analysis.
""",
        ),
        _quiz(),
    ),
)


NGS_ANALYSIS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["NGS_ANALYSIS_COURSES"]
