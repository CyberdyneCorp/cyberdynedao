from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Comparators & the Schmitt trigger": (
            q(
                "What happens to an op-amp's output with no negative feedback (open loop)?",
                (
                    opt("It stays at zero"),
                    opt(
                        "Its huge gain slams the output to a supply rail based on which input is larger",
                        correct=True,
                    ),
                    opt("It oscillates at a fixed frequency"),
                    opt("It acts as a linear amplifier with gain 1"),
                ),
                "Without negative feedback the open-loop gain saturates the output to +/-Vsat depending on which input is higher: a comparator.",
            ),
            q(
                "Why does adding hysteresis (a Schmitt trigger) prevent chatter on a noisy input?",
                (
                    opt("It lowers the op-amp gain to zero"),
                    opt(
                        "It creates two trip points, so noise smaller than the gap cannot flip the output back",
                        correct=True,
                    ),
                    opt("It adds a capacitor that filters all noise"),
                    opt("It converts the comparator into a linear amplifier"),
                ),
                "Positive feedback gives two thresholds; once flipped, the input must reach the other threshold to flip back, so small noise cannot retrigger it.",
            ),
            q(
                "A Schmitt trigger plus an RC network is the basis of which circuit?",
                (
                    opt("A precision rectifier"),
                    opt("A relaxation (square-wave) oscillator", correct=True),
                    opt("A low-pass filter"),
                    opt("A voltage divider"),
                ),
                "Charging an RC between the two hysteresis thresholds produces a square wave: a relaxation oscillator (as in the 555).",
            ),
        ),
        "Precision & nonlinear op-amp circuits": (
            q(
                "How does a precision (active) rectifier remove the diode's 0.7 V dead zone?",
                (
                    opt("It uses a Zener diode instead of a normal one"),
                    opt(
                        "The op-amp's feedback drives its output higher to compensate for the diode drop",
                        correct=True,
                    ),
                    opt("It cools the diode to reduce its drop"),
                    opt("It adds a large series resistor"),
                ),
                "Inside the feedback loop the op-amp raises its output by about the diode drop, so the rectified output has effectively no dead zone.",
            ),
            q(
                "Putting a diode or BJT (with its exponential I-V) in the feedback path gives what function?",
                (
                    opt("A differentiator"),
                    opt(
                        "A logarithmic amplifier (output proportional to ln of the input)",
                        correct=True,
                    ),
                    opt("A linear amplifier with high gain"),
                    opt("A comparator"),
                ),
                "The exponential device in feedback makes Vout proportional to ln(Vin): a log amplifier (antilog if it is in the input path).",
            ),
            q(
                "Why are log/antilog amplifiers useful for analog multiplication?",
                (
                    opt(
                        "Logs turn multiplication into addition: log, add, then antilog",
                        correct=True,
                    ),
                    opt("They double the supply voltage"),
                    opt("They remove all noise from the signals"),
                    opt("They convert AC to DC"),
                ),
                "Adding the logarithms of two signals and taking the antilog multiplies them, which is how analog multipliers and dB/companding circuits work.",
            ),
        ),
        "Biasing transistors: linear & switching modes": (
            q(
                "What is special about a JFET compared with an enhancement MOSFET?",
                (
                    opt("It is current-controlled like a BJT"),
                    opt(
                        "It is a depletion-mode device that is normally ON and pinches off as Vgs goes negative",
                        correct=True,
                    ),
                    opt("It has no gate terminal"),
                    opt("It only works as a switch, never as an amplifier"),
                ),
                "A JFET is a depletion-mode, normally-on FET; making Vgs more negative pinches the channel off at Vp.",
            ),
            q(
                "Why is BJT voltage-divider bias (with an emitter resistor) preferred over fixed-base bias?",
                (
                    opt("It uses fewer components"),
                    opt(
                        "The emitter resistor adds negative feedback, giving a stable beta-independent Q-point",
                        correct=True,
                    ),
                    opt("It removes the need for a power supply"),
                    opt("It makes the transistor switch faster"),
                ),
                "The emitter resistor provides negative feedback so the Q-point resists temperature and beta spread.",
            ),
            q(
                "For a transistor used as a switch, why drive it hard between cut-off and saturation?",
                (
                    opt("To keep it in the linear region for maximum gain"),
                    opt(
                        "Power P=Vce*Ic is lowest fully off or fully on, and highest in the linear region between",
                        correct=True,
                    ),
                    opt("To make it behave like a resistor"),
                    opt("Because the Q-point must sit mid-load-line"),
                ),
                "A switch dissipates least power fully on (low V) or fully off (low I); the linear region in between builds heat.",
            ),
        ),
        "Oscillators": (
            q(
                "What must the loop gain satisfy for sustained oscillation (Barkhausen criterion)?",
                (
                    opt("|A*beta| = 1 and total phase = 0 (or 360) degrees", correct=True),
                    opt("|A*beta| = 0 and phase = 90 degrees"),
                    opt("Infinite gain at all frequencies"),
                    opt("Negative feedback with unity gain"),
                ),
                "Barkhausen: the signal must return the same size (|A*beta|=1) and in phase (0/360 degrees) once around the loop.",
            ),
            q(
                "Which oscillator type is the right choice for a very precise, stable clock frequency?",
                (
                    opt("RC phase-shift oscillator"),
                    opt("Relaxation (555) oscillator"),
                    opt("Crystal oscillator", correct=True),
                    opt("Wien-bridge oscillator"),
                ),
                "A quartz crystal's huge Q gives parts-per-million stability, which is why crystals clock digital systems.",
            ),
            q(
                "How does a harmonic oscillator's output differ from a relaxation (555) oscillator's?",
                (
                    opt("Harmonic oscillators make square waves; relaxation makes sines"),
                    opt(
                        "Harmonic oscillators make clean sine waves; relaxation oscillators make square/triangle waves",
                        correct=True,
                    ),
                    opt("Both produce identical pure sine waves"),
                    opt("Relaxation oscillators cannot be built below 1 MHz"),
                ),
                "RC/LC/crystal oscillators produce sines at the 0-degree-phase frequency; relaxation oscillators charge/discharge a cap for square/triangle waves.",
            ),
        ),
        "Diodes & the PN junction": (
            q(
                "What does a PN junction (a diode) do to current flow?",
                (
                    opt("Conducts equally well in both directions"),
                    opt("Conducts strongly one way and barely the other", correct=True),
                    opt("Blocks current in both directions"),
                    opt("Stores charge like a capacitor"),
                ),
                "A diode is the electronic one-way valve: it conducts strongly one way and barely the other.",
            ),
            q(
                "In the Shockley equation I = Is(e^(V/nVT) - 1), how does diode current grow with voltage?",
                (
                    opt("Linearly"),
                    opt("Exponentially", correct=True),
                    opt("Logarithmically"),
                    opt("As the square of voltage"),
                ),
                "The Shockley equation shows current grows exponentially with forward voltage, giving the sharp knee.",
            ),
            q(
                "Why should you never drive an LED from a voltage source alone?",
                (
                    opt("LEDs only work on AC"),
                    opt(
                        "The exponential I-V curve makes current exquisitely sensitive to voltage, so use a series resistor",
                        correct=True,
                    ),
                    opt("LEDs need a Zener reference to glow"),
                    opt("A voltage source cannot forward bias an LED"),
                ),
                "Because the exponential curve makes current extremely sensitive to voltage and temperature, set the current with a series resistor.",
            ),
        ),
        "Transistors: BJT & MOSFET": (
            q(
                "How is a BJT controlled and what is its active-region collector current?",
                (
                    opt("Voltage controlled, Ic = Vgs/Vth"),
                    opt("Current controlled, Ic = beta times Ib", correct=True),
                    opt("Charge controlled, Ic = Q/t"),
                    opt("Power controlled, Ic = P/Vce"),
                ),
                "A BJT is current controlled: a small base current Ib controls a large collector current Ic = beta times Ib.",
            ),
            q(
                "What controls a MOSFET and turns it on?",
                (
                    opt("A steady gate current above a threshold current"),
                    opt(
                        "The gate voltage Vgs, which turns it on above the threshold Vth",
                        correct=True,
                    ),
                    opt("The base current Ib times beta"),
                    opt("The collector-emitter voltage Vce"),
                ),
                "A MOSFET is voltage controlled: the gate voltage Vgs (with near-zero gate current) turns it on above the threshold Vth.",
            ),
            q(
                "When is a transistor acting as a switch rather than an amplifier?",
                (
                    opt("When biased in the middle of the active region for small wiggles"),
                    opt("When driven hard between cut-off and saturation", correct=True),
                    opt("Only when used as a buffer with gain 1"),
                    opt("Whenever Vgs equals exactly Vth"),
                ),
                "Driven hard between cut-off and saturation it is a switch; biased in the active-region middle it is an amplifier.",
            ),
        ),
        "Operational amplifiers": (
            q(
                "What does the ideal op-amp virtual short rule state under negative feedback?",
                (
                    opt("Large current flows into both inputs"),
                    opt("The output equals the supply voltage"),
                    opt("The op-amp drives its output so the two inputs are equal", correct=True),
                    opt("The two inputs are always shorted to ground"),
                ),
                "With negative feedback the op-amp drives its output until V+ equals V-, the virtual short, and no current flows into the inputs.",
            ),
            q(
                "What is the gain of a non-inverting amplifier?",
                (
                    opt("Minus Rf divided by Rin"),
                    opt("One plus Rf divided by Rin", correct=True),
                    opt("Rf times Rin"),
                    opt("Always exactly one"),
                ),
                "The non-inverting amplifier has gain 1 + Rf/Rin, which is always at least 1.",
            ),
            q(
                "For a 1 MHz gain-bandwidth-product op-amp running at a gain of 100, what is the usable bandwidth?",
                (
                    opt("100 MHz"),
                    opt("1 MHz"),
                    opt("About 10 kHz", correct=True),
                    opt("100 kHz"),
                ),
                "Bandwidth = GBW / gain = 1 MHz / 100 = about 10 kHz.",
            ),
        ),
        "Active filters & analog building blocks": (
            q(
                "What advantage does an active filter have over a passive RC filter?",
                (
                    opt("It needs no power supply"),
                    opt(
                        "It can provide gain in the passband and a buffered, non-loading output",
                        correct=True,
                    ),
                    opt("It only attenuates, never amplifies"),
                    opt("It uses no resistors or capacitors"),
                ),
                "Active filters add gain in the passband and a buffered output that does not load the next stage, unlike passive filters that only attenuate.",
            ),
            q(
                "What does the Sallen-Key stage build from one op-amp and two RC pairs?",
                (
                    opt("A first-order high-pass filter"),
                    opt("A second-order low- or high-pass filter at -40 dB/decade", correct=True),
                    opt("A current-controlled switch"),
                    opt("A bridge rectifier"),
                ),
                "The Sallen-Key stage uses one op-amp and two RC pairs to make a second-order (-40 dB/decade) low- or high-pass filter.",
            ),
            q(
                "Which block amplifies tiny differential sensor signals and rejects noise?",
                (
                    opt("The integrator"),
                    opt("The instrumentation amplifier (three op-amps)", correct=True),
                    opt("The buffer with gain 1"),
                    opt("The differentiator"),
                ),
                "The instrumentation amplifier (three op-amps) amplifies tiny differential sensor signals while rejecting noise.",
            ),
        ),
        "Power electronics: rectifiers, regulators & converters": (
            q(
                "What is the role of the reservoir capacitor after a bridge rectifier?",
                (
                    opt("It rectifies the AC sine"),
                    opt("It smooths the bumpy DC, leaving some ripple", correct=True),
                    opt("It steps the voltage up"),
                    opt("It generates the PWM signal"),
                ),
                "The reservoir capacitor smooths the bumpy rectified DC; a bigger cap or higher frequency leaves less ripple.",
            ),
            q(
                "How does a linear LDO regulator compare to a switching SMPS on efficiency?",
                (
                    opt(
                        "The LDO burns excess voltage as heat and is inefficient at large drops, while an SMPS often hits 90%+",
                        correct=True,
                    ),
                    opt("The LDO is always more efficient than an SMPS"),
                    opt("Both have identical efficiency"),
                    opt("The SMPS burns the excess voltage as heat"),
                ),
                "A linear LDO burns the excess voltage as heat (inefficient at large drops) whereas a switching SMPS often reaches 90%+ efficiency.",
            ),
            q(
                "For a buck converter with Vin = 12 V and duty cycle D = 0.4, what is Vout?",
                (
                    opt("20 V"),
                    opt("4.8 V", correct=True),
                    opt("12 V"),
                    opt("30 V"),
                ),
                "A buck converter gives Vout = D times Vin = 0.4 times 12 = 4.8 V.",
            ),
        ),
        "Lab: half-wave rectifier with smoothing": (
            q(
                "In the lab, what happens to the ripple when you raise the smoothing capacitor C?",
                (
                    opt("The ripple grows"),
                    opt("The ripple shrinks because the reservoir is bigger", correct=True),
                    opt("The output voltage drops to zero"),
                    opt("The mains frequency changes"),
                ),
                "Raising C to 1000e-6 enlarges the reservoir so the ripple shrinks.",
            ),
            q(
                "In the simulation, when does the capacitor follow the input peak?",
                (
                    opt(
                        "When vin minus the diode drop Vd exceeds the cap voltage (diode conducts)",
                        correct=True,
                    ),
                    opt("When the diode blocks"),
                    opt("Only at 50 Hz exactly"),
                    opt("When R drops to 100 ohms"),
                ),
                "When vin minus Vd is greater than vc the diode conducts and the cap follows the peak; otherwise it discharges into R.",
            ),
            q(
                "What does dropping the load resistance R to 100 ohms do?",
                (
                    opt("It eliminates the ripple"),
                    opt(
                        "More load current drains the cap faster, giving more ripple", correct=True
                    ),
                    opt("It doubles the mains frequency"),
                    opt("It removes the diode drop"),
                ),
                "Lower R means more load current drains the cap faster between peaks, which increases the ripple.",
            ),
        ),
        "Practical design, SPICE & measurement": (
            q(
                "What does SPICE do that the Basics lab did, but extended?",
                (
                    opt(
                        "Nodal analysis, but with nonlinear device models across DC, AC, and transient",
                        correct=True,
                    ),
                    opt("Only measures voltage on a real bench"),
                    opt("Generates AC mains power"),
                    opt("Replaces the need for any resistors"),
                ),
                "SPICE does nodal analysis like the Basics lab but adds nonlinear device models across DC, AC, and transient analyses.",
            ),
            q(
                "Why place decoupling capacitors next to every chip's power pins?",
                (
                    opt("To rectify the supply AC"),
                    opt(
                        "So the chip can draw fast current locally instead of through inductive traces",
                        correct=True,
                    ),
                    opt("To increase thermal noise"),
                    opt("To raise the supply voltage"),
                ),
                "Decoupling caps next to the power pins let a chip draw fast current locally rather than through inductive traces.",
            ),
            q(
                "Which bench instrument is your window into transients and ripple (voltage vs. time)?",
                (
                    opt("The multimeter"),
                    opt("The oscilloscope", correct=True),
                    opt("The function generator"),
                    opt("The power supply"),
                ),
                "The oscilloscope shows voltage vs. time, making it your window into transients and ripple.",
            ),
        ),
    },
    final=(
        q(
            "Which diode conducts in reverse at a precise voltage to make a simple voltage reference?",
            (
                opt("Schottky"),
                opt("Zener", correct=True),
                opt("LED"),
                opt("Photodiode"),
            ),
            "A Zener diode conducts in reverse at a precise voltage, making a simple voltage reference or regulator.",
        ),
        q(
            "What is the key control difference between a BJT and a MOSFET?",
            (
                opt("BJT is voltage controlled, MOSFET is current controlled"),
                opt(
                    "BJT is current controlled (Ic = beta Ib), MOSFET is voltage controlled (Vgs vs Vth)",
                    correct=True,
                ),
                opt("Both are controlled by collector-emitter voltage"),
                opt("Neither can be used as a switch"),
            ),
            "A BJT is current controlled with Ic = beta times Ib; a MOSFET is voltage controlled by Vgs relative to the threshold Vth.",
        ),
        q(
            "What is the gain of an inverting amplifier?",
            (
                opt("One plus Rf divided by Rin"),
                opt("Minus Rf divided by Rin", correct=True),
                opt("Rf times Rin"),
                opt("Always exactly minus one"),
            ),
            "The inverting amplifier has gain minus Rf/Rin and sets a virtual ground at the inverting input.",
        ),
        q(
            "For a boost converter, how is the output voltage related to Vin and duty cycle D?",
            (
                opt("Vout = D times Vin"),
                opt("Vout = Vin divided by (1 - D)", correct=True),
                opt("Vout = Vin minus D"),
                opt("Vout = Vin times (1 - D)"),
            ),
            "A boost converter steps voltage up: Vout = Vin / (1 - D).",
        ),
        q(
            "What knob does PWM adjust to control a switching converter's output?",
            (
                opt("The diode drop Vd"),
                opt("The duty cycle D of the switch", correct=True),
                opt("The reservoir capacitor value"),
                opt("The op-amp gain-bandwidth product"),
            ),
            "PWM varies the duty cycle D driving the switch, and a feedback loop adjusts D to hold Vout steady.",
        ),
    ),
)
