"""Quiz questions for the Human Physiology - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Homeostasis and feedback control": (
            q(
                "What does homeostasis describe?",
                (
                    opt(
                        "Active maintenance of a roughly constant internal environment",
                        correct=True,
                    ),
                    opt("The permanent freezing of all body variables"),
                    opt("Random fluctuation of body temperature"),
                    opt("The death of cells under stress"),
                ),
                "Homeostasis keeps regulated variables within narrow bands despite external change.",
            ),
            q(
                "How does negative feedback respond to a deviation from the set point?",
                (
                    opt("It triggers a response that opposes the deviation", correct=True),
                    opt("It amplifies the deviation further"),
                    opt("It ignores the deviation"),
                    opt("It permanently resets the set point"),
                ),
                "Negative feedback returns the variable toward target by opposing the change.",
            ),
            q(
                "Which is an example of positive feedback in physiology?",
                (
                    opt("Oxytocin release during labour", correct=True),
                    opt("Baroreceptor control of blood pressure"),
                    opt("Thermoregulatory sweating"),
                    opt("Insulin lowering blood glucose"),
                ),
                "Positive feedback amplifies and must be ended by an external event, as in labour.",
            ),
        ),
        "The cell membrane and resting potential": (
            q(
                "What does the Na+/K+-ATPase move per ATP hydrolysed?",
                (
                    opt("3 Na+ out and 2 K+ in", correct=True),
                    opt("2 Na+ in and 3 K+ out"),
                    opt("1 Na+ out and 1 K+ in"),
                    opt("Only glucose, no ions"),
                ),
                "The pump exports 3 Na+ and imports 2 K+ per ATP, building the gradients.",
            ),
            q(
                "Why does the resting potential sit close to E_K?",
                (
                    opt("The resting membrane is most permeable to K+", correct=True),
                    opt("There are no K+ channels at rest"),
                    opt("The membrane is most permeable to Ca2+"),
                    opt("Na+ leak dominates at rest"),
                ),
                "K+ leak channels dominate resting permeability, so V_m approaches E_K.",
            ),
            q(
                "Which equation gives the equilibrium potential of a single ion?",
                (
                    opt("The Nernst equation", correct=True),
                    opt("The Starling equation"),
                    opt("The Michaelis-Menten equation"),
                    opt("Poiseuille's law"),
                ),
                "The Nernst equation relates an ion's equilibrium potential to its concentration ratio.",
            ),
        ),
        "Body fluids, osmosis and tonicity": (
            q(
                "Roughly what fraction of total body water is intracellular?",
                (
                    opt("About two thirds", correct=True),
                    opt("About one tenth"),
                    opt("Essentially none"),
                    opt("All of it"),
                ),
                "Of total body water (~60% of mass), about two thirds is intracellular.",
            ),
            q(
                "What happens to a cell placed in a hypotonic solution?",
                (
                    opt("It swells as water enters", correct=True),
                    opt("It shrinks as water leaves"),
                    opt("Its volume stays exactly constant"),
                    opt("It immediately stops all metabolism"),
                ),
                "Hypotonic surroundings drive water in, so the cell swells.",
            ),
            q(
                "What distinguishes tonicity from osmolarity?",
                (
                    opt(
                        "Tonicity counts only solutes that cannot cross the membrane", correct=True
                    ),
                    opt("Tonicity counts every solute particle present"),
                    opt("They are exactly the same quantity"),
                    opt("Tonicity ignores water entirely"),
                ),
                "Only non-penetrating solutes drive net water movement, so they set tonicity.",
            ),
        ),
        "Cell signalling and communication": (
            q(
                "Which signalling mode uses hormones carried in the blood?",
                (
                    opt("Endocrine signalling", correct=True),
                    opt("Synaptic signalling"),
                    opt("Autocrine signalling"),
                    opt("Paracrine signalling"),
                ),
                "Endocrine messengers travel through the bloodstream to distant targets.",
            ),
            q(
                "How do lipid-soluble signals such as steroid hormones act?",
                (
                    opt(
                        "They cross the membrane and bind intracellular receptors that alter transcription",
                        correct=True,
                    ),
                    opt("They open voltage-gated Na+ channels"),
                    opt("They cannot enter any cell"),
                    opt("They act only on extracellular matrix"),
                ),
                "Steroids and thyroid hormone bind intracellular transcription-factor receptors.",
            ),
            q(
                "What second messenger do many GPCRs generate via adenylyl cyclase?",
                (
                    opt("cAMP", correct=True),
                    opt("DNA"),
                    opt("Oxygen"),
                    opt("Glucose"),
                ),
                "Adenylyl cyclase converts ATP to cAMP, which activates protein kinase A.",
            ),
        ),
        "From cells to systems": (
            q(
                "Which ordering of the structural hierarchy is correct?",
                (
                    opt("Cells -> tissues -> organs -> organ systems", correct=True),
                    opt("Organs -> cells -> tissues -> systems"),
                    opt("Tissues -> cells -> systems -> organs"),
                    opt("Systems -> organs -> cells -> tissues"),
                ),
                "Cells build tissues, tissues build organs, organs form systems.",
            ),
            q(
                "Which of the following is one of the four basic tissue types?",
                (
                    opt("Epithelial tissue", correct=True),
                    opt("Plasma membrane"),
                    opt("Mitochondrion"),
                    opt("Nucleotide"),
                ),
                "The four basic tissues are epithelial, connective, muscle and nervous.",
            ),
            q(
                "Which two systems are the body's main fast and slow control systems?",
                (
                    opt("Nervous (fast) and endocrine (slow)", correct=True),
                    opt("Skeletal and integumentary"),
                    opt("Respiratory and digestive"),
                    opt("Lymphatic and reproductive"),
                ),
                "The nervous system signals fast and electrically; the endocrine system slow and chemically.",
            ),
        ),
    },
    final=(
        q(
            "The chief role of negative feedback is to do what?",
            (
                opt("Oppose deviations and restore the set point", correct=True),
                opt("Amplify every disturbance"),
                opt("Eliminate all sensors"),
                opt("Permanently change the regulated variable"),
            ),
            "Negative feedback stabilises regulated variables around their set points.",
        ),
        q(
            "Which pump establishes the Na+ and K+ gradients across the membrane?",
            (
                opt("The Na+/K+-ATPase", correct=True),
                opt("ATP synthase"),
                opt("The ryanodine receptor"),
                opt("Aquaporin"),
            ),
            "The Na+/K+-ATPase actively builds the ion gradients underlying excitability.",
        ),
        q(
            "Approximately what fraction of adult body mass is water?",
            (
                opt("About 60%", correct=True),
                opt("About 5%"),
                opt("About 95%"),
                opt("About 30%"),
            ),
            "Roughly 60% of an adult's mass is water, split into ICF and ECF.",
        ),
        q(
            "Which receptor family signals through cAMP, IP3 and Ca2+ second messengers?",
            (
                opt("G-protein-coupled receptors (GPCRs)", correct=True),
                opt("Voltage-gated Na+ channels"),
                opt("Aquaporins"),
                opt("Histone octamers"),
            ),
            "GPCRs activate enzymes that generate second messengers like cAMP and IP3.",
        ),
        q(
            "Resting membrane potential is closest to the equilibrium potential of which ion?",
            (
                opt("K+", correct=True),
                opt("Ca2+"),
                opt("Cl- only"),
                opt("H+"),
            ),
            "High resting K+ permeability pulls V_m near E_K, about -70 mV in neurons.",
        ),
        q(
            "Which level of organisation sits directly above the organ?",
            (
                opt("The organ system", correct=True),
                opt("The cell"),
                opt("The molecule"),
                opt("The tissue"),
            ),
            "Organs cooperate as organ systems, the level just below the whole organism.",
        ),
    ),
)
