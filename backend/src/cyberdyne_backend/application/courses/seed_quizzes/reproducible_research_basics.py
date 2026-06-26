"""Quiz questions for the Reproducible Research & Scientific Software - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The reproducibility crisis": (
            q(
                "What does it mean for a computational result to be reproducible?",
                (
                    opt(
                        "Someone can re-run your code on your data and get the same numbers",
                        correct=True,
                    ),
                    opt("A different team gets a similar result with new data and methods"),
                    opt("The result is published in a peer-reviewed journal"),
                    opt("The analysis uses only open-source software"),
                ),
                "Reproducibility is same data plus same code yielding the same result.",
            ),
            q(
                "Which is a leading cause of irreproducible computational results?",
                (
                    opt("Using version control too aggressively"),
                    opt(
                        "Undocumented manual steps and uncontrolled software versions", correct=True
                    ),
                    opt("Writing too many automated tests"),
                    opt("Archiving data with a DOI"),
                ),
                "Lost scripts, manual steps and uncontrolled versions are the common mundane causes.",
            ),
            q(
                "How does replicability differ from reproducibility?",
                (
                    opt("Replicability means re-running the exact same code and data"),
                    opt(
                        "Replicability means getting a consistent result with new data or methods",
                        correct=True,
                    ),
                    opt("They are identical terms with no distinction"),
                    opt("Replicability refers only to hardware, not software"),
                ),
                "Replicability uses new data or methods and still reaches a consistent conclusion.",
            ),
        ),
        "Version control with Git": (
            q(
                "What does a Git commit represent?",
                (
                    opt(
                        "A snapshot of the project tied to an exact state of the code", correct=True
                    ),
                    opt("A folder of large binary outputs"),
                    opt("A live connection to a remote server"),
                    opt("An automatically running test suite"),
                ),
                "Each commit is a snapshot, identified by a unique hash.",
            ),
            q(
                "Which files should typically NOT be committed to Git?",
                (
                    opt("Source code and small scripts"),
                    opt("Large binaries, secrets, and generated outputs", correct=True),
                    opt("The README and LICENSE"),
                    opt("Plain-text configuration"),
                ),
                "Large binaries, secrets and regenerable outputs belong in .gitignore.",
            ),
            q(
                "What is the purpose of a commit's SHA hash in a paper?",
                (
                    opt("It encrypts the repository so others cannot read it"),
                    opt(
                        "It uniquely identifies the exact code state that produced a result",
                        correct=True,
                    ),
                    opt("It compresses the history to save disk space"),
                    opt("It automatically deploys the code to a server"),
                ),
                "Citing the SHA lets anyone check out exactly the code behind a figure.",
            ),
        ),
        "Project structure": (
            q(
                "Why should raw data be treated as read-only?",
                (
                    opt("Because Git cannot track files that change"),
                    opt(
                        "So the path from raw data to result stays fully traceable",
                        correct=True,
                    ),
                    opt("Because raw data takes less disk space when locked"),
                    opt("Because processed data is always more accurate"),
                ),
                "Never editing raw data keeps every transformation traceable through scripts.",
            ),
            q(
                "What is the single most valuable reproducibility investment in project structure?",
                (
                    opt("Storing outputs inside the data/raw folder"),
                    opt("One command (e.g. a Makefile) that rebuilds every output", correct=True),
                    opt("Keeping all code in a single large notebook"),
                    opt("Committing generated figures to Git"),
                ),
                "A one-command rebuild from raw data to figures is the best investment.",
            ),
            q(
                "Why can the contents of results/ usually be safely git-ignored?",
                (
                    opt("Because results are never important"),
                    opt("Because they should be re-creatable by running the code", correct=True),
                    opt("Because Git cannot store image files"),
                    opt("Because results must always be deleted after publication"),
                ),
                "If outputs are regenerable by code, they need not be version-controlled.",
            ),
        ),
        "Literate programming & notebooks": (
            q(
                "What does literate programming interleave?",
                (
                    opt("Prose, code, and output in one readable document", correct=True),
                    opt("Multiple programming languages in one file"),
                    opt("Compiled binaries and source code"),
                    opt("Databases and web servers"),
                ),
                "It mixes narrative, the code, and its output so humans and machines both benefit.",
            ),
            q(
                "What is the danger of hidden state in a notebook?",
                (
                    opt("It makes the notebook file too large to open"),
                    opt(
                        "Out-of-order cells leave variables that vanish on a fresh start",
                        correct=True,
                    ),
                    opt("It prevents the notebook from being saved"),
                    opt("It encrypts the outputs unexpectedly"),
                ),
                "Cells run out of order create state that won't exist on a clean kernel.",
            ),
            q(
                "What practice ensures a notebook is trustworthy before committing?",
                (
                    opt("Deleting all the markdown cells"),
                    opt("Restart the kernel and run all cells top to bottom", correct=True),
                    opt("Running only the last cell"),
                    opt("Saving it as a PDF"),
                ),
                "Restart and Run All on a clean kernel confirms it reproduces the results.",
            ),
        ),
        "Tracking dependencies": (
            q(
                "Why pin exact dependency versions?",
                (
                    opt("To make installation slower and more careful"),
                    opt("So the same software stack rebuilds identically anywhere", correct=True),
                    opt("To use the newest features automatically"),
                    opt("To reduce the number of packages needed"),
                ),
                "Pinning exact versions prevents silent drift and ensures the stack reproduces.",
            ),
            q(
                "What does `pip freeze > requirements.txt` do?",
                (
                    opt("Deletes all installed packages"),
                    opt("Snapshots the resolved package versions to a file", correct=True),
                    opt("Upgrades every package to the latest version"),
                    opt("Creates a new virtual environment"),
                ),
                "It records the currently resolved versions so they can be reinstalled.",
            ),
            q(
                "What happens as the number of unpinned packages grows?",
                (
                    opt("The environment becomes more reproducible"),
                    opt(
                        "The probability the environment still matches falls quickly", correct=True
                    ),
                    opt("Installation always fails immediately"),
                    opt("Git automatically pins them for you"),
                ),
                "More loose packages means a fast-falling chance the stack still matches.",
            ),
        ),
        "Data management & licensing": (
            q(
                "What does a SHA-256 checksum of a data file let you detect?",
                (
                    opt("The author of the file"),
                    opt("Silent corruption, since any byte change alters the digest", correct=True),
                    opt("The licence terms of the file"),
                    opt("How fast the file can be downloaded"),
                ),
                "A cryptographic hash changes completely if even one byte changes.",
            ),
            q(
                "Why deposit a dataset in an archive like Zenodo or Dryad?",
                (
                    opt("To make it impossible to cite"),
                    opt("To mint a persistent DOI that won't rot like a URL", correct=True),
                    opt("To automatically run your analysis"),
                    opt("To compress the data without loss"),
                ),
                "Archives mint a DOI, giving a stable, citable identifier.",
            ),
            q(
                "What is the consequence of publishing code with no licence?",
                (
                    opt("It is automatically public domain"),
                    opt(
                        "It is effectively 'all rights reserved' and nobody may legally reuse it",
                        correct=True,
                    ),
                    opt("It becomes CC BY by default"),
                    opt("It cannot be downloaded"),
                ),
                "Without a licence the default is all rights reserved, blocking reuse.",
            ),
        ),
    },
    final=(
        q(
            "Which definition matches a reproducible result?",
            (
                opt("Same data and same code produce the same result", correct=True),
                opt("New data and new methods reach a similar conclusion"),
                opt("The work is peer-reviewed and published"),
                opt("The code is written in a popular language"),
            ),
            "Reproducible = same data + same code -> same result.",
        ),
        q(
            "What is the main role of Git in a reproducible workflow?",
            (
                opt("To store large datasets efficiently"),
                opt("To record code snapshots tied to exact, citable states", correct=True),
                opt("To run statistical analyses"),
                opt("To replace the need for documentation"),
            ),
            "Git records commits so every result links to an exact code state.",
        ),
        q(
            "Which directory should be read-only in a sound project structure?",
            (
                opt("results/"),
                opt("data/raw/", correct=True),
                opt("notebooks/"),
                opt("src/"),
            ),
            "Raw data is sacred and read-only; transformations write elsewhere.",
        ),
        q(
            "What is the recommended check before trusting a notebook?",
            (
                opt("Run only the first cell"),
                opt("Restart the kernel and run all cells in order", correct=True),
                opt("Export it to HTML"),
                opt("Increase the font size"),
            ),
            "Restart and Run All on a clean kernel catches hidden state.",
        ),
        q(
            "What is the benefit of committing a lock file (e.g. requirements.txt with pins)?",
            (
                opt("It hides the dependencies from collaborators"),
                opt(
                    "It makes the exact environment part of the version-controlled record",
                    correct=True,
                ),
                opt("It speeds up the code at runtime"),
                opt("It removes the need for tests"),
            ),
            "A committed lock file records the resolved environment for rebuilding.",
        ),
        q(
            "Which licence type is appropriate for source code?",
            (
                opt("CC0 or CC BY"),
                opt("MIT, BSD, or Apache-2.0", correct=True),
                opt("No licence at all"),
                opt("A DOI"),
            ),
            "MIT/BSD/Apache-2.0 are standard code licences; CC licences suit data.",
        ),
    ),
)
