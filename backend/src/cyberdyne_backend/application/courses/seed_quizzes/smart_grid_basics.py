"""Quiz questions for the Smart Grid, HVDC & Power Quality - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The power grid today & the smart-grid vision": (
            q(
                "The traditional grid flows power:",
                (
                    opt("one way from central plants to loads", correct=True),
                    opt("always two-way"),
                    opt("only locally"),
                    opt("backwards"),
                ),
                "Centralized one-directional flow.",
            ),
            q(
                "The smart grid adds:",
                (
                    opt("two-way power and information flow", correct=True),
                    opt("fewer sensors"),
                    opt("no communication"),
                    opt("only more wires"),
                ),
                "Digital, bidirectional, sensor-rich.",
            ),
            q(
                "A driver of the smart grid is:",
                (
                    opt("integrating distributed/renewable generation", correct=True),
                    opt("reducing all monitoring"),
                    opt("removing meters"),
                    opt("fixing voltage at zero"),
                ),
                "DER integration needs a smarter grid.",
            ),
        ),
        "Power-quality fundamentals: sags, swells & interruptions": (
            q(
                "A voltage sag is a:",
                (
                    opt("short-duration drop in RMS voltage", correct=True),
                    opt("permanent increase"),
                    opt("frequency change"),
                    opt("DC offset"),
                ),
                "Brief undervoltage, often from faults/motor starts.",
            ),
            q(
                "A voltage swell is a:",
                (
                    opt("short-duration rise in RMS voltage", correct=True),
                    opt("permanent drop"),
                    opt("harmonic"),
                    opt("interruption"),
                ),
                "Brief overvoltage.",
            ),
            q(
                "An interruption is:",
                (
                    opt("a complete loss of voltage for a period", correct=True),
                    opt("a small ripple"),
                    opt("a harmonic"),
                    opt("a phase shift"),
                ),
                "Voltage essentially zero.",
            ),
        ),
        "Harmonics & total harmonic distortion": (
            q(
                "Harmonics are:",
                (
                    opt("integer-multiple frequency components of the fundamental", correct=True),
                    opt("DC offsets"),
                    opt("random noise only"),
                    opt("phase shifts only"),
                ),
                "Multiples of 50/60 Hz.",
            ),
            q(
                "THD measures:",
                (
                    opt("the distortion relative to the fundamental", correct=True),
                    opt("the average voltage"),
                    opt("the frequency"),
                    opt("the power factor only"),
                ),
                "Ratio of harmonic content to fundamental.",
            ),
            q(
                "A major source of harmonics is:",
                (
                    opt("nonlinear loads (power electronics)", correct=True),
                    opt("pure resistors"),
                    opt("incandescent bulbs only"),
                    opt("open circuits"),
                ),
                "Rectifiers/drives inject harmonics.",
            ),
        ),
        "Reactive power & power-factor correction": (
            q(
                "Reactive power is associated with:",
                (
                    opt("energy storage in inductance/capacitance", correct=True),
                    opt("resistive heating only"),
                    opt("DC only"),
                    opt("harmonics only"),
                ),
                "Exchanged, not consumed, by L and C.",
            ),
            q(
                "Power-factor correction commonly adds:",
                (
                    opt("capacitors to offset inductive load", correct=True),
                    opt("more inductors"),
                    opt("resistors"),
                    opt("fuses"),
                ),
                "Capacitors supply reactive power locally.",
            ),
            q(
                "A low power factor causes:",
                (
                    opt("higher current and losses for the same real power", correct=True),
                    opt("lower current"),
                    opt("no effect"),
                    opt("higher frequency"),
                ),
                "More current is drawn, raising losses.",
            ),
        ),
        "Smart metering & demand response": (
            q(
                "A smart meter provides:",
                (
                    opt("two-way, interval consumption data", correct=True),
                    opt("one annual reading only"),
                    opt("no data"),
                    opt("voltage only"),
                ),
                "Detailed, communicating metering.",
            ),
            q(
                "Demand response aims to:",
                (
                    opt("shift/reduce load at peak times", correct=True),
                    opt("always increase load"),
                    opt("ignore price"),
                    opt("disconnect everyone"),
                ),
                "Adjust demand to grid conditions/price.",
            ),
            q(
                "Demand response benefits the grid by:",
                (
                    opt("reducing peak stress and cost", correct=True),
                    opt("raising peaks"),
                    opt("removing meters"),
                    opt("fixing frequency at zero"),
                ),
                "Flattens the load curve.",
            ),
        ),
        "Grid codes & interconnection basics": (
            q(
                "Grid codes specify:",
                (
                    opt("technical rules for connecting to the grid", correct=True),
                    opt("cable colors"),
                    opt("billing rates only"),
                    opt("paint"),
                ),
                "Connection/operation requirements.",
            ),
            q(
                "A modern grid-code requirement for renewables is:",
                (
                    opt("fault ride-through", correct=True),
                    opt("disconnection at any disturbance"),
                    opt("no monitoring"),
                    opt("fixed output only"),
                ),
                "Stay connected through disturbances.",
            ),
            q(
                "Interconnection studies assess:",
                (
                    opt("impact of a new generator on the grid", correct=True),
                    opt("the paint"),
                    opt("the building height"),
                    opt("the staff size"),
                ),
                "Ensure safe, stable connection.",
            ),
        ),
    },
    final=(
        q(
            "Traditional grid flow is:",
            (
                opt("one-way", correct=True),
                opt("two-way"),
                opt("local only"),
                opt("backwards"),
            ),
            "Centralized.",
        ),
        q(
            "A voltage sag is:",
            (
                opt("a short RMS drop", correct=True),
                opt("a rise"),
                opt("a harmonic"),
                opt("DC"),
            ),
            "Brief undervoltage.",
        ),
        q(
            "THD measures:",
            (
                opt("harmonic distortion vs fundamental", correct=True),
                opt("average voltage"),
                opt("frequency"),
                opt("PF only"),
            ),
            "Distortion ratio.",
        ),
        q(
            "PF correction adds:",
            (
                opt("capacitors", correct=True),
                opt("inductors"),
                opt("resistors"),
                opt("fuses"),
            ),
            "Offset inductive load.",
        ),
        q(
            "Demand response aims to:",
            (
                opt("shift/reduce peak load", correct=True),
                opt("increase load"),
                opt("ignore price"),
                opt("disconnect all"),
            ),
            "Flatten demand.",
        ),
        q(
            "Grid codes specify:",
            (
                opt("connection rules", correct=True),
                opt("cable color"),
                opt("billing"),
                opt("paint"),
            ),
            "Technical requirements.",
        ),
    ),
)
