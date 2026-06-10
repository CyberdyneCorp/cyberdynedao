from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Sensors & transducers overview": (
            q(
                "In the ideal sensor transfer function y = S x + b, what does S represent?",
                (
                    opt("the offset of the output"),
                    opt("the sensitivity, output per unit input", correct=True),
                    opt("the measurable range or span"),
                    opt("the hysteresis error"),
                ),
                "S is the sensitivity: the output per unit input, such as mV per degree C. The steeper the line, the more sensitive the sensor.",
            ),
            q(
                "What is the difference between a sensor and a transducer?",
                (
                    opt("A transducer is electrical while a sensor is mechanical"),
                    opt("They are unrelated devices"),
                    opt(
                        "A transducer converts one form of energy to another, and every sensor is a transducer",
                        correct=True,
                    ),
                    opt("A sensor always outputs a digital signal"),
                ),
                "A transducer is the broader term for any device that converts one form of energy to another, and every sensor is a transducer.",
            ),
            q(
                "Why does the lesson stress checking the range or span of a sensor first?",
                (
                    opt(
                        "Because outside its span the sensor saturates or breaks and its readings are garbage",
                        correct=True,
                    ),
                    opt("Because range determines the sensor color code"),
                    opt("Because the span sets the sensor sensitivity directly"),
                    opt("Because range is unrelated to accuracy"),
                ),
                "A sensor measuring outside its span saturates or breaks, so the numbers it returns are garbage; always check range first.",
            ),
        ),
        "Signal conditioning": (
            q(
                "What are the three core jobs of signal conditioning between a sensor and the ADC?",
                (
                    opt("Sampling, quantization, and encoding"),
                    opt("Amplification, filtering, and level shifting", correct=True),
                    opt("Calibration, averaging, and grounding"),
                    opt("Modulation, rectification, and storage"),
                ),
                "Signal conditioning amplifies a small signal, filters out high-frequency noise, and level-shifts it into the ADC input window.",
            ),
            q(
                "Why does the lesson recommend amplifying the sensor signal early, close to the sensor?",
                (
                    opt("Because op-amps only work near sensors"),
                    opt("Because early amplification reduces the cable cost"),
                    opt(
                        "Once noise rides on a tiny signal no later amplifier can separate them, so gain first then send the bigger signal",
                        correct=True,
                    ),
                    opt("Because the ADC requires a negative voltage"),
                ),
                "Once noise rides on a tiny signal, no later amplifier can separate them, so you amplify early and send the bigger signal down the wire.",
            ),
            q(
                "What is the RC cutoff frequency of the low-pass filter used in conditioning?",
                (
                    opt("fc = 2 pi R C"),
                    opt("fc = R C / (2 pi)"),
                    opt("fc = 1 / (2 pi R C)", correct=True),
                    opt("fc = 1 / (R + C)"),
                ),
                "The RC low-pass cutoff is fc = 1 / (2 pi R C), and it doubles as the anti-aliasing filter before sampling.",
            ),
        ),
        "Bridges & resistive sensors": (
            q(
                "Why is the Wheatstone bridge so useful for resistive sensors?",
                (
                    opt("It increases the baseline resistance of the sensor"),
                    opt(
                        "It turns a tiny resistance change into a clean differential voltage starting from zero",
                        correct=True,
                    ),
                    opt("It removes the need for an excitation voltage"),
                    opt("It converts resistance directly into a digital code"),
                ),
                "When balanced the bridge output is zero, so a small resistance change produces a clean differential voltage starting from zero that you then amplify.",
            ),
            q(
                "For a metal foil strain gauge, the gauge factor GF is approximately what value?",
                (
                    opt("about 0.5"),
                    opt("about 2", correct=True),
                    opt("about 10"),
                    opt("about 100"),
                ),
                "The gauge factor GF is about 2 for metal foil and links strain to resistance change via dR/R = GF times strain.",
            ),
            q(
                "Why does the lesson recommend a half or full bridge over a quarter bridge when possible?",
                (
                    opt("It needs a smaller excitation voltage"),
                    opt("It removes the need for amplification"),
                    opt(
                        "It doubles or quadruples sensitivity and cancels temperature drift because all arms drift together",
                        correct=True,
                    ),
                    opt("It makes the thermistor perfectly linear"),
                ),
                "Using two or four active gauges doubles or quadruples sensitivity and cancels temperature drift because all arms drift together.",
            ),
        ),
        "Measurement fundamentals": (
            q(
                "How do accuracy and precision differ?",
                (
                    opt(
                        "Accuracy is closeness to the true value while precision is closeness of repeated readings to each other",
                        correct=True,
                    ),
                    opt(
                        "Accuracy is closeness of repeated readings while precision is closeness to the true value"
                    ),
                    opt("They mean the same thing"),
                    opt("Accuracy applies only to digital instruments"),
                ),
                "Accuracy is how close readings are to the true value, while precision is how close repeated readings are to each other regardless of correctness.",
            ),
            q(
                "Which type of error can you average down rather than calibrate out?",
                (
                    opt("Systematic error"),
                    opt("Random error, since precision improves as 1 over sqrt(N)", correct=True),
                    opt("Quantization error from the SI units"),
                    opt("Hysteresis error"),
                ),
                "Random error can be averaged away with precision improving as 1 over sqrt(N), while systematic error must be calibrated out.",
            ),
            q(
                "What is the approximate resolution of a 12-bit ADC over a 3.3 V range?",
                (
                    opt("about 0.8 mV", correct=True),
                    opt("about 3.3 mV"),
                    opt("about 12 mV"),
                    opt("about 0.08 mV"),
                ),
                "Resolution is 3.3 V divided by 2 to the 12th, which is about 0.8 mV per LSB.",
            ),
        ),
        "Noise & grounding in measurement": (
            q(
                "What is the single best defence against common-mode interference described in the lesson?",
                (
                    opt("Increasing the sensor excitation voltage"),
                    opt(
                        "Measuring differentially, reading the difference between two wires routed together",
                        correct=True,
                    ),
                    opt("Lowering the sample rate"),
                    opt("Using a longer unshielded cable"),
                ),
                "Measuring differentially cancels common-mode interference because it couples almost equally into both wires, so the difference cancels it.",
            ),
            q(
                "Thermal (Johnson) noise increases with which set of factors?",
                (
                    opt("Resistance, bandwidth, and temperature", correct=True),
                    opt("Sample rate, gain, and cable length"),
                    opt("Capacitance, current, and frequency"),
                    opt("Offset, span, and hysteresis"),
                ),
                "Thermal noise follows vn = sqrt(4 kB T R df), so its floor rises with resistance, bandwidth, and temperature.",
            ),
            q(
                "To avoid a ground loop, how should a cable shield be grounded?",
                (
                    opt("At both ends for redundancy"),
                    opt("At one end only", correct=True),
                    opt("Never grounded at all"),
                    opt("Through every device on the bus"),
                ),
                "A shield should be grounded at one end only to avoid forming a ground loop; a single-point or star ground also cures loops.",
            ),
        ),
        "Lab: Wheatstone bridge & sensor linearization": (
            q(
                "In the lab, how is the NTC thermistor read before linearization?",
                (
                    opt("Directly as a four-arm full bridge"),
                    opt("As the top half of a divider with a fixed 10k resistor", correct=True),
                    opt("Through an I2C digital interface"),
                    opt("By measuring its excitation current"),
                ),
                "The lab reads the thermistor as the top half of a voltage divider with a fixed 10k resistor, giving a divider voltage nonlinear in temperature.",
            ),
            q(
                "What does the lab fit to recover temperature from the divider voltage?",
                (
                    opt("A linear two-point calibration"),
                    opt("A cubic polynomial via np.polyfit", correct=True),
                    opt("A Kalman filter"),
                    opt("A moving-average filter"),
                ),
                "The lab fits a cubic polynomial with np.polyfit so temperature is recovered as a function of the divider voltage.",
            ),
            q(
                "According to the try-it-yourself notes, fitting a quadratic instead of a cubic will do what?",
                (
                    opt("Make max_err grow", correct=True),
                    opt("Eliminate the bridge output entirely"),
                    opt("Double the gauge factor"),
                    opt("Remove all temperature dependence"),
                ),
                "The notes say fitting a quadratic instead of a cubic makes max_err grow, since the lower-order fit tracks the curve less well.",
            ),
        ),
    },
    final=(
        q(
            "Which ordering correctly describes the front-end measurement chain in the Basics course?",
            (
                opt("ADC, then sensor, then amplify, then filter"),
                opt("Sensor, then amplify, then filter, then level shift, then ADC", correct=True),
                opt("Filter, then sensor, then ADC, then amplify"),
                opt("Sensor, then ADC, then amplify, then filter"),
            ),
            "Signal conditioning sits between the sensor and the ADC and amplifies, filters, then level-shifts before the ADC.",
        ),
        q(
            "A quarter-bridge with one varying arm produces an output that is best described how?",
            (
                opt("Exactly linear in the fractional change for all values"),
                opt("Nearly linear in the fractional change dR/R but bends slightly", correct=True),
                opt("Completely independent of the resistance change"),
                opt("Zero regardless of the resistance change"),
            ),
            "For one varying arm the output is nearly linear in the fractional change dR/R but bends slightly, which is why the linear x/4 approximation diverges at the extremes.",
        ),
        q(
            "You take repeated readings and they cluster tightly but are all offset from the true value. What do you have and how do you fix it?",
            (
                opt("Random error, fixed by averaging"),
                opt("Systematic error (bias), fixed by calibration", correct=True),
                opt("Quantization error, fixed by oversampling"),
                opt("Hysteresis, fixed by shielding"),
            ),
            "A tight but offset cluster is precise yet biased, which is systematic error you calibrate out rather than average away.",
        ),
        q(
            "Which combination best fights mains hum on a small sensor signal, per the noise lesson?",
            (
                opt("Single-ended measurement with a long unshielded cable"),
                opt(
                    "Differential measurement with a high-CMRR instrumentation amplifier and a single-point ground",
                    correct=True,
                ),
                opt("Raising the ADC reference voltage"),
                opt("Grounding the shield at both ends"),
            ),
            "Mains hum is common-mode, so a differential measurement with a high-CMRR instrumentation amplifier plus a single-point star ground rejects it best.",
        ),
        q(
            "Why does a thermocouple signal need amplification before the ADC?",
            (
                opt(
                    "Because it outputs only microvolts per degree, too small for the ADC range",
                    correct=True,
                ),
                opt("Because it outputs a digital code that must be decoded"),
                opt("Because it swings far above the ADC input window"),
                opt("Because it is perfectly linear and needs no conditioning"),
            ),
            "A thermocouple puts out only microvolts per degree, which is useless until amplified to use the ADC full range.",
        ),
    ),
)
