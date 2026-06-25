"""Quiz questions for the Power System Protection & Relaying - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Distance (impedance) protection & zones": (
            q(
                "A distance relay measures:",
                (
                    opt("impedance to the fault (V/I)", correct=True),
                    opt("current only"),
                    opt("voltage only"),
                    opt("temperature"),
                ),
                "Impedance is proportional to distance.",
            ),
            q(
                "Distance zones are typically set as:",
                (
                    opt("Zone 1 ~80% instantaneous, Zone 2/3 time-delayed", correct=True),
                    opt("all instantaneous"),
                    opt("all delayed equally"),
                    opt("one zone only"),
                ),
                "Stepped reach for selectivity/backup.",
            ),
            q(
                "Distance protection suits:",
                (
                    opt("transmission lines", correct=True),
                    opt("single appliances"),
                    opt("DC logic"),
                    opt("lighting"),
                ),
                "Common for HV lines.",
            ),
        ),
        "Teleprotection & pilot schemes": (
            q(
                "Teleprotection uses a communication channel to:",
                (
                    opt("coordinate relays at both line ends for fast tripping", correct=True),
                    opt("replace breakers"),
                    opt("measure temperature"),
                    opt("bill customers"),
                ),
                "Permissive/blocking signals speed up clearing.",
            ),
            q(
                "A permissive overreach scheme trips when:",
                (
                    opt("both ends see the fault and exchange permission", correct=True),
                    opt("one end alone decides"),
                    opt("no signal"),
                    opt("the load is high"),
                ),
                "End-to-end confirmation.",
            ),
            q(
                "Pilot schemes improve:",
                (
                    opt("speed of clearing faults along the whole line", correct=True),
                    opt("billing"),
                    opt("efficiency"),
                    opt("color"),
                ),
                "Full-line high-speed protection.",
            ),
        ),
        "Generator, motor & transformer protection": (
            q(
                "Transformer differential protection must account for:",
                (
                    opt("magnetizing inrush current", correct=True),
                    opt("load color"),
                    opt("ambient light"),
                    opt("frequency drift only"),
                ),
                "Harmonic restraint blocks inrush mis-trips.",
            ),
            q(
                "A key generator protection is:",
                (
                    opt("stator differential and loss-of-field", correct=True),
                    opt("speed sensing only"),
                    opt("paint inspection"),
                    opt("none"),
                ),
                "Generators need many specialized elements.",
            ),
            q(
                "Large motors are protected against:",
                (
                    opt("overload, locked-rotor and unbalance", correct=True),
                    opt("only overvoltage"),
                    opt("only color"),
                    opt("nothing"),
                ),
                "Thermal and unbalance protection.",
            ),
        ),
        "Numerical/digital relays & IEC 61850": (
            q(
                "Numerical relays are based on:",
                (
                    opt("microprocessors sampling V and I", correct=True),
                    opt("mechanical discs only"),
                    opt("fuses"),
                    opt("analog meters only"),
                ),
                "DSP-based protection with many functions.",
            ),
            q(
                "IEC 61850 standardizes:",
                (
                    opt("substation communication and data models", correct=True),
                    opt("cable colors"),
                    opt("paint"),
                    opt("billing"),
                ),
                "Interoperable substation automation.",
            ),
            q(
                "A benefit of numerical relays is:",
                (
                    opt("multiple functions, self-monitoring and event records", correct=True),
                    opt("single function only"),
                    opt("no communication"),
                    opt("no settings"),
                ),
                "Rich functionality and diagnostics.",
            ),
        ),
        "Protection with inverter-based renewables": (
            q(
                "Inverter-based resources challenge protection because they:",
                (
                    opt("supply limited, controlled fault current", correct=True),
                    opt("supply huge fault current"),
                    opt("supply none ever"),
                    opt("behave like big machines"),
                ),
                "Low fault-current contribution confuses overcurrent relays.",
            ),
            q(
                "Traditional overcurrent relays may fail with IBRs because:",
                (
                    opt("fault current is barely above load", correct=True),
                    opt("fault current is enormous"),
                    opt("there is no current"),
                    opt("voltage is zero"),
                ),
                "Limited current reduces sensitivity.",
            ),
            q(
                "Adapting protection for IBRs may use:",
                (
                    opt("voltage-based or communication-assisted schemes", correct=True),
                    opt("only fuses"),
                    opt("no protection"),
                    opt("color coding"),
                ),
                "New methods cope with low fault current.",
            ),
        ),
        "Relay-coordination case study": (
            q(
                "A coordination study produces:",
                (
                    opt("relay settings that are selective across the network", correct=True),
                    opt("cable colors"),
                    opt("a billing report"),
                    opt("a paint plan"),
                ),
                "Settings ensuring selectivity.",
            ),
            q(
                "Coordination must balance:",
                (
                    opt("speed against selectivity", correct=True),
                    opt("color against weight"),
                    opt("cost against paint"),
                    opt("nothing"),
                ),
                "Faster vs more selective.",
            ),
            q(
                "Coordination is validated with:",
                (
                    opt("TCC plots and fault simulations", correct=True),
                    opt("guesswork"),
                    opt("a coin flip"),
                    opt("audio tests"),
                ),
                "Curves + fault studies.",
            ),
        ),
    },
    final=(
        q(
            "Distance relays measure:",
            (
                opt("impedance to fault", correct=True),
                opt("current only"),
                opt("voltage only"),
                opt("temperature"),
            ),
            "V/I ~ distance.",
        ),
        q(
            "Teleprotection uses:",
            (
                opt("a comms channel", correct=True),
                opt("fuses"),
                opt("paint"),
                opt("nothing"),
            ),
            "End-to-end signals.",
        ),
        q(
            "Transformer differential handles:",
            (
                opt("inrush via harmonic restraint", correct=True),
                opt("load color"),
                opt("light"),
                opt("nothing"),
            ),
            "Inrush blocking.",
        ),
        q(
            "IEC 61850 standardizes:",
            (
                opt("substation comms/data", correct=True),
                opt("cable color"),
                opt("paint"),
                opt("billing"),
            ),
            "Automation standard.",
        ),
        q(
            "Inverter-based resources give:",
            (
                opt("limited fault current", correct=True),
                opt("huge fault current"),
                opt("none"),
                opt("machine-like current"),
            ),
            "Challenges overcurrent.",
        ),
        q(
            "A coordination study yields:",
            (
                opt("selective relay settings", correct=True),
                opt("colors"),
                opt("billing"),
                opt("paint"),
            ),
            "Selective settings.",
        ),
    ),
)
