"""R & Data Analysis track: Basics -> Intermediate -> Advanced.

From R syntax, vectors and data frames, through the tidyverse, ggplot2 grammar
of graphics and core statistical modelling, to Bioconductor workflows for
high-throughput omics (RNA-seq with DESeq2, single-cell, and ML on -omics).
Lessons are ``text`` with LaTeX, interactive ```plot blocks and ```mermaid
pipeline diagrams.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- R & Data Analysis -- Basics ----------------------------------------------

_BASICS = SeedCourse(
    slug="r-data-analysis-basics",
    title="R & Data Analysis — Basics",
    description=(
        "Start from zero in R: the interactive console and RStudio, atomic "
        "vectors and vectorised arithmetic, the major data structures, and the "
        "data frame that anchors every analysis. You will read in a dataset, "
        "subset and summarise it, and make a first plot — the foundation the "
        "tidyverse and Bioconductor build on."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is R and the RStudio workflow",
            "10 min",
            r"""
# What is R and the RStudio workflow

R is a free, open-source language built *for* statistics and data analysis. You
type expressions at the **console** and R evaluates them immediately, which makes
it ideal for interactive exploration. Most people drive R through **RStudio** (or
its successor Positron), which adds a script editor, environment pane, plot pane
and help browser.

The assignment operator is `<-` (an arrow), and `#` starts a comment:

```r
x <- c(2, 4, 6, 8)   # a numeric vector
mean(x)              # -> 5
```

Reproducibility is the whole point: write your steps in a **script** (`.R`) or an
**R Markdown / Quarto** document, not just at the console, so the analysis can be
re-run end to end. Install add-on packages once with `install.packages("dplyr")`
and load them each session with `library(dplyr)`.

```mermaid
flowchart LR
  A[Raw data] --> B[Script / Quarto]
  B --> C[R engine evaluates]
  C --> D[Tables & plots]
  D --> E[Reproducible report]
```

R is **vectorised**: operations apply to whole vectors at once, which is both
faster and clearer than writing loops.

**Next:** the atomic vector, R's fundamental unit.
""",
        ),
        _t(
            "Atomic vectors and vectorised arithmetic",
            "11 min",
            r"""
# Atomic vectors and vectorised arithmetic

Everything in R is built from **vectors**. An atomic vector holds elements of
one type: `logical`, `integer`, `double`, or `character`. Even a single number is
a length-1 vector. Build one with `c()` (combine):

```r
conc <- c(0, 1, 2, 5, 10)      # double
log2(conc + 1)                 # applied to every element at once
```

Arithmetic is **element-wise**. When lengths differ R **recycles** the shorter
vector, which is powerful but a classic source of silent bugs if lengths are not
multiples. Indexing is **1-based** and very flexible: positive indices keep,
negative indices drop, and a logical vector filters.

```r
conc[conc > 2]          # logical subsetting -> 5, 10
conc[-1]                # drop the first element
```

A response that saturates with dose is a recurring shape in biology — the
Michaelis–Menten curve $v=\frac{V_{max}[S]}{K_m+[S]}$ is the canonical example:

```plot
{"title": "Saturating response v vs substrate [S]", "xLabel": "[S]", "yLabel": "v", "xRange": [0,20], "yRange": [0,9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "Vmax=8, Km=2", "color": "#2563eb"}]}
```

Missing values are the special `NA`; most functions take `na.rm = TRUE` to skip
them.

**Next:** lists, factors and the data frame.
""",
        ),
        _t(
            "Data structures: lists, factors and data frames",
            "12 min",
            r"""
# Data structures: lists, factors and data frames

Beyond atomic vectors, R has a few key structures:

- **list** — a container whose elements can be *anything* (vectors, models, even
  other lists). Indexed with `[[ ]]` for one element, `[ ]` for a sub-list.
- **factor** — a categorical variable stored as integer codes plus **levels**
  (e.g. `c("low","high")`). Essential for modelling; the first level is the
  reference in regression.
- **matrix** — a 2-D atomic structure, one type only.
- **data frame** — a list of equal-length columns of possibly different types.
  It is *the* table of data analysis: rows are observations, columns variables.

```r
df <- data.frame(
  gene = c("TP53", "EGFR", "MYC"),
  expr = c(8.2, 11.4, 9.7),
  group = factor(c("ctrl", "treat", "treat"))
)
str(df)        # inspect structure
df$expr        # extract the expr column
```

