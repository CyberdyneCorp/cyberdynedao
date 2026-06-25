"""Quiz questions for the Smart Grid, HVDC & Power Quality - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Harmonic sources & mitigation": (
            q(
                "A passive harmonic filter is essentially a:",
                (
                    opt("tuned LC trap for a harmonic", correct=True),
                    opt("large resistor"),
                    opt("fuse"),
                    opt("battery"),
                ),
                "Tuned to shunt a specific harmonic.",
            ),
            q(
                "An active power filter mitigates harmonics by:",
                (
                    opt("injecting compensating currents", correct=True),
                    opt("adding capacitors only"),
                    opt("disconnecting the load"),
                    opt("raising voltage"),
                ),
                "It cancels harmonics dynamically.",
            ),
            q(
                "Harmonics are worsened by:",
                (
                    opt("resonance between system L and C", correct=True),
                    opt("pure resistance"),
                    opt("short cables"),
                    opt("DC loads"),
                ),
                "Resonance can amplify harmonics.",
            ),
        ),
        "Voltage regulation, flicker & unbalance": (
            q(
                "Voltage flicker is typically caused by:",
                (
                    opt("fluctuating loads (e.g. arc furnaces)", correct=True),
                    opt("steady loads"),
                    opt("DC offsets"),
                    opt("harmonics only"),
                ),
                "Rapid load changes modulate voltage.",
            ),
            q(
                "Voltage unbalance in three-phase systems causes:",
                (
                    opt("negative-sequence currents and motor heating", correct=True),
                    opt("no effect"),
                    opt("higher efficiency"),
                    opt("DC current"),
                ),
                "Unbalance overheats motors.",
            ),
            q(
                "Voltage is regulated using:",
                (
                    opt("tap-changers, capacitors and regulators", correct=True),
                    opt("paint"),
                    opt("fuses only"),
                    opt("encoders"),
                ),
                "Devices hold voltage within limits.",
            ),
        ),
        "FACTS devices: SVC, STATCOM & UPFC": (
            q(
                "FACTS devices are used to:",
                (
                    opt("control power flow and voltage with power electronics", correct=True),
                    opt("measure temperature"),
                    opt("store data"),
                    opt("replace breakers"),
                ),
                "Flexible AC Transmission Systems.",
            ),
            q(
                "A STATCOM provides:",
                (
                    opt("fast dynamic reactive power support", correct=True),
                    opt("only real power"),
                    opt("DC only"),
                    opt("mechanical switching only"),
                ),
                "Inverter-based VAR control.",
            ),
            q(
                "Compared with an SVC, a STATCOM:",
                (
                    opt("responds faster and works better at low voltage", correct=True),
                    opt("is slower"),
                    opt("cannot control VARs"),
                    opt("is mechanical"),
                ),
                "Voltage-source converter advantages.",
            ),
        ),
        "Distributed generation & microgrids": (
            q(
                "A microgrid can:",
                (
                    opt("operate connected or islanded from the main grid", correct=True),
                    opt("only stay connected"),
                    opt("never island"),
                    opt("only run on coal"),
                ),
                "Islanding capability is a key feature.",
            ),
            q(
                "Distributed generation is located:",
                (
                    opt("near the loads / distribution level", correct=True),
                    opt("only at central plants"),
                    opt("offshore only"),
                    opt("underground only"),
                ),
                "DG is close to consumption.",
            ),
            q(
                "A challenge of high DG penetration is:",
                (
                    opt("reverse power flow and voltage rise", correct=True),
                    opt("lower complexity"),
                    opt("no protection issues"),
                    opt("fixed flow"),
                ),
                "Two-way flow complicates protection/voltage.",
            ),
        ),
        "Grid-scale energy storage": (
            q(
                "Grid storage helps by:",
                (
                    opt("time-shifting energy and smoothing renewables", correct=True),
                    opt("only adding load"),
                    opt("removing inertia"),
                    opt("fixing frequency at zero"),
                ),
                "Stores surplus, supplies at peak.",
            ),
            q(
                "A fast-responding storage technology is:",
                (
                    opt("batteries (BESS)", correct=True),
                    opt("pumped hydro only (slow start)"),
                    opt("coal"),
                    opt("none"),
                ),
                "BESS responds in milliseconds.",
            ),
            q(
                "Storage can provide ancillary services such as:",
                (
                    opt("frequency regulation", correct=True),
                    opt("painting"),
                    opt("metering only"),
                    opt("billing"),
                ),
                "Fast response aids frequency/voltage.",
            ),
        ),
        "SCADA, AMI & grid communications": (
            q(
                "SCADA systems provide:",
                (
                    opt("supervisory monitoring and control of the grid", correct=True),
                    opt("billing only"),
                    opt("paint"),
                    opt("HR records"),
                ),
                "Supervisory Control and Data Acquisition.",
            ),
            q(
                "AMI refers to:",
                (
                    opt("Advanced Metering Infrastructure", correct=True),
                    opt("Analog Meter Interface"),
                    opt("Auto Motor Inverter"),
                    opt("Ambient Monitor Index"),
                ),
                "Smart metering networks.",
            ),
            q(
                "Grid communications increasingly must address:",
                (
                    opt("cybersecurity", correct=True),
                    opt("paint durability"),
                    opt("font choice"),
                    opt("seating"),
                ),
                "Connected grids face cyber risk.",
            ),
        ),
    },
    final=(
        q(
            "A passive harmonic filter is a:",
            (
                opt("tuned LC trap", correct=True),
                opt("resistor"),
                opt("fuse"),
                opt("battery"),
            ),
            "Tuned trap.",
        ),
        q(
            "Flicker is caused by:",
            (
                opt("fluctuating loads", correct=True),
                opt("steady loads"),
                opt("DC"),
                opt("harmonics only"),
            ),
            "Rapid load changes.",
        ),
        q(
            "A STATCOM provides:",
            (
                opt("fast reactive support", correct=True),
                opt("real power only"),
                opt("DC"),
                opt("mechanical switching"),
            ),
            "VAR control.",
        ),
        q(
            "A microgrid can:",
            (
                opt("island", correct=True),
                opt("never island"),
                opt("only stay connected"),
                opt("run on coal only"),
            ),
            "Islanding.",
        ),
        q(
            "Grid batteries provide:",
            (
                opt("fast frequency regulation", correct=True),
                opt("painting"),
                opt("billing"),
                opt("metering only"),
            ),
            "Fast response.",
        ),
        q(
            "AMI means:",
            (
                opt("Advanced Metering Infrastructure", correct=True),
                opt("Analog Meter Interface"),
                opt("Auto Motor Inverter"),
                opt("Ambient Index"),
            ),
            "Smart metering.",
        ),
    ),
)
