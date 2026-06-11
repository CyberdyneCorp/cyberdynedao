from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "PN junction I-V and the diode": (
            q(
                "What does the Shockley diode equation describe?",
                (
                    opt("A linear resistor I-V"),
                    opt("An exponential, one-way current I = Is(exp(V/nVt) - 1)", correct=True),
                    opt("A constant current independent of voltage"),
                    opt("A purely capacitive response"),
                ),
                "The diode is an exponential, one-way current captured by I = Is(exp(V/nVt) - 1).",
            ),
            q(
                "Under forward bias of a PN junction, what happens to the depletion region?",
                (
                    opt("It widens as the applied field adds to the built-in field"),
                    opt(
                        "It shrinks because the applied voltage opposes the built-in field",
                        correct=True,
                    ),
                    opt("It is unchanged"),
                    opt("It is replaced by an oxide layer"),
                ),
                "Forward bias opposes the built-in field, shrinking depletion so majority carriers flood across.",
            ),
            q(
                "Which breakdown mechanism dominates in heavily-doped, thin junctions below about 5 V?",
                (
                    opt("Avalanche by impact ionisation"),
                    opt("Zener tunneling, where electrons tunnel straight through", correct=True),
                    opt("Thermal runaway"),
                    opt("Punch-through"),
                ),
                "Zener (tunneling) dominates below about 5 V; avalanche dominates above about 6 V.",
            ),
        ),
        "BJT physics: injection & current gain": (
            q(
                "What is the central principle that makes a BJT work?",
                (
                    opt("Field-effect control of an inversion channel"),
                    opt(
                        "Minority-carrier injection across a base thin enough to cross before recombining",
                        correct=True,
                    ),
                    opt("Tunneling across a thin oxide"),
                    opt("Photogeneration in a depletion region"),
                ),
                "The BJT relies on minority-carrier injection across a thin base before recombination.",
            ),
            q(
                "In an NPN BJT in the active region, how are the two junctions biased?",
                (
                    opt("Both junctions reverse biased"),
                    opt("Base-emitter forward, base-collector reverse", correct=True),
                    opt("Base-emitter reverse, base-collector forward"),
                    opt("Both junctions forward biased"),
                ),
                "In active mode the base-emitter junction is forward biased and the base-collector is reverse biased.",
            ),
            q(
                "What is the Early effect seen in the BJT output characteristic?",
                (
                    opt("A sharp drop of Ic at high Vce"),
                    opt(
                        "The gentle upward slope of Ic as Vce widens the base-collector depletion and thins the base",
                        correct=True,
                    ),
                    opt("The exponential rise of Ic with Vbe"),
                    opt("The fall of beta at low currents"),
                ),
                "The Early effect is the gentle upward slope: more Vce thins the effective base, nudging Ic up.",
            ),
        ),
        "The MOS capacitor & MOSFET physics": (
            q(
                "Over p-type silicon, what surface state appears at large positive gate voltage above Vth?",
                (
                    opt("Accumulation of holes"),
                    opt("Inversion, where electrons form an n-type channel", correct=True),
                    opt("Depletion only"),
                    opt("Breakdown"),
                ),
                "Above threshold the surface inverts: electrons gather to form an n-type channel.",
            ),
            q(
                "In MOSFET saturation, the drain current to first order depends on what?",
                (
                    opt("Only on Vds"),
                    opt("Only on the gate, as Id = 0.5 k (Vgs - Vth)^2", correct=True),
                    opt("On neither gate nor drain voltage"),
                    opt("Linearly on Vds like a resistor"),
                ),
                "In saturation the channel pinches off and Id = 0.5 k (Vgs - Vth)^2 depends on the gate.",
            ),
            q(
                "What does the body effect do to the threshold voltage?",
                (
                    opt("Reverse-biasing the body raises Vth", correct=True),
                    opt("Reverse-biasing the body lowers Vth"),
                    opt("It has no effect on Vth"),
                    opt("It removes the oxide charge"),
                ),
                "The body effect: reverse-biasing the body raises Vth.",
            ),
        ),
        "Device capacitances & high-frequency limits": (
            q(
                "How does junction (depletion) capacitance change as reverse bias increases?",
                (
                    opt("It increases as the depletion layer widens"),
                    opt("It decreases as the depletion layer widens", correct=True),
                    opt("It stays constant"),
                    opt("It becomes negative"),
                ),
                "Cj = Cj0/sqrt(1 - V/Vbi) decreases as reverse bias widens the depletion layer.",
            ),
            q(
                "Why are shorter MOSFET channels dramatically faster, driving Moore's law?",
                (
                    opt("Because fT scales as 1/L^2", correct=True),
                    opt("Because fT scales linearly with L"),
                    opt("Because Cox falls to zero"),
                    opt("Because beta rises with length"),
                ),
                "For a MOSFET fT is about mu(Vgs - Vth)/(2 pi L^2), so the 1/L^2 makes short channels much faster.",
            ),
            q(
                "What roughly sets a logic gate's delay?",
                (
                    opt(
                        "tau is about Ron times Cload, the on-resistance charging the next gate's capacitance",
                        correct=True,
                    ),
                    opt("Only the supply voltage"),
                    opt("Only the threshold voltage"),
                    opt("The bandgap energy"),
                ),
                "Gate delay is roughly Ron Cload, and interconnect RC increasingly dominates as devices shrink.",
            ),
        ),
        "Optoelectronic devices: LED, photodiode & solar cell": (
            q(
                "Why are LEDs not made from silicon?",
                (
                    opt("Silicon has too large a bandgap"),
                    opt(
                        "Silicon is an indirect-gap material that recombines without emitting light",
                        correct=True,
                    ),
                    opt("Silicon cannot be doped p-type"),
                    opt("Silicon has no depletion region"),
                ),
                "LEDs need direct-bandgap materials; silicon's indirect gap recombines without light.",
            ),
            q(
                "How is a solar cell operated relative to a photodiode?",
                (
                    opt("Reverse biased like a photodiode"),
                    opt("Without bias, in the power-generating fourth quadrant", correct=True),
                    opt("Forward biased like an LED"),
                    opt("In avalanche breakdown"),
                ),
                "A solar cell is a large photodiode run without bias in the power-generating quadrant.",
            ),
            q(
                "The relation lambda(um) is about 1.24/Eg(eV) means what about the bandgap?",
                (
                    opt("Larger bandgap gives longer wavelength"),
                    opt(
                        "The gap sets the colour; larger Eg gives shorter wavelength", correct=True
                    ),
                    opt("Wavelength is independent of the bandgap"),
                    opt("Only silicon obeys this relation"),
                ),
                "lambda is about 1.24/Eg, so the bandgap sets the colour and a larger gap gives shorter wavelength.",
            ),
        ),
        "Lab: diode & MOSFET I-V from the device equations": (
            q(
                "Which two device equations does the lab plot?",
                (
                    opt(
                        "The Shockley diode equation and the MOSFET square-law (triode plus saturation)",
                        correct=True,
                    ),
                    opt("The Early effect and the bandgap relation"),
                    opt("Junction capacitance and subthreshold swing"),
                    opt("Only the solar cell I-V"),
                ),
                "The lab plots the Shockley diode equation and the MOSFET square-law (triode then saturation).",
            ),
            q(
                "In the lab, what value is used for the thermal voltage Vt at 300 K?",
                (
                    opt("0.7 V"),
                    opt("0.02585 V", correct=True),
                    opt("1.0 V"),
                    opt("26 V"),
                ),
                "The lab sets Vt = 0.02585 V, the thermal voltage at 300 K.",
            ),
            q(
                "In the lab MOSFET family, raising k (a wider W/L) does what?",
                (
                    opt("Lowers the saturation current"),
                    opt("Gives a steeper triode slope and higher saturation current", correct=True),
                    opt("Has no effect on the curves"),
                    opt("Shifts the threshold voltage to zero"),
                ),
                "Raising k (wider W/L) produces a steeper triode slope and a higher saturation current.",
            ),
        ),
    },
    final=(
        q(
            "Which equation governs the PN junction diode I-V?",
            (
                opt("I = beta Ib"),
                opt("I = Is(exp(V/nVt) - 1)", correct=True),
                opt("Id = 0.5 k (Vgs - Vth)^2"),
                opt("Cj = Cj0/sqrt(1 - V/Vbi)"),
            ),
            "The Shockley diode equation is I = Is(exp(V/nVt) - 1).",
        ),
        q(
            "In a BJT, the relation Ic = beta Ib expresses what?",
            (
                opt("A small base current controlling a large collector current", correct=True),
                opt("The gate controlling an inversion channel"),
                opt("Photocurrent generation under illumination"),
                opt("The junction capacitance versus bias"),
            ),
            "Ic = beta Ib means a small base current controls a large collector current.",
        ),
        q(
            "A MOSFET enters saturation when the channel does what at the drain?",
            (
                opt("Accumulates holes"),
                opt("Pinches off, so current saturates and depends on the gate", correct=True),
                opt("Breaks down by avalanche"),
                opt("Becomes a perfect insulator"),
            ),
            "In saturation the channel pinches off at the drain and Id = 0.5 k (Vgs - Vth)^2.",
        ),
        q(
            "Which figure of merit marks where a device's current gain falls to 1?",
            (
                opt("The breakdown voltage Vbr"),
                opt("The transition frequency fT", correct=True),
                opt("The fill factor"),
                opt("The open-circuit voltage Voc"),
            ),
            "The transition frequency fT is where current gain falls to 1; for a MOSFET it scales as 1/L^2.",
        ),
        q(
            "A solar cell's I-V is the diode equation modified how?",
            (
                opt("Multiplied by beta"),
                opt("Minus the photogenerated current, I = Is(exp(V/Vt) - 1) - Iph", correct=True),
                opt("Plus the junction capacitance"),
                opt("Divided by the channel length squared"),
            ),
            "Under illumination I = Is(exp(V/Vt) - 1) - Iph, dipping into the power-generating quadrant.",
        ),
    ),
)