```mermaid
flowchart TB
  A[Atomic vector] --> B[Matrix - 2D, one type]
  A --> C[List - mixed types]
  C --> D[Data frame - columns of equal length]
  D --> E[tibble - tidy data frame]
```

The modern **tibble** (from the tidyverse) is a data frame with nicer printing
and stricter, more predictable behaviour.

**Next:** importing real data and inspecting it.
""",
        ),
        _t(
            "Importing and inspecting data",
            "10 min",
            r"""
# Importing and inspecting data

Most analyses begin by reading a file. For delimited text, `readr::read_csv()`
is fast and gives a tibble with sensible column types; base R offers
`read.csv()`. For Excel use `readxl::read_excel()`.

```r
library(readr)
cells <- read_csv("cells.csv")
```

Before *any* statistics, **look at the data**. A short inspection ritual catches
most disasters:

```r
dim(cells)        # rows, columns
head(cells)       # first rows
str(cells)        # types per column
summary(cells)    # min/median/mean/max per numeric column
colSums(is.na(cells))   # missing values per column
```

Check that numeric columns really are numeric (a stray "N/A" string coerces a
whole column to character), that factors have the levels you expect, and that
counts are non-negative. The distribution of a measured variable often grows or
decays smoothly; an exponential growth curve is a common first model to keep in
mind:

```plot
{"title": "Exponential growth of a cell count", "xLabel": "time (h)", "yLabel": "count", "xRange": [0,10], "yRange": [0,20], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "N0=1, r=0.3", "color": "#16a34a"}]}
```

Garbage in, garbage out: a careful inspection now saves hours later.

**Next:** subsetting and summarising.
""",
        ),
        _t(
            "Subsetting, summarising and tabulating",
            "11 min",
            r"""
# Subsetting, summarising and tabulating

With a clean data frame you can ask questions. Base R subsets with `[rows, cols]`
and a logical condition on rows:

```r
treated <- cells[cells$group == "treat", ]
mean(treated$expr, na.rm = TRUE)
```

Summary functions reduce a vector to one number: `mean`, `median`, `sd`,
`var`, `min`, `max`, `quantile`. To compute a summary *per group*, base R uses
`tapply` or `aggregate`:

```r
aggregate(expr ~ group, data = cells, FUN = mean)
```

Categorical variables are summarised by counting. `table()` builds a frequency
table; a two-way `table(a, b)` is a contingency table, and `prop.table()` turns
counts into proportions.

```r
table(cells$group)
prop.table(table(cells$group, cells$responder), margin = 1)
```

```mermaid
flowchart LR
  A[Data frame] --> B[Filter rows - logical]
  A --> C[Select columns]
  B --> D[Summarise - mean/sd]
  C --> D
  D --> E[Group-wise table]
```

These split-apply-combine steps are exactly what the tidyverse will make
fluent next.

**Next:** a first plot with base graphics.
""",
        ),
        _t(
            "A first plot with base graphics",
            "10 min",
            r"""
# A first plot with base graphics

A picture exposes structure no summary statistic can. Base R ships capable
plotting functions you can call in one line.

```r
hist(cells$expr)                       # distribution of one variable
boxplot(expr ~ group, data = cells)    # spread by group
plot(cells$dose, cells$response)       # scatter of y vs x
```

Add a trend line with `abline(lm(response ~ dose, data = cells))`, label axes
with `xlab`/`ylab`, and colour points by group with the `col` argument. A scatter
of response against dose frequently follows a sigmoid (logistic) dose–response
curve, which underlies EC50 estimation:

```plot
{"title": "Sigmoid dose-response", "xLabel": "log dose", "yLabel": "response", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "EC50 at log dose 5", "color": "#dc2626"}]}
```

Base graphics are quick for exploration. For polished, layered figures the
**ggplot2** grammar of graphics — the next course — is the standard, but the
habit of *plotting early and often* starts here.

**Next:** test your foundations, then move on to the tidyverse.
""",
        ),
        _quiz(),
    ),
)


# -- R & Data Analysis -- Intermediate ----------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="r-data-analysis-intermediate",
    title="R & Data Analysis — Intermediate",
    description=(
        "Work like a modern R analyst: reshape and transform with dplyr and "
        "tidyr, master the ggplot2 grammar of graphics, fit and interpret "
        "linear and generalised linear models, run the core hypothesis tests "
        "correctly, and package an analysis into a reproducible Quarto report."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The tidyverse and dplyr verbs",
            "12 min",
            r"""
