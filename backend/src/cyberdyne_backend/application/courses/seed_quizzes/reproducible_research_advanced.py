"""Quiz questions for the Reproducible Research & Scientific Software - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Containers for reproducibility": (
            q(
                "What does a container package beyond your application code?",
                (
                    opt("Only the source files"),
                    opt("The entire user-space environment (OS libs, runtime, deps)", correct=True),
                    opt("The host operating system kernel"),
                    opt("Just the Python interpreter"),
                ),
                "A container bundles the app with its full user-space environment for portability.",
            ),
            q(
                "Why use Apptainer/Singularity on a shared HPC cluster?",
                (
                    opt("It requires root access to run"),
                    opt("It runs the same image without a privileged daemon", correct=True),
                    opt("It only works on Windows"),
                    opt("It deletes the image after each run"),
                ),
                "Apptainer/Singularity runs containers without root, suiting multi-user HPC.",
            ),
            q(
                "How should a base image be pinned for reproducibility?",
                (
                    opt("By a moving tag like 'latest'"),
                    opt("By its content digest (sha256), not a moving tag", correct=True),
                    opt("By the date it was downloaded"),
                    opt("By the number of layers it has"),
                ),
                "Pinning by digest fixes the exact image; moving tags can change underneath you.",
            ),
        ),
        "Reproducible environments with Nix": (
            q(
                "What makes Nix builds more reproducible than apt-get in a Dockerfile?",
                (
                    opt("Nix uses the newest packages available each day"),
                    opt("Nix builds from a pinned, content-hashed set of sources", correct=True),
                    opt("Nix skips dependencies entirely"),
                    opt("Nix only runs on a single machine"),
                ),
                "Nix pins all sources by content hash, yielding bit-for-bit identical environments.",
            ),
            q(
                "What does a committed flake.lock pin?",
                (
                    opt("Only the top-level packages requested"),
                    opt("The exact revision of all input sources", correct=True),
                    opt("The output figures of the analysis"),
                    opt("The CI server configuration"),
                ),
                "flake.lock records the exact revision of every input, the key to reproducibility.",
            ),
            q(
                "What is the broader principle illustrated by uv.lock, renv.lock and conda-lock?",
                (
                    opt(
                        "Record a fully resolved dependency graph, not just top-level requests",
                        correct=True,
                    ),
                    opt("Avoid recording any versions"),
                    opt("Always install the newest packages"),
                    opt("Delete dependencies after install"),
                ),
                "Lock files everywhere capture the complete resolved graph for reproducibility.",
            ),
        ),
        "FAIR principles & open science": (
            q(
                "What does the 'F' in FAIR stand for?",
                (
                    opt("Fast"),
                    opt("Findable", correct=True),
                    opt("Free"),
                    opt("Formatted"),
                ),
                "FAIR = Findable, Accessible, Interoperable, Reusable.",
            ),
            q(
                "Is FAIR the same as 'open'?",
                (
                    opt("Yes, FAIR data must always be fully open"),
                    opt("No, sensitive data can be FAIR while access is controlled", correct=True),
                    opt("Yes, the terms are interchangeable"),
                    opt("No, FAIR applies only to software"),
                ),
                "FAIR is not the same as open: access can be controlled while still being FAIR.",
            ),
            q(
                "How can software be made citable under FAIR4RS?",
                (
                    opt("By deleting its version history"),
                    opt("By minting a DOI (e.g. Zenodo) and adding a CITATION.cff", correct=True),
                    opt("By keeping it private"),
                    opt("By removing its licence"),
                ),
                "A Zenodo DOI per release plus CITATION.cff makes code findable and citable.",
            ),
        ),
        "Computational provenance": (
            q(
                "What does computational provenance record?",
                (
                    opt("Only the final figure"),
                    opt(
                        "The lineage: inputs, code version, parameters and environment",
                        correct=True,
                    ),
                    opt("Just the file size of outputs"),
                    opt("The reviewer's comments"),
                ),
                "Provenance is the recorded lineage of how a result was produced.",
            ),
            q(
                "Which tool automatically logs an ML run's parameters, metrics and artifacts?",
                (
                    opt("MLflow", correct=True),
                    opt("grep"),
                    opt("tar"),
                    opt("ssh"),
                ),
                "MLflow (and W&B) log params, metrics and artifacts per run for provenance.",
            ),
            q(
                "What does the W3C PROV model provide?",
                (
                    opt("A compression algorithm"),
                    opt(
                        "A standard vocabulary (Entity, Activity, Agent) for lineage", correct=True
                    ),
                    opt("A container runtime"),
                    opt("A random number generator"),
                ),
                "PROV gives a standard, machine-readable vocabulary for expressing provenance.",
            ),
        ),
        "Reproducible machine learning": (
            q(
                "Which four things must a reproducible ML project version?",
                (
                    opt("Only the code"),
                    opt("Code, data, environment, and the trained model", correct=True),
                    opt("Only the data and the paper"),
                    opt("Only the hyperparameters"),
                ),
                "Reproducible ML versions all of code, data, environment and model.",
            ),
            q(
                "What does DVC (Data Version Control) do?",
                (
                    opt("Trains the model on a GPU"),
                    opt(
                        "Stores large data/models remotely while Git tracks lightweight pointers",
                        correct=True,
                    ),
                    opt("Replaces Git entirely"),
                    opt("Writes the research paper"),
                ),
                "DVC keeps big data/models in remote storage with Git-tracked pointers.",
            ),
            q(
                "How does the spread of reported accuracy scale with the number of seeds averaged?",
                (
                    opt("It grows linearly with the number of seeds"),
                    opt(
                        "It shrinks roughly as 1 over the square root of the number of seeds",
                        correct=True,
                    ),
                    opt("It stays constant regardless of seeds"),
                    opt("It doubles with each extra seed"),
                ),
                "The std of the mean shrinks about as 1/sqrt(n), so report mean over several runs.",
            ),
        ),
        "Publishing reproducible research": (
            q(
                "What is a reproducibility bundle?",
                (
                    opt("A single PDF of the paper"),
                    opt(
                        "Code, environment, and data archived and cross-linked by DOIs",
                        correct=True,
                    ),
                    opt("A list of authors"),
                    opt("A folder of unversioned scripts"),
                ),
                "A bundle ties code, environment and data together with persistent identifiers.",
            ),
            q(
                "What do Binder and CodeOcean enable for reviewers?",
                (
                    opt("Encrypting the manuscript"),
                    opt("Re-running the analysis in the browser without local setup", correct=True),
                    opt("Deleting the data after review"),
                    opt("Skipping peer review"),
                ),
                "Executable artifacts let reviewers re-run the analysis without installing anything.",
            ),
            q(
                "When should reproducibility be addressed?",
                (
                    opt("Only at submission time"),
                    opt("Throughout the work, so publishing is the easy last step", correct=True),
                    opt("Never, if the result looks correct"),
                    opt("Only after the paper is rejected"),
                ),
                "Reproducibility is a way of working throughout, making the final bundle easy.",
            ),
        ),
    },
    final=(
        q(
            "What is the main reproducibility advantage of a container over pinned packages alone?",
            (
                opt("It runs faster on every machine"),
                opt(
                    "It packages the entire user-space environment, not just Python deps",
                    correct=True,
                ),
                opt("It removes the need for version control"),
                opt("It encrypts the source code"),
            ),
            "A container bundles OS libraries and runtime, so it runs identically anywhere.",
        ),
        q(
            "What does committing a lock file (flake.lock, uv.lock, renv.lock) capture?",
            (
                opt("Only the top-level package names"),
                opt("The fully resolved dependency graph", correct=True),
                opt("The output figures"),
                opt("The reviewer comments"),
            ),
            "Lock files record the complete resolved dependency graph for reproducibility.",
        ),
        q(
            "Which is true of the FAIR principles?",
            (
                opt("FAIR data must always be fully open"),
                opt("Data can be FAIR even while access is controlled", correct=True),
                opt("FAIR applies only to hardware"),
                opt("FAIR forbids the use of DOIs"),
            ),
            "FAIR is not the same as open; controlled-access data can still be FAIR.",
        ),
        q(
            "What is the role of provenance versus reproducibility?",
            (
                opt("They are identical concepts"),
                opt(
                    "Provenance records how a result was made; reproducibility re-creates it",
                    correct=True,
                ),
                opt("Provenance only applies to hardware"),
                opt("Reproducibility is unrelated to lineage"),
            ),
            "Provenance is the recorded lineage; reproducibility is getting the same answer again.",
        ),
        q(
            "In reproducible ML, what does DVC let `git checkout` restore?",
            (
                opt("Nothing beyond the code"),
                opt("The matching data and model alongside the code", correct=True),
                opt("Only the README"),
                opt("The CI logs"),
            ),
            "DVC pointers in Git mean a checkout restores the matching data and model.",
        ),
        q(
            "What ties a published reproducibility bundle together?",
            (
                opt("A single uncited zip file"),
                opt(
                    "Cross-linked persistent identifiers (DOIs) for code, data and paper",
                    correct=True,
                ),
                opt("A list of email addresses"),
                opt("An unversioned notebook"),
            ),
            "Persistent identifiers for code, data and paper, cross-linked, form the bundle.",
        ),
    ),
)
