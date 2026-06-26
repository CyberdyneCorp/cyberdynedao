"""Quiz questions for the Deep Learning for Biology - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Convolutional networks for sequences and images": (
            q(
                "What property makes CNNs good at detecting motifs anywhere in a sequence?",
                (
                    opt("Translation invariance from sliding filters", correct=True),
                    opt("Their use of recurrence over time"),
                    opt("Random weight initialisation"),
                    opt("Having no learnable parameters"),
                ),
                "A shared filter scans every position, detecting patterns regardless of location.",
            ),
            q(
                "What does pooling do in a CNN?",
                (
                    opt("Downsamples feature maps, adding robustness", correct=True),
                    opt("Adds new random filters"),
                    opt("Computes the loss"),
                    opt("Increases the input resolution"),
                ),
                "Pooling reduces spatial size and adds invariance.",
            ),
            q(
                "Why are CNNs parameter-efficient for DNA?",
                (
                    opt("A small filter is reused across the whole sequence", correct=True),
                    opt("They use one weight per nucleotide position"),
                    opt("They store the entire genome as weights"),
                    opt("They have no bias terms ever"),
                ),
                "Weight sharing keeps the parameter count low.",
            ),
        ),
        "Recurrent networks and sequence memory": (
            q(
                "What does an RNN maintain across a sequence?",
                (
                    opt("A hidden state carrying past information", correct=True),
                    opt("A fixed lookup table of outputs"),
                    opt("A separate model per position"),
                    opt("Nothing; each element is independent"),
                ),
                "The hidden state passes context forward through time.",
            ),
            q(
                "What problem limits plain RNNs on long sequences?",
                (
                    opt("Vanishing or exploding gradients", correct=True),
                    opt("Too few parameters to train"),
                    opt("Inability to read text"),
                    opt("Requiring labelled data only"),
                ),
                "Gradients shrink or blow up across many time steps.",
            ),
            q(
                "How do LSTMs and GRUs improve on plain RNNs?",
                (
                    opt("Gates learn what to keep, forget and output", correct=True),
                    opt("They remove the hidden state"),
                    opt("They process all positions in parallel with attention"),
                    opt("They eliminate the need for training"),
                ),
                "Gating preserves signal over long ranges.",
            ),
        ),
        "The attention mechanism": (
            q(
                "Attention computes an output as a weighted average of what?",
                (
                    opt("The values, weighted by query-key match", correct=True),
                    opt("The raw inputs, weighted equally"),
                    opt("The gradients of the loss"),
                    opt("The biases of each layer"),
                ),
                "Weights come from query-key similarity; they multiply the values.",
            ),
            q(
                "Why divide the dot products by sqrt(d_k)?",
                (
                    opt("To keep scores from growing large and saturating softmax", correct=True),
                    opt("To convert them to integers"),
                    opt("To remove the values entirely"),
                    opt("To make the model recurrent"),
                ),
                "Scaling stabilises the softmax for large key dimensions.",
            ),
            q(
                "What does protein attention often align with?",
                (
                    opt("Residue contacts in the folded structure", correct=True),
                    opt("The alphabetical order of amino acids"),
                    opt("The length of the sequence only"),
                    opt("Random positions"),
                ),
                "Attention maps frequently reflect co-varying contacting residues.",
            ),
        ),
        "Transformers and self-attention blocks": (
            q(
                "What two main sublayers make up a transformer block?",
                (
                    opt("Multi-head self-attention and a feed-forward layer", correct=True),
                    opt("A convolution and a pooling layer"),
                    opt("An RNN cell and a softmax"),
                    opt("Two embedding lookups"),
                ),
                "Each block stacks attention and a position-wise feed-forward net.",
            ),
            q(
                "Why do transformers need positional encodings?",
                (
                    opt("Attention is order-agnostic, so order must be supplied", correct=True),
                    opt("To reduce the number of parameters"),
                    opt("To convert text to images"),
                    opt("To remove residual connections"),
                ),
                "Self-attention has no built-in notion of sequence order.",
            ),
            q(
                "How does self-attention compute scale with sequence length?",
                (
                    opt("Quadratically (O(L^2)) per layer", correct=True),
                    opt("Constant regardless of length"),
                    opt("Logarithmically"),
                    opt("Linearly with no dependence on heads"),
                ),
                "Pairwise attention over all positions costs O(L^2).",
            ),
        ),
        "Embeddings and representing biology as vectors": (
            q(
                "What is a drawback of one-hot encoding amino acids?",
                (
                    opt("It is high-dimensional and ignores similarity", correct=True),
                    opt("It cannot be fed to any network"),
                    opt("It requires training a transformer first"),
                    opt("It encodes only DNA, never protein"),
                ),
                "One-hot vectors are sparse and treat all tokens as equidistant.",
            ),
            q(
                "What does an embedding layer learn?",
                (
                    opt("A dense vector per token so similar tokens are nearby", correct=True),
                    opt("A fixed random vector that never changes"),
                    opt("The loss function"),
                    opt("The learning rate schedule"),
                ),
                "Embeddings place chemically similar tokens close together.",
            ),
            q(
                "How are protein language model embeddings commonly reused?",
                (
                    opt("As features for downstream tasks via transfer learning", correct=True),
                    opt("Only to regenerate the original sequence"),
                    opt("To increase the learning rate"),
                    opt("They cannot be reused"),
                ),
                "Pretrained embeddings transfer to contact, function and effect tasks.",
            ),
        ),
    },
    final=(
        q(
            "Which architecture is best for detecting local DNA motifs?",
            (
                opt("A 1D convolutional network", correct=True),
                opt("A plain linear regression"),
                opt("A decision stump"),
                opt("A k-means clustering"),
            ),
            "CNN filters detect position-invariant local patterns.",
        ),
        q(
            "What is the core idea of attention?",
            (
                opt("Weight all positions by query-key similarity", correct=True),
                opt("Process one element at a time with memory"),
                opt("Pool features spatially"),
                opt("Embed tokens randomly"),
            ),
            "Attention lets any position attend to any other directly.",
        ),
        q(
            "Which models are built primarily on transformers in biology?",
            (
                opt("ESM and the Nucleotide Transformer", correct=True),
                opt("Linear discriminant analysis"),
                opt("Naive Bayes classifiers"),
                opt("Support vector machines only"),
            ),
            "Protein and nucleotide language models are transformer-based.",
        ),
        q(
            "Why do LSTMs handle long-range dependencies better than plain RNNs?",
            (
                opt("Gating mechanisms preserve gradient flow", correct=True),
                opt("They use convolution instead of recurrence"),
                opt("They have no hidden state"),
                opt("They ignore earlier inputs"),
            ),
            "Gates control memory and stabilise gradients.",
        ),
        q(
            "An embedding turns a biological token into what?",
            (
                opt("A learned dense vector", correct=True),
                opt("A single integer label"),
                opt("A loss value"),
                opt("A gradient"),
            ),
            "Embeddings are dense, learned representations.",
        ),
        q(
            "What limits naive self-attention on very long genomes?",
            (
                opt("Its O(L^2) compute and memory cost", correct=True),
                opt("It cannot represent order at all"),
                opt("It has no learnable parameters"),
                opt("It only works on images"),
            ),
            "Quadratic scaling motivates efficient-attention variants.",
        ),
    ),
)
