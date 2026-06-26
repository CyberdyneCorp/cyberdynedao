"""Quiz questions for the Next-Generation Sequencing Analysis - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Structural variants and copy number": (
            q(
                "Which three short-read signals do SV callers triangulate?",
                (
                    opt("Discordant pairs, split reads, and read-depth changes", correct=True),
                    opt("GC content, adapter, and read name"),
                    opt("MAPQ, FLAG, and CIGAR only"),
                    opt("QUAL, FILTER, and INFO"),
                ),
                "Manta/DELLY combine paired-end, split-read and depth evidence.",
            ),
            q(
                "Why do long reads improve SV detection?",
                (
                    opt("A single read can span an entire SV breakpoint", correct=True),
                    opt("They have zero error"),
                    opt("They are always cheaper"),
                    opt("They cannot align to a reference"),
                ),
                "Spanning the event gives precise breakpoints and high sensitivity.",
            ),
            q(
                "A heterozygous deletion changes normalized read depth to about:",
                (
                    opt("0.5x of the diploid baseline", correct=True),
                    opt("2x of baseline"),
                    opt("Unchanged baseline"),
                    opt("Zero everywhere"),
                ),
                "Losing one copy halves the expected depth over the region.",
            ),
        ),
        "Somatic variant calling and tumor purity": (
            q(
                "How are somatic variants distinguished from germline?",
                (
                    opt("By subtracting a matched normal sample", correct=True),
                    opt("By their Phred+33 encoding"),
                    opt("By read length alone"),
                    opt("By the FASTQ header"),
                ),
                "Mutect2/Strelka2 contrast tumor vs matched normal pileups.",
            ),
            q(
                "For a clonal diploid heterozygous somatic mutation, VAF equals about:",
                (
                    opt("purity / 2", correct=True),
                    opt("purity x 2"),
                    opt("Always 0.5"),
                    opt("Always 1.0"),
                ),
                "VAF scales with tumor purity for a clonal diploid het.",
            ),
            q(
                "Why does somatic / ctDNA calling demand high depth?",
                (
                    opt("Subclonal and low-purity variants have very low VAF", correct=True),
                    opt("Tumors have no mutations"),
                    opt("Depth has no effect on sensitivity"),
                    opt("Germline het VAF is hard to detect"),
                ),
                "Low-VAF variants need deep coverage (and UMIs for ctDNA) to detect.",
            ),
        ),
        "Deep learning and pangenome references": (
            q(
                "How does DeepVariant call genotypes?",
                (
                    opt(
                        "By rendering the pileup as a tensor and classifying with a CNN",
                        correct=True,
                    ),
                    opt("With a fixed QUAL cutoff"),
                    opt("By Sanger chain termination"),
                    opt("By counting chromosomes"),
                ),
                "DeepVariant treats calling as CNN image classification.",
            ),
            q(
                "What problem does a pangenome graph reference reduce?",
                (
                    opt("Reference bias against non-reference alleles", correct=True),
                    opt("The need for any alignment"),
                    opt("Sequencing error in raw reads"),
                    opt("The size of the FASTQ file"),
                ),
                "Encoding many haplotypes lets reads align to the closest path.",
            ),
            q(
                "Which tool aligns reads to a pangenome graph?",
                (
                    opt("vg giraffe", correct=True),
                    opt("FastQC"),
                    opt("Trimmomatic"),
                    opt("tabix"),
                ),
                "vg giraffe maps reads onto a variation graph.",
            ),
        ),
        "Reproducible NGS pipelines": (
            q(
                "How do Nextflow and Snakemake model a pipeline?",
                (
                    opt("As a directed acyclic graph of tasks with declared I/O", correct=True),
                    opt("As a single monolithic shell script"),
                    opt("As a VCF file"),
                    opt("As a CNN"),
                ),
                "A DAG lets the engine parallelize, cache and resume steps.",
            ),
            q(
                "What pins exact tool versions for reproducibility?",
                (
                    opt("Containers (Docker/Singularity) or conda environments", correct=True),
                    opt("Larger read length"),
                    opt("A higher Phred score"),
                    opt("More chromosomes"),
                ),
                "Containers/conda fix every dependency version.",
            ),
            q(
                "What does the nf-core project provide?",
                (
                    opt("Community-curated, peer-reviewed Nextflow pipelines", correct=True),
                    opt("A new sequencing chemistry"),
                    opt("A replacement for VCF"),
                    opt("A truth set for benchmarking"),
                ),
                "nf-core/sarek and nf-core/rnaseq bake in best practices.",
            ),
        ),
        "Benchmarking and best practices": (
            q(
                "What does the Genome in a Bottle (GIAB) project provide?",
                (
                    opt("Reference samples with high-confidence truth VCF and BED", correct=True),
                    opt("A new aligner"),
                    opt("A cloud workflow engine"),
                    opt("A library prep kit"),
                ),
                "GIAB (e.g. HG002) gives a truth set for evaluating callers.",
            ),
            q(
                "Why use haplotype-aware comparison (hap.py / vcfeval)?",
                (
                    opt(
                        "Equivalent representations of the same variant are not counted as errors",
                        correct=True,
                    ),
                    opt("It speeds up alignment"),
                    opt("It removes adapters"),
                    opt("It increases coverage"),
                ),
                "Indels can be written several ways; haplotype matching avoids false errors.",
            ),
            q(
                "The F1 score for variant calls is:",
                (
                    opt("The harmonic mean of precision and recall", correct=True),
                    opt("The product of depth and read length"),
                    opt("The mean Phred score"),
                    opt("The number of true positives"),
                ),
                "F1 = 2*P*R/(P+R), high only when both precision and recall are high.",
            ),
        ),
    },
    final=(
        q(
            "Which class of variant is hardest to call from short reads?",
            (
                opt("Large structural variants spanning breakpoints", correct=True),
                opt("Single-nucleotide variants"),
                opt("Short indels in unique regions"),
                opt("Synonymous SNVs"),
            ),
            "A 150 bp read rarely spans an SV breakpoint.",
        ),
        q(
            "A somatic variant's allele fraction depends primarily on:",
            (
                opt("Tumor purity, copy number and clonality", correct=True),
                opt("The FASTQ line count"),
                opt("The adapter sequence"),
                opt("The reference file name"),
            ),
            "VAF reflects purity, ploidy and subclonal structure.",
        ),
        q(
            "DeepVariant's key idea is to:",
            (
                opt("Classify pileup images of each site with a CNN", correct=True),
                opt("Use only a fixed QUAL threshold"),
                opt("Skip the reference genome"),
                opt("Sequence by chain termination"),
            ),
            "It reframes calling as image classification.",
        ),
        q(
            "A pangenome graph reference mainly improves:",
            (
                opt("Recall in diverse/variable regions by cutting reference bias", correct=True),
                opt("FASTQ compression"),
                opt("Adapter trimming"),
                opt("Flow-cell loading"),
            ),
            "Multiple haplotypes reduce bias against non-reference alleles.",
        ),
        q(
            "Why use a workflow manager like Nextflow for NGS?",
            (
                opt("Reproducible, parallel, resumable, portable pipelines", correct=True),
                opt("To increase per-base quality"),
                opt("To lengthen reads"),
                opt("To replace the VCF format"),
            ),
            "A DAG plus containers makes runs deterministic and scalable.",
        ),
        q(
            "Which metrics should a caller benchmark report?",
            (
                opt("Recall, precision and F1, broken out by variant type", correct=True),
                opt("Only the total read count"),
                opt("Only GC content"),
                opt("Only the genome size"),
            ),
            "Report sensitivity, precision and F1 for SNVs and indels separately.",
        ),
    ),
)
