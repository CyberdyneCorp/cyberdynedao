"""Quiz questions for the Molecular Modeling & Visualization - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Homology and comparative modeling": (
            q(
                "Homology modeling works because:",
                (
                    opt("structure is more conserved than sequence", correct=True),
                    opt("sequence is more conserved than structure"),
                    opt("all proteins share one fold"),
                    opt("templates are never needed"),
                ),
                "Homologous proteins keep their fold even as sequence diverges.",
            ),
            q(
                "Which step most determines homology-model quality?",
                (
                    opt("the target-template alignment", correct=True),
                    opt("the choice of viewer color"),
                    opt("the file format"),
                    opt("the screen resolution"),
                ),
                "Alignment errors propagate into the model, so it is the most critical step.",
            ),
            q(
                "The 'twilight zone' refers to sequence identity around:",
                (
                    opt("20-25 percent, where alignments become unreliable", correct=True),
                    opt("90 percent, where models are perfect"),
                    opt("100 percent identity"),
                    opt("zero atoms"),
                ),
                "Below ~20-25% identity, alignments and thus models become unreliable.",
            ),
        ),
        "AI structure prediction: AlphaFold and beyond": (
            q(
                "A key input that gives AlphaFold2 its co-evolution signal is:",
                (
                    opt("a multiple sequence alignment (MSA)", correct=True),
                    opt("a single sequence with no homologs"),
                    opt("the crystallographic R-factor"),
                    opt("a docking score"),
                ),
                "Co-evolving residues in the MSA signal spatial contacts.",
            ),
            q(
                "pLDDT in AlphaFold reports:",
                (
                    opt("per-residue confidence", correct=True),
                    opt("the binding affinity"),
                    opt("the solvent box size"),
                    opt("the partial charge"),
                ),
                "pLDDT is a per-residue confidence; PAE captures inter-domain confidence.",
            ),
            q(
                "ESMFold differs from AlphaFold2 mainly in that it:",
                (
                    opt("uses a protein language model and needs no MSA", correct=True),
                    opt("requires X-ray data"),
                    opt("uses an explicit force field only"),
                    opt("cannot predict any structure"),
                ),
                "ESMFold predicts from a single sequence via a language model, without building an MSA.",
            ),
        ),
        "Loop modeling, side chains and refinement": (
            q(
                "Loops are hard to model because:",
                (
                    opt("they often have no template and large conformational space", correct=True),
                    opt("they are always identical to the template"),
                    opt("they contain no atoms"),
                    opt("they never carry function"),
                ),
                "Insertions/deletions lack a template and explore a large conformational space.",
            ),
            q(
                "Side-chain placement typically uses:",
                (
                    opt("a backbone-dependent rotamer library", correct=True),
                    opt("Particle Mesh Ewald"),
                    opt("the Henderson-Hasselbalch equation"),
                    opt("a multiple sequence alignment"),
                ),
                "Tools like SCWRL4 place rotamers from a backbone-dependent (Dunbrack) library.",
            ),
            q(
                "Loop-prediction accuracy generally:",
                (
                    opt("decreases as loop length increases", correct=True),
                    opt("increases as loop length increases"),
                    opt("is independent of loop length"),
                    opt("is always perfect"),
                ),
                "Longer loops have far larger conformational spaces, lowering accuracy.",
            ),
        ),
        "System preparation for molecular dynamics": (
            q(
                "Solvating a system for MD typically means:",
                (
                    opt("placing the solute in a periodic box of explicit water", correct=True),
                    opt("removing all atoms"),
                    opt("rendering a cartoon view"),
                    opt("running a BLAST search"),
                ),
                "Solvation surrounds the solute with explicit water (and ions) in a periodic box.",
            ),
            q(
                "Why add salt such as 0.15 M NaCl during preparation?",
                (
                    opt("to neutralise charge and set physiological ionic strength", correct=True),
                    opt("to break covalent bonds"),
                    opt("to increase sequence identity"),
                    opt("to change the file format"),
                ),
                "Counter-ions neutralise the system and salt sets a realistic ionic strength.",
            ),
            q(
                "Equilibration before production MD usually proceeds as:",
                (
                    opt("minimize, heat, then NVT/NPT equilibration", correct=True),
                    opt("production first, then minimize"),
                    opt("only a single energy minimization"),
                    opt("docking then virtual screening"),
                ),
                "Standard staging: minimize, heat with restraints, equilibrate NVT then NPT, then produce.",
            ),
        ),
        "Structure-based and generative design": (
            q(
                "Molecular docking primarily:",
                (
                    opt("poses and scores a ligand in a binding pocket", correct=True),
                    opt("predicts protein secondary structure"),
                    opt("aligns two sequences"),
                    opt("computes a partition function"),
                ),
                "Docking (Vina, Glide, GOLD) generates and scores ligand poses in a pocket.",
            ),
            q(
                "ProteinMPNN is used to:",
                (
                    opt("design a sequence that folds to a given backbone", correct=True),
                    opt("generate novel backbones from noise"),
                    opt("compute X-ray resolution"),
                    opt("solvate a system"),
                ),
                "ProteinMPNN designs sequences for a fixed backbone; RFdiffusion generates backbones.",
            ),
            q(
                "Free-energy perturbation (FEP) is used in design to:",
                (
                    opt("compute accurate relative binding affinities", correct=True),
                    opt("render molecular surfaces"),
                    opt("assign protonation states"),
                    opt("build the MSA"),
                ),
                "FEP gives accurate relative binding free energies for lead optimization.",
            ),
        ),
    },
    final=(
        q(
            "Homology model accuracy is most strongly tied to:",
            (
                opt("sequence identity to the template", correct=True),
                opt("the viewer used"),
                opt("the operating system"),
                opt("the file extension"),
            ),
            "Higher target-template identity yields more accurate models.",
        ),
        q(
            "AlphaFold2 predicts structure directly from sequence without:",
            (
                opt("an explicit physics-based force field", correct=True),
                opt("any neural network"),
                opt("any training data"),
                opt("multiple sequence alignments"),
            ),
            "It learns from data rather than relying on an explicit force field.",
        ),
        q(
            "The hardest regions to model in a protein are usually:",
            (
                opt("loops and side chains", correct=True),
                opt("the conserved hydrophobic core"),
                opt("the alpha-helices copied from a template"),
                opt("the file header"),
            ),
            "Cores copy well; loops and side chains are the difficult parts.",
        ),
        q(
            "A correct system-preparation order before production MD is:",
            (
                opt("clean, protonate, solvate, add ions, minimize, equilibrate", correct=True),
                opt("production, then solvate, then clean"),
                opt("dock, then minimize, then clean"),
                opt("validate only, then produce"),
            ),
            "Preparation builds up from cleaning through equilibration before production.",
        ),
        q(
            "RFdiffusion is an example of:",
            (
                opt("a generative model for novel protein backbones", correct=True),
                opt("a docking scoring function"),
                opt("a partial-charge method"),
                opt("a sequence aligner"),
            ),
            "RFdiffusion generates new backbones; ProteinMPNN then designs sequences for them.",
        ),
        q(
            "The honest design workflow ends with:",
            (
                opt("experimental synthesis and testing", correct=True),
                opt("a single docking score, accepted as truth"),
                opt("only a prettier visualization"),
                opt("deleting the model"),
            ),
            "Computational predictions must ultimately be validated by making and testing molecules.",
        ),
    ),
)
