"""Quiz questions for the Structural Biology - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Structure-function and active sites": (
            q(
                "Enzymes accelerate reactions primarily by:",
                (
                    opt(
                        "stabilising the transition state to lower the activation barrier",
                        correct=True,
                    ),
                    opt("raising the activation barrier"),
                    opt("heating the substrate"),
                    opt("changing the equilibrium constant of the reaction"),
                ),
                "Catalysts lower delta-G-double-dagger by binding the transition state tightly.",
            ),
            q(
                "The catalytic triad of serine proteases such as chymotrypsin is:",
                (
                    opt("Ser-His-Asp", correct=True),
                    opt("Ala-Gly-Val"),
                    opt("Cys-Cys-Cys"),
                    opt("Lys-Arg-His"),
                ),
                "The classic Ser-His-Asp triad positions a nucleophilic serine.",
            ),
            q(
                "Active-site residues are often:",
                (
                    opt("distant in sequence but brought together by the fold", correct=True),
                    opt("always consecutive in the sequence"),
                    opt("located outside the protein"),
                    opt("identical for every enzyme"),
                ),
                "The 3D fold assembles residues that are far apart in the primary sequence.",
            ),
        ),
        "Allostery and cooperativity": (
            q(
                "Allostery is best described as:",
                (
                    opt("binding at one site changing activity at a distant site", correct=True),
                    opt("a covalent bond between subunits"),
                    opt("the linear amino-acid sequence"),
                    opt("the diffraction of X-rays"),
                ),
                "Allostery is regulation transmitted through structure to a distant site.",
            ),
            q(
                "In the MWC (concerted) model, the oligomer switches between:",
                (
                    opt("T (tense) and R (relaxed) states in unison", correct=True),
                    opt("folded and unfolded states only"),
                    opt("crystalline and amorphous forms"),
                    opt("parallel and antiparallel sheets"),
                ),
                "MWC assumes a concerted T<->R transition of the whole assembly.",
            ),
            q(
                "A Hill coefficient greater than 1 indicates:",
                (
                    opt("positive cooperativity", correct=True),
                    opt("no cooperativity"),
                    opt("negative stability"),
                    opt("an unfolded protein"),
                ),
                "n_H > 1 means positive cooperativity, as in hemoglobin (~2.8).",
            ),
        ),
        "Conformational dynamics and molecular dynamics": (
            q(
                "Molecular dynamics simulates motion by:",
                (
                    opt(
                        "integrating Newton's equations for each atom under a force field",
                        correct=True,
                    ),
                    opt("solving Bragg's law for each atom"),
                    opt("measuring melting temperature"),
                    opt("counting reflections"),
                ),
                "MD numerically integrates Newtonian equations with an empirical force field.",
            ),
            q(
                "MD time steps are typically about:",
                (
                    opt("2 femtoseconds", correct=True),
                    opt("2 seconds"),
                    opt("2 minutes"),
                    opt("2 hours"),
                ),
                "Steps of ~2 fs resolve fast bond vibrations.",
            ),
            q(
                "Why is reaching biological timescales hard in MD?",
                (
                    opt(
                        "many motions take micro- to milliseconds, needing billions of tiny steps",
                        correct=True,
                    ),
                    opt("force fields are exact and need no sampling"),
                    opt("atoms do not move at all"),
                    opt("the simulation has no time step"),
                ),
                "The femtosecond step versus millisecond events creates a vast sampling gap.",
            ),
        ),
        "Structure-based drug design and docking": (
            q(
                "Molecular docking predicts:",
                (
                    opt(
                        "how a small molecule binds and scores its poses in a pocket", correct=True
                    ),
                    opt("the melting temperature of a protein"),
                    opt("the number of reflections in a data set"),
                    opt("the Hill coefficient"),
                ),
                "Docking samples and scores candidate binding poses of a ligand.",
            ),
            q(
                "Virtual screening is used to:",
                (
                    opt(
                        "rank many library compounds computationally before synthesis", correct=True
                    ),
                    opt("crystallise the target faster"),
                    opt("replace all experimental validation"),
                    opt("measure resolution"),
                ),
                "It docks large libraries to prioritise candidates cheaply.",
            ),
            q(
                "The central limitation of docking is:",
                (
                    opt("the approximate accuracy of scoring functions", correct=True),
                    opt("that proteins have no pockets"),
                    opt("that ligands cannot be drawn"),
                    opt("that X-rays are too weak"),
                ),
                "Scoring functions are approximate, so predictions need experimental confirmation.",
            ),
        ),
        "Deep learning: AlphaFold and protein design": (
            q(
                "A key input that lets AlphaFold infer 3D contacts is:",
                (
                    opt(
                        "multiple sequence alignments revealing co-evolving residues", correct=True
                    ),
                    opt("the crystal's space group"),
                    opt("the melting temperature"),
                    opt("the detector pixel size"),
                ),
                "Co-evolution signals in MSAs hint at spatially close residue pairs.",
            ),
            q(
                "AlphaFold's per-residue confidence score is called:",
                (
                    opt("pLDDT", correct=True),
                    opt("R-free"),
                    opt("FSC"),
                    opt("Hill coefficient"),
                ),
                "pLDDT reports AlphaFold's per-residue confidence.",
            ),
            q(
                "Which tool designs an amino-acid sequence to fold to a given backbone?",
                (
                    opt("ProteinMPNN", correct=True),
                    opt("AutoDock Vina"),
                    opt("RELION"),
                    opt("MolProbity"),
                ),
                "ProteinMPNN is an inverse-folding / sequence-design network.",
            ),
        ),
    },
    final=(
        q(
            "Transition-state stabilisation by an enzyme:",
            (
                opt("lowers the activation barrier and speeds the reaction", correct=True),
                opt("raises the barrier"),
                opt("has no effect on rate"),
                opt("changes the reaction's equilibrium constant"),
            ),
            "Binding the transition state tightly lowers delta-G-double-dagger.",
        ),
        q(
            "Hemoglobin's sigmoidal oxygen-binding curve reflects:",
            (
                opt("positive cooperativity among subunits", correct=True),
                opt("no cooperativity"),
                opt("covalent oxygen bonding"),
                opt("denaturation"),
            ),
            "Cooperative binding (Hill coefficient ~2.8) gives the S-shaped curve.",
        ),
        q(
            "Molecular dynamics is fundamentally limited by:",
            (
                opt("the gap between femtosecond steps and slow biological motions", correct=True),
                opt("the absence of any force field"),
                opt("an inability to model solvent"),
                opt("the need for a crystal"),
            ),
            "Sampling micro- to millisecond events with ~2 fs steps is the core challenge.",
        ),
        q(
            "Structure-based drug design uses the target structure to:",
            (
                opt("design or screen molecules complementary to a binding pocket", correct=True),
                opt("measure GC content"),
                opt("crystallise water"),
                opt("compute the Hill coefficient"),
            ),
            "SBDD designs ligands that fit a druggable pocket, then iterates.",
        ),
        q(
            "AlphaFold 2's breakthrough at CASP14 was:",
            (
                opt("near-experimental accuracy in protein-structure prediction", correct=True),
                opt("the first protein crystal"),
                opt("a new force field for MD"),
                opt("a faster electron detector"),
            ),
            "AlphaFold 2 reached near-experimental accuracy on structure prediction.",
        ),
        q(
            "Generative design tools such as RFdiffusion are used to:",
            (
                opt("create novel protein backbones for a desired function", correct=True),
                opt("solve the X-ray phase problem"),
                opt("measure resolution by FSC"),
                opt("compute denaturation midpoints"),
            ),
            "RFdiffusion generates new backbones; ProteinMPNN then designs sequences for them.",
        ),
    ),
)
