"""Quiz questions for the Drug Development, Clinical Trials & Regulatory - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Regulatory pathways and expedited programmes": (
            q(
                "Accelerated Approval allows approval based on:",
                (
                    opt("a surrogate endpoint reasonably likely to predict benefit", correct=True),
                    opt("a single healthy volunteer"),
                    opt("manufacturing cost alone"),
                    opt("patent count"),
                ),
                "Accelerated Approval uses a surrogate, with confirmatory trials required afterward.",
            ),
            q(
                "What happens if a confirmatory trial after Accelerated Approval fails?",
                (
                    opt("the approval can be withdrawn", correct=True),
                    opt("nothing, approval is permanent"),
                    opt("the patent is extended"),
                    opt("the drug becomes a generic automatically"),
                ),
                "Failed confirmatory trials can lead to withdrawal of accelerated approvals.",
            ),
            q(
                "Orphan Drug designation is intended for:",
                (
                    opt("rare diseases, offering incentives and exclusivity", correct=True),
                    opt("the most common chronic diseases"),
                    opt("over-the-counter vitamins"),
                    opt("manufacturing equipment"),
                ),
                "Orphan designation incentivizes development for rare conditions.",
            ),
        ),
        "The CTD/eCTD dossier and global submissions": (
            q(
                "How many modules make up the Common Technical Document?",
                (
                    opt("five", correct=True),
                    opt("two"),
                    opt("ten"),
                    opt("one"),
                ),
                "The CTD has five modules (Module 1 is region-specific).",
            ),
            q(
                "Module 3 of the CTD contains:",
                (
                    opt("quality / CMC information", correct=True),
                    opt("clinical study reports"),
                    opt("regional administrative forms"),
                    opt("the patent application"),
                ),
                "Module 3 covers Chemistry, Manufacturing and Controls (quality).",
            ),
            q(
                "CDISC SDTM and ADaM standards apply to:",
                (
                    opt("structuring clinical data and analysis datasets", correct=True),
                    opt("pricing negotiations"),
                    opt("patent filings"),
                    opt("manufacturing robots"),
                ),
                "SDTM standardizes tabulated data and ADaM the analysis datasets for review.",
            ),
        ),
        "Intellectual property and market exclusivity": (
            q(
                "A standard patent grants protection for about how long from filing?",
                (
                    opt("20 years", correct=True),
                    opt("3 years"),
                    opt("50 years"),
                    opt("forever"),
                ),
                "Patents last roughly 20 years from the filing date.",
            ),
            q(
                "Why is effective patent life at launch much shorter than 20 years?",
                (
                    opt(
                        "much of the term is consumed by the long development process", correct=True
                    ),
                    opt("patents expire the day they are granted"),
                    opt("regulators void all patents"),
                    opt("generics are filed first"),
                ),
                "Filing happens early, so 8-12 years often remain at launch.",
            ),
            q(
                "When small-molecule patents and exclusivity lapse, market entry by:",
                (
                    opt("generics (via bioequivalence) drives prices down", correct=True),
                    opt("more brand competitors only"),
                    opt("nothing changes"),
                    opt("biosimilars of small molecules"),
                ),
                "Generics enter via ANDAs proving bioequivalence, causing the patent cliff.",
            ),
        ),
        "Adaptive, platform and Bayesian trial designs": (
            q(
                "An adaptive design modifies the trial using:",
                (
                    opt("pre-planned interim analyses", correct=True),
                    opt("post-hoc unblinded snooping with no plan"),
                    opt("the marketing team's opinion"),
                    opt("the patent office"),
                ),
                "Adaptations are pre-specified at interim analyses with error control.",
            ),
            q(
                "A platform trial is characterized by:",
                (
                    opt(
                        "a master protocol evaluating multiple treatments, often with a shared control",
                        correct=True,
                    ),
                    opt("a single drug versus placebo only"),
                    opt("no control group"),
                    opt("testing one patient at a time"),
                ),
                "Platform trials use one infrastructure and shared control for many arms.",
            ),
            q(
                "Bayesian trials make decisions by:",
                (
                    opt(
                        "updating a posterior belief about the treatment effect as data accrue",
                        correct=True,
                    ),
                    opt("ignoring all prior information"),
                    opt("fixing a p-value before any data"),
                    opt("counting patents"),
                ),
                "Bayesian designs update the posterior P(theta|data) as evidence accumulates.",
            ),
        ),
        "Pharmacovigilance and signal detection": (
            q(
                "Why is post-marketing surveillance necessary even after large trials?",
                (
                    opt("trials are too small to detect very rare adverse events", correct=True),
                    opt("trials never measure safety"),
                    opt("regulators require nothing after approval"),
                    opt("patents demand it"),
                ),
                "A trial of thousands cannot detect a 1-in-50,000 event; surveillance continues.",
            ),
            q(
                "Disproportionality analysis (e.g. the PRR) looks for:",
                (
                    opt("drug-event pairs reported more often than expected", correct=True),
                    opt("the cheapest manufacturing route"),
                    opt("the longest patent"),
                    opt("the fastest trial"),
                ),
                "PRR flags drug-event combinations that are over-reported, a statistical signal.",
            ),
            q(
                "A confirmed safety signal can lead to:",
                (
                    opt("a label warning, REMS, restricted use, or withdrawal", correct=True),
                    opt("an automatic patent extension"),
                    opt("a guaranteed price increase"),
                    opt("removal of the ethics committee"),
                ),
                "Signals trigger benefit-risk review and risk-mitigation actions.",
            ),
        ),
        "AI and computational methods across development": (
            q(
                "A synthetic control arm in a trial uses:",
                (
                    opt(
                        "external or historical data to substitute for some concurrent controls",
                        correct=True,
                    ),
                    opt("a placebo with no data"),
                    opt("only animal data"),
                    opt("the patent database"),
                ),
                "Synthetic/external controls borrow historical data to reduce concurrent control needs.",
            ),
            q(
                "Which is a documented application of NLP in pharmacovigilance?",
                (
                    opt(
                        "mining case narratives and literature to surface safety signals",
                        correct=True,
                    ),
                    opt("setting the drug price"),
                    opt("manufacturing tablets"),
                    opt("drafting patents only"),
                ),
                "NLP extracts adverse-event signals from text faster than manual review.",
            ),
            q(
                "The hardest challenges for AI in regulated decisions are mainly:",
                (
                    opt("validation, bias, interpretability and reproducibility", correct=True),
                    opt("choosing a logo color"),
                    opt("naming the molecule"),
                    opt("scheduling meetings"),
                ),
                "Models informing dosing/approval must be rigorously qualified, not just accurate.",
            ),
        ),
    },
    final=(
        q(
            "Which programme grants approval on a surrogate endpoint with required confirmation?",
            (
                opt("Accelerated Approval", correct=True),
                opt("Priority Review"),
                opt("Orphan Drug designation"),
                opt("Standard Review"),
            ),
            "Accelerated Approval uses a surrogate and mandates confirmatory trials.",
        ),
        q(
            "Which CTD module holds clinical study reports?",
            (
                opt("Module 5", correct=True),
                opt("Module 1"),
                opt("Module 3"),
                opt("Module 2"),
            ),
            "Module 5 contains the clinical study reports; Module 3 is quality/CMC.",
        ),
        q(
            "The 'patent cliff' refers to:",
            (
                opt(
                    "the sharp revenue drop when exclusivity lapses and generics/biosimilars enter",
                    correct=True,
                ),
                opt("the day a patent is filed"),
                opt("a manufacturing defect"),
                opt("a Phase I dose escalation"),
            ),
            "Loss of exclusivity opens the door to cheaper competitors and a revenue cliff.",
        ),
        q(
            "Response-adaptive randomization tends to:",
            (
                opt("allocate more patients to arms that appear to be winning", correct=True),
                opt("ignore accumulating data"),
                opt("eliminate the control arm always"),
                opt("fix allocation regardless of results"),
            ),
            "It shifts allocation toward better-performing arms as data accrue.",
        ),
        q(
            "The Proportional Reporting Ratio (PRR) is a tool in:",
            (
                opt("pharmacovigilance signal detection", correct=True),
                opt("patent drafting"),
                opt("manufacturing scale-up"),
                opt("dose-response curve fitting"),
            ),
            "PRR is a disproportionality metric for spontaneous-report safety signals.",
        ),
        q(
            "A responsible use of AI in regulated development requires above all:",
            (
                opt("rigorous validation and control of bias and reproducibility", correct=True),
                opt("the largest possible model regardless of evidence"),
                opt("hiding the methods from regulators"),
                opt("skipping clinical trials"),
            ),
            "Models that inform safety or approval must be qualified as carefully as any assay.",
        ),
    ),
)
