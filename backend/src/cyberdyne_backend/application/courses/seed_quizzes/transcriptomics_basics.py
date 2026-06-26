"""Quiz questions for the Transcriptomics (RNA-Seq) - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is the transcriptome?": (
            q(
                "What is the transcriptome?",
                (
                    opt(
                        "The complete set of RNA molecules in a sample at a given time",
                        correct=True,
                    ),
                    opt("The complete set of DNA in a cell"),
                    opt("The set of all proteins in a cell"),
                    opt("The set of all metabolites in a cell"),
                ),
                "The transcriptome is the RNA snapshot, and it changes with condition.",
            ),
            q(
                "Which RNA species makes up most of the mass of total RNA?",
                (
                    opt("Ribosomal RNA (rRNA)", correct=True),
                    opt("Messenger RNA (mRNA)"),
                    opt("microRNA (miRNA)"),
                    opt("Transfer RNA only"),
                ),
                "rRNA is ~80-90% of total RNA, so prep must select mRNA or deplete rRNA.",
            ),
            q(
                "Why is the transcriptome described as dynamic compared to the genome?",
                (
                    opt("It changes with cell type, stage, environment and disease", correct=True),
                    opt("Its DNA sequence mutates every minute"),
                    opt("It is identical in every cell at all times"),
                    opt("It contains no information about gene activity"),
                ),
                "The genome is essentially fixed; the transcriptome reflects what is being expressed.",
            ),
        ),
        "From gene to RNA: the central dogma": (
            q(
                "What modification allows oligo-dT capture of mRNA?",
                (
                    opt("The poly(A) tail", correct=True),
                    opt("The 5' cap"),
                    opt("Intron retention"),
                    opt("Histone wrapping"),
                ),
                "Oligo-dT beads hybridize to the poly(A) tail of mature mRNA.",
            ),
            q(
                "Why can a single read be ambiguous about which isoform it came from?",
                (
                    opt("It may map to an exon shared by several isoforms", correct=True),
                    opt("Reads are always longer than a transcript"),
                    opt("Isoforms have identical introns only"),
                    opt("Reads never align to exons"),
                ),
                "Alternative splicing means isoforms share exons, making shared-exon reads ambiguous.",
            ),
            q(
                "Steady-state mRNA level reflects a balance between what two processes?",
                (
                    opt("Synthesis (transcription) and degradation", correct=True),
                    opt("Translation and replication"),
                    opt("Capping and splicing only"),
                    opt("Methylation and acetylation"),
                ),
                "Abundance is set by transcription rate versus decay (half-life).",
            ),
        ),
        "Building an RNA-seq library": (
            q(
                "What does rRNA depletion offer over poly(A) selection?",
                (
                    opt("It retains non-polyadenylated and degraded RNA", correct=True),
                    opt("It captures only intact mRNA"),
                    opt("It removes all mRNA"),
                    opt("It avoids needing reverse transcription"),
                ),
                "rRNA depletion keeps ncRNAs and degraded RNA that poly(A) selection misses.",
            ),
            q(
                "What problem does PCR amplification introduce in library prep?",
                (
                    opt("Duplicate reads and amplification bias", correct=True),
                    opt("Loss of all sequencing adapters"),
                    opt("Conversion of DNA back to RNA"),
                    opt("Complete removal of rRNA"),
                ),
                "PCR enables tiny inputs but creates duplicates and biases.",
            ),
            q(
                "Why does the number of distinct molecules detected saturate with depth?",
                (
                    opt(
                        "Library complexity is finite, so re-sequencing hits the same molecules",
                        correct=True,
                    ),
                    opt("The sequencer stops reading after a fixed time"),
                    opt("Adapters degrade at high depth"),
                    opt("Genes physically merge at high coverage"),
                ),
                "Once most distinct molecules are seen, extra reads mostly re-read duplicates.",
            ),
        ),
        "From reads to a count matrix": (
            q(
                "Why must an RNA-seq read aligner be splice-aware?",
                (
                    opt("Reads can span exon-exon junctions", correct=True),
                    opt("Reads always map to introns"),
                    opt("DNA has no introns to consider"),
                    opt("Splicing only happens after alignment"),
                ),
                "A mature mRNA read may straddle a junction absent from the genome contiguously.",
            ),
            q(
                "What do pseudo-aligners like salmon and kallisto do differently?",
                (
                    opt(
                        "Assign reads to transcripts without base-level alignment, much faster",
                        correct=True,
                    ),
                    opt("Perform slower base-by-base genome alignment"),
                    opt("Skip quantification entirely"),
                    opt("Only work on DNA sequencing data"),
                ),
                "Pseudo-alignment maps reads to compatible transcripts quickly.",
            ),
            q(
                "What are the dimensions of a typical count matrix?",
                (
                    opt("Genes as rows, samples as columns, counts as entries", correct=True),
                    opt("Samples as rows, nucleotides as columns"),
                    opt("Reads as rows, genomes as columns"),
                    opt("Pathways as rows, proteins as columns"),
                ),
                "The count matrix feeds nearly all downstream analysis.",
            ),
        ),
        "Normalization: CPM, TPM and FPKM": (
            q(
                "What does CPM correct for, and what does it miss?",
                (
                    opt("It corrects sequencing depth but not gene length", correct=True),
                    opt("It corrects gene length but not depth"),
                    opt("It corrects both depth and composition fully"),
                    opt("It corrects nothing, equal to raw counts"),
                ),
                "CPM = count x 1e6 / library size; length is not addressed.",
            ),
            q(
                "What property makes TPM the preferred within-sample relative measure?",
                (
                    opt("TPM values sum to the same total in every sample", correct=True),
                    opt("TPM ignores gene length entirely"),
                    opt("TPM equals raw counts"),
                    opt("TPM only works across samples, not within"),
                ),
                "Length-first normalization makes each sample's TPM sum to 1e6.",
            ),
            q(
                "What input do differential expression tools actually use?",
                (
                    opt("Raw counts with their own internal normalization", correct=True),
                    opt("TPM values directly"),
                    opt("FPKM values directly"),
                    opt("Aligned BAM files without counting"),
                ),
                "TPM/CPM are for visualization; DE tools model raw counts.",
            ),
        ),
        "Experimental design and replication": (
            q(
                "What is the dominant source of uncertainty in detecting differential expression?",
                (
                    opt("Biological variability between replicates", correct=True),
                    opt("Sequencer thermal noise"),
                    opt("The choice of FASTQ file name"),
                    opt("The color of the flow cell"),
                ),
                "Biological variation, not sequencing noise, limits DE detection.",
            ),
            q(
                "Why randomize conditions across sequencing lanes and days?",
                (
                    opt("To avoid confounding batch effects with biology", correct=True),
                    opt("To increase total read length"),
                    opt("To remove the need for replicates"),
                    opt("To eliminate gene-length bias"),
                ),
                "Confounded batches make biological and technical effects inseparable.",
            ),
            q(
                "For detecting moderate fold changes, what generally helps most?",
                (
                    opt("More biological replicates", correct=True),
                    opt("More sequencing depth per sample"),
                    opt("Fewer genes in the annotation"),
                    opt("Longer adapter sequences"),
                ),
                "Power rises faster with replicate number than with depth.",
            ),
        ),
    },
    final=(
        q(
            "Which fraction of total RNA is typically information-rich mRNA?",
            (
                opt("About 1-5%", correct=True),
                opt("About 80-90%"),
                opt("About 50%"),
                opt("Essentially 100%"),
            ),
            "rRNA dominates mass; mRNA is only ~1-5%.",
        ),
        q(
            "Which two nuisances does normalization primarily correct?",
            (
                opt("Sequencing depth and gene length", correct=True),
                opt("GC content and read color"),
                opt("Adapter length and lane number"),
                opt("Intron number and exon order"),
            ),
            "Bigger libraries and longer genes catch more reads.",
        ),
        q(
            "Which tools perform fast pseudo-alignment?",
            (
                opt("salmon and kallisto", correct=True),
                opt("FastQC and MultiQC"),
                opt("Bonferroni and BH"),
                opt("WGCNA and GSEA"),
            ),
            "Pseudo-aligners assign reads to transcripts without full alignment.",
        ),
        q(
            "Why is TPM preferred over RPKM for within-sample comparison?",
            (
                opt("TPM values sum to a constant total across samples", correct=True),
                opt("TPM ignores library size"),
                opt("RPKM corrects composition perfectly"),
                opt("TPM uses no normalization at all"),
            ),
            "Length-first normalization gives a consistent per-sample total.",
        ),
        q(
            "What is the recommended minimum kind of replicate for DE?",
            (
                opt("Biological replicates, at least three", correct=True),
                opt("A single technical replicate"),
                opt("No replicates if depth is high"),
                opt("Only pooled samples"),
            ),
            "Biological replicates capture the variability DE must account for.",
        ),
        q(
            "What does a splice-aware aligner handle that a DNA aligner may not?",
            (
                opt("Reads spanning exon-exon junctions", correct=True),
                opt("Reads with sequencing adapters"),
                opt("Reads shorter than 50 bp"),
                opt("Reads from the mitochondrial genome"),
            ),
            "Mature mRNA reads can cross junctions absent from contiguous genome.",
        ),
    ),
)
