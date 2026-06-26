"""Quiz questions for the Phylogenetics & Molecular Evolution - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Maximum parsimony and homoplasy": (
            q(
                "Maximum parsimony selects the tree that:",
                (
                    opt("Requires the fewest character-state changes", correct=True),
                    opt("Has the most changes"),
                    opt("Has the longest branches"),
                    opt("Maximizes the likelihood"),
                ),
                "MP minimizes the total number of evolutionary changes (tree length).",
            ),
            q(
                "Long-branch attraction is a failure mode in which:",
                (
                    opt(
                        "Two unrelated long branches are grouped due to chance similarity",
                        correct=True,
                    ),
                    opt("Short branches always merge"),
                    opt("The root is removed"),
                    opt("All taxa get equal branch lengths"),
                ),
                "Independent changes on long branches coincide and mislead parsimony.",
            ),
            q(
                "The Fitch algorithm computes a character's minimum changes by:",
                (
                    opt(
                        "A post-order pass taking intersections or unions of child state sets",
                        correct=True,
                    ),
                    opt("Random guessing"),
                    opt("Exponentiating the rate matrix"),
                    opt("Sampling from the posterior"),
                ),
                "Empty intersection forces a union and adds one step.",
            ),
        ),
        "Substitution models: from JC69 to GTR": (
            q(
                "Over a branch of length t, the transition probabilities are given by:",
                (
                    opt("The matrix exponential P(t) = exp(Qt)", correct=True),
                    opt("The determinant of Q"),
                    opt("The inverse of Q"),
                    opt("Q multiplied by t only"),
                ),
                "Continuous-time Markov chains give P(t) = e^{Qt}.",
            ),
            q(
                "What distinguishes the GTR model from JC69?",
                (
                    opt(
                        "GTR allows six exchangeability rates and unequal base frequencies",
                        correct=True,
                    ),
                    opt("GTR assumes equal base frequencies and one rate"),
                    opt("GTR ignores transitions"),
                    opt("GTR cannot be time-reversible"),
                ),
                "GTR is the most general time-reversible nucleotide model.",
            ),
            q(
                "Under JC69, the probability that a site differs from its ancestor:",
                (
                    opt("Rises and plateaus at 3/4 with time", correct=True),
                    opt("Decreases to zero"),
                    opt("Grows without bound"),
                    opt("Stays exactly at p-distance"),
                ),
                "The equilibrium difference probability is 3/4, causing saturation.",
            ),
        ),
        "Among-site rate variation and the gamma model": (
            q(
                "Among-site rate variation is commonly modelled with a:",
                (
                    opt("Gamma distribution of site rates (mean 1, shape alpha)", correct=True),
                    opt("Uniform rate for every site"),
                    opt("Poisson tree prior"),
                    opt("Linear rate increase"),
                ),
                "The +G model draws per-site rates from a gamma with shape alpha.",
            ),
            q(
                "A small gamma shape parameter alpha (less than 1) implies:",
                (
                    opt("Strong rate heterogeneity: most sites slow, a few fast", correct=True),
                    opt("All sites evolve identically"),
                    opt("No invariant sites"),
                    opt("A strict molecular clock"),
                ),
                "Small alpha gives an L-shaped density with extreme heterogeneity.",
            ),
            q(
                "The '+I' addition to a model accounts for:",
                (
                    opt("A proportion of invariant sites that never change", correct=True),
                    opt("Insertions and deletions"),
                    opt("The ingroup taxa"),
                    opt("Internal nodes"),
                ),
                "+I models a class of completely invariant positions.",
            ),
        ),
        "Maximum likelihood and tree search": (
            q(
                "Felsenstein's pruning algorithm computes the likelihood by:",
                (
                    opt(
                        "A post-order pass combining subtree conditional likelihoods", correct=True
                    ),
                    opt("Counting parsimony steps"),
                    opt("Resampling columns"),
                    opt("Averaging distances"),
                ),
                "Pruning combines conditional likelihoods via transition probabilities.",
            ),
            q(
                "Why is exhaustive topology search impossible for many taxa?",
                (
                    opt("The number of trees grows super-exponentially, as (2n-5)!!", correct=True),
                    opt("Each tree takes forever to draw"),
                    opt("Likelihood cannot be computed"),
                    opt("There are only a few possible trees"),
                ),
                "The tree space explodes, so heuristic search is required.",
            ),
            q(
                "NNI, SPR and TBR are:",
                (
                    opt("Topology rearrangement moves used in heuristic tree search", correct=True),
                    opt("Substitution models"),
                    opt("Distance corrections"),
                    opt("Bootstrap methods"),
                ),
                "They propose new topologies to climb toward higher likelihood.",
            ),
        ),
        "Bootstrap support and model selection": (
            q(
                "The nonparametric bootstrap assesses clade support by:",
                (
                    opt(
                        "Resampling alignment columns with replacement and re-inferring trees",
                        correct=True,
                    ),
                    opt("Removing one taxon at a time"),
                    opt("Changing the substitution model"),
                    opt("Adding random sequences"),
                ),
                "Bootstrap support is the percentage of pseudo-replicates recovering a clade.",
            ),
            q(
                "Two nested substitution models are best compared with:",
                (
                    opt("A likelihood-ratio test (chi-square distributed)", correct=True),
                    opt("A bootstrap"),
                    opt("A distance matrix"),
                    opt("Midpoint rooting"),
                ),
                "The LRT applies to nested models; AIC/BIC handle non-nested ones.",
            ),
            q(
                "The Akaike Information Criterion, AIC = 2k - 2lnL, penalizes:",
                (
                    opt("The number of parameters k", correct=True),
                    opt("The number of taxa"),
                    opt("The branch lengths"),
                    opt("The alignment length only"),
                ),
                "AIC trades model fit against parameter count to avoid overfitting.",
            ),
        ),
    },
    final=(
        q(
            "Maximum parsimony can be statistically inconsistent because of:",
            (
                opt("Long-branch attraction under high homoplasy", correct=True),
                opt("Too few parameters in the rate matrix"),
                opt("Using an outgroup"),
                opt("Gamma-distributed rates"),
            ),
            "LBA can drive parsimony to the wrong tree even with more data.",
        ),
        q(
            "The substitution probability over time is obtained from the rate matrix by:",
            (
                opt("Matrix exponentiation, P(t) = exp(Qt)", correct=True),
                opt("Bootstrapping"),
                opt("Taking the p-distance"),
                opt("Counting parsimony steps"),
            ),
            "Continuous-time Markov models give P(t) = e^{Qt}.",
        ),
        q(
            "The 'GTR+G+I' model name indicates:",
            (
                opt(
                    "General time-reversible substitution with gamma rates and invariant sites",
                    correct=True,
                ),
                opt("Equal base frequencies and one rate"),
                opt("A distance-only method"),
                opt("A rooting procedure"),
            ),
            "GTR substitution, +G rate variation, +I invariant class.",
        ),
        q(
            "Maximum likelihood searches tree space using:",
            (
                opt("Heuristic rearrangements such as NNI, SPR and TBR", correct=True),
                opt("Exhaustive enumeration for any number of taxa"),
                opt("Random tree selection only"),
                opt("Midpoint rooting"),
            ),
            "Heuristics are needed because exhaustive search is intractable.",
        ),
        q(
            "Bootstrap support values are best interpreted as:",
            (
                opt(
                    "The frequency with which a clade recurs across resampled datasets",
                    correct=True,
                ),
                opt("The number of substitutions on a branch"),
                opt("The posterior probability of the tree"),
                opt("The gamma shape parameter"),
            ),
            "They estimate repeatability of a clade under column resampling.",
        ),
        q(
            "ModelFinder / ModelTest-NG choose a substitution model by:",
            (
                opt("Ranking candidates with criteria like AIC or BIC", correct=True),
                opt("Picking the model with the most parameters"),
                opt("Using the longest branch"),
                opt("Resampling taxa"),
            ),
            "Information criteria balance fit against complexity.",
        ),
    ),
)
