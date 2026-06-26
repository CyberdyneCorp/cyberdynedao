"""Quiz questions for the Cheminformatics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Chemical space and dimensionality reduction": (
            q(
                "What is 'chemical space'?",
                (
                    opt(
                        "A high-dimensional space whose axes are molecular features, with molecules as points",
                        correct=True,
                    ),
                    opt("The physical lab where chemistry is done"),
                    opt("A single number per molecule"),
                    opt("A protein binding pocket"),
                ),
                "Each molecule is a point in a feature-defined high-dimensional space.",
            ),
            q(
                "Which method is a linear dimensionality reduction technique?",
                (
                    opt("PCA", correct=True),
                    opt("t-SNE"),
                    opt("UMAP"),
                    opt("Taylor-Butina clustering"),
                ),
                "PCA is linear; t-SNE and UMAP are non-linear neighbourhood-preserving.",
            ),
            q(
                "The curse of dimensionality means that in high dimensions:",
                (
                    opt("Distances concentrate and become less discriminating", correct=True),
                    opt("Distances become infinitely large and useful"),
                    opt("Every molecule becomes identical"),
                    opt("Computation becomes free"),
                ),
                "Distance contrast shrinks, motivating reduction and careful metrics.",
            ),
        ),
        "Clustering chemical libraries": (
            q(
                "Why cluster a chemical library?",
                (
                    opt(
                        "To pick diverse representatives, deduplicate series and summarise hits",
                        correct=True,
                    ),
                    opt("To compute exact binding energies"),
                    opt("To synthesise compounds automatically"),
                    opt("To draw 3D structures"),
                ),
                "Clustering groups similar molecules for selection and summary.",
            ),
            q(
                "The Taylor-Butina algorithm clusters using:",
                (
                    opt(
                        "A Tanimoto similarity threshold, greedily around the most-connected molecules",
                        correct=True,
                    ),
                    opt("A fixed number k chosen in advance"),
                    opt("Gradient descent on coordinates"),
                    opt("Random assignment"),
                ),
                "Butina is deterministic and threshold-based, needing no preset k.",
            ),
            q(
                "As the similarity threshold is loosened, the number of clusters tends to:",
                (
                    opt("Decrease as clusters merge", correct=True),
                    opt("Increase without bound"),
                    opt("Stay exactly constant"),
                    opt("Become negative"),
                ),
                "Looser thresholds merge molecules into fewer, larger clusters.",
            ),
        ),
        "RDKit workflows in practice": (
            q(
                "RDKit is best described as:",
                (
                    opt("A leading open-source cheminformatics toolkit", correct=True),
                    opt("A commercial-only docking suite"),
                    opt("A database of genomes"),
                    opt("A spreadsheet program"),
                ),
                "RDKit is the standard open-source toolkit for these workflows.",
            ),
            q(
                "Why is standardisation (salt stripping, charge/tautomer normalisation) important?",
                (
                    opt(
                        "So the same compound is not counted twice and similarity is accurate",
                        correct=True,
                    ),
                    opt("To increase the file size"),
                    opt("To make SMILES longer"),
                    opt("It has no practical effect"),
                ),
                "Without standardisation, duplicate and similarity counts are silently inflated.",
            ),
            q(
                "What are PAINS filters used for?",
                (
                    opt("Removing frequent assay-interference false positives", correct=True),
                    opt("Computing logP"),
                    opt("Generating 3D conformers"),
                    opt("Naming molecules"),
                ),
                "PAINS substructures flag pan-assay interference compounds.",
            ),
        ),
        "Graph neural networks and learned representations": (
            q(
                "How do graph neural networks differ from fixed fingerprints?",
                (
                    opt(
                        "They learn a representation directly from the molecular graph rather than using predefined features",
                        correct=True,
                    ),
                    opt("They ignore the molecular graph entirely"),
                    opt("They only work on text, not graphs"),
                    opt("They require no training data ever"),
                ),
                "GNNs learn differentiable representations from the graph.",
            ),
            q(
                "In a message-passing network, after k rounds an atom's embedding summarises:",
                (
                    opt("Its k-hop neighbourhood", correct=True),
                    opt("The entire periodic table"),
                    opt("Only its own element"),
                    opt("A random subset of atoms"),
                ),
                "k rounds of message passing aggregate information from k hops away.",
            ),
            q(
                "Compared with a simple ECFP + random-forest model, learned GNNs tend to:",
                (
                    opt("Overtake it as the amount of training data grows", correct=True),
                    opt("Always win even with tiny datasets"),
                    opt("Never be competitive"),
                    opt("Require no readout step"),
                ),
                "Learned representations show a learning-curve crossover with more data.",
            ),
        ),
        "Generative models for de novo design": (
            q(
                "What is de novo molecular design?",
                (
                    opt(
                        "Generating new molecules with desired properties rather than screening existing ones",
                        correct=True,
                    ),
                    opt("Renaming known molecules"),
                    opt("Measuring melting points"),
                    opt("Storing molecules in a database"),
                ),
                "Generative models sample novel candidates from a learned distribution.",
            ),
            q(
                "Which is a standard evaluation axis for generative models?",
                (
                    opt("Validity, uniqueness and novelty of generated molecules", correct=True),
                    opt("The font used in the SMILES"),
                    opt("The number of authors"),
                    opt("The price of electricity"),
                ),
                "Validity, uniqueness, novelty and synthetic accessibility are key metrics.",
            ),
            q(
                "Why is multi-objective optimisation central to de novo design?",
                (
                    opt(
                        "Improving potency often hurts drug-likeness or synthesisability, so goals must be balanced",
                        correct=True,
                    ),
                    opt("There is only ever one objective"),
                    opt("Objectives never conflict"),
                    opt("It is irrelevant to design"),
                ),
                "Competing goals require Pareto or weighted-reward balancing.",
            ),
        ),
    },
    final=(
        q(
            "Which technique is a non-linear, neighbourhood-preserving embedding method?",
            (
                opt("UMAP", correct=True),
                opt("PCA"),
                opt("Linear regression"),
                opt("Tanimoto coefficient"),
            ),
            "UMAP and t-SNE are non-linear; PCA is linear.",
        ),
        q(
            "The Taylor-Butina clustering algorithm requires:",
            (
                opt("A Tanimoto threshold, but not a preset number of clusters", correct=True),
                opt("A fixed k chosen in advance"),
                opt("3D coordinates only"),
                opt("A neural network"),
            ),
            "Butina is threshold-based and determines clusters automatically.",
        ),
        q(
            "Before similarity analysis in RDKit you should:",
            (
                opt(
                    "Standardise structures (strip salts, normalise charges/tautomers)",
                    correct=True,
                ),
                opt("Randomly shuffle the atoms"),
                opt("Delete all hydrogens permanently"),
                opt("Convert everything to images"),
            ),
            "Standardisation prevents duplicate inflation and bad similarity scores.",
        ),
        q(
            "A message-passing GNN's final molecule vector is produced by a:",
            (
                opt("Readout / pooling step over atom embeddings", correct=True),
                opt("Single matrix inversion"),
                opt("Fourier transform"),
                opt("Random number generator"),
            ),
            "Readout pools per-atom embeddings into one molecule representation.",
        ),
        q(
            "Which property is NOT typically a generative-model evaluation metric?",
            (
                opt("The retail price of the starting reagents", correct=True),
                opt("Validity"),
                opt("Novelty"),
                opt("Synthetic accessibility"),
            ),
            "Validity, uniqueness, novelty and SA are standard; reagent price is not.",
        ),
        q(
            "Frameworks like REINVENT optimise generators using:",
            (
                opt(
                    "Reinforcement learning toward a multi-component scoring function", correct=True
                ),
                opt("Manual atom-by-atom drawing only"),
                opt("Random SMILES with no scoring"),
                opt("Exact enumeration of 10^60 molecules"),
            ),
            "REINVENT couples an RNN generator to RL with a composite reward.",
        ),
    ),
)
