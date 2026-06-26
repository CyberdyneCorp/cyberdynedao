"""Quiz questions for the Human Physiology - Advanced course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Endocrine feedback and enzyme kinetics": (
            q(
                "In the HPA axis, cortisol regulates its own secretion how?",
                (
                    opt("By negative feedback onto the hypothalamus and pituitary", correct=True),
                    opt("By positive feedback that keeps raising CRH"),
                    opt("By having no effect upstream"),
                    opt("By permanently destroying the pituitary"),
                ),
                "Cortisol suppresses both CRH and ACTH, closing the negative-feedback loop.",
            ),
            q(
                "What does the Michaelis constant K_m represent?",
                (
                    opt(
                        "The substrate concentration giving half-maximal reaction velocity",
                        correct=True,
                    ),
                    opt("The maximum possible velocity"),
                    opt("The total amount of enzyme"),
                    opt("The concentration that fully inhibits the enzyme"),
                ),
                "K_m is the substrate level at which v equals half of Vmax.",
            ),
            q(
                "A competitive inhibitor of an enzyme typically does what to apparent K_m?",
                (
                    opt("Raises it", correct=True),
                    opt("Lowers it to zero"),
                    opt("Has no effect on it"),
                    opt("Makes velocity negative"),
                ),
                "Competitive inhibitors increase the apparent K_m without changing Vmax.",
            ),
        ),
        "Integrative glucose and energy regulation": (
            q(
                "How do pancreatic beta-cells initiate insulin secretion when glucose rises?",
                (
                    opt(
                        "Glucose metabolism raises ATP, closing K_ATP channels and allowing Ca2+ entry",
                        correct=True,
                    ),
                    opt("Glucose directly binds DNA"),
                    opt("Glucose opens voltage-gated Na+ channels in neurons"),
                    opt("Glucose blocks all calcium entry"),
                ),
                "ATP from glucose closes K_ATP channels, depolarising the cell and admitting Ca2+.",
            ),
            q(
                "Why is glucose-stimulated insulin secretion described by a Hill function with n>1?",
                (
                    opt(
                        "The response is cooperative, giving a sharp sigmoidal threshold",
                        correct=True,
                    ),
                    opt("The response is perfectly linear"),
                    opt("Insulin falls as glucose rises"),
                    opt("There is no threshold at all"),
                ),
                "A Hill coefficient above 1 sharpens the threshold of the secretion curve.",
            ),
            q(
                "Which best characterises type 2 diabetes?",
                (
                    opt("Insulin resistance combined with beta-cell failure", correct=True),
                    opt("Complete absence of insulin receptors from birth"),
                    opt("Excessive sensitivity to insulin"),
                    opt("A pure problem of red blood cells"),
                ),
                "Type 2 diabetes pairs reduced insulin sensitivity with declining beta-cell output.",
            ),
        ),
        "The immune response": (
            q(
                "Which feature distinguishes adaptive from innate immunity?",
                (
                    opt("Specificity and immunological memory", correct=True),
                    opt("It is faster and germline-encoded"),
                    opt("It relies only on physical barriers"),
                    opt("It cannot recognise any antigen"),
                ),
                "Adaptive immunity is slower but specific and remembering, unlike innate defence.",
            ),
            q(
                "What do innate pattern-recognition receptors such as TLRs detect?",
                (
                    opt("Conserved microbial molecular motifs", correct=True),
                    opt("Self DNA exclusively"),
                    opt("Only the host's own proteins"),
                    opt("Plasma glucose levels"),
                ),
                "TLRs recognise conserved pathogen-associated patterns to launch inflammation.",
            ),
            q(
                "Why is a secondary immune response faster and stronger than the first?",
                (
                    opt("Memory B and T cells persist from the primary response", correct=True),
                    opt("The pathogen becomes weaker over time"),
                    opt("Antibodies are made without any cells"),
                    opt("Innate immunity is permanently disabled"),
                ),
                "Memory cells enable a rapid, larger, higher-affinity response on re-exposure.",
            ),
        ),
        "Receptor pharmacology and dose–response": (
            q(
                "What does EC50 measure?",
                (
                    opt("The concentration producing half-maximal effect (potency)", correct=True),
                    opt("The maximum effect a drug can produce"),
                    opt("The lethal dose in all patients"),
                    opt("The molecular weight of the drug"),
                ),
                "EC50 indexes potency: the dose at which effect is half of maximal.",
            ),
            q(
                "How does a competitive antagonist alter the agonist dose-response curve?",
                (
                    opt("Shifts it rightward without lowering the maximum", correct=True),
                    opt("Lowers the maximum without shifting it"),
                    opt("Has no effect at all"),
                    opt("Converts the agonist into a full agonist"),
                ),
                "Competitive antagonism raises apparent EC50 but the maximum is still reachable.",
            ),
            q(
                "A partial agonist differs from a full agonist in that it has lower what?",
                (
                    opt("Efficacy (maximal achievable effect)", correct=True),
                    opt("Molecular weight only"),
                    opt("Affinity, always"),
                    opt("Number of atoms"),
                ),
                "A partial agonist produces a submaximal effect even when fully bound.",
            ),
        ),
        "Pharmacokinetics and clearance": (
            q(
                "After an IV bolus, a one-compartment drug's plasma concentration falls how?",
                (
                    opt("Exponentially, by first-order kinetics", correct=True),
                    opt("Linearly to zero immediately"),
                    opt("It rises indefinitely"),
                    opt("It stays perfectly constant"),
                ),
                "First-order elimination gives C(t) = C0 * exp(-ke*t).",
            ),
            q(
                "Which parameter sets the maintenance dose rate at a target steady-state level?",
                (
                    opt("Clearance (Dose rate = CL x Css)", correct=True),
                    opt("Volume of distribution alone"),
                    opt("Half-life alone"),
                    opt("Heart rate"),
                ),
                "Maintenance dose rate equals clearance times the target steady-state concentration.",
            ),
            q(
                "About how many half-lives are needed to reach steady state on repeated dosing?",
                (
                    opt("Roughly 4 to 5", correct=True),
                    opt("Exactly 1"),
                    opt("More than 50"),
                    opt("Steady state is never reached"),
                ),
                "Plasma levels plateau after about 4-5 half-lives of repeated dosing.",
            ),
        ),
        "Computational and AI methods in physiology": (
            q(
                "What does a PBPK model represent?",
                (
                    opt(
                        "Physiologically based compartments linked by organ blood flows to predict drug exposure",
                        correct=True,
                    ),
                    opt("A purely random number generator"),
                    opt("A static anatomical drawing only"),
                    opt("A model with no physiological basis"),
                ),
                "PBPK chains organ compartments with blood flows to predict pharmacokinetics.",
            ),
            q(
                "What is a physiological 'digital twin'?",
                (
                    opt(
                        "A mechanistic model personalised to an individual patient's data",
                        correct=True,
                    ),
                    opt("An identical sibling of the patient"),
                    opt("A backup copy of an ECG file"),
                    opt("A purely cosmetic 3D avatar"),
                ),
                "A digital twin calibrates a mechanistic model to one patient for prediction.",
            ),
            q(
                "Which is a documented clinical use of machine learning on physiological signals?",
                (
                    opt(
                        "Detecting arrhythmias and estimating ejection fraction from the ECG",
                        correct=True,
                    ),
                    opt("Replacing the need for any validation"),
                    opt("Eliminating uncertainty entirely"),
                    opt("Proving cells are not made of molecules"),
                ),
                "Deep networks read ECGs to detect arrhythmias and estimate ejection fraction.",
            ),
        ),
    },
    final=(
        q(
            "The HPA axis is an example of which control architecture?",
            (
                opt("A hierarchical negative-feedback axis", correct=True),
                opt("Pure positive feedback"),
                opt("An open loop with no feedback"),
                opt("A purely mechanical lever"),
            ),
            "CRH -> ACTH -> cortisol, with cortisol suppressing the upstream steps.",
        ),
        q(
            "In Michaelis-Menten kinetics, Vmax is reached when what is true?",
            (
                opt("The enzyme is saturated with substrate", correct=True),
                opt("Substrate concentration is zero"),
                opt("The inhibitor concentration is maximal"),
                opt("Temperature is absolute zero"),
            ),
            "At saturating substrate, velocity approaches Vmax.",
        ),
        q(
            "Cooperative, sigmoidal physiological responses are well described by which function?",
            (
                opt("The Hill equation", correct=True),
                opt("Poiseuille's law"),
                opt("The Nernst equation"),
                opt("Ohm's law"),
            ),
            "The Hill equation with n>1 captures cooperative sigmoidal behaviour.",
        ),
        q(
            "Immunological memory is the physiological basis of what intervention?",
            (
                opt("Vaccination", correct=True),
                opt("Dialysis"),
                opt("Defibrillation"),
                opt("Blood typing"),
            ),
            "Memory cells let vaccines prime a fast, strong response on later exposure.",
        ),
        q(
            "A drug's half-life relates to its elimination rate constant by which formula?",
            (
                opt("t_half = ln 2 / ke", correct=True),
                opt("t_half = ke / ln 2"),
                opt("t_half = ke squared"),
                opt("t_half = 1 - ke"),
            ),
            "For first-order elimination, t_half equals ln 2 divided by ke.",
        ),
        q(
            "Which describes a physics-informed neural network in physiology?",
            (
                opt(
                    "A model blending mechanistic equations with data-driven learning", correct=True
                ),
                opt("A network that ignores all physical laws"),
                opt("A purely analog electronic circuit"),
                opt("A spreadsheet with no model"),
            ),
            "Physics-informed neural networks combine governing equations with learned components.",
        ),
    ),
)
