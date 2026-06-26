"""Quiz questions for the Molecular Docking & Virtual Screening - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Scoring functions: families and form": (
            q(
                "Which scoring family derives pairwise potentials from observed PDB distances?",
                (
                    opt("Knowledge-based (statistical potentials)", correct=True),
                    opt("Force-field based"),
                    opt("Empirical regression"),
                    opt("Random sampling"),
                ),
                "Knowledge-based scores use atom-pair statistics from known structures.",
            ),
            q(
                "The Lennard-Jones potential models which interaction?",
                (
                    opt("Van der Waals attraction and short-range repulsion", correct=True),
                    opt("Covalent bond breaking"),
                    opt("Solvent pH"),
                    opt("Gene expression"),
                ),
                "LJ captures vdW: attractive at medium range, steeply repulsive on clash.",
            ),
            q(
                "Empirical scoring functions get their term weights from:",
                (
                    opt("Fitting to experimental affinity data", correct=True),
                    opt("Random guesses"),
                    opt("Protein sequence only"),
                    opt("The PDB header text"),
                ),
                "Empirical scores regress weighted terms against measured affinities.",
            ),
        ),
        "Search algorithms for pose space": (
            q(
                "Rigid placement of a ligand in a pocket is how many dimensional?",
                (
                    opt("6 (3 translation + 3 rotation)", correct=True),
                    opt("1"),
                    opt("100"),
                    opt("0"),
                ),
                "Position and orientation give six rigid-body degrees of freedom.",
            ),
            q(
                "Which is a stochastic search method used in docking?",
                (
                    opt("Genetic algorithm / Monte Carlo", correct=True),
                    opt("Exhaustive enumeration of all poses"),
                    opt("Gel electrophoresis"),
                    opt("Mass spectrometry"),
                ),
                "GOLD/AutoDock use genetic algorithms; Vina uses a Monte Carlo variant.",
            ),
            q(
                "The Metropolis criterion lets a search accept a worse pose to:",
                (
                    opt("Escape local minima", correct=True),
                    opt("Guarantee the global minimum instantly"),
                    opt("Avoid scoring entirely"),
                    opt("Stop the search"),
                ),
                "Accepting some uphill moves prevents getting trapped in local minima.",
            ),
        ),
        "Modelling flexibility": (
            q(
                "Soft docking improves tolerance to small clashes by:",
                (
                    opt("Softening the repulsive van der Waals wall", correct=True),
                    opt("Deleting the ligand"),
                    opt("Removing all hydrogen bonds"),
                    opt("Freezing the temperature"),
                ),
                "Soft docking dampens the steep repulsion to mimic minor side-chain give.",
            ),
            q(
                "Ensemble docking handles receptor flexibility by:",
                (
                    opt("Docking against several receptor conformations", correct=True),
                    opt("Using a single rigid structure only"),
                    opt("Ignoring the receptor"),
                    opt("Randomising atom elements"),
                ),
                "Ensemble docking uses multiple snapshots (crystal/NMR/MD) and keeps the best.",
            ),
            q(
                "Side-chain flexibility is commonly sampled using:",
                (
                    opt("Rotamer libraries", correct=True),
                    opt("Codon tables"),
                    opt("BLAST hits"),
                    opt("Buffer recipes"),
                ),
                "Selected pocket residues sample discrete rotamers from a library.",
            ),
        ),
        "Pose validation and metrics": (
            q(
                "Re-docking validation measures success primarily by:",
                (
                    opt("RMSD of the top pose to the crystal pose", correct=True),
                    opt("The molecule's molecular weight"),
                    opt("The number of atoms"),
                    opt("The protein's pI"),
                ),
                "Re-docking checks geometric agreement via RMSD, usually under 2 A.",
            ),
            q(
                "An interaction fingerprint encodes:",
                (
                    opt("Which contacts (H-bond, hydrophobic, ionic) a pose makes", correct=True),
                    opt("The DNA sequence"),
                    opt("The assay temperature"),
                    opt("The pixel colors of a render"),
                ),
                "IFPs are bit vectors of contact types for comparing binding modes.",
            ),
            q(
                "Why can clustering poses beat taking the single best score?",
                (
                    opt("The best-scoring pose is not always the most native-like", correct=True),
                    opt("Clustering is required by law"),
                    opt("Scores are always exactly correct"),
                    opt("Poses never recur"),
                ),
                "Score-RMSD discordance means a populated cluster is often more reliable.",
            ),
        ),
        "From single docking to screening": (
            q(
                "The main goal of virtual screening is:",
                (
                    opt("Enrichment: getting true binders to the top of the ranking", correct=True),
                    opt("Perfect absolute affinity for every molecule"),
                    opt("Synthesising every compound"),
                    opt("Sequencing the library"),
                ),
                "VS prioritises a few candidates; enrichment, not perfect affinity, matters.",
            ),
            q(
                "Lipinski's rule of five is used as a:",
                (
                    opt("Physicochemical filter before docking", correct=True),
                    opt("Scoring function"),
                    opt("Search algorithm"),
                    opt("Crystallisation method"),
                ),
                "Rule-of-five filters prune drug-unlikely chemistry cheaply.",
            ),
            q(
                "The enrichment factor at the top x% compares:",
                (
                    opt("The hit rate there to random selection", correct=True),
                    opt("Two proteins' sequences"),
                    opt("The assay pH to 7"),
                    opt("Atom counts of decoys"),
                ),
                "EF measures how much more concentrated actives are versus random.",
            ),
        ),
    },
    final=(
        q(
            "Which scoring family learns its mapping from data rather than a fixed form?",
            (
                opt("Machine-learning scoring", correct=True),
                opt("Force-field based"),
                opt("Knowledge-based"),
                opt("Empirical regression"),
            ),
            "ML scoring functions learn affinity from descriptors and examples.",
        ),
        q(
            "Flexible-ligand docking, versus rigid, primarily increases:",
            (
                opt("The dimensionality of the search", correct=True),
                opt("The molecular weight"),
                opt("The crystal resolution"),
                opt("The protein's charge"),
            ),
            "Each sampled torsion adds a dimension to the search space.",
        ),
        q(
            "A good virtual screen's cumulative-actives curve relative to random is:",
            (
                opt("Above the diagonal (finds actives early)", correct=True),
                opt("Below the diagonal"),
                opt("Exactly the diagonal"),
                opt("A vertical line at the end"),
            ),
            "Enriched screens recover actives faster than random selection.",
        ),
        q(
            "Simulated annealing and genetic algorithms are examples of:",
            (
                opt("Stochastic search methods", correct=True),
                opt("Scoring functions"),
                opt("File formats"),
                opt("Crystallisation buffers"),
            ),
            "They are stochastic samplers of pose space.",
        ),
        q(
            "PAINS substructure filtering is done to:",
            (
                opt("Remove promiscuous/reactive compounds before docking", correct=True),
                opt("Add hydrogens to the receptor"),
                opt("Increase the library size"),
                opt("Compute the ROC curve"),
            ),
            "PAINS filters drop frequent false-positive chemotypes.",
        ),
        q(
            "The conventional RMSD threshold for a correct re-docked pose is:",
            (
                opt("About 2 Angstrom", correct=True),
                opt("About 10 Angstrom"),
                opt("0 exactly"),
                opt("Any value"),
            ),
            "Two angstrom is the standard pose-prediction success cutoff.",
        ),
    ),
)
