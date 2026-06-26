"""Quiz questions for the Introduction to Bioinformatics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Pairwise alignment by dynamic programming": (
            q(
                "Which algorithm computes an optimal global alignment?",
                (
                    opt("Needleman-Wunsch", correct=True),
                    opt("Smith-Waterman"),
                    opt("Neighbor-joining"),
                    opt("Baum-Welch"),
                ),
                "Needleman-Wunsch is global; Smith-Waterman is local.",
            ),
            q(
                "What is the time complexity of DP pairwise alignment for sequences of length m and n?",
                (
                    opt("O(mn)", correct=True),
                    opt("O(m+n)"),
                    opt("O(2^n)"),
                    opt("O(log mn)"),
                ),
                "Filling the m-by-n scoring matrix takes O(mn).",
            ),
            q(
                "How does Smith-Waterman produce a local alignment?",
                (
                    opt("It adds a 0 option so scores never go negative", correct=True),
                    opt("It ignores gap penalties entirely"),
                    opt("It requires sequences of equal length"),
                    opt("It uses a phylogenetic tree"),
                ),
                "Clamping at 0 lets the best-scoring subsegment be found.",
            ),
        ),
        "Substitution matrices and gap penalties": (
            q(
                "BLOSUM substitution matrices are derived from what?",
                (
                    opt("Conserved blocks of aligned sequences at a given identity", correct=True),
                    opt("Random sequence shuffles"),
                    opt("3D structure coordinates only"),
                    opt("Codon usage tables"),
                ),
                "BLOSUM is built directly from conserved blocks; PAM extrapolates.",
            ),
            q(
                "An affine gap penalty charges what?",
                (
                    opt(
                        "A large opening cost plus a smaller per-residue extension cost",
                        correct=True,
                    ),
                    opt("The same cost per gap regardless of length"),
                    opt("No cost for gaps"),
                    opt("A cost only at the end of the alignment"),
                ),
                "Affine gaps favour a few long gaps over many short ones.",
            ),
            q(
                "For aligning distantly related proteins, which matrix is more appropriate?",
                (
                    opt("BLOSUM45", correct=True),
                    opt("BLOSUM90"),
                    opt("BLOSUM80"),
                    opt("Identity matrix only"),
                ),
                "Lower-number BLOSUM (e.g. 45) suits more divergent sequences.",
            ),
        ),
        "BLAST and the statistics of search": (
            q(
                "BLAST achieves speed using which strategy?",
                (
                    opt("Seed-and-extend on shared words", correct=True),
                    opt("Full dynamic programming against every entry"),
                    opt("Random sampling of the database"),
                    opt("Brute-force enumeration of all alignments"),
                ),
                "It finds word hits, then extends only those into alignments.",
            ),
            q(
                "What does a BLAST E-value represent?",
                (
                    opt(
                        "Expected number of equally good hits by chance in that database",
                        correct=True,
                    ),
                    opt("The percent identity of the alignment"),
                    opt("The number of gaps in the alignment"),
                    opt("The length of the query"),
                ),
                "E is the chance-expected count of hits scoring at least as high.",
            ),
            q(
                "How does the E-value change as the alignment score increases?",
                (
                    opt("It decays exponentially", correct=True),
                    opt("It increases linearly"),
                    opt("It stays constant"),
                    opt("It increases exponentially"),
                ),
                "E ~ K m n exp(-lambda S), so it falls steeply with score.",
            ),
        ),
        "Hidden Markov models for sequences": (
            q(
                "A profile HMM represents a sequence family using which state types?",
                (
                    opt("Match, insert and delete states", correct=True),
                    opt("Only a single average sequence"),
                    opt("Leaves and internal nodes of a tree"),
                    opt("Codons and anticodons"),
                ),
                "Profile HMMs use per-position match, insert and delete states.",
            ),
            q(
                "Which algorithm finds the most likely hidden state path?",
                (
                    opt("Viterbi", correct=True),
                    opt("Forward"),
                    opt("Baum-Welch"),
                    opt("Neighbor-joining"),
                ),
                "Viterbi decodes the most probable path; forward sums all paths.",
            ),
            q(
                "Why do profile HMMs detect remote homologs better than pairwise BLAST?",
                (
                    opt(
                        "They pool position-specific information across many family members",
                        correct=True,
                    ),
                    opt("They ignore conservation entirely"),
                    opt("They require 3D structures"),
                    opt("They only compare two sequences at a time"),
                ),
                "Pooling family information captures position-specific conservation.",
            ),
        ),
        "Multiple sequence alignment": (
            q(
                "Why is optimal multiple sequence alignment not solved by exact DP in practice?",
                (
                    opt("Its cost grows roughly as L^N, which is NP-hard", correct=True),
                    opt("It is impossible to score columns"),
                    opt("DNA cannot be aligned"),
                    opt("There is no reference genome"),
                ),
                "Exact MSA is NP-hard, so heuristics are used.",
            ),
            q(
                "What is the dominant MSA heuristic used by Clustal, MUSCLE and MAFFT?",
                (
                    opt("Progressive alignment guided by a tree", correct=True),
                    opt("Brute-force enumeration"),
                    opt("Random pairing"),
                    opt("Burrows-Wheeler transform"),
                ),
                "They align from most to least similar using a guide tree.",
            ),
            q(
                "A sequence logo visualises what per column?",
                (
                    opt("Conservation / information content in bits", correct=True),
                    opt("The E-value"),
                    opt("Branch length"),
                    opt("Read coverage"),
                ),
                "Taller letters mark more conserved, information-rich positions.",
            ),
        ),
        "Phylogenetics: trees from sequences": (
            q(
                "Which phylogenetic method scores trees under an explicit substitution model?",
                (
                    opt("Maximum likelihood", correct=True),
                    opt("Neighbor-joining (distance)"),
                    opt("UPGMA only"),
                    opt("Sequence logos"),
                ),
                "ML/Bayesian methods use models like GTR; NJ is distance-based.",
            ),
            q(
                "What does bootstrapping estimate in phylogenetics?",
                (
                    opt("Branch support by resampling alignment columns", correct=True),
                    opt("The substitution matrix"),
                    opt("Read quality"),
                    opt("Gene expression level"),
                ),
                "Resampling columns gives confidence values for branches.",
            ),
            q(
                "Why does observed sequence distance saturate over long evolutionary times?",
                (
                    opt("Repeated mutations at the same sites hide earlier changes", correct=True),
                    opt("Sequences stop mutating"),
                    opt("Branch lengths become negative"),
                    opt("The alignment gets shorter"),
                ),
                "Multiple hits per site cap apparent differences; corrections recover true distance.",
            ),
        ),
    },
    final=(
        q(
            "Needleman-Wunsch and Smith-Waterman differ primarily in that one is what?",
            (
                opt("Global and the other local", correct=True),
                opt("Faster and the other slower by a constant"),
                opt("For DNA and the other for protein only"),
                opt("Heuristic and the other exact"),
            ),
            "NW is global end-to-end; SW finds the best local subsegment.",
        ),
        q(
            "An affine gap model is preferred because it does what?",
            (
                opt("Favours a few long gaps over many short ones", correct=True),
                opt("Eliminates gaps entirely"),
                opt("Penalizes matches"),
                opt("Ignores sequence length"),
            ),
            "Opening cost plus extension cost matches how indels occur.",
        ),
        q(
            "A smaller BLAST E-value means what?",
            (
                opt("Stronger evidence of true homology", correct=True),
                opt("More chance hits expected"),
                opt("A longer query"),
                opt("A weaker match"),
            ),
            "Fewer chance hits expected implies a more significant match.",
        ),
        q(
            "Which algorithm trains HMM parameters from unlabelled data?",
            (
                opt("Baum-Welch (EM)", correct=True),
                opt("Viterbi"),
                opt("Forward only"),
                opt("Bootstrap"),
            ),
            "Baum-Welch is the expectation-maximization training procedure.",
        ),
        q(
            "Progressive multiple alignment first requires what?",
            (
                opt("A guide tree from pairwise distances", correct=True),
                opt("A finished phylogenetic tree with support"),
                opt("A variant call file"),
                opt("A 3D structure"),
            ),
            "Pairwise distances build a guide tree that orders the alignment.",
        ),
        q(
            "Maximum-likelihood phylogenetics relies on what?",
            (
                opt("An explicit nucleotide/amino-acid substitution model", correct=True),
                opt("Only counting identical residues"),
                opt("Ignoring branch lengths"),
                opt("Read coverage"),
            ),
            "Models like Jukes-Cantor or GTR define the likelihood of trees.",
        ),
    ),
)
