"""Quiz questions for the Phylogenetics & Molecular Evolution - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Bayesian inference and MCMC": (
            q(
                "Bayesian phylogenetics targets which quantity?",
                (
                    opt(
                        "The posterior probability of trees given the data and priors", correct=True
                    ),
                    opt("Only the maximum likelihood"),
                    opt("The p-distance"),
                    opt("The bootstrap proportion"),
                ),
                "Posterior = likelihood times prior, normalized over all trees.",
            ),
            q(
                "MCMC is used because:",
                (
                    opt(
                        "The marginal likelihood integral over all trees is intractable",
                        correct=True,
                    ),
                    opt("Likelihood cannot be computed at all"),
                    opt("There are only a few trees to evaluate"),
                    opt("Priors are unnecessary"),
                ),
                "MCMC samples the posterior without computing the normalizing constant.",
            ),
            q(
                "A standard MCMC convergence diagnostic is:",
                (
                    opt("Effective sample size (ESS) above ~200 after burn-in", correct=True),
                    opt("A bootstrap value above 50"),
                    opt("A p-distance below 0.75"),
                    opt("A single chain accepting every move"),
                ),
                "Low ESS or high split-frequency SD signals non-convergence.",
            ),
        ),
        "Relaxed clocks and molecular dating": (
            q(
                "A relaxed-clock model differs from a strict clock by:",
                (
                    opt("Allowing substitution rates to vary across branches", correct=True),
                    opt("Forbidding any rate variation"),
                    opt("Removing the need for calibrations"),
                    opt("Using parsimony instead of likelihood"),
                ),
                "Relaxed clocks (e.g. uncorrelated lognormal) let rates differ per branch.",
            ),
            q(
                "To convert branch lengths into calendar time you need:",
                (
                    opt("External calibrations such as fossils or tip dates", correct=True),
                    opt("Only a longer alignment"),
                    opt("A higher bootstrap value"),
                    opt("More substitution models"),
                ),
                "Calibrations anchor node ages; without them only relative time is known.",
            ),
            q(
                "Tip-dating is especially useful for:",
                (
                    opt("Rapidly evolving organisms like viruses sampled over time", correct=True),
                    opt("Slowly evolving deep nodes only"),
                    opt("Datasets with no time information"),
                    opt("Rooting by midpoint"),
                ),
                "Measurably evolving populations let sampling dates calibrate the clock.",
            ),
        ),
        "Multispecies coalescent and gene-tree discordance": (
            q(
                "Incomplete lineage sorting causes:",
                (
                    opt("Individual gene trees to disagree with the species tree", correct=True),
                    opt("All genes to share one identical history"),
                    opt("Alignments to fail"),
                    opt("Branch lengths to vanish"),
                ),
                "ILS is ancestral polymorphism that fails to sort before speciation.",
            ),
            q(
                "ASTRAL estimates a species tree by:",
                (
                    opt(
                        "Finding the tree agreeing with the most quartets across gene trees",
                        correct=True,
                    ),
                    opt("Concatenating all genes into one matrix"),
                    opt("Using parsimony on a single gene"),
                    opt("Ignoring gene trees entirely"),
                ),
                "ASTRAL is a quartet-based summary method consistent under the MSC.",
            ),
            q(
                "The 'anomaly zone' refers to the situation where:",
                (
                    opt("The most probable gene tree differs from the species tree", correct=True),
                    opt("All gene trees match the species tree"),
                    opt("There is no incomplete lineage sorting"),
                    opt("Branch lengths are very long"),
                ),
                "With very short internal branches, the common gene tree can be wrong.",
            ),
        ),
        "Phylogenomics at genome scale": (
            q(
                "In phylogenomics, why are high bootstrap values no longer reassuring?",
                (
                    opt(
                        "Huge datasets give strong support even to systematically wrong trees",
                        correct=True,
                    ),
                    opt("Bootstrap cannot be computed at scale"),
                    opt("There is no model misspecification"),
                    opt("Support always drops with more data"),
                ),
                "Sampling error shrinks while systematic bias dominates.",
            ),
            q(
                "Compositional heterogeneity (lineage-specific GC bias) is addressed by:",
                (
                    opt("Non-stationary models or amino-acid recoding", correct=True),
                    opt("Increasing bootstrap replicates"),
                    opt("Midpoint rooting"),
                    opt("Removing the outgroup"),
                ),
                "Stationarity violations need non-stationary models or recoding.",
            ),
            q(
                "Recommended practice for genome-scale trees is to:",
                (
                    opt(
                        "Run both concatenation and coalescent analyses and assess conflict",
                        correct=True,
                    ),
                    opt("Trust a single concatenated supermatrix tree"),
                    opt("Use parsimony on one gene"),
                    opt("Ignore gene-tree discordance"),
                ),
                "Comparing methods and quantifying conflict reveals bias and biology.",
            ),
        ),
        "Detecting selection with dN/dS": (
            q(
                "An omega (dN/dS) value greater than 1 indicates:",
                (
                    opt("Positive (diversifying) selection", correct=True),
                    opt("Purifying selection"),
                    opt("Strictly neutral evolution"),
                    opt("No selection can be inferred"),
                ),
                "Excess nonsynonymous change signals adaptive evolution.",
            ),
            q(
                "Why is a gene-wide, branch-wide average of omega often uninformative?",
                (
                    opt(
                        "Selection is usually episodic and site-specific, so averaging hides it",
                        correct=True,
                    ),
                    opt("dN and dS cannot be measured"),
                    opt("Omega is always exactly 1"),
                    opt("Synonymous sites do not exist"),
                ),
                "Site and branch-site models are needed to detect localized selection.",
            ),
            q(
                "Branch-site tests in PAML or HyPhy detect positive selection using:",
                (
                    opt(
                        "A likelihood-ratio test between null and alternative codon models",
                        correct=True,
                    ),
                    opt("A bootstrap of taxa"),
                    opt("The p-distance"),
                    opt("Midpoint rooting"),
                ),
                "LRTs compare a model allowing omega>1 against one that does not.",
            ),
        ),
        "Machine learning for phylogenetics": (
            q(
                "How are ML models for phylogenetics typically trained?",
                (
                    opt("On large numbers of simulated alignments with known trees", correct=True),
                    opt("On a single real alignment"),
                    opt("Without any training data"),
                    opt("Only on distance matrices"),
                ),
                "Simulation provides labelled data for the inverse inference problem.",
            ),
            q(
                "A key appeal of learned inference over full likelihood/Bayesian methods is:",
                (
                    opt("Speed, especially for screening and hard regimes like LBA", correct=True),
                    opt("Guaranteed calibrated uncertainty without checks"),
                    opt("No need to validate results"),
                    opt("Elimination of all model assumptions forever"),
                ),
                "ML is fast and robust in tough regimes but still needs validation.",
            ),
            q(
                "Why are out-of-distribution checks essential for ML phylogenetics?",
                (
                    opt(
                        "A net trained on one model class can fail silently on data that violate it",
                        correct=True,
                    ),
                    opt("Neural networks never make mistakes"),
                    opt("Real data always match the simulator"),
                    opt("Training data are irrelevant"),
                ),
                "Generalization failure is hidden unless OOD performance is tested.",
            ),
        ),
    },
    final=(
        q(
            "The posterior distribution from Bayesian phylogenetics is summarized as:",
            (
                opt("A consensus tree with posterior probabilities on clades", correct=True),
                opt("A single parsimony tree"),
                opt("A distance matrix"),
                opt("A bootstrap percentage only"),
            ),
            "Posterior clade probabilities come from the sampled tree distribution.",
        ),
        q(
            "Molecular dating requires, in addition to sequences:",
            (
                opt(
                    "Calibrations (fossils, biogeography or tip dates) and a clock model",
                    correct=True,
                ),
                opt("Only a larger bootstrap"),
                opt("Removal of all rate variation"),
                opt("A polyphyletic outgroup"),
            ),
            "Calibrations anchor the relaxed-clock conversion to absolute time.",
        ),
        q(
            "Gene-tree/species-tree discordance from incomplete lineage sorting is modelled by:",
            (
                opt("The multispecies coalescent", correct=True),
                opt("The Jukes-Cantor correction"),
                opt("Midpoint rooting"),
                opt("The Fitch algorithm"),
            ),
            "The MSC embeds coalescent processes inside the species tree.",
        ),
        q(
            "In phylogenomics, strongly supported but wrong trees usually arise from:",
            (
                opt("Systematic error such as model misspecification", correct=True),
                opt("Too little data"),
                opt("Using likelihood instead of parsimony"),
                opt("Rooting with an outgroup"),
            ),
            "At genome scale, bias rather than sampling error dominates.",
        ),
        q(
            "An omega (dN/dS) below 1 across a protein-coding gene indicates:",
            (
                opt("Purifying (negative) selection", correct=True),
                opt("Positive selection"),
                opt("No homology"),
                opt("Saturation of synonymous sites"),
            ),
            "Most amino acids are constrained, giving dN/dS < 1.",
        ),
        q(
            "Machine-learning phylogenetic methods are best regarded as:",
            (
                opt("Complements to model-based inference, requiring validation", correct=True),
                opt("Full replacements that need no checking"),
                opt("Methods that avoid all training data"),
                opt("Distance-only clustering tools"),
            ),
            "ML adds speed; model-based methods give calibrated uncertainty.",
        ),
    ),
)
