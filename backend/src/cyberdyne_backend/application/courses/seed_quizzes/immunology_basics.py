"""Quiz questions for the Immunology - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What the immune system defends and how": (
            q(
                "What is the central problem the immune system must solve?",
                (
                    opt("Discriminating dangerous threats from healthy self tissue", correct=True),
                    opt("Producing energy for the cell"),
                    opt("Replicating DNA accurately"),
                    opt("Transporting oxygen in the blood"),
                ),
                "Immunity must destroy pathogens and cancer while sparing self.",
            ),
            q(
                "How does innate immunity differ from adaptive immunity in timing?",
                (
                    opt("Innate responds in minutes to hours; adaptive takes days", correct=True),
                    opt("Adaptive responds first, innate later"),
                    opt("Both respond at exactly the same speed"),
                    opt("Innate takes weeks while adaptive is instant"),
                ),
                "Innate is fast and fixed; adaptive is slower, specific and improves with experience.",
            ),
            q(
                "Which feature is unique to adaptive immunity?",
                (
                    opt("Immunological memory of past exposures", correct=True),
                    opt("Use of physical barriers like skin"),
                    opt("The same response on every exposure"),
                    opt("Germline-encoded fixed receptors only"),
                ),
                "Adaptive immunity leaves memory, making recall responses faster and larger.",
            ),
        ),
        "Innate immunity: cells and barriers": (
            q(
                "Which cell is typically the first phagocyte to arrive at a wound?",
                (
                    opt("The neutrophil", correct=True),
                    opt("The B cell"),
                    opt("The plasma cell"),
                    opt("The memory T cell"),
                ),
                "Neutrophils are abundant, short-lived first responders.",
            ),
            q(
                "How do NK cells decide to kill a target?",
                (
                    opt("They kill cells that have lowered MHC-I (missing-self)", correct=True),
                    opt("They require a specific antibody for every target"),
                    opt("They only kill cells with high MHC-I"),
                    opt("They engulf bacteria by phagocytosis"),
                ),
                "NK cells target stressed or infected cells that downregulate MHC-I.",
            ),
            q(
                "What does the NADPH oxidase respiratory burst produce inside the phagosome?",
                (
                    opt("Reactive oxygen species that kill the engulfed microbe", correct=True),
                    opt("Antibodies"),
                    opt("New ribosomes"),
                    opt("Glucose for the cell"),
                ),
                "The respiratory burst floods the phagosome with microbicidal ROS.",
            ),
        ),
        "Pattern recognition and inflammation": (
            q(
                "What do pattern recognition receptors (PRRs) recognize?",
                (
                    opt(
                        "Conserved molecular patterns shared by classes of microbes (PAMPs)",
                        correct=True,
                    ),
                    opt("A single unique antigen per receptor"),
                    opt("Only host self proteins"),
                    opt("Random sequences with no pattern"),
                ),
                "PRRs bind conserved PAMPs like LPS that microbes cannot easily lose.",
            ),
            q(
                "TLR4 engagement signals through MyD88 to activate which transcription factor?",
                (
                    opt("NF-kB, driving inflammatory cytokine genes", correct=True),
                    opt("Hemoglobin"),
                    opt("DNA polymerase"),
                    opt("The proteasome"),
                ),
                "TLR signaling activates NF-kB to transcribe TNF, IL-1, IL-6 and chemokines.",
            ),
            q(
                "What is a DAMP?",
                (
                    opt(
                        "A danger signal released by damaged self cells, such as ATP or HMGB1",
                        correct=True,
                    ),
                    opt("A microbial sugar only"),
                    opt("A type of antibody"),
                    opt("A complement protein"),
                ),
                "DAMPs are damage-associated molecular patterns from injured host tissue.",
            ),
        ),
        "The complement cascade": (
            q(
                "What kind of system is complement?",
                (
                    opt(
                        "A proteolytic cascade that amplifies as each component cleaves the next",
                        correct=True,
                    ),
                    opt("A single membrane protein"),
                    opt("A type of T-cell receptor"),
                    opt("A DNA repair pathway"),
                ),
                "Complement is an amplifying cascade of ~30 plasma proteins.",
            ),
            q(
                "Which complement function is performed by C3b?",
                (
                    opt("Opsonization: coating microbes for phagocytosis", correct=True),
                    opt("Forming the membrane attack complex alone"),
                    opt("Cleaving DNA"),
                    opt("Presenting antigen on MHC"),
                ),
                "C3b opsonizes targets; C5b-C9 forms the MAC; C3a/C5a are anaphylatoxins.",
            ),
            q(
                "All three complement pathways converge on cleaving which component?",
                (
                    opt("C3", correct=True),
                    opt("IgE"),
                    opt("CD4"),
                    opt("Lysozyme"),
                ),
                "Classical, lectin and alternative pathways all generate a C3 convertase.",
            ),
        ),
        "Adaptive immunity and clonal selection": (
            q(
                "How is the diversity of antigen receptors generated?",
                (
                    opt(
                        "V(D)J recombination shuffles gene segments in each lymphocyte",
                        correct=True,
                    ),
                    opt("Each receptor is copied from a single fixed gene"),
                    opt("Receptors are absorbed from food"),
                    opt("Complement assembles them"),
                ),
                "V(D)J recombination builds a repertoire of ~10^11 distinct receptors.",
            ),
            q(
                "What does clonal selection state?",
                (
                    opt(
                        "Antigen selects and expands the rare pre-existing clones whose receptor fits it",
                        correct=True,
                    ),
                    opt("Antigen creates a brand-new receptor on demand"),
                    opt("All lymphocytes respond to every antigen equally"),
                    opt("Lymphocytes never proliferate"),
                ),
                "Burnet's clonal selection: antigen selects matching clones to expand.",
            ),
            q(
                "Why is a secondary response faster and stronger than a primary one?",
                (
                    opt("Memory clones persist and respond rapidly on re-exposure", correct=True),
                    opt("The pathogen is weaker the second time"),
                    opt("Barriers improve permanently"),
                    opt("Complement is no longer needed"),
                ),
                "Surviving memory lymphocytes give the faster, larger secondary response.",
            ),
        ),
    },
    final=(
        q(
            "Place the layers of defense in the order a pathogen encounters them.",
            (
                opt("Barriers, then innate immunity, then adaptive immunity", correct=True),
                opt("Adaptive, then innate, then barriers"),
                opt("Innate, then barriers, then adaptive"),
                opt("Adaptive and barriers simultaneously, innate never"),
            ),
            "Defense is layered: physical barriers, fast innate, then slow specific adaptive.",
        ),
        q(
            "Which cell bridges innate and adaptive immunity by presenting antigen?",
            (
                opt("The dendritic cell", correct=True),
                opt("The erythrocyte"),
                opt("The platelet"),
                opt("The neutrophil only"),
            ),
            "Dendritic cells are professional antigen-presenting cells that prime T cells.",
        ),
        q(
            "What is the role of the membrane attack complex (C5b-C9)?",
            (
                opt("It punches pores in the target membrane, causing lysis", correct=True),
                opt("It transcribes cytokine genes"),
                opt("It recombines antibody genes"),
                opt("It transports peptides into the ER"),
            ),
            "The MAC lyses pathogens; host cells are protected by CD55/CD59.",
        ),
        q(
            "Which statement about innate immunity is correct?",
            (
                opt("It is fast, germline-encoded and the same on each exposure", correct=True),
                opt("It is slow and improves with memory"),
                opt("It uses V(D)J-recombined receptors"),
                opt("It is unique to vertebrates"),
            ),
            "Innate immunity is rapid, fixed in specificity and evolutionarily ancient.",
        ),
        q(
            "What does opsonization accomplish?",
            (
                opt("It coats a microbe to make it easier for phagocytes to engulf", correct=True),
                opt("It directly synthesizes ATP"),
                opt("It mutates antibody genes"),
                opt("It builds the plasma membrane"),
            ),
            "Opsonins like C3b and antibody tag microbes for phagocytosis.",
        ),
        q(
            "Two features define adaptive immunity. Which pair is correct?",
            (
                opt("Specificity and memory", correct=True),
                opt("Speed and non-specificity"),
                opt("Lysozyme and mucus"),
                opt("Phagocytosis and the respiratory burst"),
            ),
            "Each clone is specific, and surviving memory clones speed up recall responses.",
        ),
    ),
)
