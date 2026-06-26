"""Quiz questions for the Transcriptomics (RNA-Seq) - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Pathway and gene-set enrichment analysis": (
            q(
                "What does GSEA compute as it walks a ranked gene list?",
                (
                    opt("A running enrichment score, max deviation gives the ES", correct=True),
                    opt("A negative binomial dispersion"),
                    opt("A size factor per sample"),
                    opt("A poly(A) tail length"),
                ),
                "ES is the maximum deviation of the running sum from zero.",
            ),
            q(
                "How is GSEA significance typically established?",
                (
                    opt(
                        "By permutation of sample labels or genes, with FDR adjustment",
                        correct=True,
                    ),
                    opt("By a single Wald test"),
                    opt("By raw p-value with no correction"),
                    opt("By counting exons"),
                ),
                "Permutation builds the null; FDR adjusts for many sets.",
            ),
            q(
                "Which resource provides curated gene-set collections like Hallmark?",
                (
                    opt("MSigDB", correct=True),
                    opt("FASTQ"),
                    opt("STAR index"),
                    opt("Phred table"),
                ),
                "MSigDB hosts Hallmark, C2 and GO collections.",
            ),
        ),
        "Co-expression networks and WGCNA": (
            q(
                "What does WGCNA's soft-thresholding power beta do?",
                (
                    opt(
                        "Raises absolute correlations to a power, emphasizing strong links",
                        correct=True,
                    ),
                    opt("Sets all correlations to 0 or 1"),
                    opt("Removes the correlation step entirely"),
                    opt("Normalizes counts to TPM"),
                ),
                "a_ij = |cor|^beta suppresses weak, noisy correlations.",
            ),
            q(
                "How does WGCNA summarize a module?",
                (
                    opt("By its module eigengene (first principal component)", correct=True),
                    opt("By the longest gene in it"),
                    opt("By the total read count"),
                    opt("By the GC content"),
                ),
                "The eigengene is correlated with traits; central genes are hubs.",
            ),
            q(
                "What topology does soft-thresholding help the network approximate?",
                (
                    opt("Scale-free topology", correct=True),
                    opt("A perfectly random graph"),
                    opt("A fully connected clique"),
                    opt("A linear chain"),
                ),
                "Biological networks tend toward scale-free structure.",
            ),
        ),
        "Isoform and transcript-level quantification": (
            q(
                "Why is isoform quantification harder than gene-level counting?",
                (
                    opt("Reads from shared exons are ambiguous among isoforms", correct=True),
                    opt("Isoforms have no exons"),
                    opt("Reads never map to transcripts"),
                    opt("All isoforms are identical"),
                ),
                "Shared exons make read-to-isoform assignment uncertain.",
            ),
            q(
                "What algorithm do salmon, kallisto and RSEM use to assign ambiguous reads?",
                (
                    opt("Expectation-maximization (EM)", correct=True),
                    opt("Bonferroni correction"),
                    opt("Principal component analysis"),
                    opt("Hierarchical clustering"),
                ),
                "EM maximizes the likelihood of the observed reads over transcripts.",
            ),
            q(
                "What does rMATS quantify for splicing events?",
                (
                    opt("Percent spliced-in (PSI)", correct=True),
                    opt("Size factors"),
                    opt("Phred quality scores"),
                    opt("GC bias"),
                ),
                "PSI measures inclusion of an exon/event across conditions.",
            ),
        ),
        "Single-cell RNA-seq": (
            q(
                "What does a unique molecular identifier (UMI) enable?",
                (
                    opt("Collapsing PCR duplicates to true molecule counts", correct=True),
                    opt("Sorting cells by size"),
                    opt("Aligning to the genome"),
                    opt("Removing introns"),
                ),
                "UMIs tag each original molecule, so duplicates collapse.",
            ),
            q(
                "What characterizes scRNA-seq data statistically?",
                (
                    opt(
                        "High sparsity (many zeros / dropout) and high dimensionality", correct=True
                    ),
                    opt("Dense matrices with no zeros"),
                    opt("Only a handful of genes measured"),
                    opt("Continuous negative values"),
                ),
                "Most genes are zero in any given cell.",
            ),
            q(
                "Which step typically precedes UMAP and clustering in a standard pipeline?",
                (
                    opt("PCA for dimensionality reduction", correct=True),
                    opt("Final pathway enrichment"),
                    opt("Adapter ligation"),
                    opt("rRNA depletion"),
                ),
                "PCA reduces dimensions before UMAP/Leiden clustering.",
            ),
        ),
        "Long-read, spatial and deep learning": (
            q(
                "What key advantage do long-read RNA-seq platforms offer?",
                (
                    opt("Reading full-length isoforms directly", correct=True),
                    opt("Lower per-base error than short reads"),
                    opt("No need for any RNA at all"),
                    opt("Elimination of splicing"),
                ),
                "Nanopore and PacBio capture whole isoforms despite higher error.",
            ),
            q(
                "What does spatial transcriptomics preserve that bulk and single-cell lose?",
                (
                    opt("The tissue coordinates of each measurement", correct=True),
                    opt("The DNA methylation state"),
                    opt("The poly(A) tail"),
                    opt("The sequencing adapter"),
                ),
                "Spatial methods map expression onto histology positions.",
            ),
            q(
                "Which model predicts expression directly from DNA sequence?",
                (
                    opt("Enformer / Borzoi (transformer models)", correct=True),
                    opt("DESeq2"),
                    opt("featureCounts"),
                    opt("TMM"),
                ),
                "Enformer and Borzoi use transformers over genomic sequence.",
            ),
        ),
        "Multi-omics integration and applications": (
            q(
                "What does eQTL mapping associate?",
                (
                    opt("Genetic variants with gene expression levels", correct=True),
                    opt("Proteins with metabolites only"),
                    opt("Read length with GC content"),
                    opt("Adapters with lanes"),
                ),
                "eQTLs link genotype to expression (e.g. GTEx).",
            ),
            q(
                "What does CIBERSORTx perform on bulk RNA-seq?",
                (
                    opt("Deconvolution into cell-type proportions", correct=True),
                    opt("Genome assembly"),
                    opt("Adapter trimming"),
                    opt("Variant calling"),
                ),
                "Deconvolution estimates cell-type composition of bulk samples.",
            ),
            q(
                "Which platform measures RNA and chromatin accessibility in the same cell?",
                (
                    opt("10x Multiome (RNA + ATAC)", correct=True),
                    opt("Sanger sequencing"),
                    opt("Bulk poly(A) RNA-seq"),
                    opt("Western blot"),
                ),
                "Multi-modal single cell integrates RNA and ATAC per cell.",
            ),
        ),
    },
    final=(
        q(
            "What is the enrichment score (ES) in GSEA?",
            (
                opt("The maximum deviation of the running sum from zero", correct=True),
                opt("The mean of all p-values"),
                opt("The total read count"),
                opt("The gene length sum"),
            ),
            "GSEA walks the ranked list and records the peak deviation.",
        ),
        q(
            "In WGCNA, what is a module eigengene?",
            (
                opt("The first principal component summarizing a module", correct=True),
                opt("The longest gene in the module"),
                opt("The raw count of a hub gene"),
                opt("The GC content of the module"),
            ),
            "The eigengene is correlated with traits to find relevant modules.",
        ),
        q(
            "Which algorithm resolves ambiguous reads in transcript quantification?",
            (
                opt("Expectation-maximization", correct=True),
                opt("Benjamini-Hochberg"),
                opt("Leiden clustering"),
                opt("Soft-thresholding"),
            ),
            "EM assigns reads probabilistically to transcripts.",
        ),
        q(
            "What is the main role of UMIs in droplet scRNA-seq?",
            (
                opt("Counting true molecules by collapsing PCR duplicates", correct=True),
                opt("Encoding the cell type"),
                opt("Trimming adapters"),
                opt("Depleting rRNA"),
            ),
            "Each original molecule gets a unique tag.",
        ),
        q(
            "Which is a deep-learning foundation model for single-cell data?",
            (
                opt("scGPT / Geneformer", correct=True),
                opt("STAR"),
                opt("HTSeq"),
                opt("kallisto"),
            ),
            "These are pretrained on millions of cells for transfer tasks.",
        ),
        q(
            "What does multi-omics integration aim to provide over RNA-seq alone?",
            (
                opt("A more mechanistic, multi-layer biological picture", correct=True),
                opt("Faster sequencing only"),
                opt("Removal of all replicates"),
                opt("Shorter reads"),
            ),
            "Combining layers (ATAC, methylation, genotype) links mechanism.",
        ),
    ),
)
