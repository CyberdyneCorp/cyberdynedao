"""Quiz questions for the Genetics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Genes, alleles and the language of heredity": (
            q(
                "What is an allele?",
                (
                    opt("An alternative version of a gene at a given locus", correct=True),
                    opt("A type of chromosome"),
                    opt("The observable trait of an organism"),
                    opt("A ribosome bound to mRNA"),
                ),
                "Alleles are sequence variants of the same gene occupying the same locus.",
            ),
            q(
                "An individual with two different alleles at a locus is called what?",
                (
                    opt("Heterozygous", correct=True),
                    opt("Homozygous"),
                    opt("Hemizygous"),
                    opt("Haploid"),
                ),
                "Two different alleles means heterozygous; two identical alleles means homozygous.",
            ),
            q(
                "What does penetrance measure?",
                (
                    opt(
                        "The fraction of individuals with a genotype who show the expected phenotype",
                        correct=True,
                    ),
                    opt("How many genes an organism has"),
                    opt("The speed of DNA replication"),
                    opt("The number of chromosomes in a gamete"),
                ),
                "Penetrance is the proportion showing the phenotype; expressivity is how strongly it shows.",
            ),
        ),
        "Mendel's laws: segregation and independent assortment": (
            q(
                "The law of segregation states that during gamete formation, the two alleles of a gene do what?",
                (
                    opt("Separate so each gamete carries exactly one", correct=True),
                    opt("Both go into every gamete"),
                    opt("Are destroyed and remade"),
                    opt("Always stay together"),
                ),
                "Each gamete receives one of the two alleles, in equal proportion for a heterozygote.",
            ),
            q(
                "Independent assortment applies most cleanly to genes located where?",
                (
                    opt("On different chromosomes", correct=True),
                    opt("Right next to each other on one chromosome"),
                    opt("Only on the Y chromosome"),
                    opt("Inside mitochondria"),
                ),
                "Genes on different chromosomes assort independently; linked genes do not.",
            ),
            q(
                "How many distinct gamete genotypes can n independently assorting heterozygous loci produce?",
                (
                    opt("2^n", correct=True),
                    opt("2n"),
                    opt("n^2"),
                    opt("n/2"),
                ),
                "Each locus contributes two choices, giving 2^n combinations.",
            ),
        ),
        "The monohybrid and dihybrid cross": (
            q(
                "Crossing two heterozygotes Aa x Aa gives what phenotypic ratio when A is dominant?",
                (
                    opt("3:1", correct=True),
                    opt("1:1"),
                    opt("9:3:3:1"),
                    opt("1:2:1"),
                ),
                "The 3 dominant : 1 recessive ratio comes from 1 AA : 2 Aa : 1 aa.",
            ),
            q(
                "A dihybrid cross AaBb x AaBb (independent assortment) gives which phenotypic ratio?",
                (
                    opt("9:3:3:1", correct=True),
                    opt("3:1"),
                    opt("1:1:1:1"),
                    opt("2:1"),
                ),
                "Multiplying two 3:1 ratios yields 9:3:3:1 over 16 combinations.",
            ),
            q(
                "A test cross is performed against which genotype?",
                (
                    opt("Homozygous recessive (aa)", correct=True),
                    opt("Homozygous dominant (AA)"),
                    opt("A heterozygote (Aa)"),
                    opt("A different species"),
                ),
                "Crossing to aa exposes the unknown's alleles directly in the offspring ratio.",
            ),
        ),
        "Beyond simple dominance: codominance and multiple alleles": (
            q(
                "In incomplete dominance, the heterozygote phenotype is what?",
                (
                    opt("Intermediate between the two homozygotes", correct=True),
                    opt("Identical to the dominant homozygote"),
                    opt("Identical to the recessive homozygote"),
                    opt("Absent entirely"),
                ),
                "Incomplete dominance blends the two, e.g. red x white snapdragons giving pink.",
            ),
            q(
                "AB blood type is an example of what inheritance pattern?",
                (
                    opt("Codominance (both alleles fully expressed)", correct=True),
                    opt("Complete dominance"),
                    opt("X-linked recessive"),
                    opt("Incomplete dominance"),
                ),
                "Both A and B antigens appear, so the alleles are codominant.",
            ),
            q(
                "When one gene affects many different traits, the phenomenon is called what?",
                (
                    opt("Pleiotropy", correct=True),
                    opt("Epistasis"),
                    opt("Codominance"),
                    opt("Penetrance"),
                ),
                "Pleiotropy is one gene influencing multiple traits; epistasis is one gene masking another.",
            ),
        ),
        "Meiosis: the cellular basis of inheritance": (
            q(
                "What is the overall result of meiosis?",
                (
                    opt("Four haploid gametes from one diploid cell", correct=True),
                    opt("Two identical diploid cells"),
                    opt("One haploid cell"),
                    opt("Four diploid cells"),
                ),
                "Meiosis halves the chromosome number across two divisions, yielding four haploid gametes.",
            ),
            q(
                "Crossing over occurs during which stage?",
                (
                    opt("Prophase I", correct=True),
                    opt("Anaphase II"),
                    opt("Telophase II"),
                    opt("Interphase"),
                ),
                "Homologs pair and exchange segments in prophase I.",
            ),
            q(
                "Errors in chromosome separation during meiosis are called what?",
                (
                    opt("Nondisjunction", correct=True),
                    opt("Recombination"),
                    opt("Synapsis"),
                    opt("Transcription"),
                ),
                "Nondisjunction produces aneuploid gametes, such as those causing trisomy 21.",
            ),
        ),
        "The chromosome theory and sex linkage": (
            q(
                "The chromosome theory of inheritance states that genes are located where?",
                (
                    opt("On chromosomes", correct=True),
                    opt("In the cytoplasm only"),
                    opt("Inside ribosomes"),
                    opt("In the cell membrane"),
                ),
                "Sutton, Boveri and Morgan established that genes reside on chromosomes.",
            ),
            q(
                "Why are X-linked recessive conditions more common in males?",
                (
                    opt(
                        "Males are hemizygous, so one recessive X allele is expressed", correct=True
                    ),
                    opt("Males have two X chromosomes"),
                    opt("Males never inherit the X chromosome"),
                    opt("The Y chromosome carries the recessive allele"),
                ),
                "With only one X, a male needs just one copy to show the trait.",
            ),
            q(
                "A carrier mother (X^H X^h) and unaffected father (X^H Y) have sons. What fraction of sons is expected to be affected?",
                (
                    opt("About one half", correct=True),
                    opt("None"),
                    opt("All"),
                    opt("One quarter"),
                ),
                "Each son gets either the X^H or X^h from the mother with equal probability.",
            ),
        ),
    },
    final=(
        q(
            "What is the difference between genotype and phenotype?",
            (
                opt(
                    "Genotype is the allele makeup; phenotype is the observable trait", correct=True
                ),
                opt("They are the same thing"),
                opt("Genotype is the visible trait; phenotype is the DNA"),
                opt("Phenotype refers only to gametes"),
            ),
            "Genotype is what alleles you carry; phenotype is what those alleles produce.",
        ),
        q(
            "Mendel's law of segregation is physically explained by which event in meiosis?",
            (
                opt("Separation of homologous chromosomes", correct=True),
                opt("DNA replication in S phase"),
                opt("Ribosome assembly"),
                opt("Fusion of two gametes"),
            ),
            "Homologs carrying the two alleles separate, sending one allele to each gamete.",
        ),
        q(
            "A cross of two heterozygotes for two independent genes gives offspring in what phenotypic ratio?",
            (
                opt("9:3:3:1", correct=True),
                opt("3:1"),
                opt("1:1"),
                opt("1:2:1"),
            ),
            "The dihybrid 9:3:3:1 ratio results from independent assortment of two genes.",
        ),
        q(
            "Which inheritance pattern describes both alleles being fully and separately expressed?",
            (
                opt("Codominance", correct=True),
                opt("Incomplete dominance"),
                opt("Complete dominance"),
                opt("Epistasis"),
            ),
            "In codominance, such as AB blood type, both products appear together.",
        ),
        q(
            "What two meiotic mechanisms generate genetic variation in gametes?",
            (
                opt("Independent assortment and crossing over", correct=True),
                opt("Transcription and translation"),
                opt("Replication and repair"),
                opt("Capping and splicing"),
            ),
            "Independent assortment shuffles chromosomes; crossing over recombines alleles along them.",
        ),
        q(
            "A man cannot pass an X-linked allele to which offspring?",
            (
                opt("His sons", correct=True),
                opt("His daughters"),
                opt("Any of his children"),
                opt("Only his first child"),
            ),
            "A father gives his Y to sons and his single X to daughters, so X-linked alleles go to daughters.",
        ),
    ),
)
