from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is power electronics? A short history": (
            q(
                "Which of the four basic power conversions is performed by a rectifier?",
                (
                    opt("DC to DC"),
                    opt("AC to DC", correct=True),
                    opt("DC to AC"),
                    opt("AC to AC"),
                ),
                "A rectifier converts AC to DC. DC-DC is a converter, DC-AC is an inverter, and AC-AC is a cycloconverter or matrix converter.",
            ),
            q(
                "Why does a switching converter achieve much higher efficiency than a linear regulator?",
                (
                    opt("It drops the excess voltage across a transistor as heat"),
                    opt(
                        "It keeps the switch either fully on or fully off, both low-loss states, and filters with L and C",
                        correct=True,
                    ),
                    opt("It uses a larger resistor to share the load"),
                    opt("Its efficiency equals the output-to-input voltage ratio"),
                ),
                "A switcher toggles the switch fully on or fully off (low loss) and uses an inductor and capacitor to deliver a smooth output, reaching 90 to 98 percent. The linear regulator wastes the dropped voltage as heat.",
            ),
            q(
                "Which device was the first solid-state controllable power switch, ruling high-power AC control for decades?",
                (
                    opt("The power MOSFET"),
                    opt("The IGBT"),
                    opt("The thyristor (SCR)", correct=True),
                    opt("The GaN transistor"),
                ),
                "The thyristor (SCR), introduced in 1957, was the first solid-state controllable power switch. The MOSFET (1970s) and IGBT (1980s) came later.",
            ),
        ),
        "The ideal switch & real power devices": (
            q(
                "What characterizes the ideal switch that real power devices try to approximate?",
                (
                    opt(
                        "Zero voltage drop when on, zero current when off, instantaneous switching, so zero loss",
                        correct=True,
                    ),
                    opt("A fixed forward voltage drop of 0.7 V"),
                    opt("A constant on-resistance that dissipates I squared R"),
                    opt("A slow but rugged latching turn-on"),
                ),
                "The ideal switch has zero voltage drop when on, zero current when off, and switches instantaneously, giving zero loss. Real devices fall short, and that gap is where losses live.",
            ),
            q(
                "Which device family is best matched to very high power AC applications such as the grid and rail?",
                (
                    opt("MOSFET"),
                    opt("GaN"),
                    opt("Thyristor / SCR", correct=True),
                    opt("Diode"),
                ),
                "Thyristors (SCRs) are slow but handle enormous power and are rugged, making them the choice for very high power AC such as grid and rail. MOSFETs and GaN suit low-voltage high-frequency work.",
            ),
            q(
                "How does switching loss differ from conduction loss in a power device?",
                (
                    opt(
                        "Switching loss occurs while the device is fully on, conduction loss during transitions"
                    ),
                    opt(
                        "Switching loss happens during on/off transitions and grows with switching frequency, while conduction loss occurs while the device conducts",
                        correct=True,
                    ),
                    opt("Both are independent of switching frequency"),
                    opt("Conduction loss only happens at turn-off"),
                ),
                "Switching loss comes from the voltage and current overlapping during the brief transition each cycle, so it grows with switching frequency. Conduction loss (I squared R or V times I) occurs while the device conducts.",
            ),
        ),
        "PWM: controlling power by switching": (
            q(
                "For a PWM signal switching between 0 and Vin, what is the average output voltage?",
                (
                    opt("Vin divided by D"),
                    opt("D times Vin", correct=True),
                    opt("Vin minus D"),
                    opt("D squared times Vin"),
                ),
                "The average of a PWM signal that toggles between 0 and Vin is Vavg = D times Vin, where D is the duty cycle (on-time fraction) between 0 and 1.",
            ),
            q(
                "What recovers the smooth DC average from the switched PWM waveform with almost no loss?",
                (
                    opt("A series resistor"),
                    opt(
                        "A low-pass LC filter that passes the DC average and blocks the switching ripple",
                        correct=True,
                    ),
                    opt("A larger gate driver"),
                    opt("A second switch in parallel"),
                ),
                "A low-pass LC filter passes the DC average and blocks the switching ripple, and because an inductor and capacitor store energy rather than burning it, there is almost no loss.",
            ),
            q(
                "What is the effect of raising the switching frequency fsw?",
                (
                    opt("It allows a smaller L and C but increases switching loss", correct=True),
                    opt("It requires a larger L and C and reduces switching loss"),
                    opt("It has no effect on filter size or loss"),
                    opt("It eliminates the need for an LC filter"),
                ),
                "Higher fsw lets the filter inductor and capacitor be smaller, but it raises switching loss, which is the central trade-off.",
            ),
        ),
        "Rectifiers: AC to DC": (
            q(
                "How many diodes does a single-phase bridge rectifier use?",
                (
                    opt("1"),
                    opt("2"),
                    opt("4", correct=True),
                    opt("6"),
                ),
                "The standard single-phase bridge rectifier uses 4 diodes. A half-wave uses 1, a full-wave center-tap uses 2, and a three-phase bridge uses 6.",
            ),
            q(
                "Compared with a half-wave rectifier on the same line, what is the ripple frequency of a full-wave or bridge rectifier?",
                (
                    opt("Half the line frequency"),
                    opt("Equal to the line frequency"),
                    opt("Twice the line frequency", correct=True),
                    opt("Six times the line frequency"),
                ),
                "A full-wave or bridge rectifier produces ripple at twice the line frequency, so a smaller reservoir capacitor suffices for the same ripple. Half-wave ripples at the line frequency; a three-phase bridge at six times.",
            ),
            q(
                "Why does a capacitor-input rectifier give a poor power factor?",
                (
                    opt("It draws current in narrow spikes at the voltage peaks", correct=True),
                    opt("It draws a perfectly sinusoidal current"),
                    opt("It uses thyristors instead of diodes"),
                    opt("It has no reservoir capacitor"),
                ),
                "A cap-input rectifier draws current in narrow spikes at the voltage peaks, giving a poor power factor and harmonic current, which is why high-power supplies add power-factor correction.",
            ),
        ),
        "Introduction to the buck converter": (
            q(
                "What is the output voltage of an ideal buck converter?",
                (
                    opt("Vin divided by (1 minus D)"),
                    opt("D times Vin", correct=True),
                    opt("Vin divided by D"),
                    opt("negative D over (1 minus D) times Vin"),
                ),
                "The buck converter steps down, with Vout = D times Vin. The boost gives Vin over (1 minus D) and the buck-boost gives the inverted ratio.",
            ),
            q(
                "What carries the inductor current when the buck converter switch turns off?",
                (
                    opt("The input source directly"),
                    opt("The freewheeling diode", correct=True),
                    opt("The gate driver"),
                    opt("A series resistor"),
                ),
                "When the switch turns off, the inductor current keeps flowing through the freewheeling diode, releasing the inductor's stored energy to the load.",
            ),
            q(
                "Why is the buck converter efficient compared with a linear regulator?",
                (
                    opt("It drops the excess voltage across a resistive element"),
                    opt(
                        "The switch is either on with tiny Rds-on loss or off, and the inductor and capacitor store and release energy without dissipating it",
                        correct=True,
                    ),
                    opt("It runs at a very low switching frequency"),
                    opt("It avoids using any inductor or capacitor"),
                ),
                "The buck never drops the excess voltage across a resistive element; the switch is on (tiny Rds-on loss) or off, and the inductor and capacitor store and release energy, so real bucks hit 90 to 95 percent or more.",
            ),
        ),
        "Lab: PWM and average voltage": (
            q(
                "In the lab, what does multiplying Vin by the boolean ((t*fsw) % 1.0) < D produce?",
                (
                    opt("A sine wave at frequency fsw"),
                    opt(
                        "A PWM signal that is high for the first fraction D of each switching period",
                        correct=True,
                    ),
                    opt("A constant DC level of D times Vin"),
                    opt("A triangle carrier waveform"),
                ),
                "The expression is high during the first fraction D of each switching period, so multiplying by Vin gives a PWM waveform that toggles between Vin and 0.",
            ),
            q(
                "What role does the first-order RC averaging loop play in the lab?",
                (
                    opt(
                        "It models the LC filter's job of recovering the average from the PWM",
                        correct=True,
                    ),
                    opt("It generates the switching frequency"),
                    opt("It increases the duty cycle over time"),
                    opt("It measures the gate-drive current"),
                ),
                "The RC averaging loop models the low-pass LC filter, recovering the smooth average (near D times Vin) from the switched PWM signal.",
            ),
            q(
                "According to the lab, setting D = 0.75 with Vin = 12 V makes the filtered average rise to about what value?",
                (
                    opt("3 V"),
                    opt("4.2 V"),
                    opt("9 V", correct=True),
                    opt("12 V"),
                ),
                "With D = 0.75 and Vin = 12 V, the average D times Vin equals 9 V, as the lab's try-it-yourself step notes.",
            ),
        ),
    },
    final=(
        q(
            "Which sequence of conversions describes a variable-speed AC motor drive?",
            (
                opt("AC to DC only"),
                opt("DC to AC only"),
                opt("AC to DC to AC", correct=True),
                opt("DC to DC to DC"),
            ),
            "A variable-speed motor drive rectifies the mains (AC to DC) and then inverts the DC bus to adjustable-frequency AC, an AC to DC to AC chain.",
        ),
        q(
            "Which statement about the duty cycle D is correct across PWM and the buck converter?",
            (
                opt("D ranges from 0 to 1 and the average output is D times Vin", correct=True),
                opt("D can exceed 1 to boost the output above Vin"),
                opt("D sets the switching frequency"),
                opt("D is the ratio of off-time to total period"),
            ),
            "The duty cycle D is the on-time fraction, between 0 and 1, and the average (and ideal buck output) is D times Vin.",
        ),
        q(
            "Which device best fits high-voltage, high-current motor drives and EV traction?",
            (
                opt("Diode"),
                opt("IGBT", correct=True),
                opt("Thyristor / SCR"),
                opt("Schottky diode"),
            ),
            "The IGBT marries MOSFET-style gate-voltage drive with bipolar current handling, making it the sweet spot for medium-to-high voltage and current such as motor drives and EVs.",
        ),
        q(
            "A bridge rectifier feeds a reservoir capacitor. Why does its ripple frequency being twice the line frequency help?",
            (
                opt("It lets a smaller capacitor achieve the same ripple", correct=True),
                opt("It increases the power factor to unity"),
                opt("It removes the need for any capacitor"),
                opt("It doubles the output voltage"),
            ),
            "Full-wave and bridge rectifiers ripple at twice the line frequency, and since Vripple is roughly Iload over (fripple times C), a higher ripple frequency means a smaller cap suffices for the same ripple.",
        ),
        q(
            "What is the throughline of the whole power-electronics field as the course frames it?",
            (
                opt("Drop excess voltage across a transistor and dissipate it as heat"),
                opt(
                    "Switch fully on and off, filter with L and C, control the duty cycle to set the output, and manage the heat",
                    correct=True,
                ),
                opt("Use only linear regulators to keep the output clean"),
                opt("Avoid switching to eliminate EMI entirely"),
            ),
            "The course's throughline is to switch fast between fully on and fully off, filter the result with L and C, control the duty cycle (or frequency) to set the output, and manage the heat that switching creates.",
        ),
    ),
)
