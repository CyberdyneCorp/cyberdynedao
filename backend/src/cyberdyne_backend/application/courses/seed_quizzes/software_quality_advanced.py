"""Curated quiz questions for the Software Quality - Advanced course. Keys are
the EXACT content-lesson titles; the seed interleaves a checkpoint quiz after
each content lesson plus a final comprehensive quiz."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Process maturity: CMMI (5 levels)": (
            q(
                "How many maturity levels does CMMI define?",
                (
                    opt("5", correct=True),
                    opt("3"),
                    opt("7"),
                    opt("10"),
                ),
                "CMMI has 5 maturity levels.",
            ),
            q(
                "What is the central idea of CMMI level 5?",
                (
                    opt("Optimizing: continuous process improvement", correct=True),
                    opt("Initial: unpredictable processes"),
                    opt("Managed: projects planned and tracked"),
                    opt("Defined: standardised processes"),
                ),
                "Level 5 (Optimizing) is about continuous improvement.",
            ),
            q(
                "Which benefit is commonly attributed to adopting CMMI?",
                (
                    opt(
                        "Improved process predictability and reduced rework",
                        correct=True,
                    ),
                    opt("Guaranteed zero defects forever"),
                    opt("Faster typing speed for developers"),
                    opt("Smaller binary sizes"),
                ),
                "CMMI improves processes, quality, predictability, and reduces rework.",
            ),
        ),
        "The MPS.BR maturity model": (
            q(
                "MPS.BR is best described as:",
                (
                    opt(
                        "A process maturity model (Brazilian), aligned with CMMI",
                        correct=True,
                    ),
                    opt("A programming language"),
                    opt("A testing framework"),
                    opt("A cloud hosting provider"),
                ),
                "MPS.BR is a graduated process maturity model.",
            ),
            q(
                "MPS.BR level 2 (Managed) is associated with:",
                (
                    opt(
                        "Project planning, requirements management, monitoring, and suppliers",
                        correct=True,
                    ),
                    opt("Innovation rolled out across the organisation"),
                    opt("Causal analysis and resolution"),
                    opt("Writing unit tests only"),
                ),
                "Level 2 brings individual projects under control.",
            ),
            q(
                "MPS.BR level 5 (Optimizing) is associated with:",
                (
                    opt(
                        "Innovation, organisational rollout, and analysis/resolution of causes",
                        correct=True,
                    ),
                    opt("Basic project planning"),
                    opt("Supplier agreements only"),
                    opt("Unpredictable, ad-hoc processes"),
                ),
                "Level 5 is continuous improvement and root-cause elimination.",
            ),
        ),
        "Quality management at three levels (Sommerville)": (
            q(
                "Which level defines the company's quality policies, standards, and culture?",
                (
                    opt("Organizational level", correct=True),
                    opt("Project level"),
                    opt("Product/process level"),
                    opt("Hardware level"),
                ),
                "The organizational level sets company-wide policies and culture.",
            ),
            q(
                "A quality plan with goals, processes, and standards for a specific "
                "delivery belongs to which level?",
                (
                    opt("Project level", correct=True),
                    opt("Organizational level"),
                    opt("Product/process level"),
                    opt("Network level"),
                ),
                "A project's quality plan is the project level.",
            ),
            q(
                "How do decisions and evidence flow across Sommerville's levels?",
                (
                    opt(
                        "Decisions flow down (org → project → product); findings flow back up",
                        correct=True,
                    ),
                    opt("Everything flows only upward"),
                    opt("The levels are completely independent"),
                    opt("Only the product level makes decisions"),
                ),
                "Standards constrain plans downward; findings flow back up.",
            ),
        ),
        "Building a quality plan & strategy (GQM)": (
            q(
                "What does the GQM approach stand for?",
                (
                    opt("Goal, Question, Metric", correct=True),
                    opt("Gather, Quantify, Measure"),
                    opt("Govern, Qualify, Manage"),
                    opt("Generate, Query, Mutate"),
                ),
                "GQM derives metrics top-down from goals via questions.",
            ),
            q(
                "In GQM, what should be true of every metric you collect?",
                (
                    opt(
                        "It traces back up to a question and a goal",
                        correct=True,
                    ),
                    opt("It is the easiest number to gather"),
                    opt("It is unrelated to any objective"),
                    opt("It maximises the metric count"),
                ),
                "If a metric doesn't trace to a goal, drop it (avoid vanity metrics).",
            ),
            q(
                "At which of Sommerville's levels does a quality plan live?",
                (
                    opt("The project level", correct=True),
                    opt("The organizational level"),
                    opt("The hardware level"),
                    opt("The marketing level"),
                ),
                "A quality plan is a project-level artifact.",
            ),
        ),
        "Continuous improvement: PDCA & root-cause analysis": (
            q(
                "What are the four stages of the PDCA cycle?",
                (
                    opt("Plan, Do, Check, Act", correct=True),
                    opt("Plan, Deploy, Commit, Audit"),
                    opt("Prepare, Design, Code, Assess"),
                    opt("Predict, Develop, Compare, Approve"),
                ),
                "PDCA = Plan-Do-Check-Act, the Deming improvement cycle.",
            ),
            q(
                "What is the purpose of root-cause analysis (e.g. 5 Whys)?",
                (
                    opt(
                        "Trace a defect to its underlying cause so the class of "
                        "defects stops recurring",
                        correct=True,
                    ),
                    opt("Quickly patch the symptom and move on"),
                    opt("Count the total lines of code"),
                    opt("Generate random test inputs"),
                ),
                "RCA fixes the process that let the bug in, not just the symptom.",
            ),
            q(
                "Which maturity-model practice does root-cause analysis embody?",
                (
                    opt(
                        "MPS.BR level 5 / CMMI level 5 causal analysis and continuous improvement",
                        correct=True,
                    ),
                    opt("CMMI level 1 ad-hoc processes"),
                    opt("Basic project planning at level 2 only"),
                    opt("Writing more code without review"),
                ),
                "Causal analysis and resolution is the level-5 continuous-improvement practice.",
            ),
        ),
        "Lab: a maturity-assessment scorer": (
            q(
                "In the lab, why is the assessed level capped even though level-4 "
                "practices are present?",
                (
                    opt(
                        "Maturity is cumulative, so a gap at level 5 caps the score below it",
                        correct=True,
                    ),
                    opt("Because level 4 is invalid"),
                    opt("Because the loop runs backwards"),
                    opt("Because availability was too low"),
                ),
                "A missing lower/upper level caps maturity; you can't skip levels.",
            ),
            q(
                "What does the lab recommend as the 'next focus'?",
                (
                    opt("The first unmet level", correct=True),
                    opt("The highest level already achieved"),
                    opt("Level 1 (Initial)"),
                    opt("A random level"),
                ),
                "The scorer points you at the lowest unmet level.",
            ),
            q(
                "What is the readiness percentage in the lab based on?",
                (
                    opt(
                        "How many of the four practice areas (levels 2-5) are in place",
                        correct=True,
                    ),
                    opt("The number of lines of code"),
                    opt("The MTTR value"),
                    opt("The defect density"),
                ),
                "Readiness = practice areas in place / 4.",
            ),
        ),
    },
    final=(
        q(
            "How many levels does CMMI have, and what is the top one?",
            (
                opt("5 levels; the top is Optimizing", correct=True),
                opt("3 levels; the top is Defined"),
                opt("7 levels; the top is Managed"),
                opt("5 levels; the top is Initial"),
            ),
            "CMMI has 5 levels, topped by Optimizing (continuous improvement).",
        ),
        q(
            "MPS.BR level 2 (Managed) centres on:",
            (
                opt(
                    "Project planning, requirements management, monitoring, suppliers",
                    correct=True,
                ),
                opt("Innovation and causal analysis"),
                opt("Ad-hoc, unpredictable work"),
                opt("Only writing documentation"),
            ),
            "Level 2 gets projects under control.",
        ),
        q(
            "Which Sommerville level owns a project's quality plan with its goals and standards?",
            (
                opt("Project level", correct=True),
                opt("Organizational level"),
                opt("Product/process level"),
                opt("Vendor level"),
            ),
            "The project level defines the project's quality plan.",
        ),
        q(
            "In GQM, metrics are derived from:",
            (
                opt("Goals, via questions", correct=True),
                opt("Whatever is easiest to measure"),
                opt("The number of developers"),
                opt("The programming language used"),
            ),
            "GQM is a top-down Goal → Question → Metric derivation.",
        ),
        q(
            "The PDCA cycle's stages are:",
            (
                opt("Plan, Do, Check, Act", correct=True),
                opt("Plan, Deploy, Commit, Act"),
                opt("Predict, Do, Compare, Audit"),
                opt("Prepare, Design, Check, Approve"),
            ),
            "PDCA is the Plan-Do-Check-Act improvement loop.",
        ),
        q(
            "What links MPS.BR/CMMI level 5 with root-cause analysis?",
            (
                opt(
                    "Both target continuous improvement by eliminating the causes of defects",
                    correct=True,
                ),
                opt("Both forbid measuring anything"),
                opt("Both are about initial, ad-hoc processes"),
                opt("Neither relates to process improvement"),
            ),
            "Level 5 causal analysis and resolution is continuous improvement via RCA.",
        ),
    ),
)
