"""Quiz questions for the Sequence Analysis & Alignment - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Position-specific scoring and PSI-BLAST": (
            q(
                "What does a position-specific scoring matrix (PSSM) store?",
                (
                    opt("A separate log-odds score for each residue at each column", correct=True),
                    opt("One score per residue pair, shared across all columns"),
                    opt("Only gap penalties"),
                    opt("3D coordinates"),
                ),
                "A PSSM captures per-column conservation, unlike a flat matrix.",
            ),
            q(
                "How does PSI-BLAST build its profile?",
                (
                    opt(
                        "It runs blastp, builds a PSSM from significant hits, then re-searches, iterating",
                        correct=True,
                    ),
                    opt("It uses a fixed BLOSUM62 matrix only"),
                    opt("It aligns 3D structures"),
                    opt("It samples motifs with Gibbs sampling"),
                ),
                "Iterated searches refine a PSSM toward remote homologs.",
            ),
            q(
                "A risk of iterated profile search is:",
                (
                    opt("Profile drift from contaminating unrelated hits", correct=True),
                    opt("Running too fast to converge"),
                    opt("Finding only identical sequences"),
                    opt("Ignoring all conserved columns"),
                ),
                "Unrelated hits can corrupt the profile across iterations.",
            ),
        ),
        "Profile hidden Markov models and HMMER": (
            q(
                "A profile HMM models indels using which states?",
                (
                    opt("Insert and delete states with their own transitions", correct=True),
                    opt("Only match states"),
                    opt("A single fixed gap penalty"),
                    opt("Reverse-complement states"),
                ),
                "Match, insert and delete states give position-specific gap behaviour.",
            ),
            q(
                "Which algorithm finds the single most likely state path through an HMM?",
                (
                    opt("Viterbi", correct=True),
                    opt("Forward"),
                    opt("Baum-Welch"),
                    opt("Neighbor-joining"),
                ),
                "Viterbi decodes the most probable path; forward sums over all paths.",
            ),
            q(
                "Which software builds and searches profile HMMs and underpins Pfam?",
                (
                    opt("HMMER", correct=True),
                    opt("BWA"),
                    opt("DESeq2"),
                    opt("STAR"),
                ),
                "HMMER's hmmbuild/hmmsearch power the Pfam database.",
            ),
        ),
        "Sequence logos and information content": (
            q(
                "In a sequence logo, the total height of a column represents:",
                (
                    opt("Information content (conservation) in bits", correct=True),
                    opt("The number of sequences"),
                    opt("The gap penalty"),
                    opt("The molecular weight"),
                ),
                "Column height is information content; letter heights show residue mix.",
            ),
            q(
                "A fully conserved DNA column carries how much information?",
                (
                    opt("2 bits (log2 of 4)", correct=True),
                    opt("0 bits"),
                    opt("4 bits"),
                    opt("20 bits"),
                ),
                "log2(4) = 2 bits for a perfectly conserved DNA position.",
            ),
            q(
                "Information content is computed as log2(N) minus what?",
                (
                    opt("The Shannon entropy of the column", correct=True),
                    opt("The gap count"),
                    opt("The E-value"),
                    opt("The sequence length"),
                ),
                "R = log2(N) - H, where H is the column's entropy.",
            ),
        ),
        "Motif discovery in sequences": (
            q(
                "What is a sequence motif?",
                (
                    opt("A short recurring pattern with biological meaning", correct=True),
                    opt("A whole chromosome"),
                    opt("A 3D fold"),
                    opt("A sequencing error"),
                ),
                "Motifs include binding sites, splice signals and target sequences.",
            ),
            q(
                "Which tool uses expectation-maximisation for de novo motif discovery?",
                (
                    opt("MEME", correct=True),
                    opt("BWA"),
                    opt("Bowtie2"),
                    opt("RAxML"),
                ),
                "MEME fits a position-weight matrix via EM; Gibbs sampling is an alternative.",
            ),
            q(
                "The main difficulty in motif discovery is:",
                (
                    opt("Finding a faint signal against a large random background", correct=True),
                    opt("Sequences being too short to store"),
                    opt("Too few possible patterns"),
                    opt("Lack of any background noise"),
                ),
                "Spurious matches rise with background size, masking real motifs.",
            ),
        ),
        "Protein domains and structure-based alignment": (
            q(
                "A protein domain is best described as:",
                (
                    opt("An independently folding, reusable evolutionary unit", correct=True),
                    opt("A single amino acid"),
                    opt("A whole genome"),
                    opt("A sequencing read"),
                ),
                "Domains are modular folding units reused across proteins.",
            ),
            q(
                "Which database stores profile-HMM models of protein domain families?",
                (
                    opt("Pfam", correct=True),
                    opt("SRA"),
                    opt("FASTQ"),
                    opt("dbSNP"),
                ),
                "Pfam holds HMM models; InterPro integrates several such resources.",
            ),
            q(
                "As sequences diverge far past the twilight zone, what tends to persist?",
                (
                    opt("Structural similarity (the fold)", correct=True),
                    opt("Percent sequence identity"),
                    opt("Exact nucleotide matches"),
                    opt("Identical gap patterns"),
                ),
                "Structure is conserved far longer than sequence; TM-align detects shared folds.",
            ),
        ),
        "Protein language models and AlphaFold": (
            q(
                "Protein language models such as ESM are trained how?",
                (
                    opt(
                        "As transformers predicting masked residues over huge sequence sets",
                        correct=True,
                    ),
                    opt("By hand-coding every rule"),
                    opt("By aligning only two sequences"),
                    opt("By measuring melting temperatures"),
                ),
                "Masked-residue prediction yields embeddings capturing structure and function.",
            ),
            q(
                "AlphaFold predicts what, and from what input?",
                (
                    opt(
                        "3D protein structure from sequence (using MSAs and the Evoformer)",
                        correct=True,
                    ),
                    opt("Gene expression from RNA-seq"),
                    opt("Variants from BAM files"),
                    opt("Phylogenetic trees from distances"),
                ),
                "It maps sequence plus MSA features to atomic coordinates.",
            ),
            q(
                "What does AlphaFold's pLDDT score report?",
                (
                    opt("Per-residue confidence in the predicted structure", correct=True),
                    opt("The E-value of a BLAST hit"),
                    opt("The number of training sequences"),
                    opt("The gap penalty used"),
                ),
                "pLDDT flags which regions of the prediction are reliable.",
            ),
        ),
    },
    final=(
        q(
            "A PSSM improves on a single substitution matrix by being:",
            (
                opt("Position-specific (per-column scores)", correct=True),
                opt("Faster but less sensitive"),
                opt("Free of any scoring"),
                opt("Limited to DNA only"),
            ),
            "Per-column log-odds capture position-specific conservation.",
        ),
        q(
            "Profile HMMs detect distant homologs better than pairwise BLAST because they:",
            (
                opt("Pool evidence across an entire family", correct=True),
                opt("Ignore conservation"),
                opt("Use no probabilities"),
                opt("Only compare two sequences"),
            ),
            "Family-wide statistics reveal remote relationships.",
        ),
        q(
            "The height of a sequence-logo column measures:",
            (
                opt("Information content in bits", correct=True),
                opt("The number of gaps"),
                opt("The molecular weight"),
                opt("The E-value"),
            ),
            "Taller columns are more conserved (higher information content).",
        ),
        q(
            "MEME and Gibbs sampling are methods for:",
            (
                opt("De novo motif discovery", correct=True),
                opt("Read mapping"),
                opt("Tree building"),
                opt("Variant calling"),
            ),
            "Both fit motif models from sets of sequences.",
        ),
        q(
            "Which database stores HMM models of protein domain families?",
            (
                opt("Pfam", correct=True),
                opt("GenBank"),
                opt("SRA"),
                opt("PDB raw reads"),
            ),
            "Pfam profiles classify domains; InterPro integrates them.",
        ),
        q(
            "AlphaFold's main achievement is:",
            (
                opt(
                    "Predicting 3D protein structure from sequence at near-experimental accuracy",
                    correct=True,
                ),
                opt("Sequencing genomes faster"),
                opt("Replacing all alignment forever"),
                opt("Measuring gene expression"),
            ),
            "It learns structure from MSAs via the Evoformer and a structure module.",
        ),
    ),
)
