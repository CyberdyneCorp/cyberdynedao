"""Quiz questions for the Biological Databases & Data Management - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why biological databases exist": (
            q(
                "What does the INSDC ensure about GenBank, ENA and DDBJ?",
                (
                    opt("They mirror the same nucleotide records daily", correct=True),
                    opt("They each hold a completely different set of organisms"),
                    opt("Only one of them may store any given sequence"),
                    opt("They store only protein structures, not sequences"),
                ),
                "The INSDC partners synchronise so a record submitted to one appears in all three.",
            ),
            q(
                "Which best distinguishes a primary from a secondary database?",
                (
                    opt(
                        "Primary stores submitted data as-is; secondary adds curation and cross-links",
                        correct=True,
                    ),
                    opt("Primary is older; secondary is simply a backup copy"),
                    opt("Primary holds proteins; secondary holds only DNA"),
                    opt("Primary is private; secondary is public"),
                ),
                "Primary/archival databases keep author-submitted data; secondary databases add expert annotation.",
            ),
            q(
                "Roughly how has the volume of public sequence records grown?",
                (
                    opt(
                        "Exponentially, doubling on a timescale of order a year or two",
                        correct=True,
                    ),
                    opt("Linearly, by a fixed number of records per year"),
                    opt("It has stayed essentially constant since the 1980s"),
                    opt("It has steadily shrunk as duplicates are removed"),
                ),
                "Sequence accumulation has been roughly exponential in the high-throughput era.",
            ),
        ),
        "The three pillars: NCBI, UniProt, PDB": (
            q(
                "Which resource is the global archive of experimentally determined 3D structures?",
                (
                    opt("The Protein Data Bank (PDB)", correct=True),
                    opt("GenBank"),
                    opt("PubMed"),
                    opt("Swiss-Prot"),
                ),
                "The PDB (run by the wwPDB) archives X-ray, cryo-EM and NMR macromolecular structures.",
            ),
            q(
                "What are the two main sections of UniProtKB?",
                (
                    opt("Swiss-Prot (reviewed) and TrEMBL (automatic)", correct=True),
                    opt("GenBank and RefSeq"),
                    opt("Entrez and BLAST"),
                    opt("X-ray and cryo-EM"),
                ),
                "UniProtKB splits into manually reviewed Swiss-Prot and automatically annotated TrEMBL.",
            ),
            q(
                "Why is there a large gap between known sequences and known structures?",
                (
                    opt(
                        "Determining a 3D structure experimentally is far harder than sequencing",
                        correct=True,
                    ),
                    opt("Structures are deliberately kept secret"),
                    opt("Most proteins simply have no structure"),
                    opt("Sequences are stored only on paper"),
                ),
                "Far more sequences are deposited than structures, motivating structure prediction.",
            ),
        ),
        "Accessions, versions and identifiers": (
            q(
                "Why should you cite a versioned accession like NM_000518.5?",
                (
                    opt(
                        "Records are revised, and the version pins exactly what you used",
                        correct=True,
                    ),
                    opt("The version number is the organism's taxonomy ID"),
                    opt("Bare accessions are invalid and rejected by databases"),
                    opt("The version encodes the sequence length"),
                ),
                "Versioning makes an analysis reproducible because records change over time.",
            ),
            q(
                "A prefix like NP_ on an accession tells you it is a:",
                (
                    opt("RefSeq protein record", correct=True),
                    opt("PDB structure"),
                    opt("Raw FASTQ read"),
                    opt("Gene Ontology term"),
                ),
                "NP_ denotes a RefSeq protein; NM_ a RefSeq transcript, for example.",
            ),
            q(
                "The 'identifier mapping' problem refers to:",
                (
                    opt(
                        "one molecule appearing under different IDs across databases", correct=True
                    ),
                    opt("two molecules accidentally sharing one accession"),
                    opt("converting DNA letters to RNA letters"),
                    opt("renaming a file from FASTA to GenBank"),
                ),
                "The same entity has distinct accessions per database, which must be reconciled to integrate data.",
            ),
        ),
        "FASTA and GenBank file formats": (
            q(
                "What does a FASTA record contain?",
                (
                    opt("A '>' header line plus the sequence in one-letter codes", correct=True),
                    opt("A full features table with gene coordinates"),
                    opt("Per-base quality scores for each residue"),
                    opt("Atomic 3D coordinates"),
                ),
                "FASTA is just a header and the residues; it carries no annotation.",
            ),
            q(
                "Which part of a GenBank flat file lets a browser draw a gene model?",
                (
                    opt("The FEATURES table with feature coordinates and qualifiers", correct=True),
                    opt("The LOCUS line only"),
                    opt("The ORIGIN sequence block alone"),
                    opt("The DEFINITION free text"),
                ),
                "The FEATURES table annotates genes, CDS and exons with coordinates.",
            ),
            q(
                "Compared with FASTA, what does FASTQ add?",
                (
                    opt("Per-base Phred quality scores", correct=True),
                    opt("3D atomic coordinates"),
                    opt("Gene Ontology annotations"),
                    opt("Foreign-key references"),
                ),
                "FASTQ extends FASTA with a quality string for each base, used for raw reads.",
            ),
        ),
        "Searching and retrieving records": (
            q(
                "In a BLAST result, a smaller E-value means:",
                (
                    opt("the match is more statistically significant", correct=True),
                    opt("the match is less significant"),
                    opt("the sequences are unrelated"),
                    opt("the alignment is longer but weaker"),
                ),
                "The E-value is the number of equally good hits expected by chance; smaller is more significant.",
            ),
            q(
                "Which tool finds records by sequence content rather than metadata?",
                (
                    opt("BLAST", correct=True),
                    opt("Entrez field search"),
                    opt("A GenBank text query"),
                    opt("ORDER BY in SQL"),
                ),
                "BLAST ranks database hits by local alignment to a query sequence.",
            ),
            q(
                "What is the purpose of field tags like [Organism] in an Entrez query?",
                (
                    opt(
                        "To restrict a term to a specific record field, narrowing hits",
                        correct=True,
                    ),
                    opt("To compress the downloaded file"),
                    opt("To convert the sequence to protein"),
                    opt("To assign a new accession"),
                ),
                "Field tags scope each term so Boolean queries return precise hit lists.",
            ),
        ),
        "From clicks to reproducible workflows": (
            q(
                "Why are NCBI E-utilities preferred over manual web downloads for analysis?",
                (
                    opt("They make retrieval scripted, recorded and reproducible", correct=True),
                    opt("They return data no web page can show"),
                    opt("They avoid the need to cite accessions"),
                    opt("They delete old database releases"),
                ),
                "Scripted endpoints (esearch/efetch/elink) let a pipeline rerun exactly.",
            ),
            q(
                "Which habit most improves reproducibility of a retrieval step?",
                (
                    opt("Recording the database release and exact query string used", correct=True),
                    opt("Renaming files to remove version numbers"),
                    opt("Querying only through the mouse"),
                    opt("Deleting the raw downloads after analysis"),
                ),
                "Pinning versions, releases and queries lets others reproduce the fetch.",
            ),
            q(
                "Why does scanning flat files become a problem as datasets grow?",
                (
                    opt(
                        "A linear scan costs O(n), growing with the number of records", correct=True
                    ),
                    opt("Flat files cannot exceed one megabyte"),
                    opt("FASTA cannot store more than one sequence"),
                    opt("Text files are encrypted by default"),
                ),
                "Naive scans scale linearly, motivating indexed databases.",
            ),
        ),
    },
    final=(
        q(
            "Which three databases form the INSDC?",
            (
                opt("GenBank, ENA and DDBJ", correct=True),
                opt("NCBI, UniProt and the PDB"),
                opt("RefSeq, Pfam and GO"),
                opt("BLAST, Entrez and BioMart"),
            ),
            "The INSDC partners are GenBank (NCBI), the ENA (EMBL-EBI) and the DDBJ.",
        ),
        q(
            "Which resource is the reference for protein sequence and function?",
            (
                opt("UniProt", correct=True),
                opt("GenBank"),
                opt("The PDB"),
                opt("PubMed"),
            ),
            "UniProt is the central protein knowledgebase (Swiss-Prot + TrEMBL).",
        ),
        q(
            "What does the '>' line in a FASTA file hold?",
            (
                opt("The identifier and a free-text description", correct=True),
                opt("Per-base quality scores"),
                opt("Atomic coordinates"),
                opt("A foreign key to another table"),
            ),
            "The header line names the sequence and describes it; residues follow.",
        ),
        q(
            "Citing NM_000518.5 rather than NM_000518 mainly improves:",
            (
                opt("reproducibility, by pinning the exact revision", correct=True),
                opt("download speed"),
                opt("the organism classification"),
                opt("the file format"),
            ),
            "The version suffix records exactly which revision an analysis used.",
        ),
        q(
            "A very small BLAST E-value indicates a hit that is:",
            (
                opt("highly significant (unlikely by chance)", correct=True),
                opt("likely a chance match"),
                opt("from an unrelated organism"),
                opt("too short to score"),
            ),
            "The E-value is the expected number of such hits by chance; smaller is better.",
        ),
        q(
            "The main reason to script retrieval with E-utilities or Biopython is to make it:",
            (
                opt("reproducible and scalable", correct=True),
                opt("impossible to cite"),
                opt("slower but prettier"),
                opt("invisible to other databases"),
            ),
            "Scripted, recorded retrieval replaces unrepeatable manual downloads.",
        ),
    ),
)
