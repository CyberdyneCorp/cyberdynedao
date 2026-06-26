"""Quiz questions for the Molecular Modeling & Visualization - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Energy minimization algorithms": (
            q(
                "Energy minimization finds:",
                (
                    opt("the nearest local minimum, not necessarily the global one", correct=True),
                    opt("always the global minimum"),
                    opt("a transition state"),
                    opt("the highest-energy structure"),
                ),
                "Minimization moves downhill without crossing barriers, so it lands in a local minimum.",
            ),
            q(
                "Steepest descent is best described as:",
                (
                    opt("robust far from a minimum but slow near it", correct=True),
                    opt("fast near a minimum but unstable far away"),
                    opt("a method that uses the full Hessian"),
                    opt("a conformational search method"),
                ),
                "Steepest descent follows the negative gradient: robust but zig-zags slowly near a minimum.",
            ),
            q(
                "Which quasi-Newton method uses curvature for fast convergence?",
                (
                    opt("L-BFGS", correct=True),
                    opt("Gasteiger"),
                    opt("ETKDG"),
                    opt("Monte Carlo"),
                ),
                "L-BFGS approximates the Hessian for fast convergence near a minimum.",
            ),
        ),
        "Conformational search and sampling": (
            q(
                "Why is exhaustive systematic conformer search often infeasible?",
                (
                    opt("the count grows exponentially with rotatable bonds", correct=True),
                    opt("conformers all have the same energy"),
                    opt("torsions cannot rotate"),
                    opt("RMSD cannot be computed"),
                ),
                "With m rotatable bonds and k states each there are about k^m candidates.",
            ),
            q(
                "RDKit's ETKDG generates 3D conformers using:",
                (
                    opt("distance geometry from connectivity", correct=True),
                    opt("X-ray diffraction"),
                    opt("the Henderson-Hasselbalch equation"),
                    opt("Particle Mesh Ewald"),
                ),
                "ETKDG is a distance-geometry embedding method with experimental torsion knowledge.",
            ),
            q(
                "After generating candidates, duplicates are removed by:",
                (
                    opt("clustering by RMSD", correct=True),
                    opt("sorting by atom name"),
                    opt("counting hydrogen bonds only"),
                    opt("checking the file format"),
                ),
                "Conformers are minimized and clustered by RMSD to discard duplicates.",
            ),
        ),
        "Boltzmann populations of conformers": (
            q(
                "The Boltzmann probability of a conformer is proportional to:",
                (
                    opt("exp(-E / kT)", correct=True),
                    opt("E / kT"),
                    opt("exp(+E / kT)"),
                    opt("1 / E"),
                ),
                "p_i is proportional to exp(-E_i/kT), normalized by the partition function.",
            ),
            q(
                "At room temperature, kT is approximately:",
                (
                    opt("0.59 kcal/mol", correct=True),
                    opt("59 kcal/mol"),
                    opt("0 kcal/mol"),
                    opt("1000 kcal/mol"),
                ),
                "kT at ~298 K is about 0.59 kcal/mol (about 2.5 kJ/mol).",
            ),
            q(
                "Strictly, conformer populations are governed by:",
                (
                    opt("free energy, which includes entropy", correct=True),
                    opt("potential energy alone, always"),
                    opt("bond length only"),
                    opt("the number of atoms only"),
                ),
                "Populations depend on free energy G, which adds an entropic term to the energy.",
            ),
        ),
        "Partial charges and protonation states": (
            q(
                "Which partial-charge scheme fits charges to a QM electrostatic potential?",
                (
                    opt("RESP", correct=True),
                    opt("Gasteiger"),
                    opt("Lennard-Jones"),
                    opt("Ramachandran"),
                ),
                "RESP fits charges to a quantum ESP and is considered the gold standard.",
            ),
            q(
                "A residue is half-ionized when:",
                (
                    opt("the pH equals its pKa", correct=True),
                    opt("the pH is far below its pKa"),
                    opt("the temperature is zero"),
                    opt("it has no charge at all"),
                ),
                "Henderson-Hasselbalch gives 50% ionization when pH = pKa.",
            ),
            q(
                "Which residue's protonation state is most often ambiguous near physiological pH?",
                (
                    opt("Histidine (pKa ~ 6)", correct=True),
                    opt("Alanine"),
                    opt("Glycine"),
                    opt("Leucine"),
                ),
                "Histidine's pKa near 6 makes its charge/tautomer state ambiguous at pH ~7.4.",
            ),
        ),
        "Solvation models": (
            q(
                "Explicit solvent models such as TIP3P represent water as:",
                (
                    opt("actual water molecules in a periodic box", correct=True),
                    opt("a uniform continuum dielectric"),
                    opt("a single point charge on the solute"),
                    opt("no water at all"),
                ),
                "Explicit models place real water molecules (TIP3P, SPC/E, etc.) around the solute.",
            ),
            q(
                "Generalized Born (GB) is best described as:",
                (
                    opt(
                        "a cheap approximation to Poisson-Boltzmann implicit solvation",
                        correct=True,
                    ),
                    opt("an explicit-water model"),
                    opt("a docking program"),
                    opt("a partial-charge scheme"),
                ),
                "GB approximates the rigorous Poisson-Boltzmann continuum electrostatics at lower cost.",
            ),
            q(
                "In water (dielectric ~80), charge-charge interactions are:",
                (
                    opt("strongly screened compared with vacuum", correct=True),
                    opt("stronger than in vacuum"),
                    opt("completely unchanged"),
                    opt("repulsive only"),
                ),
                "A high dielectric screens electrostatics roughly as 1/(epsilon r).",
            ),
        ),
        "Model quality and geometry validation": (
            q(
                "Clashscore measures:",
                (
                    opt("severe van der Waals overlaps between atoms", correct=True),
                    opt("the number of hydrogen bonds"),
                    opt("sequence identity to a template"),
                    opt("the partition function"),
                ),
                "Clashscore counts steric clashes (bad vdW overlaps) per atoms.",
            ),
            q(
                "A Ramachandran plot in validation checks whether:",
                (
                    opt("backbone phi/psi angles fall in favoured regions", correct=True),
                    opt("partial charges sum to zero"),
                    opt("the box is large enough"),
                    opt("the MSA is deep enough"),
                ),
                "It flags backbone conformations that are sterically improbable.",
            ),
            q(
                "Which tool is commonly used for model geometry validation?",
                (
                    opt("MolProbity", correct=True),
                    opt("AutoDock Vina"),
                    opt("BLAST"),
                    opt("GROMACS production run"),
                ),
                "MolProbity (and PROCHECK, WHAT_CHECK) validate geometry against known statistics.",
            ),
        ),
    },
    final=(
        q(
            "Energy minimization stops when:",
            (
                opt("the RMS gradient and energy change fall below tolerances", correct=True),
                opt("the global minimum is provably reached"),
                opt("all barriers have been crossed"),
                opt("the temperature reaches zero"),
            ),
            "Convergence is judged by the gradient norm and energy change reaching set tolerances.",
        ),
        q(
            "The number of candidate conformers grows ___ with rotatable bonds.",
            (
                opt("exponentially", correct=True),
                opt("linearly"),
                opt("inversely"),
                opt("not at all"),
            ),
            "About k^m candidates for m rotatable bonds with k states each.",
        ),
        q(
            "A conformer about 1.4 kcal/mol above the minimum is roughly:",
            (
                opt("ten-fold less populated at room temperature", correct=True),
                opt("equally populated"),
                opt("ten-fold more populated"),
                opt("the global minimum"),
            ),
            "exp(-1.4/0.59) is about 0.1, so roughly ten-fold less populated.",
        ),
        q(
            "AM1-BCC charges are commonly used because they:",
            (
                opt("are a fast standard for ligands in AMBER/GAFF", correct=True),
                opt("require no structure at all"),
                opt("are the most expensive QM method"),
                opt("only work for water"),
            ),
            "AM1-BCC is the GAFF/AMBER default partial-charge scheme for small-molecule ligands.",
        ),
        q(
            "MM/GBSA is used to estimate:",
            (
                opt("binding free energies", correct=True),
                opt("sequence identity"),
                opt("X-ray resolution"),
                opt("the number of rotatable bonds"),
            ),
            "MM/GBSA (and MM/PBSA) combine MM energies with implicit solvation to estimate binding.",
        ),
        q(
            "A model can minimize to low energy yet still be wrong because:",
            (
                opt("low energy does not guarantee correct geometry/validation", correct=True),
                opt("low energy always means correct geometry"),
                opt("validation is unnecessary"),
                opt("force fields are exact"),
            ),
            "Geometry validation (Ramachandran, clashscore, rotamers) is needed beyond low energy.",
        ),
    ),
)
