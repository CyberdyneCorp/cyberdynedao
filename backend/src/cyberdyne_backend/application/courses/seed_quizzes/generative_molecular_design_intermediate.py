"""Quiz questions for the Generative Models for Molecular Design - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Variational autoencoders and the ELBO": (
            q(
                "What two terms make up the ELBO objective of a VAE?",
                (
                    opt("A reconstruction term and a KL-divergence regularizer", correct=True),
                    opt("A docking term and a synthesis term"),
                    opt("Two adversarial terms"),
                    opt("A reward and a baseline"),
                ),
                "ELBO = expected reconstruction log-likelihood minus KL to the prior.",
            ),
            q(
                "What does the reparameterization trick enable?",
                (
                    opt("Backpropagation through the sampling of z", correct=True),
                    opt("Removing the decoder entirely"),
                    opt("Exact docking scores"),
                    opt("Discrete graph generation only"),
                ),
                "Writing z = mu + sigma * epsilon makes sampling differentiable.",
            ),
            q(
                "What is 'posterior collapse' in a VAE?",
                (
                    opt("The decoder ignores z because the KL term is too strong", correct=True),
                    opt("The encoder produces 3D coordinates"),
                    opt("The reward becomes negative"),
                    opt("The discriminator wins the game"),
                ),
                "Too much KL weight can make z uninformative and ignored by the decoder.",
            ),
        ),
        "GANs for molecular generation": (
            q(
                "In a GAN, what is the role of the discriminator?",
                (
                    opt("To distinguish real molecules from generated ones", correct=True),
                    opt("To compute exact likelihood"),
                    opt("To dock molecules into a pocket"),
                    opt("To canonicalize SMILES"),
                ),
                "The discriminator classifies real vs fake; the generator tries to fool it.",
            ),
            q(
                "What is a common failure mode of molecular GANs like MolGAN?",
                (
                    opt("Mode collapse with low uniqueness", correct=True),
                    opt("Always exact likelihood"),
                    opt("Guaranteed 3D validity"),
                    opt("Infinite diversity"),
                ),
                "MolGAN is fast but prone to mode collapse (repetitive samples).",
            ),
            q(
                "Why is WGAN-GP used in molecular GAN training?",
                (
                    opt(
                        "To stabilize training via a Wasserstein loss and gradient penalty",
                        correct=True,
                    ),
                    opt("To remove the generator"),
                    opt("To compute docking energies"),
                    opt("To enforce Lipinski's rules"),
                ),
                "The Wasserstein distance with gradient penalty reduces instability.",
            ),
        ),
        "Graph-based molecular generation": (
            q(
                "What advantage does valence-masked graph generation provide?",
                (
                    opt(
                        "Near-100% chemical validity by enforcing valences each step", correct=True
                    ),
                    opt("Exact binding free energies"),
                    opt("Shorter strings"),
                    opt("Guaranteed novelty"),
                ),
                "Masking illegal bonds at each step keeps partial graphs valid.",
            ),
            q(
                "How do autoregressive graph models build a molecule?",
                (
                    opt("By adding atoms and bonds one step at a time", correct=True),
                    opt("By emitting the full adjacency tensor in one shot"),
                    opt("By diffusing 3D coordinates"),
                    opt("By docking into a pocket"),
                ),
                "They sequentially add nodes and edges with valence constraints.",
            ),
            q(
                "What network type processes molecular graphs by updating atoms from neighbors?",
                (
                    opt("Message-passing graph neural networks", correct=True),
                    opt("Fully connected image classifiers"),
                    opt("Recurrent audio models"),
                    opt("Decision forests"),
                ),
                "GNNs pass messages between neighboring atoms.",
            ),
        ),
        "Reinforcement learning for property optimization": (
            q(
                "In RL-based molecule design, what is the 'reward'?",
                (
                    opt("A score of the finished molecule's desired properties", correct=True),
                    opt("The KL divergence of the encoder"),
                    opt("The number of training epochs"),
                    opt("The SMILES string length only"),
                ),
                "Reward measures properties like predicted potency, QED or docking score.",
            ),
            q(
                "Why does REINVENT add a penalty toward a fixed prior policy?",
                (
                    opt(
                        "To keep the agent in realistic chemistry while earning reward",
                        correct=True,
                    ),
                    opt("To remove the reward signal"),
                    opt("To force mode collapse"),
                    opt("To compute exact likelihood"),
                ),
                "The prior penalty stops the agent drifting into invalid or bizarre molecules.",
            ),
            q(
                "What is 'reward hacking' in this context?",
                (
                    opt(
                        "Exploiting flaws in the scoring function to score high uselessly",
                        correct=True,
                    ),
                    opt("Encrypting the reward function"),
                    opt("Training without any data"),
                    opt("Adding more atoms to every molecule"),
                ),
                "The agent games an imperfect scorer instead of finding truly good molecules.",
            ),
        ),
        "Latent-space optimization and Bayesian search": (
            q(
                "Why is Bayesian optimization well-suited to molecular property search?",
                (
                    opt("It is sample-efficient when each evaluation is expensive", correct=True),
                    opt("It requires no surrogate model"),
                    opt("It guarantees the global optimum in one step"),
                    opt("It only works on images"),
                ),
                "BO minimizes costly evaluations like docking runs or assays.",
            ),
            q(
                "What does an acquisition function like Expected Improvement balance?",
                (
                    opt(
                        "Exploitation of high predictions against exploration of uncertainty",
                        correct=True,
                    ),
                    opt("Validity against novelty"),
                    opt("Encoder against decoder"),
                    opt("Atoms against bonds"),
                ),
                "Acquisition trades off predicted value and model uncertainty.",
            ),
            q(
                "What risk arises from optimizing too aggressively in latent space?",
                (
                    opt(
                        "Drifting into low-density regions that decode to invalid molecules",
                        correct=True,
                    ),
                    opt("The surrogate becomes exact"),
                    opt("The reward always increases forever"),
                    opt("The decoder disappears"),
                ),
                "Off-manifold latent points decode to unrealistic or invalid structures.",
            ),
        ),
    },
    final=(
        q(
            "What does maximizing the ELBO approximate?",
            (
                opt("The intractable log-likelihood of the data", correct=True),
                opt("The docking score"),
                opt("The number of valid samples"),
                opt("The discriminator accuracy"),
            ),
            "ELBO is a tractable lower bound on log p(x).",
        ),
        q(
            "Which method has no explicit likelihood and uses an adversarial game?",
            (
                opt("GAN", correct=True),
                opt("VAE"),
                opt("Normalizing flow"),
                opt("Autoregressive model"),
            ),
            "GANs train a generator against a discriminator without explicit likelihood.",
        ),
        q(
            "What is the key benefit of generating molecular graphs over raw SMILES?",
            (
                opt("Valence constraints give high validity at each step", correct=True),
                opt("Strings are always shorter"),
                opt("Graphs need no neural network"),
                opt("Graphs guarantee binding"),
            ),
            "Graph generation respects valence, avoiding many invalid outputs.",
        ),
        q(
            "What does the REINFORCE policy gradient maximize?",
            (
                opt("Expected reward of the generated molecules", correct=True),
                opt("The KL term of a VAE"),
                opt("The discriminator loss"),
                opt("The number of epochs"),
            ),
            "It increases the probability of high-reward action sequences.",
        ),
        q(
            "Which surrogate model is typically used in Bayesian optimization?",
            (
                opt("A Gaussian process", correct=True),
                opt("A GAN discriminator"),
                opt("A random forest of SMILES"),
                opt("A docking engine"),
            ),
            "BO commonly fits a Gaussian-process surrogate to observed points.",
        ),
        q(
            "What ties latent-space optimization back to a usable molecule?",
            (
                opt("Decoding the optimized latent vector z into a molecule", correct=True),
                opt("Discarding the decoder"),
                opt("Running a GAN discriminator"),
                opt("Computing the ELBO only"),
            ),
            "The VAE decoder maps the optimized z back to a concrete molecule.",
        ),
    ),
)
