"""Quiz questions for the Python Programming for Biologists - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Biopython for sequences": (
            q(
                "Which Biopython method returns the antisense strand of a Seq?",
                (
                    opt("reverse_complement()", correct=True),
                    opt("translate()"),
                    opt("transcribe()"),
                    opt("upper()"),
                ),
                "reverse_complement gives the complementary strand read 5'->3'.",
            ),
            q(
                "What does SeqIO.parse give you?",
                (
                    opt("An iterator of SeqRecord objects from a sequence file", correct=True),
                    opt("A single string of the whole file"),
                    opt("A pandas DataFrame"),
                    opt("A Matplotlib figure"),
                ),
                "SeqIO.parse lazily yields one SeqRecord per record.",
            ),
            q(
                "As evolutionary distance increases, alignment percent identity typically:",
                (
                    opt("Decreases", correct=True),
                    opt("Increases"),
                    opt("Stays at 100%"),
                    opt("Becomes undefined"),
                ),
                "More divergence means fewer conserved residues, so identity falls.",
            ),
        ),
        "Publication-quality plotting": (
            q(
                "A volcano plot displays:",
                (
                    opt(
                        "Effect size (log2 fold change) versus significance (-log10 p)",
                        correct=True,
                    ),
                    opt("Time versus temperature"),
                    opt("A sequence alignment"),
                    opt("A phylogenetic tree"),
                ),
                "Volcano plots summarise differential expression: magnitude vs significance.",
            ),
            q(
                "Which output format is preferred for journal figures?",
                (
                    opt("Vector formats like PDF or SVG", correct=True),
                    opt("Low-resolution JPEG"),
                    opt("Animated GIF"),
                    opt("BMP"),
                ),
                "Vector formats scale without pixelation and are accepted by journals.",
            ),
            q(
                "From a dose-response sigmoid you can read off the:",
                (
                    opt("EC50", correct=True),
                    opt("GC content"),
                    opt("Read length"),
                    opt("Phred score"),
                ),
                "The EC50 is the dose giving half-maximal response, the sigmoid's midpoint.",
            ),
        ),
        "Reproducible notebooks & environments": (
            q(
                "The main reproducibility trap of Jupyter notebooks is:",
                (
                    opt("Out-of-order cell execution", correct=True),
                    opt("They cannot run Python"),
                    opt("They delete data automatically"),
                    opt("They cannot show plots"),
                ),
                "Cells run in any order; restart-and-run-all restores a clean linear state.",
            ),
            q(
                "Which command captures exact package versions for reproducibility?",
                (
                    opt("pip freeze > requirements.txt", correct=True),
                    opt("pip list --short"),
                    opt("python --version"),
                    opt("ls -l"),
                ),
                "pip freeze (or conda env export) pins exact versions.",
            ),
            q(
                "Setting np.random.seed(0) ensures that:",
                (
                    opt("Stochastic steps reproduce the same results", correct=True),
                    opt("The code runs faster"),
                    opt("Files are compressed"),
                    opt("Plots use more colours"),
                ),
                "A fixed seed makes random number generation deterministic across runs.",
            ),
        ),
        "Scaling pipelines & performance": (
            q(
                "Before optimising performance you should first:",
                (
                    opt("Profile to find the real bottleneck", correct=True),
                    opt("Rewrite everything in C"),
                    opt("Buy a bigger laptop"),
                    opt("Delete the slow data"),
                ),
                "Profiling (cProfile, %timeit) reveals where time is actually spent.",
            ),
            q(
                "What do workflow managers like Snakemake or Nextflow provide?",
                (
                    opt("Declared step inputs/outputs so only stale steps rerun", correct=True),
                    opt("Automatic statistical significance"),
                    opt("Free cloud storage"),
                    opt("Sequence translation"),
                ),
                "They build a dependency DAG, caching results and parallelising independent steps.",
            ),
            q(
                "Amdahl's law says parallel speed-up is ultimately limited by:",
                (
                    opt("The serial (non-parallel) fraction of the work", correct=True),
                    opt("The number of genes"),
                    opt("The file format"),
                    opt("The plotting library"),
                ),
                "Even infinite workers cannot speed up the serial portion.",
            ),
        ),
        "Machine learning for biology": (
            q(
                "In biology, p >> n (many features, few samples) primarily risks:",
                (
                    opt("Overfitting", correct=True),
                    opt("Underflow errors"),
                    opt("Slow file reading"),
                    opt("Loss of colour in plots"),
                ),
                "With more features than samples, models can memorise noise; use CV and regularisation.",
            ),
            q(
                "The area under the ROC curve (AUC) measures:",
                (
                    opt(
                        "Classifier ranking performance; 0.5 is random, 1.0 is perfect",
                        correct=True,
                    ),
                    opt("The number of features"),
                    opt("The training time"),
                    opt("The GC content"),
                ),
                "AUC summarises the trade-off between true and false positive rates.",
            ),
            q(
                "Which is a state-of-the-art deep-learning tool reachable from Python for structure prediction?",
                (
                    opt("AlphaFold", correct=True),
                    opt("FASTA"),
                    opt("CSV"),
                    opt("grep"),
                ),
                "AlphaFold predicts protein 3-D structure and is used via Python tooling.",
            ),
        ),
    },
    final=(
        q(
            "Which Biopython call converts DNA to mRNA?",
            (
                opt("transcribe()", correct=True),
                opt("translate()"),
                opt("complement()"),
                opt("count()"),
            ),
            "transcribe replaces T with U to give the mRNA sequence.",
        ),
        q(
            "Saving the code that makes a figure (not just the image) ensures:",
            (
                opt("The figure can be regenerated when data updates", correct=True),
                opt("Smaller image files only"),
                opt("Faster internet"),
                opt("The figure is encrypted"),
            ),
            "Reproducible figures come from rerunnable code, not static images.",
        ),
        q(
            "Which practice does NOT improve reproducibility?",
            (
                opt("Running cells in a random order and sharing the result", correct=True),
                opt("Pinning package versions"),
                opt("Setting random seeds"),
                opt("Using version control"),
            ),
            "Out-of-order execution undermines reproducibility; the others support it.",
        ),
        q(
            "To analyse a file larger than RAM you can:",
            (
                opt("Stream it in chunks or use Dask/Polars", correct=True),
                opt("Always load it fully into a list"),
                opt("Convert it to an image first"),
                opt("Delete half the rows at random"),
            ),
            "Chunked reading or out-of-core dataframes handle data bigger than memory.",
        ),
        q(
            "Cross-validation in scikit-learn is used to:",
            (
                opt("Estimate how well a model generalises to unseen data", correct=True),
                opt("Increase the number of features"),
                opt("Plot a volcano figure"),
                opt("Transcribe DNA"),
            ),
            "CV repeatedly trains/tests on splits to give an honest performance estimate.",
        ),
        q(
            "Before claiming a biological discovery from an ML model you should:",
            (
                opt("Validate on an independent test cohort", correct=True),
                opt("Report only the training accuracy"),
                opt("Maximise the number of parameters"),
                opt("Skip cross-validation"),
            ),
            "Independent validation guards against overfitting and inflated performance.",
        ),
    ),
)
