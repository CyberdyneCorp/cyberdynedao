"""Quiz questions for the Genetics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Linkage, recombination and genetic mapping": (
            q(
                "What is the maximum possible recombination frequency between two loci?",
                (
                    opt("0.5", correct=True),
                    opt("1.0"),
                    opt("0.25"),
                    opt("2.0"),
                ),
                "At RF = 0.5 loci behave as if unlinked; it cannot exceed one half.",
            ),
            q(
                "One centiMorgan (map unit) corresponds to what?",
                (
                    opt("1% recombination frequency", correct=True),
                    opt("One base pair"),
                    opt("One chromosome"),
                    opt("10% recombination frequency"),
                ),
                "1 cM = 1% recombinants, approximating distance for nearby loci.",
            ),
            q(
                "Why does raw recombination frequency underestimate distance for far-apart loci?",
                (
                    opt("Double crossovers go undetected", correct=True),
                    opt("Mutation rates are too high"),
                    opt("DNA repair removes the markers"),
                    opt("The loci are on different chromosomes"),
                ),
                "Even-numbered crossovers restore the parental arrangement, hiding recombination.",
            ),
        ),
        "Mutation: types, rates and consequences": (
            q(
                "A point mutation that changes one codon to a stop codon is called what?",
                (
                    opt("Nonsense mutation", correct=True),
                    opt("Silent mutation"),
                    opt("Missense mutation"),
                    opt("Synonymous mutation"),
                ),
                "A nonsense mutation introduces a premature stop, truncating the protein.",
            ),
            q(
                "Why is a frameshift mutation usually severe?",
                (
                    opt(
                        "An indel not a multiple of three scrambles all downstream codons",
                        correct=True,
                    ),
                    opt("It changes only one amino acid"),
                    opt("It has no effect on the protein"),
                    opt("It only affects non-coding DNA"),
                ),
                "Shifting the reading frame alters every codon after the insertion or deletion.",
            ),
            q(
                "Under a constant per-site mutation rate, the probability a site stays unmutated over time follows what?",
                (
                    opt("Exponential decay", correct=True),
                    opt("Linear increase"),
                    opt("A bell curve"),
                    opt("A step function"),
                ),
                "P(no mutation) = e^(-mu t), decaying exponentially with generations.",
            ),
        ),
        "Hardy-Weinberg equilibrium": (
            q(
                "Under Hardy-Weinberg, what is the expected frequency of heterozygotes?",
                (
                    opt("2pq", correct=True),
                    opt("p^2"),
                    opt("q^2"),
                    opt("p + q"),
                ),
                "Genotype frequencies are p^2 (AA), 2pq (Aa), q^2 (aa).",
            ),
            q(
                "Which is NOT an assumption of Hardy-Weinberg equilibrium?",
                (
                    opt("Strong natural selection", correct=True),
                    opt("Random mating"),
                    opt("No migration"),
                    opt("Very large population size"),
                ),
                "HWE assumes no selection, no mutation, no migration, no drift, and random mating.",
            ),
            q(
                "If the affected fraction of a recessive disease is q^2, the carrier frequency for a rare allele is approximately what?",
                (
                    opt("2q, much larger than q^2", correct=True),
                    opt("Equal to q^2"),
                    opt("Smaller than q^2"),
                    opt("Zero"),
                ),
                "Carriers (2pq, about 2q for rare alleles) greatly outnumber affected homozygotes.",
            ),
        ),
        "Forces of evolution: selection, drift and migration": (
            q(
                "Genetic drift has the strongest effect in which populations?",
                (
                    opt("Small populations", correct=True),
                    opt("Infinitely large populations"),
                    opt("Populations with high migration"),
                    opt("Populations under strong selection only"),
                ),
                "Drift scales as 1/(2N), so small N means rapid random change.",
            ),
            q(
                "Heterozygote advantage at the sickle-cell locus is an example of what?",
                (
                    opt("Balancing selection maintaining polymorphism", correct=True),
                    opt("Directional selection fixing one allele"),
                    opt("Pure genetic drift"),
                    opt("A neutral mutation"),
                ),
                "HbA/HbS heterozygotes resist malaria, keeping both alleles in the population.",
            ),
            q(
                "Migration (gene flow) between populations tends to do what?",
                (
                    opt("Homogenize allele frequencies across populations", correct=True),
                    opt("Always increase differences between populations"),
                    opt("Create new alleles"),
                    opt("Eliminate all variation"),
                ),
                "Gene flow mixes alleles, opposing differentiation by drift and local selection.",
            ),
        ),
        "Quantitative genetics and heritability": (
            q(
                "Narrow-sense heritability h^2 is defined as which ratio?",
                (
                    opt(
                        "Additive genetic variance over phenotypic variance (V_A/V_P)", correct=True
                    ),
                    opt("Environmental over phenotypic variance"),
                    opt("Total genetic over additive variance"),
                    opt("Phenotypic over genetic variance"),
                ),
                "h^2 = V_A/V_P captures the heritable variance that responds to selection.",
            ),
            q(
                "The breeder's equation R = h^2 S predicts what?",
                (
                    opt(
                        "The response to selection from heritability and the selection differential",
                        correct=True,
                    ),
                    opt("The mutation rate per generation"),
                    opt("The recombination frequency"),
                    opt("The number of chromosomes"),
                ),
                "Response R equals narrow-sense heritability times the selection differential S.",
            ),
            q(
                "Which statement about heritability is correct?",
                (
                    opt(
                        "It is specific to a population and environment, not a fixed trait property",
                        correct=True,
                    ),
                    opt("It is a universal constant for each trait"),
                    opt("It measures differences between groups"),
                    opt("It equals 1 for all genetic traits"),
                ),
                "Heritability depends on the population and environment and says nothing about group differences.",
            ),
        ),
    },
    final=(
        q(
            "Two genes show a recombination frequency of 0.5. What does this imply?",
            (
                opt("They are unlinked (or very far apart)", correct=True),
                opt("They are tightly linked"),
                opt("One gene caused a mutation in the other"),
                opt("They are the same gene"),
            ),
            "RF of 0.5 is the unlinked maximum, indistinguishable from independent assortment.",
        ),
        q(
            "Which mutation type leaves the encoded protein sequence unchanged?",
            (
                opt("Synonymous (silent) substitution", correct=True),
                opt("Missense substitution"),
                opt("Nonsense substitution"),
                opt("Frameshift insertion"),
            ),
            "Synonymous changes exploit the genetic code's redundancy, keeping the amino acid.",
        ),
        q(
            "At a Hardy-Weinberg locus, allele frequencies are p = 0.7 and q = 0.3. The frequency of aa homozygotes is?",
            (
                opt("0.09", correct=True),
                opt("0.21"),
                opt("0.42"),
                opt("0.30"),
            ),
            "q^2 = 0.3^2 = 0.09.",
        ),
        q(
            "Which evolutionary force introduces entirely new alleles?",
            (
                opt("Mutation", correct=True),
                opt("Genetic drift"),
                opt("Migration"),
                opt("Random mating"),
            ),
            "Mutation is the ultimate source of new genetic variants; the others redistribute existing ones.",
        ),
        q(
            "Phenotypic variance V_P is partitioned (ignoring interaction) into which components?",
            (
                opt("Genetic plus environmental variance", correct=True),
                opt("Only additive variance"),
                opt("Only environmental variance"),
                opt("Mutation rate plus recombination rate"),
            ),
            "V_P = V_G + V_E, with V_G splitting into additive, dominance and epistatic parts.",
        ),
        q(
            "Why do deleterious recessive alleles decline slowly when rare?",
            (
                opt("They are hidden from selection in heterozygous carriers", correct=True),
                opt("Selection cannot act on recessive alleles at all"),
                opt("Mutation constantly recreates them faster than removal"),
                opt("They convert into dominant alleles"),
            ),
            "Rare recessive alleles mostly sit in unaffected heterozygotes, shielding them from selection.",
        ),
    ),
)
