"""Quiz questions for the Reproducible Research & Scientific Software - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Branching & collaboration": (
            q(
                "What is a Git branch?",
                (
                    opt("A movable pointer for developing without disturbing main", correct=True),
                    opt("A backup copy stored on a separate disk"),
                    opt("A compressed archive of the repository"),
                    opt("A remote server that hosts the code"),
                ),
                "A branch lets you develop a feature in isolation from main.",
            ),
            q(
                "What is the purpose of a Pull/Merge Request?",
                (
                    opt("To delete a branch automatically"),
                    opt("To provide peer review of a diff before it reaches main", correct=True),
                    opt("To run the analysis on a cluster"),
                    opt("To mint a DOI for the code"),
                ),
                "A PR is the unit of code review: a colleague reviews and approves the diff.",
            ),
            q(
                "What does a Git tag like v1.0.0 mark?",
                (
                    opt("A file that should be ignored"),
                    opt("The exact commit behind a published result", correct=True),
                    opt("A temporary branch for experiments"),
                    opt("A merge conflict that needs resolving"),
                ),
                "Tags mark a specific commit so reviewers can fetch precisely that state.",
            ),
        ),
        "Automated testing": (
            q(
                "Why are bugs in scientific code described as 'quiet'?",
                (
                    opt("They crash the program immediately"),
                    opt(
                        "A wrong sign or off-by-one can still produce plausible numbers",
                        correct=True,
                    ),
                    opt("They only occur on weekends"),
                    opt("They are always caught by the compiler"),
                ),
                "Scientific bugs often yield believable but wrong results, so tests are vital.",
            ),
            q(
                "What does a property-based test assert?",
                (
                    opt("That one specific input gives one specific output"),
                    opt("An invariant that holds across many random inputs", correct=True),
                    opt("That the code runs without any output"),
                    opt("That the code is faster than a baseline"),
                ),
                "Property tests check invariants (e.g. a normalised vector has norm 1) over many inputs.",
            ),
            q(
                "What is the relationship between test coverage and bugs caught?",
                (
                    opt("Value is flat until 100% coverage"),
                    opt(
                        "Value rises sharply early, then sees diminishing returns near 100%",
                        correct=True,
                    ),
                    opt("More coverage always reduces bugs caught"),
                    opt("Coverage has no effect on bugs caught"),
                ),
                "Even modest coverage catches many bugs; gains taper off near full coverage.",
            ),
        ),
        "Build automation with Make": (
            q(
                "When does Make rebuild a target?",
                (
                    opt("Every single time, regardless of changes"),
                    opt("Only when a prerequisite is newer than the target", correct=True),
                    opt("Only when the user edits the Makefile"),
                    opt("Never, unless forced manually"),
                ),
                "Make rebuilds a target only if a prerequisite has changed, doing minimum work.",
            ),
            q(
                "What does a Makefile encode?",
                (
                    opt("The dependency graph between files and how to rebuild them", correct=True),
                    opt("A list of git commits"),
                    opt("The database schema"),
                    opt("The licence terms of the project"),
                ),
                "A Makefile is the dependency graph plus recipes to rebuild each target.",
            ),
            q(
                "Why is a Makefile good for reproducibility?",
                (
                    opt("It hides the build steps from users"),
                    opt(
                        "It is a single source of truth that rebuilds everything deterministically",
                        correct=True,
                    ),
                    opt("It encrypts the source code"),
                    opt("It deletes intermediate files automatically"),
                ),
                "make all on a fresh clone regenerates every output in the correct order.",
            ),
        ),
        "Workflow management with Snakemake": (
            q(
                "What do wildcards in a Snakemake rule allow?",
                (
                    opt("Encrypting the output files"),
                    opt("Applying one rule to many similar files (e.g. samples)", correct=True),
                    opt("Skipping the dependency graph"),
                    opt("Running code without an environment"),
                ),
                "Wildcards generalise a rule across many samples or inputs.",
            ),
            q(
                "What structure does Snakemake build from the rules?",
                (
                    opt("A relational database"),
                    opt("A directed acyclic graph (DAG) of jobs", correct=True),
                    opt("A single linear script"),
                    opt("A container image"),
                ),
                "Snakemake builds a DAG, runs independent branches in parallel, and re-runs only stale jobs.",
            ),
            q(
                "How can a Snakemake rule guarantee a portable environment?",
                (
                    opt("By declaring its own conda environment or container", correct=True),
                    opt("By running only on the developer's laptop"),
                    opt("By disabling all dependencies"),
                    opt("By avoiding the use of wildcards"),
                ),
                "Each rule can specify a conda env or container, making the step reproducible.",
            ),
        ),
        "Continuous integration": (
            q(
                "What does Continuous Integration do on every push?",
                (
                    opt("Deletes the branch"),
                    opt("Runs the tests automatically in a clean environment", correct=True),
                    opt("Publishes the paper"),
                    opt("Mints a DOI"),
                ),
                "CI runs tests on every push in a fresh environment, catching breakage early.",
            ),
            q(
                "Why does CI also verify your environment file?",
                (
                    opt("It deletes the environment file"),
                    opt("It re-installs pinned dependencies from scratch every run", correct=True),
                    opt("It ignores dependencies entirely"),
                    opt("It only checks code formatting"),
                ),
                "A fresh dependency install each run silently confirms the environment is complete.",
            ),
            q(
                "What happens when CI tests fail on a pull request?",
                (
                    opt("The merge is allowed anyway"),
                    opt("The merge is blocked and the team is notified", correct=True),
                    opt("The repository is deleted"),
                    opt("All branches are merged automatically"),
                ),
                "A failing CI run blocks the merge and notifies the team within minutes.",
            ),
        ),
        "Random seeds & determinism": (
            q(
                "Why fix the seed of a pseudo-random number generator?",
                (
                    opt("To make the code run faster"),
                    opt("So the same seed yields the same random stream every run", correct=True),
                    opt("To increase the randomness of the output"),
                    opt("To avoid using any randomness at all"),
                ),
                "A PRNG is deterministic: a fixed seed reproduces the same sequence.",
            ),
            q(
                "Why prefer an explicit generator over the global np.random.seed?",
                (
                    opt(
                        "The global state leaks between modules and is hard to reason about",
                        correct=True,
                    ),
                    opt("The global seed is always slower"),
                    opt("Explicit generators cannot be reproduced"),
                    opt("The global seed produces no randomness"),
                ),
                "Global RNG state leaks across modules; an explicit generator is local and clear.",
            ),
            q(
                "What can make results non-deterministic even with a fixed seed?",
                (
                    opt("Using a README file"),
                    opt(
                        "Parallelism, where results depend on thread completion order", correct=True
                    ),
                    opt("Committing to Git"),
                    opt("Writing unit tests"),
                ),
                "Parallel execution order can introduce non-determinism despite a fixed seed.",
            ),
        ),
    },
    final=(
        q(
            "What is the unit of peer review for code changes?",
            (
                opt("A commit message"),
                opt("A Pull/Merge Request", correct=True),
                opt("A Git tag"),
                opt("A Makefile target"),
            ),
            "A PR lets a reviewer read the diff, run tests and approve before merge.",
        ),
        q(
            "Which test type locks in a previously correct numeric result?",
            (
                opt("A regression test", correct=True),
                opt("A load test"),
                opt("A smoke screen"),
                opt("A lint check"),
            ),
            "Regression tests pin a known-good numeric result to catch future drift.",
        ),
        q(
            "What advantage does Snakemake have over plain Make?",
            (
                opt("It cannot run in parallel"),
                opt("Wildcards and cluster/cloud support for many samples", correct=True),
                opt("It removes the need for any rules"),
                opt("It only works on a single file"),
            ),
            "Snakemake generalises Make with wildcards and cluster/cloud execution.",
        ),
        q(
            "What is a key reproducibility side-benefit of CI?",
            (
                opt("It compresses the repository"),
                opt(
                    "It re-installs pinned dependencies from scratch, verifying the environment",
                    correct=True,
                ),
                opt("It writes the paper for you"),
                opt("It removes the need for branches"),
            ),
            "CI's clean install each run confirms the environment file is complete.",
        ),
        q(
            "How should stochastic results be reported in a paper?",
            (
                opt("As a single best run"),
                opt("As mean plus/minus standard deviation over several seeds", correct=True),
                opt("Without any seed information"),
                opt("Only as the worst-case run"),
            ),
            "Reporting mean and spread over multiple seeds reflects run-to-run variance honestly.",
        ),
        q(
            "What does committing a Makefile contribute to reproducibility?",
            (
                opt("It encrypts the outputs"),
                opt("A single command rebuilds every output deterministically", correct=True),
                opt("It hides the dependency graph"),
                opt("It replaces version control"),
            ),
            "make all turns scattered scripts into a deterministic, one-command pipeline.",
        ),
    ),
)
