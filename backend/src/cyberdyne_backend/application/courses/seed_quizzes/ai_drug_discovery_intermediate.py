"""Quiz questions for the AI-Driven Drug Discovery - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "QSAR: regressing activity from structure": (
            q(
                "What is the core assumption of QSAR?",
                (
                    opt("activity is a function of molecular structure", correct=True),
                    opt("activity is purely random"),
                    opt("structure has no effect on activity"),
                    opt("only price predicts activity"),
                ),
                "QSAR models y = f(structure) + noise.",
            ),
            q(
                "Which loss is typically minimized in a QSAR regression?",
                (
                    opt("mean squared error", correct=True),
                    opt("cross-entropy of class labels"),
                    opt("Tanimoto distance"),
                    opt("the molecular weight"),
                ),
                "Regression of continuous pIC50 minimizes MSE.",
            ),
            q(
                "QSAR predictive skill ultimately is bounded by what?",
                (
                    opt("experimental noise in the assay", correct=True),
                    opt("the number of carbon atoms"),
                    opt("the color of the compound"),
                    opt("the year of publication"),
                ),
                "Performance saturates and is capped by assay measurement noise.",
            ),
        ),
        "Validation, splits and applicability domain": (
            q(
                "Why is a scaffold split preferred over a random split?",
                (
                    opt(
                        "It forces the model to generalize to unseen chemical series",
                        correct=True,
                    ),
                    opt("It is faster to compute"),
                    opt("It always raises the reported score"),
                    opt("It removes the need for a test set"),
                ),
                "Scaffold splits mimic the real task of predicting novel chemistry.",
            ),
            q(
                "What is the applicability domain of a model?",
                (
                    opt(
                        "The region of chemical space close to its training data",
                        correct=True,
                    ),
                    opt("The list of authors"),
                    opt("The GPU memory it needs"),
                    opt("The number of epochs trained"),
                ),
                "Predictions far from training data are unreliable and should be flagged.",
            ),
            q(
                "Which inflates validation scores deceptively?",
                (
                    opt("near-duplicate molecules leaking across the split", correct=True),
                    opt("using more cross-validation folds"),
                    opt("scaffold-based splitting"),
                    opt("flagging out-of-domain predictions"),
                ),
                "Leakage of near-duplicates between train and test inflates apparent skill.",
            ),
        ),
        "Graph neural networks for molecules": (
            q(
                "How does a GNN represent a molecule?",
                (
                    opt("atoms as nodes and bonds as edges", correct=True),
                    opt("as a single scalar"),
                    opt("as a raw image only"),
                    opt("as a clinical record"),
                ),
                "GNNs operate on the molecular graph directly.",
            ),
            q(
                "What is the core operation in a GNN?",
                (
                    opt("message passing between neighboring atoms", correct=True),
                    opt("matrix inversion of the assay"),
                    opt("docking pose search"),
                    opt("random shuffling of bits"),
                ),
                "Nodes aggregate messages from neighbors over several rounds.",
            ),
            q(
                "What does increasing the number of message-passing rounds do?",
                (
                    opt("widens the substructure each atom can see", correct=True),
                    opt("shrinks the molecule"),
                    opt("removes all bonds"),
                    opt("converts the graph to SMILES"),
                ),
                "More rounds grow the receptive field around each atom.",
            ),
        ),
        "Virtual screening and enrichment": (
            q(
                "Why is enrichment, not raw accuracy, the key VS metric?",
                (
                    opt("actives are rare, so top-ranked recovery matters most", correct=True),
                    opt("accuracy is impossible to compute"),
                    opt("enrichment ignores the actives"),
                    opt("VS never finds actives"),
                ),
                "With <1% actives, you care about how many appear at the top of the ranking.",
            ),
            q(
                "What does the enrichment factor at the top 1% compare?",
                (
                    opt(
                        "actives found in the top 1% versus expected by random",
                        correct=True,
                    ),
                    opt("molecular weight versus logP"),
                    opt("docking time versus assay time"),
                    opt("number of atoms versus bonds"),
                ),
                "EF compares actives recovered to the random-chance expectation.",
            ),
            q(
                "Which metric better rewards early recognition of actives?",
                (
                    opt("BEDROC", correct=True),
                    opt("plain accuracy"),
                    opt("molecular weight"),
                    opt("training time"),
                ),
                "BEDROC up-weights actives ranked near the very top.",
            ),
        ),
        "Molecular docking and scoring": (
            q(
                "Docking has which two main components?",
                (
                    opt("pose search and a scoring function", correct=True),
                    opt("SMILES parsing and printing"),
                    opt("clinical trial and approval"),
                    opt("fingerprinting and clustering"),
                ),
                "Docking searches poses and scores them for affinity.",
            ),
            q(
                "What does a docking scoring function estimate?",
                (
                    opt("the binding free energy of a pose", correct=True),
                    opt("the patent value"),
                    opt("the boiling point"),
                    opt("the number of stereocenters"),
                ),
                "Scoring functions approximate deltaG of binding from physical terms.",
            ),
            q(
                "A tighter binder (smaller Kd) corresponds to what deltaG?",
                (
                    opt("more negative deltaG", correct=True),
                    opt("more positive deltaG"),
                    opt("exactly zero deltaG"),
                    opt("deltaG is unrelated to Kd"),
                ),
                "deltaG = RT ln(Kd), so smaller Kd gives more negative deltaG.",
            ),
        ),
        "Scaffolds, similarity and chemical space": (
            q(
                "What is a Bemis-Murcko scaffold?",
                (
                    opt("the ring systems plus linkers, side chains stripped", correct=True),
                    opt("the full 3D protein"),
                    opt("the assay protocol"),
                    opt("the clinical dose"),
                ),
                "It is the molecular framework: rings and connecting linkers.",
            ),
            q(
                "What does the similarity principle state?",
                (
                    opt("similar molecules tend to have similar activity", correct=True),
                    opt("similar molecules always differ in activity"),
                    opt("structure is irrelevant to activity"),
                    opt("only weight predicts activity"),
                ),
                "Similar structures usually have similar activity, with notable exceptions.",
            ),
            q(
                "What is an activity cliff?",
                (
                    opt(
                        "a tiny structural change causing a large activity change",
                        correct=True,
                    ),
                    opt("a molecule with no rings"),
                    opt("an assay with no signal"),
                    opt("a protein with low pLDDT"),
                ),
                "Activity cliffs break the similarity principle and are hard to model.",
            ),
        ),
    },
    final=(
        q(
            "QSAR models predict activity primarily from what?",
            (
                opt("molecular structure / descriptors", correct=True),
                opt("the author list"),
                opt("the publication date"),
                opt("the funding amount"),
            ),
            "QSAR maps structure to activity.",
        ),
        q(
            "Which split best estimates generalization to new chemistry?",
            (
                opt("scaffold split", correct=True),
                opt("random split"),
                opt("alphabetical split by name"),
                opt("split by molecular weight only"),
            ),
            "Scaffold splits force prediction on unseen series.",
        ),
        q(
            "A GNN learns the molecular representation by doing what?",
            (
                opt("message passing on the atom-bond graph", correct=True),
                opt("inverting the assay matrix"),
                opt("reading the patent"),
                opt("counting only carbons"),
            ),
            "GNNs pass messages between neighboring atoms.",
        ),
        q(
            "Virtual screening success is judged mainly by what?",
            (
                opt("enrichment of actives near the top of the ranking", correct=True),
                opt("total compute hours"),
                opt("average molecular weight"),
                opt("number of rings"),
            ),
            "Enrichment captures recovery of rare actives at the top.",
        ),
        q(
            "Docking scoring functions approximate which quantity?",
            (
                opt("the binding free energy", correct=True),
                opt("the melting point"),
                opt("the patent number"),
                opt("the clinical phase"),
            ),
            "They estimate deltaG of the protein-ligand complex.",
        ),
        q(
            "An activity cliff is dangerous because it does what?",
            (
                opt("violates the similarity principle, fooling models", correct=True),
                opt("makes every model perfectly accurate"),
                opt("only affects 3D structures"),
                opt("removes the need for validation"),
            ),
            "Tiny structural changes cause huge activity jumps, hard for ML.",
        ),
    ),
)
