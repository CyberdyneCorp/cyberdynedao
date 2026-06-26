"""Quiz questions for the Evolution & Ecology - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Molecular evolution and detecting selection": (
            q(
                "Under the neutral theory, most fixed substitutions are:",
                (
                    opt("Selectively neutral, fixed by drift", correct=True),
                    opt("Strongly advantageous"),
                    opt("Strongly deleterious"),
                    opt("Caused by gene flow"),
                ),
                "Kimura's neutral theory attributes most molecular evolution to drift of neutral variants.",
            ),
            q(
                "A dN/dS ratio (omega) greater than 1 indicates:",
                (
                    opt("Positive (diversifying) selection", correct=True),
                    opt("Purifying selection"),
                    opt("Strict neutrality"),
                    opt("No substitutions occurred"),
                ),
                "omega > 1 means amino-acid changes are favoured over silent changes.",
            ),
            q(
                "The molecular clock predicts that substitutions accumulate:",
                (
                    opt("Approximately linearly with time", correct=True),
                    opt("Exponentially with time"),
                    opt("Only during speciation events"),
                    opt("Never in conserved genes"),
                ),
                "Under a clock, neutral substitutions accrue at a roughly constant rate over time.",
            ),
        ),
        "Coalescent theory and demographic inference": (
            q(
                "The coalescent models evolution by:",
                (
                    opt("Tracing sampled lineages backward until they merge", correct=True),
                    opt("Simulating every individual forward in time"),
                    opt("Ignoring genealogy entirely"),
                    opt("Assuming infinite recombination"),
                ),
                "The coalescent runs backward, merging lineages into common ancestors.",
            ),
            q(
                "Expected pairwise coalescence time scales with:",
                (
                    opt("Effective population size Ne", correct=True),
                    opt("The mutation rate only"),
                    opt("The number of chromosomes"),
                    opt("The recombination rate only"),
                ),
                "E[T2] = 2 Ne, so larger Ne means deeper genealogies and more diversity.",
            ),
            q(
                "Methods like PSMC/MSMC and dadi are used to infer:",
                (
                    opt("Ancestral population size history (demography)", correct=True),
                    opt("Protein 3D structure"),
                    opt("The genetic code"),
                    opt("Carrying capacity in ecosystems"),
                ),
                "These read genomic patterns to reconstruct demographic history.",
            ),
        ),
        "Coevolution and the Red Queen": (
            q(
                "Coevolution is best described as:",
                (
                    opt("Reciprocal evolutionary change between interacting species", correct=True),
                    opt("Evolution of one species in isolation"),
                    opt("Random drift in a single population"),
                    opt("Convergence of unrelated traits"),
                ),
                "Each species acts as a selective pressure on the other.",
            ),
            q(
                "The Red Queen hypothesis is a leading explanation for:",
                (
                    opt("The maintenance of sexual reproduction", correct=True),
                    opt("The origin of the genetic code"),
                    opt("Carrying capacity in ecosystems"),
                    opt("The molecular clock"),
                ),
                "Sex generates novelty needed to keep pace with coevolving parasites.",
            ),
            q(
                "Under negative frequency-dependent selection, a host genotype is favoured when it is:",
                (
                    opt("Rare", correct=True),
                    opt("Common"),
                    opt("Fixed"),
                    opt("Extinct"),
                ),
                "Common genotypes are tracked by parasites, so rare ones have higher fitness.",
            ),
        ),
        "Evolutionary medicine and antibiotic resistance": (
            q(
                "Antibiotic resistance spreads rapidly between bacteria mainly through:",
                (
                    opt("Horizontal gene transfer (e.g. plasmids)", correct=True),
                    opt("Vertical inheritance only"),
                    opt("Sexual reproduction"),
                    opt("Random genetic drift only"),
                ),
                "Plasmid-borne resistance genes transfer horizontally across bacteria.",
            ),
            q(
                "Why is combination therapy often used against resistance?",
                (
                    opt("Simultaneous resistance to multiple drugs is improbable", correct=True),
                    opt("It is always cheaper"),
                    opt("It eliminates the need for dosing"),
                    opt("It prevents any mutation from occurring"),
                ),
                "Requiring multiple independent mutations at once makes resistance far less likely.",
            ),
            q(
                "Antibiotic resistance is a clear example of:",
                (
                    opt("Natural selection acting in real time", correct=True),
                    opt("Lamarckian inheritance of acquired traits"),
                    opt("Random drift with no selection"),
                    opt("Gene flow between species only"),
                ),
                "The drug imposes strong selection favouring pre-existing resistant variants.",
            ),
        ),
        "Machine learning in evolution and ecology": (
            q(
                "Simulation-based inference is valuable when:",
                (
                    opt(
                        "The likelihood is intractable but the model can be simulated", correct=True
                    ),
                    opt("There is no model at all"),
                    opt("Data are unavailable"),
                    opt("Only linear regression is needed"),
                ),
                "SBI/ABC train on simulations to bypass intractable likelihoods.",
            ),
            q(
                "Convolutional neural networks are applied in population genomics to:",
                (
                    opt("Detect selective sweeps and recombination from alignments", correct=True),
                    opt("Replace DNA sequencing"),
                    opt("Eliminate the need for any data"),
                    opt("Compute carrying capacity"),
                ),
                "CNNs read genotype matrices directly to localize sweeps and hotspots.",
            ),
            q(
                "Why must ML inference methods be validated on held-out simulations?",
                (
                    opt(
                        "To check accuracy and avoid overfitting to the training set", correct=True
                    ),
                    opt("Because training data are always perfect"),
                    opt("To increase the mutation rate"),
                    opt("Validation is unnecessary for ML"),
                ),
                "Held-out simulations give an honest estimate of generalization performance.",
            ),
        ),
    },
    final=(
        q(
            "Tools such as PAML and HyPhy are primarily used to:",
            (
                opt("Estimate dN/dS and detect selection on sequences", correct=True),
                opt("Assemble genomes from reads"),
                opt("Predict protein structure"),
                opt("Measure carrying capacity"),
            ),
            "These codon-model packages estimate omega per site or branch.",
        ),
        q(
            "In the coalescent, the rate of coalescence increases when:",
            (
                opt("Many lineages remain in the sample", correct=True),
                opt("Only two lineages remain"),
                opt("Effective population size is very large"),
                opt("Mutation rate is zero"),
            ),
            "Coalescence rate scales with the number of pairs, ~ k choose 2.",
        ),
        q(
            "A bottleneck in a population's history leaves what signature in genealogies?",
            (
                opt("Compressed coalescence times during the bottleneck", correct=True),
                opt("Stretched coalescence times"),
                opt("No effect on genealogies"),
                opt("Increased heterozygosity"),
            ),
            "Small size during a bottleneck accelerates coalescence and reduces diversity.",
        ),
        q(
            "The Red Queen dynamic between hosts and parasites typically maintains diversity through:",
            (
                opt("Negative frequency-dependent selection", correct=True),
                opt("Positive frequency-dependent selection"),
                opt("Directional selection to fixation"),
                opt("Complete absence of selection"),
            ),
            "Rare-advantage selection cycles genotype frequencies and preserves variation.",
        ),
        q(
            "A clinical strategy that exploits the fitness cost of resistance is:",
            (
                opt("Cycling or withdrawing the antibiotic", correct=True),
                opt("Permanent low-dose exposure"),
                opt("Using a single drug forever"),
                opt("Stopping treatment as soon as symptoms ease"),
            ),
            "When the drug is removed, costly resistant strains can lose ground to susceptible ones.",
        ),
        q(
            "Protein language models like ESM and structure predictors like AlphaFold contribute to molecular evolution by:",
            (
                opt("Informing predictions of fitness effects of mutations", correct=True),
                opt("Replacing phylogenetic trees entirely"),
                opt("Measuring population density"),
                opt("Setting carrying capacity"),
            ),
            "Learned representations of sequence and structure help predict mutational consequences.",
        ),
    ),
)
