"""Quiz questions for the Generative Models for Molecular Design - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Denoising diffusion and score-based models": (
            q(
                "What does the denoising network in a diffusion model learn to predict?",
                (
                    opt("The noise added at each forward step", correct=True),
                    opt("The docking score"),
                    opt("The SMILES length"),
                    opt("The discriminator output"),
                ),
                "It predicts epsilon, equivalent to learning the score of the data.",
            ),
            q(
                "Diffusion training is mathematically equivalent to learning what?",
                (
                    opt("The score, the gradient of log-density", correct=True),
                    opt("The exact partition function"),
                    opt("A GAN minimax game"),
                    opt("A fixed lookup table"),
                ),
                "Denoising score matching learns the gradient of log p(x).",
            ),
            q(
                "What does the noise schedule control?",
                (
                    opt("How fast signal is destroyed across timesteps", correct=True),
                    opt("The number of atoms generated"),
                    opt("The docking software used"),
                    opt("The patent status"),
                ),
                "The schedule sets how the signal-to-noise ratio decays over t.",
            ),
        ),
        "Equivariant 3D generation": (
            q(
                "What symmetry should a 3D molecular generator respect?",
                (
                    opt("Rotation, translation and reflection (E(3))", correct=True),
                    opt("Only color invariance"),
                    opt("Alphabetical ordering of atoms"),
                    opt("Time reversal only"),
                ),
                "Physics is invariant to rigid motions, so generation should be E(3)-equivariant.",
            ),
            q(
                "How do E(3)-equivariant GNNs like EGNN achieve equivariance?",
                (
                    opt(
                        "By updating coordinates using only distances and relative vectors",
                        correct=True,
                    ),
                    opt("By memorizing every orientation"),
                    opt("By converting to SMILES first"),
                    opt("By ignoring 3D geometry"),
                ),
                "Using relative geometry makes outputs transform correctly under rotations.",
            ),
            q(
                "Why does building in equivariance help data efficiency?",
                (
                    opt("Capacity is not wasted learning symmetry from data", correct=True),
                    opt("It removes the need for any training"),
                    opt("It guarantees binding affinity"),
                    opt("It makes molecules 2D"),
                ),
                "Equivariance is an inductive bias, improving generalization with less data.",
            ),
        ),
        "Structure-based (pocket-conditioned) design": (
            q(
                "What does pocket-conditioned generation model?",
                (
                    opt(
                        "p(ligand | pocket): molecules that fit a given binding site", correct=True
                    ),
                    opt("p(pocket | ligand) only"),
                    opt("The protein's full genome"),
                    opt("The synthesis cost only"),
                ),
                "SBDD conditions the generator on the 3D protein pocket.",
            ),
            q(
                "Which methods exemplify pocket-conditioned 3D generation?",
                (
                    opt("Pocket2Mol, TargetDiff, DiffSBDD", correct=True),
                    opt("BLAST and Clustal"),
                    opt("PCA and t-SNE"),
                    opt("FFT and DCT"),
                ),
                "These are diffusion/autoregressive pocket-conditioned generators.",
            ),
            q(
                "Why must high docking scores be treated cautiously?",
                (
                    opt("Docking correlates only loosely with true binding affinity", correct=True),
                    opt("Docking always equals experimental affinity"),
                    opt("Docking measures solubility exactly"),
                    opt("Docking proves a molecule is synthesizable"),
                ),
                "Docking scores are enrichment signals, not proof; wet-lab confirmation is needed.",
            ),
        ),
        "Multi-objective and synthesis-aware optimization": (
            q(
                "What is a Pareto-optimal molecule?",
                (
                    opt(
                        "One where no objective can improve without worsening another", correct=True
                    ),
                    opt("The molecule with the most atoms"),
                    opt("The cheapest molecule only"),
                    opt("Any valid molecule"),
                ),
                "Pareto-optimal points are non-dominated trade-offs among objectives.",
            ),
            q(
                "Why include synthesizability as a design objective?",
                (
                    opt("A molecule no chemist can make is worthless", correct=True),
                    opt("It increases molecular weight"),
                    opt("It removes the need for potency"),
                    opt("It guarantees novelty"),
                ),
                "Synthesis-aware scoring (SA score, retrosynthesis) keeps designs makeable.",
            ),
            q(
                "Which is a multi-objective optimization approach used over candidates?",
                (
                    opt("NSGA-II genetic algorithm", correct=True),
                    opt("Plain linear regression"),
                    opt("k-means only"),
                    opt("A single random sample"),
                ),
                "NSGA-II is a Pareto-based multi-objective genetic algorithm.",
            ),
        ),
        "Benchmarking, validation and deployment": (
            q(
                "Which benchmark suites are standard for molecular generation?",
                (
                    opt("GuacaMol and MOSES", correct=True),
                    opt("ImageNet and COCO"),
                    opt("GLUE and SQuAD"),
                    opt("MNIST and CIFAR"),
                ),
                "GuacaMol and MOSES report validity, novelty, FCD and goal-directed scores.",
            ),
            q(
                "What does the Frechet ChemNet Distance (FCD) measure?",
                (
                    opt("Distributional similarity of generated to real molecules", correct=True),
                    opt("Exact binding free energy"),
                    opt("Synthesis cost"),
                    opt("Patent overlap"),
                ),
                "FCD compares feature distributions of generated and real sets.",
            ),
            q(
                "What is the only decisive validation of generated candidates?",
                (
                    opt("Synthesizing and assaying them in the make-test loop", correct=True),
                    opt("A higher FCD score"),
                    opt("Adding more training epochs"),
                    opt("Increasing the latent dimension"),
                ),
                "Wet-lab synthesis and assay, ideally in a closed loop, is decisive.",
            ),
        ),
    },
    final=(
        q(
            "What is the simple training objective of a denoising diffusion model?",
            (
                opt("Predicting the added noise via a mean-squared-error loss", correct=True),
                opt("Maximizing a discriminator's accuracy"),
                opt("Minimizing molecular weight"),
                opt("Counting valid SMILES"),
            ),
            "The network minimizes ||epsilon - epsilon_theta||^2.",
        ),
        q(
            "Why are equivariant networks preferred for 3D molecule generation?",
            (
                opt("They respect rotation/translation symmetry by construction", correct=True),
                opt("They are always faster than any model"),
                opt("They avoid using neural networks"),
                opt("They generate only 2D graphs"),
            ),
            "E(3)-equivariance is a strong, data-efficient inductive bias.",
        ),
        q(
            "What is the goal of structure-based (pocket-conditioned) design?",
            (
                opt("Generate ligands that fit and bind a specific protein pocket", correct=True),
                opt("Sequence a protein's DNA"),
                opt("Predict melting points only"),
                opt("Enumerate all possible molecules"),
            ),
            "It conditions generation on the 3D binding site.",
        ),
        q(
            "What does a Pareto front represent in multi-objective design?",
            (
                opt("The set of best achievable trade-offs among objectives", correct=True),
                opt("The single globally best molecule"),
                opt("A list of invalid molecules"),
                opt("The training loss curve"),
            ),
            "Designers pick operating points along the Pareto front of trade-offs.",
        ),
        q(
            "Which failure mode means the model just copies training data?",
            (
                opt("Memorization (low novelty)", correct=True),
                opt("Reward hacking"),
                opt("Posterior collapse"),
                opt("Gradient vanishing"),
            ),
            "Low novelty against the training set indicates memorization.",
        ),
        q(
            "Why is a tuned random or enumeration baseline important?",
            (
                opt("It often beats flashy models and exposes overstated claims", correct=True),
                opt("It guarantees synthesizable molecules"),
                opt("It replaces the need for benchmarks"),
                opt("It computes exact affinities"),
            ),
            "Honest reporting needs strong baselines to contextualize results.",
        ),
    ),
)
