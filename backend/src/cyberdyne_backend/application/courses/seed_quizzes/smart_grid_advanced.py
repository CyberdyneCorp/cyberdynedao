"""Quiz questions for the Smart Grid, HVDC & Power Quality - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "HVDC transmission: LCC vs VSC": (
            q(
                "HVDC transmits power as:",
                (
                    opt("direct current via converter stations", correct=True),
                    opt("AC only"),
                    opt("mechanical energy"),
                    opt("light only"),
                ),
                "AC-DC-AC with converters.",
            ),
            q(
                "LCC HVDC uses:",
                (
                    opt("thyristors (line-commutated)", correct=True),
                    opt("IGBTs only"),
                    opt("no semiconductors"),
                    opt("mechanical switches"),
                ),
                "Line-commutated converters use thyristors.",
            ),
            q(
                "VSC HVDC advantages include:",
                (
                    opt("independent P/Q control and black-start capability", correct=True),
                    opt("needing a strong AC grid only"),
                    opt("no control"),
                    opt("higher losses always"),
                ),
                "Voltage-source converters are more flexible.",
            ),
        ),
        "HVDC control & multi-terminal grids": (
            q(
                "In an HVDC link, power flow is set by controlling:",
                (
                    opt("the converter firing/modulation", correct=True),
                    opt("cable color"),
                    opt("ambient temperature"),
                    opt("the paint"),
                ),
                "Converters regulate DC voltage/current.",
            ),
            q(
                "A multi-terminal HVDC grid requires:",
                (
                    opt("coordinated control and DC breakers", correct=True),
                    opt("no control"),
                    opt("AC breakers only"),
                    opt("a single terminal"),
                ),
                "DC grids need fast DC protection.",
            ),
            q(
                "A challenge unique to DC grids is:",
                (
                    opt("interrupting DC fault current (no natural zero crossing)", correct=True),
                    opt("too many zero crossings"),
                    opt("no faults"),
                    opt("low voltage only"),
                ),
                "DC has no current zero to ease breaking.",
            ),
        ),
        "Wide-area monitoring: PMUs, synchrophasors & WAMS": (
            q(
                "A PMU measures:",
                (
                    opt("time-synchronized voltage/current phasors", correct=True),
                    opt("only energy"),
                    opt("temperature"),
                    opt("paint"),
                ),
                "Phasor Measurement Unit with GPS time.",
            ),
            q(
                "Synchrophasors are synchronized using:",
                (
                    opt("GPS time reference", correct=True),
                    opt("local clocks only"),
                    opt("no time base"),
                    opt("manual stopwatches"),
                ),
                "Common time enables wide-area comparison.",
            ),
            q(
                "WAMS enables:",
                (
                    opt("real-time wide-area situational awareness", correct=True),
                    opt("billing only"),
                    opt("painting"),
                    opt("HR"),
                ),
                "Detects oscillations/instability across the grid.",
            ),
        ),
        "Renewable integration & grid stability": (
            q(
                "High inverter-based renewable penetration reduces:",
                (
                    opt("system inertia", correct=True),
                    opt("voltage to zero"),
                    opt("the need for any control"),
                    opt("the grid size"),
                ),
                "Fewer spinning machines -> less inertia.",
            ),
            q(
                "Lower inertia makes the grid more sensitive to:",
                (
                    opt("frequency deviations after disturbances", correct=True),
                    opt("paint"),
                    opt("ambient light"),
                    opt("font size"),
                ),
                "Frequency changes faster (high RoCoF).",
            ),
            q(
                "Grid-forming inverters help by:",
                (
                    opt(
                        "providing voltage/frequency reference and synthetic inertia", correct=True
                    ),
                    opt("only following the grid"),
                    opt("disconnecting"),
                    opt("adding harmonics"),
                ),
                "They emulate machine behavior.",
            ),
        ),
        "Demand-side management, markets & DERMS": (
            q(
                "DERMS manages:",
                (
                    opt("distributed energy resources at scale", correct=True),
                    opt("only central plants"),
                    opt("paint"),
                    opt("HR"),
                ),
                "Distributed Energy Resource Management System.",
            ),
            q(
                "Electricity markets set prices via:",
                (
                    opt("supply-demand bidding/dispatch", correct=True),
                    opt("fixed government-only rates always"),
                    opt("coin flips"),
                    opt("paint cost"),
                ),
                "Wholesale market clearing.",
            ),
            q(
                "Demand-side management can provide:",
                (
                    opt("flexibility as a grid resource", correct=True),
                    opt("only added load"),
                    opt("no value"),
                    opt("fixed demand"),
                ),
                "Flexible demand is a resource.",
            ),
        ),
        "Case study: a smart-grid / power-quality deployment": (
            q(
                "A smart-grid project typically starts by:",
                (
                    opt("assessing needs and defining objectives", correct=True),
                    opt("buying random hardware"),
                    opt("painting"),
                    opt("hiring only"),
                ),
                "Requirements before technology.",
            ),
            q(
                "Power-quality issues are diagnosed with:",
                (
                    opt("monitoring/measurement campaigns", correct=True),
                    opt("guesswork"),
                    opt("paint samples"),
                    opt("surveys only"),
                ),
                "Measure before mitigating.",
            ),
            q(
                "Integrating DER and storage requires:",
                (
                    opt("updated protection and control", correct=True),
                    opt("no changes"),
                    opt("fewer sensors"),
                    opt("only more wires"),
                ),
                "Two-way flow needs new schemes.",
            ),
        ),
    },
    final=(
        q(
            "HVDC transmits as:",
            (
                opt("DC via converters", correct=True),
                opt("AC only"),
                opt("mechanical"),
                opt("light"),
            ),
            "Converter stations.",
        ),
        q(
            "VSC HVDC allows:",
            (
                opt("independent P/Q control", correct=True),
                opt("no control"),
                opt("higher losses only"),
                opt("strong-grid only"),
            ),
            "Flexible.",
        ),
        q(
            "A PMU measures:",
            (
                opt("synchronized phasors", correct=True),
                opt("energy only"),
                opt("temperature"),
                opt("paint"),
            ),
            "GPS-timed phasors.",
        ),
        q(
            "High renewables reduce:",
            (
                opt("system inertia", correct=True),
                opt("grid size"),
                opt("control need"),
                opt("voltage to zero"),
            ),
            "Less inertia.",
        ),
        q(
            "DERMS manages:",
            (
                opt("distributed energy resources", correct=True),
                opt("central plants only"),
                opt("paint"),
                opt("HR"),
            ),
            "DER coordination.",
        ),
        q(
            "Power quality is diagnosed by:",
            (
                opt("measurement campaigns", correct=True),
                opt("guesswork"),
                opt("paint"),
                opt("surveys"),
            ),
            "Measure first.",
        ),
    ),
)
