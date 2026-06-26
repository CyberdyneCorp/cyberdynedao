"""Quiz questions for the Molecular Docking & Virtual Screening - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Enrichment, ROC and screening metrics": (
            q(
                "What does an ROC AUC of 0.5 indicate?",
                (
                    opt("Random performance", correct=True),
                    opt("Perfect performance"),
                    opt("Impossible result"),
                    opt("Half the actives are toxic"),
                ),
                "AUC 0.5 is random; 1.0 is perfect ranking.",
            ),
            q(
                "Why are early-recognition metrics (BEDROC, RIE) often preferred over global AUC?",
                (
                    opt("Hits are wanted from the very top of the ranking", correct=True),
                    opt("They are easier to misuse"),
                    opt("AUC cannot be computed"),
                    opt("They ignore the actives"),
                ),
                "Screens test only top compounds, so early ranks matter most.",
            ),
            q(
                "Property-matched but topologically distinct decoys (DUD-E) help avoid:",
                (
                    opt("Trivial separation by simple properties", correct=True),
                    opt("Computing the ROC curve"),
                    opt("Adding hydrogens"),
                    opt("Parallel computing"),
                ),
                "Matched decoys stop methods from cheating on size/charge differences.",
            ),
        ),
        "Ultra-large library screening": (
            q(
                "Why is docking every molecule of a 10^10 library impractical?",
                (
                    opt("Brute-force cost grows linearly with library size", correct=True),
                    opt("The molecules cannot be drawn"),
                    opt("Scoring functions do not exist"),
                    opt("RMSD cannot be computed"),
                ),
                "Cost scales with size, so tens of billions overwhelm brute force.",
            ),
            q(
                "Active-learning screening (e.g. MolPAL) reduces cost by:",
                (
                    opt(
                        "Training a surrogate model to triage which compounds to dock", correct=True
                    ),
                    opt("Docking everything twice"),
                    opt("Ignoring the target"),
                    opt("Using only random selection"),
                ),
                "A surrogate predicts scores so only top candidates are actually docked.",
            ),
            q(
                "At billion-compound scale, even a tiny false-positive rate means:",
                (
                    opt("Many garbage top hits, so rescoring is essential", correct=True),
                    opt("No false positives at all"),
                    opt("The library shrinks automatically"),
                    opt("Scores become exact"),
                ),
                "Scale amplifies error, demanding careful rescoring of the shortlist.",
            ),
        ),
        "Consensus scoring and rescoring": (
            q(
                "The rationale for consensus scoring is that:",
                (
                    opt("Independent scoring errors partly cancel", correct=True),
                    opt("One function is always perfect"),
                    opt("Scores are irrelevant"),
                    opt("It removes the need for poses"),
                ),
                "Combining functions exploits partly independent errors.",
            ),
            q(
                "MM/GBSA and FEP are used during which step?",
                (
                    opt("Rescoring a small set of top poses more accurately", correct=True),
                    opt("Initial fast docking of the whole library"),
                    opt("Filtering by molecular weight"),
                    opt("Drawing 2D structures"),
                ),
                "These expensive free-energy methods rescore the funnel's top tier.",
            ),
            q(
                "FEP computes relative binding free energies by:",
                (
                    opt(
                        "Alchemical transformation along a coupling parameter lambda", correct=True
                    ),
                    opt("Counting hydrogen atoms"),
                    opt("Measuring the crystal color"),
                    opt("Sequencing the protein"),
                ),
                "FEP/TI transform one ligand into another along lambda to get dG.",
            ),
        ),
        "Machine-learning scoring functions": (
            q(
                "An early ML scoring function on PDBbind using random forests was:",
                (
                    opt("RF-Score", correct=True),
                    opt("BLAST"),
                    opt("Clustal"),
                    opt("GROMACS"),
                ),
                "RF-Score used random forests on interaction counts.",
            ),
            q(
                "The main risk of ML scoring functions is:",
                (
                    opt("Dataset bias / memorisation rather than learning physics", correct=True),
                    opt("They are too slow to ever run"),
                    opt("They cannot read SMILES"),
                    opt("They require no data"),
                ),
                "Many MLSFs exploit ligand or target memorisation and generalise poorly.",
            ),
            q(
                "Honest evaluation of an MLSF requires:",
                (
                    opt("Scaffold or target splits dissimilar to training", correct=True),
                    opt("Testing on the training data"),
                    opt("Removing the test set"),
                    opt("Using only one molecule"),
                ),
                "Dissimilar splits expose whether the model truly generalises.",
            ),
        ),
        "Bias, validation and applied pipelines": (
            q(
                "The most decisive test of a screening pipeline is:",
                (
                    opt(
                        "Prospective validation by experimental assay of predicted top hits",
                        correct=True,
                    ),
                    opt("Re-running the same benchmark"),
                    opt("Increasing the library size"),
                    opt("Choosing a nicer color scheme"),
                ),
                "Prospective predictions confirmed by experiment are the gold standard.",
            ),
            q(
                "Data leakage in ML virtual screening is best avoided with:",
                (
                    opt("Time-split or target-clustered train/test splits", correct=True),
                    opt("Random splits with overlapping targets"),
                    opt("No test set"),
                    opt("Larger fonts"),
                ),
                "Clustered/time splits prevent train-test overlap inflating metrics.",
            ),
            q(
                "A realistic structure-based screen can lift experimental hit rate to roughly:",
                (
                    opt("5-20% from a ~1% baseline", correct=True),
                    opt("Exactly 100%"),
                    opt("0% always"),
                    opt("Below the random baseline"),
                ),
                "Even modest accuracy yields a large practical enrichment over ~1% random.",
            ),
        ),
    },
    final=(
        q(
            "A threshold-free measure of ranking quality across all cutoffs is:",
            (
                opt("ROC AUC", correct=True),
                opt("Molecular weight"),
                opt("RMSD at 2 A"),
                opt("The number of atoms"),
            ),
            "AUC summarises the full ROC curve independent of any single threshold.",
        ),
        q(
            "The typical accuracy-vs-cost funnel for screening is:",
            (
                opt("Docking -> MM/GBSA -> FEP on progressively fewer compounds", correct=True),
                opt("FEP on everything first"),
                opt("No scoring at any stage"),
                opt("Random ranking only"),
            ),
            "Spend more expensive methods on fewer, more promising candidates.",
        ),
        q(
            "Surrogate active-learning screening helps mainly by:",
            (
                opt("Avoiding docking the entire ultra-large library", correct=True),
                opt("Removing the need for a target"),
                opt("Eliminating all false positives"),
                opt("Making molecules smaller"),
            ),
            "It triages billions so only top candidates are docked.",
        ),
        q(
            "Property-matched decoy sets such as DUD-E exist to:",
            (
                opt("Prevent trivial active/decoy separation and inflated metrics", correct=True),
                opt("Increase memorisation"),
                opt("Speed up FEP"),
                opt("Replace the receptor"),
            ),
            "Matched decoys force methods to use genuine binding signal.",
        ),
        q(
            "Graph neural networks for scoring treat a complex as:",
            (
                opt("A graph of atoms and bonds", correct=True),
                opt("A flat string of text only"),
                opt("A single number"),
                opt("An unrelated image"),
            ),
            "GNNs operate on the atom-bond graph of the protein-ligand complex.",
        ),
        q(
            "Consensus scoring improves reliability because:",
            (
                opt(
                    "Combining several functions cancels part of their independent error",
                    correct=True,
                ),
                opt("One function is always exactly right"),
                opt("It ignores poses entirely"),
                opt("It removes the need for experiments"),
            ),
            "Merging multiple scores reduces the impact of any one's errors.",
        ),
    ),
)