# The tidyverse and dplyr verbs

The **tidyverse** is a coherent family of packages sharing a philosophy: tidy
data (one observation per row, one variable per column) flowing through small,
composable verbs. The pipe `|>` (or `%>%`) passes the left value as the first
argument of the next call, so code reads top-to-bottom like a recipe.

The five core **dplyr** verbs:

- `filter()` — keep rows by condition
- `select()` — keep/drop columns
- `mutate()` — add or transform columns
- `arrange()` — sort rows
- `summarise()` + `group_by()` — collapse groups to summaries

```r
library(dplyr)
cells |>
  filter(!is.na(expr)) |>
  group_by(group) |>
  summarise(mean_expr = mean(expr), n = n())
```

```mermaid
flowchart LR
  A[tibble] --> B[filter]
  B --> C[mutate]
  C --> D[group_by]
  D --> E[summarise]
  E --> F[arrange -> result]
```

`group_by()` + `summarise()` is the split-apply-combine pattern from the basics,
now declarative and fast. This single idiom covers most day-to-day wrangling.

**Next:** reshaping data with tidyr.
""",
        ),
        _t(
            "Reshaping and joining with tidyr",
            "11 min",
            r"""
# Reshaping and joining with tidyr

Data rarely arrives in the shape your model needs. **tidyr** reshapes it.
`pivot_longer()` turns wide columns into key/value rows; `pivot_wider()` does the
reverse. Omics expression matrices (genes x samples) are wide; most tidyverse and
ggplot2 code wants the **long** form.

```r
library(tidyr)
long <- expr_wide |>
  pivot_longer(cols = -gene, names_to = "sample", values_to = "count")
```

To combine tables, **mutating joins** match on key columns:

- `inner_join` — rows present in both
- `left_join` — all rows of the left, NA where unmatched
- `full_join` — union of keys

```r
long |> left_join(sample_metadata, by = "sample")
```

```mermaid
flowchart LR
  A[Wide: genes x samples] -->|pivot_longer| B[Long: gene, sample, count]
  B -->|left_join metadata| C[Tidy analysis table]
  C -->|pivot_wider| A
```

The fraction of samples matched in a join behaves like a saturating curve as you
add reference keys — coverage rises but with diminishing returns:

```plot
{"title": "Join coverage vs reference keys", "xLabel": "keys added", "yLabel": "fraction matched", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating coverage", "color": "#2563eb"}]}
```

**Next:** the grammar of graphics with ggplot2.
""",
        ),
        _t(
            "ggplot2 and the grammar of graphics",
            "12 min",
            r"""
# ggplot2 and the grammar of graphics

**ggplot2** builds a plot from layered components: **data**, an **aesthetic
mapping** (`aes`) from variables to visual channels (x, y, colour, size), and one
or more **geoms** (points, lines, bars). You add layers with `+`.

```r
library(ggplot2)
ggplot(cells, aes(x = dose, y = response, colour = group)) +
  geom_point() +
  geom_smooth(method = "lm") +
  scale_x_log10() +
  labs(x = "Dose", y = "Response", title = "Dose-response by group")
```

Key extras: **facets** (`facet_wrap(~ group)`) split one plot into small
multiples; **scales** control axes and colour; **themes** control non-data ink.
Because the mapping is explicit, the same code adapts to new variables by editing
`aes()` alone.

```mermaid
flowchart LR
  A[data] --> B[aes mapping]
  B --> C[geom layer]
  C --> D[scales]
  D --> E[facets]
  E --> F[theme -> figure]
```

A `geom_smooth(method = "lm")` overlays a fitted line; for a Hill-shaped binding
curve you would instead fit a nonlinear model and plot its prediction:

```plot
{"title": "Hill binding curve overlaid on data", "xLabel": "ligand", "yLabel": "occupancy", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "Hill n=2, K=3", "color": "#16a34a"}]}
```

**Next:** fitting linear models.
""",
        ),
        _t(
            "Linear models with lm()",
            "12 min",
            r"""
# Linear models with lm()

