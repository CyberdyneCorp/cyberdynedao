from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Buck, boost & buck-boost converters": (
            q(
                "What does volt-second balance state about a converter inductor in steady state?",
                (
                    opt("Its average current over a switching period is zero"),
                    opt("Its average voltage over a switching period is zero", correct=True),
                    opt("Its peak voltage equals the input voltage"),
                    opt("Its stored energy doubles each cycle"),
                ),
                "In steady state the inductor average voltage over a period is zero, otherwise its current would ramp forever.",
            ),
            q(
                "What is the boost converter output voltage in terms of Vin and duty cycle D?",
                (
                    opt("D times Vin"),
                    opt("Vin divided by (1 minus D)", correct=True),
                    opt("minus D over (1 minus D) times Vin"),
                    opt("Vin times (1 minus D)"),
                ),
                "Boost steps up: Vout equals Vin over (1 minus D), derived from volt-second balance.",
            ),
            q(
                "Why can you not boost arbitrarily high as D approaches 1?",
                (
                    opt("Volt-second balance no longer applies"),
                    opt("The diode stops conducting entirely"),
                    opt(
                        "Parasitic resistances cap the ratio and efficiency collapses", correct=True
                    ),
                    opt("The inductor current reaches zero"),
                ),
                "The ideal boost ratio runs away as D approaches 1, but parasitic resistances cap it and efficiency collapses.",
            ),
        ),
        "Inductor & capacitor design (ripple)": (
            q(
                "For a buck, the inductor ripple current diL is proportional to which combination?",
                (
                    opt("(Vin minus Vout) times D divided by (L times fsw)", correct=True),
                    opt("(Vin plus Vout) times L times fsw"),
                    opt("Vout times D divided by ESR"),
                    opt("(Vin minus Vout) times L divided by D"),
                ),
                "The buck inductor ripple is diL equals (Vin minus Vout) times D divided by (L times fsw).",
            ),
            q(
                "What distinguishes discontinuous conduction mode (DCM) from CCM?",
                (
                    opt("The inductor current never reaches zero"),
                    opt(
                        "The inductor current hits zero each cycle and the ratio becomes load-dependent",
                        correct=True,
                    ),
                    opt("The output voltage ripple disappears"),
                    opt("The switching frequency must double"),
                ),
                "In DCM the inductor current reaches zero each cycle at light load, making the conversion ratio load-dependent.",
            ),
            q(
                "In real output capacitors, what often dominates the output voltage ripple?",
                (
                    opt("The capacitor equivalent series resistance (ESR)", correct=True),
                    opt("The inductor DCR"),
                    opt("The diode forward voltage"),
                    opt("The gate-charge loss"),
                ),
                "ESR often dominates the output ripple, which is why low-ESR ceramics and polymer caps matter.",
            ),
        ),
        "Synchronous rectification & efficiency": (
            q(
                "What does synchronous rectification replace the freewheeling diode with?",
                (
                    opt("A second MOSFET driven on when the diode would conduct", correct=True),
                    opt("A larger reservoir capacitor"),
                    opt("A thyristor fired at angle alpha"),
                    opt("A second inductor in series"),
                ),
                "Synchronous rectification swaps the diode for a low-side MOSFET, dropping only I times Rdson instead of 0.5 to 0.7 V.",
            ),
            q(
                "Which loss dominates at high load in a synchronous buck?",
                (
                    opt("Quiescent controller bias loss"),
                    opt("Switching and gate-charge loss"),
                    opt("Conduction loss (I squared times Rdson)", correct=True),
                    opt("Diode reverse-recovery loss"),
                ),
                "Conduction loss scales with current squared, so it dominates at high load while switching loss dominates at light load.",
            ),
            q(
                "Why does the gate driver insert dead time between the two MOSFETs?",
                (
                    opt("To increase the switching frequency"),
                    opt("To prevent shoot-through that would short the input", correct=True),
                    opt("To raise the output voltage ripple"),
                    opt("To eliminate conduction loss"),
                ),
                "If both MOSFETs are on together the input is shorted (shoot-through); dead time is a small gap that prevents it.",
            ),
        ),
        "Controlled rectifiers & thyristors": (
            q(
                "What controls the DC output of a thyristor controlled rectifier?",
                (
                    opt("The firing angle alpha, choosing when to turn the SCRs on", correct=True),
                    opt("The duty cycle of a high-frequency PWM"),
                    opt("The inductor ripple current"),
                    opt("The dead time between switches"),
                ),
                "Phase control sets the DC by choosing when in each half-cycle to fire the thyristors, the firing angle alpha.",
            ),
            q(
                "For a single-phase controlled rectifier, what is the average output Vavg?",
                (
                    opt("(Vm over pi) times (1 plus cos alpha)", correct=True),
                    opt("(Vm over pi) times (1 minus cos alpha)"),
                    opt("Vm times D"),
                    opt("Vm over (1 minus alpha)"),
                ),
                "Vavg equals (Vm over pi) times (1 plus cos alpha): full output near alpha 0, near zero near alpha pi.",
            ),
            q(
                "How does a thyristor (SCR) behave once a gate pulse turns it on?",
                (
                    opt("It turns off immediately when the gate pulse ends"),
                    opt("It latches on until its current drops to zero", correct=True),
                    opt("It oscillates at the switching frequency"),
                    opt("It conducts only while the gate is held high"),
                ),
                "A thyristor latches: a gate pulse turns it on and it stays on until current falls to zero, e.g. at the AC zero-crossing.",
            ),
        ),
        "Closed-loop control of converters": (
            q(
                "What is the main difference between current-mode and voltage-mode control?",
                (
                    opt("Voltage-mode adds an inner loop regulating inductor current"),
                    opt(
                        "Current-mode adds an inner loop regulating the inductor current each cycle",
                        correct=True,
                    ),
                    opt("Current-mode ignores the output voltage entirely"),
                    opt("Voltage-mode requires slope compensation above 50% duty"),
                ),
                "Current-mode adds an inner inductor-current loop that tames the LC pole and gives inherent current limiting.",
            ),
            q(
                "Roughly where should the loop crossover frequency be targeted?",
                (
                    opt("Equal to fsw"),
                    opt("Near fsw divided by 10", correct=True),
                    opt("Near 10 times fsw"),
                    opt("At the line frequency"),
                ),
                "A common target is a crossover near fsw over 10 while keeping about 45 to 60 degrees of phase margin.",
            ),
            q(
                "Why does voltage-mode control make the loop harder to stabilise?",
                (
                    opt("The LC filter's resonant double pole complicates the loop", correct=True),
                    opt("It has no compensator at all"),
                    opt("It needs slope compensation below 50% duty"),
                    opt("It cannot measure the output voltage"),
                ),
                "In voltage-mode the LC filter's resonant double pole makes the loop harder to stabilise than current-mode.",
            ),
        ),
        "Lab: simulate a buck converter": (
            q(
                "In the buck simulation, what value should the settled Vout approach?",
                (
                    opt("Vin divided by (1 minus D)"),
                    opt("D times Vin", correct=True),
                    opt("minus D over (1 minus D) times Vin"),
                    opt("Vin minus Vout"),
                ),
                "The buck settles near Vout equals D times Vin, e.g. D 0.42 at Vin 12 gives about 5 V.",
            ),
            q(
                "In the lab, halving the inductance L from 47e-6 to 22e-6 does what to the inductor current?",
                (
                    opt("Produces a larger inductor-current ripple", correct=True),
                    opt("Eliminates the ripple entirely"),
                    opt("Lowers the settled output voltage"),
                    opt("Doubles the switching frequency"),
                ),
                "Smaller L gives a larger triangular ripple, since diL is inversely proportional to L.",
            ),
            q(
                "Why does the simulation clamp the inductor current iL to zero when it goes negative?",
                (
                    opt(
                        "To model the diode blocking reverse current (CCM/DCM behaviour)",
                        correct=True,
                    ),
                    opt("To model shoot-through in the switches"),
                    opt("To enforce volt-second balance"),
                    opt("To set the crossover frequency"),
                ),
                "The freewheeling diode blocks reverse current, so iL is clamped at zero, capturing the CCM to DCM transition.",
            ),
        ),
    },
    final=(
        q(
            "Which conversion ratio belongs to the buck-boost converter?",
            (
                opt("D times Vin"),
                opt("Vin divided by (1 minus D)"),
                opt("minus D over (1 minus D) times Vin", correct=True),
                opt("Vin times (1 minus D)"),
            ),
            "Buck-boost gives an inverted output: minus D over (1 minus D) times Vin.",
        ),
        q(
            "What is the key analytical tool used to derive converter conversion ratios?",
            (
                opt("Volt-second balance on the inductor", correct=True),
                opt("The firing angle alpha"),
                opt("ESR of the output capacitor"),
                opt("The modulation index"),
            ),
            "Volt-second balance (zero average inductor voltage in steady state) yields buck, boost, and buck-boost ratios.",
        ),
        q(
            "Which statement about losses in a synchronous buck is correct?",
            (
                opt(
                    "Conduction loss dominates at high load and switching loss at light load",
                    correct=True,
                ),
                opt("Switching loss is independent of frequency"),
                opt("Quiescent loss dominates at high load"),
                opt("Conduction loss scales linearly with current"),
            ),
            "Conduction loss (I squared Rdson) dominates at high load; switching loss (proportional to fsw) dominates at light/medium load.",
        ),
        q(
            "For a single-phase controlled rectifier, as the firing angle alpha increases toward pi, the average output Vavg does what?",
            (
                opt("Rises toward its maximum"),
                opt("Falls toward zero", correct=True),
                opt("Stays constant"),
                opt("Becomes negative and latches"),
            ),
            "Vavg equals (Vm over pi)(1 plus cos alpha), so firing late (alpha toward pi) drives the output near zero.",
        ),
        q(
            "Which closed-loop choice is the industry default and provides inherent current limiting?",
            (
                opt("Voltage-mode control"),
                opt("Current-mode control", correct=True),
                opt("Open-loop control"),
                opt("Phase control with thyristors"),
            ),
            "Current-mode control regulates inductor current each cycle, taming the LC pole and giving inherent current limiting.",
        ),
    ),
)
