"""Quiz questions for the Introduction to Bioinformatics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is bioinformatics and why it exists": (
            q(
                "Bioinformatics is best described as the science of what?",
                (
                    opt(
                        "Storing, searching and analysing biological data with computers",
                        correct=True,
                    ),
                    opt("Breeding organisms for desirable traits"),
                    opt("Designing laboratory glassware"),
                    opt("Manufacturing pharmaceutical drugs"),
                ),
                "It applies computation and statistics to biological data.",
            ),
            q(
                "Which three fields most directly intersect in bioinformatics?",
                (
                    opt("Biology, computer science and statistics", correct=True),
                    opt("Chemistry, geology and astronomy"),
                    opt("Economics, law and history"),
                    opt("Mechanical, civil and electrical engineering"),
                ),
                "It sits at the intersection of biology, computing and statistics.",
            ),
            q(
                "Why has computation become the bottleneck in modern biology?",
                (
                    opt(
                        "Sequencing cost fell faster than computing cost, so data volume exploded",
                        correct=True,
                    ),
                    opt("Microscopes stopped improving"),
                    opt("Biologists stopped collecting data"),
                    opt("Computers became slower over time"),
                ),
                "Cost per genome dropped faster than Moore's law, creating a data deluge.",
            ),
        ),
        "Biological sequences: DNA, RNA and protein": (
            q(
                "Which alphabet does DNA use?",
                (
                    opt("A, C, G, T", correct=True),
                    opt("A, C, G, U"),
                    opt("20 amino-acid letters"),
                    opt("0 and 1"),
                ),
                "DNA uses A, C, G, T; RNA replaces T with U; protein uses 20 amino acids.",
            ),
            q(
                "The central dogma describes information flow in which order?",
                (
                    opt("DNA to RNA to protein", correct=True),
                    opt("Protein to RNA to DNA"),
                    opt("RNA to protein to DNA"),
                    opt("Protein to DNA to RNA"),
                ),
                "DNA is transcribed to mRNA, which is translated to protein.",
            ),
            q(
                "How many distinct DNA k-mers of length k exist?",
                (
                    opt("4^k", correct=True),
                    opt("k^4"),
                    opt("4*k"),
                    opt("2^k"),
                ),
                "With a 4-letter alphabet there are 4^k possible k-mers.",
            ),
        ),
        "The central computational problems": (
            q(
                "Reconstructing a genome from many short overlapping reads is called what?",
                (
                    opt("Assembly", correct=True),
                    opt("Annotation"),
                    opt("Translation"),
                    opt("Bootstrapping"),
                ),
                "Assembly stitches reads back into the original sequence.",
            ),
            q(
                "Labelling a genome with genes and regulatory features is called what?",
                (
                    opt("Annotation", correct=True),
                    opt("Alignment"),
                    opt("Assembly"),
                    opt("Replication"),
                ),
                "Annotation assigns biological meaning to genomic positions.",
            ),
            q(
                "A naive all-against-all comparison of n sequences scales roughly as what?",
                (
                    opt("n^2", correct=True),
                    opt("log n"),
                    opt("n"),
                    opt("constant time"),
                ),
                "Pairwise comparison of n items is about n(n-1)/2, i.e. order n^2.",
            ),
        ),
        "File formats: FASTA, FASTQ and beyond": (
            q(
                "What does FASTQ add compared with FASTA?",
                (
                    opt("Per-base quality scores", correct=True),
                    opt("3D structure coordinates"),
                    opt("Phylogenetic trees"),
                    opt("Gene ontology terms"),
                ),
                "FASTQ stores reads plus a Phred quality line.",
            ),
            q(
                "A Phred quality score of Q=30 corresponds to what error probability?",
                (
                    opt("0.001 (0.1%)", correct=True),
                    opt("0.5 (50%)"),
                    opt("0.1 (10%)"),
                    opt("0.0 (never wrong)"),
                ),
                "Q = -10 log10(P), so Q=30 means P=10^-3 = 0.1%.",
            ),
            q(
                "Which format stores called genetic variants?",
                (
                    opt("VCF", correct=True),
                    opt("FASTA"),
                    opt("PDB"),
                    opt("FASTQ"),
                ),
                "VCF (Variant Call Format) records variants; BAM stores alignments.",
            ),
        ),
        "Biological databases and resources": (
            q(
                "Which database stores experimentally determined 3D protein structures?",
                (
                    opt("PDB", correct=True),
                    opt("UniProt"),
                    opt("SRA"),
                    opt("GenBank"),
                ),
                "The Protein Data Bank (PDB) holds 3D structures.",
            ),
            q(
                "Which resource holds raw sequencing reads from experiments?",
                (
                    opt("SRA", correct=True),
                    opt("PDB"),
                    opt("RefSeq"),
                    opt("Pfam"),
                ),
                "The Sequence Read Archive (SRA) stores raw reads.",
            ),
            q(
                "RefSeq is best described as which kind of resource?",
                (
                    opt("Curated, non-redundant reference sequences", correct=True),
                    opt("A 3D structure archive"),
                    opt("A raw-reads archive"),
                    opt("A literature database"),
                ),
                "RefSeq provides curated reference sequences derived from GenBank.",
            ),
        ),
    },
    final=(
        q(
            "What is the core aim of bioinformatics?",
            (
                opt("Apply computation and statistics to biological data", correct=True),
                opt("Replace all wet-lab experiments"),
                opt("Manufacture proteins industrially"),
                opt("Build microscopes"),
            ),
            "It analyses biological data computationally to extract meaning.",
        ),
        q(
            "Which base pairs with adenine (A) in DNA?",
            (
                opt("Thymine (T)", correct=True),
                opt("Guanine (G)"),
                opt("Cytosine (C)"),
                opt("Uracil in DNA"),
            ),
            "A pairs with T, and C pairs with G in double-stranded DNA.",
        ),
        q(
            "Translation reads mRNA in units of how many nucleotides?",
            (
                opt("Three (codons)", correct=True),
                opt("One"),
                opt("Two"),
                opt("Four"),
            ),
            "Codons are triplets; 64 codons encode 20 amino acids plus stops.",
        ),
        q(
            "Which problem matches a query sequence against a large database?",
            (
                opt("Search (e.g. BLAST)", correct=True),
                opt("Assembly"),
                opt("Translation"),
                opt("Replication"),
            ),
            "Database search finds where a query occurs among many sequences.",
        ),
        q(
            "On the Phred scale, higher quality scores mean what?",
            (
                opt("Exponentially lower error probability", correct=True),
                opt("Higher error probability"),
                opt("No relationship to error"),
                opt("Linearly higher error"),
            ),
            "P = 10^(-Q/10), so error falls steeply as Q rises.",
        ),
        q(
            "Which is a primary nucleotide sequence archive?",
            (
                opt("GenBank", correct=True),
                opt("PDB"),
                opt("Pfam"),
                opt("UniProt (proteins)"),
            ),
            "GenBank/ENA/DDBJ are the mirrored nucleotide archives.",
        ),
    ),
)
