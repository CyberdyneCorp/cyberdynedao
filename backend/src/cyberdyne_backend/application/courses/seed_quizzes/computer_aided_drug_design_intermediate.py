"""Quiz questions for the Computer-Aided Drug Design (CADD) - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Molecular docking": (
            q(
                "Molecular docking solves which two coupled problems?",
                (
                    opt("searching for poses and scoring them", correct=True),
                    opt("synthesis and purification"),
                    opt("crystallisation and diffraction"),
                    opt("transcription and translation"),
                ),
                "Docking samples binding poses (search) and ranks them (scoring).",
            ),
            q(
                "In standard docking the ligand and receptor are usually treated as:",
                (
                    opt("flexible ligand, mostly rigid receptor", correct=True),
                    opt("both fully rigid always"),
                    opt("ligand rigid, receptor fully flexible"),
                    opt("both ignored entirely"),
                ),
                "Ligand rotatable bonds are sampled while the receptor is often held rigid.",
            ),
            q(
                "Which is a widely used docking program?",
                (
                    opt("AutoDock Vina", correct=True),
                    opt("GROMACS only for docking"),
                    opt("Microsoft Excel"),
                    opt("BLAST"),
                ),
                "Vina, Glide and GOLD are standard docking engines.",
            ),
        ),
        "Scoring functions": (
            q(
                "Which is one of the three main families of scoring functions?",
                (
                    opt("knowledge-based (statistical potentials)", correct=True),
                    opt("sequence-alignment-based"),
                    opt("mass-spectrometry-based"),
                    opt("crystallography-based scoring only"),
                ),
                "Force-field, empirical and knowledge-based are the three families.",
            ),
            q(
                "What is consensus scoring?",
                (
                    opt(
                        "combining several scoring functions to reduce ranking error", correct=True
                    ),
                    opt("using a single perfect function"),
                    opt("scoring only the largest molecule"),
                    opt("averaging molecular weights"),
                ),
                "Multiple imperfect functions averaged together tend to rank more robustly.",
            ),
            q(
                "Scoring is often called the weakest link in docking because:",
                (
                    opt(
                        "functions find poses well but rank affinities less accurately",
                        correct=True,
                    ),
                    opt("it never finds any pose"),
                    opt("it requires no computation"),
                    opt("it always predicts affinity exactly"),
                ),
                "Pose generation is reliable; absolute affinity ranking remains hard.",
            ),
        ),
        "Pharmacophore modelling": (
            q(
                "A pharmacophore is best defined as:",
                (
                    opt(
                        "the abstract set of features needed for activity, independent of scaffold",
                        correct=True,
                    ),
                    opt("a specific atom in a specific drug"),
                    opt("the molecular weight of a ligand"),
                    opt("the crystal lattice of a protein"),
                ),
                "It captures donors, acceptors, hydrophobes and rings in a 3D arrangement.",
            ),
            q(
                "A ligand-based pharmacophore is built by:",
                (
                    opt(
                        "aligning several known actives and extracting common features",
                        correct=True,
                    ),
                    opt("sequencing the target gene"),
                    opt("running mass spectrometry on the solvent"),
                    opt("measuring the melting point"),
                ),
                "Common features across aligned actives define the ligand-based model.",
            ),
            q(
                "Loosening feature-distance tolerances tends to:",
                (
                    opt("retrieve more hits but lower selectivity", correct=True),
                    opt("retrieve fewer hits with higher selectivity"),
                    opt("have no effect on screening"),
                    opt("guarantee only true actives"),
                ),
                "Wider tolerances match more conformers, trading precision for recall.",
            ),
        ),
        "QSAR and molecular descriptors": (
            q(
                "QSAR models map which inputs to activity?",
                (
                    opt("molecular descriptors", correct=True),
                    opt("crystallisation temperatures"),
                    opt("the names of researchers"),
                    opt("the price of reagents"),
                ),
                "QSAR learns activity as a function of computed descriptors.",
            ),
            q(
                "Why is the applicability domain important in QSAR?",
                (
                    opt(
                        "predictions are unreliable for molecules outside the training space",
                        correct=True,
                    ),
                    opt("it sets the molecular weight limit"),
                    opt("it defines the synthesis route"),
                    opt("it has no effect on reliability"),
                ),
                "Models extrapolate poorly beyond the chemistry they were trained on.",
            ),
            q(
                "Using too many descriptors on too few compounds risks:",
                (
                    opt("overfitting, memorising noise", correct=True),
                    opt("perfect generalisation"),
                    opt("eliminating all error"),
                    opt("reducing the descriptor count automatically"),
                ),
                "High dimensionality with few samples leads to overfitting.",
            ),
        ),
        "Molecular dynamics simulations": (
            q(
                "Molecular dynamics integrates which physical law?",
                (
                    opt("Newton's equations of motion", correct=True),
                    opt("Ohm's law"),
                    opt("the ideal gas law only"),
                    opt("Hooke's law exclusively"),
                ),
                "MD numerically integrates F = m a using force-field gradients.",
            ),
            q(
                "What is a typical MD integration time step?",
                (
                    opt("about 2 femtoseconds", correct=True),
                    opt("about 2 seconds"),
                    opt("about 2 minutes"),
                    opt("about 2 hours"),
                ),
                "Femtosecond steps are needed to resolve fast bond vibrations.",
            ),
            q(
                "How does MD help structure-based design?",
                (
                    opt(
                        "it reveals receptor flexibility, cryptic pockets and ensembles",
                        correct=True,
                    ),
                    opt("it sequences the protein"),
                    opt("it replaces all experiments"),
                    opt("it only computes molecular weight"),
                ),
                "MD captures protein motion useful for ensemble docking and pocket discovery.",
            ),
        ),
        "Binding free-energy methods": (
            q(
                "MM-PBSA / MM-GBSA are best described as:",
                (
                    opt("end-point free-energy estimates from MD snapshots", correct=True),
                    opt("sequence alignment tools"),
                    opt("X-ray refinement programs"),
                    opt("synthesis planning software"),
                ),
                "They combine MM energy, implicit solvation and entropy over snapshots.",
            ),
            q(
                "Free-energy perturbation (FEP) is most accurate for computing:",
                (
                    opt("relative binding free energies between similar ligands", correct=True),
                    opt("absolute molecular weights"),
                    opt("the colour of a compound"),
                    opt("DNA sequences"),
                ),
                "Alchemical FEP/TI excel at relative ddG between congeneric ligands.",
            ),
            q(
                "In thermodynamic integration, delta G is obtained by:",
                (
                    opt("integrating the ensemble average of dU/dlambda over lambda", correct=True),
                    opt("counting heavy atoms"),
                    opt("measuring the boiling point"),
                    opt("summing molecular weights"),
                ),
                "TI integrates <dU/dlambda> from lambda 0 to 1 to give the free-energy change.",
            ),
        ),
    },
    final=(
        q(
            "The central computational challenge in docking search is:",
            (
                opt("combinatorial explosion of ligand conformations", correct=True),
                opt("a shortage of scoring functions"),
                opt("the lack of any binding site"),
                opt("excessive solubility"),
            ),
            "Conformational space grows rapidly with rotatable bonds.",
        ),
        q(
            "Which best describes empirical scoring functions?",
            (
                opt("weighted terms fitted to experimental affinities", correct=True),
                opt("pure quantum-mechanical calculations only"),
                opt("random number generators"),
                opt("sequence similarity scores"),
            ),
            "Empirical functions fit interpretable terms to measured binding data.",
        ),
        q(
            "A 3D pharmacophore query is used to:",
            (
                opt("screen databases for molecules matching key features", correct=True),
                opt("determine the protein's amino-acid sequence"),
                opt("measure plasma half-life"),
                opt("calculate the boiling point"),
            ),
            "It retrieves compounds whose conformers fit the feature geometry.",
        ),
        q(
            "Proper QSAR validation includes:",
            (
                opt("cross-validated q2 and external test-set R2", correct=True),
                opt("only fitting the training set"),
                opt("ignoring any test data"),
                opt("reporting molecular weight alone"),
            ),
            "Internal and external validation guard against overfitting.",
        ),
        q(
            "Why run molecular dynamics before or after docking?",
            (
                opt("to account for protein flexibility and refine complexes", correct=True),
                opt("to determine the gene sequence"),
                opt("to weigh the protein"),
                opt("to remove the need for any force field"),
            ),
            "MD relaxes complexes and samples conformations docking misses.",
        ),
        q(
            "Which method is considered the gold standard for relative affinity ranking?",
            (
                opt("alchemical FEP / TI", correct=True),
                opt("simple 2D similarity"),
                opt("molecular weight comparison"),
                opt("counting hydrogen bonds by hand"),
            ),
            "Alchemical free-energy methods can reach roughly 1 kcal/mol accuracy.",
        ),
    ),
)
