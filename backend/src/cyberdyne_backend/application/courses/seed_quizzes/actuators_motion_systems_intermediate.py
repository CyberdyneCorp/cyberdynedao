"""Quiz questions for the Actuators & Motion Systems - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Modeling the actuator dynamics": (
            q(
                "The actuator dynamic model couples which two equations?",
                (
                    opt(
                        "An electrical (voltage) and a mechanical (Newton/torque) equation",
                        correct=True,
                    ),
                    opt("Two purely electrical equations"),
                    opt("Two purely thermal equations"),
                    opt("A chemical and an optical equation"),
                ),
                "L di/dt = V - Ri - ke*w (electrical) couples to J dw/dt = kt*i - b*w - tau_L (mechanical).",
            ),
            q(
                "The electrical time constant of the winding is given by:",
                (
                    opt("R/L"),
                    opt("L/R", correct=True),
                    opt("J*R"),
                    opt("kt*ke"),
                ),
                "The electrical time constant is tau_e = L/R, usually milliseconds.",
            ),
            q(
                "Why can the current loop and speed loop be designed separately?",
                (
                    opt("They share the same time constant"),
                    opt(
                        "The electrical and mechanical time constants differ by about an order of magnitude",
                        correct=True,
                    ),
                    opt("The motor has no inertia"),
                    opt("Voltage and torque are unrelated"),
                ),
                "Time-scale separation between tau_e and tau_m lets the loops be tuned independently.",
            ),
        ),
        "Trapezoidal and S-curve motion profiles": (
            q(
                "What is the main drawback of a pure trapezoidal velocity profile?",
                (
                    opt("It is never time-optimal"),
                    opt("Its instantaneous acceleration jumps give infinite jerk", correct=True),
                    opt("It cannot reach the target"),
                    opt("It requires an encoder"),
                ),
                "The trapezoid steps acceleration, giving infinite jerk that excites vibration.",
            ),
            q(
                "What does an S-curve profile bound that a trapezoid does not?",
                (
                    opt("Velocity"),
                    opt("Acceleration"),
                    opt("Jerk (rate of change of acceleration)", correct=True),
                    opt("Distance"),
                ),
                "The S-curve limits jerk, smoothing acceleration at the cost of slightly longer moves.",
            ),
            q(
                "If a trapezoidal move never reaches vmax, the profile becomes:",
                (
                    opt("Triangular", correct=True),
                    opt("Rectangular"),
                    opt("Sinusoidal"),
                    opt("Constant"),
                ),
                "For short moves the cruise phase vanishes and the velocity profile is triangular.",
            ),
        ),
        "Inertia matching and reflected load": (
            q(
                "A common rule of thumb keeps the reflected inertia ratio below about:",
                (
                    opt("0.1:1"),
                    opt("5 to 10:1", correct=True),
                    opt("100:1"),
                    opt("1000:1"),
                ),
                "Responsive servos typically keep load-to-motor reflected inertia under 5-10:1.",
            ),
            q(
                "The gear ratio that minimizes acceleration torque for a given load is:",
                (
                    opt("N = J_load / J_motor"),
                    opt("N = sqrt(J_load / J_motor)", correct=True),
                    opt("N = 1"),
                    opt("N = J_motor / J_load"),
                ),
                "Optimal matching sets N* = sqrt(J_load/J_motor), matching reflected load inertia to motor inertia.",
            ),
            q(
                "A load mass m on a screw of lead L reflects to the motor as inertia:",
                (
                    opt("m * (L / (2*pi))^2", correct=True),
                    opt("m * L"),
                    opt("m / L"),
                    opt("m * (2*pi*L)^2"),
                ),
                "Reflected rotary inertia of a translating mass on a screw is m*(L/2pi)^2.",
            ),
        ),
        "RMS torque and thermal sizing": (
            q(
                "Which torque value governs the continuous (thermal) motor rating?",
                (
                    opt("Peak torque"),
                    opt("RMS torque over the duty cycle", correct=True),
                    opt("Stall torque"),
                    opt("No-load torque"),
                ),
                "Heating depends on i^2*R averaged over the cycle, captured by the RMS torque.",
            ),
            q(
                "When sizing, the peak torque rating must exceed:",
                (
                    opt("The average torque"),
                    opt(
                        "The worst instantaneous torque, usually during acceleration", correct=True
                    ),
                    opt("The RMS torque only"),
                    opt("Zero"),
                ),
                "Peak rating must cover the worst instant; RMS covers heating - both checks are needed.",
            ),
            q(
                "How does a long dwell in the cycle affect required motor size?",
                (
                    opt("It raises RMS torque"),
                    opt("It lowers RMS torque, possibly allowing a smaller motor", correct=True),
                    opt("It has no effect"),
                    opt("It raises peak torque"),
                ),
                "Adding idle time lowers the RMS value, so a smaller continuous rating can suffice.",
            ),
        ),
        "Cascaded velocity and current loops": (
            q(
                "Which loop should be tuned first in a cascaded servo drive?",
                (
                    opt("The position loop"),
                    opt("The inner current (torque) loop", correct=True),
                    opt("The velocity loop"),
                    opt("They are tuned simultaneously"),
                ),
                "Tune the innermost current loop first; it sets the torque bandwidth the outer loops rely on.",
            ),
            q(
                "Typical bandwidth separation between current and velocity loops is about:",
                (
                    opt("Equal bandwidth"),
                    opt("Current loop 5-10x faster than velocity loop", correct=True),
                    opt("Velocity loop 100x faster"),
                    opt("No separation needed"),
                ),
                "The current loop is usually 5-10x faster so the velocity loop sees an ideal torque source.",
            ),
            q(
                "What feature prevents the PI integrator from overshooting when actuators saturate?",
                (
                    opt("Anti-windup", correct=True),
                    opt("Higher proportional gain"),
                    opt("Removing the integrator"),
                    opt("Lower sampling rate"),
                ),
                "Anti-windup limits integrator buildup during saturation, avoiding large overshoot.",
            ),
        ),
        "Feedback devices and resolution": (
            q(
                "With N encoder lines, quadrature decoding yields how many counts per revolution?",
                (
                    opt("N"),
                    opt("2N"),
                    opt("4N", correct=True),
                    opt("N/4"),
                ),
                "Quadrature decoding of A/B channels gives 4N counts per revolution.",
            ),
            q(
                "Which feedback device reports true angle at power-up with no homing?",
                (
                    opt("Incremental encoder"),
                    opt("Absolute encoder", correct=True),
                    opt("Tachometer"),
                    opt("Open-loop step counter"),
                ),
                "An absolute encoder knows the true position immediately at power-up.",
            ),
            q(
                "A high-resolution encoder behind a backlashed gear is best described as:",
                (
                    opt("Precise but possibly inaccurate", correct=True),
                    opt("Both accurate and repeatable"),
                    opt("Low resolution"),
                    opt("Impossible to read"),
                ),
                "Resolution, accuracy and repeatability differ; backlash hurts accuracy despite fine resolution.",
            ),
        ),
    },
    final=(
        q(
            "The mechanical time constant tau_m of a DC motor is approximately:",
            (
                opt("L/R"),
                opt("J*R/(kt*ke)", correct=True),
                opt("kt*ke"),
                opt("1/(J*b)"),
            ),
            "tau_m = J*R/(kt*ke), typically tens of milliseconds.",
        ),
        q(
            "Which profile is preferred when minimizing vibration and noise matters?",
            (
                opt("Pure trapezoidal"),
                opt("S-curve (jerk-limited)", correct=True),
                opt("Step input"),
                opt("Random profile"),
            ),
            "The jerk-limited S-curve reduces vibration and noise versus a trapezoid.",
        ),
        q(
            "Optimal inertia matching occurs at gear ratio:",
            (
                opt("N = sqrt(J_load/J_motor)", correct=True),
                opt("N = J_load*J_motor"),
                opt("N = 1 always"),
                opt("N = J_load + J_motor"),
            ),
            "N* = sqrt(J_load/J_motor) minimizes acceleration torque.",
        ),
        q(
            "A motor selection passes thermal sizing when:",
            (
                opt("Peak torque exceeds RMS torque"),
                opt("Continuous rating exceeds RMS torque (with margin)", correct=True),
                opt("No-load speed exceeds command"),
                opt("Inductance is high"),
            ),
            "Continuous rating must exceed RMS torque, and peak rating must exceed peak torque, with margin.",
        ),
        q(
            "In a cascaded drive, the innermost loop controls:",
            (
                opt("Position"),
                opt("Velocity"),
                opt("Current (torque)", correct=True),
                opt("Temperature"),
            ),
            "The innermost loop regulates current, hence torque, and is the fastest loop.",
        ),
        q(
            "Linear resolution of a 2000-line encoder on a 5 mm-lead ball screw is about:",
            (
                opt("0.625 um", correct=True),
                opt("5 um"),
                opt("62.5 um"),
                opt("0.05 um"),
            ),
            "resolution = lead/(4N) = 5 mm / 8000 = 0.625 um.",
        ),
    ),
)
