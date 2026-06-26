"""Quiz questions for the Deep Learning for Biology - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Graph neural networks for molecules": (
            q(
                "How does a GNN update a node's representation?",
                (
                    opt("By aggregating messages from its neighbours", correct=True),
                    opt("By sorting all nodes alphabetically"),
                    opt("By ignoring the graph structure"),
                    opt("By a single global average only"),
                ),
                "Message passing aggregates neighbour information each round.",
            ),
            q(
                "Why is permutation invariance important for molecular GNNs?",
                (
                    opt("Predictions should not depend on arbitrary atom ordering", correct=True),
                    opt("It speeds up the optimiser"),
                    opt("It removes the need for edges"),
                    opt("It converts the graph to a sequence"),
                ),
                "A molecule's identity is independent of atom indexing.",
            ),
            q(
                "What problem arises from stacking too many message-passing layers?",
                (
                    opt("Over-smoothing, where node representations converge", correct=True),
                    opt("The graph loses all its edges"),
                    opt("The atoms double in number"),
                    opt("The model becomes linear"),
                ),
                "Deep GNNs can make all nodes look alike.",
            ),
        ),
        "Protein language models": (
            q(
                "What self-supervised objective trains a protein language model?",
                (
                    opt("Masked language modelling of residues", correct=True),
                    opt("Predicting the next pixel"),
                    opt("Clustering with k-means"),
                    opt("Manual labelling of every residue"),
                ),
                "Residues are masked and predicted from context.",
            ),
            q(
                "Which is a real protein language model?",
                (
                    opt("ESM-2", correct=True),
                    opt("BLASTn"),
                    opt("Clustal Omega"),
                    opt("Bowtie2"),
                ),
                "ESM-2 is a transformer-based protein language model.",
            ),
            q(
                "What empirical trend do protein language models show with scale?",
                (
                    opt(
                        "Capability improves roughly log-linearly with size and data", correct=True
                    ),
                    opt("Performance is independent of model size"),
                    opt("Larger models always perform worse"),
                    opt("They require no data"),
                ),
                "They follow NLP-like scaling laws with diminishing returns.",
            ),
        ),
        "Structure prediction with AlphaFold": (
            q(
                "What evolutionary information does AlphaFold exploit?",
                (
                    opt("Co-variation in a multiple sequence alignment", correct=True),
                    opt("The melting temperature of the protein"),
                    opt("The organism's body weight"),
                    opt("The sequencing machine model"),
                ),
                "Co-evolving residues signal spatial contacts.",
            ),
            q(
                "What does the AlphaFold pLDDT score measure?",
                (
                    opt("Per-residue confidence in the predicted structure", correct=True),
                    opt("The total number of atoms"),
                    opt("The expression level of the gene"),
                    opt("The learning rate used"),
                ),
                "pLDDT (0-100) rates confidence; low values often flag disorder.",
            ),
            q(
                "Which component reasons jointly over the MSA and residue pairs?",
                (
                    opt("The Evoformer", correct=True),
                    opt("A pooling layer"),
                    opt("A k-nearest-neighbour search"),
                    opt("A random forest"),
                ),
                "The Evoformer is AlphaFold2's central attention module.",
            ),
        ),
        "Generative models for molecular design": (
            q(
                "How does a diffusion model generate samples?",
                (
                    opt("By iteratively denoising from random noise", correct=True),
                    opt("By memorising the training set exactly"),
                    opt("By a single linear projection"),
                    opt("By sorting atoms by mass"),
                ),
                "Diffusion learns to reverse a noising process step by step.",
            ),
            q(
                "What does ProteinMPNN do?",
                (
                    opt("Designs sequences that fold to a target backbone", correct=True),
                    opt("Aligns two genomes"),
                    opt("Counts sequencing reads"),
                    opt("Measures gene expression"),
                ),
                "ProteinMPNN performs inverse folding (sequence design).",
            ),
            q(
                "Why pair a generative model with a property predictor?",
                (
                    opt("To enable goal-directed design toward desired properties", correct=True),
                    opt("To remove the need for any training"),
                    opt("To increase the learning rate"),
                    opt("To convert proteins into DNA"),
                ),
                "Scoring guides sampling toward valid, high-affinity candidates.",
            ),
        ),
        "Training, evaluation and trust in biological models": (
            q(
                "What is data leakage in a biological model?",
                (
                    opt("Highly similar sequences appear in both train and test", correct=True),
                    opt("Using too small a learning rate"),
                    opt("Having too many GPUs"),
                    opt("Storing data in a database"),
                ),
                "Similarity across splits inflates reported performance.",
            ),
            q(
                "Which metric is appropriate for imbalanced classification?",
                (
                    opt("AUPRC (area under precision-recall curve)", correct=True),
                    opt("Raw accuracy alone"),
                    opt("Sequence length"),
                    opt("The number of epochs"),
                ),
                "AUPRC is informative when positives are rare.",
            ),
            q(
                "Why does calibration matter clinically?",
                (
                    opt("Stated probabilities should match observed frequencies", correct=True),
                    opt("It makes training faster"),
                    opt("It removes the validation set"),
                    opt("It reduces the number of layers"),
                ),
                "Clinicians may act on the probability, so it must be honest.",
            ),
        ),
    },
    final=(
        q(
            "What is the central operation of a graph neural network?",
            (
                opt("Message passing between neighbouring nodes", correct=True),
                opt("Sliding convolution over pixels"),
                opt("Recurrent updates over time only"),
                opt("Global softmax over the dataset"),
            ),
            "GNNs aggregate neighbour messages to update nodes.",
        ),
        q(
            "Protein language models are trained mainly by:",
            (
                opt("Self-supervised masked residue prediction", correct=True),
                opt("Supervised labels for every protein function"),
                opt("Reinforcement learning from human feedback only"),
                opt("Hand-written rules"),
            ),
            "Masked language modelling needs no manual labels.",
        ),
        q(
            "AlphaFold2's accuracy depends strongly on:",
            (
                opt("The depth of the multiple sequence alignment", correct=True),
                opt("The color of the protein"),
                opt("The day of the week"),
                opt("The size of the lab"),
            ),
            "More homologues give stronger co-evolution signal, up to saturation.",
        ),
        q(
            "Diffusion models for protein design (e.g. RFdiffusion) work by:",
            (
                opt("Reversing a noising process to generate structures", correct=True),
                opt("Aligning sequences with dynamic programming"),
                opt("Counting k-mers"),
                opt("Running PCR in silico"),
            ),
            "They denoise from random noise into valid backbones.",
        ),
        q(
            "To avoid leakage when splitting protein data, you should:",
            (
                opt("Cluster by sequence identity and split between clusters", correct=True),
                opt("Split rows uniformly at random"),
                opt("Put every sequence in both train and test"),
                opt("Sort by length and take the first half"),
            ),
            "Cluster-aware splits prevent near-duplicate leakage.",
        ),
        q(
            "A well-calibrated model has a calibration curve that:",
            (
                opt("Lies close to the diagonal (predicted = observed)", correct=True),
                opt("Is flat at zero"),
                opt("Rises then crashes to zero"),
                opt("Is vertical"),
            ),
            "Predicted probabilities should match observed frequencies.",
        ),
    ),
)
