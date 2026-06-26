"""Quiz questions for the Generative Models for Molecular Design - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is generative molecular design": (
            q(
                "How does a generative model differ from classical virtual screening?",
                (
                    opt("It samples novel molecules from a learned distribution", correct=True),
                    opt("It only ranks molecules in a fixed library"),
                    opt("It measures binding affinity in a wet lab"),
                    opt("It crystallizes proteins for X-ray studies"),
                ),
                "Screening ranks a fixed set; generation proposes new molecules from p(x).",
            ),
            q(
                "Roughly how large is the estimated space of small drug-like molecules?",
                (
                    opt("About 10^60", correct=True),
                    opt("About 10^6"),
                    opt("About 10^12"),
                    opt("About 100"),
                ),
                "Drug-like chemical space is estimated near 10^60, far beyond enumeration.",
            ),
            q(
                "What is the main practical promise of generative design?",
                (
                    opt(
                        "Exploring vast chemical space to find novel useful candidates",
                        correct=True,
                    ),
                    opt("Eliminating the need for any experimental testing"),
                    opt("Guaranteeing every molecule is a marketed drug"),
                    opt("Replacing chemistry with pure enumeration of all molecules"),
                ),
                "It intelligently explores spaces too large to enumerate or screen exhaustively.",
            ),
        ),
        "Molecular representations: SMILES, graphs and fingerprints": (
            q(
                "What does a SMILES string encode?",
                (
                    opt("A molecule as a line-notation character string", correct=True),
                    opt("A 3D electron density map"),
                    opt("A protein amino-acid sequence only"),
                    opt("A docking score"),
                ),
                "SMILES is a string notation, e.g. CCO for ethanol.",
            ),
            q(
                "Why is SELFIES attractive for generation compared to plain SMILES?",
                (
                    opt("Every SELFIES string decodes to a valid molecule", correct=True),
                    opt("It is shorter for every molecule"),
                    opt("It stores 3D coordinates directly"),
                    opt("It cannot represent rings"),
                ),
                "SELFIES is a robust grammar where all strings map to valid molecules.",
            ),
            q(
                "Which representation is the natural, permutation-invariant input for GNNs?",
                (
                    opt("The molecular graph of atoms and bonds", correct=True),
                    opt("A canonical SMILES string"),
                    opt("A 1024-bit ECFP fingerprint"),
                    opt("A docking pose"),
                ),
                "Graphs (atoms as nodes, bonds as edges) are handled by graph neural networks.",
            ),
        ),
        "Scoring molecules: validity, drug-likeness and properties": (
            q(
                "What does the 'validity' metric check for generated molecules?",
                (
                    opt("That the structure parses with sensible valences", correct=True),
                    opt("That the molecule is patented"),
                    opt("That it has high binding affinity"),
                    opt("That it is identical to a training molecule"),
                ),
                "Validity means the SMILES/graph yields a chemically sensible molecule.",
            ),
            q(
                "What does the QED score summarize?",
                (
                    opt("Quantitative drug-likeness as a single 0-1 value", correct=True),
                    opt("Exact synthesis cost in dollars"),
                    opt("The number of rotatable bonds only"),
                    opt("The crystal structure resolution"),
                ),
                "QED collapses several descriptors into one drug-likeness score.",
            ),
            q(
                "Why does desirability for logP typically peak in a middle range?",
                (
                    opt("Too low fails membrane crossing, too high hurts solubility", correct=True),
                    opt("Higher logP is always better"),
                    opt("Lower logP is always better"),
                    opt("logP has no effect on a drug"),
                ),
                "Lipophilicity has a sweet spot between permeability and solubility.",
            ),
        ),
        "Learning a distribution over molecules": (
            q(
                "What does maximum-likelihood training of a generative model do?",
                (
                    opt(
                        "Maximizes the probability the model assigns to real molecules",
                        correct=True,
                    ),
                    opt("Minimizes the number of atoms"),
                    opt("Maximizes docking scores directly"),
                    opt("Removes all rings from molecules"),
                ),
                "Training maximizes likelihood (minimizes negative log-likelihood) of the data.",
            ),
            q(
                "How does an autoregressive SMILES model factorize p(x)?",
                (
                    opt("As a product of next-token probabilities given the prefix", correct=True),
                    opt("As a sum of independent atom energies"),
                    opt("As a single Gaussian over coordinates"),
                    opt("As a fixed lookup table"),
                ),
                "It predicts each token conditioned on previous tokens, like a language model.",
            ),
            q(
                "What does conditional generation p(x | c) enable?",
                (
                    opt("Biasing samples toward a desired property c", correct=True),
                    opt("Removing the need for any training data"),
                    opt("Guaranteeing valid molecules without checks"),
                    opt("Computing exact free energies"),
                ),
                "Conditioning lets the model target molecules with specific properties.",
            ),
        ),
        "A map of generative model families": (
            q(
                "Which family provides a smooth latent space useful for interpolation?",
                (
                    opt("Variational autoencoders (VAEs)", correct=True),
                    opt("Plain decision trees"),
                    opt("k-nearest neighbors"),
                    opt("Linear regression"),
                ),
                "VAEs encode molecules into a continuous latent space.",
            ),
            q(
                "Which family is currently state-of-the-art for 3D molecular structures?",
                (
                    opt("Diffusion / score-based models", correct=True),
                    opt("Naive Bayes classifiers"),
                    opt("Random number generators"),
                    opt("Support vector machines"),
                ),
                "Diffusion models lead for 3D molecular generation.",
            ),
            q(
                "What role does reinforcement learning play among these methods?",
                (
                    opt(
                        "It steers a generator toward a reward rather than modeling density",
                        correct=True,
                    ),
                    opt("It is a density model giving exact likelihood"),
                    opt("It only compresses fingerprints"),
                    opt("It replaces the need for any generator"),
                ),
                "RL optimizes a generator toward a reward; it is not itself a density model.",
            ),
        ),
    },
    final=(
        q(
            "What is the core capability of a generative molecular model?",
            (
                opt("Sampling novel molecules from a learned distribution", correct=True),
                opt("Ranking only a fixed existing library"),
                opt("Running biological assays"),
                opt("Purifying compounds in a lab"),
            ),
            "Generative models sample new molecules from p(x).",
        ),
        q(
            "Which representation pairs naturally with sequence models like Transformers?",
            (
                opt("SMILES / SELFIES strings", correct=True),
                opt("3D voxel grids only"),
                opt("Raw mass spectra"),
                opt("Crystallographic unit cells"),
            ),
            "String notations let us reuse sequence-model architectures.",
        ),
        q(
            "Which metrics together guard against memorization and mode collapse?",
            (
                opt("Uniqueness and novelty", correct=True),
                opt("Molecular weight and color"),
                opt("Boiling point and density"),
                opt("Patent number and price"),
            ),
            "Uniqueness and novelty check diversity and difference from training data.",
        ),
        q(
            "What does minimizing negative log-likelihood accomplish?",
            (
                opt("Fitting the model distribution to the training molecules", correct=True),
                opt("Maximizing molecular weight"),
                opt("Increasing the number of invalid samples"),
                opt("Deleting the latent space"),
            ),
            "Lower NLL means higher assigned probability to real data.",
        ),
        q(
            "Which tool is commonly used to parse and validate molecular structures?",
            (
                opt("RDKit", correct=True),
                opt("Photoshop"),
                opt("Excel"),
                opt("FFmpeg"),
            ),
            "RDKit is the standard cheminformatics toolkit for these tasks.",
        ),
        q(
            "Why is good in-silico scoring necessary even with a great generator?",
            (
                opt("To judge and prioritize which generated molecules are useful", correct=True),
                opt("Because generators never produce valid molecules"),
                opt("Because scoring replaces the generator entirely"),
                opt("Because synthesis is never needed"),
            ),
            "Scoring (validity, drug-likeness, predicted properties) ranks candidates.",
        ),
    ),
)
