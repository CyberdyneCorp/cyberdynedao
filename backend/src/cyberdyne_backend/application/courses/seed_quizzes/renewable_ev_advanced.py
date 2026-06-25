"""Quiz questions for the Renewable Energy & EV Powertrains - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Grid-forming vs grid-following inverters": (
            q(
                "A grid-forming inverter:",
                (
                    opt("sets its own voltage and frequency reference", correct=True),
                    opt("needs an existing grid to follow"),
                    opt("cannot operate islanded"),
                    opt("only rectifies"),
                ),
                "It can form/lead the grid.",
            ),
            q(
                "Grid-forming inverters can provide:",
                (
                    opt("synthetic inertia and black start", correct=True),
                    opt("only harmonics"),
                    opt("no services"),
                    opt("DC to loads only"),
                ),
                "They emulate synchronous machines.",
            ),
            q(
                "Grid-following inverters fail when:",
                (
                    opt("the grid voltage is weak or absent", correct=True),
                    opt("the grid is strong"),
                    opt("there is sunlight"),
                    opt("the battery is full"),
                ),
                "They need a stiff grid reference.",
            ),
        ),
        "Hybrid systems & microgrids: sizing & dispatch": (
            q(
                "Sizing a PV+battery microgrid balances:",
                (
                    opt("cost against reliability/autonomy", correct=True),
                    opt("only color"),
                    opt("only weight"),
                    opt("nothing"),
                ),
                "Trade capital cost vs energy security.",
            ),
            q(
                "An energy management system dispatches resources to:",
                (
                    opt("minimize cost while meeting demand", correct=True),
                    opt("maximize cost"),
                    opt("ignore demand"),
                    opt("disconnect loads randomly"),
                ),
                "Optimal dispatch of generation/storage.",
            ),
            q(
                "Hybrid systems often combine PV/wind with:",
                (
                    opt("storage and a backup generator", correct=True),
                    opt("nothing"),
                    opt("only coal"),
                    opt("only the grid"),
                ),
                "Complementary resources improve reliability.",
            ),
        ),
        "Vehicle-to-grid (V2G) & smart charging": (
            q(
                "V2G allows EVs to:",
                (
                    opt("return energy to the grid", correct=True),
                    opt("only consume energy"),
                    opt("never charge"),
                    opt("disconnect permanently"),
                ),
                "Bidirectional power flow.",
            ),
            q(
                "Smart charging primarily:",
                (
                    opt("shifts charging to favorable times", correct=True),
                    opt("always charges at full power"),
                    opt("ignores price"),
                    opt("disables charging"),
                ),
                "Aligns charging with grid/price signals.",
            ),
            q(
                "A concern with V2G is:",
                (
                    opt("added battery cycling/degradation", correct=True),
                    opt("more range always"),
                    opt("no impact"),
                    opt("reduced safety only if painted"),
                ),
                "Extra cycles can age the battery.",
            ),
        ),
        "EV traction motor & drive optimisation": (
            q(
                "An efficiency map shows motor efficiency versus:",
                (
                    opt("torque and speed", correct=True),
                    opt("color and weight"),
                    opt("voltage and paint"),
                    opt("time of day"),
                ),
                "Efficiency varies over the torque-speed plane.",
            ),
            q(
                "Field weakening in EV motors extends:",
                (
                    opt("the high-speed operating range", correct=True),
                    opt("low-speed torque only"),
                    opt("the battery capacity"),
                    opt("the color"),
                ),
                "Enables higher speed above base speed.",
            ),
            q(
                "Wide-bandgap devices (SiC/GaN) improve drives by:",
                (
                    opt("higher efficiency and switching frequency", correct=True),
                    opt("lower efficiency"),
                    opt("mechanical switching"),
                    opt("no benefit"),
                ),
                "SiC/GaN reduce losses and size.",
            ),
        ),
        "Thermal management of batteries & drives": (
            q(
                "Battery thermal management is critical because:",
                (
                    opt("temperature affects life, safety and performance", correct=True),
                    opt("color matters"),
                    opt("it has no effect"),
                    opt("only for looks"),
                ),
                "Heat causes degradation and risk.",
            ),
            q(
                "Thermal runaway is:",
                (
                    opt("a self-sustaining exothermic failure of a cell", correct=True),
                    opt("normal operation"),
                    opt("a charging mode"),
                    opt("a cooling method"),
                ),
                "A dangerous cascading overheating.",
            ),
            q(
                "Power-electronic devices are cooled to:",
                (
                    opt("keep junction temperature within limits", correct=True),
                    opt("increase losses"),
                    opt("change color"),
                    opt("slow switching"),
                ),
                "Junction temperature limits reliability.",
            ),
        ),
        "Case study: renewable + EV integration design": (
            q(
                "Pairing rooftop PV with EV charging benefits from:",
                (
                    opt("aligning charging with solar generation", correct=True),
                    opt("charging only at night always"),
                    opt("ignoring solar"),
                    opt("disconnecting PV"),
                ),
                "Use local clean energy directly.",
            ),
            q(
                "Managing many EVs on a feeder needs:",
                (
                    opt("coordinated/smart charging to avoid overload", correct=True),
                    opt("uncontrolled simultaneous charging"),
                    opt("no management"),
                    opt("fewer meters"),
                ),
                "Avoid exceeding transformer/feeder limits.",
            ),
            q(
                "A combined renewable+EV+storage site is essentially a:",
                (
                    opt("microgrid requiring energy management", correct=True),
                    opt("single appliance"),
                    opt("passive load"),
                    opt("fixed resistor"),
                ),
                "It needs coordinated control.",
            ),
        ),
    },
    final=(
        q(
            "A grid-forming inverter:",
            (
                opt("sets its own V/f reference", correct=True),
                opt("follows the grid"),
                opt("cannot island"),
                opt("only rectifies"),
            ),
            "Forms the grid.",
        ),
        q(
            "Microgrid sizing balances:",
            (
                opt("cost vs reliability", correct=True),
                opt("color"),
                opt("weight"),
                opt("nothing"),
            ),
            "Capital vs autonomy.",
        ),
        q(
            "V2G lets EVs:",
            (
                opt("return energy to the grid", correct=True),
                opt("only consume"),
                opt("never charge"),
                opt("disconnect"),
            ),
            "Bidirectional.",
        ),
        q(
            "An efficiency map plots efficiency vs:",
            (
                opt("torque and speed", correct=True),
                opt("color/weight"),
                opt("voltage/paint"),
                opt("time"),
            ),
            "Torque-speed plane.",
        ),
        q(
            "Thermal runaway is:",
            (
                opt("self-sustaining cell failure", correct=True),
                opt("normal operation"),
                opt("a charge mode"),
                opt("cooling"),
            ),
            "Dangerous overheating.",
        ),
        q(
            "Rooftop PV + EV charging should:",
            (
                opt("align charging with solar", correct=True),
                opt("charge at night only"),
                opt("ignore solar"),
                opt("disconnect PV"),
            ),
            "Use local solar.",
        ),
    ),
)
