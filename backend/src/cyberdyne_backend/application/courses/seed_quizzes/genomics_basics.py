"""Quiz questions for the Genomics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is a genome?": (
            q(
                "What does a genome include?",
                (
                    opt("All of an organism's DNA, coding and non-coding", correct=True),
                    opt("Only the protein-coding genes"),
                    opt("Only the chromosomes, not the mitochondrial DNA"),
                    opt("Only the regulatory elements"),
                ),
                "A genome is the complete set of genetic material, mostly non-coding.",
            ),
            q(
                "Roughly how many protein-coding genes does the human genome contain?",
                (
                    opt("About 20,000", correct=True),
                    opt("About 3 billion"),
                    opt("About 100"),
                    opt("About 2 million"),
                ),
                "~20,000 genes occupy under 2% of the 3.2 Gb human genome.",
            ),
            q(
                "What is the C-value paradox?",
                (
                    opt("Genome size does not correlate with organism complexity", correct=True),
                    opt("Larger genomes always make more proteins"),
                    opt("All genomes are the same size"),
                    opt("GC content equals organism complexity"),
                ),
                "Much of a large genome is repetitive, non-coding DNA.",
            ),
        ),
        "Chromosomes and genome organization": (
            q(
                "What protects the ends of linear eukaryotic chromosomes?",
                (
                    opt("Telomeres", correct=True),
                    opt("Centromeres"),
                    opt("Promoters"),
                    opt("Ribosomes"),
                ),
                "Telomeres are repeat caps (TTAGGG in humans) that shorten with division.",
            ),
            q(
                "What is the basic packaging unit of DNA around histones?",
                (
                    opt("The nucleosome", correct=True),
                    opt("The centromere"),
                    opt("The ribosome"),
                    opt("The plasmid"),
                ),
                "DNA wraps around a histone octamer to form a nucleosome.",
            ),
            q(
                "Which chromatin state is gene-rich and actively transcribed?",
                (
                    opt("Euchromatin", correct=True),
                    opt("Heterochromatin"),
                    opt("Telomeric repeats"),
                    opt("The centromere"),
                ),
                "Euchromatin is open and gene-rich; heterochromatin is condensed and mostly silent.",
            ),
        ),
        "Genes, non-coding DNA and repeats": (
            q(
                "What happens to introns during mRNA maturation?",
                (
                    opt("They are spliced out", correct=True),
                    opt("They are translated into protein"),
                    opt("They become the promoter"),
                    opt("They are kept in the mature mRNA"),
                ),
                "Exons are retained; introns are removed by splicing.",
            ),
            q(
                "Which is an example of an interspersed transposable element?",
                (
                    opt("Alu (a SINE)", correct=True),
                    opt("A telomere"),
                    opt("A centromere"),
                    opt("A ribosome"),
                ),
                "LINEs, SINEs (e.g. Alu) and LTR elements are interspersed repeats.",
            ),
            q(
                "Why do repeats make assembly and alignment difficult?",
                (
                    opt("Identical copies are ambiguous to place", correct=True),
                    opt("They cannot be sequenced at all"),
                    opt("They always contain genes"),
                    opt("They have no DNA bases"),
                ),
                "Multiple near-identical copies create placement ambiguity.",
            ),
        ),
        "Sanger sequencing": (
            q(
                "What causes chain termination in Sanger sequencing?",
                (
                    opt("Incorporation of a ddNTP lacking a 3'-OH", correct=True),
                    opt("Loss of the phosphate backbone"),
                    opt("Addition of an extra primer"),
                    opt("High temperature alone"),
                ),
                "A dideoxynucleotide cannot bond the next base, ending the chain.",
            ),
            q(
                "How are Sanger fragments separated to read the sequence?",
                (
                    opt("By size using capillary electrophoresis", correct=True),
                    opt("By colour only, with no separation"),
                    opt("By mass spectrometry of intact DNA"),
                    opt("By centrifugation of chromosomes"),
                ),
                "Electrophoresis sorts fragments to single-base resolution.",
            ),
            q(
                "A Phred Q score of 30 corresponds to what error probability?",
                (
                    opt("1 in 1000", correct=True),
                    opt("1 in 10"),
                    opt("1 in 2"),
                    opt("1 in 100"),
                ),
                "Q = -10 log10(P), so Q30 means P = 10^-3.",
            ),
        ),
        "Next-generation sequencing": (
            q(
                "What chemistry does Illumina sequencing use?",
                (
                    opt("Sequencing by synthesis with reversible terminators", correct=True),
                    opt("Chain termination with ddNTPs in capillaries"),
                    opt("Measuring ionic current through a pore"),
                    opt("Mass spectrometry of nucleotides"),
                ),
                "Illumina images one reversible-terminator base per cycle.",
            ),
            q(
                "What is a key advantage of long-read platforms (Nanopore, PacBio)?",
                (
                    opt("They span repeats and structural variants", correct=True),
                    opt("They are always cheaper per base than Illumina"),
                    opt("They produce only single bases"),
                    opt("They cannot sequence genomic DNA"),
                ),
                "Long reads resolve repeats and SVs that short reads cannot.",
            ),
            q(
                "How does Illumina amplify fragments before sequencing?",
                (
                    opt("Clonal cluster generation by bridge amplification", correct=True),
                    opt("Capillary electrophoresis"),
                    opt("Threading DNA through a protein pore"),
                    opt("Sanger chain termination"),
                ),
                "Bridge amplification makes clusters of identical fragments on the flow cell.",
            ),
        ),
        "Coverage and read alignment": (
            q(
                "What does sequencing coverage (depth) at a position mean?",
                (
                    opt("How many reads overlap that position", correct=True),
                    opt("The length of a single read"),
                    opt("The number of chromosomes"),
                    opt("The GC content of the genome"),
                ),
                "Lander-Waterman: C = N*L/G, the expected reads per position.",
            ),
            q(
                "Why do short-read aligners use a Burrows-Wheeler Transform / FM-index?",
                (
                    opt("To find seed matches against the reference quickly", correct=True),
                    opt("To call variants directly"),
                    opt("To assemble genomes without a reference"),
                    opt("To translate DNA into protein"),
                ),
                "BWA-MEM and Bowtie2 use the FM-index for fast exact-match seeding.",
            ),
            q(
                "What does a CIGAR string in a BAM file describe?",
                (
                    opt("Matches, insertions and deletions in an alignment", correct=True),
                    opt("The sample's name only"),
                    opt("The Phred quality of the whole genome"),
                    opt("The chromosome count"),
                ),
                "CIGAR encodes how the read aligns: M, I, D operations.",
            ),
        ),
    },
    final=(
        q(
            "Which statement best distinguishes genomics from genetics?",
            (
                opt("Genomics studies the whole genome with high-throughput data", correct=True),
                opt("Genomics studies only one gene at a time"),
                opt("Genetics uses only computers, genomics only wet lab"),
                opt("There is no difference"),
            ),
            "Genomics is genome-wide and computational; genetics focuses on single genes.",
        ),
        q(
            "Which feature attaches the spindle during mitosis?",
            (
                opt("The centromere", correct=True),
                opt("The telomere"),
                opt("The promoter"),
                opt("The 5' UTR"),
            ),
            "Centromeres are the spindle attachment site; telomeres cap the ends.",
        ),
        q(
            "Compared with Sanger, NGS primarily offers:",
            (
                opt("Massively parallel reads at far lower cost per base", correct=True),
                opt("Longer reads than any other method"),
                opt("Perfect zero-error sequencing"),
                opt("No need for a library prep"),
            ),
            "NGS trades read length for huge parallelism and low cost.",
        ),
        q(
            "What does a higher sequencing depth improve?",
            (
                opt("Confidence in base/variant calls by outvoting errors", correct=True),
                opt("The physical length of the genome"),
                opt("The number of chromosomes"),
                opt("The GC content"),
            ),
            "Overlapping reads let random errors be corrected by consensus.",
        ),
        q(
            "Most of the human genome is:",
            (
                opt("Non-coding (regulatory, repeats, ncRNA, introns)", correct=True),
                opt("Protein-coding exons"),
                opt("Mitochondrial DNA"),
                opt("Telomeric repeats only"),
            ),
            "Under 2% codes for protein; the rest is non-coding.",
        ),
        q(
            "A Phred score expresses base quality as:",
            (
                opt("Q = -10 log10(P_error)", correct=True),
                opt("Q = read length / coverage"),
                opt("Q = number of chromosomes"),
                opt("Q = GC content percentage"),
            ),
            "Higher Q means exponentially lower error probability.",
        ),
    ),
)
