"""Quiz questions for the Computer-Aided Drug Design (CADD) - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Fragment-based drug design": (
            q(
                "Fragment-based drug design starts from molecules that are:",
                (
                    opt(
                        "small and weakly binding but cover chemical space efficiently",
                        correct=True,
                    ),
                    opt("large and tightly binding drug-sized compounds"),
                    opt("only natural products over 1000 Da"),
                    opt("polymers with no binding affinity"),
                ),
                "Fragments (<300 Da) bind weakly but sample chemical space efficiently.",
            ),
            q(
                "Why are sensitive biophysical methods (X-ray, NMR, SPR) needed in FBDD?",
                (
                    opt("fragments bind weakly and need sensitive detection", correct=True),
                    opt("fragments are radioactive"),
                    opt("fragments cannot be dissolved"),
                    opt("fragments are too large to detect"),
                ),
                "Millimolar-range binding requires biophysical techniques to confirm.",
            ),
            q(
                "Ligand efficiency (LE) measures:",
                (
                    opt("binding free energy per heavy atom", correct=True),
                    opt("molecular weight per ring"),
                    opt("solubility per gram"),
                    opt("number of atoms per dollar"),
                ),
                "LE normalises binding energy by heavy-atom count; fragments score well.",
            ),
        ),
        "De novo molecular design": (
            q(
                "De novo design differs from screening because it:",
                (
                    opt(
                        "builds novel molecules to satisfy a target rather than searching a library",
                        correct=True,
                    ),
                    opt("only tests molecules already in a catalogue"),
                    opt("avoids any scoring"),
                    opt("ignores the target entirely"),
                ),
                "De novo generates new structures instead of screening existing ones.",
            ),
            q(
                "What is the central challenge of de novo design?",
                (
                    opt(
                        "navigating vast chemical space toward potent, synthesisable molecules",
                        correct=True,
                    ),
                    opt("running out of element types"),
                    opt("a lack of any scoring methods"),
                    opt("molecules being too easy to make"),
                ),
                "Drug-like space is about 10^60 molecules; steering toward good, makeable ones is hard.",
            ),
            q(
                "Why is synthetic accessibility scoring essential in de novo design?",
                (
                    opt("so proposed molecules can actually be synthesised", correct=True),
                    opt("to compute the boiling point"),
                    opt("to translate SMILES into protein sequences"),
                    opt("to measure plasma half-life"),
                ),
                "SA scoring and retrosynthesis prevent unmakeable designs.",
            ),
        ),
        "Generative AI for molecule generation": (
            q(
                "A variational autoencoder (VAE) is useful in molecule generation because it:",
                (
                    opt(
                        "encodes molecules into a continuous latent space for optimisation",
                        correct=True,
                    ),
                    opt("aligns DNA sequences"),
                    opt("measures crystal diffraction"),
                    opt("computes molecular weight only"),
                ),
                "The continuous latent space lets you optimise and interpolate molecules.",
            ),
            q(
                "Reinforcement learning (e.g. REINVENT) biases generation toward goals by:",
                (
                    opt(
                        "rewarding molecules that score well on affinity, drug-likeness and SA",
                        correct=True,
                    ),
                    opt("deleting all generated molecules"),
                    opt("randomly mutating protein sequences"),
                    opt("ignoring all scoring signals"),
                ),
                "RL rewards desirable predicted properties while a prior keeps outputs realistic.",
            ),
            q(
                "Structure-based generative models (e.g. Pocket2Mol) condition generation on:",
                (
                    opt("the target binding pocket", correct=True),
                    opt("the researcher's name"),
                    opt("the date of synthesis"),
                    opt("the solvent boiling point"),
                ),
                "They place atoms directly into the binding-site geometry.",
            ),
        ),
        "AlphaFold and structure prediction": (
            q(
                "AlphaFold2 predicts protein structure primarily from:",
                (
                    opt(
                        "sequence using multiple-sequence alignments and a transformer",
                        correct=True,
                    ),
                    opt("X-ray diffraction patterns only"),
                    opt("mass-spectrometry fragment ions"),
                    opt("the molecule's logP"),
                ),
                "The Evoformer processes MSAs and a structure module outputs coordinates.",
            ),
            q(
                "What does the pLDDT score report?",
                (
                    opt("per-residue confidence in the predicted structure", correct=True),
                    opt("the binding affinity of a ligand"),
                    opt("the molecular weight"),
                    opt("the synthesis yield"),
                ),
                "pLDDT (and PAE) indicate where the prediction can be trusted.",
            ),
            q(
                "A key caveat when docking into AlphaFold structures is that the model:",
                (
                    opt(
                        "usually gives one apo conformation and is not trained to place ligands",
                        correct=True,
                    ),
                    opt("always includes the bound ligand"),
                    opt("perfectly models all side-chain flexibility"),
                    opt("guarantees correct docking poses"),
                ),
                "Single apo predictions can disappoint for ligand placement.",
            ),
        ),
        "Multi-parameter lead optimisation": (
            q(
                "Multi-parameter optimisation (MPO) addresses the fact that drug properties:",
                (
                    opt("often conflict and must be balanced together", correct=True),
                    opt("are all perfectly correlated"),
                    opt("only involve potency"),
                    opt("never matter after the hit stage"),
                ),
                "Potency, ADMET and safety frequently trade off against each other.",
            ),
            q(
                "Using a geometric-mean desirability means that:",
                (
                    opt("one failing property tanks the overall score", correct=True),
                    opt("a single property dominates regardless of others"),
                    opt("scores can exceed one"),
                    opt("properties are ignored"),
                ),
                "The geometric mean is small if any component is small.",
            ),
            q(
                "The DMTA cycle stands for:",
                (
                    opt("Design, Make, Test, Analyse", correct=True),
                    opt("Dock, Model, Train, Assay"),
                    opt("Distribute, Metabolise, Treat, Apply"),
                    opt("Define, Measure, Adjust, Trial"),
                ),
                "DMTA is the iterative loop of lead optimisation.",
            ),
        ),
        "Case studies in CADD": (
            q(
                "HIV protease inhibitors are a classic example of:",
                (
                    opt("structure-based drug design against a crystal structure", correct=True),
                    opt("pure random screening with no structure"),
                    opt("ligand-based QSAR only"),
                    opt("natural-product isolation alone"),
                ),
                "They were designed exploiting the protease's symmetric active site.",
            ),
            q(
                "Nirmatrelvir (in Paxlovid) targets which SARS-CoV-2 enzyme?",
                (
                    opt("the main protease (Mpro)", correct=True),
                    opt("DNA polymerase"),
                    opt("the spike glycoprotein only"),
                    opt("human cytochrome P450"),
                ),
                "It is a structure-based inhibitor of the viral main protease.",
            ),
            q(
                "A recurring lesson across CADD case studies is that success is most likely when:",
                (
                    opt(
                        "a validated, druggable target with structural data meets rigorous computation",
                        correct=True,
                    ),
                    opt("no structural data is available"),
                    opt("the target is undruggable"),
                    opt("computation is avoided entirely"),
                ),
                "Structure plus rigorous prioritisation shortens the path to a lead.",
            ),
        ),
    },
    final=(
        q(
            "Why do fragments cover chemical space more efficiently than drug-sized molecules?",
            (
                opt(
                    "a small fragment library samples more of chemical space than a huge HTS deck",
                    correct=True,
                ),
                opt("fragments are always more potent"),
                opt("fragments cannot bind any target"),
                opt("fragments are larger than leads"),
            ),
            "Lower complexity means a small fragment set probes more interaction space.",
        ),
        q(
            "Roughly how large is estimated drug-like chemical space?",
            (
                opt("about 10^60 molecules", correct=True),
                opt("about 100 molecules"),
                opt("about 10^6 molecules total"),
                opt("a fixed list of 500"),
            ),
            "The vastness of chemical space is why de novo design must be steered.",
        ),
        q(
            "Which generative approach increasingly produces 3D molecular structures?",
            (
                opt("diffusion models", correct=True),
                opt("simple linear regression"),
                opt("BLAST alignment"),
                opt("spreadsheet macros"),
            ),
            "Diffusion models are a leading method for 3D structure generation.",
        ),
        q(
            "AlphaFold expanded CADD chiefly by:",
            (
                opt("providing 3D structures for targets lacking experimental ones", correct=True),
                opt("synthesising molecules automatically"),
                opt("replacing all clinical trials"),
                opt("measuring binding affinities directly"),
            ),
            "Predicted structures unlock structure-based design for more targets.",
        ),
        q(
            "Multi-parameter optimisation matters because optimisation gets harder as:",
            (
                opt("the number of independent must-pass objectives grows", correct=True),
                opt("molecules get simpler"),
                opt("there is only one objective"),
                opt("potency becomes irrelevant"),
            ),
            "Joint desirability falls steeply with more conflicting criteria.",
        ),
        q(
            "What common pattern explains CADD's landmark successes?",
            (
                opt(
                    "a validated druggable target with structural data plus rigorous computation",
                    correct=True,
                ),
                opt("avoiding any structural or computational input"),
                opt("relying solely on luck"),
                opt("targeting only undruggable interfaces"),
            ),
            "Structure-informed, computationally prioritised campaigns shorten discovery.",
        ),
    ),
)
