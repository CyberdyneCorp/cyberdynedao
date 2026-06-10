from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Charge, current, voltage & power": (
            q(
                "Current I is best described as the rate of flow of charge, I = dQ/dt. What is its unit?",
                (
                    opt("coulomb (C)"),
                    opt("volt (V)"),
                    opt("ampere (A)", correct=True),
                    opt("watt (W)"),
                ),
                "Current is charge flow rate, measured in amperes; coulomb is charge, volt is voltage, watt is power.",
            ),
            q(
                "Voltage represents which physical quantity?",
                (
                    opt("energy per unit charge", correct=True),
                    opt("charge per unit time"),
                    opt("energy per unit time"),
                    opt("charge per unit volume"),
                ),
                "Voltage is energy per charge, the push; energy per time is power and charge per time is current.",
            ),
            q(
                "Using P = VI, a 5 V source pushing 0.0227 A through a resistor delivers about how much power?",
                (
                    opt("about 0.114 W", correct=True),
                    opt("about 5 W"),
                    opt("about 0.0227 W"),
                    opt("about 1.14 W"),
                ),
                "P = VI = 5 times 0.0227 = 0.114 W, matching the lesson example with V=5 and R=220.",
            ),
        ),
        "Ohm's law & resistor networks": (
            q(
                "For resistors in series, how do you find the equivalent resistance?",
                (
                    opt("add them: Req = R1 + R2 + ...", correct=True),
                    opt("add reciprocals: 1/Req = 1/R1 + 1/R2 + ..."),
                    opt("multiply them: Req = R1 times R2"),
                    opt("take the smallest of the resistors"),
                ),
                "Series resistors share the same current and simply add; the reciprocal rule is for parallel.",
            ),
            q(
                "A voltage divider has Vin = 10 V, R1 = 1 kohm and R2 = 2 kohm. What is Vout = Vin R2/(R1+R2)?",
                (
                    opt("about 6.67 V", correct=True),
                    opt("about 3.33 V"),
                    opt("about 5.0 V"),
                    opt("about 10 V"),
                ),
                "Vout = 10 times 2000/3000 = 6.67 V; the larger R2 takes the larger share of the voltage.",
            ),
            q(
                "Why should a voltage divider not be used to power a load directly?",
                (
                    opt(
                        "its output sags under load because of its output impedance R1 parallel R2",
                        correct=True,
                    ),
                    opt("it can only divide voltages above 10 V"),
                    opt("it adds the two resistances in parallel instead of series"),
                    opt("it converts the DC voltage into AC"),
                ),
                "A divider has output impedance R1 parallel R2, so connecting a load pulls the output down; use it for references and signals.",
            ),
        ),
        "Kirchhoff's laws: KCL & KVL": (
            q(
                "Kirchhoff's Current Law (KCL) at a node states that:",
                (
                    opt(
                        "the currents into the node sum to zero (charge is conserved)", correct=True
                    ),
                    opt("the voltages around the node sum to zero"),
                    opt("the resistances at the node add in series"),
                    opt("the power into the node equals zero"),
                ),
                "KCL is conservation of charge: current in equals current out, so the signed sum of node currents is zero.",
            ),
            q(
                "Kirchhoff's Voltage Law (KVL) is a statement of which conservation principle?",
                (
                    opt("conservation of energy around a closed loop", correct=True),
                    opt("conservation of charge at a node"),
                    opt("conservation of momentum in the wire"),
                    opt("conservation of current through a resistor"),
                ),
                "KVL says voltages around any closed loop sum to zero, which is conservation of energy.",
            ),
            q(
                "A 12 V source drives R1 = 1 kohm and R2 = 2 kohm in series. By KVL, what current flows?",
                (
                    opt("4 mA", correct=True),
                    opt("12 mA"),
                    opt("6 mA"),
                    opt("2 mA"),
                ),
                "KVL gives 12 = I(R1+R2), so I = 12/3000 = 4 mA, and the drops 4 V and 8 V sum back to 12 V.",
            ),
        ),
        "Circuit analysis: nodal, mesh & Thevenin": (
            q(
                "Nodal analysis turns a circuit into the linear system G v = i by writing which law at each node?",
                (
                    opt("KCL (current law)", correct=True),
                    opt("KVL (voltage law)"),
                    opt("the maximum power transfer rule"),
                    opt("the voltage divider rule"),
                ),
                "Nodal analysis writes KCL at every non-reference node and expresses branch currents with Ohm's law, giving G v = i.",
            ),
            q(
                "A Thevenin equivalent reduces any linear two-terminal network to:",
                (
                    opt("a voltage source Vth in series with a resistor Rth", correct=True),
                    opt("a current source in parallel with a capacitor"),
                    opt("two resistors in a voltage divider"),
                    opt("an ideal voltage source with no resistance"),
                ),
                "Thevenin gives one source Vth in series with Rth; its Norton dual is a current source in parallel with Rn = Rth.",
            ),
            q(
                "How is the Thevenin resistance Rth found for a linear network?",
                (
                    opt(
                        "the resistance looking into the terminals with sources zeroed",
                        correct=True,
                    ),
                    opt("the open-circuit voltage at the terminals"),
                    opt("the sum of all branch resistances in the network"),
                    opt("the load resistance that draws maximum current"),
                ),
                "Rth is the resistance seen at the terminals with independent sources zeroed; Vth is the open-circuit voltage.",
            ),
        ),
        "Power, energy & sources": (
            q(
                "Which expression is NOT a valid form of the power dissipated by a resistor?",
                (
                    opt("P = I/V", correct=True),
                    opt("P = VI"),
                    opt("P = I^2 R"),
                    opt("P = V^2/R"),
                ),
                "The valid forms are P = VI = I^2 R = V^2/R; P = I/V is not one of them.",
            ),
            q(
                "A real battery with internal resistance Rs has terminal voltage that, under load current I:",
                (
                    opt("sags to V - I Rs", correct=True),
                    opt("rises to V + I Rs"),
                    opt("stays exactly at V regardless of load"),
                    opt("drops to zero immediately"),
                ),
                "A real source drops I Rs across its internal resistance, so the terminal voltage sags to V - I Rs under load.",
            ),
            q(
                "Maximum power is transferred to a load when its resistance equals Rth. What efficiency results at that point?",
                (
                    opt("50%, since half the power heats the source", correct=True),
                    opt("100%, all power reaches the load"),
                    opt("90%, typical of power systems"),
                    opt("0%, no power reaches the load"),
                ),
                "At the matched condition RL = Rth, efficiency is only 50% because equal power is dissipated in the source.",
            ),
        ),
        "Lab: solve a resistor network": (
            q(
                "In the lab, the conductance matrix G is built and then solved for node voltages. Which equation is solved?",
                (
                    opt("G v = i", correct=True),
                    opt("v = G i"),
                    opt("i = R v"),
                    opt("G = v i"),
                ),
                "Nodal analysis forms G v = i, then v = np.linalg.solve(G, i) gives the node voltages, just as SPICE does.",
            ),
            q(
                "A diagonal entry of G for a node is built from which combination of the branch resistors at that node?",
                (
                    opt(
                        "the sum of the conductances 1/R of the resistors touching the node",
                        correct=True,
                    ),
                    opt("the sum of the resistances R of the resistors touching the node"),
                    opt("the product of the resistances at the node"),
                    opt("the single largest resistance at the node"),
                ),
                "Each diagonal entry sums the conductances 1/R of all resistors connected to that node, e.g. 1/R1 + 1/R2 + 1/R4.",
            ),
            q(
                "In the lab the current through R2 is computed as (v[0] - v[1])/R2. Which law justifies this?",
                (
                    opt("Ohm's law applied to the voltage across R2", correct=True),
                    opt("Kirchhoff's voltage law around the supply loop"),
                    opt("the maximum power transfer theorem"),
                    opt("the voltage divider rule"),
                ),
                "The branch current is the node-voltage difference across R2 divided by R2, which is Ohm's law I = V/R.",
            ),
        ),
    },
    final=(
        q(
            "Ohm's law relates voltage, current and resistance as:",
            (
                opt("V = I R", correct=True),
                opt("V = I/R"),
                opt("V = R/I"),
                opt("V = I^2 R"),
            ),
            "Ohm's law is V = I R; from it the power forms P = VI = I^2 R = V^2/R follow.",
        ),
        q(
            "Three resistors of 1 kohm, 1 kohm and 1 kohm are placed in parallel. The equivalent resistance is:",
            (
                opt("about 333 ohm", correct=True),
                opt("3 kohm"),
                opt("1 kohm"),
                opt("about 667 ohm"),
            ),
            "Parallel resistors give 1/Req = 3/1000, so Req = 333 ohm, always smaller than the smallest resistor.",
        ),
        q(
            "Which pair of laws together with Ohm's law can solve any lumped circuit?",
            (
                opt("KCL and KVL", correct=True),
                opt("KCL and the voltage divider rule"),
                opt("the maximum power transfer and Thevenin rules"),
                opt("the series and parallel reduction rules only"),
            ),
            "KCL, KVL and Ohm's law are complete; nodal, mesh and Thevenin methods are just efficient bookkeeping of these.",
        ),
        q(
            "A 9 V source has internal resistance 1 ohm and drives a 2 ohm load. What is the load current?",
            (
                opt("3 A", correct=True),
                opt("4.5 A"),
                opt("9 A"),
                opt("1.5 A"),
            ),
            "The total resistance is 1 + 2 = 3 ohm, so I = 9/3 = 3 A and the terminal voltage sags to 9 - 3 times 1 = 6 V.",
        ),
        q(
            "Why must resistors be sized by their power rating, not just resistance?",
            (
                opt(
                    "dissipated power P = V^2/R heats the part, and exceeding the rating destroys it",
                    correct=True,
                ),
                opt("higher resistance always means higher cost"),
                opt("power rating changes the resistance value"),
                opt("a higher rating reduces the current through the resistor"),
            ),
            "A 1/4 W resistor with 1 W across it burns up; P = V^2/R tells you the rating you need for the heat.",
        ),
    ),
)
