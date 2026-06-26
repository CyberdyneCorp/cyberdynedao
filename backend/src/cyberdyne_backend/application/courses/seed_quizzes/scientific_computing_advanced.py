"""Quiz questions for the Scientific Computing & Linux - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Reproducible pipelines: Snakemake and Nextflow": (
            q(
                "How does a workflow manager model an analysis?",
                (
                    opt(
                        "As a directed acyclic graph (DAG) of rules with inputs and outputs",
                        correct=True,
                    ),
                    opt("As a single linear shell script"),
                    opt("As a spreadsheet"),
                    opt("As a database table"),
                ),
                "Rules form a DAG so the engine orders, parallelises and resumes.",
            ),
            q(
                "What does a Snakemake wildcard like {sample} provide?",
                (
                    opt("One rule that fans out over many samples", correct=True),
                    opt("A random number"),
                    opt("A comment"),
                    opt("A fixed filename"),
                ),
                "Wildcards generalise a rule across inputs.",
            ),
            q(
                "Why re-run only out-of-date steps?",
                (
                    opt("It saves time and the DAG tracks what changed", correct=True),
                    opt("It corrupts outputs"),
                    opt("It is required by Slurm"),
                    opt("It disables parallelism"),
                ),
                "Incremental execution recomputes only stale outputs.",
            ),
        ),
        "HPC clusters and the Slurm scheduler": (
            q(
                "Why should you not run heavy jobs on the login node?",
                (
                    opt("It is shared; heavy work belongs in scheduled batch jobs", correct=True),
                    opt("The login node has no CPU"),
                    opt("It is illegal"),
                    opt("It deletes your files"),
                ),
                "Submit to the scheduler; the login node is for light tasks.",
            ),
            q(
                "Which directive requests memory in a Slurm script?",
                (
                    opt("#SBATCH --mem=32G", correct=True),
                    opt("#SBATCH --job-name"),
                    opt("module load"),
                    opt("squeue"),
                ),
                "--mem sets the memory request.",
            ),
            q(
                "What is the benefit of a Slurm job array?",
                (
                    opt(
                        "One submission spawns many parallel tasks, e.g. one per sample",
                        correct=True,
                    ),
                    opt("It compresses files"),
                    opt("It encrypts the job"),
                    opt("It runs only on the login node"),
                ),
                "Arrays are ideal for embarrassingly parallel per-sample work.",
            ),
        ),
        "Parallel and distributed computing": (
            q(
                "What does Amdahl's law describe?",
                (
                    opt(
                        "The maximum speedup bounded by the serial fraction of the work",
                        correct=True,
                    ),
                    opt("The cost of storage"),
                    opt("Network latency"),
                    opt("GPU memory size"),
                ),
                "Speedup is capped at 1/(1-p) as processors grow.",
            ),
            q(
                "With 90% parallel work, the speedup ceiling is about:",
                (
                    opt("10x", correct=True),
                    opt("90x"),
                    opt("unlimited"),
                    opt("2x"),
                ),
                "1/(1-0.9) = 10.",
            ),
            q(
                "Which problems scale closest to linearly?",
                (
                    opt("Embarrassingly parallel, independent per-sample tasks", correct=True),
                    opt("Tightly coupled tasks with heavy communication"),
                    opt("Purely serial tasks"),
                    opt("I/O-bound tasks on one disk"),
                ),
                "Independent tasks avoid communication overhead.",
            ),
        ),
        "Containers for bioinformatics": (
            q(
                "How does a container differ from a virtual machine?",
                (
                    opt(
                        "It shares the host kernel, so it is lightweight and fast to start",
                        correct=True,
                    ),
                    opt("It boots a full separate operating system"),
                    opt("It cannot run scientific tools"),
                    opt("It requires its own physical hardware"),
                ),
                "Containers share the kernel; VMs virtualise hardware.",
            ),
            q(
                "Why do HPC clusters use Singularity/Apptainer instead of plain Docker?",
                (
                    opt("It runs as an unprivileged user (no root needed)", correct=True),
                    opt("It is faster than the CPU"),
                    opt("It cannot read Docker images"),
                    opt("It requires a GPU"),
                ),
                "Apptainer avoids the root daemon that clusters forbid.",
            ),
            q(
                "What does combining containers with a workflow manager give?",
                (
                    opt(
                        "Byte-for-byte reproducible pipelines, each rule in a pinned image",
                        correct=True,
                    ),
                    opt("Faster internet"),
                    opt("Automatic publication"),
                    opt("Unlimited memory"),
                ),
                "Pinned containers per rule make pipelines reproducible long-term.",
            ),
        ),
        "GPU and AI-accelerated computing": (
            q(
                "Why are GPUs suited to deep learning and simulation?",
                (
                    opt("Thousands of cores run dense linear algebra in parallel", correct=True),
                    opt("They have one very fast core"),
                    opt("They store more data than disks"),
                    opt("They replace the operating system"),
                ),
                "GPUs excel at massively parallel matrix math.",
            ),
            q(
                "What problem did AlphaFold2 famously address?",
                (
                    opt("Predicting a protein's 3D structure from its sequence", correct=True),
                    opt("Sorting FASTQ files"),
                    opt("Compressing BAM files"),
                    opt("Scheduling Slurm jobs"),
                ),
                "AlphaFold2 solved protein structure prediction with deep learning.",
            ),
            q(
                "How does Google's DeepVariant reframe variant calling?",
                (
                    opt("As an image-classification problem for a neural network", correct=True),
                    opt("As a spreadsheet sort"),
                    opt("As a cron schedule"),
                    opt("As a permissions check"),
                ),
                "DeepVariant turns pileups into images classified by a CNN.",
            ),
        ),
        "Reproducibility and FAIR data": (
            q(
                "Reproducibility requires capturing which combination?",
                (
                    opt("Code + environment + data + provenance together", correct=True),
                    opt("Only the final figures"),
                    opt("Only the source code"),
                    opt("Only a screenshot of results"),
                ),
                "All four together let results be regenerated exactly.",
            ),
            q(
                "What do the letters FAIR stand for?",
                (
                    opt("Findable, Accessible, Interoperable, Reusable", correct=True),
                    opt("Fast, Automated, Indexed, Remote"),
                    opt("Formatted, Archived, Internal, Restricted"),
                    opt("Free, Anonymous, Iterative, Rapid"),
                ),
                "FAIR = Findable, Accessible, Interoperable, Reusable.",
            ),
            q(
                "What does workflow provenance record?",
                (
                    opt(
                        "Which inputs, parameters and software versions produced each output",
                        correct=True,
                    ),
                    opt("Only the wall-clock time"),
                    opt("The user's password"),
                    opt("The colour of plots"),
                ),
                "Provenance makes every output traceable.",
            ),
        ),
    },
    final=(
        q(
            "What is the central advantage of a workflow DAG over a Bash script?",
            (
                opt(
                    "It orders steps, parallelises them, resumes after failure and re-runs only stale work",
                    correct=True,
                ),
                opt("It uses fewer files"),
                opt("It needs no environment"),
                opt("It runs without any inputs"),
            ),
            "The DAG engine manages ordering, parallelism and incremental execution.",
        ),
        q(
            "How do you run work on an HPC cluster correctly?",
            (
                opt("Submit batch jobs to the scheduler (e.g. sbatch)", correct=True),
                opt("Run everything on the login node"),
                opt("Use a desktop GUI"),
                opt("Email the admin each command"),
            ),
            "Heavy work is submitted to Slurm, not run on the login node.",
        ),
        q(
            "As processors increase, Amdahl's speedup approaches:",
            (
                opt("1/(1-p), set by the serial fraction", correct=True),
                opt("infinity"),
                opt("the number of processors exactly"),
                opt("zero"),
            ),
            "The serial part caps the achievable speedup.",
        ),
        q(
            "Why use Apptainer/Singularity on a shared cluster?",
            (
                opt("It runs containers without root privileges", correct=True),
                opt("It is the only way to use Python"),
                opt("It replaces Slurm"),
                opt("It requires a GPU"),
            ),
            "Apptainer runs unprivileged, unlike the Docker daemon.",
        ),
        q(
            "Which is a real AI-driven genomics tool?",
            (
                opt("DeepVariant for variant calling", correct=True),
                opt("grep for structure prediction"),
                opt("cron for basecalling"),
                opt("scp for alignment"),
            ),
            "DeepVariant uses deep learning for variant calling.",
        ),
        q(
            "Why is reproducibility essential to computational science?",
            (
                opt(
                    "It lets others regenerate results, making them science rather than anecdote",
                    correct=True,
                ),
                opt("It is only a legal formality"),
                opt("It speeds up the GPU"),
                opt("It reduces disk usage"),
            ),
            "Reproducible results let the field build cumulatively.",
        ),
    ),
)
