from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Modeling & transfer functions": (
            q(
                "What does a transfer function G(s) represent?",
                (
                    opt("The system output minus its input over time"),
                    opt("Output over input as a ratio of polynomials in s", correct=True),
                    opt("The integral of the input signal only"),
                    opt("A list of the measured states of the plant"),
                ),
                "A transfer function is Y(s)/U(s), output over input as a ratio of polynomials in s.",
            ),
            q(
                "In the closed-loop transfer function T(s) = C(s)G(s) / (1 + C(s)G(s)), what do the roots of the denominator give?",
                (
                    opt("The open-loop zeros"),
                    opt("The closed-loop poles", correct=True),
                    opt("The numerator polynomial coefficients"),
                    opt("The steady-state gain"),
                ),
                "The denominator 1 + C(s)G(s) has roots that are the closed-loop poles, and they decide everything.",
            ),
            q(
                "What do poles versus zeros control in a transfer function?",
                (
                    opt("Poles shape input coupling; zeros set the dynamics"),
                    opt(
                        "Poles set the dynamics (speed and damping); zeros shape how inputs couple in",
                        correct=True,
                    ),
                    opt("Both poles and zeros set only the steady-state error"),
                    opt("Neither affects speed or damping"),
                ),
                "Poles (denominator roots) set the dynamics, speed and damping; zeros (numerator roots) shape how inputs couple in.",
            ),
        ),
        "Stability & the characteristic equation": (
            q(
                "A continuous LTI system is stable if and only if every pole has what property?",
                (
                    opt("A positive real part"),
                    opt("A negative real part (sits in the left half-plane)", correct=True),
                    opt("Zero imaginary part"),
                    opt("A magnitude greater than one"),
                ),
                "Stability requires every pole to have a negative real part, sitting in the left half of the s-plane.",
            ),
            q(
                "What does the Routh-Hurwitz criterion let you check?",
                (
                    opt("The exact value of every closed-loop pole"),
                    opt(
                        "Whether any pole strays into the right half-plane, from the coefficients alone",
                        correct=True,
                    ),
                    opt("The frequency response magnitude at crossover"),
                    opt("The numerator zeros of the plant"),
                ),
                "Routh-Hurwitz answers whether any pole is in the right half-plane from the coefficients alone, with no root-finding.",
            ),
            q(
                "According to the lesson, what is the number one hidden cause of instability on real hardware?",
                (
                    opt(
                        "Time delay from sensors, computation, and actuators eating phase",
                        correct=True,
                    ),
                    opt("Too many zeros in the numerator"),
                    opt("A perfectly modeled plant"),
                    opt("Using the Routh-Hurwitz criterion"),
                ),
                "Real loops have time delay that eats phase and is the number one hidden cause of instability.",
            ),
        ),
        "The root locus": (
            q(
                "What does the root locus trace as you vary a single gain K?",
                (
                    opt("The frequency response magnitude"),
                    opt("The paths the closed-loop poles trace through the s-plane", correct=True),
                    opt("The open-loop zeros only"),
                    opt("The steady-state error versus time"),
                ),
                "The root locus is the map of paths the closed-loop poles trace through the s-plane as gain K increases.",
            ),
            q(
                "For G(s) = 1/(s(s+2)) with gain K, where do the closed-loop poles start and how do they move?",
                (
                    opt("They start at the zeros and move to infinity"),
                    opt(
                        "They start at the open-loop poles s=0 and s=-2, meet at s=-1, then split into a complex pair",
                        correct=True,
                    ),
                    opt("They stay fixed at s=-1 regardless of K"),
                    opt("They move into the right half-plane immediately"),
                ),
                "The poles start at the open-loop poles s=0 and s=-2, meet at s=-1, then split vertically as a complex pair.",
            ),
            q(
                "How does a lead compensator affect the root locus?",
                (
                    opt("It lifts low-frequency gain to reduce steady-state error"),
                    opt("It bends the locus left, adding more damping and speed", correct=True),
                    opt("It removes all the open-loop poles"),
                    opt("It has no effect on the locus shape"),
                ),
                "A lead compensator bends the locus left for more damping and speed; a lag lifts low-frequency gain for less steady-state error.",
            ),
        ),
        "Frequency response & stability margins": (
            q(
                "On a Bode plot, when does the loop become unstable?",
                (
                    opt(
                        "When the phase reaches -180 degrees at the frequency where loop gain is 1 (0 dB)",
                        correct=True,
                    ),
                    opt("When the gain reaches 0 dB at zero phase"),
                    opt("When the phase reaches +90 degrees at any frequency"),
                    opt("When the magnitude is constant across all frequencies"),
                ),
                "Instability occurs when, at the 0 dB crossover frequency, the phase reaches -180 degrees and feedback flips to positive.",
            ),
            q(
                "What does the gain margin measure?",
                (
                    opt("How much more phase lag you could tolerate"),
                    opt("How much more gain you could add before instability", correct=True),
                    opt("The bandwidth of the closed loop"),
                    opt("The number of poles in the right half-plane"),
                ),
                "Gain margin is how much more gain you could add before instability; phase margin is how much more phase lag you could tolerate.",
            ),
            q(
                "What are the suggested rules of thumb for the margins?",
                (
                    opt("Phase margin of 0 degrees and gain margin of 0 dB"),
                    opt(
                        "Phase margin of 45-60 degrees and gain margin greater than 6 dB",
                        correct=True,
                    ),
                    opt("Phase margin of 180 degrees and gain margin of 1 dB"),
                    opt("Phase margin below 10 degrees and gain margin below 2 dB"),
                ),
                "Aim for a phase margin of 45-60 degrees and a gain margin greater than 6 dB (2x).",
            ),
        ),
        "PID tuning that works": (
            q(
                "In the Ziegler-Nichols method, what are Ku and Tu?",
                (
                    opt("The integral and derivative gains at steady state"),
                    opt(
                        "The ultimate gain and period found when the output oscillates steadily",
                        correct=True,
                    ),
                    opt("The crossover frequency and phase margin"),
                    opt("The plant mass and damping coefficient"),
                ),
                "Raise Kp until the output oscillates steadily; that gives the ultimate gain Ku and period Tu.",
            ),
            q(
                "What problem does anti-windup solve?",
                (
                    opt("Derivative kick on setpoint steps"),
                    opt(
                        "The integral accumulating error during actuator saturation, causing massive overshoot on recovery",
                        correct=True,
                    ),
                    opt("Too little steady-state gain"),
                    opt("Excessive bandwidth at high frequency"),
                ),
                "When the actuator saturates, the integral keeps accumulating error it cannot act on, then overshoots massively on recovery; anti-windup clamps or back-calculates it.",
            ),
            q(
                "How do you avoid derivative kick and noise amplification from the D term?",
                (
                    opt("Apply D to the error and never filter it"),
                    opt(
                        "Filter D with a first-order lag and apply D to the measurement, not the error",
                        correct=True,
                    ),
                    opt("Remove the proportional term entirely"),
                    opt("Increase Ki until the noise disappears"),
                ),
                "Filter D with a first-order lag and apply D to the measurement (not the error) to avoid derivative kick.",
            ),
        ),
        "Lab: tune a PID with anti-windup": (
            q(
                "In the lab loop, when is the integral updated to implement anti-windup?",
                (
                    opt("Always, every step regardless of saturation"),
                    opt(
                        "Only when the control is not saturated (u equals the unsaturated value)",
                        correct=True,
                    ),
                    opt("Only when the error is exactly zero"),
                    opt("Only when the derivative term is positive"),
                ),
                "The code integrates only when u == u_unsat, that is, when the control is not saturated.",
            ),
            q(
                "What does removing anti-windup and lowering umax to 8 demonstrate in the lab?",
                (
                    opt("The integral winds up and the output overshoots badly", correct=True),
                    opt("The response becomes instantly perfect"),
                    opt("The plant becomes unobservable"),
                    opt("The control effort drops to zero"),
                ),
                "Without anti-windup and with a low umax, the integral winds up and the output overshoots badly.",
            ),
            q(
                "What does the actuator saturation line u = max(-umax, min(umax, u_unsat)) enforce?",
                (
                    opt("That the integral never resets"),
                    opt("That the control u stays within plus or minus umax", correct=True),
                    opt("That the position x never exceeds the setpoint"),
                    opt("That the derivative term is always filtered"),
                ),
                "The clamp keeps the control u within the actuator limits, between -umax and umax.",
            ),
        ),
    },
    final=(
        q(
            "What does the denominator 1 + C(s)G(s) of the closed-loop transfer function determine?",
            (
                opt("The open-loop zeros"),
                opt("The closed-loop poles, via its roots", correct=True),
                opt("The setpoint value"),
                opt("The sampling rate"),
            ),
            "The roots of 1 + C(s)G(s) are the closed-loop poles, and they decide everything.",
        ),
        q(
            "A loop is stable if and only if all closed-loop poles are where?",
            (
                opt("In the right half of the s-plane"),
                opt("In the left half of the s-plane (negative real parts)", correct=True),
                opt("Exactly on the imaginary axis"),
                opt("At the origin"),
            ),
            "Stability requires every closed-loop pole to have a negative real part, in the left half-plane.",
        ),
        q(
            "For G(s) = 1/(s(s+2)) on the root locus, the closed-loop poles ride which line as K grows past 1?",
            (
                opt("The imaginary axis"),
                opt(
                    "The vertical line Re(s) = -1, so settling time stays the same while overshoot grows",
                    correct=True,
                ),
                opt("The real axis from -2 to infinity"),
                opt("The unit circle"),
            ),
            "The poles ride the vertical line Re(s) = -1; settling time stays the same while overshoot grows with K.",
        ),
        q(
            "Which pair of stability-margin targets does the lesson recommend?",
            (
                opt("Phase margin 45-60 degrees and gain margin greater than 6 dB", correct=True),
                opt("Phase margin 0 degrees and gain margin 0 dB"),
                opt("Phase margin 180 degrees and gain margin 1 dB"),
                opt("Phase margin under 10 degrees and gain margin under 2 dB"),
            ),
            "Aim for a phase margin of 45-60 degrees and a gain margin greater than 6 dB.",
        ),
        q(
            "Which two fixes separate textbook PID from working PID?",
            (
                opt("Removing the integral term and adding more proportional gain"),
                opt("Anti-windup, plus derivative filtering and setpoint weighting", correct=True),
                opt("Raising the sampling period and ignoring delay"),
                opt("Using only the Ziegler-Nichols gains unchanged"),
            ),
            "Anti-windup and derivative filtering with setpoint weighting are the two fixes that make PID work in the field.",
        ),
    ),
)
