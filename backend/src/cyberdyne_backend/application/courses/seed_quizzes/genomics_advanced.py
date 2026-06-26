"""Quiz questions for the Genomics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Comparative and evolutionary genomics": (
            q(
                "What distinguishes orthologs from paralogs?",
                (
                    opt("Orthologs split by speciation; paralogs by duplication", correct=True),
                    opt("Orthologs are always non-coding"),
                    opt("Paralogs occur only across species"),
                    opt("They are identical concepts"),
                ),
                "Phylogeny separates speciation (ortholog) from duplication (paralog).",
            ),
            q(
                "A dN/dS (omega) value greater than 1 indicates:",
                (
                    opt("Positive (diversifying) selection", correct=True),
                    opt("Purifying selection"),
                    opt("Neutral evolution"),
                    opt("No substitutions at all"),
                ),
                "omega < 1 purifying, = 1 neutral, > 1 positive selection.",
            ),
            q(
                "What does conserved synteny across genomes reveal?",
                (
                    opt("Preserved gene order, plus rearrangements where broken", correct=True),
                    opt("The GC content only"),
                    opt("The sequencing depth"),
                    opt("The Phred quality"),
                ),
                "Whole-genome alignment exposes synteny and rearrangements.",
            ),
        ),
        "Functional genomics: RNA-seq and ATAC-seq": (
            q(
                "Why do RNA-seq differential-expression tools use the negative binomial?",
                (
                    opt("To model overdispersion beyond a Poisson", correct=True),
                    opt("Because counts are always Gaussian"),
                    opt("To align reads to the genome"),
                    opt("To mask repeats"),
                ),
                "Biological variance exceeds Poisson; NB adds a dispersion term.",
            ),
            q(
                "What does ATAC-seq measure?",
                (
                    opt("Open (accessible) chromatin via Tn5 transposase", correct=True),
                    opt("Total RNA abundance"),
                    opt("Protein 3D structure"),
                    opt("DNA methylation only"),
                ),
                "Tn5 inserts adapters into accessible DNA, marking active regions.",
            ),
            q(
                "Which tool is commonly used to call peaks from ATAC/ChIP data?",
                (
                    opt("MACS2", correct=True),
                    opt("DESeq2"),
                    opt("BWA-MEM"),
                    opt("AUGUSTUS"),
                ),
                "MACS2 identifies enriched peaks; DESeq2 is for expression.",
            ),
        ),
        "Single-cell and spatial genomics": (
            q(
                "What is the role of a UMI in single-cell RNA-seq?",
                (
                    opt("Tag each transcript to remove PCR duplicates", correct=True),
                    opt("Identify the chromosome"),
                    opt("Replace the reference genome"),
                    opt("Call structural variants"),
                ),
                "Unique molecular identifiers count original molecules, not PCR copies.",
            ),
            q(
                "Which dimensionality-reduction step is standard before clustering cells?",
                (
                    opt("PCA followed by UMAP", correct=True),
                    opt("Smith-Waterman alignment"),
                    opt("Bonferroni correction"),
                    opt("Repeat masking"),
                ),
                "Counts are normalized, then PCA -> UMAP precedes clustering.",
            ),
            q(
                "What does spatial transcriptomics add over standard scRNA-seq?",
                (
                    opt("Physical tissue coordinates for expression", correct=True),
                    opt("Longer sequencing reads"),
                    opt("Higher Phred scores"),
                    opt("Removal of all noise"),
                ),
                "Spatial methods map expression back onto tissue architecture.",
            ),
        ),
        "Pangenomes and graph references": (
            q(
                "What problem does a graph genome reduce relative to a single linear reference?",
                (
                    opt("Reference bias against non-reference alleles", correct=True),
                    opt("The need to sequence at all"),
                    opt("The existence of genes"),
                    opt("The Phred score"),
                ),
                "Graphs encode alternative alleles as parallel paths, cutting bias.",
            ),
            q(
                "In a pangenome, the core genome is:",
                (
                    opt("The set of genes shared by all individuals", correct=True),
                    opt("Genes present in only one individual"),
                    opt("All repeats in the genome"),
                    opt("The mitochondrial DNA only"),
                ),
                "Core = shared by all; accessory = present in only some.",
            ),
            q(
                "How does a sequence graph represent an alternative allele?",
                (
                    opt("As a parallel path (bubble) between shared nodes", correct=True),
                    opt("As a deleted chromosome"),
                    opt("As a higher Phred score"),
                    opt("As a separate FASTQ file"),
                ),
                "vg-style graphs branch into bubbles at variable sites.",
            ),
        ),
        "Clinical genomics": (
            q(
                "Which framework classifies germline variant pathogenicity in the clinic?",
                (
                    opt("ACMG/AMP criteria", correct=True),
                    opt("The N50 standard"),
                    opt("The BLOSUM matrix"),
                    opt("The CIGAR convention"),
                ),
                "ACMG/AMP grades variants from pathogenic to benign.",
            ),
            q(
                "Why is matched normal tissue used in somatic (cancer) variant calling?",
                (
                    opt(
                        "To separate tumor-specific mutations from germline variants", correct=True
                    ),
                    opt("To increase read length"),
                    opt("To mask repeats"),
                    opt("To compute N50"),
                ),
                "Tumor-vs-normal subtraction isolates somatic drivers.",
            ),
            q(
                "What does a rare population frequency contribute to variant interpretation?",
                (
                    opt("It raises the prior that the variant is pathogenic", correct=True),
                    opt("It proves the variant is benign"),
                    opt("It has no role"),
                    opt("It sets the sequencing depth"),
                ),
                "Rarity (low gnomAD frequency) is supporting pathogenic evidence.",
            ),
        ),
        "Deep learning in genomics": (
            q(
                "What does Enformer predict from DNA sequence?",
                (
                    opt("Gene expression with long-range regulatory effects", correct=True),
                    opt("Only the GC content"),
                    opt("The Phred quality"),
                    opt("The N50 of an assembly"),
                ),
                "Enformer is a transformer with a wide receptive field over ~100 kb.",
            ),
            q(
                "What problem did AlphaFold address?",
                (
                    opt("Predicting protein 3D structure from sequence", correct=True),
                    opt("Calling SNPs from BAM files"),
                    opt("Assembling genomes from reads"),
                    opt("Masking repeats"),
                ),
                "AlphaFold predicts structure at near-experimental accuracy.",
            ),
            q(
                "What does SpliceAI predict?",
                (
                    opt("Whether a variant disrupts splice sites", correct=True),
                    opt("The chromosome number"),
                    opt("Read mapping quality"),
                    opt("The sequencing cost"),
                ),
                "SpliceAI flags splicing-disrupting variants.",
            ),
        ),
    },
    final=(
        q(
            "A dN/dS ratio well below 1 indicates a gene is under:",
            (
                opt("Purifying (negative) selection / strong constraint", correct=True),
                opt("Positive selection"),
                opt("No selection"),
                opt("Reference bias"),
            ),
            "Fewer non-synonymous changes than synonymous implies constraint.",
        ),
        q(
            "DESeq2 and edgeR are used for:",
            (
                opt("Differential gene expression from RNA-seq counts", correct=True),
                opt("Genome assembly"),
                opt("Variant calling"),
                opt("Protein structure prediction"),
            ),
            "Both use negative-binomial models for expression testing.",
        ),
        q(
            "Single-cell RNA-seq matrices are characteristically:",
            (
                opt("Sparse, with many zero entries (dropout)", correct=True),
                opt("Completely dense"),
                opt("Always perfectly balanced"),
                opt("Free of technical noise"),
            ),
            "Limited capture per cell leaves most entries zero.",
        ),
        q(
            "An 'open' pangenome means that as genomes are added:",
            (
                opt("New gene families keep appearing (union grows)", correct=True),
                opt("The total gene set stops changing immediately"),
                opt("The core genome grows without bound"),
                opt("All genomes become identical"),
            ),
            "The pangenome grows while the core shrinks toward a plateau.",
        ),
        q(
            "In clinical genomics, gnomAD is primarily used to provide:",
            (
                opt("Population allele frequencies for variant interpretation", correct=True),
                opt("Protein 3D structures"),
                opt("RNA-seq counts"),
                opt("Assembly N50 values"),
            ),
            "gnomAD frequencies inform ACMG classification.",
        ),
        q(
            "Which deep-learning model scores missense variant pathogenicity?",
            (
                opt("AlphaMissense", correct=True),
                opt("MACS2"),
                opt("BWA-MEM"),
                opt("SPAdes"),
            ),
            "AlphaMissense predicts pathogenicity of missense substitutions.",
        ),
    ),
)
