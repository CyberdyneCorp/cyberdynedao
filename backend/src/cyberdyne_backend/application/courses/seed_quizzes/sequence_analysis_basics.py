"""Quiz questions for the Sequence Analysis & Alignment - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What sequence analysis is and why we align": (
            q(
                "What is the central tool of sequence analysis?",
                (
                    opt("Alignment of corresponding residues", correct=True),
                    opt("Centrifugation of cells"),
                    opt("Gel electrophoresis"),
                    opt("DNA replication"),
                ),
                "Alignment lines up corresponding residues to reveal shared signal.",
            ),
            q(
                "How do homology and similarity differ?",
                (
                    opt(
                        "Homology is shared ancestry (yes/no); similarity is a measurable quantity",
                        correct=True,
                    ),
                    opt("They are exactly the same thing"),
                    opt("Similarity is yes/no; homology is a percentage"),
                    opt("Homology applies only to RNA"),
                ),
                "Homology is a binary statement; similarity is measured as percent identity.",
            ),
            q(
                "As evolutionary distance increases, sequence identity tends to do what?",
                (
                    opt("Decay roughly exponentially", correct=True),
                    opt("Increase steadily"),
                    opt("Stay perfectly constant"),
                    opt("Jump to 100%"),
                ),
                "Related sequences diverge over time, so percent identity falls.",
            ),
        ),
        "Scoring matches, mismatches and gaps": (
            q(
                "In a simple scheme, how is a gap treated relative to a match?",
                (
                    opt("It is penalised (negative)", correct=True),
                    opt("It is rewarded (positive)"),
                    opt("It is ignored entirely"),
                    opt("It always scores zero"),
                ),
                "Gaps are insertions/deletions and carry a penalty.",
            ),
            q(
                "An affine gap model charges what?",
                (
                    opt("An opening cost plus a per-residue extension cost", correct=True),
                    opt("Only a single flat cost regardless of length"),
                    opt("Nothing for the first ten residues"),
                    opt("A reward that grows with gap length"),
                ),
                "Affine cost is o + e*g, favouring fewer long gaps.",
            ),
            q(
                "The overall alignment score is computed how?",
                (
                    opt("By summing the scores of all columns", correct=True),
                    opt("By taking the single best column"),
                    opt("By multiplying mismatch counts"),
                    opt("By counting gaps only"),
                ),
                "The score is the sum of match, mismatch and gap contributions.",
            ),
        ),
        "Identity, similarity and conservation": (
            q(
                "Percent identity counts what?",
                (
                    opt("Aligned columns holding the same residue", correct=True),
                    opt("Total length of the sequences"),
                    opt("Number of gaps only"),
                    opt("Chemically similar but different residues"),
                ),
                "Identity is the fraction of identical aligned positions.",
            ),
            q(
                "Why is similarity usually higher than identity for proteins?",
                (
                    opt("It also counts conservative substitutions", correct=True),
                    opt("It excludes mismatches"),
                    opt("It double-counts gaps"),
                    opt("It ignores conserved residues"),
                ),
                "Similarity includes swaps between chemically alike amino acids.",
            ),
            q(
                "What is the 'twilight zone' of sequence identity?",
                (
                    opt(
                        "Below ~30% identity, where true homology is hard to distinguish from chance",
                        correct=True,
                    ),
                    opt("Above 90% identity, where everything is certain"),
                    opt("The region of a gene with no function"),
                    opt("A type of substitution matrix"),
                ),
                "Below roughly 30% identity, homology calls become unreliable.",
            ),
        ),
        "Dot plots: visualising sequence relatedness": (
            q(
                "In a dot plot, a dot is placed where?",
                (
                    opt("Two residues (one per axis) match", correct=True),
                    opt("A gap is introduced"),
                    opt("The sequences end"),
                    opt("A mismatch occurs"),
                ),
                "A dot marks a match between the row and column residues.",
            ),
            q(
                "A single strong main diagonal in a dot plot indicates what?",
                (
                    opt("Global similarity between the two sequences", correct=True),
                    opt("A complete lack of similarity"),
                    opt("Only an inverted region"),
                    opt("Random noise"),
                ),
                "One clean diagonal means the sequences align end to end.",
            ),
            q(
                "Why do dot plots use a window and threshold?",
                (
                    opt("To suppress random single-residue match noise", correct=True),
                    opt("To make the plot larger"),
                    opt("To remove all the real signal"),
                    opt("To convert DNA to protein"),
                ),
                "A window/threshold plots a dot only when enough residues match, cutting noise.",
            ),
        ),
        "Sequence alphabets and substitution patterns": (
            q(
                "In DNA, transitions versus transversions:",
                (
                    opt("Transitions are more frequent than transversions", correct=True),
                    opt("Transversions are far more frequent"),
                    opt("They occur at exactly equal rates"),
                    opt("Neither ever occurs"),
                ),
                "Purine<->purine and pyrimidine<->pyrimidine (transitions) dominate.",
            ),
            q(
                "Substitution scores are typically expressed as what?",
                (
                    opt("Log-odds of observed versus chance frequencies", correct=True),
                    opt("Raw molecular weights"),
                    opt("Random integers"),
                    opt("Melting temperatures"),
                ),
                "A log-odds score is positive when a swap exceeds chance expectation.",
            ),
            q(
                "Why do chemically drastic amino-acid swaps score very negative?",
                (
                    opt("They are rare and usually deleterious", correct=True),
                    opt("They are the most common substitutions"),
                    opt("They never affect function"),
                    opt("They increase sequence length"),
                ),
                "Rare, function-disrupting changes get the largest penalties.",
            ),
        ),
    },
    final=(
        q(
            "What does sequence alignment fundamentally reveal?",
            (
                opt("Shared ancestry, conservation and divergence", correct=True),
                opt("The melting point of DNA"),
                opt("The mass of a protein"),
                opt("The color of a cell"),
            ),
            "Alignment exposes homologous signal across related sequences.",
        ),
        q(
            "Which contributes a penalty to an alignment score?",
            (
                opt("A gap", correct=True),
                opt("A match"),
                opt("A conserved residue"),
                opt("A high-information column"),
            ),
            "Gaps and mismatches are penalised; matches are rewarded.",
        ),
        q(
            "Similarity is always at least as high as identity because it includes:",
            (
                opt("Conservative substitutions", correct=True),
                opt("Only identical residues"),
                opt("Gaps as matches"),
                opt("Reverse complements"),
            ),
            "Similarity counts chemically conservative swaps in addition to identities.",
        ),
        q(
            "A broken or shifted diagonal in a dot plot suggests:",
            (
                opt("An insertion or deletion (indel)", correct=True),
                opt("A perfect global match"),
                opt("No relationship at all"),
                opt("A scoring matrix error"),
            ),
            "Indels shift the diagonal where the alignment jumps.",
        ),
        q(
            "Which DNA mutation type is generally most frequent?",
            (
                opt("Transitions", correct=True),
                opt("Transversions"),
                opt("Large inversions"),
                opt("Whole-genome duplications"),
            ),
            "Transitions occur more often than transversions.",
        ),
        q(
            "Below roughly 30% identity, homology calls are:",
            (
                opt("Unreliable (the twilight zone)", correct=True),
                opt("Completely certain"),
                opt("Always false"),
                opt("Irrelevant"),
            ),
            "The twilight zone is where chance similarity mimics homology.",
        ),
    ),
)
