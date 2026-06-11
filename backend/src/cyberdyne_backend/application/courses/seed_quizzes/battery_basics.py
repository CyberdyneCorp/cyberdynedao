from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Electrochemical fundamentals": (
            q(
                "On discharge, what happens at the anode of a cell?",
                (
                    opt("It accepts electrons (reduction)"),
                    opt("It gives up electrons (oxidation)", correct=True),
                    opt("It only carries ions internally"),
                    opt("It blocks electrons from leaving"),
                ),
                "The anode is the negative electrode; on discharge it is oxidized and gives up electrons.",
            ),
            q(
                "A 3.2 Ah cell at 3.7 V nominal stores roughly how much energy?",
                (
                    opt("About 3.2 Wh"),
                    opt("About 3.7 Wh"),
                    opt("About 11.8 Wh", correct=True),
                    opt("About 100 Wh"),
                ),
                "Energy is capacity times voltage: 3.2 Ah times 3.7 V is about 11.8 Wh.",
            ),
            q(
                "Why should two cells with the same Ah be compared in Wh rather than Ah?",
                (
                    opt("Because Ah is energy and Wh is charge"),
                    opt(
                        "Because cells with the same Ah but different voltages store different energy",
                        correct=True,
                    ),
                    opt("Because Ah always equals Wh for any cell"),
                    opt("Because voltage has no effect on stored energy"),
                ),
                "Ah is charge and Wh is energy; differing voltages mean different stored energy for the same Ah.",
            ),
        ),
        "Battery chemistries & tradeoffs": (
            q(
                "Which chemistry is described as very safe with long cycle life and low cost, but lower energy density?",
                (
                    opt("Li-ion NMC/LCO"),
                    opt("Lead-acid"),
                    opt("LiFePO4 (LFP)", correct=True),
                    opt("NiMH"),
                ),
                "LFP is very safe with long cycle life and cheap, at the cost of lower energy density.",
            ),
            q(
                "For a phone, which property do you maximize when picking a chemistry?",
                (
                    opt("Surge power (lead-acid)"),
                    opt("Energy density in Wh/kg (NMC/LCO)", correct=True),
                    opt("Lowest possible cost regardless of weight"),
                    opt("Cycle life above all else"),
                ),
                "Phones maximize Wh/kg, favoring NMC/LCO; safety/cycle-life and surge power matter more for other uses.",
            ),
            q(
                "On a Ragone-style energy vs power map, where does a supercapacitor sit?",
                (
                    opt("High energy, low power"),
                    opt("Extreme high power, low energy", correct=True),
                    opt("Balanced middle of the map"),
                    opt("Lowest power and lowest energy"),
                ),
                "A supercapacitor occupies the extreme high-power, low-energy corner of the map.",
            ),
        ),
        "Cell characteristics: OCV, C-rate & internal resistance": (
            q(
                "Open-circuit voltage (OCV) is best described as a function of what?",
                (
                    opt("The discharge current only"),
                    opt("The internal resistance only"),
                    opt("State of charge (SoC)", correct=True),
                    opt("The ambient temperature only"),
                ),
                "A rested cell settles to its OCV, which is a function of state of charge.",
            ),
            q(
                "A 3 Ah cell discharged at 2C draws how much current?",
                (
                    opt("1.5 A"),
                    opt("3 A"),
                    opt("6 A", correct=True),
                    opt("12 A"),
                ),
                "C-rate times capacity gives current: 2C times 3 Ah is 6 A.",
            ),
            q(
                "Under load, how does internal resistance R0 affect terminal voltage?",
                (
                    opt("Vterm = OCV(SoC) - I*R0, so it drops below OCV", correct=True),
                    opt("Vterm = OCV(SoC) + I*R0, so it rises above OCV"),
                    opt("It has no effect on terminal voltage"),
                    opt("It only changes the OCV-SoC curve shape"),
                ),
                "Under load the terminal voltage is OCV minus the I*R0 drop, and the cell heats by I^2*R0.",
            ),
        ),
        "The equivalent-circuit model: Rint & RC": (
            q(
                "What does the Rint model consist of?",
                (
                    opt("An OCV(SoC) source in series with R0", correct=True),
                    opt("Two parallel RC branches only"),
                    opt("A capacitor in series with the load"),
                    opt("An OCV source with no resistance at all"),
                ),
                "The Rint model is an OCV(SoC) source in series with a single internal resistance R0.",
            ),
            q(
                "In the Thevenin/RC model, what does the parallel RC branch model?",
                (
                    opt("The instant ohmic voltage drop"),
                    opt(
                        "Polarization: the slow voltage recovery over seconds to minutes",
                        correct=True,
                    ),
                    opt("The total stored energy"),
                    opt("The cut-off voltage threshold"),
                ),
                "The RC branch models polarization, the slow relaxation seen after current stops, with tau = R1*C1.",
            ),
            q(
                "For an RC branch with R1 = 0.02 ohm and C1 = 800 F, the time constant tau is about?",
                (
                    opt("0.4 s"),
                    opt("16 s", correct=True),
                    opt("160 s"),
                    opt("800 s"),
                ),
                "tau = R1*C1 = 0.02 times 800 = 16 s.",
            ),
        ),
        "Safety & degradation basics": (
            q(
                "What makes thermal runaway a self-reinforcing loop?",
                (
                    opt(
                        "Exothermic reactions generate more heat, which speeds up the reactions",
                        correct=True,
                    ),
                    opt("Cooling rises exponentially while heat rises linearly"),
                    opt("The cell voltage rises without any heat"),
                    opt("Ions stop moving through the electrolyte"),
                ),
                "Heat triggers exothermic reactions that produce more heat, accelerating until runaway.",
            ),
            q(
                "Why can a small overheat run away past a tipping point?",
                (
                    opt("Heat generation rises linearly while cooling rises exponentially"),
                    opt(
                        "Heat generation rises roughly exponentially while cooling rises only linearly",
                        correct=True,
                    ),
                    opt("Both heat generation and cooling are constant"),
                    opt("Cooling always exceeds heat generation"),
                ),
                "Generation rises roughly exponentially with temperature while cooling rises only linearly; past the crossover, generation wins.",
            ),
            q(
                "Which two effects dominate cell aging?",
                (
                    opt("Capacity fade and resistance growth", correct=True),
                    opt("Voltage gain and capacity gain"),
                    opt("Falling internal resistance and rising capacity"),
                    opt("Electrolyte freezing and anode plating only"),
                ),
                "Aging shows up as capacity fade (less usable Ah) and resistance growth (R0 rises).",
            ),
        ),
        "Lab: discharge curve from a cell model": (
            q(
                "In the lab, how is state of charge updated each time step?",
                (
                    opt("By coulomb counting: soc = soc - (I*dt)/Q_coulomb", correct=True),
                    opt("By reading OCV directly each step"),
                    opt("By adding I*R0 to the previous SoC"),
                    opt("By holding SoC constant until cut-off"),
                ),
                "The lab drops SoC by coulomb counting each second, subtracting (I*dt)/Q_coulomb.",
            ),
            q(
                "How is the lab's terminal voltage computed at each step?",
                (
                    opt("vterm = ocv - I*R0 - v1", correct=True),
                    opt("vterm = ocv + I*R0 + v1"),
                    opt("vterm = ocv only"),
                    opt("vterm = I*R0 - ocv"),
                ),
                "Terminal voltage is OCV(SoC) minus the I*R0 ohmic drop minus the polarization branch voltage v1.",
            ),
            q(
                "Per the lab's suggested experiments, what happens if you raise R0 to 0.15 (an aged cell)?",
                (
                    opt("Every curve sags and cuts off sooner", correct=True),
                    opt("Every curve rises and lasts longer"),
                    opt("The curves are unchanged"),
                    opt("The cut-off voltage disappears"),
                ),
                "A higher R0 models an aged cell: every discharge curve sags more and reaches cut-off sooner.",
            ),
        ),
    },
    final=(
        q(
            "What is the correct relationship between charge, voltage, and energy?",
            (
                opt("Energy (Wh) = capacity (Ah) times voltage (V)", correct=True),
                opt("Energy (Ah) = capacity (Wh) times voltage (V)"),
                opt("Energy equals capacity divided by voltage"),
                opt("Energy equals voltage divided by capacity"),
            ),
            "Energy is capacity times nominal voltage: Wh = Ah times V.",
        ),
        q(
            "Which chemistry pairing matches its typical strength?",
            (
                opt("Lead-acid: highest energy density"),
                opt("LFP: very safe with long cycle life", correct=True),
                opt("NiMH: best energy density and lightest"),
                opt("LCO: safest chemistry of all"),
            ),
            "LFP is prized for safety and long cycle life; LCO has the highest energy but is least safe.",
        ),
        q(
            "A flat OCV-SoC curve (LFP) creates which estimation challenge?",
            (
                opt("A tiny voltage error maps to a huge SoC error", correct=True),
                opt("It makes coulomb counting impossible"),
                opt("It eliminates the need for any SoC estimation"),
                opt("It makes terminal voltage independent of current"),
            ),
            "Because the curve is flat, a millivolt of voltage error maps to a large SoC error, so gauges lean on coulomb counting.",
        ),
        q(
            "Which RC-model statement is correct for terminal voltage under load?",
            (
                opt("Vterm = OCV(SoC) - I*R0 - V1 with tau = R1*C1", correct=True),
                opt("Vterm = OCV(SoC) + I*R0 + V1 with tau = R1/C1"),
                opt("Vterm = OCV(SoC) only, ignoring R0 and V1"),
                opt("Vterm = I*R0 - V1, ignoring OCV"),
            ),
            "The first-order Thevenin model gives Vterm = OCV(SoC) - I*R0 - V1 with polarization time constant tau = R1*C1.",
        ),
        q(
            "Which set of conditions accelerates battery aging?",
            (
                opt("High temperature, high SoC, deep discharge, and high C-rate", correct=True),
                opt("Low temperature, mid SoC, shallow cycling, and low C-rate"),
                opt("Storing cool at a mid charge level"),
                opt("Hiding the top and bottom few percent of the pack"),
            ),
            "Aging accelerates with high temperature, high SoC, deep discharge, and high C-rate; cool storage and shallow cycling extend life.",
        ),
    ),
)
