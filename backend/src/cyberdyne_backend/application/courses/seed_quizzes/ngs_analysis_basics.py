"""Quiz questions for the Next-Generation Sequencing Analysis - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "From DNA to reads: sequencing technologies": (
            q(
                "How does Illumina amplify fragments before sequencing?",
                (
                    opt("Clonal cluster generation by bridge amplification", correct=True),
                    opt("Threading single strands through a protein pore"),
                    opt("Circularizing and reading a fragment many times"),
                    opt("Capillary electrophoresis of labeled fragments"),
                ),
                "Illumina forms clonal clusters on a flow cell, then sequences by synthesis.",
            ),
            q(
                "What does Oxford Nanopore physically measure?",
                (
                    opt("Ionic current as a strand passes through a pore", correct=True),
                    opt("Fluorescence of reversible-terminator bases"),
                    opt("Mass of each released nucleotide"),
                    opt("Migration distance in a gel"),
                ),
                "Nanopore reads disruptions in ionic current to infer the sequence.",
            ),
            q(
                "Which platform gives long AND highly accurate reads via circular consensus?",
                (
                    opt("PacBio HiFi", correct=True),
                    opt("Illumina NovaSeq"),
                    opt("Sanger capillary"),
                    opt("Early Nanopore R7"),
                ),
                "PacBio HiFi reads a circularized fragment repeatedly for high accuracy.",
            ),
        ),
        "FASTQ and Phred quality scores": (
            q(
                "How many lines describe one read in a FASTQ file?",
                (
                    opt("Four: identifier, sequence, separator, quality", correct=True),
                    opt("Two: identifier and sequence"),
                    opt("One tab-delimited line"),
                    opt("Eight fixed columns"),
                ),
                "FASTQ stores each read as @id, sequence, +, and a quality string.",
            ),
            q(
                "A Phred Q30 base corresponds to what error probability?",
                (
                    opt("1 in 1000", correct=True),
                    opt("1 in 100"),
                    opt("1 in 10"),
                    opt("1 in 30"),
                ),
                "Q = -10 log10(P), so Q30 means P = 10^-3.",
            ),
            q(
                "What does the Phred+33 encoding mean?",
                (
                    opt("Subtract 33 from the ASCII value to get Q", correct=True),
                    opt("Add 33 to the read length"),
                    opt("Multiply the base count by 33"),
                    opt("The genome is offset by 33 bp"),
                ),
                "Each quality character's ASCII value minus 33 gives the Phred score.",
            ),
        ),
        "Read quality control": (
            q(
                "Which tool is the standard first-pass QC report for a FASTQ file?",
                (
                    opt("FastQC", correct=True),
                    opt("BWA-MEM"),
                    opt("GATK HaplotypeCaller"),
                    opt("samtools sort"),
                ),
                "FastQC summarizes per-base quality, GC, adapters and duplication.",
            ),
            q(
                "Where does per-base quality typically fall on an Illumina read?",
                (
                    opt("Toward the 3' end as cycles accumulate", correct=True),
                    opt("Only at the very first base"),
                    opt("Uniformly across all positions"),
                    opt("It rises along the read"),
                ),
                "Signal decay and phasing degrade quality at the 3' end.",
            ),
            q(
                "What does MultiQC add over FastQC?",
                (
                    opt("It aggregates many samples into one combined report", correct=True),
                    opt("It calls variants from the reads"),
                    opt("It aligns reads to a reference"),
                    opt("It synthesizes new DNA"),
                ),
                "MultiQC merges per-sample reports into a single overview.",
            ),
        ),
        "Trimming and filtering reads": (
            q(
                "Which is a common read-trimming/adapter-removal tool?",
                (
                    opt("fastp", correct=True),
                    opt("samtools"),
                    opt("bcftools"),
                    opt("VEP"),
                ),
                "fastp, Trimmomatic and cutadapt trim adapters and low-quality bases.",
            ),
            q(
                "How does sliding-window quality trimming decide where to cut?",
                (
                    opt("It cuts when a window's mean Phred drops below a threshold", correct=True),
                    opt("It removes every other base"),
                    opt("It trims a fixed 50% of every read"),
                    opt("It deletes reads with any mismatch"),
                ),
                "A window is scanned and trimmed once its mean quality falls too low.",
            ),
            q(
                "Why keep R1 and R2 synchronized when trimming paired-end data?",
                (
                    opt("Dropping one mate leaves an orphan that breaks pairing", correct=True),
                    opt("Because R2 is always discarded"),
                    opt("To double the read length"),
                    opt("Pairing is irrelevant after trimming"),
                ),
                "Aligners expect matched pairs; lone mates must be handled separately.",
            ),
        ),
        "Coverage and sequencing depth": (
            q(
                "What does the Lander-Waterman formula C = N*L/G give?",
                (
                    opt("Expected average coverage depth", correct=True),
                    opt("The number of chromosomes"),
                    opt("The Phred score of a base"),
                    opt("The adapter sequence length"),
                ),
                "C is mean depth from N reads of length L over a genome of size G.",
            ),
            q(
                "Under a Poisson model, what is the chance a base gets zero reads?",
                (
                    opt("exp(-C), where C is mean depth", correct=True),
                    opt("1 - C"),
                    opt("C squared"),
                    opt("Always zero above 1x"),
                ),
                "P(0 reads) = e^-C, falling fast as depth rises.",
            ),
            q(
                "Why does higher depth improve variant calling?",
                (
                    opt("Random errors are outvoted by consensus across reads", correct=True),
                    opt("It lengthens each individual read"),
                    opt("It removes the need for a reference"),
                    opt("It changes the genome size"),
                ),
                "More overlapping reads give independent evidence per site.",
            ),
        ),
        "Short reads vs long reads": (
            q(
                "For what task are short Illumina reads especially well suited?",
                (
                    opt("Accurate SNV/indel calling and expression counting", correct=True),
                    opt("Spanning long repeats in one read"),
                    opt("Reading base modifications directly"),
                    opt("Resolving large inversions alone"),
                ),
                "Short reads are cheap and accurate for reference-mappable tasks.",
            ),
            q(
                "What is a key strength of long reads?",
                (
                    opt("Spanning repeats and resolving structural variants", correct=True),
                    opt("Lowest possible cost per gigabase"),
                    opt("Zero sequencing error"),
                    opt("Inability to phase haplotypes"),
                ),
                "Long reads span repeats, resolve SVs, phase and enable assembly.",
            ),
            q(
                "What does a hybrid sequencing strategy do?",
                (
                    opt(
                        "Uses long reads for scaffold/SVs and short reads to polish accuracy",
                        correct=True,
                    ),
                    opt("Uses only Sanger sequencing"),
                    opt("Avoids alignment entirely"),
                    opt("Sequences without any library prep"),
                ),
                "Long reads provide structure; short reads correct base errors.",
            ),
        ),
    },
    final=(
        q(
            "Which chemistry describes Illumina sequencing?",
            (
                opt("Sequencing-by-synthesis with reversible terminators", correct=True),
                opt("Ionic current through a nanopore"),
                opt("Chain termination with ddNTPs"),
                opt("Mass spectrometry of nucleotides"),
            ),
            "Illumina images one reversible-terminator base per cycle.",
        ),
        q(
            "A Phred score of 20 means the error probability is:",
            (
                opt("1 in 100", correct=True),
                opt("1 in 1000"),
                opt("1 in 10"),
                opt("1 in 20"),
            ),
            "Q20 -> P = 10^-2 = 0.01.",
        ),
        q(
            "What is the main purpose of read QC with FastQC/MultiQC?",
            (
                opt("Assess read quality before downstream analysis", correct=True),
                opt("Call variants directly"),
                opt("Assemble the genome"),
                opt("Annotate gene function"),
            ),
            "QC inspects quality, adapters, GC and duplication up front.",
        ),
        q(
            "Coverage (depth) at a position is:",
            (
                opt("The number of reads overlapping that position", correct=True),
                opt("The length of a single read"),
                opt("The GC content of the genome"),
                opt("The number of chromosomes"),
            ),
            "Depth is how many reads cover a given base.",
        ),
        q(
            "Which platform best resolves large structural variants and repeats?",
            (
                opt("Long-read (PacBio / Nanopore)", correct=True),
                opt("Short-read Illumina alone"),
                opt("Sanger capillary"),
                opt("None can detect SVs"),
            ),
            "Long reads can span breakpoints and repeats that short reads cannot.",
        ),
        q(
            "Why trim reads before alignment?",
            (
                opt("Remove adapters and low-quality bases that hurt mapping", correct=True),
                opt("To increase the genome size"),
                opt("To convert FASTQ into BAM"),
                opt("To add new sequence to reads"),
            ),
            "Trimming cleans contaminating adapters and poor 3' bases.",
        ),
    ),
)
