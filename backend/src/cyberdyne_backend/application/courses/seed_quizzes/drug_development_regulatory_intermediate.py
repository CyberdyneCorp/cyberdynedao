"""Quiz questions for the Drug Development, Clinical Trials & Regulatory - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Pharmacokinetics: compartment models and clearance": (
            q(
                "In a one-compartment model after an IV dose, plasma concentration over time:",
                (
                    opt("decays exponentially", correct=True),
                    opt("rises linearly forever"),
                    opt("stays constant"),
                    opt("oscillates sinusoidally"),
                ),
                "First-order elimination gives C(t) = C0 * exp(-ke*t).",
            ),
            q(
                "What does clearance (CL) measure?",
                (
                    opt("the volume of plasma cleared of drug per unit time", correct=True),
                    opt("the total dose administered"),
                    opt("the molecular weight"),
                    opt("the number of doses per day"),
                ),
                "Clearance is the plasma volume cleared per unit time and sets steady-state levels.",
            ),
            q(
                "Total drug exposure (AUC) after a dose equals approximately:",
                (
                    opt("Dose / clearance", correct=True),
                    opt("Dose times half-life squared"),
                    opt("clearance times volume"),
                    opt("dose divided by molecular weight"),
                ),
                "AUC = Dose/CL, the area under the concentration-time curve.",
            ),
        ),
        "PK/PD modeling: linking exposure to effect": (
            q(
                "The Emax model describes effect as a function of:",
                (
                    opt("drug concentration, saturating at Emax", correct=True),
                    opt("time only, ignoring concentration"),
                    opt("patient age only"),
                    opt("the patent term"),
                ),
                "Effect = E0 + Emax*C/(EC50+C), saturating as concentration rises.",
            ),
            q(
                "In the Emax model, EC50 is the concentration that gives:",
                (
                    opt("half of the maximal effect", correct=True),
                    opt("zero effect"),
                    opt("the toxic dose"),
                    opt("the full maximal effect"),
                ),
                "EC50 is where effect reaches half of Emax.",
            ),
            q(
                "Hysteresis between concentration and effect is often modeled with:",
                (
                    opt("an effect compartment", correct=True),
                    opt("a higher patent count"),
                    opt("a larger placebo arm"),
                    opt("removing randomization"),
                ),
                "An effect compartment captures the lag (hysteresis) between plasma level and effect.",
            ),
        ),
        "Controlled trial design: randomization, blinding and controls": (
            q(
                "Why is randomization the key to causal inference in a trial?",
                (
                    opt(
                        "it balances known and unknown confounders across arms on average",
                        correct=True,
                    ),
                    opt("it guarantees a positive result"),
                    opt("it reduces the number of patients to zero"),
                    opt("it removes the need for a control group"),
                ),
                "Random allocation balances confounders, licensing causal claims.",
            ),
            q(
                "What is the purpose of blinding?",
                (
                    opt("to prevent expectation and assessment bias", correct=True),
                    opt("to increase the dose"),
                    opt("to speed up manufacturing"),
                    opt("to extend the patent"),
                ),
                "Blinding hides allocation from patients, clinicians and assessors to reduce bias.",
            ),
            q(
                "In a crossover design, the control for each patient is:",
                (
                    opt("the same patient in the other period", correct=True),
                    opt("a different unrelated patient"),
                    opt("an animal model"),
                    opt("the regulator"),
                ),
                "Crossover trials use each patient as their own control across periods.",
            ),
        ),
        "Endpoints, hypothesis testing and statistical power": (
            q(
                "Statistical power is defined as:",
                (
                    opt("the probability of detecting a true effect (1 - beta)", correct=True),
                    opt("the probability of a false positive"),
                    opt("the p-value threshold"),
                    opt("the sample size itself"),
                ),
                "Power = 1 - beta, the chance of detecting a real effect; alpha is the false-positive rate.",
            ),
            q(
                "A Type I error is:",
                (
                    opt("rejecting a true null hypothesis (false positive)", correct=True),
                    opt("failing to reject a false null (false negative)"),
                    opt("a manufacturing defect"),
                    opt("an unblinding event"),
                ),
                "Type I error is a false positive, controlled by alpha (often 0.05).",
            ),
            q(
                "To detect a smaller treatment effect, the required sample size:",
                (
                    opt("increases (roughly as 1/effect^2)", correct=True),
                    opt("decreases"),
                    opt("stays the same"),
                    opt("becomes zero"),
                ),
                "Smaller effects need more patients; n scales roughly with 1/effect^2.",
            ),
        ),
        "Survival analysis and time-to-event endpoints": (
            q(
                "A patient who leaves the study event-free before it ends is:",
                (
                    opt("censored", correct=True),
                    opt("randomized"),
                    opt("a Type I error"),
                    opt("an agonist"),
                ),
                "Censoring means we know only that the event time exceeds the observed time.",
            ),
            q(
                "The Kaplan-Meier method estimates:",
                (
                    opt("the survival function S(t)", correct=True),
                    opt("the molecular weight"),
                    opt("the patent term"),
                    opt("the manufacturing yield"),
                ),
                "Kaplan-Meier gives a nonparametric step estimate of S(t) = P(T > t).",
            ),
            q(
                "A hazard ratio of 0.7 from a Cox model means the treatment:",
                (
                    opt("reduces the instantaneous event rate by about 30%", correct=True),
                    opt("increases risk by 70%"),
                    opt("has no effect"),
                    opt("doubles the hazard"),
                ),
                "HR < 1 lowers risk; HR = 0.7 is a 30% hazard reduction.",
            ),
        ),
        "GxP quality systems and research ethics": (
            q(
                "Which standard governs the conduct of clinical trials?",
                (
                    opt("Good Clinical Practice (GCP), ICH E6", correct=True),
                    opt("Good Laboratory Practice (GLP)"),
                    opt("Good Manufacturing Practice (GMP)"),
                    opt("ISO 27001"),
                ),
                "GCP (ICH E6) governs clinical conduct; GLP is preclinical, GMP manufacturing.",
            ),
            q(
                "The ALCOA principle concerns:",
                (
                    opt(
                        "data integrity (attributable, legible, contemporaneous, original, accurate)",
                        correct=True,
                    ),
                    opt("dose escalation rules"),
                    opt("patent strategy"),
                    opt("pricing"),
                ),
                "ALCOA summarizes the qualities of trustworthy records.",
            ),
            q(
                "What independent body must review and approve a trial's ethics before it starts?",
                (
                    opt("an IRB / Ethics Committee", correct=True),
                    opt("the marketing department"),
                    opt("the patent office"),
                    opt("the data vendor"),
                ),
                "An IRB/Ethics Committee independently reviews the trial for subject protection.",
            ),
        ),
    },
    final=(
        q(
            "Half-life relates to the elimination rate constant by:",
            (
                opt("t_half = ln(2) / ke", correct=True),
                opt("t_half = ke / ln(2)"),
                opt("t_half = ke squared"),
                opt("t_half = dose * ke"),
            ),
            "Half-life is ln(2)/ke for first-order elimination.",
        ),
        q(
            "The Emax model saturates because:",
            (
                opt("there is a finite maximum effect once targets are engaged", correct=True),
                opt("the dose cannot be measured"),
                opt("clearance is infinite"),
                opt("the trial is unblinded"),
            ),
            "Effect plateaus at Emax as concentration rises.",
        ),
        q(
            "Which design feature most directly enables causal conclusions?",
            (
                opt("randomization", correct=True),
                opt("a larger patent estate"),
                opt("a faster manufacturing line"),
                opt("a surrogate endpoint"),
            ),
            "Randomization balances confounders, the basis for causal inference.",
        ),
        q(
            "Intention-to-treat analysis means:",
            (
                opt("analyze patients in the group they were randomized to", correct=True),
                opt("analyze only patients who completed treatment"),
                opt("exclude all dropouts"),
                opt("analyze only the control arm"),
            ),
            "ITT preserves randomization by keeping patients in their assigned groups.",
        ),
        q(
            "The log-rank test is used to:",
            (
                opt("compare survival curves between arms", correct=True),
                opt("estimate molecular weight"),
                opt("set the patent term"),
                opt("measure bioavailability"),
            ),
            "The log-rank test compares time-to-event distributions across groups.",
        ),
        q(
            "A Data Safety Monitoring Board can:",
            (
                opt("stop a trial early for harm or overwhelming benefit", correct=True),
                opt("set the drug's price"),
                opt("write the marketing copy"),
                opt("file the patent"),
            ),
            "The DSMB independently watches safety data and can recommend stopping.",
        ),
    ),
)
