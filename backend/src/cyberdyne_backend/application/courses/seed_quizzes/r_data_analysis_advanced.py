"""Quiz questions for the R & Data Analysis - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Bioconductor and S4 data containers": (
            q(
                "How are Bioconductor packages installed?",
                (
                    opt("With BiocManager::install()", correct=True),
                    opt("With pip install"),
                    opt("By copying files manually only"),
                    opt("They cannot be installed"),
                ),
                "BiocManager coordinates Bioconductor's versioned releases.",
            ),
            q(
                "A SummarizedExperiment binds an assay matrix together with:",
                (
                    opt("rowData (feature annotation) and colData (sample metadata)", correct=True),
                    opt("Only a list of file paths"),
                    opt("A single p-value"),
                    opt("Nothing else"),
                ),
                "The container keeps counts, gene annotation and sample metadata aligned.",
            ),
            q(
                "Why does keeping data and metadata in one S4 object help?",
                (
                    opt(
                        "Subsetting keeps samples and metadata aligned, avoiding mix-ups",
                        correct=True,
                    ),
                    opt("It makes the file smaller than a CSV always"),
                    opt("It removes the need for normalisation"),
                    opt("It guarantees significance"),
                ),
                "Coordinated subsetting prevents the sample-swap errors of loose spreadsheets.",
            ),
        ),
        "RNA-seq differential expression with DESeq2": (
            q(
                "DESeq2 models RNA-seq counts with which distribution?",
                (
                    opt("Negative binomial", correct=True),
                    opt("Normal (Gaussian)"),
                    opt("Uniform"),
                    opt("Exponential"),
                ),
                "Counts are over-dispersed, so DESeq2 uses a negative-binomial GLM.",
            ),
            q(
                "Size-factor estimation in DESeq2 corrects for:",
                (
                    opt(
                        "Differences in library size and composition between samples", correct=True
                    ),
                    opt("Gene length only"),
                    opt("The number of replicates"),
                    opt("The colour of the plot"),
                ),
                "Size factors normalise sequencing depth and composition across samples.",
            ),
            q(
                "Why is the Poisson model too tight for RNA-seq counts?",
                (
                    opt(
                        "Its variance equals the mean, but real counts are over-dispersed",
                        correct=True,
                    ),
                    opt("It cannot handle integers"),
                    opt("It requires continuous data only"),
                    opt("It ignores the design formula"),
                ),
                "Poisson forces var = mean; biological counts show var > mean, hence the NB model.",
            ),
        ),
        "Multiple testing at genome scale": (
            q(
                "Testing 20,000 genes at alpha = 0.05 with no correction yields roughly:",
                (
                    opt("About 1000 false positives by chance", correct=True),
                    opt("Zero false positives"),
                    opt("Exactly one false positive"),
                    opt("All genes significant"),
                ),
                "0.05 x 20000 = 1000 expected false positives without correction.",
            ),
            q(
                "Benjamini-Hochberg controls the:",
                (
                    opt(
                        "False discovery rate (expected fraction of false positives)", correct=True
                    ),
                    opt("Family-wise error rate"),
                    opt("Type II error rate exactly"),
                    opt("Effect size"),
                ),
                "BH bounds the expected proportion of false positives among the calls.",
            ),
            q(
                "Compared with Bonferroni, FDR control is preferred in genomics because it:",
                (
                    opt("Keeps more power across tens of thousands of tests", correct=True),
                    opt("Guarantees no false positives at all"),
                    opt("Requires fewer samples"),
                    opt("Ignores the p-values"),
                ),
                "FDR trades a controlled fraction of false positives for much greater power than FWER control.",
            ),
        ),
        "Single-cell RNA-seq analysis": (
            q(
                "A common single-cell QC filter removes cells with:",
                (
                    opt("Very few detected genes or high mitochondrial fraction", correct=True),
                    opt("Exactly the median number of genes"),
                    opt("Any expression of housekeeping genes"),
                    opt("Names starting with a vowel"),
                ),
                "Low gene counts and high mito fraction flag empty droplets or dying cells.",
            ),
            q(
                "Which step is used to visualise cells in 2-D after PCA?",
                (
                    opt("UMAP or t-SNE", correct=True),
                    opt("A t-test"),
                    opt("A pivot_longer call"),
                    opt("A Bonferroni correction"),
                ),
                "Nonlinear embeddings like UMAP/t-SNE place cells in 2-D for visualisation.",
            ),
            q(
                "Cell-type identity of a cluster is determined from its:",
                (
                    opt("Marker genes (differentially expressed vs other cells)", correct=True),
                    opt("Total read count alone"),
                    opt("Alphabetical cluster label"),
                    opt("Number of principal components"),
                ),
                "Marker genes that are up in a cluster name its cell type.",
            ),
        ),
        "Machine learning on omics with tidymodels": (
            q(
                "The 'p >> n' regime in omics means:",
                (
                    opt("Far more features than samples, so models easily overfit", correct=True),
                    opt("More samples than features"),
                    opt("Exactly equal features and samples"),
                    opt("No features at all"),
                ),
                "Thousands of predictors with few samples make regularisation essential.",
            ),
            q(
                "The lasso penalty (L1) is special because it:",
                (
                    opt(
                        "Drives many coefficients to exactly zero, selecting features", correct=True
                    ),
                    opt("Never shrinks coefficients"),
                    opt("Adds new features automatically"),
                    opt("Requires a Gaussian response"),
                ),
                "The L1 penalty performs feature selection by zeroing out coefficients.",
            ),
            q(
                "How should model performance be estimated to avoid optimism?",
                (
                    opt(
                        "Cross-validation on held-out folds, with a final untouched test set",
                        correct=True,
                    ),
                    opt("On the same data used to train"),
                    opt("By picking the lowest training error"),
                    opt("By the number of features alone"),
                ),
                "Held-out folds and a separate test set give an honest performance estimate.",
            ),
        ),
    },
    final=(
        q(
            "The workhorse Bioconductor container for assay + metadata is:",
            (
                opt("SummarizedExperiment", correct=True),
                opt("data.frame"),
                opt("tibble"),
                opt("matrix"),
            ),
            "It binds the assay matrix to rowData and colData.",
        ),
        q(
            "DESeq2's per-gene effect size is reported as:",
            (
                opt("A log2 fold change", correct=True),
                opt("A raw read count"),
                opt("A p-value only"),
                opt("A size factor"),
            ),
            "log2 fold change is the effect; the adjusted p-value is the evidence.",
        ),
        q(
            "p.adjust(p, method = 'BH') controls the:",
            (
                opt("False discovery rate", correct=True),
                opt("Family-wise error rate"),
                opt("Mean squared error"),
                opt("Library size"),
            ),
            "BH is the genomics default for FDR control.",
        ),
        q(
            "In single-cell analysis, graph-based clustering (Louvain/Leiden) is used to:",
            (
                opt("Group similar cells into putative cell types", correct=True),
                opt("Normalise read depth"),
                opt("Render a UMAP"),
                opt("Estimate size factors"),
            ),
            "Shared-nearest-neighbour graphs plus community detection call clusters.",
        ),
        q(
            "Regularisation in p >> n omics models exists to:",
            (
                opt("Reduce overfitting by shrinking or zeroing coefficients", correct=True),
                opt("Increase the number of features"),
                opt("Remove the need for cross-validation"),
                opt("Guarantee a perfect fit on training data"),
            ),
            "Penalties control variance when predictors vastly outnumber samples.",
        ),
        q(
            "As model complexity increases, test error typically:",
            (
                opt("Falls then rises (a U-shaped overfitting curve)", correct=True),
                opt("Always decreases monotonically"),
                opt("Stays exactly constant"),
                opt("Always increases from the start"),
            ),
            "Beyond a point, added complexity overfits and test error climbs again.",
        ),
    ),
)
