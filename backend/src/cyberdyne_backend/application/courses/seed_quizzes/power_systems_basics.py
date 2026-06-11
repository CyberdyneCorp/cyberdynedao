from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "AC power: RMS, real, reactive & apparent power": (
            q(
                "For a sinusoid, how is the RMS value related to the peak value?",
                (
                    opt("V_rms = V_peak times sqrt(2)"),
                    opt("V_rms = V_peak divided by sqrt(2)", correct=True),
                    opt("V_rms = V_peak divided by 2"),
                    opt("V_rms = V_peak (they are equal)"),
                ),
                "RMS equals peak divided by sqrt(2), so a 230 V outlet has a peak about 1.41 times higher.",
            ),
            q(
                "Which of the three powers is measured in volt-amperes reactive (var) and does no net work?",
                (
                    opt("Real (active) power P"),
                    opt("Reactive power Q", correct=True),
                    opt("Apparent power S"),
                    opt("Power factor pf"),
                ),
                "Reactive power Q sloshes back and forth doing no net work and is measured in var.",
            ),
            q(
                "A load runs at power factor 0.7. Roughly what does this mean for the current the wires carry?",
                (
                    opt(
                        "The wires carry about 1.4 times more current than the real power needs",
                        correct=True,
                    ),
                    opt("All the current does useful work"),
                    opt("The reactive power is zero"),
                    opt("The apparent power equals the real power"),
                ),
                "Power factor is pf = cos(phi) = P/S; a pf of 0.7 means the wires carry about 1.4x more current than the real power alone needs.",
            ),
        ),
        "The power triangle & power-factor correction": (
            q(
                "In the power triangle, which relationship is correct?",
                (
                    opt("S = P + Q"),
                    opt("S squared = P squared + Q squared", correct=True),
                    opt("P squared = S squared + Q squared"),
                    opt("Q = S times P"),
                ),
                "The three powers form a right triangle with S as the hypotenuse, so S squared = P squared + Q squared.",
            ),
            q(
                "To correct an inductive motor's power factor, what is placed in parallel and why?",
                (
                    opt("A capacitor, because it supplies reactive power locally", correct=True),
                    opt("An inductor, because it absorbs the motor's real power"),
                    opt("A resistor, because it dissipates the reactive power"),
                    opt("Another motor, because it doubles the apparent power"),
                ),
                "A parallel capacitor supplies reactive power locally, cancelling the motor's Q so the grid only delivers real power.",
            ),
            q(
                "Why does the lesson recommend aiming for a corrected pf near 0.95 to 0.98 rather than exactly 1.0?",
                (
                    opt(
                        "Over-correcting pushes pf leading, which can raise voltage and cause resonance",
                        correct=True,
                    ),
                    opt("A pf of 1.0 is physically impossible to reach"),
                    opt("Utilities penalize any pf above 0.9"),
                    opt("Capacitors cannot supply enough var to reach 1.0"),
                ),
                "Too much capacitance pushes the pf leading, which can raise voltage and cause resonance with the system inductance, so aim for about 0.95 to 0.98.",
            ),
        ),
        "Three-phase systems: wye, delta & balanced power": (
            q(
                "By how many degrees is each of the three balanced phase voltages shifted from the next?",
                (
                    opt("90 degrees"),
                    opt("120 degrees", correct=True),
                    opt("180 degrees"),
                    opt("60 degrees"),
                ),
                "The three sinusoids are each shifted 120 degrees, so they sum to zero at every instant.",
            ),
            q(
                "In a wye (star) connection, how do line and phase voltages relate?",
                (
                    opt("V_line = V_phase"),
                    opt("V_line = sqrt(3) times V_phase", correct=True),
                    opt("V_line = V_phase divided by sqrt(3)"),
                    opt("V_line = 3 times V_phase"),
                ),
                "In wye, V_line = sqrt(3) times V_phase, while line and phase currents are equal.",
            ),
            q(
                "What is the total real power of a balanced three-phase load in line quantities?",
                (
                    opt("P = V_line times I_line times cos(phi)"),
                    opt("P = sqrt(3) times V_line times I_line times cos(phi)", correct=True),
                    opt("P = 3 times V_line times I_line"),
                    opt("P = V_line times I_line divided by sqrt(3)"),
                ),
                "Balanced three-phase power in line quantities is P = sqrt(3) times V_line times I_line times cos(phi).",
            ),
        ),
        "The per-unit system & phasors": (
            q(
                "How is a per-unit value defined?",
                (
                    opt("Actual value divided by base value", correct=True),
                    opt("Base value divided by actual value"),
                    opt("Actual value times base value"),
                    opt("Actual value minus base value"),
                ),
                "A per-unit value is the actual value divided by a chosen base value.",
            ),
            q(
                "A major convenience of per-unit is that a transformer's per-unit impedance is what?",
                (
                    opt(
                        "The same on both sides, so transformers nearly vanish from the math",
                        correct=True,
                    ),
                    opt("Always exactly 1.0 pu"),
                    opt("Doubled on the high-voltage side"),
                    opt("Different by the turns ratio on each side"),
                ),
                "A transformer's per-unit impedance is the same on both sides, so transformers practically vanish (no turns-ratio juggling).",
            ),
            q(
                "What does a phasor capture about a steady AC sinusoid?",
                (
                    opt("Its magnitude and angle as a complex number", correct=True),
                    opt("Only its frequency"),
                    opt("Only its instantaneous value at t = 0"),
                    opt("Its RMS value but not its phase"),
                ),
                "A phasor is a complex number holding magnitude and angle, so V = I times Z becomes complex multiplication.",
            ),
        ),
        "The power grid overview: generation, transmission & distribution": (
            q(
                "Why is voltage stepped way up to 110 to 765 kV for transmission?",
                (
                    opt(
                        "Raising V lowers current I, and loss falls with the square of current",
                        correct=True,
                    ),
                    opt("Higher voltage increases the current and therefore the power"),
                    opt("High voltage is safer for nearby homes"),
                    opt("Transformers only work above 100 kV"),
                ),
                "Line loss is I squared times R; for fixed power, raising voltage slashes current, and loss falls with the square of that current.",
            ),
            q(
                "What is the typical voltage at which power plants generate AC before step-up?",
                (
                    opt("120 to 400 V"),
                    opt("10 to 25 kV", correct=True),
                    opt("110 to 765 kV"),
                    opt("4 to 35 kV"),
                ),
                "Generators produce AC at 10 to 25 kV, then step-up transformers raise it for transmission.",
            ),
            q(
                "How do the transmission and distribution network topologies typically differ?",
                (
                    opt(
                        "Transmission is meshed (looped) while distribution is usually radial (tree-like)",
                        correct=True,
                    ),
                    opt("Transmission is radial while distribution is meshed"),
                    opt("Both are always fully meshed"),
                    opt("Both are always radial"),
                ),
                "Transmission is meshed so power can reroute around outages; distribution is usually radial, simpler but a fault darkens everything downstream.",
            ),
        ),
        "Transformers in power systems": (
            q(
                "How does the turns ratio a = N1/N2 relate voltage and current?",
                (
                    opt("V1/V2 = a and I1/I2 = 1/a", correct=True),
                    opt("V1/V2 = 1/a and I1/I2 = a"),
                    opt("V1/V2 = a and I1/I2 = a"),
                    opt("V1/V2 = 1/a and I1/I2 = 1/a"),
                ),
                "Voltage steps by the turns ratio a while current steps inversely, so V1/V2 = a and I1/I2 = 1/a and power is nearly conserved.",
            ),
            q(
                "What does an on-load tap changer (OLTC) do?",
                (
                    opt(
                        "Adjusts winding taps automatically while energized to hold downstream voltage steady",
                        correct=True,
                    ),
                    opt("Disconnects the transformer during faults"),
                    opt("Converts AC to DC inside the transformer"),
                    opt("Changes the 50/60 Hz frequency of the output"),
                ),
                "An OLTC adjusts taps automatically while energized, holding downstream voltage steady as load varies through the day.",
            ),
            q(
                "Why is delta-wye the workhorse step-down connection?",
                (
                    opt(
                        "The wye secondary provides a neutral for distribution while the delta primary traps harmonics",
                        correct=True,
                    ),
                    opt("It eliminates the need for any insulation"),
                    opt("It removes the 30-degree phase shift entirely"),
                    opt("It is the only connection that conserves power"),
                ),
                "Delta-wye gives a wye secondary with a neutral for distribution while the delta primary traps harmonic currents; it adds a fixed 30-degree phase shift.",
            ),
        ),
        "Lab: power triangle, PF correction & three-phase waveforms": (
            q(
                "In the lab, the load is 230 V rms, 10 A rms at pf 0.75. How is apparent power S computed?",
                (
                    opt("S = Vrms times Irms", correct=True),
                    opt("S = Vrms times Irms times cos(phi)"),
                    opt("S = Vrms divided by Irms"),
                    opt("S = Vrms times Irms times sin(phi)"),
                ),
                "Apparent power S = Vrms times Irms = 230 times 10; real power then uses cos(phi) and reactive power uses sin(phi).",
            ),
            q(
                "After correcting from pf 0.75 to pf 0.95, how much reactive power must the capacitor supply (Qc)?",
                (
                    opt("Qc = Q1 minus Q2 (the difference in reactive power)", correct=True),
                    opt("Qc = Q1 plus Q2"),
                    opt("Qc = P times Q2"),
                    opt("Qc = S minus P"),
                ),
                "The capacitor supplies Qc = Q1 - Q2, the reduction in reactive power from before to after correction.",
            ),
            q(
                "What does the lab plot of the three phase voltages a, b, c demonstrate when summed?",
                (
                    opt("a + b + c equals zero at every instant", correct=True),
                    opt("a + b + c equals three times the peak"),
                    opt("a + b + c grows over time"),
                    opt("a + b + c equals the apparent power"),
                ),
                "The balanced three-phase voltages sum to zero (a+b+c = 0), which is why a balanced load needs no neutral current.",
            ),
        ),
    },
    final=(
        q(
            "Which formula correctly gives the real power of a single-phase AC load?",
            (
                opt("P = Vrms times Irms times cos(phi)", correct=True),
                opt("P = Vrms times Irms times sin(phi)"),
                opt("P = Vrms times Irms"),
                opt("P = Vrms divided by Irms"),
            ),
            "Real power P = Vrms times Irms times cos(phi); the sin term gives reactive power Q and the product alone gives apparent power S.",
        ),
        q(
            "A factory at pf 0.75 adds capacitors to reach pf 0.95. What is the main benefit?",
            (
                opt(
                    "Lower line current and removal of the utility power-factor penalty",
                    correct=True,
                ),
                opt("Higher reactive power drawn from the grid"),
                opt("An increase in the real power consumed"),
                opt("A change in the 50/60 Hz system frequency"),
            ),
            "Capacitor banks supply reactive power locally, cutting line current (about 20%) and erasing the utility's power-factor penalty.",
        ),
        q(
            "Why does long-distance transmission use very high voltage?",
            (
                opt(
                    "For fixed power, high voltage means low current, and I squared R loss falls with current squared",
                    correct=True,
                ),
                opt("High voltage increases current and thus delivered power"),
                opt("High voltage lets transformers be removed"),
                opt("High voltage eliminates reactive power"),
            ),
            "Since loss is I squared times R and power is V times I, raising V lowers I, and loss drops with the square of current.",
        ),
        q(
            "In the per-unit system, why do balanced three-phase systems get drawn as a single-line diagram?",
            (
                opt(
                    "Because the system is symmetric, one line can represent all three phases",
                    correct=True,
                ),
                opt("Because only one phase actually carries power"),
                opt("Because per-unit removes two of the three phases"),
                opt("Because the neutral carries the other two phases"),
            ),
            "A balanced three-phase system is symmetric, so engineers draw one line standing for all three phases with standard component symbols.",
        ),
        q(
            "What does a transformer with turns ratio a do to voltage and current between primary and secondary?",
            (
                opt("Steps voltage up by a and current down by a, conserving power", correct=True),
                opt("Steps both voltage and current up by a"),
                opt("Steps voltage down by a and current down by a"),
                opt("Leaves voltage unchanged but doubles current"),
            ),
            "Volts trade for amps: stepping voltage up by a steps current down by a, so S = VI is nearly conserved.",
        ),
    ),
)
