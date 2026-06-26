"""Quiz questions for the Sequence Analysis & Alignment - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Global alignment with Needleman-Wunsch": (
            q(
                "Needleman-Wunsch computes which kind of alignment?",
                (
                    opt("A global, end-to-end alignment", correct=True),
                    opt("A local sub-region alignment"),
                    opt("A structural superposition"),
                    opt("A random alignment"),
                ),
                "Needleman-Wunsch aligns two sequences over their full length.",
            ),
            q(
                "What is the time complexity of filling the DP matrix for two sequences of length m and n?",
                (
                    opt("O(mn)", correct=True),
                    opt("O(2^n)"),
                    opt("O(log n)"),
                    opt("O(1)"),
                ),
                "Dynamic programming fills m*n cells.",
            ),
            q(
                "After filling the matrix, how is the alignment recovered?",
                (
                    opt("By traceback from the bottom-right corner", correct=True),
                    opt("By sorting the rows"),
                    opt("By deleting all gaps"),
                    opt("By a BLAST search"),
                ),
                "Traceback from F(m,n) reconstructs the optimal global alignment.",
            ),
        ),
        "Local alignment with Smith-Waterman": (
            q(
                "What single change turns global DP into Smith-Waterman local alignment?",
                (
                    opt("Adding a zero option so scores cannot go negative", correct=True),
                    opt("Removing all gap penalties"),
                    opt("Doubling the match score"),
                    opt("Reversing one sequence"),
                ),
                "The 0 floor plus traceback from the max cell yields local alignment.",
            ),
            q(
                "Where does Smith-Waterman traceback begin?",
                (
                    opt("From the maximum-scoring cell", correct=True),
                    opt("From the bottom-right corner"),
                    opt("From the top-left corner"),
                    opt("From a random cell"),
                ),
                "Local alignment starts traceback at the matrix maximum.",
            ),
            q(
                "Local alignment is preferred when sequences share:",
                (
                    opt("Only a conserved region or domain", correct=True),
                    opt("Identical full lengths"),
                    opt("No similarity at all"),
                    opt("The same name"),
                ),
                "It finds the best subsegment, ideal for shared domains.",
            ),
        ),
        "Substitution matrices: PAM and BLOSUM": (
            q(
                "A substitution matrix score s(a,b) is fundamentally a:",
                (
                    opt("Log-odds of observed vs expected substitution frequency", correct=True),
                    opt("Molecular weight difference"),
                    opt("Count of hydrogen bonds"),
                    opt("Random value"),
                ),
                "Scores are log-odds of observed over chance frequencies.",
            ),
            q(
                "BLOSUM62 is built from blocks at what identity level?",
                (
                    opt("62% identity", correct=True),
                    opt("250% identity"),
                    opt("6.2% identity"),
                    opt("100% identity"),
                ),
                "The number in BLOSUM is the clustering identity threshold.",
            ),
            q(
                "For PAM and BLOSUM, the numbering runs in opposite directions. Which is true?",
                (
                    opt(
                        "Higher PAM means more divergence; higher BLOSUM means less divergence",
                        correct=True,
                    ),
                    opt("Higher numbers always mean more divergence in both"),
                    opt("The numbers are arbitrary and meaningless"),
                    opt("Both decrease with divergence"),
                ),
                "PAM250 is for distant relatives; BLOSUM80 is for close ones.",
            ),
        ),
        "Affine gap penalties and gap models": (
            q(
                "The affine gap cost for a gap of length g is:",
                (
                    opt("o + e*g (opening plus extension)", correct=True),
                    opt("o*g only"),
                    opt("a fixed value independent of g"),
                    opt("a reward proportional to g"),
                ),
                "Affine cost pays one opening plus per-residue extension.",
            ),
            q(
                "Why does biology favour the affine model over a linear one?",
                (
                    opt("It prefers fewer, longer indels over many short ones", correct=True),
                    opt("It makes alignments shorter"),
                    opt("It removes all gaps"),
                    opt("It rewards mismatches"),
                ),
                "A single long indel is more plausible than many scattered ones.",
            ),
            q(
                "Which algorithm implements affine gaps while keeping O(mn) time?",
                (
                    opt("Gotoh (three DP matrices)", correct=True),
                    opt("BLAST"),
                    opt("Neighbor-joining"),
                    opt("Gibbs sampling"),
                ),
                "Gotoh's algorithm uses match and two gap matrices.",
            ),
        ),
        "BLAST and E-value statistics": (
            q(
                "BLAST speeds up search using which strategy?",
                (
                    opt("Seed-and-extend from short word hits", correct=True),
                    opt("Full Smith-Waterman against every entry"),
                    opt("Random sampling of the database"),
                    opt("Sorting the database alphabetically"),
                ),
                "It finds word (k-mer) hits, then extends them into HSPs.",
            ),
            q(
                "The BLAST E-value measures what?",
                (
                    opt(
                        "The number of hits of that score expected by chance in the database",
                        correct=True,
                    ),
                    opt("The percent identity of the hit"),
                    opt("The length of the query"),
                    opt("The number of gaps"),
                ),
                "E = K*m*n*exp(-lambda*S); lower E means stronger evidence.",
            ),
            q(
                "How does the E-value change as the alignment score rises?",
                (
                    opt("It falls exponentially", correct=True),
                    opt("It rises linearly"),
                    opt("It stays constant"),
                    opt("It oscillates"),
                ),
                "E decays as exp(-lambda*S), so higher scores are far more significant.",
            ),
        ),
        "Multiple sequence alignment basics": (
            q(
                "Optimal MSA by dynamic programming is:",
                (
                    opt("NP-hard, scaling about L^N", correct=True),
                    opt("Always O(mn)"),
                    opt("Constant time"),
                    opt("Solvable by sorting"),
                ),
                "Exact MSA cost grows like L^N, so heuristics are used.",
            ),
            q(
                "The dominant MSA heuristic is:",
                (
                    opt("Progressive alignment guided by a tree", correct=True),
                    opt("Random pairing"),
                    opt("Brute-force enumeration"),
                    opt("Reverse complementation"),
                ),
                "Progressive methods align from most to least similar via a guide tree.",
            ),
            q(
                "Which is a widely used MSA tool?",
                (
                    opt("MAFFT", correct=True),
                    opt("GATK"),
                    opt("Bowtie2"),
                    opt("Salmon"),
                ),
                "MAFFT, MUSCLE and Clustal Omega are common MSA tools.",
            ),
        ),
    },
    final=(
        q(
            "Which algorithm gives the optimal global alignment of two sequences?",
            (
                opt("Needleman-Wunsch", correct=True),
                opt("Smith-Waterman"),
                opt("Neighbor-joining"),
                opt("MEME"),
            ),
            "Needleman-Wunsch is exact global DP alignment.",
        ),
        q(
            "Smith-Waterman differs from Needleman-Wunsch chiefly by:",
            (
                opt("A zero floor and traceback from the maximum cell", correct=True),
                opt("Using no scoring matrix"),
                opt("Aligning three sequences at once"),
                opt("Skipping dynamic programming"),
            ),
            "These two changes produce a local alignment.",
        ),
        q(
            "Which matrix is the default for protein BLAST?",
            (
                opt("BLOSUM62", correct=True),
                opt("PAM1"),
                opt("Identity matrix"),
                opt("A random matrix"),
            ),
            "BLOSUM62 is the standard general-purpose protein matrix.",
        ),
        q(
            "An affine gap penalty for length g equals:",
            (
                opt("o + e*g", correct=True),
                opt("e*g only"),
                opt("a constant"),
                opt("a positive reward"),
            ),
            "Opening cost plus per-residue extension cost.",
        ),
        q(
            "A BLAST E-value of 1e-20 versus 1.0 means the 1e-20 hit is:",
            (
                opt("Far more significant (fewer chance hits expected)", correct=True),
                opt("Less significant"),
                opt("Equally significant"),
                opt("A sequencing error"),
            ),
            "Smaller E-values indicate stronger evidence of homology.",
        ),
        q(
            "Why are MSAs computed with heuristics rather than exact DP?",
            (
                opt("Exact MSA is NP-hard and scales like L^N", correct=True),
                opt("Exact MSA is too fast to be useful"),
                opt("Heuristics are always more accurate"),
                opt("DP cannot handle proteins"),
            ),
            "The exponential cost in the number of sequences forces heuristics.",
        ),
    ),
)