A linear model relates a continuous response to predictors:
$y = \beta_0 + \beta_1 x_1 + \dots + \beta_p x_p + \varepsilon$, with errors
$\varepsilon \sim N(0,\sigma^2)$. In R the **formula** `y ~ x` is the interface.

```r
fit <- lm(response ~ dose + group, data = cells)
summary(fit)        # coefficients, std errors, p-values, R^2
confint(fit)        # confidence intervals
```

Each coefficient $\beta_j$ is the expected change in $y$ per unit of $x_j$,
*holding the others fixed*. A factor predictor enters as dummy variables relative
to its reference level. The model is fit by **ordinary least squares**, minimising
$\sum (y_i - \hat y_i)^2$.

Always check assumptions with `plot(fit)`: residuals vs fitted (linearity,
constant variance) and a Q–Q plot (normality). The simplest case, one predictor,
is just a straight line through the cloud:

```plot
{"title": "Fitted regression line y = 1 + 0.8x", "xLabel": "x", "yLabel": "y", "xRange": [0,10], "yRange": [0,10], "grid": true, "functions": [{"expr": "1+0.8*x", "label": "OLS fit", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  A[Formula y ~ x] --> B[lm fits by OLS]
  B --> C[summary: betas, R^2]
  C --> D[Check residual plots]
  D --> E[Predict / interpret]
```

**Next:** generalised linear models and hypothesis tests.
""",
        ),
        _t(
            "GLMs and hypothesis testing",
            "12 min",
            r"""
# GLMs and hypothesis testing

When the response is not continuous-Normal, use a **generalised linear model**
(`glm`): a linear predictor passed through a **link** function with a chosen
error family.

- **Binary outcome** -> logistic regression: `family = binomial`, logit link.
  $\log\frac{p}{1-p} = \beta_0 + \beta_1 x$.
- **Counts** -> Poisson (or negative binomial) regression: `family = poisson`,
  log link.

```r
glm(responder ~ dose, data = cells, family = binomial)
```

For simple comparisons, the classic **tests** still matter and must match the
data: Student's *t*-test (two means), ANOVA (more than two groups), the
chi-square / Fisher exact test (categorical association), and the Wilcoxon /
Mann–Whitney (non-parametric). Each returns a **p-value**: the probability of data
this extreme if the null hypothesis were true. The logistic mean curve is a
sigmoid in the predictor:

```plot
{"title": "Logistic regression mean response", "xLabel": "predictor", "yLabel": "P(event)", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "logit fit", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  A{Response type?} -->|Continuous| B[lm / t-test / ANOVA]
  A -->|Binary| C[Logistic glm]
  A -->|Count| D[Poisson / NB glm]
```

A small p-value flags evidence against the null; it is not the probability the
null is true.

**Next:** packaging it all into a reproducible report.
""",
        ),
        _t(
            "Reproducible analysis with Quarto",
            "10 min",
            r"""
# Reproducible analysis with Quarto

An analysis no one can re-run is a liability. **Quarto** (`.qmd`, the successor to
R Markdown) interleaves prose, code and output in one document that **renders** to
HTML, PDF or Word. Code lives in chunks; the rendered report always reflects the
current code and data.

````r
```{r}
library(dplyr); library(ggplot2)
cells |> group_by(group) |> summarise(m = mean(expr))
```
````

Pillars of reproducibility:

- **One document, top to bottom** — no hidden console state.
- **Pin package versions** with `renv` so the environment is restorable.
- **Set a seed** (`set.seed(42)`) before any randomness.
- **Version control** the source with git.

```mermaid
flowchart LR
  A[Data + .qmd source] --> B[quarto render]
  B --> C[Code executed fresh]
  C --> D[HTML / PDF report]
  D --> E[Shareable, re-runnable]
```

The probability that a result reproduces decays sharply with each undocumented
manual step — automation is what keeps it near one:

```plot
{"title": "Reproducibility vs manual steps", "xLabel": "manual steps", "yLabel": "P(reproduces)", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "decay with manual steps", "color": "#dc2626"}]}
```

