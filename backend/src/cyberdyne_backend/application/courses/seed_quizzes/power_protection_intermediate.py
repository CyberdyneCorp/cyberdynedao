"""Quiz questions for the Power System Protection & Relaying - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Overcurrent protection & inverse-time curves": (
            q(
                "An inverse-time overcurrent relay trips:",
                (
                    opt("faster for larger fault currents", correct=True),
                    opt("slower for larger currents"),
                    opt("at a fixed time always"),
                    opt("never"),
                ),
                "Higher current -> shorter operating time.",
            ),
            q(
                "The pickup setting defines:",
                (
                    opt("the current above which the relay starts timing", correct=True),
                    opt("the trip voltage"),
                    opt("the frequency"),
                    opt("the temperature"),
                ),
                "Threshold to begin operation.",
            ),
            q(
                "Definite-time vs inverse-time relays differ in:",
                (
                    opt("how operating time varies with current", correct=True),
                    opt("color"),
                    opt("cost only"),
                    opt("phase count"),
                ),
                "Definite-time is constant; inverse depends on current.",
            ),
        ),
        "Coordination & discrimination": (
            q(
                "Relay coordination ensures:",
                (
                    opt("the relay nearest the fault trips first", correct=True),
                    opt("all relays trip together"),
                    opt("no relay trips"),
                    opt("random tripping"),
                ),
                "Selectivity via grading.",
            ),
            q(
                "A coordination/grading margin is the:",
                (
                    opt("time gap between successive relays", correct=True),
                    opt("voltage drop"),
                    opt("frequency offset"),
                    opt("cable length"),
                ),
                "Ensures the downstream device acts first.",
            ),
            q(
                "Coordination is shown graphically on:",
                (
                    opt("time-current characteristic curves", correct=True),
                    opt("Bode plots"),
                    opt("Smith charts"),
                    opt("truth tables"),
                ),
                "TCC curves are plotted together.",
            ),
        ),
        "Directional overcurrent protection": (
            q(
                "A directional relay responds to:",
                (
                    opt("fault current in a specific direction", correct=True),
                    opt("magnitude only"),
                    opt("voltage only"),
                    opt("temperature"),
                ),
                "It uses a polarizing reference for direction.",
            ),
            q(
                "Directional protection is needed in:",
                (
                    opt("meshed/parallel networks with multiple sources", correct=True),
                    opt("a single radial feeder only"),
                    opt("DC circuits only"),
                    opt("lighting"),
                ),
                "Direction discrimination prevents mis-trips.",
            ),
            q(
                "Direction is determined by comparing current with a:",
                (
                    opt("reference (polarizing) voltage", correct=True),
                    opt("random signal"),
                    opt("clock only"),
                    opt("the paint"),
                ),
                "Phase relationship gives direction.",
            ),
        ),
        "Differential protection": (
            q(
                "Differential protection compares:",
                (
                    opt("currents entering and leaving a zone", correct=True),
                    opt("two voltages far apart"),
                    opt("frequency and phase"),
                    opt("temperature"),
                ),
                "It trips when in != out (internal fault).",
            ),
            q(
                "Differential protection provides:",
                (
                    opt("fast, selective protection of a defined zone", correct=True),
                    opt("slow backup only"),
                    opt("no selectivity"),
                    opt("grid-wide tripping"),
                ),
                "Inherently selective unit protection.",
            ),
            q(
                "Through-faults can cause mis-operation due to:",
                (
                    opt("CT mismatch/saturation", correct=True),
                    opt("perfect CTs"),
                    opt("no current"),
                    opt("low voltage"),
                ),
                "Restraint/bias guards against this.",
            ),
        ),
        "Per-unit system & short-circuit calculation": (
            q(
                "The per-unit system normalizes quantities to:",
                (
                    opt("chosen base values", correct=True),
                    opt("zero always"),
                    opt("the frequency"),
                    opt("the paint"),
                ),
                "Values expressed as fractions of a base.",
            ),
            q(
                "A benefit of per-unit is that transformer turns ratios:",
                (
                    opt("drop out across voltage levels", correct=True),
                    opt("double"),
                    opt("become nonlinear"),
                    opt("disappear from the data"),
                ),
                "Per-unit simplifies multi-voltage networks.",
            ),
            q(
                "Short-circuit current is found from:",
                (
                    opt("the system impedance to the fault", correct=True),
                    opt("the load impedance only"),
                    opt("the ambient temperature"),
                    opt("the cable color"),
                ),
                "I_sc = V_pu / Z_pu.",
            ),
        ),
        "Symmetrical components for unbalanced faults": (
            q(
                "Symmetrical components decompose unbalanced phasors into:",
                (
                    opt("positive, negative and zero sequences", correct=True),
                    opt("two phases only"),
                    opt("DC and AC"),
                    opt("red/green/blue"),
                ),
                "Three balanced sequence sets.",
            ),
            q(
                "Zero-sequence current is associated with:",
                (
                    opt("ground (earth) faults", correct=True),
                    opt("balanced loads"),
                    opt("three-phase faults only"),
                    opt("no fault"),
                ),
                "Ground faults produce zero-sequence.",
            ),
            q(
                "Symmetrical components make unbalanced analysis:",
                (
                    opt("tractable by using sequence networks", correct=True),
                    opt("impossible"),
                    opt("unnecessary"),
                    opt("slower than direct phase analysis always"),
                ),
                "Sequence networks simplify the math.",
            ),
        ),
    },
    final=(
        q(
            "Inverse-time relay trips:",
            (
                opt("faster at higher current", correct=True),
                opt("slower at higher current"),
                opt("fixed time"),
                opt("never"),
            ),
            "Inverse characteristic.",
        ),
        q(
            "Coordination ensures:",
            (
                opt("nearest relay trips first", correct=True),
                opt("all trip together"),
                opt("none trip"),
                opt("random"),
            ),
            "Selectivity.",
        ),
        q(
            "Directional relays need a:",
            (
                opt("polarizing reference", correct=True),
                opt("random signal"),
                opt("clock only"),
                opt("paint"),
            ),
            "For direction.",
        ),
        q(
            "Differential protection compares:",
            (
                opt("currents in vs out of a zone", correct=True),
                opt("two far voltages"),
                opt("temperature"),
                opt("frequency"),
            ),
            "Unit protection.",
        ),
        q(
            "Per-unit normalizes to:",
            (
                opt("base values", correct=True),
                opt("zero"),
                opt("frequency"),
                opt("color"),
            ),
            "Base-relative.",
        ),
        q(
            "Symmetrical components give:",
            (
                opt("pos/neg/zero sequences", correct=True),
                opt("two phases"),
                opt("DC/AC"),
                opt("colors"),
            ),
            "Sequence decomposition.",
        ),
    ),
)
