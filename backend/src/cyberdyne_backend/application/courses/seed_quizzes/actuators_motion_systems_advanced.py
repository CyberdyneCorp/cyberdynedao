"""Quiz questions for the Actuators & Motion Systems - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Sensorless FOC and observers": (
            q(
                "What does field-oriented control decouple for independent control?",
                (
                    opt("Torque (i_q) and flux (i_d) in the rotating d-q frame", correct=True),
                    opt("Voltage and current magnitude only"),
                    opt("Temperature and speed"),
                    opt("Resistance and inductance"),
                ),
                "FOC works in the d-q frame so i_q controls torque and i_d controls flux independently.",
            ),
            q(
                "At medium and high speed, sensorless FOC commonly estimates rotor angle from:",
                (
                    opt("The back-EMF via an observer", correct=True),
                    opt("A resolver"),
                    opt("Counting steps"),
                    opt("DC bus ripple"),
                ),
                "Back-EMF carries the angle; a sliding-mode or Luenberger observer reconstructs it.",
            ),
            q(
                "Why does back-EMF estimation fail near zero speed, requiring another method?",
                (
                    opt("Back-EMF amplitude vanishes as speed goes to zero", correct=True),
                    opt("The inverter shuts off"),
                    opt("Resistance becomes infinite"),
                    opt("Current cannot flow"),
                ),
                "Back-EMF = ke*omega vanishes at standstill, so high-frequency injection using saliency takes over.",
            ),
        ),
        "Time-optimal jerk-limited trajectories": (
            q(
                "With bounded jerk, a time-optimal point-to-point velocity profile becomes:",
                (
                    opt("A single rectangular pulse"),
                    opt("A 7-segment S-curve", correct=True),
                    opt("A pure sinusoid"),
                    opt("A constant"),
                ),
                "Bounding jerk yields the classic 7-segment S-curve profile.",
            ),
            q(
                "The general time-optimal planning problem is posed as:",
                (
                    opt(
                        "An optimal control problem minimizing move time subject to dynamics and bounds",
                        correct=True,
                    ),
                    opt("A linear regression"),
                    opt("A sorting algorithm"),
                    opt("A Fourier transform"),
                ),
                "It minimizes T subject to the system dynamics and bounds on u, a, and jerk.",
            ),
            q(
                "What speeds up convergence of the trajectory optimizer?",
                (
                    opt("Random restarts only"),
                    opt("Warm-starting near the analytic S-curve", correct=True),
                    opt("Removing all constraints"),
                    opt("Using zero initial guess far from optimum"),
                ),
                "A warm start near the analytic S-curve gives fast convergence.",
            ),
        ),
        "Input shaping and resonance suppression": (
            q(
                "Input shaping suppresses residual vibration by:",
                (
                    opt(
                        "Convolving the command with designed impulses that cancel vibration",
                        correct=True,
                    ),
                    opt("Adding a heavier motor"),
                    opt("Increasing the encoder resolution"),
                    opt("Removing the controller"),
                ),
                "Shaping convolves the reference with impulses timed so their vibrations cancel.",
            ),
            q(
                "A Zero-Vibration (ZV) shaper uses how many impulses?",
                (
                    opt("One"),
                    opt("Two", correct=True),
                    opt("Five"),
                    opt("Ten"),
                ),
                "The ZV shaper uses two impulses separated by half the damped period.",
            ),
            q(
                "What does a ZVD shaper add compared to a ZV shaper?",
                (
                    opt("Lower cost"),
                    opt("Robustness to errors in the estimated natural frequency", correct=True),
                    opt("Faster moves"),
                    opt("Higher resolution"),
                ),
                "ZVD adds a third impulse, widening the notch for robustness to frequency error.",
            ),
        ),
        "Iterative learning control": (
            q(
                "Iterative learning control is best suited to systems that:",
                (
                    opt("Repeat the same trajectory many times", correct=True),
                    opt("Never repeat a motion"),
                    opt("Have no sensors"),
                    opt("Run open loop only"),
                ),
                "ILC learns from one run to improve the next, ideal for repetitive trajectories.",
            ),
            q(
                "In the ILC update u_{k+1} = Q(u_k + L*e_k), what is the role of Q?",
                (
                    opt(
                        "A low-pass filter bounding learning to trustworthy frequencies",
                        correct=True,
                    ),
                    opt("The learning gain"),
                    opt("The plant inverse"),
                    opt("A random number"),
                ),
                "Q is a low-pass filter that limits learning to the band where the model is reliable.",
            ),
            q(
                "The ILC convergence condition over the passband of Q is:",
                (
                    opt("|1 - L*G(jw)| < 1", correct=True),
                    opt("L*G = 0"),
                    opt("G = infinity"),
                    opt("Q = 0"),
                ),
                "Monotonic convergence requires |1 - L*G(jw)| < 1 across Q's passband.",
            ),
        ),
        "Optimization-based actuator sizing": (
            q(
                "Optimization-based sizing differs from classical sizing by:",
                (
                    opt(
                        "Searching the catalog and ratio to minimize an objective under constraints",
                        correct=True,
                    ),
                    opt("Ignoring torque limits"),
                    opt("Checking only one fixed motor"),
                    opt("Removing the gearbox"),
                ),
                "It optimizes mass/cost/energy over motor and ratio choices subject to RMS, peak and inertia limits.",
            ),
            q(
                "What is co-design in this context?",
                (
                    opt("Optimizing the trajectory and the actuator together", correct=True),
                    opt("Designing only the controller"),
                    opt("Picking colors for the housing"),
                    opt("Outsourcing the design"),
                ),
                "Co-design optimizes the motion profile and hardware jointly, often shrinking the motor.",
            ),
            q(
                "Why can a gentler trajectory allow a smaller motor?",
                (
                    opt("It lowers the peak torque demand", correct=True),
                    opt("It raises RMS torque"),
                    opt("It increases inertia"),
                    opt("It removes the load"),
                ),
                "A gentler profile reduces peak torque, relaxing the peak rating and enabling mass savings.",
            ),
        ),
        "Case study: precision nano-positioning": (
            q(
                "Why does a precision wafer stage use a dual-stage design?",
                (
                    opt("No single actuator gives both long travel and nm precision", correct=True),
                    opt("To use two power supplies"),
                    opt("To double the cost"),
                    opt("To avoid using feedback"),
                ),
                "A coarse long-travel stage carries a short-travel high-bandwidth fine stage.",
            ),
            q(
                "What sets the achievable accuracy in the nano-positioning stage?",
                (
                    opt("The motor torque"),
                    opt("The metrology / interferometric feedback resolution", correct=True),
                    opt("The DC bus voltage"),
                    opt("The cable length"),
                ),
                "The encoder/interferometer, not the motor, sets achievable accuracy at the nm scale.",
            ),
            q(
                "The fine stage in the case study is typically a:",
                (
                    opt("Piezoelectric actuator with kHz bandwidth", correct=True),
                    opt("Large induction motor"),
                    opt("Hydraulic ram"),
                    opt("Stepper with a belt"),
                ),
                "A piezo fine stage provides the high bandwidth and sub-micron stroke for residual error rejection.",
            ),
        ),
    },
    final=(
        q(
            "Sensorless FOC at standstill relies on which technique instead of back-EMF?",
            (
                opt("High-frequency injection exploiting magnetic saliency", correct=True),
                opt("Counting encoder lines"),
                opt("Measuring the DC bus only"),
                opt("Open-loop voltage ramp forever"),
            ),
            "At zero speed back-EMF vanishes, so saliency-based HF injection estimates the angle.",
        ),
        q(
            "Jerk-limited time-optimal planning is formulated as:",
            (
                opt("An optimal control problem under dynamics and bounds", correct=True),
                opt("A linear least-squares fit"),
                opt("A Fourier series"),
                opt("A lookup table only"),
            ),
            "It minimizes move time subject to dynamics and velocity/acceleration/jerk bounds.",
        ),
        q(
            "The deepest vibration cancellation of a ZV shaper occurs:",
            (
                opt("At the structure's natural frequency", correct=True),
                opt("At DC"),
                opt("At twice the sample rate"),
                opt("At infinite frequency"),
            ),
            "The ZV shaper places a notch exactly at the resonant natural frequency.",
        ),
        q(
            "ILC improves performance over iterations by using:",
            (
                opt("The previous run's tracking error to update the feedforward", correct=True),
                opt("A random feedforward each run"),
                opt("Only feedback gains"),
                opt("No memory"),
            ),
            "ILC stores past error and command and updates the feedforward each iteration.",
        ),
        q(
            "Actuator co-design can save mass mainly because it:",
            (
                opt(
                    "Optimizes trajectory and hardware jointly, lowering peak torque", correct=True
                ),
                opt("Uses a larger gearbox always"),
                opt("Ignores constraints"),
                opt("Removes feedback"),
            ),
            "Jointly tuning the profile and hardware lowers peak torque, allowing a smaller, lighter motor.",
        ),
        q(
            "The recurring lesson of precision motion engineering is that accuracy comes from:",
            (
                opt(
                    "The co-designed system: metrology, mechanics, trajectory and control",
                    correct=True,
                ),
                opt("One heroic high-torque motor"),
                opt("A faster CPU alone"),
                opt("More current"),
            ),
            "Precision is a system property - metrology, mechanics, trajectory and control together.",
        ),
    ),
)
