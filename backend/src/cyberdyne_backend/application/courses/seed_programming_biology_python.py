"""Python Programming for Biologists track: Basics -> Intermediate -> Advanced.

From Python syntax, data types and control flow, through functions, files and
the NumPy/pandas stack, to Biopython, plotting and reproducible analysis
notebooks. Lessons are ``text`` with code, interactive ```plot blocks and
```mermaid pipeline diagrams.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Python Programming for Biologists -- Basics ------------------------------

_BASICS = SeedCourse(
    slug="programming-biology-python-basics",
    title="Python Programming for Biologists — Basics",
    description=(
        "Start from zero: why Python dominates modern biology, its core data "
        "types, strings as sequences, collections, and control flow. Concrete "
        "examples from molecular biology — counting nucleotides, computing GC "
        "content, transcribing DNA — so the syntax sticks because it solves a "
        "real problem."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why Python for biology",
            "9 min",
            r"""
# Why Python for biology

Modern biology is a data science. A single Illumina run yields hundreds of
gigabytes of reads; a flow-cytometry experiment, millions of cells; a screen,
thousands of dose-response curves. **Python** has become the lingua franca for
turning that data into knowledge because it is readable, free, and backed by a
mature scientific stack: **NumPy** and **pandas** for arrays and tables,
**Matplotlib** for figures, **Biopython** for sequences, **scikit-learn** for
modelling, and **Jupyter** for narrative notebooks.

```mermaid
flowchart LR
  A[Raw data: FASTQ, CSV, FASTA] --> B[Python script / notebook]
  B --> C[NumPy / pandas]
  C --> D[Statistics & models]
  D --> E[Matplotlib figures]
  E --> F[Reproducible report]
```

You write Python in two modes: an **interactive interpreter** (or Jupyter cell)
for exploration, and **scripts** (`.py` files) for pipelines you rerun. A first
program is one line:

```python
print("Hello, genome")
```

Python is **interpreted** and **dynamically typed**: you never declare types,
and indentation — not braces — defines blocks. That forces clean, uniform
layout, which matters when a wet-lab colleague has to read your analysis.

**Next:** the numeric and text types you will use every day.
""",
        ),
        _t(
            "Numbers, strings & variables",
            "11 min",
            r"""
# Numbers, strings & variables

A **variable** is a name bound to an object. Assignment uses `=`:

```python
gc_count = 12        # int
seq_length = 40      # int
gc_fraction = gc_count / seq_length   # float -> 0.3
species = "E. coli"  # str
```

Python has `int` (unbounded precision), `float` (64-bit IEEE 754), and `bool`.
True division `/` always yields a float; `//` is floor division and `%` is the
remainder — handy for reading frames, since codon position is `i % 3`.

**Strings are immutable sequences of characters.** Index from `0`, slice with
`start:stop`:

```python
dna = "ATGCGTAA"
dna[0]      # 'A'
dna[0:3]    # 'ATG'  (the start codon)
dna[-1]     # 'A'    (last base)
len(dna)    # 8
dna.count("G")        # 2
dna.replace("T", "U") # 'AUGCGUAA' (transcription)
```

GC content — a core sequence statistic correlated with melting temperature — is
just arithmetic on counts:

```python
gc = (dna.count("G") + dna.count("C")) / len(dna)
```

GC fraction is bounded in $[0, 1]$ and the duplex melting temperature rises
roughly linearly with it over typical ranges:

```plot
{"title": "Approx. melting temperature vs GC fraction", "xLabel": "GC fraction", "yLabel": "Tm (°C)", "xRange": [0, 1], "yRange": [40, 100], "grid": true, "functions": [{"expr": "64.9 + 41*(x - 0.1645)", "label": "Tm estimate", "color": "#2563eb"}]}
```

**Next:** grouping many sequences with lists, tuples and dicts.
""",
        ),
        _t(
            "Lists, tuples & dictionaries",
            "12 min",
            r"""
# Lists, tuples & dictionaries

Real datasets are collections. Python gives you three workhorses.

A **list** is an ordered, mutable sequence — use it for a set of reads or
samples:

```python
samples = ["WT", "mut1", "mut2"]
samples.append("mut3")
samples[1]            # 'mut1'
samples[1:3]          # ['mut1', 'mut2']
```

