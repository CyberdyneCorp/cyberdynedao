from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Capacitors & inductors": (
            q(
                "What is the current-voltage law for a capacitor C?",
                (
                    opt("v = L di/dt"),
                    opt("i = C dv/dt", correct=True),
                    opt("v = i R"),
                    opt("i = v / C"),
                ),
                "A capacitor obeys i = C dv/dt; the inductor dual is v = L di/dt.",
            ),
            q(
                "Charging a capacitor through a resistor R, what is the time constant?",
                (
                    opt("tau = L/R"),
                    opt("tau = R/C"),
                    opt("tau = RC", correct=True),
                    opt("tau = 1/(RC)"),
                ),
                "For an RC charge, tau = RC; after tau the voltage reaches about 63 percent.",
            ),
            q(
                "Which quantity can a capacitor NOT change instantaneously?",
                (
                    opt("its voltage", correct=True),
                    opt("its current"),
                    opt("its capacitance"),
                    opt("its stored charge per coulomb"),
                ),
                "A capacitor resists voltage change so its voltage cannot jump; an inductor resists current change.",
            ),
        ),
        "First-order transients: RC & RL": (
            q(
                "What is the time constant of a first-order RL circuit?",
                (
                    opt("tau = RC"),
                    opt("tau = L/R", correct=True),
                    opt("tau = R/L"),
                    opt("tau = LC"),
                ),
                "For RL the time constant is tau = L/R; for RC it is tau = RC.",
            ),
            q(
                "The universal first-order response is x(t) = x_inf + (x0 - x_inf) e^(-t/tau). What is x0?",
                (
                    opt("the final steady value"),
                    opt("the time constant"),
                    opt("the initial value at t = 0", correct=True),
                    opt("the rate of change"),
                ),
                "x0 is the initial value and x_inf the final value; the response relaxes exponentially between them.",
            ),
            q(
                "Why do you place a flyback diode across an inductive coil like a relay?",
                (
                    opt("to give the inductor current a path when the switch opens", correct=True),
                    opt("to increase the time constant RC"),
                    opt("to block DC current through the coil"),
                    opt("to make the capacitor voltage jump"),
                ),
                "Opening a switch on an inductor makes v = L di/dt spike; a flyback diode gives the current somewhere to go.",
            ),
        ),
        "AC circuits, phasors & impedance": (
            q(
                "What is the impedance of a capacitor in AC steady state?",
                (
                    opt("Zc = j w C"),
                    opt("Zc = 1/(j w C)", correct=True),
                    opt("Zc = j w L"),
                    opt("Zc = R"),
                ),
                "A capacitor's impedance is Zc = 1/(j w C); an inductor's is Zl = j w L.",
            ),
            q(
                "How does the impedance magnitude of an inductor behave with frequency?",
                (
                    opt("it rises with frequency", correct=True),
                    opt("it falls with frequency"),
                    opt("it is flat with frequency"),
                    opt("it is always zero"),
                ),
                "An inductor's |Z| = 2 pi f L rises with f, while a capacitor's |Z| = 1/(2 pi f C) falls with f.",
            ),
            q(
                "In an AC circuit, how does a capacitor's current relate to its voltage?",
                (
                    opt("current lags voltage by 90 degrees"),
                    opt("current leads voltage by 90 degrees", correct=True),
                    opt("current is in phase with voltage"),
                    opt("current leads voltage by 45 degrees"),
                ),
                "A capacitor's current leads its voltage by 90 degrees; an inductor's current lags by 90 degrees (ELI the ICE man).",
            ),
        ),
        "RLC resonance & the Q factor": (
            q(
                "What is the resonant angular frequency of an RLC circuit?",
                (
                    opt("w0 = 1/sqrt(LC)", correct=True),
                    opt("w0 = sqrt(LC)"),
                    opt("w0 = 1/(RC)"),
                    opt("w0 = R/L"),
                ),
                "At resonance the L and C impedances cancel, giving w0 = 1/sqrt(LC) and f0 = 1/(2 pi sqrt(LC)).",
            ),
            q(
                "What is the bandwidth of a series RLC resonance in terms of f0 and Q?",
                (
                    opt("bandwidth = f0 * Q"),
                    opt("bandwidth = Q / f0"),
                    opt("bandwidth = f0 / Q", correct=True),
                    opt("bandwidth = f0 * Q^2"),
                ),
                "The bandwidth is f0 / Q; higher Q means a narrower, sharper peak.",
            ),
            q(
                "How does the quality factor Q relate to the damping ratio zeta?",
                (
                    opt("zeta = 2 Q"),
                    opt("zeta = 1/(2 Q)", correct=True),
                    opt("zeta = Q"),
                    opt("zeta = Q / 2"),
                ),
                "zeta = 1/(2Q); high Q means lightly damped and rings, low Q means heavily damped.",
            ),
        ),
        "Frequency response & passive filters": (
            q(
                "What is the cutoff frequency of an RC low-pass filter?",
                (
                    opt("fc = 1/(2 pi R C)", correct=True),
                    opt("fc = 2 pi R C"),
                    opt("fc = 1/sqrt(LC)"),
                    opt("fc = R C"),
                ),
                "The -3 dB cutoff is fc = 1/(2 pi R C), where the output is down to 1/sqrt(2).",
            ),
            q(
                "Beyond the cutoff, how fast does a first-order RC filter roll off?",
                (
                    opt("-3 dB/decade"),
                    opt("-20 dB/decade", correct=True),
                    opt("-40 dB/decade"),
                    opt("-6 dB/octave per order squared"),
                ),
                "A first-order filter rolls off at -20 dB/decade per order beyond the cutoff.",
            ),
            q(
                "How do you turn an RC low-pass into a high-pass filter?",
                (
                    opt("swap the positions of R and C", correct=True),
                    opt("increase the resistor value only"),
                    opt("add a flyback diode"),
                    opt("set the cutoff to zero"),
                ),
                "Swapping R and C gives a high-pass; cascading or using RLC gives band-pass and band-stop.",
            ),
        ),
        "Lab: RLC transient & resonance": (
            q(
                "In the lab, what does a low series resistance R (high Q) produce in the step response?",
                (
                    opt("under-damped ringing", correct=True),
                    opt("over-damped slow rise"),
                    opt("no response at all"),
                    opt("a flat DC level"),
                ),
                "Low R gives high Q and under-damped ringing; high R gives an over-damped, non-ringing response.",
            ),
            q(
                "The lab integrates the state using which two state variables?",
                (
                    opt("capacitor voltage vc and inductor current iL", correct=True),
                    opt("resistor voltage and source current"),
                    opt("frequency and phase"),
                    opt("capacitance and inductance"),
                ),
                "The Euler integration tracks capacitor voltage vc and inductor current iL over time.",
            ),
            q(
                "What does increasing R toward R=300 do in the lab plot?",
                (
                    opt("makes the response over-damped with no ringing", correct=True),
                    opt("increases the ringing amplitude"),
                    opt("raises the resonant frequency f0"),
                    opt("makes Q very large"),
                ),
                "Large R lowers Q and over-damps the circuit, so the capacitor voltage rises smoothly without ringing.",
            ),
        ),
    },
    final=(
        q(
            "Which pair correctly gives the capacitor and inductor laws?",
            (
                opt("i = C dv/dt and v = L di/dt", correct=True),
                opt("v = C di/dt and i = L dv/dt"),
                opt("i = L dv/dt and v = C di/dt"),
                opt("i = v/C and v = i/L"),
            ),
            "A capacitor obeys i = C dv/dt and an inductor v = L di/dt.",
        ),
        q(
            "A first-order RC circuit and an RL circuit have time constants of:",
            (
                opt("RC and L/R respectively", correct=True),
                opt("L/R and RC respectively"),
                opt("RC and R/L respectively"),
                opt("LC and RC respectively"),
            ),
            "RC circuits use tau = RC and RL circuits use tau = L/R.",
        ),
        q(
            "At resonance in a series RLC, what happens?",
            (
                opt(
                    "the L and C impedances cancel, giving minimum impedance and maximum current",
                    correct=True,
                ),
                opt("the impedance is maximum and current is zero"),
                opt("the capacitor voltage jumps instantly"),
                opt("the time constant becomes infinite"),
            ),
            "At w0 = 1/sqrt(LC) a series RLC is purely resistive: minimum impedance, maximum current.",
        ),
        q(
            "Which describes an RC low-pass filter correctly?",
            (
                opt("cutoff fc = 1/(2 pi R C), rolling off at -20 dB/decade", correct=True),
                opt("cutoff fc = 2 pi R C, rolling off at -3 dB/decade"),
                opt("cutoff fc = 1/sqrt(LC), rolling off at -40 dB/decade"),
                opt("cutoff fc = RC, with no roll-off"),
            ),
            "An RC low-pass has fc = 1/(2 pi R C) and a first-order -20 dB/decade roll-off beyond cutoff.",
        ),
        q(
            "How are the quality factor Q and damping ratio zeta related in a series RLC?",
            (
                opt("zeta = 1/(2 Q), so high Q rings and low Q is heavily damped", correct=True),
                opt("zeta = 2 Q, so high Q is heavily damped"),
                opt("zeta = Q, so they are equal"),
                opt("zeta = f0 / Q, the bandwidth"),
            ),
            "zeta = 1/(2Q): high Q is lightly damped and rings, low Q is heavily damped; bandwidth is f0/Q.",
        ),
    ),
)
