"""Quiz questions for the Scientific Computing & Linux - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Bash scripting fundamentals": (
            q(
                "What does `set -euo pipefail` do?",
                (
                    opt(
                        "Makes the script fail fast on errors, unset vars and pipe failures",
                        correct=True,
                    ),
                    opt("Enables verbose colour output"),
                    opt("Runs the script in the background"),
                    opt("Disables all error checking"),
                ),
                "It exits on errors, undefined variables and failed pipeline stages.",
            ),
            q(
                "What is the shebang `#!/usr/bin/env bash` for?",
                (
                    opt("It names the interpreter that runs the script", correct=True),
                    opt("It is a comment ignored by everything"),
                    opt("It deletes the file after running"),
                    opt("It sets file permissions"),
                ),
                "The shebang tells the OS which interpreter to use.",
            ),
            q(
                'Why quote variables like "$s" in scripts?',
                (
                    opt(
                        "To stop spaces in values from splitting into multiple arguments",
                        correct=True,
                    ),
                    opt("To make them uppercase"),
                    opt("To export them globally"),
                    opt("Quoting has no effect in Bash"),
                ),
                "Unquoted variables word-split on spaces, a common bug.",
            ),
        ),
        "Reproducible environments: conda and venv": (
            q(
                "Why are isolated environments important in science?",
                (
                    opt(
                        "Different package versions can change results; isolation pins them",
                        correct=True,
                    ),
                    opt("They make the terminal prettier"),
                    opt("They speed up the CPU"),
                    opt("They are required to use SSH"),
                ),
                "Pinned dependencies give identical, reproducible numbers.",
            ),
            q(
                "Why is conda (with bioconda) common in bioinformatics?",
                (
                    opt("It installs non-Python tools and their C libraries too", correct=True),
                    opt("It only installs pure-Python packages"),
                    opt("It is the system package manager"),
                    opt("It replaces Git"),
                ),
                "conda handles compiled tools like samtools, not just Python packages.",
            ),
            q(
                "Which command captures pinned Python versions for sharing?",
                (
                    opt("pip freeze > requirements.txt", correct=True),
                    opt("pip list --outdated"),
                    opt("python --version"),
                    opt("conda clean"),
                ),
                "pip freeze records exact versions to reproduce the env.",
            ),
        ),
        "Version control with Git": (
            q(
                "What is a Git commit?",
                (
                    opt("A recorded snapshot of the project pointing to its parent", correct=True),
                    opt("A live copy of the working directory only"),
                    opt("A backup on a USB drive"),
                    opt("A remote server"),
                ),
                "Commits are snapshots linked into a history graph.",
            ),
            q(
                "What do branches enable?",
                (
                    opt(
                        "Developing a feature without disturbing the working version", correct=True
                    ),
                    opt("Deleting the repository history"),
                    opt("Compressing files"),
                    opt("Logging into remote servers"),
                ),
                "Branches isolate work until you merge it back.",
            ),
            q(
                "What belongs in .gitignore for a data project?",
                (
                    opt("Large data and generated outputs", correct=True),
                    opt("Your source code"),
                    opt("The README"),
                    opt("The commit messages"),
                ),
                "Version the code, not gigabytes of data or outputs.",
            ),
        ),
        "Processes, jobs and resource monitoring": (
            q(
                "What identifies a running process?",
                (
                    opt("Its PID (process id)", correct=True),
                    opt("Its file extension"),
                    opt("Its IP address"),
                    opt("Its permission bits"),
                ),
                "Each process has a numeric PID.",
            ),
            q(
                "What does the kernel's OOM killer do?",
                (
                    opt("Kills processes when the system runs out of memory", correct=True),
                    opt("Optimises output ordering"),
                    opt("Restarts the network"),
                    opt("Cleans up old files"),
                ),
                "Out-Of-Memory killer terminates processes under memory pressure.",
            ),
            q(
                "What does appending `&` to a command do?",
                (
                    opt("Runs it in the background", correct=True),
                    opt("Forces it to fail"),
                    opt("Pipes it to another command"),
                    opt("Redirects its output to a file"),
                ),
                "& launches the job in the background.",
            ),
        ),
        "Scheduling and automation with cron": (
            q(
                "How many time fields does a cron schedule line have?",
                (
                    opt("Five (minute, hour, day-of-month, month, day-of-week)", correct=True),
                    opt("Three"),
                    opt("Seven"),
                    opt("One"),
                ),
                "Cron uses five time fields then the command.",
            ),
            q(
                "Why must cron scripts use absolute paths and activate their env?",
                (
                    opt("Cron runs with a minimal environment and bare PATH", correct=True),
                    opt("Cron deletes relative paths"),
                    opt("Absolute paths run faster"),
                    opt("Cron cannot read variables at all"),
                ),
                "The cron environment is minimal, so be explicit.",
            ),
            q(
                "What does `0 2 * * *` mean?",
                (
                    opt("Run every day at 02:00", correct=True),
                    opt("Run every 2 minutes"),
                    opt("Run on the 2nd of every month"),
                    opt("Run twice a year"),
                ),
                "Minute 0, hour 2, every day.",
            ),
        ),
        "Package and build tooling": (
            q(
                "What does `make` use to decide what to rebuild?",
                (
                    opt(
                        "A dependency graph of targets and prerequisites, rebuilding only what changed",
                        correct=True,
                    ),
                    opt("It always rebuilds everything from scratch"),
                    opt("Random selection"),
                    opt("The current time of day"),
                ),
                "make tracks dependencies and skips unchanged targets.",
            ),
            q(
                "What does `make -j4` do?",
                (
                    opt("Builds using 4 parallel jobs", correct=True),
                    opt("Jumps to target 4"),
                    opt("Installs 4 packages"),
                    opt("Limits memory to 4 GB"),
                ),
                "-j4 runs four compilation jobs in parallel.",
            ),
            q(
                "Where do modern Python projects declare their build config?",
                (
                    opt("pyproject.toml", correct=True),
                    opt("Makefile"),
                    opt("requirements.lock only"),
                    opt(".gitignore"),
                ),
                "pyproject.toml is the standard build/declaration file.",
            ),
        ),
    },
    final=(
        q(
            "Which habit makes a Bash script fail fast?",
            (
                opt("set -euo pipefail", correct=True),
                opt("echo everything"),
                opt("running as root"),
                opt("removing the shebang"),
            ),
            "It stops on errors, unset vars and pipe failures.",
        ),
        q(
            "What does sharing environment.yml accomplish?",
            (
                opt("Lets a collaborator recreate your exact dependency stack", correct=True),
                opt("Encrypts the project"),
                opt("Speeds up the GPU"),
                opt("Submits a cluster job"),
            ),
            "It is a reproducible spec of the conda environment.",
        ),
        q(
            "Which command stages a file for the next Git commit?",
            (
                opt("git add file.py", correct=True),
                opt("git commit"),
                opt("git log"),
                opt("git push"),
            ),
            "git add stages changes for committing.",
        ),
        q(
            "Which command shows live per-process CPU and memory?",
            (opt("top (or htop)", correct=True), opt("ls -l"), opt("df -h"), opt("git status")),
            "top/htop give a live process view.",
        ),
        q(
            "cron is best described as a:",
            (
                opt("time-based job scheduler", correct=True),
                opt("version control system"),
                opt("text editor"),
                opt("package manager"),
            ),
            "cron runs commands on a schedule.",
        ),
        q(
            "What is the unifying idea behind make and modern build tools?",
            (
                opt(
                    "A declarative spec: state inputs/outputs and let the tool order and skip work",
                    correct=True,
                ),
                opt("Always recompile from scratch"),
                opt("Avoid dependencies entirely"),
                opt("Manual step-by-step execution"),
            ),
            "Declarative dependency graphs drive incremental builds and pipelines.",
        ),
    ),
)
