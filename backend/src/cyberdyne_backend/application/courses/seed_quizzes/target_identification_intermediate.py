"""Quiz questions for the Computational Target Identification - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Differential expression done rigorously": (
            q(
                "Which distribution do DESeq2 and edgeR use to model RNA-seq counts?",
                (
                    opt("The negative binomial distribution", correct=True),
                    opt("The standard normal distribution"),
                    opt("The uniform distribution"),
                    opt("The exponential distribution"),
                ),
                "Counts are over-dispersed, so a negative binomial with a gene-specific dispersion is used.",
            ),
            q(
                "What does empirical Bayes shrinkage in limma improve?",
                (
                    opt(
                        "Variance estimates by borrowing information across genes, raising power",
                        correct=True,
                    ),
                    opt("The sequencing read length"),
                    opt("The number of samples collected"),
                    opt("The gene's chromosomal position"),
                ),
                "Moderated variances stabilise small-sample tests and improve power.",
            ),
            q(
                "What does the Benjamini-Hochberg procedure control?",
                (
                    opt("The false discovery rate among the called genes", correct=True),
                    opt("The total RNA yield"),
                    opt("The fold-change magnitude"),
                    opt("The number of genes in the genome"),
                ),
                "BH controls the expected proportion of false positives among discoveries.",
            ),
        ),
        "Network-based target prioritisation": (
            q(
                "What does betweenness centrality measure?",
                (
                    opt(
                        "How often a node lies on shortest paths between other nodes", correct=True
                    ),
                    opt("The molecular weight of a protein"),
                    opt("The number of samples in a study"),
                    opt("The GC content of a gene"),
                ),
                "Betweenness captures a node's role as a bridge in the network.",
            ),
            q(
                "What does random walk with restart accomplish in prioritisation?",
                (
                    opt(
                        "It diffuses signal from disease seed genes to score nearby candidates",
                        correct=True,
                    ),
                    opt("It sequences the genome faster"),
                    opt("It removes all hubs from the graph"),
                    opt("It computes fold-changes"),
                ),
                "RWR implements guilt-by-association via network proximity to seeds.",
            ),
            q(
                "A scale-free network's degree distribution follows what form?",
                (
                    opt("A power law, P(k) ~ k^-gamma, with a few high-degree hubs", correct=True),
                    opt("A flat uniform distribution"),
                    opt("A perfectly normal bell curve"),
                    opt("A single fixed degree for all nodes"),
                ),
                "Power-law degree distributions produce a small number of highly connected hubs.",
            ),
        ),
        "Genetic evidence: GWAS and eQTL": (
            q(
                "Why is genetic evidence so valuable for target identification?",
                (
                    opt(
                        "It supports causality and roughly doubles clinical success rates",
                        correct=True,
                    ),
                    opt("It is the cheapest assay available"),
                    opt("It eliminates the need for any validation"),
                    opt("It measures protein structure directly"),
                ),
                "Genetically supported targets succeed about twice as often in the clinic.",
            ),
            q(
                "What problem do eQTLs help solve for GWAS hits?",
                (
                    opt(
                        "Mapping mostly non-coding signals to the gene they regulate", correct=True
                    ),
                    opt("Increasing sequencing depth"),
                    opt("Removing the need for replication"),
                    opt("Folding the implicated protein"),
                ),
                "eQTLs link expression-altering variants to the responsible gene.",
            ),
            q(
                "What is the conventional genome-wide significance threshold for GWAS?",
                (
                    opt("p < 5e-8", correct=True),
                    opt("p < 0.05"),
                    opt("p < 0.5"),
                    opt("p < 1"),
                ),
                "The stringent 5e-8 threshold accounts for the multiple-testing burden across the genome.",
            ),
        ),
        "Colocalisation and Mendelian randomization": (
            q(
                "What does colocalisation assess?",
                (
                    opt(
                        "Whether a trait and a gene's expression share the same causal variant",
                        correct=True,
                    ),
                    opt("The temperature of the assay"),
                    opt("The molecular weight of the protein"),
                    opt("The number of cells sequenced"),
                ),
                "Coloc gives the posterior probability of a shared causal variant.",
            ),
            q(
                "In Mendelian randomization, genetic variants serve as what?",
                (
                    opt("Instrumental variables mimicking a randomized trial", correct=True),
                    opt("Confounders to be removed"),
                    opt("The disease outcome itself"),
                    opt("Laboratory controls"),
                ),
                "Randomised-at-conception alleles act as instruments for the exposure.",
            ),
            q(
                "What threat to validity does MR-Egger test for?",
                (
                    opt(
                        "Pleiotropy, where an instrument affects the outcome bypassing the exposure",
                        correct=True,
                    ),
                    opt("Low sequencing depth"),
                    opt("Protein misfolding"),
                    opt("Sample contamination"),
                ),
                "Pleiotropy violates the MR assumptions; MR-Egger detects and adjusts for it.",
            ),
        ),
        "Druggability and pocket assessment": (
            q(
                "What does a small-molecule druggability assessment chiefly look for?",
                (
                    opt(
                        "A suitable binding pocket of adequate volume, depth and hydrophobicity",
                        correct=True,
                    ),
                    opt("A high molecular weight"),
                    opt("A long mRNA transcript"),
                    opt("A high GC content"),
                ),
                "Pocket geometry and chemistry determine small-molecule tractability.",
            ),
            q(
                "Which tools detect and score binding pockets from structure?",
                (
                    opt("fpocket, SiteMap and DoGSiteScorer", correct=True),
                    opt("BLAST and Bowtie"),
                    opt("DESeq2 and edgeR"),
                    opt("limma and voom"),
                ),
                "These cavity-detection tools quantify pocket descriptors for druggability.",
            ),
            q(
                "Why are flat protein-protein interfaces often called undruggable?",
                (
                    opt(
                        "They lack deep, enclosed pockets for conventional small molecules",
                        correct=True,
                    ),
                    opt("They have too many deep pockets"),
                    opt("They cannot be crystallised at all"),
                    opt("They are never disease-relevant"),
                ),
                "Shallow, polar, flat surfaces resist classical small-molecule binding.",
            ),
        ),
        "Aggregating evidence into a target score": (
            q(
                "What does the Open Targets platform produce?",
                (
                    opt(
                        "A target-disease association score combining many data types", correct=True
                    ),
                    opt("A single GWAS p-value"),
                    opt("A protein crystal structure"),
                    opt("A cell-culture protocol"),
                ),
                "It harmonises and aggregates evidence into an overall association score.",
            ),
            q(
                "Why is a harmonic-sum aggregation used across evidence?",
                (
                    opt(
                        "It is dominated by the strongest evidence while still rewarding corroboration",
                        correct=True,
                    ),
                    opt("It ignores all but the weakest evidence"),
                    opt("It only counts the number of genes"),
                    opt("It requires no scoring at all"),
                ),
                "The harmonic sum weights the top-ranked scores most but credits multiple strands.",
            ),
            q(
                "What is the practical effect of diminishing returns in evidence aggregation?",
                (
                    opt(
                        "Single-source claims are penalised; convergent orthogonal support is rewarded",
                        correct=True,
                    ),
                    opt("More weak evidence always wins"),
                    opt("Evidence is ignored entirely"),
                    opt("The score becomes negative"),
                ),
                "Concave aggregation rewards independent corroboration over redundant weak signals.",
            ),
        ),
    },
    final=(
        q(
            "Which method models RNA-seq counts with a gene-specific dispersion?",
            (
                opt("DESeq2 / edgeR with the negative binomial", correct=True),
                opt("A simple t-test on raw counts"),
                opt("A Fourier transform"),
                opt("Principal component analysis only"),
            ),
            "Over-dispersed counts require a negative binomial with estimated dispersion.",
        ),
        q(
            "Random walk with restart on a PPI network implements which principle?",
            (
                opt("Guilt by association via proximity to disease seed genes", correct=True),
                opt("Random sequencing of reads"),
                opt("Crystallographic phasing"),
                opt("Codon optimisation"),
            ),
            "RWR scores candidates by network proximity to known disease genes.",
        ),
        q(
            "Why does genetic support strengthen a target hypothesis?",
            (
                opt(
                    "It provides causal evidence and predicts higher clinical success", correct=True
                ),
                opt("It lowers the cost of sequencing"),
                opt("It guarantees a deep binding pocket"),
                opt("It removes the need for any model"),
            ),
            "Genetics is the strongest non-experimental causal signal.",
        ),
        q(
            "Mendelian randomization estimates what?",
            (
                opt("The causal effect of a target's activity on disease risk", correct=True),
                opt("The crystal structure of the target"),
                opt("The sequencing error rate"),
                opt("The melting temperature of DNA"),
            ),
            "Using genetic instruments, MR infers the causal exposure-outcome effect.",
        ),
        q(
            "Which signal indicates a small-molecule-druggable target?",
            (
                opt("A deep, enclosed, suitably hydrophobic binding pocket", correct=True),
                opt("A flat, polar protein surface"),
                opt("A very long mRNA"),
                opt("A high chromosomal copy number"),
            ),
            "Pocket geometry and chemistry drive small-molecule tractability.",
        ),
        q(
            "How should disparate lines of target evidence be combined?",
            (
                opt(
                    "Harmonised per data type then aggregated, rewarding orthogonal support",
                    correct=True,
                ),
                opt("By keeping only the single weakest source"),
                opt("By averaging without any harmonisation"),
                opt("By ignoring genetics entirely"),
            ),
            "Platforms aggregate harmonised evidence so convergent strands raise confidence.",
        ),
    ),
)