A **tuple** is an ordered, *immutable* sequence — good for fixed records like a
genomic coordinate `(chrom, start, end)`:

```python
feature = ("chr1", 10450, 11200)
```

A **dictionary** maps keys to values — ideal for codon tables, counts, or a
gene-to-expression lookup:

```python
counts = {"A": 0, "C": 0, "G": 0, "T": 0}
for base in "ATGCGT":
    counts[base] += 1
# {'A': 1, 'C': 1, 'G': 2, 'T': 2}
```

```mermaid
flowchart TB
  A[Need a collection?] --> B{Order matters?}
  B -->|Yes, will change| C[list]
  B -->|Yes, fixed| D[tuple]
  B -->|No, key-value| E[dict]
```

Dictionaries give average $O(1)$ lookup — counting bases over a whole chromosome
stays fast as the sequence grows, unlike a linear scan per query.

**Next:** making decisions and repeating work with control flow.
""",
        ),
        _t(
            "Control flow: if, for, while",
            "12 min",
            r"""
# Control flow: if, for, while

Programs make decisions and repeat work.

**Conditionals** branch on truth values:

```python
gc = 0.62
if gc > 0.6:
    label = "GC-rich"
elif gc < 0.4:
    label = "AT-rich"
else:
    label = "balanced"
```

**`for` loops** iterate over any sequence — the natural way to walk a genome in
codons:

```python
dna = "ATGCGTAAA"
protein = ""
for i in range(0, len(dna) - 2, 3):
    codon = dna[i:i+3]
    protein += translate(codon)   # using a codon table dict
```

`range(start, stop, step)` produces integers; `enumerate` pairs an index with
each item; `zip` walks two lists in lockstep (e.g. positions and qualities).

**`while` loops** repeat until a condition fails — useful for convergence, such
as iterating a logistic population model until the change is tiny:

```python
N, r, K = 2.0, 0.5, 100.0
while abs(r * N * (1 - N / K)) > 1e-3:
    N += r * N * (1 - N / K)
```

Bounded logistic growth is the classic S-curve such a loop traces:

```plot
{"title": "Logistic population growth", "xLabel": "time", "yLabel": "population N", "xRange": [0, 12], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "N(t)/K", "color": "#16a34a"}]}
```

Use `break` to exit early and `continue` to skip an iteration (e.g. ambiguous
`N` bases).

**Next:** the comprehensions that make Python concise.
""",
        ),
        _t(
            "Comprehensions & clean iteration",
            "10 min",
            r"""
# Comprehensions & clean iteration

A **list comprehension** builds a list from an iterable in one readable line. It
replaces the `for`-append pattern and reads like set-builder notation
$\{f(x) : x \in S\}$.

```python
seqs = ["atg", "ggc", "ttt"]
upper = [s.upper() for s in seqs]              # ['ATG', 'GGC', 'TTT']
gc = [ (s.count("g") + s.count("c")) / len(s) for s in seqs ]
```

Add a **filter** clause to keep only some elements — here, long reads:

```python
long_reads = [r for r in reads if len(r) >= 150]
```

**Dictionary comprehensions** build maps; pairing with `zip` is idiomatic:

```python
genes = ["BRCA1", "TP53", "EGFR"]
expr = [8.2, 11.4, 6.7]
table = {g: e for g, e in zip(genes, expr)}
```

```mermaid
flowchart LR
  A[iterable] --> B[expression f x]
  A --> C{condition?}
  C -->|keep| B
  B --> D[new list / dict]
```

Comprehensions are not just shorter — they signal intent ("transform" or
"filter") and are typically faster than an explicit loop because the iteration
runs in optimised C. Reserve plain loops for side effects (writing files,
printing) and complex multi-step logic.

The payoff scales: as a dataset grows, vectorised, comprehension-style code
keeps runtime nearly linear while staying legible.

```plot
{"title": "Comprehension runtime scales linearly", "xLabel": "thousands of reads", "yLabel": "relative time", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "O(n)", "color": "#2563eb"}]}
```

**Next:** check your understanding of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- Python Programming for Biologists -- Intermediate ------------------------

