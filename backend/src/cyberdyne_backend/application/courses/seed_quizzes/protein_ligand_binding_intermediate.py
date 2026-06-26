"""Quiz questions for the Protein-Ligand Binding & Free-Energy Methods - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Statistical mechanics of binding": (
            q(
                "The binding constant is fundamentally a ratio of:",
                (
                    opt(
                        "Configuration integrals (partition functions) of the bound and unbound states",
                        correct=True,
                    ),
                    opt("Single minimum-energy structures only"),
                    opt("Molecular weights"),
                    opt("Atom counts"),
                ),
                "ΔG depends on the free energy of each ensemble, not a single pose.",
            ),
            q(
                "According to the Boltzmann factor, higher-energy configurations:",
                (
                    opt(
                        "Are less populated but still contribute, especially if numerous",
                        correct=True,
                    ),
                    opt("Never contribute at all"),
                    opt("Are the most populated states"),
                    opt("Have negative probability"),
                ),
                "Population scales as exp(-E/kT); rare high-energy states can still matter collectively.",
            ),
            q(
                "Why is the standard-state term needed in the binding free energy?",
                (
                    opt(
                        "To reference the result to a defined concentration such as 1 M",
                        correct=True,
                    ),
                    opt("To convert energy to mass"),
                    opt("To remove temperature dependence"),
                    opt("To count the atoms in the ligand"),
                ),
                "The 1 M standard state fixes the reference concentration for ΔG°.",
            ),
        ),
        "Molecular mechanics force fields": (
            q(
                "Which terms in an MM force field dominate the protein-ligand interaction energy?",
                (
                    opt("Non-bonded electrostatic and van der Waals terms", correct=True),
                    opt("Only bond-stretching terms"),
                    opt("Only angle-bending terms"),
                    opt("Only dihedral terms"),
                ),
                "Intermolecular contacts are captured mainly by the non-bonded terms.",
            ),
            q(
                "Which is a common general force field for small-molecule ligands?",
                (
                    opt("GAFF (General AMBER Force Field)", correct=True),
                    opt("BLOSUM62"),
                    opt("PAM250"),
                    opt("FASTA"),
                ),
                "GAFF and CGenFF parameterise drug-like ligands for AMBER/CHARMM.",
            ),
            q(
                "A key limitation of classical fixed-charge force fields is that they:",
                (
                    opt("Omit electronic polarisation and cannot break bonds", correct=True),
                    opt("Are too slow to run any simulation"),
                    opt("Cannot represent van der Waals forces"),
                    opt("Require quantum hardware"),
                ),
                "Fixed partial charges miss polarisation; reactive chemistry needs QM or ML potentials.",
            ),
        ),
        "Scoring functions and their limits": (
            q(
                "Which scoring-function family uses statistical potentials from observed PDB contact frequencies?",
                (
                    opt("Knowledge-based", correct=True),
                    opt("Force-field based"),
                    opt("Empirical fitted"),
                    opt("Quantum mechanical"),
                ),
                "Knowledge-based potentials (e.g. DrugScore, PMF) derive from contact statistics.",
            ),
            q(
                "Docking scoring functions are generally better at:",
                (
                    opt("Pose prediction than at accurate affinity ranking", correct=True),
                    opt("Affinity ranking than at pose prediction"),
                    opt("Both equally and perfectly"),
                    opt("Neither task at all"),
                ),
                "They place ligands well but rank affinities poorly due to neglected entropy and solvent.",
            ),
            q(
                "Why do scoring functions correlate only modestly with measured affinity?",
                (
                    opt(
                        "They neglect entropy, treat solvent crudely, and use one conformation",
                        correct=True,
                    ),
                    opt("They use exact quantum free energies"),
                    opt("They sample every configuration rigorously"),
                    opt("They include full explicit-solvent thermodynamics"),
                ),
                "These approximations are the price of speed, motivating rescoring and FEP.",
            ),
        ),
        "MM/PBSA and MM/GBSA end-point methods": (
            q(
                "What is the difference between MM/PBSA and MM/GBSA?",
                (
                    opt(
                        "PBSA uses Poisson-Boltzmann; GBSA uses the faster Generalized Born approximation",
                        correct=True,
                    ),
                    opt("GBSA breaks covalent bonds; PBSA does not"),
                    opt("PBSA ignores electrostatics entirely"),
                    opt("They are identical in every way"),
                ),
                "The polar solvation term distinguishes them; GB is a fast approximation to PB.",
            ),
            q(
                "End-point methods estimate ΔG_bind from:",
                (
                    opt(
                        "Only the complex and free-partner end states, with no alchemical path",
                        correct=True,
                    ),
                    opt("A full alchemical lambda path"),
                    opt("A single docking pose with no simulation"),
                    opt("Quantum dynamics of the whole cell"),
                ),
                "They combine MM energy, implicit solvation and entropy at the two physical end states.",
            ),
            q(
                "The nonpolar solvation term in MM/PBSA is usually taken proportional to:",
                (
                    opt("Buried solvent-accessible surface area", correct=True),
                    opt("The number of hydrogen-bond donors only"),
                    opt("Molecular weight"),
                    opt("Net formal charge"),
                ),
                "A surface-tension coefficient times buried SASA captures the hydrophobic term.",
            ),
        ),
        "Entropy estimation in binding": (
            q(
                "Which method estimates configurational entropy by diagonalising the mass-weighted Hessian?",
                (
                    opt("Normal-mode analysis (NMA)", correct=True),
                    opt("Poisson-Boltzmann"),
                    opt("Docking"),
                    opt("Cheng-Prusoff"),
                ),
                "NMA sums harmonic-oscillator entropies of the vibrational modes.",
            ),
            q(
                "On binding, the ligand typically loses which entropy?",
                (
                    opt("Translational and rotational entropy", correct=True),
                    opt("Nuclear spin entropy primarily"),
                    opt("It gains translational entropy"),
                    opt("No entropy change occurs"),
                ),
                "Confining the ligand in the pocket costs translational and rotational freedom.",
            ),
            q(
                "Why do practitioners sometimes drop -TΔS when ranking congeneric ligands in MM/GBSA?",
                (
                    opt(
                        "They assume the noisy entropy term largely cancels between similar ligands",
                        correct=True,
                    ),
                    opt("Because entropy is always exactly zero"),
                    opt("Because entropy raises affinity infinitely"),
                    opt("Because entropy is forbidden by thermodynamics"),
                ),
                "The shortcut works for similar ligands but fails when flexibility differs.",
            ),
        ),
        "The thermodynamic cycle": (
            q(
                "Why can a thermodynamic cycle replace a hard physical process with an unphysical path?",
                (
                    opt(
                        "Free energy is a state function depending only on the end states",
                        correct=True,
                    ),
                    opt("Because energy is not conserved"),
                    opt("Because paths never matter for any quantity"),
                    opt("Because entropy is ignored"),
                ),
                "State functions depend only on endpoints, so any closed path gives the same ΔG.",
            ),
            q(
                "In the relative binding cycle, ΔΔG between ligands A and B equals:",
                (
                    opt(
                        "The difference of the alchemical mutation legs in complex and in solvent",
                        correct=True,
                    ),
                    opt("The sum of all four legs"),
                    opt("Half the absolute binding energy of A"),
                    opt("The molecular weight difference"),
                ),
                "Closing the loop gives ΔΔG = ΔG_mut,complex - ΔG_mut,solvent.",
            ),
            q(
                "What is the practical advantage of computing the alchemical legs instead of absolute binding?",
                (
                    opt(
                        "Transforming A into B is far easier to sample than the full binding event",
                        correct=True,
                    ),
                    opt("It removes the need for any simulation"),
                    opt("It eliminates the need for a force field"),
                    opt("It makes entropy exactly computable"),
                ),
                "Small A-to-B perturbations sample better than a ligand fully leaving the pocket.",
            ),
        ),
    },
    final=(
        q(
            "The rigorous binding free energy depends on:",
            (
                opt("The free energy of each ensemble, not a single pose", correct=True),
                opt("Only the lowest-energy structure"),
                opt("Only the molecular weight"),
                opt("Only the number of atoms"),
            ),
            "Statistical mechanics defines ΔG from partition functions over ensembles.",
        ),
        q(
            "In an MM force field, protein-ligand affinity is captured mainly by:",
            (
                opt("Non-bonded electrostatic and van der Waals terms", correct=True),
                opt("Bond-stretch terms only"),
                opt("Angle terms only"),
                opt("Dihedral terms only"),
            ),
            "Intermolecular contacts come from the non-bonded interactions.",
        ),
        q(
            "Docking scoring functions are weakest at:",
            (
                opt("Accurate absolute affinity ranking", correct=True),
                opt("Placing the ligand in roughly the right pose"),
                opt("Running quickly"),
                opt("Handling many candidate molecules"),
            ),
            "Neglected entropy and crude solvent treatment hurt affinity prediction most.",
        ),
        q(
            "MM/GBSA differs from MM/PBSA in its treatment of:",
            (
                opt("Polar solvation (Generalized Born vs Poisson-Boltzmann)", correct=True),
                opt("Bond connectivity"),
                opt("Atom masses"),
                opt("Temperature units"),
            ),
            "GB is a faster approximation to the PB polar solvation free energy.",
        ),
        q(
            "Configurational entropy in binding is hardest because:",
            (
                opt(
                    "Estimators like NMA and quasi-harmonic analysis are noisy and expensive",
                    correct=True,
                ),
                opt("Entropy is always zero"),
                opt("Entropy is trivial to compute exactly"),
                opt("Entropy does not affect ΔG"),
            ),
            "Entropy is decisive yet difficult, so it is often approximated or dropped.",
        ),
        q(
            "The thermodynamic cycle is useful because free energy:",
            (
                opt("Is a state function, so only the end states matter", correct=True),
                opt("Changes with the chosen path"),
                opt("Cannot be computed at all"),
                opt("Depends only on temperature"),
            ),
            "Path independence lets us substitute easy alchemical legs for hard physical ones.",
        ),
    ),
)