**Next:** check your knowledge, then on to Bioconductor and omics.
""",
        ),
        _quiz(),
    ),
)


# -- R & Data Analysis -- Advanced --------------------------------------------

_ADVANCED = SeedCourse(
    slug="r-data-analysis-advanced",
    title="R & Data Analysis — Advanced",
    description=(
        "Apply R to high-throughput biology with Bioconductor: the core "
        "S4 data containers, the RNA-seq differential-expression workflow with "
        "DESeq2, multiple-testing correction at genome scale, single-cell "
        "analysis, and machine learning on omics data with tidymodels."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Bioconductor and S4 data containers",
            "12 min",
            r"""
# Bioconductor and S4 data containers

**Bioconductor** is a curated ecosystem of >2000 R packages for genomics,
installed via `BiocManager::install()` and released on a coordinated schedule so
packages interoperate. Its data is organised into **S4** objects — formal classes
with typed **slots** (accessed with `@` or, better, accessor functions) — that
keep an assay matrix and its metadata bound together.

The workhorse container is **SummarizedExperiment**: an `assay` matrix (genes x
samples), `rowData` (feature annotation), and `colData` (sample metadata).

```r
library(SummarizedExperiment)
se <- SummarizedExperiment(
  assays = list(counts = count_matrix),
  colData = sample_info
)
assay(se)[1:3, 1:3]
colData(se)$condition
```

```mermaid
flowchart TB
  A[SummarizedExperiment] --> B[assay: counts genes x samples]
  A --> C[rowData: gene annotation]
  A --> D[colData: sample metadata]
  B --> E[DESeq2 / edgeR]
```

Because data and metadata travel together, subsetting `se[, se$condition ==
"treat"]` keeps everything aligned — a guard against the sample-mixup errors that
plague spreadsheet workflows.

**Next:** the RNA-seq differential-expression workflow.
""",
        ),
        _t(
            "RNA-seq differential expression with DESeq2",
            "13 min",
            r"""
# RNA-seq differential expression with DESeq2

RNA-seq yields **counts** of reads per gene per sample. Counts are
over-dispersed (variance exceeds the mean), so **DESeq2** models them with a
**negative binomial** GLM, estimating a gene-wise dispersion that is shrunk
toward a fitted mean–dispersion trend for stability with few replicates.

```r
library(DESeq2)
dds <- DESeqDataSetFromMatrix(counts, colData = info, design = ~ condition)
dds <- DESeq(dds)
res <- results(dds, contrast = c("condition", "treat", "ctrl"))
```

The pipeline: estimate **size factors** (library-size/composition normalisation),
estimate dispersions, fit the NB GLM, and test each gene's log2 fold change with a
Wald test. The effect size is the $\log_2$ fold change; the evidence is an
adjusted p-value.

```mermaid
flowchart LR
  A[Count matrix] --> B[Size-factor normalisation]
  B --> C[Dispersion estimation + shrinkage]
  C --> D[NB GLM fit]
  D --> E[Wald test per gene]
  E --> F[log2FC + adjusted p]
```

The mean–variance relationship is super-linear (variance grows faster than the
mean), which is exactly why a Poisson model is too tight:

```plot
{"title": "Mean-variance: counts are over-dispersed", "xLabel": "mean count", "yLabel": "variance", "xRange": [0,10], "yRange": [0,20], "grid": true, "functions": [{"expr": "x+0.2*x^2", "label": "NB: var = mu + a*mu^2", "color": "#2563eb"}, {"expr": "x", "label": "Poisson: var = mu", "color": "#16a34a"}]}
```

**Next:** correcting for testing thousands of genes at once.
""",
        ),
        _t(
            "Multiple testing at genome scale",
            "12 min",
            r"""
# Multiple testing at genome scale

Testing 20,000 genes at $\alpha = 0.05$ would yield ~1000 false positives by
chance alone. You must **correct for multiplicity**. Two error rates matter:

- **FWER** (family-wise error rate): P(any false positive). Controlled
  conservatively by **Bonferroni** ($\alpha/m$) or Holm.
- **FDR** (false discovery rate): expected *fraction* of false positives among
  the calls. Controlled by **Benjamini–Hochberg**, the genomics default —
  `p.adjust(p, method = "BH")`.

FDR is the right trade-off for discovery: you accept some false positives to keep
power across tens of thousands of tests. DESeq2 also applies **independent
filtering** to drop low-count genes that have no power, improving the BH
adjustment.

```r
res$padj <- p.adjust(res$pvalue, method = "BH")
sum(res$padj < 0.05, na.rm = TRUE)   # genes called significant
```