_INTERMEDIATE = SeedCourse(
    slug="programming-biology-python-intermediate",
    title="Python Programming for Biologists — Intermediate",
    description=(
        "Move from scripting to real analysis: write reusable functions and "
        "modules, read and write biological file formats, and master the "
        "NumPy/pandas stack for fast numerical arrays and tabular data. The "
        "quantitative core every downstream model and figure depends on."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Functions, modules & docstrings",
            "11 min",
            r"""
# Functions, modules & docstrings

A **function** packages reusable logic behind a name. Define with `def`, return
with `return`, document with a triple-quoted **docstring**:

```python
def gc_content(seq: str) -> float:
    "Fraction of G or C bases in a DNA string (0-1)."
    seq = seq.upper()
    return (seq.count("G") + seq.count("C")) / len(seq)
```

Type hints (`seq: str -> float`) document intent and let tools like **mypy**
catch errors. Use **default arguments** for options and **keyword arguments**
for clarity:

```python
def trim(seq, min_qual=20, max_len=150):
    ...
```

Group related functions into a **module** (`seqtools.py`) and import them:

```python
from seqtools import gc_content, reverse_complement
```

```mermaid
flowchart LR
  A[seqtools.py] --> B[gc_content]
  A --> C[reverse_complement]
  A --> D[translate]
  E[analysis.py] -->|import| A
```

Good functions are **pure** where possible — output depends only on inputs, no
hidden state — which makes them easy to test with `assert gc_content("GGCC") ==
1.0`. Small, named, documented functions are the unit of reproducible science:
each can be verified independently before you trust the pipeline.

**Next:** getting data in and out of files.
""",
        ),
        _t(
            "Files & biological formats",
            "12 min",
            r"""
# Files & biological formats

Biology lives in text files. Open them with a **context manager** so they close
automatically even on error:

```python
with open("reads.fastq") as fh:
    for line in fh:
        process(line.rstrip())
```

Key formats you will meet:

- **FASTA** — `>header` line then sequence lines. Genomes, proteins.
- **FASTQ** — four lines per read: id, sequence, `+`, Phred quality string.
- **CSV/TSV** — sample sheets, count matrices, metadata.
- **GFF/BED** — genomic feature coordinates.

A minimal FASTA parser, yielding `(header, sequence)` pairs:

```python
def read_fasta(path):
    header, seq = None, []
    with open(path) as fh:
        for line in fh:
            line = line.rstrip()
            if line.startswith(">"):
                if header:
                    yield header, "".join(seq)
                header, seq = line[1:], []
            else:
                seq.append(line)
    if header:
        yield header, "".join(seq)
```

```mermaid
flowchart LR
  A[FASTA/FASTQ file] --> B[open + iterate lines]
  B --> C[parse records]
  C --> D[dict / list of seqs]
  D --> E[downstream analysis]
```

FASTQ Phred quality $Q$ encodes error probability as $Q = -10 \log_{10} P$, so
the chance a base is wrong falls steeply as $Q$ rises:

```plot
{"title": "Phred quality vs error probability", "xLabel": "Phred Q", "yLabel": "error probability", "xRange": [0, 40], "yRange": [0, 1], "grid": true, "functions": [{"expr": "10^(-x/10)", "label": "P(error)", "color": "#dc2626"}]}
```

**Next:** fast numerical arrays with NumPy.
""",
        ),
        _t(
            "NumPy arrays & vectorisation",
            "13 min",
            r"""
# NumPy arrays & vectorisation

**NumPy** provides the `ndarray`: a fixed-type, contiguous, N-dimensional array
that is far faster and leaner than a Python list for numbers. It underpins
pandas, scikit-learn and almost every scientific library.

```python
import numpy as np
expr = np.array([8.2, 11.4, 6.7, 9.1])
expr.mean()        # 8.85
expr.std()         # spread
np.log2(expr)      # element-wise log2, vectorised
```

**Vectorisation** means applying an operation to a whole array at once in C, with
no Python loop. It is both shorter and often 10–100x faster:

```python
fold_change = treated / control          # element-wise
log_fc = np.log2(fold_change)
upregulated = log_fc > 1                  # boolean mask
genes[upregulated]                        # fancy indexing
```

**Broadcasting** lets arrays of different shapes combine (e.g. subtract a
per-gene mean from a matrix), and 2-D arrays model count matrices
(`genes × samples`):

```python
mat = np.array([[10, 12], [3, 2], [7, 9]])
mat.sum(axis=1)    # total per gene
```

```mermaid
flowchart LR
  A[Python list] -->|np.array| B[ndarray]
  B --> C[vectorised math]
  B --> D[boolean masking]
  B --> E[broadcasting]
```

The speed-up over a pure-Python loop widens as arrays grow — vectorised code
stays roughly linear with a tiny constant:

```plot
{"title": "Vectorised vs loop runtime", "xLabel": "array size (millions)", "yLabel": "relative time", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "0.2*x", "label": "vectorised", "color": "#16a34a"}, {"expr": "x", "label": "Python loop", "color": "#dc2626"}]}
```

**Next:** labelled tables with pandas.
""",
        ),
        _t(
            "pandas DataFrames",
            "13 min",
            r"""
# pandas DataFrames

A **pandas** `DataFrame` is a labelled 2-D table — think a spreadsheet or an R
data.frame backed by NumPy. It is how biologists hold sample sheets, count
matrices and metadata.

```python
import pandas as pd
df = pd.read_csv("counts.csv", index_col="gene")
df.head()
df.shape          # (n_genes, n_samples)
df["sample1"]     # a Series (one column)
```

**Selection** uses labels (`.loc`) or positions (`.iloc`):

```python
df.loc["TP53"]                 # one gene across samples
df.loc[df["sample1"] > 100]    # boolean filter
```

**Transform and summarise** without loops:

```python
df["mean"] = df.mean(axis=1)
df["log2"] = np.log2(df["mean"] + 1)
```

**Group-and-aggregate** — the split-apply-combine pattern — is the heart of
tabular analysis (e.g. mean expression per condition):

```python
meta.groupby("condition")["expr"].mean()
```

```mermaid
flowchart LR
  A[CSV / TSV] -->|read_csv| B[DataFrame]
  B --> C[filter rows]
  B --> D[groupby + agg]
  B --> E[merge / join metadata]
  E --> F[tidy table -> plot]
```

A **tidy** table — one observation per row, one variable per column — makes every
later step (plotting, modelling, statistics) trivial. Log transforms tame the
skew typical of expression counts, compressing a wide dynamic range:

```plot
{"title": "log2 compresses expression counts", "xLabel": "raw count", "yLabel": "log2(count+1)", "xRange": [0, 100], "yRange": [0, 7], "grid": true, "functions": [{"expr": "log(x+1)/log(2)", "label": "log2(x+1)", "color": "#2563eb"}]}
```

**Next:** combining functions, files and tables into a small pipeline.
""",
        ),
        _t(
            "From data to a tidy analysis",
            "11 min",
            r"""
# From data to a tidy analysis

The intermediate skills combine into a repeatable mini-pipeline: **read,
transform, summarise, save.** Each stage is a small function so you can test and
rerun it.

```python
import pandas as pd, numpy as np

def load(path):
    return pd.read_csv(path, index_col="gene")

def normalise(df):
    "Counts per million, then log2."
    cpm = df / df.sum(axis=0) * 1e6
    return np.log2(cpm + 1)

def top_variable(df, n=500):
    return df.loc[df.var(axis=1).sort_values(ascending=False).index[:n]]

counts = load("counts.csv")
logcpm = normalise(counts)
hv = top_variable(logcpm)
hv.to_csv("highly_variable.csv")
```

```mermaid
flowchart LR
  A[counts.csv] --> B[load]
  B --> C[normalise CPM + log2]
  C --> D[select variable genes]
  D --> E[highly_variable.csv]
```

CPM normalisation removes library-size differences so samples are comparable;
selecting highly variable genes focuses downstream clustering on real biological
signal, not noise. Variance-based ranking keeps the genes whose spread across
samples is largest:

```plot
{"title": "Ranked gene variance (select the top tail)", "xLabel": "gene rank", "yLabel": "variance", "xRange": [1, 10], "yRange": [0, 5], "grid": true, "functions": [{"expr": "5*exp(-0.5*x)", "label": "variance", "color": "#16a34a"}]}
```

Because every step is a named function reading and writing explicit files,
rerunning on a new dataset is one command — the foundation of reproducibility you
will formalise next.

**Next:** check your understanding of the quantitative core.
""",
        ),
        _quiz(),
    ),
)


