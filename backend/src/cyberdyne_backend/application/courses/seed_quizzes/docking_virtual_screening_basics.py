"""Quiz questions for the Molecular Docking & Virtual Screening - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What molecular recognition means": (
            q(
                "What does molecular docking primarily predict?",
                (
                    opt("How a ligand binds a target and how strongly", correct=True),
                    opt("The protein's amino acid sequence"),
                    opt("The melting point of a crystal"),
                    opt("The gene that encodes the protein"),
                ),
                "Docking predicts the binding pose and a score reflecting binding strength.",
            ),
            q(
                "Which interaction drives non-polar surfaces to associate by releasing ordered water?",
                (
                    opt("The hydrophobic effect", correct=True),
                    opt("A covalent bond"),
                    opt("Nuclear forces"),
                    opt("Gravity"),
                ),
                "The hydrophobic effect releases structured water into bulk, favouring binding.",
            ),
            q(
                "The refined 'lock and key' picture that allows both partners to adjust is called:",
                (
                    opt("Induced fit", correct=True),
                    opt("Rigid docking only"),
                    opt("Covalent capture"),
                    opt("Denaturation"),
                ),
                "Induced fit recognises that protein and ligand reshape upon binding.",
            ),
        ),
        "Binding affinity and free energy": (
            q(
                "A smaller dissociation constant Kd means:",
                (
                    opt("Tighter binding", correct=True),
                    opt("Weaker binding"),
                    opt("No binding"),
                    opt("A larger protein"),
                ),
                "Kd has units of concentration; smaller Kd means tighter binding.",
            ),
            q(
                "At a ligand concentration equal to Kd, what fraction of protein is occupied?",
                (
                    opt("About half", correct=True),
                    opt("All of it"),
                    opt("None of it"),
                    opt("Exactly 10 percent"),
                ),
                "By definition, [L] = Kd gives 50 percent occupancy.",
            ),
            q(
                "Why is each tenfold gain in Kd worth only ~1.4 kcal/mol of free energy?",
                (
                    opt("Because dG depends on the logarithm of Kd", correct=True),
                    opt("Because energy is unrelated to Kd"),
                    opt("Because Kd is always 1"),
                    opt("Because temperature is zero"),
                ),
                "dG = RT ln Kd, so affinity scales logarithmically with free energy.",
            ),
        ),
        "The binding site and the pose": (
            q(
                "A docking 'pose' is best described as:",
                (
                    opt(
                        "A candidate placement: position, orientation and conformation",
                        correct=True,
                    ),
                    opt("The protein's secondary structure"),
                    opt("A list of gene names"),
                    opt("The crystal's space group"),
                ),
                "A pose is one full placement of the ligand in the pocket.",
            ),
            q(
                "RMSD below which value is the usual threshold for a 'correct' pose?",
                (
                    opt("2 Angstrom", correct=True),
                    opt("20 Angstrom"),
                    opt("2 nanometers"),
                    opt("200 Angstrom"),
                ),
                "A pose within 2 A of the experimental structure is considered correct.",
            ),
            q(
                "A site elsewhere on the protein than where the natural ligand binds is called:",
                (
                    opt("Allosteric", correct=True),
                    opt("Orthosteric"),
                    opt("Cytoplasmic"),
                    opt("Hydrophilic"),
                ),
                "Orthosteric = native ligand site; allosteric = a different regulatory site.",
            ),
        ),
        "Conformational flexibility": (
            q(
                "What adds a torsional degree of freedom to a ligand?",
                (
                    opt("Each rotatable bond", correct=True),
                    opt("Each carbon atom"),
                    opt("Each hydrogen bond"),
                    opt("Each water molecule"),
                ),
                "Rotatable single bonds create dihedral (torsion) degrees of freedom.",
            ),
            q(
                "How does the number of conformers scale with rotatable bonds n?",
                (
                    opt("Roughly exponentially (about k^n)", correct=True),
                    opt("Linearly with n"),
                    opt("It stays constant"),
                    opt("It decreases with n"),
                ),
                "With k states per torsion, conformers grow like k^n.",
            ),
            q(
                "Standard modern docking treats the ligand as:",
                (
                    opt("Flexible (sampling torsions)", correct=True),
                    opt("Always perfectly rigid"),
                    opt("A single point"),
                    opt("A sphere with no shape"),
                ),
                "Flexible-ligand docking samples torsions and is now standard.",
            ),
        ),
        "Your first docking run": (
            q(
                "Why re-dock a ligand whose bound structure is already known?",
                (
                    opt(
                        "To validate that the engine reproduces a known binding mode", correct=True
                    ),
                    opt("To synthesise the compound"),
                    opt("To sequence the protein"),
                    opt("To measure the protein's mass"),
                ),
                "Re-docking checks the method can recover a known pose before trusting it.",
            ),
            q(
                "Which of these is a free, widely used docking engine?",
                (
                    opt("AutoDock Vina", correct=True),
                    opt("BLAST"),
                    opt("Clustal Omega"),
                    opt("Gaussian blur"),
                ),
                "AutoDock/Vina are free, popular docking engines.",
            ),
            q(
                "A correct first step before docking the receptor is to:",
                (
                    opt("Add hydrogens and assign protonation/charges", correct=True),
                    opt("Delete the entire active site"),
                    opt("Translate the sequence to RNA"),
                    opt("Heat the crystal"),
                ),
                "Receptor preparation includes hydrogens, protonation states and charges.",
            ),
        ),
    },
    final=(
        q(
            "Binding free energy relates to the dissociation constant by:",
            (
                opt("dG = RT ln Kd", correct=True),
                opt("dG = Kd squared"),
                opt("dG = 1 / Kd"),
                opt("dG = Kd + RT"),
            ),
            "Free energy is the logarithm of Kd scaled by RT.",
        ),
        q(
            "Which set lists non-covalent binding interactions?",
            (
                opt("Hydrogen bonds, salt bridges, van der Waals, hydrophobic", correct=True),
                opt("Peptide bonds and disulfides only"),
                opt("Only covalent bonds"),
                opt("Only metallic bonds"),
            ),
            "These non-covalent forces dominate reversible ligand binding.",
        ),
        q(
            "A pose is judged correct when its RMSD to the crystal pose is:",
            (
                opt("Below about 2 Angstrom", correct=True),
                opt("Above 10 Angstrom"),
                opt("Exactly 0 always"),
                opt("Any value at all"),
            ),
            "The conventional success threshold is 2 A.",
        ),
        q(
            "Increasing ligand and receptor flexibility tends to:",
            (
                opt("Make the model more realistic but the search larger", correct=True),
                opt("Always make docking faster"),
                opt("Remove the need for scoring"),
                opt("Eliminate all conformers"),
            ),
            "Flexibility improves realism at the cost of a bigger search space.",
        ),
        q(
            "The active site of an enzyme is an example of:",
            (
                opt("A binding pocket where docking occurs", correct=True),
                opt("A random surface patch ignored by docking"),
                opt("The mRNA of the gene"),
                opt("A lipid membrane"),
            ),
            "Docking targets a defined pocket such as an enzyme active site.",
        ),
        q(
            "At [ligand] = Kd the protein is approximately:",
            (
                opt("Half occupied", correct=True),
                opt("Fully unoccupied"),
                opt("Fully occupied"),
                opt("Denatured"),
            ),
            "Kd is the concentration giving 50 percent occupancy.",
        ),
    ),
)
