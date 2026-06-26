"""Quiz questions for the Introduction to Bioinformatics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "NGS read mapping and the Burrows-Wheeler transform": (
            q(
                "Why do mappers like BWA and Bowtie2 use the Burrows-Wheeler transform?",
                (
                    opt(
                        "It enables fast substring search in a compact index of a huge reference",
                        correct=True,
                    ),
                    opt("It improves base-calling quality"),
                    opt("It removes PCR duplicates"),
                    opt("It builds phylogenetic trees"),
                ),
                "BWT + FM-index makes search scale with read length, not genome size.",
            ),
            q(
                "Coverage of 30x primarily improves what?",
                (
                    opt(
                        "Sensitivity, leaving a negligible fraction of bases uncovered",
                        correct=True,
                    ),
                    opt("The speed of the BWT"),
                    opt("The reference genome length"),
                    opt("The number of chromosomes"),
                ),
                "Under a Poisson model the uncovered fraction falls as exp(-coverage).",
            ),
            q(
                "How does the fraction of uncovered genome change as mean coverage rises?",
                (
                    opt("It falls exponentially", correct=True),
                    opt("It rises linearly"),
                    opt("It stays constant"),
                    opt("It rises exponentially"),
                ),
                "The Poisson miss probability is exp(-lambda).",
            ),
        ),
        "Variant calling and best practices": (
            q(
                "In the GATK workflow, what does HaplotypeCaller do differently from naive per-base calling?",
                (
                    opt("It locally reassembles reads into candidate haplotypes", correct=True),
                    opt("It ignores read alignments"),
                    opt("It only counts coverage"),
                    opt("It builds a phylogenetic tree"),
                ),
                "Local reassembly improves indel and SNP calls in complex regions.",
            ),
            q(
                "What is the purpose of base quality score recalibration (BQSR)?",
                (
                    opt("Correct systematic errors in per-base quality estimates", correct=True),
                    opt("Remove the reference genome"),
                    opt("Assemble the genome de novo"),
                    opt("Translate DNA to protein"),
                ),
                "BQSR adjusts biased quality scores before calling.",
            ),
            q(
                "A variant QUAL of 30 implies the call-error probability is about what?",
                (
                    opt("0.001 (10^-3)", correct=True),
                    opt("0.3"),
                    opt("0.5"),
                    opt("0.0"),
                ),
                "QUAL is Phred-scaled: P = 10^(-QUAL/10).",
            ),
        ),
        "RNA-seq and differential expression": (
            q(
                "Why do DESeq2 and edgeR use the negative binomial distribution for counts?",
                (
                    opt(
                        "RNA-seq counts are over-dispersed (variance exceeds the mean)",
                        correct=True,
                    ),
                    opt("Counts are always normally distributed"),
                    opt("Counts have no variance"),
                    opt("Counts are continuous percentages"),
                ),
                "The negative binomial models variance = mu + alpha*mu^2.",
            ),
            q(
                "Tools like Salmon and kallisto perform what step quickly?",
                (
                    opt("Transcript quantification via pseudo-alignment", correct=True),
                    opt("Variant calling"),
                    opt("Phylogenetic inference"),
                    opt("Protein folding"),
                ),
                "They assign reads to transcripts without full base-level alignment.",
            ),
            q(
                "Why is multiple-testing correction (e.g. Benjamini-Hochberg) needed in RNA-seq?",
                (
                    opt("Thousands of simultaneous tests inflate false positives", correct=True),
                    opt("Only one gene is ever tested"),
                    opt("It increases the raw p-values"),
                    opt("It assembles the transcriptome"),
                ),
                "FDR control limits false discoveries across many genes.",
            ),
        ),
        "Reproducible pipelines and workflows": (
            q(
                "Workflow managers like Nextflow and Snakemake model a pipeline as what?",
                (
                    opt("A directed acyclic graph of tasks", correct=True),
                    opt("A single monolithic script with no structure"),
                    opt("A phylogenetic tree"),
                    opt("A relational database"),
                ),
                "A task DAG enables parallelism, resume and portability.",
            ),
            q(
                "How do containers (Docker/Singularity) aid reproducibility?",
                (
                    opt("They pin exact tool versions and environments", correct=True),
                    opt("They speed up the BWT"),
                    opt("They call variants"),
                    opt("They generate sequence logos"),
                ),
                "Pinned environments stop results from drifting across machines.",
            ),
            q(
                "What does FAIR stand for in data practice?",
                (
                    opt("Findable, Accessible, Interoperable, Reusable", correct=True),
                    opt("Fast, Accurate, Indexed, Robust"),
                    opt("Filtered, Aligned, Indexed, Recalibrated"),
                    opt("Final, Approved, Independent, Reviewed"),
                ),
                "FAIR principles guide good data stewardship.",
            ),
        ),
        "Multi-omics data integration": (
            q(
                "What is the main challenge in multi-omics integration?",
                (
                    opt(
                        "Heterogeneous scales, noise models and dimensionality across data types",
                        correct=True,
                    ),
                    opt("Having too few data types"),
                    opt("All omics data being identical"),
                    opt("The absence of any computational tools"),
                ),
                "Different omics layers differ in scale, noise and missingness.",
            ),
            q(
                "MOFA integrates omics by doing what?",
                (
                    opt("Learning a shared latent factor space across data types", correct=True),
                    opt("Calling variants from BAM files"),
                    opt("Mapping reads with the BWT"),
                    opt("Building phylogenetic trees"),
                ),
                "Multi-omics factor analysis finds latent factors spanning layers.",
            ),
            q(
                "Why is the curse of dimensionality a core obstacle in multi-omics?",
                (
                    opt(
                        "Features vastly outnumber samples, inflating spurious associations",
                        correct=True,
                    ),
                    opt("There are too many samples"),
                    opt("Data is always low-dimensional"),
                    opt("Models cannot be regularized"),
                ),
                "High feature-to-sample ratios demand regularization and reduction.",
            ),
        ),
        "Deep learning in genomics and structure": (
            q(
                "AlphaFold predicts what from a protein sequence?",
                (
                    opt("Its 3D structure at near-experimental accuracy", correct=True),
                    opt("Its gene expression level"),
                    opt("Its phylogenetic position"),
                    opt("Its E-value"),
                ),
                "AlphaFold predicts 3D structure using MSAs and learned representations.",
            ),
            q(
                "What does AlphaFold's pLDDT score report?",
                (
                    opt("Per-residue confidence in the predicted structure", correct=True),
                    opt("The read coverage"),
                    opt("The substitution matrix used"),
                    opt("The number of training epochs"),
                ),
                "pLDDT flags which regions of the prediction are reliable.",
            ),
            q(
                "As training data grows, deep-learning accuracy typically shows what?",
                (
                    opt("Diminishing returns (saturating gains)", correct=True),
                    opt("Unlimited linear improvement"),
                    opt("A steady decline"),
                    opt("No change at all"),
                ),
                "Gains saturate, so diverse, curated data matters more than raw volume.",
            ),
        ),
    },
    final=(
        q(
            "The Burrows-Wheeler transform lets read mappers search in time that scales with what?",
            (
                opt("Read length, largely independent of genome size", correct=True),
                opt("The square of the genome size"),
                opt("The number of chromosomes"),
                opt("The number of variants called"),
            ),
            "The FM-index gives fast search regardless of reference size.",
        ),
        q(
            "Which step locally reassembles reads to improve variant calls?",
            (
                opt("HaplotypeCaller", correct=True),
                opt("FastQC"),
                opt("Salmon"),
                opt("MultiQC"),
            ),
            "GATK's HaplotypeCaller reassembles candidate haplotypes.",
        ),
        q(
            "The negative binomial model in RNA-seq accounts for what property of counts?",
            (
                opt("Over-dispersion (variance greater than the mean)", correct=True),
                opt("Perfect Poisson behaviour"),
                opt("Continuous Gaussian noise"),
                opt("Zero variance"),
            ),
            "Variance = mu + alpha*mu^2 captures over-dispersion.",
        ),
        q(
            "A key benefit of workflow managers (Nextflow/Snakemake) is what?",
            (
                opt("Resume-on-failure and automatic parallelism over a task DAG", correct=True),
                opt("Higher sequencing quality"),
                opt("Larger reference genomes"),
                opt("Eliminating the need for any tools"),
            ),
            "DAG-based managers parallelise, cache and resume pipelines.",
        ),
        q(
            "Multi-omics integration must contend with which statistical risk?",
            (
                opt("Spurious associations from far more features than samples", correct=True),
                opt("Too few features to model"),
                opt("Identical noise across all layers"),
                opt("No missing data ever"),
            ),
            "High dimensionality relative to sample size inflates false discoveries.",
        ),
        q(
            "Why must deep-learning genomics models be evaluated and interpreted carefully?",
            (
                opt("They can learn dataset biases and need calibrated confidence", correct=True),
                opt("They are always perfectly accurate"),
                opt("They never overfit"),
                opt("They require no held-out data"),
            ),
            "Bias, calibration and rigorous held-out testing are essential.",
        ),
    ),
)
