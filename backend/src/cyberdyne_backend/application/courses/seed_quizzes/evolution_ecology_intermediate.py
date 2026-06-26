"""Quiz questions for the Evolution & Ecology - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Hardy-Weinberg equilibrium": (
            q(
                "Under Hardy-Weinberg, the genotype frequencies for alleles at frequencies p and q are:",
                (
                    opt("p^2 + 2pq + q^2 = 1", correct=True),
                    opt("p + q = 2"),
                    opt("p^3 + q^3 = 1"),
                    opt("2p + 2q = 1"),
                ),
                "HW expands (p+q)^2 into homozygote and heterozygote frequencies.",
            ),
            q(
                "Why is Hardy-Weinberg useful as a null model?",
                (
                    opt(
                        "Deviations from it flag that an evolutionary force is acting", correct=True
                    ),
                    opt("It proves a population is evolving"),
                    opt("It measures mutation rate directly"),
                    opt("It only applies to asexual species"),
                ),
                "HW is the no-evolution baseline; deviations indicate selection, drift, etc.",
            ),
            q(
                "Which is NOT a Hardy-Weinberg assumption?",
                (
                    opt("Strong directional selection", correct=True),
                    opt("Random mating"),
                    opt("No migration"),
                    opt("Infinite population size"),
                ),
                "HW assumes no selection, no mutation, no migration, random mating, and no drift.",
            ),
        ),
        "Phylogenetics: reading the tree of life": (
            q(
                "A monophyletic group (clade) contains:",
                (
                    opt("An ancestor and all of its descendants", correct=True),
                    opt("An ancestor and only some descendants"),
                    opt("Unrelated species that look alike"),
                    opt("Only the most recent species"),
                ),
                "A clade includes a common ancestor and every descendant lineage.",
            ),
            q(
                "Which tree-inference method evaluates trees under an explicit substitution model?",
                (
                    opt("Maximum likelihood", correct=True),
                    opt("Maximum parsimony"),
                    opt("Eyeballing the alignment"),
                    opt("Alphabetical ordering of taxa"),
                ),
                "ML (and Bayesian) methods use models like Jukes-Cantor or GTR.",
            ),
            q(
                "Why must observed sequence differences be corrected for multiple hits?",
                (
                    opt(
                        "Multiple substitutions at the same site hide true changes, so observed differences saturate",
                        correct=True,
                    ),
                    opt("Sequences never change at the same site twice"),
                    opt("Observed differences always overestimate true distance"),
                    opt("Correction is only cosmetic"),
                ),
                "Repeated substitutions at a site cause observed identity to plateau below the true count.",
            ),
        ),
        "Speciation and reproductive isolation": (
            q(
                "Under the biological species concept, species are defined by:",
                (
                    opt("Reproductive isolation from other groups", correct=True),
                    opt("Identical appearance"),
                    opt("Living in the same habitat"),
                    opt("Equal body size"),
                ),
                "Species are reproductively isolated, interbreeding groups.",
            ),
            q(
                "Allopatric speciation is initiated by:",
                (
                    opt("A geographic barrier separating populations", correct=True),
                    opt("Polyploidy within one location"),
                    opt("Host shifts in the same area"),
                    opt("Random mating across populations"),
                ),
                "Allopatric speciation begins with geographic isolation, then divergence.",
            ),
            q(
                "Which is a prezygotic isolation barrier?",
                (
                    opt("Behavioral (mating signal) differences", correct=True),
                    opt("Hybrid sterility"),
                    opt("Hybrid inviability"),
                    opt("Hybrid breakdown in the F2 generation"),
                ),
                "Prezygotic barriers act before fertilization; sterility and inviability are postzygotic.",
            ),
        ),
        "Quantitative genetics and the breeder's equation": (
            q(
                "Narrow-sense heritability h^2 is defined as:",
                (
                    opt("V_A / V_P (additive variance over phenotypic variance)", correct=True),
                    opt("V_E / V_P"),
                    opt("V_P / V_G"),
                    opt("V_D / V_A"),
                ),
                "Narrow-sense heritability is the additive genetic fraction of phenotypic variance.",
            ),
            q(
                "The breeder's equation states that the response to selection R equals:",
                (
                    opt("h^2 times the selection differential S", correct=True),
                    opt("S divided by h^2"),
                    opt("V_E times S"),
                    opt("the mutation rate times S"),
                ),
                "R = h^2 * S predicts one generation of response to selection.",
            ),
            q(
                "If heritability is near zero, the response to a given selection differential will be:",
                (
                    opt("Near zero", correct=True),
                    opt("Maximal"),
                    opt("Negative"),
                    opt("Independent of heritability"),
                ),
                "With h^2 = 0, R = h^2 * S = 0: no heritable variation, no response.",
            ),
        ),
        "Population dynamics and species interactions": (
            q(
                "Exponential growth dN/dt = rN occurs when:",
                (
                    opt("Resources are unlimited", correct=True),
                    opt("The population is at carrying capacity"),
                    opt("Predators dominate"),
                    opt("The growth rate is zero"),
                ),
                "Unlimited resources give pure exponential growth.",
            ),
            q(
                "In the logistic model dN/dt = rN(1 - N/K), the population stabilizes at:",
                (
                    opt("N = K", correct=True),
                    opt("N = 0"),
                    opt("N = r"),
                    opt("N = 2K"),
                ),
                "Growth slows and equilibrium is reached at the carrying capacity K.",
            ),
            q(
                "The Lotka-Volterra predator-prey model characteristically produces:",
                (
                    opt("Out-of-phase oscillations of predator and prey", correct=True),
                    opt("Constant unchanging populations"),
                    opt("Immediate extinction of both"),
                    opt("Exponential growth of both forever"),
                ),
                "Predator and prey abundances oscillate, with the predator lagging the prey.",
            ),
        ),
    },
    final=(
        q(
            "A locus shows far fewer heterozygotes than 2pq predicts. This most likely indicates:",
            (
                opt("A deviation from Hardy-Weinberg, e.g. inbreeding or selection", correct=True),
                opt("Perfect Hardy-Weinberg equilibrium"),
                opt("Infinite population size"),
                opt("No alleles present"),
            ),
            "A heterozygote deficit signals a violated HW assumption such as nonrandom mating.",
        ),
        q(
            "Synapomorphies used to define clades are:",
            (
                opt("Shared derived characters", correct=True),
                opt("Shared ancestral characters"),
                opt("Convergent (analogous) traits"),
                opt("Randomly chosen traits"),
            ),
            "Clades are recognized by shared derived characters (synapomorphies).",
        ),
        q(
            "Polyploidy can cause speciation that is:",
            (
                opt("Sympatric and effectively instantaneous, common in plants", correct=True),
                opt("Always allopatric and gradual"),
                opt("Impossible in plants"),
                opt("Only postzygotic"),
            ),
            "Polyploidy creates instant reproductive isolation in the same area, common in plants.",
        ),
        q(
            "A trait has V_A = 30, V_D = 10, V_E = 60, so V_P = 100. Its narrow-sense heritability is:",
            (
                opt("0.30", correct=True),
                opt("0.40"),
                opt("0.60"),
                opt("0.10"),
            ),
            "h^2 = V_A / V_P = 30/100 = 0.30.",
        ),
        q(
            "In logistic growth, per-capita growth rate is highest when:",
            (
                opt("N is very small relative to K", correct=True),
                opt("N equals K"),
                opt("N exceeds K"),
                opt("N equals 2K"),
            ),
            "Per-capita rate r(1 - N/K) is maximal near N = 0 and falls to zero at K.",
        ),
        q(
            "Bootstrapping in phylogenetics is used to:",
            (
                opt("Estimate support for branches by resampling sites", correct=True),
                opt("Choose the substitution model"),
                opt("Align the sequences"),
                opt("Date the tree from fossils"),
            ),
            "Bootstrap resampling of alignment columns yields branch support values.",
        ),
    ),
)
