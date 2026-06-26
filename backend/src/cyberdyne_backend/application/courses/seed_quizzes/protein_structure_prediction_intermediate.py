"""Quiz questions for the Protein Structure Prediction - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Multiple sequence alignments and profiles": (
            q(
                "What is the most informative single input for modern prediction?",
                (
                    opt("A deep multiple sequence alignment (MSA)", correct=True),
                    opt("The molecular weight"),
                    opt("The isoelectric point"),
                    opt("The crystal color"),
                ),
                "MSAs reveal conservation and covariation across homologs.",
            ),
            q(
                "A profile (PSSM) encodes what?",
                (
                    opt("Position-specific amino-acid probabilities", correct=True),
                    opt("The melting temperature"),
                    opt("A single best sequence"),
                    opt("The 3D coordinates"),
                ),
                "It gives per-column residue probabilities from the MSA.",
            ),
            q(
                "Which tool builds deep MSAs by iterative database search?",
                (
                    opt("HHblits", correct=True),
                    opt("DSSP"),
                    opt("PyMOL"),
                    opt("Clustal once with no iteration"),
                ),
                "HHblits and jackhmmer iteratively gather homologs.",
            ),
        ),
        "Fold recognition by threading": (
            q(
                "Threading answers which question?",
                (
                    opt("Which known fold best accommodates this sequence?", correct=True),
                    opt("What is the exact melting temperature?"),
                    opt("How many genes are in the genome?"),
                    opt("What is the codon usage?"),
                ),
                "It fits the query onto candidate template folds.",
            ),
            q(
                "Knowledge-based statistical potentials are derived how?",
                (
                    opt(
                        "From observed PDB contact frequencies via the inverse Boltzmann relation",
                        correct=True,
                    ),
                    opt("By guessing"),
                    opt("From the genetic code"),
                    opt("From mass spectra"),
                ),
                "Frequent contacts become favourable pseudo-energies.",
            ),
            q(
                "Which method is a well-known threading/fold-recognition tool?",
                (
                    opt("I-TASSER", correct=True),
                    opt("Sanger"),
                    opt("Western blot"),
                    opt("ImageJ"),
                ),
                "I-TASSER, RaptorX and Phyre2 do fold recognition.",
            ),
        ),
        "Secondary-structure and solvent prediction": (
            q(
                "What did PSIPRED use to reach ~80% Q3 accuracy?",
                (
                    opt("A PSI-BLAST profile fed into a neural network", correct=True),
                    opt("A single sequence only"),
                    opt("X-ray diffraction"),
                    opt("Random guessing"),
                ),
                "Profiles capture conservation signals a single sequence hides.",
            ),
            q(
                "Q3 accuracy refers to three states. Which set is correct?",
                (
                    opt("Helix, strand, coil", correct=True),
                    opt("A, T, G"),
                    opt("Hydrophobic, polar, charged"),
                    opt("Alpha, beta, gamma rays"),
                ),
                "Q3 scores H/E/C assignment per residue.",
            ),
            q(
                "Why does the secondary-structure accuracy ceiling sit near ~88%?",
                (
                    opt(
                        "Experimental assignment methods (e.g. DSSP vs STRIDE) disagree",
                        correct=True,
                    ),
                    opt("Computers cannot count that high"),
                    opt("Proteins have no secondary structure"),
                    opt("Profiles are forbidden"),
                ),
                "Ground-truth disagreement caps measurable accuracy.",
            ),
        ),
        "Coevolution and evolutionary couplings": (
            q(
                "Why do contacting residues tend to coevolve?",
                (
                    opt(
                        "A mutation in one is compensated by a mutation in its partner",
                        correct=True,
                    ),
                    opt("They share the same codon"),
                    opt("They are always identical"),
                    opt("Random chance only"),
                ),
                "Compensatory mutations correlate the two MSA columns.",
            ),
            q(
                "What problem does direct coupling analysis (DCA) solve?",
                (
                    opt(
                        "Separating direct couplings from indirect (transitive) ones", correct=True
                    ),
                    opt("Aligning DNA to protein"),
                    opt("Measuring melting temperature"),
                    opt("Counting chromosomes"),
                ),
                "A global Potts model removes transitive correlations.",
            ),
            q(
                "Coevolution-based contact accuracy depends most on what?",
                (
                    opt("The number of effective sequences per length (Neff/L)", correct=True),
                    opt("The protein's color"),
                    opt("The time of day"),
                    opt("The font of the FASTA file"),
                ),
                "Deep, diverse MSAs give reliable couplings.",
            ),
        ),
        "Contact and distance prediction": (
            q(
                "How is a contact map treated by deep networks like RaptorX-Contact?",
                (
                    opt(
                        "Like an image processed by a residual/convolutional network", correct=True
                    ),
                    opt("As a single number"),
                    opt("As raw DNA"),
                    opt("As a phylogenetic tree"),
                ),
                "The residue-by-residue matrix is an image-like 2D input.",
            ),
            q(
                "What replaced binary contacts for more reliable folding?",
                (
                    opt("Predicted distance distributions (distograms)", correct=True),
                    opt("Single melting temperatures"),
                    opt("Codon tables"),
                    opt("Random restraints"),
                ),
                "Distograms give richer geometric restraints.",
            ),
            q(
                "Why does top-L precision matter more than recall for contacts?",
                (
                    opt(
                        "True contacts are sparse; high-confidence top pairs drive folding",
                        correct=True,
                    ),
                    opt("Recall is illegal"),
                    opt("All pairs are contacts"),
                    opt("Precision is unmeasurable"),
                ),
                "Most pairs are non-contacts, so the best pairs count most.",
            ),
        ),
    },
    final=(
        q(
            "A profile-HMM method gains sensitivity to remote homologs because:",
            (
                opt("Position-specific profiles capture conservation patterns", correct=True),
                opt("They ignore the sequence"),
                opt("They only use one sequence"),
                opt("They use random scores"),
            ),
            "Profiles detect distant relatives a single sequence misses.",
        ),
        q(
            "Threading scores a query against folds using mainly:",
            (
                opt("Knowledge-based statistical potentials", correct=True),
                opt("Gel electrophoresis"),
                opt("Codon optimization"),
                opt("Random numbers"),
            ),
            "Statistical potentials measure environment fit.",
        ),
        q(
            "PSIPRED improved secondary-structure prediction by using:",
            (
                opt("Evolutionary profiles plus a neural network", correct=True),
                opt("Only amino-acid propensities"),
                opt("X-ray data at runtime"),
                opt("No input at all"),
            ),
            "Profile-based networks reached ~80% Q3.",
        ),
        q(
            "Direct coupling analysis is built on which statistical model?",
            (
                opt("A maximum-entropy Potts model", correct=True),
                opt("Linear regression on mass"),
                opt("A decision tree of codons"),
                opt("A Markov chain of nucleotides only"),
            ),
            "The Potts model separates direct from indirect couplings.",
        ),
        q(
            "The strongest predictor of coevolution-based contact accuracy is:",
            (
                opt("Effective sequences per length (Neff/L)", correct=True),
                opt("Protein molecular weight"),
                opt("Number of cysteines"),
                opt("File size"),
            ),
            "Deeper MSAs yield more accurate couplings.",
        ),
        q(
            "Distograms improved over binary contact maps because they:",
            (
                opt("Provide richer distance restraints for folding", correct=True),
                opt("Are smaller files"),
                opt("Ignore geometry"),
                opt("Remove the need for an MSA"),
            ),
            "Distance distributions constrain structure better than 0/1 contacts.",
        ),
    ),
)
