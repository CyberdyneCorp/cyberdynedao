"""Quiz questions for the Evolution & Ecology - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Variation: the raw material of evolution": (
            q(
                "What kind of variation can evolution act on over the long term?",
                (
                    opt("Heritable (genetic) variation", correct=True),
                    opt("Purely environmental variation"),
                    opt("Variation acquired during an individual's lifetime and not in DNA"),
                    opt("Random measurement error"),
                ),
                "Only the genetic component of variation is transmitted to offspring.",
            ),
            q(
                "What is the ultimate source of new alleles?",
                (
                    opt("Mutation", correct=True),
                    opt("Recombination alone"),
                    opt("Gene flow alone"),
                    opt("Natural selection"),
                ),
                "Recombination and gene flow rearrange or import existing alleles; mutation creates new ones.",
            ),
            q(
                "Why are many quantitative traits roughly normally distributed?",
                (
                    opt("They are controlled by many genes plus environment", correct=True),
                    opt("They are controlled by a single gene"),
                    opt("They are not heritable at all"),
                    opt("Selection forces a normal distribution"),
                ),
                "Polygenic traits with environmental input sum to an approximately normal distribution.",
            ),
        ),
        "Natural selection and adaptation": (
            q(
                "Fitness in evolutionary biology refers to:",
                (
                    opt("Expected number of surviving, reproducing offspring", correct=True),
                    opt("Physical strength of an individual"),
                    opt("Body size relative to others"),
                    opt("Lifespan only"),
                ),
                "Fitness is reproductive success, not athletic fitness.",
            ),
            q(
                "Which mode of selection favours the population mean and reduces variance?",
                (
                    opt("Stabilizing selection", correct=True),
                    opt("Directional selection"),
                    opt("Disruptive selection"),
                    opt("Random drift"),
                ),
                "Stabilizing selection favours intermediate phenotypes, e.g. human birth weight.",
            ),
            q(
                "Why is natural selection said to lack foresight?",
                (
                    opt(
                        "It acts only on currently available variation, not future needs",
                        correct=True,
                    ),
                    opt("It plans adaptations in advance"),
                    opt("It always produces perfect designs"),
                    opt("It works independently of the environment"),
                ),
                "Selection is constrained by history and produces 'good enough' solutions.",
            ),
        ),
        "The four forces of evolution": (
            q(
                "Mechanically, evolution is defined as:",
                (
                    opt("Change in allele frequencies across generations", correct=True),
                    opt("Change in an individual's phenotype during life"),
                    opt("The appearance of new species only"),
                    opt("Improvement toward a goal"),
                ),
                "Evolution at the population level is allele-frequency change over generations.",
            ),
            q(
                "Genetic drift is strongest in:",
                (
                    opt("Small populations", correct=True),
                    opt("Large populations"),
                    opt("Populations with high gene flow"),
                    opt("Populations under strong selection"),
                ),
                "Drift strength scales with 1/N, so it dominates when N is small.",
            ),
            q(
                "Which force homogenizes gene pools and opposes divergence?",
                (
                    opt("Gene flow (migration)", correct=True),
                    opt("Mutation"),
                    opt("Genetic drift"),
                    opt("Disruptive selection"),
                ),
                "Migration mixes alleles among populations, reducing differences between them.",
            ),
        ),
        "Evidence for common descent": (
            q(
                "Homologous structures (human arm, bat wing, whale flipper) indicate:",
                (
                    opt("Shared ancestry with the same underlying bones", correct=True),
                    opt("Convergent evolution from unrelated ancestors"),
                    opt("Identical function with no shared origin"),
                    opt("Random similarity"),
                ),
                "Homology is similarity due to common descent, unlike analogy from convergence.",
            ),
            q(
                "Which is the strongest molecular evidence for common descent?",
                (
                    opt("The near-universal genetic code shared across life", correct=True),
                    opt("All species having the same number of chromosomes"),
                    opt("Identical body plans across all animals"),
                    opt("The fossil record alone"),
                ),
                "A shared genetic code points to a common ancestor of cellular life.",
            ),
            q(
                "How does sequence identity between species typically change with divergence time?",
                (
                    opt("It decreases as substitutions accumulate", correct=True),
                    opt("It increases over time"),
                    opt("It stays exactly constant"),
                    opt("It is unrelated to time"),
                ),
                "More distantly related species share fewer identical residues.",
            ),
        ),
        "Ecology: the stage for selection": (
            q(
                "A population is best defined as:",
                (
                    opt("Individuals of the same species in a given area", correct=True),
                    opt("All species in a region"),
                    opt("A single organism"),
                    opt("Community plus abiotic environment"),
                ),
                "A population is one species; a community is many interacting species.",
            ),
            q(
                "A mutualistic interaction has which effect on the two partners?",
                (
                    opt("Benefit to both (+/+)", correct=True),
                    opt("Harm to both (-/-)"),
                    opt("Benefit to one, harm to the other (+/-)"),
                    opt("Benefit to one, no effect on the other (+/0)"),
                ),
                "Mutualism is +/+, e.g. pollinators and flowers.",
            ),
            q(
                "What does carrying capacity (K) represent?",
                (
                    opt("The maximum population size an environment can sustain", correct=True),
                    opt("The intrinsic growth rate"),
                    opt("The mutation rate"),
                    opt("The minimum viable population"),
                ),
                "Logistic growth slows and levels off as the population approaches K.",
            ),
        ),
    },
    final=(
        q(
            "Which combination is required for natural selection to occur?",
            (
                opt("Heritable variation, differential fitness, and overproduction", correct=True),
                opt("Identical individuals and unlimited resources"),
                opt("Only environmental variation"),
                opt("Random mating and infinite population size"),
            ),
            "Darwin's conditions: heritable variation, struggle for existence, and fitness differences.",
        ),
        q(
            "An allele increases in frequency purely by random chance in a small population. This is:",
            (
                opt("Genetic drift", correct=True),
                opt("Natural selection"),
                opt("Gene flow"),
                opt("Directional mutation"),
            ),
            "Random change from finite sampling is drift, strongest when N is small.",
        ),
        q(
            "Insect wings and bird wings perform the same function but evolved independently. They are:",
            (
                opt("Analogous structures (convergent evolution)", correct=True),
                opt("Homologous structures"),
                opt("Vestigial structures"),
                opt("Evidence against evolution"),
            ),
            "Similar function without shared ancestry is analogy from convergent selection.",
        ),
        q(
            "Which selection mode would tend to split one population toward two extremes?",
            (
                opt("Disruptive selection", correct=True),
                opt("Stabilizing selection"),
                opt("Purifying selection"),
                opt("No selection"),
            ),
            "Disruptive selection favours both extremes over the mean.",
        ),
        q(
            "The ecological niche of an organism is:",
            (
                opt("The set of resources and conditions it uses and tolerates", correct=True),
                opt("Only its physical location"),
                opt("Its number of offspring"),
                opt("Its DNA sequence"),
            ),
            "A niche is the multidimensional set of resources and conditions an organism exploits.",
        ),
        q(
            "Heterozygote frequency 2pq is maximized when:",
            (
                opt("p = q = 0.5", correct=True),
                opt("p is close to 1"),
                opt("q is close to 0"),
                opt("p = 0.9"),
            ),
            "2pq peaks at 0.5 when both alleles are at frequency 0.5.",
        ),
    ),
)
