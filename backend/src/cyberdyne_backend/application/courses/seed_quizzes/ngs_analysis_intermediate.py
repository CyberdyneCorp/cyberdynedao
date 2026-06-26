"""Quiz questions for the Next-Generation Sequencing Analysis - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Read alignment and the SAM/BAM format": (
            q(
                "Why do short-read aligners use a BWT / FM-index?",
                (
                    opt("To find exact-match seeds against the reference quickly", correct=True),
                    opt("To call variants directly"),
                    opt("To translate DNA into protein"),
                    opt("To compress the FASTQ file"),
                ),
                "BWA-MEM and Bowtie2 seed with the FM-index, then extend.",
            ),
            q(
                "What does a CIGAR string encode?",
                (
                    opt("Matches, insertions, deletions and clips in the alignment", correct=True),
                    opt("The sample name"),
                    opt("The genome size"),
                    opt("The Phred quality of the read only"),
                ),
                "CIGAR uses M, I, D, S operations to describe the alignment.",
            ),
            q(
                "MAPQ in a BAM record measures:",
                (
                    opt("Confidence that the read is placed at the right locus", correct=True),
                    opt("The per-base sequencing quality"),
                    opt("The number of duplicates"),
                    opt("The insert size"),
                ),
                "MAPQ is the Phred-scaled probability of mis-mapping.",
            ),
        ),
        "Alignment cleanup: duplicates and recalibration": (
            q(
                "Why are PCR/optical duplicates marked before calling?",
                (
                    opt("They are not independent evidence and inflate confidence", correct=True),
                    opt("They contain the only real variants"),
                    opt("They improve coverage uniformity"),
                    opt("They must be translated"),
                ),
                "Duplicates share a fragment, so they are flagged and excluded.",
            ),
            q(
                "What does Base Quality Score Recalibration (BQSR) fix?",
                (
                    opt("Systematically miscalibrated reported Phred scores", correct=True),
                    opt("The chromosome count"),
                    opt("The reference genome version"),
                    opt("The adapter sequence"),
                ),
                "BQSR re-estimates quality from empirical error at non-variant sites.",
            ),
            q(
                "BQSR builds its error model using which resource?",
                (
                    opt("A known-variant mask (e.g. dbSNP) to ignore true variants", correct=True),
                    opt("The FASTQ identifiers only"),
                    opt("The CIGAR strings alone"),
                    opt("A random subset of bases with no mask"),
                ),
                "Masking known sites lets remaining mismatches estimate the error rate.",
            ),
        ),
        "Variant calling and genotype likelihoods": (
            q(
                "What does a genotype likelihood P(reads | G) represent?",
                (
                    opt("How well genotype G explains the observed read bases", correct=True),
                    opt("The depth of coverage"),
                    opt("The length of the read"),
                    opt("The GC content"),
                ),
                "Callers score each candidate genotype against the pileup.",
            ),
            q(
                "What advance do HaplotypeCaller and DeepVariant share?",
                (
                    opt(
                        "Local reassembly of active regions into candidate haplotypes", correct=True
                    ),
                    opt("They skip alignment entirely"),
                    opt("They only call from Sanger traces"),
                    opt("They ignore base qualities"),
                ),
                "Local reassembly fixes alignment artifacts, especially around indels.",
            ),
            q(
                "Expected allele balance at a true heterozygous site is about:",
                (
                    opt("0.5", correct=True),
                    opt("0.0"),
                    opt("1.0"),
                    opt("0.1"),
                ),
                "A het carries each allele on ~half its reads.",
            ),
        ),
        "The VCF format": (
            q(
                "Which are the eight fixed VCF columns?",
                (
                    opt("CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO", correct=True),
                    opt("NAME, FLAG, POS, MAPQ, CIGAR, SEQ, QUAL, TAG"),
                    opt("CHROM, START, END, STRAND, NAME, SCORE, GENE, EXON"),
                    opt("READ, R1, R2, GC, DUP, ADAPTER, LEN, Q"),
                ),
                "Those eight precede FORMAT and per-sample columns.",
            ),
            q(
                "In the per-sample FORMAT fields, what does GT hold?",
                (
                    opt("The genotype, e.g. 0/1", correct=True),
                    opt("The total depth"),
                    opt("The allele frequency"),
                    opt("The mapping quality"),
                ),
                "GT is the called genotype; DP/AD/GQ/PL carry the rest.",
            ),
            q(
                "What does a gVCF add over a plain VCF?",
                (
                    opt(
                        "Confidence records for non-variant blocks for joint genotyping",
                        correct=True,
                    ),
                    opt("Only the header lines"),
                    opt("Raw FASTQ reads"),
                    opt("The reference FASTA"),
                ),
                "gVCF stores reference-confidence so cohorts can be jointly genotyped.",
            ),
        ),
        "Variant filtering": (
            q(
                "Hard filtering of variants works by:",
                (
                    opt(
                        "Applying fixed thresholds on INFO annotations (QD, FS, MQ...)",
                        correct=True,
                    ),
                    opt("Training a neural network per sample"),
                    opt("Re-aligning every read"),
                    opt("Removing the header"),
                ),
                "Hard filters use simple cutoffs; good for small cohorts.",
            ),
            q(
                "What does VQSR produce for each variant?",
                (
                    opt("A VQSLOD log-odds of being a true variant", correct=True),
                    opt("A new CIGAR string"),
                    opt("A raw Phred base quality"),
                    opt("An adapter match score"),
                ),
                "VQSR fits a Gaussian mixture to known true sites and scores calls.",
            ),
            q(
                "In the VCF FILTER column, what does PASS mean?",
                (
                    opt("The variant passed all applied filters", correct=True),
                    opt("The variant failed every filter"),
                    opt("The site was not tested"),
                    opt("The read was a duplicate"),
                ),
                "PASS is the keep flag; other values name the failed filter.",
            ),
        ),
        "Variant annotation": (
            q(
                "Which tool predicts a variant's functional consequence?",
                (
                    opt("VEP (Ensembl) or SnpEff", correct=True),
                    opt("samtools sort"),
                    opt("FastQC"),
                    opt("bridge amplification"),
                ),
                "VEP, SnpEff and ANNOVAR annotate consequence and databases.",
            ),
            q(
                "Which database gives population allele frequencies for prioritization?",
                (
                    opt("gnomAD", correct=True),
                    opt("GIAB truth set"),
                    opt("The CIGAR table"),
                    opt("The flow-cell manifest"),
                ),
                "gnomAD frequencies help flag rare vs common variants.",
            ),
            q(
                "A high-priority candidate variant is typically:",
                (
                    opt(
                        "Rare, protein-truncating, in a relevant gene, high impact score",
                        correct=True,
                    ),
                    opt("Common and synonymous"),
                    opt("Outside any gene and benign"),
                    opt("Present in every sample equally"),
                ),
                "Rarity plus predicted damage in a disease gene drives prioritization.",
            ),
        ),
    },
    final=(
        q(
            "What output format does an aligner like BWA-MEM produce?",
            (
                opt("SAM/BAM alignments", correct=True),
                opt("A VCF of variants"),
                opt("A FASTQ of raw reads"),
                opt("A FASTA reference"),
            ),
            "Alignment yields SAM (text) or compressed BAM.",
        ),
        q(
            "Which two cleanup steps precede GATK variant calling?",
            (
                opt("Duplicate marking and base quality recalibration", correct=True),
                opt("Adapter trimming and FastQC"),
                opt("Annotation and prioritization"),
                opt("Assembly and scaffolding"),
            ),
            "MarkDuplicates then BQSR produce an analysis-ready BAM.",
        ),
        q(
            "A genotype likelihood compares candidate genotypes by:",
            (
                opt("How well each explains the read bases and their qualities", correct=True),
                opt("The number of chromosomes"),
                opt("The adapter content"),
                opt("The file size of the BAM"),
            ),
            "P(reads|G) scores 0/0, 0/1, 1/1 against the pileup.",
        ),
        q(
            "In a VCF, the GT:DP:AD:GQ:PL fields belong to which part?",
            (
                opt("The per-sample columns under FORMAT", correct=True),
                opt("The ## header only"),
                opt("The CHROM field"),
                opt("The INFO field exclusively"),
            ),
            "FORMAT defines keys; each sample column supplies their values.",
        ),
        q(
            "VQSR differs from hard filtering because it:",
            (
                opt("Learns the annotation distribution of known true variants", correct=True),
                opt("Uses a single fixed QUAL cutoff"),
                opt("Ignores all annotations"),
                opt("Requires no truth data at all"),
            ),
            "VQSR is model-based (Gaussian mixture); hard filters are fixed cutoffs.",
        ),
        q(
            "Annotation tools like VEP attach which of the following?",
            (
                opt("Consequence, population frequency and deleteriousness scores", correct=True),
                opt("New CIGAR strings"),
                opt("Raw flow-cell images"),
                opt("Adapter sequences"),
            ),
            "Annotation adds biological/clinical meaning to a call.",
        ),
    ),
)