```mermaid
flowchart LR
  A[m raw p-values] --> B[Sort ascending]
  B --> C[BH threshold: p(k) <= k/m * q]
  C --> D[Reject below threshold]
  D --> E[FDR controlled at q]
```

Under the null, p-values are uniform, so their histogram is flat; a spike near
zero reveals true signal. The expected number of false positives grows linearly
with the number of tests at fixed alpha:

```plot
{"title": "Expected false positives vs tests (alpha=0.05)", "xLabel": "tests (thousands)", "yLabel": "false positives", "xRange": [0,10], "yRange": [0,0.6], "grid": true, "functions": [{"expr": "0.05*x", "label": "0.05 * m", "color": "#dc2626"}]}
```

**Next:** single-cell analysis.
""",
        ),
        _t(
            "Single-cell RNA-seq analysis",
            "13 min",
            r"""
# Single-cell RNA-seq analysis

Single-cell RNA-seq (scRNA-seq) measures expression in *each cell*, giving a
sparse genes x cells matrix with thousands of cells. Bioconductor's
**SingleCellExperiment** container plus **scran**/**scater** (or the Seurat
ecosystem) drive the workflow.

Standard steps:

1. **Quality control** — drop cells with too few genes or high mitochondrial
   fraction (dying cells).
2. **Normalisation** — deconvolution size factors (scran) for the sparse,
   variable depth.
3. **Feature selection** — keep highly variable genes.
4. **Dimensionality reduction** — PCA, then **UMAP**/t-SNE for visualisation.
5. **Clustering** — graph-based (shared-nearest-neighbour + Louvain/Leiden) to
   call cell types.

```mermaid
flowchart LR
  A[Cells x genes] --> B[QC filter]
  B --> C[Normalise]
  C --> D[Select HVGs]
  D --> E[PCA -> UMAP]
  E --> F[Graph clustering -> cell types]
```

PCA variance explained drops off steeply across components — the "elbow" guides
how many PCs to keep before clustering:

```plot
{"title": "Scree: variance explained per PC", "xLabel": "principal component", "yLabel": "variance explained", "xRange": [1,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "elbow decay", "color": "#16a34a"}]}
```

Each cluster's **marker genes** (differential expression vs the rest) name the
cell type — the biological payoff of the whole pipeline.

**Next:** machine learning on omics data.
""",
        ),
        _t(
            "Machine learning on omics with tidymodels",
            "13 min",
            r"""
# Machine learning on omics with tidymodels

Predicting a phenotype (e.g. tumour subtype) from thousands of features is the
**p >> n** regime — far more predictors than samples — where ordinary regression
overfits. **Regularisation** is essential. **tidymodels** gives a consistent
interface over many engines.

- **Penalised regression** (`glmnet`): the **lasso** adds an $\ell_1$ penalty
  $\lambda\sum|\beta_j|$ that drives many coefficients to exactly zero, doing
  feature selection; **ridge** uses $\ell_2$; **elastic net** blends both.
- **Random forests** / gradient boosting (`ranger`, `xgboost`) capture
  nonlinearities and rank feature importance.

```r
library(tidymodels)
spec <- logistic_reg(penalty = tune(), mixture = 1) |>  # lasso
  set_engine("glmnet")
wf <- workflow() |> add_model(spec) |> add_recipe(rec)
tuned <- tune_grid(wf, resamples = vfold_cv(train, v = 5))
```

**Always** estimate performance by **cross-validation** on held-out folds and
keep a final test set untouched. As model complexity rises, training error falls
but test error eventually climbs — the classic overfitting U-curve that
regularisation and CV exist to control:

```plot
{"title": "Test error vs model complexity (overfitting)", "xLabel": "complexity", "yLabel": "test error", "xRange": [0,10], "yRange": [0,5], "grid": true, "functions": [{"expr": "(x-5)^2/5+0.5", "label": "U-shaped test error", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  A[Omics features p >> n] --> B[Recipe: preprocess]
  B --> C[Lasso / RF model]
  C --> D[Cross-validated tuning]
  D --> E[Held-out test evaluation]
```

**Next:** check your knowledge to complete the track.
""",
        ),
        _quiz(),
    ),
)


R_DATA_ANALYSIS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["R_DATA_ANALYSIS_COURSES"]
