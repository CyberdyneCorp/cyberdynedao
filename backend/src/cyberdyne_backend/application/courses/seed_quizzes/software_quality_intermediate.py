"""Curated quiz questions for the Software Quality - Intermediate course. Keys
are the EXACT content-lesson titles; the seed interleaves a checkpoint quiz
after each content lesson plus a final comprehensive quiz."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The ISO/IEC 25010 product quality model": (
            q(
                "What does the ISO/IEC 25010 product quality model provide?",
                (
                    opt(
                        "Eight top-level quality characteristics to evaluate software against",
                        correct=True,
                    ),
                    opt("A programming language specification"),
                    opt("A list of approved cloud providers"),
                    opt("A single overall quality score formula"),
                ),
                "25010 defines eight characteristics, each with sub-characteristics.",
            ),
            q(
                "Which of these is one of the eight ISO/IEC 25010 characteristics?",
                (
                    opt("Maintainability", correct=True),
                    opt("Profitability"),
                    opt("Marketability"),
                    opt("Headcount"),
                ),
                "Maintainability is one of the eight product-quality characteristics.",
            ),
            q(
                "The 25010 product model describes quality of:",
                (
                    opt("The software artifact itself", correct=True),
                    opt("Only the user's real-world outcomes"),
                    opt("The development team's morale"),
                    opt("The sales pipeline"),
                ),
                "Product quality is the artifact view; quality in use is outcomes.",
            ),
        ),
        "SQuaRE & quality in use": (
            q(
                "What are the four quality-in-use characteristics in SQuaRE?",
                (
                    opt(
                        "Effectiveness, productivity, safety, satisfaction",
                        correct=True,
                    ),
                    opt("Speed, size, security, scalability"),
                    opt("Cost, schedule, scope, staffing"),
                    opt("Correctness, completeness, clarity, coverage"),
                ),
                "Quality in use = effectiveness, productivity, safety, satisfaction.",
            ),
            q(
                "In quality in use, 'effectiveness' means:",
                (
                    opt("The user achieves their goals", correct=True),
                    opt("The CPU usage is low"),
                    opt("The code compiles quickly"),
                    opt("The binary is small"),
                ),
                "Effectiveness is about the user accurately achieving their goals.",
            ),
            q(
                "How does quality in use differ from product quality?",
                (
                    opt(
                        "It measures the outcomes of a user pursuing a goal in a "
                        "real context, not the artifact's properties",
                        correct=True,
                    ),
                    opt("It only measures lines of code"),
                    opt("It ignores the user entirely"),
                    opt("It is identical to product quality"),
                ),
                "Quality in use is context- and outcome-oriented.",
            ),
        ),
        "Reviews, inspections & audits": (
            q(
                "Which is the MOST formal static quality technique, with defined "
                "roles and checklists?",
                (
                    opt("Inspection", correct=True),
                    opt("Walkthrough"),
                    opt("Coffee chat"),
                    opt("Smoke test"),
                ),
                "Inspections (Fagan) use roles, entry/exit criteria, and checklists.",
            ),
            q(
                "What is the primary purpose of an audit?",
                (
                    opt(
                        "Independently check that the process and standards were actually followed",
                        correct=True,
                    ),
                    opt("Run the unit-test suite"),
                    opt("Measure CPU performance"),
                    opt("Generate random test inputs"),
                ),
                "An audit is an independent compliance check of process/standards.",
            ),
            q(
                "Why are reviews and inspections high-ROI quality activities?",
                (
                    opt(
                        "They catch defects early, before code runs, where fixing is far cheaper",
                        correct=True,
                    ),
                    opt("They replace the need for requirements"),
                    opt("They only work after release"),
                    opt("They eliminate the need to write code"),
                ),
                "Static techniques shift detection left, where defects cost less.",
            ),
        ),
        "Defect management & the defect lifecycle": (
            q(
                "In the defect lifecycle, what happens when a retest of a 'Fixed' defect fails?",
                (
                    opt("It is reopened and goes back into progress", correct=True),
                    opt("It is automatically closed"),
                    opt("It is deleted permanently"),
                    opt("It becomes a new feature"),
                ),
                "A failed retest reopens the defect for more work.",
            ),
            q(
                "What is the difference between severity and priority?",
                (
                    opt(
                        "Severity is technical impact; priority is business urgency",
                        correct=True,
                    ),
                    opt("Severity is business urgency; priority is technical impact"),
                    opt("They always have the same value"),
                    opt("Severity is the fix time; priority is the line number"),
                ),
                "A high-severity bug can be low priority, and vice versa.",
            ),
            q(
                "Why track defects with consistent states, severity, and root cause?",
                (
                    opt(
                        "It turns bug-fixing into data that drives metrics and process improvement",
                        correct=True,
                    ),
                    opt("To make the backlog look larger"),
                    opt("To slow down developers"),
                    opt("To avoid writing tests"),
                ),
                "Structured defect data feeds metrics like DRE and reveals where "
                "defects enter the process.",
            ),
        ),
        "Quality metrics that matter (MTBF, MTTR, availability, DRE)": (
            q(
                "How is availability computed from MTBF and MTTR?",
                (
                    opt("MTBF / (MTBF + MTTR)", correct=True),
                    opt("MTTR / (MTBF + MTTR)"),
                    opt("MTBF * MTTR"),
                    opt("MTBF - MTTR"),
                ),
                "Availability = MTBF / (MTBF + MTTR).",
            ),
            q(
                "What does Defect Removal Efficiency (DRE) measure?",
                (
                    opt(
                        "The fraction of defects caught before release out of all defects",
                        correct=True,
                    ),
                    opt("The average response latency"),
                    opt("The number of lines of code"),
                    opt("The time to compile"),
                ),
                "DRE = defects found before release / total defects found.",
            ),
            q(
                "For a fixed MTBF, what raises availability the most?",
                (
                    opt("Reducing MTTR (recovering faster)", correct=True),
                    opt("Increasing MTTR"),
                    opt("Adding more lines of code"),
                    opt("Lowering DRE"),
                ),
                "With MTBF fixed, smaller MTTR pushes availability toward 1.",
            ),
        ),
        "Lab: a quality scorecard (availability & DRE)": (
            q(
                "In the lab, MTTR is computed as:",
                (
                    opt("Downtime hours divided by the number of incidents", correct=True),
                    opt("Operating hours divided by failures"),
                    opt("Defects divided by KLOC"),
                    opt("Incidents multiplied by downtime"),
                ),
                "MTTR = total downtime / incidents.",
            ),
            q(
                "In the lab, what range must availability fall within?",
                (
                    opt("Strictly between 0 and 1", correct=True),
                    opt("Any value above 1"),
                    opt("Exactly 0"),
                    opt("Between 1 and 100 with no upper bound"),
                ),
                "Availability is a fraction in (0, 1); the lab asserts this.",
            ),
            q(
                "In the lab's letter-grade logic, what earns extra points?",
                (
                    opt(
                        "Higher availability and higher DRE thresholds",
                        correct=True,
                    ),
                    opt("More lines of code"),
                    opt("A larger defect count"),
                    opt("A longer MTTR"),
                ),
                "Points accrue as availability and DRE cross higher thresholds.",
            ),
        ),
    },
    final=(
        q(
            "The ISO/IEC 25010 product quality model consists of:",
            (
                opt("Eight quality characteristics", correct=True),
                opt("Five maturity levels"),
                opt("Four quality-in-use factors"),
                opt("Three levels of concern"),
            ),
            "25010 has eight product-quality characteristics.",
        ),
        q(
            "Quality in use (SQuaRE) is made up of:",
            (
                opt(
                    "Effectiveness, productivity, safety, satisfaction",
                    correct=True,
                ),
                opt("Functionality, reliability, usability, portability"),
                opt("Plan, do, check, act"),
                opt("Initial, managed, defined, optimizing"),
            ),
            "Those four are the quality-in-use characteristics.",
        ),
        q(
            "Which static technique is an independent check that the process was followed?",
            (
                opt("Audit", correct=True),
                opt("Walkthrough"),
                opt("Inspection"),
                opt("Technical review"),
            ),
            "An audit independently verifies process/standards compliance.",
        ),
        q(
            "Severity vs priority is best summarised as:",
            (
                opt(
                    "Severity = technical impact; priority = business urgency",
                    correct=True,
                ),
                opt("Both mean the same thing"),
                opt("Severity = urgency; priority = impact"),
                opt("Severity = fix cost; priority = bug id"),
            ),
            "They are independent axes of a defect.",
        ),
        q(
            "Availability equals:",
            (
                opt("MTBF / (MTBF + MTTR)", correct=True),
                opt("MTTR / MTBF"),
                opt("MTBF + MTTR"),
                opt("Defects / KLOC"),
            ),
            "Availability = MTBF / (MTBF + MTTR).",
        ),
        q(
            "A high Defect Removal Efficiency (DRE) means:",
            (
                opt("Most defects are caught before they reach users", correct=True),
                opt("Most defects escape to production"),
                opt("The system has low availability"),
                opt("MTTR is very high"),
            ),
            "High DRE = few escaped defects, a strong process signal.",
        ),
    ),
)