# -- Python Programming for Biologists -- Advanced ----------------------------

_ADVANCED = SeedCourse(
    slug="programming-biology-python-advanced",
    title="Python Programming for Biologists — Advanced",
    description=(
        "Apply Python at research scale: Biopython for sequence and structure "
        "work, publication-quality plotting, fully reproducible Jupyter "
        "notebooks and environments, scaling with Biopython/scikit-learn "
        "pipelines, and machine-learning models for biological prediction."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Biopython for sequences",
            "12 min",
            r"""
# Biopython for sequences

**Biopython** is the de facto toolkit for biological computation in Python. Its
`Seq` and `SeqRecord` objects, `SeqIO` parsers and Entrez clients save you from
hand-rolling parsers.

```python
from Bio.Seq import Seq
from Bio import SeqIO

dna = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")
dna.complement()           # base-pairing
dna.reverse_complement()   # the antisense strand
mrna = dna.transcribe()    # T -> U
protein = dna.translate()  # to_stop also available
```

Parse a whole file lazily with `SeqIO`:

```python
for record in SeqIO.parse("genome.fasta", "fasta"):
    print(record.id, len(record.seq))
```

```mermaid
flowchart LR
  A[FASTA / GenBank] -->|SeqIO.parse| B[SeqRecord]
  B --> C[Seq object]
  C --> D[transcribe]
  C --> E[translate]
  C --> F[reverse_complement]
```

Biopython also wraps **BLAST**, **Entrez** (programmatic NCBI access) and
alignment I/O, so a single script can fetch sequences, search a database and
parse hits. Sequence alignment scores decay with evolutionary distance, the
intuition behind every homology search:

```plot
{"title": "Alignment identity decays with divergence", "xLabel": "evolutionary distance", "yLabel": "% identity", "xRange": [0, 10], "yRange": [0, 100], "grid": true, "functions": [{"expr": "100*exp(-0.3*x)", "label": "identity", "color": "#dc2626"}]}
```

**Next:** turning results into publication-quality figures.
""",
        ),
        _t(
            "Publication-quality plotting",
            "12 min",
            r"""
# Publication-quality plotting

Figures are how science is communicated. **Matplotlib** is the foundation;
**seaborn** adds statistical defaults; both produce vector output (PDF/SVG) for
journals.

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(4, 3))
ax.scatter(log_fc, -np.log10(pvalue), s=8)
ax.set_xlabel("log2 fold change")
ax.set_ylabel("-log10 p-value")
ax.axhline(-np.log10(0.05), ls="--", color="grey")
fig.savefig("volcano.pdf", bbox_inches="tight", dpi=300)
```

That is a **volcano plot** — effect size against significance — the standard
summary of a differential-expression experiment.

```mermaid
flowchart LR
  A[results table] --> B[choose encoding]
  B --> C[matplotlib axes]
  C --> D[labels, scale, legend]
  D --> E[savefig PDF/SVG 300 dpi]
```

A dose-response **sigmoid** is another staple — fit and overlay the curve to read
off the $EC_{50}$:

```plot
{"title": "Dose-response sigmoid", "xLabel": "log dose", "yLabel": "response", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "fitted response", "color": "#2563eb"}]}
```

Good figures follow a few rules: label axes with units, prefer vector formats,
use colourblind-safe palettes, and avoid 3-D effects that distort comparison.
Save the *code* that makes the figure, not just the image — so the figure can be
regenerated when the data updates.

**Next:** making the whole analysis reproducible.
""",
        ),
        _t(
            "Reproducible notebooks & environments",
            "12 min",
            r"""
# Reproducible notebooks & environments

A result no one can rerun is not yet science. Two practices fix this.

**Jupyter notebooks** interleave code, output and prose, but they have a trap:
out-of-order execution. Discipline keeps them honest — restart-and-run-all
before sharing, and keep heavy steps in imported `.py` modules so the notebook
stays a thin narrative.

**Pinned environments** make the software stack reproducible. Capture exact
versions:

```bash
conda env export > environment.yml      # or
pip freeze > requirements.txt
```

```mermaid
flowchart LR
  A[raw data + seed] --> B[pinned environment]
  B --> C[notebook: restart & run all]
  C --> D[figures + tables]
  D --> E[version control: git]
  E --> F[anyone reruns -> same result]
```

Round out reproducibility with **version control** (git for code and notebooks),
**random seeds** (`np.random.seed(0)`) so stochastic steps repeat, and a
**README** describing how to run everything. The dependency chain matters: change
a library version and a result can silently shift.

The cost of *not* doing this compounds — irreproducible steps accumulate until a
project cannot be rerun at all, while disciplined projects stay reproducible
indefinitely:

```plot
{"title": "Reproducibility decays without discipline", "xLabel": "months since analysis", "yLabel": "chance it reruns", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "ad-hoc project", "color": "#dc2626"}]}
```

**Next:** scaling pipelines beyond a single notebook.
""",
        ),
        _t(
            "Scaling pipelines & performance",
            "12 min",
            r"""
# Scaling pipelines & performance

Genomics-scale data outgrows a laptop's interactive loop. Several strategies keep
Python fast and organised.

**Profile first.** Use `%timeit` or `cProfile` to find the real bottleneck
before optimising — intuition is usually wrong.

**Vectorise and chunk.** Replace loops with NumPy/pandas operations; for files
bigger than RAM, stream in chunks (`pd.read_csv(..., chunksize=10_000)`) or use
**Dask** / **Polars** for out-of-core, parallel dataframes.

**Workflow managers** (Snakemake, Nextflow) declare each step's inputs and
outputs so only stale steps rerun and independent steps run in parallel:

```python
rule align:
    input: "reads/{sample}.fastq"
    output: "bam/{sample}.bam"
    shell: "bwa mem ref.fa {input} | samtools sort -o {output}"
```

```mermaid
flowchart LR
  A[FASTQ] --> B[QC trim]
  B --> C[align]
  C --> D[quantify]
  D --> E[differential expression]
  E --> F[report]
```

**Parallelism** via `multiprocessing`, `joblib` or a cluster turns embarrassingly
parallel work (per-sample alignment) into near-linear speed-ups. With $p$
workers, runtime falls but Amdahl's law caps the gain at the serial fraction:

```plot
{"title": "Speed-up vs number of workers (Amdahl)", "xLabel": "workers", "yLabel": "speed-up", "xRange": [1, 10], "yRange": [1, 6], "grid": true, "functions": [{"expr": "1/(0.1 + 0.9/x)", "label": "10% serial", "color": "#16a34a"}]}
```

A declarative, parallel pipeline is both faster and more reproducible than a
monolithic script — each step is cached, logged and rerunnable.

**Next:** machine learning for biological prediction.
""",
        ),
        _t(
            "Machine learning for biology",
            "13 min",
            r"""
# Machine learning for biology

When rules are unknown, learn them from data. **scikit-learn** offers a uniform
`fit`/`predict` API for classification (disease vs healthy), regression
(predicting drug response) and clustering (cell types from scRNA-seq).

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

X = logcpm.T.values        # samples × genes
y = labels                 # phenotype per sample
clf = RandomForestClassifier(n_estimators=300)
scores = cross_val_score(clf, X, y, cv=5)
```

```mermaid
flowchart LR
  A[features: genes × samples] --> B[train / test split]
  B --> C[fit model]
  C --> D[cross-validate]
  D --> E[evaluate: ROC, AUC]
  E --> F[interpret: feature importance]
```

Biology brings hard constraints: **many features, few samples** ($p \gg n$)
invites overfitting, so use **cross-validation**, **regularisation** and an
**independent test cohort**. Evaluate classifiers with the **ROC curve** and its
area (AUC); a perfect model bows toward the top-left, random sits on the
diagonal:

```plot
{"title": "ROC curve: good model vs random", "xLabel": "false positive rate", "yLabel": "true positive rate", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "sqrt(x)", "label": "good classifier", "color": "#16a34a"}, {"expr": "x", "label": "random", "color": "#dc2626"}]}
```

State of the art now includes **deep learning** — AlphaFold for structure
prediction, CNNs for variant effect, transformers for protein language models —
all reachable from Python (PyTorch, TensorFlow). The constant rule: hold out
data, report honest error, and validate biologically before claiming discovery.

**Next:** test your advanced mastery.
""",
        ),
        _quiz(),
    ),
)


PROGRAMMING_BIOLOGY_PYTHON_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["PROGRAMMING_BIOLOGY_PYTHON_COURSES"]
