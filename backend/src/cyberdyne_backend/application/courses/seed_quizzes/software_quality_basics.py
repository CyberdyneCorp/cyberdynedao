"""Curated quiz questions for the Software Quality - Basics course. Keys are the
EXACT content-lesson titles; the seed interleaves a checkpoint quiz after each
content lesson plus a final comprehensive quiz."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is software quality?": (
            q(
                "Which set of benefits is the classic signal that the answer is "
                "'software quality'?",
                (
                    opt(
                        "Saves money, prevents catastrophic emergencies, earns "
                        "customer trust, keeps the user experience high",
                        correct=True,
                    ),
                    opt("Faster compilation and smaller binaries"),
                    opt("More lines of code per developer per day"),
                    opt("Lower cloud storage costs only"),
                ),
                "Those four business benefits together point to software quality.",
            ),
            q(
                "Software quality is best defined as the degree to which a system:",
                (
                    opt(
                        "Meets users' needs, defined requirements, and expected "
                        "technical standards",
                        correct=True,
                    ),
                    opt("Uses the newest programming language"),
                    opt("Has the most automated tests"),
                    opt("Was written the fastest"),
                ),
                "Quality is conformance to needs, requirements, and standards.",
            ),
            q(
                "Why is quality not something you 'bolt on at the end'?",
                (
                    opt(
                        "It is the cumulative result of good requirements, design, "
                        "construction, and verification",
                        correct=True,
                    ),
                    opt("Because tools forbid late changes"),
                    opt("Because customers never inspect the product"),
                    opt("Because it only depends on the programming language"),
                ),
                "Quality accumulates across every phase, not just a final step.",
            ),
        ),
        "Quality assurance (QA) vs quality control": (
            q(
                "What is the primary aim of quality assurance (QA)?",
                (
                    opt(
                        "Ensure the software is delivered with quality and that "
                        "verification is run in an organised way",
                        correct=True,
                    ),
                    opt("Write as much production code as possible"),
                    opt("Replace developers with auditors"),
                    opt("Find every bug only after release"),
                ),
                "QA assures quality delivery and an organised verification process.",
            ),
            q(
                "Which statement correctly distinguishes QA from QC?",
                (
                    opt(
                        "QA is preventive and process-focused; QC is detective and product-focused",
                        correct=True,
                    ),
                    opt("QA tests the product; QC writes the requirements"),
                    opt("QA and QC are the same activity"),
                    opt("QC defines the process; QA inspects each build"),
                ),
                "QA builds the process; QC checks the built product.",
            ),
            q(
                "Recording errors and non-conformities is a QA activity mainly so the team can:",
                (
                    opt("Fix them and learn to prevent recurrence", correct=True),
                    opt("Bill the customer for each bug"),
                    opt("Increase the line count"),
                    opt("Avoid writing any tests"),
                ),
                "Logging defects feeds correction and continuous learning.",
            ),
        ),
        "Quality attributes vs metrics": (
            q(
                "What is the difference between a quality attribute and a metric?",
                (
                    opt(
                        "An attribute is a desired characteristic; a metric is a way to measure it",
                        correct=True,
                    ),
                    opt("An attribute is a number; a metric is a feeling"),
                    opt("They are interchangeable terms"),
                    opt("An attribute is hardware; a metric is software"),
                ),
                "Attributes are what you want; metrics quantify how much you have.",
            ),
            q(
                "Which group lists quality ATTRIBUTES (not metrics)?",
                (
                    opt("Completeness, understandability, ambiguity", correct=True),
                    opt("MTBF, readability index, requirement count"),
                    opt("Time to fix, number of ambiguous terms"),
                    opt("Lines of code, build duration"),
                ),
                "Completeness, understandability, and ambiguity are characteristics.",
            ),
            q(
                "Which is an example of a METRIC rather than an attribute?",
                (
                    opt(
                        "Mean time between failures (MTBF) for reliability",
                        correct=True,
                    ),
                    opt("Reliability"),
                    opt("Maintainability"),
                    opt("Completeness"),
                ),
                "MTBF is a measurement; reliability/maintainability are attributes.",
            ),
        ),
        "The dependability dimensions": (
            q(
                "Which properties are core to the dependability (trust) dimension?",
                (
                    opt(
                        "Availability, reliability, safety, security",
                        correct=True,
                    ),
                    opt("Color, font, layout, spacing"),
                    opt("Compilation speed and binary size"),
                    opt("Lines of code and commit count"),
                ),
                "Dependability covers availability, reliability, safety, security.",
            ),
            q(
                "Which additional property is commonly cited under dependability and "
                "lets you fix/adapt software without harming trust?",
                (
                    opt("Maintainability", correct=True),
                    opt("Verbosity"),
                    opt("Obfuscation"),
                    opt("Cyclomatic bloat"),
                ),
                "Maintainability lets you correct and adapt while keeping reliability.",
            ),
            q(
                "Why does maintainability matter even more in the era of fast/AI code generation?",
                (
                    opt(
                        "Code must stay organised, understandable, and safe to "
                        "change, not just be produced quickly",
                        correct=True,
                    ),
                    opt("Because AI code never has defects"),
                    opt("Because speed makes maintainability irrelevant"),
                    opt("Because it removes the need for any tests"),
                ),
                "Fast code that can't be changed safely is a liability.",
            ),
        ),
        "Software maintenance types": (
            q(
                "Maintenance done to correct defects, faults, or non-conformities "
                "found after delivery is:",
                (
                    opt("Corrective", correct=True),
                    opt("Adaptive"),
                    opt("Perfective"),
                    opt("Preventive"),
                ),
                "Fixing defects after delivery is corrective maintenance.",
            ),
            q(
                "Adapting software to a new operating system, law, or third-party API "
                "is which type of maintenance?",
                (
                    opt("Adaptive", correct=True),
                    opt("Corrective"),
                    opt("Perfective"),
                    opt("Preventive"),
                ),
                "Adapting to environment changes is adaptive maintenance.",
            ),
            q(
                "Improving the internal structure to avoid future problems (before "
                "they become failures) is:",
                (
                    opt("Preventive", correct=True),
                    opt("Perfective"),
                    opt("Corrective"),
                    opt("Adaptive"),
                ),
                "Preventive maintenance hardens internal structure proactively; "
                "perfective is outward improvement.",
            ),
        ),
        "Lab: measuring quality (defect density & MTBF)": (
            q(
                "In the lab, how is defect density computed?",
                (
                    opt("Defects divided by size in KLOC", correct=True),
                    opt("Defects multiplied by lines of code"),
                    opt("Failures divided by operating hours"),
                    opt("Downtime divided by incidents"),
                ),
                "Defect density = defects / KLOC; lower is better.",
            ),
            q(
                "In the lab, how is MTBF calculated?",
                (
                    opt(
                        "Total operating time divided by the number of failures",
                        correct=True,
                    ),
                    opt("Defects divided by KLOC"),
                    opt("Downtime divided by uptime"),
                    opt("Failures multiplied by 24"),
                ),
                "MTBF = total operating time / failures; higher means more reliable.",
            ),
            q(
                "For the two releases in the lab, which indicates improving quality?",
                (
                    opt("Release B has a lower defect density than A", correct=True),
                    opt("Release B has a higher defect density than A"),
                    opt("Both releases have identical MTBF"),
                    opt("Defect density rose between releases"),
                ),
                "A lower defect density in the later release shows improvement.",
            ),
        ),
    },
    final=(
        q(
            "Which best captures the definition of software quality?",
            (
                opt(
                    "The degree to which a system meets user needs, requirements, "
                    "and technical standards",
                    correct=True,
                ),
                opt("The number of features shipped per quarter"),
                opt("The newest framework in use"),
                opt("The size of the codebase"),
            ),
            "Quality is conformance to needs, requirements, and standards.",
        ),
        q(
            "QA is best described as:",
            (
                opt(
                    "A preventive, process-focused discipline that organises verification",
                    correct=True,
                ),
                opt("A purely detective check of the finished product"),
                opt("Writing more production code"),
                opt("A synonym for compilation"),
            ),
            "QA builds the process so defects are prevented; QC checks the product.",
        ),
        q(
            "Which pairing is correct?",
            (
                opt(
                    "Reliability is an attribute; MTBF is its metric",
                    correct=True,
                ),
                opt("MTBF is an attribute; reliability is its metric"),
                opt("Both reliability and MTBF are metrics"),
                opt("Both reliability and MTBF are attributes"),
            ),
            "Reliability is a desired characteristic; MTBF measures it.",
        ),
        q(
            "Which set are core dependability properties?",
            (
                opt("Availability, reliability, safety, security", correct=True),
                opt("Indentation, naming, comments, spacing"),
                opt("Compile time, binary size, RAM, disk"),
                opt("Commits, branches, tags, forks"),
            ),
            "These four (plus maintainability) make up dependability.",
        ),
        q(
            "Improving performance or adding a desired feature to working software "
            "is which maintenance type?",
            (
                opt("Perfective", correct=True),
                opt("Corrective"),
                opt("Adaptive"),
                opt("Preventive"),
            ),
            "Perfective maintenance improves or extends already-working software.",
        ),
        q(
            "A higher MTBF and a lower defect density together indicate:",
            (
                opt("More reliable, higher-quality software", correct=True),
                opt("Less reliable software"),
                opt("More escaped defects"),
                opt("A slower build"),
            ),
            "Higher MTBF = more reliable; lower defect density = fewer bugs per size.",
        ),
    ),
)
