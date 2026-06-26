"""Quiz questions for the Single-Cell & Spatial Omics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Normalization and variance stabilization": (
            q(
                "Why must raw counts be normalized before comparing cells?",
                (
                    opt("Cells differ in library size for technical reasons", correct=True),
                    opt("Counts are always negative"),
                    opt("Genes have different chromosome lengths"),
                    opt("Normalization removes all biological signal"),
                ),
                "Capture and depth vary per cell, so totals are not comparable.",
            ),
            q(
                "What does the log(1+x) transform achieve?",
                (
                    opt("Variance stabilization and taming the heavy right tail", correct=True),
                    opt("It deletes lowly expressed genes"),
                    opt("It converts counts to DNA sequence"),
                    opt("It makes all genes equal"),
                ),
                "log1p compresses large values, stabilizing variance.",
            ),
            q(
                "Which method uses a regularized negative binomial and Pearson residuals?",
                (
                    opt("sctransform", correct=True),
                    opt("BLAST"),
                    opt("k-means"),
                    opt("FASTQC"),
                ),
                "sctransform models counts with an NB and returns Pearson residuals.",
            ),
        ),
        "Highly variable genes and feature selection": (
            q(
                "Why select highly variable genes (HVGs) before analysis?",
                (
                    opt("Most genes add noise; HVGs carry cell-type signal", correct=True),
                    opt("HVGs are the longest genes"),
                    opt("Using all genes is computationally impossible"),
                    opt("HVGs are the only protein-coding genes"),
                ),
                "Restricting to ~2000 HVGs sharpens structure and speeds analysis.",
            ),
            q(
                "Why can't you just rank genes by raw variance?",
                (
                    opt("Variance rises with the mean under technical noise", correct=True),
                    opt("Variance is always zero"),
                    opt("Highly expressed genes have no variance"),
                    opt("Variance equals the gene length"),
                ),
                "HVG methods correct for the mean-variance trend before ranking.",
            ),
            q(
                "A highly variable gene is one whose variance is:",
                (
                    opt("Above the expected technical mean-variance trend", correct=True),
                    opt("Exactly equal to its mean"),
                    opt("Below the trend line"),
                    opt("Always zero"),
                ),
                "Excess variance above the fitted trend marks an HVG.",
            ),
        ),
        "Dimensionality reduction: PCA to UMAP": (
            q(
                "What is PCA used for in the single-cell pipeline?",
                (
                    opt(
                        "Linear reduction to ~30-50 components feeding the kNN graph", correct=True
                    ),
                    opt("Aligning DNA sequences"),
                    opt("Counting UMIs"),
                    opt("Calling variants"),
                ),
                "PCA denoises and provides the space for neighbour-graph construction.",
            ),
            q(
                "What does a scree/elbow plot help decide?",
                (
                    opt("How many principal components to retain", correct=True),
                    opt("How many cells to load"),
                    opt("Which barcode is a doublet"),
                    opt("The mitochondrial threshold"),
                ),
                "The elbow marks where additional PCs add little variance.",
            ),
            q(
                "A correct caution about UMAP/t-SNE embeddings is that:",
                (
                    opt(
                        "Distances and cluster sizes are not quantitatively meaningful",
                        correct=True,
                    ),
                    opt("They are exact and should drive clustering directly"),
                    opt("They are linear projections"),
                    opt("They preserve global distances perfectly"),
                ),
                "They are non-linear visualization tools, not metric spaces.",
            ),
        ),
        "Graph-based clustering with Leiden": (
            q(
                "What structure does single-cell graph clustering operate on?",
                (
                    opt("A k-nearest-neighbour (or SNN) graph in PC space", correct=True),
                    opt("A phylogenetic tree of genes"),
                    opt("The raw FASTQ files"),
                    opt("A protein structure"),
                ),
                "Cells are linked to nearest neighbours, then partitioned.",
            ),
            q(
                "What did Leiden improve over the Louvain algorithm?",
                (
                    opt("It guarantees well-connected communities", correct=True),
                    opt("It runs only on DNA sequences"),
                    opt("It removes the resolution parameter"),
                    opt("It eliminates the need for a graph"),
                ),
                "Louvain could yield disconnected clusters; Leiden fixes this.",
            ),
            q(
                "Raising the Leiden resolution parameter tends to:",
                (
                    opt("Produce more, smaller clusters", correct=True),
                    opt("Produce fewer, larger clusters"),
                    opt("Have no effect on cluster count"),
                    opt("Delete the graph"),
                ),
                "Higher resolution increases granularity.",
            ),
        ),
        "Cell-type annotation with marker genes": (
            q(
                "How are cluster marker genes typically identified?",
                (
                    opt("Differential expression of a cluster versus the rest", correct=True),
                    opt("By gene length"),
                    opt("By chromosome position"),
                    opt("Randomly"),
                ),
                "Wilcoxon/t-test DE finds genes up in the cluster vs all others.",
            ),
            q(
                "CD3D/CD3E are canonical markers of which cell type?",
                (
                    opt("T cells", correct=True),
                    opt("B cells"),
                    opt("Endothelial cells"),
                    opt("Erythrocytes"),
                ),
                "CD3 components mark T cells; CD19/MS4A1 mark B cells.",
            ),
            q(
                "A reference-based annotation tool such as SingleR or CellTypist works by:",
                (
                    opt("Projecting query cells onto a labelled reference", correct=True),
                    opt("Aligning reads to a genome"),
                    opt("Folding proteins"),
                    opt("Counting UMIs"),
                ),
                "These classifiers transfer labels from an annotated reference.",
            ),
        ),
    },
    final=(
        q(
            "The standard normalization recipe scales each cell by its total counts and then:",
            (
                opt("Applies a log(1+x) transform", correct=True),
                opt("Squares the values"),
                opt("Multiplies by gene length"),
                opt("Discards all zeros"),
            ),
            "CP10K scaling followed by log1p is the classic pipeline.",
        ),
        q(
            "Feature selection keeps roughly how many genes for downstream analysis?",
            (
                opt("About 2000-3000 highly variable genes", correct=True),
                opt("All 20000 genes"),
                opt("Exactly 50 genes"),
                opt("Only mitochondrial genes"),
            ),
            "HVG selection focuses on the most informative ~2-3k genes.",
        ),
        q(
            "The correct order of the embedding/clustering pipeline is:",
            (
                opt("Normalize -> HVG -> PCA -> kNN graph -> Leiden", correct=True),
                opt("Leiden -> PCA -> normalize -> HVG"),
                opt("PCA -> normalize -> Leiden -> HVG"),
                opt("kNN -> HVG -> normalize -> PCA"),
            ),
            "PCA and the neighbour graph precede community detection.",
        ),
        q(
            "Compared with k-means, single-cell clustering usually uses:",
            (
                opt("Graph-based community detection (Leiden/Louvain)", correct=True),
                opt("Hierarchical DNA alignment"),
                opt("Linear regression"),
                opt("Principal curves only"),
            ),
            "Neighbour-graph community detection dominates the field.",
        ),
        q(
            "Annotating a cluster as a cell type relies primarily on:",
            (
                opt("Matching up-regulated marker genes to known signatures", correct=True),
                opt("The cluster's number"),
                opt("Its position in the UMAP plot only"),
                opt("Its total UMI count"),
            ),
            "DE markers are matched to canonical cell-type signatures.",
        ),
        q(
            "UMAP and t-SNE in this pipeline are best used for:",
            (
                opt("Visualization, not as the metric basis for clustering", correct=True),
                opt("Exact distance computation"),
                opt("Variant calling"),
                opt("Library-size normalization"),
            ),
            "They display structure; clustering uses the graph in PC space.",
        ),
    ),
)
