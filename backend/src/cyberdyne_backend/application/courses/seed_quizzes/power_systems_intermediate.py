from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Transmission line modeling: R, L, C & ABCD parameters": (
            q(
                "On a transmission line, which parameter is responsible for real-power loss and heating?",
                (
                    opt("series resistance R", correct=True),
                    opt("series inductance L"),
                    opt("shunt capacitance C"),
                    opt("the angle difference delta"),
                ),
                "Series R is conductor resistance, which causes real-power loss and heating.",
            ),
            q(
                "For a short line (under 80 km), how is the line modeled?",
                (
                    opt("just the series impedance Z, ignoring C", correct=True),
                    opt("the nominal pi model with shunt C split in two halves"),
                    opt("hyperbolic functions of the line length"),
                    opt("only the shunt capacitance C"),
                ),
                "A short line under 80 km ignores C and uses just the series impedance Z = R + jwL.",
            ),
            q(
                "In the power-transfer equation P = Vs Vr sin(delta) / X, at what angle difference does power peak?",
                (
                    opt("90 degrees", correct=True),
                    opt("0 degrees"),
                    opt("45 degrees"),
                    opt("180 degrees"),
                ),
                "Since P is proportional to sin(delta), it peaks at delta = 90 degrees.",
            ),
        ),
        "Power flow analysis: Ybus, Gauss-Seidel & Newton-Raphson": (
            q(
                "In the bus admittance matrix Ybus, what does an off-diagonal entry Yij equal?",
                (
                    opt("minus the admittance directly between buses i and j", correct=True),
                    opt("the sum of all admittances connected to bus i"),
                    opt("the Thevenin impedance at bus j"),
                    opt("the product of the bus voltages"),
                ),
                "The off-diagonal Yij is minus the admittance directly between buses i and j.",
            ),
            q(
                "For a PQ (load) bus, which quantities are the unknowns to solve for?",
                (
                    opt("the voltage magnitude |V| and angle", correct=True),
                    opt("the real power P and reactive power Q"),
                    opt("the reactive power Q and angle"),
                    opt("the real power P and voltage magnitude |V|"),
                ),
                "A PQ load bus knows P and Q, so the unknowns are the voltage magnitude and angle.",
            ),
            q(
                "Why is Newton-Raphson the industry standard for power flow over Gauss-Seidel?",
                (
                    opt("it converges quadratically, typically in 3-5 iterations", correct=True),
                    opt("it avoids forming the Ybus matrix entirely"),
                    opt("it converges only linearly but is simpler"),
                    opt("it requires no Jacobian and never iterates"),
                ),
                "Newton-Raphson linearizes with the Jacobian and converges quadratically in about 3-5 iterations.",
            ),
        ),
        "Fault analysis: symmetrical faults & symmetrical components": (
            q(
                "In per-unit, the symmetrical fault current is given by which expression?",
                (
                    opt("Vprefault / Zth", correct=True),
                    opt("Zth / Vprefault"),
                    opt("Vprefault times Zth"),
                    opt("Vprefault + Zth"),
                ),
                "I_fault = Vprefault / Zth, so a small Thevenin impedance gives a huge fault current.",
            ),
            q(
                "Which symmetrical component consists of all three phasors in phase together, flowing in the neutral or ground?",
                (
                    opt("zero sequence", correct=True),
                    opt("positive sequence"),
                    opt("negative sequence"),
                    opt("balanced sequence"),
                ),
                "Zero sequence has all three phasors in phase and flows in the neutral or ground.",
            ),
            q(
                "What does a smaller Thevenin impedance Zth at a bus mean for fault current?",
                (
                    opt("a stronger bus with a much larger fault current", correct=True),
                    opt("a weaker bus with a smaller fault current"),
                    opt("no change, since fault current depends only on voltage"),
                    opt("a bus that cannot experience a fault"),
                ),
                "A small Zth indicates a strong bus close to big generators and yields a huge fault current.",
            ),
        ),
        "Protection systems: relays, breakers & coordination": (
            q(
                "Which relay type senses impedance (V over I) to the fault and is used for transmission lines?",
                (
                    opt("distance relay (21)", correct=True),
                    opt("overcurrent relay (50/51)"),
                    opt("differential relay (87)"),
                    opt("directional relay"),
                ),
                "The distance relay (21) measures impedance V/I to the fault and protects transmission lines.",
            ),
            q(
                "On an inverse-time overcurrent relay, how does trip time change as fault current grows larger?",
                (
                    opt("trip time gets shorter", correct=True),
                    opt("trip time gets longer"),
                    opt("trip time stays constant"),
                    opt("the relay stops tripping"),
                ),
                "An inverse-time curve means a larger current trips faster, so a dead short trips almost instantly.",
            ),
            q(
                "In protection coordination, what is the typical grading margin the upstream backup device waits?",
                (
                    opt("about 0.3 s", correct=True),
                    opt("about 3 s"),
                    opt("about 30 ms with no margin"),
                    opt("about 10 s"),
                ),
                "The upstream device waits a grading margin of about 0.3 s as backup so the nearest device trips first.",
            ),
        ),
        "Voltage & reactive-power control": (
            q(
                "Holding bus voltage near 1.0 pu is achieved mainly by controlling which quantity?",
                (
                    opt("reactive power Q", correct=True),
                    opt("system frequency"),
                    opt("real power P only"),
                    opt("the line resistance R"),
                ),
                "Voltage is local and the lever to control it is reactive power Q.",
            ),
            q(
                "Approximately how does reactive power flow Q through a reactance X affect voltage?",
                (
                    opt("it causes a voltage drop of about Q X / V", correct=True),
                    opt("it has no effect on voltage"),
                    opt("it raises voltage by R Q"),
                    opt("it sets the system frequency"),
                ),
                "Pushing Q through reactance X causes a voltage drop of roughly delta V = Q X / V.",
            ),
            q(
                "Which device supplies reactive power to boost voltage and is switched in steps near the load?",
                (
                    opt("a shunt capacitor bank", correct=True),
                    opt("a shunt reactor"),
                    opt("an out-of-step protection relay"),
                    opt("a circuit breaker"),
                ),
                "A shunt capacitor bank supplies Q to boost voltage and is cheap and switched in steps.",
            ),
        ),
        "Lab: build Ybus & compute a three-phase fault current": (
            q(
                "In the lab, how is Zbus obtained from Ybus, and what does its diagonal represent?",
                (
                    opt(
                        "Zbus is the inverse of Ybus; the diagonal is the Thevenin impedance at each bus",
                        correct=True,
                    ),
                    opt("Zbus is the transpose of Ybus; the diagonal is the bus voltage"),
                    opt("Zbus is Ybus times two; the diagonal is the line current"),
                    opt("Zbus is the conjugate of Ybus; the diagonal is the injected power"),
                ),
                "Zbus = inverse of Ybus, and its diagonal entries are the Thevenin impedances at each bus.",
            ),
            q(
                "In the Gauss-Seidel sweep, how is bus 1 treated and how are buses 2 and 3 treated?",
                (
                    opt("bus 1 is the slack bus; buses 2 and 3 are PQ loads", correct=True),
                    opt("bus 1 is a PQ load; buses 2 and 3 are slack buses"),
                    opt("all three buses are PV generator buses"),
                    opt("bus 1 is a PV bus; buses 2 and 3 are slack buses"),
                ),
                "The lab fixes bus 1 as the slack reference and iterates buses 2 and 3 as PQ loads.",
            ),
            q(
                "According to the lab's try-it-yourself notes, what happens if you halve z12 to make a stronger tie?",
                (
                    opt("the bus fault currents rise", correct=True),
                    opt("the bus fault currents fall to zero"),
                    opt("the Gauss-Seidel sweep stops converging"),
                    opt("the base current Ibase doubles"),
                ),
                "Halving z12 strengthens the tie, lowering Thevenin impedance and raising bus fault currents.",
            ),
        ),
    },
    final=(
        q(
            "Which line model lumps the shunt capacitance C into two halves at each end for an 80-250 km line?",
            (
                opt("the nominal pi model", correct=True),
                opt("the short-line series-impedance model"),
                opt("the long-line hyperbolic model"),
                opt("the ABCD lossless model"),
            ),
            "The medium-length (80-250 km) line uses the nominal pi model with C split into two halves.",
        ),
        q(
            "Which bus type in power flow has known voltage magnitude with angle fixed at zero, and unknown P and Q?",
            (
                opt("the slack (reference) bus", correct=True),
                opt("the PV generator bus"),
                opt("the PQ load bus"),
                opt("the zero-sequence bus"),
            ),
            "The slack bus fixes |V| and angle = 0, leaving P and Q as the unknowns.",
        ),
        q(
            "Switchgear is rated by its interrupting capacity (for example 40 kA); what study computes the fault current at every bus?",
            (
                opt("the short-circuit study", correct=True),
                opt("the load-frequency control study"),
                opt("the Ferranti-effect study"),
                opt("the duck-curve study"),
            ),
            "The short-circuit study computes fault current at every bus to ensure each breaker can interrupt its worst case.",
        ),
        q(
            "What is voltage collapse and why does it occur?",
            (
                opt(
                    "a runaway voltage drop when a stressed grid runs out of reactive reserve",
                    correct=True,
                ),
                opt("a sudden rise in frequency from too much inertia"),
                opt("a relay tripping faster as current grows"),
                opt("a balanced three-phase fault clearing itself"),
            ),
            "When reactive reserve runs out, lower voltage forces more current, dropping voltage further in a spiral.",
        ),
        q(
            "The power-transfer equation P = Vs Vr sin(delta) / X shows power flows in which direction?",
            (
                opt("from the leading angle to the lagging angle", correct=True),
                opt("from the lagging angle to the leading angle"),
                opt("from low voltage to high voltage only"),
                opt("only when delta equals zero"),
            ),
            "Power flows from the leading to the lagging angle and peaks at delta = 90 degrees.",
        ),
    ),
)
