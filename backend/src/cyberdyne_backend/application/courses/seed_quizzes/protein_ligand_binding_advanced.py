"""Quiz questions for the Protein-Ligand Binding & Free-Energy Methods - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Free-energy perturbation (FEP)": (
            q(
                "The Zwanzig equation computes ΔG between two states from:",
                (
                    opt(
                        "The exponential average of the energy difference sampled from one state",
                        correct=True,
                    ),
                    opt("The arithmetic mean of atomic masses"),
                    opt("A single docking score"),
                    opt("The molecular weight ratio"),
                ),
                "ΔG = -RT ln <exp(-(H_B - H_A)/RT)>_A, averaged over state A.",
            ),
            q(
                "Why are intermediate lambda windows inserted in FEP?",
                (
                    opt(
                        "To ensure neighbouring states overlap in phase space for reliable estimates",
                        correct=True,
                    ),
                    opt("To increase the molecular weight"),
                    opt("To remove the need for a force field"),
                    opt("To eliminate sampling entirely"),
                ),
                "Without overlap the exponential average is biased; windows bridge the gap.",
            ),
            q(
                "Poor overlap between two states in FEP leads to:",
                (
                    opt("Biased estimates dominated by a few rare snapshots", correct=True),
                    opt("Perfectly accurate results"),
                    opt("Faster convergence"),
                    opt("Lower computational cost with no downside"),
                ),
                "If B's important configurations are rare under A, the estimate is unreliable.",
            ),
        ),
        "Thermodynamic integration": (
            q(
                "Thermodynamic integration computes ΔG by:",
                (
                    opt(
                        "Integrating the ensemble average of the Hamiltonian derivative over lambda",
                        correct=True,
                    ),
                    opt("Taking a single exponential average"),
                    opt("Counting hydrogen bonds"),
                    opt("Measuring molecular weight"),
                ),
                "ΔG = integral over lambda of <dH/dlambda>_lambda.",
            ),
            q(
                "Soft-core potentials are used in alchemical transformations to:",
                (
                    opt(
                        "Avoid singularities when atoms appear or disappear near the endpoints",
                        correct=True,
                    ),
                    opt("Increase electrostatic repulsion to infinity"),
                    opt("Make the ligand heavier"),
                    opt("Disable van der Waals forces permanently"),
                ),
                "Soft-core scaling smoothly removes interactions so endpoint terms stay finite.",
            ),
            q(
                "TI and FEP are best described as:",
                (
                    opt("Two views of the same alchemical lambda path", correct=True),
                    opt("Completely unrelated methods"),
                    opt("Methods that ignore the force field"),
                    opt("Docking algorithms"),
                ),
                "They share the lambda path; the estimator choice often matters more than TI vs FEP.",
            ),
        ),
        "BAR, MBAR and convergence": (
            q(
                "What advantage does BAR have over one-directional Zwanzig averaging?",
                (
                    opt(
                        "It combines forward and reverse sampling for minimum-variance estimates",
                        correct=True,
                    ),
                    opt("It ignores half of the data"),
                    opt("It requires no simulation"),
                    opt("It works only at zero temperature"),
                ),
                "BAR optimally fuses forward and reverse work between two states.",
            ),
            q(
                "How does the statistical error of a free-energy estimate scale with uncorrelated samples N?",
                (
                    opt("Roughly as 1/sqrt(N)", correct=True),
                    opt("As N squared"),
                    opt("Linearly with N"),
                    opt("Independent of N"),
                ),
                "Halving the error requires about four times the sampling.",
            ),
            q(
                "Which diagnostic helps confirm FEP convergence?",
                (
                    opt("The MBAR overlap matrix and forward/reverse hysteresis", correct=True),
                    opt("The molecular weight of the ligand"),
                    opt("The number of carbon atoms"),
                    opt("The color of the simulation box"),
                ),
                "Overlap and hysteresis reveal whether windows and sampling are adequate.",
            ),
        ),
        "Absolute binding free energy with restraints": (
            q(
                "Why are restraints (e.g. Boresch restraints) needed in absolute binding free-energy calculations?",
                (
                    opt(
                        "To keep the decoupling ligand in place as its interactions vanish",
                        correct=True,
                    ),
                    opt("To speed up integration by removing the force field"),
                    opt("To increase the molecular weight"),
                    opt("To break covalent bonds"),
                ),
                "Without restraints the decoupled ligand drifts away and the integral diverges.",
            ),
            q(
                "The double-decoupling method computes ΔG_bind by decoupling the ligand in:",
                (
                    opt(
                        "Both the binding site and bulk solvent, then taking the difference",
                        correct=True,
                    ),
                    opt("The binding site only"),
                    opt("Bulk solvent only"),
                    opt("Neither environment"),
                ),
                "DDM uses a thermodynamic cycle over site and solvent decoupling legs.",
            ),
            q(
                "The known analytical free energy of the restraints is:",
                (
                    opt(
                        "Subtracted via the thermodynamic cycle to recover the true ΔG_bind",
                        correct=True,
                    ),
                    opt("Ignored entirely"),
                    opt("Added to the molecular weight"),
                    opt("Used to define the force field"),
                ),
                "The restraint contribution is corrected analytically, with a standard-state term.",
            ),
        ),
        "Enhanced sampling methods": (
            q(
                "What does metadynamics do to escape free-energy wells?",
                (
                    opt(
                        "Deposits a history-dependent bias along collective variables", correct=True
                    ),
                    opt("Lowers the temperature to zero"),
                    opt("Removes all atoms from the system"),
                    opt("Freezes the protein rigidly"),
                ),
                "Accumulating Gaussian bias fills wells and reconstructs the free-energy surface.",
            ),
            q(
                "Replica exchange accelerates sampling by:",
                (
                    opt(
                        "Swapping configurations between replicas at different temperatures or lambda values",
                        correct=True,
                    ),
                    opt("Deleting high-energy configurations"),
                    opt("Running a single short simulation"),
                    opt("Disabling the thermostat"),
                ),
                "High-temperature (or different-lambda) replicas cross barriers and pass states down.",
            ),
            q(
                "Umbrella sampling recovers the potential of mean force by:",
                (
                    opt(
                        "Restraining a collective variable to overlapping windows and recombining with WHAM",
                        correct=True,
                    ),
                    opt("Using a single unbiased trajectory"),
                    opt("Counting atoms"),
                    opt("Measuring molecular weight"),
                ),
                "Biased windows are unbiased and stitched together (e.g. via WHAM) into the PMF.",
            ),
        ),
        "Machine learning for affinity prediction": (
            q(
                "What is the central caveat when evaluating ML scoring models?",
                (
                    opt(
                        "They may memorise the protein or ligand instead of learning the interaction",
                        correct=True,
                    ),
                    opt("They are always slower than FEP"),
                    opt("They cannot use any structural data"),
                    opt("They require breaking covalent bonds"),
                ),
                "Generalisation is the key risk; honest tests need scaffold- and target-split sets.",
            ),
            q(
                "How are graph neural networks applied to protein-ligand affinity?",
                (
                    opt(
                        "By treating the complex as a graph of atoms and contacts to learn interaction features",
                        correct=True,
                    ),
                    opt("By ignoring all structural information"),
                    opt("By solving the Schrodinger equation exactly"),
                    opt("By measuring only molecular weight"),
                ),
                "GNNs learn directly from the atom-and-bond graph of the complex.",
            ),
            q(
                "How is ML best combined with rigorous FEP in a campaign?",
                (
                    opt(
                        "Use cheap ML to prioritise candidates, then run FEP on the most informative ones (active learning)",
                        correct=True,
                    ),
                    opt("Replace all physics-based methods entirely"),
                    opt("Use ML only after the drug is approved"),
                    opt("Avoid ML because it is always wrong"),
                ),
                "Active learning triages large libraries, reserving expensive FEP for promising compounds.",
            ),
        ),
    },
    final=(
        q(
            "The Zwanzig (FEP) equation requires which condition to be reliable?",
            (
                opt("Phase-space overlap between the two states", correct=True),
                opt("Identical molecular weights"),
                opt("Zero temperature"),
                opt("No force field"),
            ),
            "Poor overlap biases the exponential average; windows restore overlap.",
        ),
        q(
            "Thermodynamic integration integrates which quantity over lambda?",
            (
                opt("The ensemble average of dH/dlambda", correct=True),
                opt("The molecular weight"),
                opt("The number of atoms"),
                opt("A single docking score"),
            ),
            "TI integrates <dH/dlambda> across the alchemical path.",
        ),
        q(
            "MBAR is preferred over single-direction averaging because it:",
            (
                opt(
                    "Uses all windows together for minimum-variance estimates with error bars",
                    correct=True,
                ),
                opt("Ignores most of the data"),
                opt("Requires no sampling"),
                opt("Works only for a single state"),
            ),
            "Multistate BAR extracts maximal information and rigorous uncertainties.",
        ),
        q(
            "Absolute binding free energy calculations use restraints to:",
            (
                opt(
                    "Hold the ligand in the pocket as its interactions are switched off",
                    correct=True,
                ),
                opt("Add mass to the protein"),
                opt("Break the thermodynamic cycle"),
                opt("Disable solvation"),
            ),
            "Boresch restraints prevent divergence; their analytic free energy is corrected out.",
        ),
        q(
            "Enhanced-sampling methods are needed because:",
            (
                opt(
                    "Slow motions can be missed in short simulations, biasing free energies",
                    correct=True,
                ),
                opt("Force fields are exact"),
                opt("Entropy is always zero"),
                opt("Sampling is never a problem"),
            ),
            "Sidechain flips, loop motions and water exchange need accelerated barrier crossing.",
        ),
        q(
            "The safest role for ML affinity models in a real campaign is to:",
            (
                opt("Prioritise compounds for rigorous FEP or experimental testing", correct=True),
                opt("Fully replace experiments and physics"),
                opt("Be ignored entirely"),
                opt("Set the standard-state concentration"),
            ),
            "Generalisation limits make ML best for triage, not as a final arbiter.",
        ),
    ),
)
