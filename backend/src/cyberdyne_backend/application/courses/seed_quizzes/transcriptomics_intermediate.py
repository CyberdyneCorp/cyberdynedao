"""Quiz questions for the Transcriptomics (RNA-Seq) - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Count distributions and overdispersion": (
            q(
                "What relationship between mean and variance defines the Poisson distribution?",
                (
                    opt("Variance equals the mean", correct=True),
                    opt("Variance is always zero"),
                    opt("Variance is the square of the mean"),
                    opt("Variance is unrelated to the mean"),
                ),
                "Poisson has Var = mean, which holds for technical replicates.",
            ),
            q(
                "What is overdispersion in RNA-seq counts?",
                (
                    opt("Biological variance exceeds the Poisson mean", correct=True),
                    opt("Variance is smaller than the mean"),
                    opt("Counts become negative"),
                    opt("All genes have identical counts"),
                ),
                "Across biological replicates, variance is larger than the mean.",
            ),
            q(
                "In the negative binomial, what happens as dispersion alpha approaches zero?",
                (
                    opt("It collapses to the Poisson distribution", correct=True),
                    opt("Variance grows without bound"),
                    opt("The mean becomes infinite"),
                    opt("Counts become continuous"),
                ),
                "Var = mu + alpha*mu^2 reduces to Var = mu when alpha -> 0.",
            ),
        ),
        "Normalization for differential expression": (
            q(
                "Why do DE tools use composition-aware normalization instead of plain CPM?",
                (
                    opt("A few dominant genes can bias simple per-million scaling", correct=True),
                    opt("CPM cannot be computed from counts"),
                    opt("Gene length is irrelevant to CPM"),
                    opt("Libraries always have identical composition"),
                ),
                "Highly expressed genes steal reads, distorting naive scaling.",
            ),
            q(
                "How does DESeq2 compute a sample's size factor?",
                (
                    opt(
                        "Median of each gene's ratio to the geometric mean across samples",
                        correct=True,
                    ),
                    opt("Mean of all raw counts"),
                    opt("Maximum count in the sample"),
                    opt("Total reads divided by gene length"),
                ),
                "The median-of-ratios method is robust to a few variable genes.",
            ),
            q(
                "What does edgeR's TMM method estimate?",
                (
                    opt("A scaling factor from trimmed log-ratios of counts", correct=True),
                    opt("The gene length of each transcript"),
                    opt("The number of PCR cycles used"),
                    opt("The adapter sequence"),
                ),
                "TMM = trimmed mean of M-values, excluding extreme genes.",
            ),
        ),
        "Differential expression with DESeq2 and edgeR": (
            q(
                "What statistical model do DESeq2 and edgeR fit per gene?",
                (
                    opt("A negative binomial generalized linear model", correct=True),
                    opt("A simple linear regression on raw CPM"),
                    opt("A Poisson model with no dispersion"),
                    opt("A logistic classifier"),
                ),
                "Both fit an NB GLM with a size-factor offset.",
            ),
            q(
                "What does the beta1 coefficient in the GLM represent?",
                (
                    opt("The log2 fold change between conditions", correct=True),
                    opt("The sequencing depth"),
                    opt("The gene length"),
                    opt("The intercept baseline"),
                ),
                "beta1 multiplies the condition indicator, giving the log2FC.",
            ),
            q(
                "Why do these tools shrink per-gene dispersion toward a fitted trend?",
                (
                    opt("Per-gene estimates are unreliable with few replicates", correct=True),
                    opt("To make all genes have identical dispersion"),
                    opt("To remove the need for replicates"),
                    opt("To increase the number of false positives"),
                ),
                "Empirical Bayes shrinkage stabilizes low-replicate experiments.",
            ),
        ),
        "Multiple testing and the false discovery rate": (
            q(
                "Why is multiple-testing correction essential in RNA-seq?",
                (
                    opt(
                        "Testing thousands of genes yields many false positives at p<0.05",
                        correct=True,
                    ),
                    opt("Genes are tested only one at a time"),
                    opt("p-values are always exactly zero"),
                    opt("Counts are never random"),
                ),
                "At p<0.05 across 20,000 genes, ~1,000 false hits are expected by chance.",
            ),
            q(
                "What does the false discovery rate control?",
                (
                    opt(
                        "The expected proportion of false positives among called genes",
                        correct=True,
                    ),
                    opt("The probability of any single false positive"),
                    opt("The total number of genes tested"),
                    opt("The sequencing error rate"),
                ),
                "FDR is a proportion among discoveries, unlike family-wise error.",
            ),
            q(
                "Which procedure is the standard FDR control in RNA-seq?",
                (
                    opt("Benjamini-Hochberg", correct=True),
                    opt("Bonferroni"),
                    opt("Tukey's HSD"),
                    opt("Chi-square goodness of fit"),
                ),
                "BH yields adjusted p-values (q-values) controlling FDR.",
            ),
        ),
        "Visualizing results: MA, volcano and PCA": (
            q(
                "What does an MA plot display?",
                (
                    opt("Log2 fold change versus mean expression", correct=True),
                    opt("p-value versus gene length"),
                    opt("Read length versus GC content"),
                    opt("Sample versus batch only"),
                ),
                "M = log2FC on y, A = mean expression on x.",
            ),
            q(
                "What are the axes of a volcano plot?",
                (
                    opt("Log2 fold change versus -log10 p-value", correct=True),
                    opt("Mean expression versus dispersion"),
                    opt("PC1 versus PC2"),
                    opt("Count versus gene length"),
                ),
                "Significant large-effect genes sit in the upper corners.",
            ),
            q(
                "What is PCA on variance-stabilized counts mainly used to check?",
                (
                    opt("Whether samples group by biology rather than batch", correct=True),
                    opt("The exact fold change of each gene"),
                    opt("The adapter contamination level"),
                    opt("The poly(A) tail length"),
                ),
                "PCA/clustering is a key QC for detecting batch effects.",
            ),
        ),
        "From gene lists to biology: an overview": (
            q(
                "What test underlies over-representation analysis (ORA)?",
                (
                    opt(
                        "Hypergeometric / Fisher's exact test on the significant gene set",
                        correct=True,
                    ),
                    opt("A negative binomial GLM"),
                    opt("Principal component analysis"),
                    opt("A t-test on raw counts"),
                ),
                "ORA asks if a category is enriched in the significant set.",
            ),
            q(
                "How does GSEA differ from ORA?",
                (
                    opt(
                        "It uses the whole ranked list, catching coordinated modest changes",
                        correct=True,
                    ),
                    opt("It ignores gene rankings entirely"),
                    opt("It only works on a single gene"),
                    opt("It requires no gene sets"),
                ),
                "GSEA detects sets clustered toward the top or bottom of the ranking.",
            ),
            q(
                "What kinds of annotated categories are commonly tested for enrichment?",
                (
                    opt("GO terms and KEGG pathways", correct=True),
                    opt("FASTQ quality scores"),
                    opt("Flow-cell lane numbers"),
                    opt("Adapter sequences"),
                ),
                "GO and KEGG describe functions and pathways.",
            ),
        ),
    },
    final=(
        q(
            "What distribution is standard for modeling RNA-seq counts across biological replicates?",
            (
                opt("Negative binomial", correct=True),
                opt("Normal"),
                opt("Uniform"),
                opt("Exponential"),
            ),
            "NB adds a dispersion term to handle overdispersion.",
        ),
        q(
            "Which method is DESeq2's normalization?",
            (
                opt("Median of ratios", correct=True),
                opt("TMM"),
                opt("Quantile normalization"),
                opt("Z-scoring"),
            ),
            "DESeq2 uses median-of-ratios size factors; edgeR uses TMM.",
        ),
        q(
            "What does an FDR-adjusted p-value (q-value) of 0.05 mean?",
            (
                opt(
                    "About 5% of the genes called significant are expected to be false",
                    correct=True,
                ),
                opt("Exactly one gene is a false positive"),
                opt("5% of all reads are errors"),
                opt("The fold change is 5%"),
            ),
            "FDR is a proportion among discoveries.",
        ),
        q(
            "Why apply fold-change shrinkage (lfcShrink) before an MA plot?",
            (
                opt("Low-count genes otherwise show inflated, noisy fold changes", correct=True),
                opt("It removes all significant genes"),
                opt("It converts counts to TPM"),
                opt("It increases sequencing depth"),
            ),
            "Shrinkage stabilizes estimates for low-expression genes.",
        ),
        q(
            "What does empirical Bayes dispersion shrinkage achieve?",
            (
                opt("More stable estimates in low-replicate experiments", correct=True),
                opt("Identical dispersion for all genes always"),
                opt("Removal of the need for normalization"),
                opt("Conversion to a Poisson model"),
            ),
            "Per-gene estimates are pulled toward the fitted trend.",
        ),
        q(
            "GSEA's significance is typically assessed by what?",
            (
                opt("Permutation of labels or genes", correct=True),
                opt("A single t-test"),
                opt("Reading the raw p-values directly"),
                opt("Counting exon-exon junctions"),
            ),
            "Permutation builds a null for the enrichment score.",
        ),
    ),
)
