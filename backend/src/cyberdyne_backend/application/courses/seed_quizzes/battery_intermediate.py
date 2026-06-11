from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The battery management system": (
            q(
                "What is the primary role of the analog front-end (AFE) in a BMS?",
                (
                    opt("Compute SoC and SoH from the cell model"),
                    opt(
                        "Measure each series cell voltage, pack current, and temperatures",
                        correct=True,
                    ),
                    opt("Transfer charge between cells during balancing"),
                    opt("Report pack status to the charger over CAN"),
                ),
                "The AFE is the measurement chip set that reads series cell voltages to "
                "millivolt accuracy, pack current, and temperatures.",
            ),
            q(
                "The safe operating area (SOA) that the BMS enforces is a box defined in which dimensions?",
                (
                    opt("Voltage, current, and temperature", correct=True),
                    opt("State of charge, state of health, and age"),
                    opt("Voltage, capacity, and resistance"),
                    opt("Current, energy, and cell count"),
                ),
                "The SOA bounds each cell in voltage, current, and temperature; crossing a "
                "limit makes the BMS warn, derate, or open the contactors.",
            ),
            q(
                "According to the lesson, the BMS is best described as which kind of system first?",
                (
                    opt("A communication gateway"),
                    opt("A fuel gauge"),
                    opt("A safety system that disconnects when in doubt", correct=True),
                    opt("A balancing controller"),
                ),
                "The practical insight states the BMS is a safety system first and a fuel "
                "gauge second; when in doubt it disconnects.",
            ),
        ),
        "State-of-charge estimation": (
            q(
                "Why does coulomb counting drift over time?",
                (
                    opt(
                        "Any current-sensor bias accumulates forever as it integrates",
                        correct=True,
                    ),
                    opt("The open-circuit voltage curve is too flat"),
                    opt("It requires the cell to rest for several minutes"),
                    opt("It cannot be combined with a Kalman filter"),
                ),
                "Coulomb counting integrates current, so any sensor bias accumulates "
                "forever and it also needs a correct starting point and capacity.",
            ),
            q(
                "What is the main limitation of OCV lookup for SoC estimation?",
                (
                    opt("It accumulates current-sensor bias over time"),
                    opt(
                        "It is only valid at rest and useless on the flat part of an LFP curve",
                        correct=True,
                    ),
                    opt("It cannot give an absolute SoC reading"),
                    opt("It requires a full equivalent-circuit model"),
                ),
                "OCV lookup is drift-free and absolute but only valid at rest, and a "
                "millivolt of error is a big chunk of SoC on the flat LFP plateau.",
            ),
            q(
                "How does a Kalman filter improve SoC estimation?",
                (
                    opt("It replaces coulomb counting with pure OCV lookup"),
                    opt("It measures SoC directly from the cell terminals"),
                    opt(
                        "It blends coulomb counting with OCV anchoring, correcting when measured "
                        "voltage disagrees with the model",
                        correct=True,
                    ),
                    opt("It eliminates the need for a current sensor"),
                ),
                "The Kalman filter runs the cell model, predicts voltage from coulomb-counted "
                "SoC, and corrects whenever the measured terminal voltage disagrees.",
            ),
        ),
        "State of health & aging": (
            q(
                "How is capacity-based state of health (SoH) defined?",
                (
                    opt("R_new divided by R_now, as a percentage"),
                    opt("Q_now divided by Q_new, as a percentage", correct=True),
                    opt("Q_new divided by Q_now, as a percentage"),
                    opt("R_now divided by R_new, as a percentage"),
                ),
                "Capacity SoH is Q_now / Q_new x 100 percent, tracking how the usable Ah "
                "shrinks relative to a new cell.",
            ),
            q(
                "What distinguishes calendar aging from cycle aging?",
                (
                    opt("Calendar aging is wear just from time, even when idle", correct=True),
                    opt("Calendar aging is wear per charge-discharge cycle"),
                    opt("Calendar aging only happens at low temperature"),
                    opt("Calendar aging is caused by lithium plating during cycling"),
                ),
                "Calendar aging is wear from time alone, even idle, worsened by high "
                "temperature and high SoC; cycle aging is wear per charge-discharge cycle.",
            ),
            q(
                "What is the rough rule about temperature and cell life given in the lesson?",
                (
                    opt("Life roughly doubles for every 10 C rise"),
                    opt("Life roughly halves for every 10 C rise", correct=True),
                    opt("Life is independent of temperature"),
                    opt("Life roughly halves for every 1 C rise"),
                ),
                "Both aging modes accelerate sharply with temperature, with a rough rule "
                "that life roughly halves for every 10 C rise.",
            ),
        ),
        "Cell balancing: passive vs active": (
            q(
                "Why does an unbalanced series pack waste capacity?",
                (
                    opt(
                        "The weakest cell hits its limit first, ending charge or discharge early",
                        correct=True,
                    ),
                    opt("Parallel cells fail to self-balance"),
                    opt("The AFE cannot measure mismatched cells"),
                    opt("The strongest cell forces the others to over-charge"),
                ),
                "Series cells share the same current, so the weakest cell decides when "
                "charging and discharging stop, wasting the rest of the pack capacity.",
            ),
            q(
                "How does passive balancing work?",
                (
                    opt("It transfers charge from full cells to empty ones"),
                    opt(
                        "It burns off excess from the fullest cells as heat through a resistor",
                        correct=True,
                    ),
                    opt("It cools the hottest cells to slow their aging"),
                    opt("It increases the capacity of the weakest cell"),
                ),
                "Passive balancing turns on a resistor across the fullest cells, burning off "
                "their excess as heat until the laggards catch up.",
            ),
            q(
                "What is a key advantage of active balancing over passive balancing?",
                (
                    opt("It is simpler and cheaper to build"),
                    opt("It can increase a worn cell's capacity"),
                    opt(
                        "It transfers charge instead of burning it, so it is far more efficient and "
                        "works while discharging",
                        correct=True,
                    ),
                    opt("It only equalises during charge"),
                ),
                "Active balancing moves charge between cells with capacitors, inductors, or "
                "DC-DC converters, making it more efficient and usable while discharging.",
            ),
        ),
        "Pack design: series, parallel & thermal": (
            q(
                "In xSyP notation, what does adding cells in series do?",
                (
                    opt("Voltages add while capacity stays the same", correct=True),
                    opt("Capacities add while voltage stays the same"),
                    opt("Both voltage and capacity stay the same"),
                    opt("Voltage stays the same while capacity falls"),
                ),
                "Series adds voltage (V_pack = N_s x V_cell) with capacity unchanged; "
                "parallel adds capacity (Q_pack = N_p x Q_cell) with voltage unchanged.",
            ),
            q(
                "What temperature band do lithium cells prefer, per the lesson?",
                (
                    opt("0 to 10 C"),
                    opt("15 to 35 C", correct=True),
                    opt("40 to 60 C"),
                    opt("-20 to 0 C"),
                ),
                "Cells like 15 to 35 C: too cold and resistance soars and charging plates "
                "lithium; too hot and they age fast and risk runaway.",
            ),
            q(
                "How does the heat generated per cell scale with current?",
                (
                    opt("Linearly, as P = I times R_0"),
                    opt("As the square of current, P = I squared times R_0", correct=True),
                    opt("Inversely with current"),
                    opt("It does not depend on current"),
                ),
                "Heat generated is P = I^2 R_0 per cell, so high C-rate and high resistance "
                "both push the cooling requirement up.",
            ),
        ),
        "Lab: coulomb-counting SoC & cell balancing": (
            q(
                "In simulation (A), what causes the estimated SoC to drift from the true SoC?",
                (
                    opt("A 50 mA current-sensor bias added to the estimator only", correct=True),
                    opt("An incorrect cell capacity Q_Ah"),
                    opt("A wrong initial SoC of 0.90"),
                    opt("The 1 second time step being too large"),
                ),
                "Part (A) adds a 50 mA bias to the measured current used only by the "
                "estimator, so the coulomb-counted estimate drifts from the true SoC.",
            ),
            q(
                "In simulation (B), which cells does the passive-balancing loop bleed?",
                (
                    opt("All four cells equally"),
                    opt("Only cells above the running average voltage", correct=True),
                    opt("Only the single lowest cell"),
                    opt("Cells below the average voltage"),
                ),
                "Part (B) computes over = max(vcells - vavg, 0) and bleeds only cells above "
                "the average, never adding charge.",
            ),
            q(
                "According to the Try it yourself notes, what happens if you set bias = 0.0 in (A)?",
                (
                    opt("The estimate tracks the truth exactly with no drift", correct=True),
                    opt("The cells converge faster"),
                    opt("The simulation runs for twice as long"),
                    opt("The estimate drifts even more"),
                ),
                "The notes say setting bias = 0.0 makes the estimate track truth exactly, "
                "since there is no sensor bias to accumulate.",
            ),
        ),
    },
    final=(
        q(
            "Which BMS responsibility is concerned with never letting a cell exceed safe voltage, current, or temperature?",
            (
                opt("Estimate"),
                opt("Protect", correct=True),
                opt("Communicate"),
                opt("Balance"),
            ),
            "Protect is the job of keeping every cell inside its safe operating area; "
            "estimate, balance, and communicate are separate BMS functions.",
        ),
        q(
            "Which combination of methods do production fuel gauges use for robust SoC estimation?",
            (
                opt("OCV lookup alone, sampled continuously"),
                opt("Coulomb counting alone with a perfect sensor"),
                opt(
                    "Continuous coulomb counting re-anchored to OCV at rest, wrapped in a Kalman filter",
                    correct=True,
                ),
                opt("Direct SoC measurement at the terminals"),
            ),
            "Production gauges run coulomb counting continuously, re-anchor to OCV when "
            "the pack rests long enough, and wrap it all in a Kalman filter.",
        ),
        q(
            "Why does SoH feed back into the SoC calculation?",
            (
                opt(
                    "Because the gauge must divide by the present capacity, not the nameplate",
                    correct=True,
                ),
                opt("Because SoH replaces the current sensor"),
                opt("Because OCV lookup needs the resistance SoH"),
                opt("Because balancing can restore lost capacity"),
            ),
            "As a cell ages its usable capacity shrinks, so the fuel gauge must divide by "
            "the present capacity rather than the nameplate value.",
        ),
        q(
            "A pack is wired 96S with cells around 3.6 V. Roughly what pack voltage does this give?",
            (
                opt("About 12 V"),
                opt("About 48 V"),
                opt("About 350 V", correct=True),
                opt("About 1000 V"),
            ),
            "V_pack = N_s x V_cell = 96 x 3.6, which is about 346 V, roughly the 350 V "
            "of a typical EV pack.",
        ),
        q(
            "Why is balancing unable to make an unbalanced pack hold more total capacity?",
            (
                opt("Because it only runs during discharge"),
                opt(
                    "Because it fixes charge mismatch, not capacity mismatch, so the weakest cell still limits the pack",
                    correct=True,
                ),
                opt("Because passive balancing burns energy as heat"),
                opt("Because the AFE cannot measure parallel groups"),
            ),
            "Balancing equalises charge but cannot make a worn cell hold more, so usable "
            "pack capacity is still set by the weakest cell.",
        ),
    ),
)
