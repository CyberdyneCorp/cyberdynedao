"""Quiz questions for the Pharmacology - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Receptor signalling and second messengers": (
            q(
                "Which second messenger does adenylyl cyclase produce?",
                (
                    opt("cAMP", correct=True),
                    opt("IP3"),
                    opt("DAG"),
                    opt("GTP"),
                ),
                "Adenylyl cyclase makes cAMP, which activates PKA.",
            ),
            q(
                "The Gq pathway activates which enzyme?",
                (
                    opt("Phospholipase C", correct=True),
                    opt("Adenylyl cyclase only"),
                    opt("DNA polymerase"),
                    opt("Acetylcholinesterase"),
                ),
                "Gq activates PLC, generating IP3 and DAG.",
            ),
            q(
                "Why can a few occupied receptors drive a large response?",
                (
                    opt("Signalling cascades amplify the signal at each step", correct=True),
                    opt("Receptors never desensitise"),
                    opt("G proteins are infinitely abundant"),
                    opt("The drug binds covalently"),
                ),
                "Cascade amplification (one receptor to many messengers) gives biochemical gain.",
            ),
        ),
        "Receptor theory and spare receptors": (
            q(
                "A receptor reserve causes EC50 to be:",
                (
                    opt("Less than Kd", correct=True),
                    opt("Equal to Kd"),
                    opt("Greater than Kd"),
                    opt("Equal to Emax"),
                ),
                "Spare receptors mean half-maximal effect occurs below half occupancy, so EC50 < Kd.",
            ),
            q(
                "In the operational model, a large transducer ratio tau means:",
                (
                    opt("High efficiency and a large receptor reserve", correct=True),
                    opt("No coupling to a response"),
                    opt("The drug is an antagonist"),
                    opt("The Kd is very large"),
                ),
                "Large tau means efficient transduction and an effect curve far left of binding.",
            ),
            q(
                "What does an irreversible antagonist do first when a reserve is present?",
                (
                    opt("Shift the agonist curve before depressing the maximum", correct=True),
                    opt("Immediately abolish all response"),
                    opt("Increase the maximal response"),
                    opt("Have no effect at all"),
                ),
                "It uses up the reserve first (shifting the curve) then lowers the maximum.",
            ),
        ),
        "One-compartment pharmacokinetics": (
            q(
                "After an IV bolus in a one-compartment model, plasma concentration:",
                (
                    opt("Falls exponentially by first-order elimination", correct=True),
                    opt("Rises linearly forever"),
                    opt("Stays constant"),
                    opt("Falls at a constant absolute rate (zero-order)"),
                ),
                "First-order elimination gives C(t) = C0 e^(-ke t).",
            ),
            q(
                "Half-life relates to the elimination rate constant as:",
                (
                    opt("t1/2 = 0.693 / ke", correct=True),
                    opt("t1/2 = ke / 0.693"),
                    opt("t1/2 = ke * Vd"),
                    opt("t1/2 = Dose / C0"),
                ),
                "Half-life is 0.693/ke (ln 2 over ke).",
            ),
            q(
                "Clearance CL equals:",
                (
                    opt("ke times Vd", correct=True),
                    opt("Vd divided by ke"),
                    opt("Dose times ke"),
                    opt("C0 times t1/2"),
                ),
                "CL = ke * Vd, the volume cleared of drug per unit time.",
            ),
        ),
        "Metabolism and Michaelis-Menten kinetics": (
            q(
                "Which enzyme family carries out most Phase I drug metabolism?",
                (
                    opt("Cytochrome P450", correct=True),
                    opt("DNA ligase"),
                    opt("Na+/K+-ATPase"),
                    opt("Carbonic anhydrase"),
                ),
                "Hepatic cytochrome P450 enzymes dominate Phase I metabolism.",
            ),
            q(
                "In Michaelis-Menten kinetics, Km is:",
                (
                    opt("The substrate concentration at half Vmax", correct=True),
                    opt("The maximal rate"),
                    opt("The total enzyme amount"),
                    opt("The half-life"),
                ),
                "Km is the substrate concentration giving half-maximal rate.",
            ),
            q(
                "When metabolic enzymes saturate at high concentrations, elimination becomes:",
                (
                    opt("Zero-order (constant amount per time)", correct=True),
                    opt("First-order"),
                    opt("Infinitely fast"),
                    opt("Independent of the enzyme"),
                ),
                "Capacity-limited drugs like phenytoin show zero-order kinetics when saturated.",
            ),
        ),
        "Dosing regimens and steady state": (
            q(
                "Steady state during repeated dosing is reached after about:",
                (
                    opt("4 to 5 half-lives", correct=True),
                    opt("Half of one half-life"),
                    opt("100 half-lives"),
                    opt("It is never reached"),
                ),
                "Accumulation plateaus after roughly 4-5 half-lives, independent of dose.",
            ),
            q(
                "Bioavailability F is reduced by:",
                (
                    opt("Incomplete absorption and first-pass metabolism", correct=True),
                    opt("A large volume of distribution only"),
                    opt("A high Hill coefficient"),
                    opt("A long half-life"),
                ),
                "F is the fraction reaching systemic circulation, cut by absorption losses and first-pass.",
            ),
            q(
                "A loading dose is used to:",
                (
                    opt("Reach the target concentration quickly by filling Vd", correct=True),
                    opt("Lower the steady-state level"),
                    opt("Slow down absorption"),
                    opt("Avoid reaching steady state"),
                ),
                "Loading dose = Ctarget * Vd / F fills the volume of distribution at once.",
            ),
        ),
    },
    final=(
        q(
            "PKA is activated by which second messenger?",
            (
                opt("cAMP", correct=True),
                opt("Ca2+ alone"),
                opt("GDP"),
                opt("NAPQI"),
            ),
            "cAMP from adenylyl cyclase activates protein kinase A.",
        ),
        q(
            "Spare receptors explain why:",
            (
                opt("Maximal response can occur below full occupancy", correct=True),
                opt("Drugs never reach their target"),
                opt("Antagonists become agonists"),
                opt("Kd always equals EC50"),
            ),
            "A receptor reserve allows maximal effect at partial occupancy.",
        ),
        q(
            "The maintenance dose rate is set primarily by which PK parameter?",
            (
                opt("Clearance", correct=True),
                opt("Half-life only"),
                opt("Hill coefficient"),
                opt("Bioavailability of zero"),
            ),
            "At steady state, input rate equals CL * Css, so clearance sets the dose.",
        ),
        q(
            "Drugs like phenytoin and ethanol are dangerous near saturation because:",
            (
                opt(
                    "Small dose increases cause disproportionate concentration jumps", correct=True
                ),
                opt("They have an infinite therapeutic index"),
                opt("They are never metabolised"),
                opt("They have no half-life"),
            ),
            "Capacity-limited (zero-order) metabolism makes levels rise steeply.",
        ),
        q(
            "Average steady-state concentration Css is proportional to:",
            (
                opt("F times Dose, divided by CL times the interval", correct=True),
                opt("Vd divided by ke"),
                opt("Emax times EC50"),
                opt("The Hill coefficient"),
            ),
            "Css = F * Dose / (CL * tau).",
        ),
        q(
            "Inhibition of CYP3A4 by grapefruit juice typically causes:",
            (
                opt("Higher drug concentrations and interaction risk", correct=True),
                opt("Faster elimination"),
                opt("Lower bioavailability"),
                opt("No change in metabolism"),
            ),
            "Enzyme inhibition slows metabolism, raising drug levels.",
        ),
    ),
)
