"""Quiz questions for the Systems & Network Biology - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Multi-omics data integration": (
            q(
                "What is the central challenge of multi-omics integration?",
                (
                    opt(
                        "Combining noisy layers of different scale into a coherent model",
                        correct=True,
                    ),
                    opt("Sequencing a single gene"),
                    opt("Avoiding all computation"),
                    opt("Measuring only one omics layer"),
                ),
                "Each layer is a different view of the same underlying state.",
            ),
            q(
                "Which method learns shared latent factors across omics layers?",
                (
                    opt("MOFA (multi-omics factor analysis)", correct=True),
                    opt("Smith-Waterman"),
                    opt("Gillespie SSA"),
                    opt("Linear programming"),
                ),
                "MOFA factorises multiple layers into shared latent factors.",
            ),
            q(
                "Why does explained variance saturate with the number of latent factors?",
                (
                    opt("A few factors capture most of the joint variation", correct=True),
                    opt("Each factor explains exactly the same amount"),
                    opt("Factors add no information"),
                    opt("Variance is always zero"),
                ),
                "Most joint variance lies along a handful of axes.",
            ),
        ),
        "Single-cell network inference": (
            q(
                "Why is single-cell RNA-seq valuable for network inference?",
                (
                    opt(
                        "It exposes heterogeneity and gives many observations to infer regulation",
                        correct=True,
                    ),
                    opt("It measures only one cell ever"),
                    opt("It removes all biological variation"),
                    opt("It cannot detect gene expression"),
                ),
                "Thousands of individual cells provide the data GRN inference needs.",
            ),
            q(
                "What does RNA velocity use to infer the direction of change?",
                (
                    opt("The ratio of unspliced to spliced reads", correct=True),
                    opt("The total genome size"),
                    opt("The number of chromosomes"),
                    opt("The protein melting temperature"),
                ),
                "Unspliced/spliced ratios indicate where expression is heading.",
            ),
            q(
                "Which tool adds motif-based pruning to single-cell GRN inference?",
                (
                    opt("SCENIC", correct=True),
                    opt("COBRApy"),
                    opt("BLAST"),
                    opt("ImageJ"),
                ),
                "SCENIC keeps edges supported by regulator binding motifs.",
            ),
        ),
        "Whole-cell models and digital twins": (
            q(
                "What does a whole-cell model aim to simulate?",
                (
                    opt("Every known molecular function of a cell simultaneously", correct=True),
                    opt("Only the metabolism of one pathway"),
                    opt("Just the genome sequence"),
                    opt("A single enzyme reaction"),
                ),
                "The 2012 M. genitalium model coupled 28 sub-models.",
            ),
            q(
                "Whole-cell models are described as which kind of approach?",
                (
                    opt("Multi-scale and hybrid (different formalisms per process)", correct=True),
                    opt("Single-equation linear only"),
                    opt("Purely statistical with no mechanism"),
                    opt("Sequence alignment only"),
                ),
                "They combine FBA, ODEs and stochastic processes synchronised each step.",
            ),
            q(
                "What is a biological digital twin?",
                (
                    opt(
                        "A continuously updated computational replica used to predict interventions",
                        correct=True,
                    ),
                    opt("A cloned laboratory animal"),
                    opt("A backup DNA sample"),
                    opt("A second physical microscope"),
                ),
                "Digital twins are data-fed in-silico replicas of a specific system.",
            ),
        ),
        "Synthetic biology design principles": (
            q(
                "What does the genetic toggle switch (Gardner et al. 2000) implement?",
                (
                    opt("Bistable memory from two mutually repressing genes", correct=True),
                    opt("A sustained oscillation"),
                    opt("A metabolic flux maximiser"),
                    opt("A sequence aligner"),
                ),
                "Two cross-repressing genes give two stable states (memory).",
            ),
            q(
                "What is the synthetic-biology engineering cycle?",
                (
                    opt("Design - Build - Test - Learn", correct=True),
                    opt("Measure - Forget - Repeat"),
                    opt("Sequence - Stop"),
                    opt("Sample - Discard"),
                ),
                "Model-guided design iterates through build, test and learn.",
            ),
            q(
                "Which real-world constraint couples otherwise separate synthetic circuits?",
                (
                    opt(
                        "Load and resource competition for shared ribosomes/polymerase",
                        correct=True,
                    ),
                    opt("The color of the colony"),
                    opt("The lab's room temperature alone"),
                    opt("The font of the part labels"),
                ),
                "Shared cellular machinery makes parts interfere via load.",
            ),
        ),
        "Emergent and collective behaviour": (
            q(
                "What does quorum sensing let a bacterial population do?",
                (
                    opt(
                        "Coordinate a synchronous response above a density threshold", correct=True
                    ),
                    opt("Replicate faster than physics allows"),
                    opt("Ignore all neighbours"),
                    opt("Permanently stop dividing"),
                ),
                "An autoinducer reports density and triggers a group decision.",
            ),
            q(
                "Turing reaction-diffusion patterns require what ingredients?",
                (
                    opt("A short-range activator and a long-range inhibitor", correct=True),
                    opt("Only a single diffusing species"),
                    opt("No diffusion at all"),
                    opt("A perfectly uniform field forever"),
                ),
                "Differential diffusion of activator and inhibitor breaks symmetry.",
            ),
            q(
                "What is the common principle behind these collective phenomena?",
                (
                    opt("Local rules plus coupling produce global order (emergence)", correct=True),
                    opt("A single cell dictates everything"),
                    opt("Order requires no interactions"),
                    opt("Randomness alone with no rules"),
                ),
                "Coupled local interactions self-organise into global patterns.",
            ),
        ),
    },
    final=(
        q(
            "Which method integrates multiple omics layers into shared latent factors?",
            (
                opt("MOFA", correct=True),
                opt("FBA"),
                opt("BLAST"),
                opt("Gillespie SSA"),
            ),
            "MOFA learns latent factors explaining joint variation.",
        ),
        q(
            "What does RNA velocity add to a static single-cell snapshot?",
            (
                opt("A direction of future expression change", correct=True),
                opt("The genome assembly"),
                opt("The protein structure"),
                opt("The metabolic flux cone"),
            ),
            "Unspliced/spliced ratios infer dynamics from a snapshot.",
        ),
        q(
            "The 2012 whole-cell model of M. genitalium is notable because it",
            (
                opt("Predicted phenotype from genotype by coupling many sub-models", correct=True),
                opt("Modelled only glycolysis"),
                opt("Used a single ODE"),
                opt("Ignored metabolism entirely"),
            ),
            "It integrated 28 sub-models across formalisms.",
        ),
        q(
            "The repressilator and toggle switch are foundational examples of what field?",
            (
                opt("Synthetic biology", correct=True),
                opt("Sanger sequencing"),
                opt("X-ray crystallography"),
                opt("Mass spectrometry"),
            ),
            "Both are engineered genetic circuits.",
        ),
        q(
            "Quorum sensing produces what type of input-output behaviour?",
            (
                opt("A sharp, density-dependent switch", correct=True),
                opt("A perfectly linear response"),
                opt("No response at any density"),
                opt("A decaying exponential to zero"),
            ),
            "Response is near-zero below and saturating above a critical density.",
        ),
        q(
            "What unifies quorum sensing, synchronised clocks and Turing patterns?",
            (
                opt("Emergence: local rules plus coupling yield global order", correct=True),
                opt("They all require a single cell only"),
                opt("They forbid any interaction"),
                opt("They are purely random with no structure"),
            ),
            "Collective behaviour emerges from coupled local interactions.",
        ),
    ),
)
