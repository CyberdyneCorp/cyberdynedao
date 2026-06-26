"""Quiz questions for the Mechatronics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Sensor fusion and the Kalman filter": (
            q(
                "What does the Kalman filter track in addition to the state estimate?",
                (
                    opt("The estimate's error covariance P", correct=True),
                    opt("The raw analog voltage only"),
                    opt("The CPU clock frequency"),
                    opt("Nothing else"),
                ),
                "It propagates both x_hat and its covariance P each cycle.",
            ),
            q(
                "In the Kalman update, the matrices Q and R represent?",
                (
                    opt("Process (model) noise and measurement (sensor) noise", correct=True),
                    opt("Resistance and reactance"),
                    opt("Reference and output"),
                    opt("Two unrelated constants"),
                ),
                "Q is model uncertainty, R is sensor uncertainty; the gain K blends them optimally.",
            ),
            q(
                "For a nonlinear system, which variants of the Kalman filter are used?",
                (
                    opt("The Extended (EKF) or Unscented (UKF) Kalman filter", correct=True),
                    opt("Only the linear KF, unchanged"),
                    opt("A PID controller"),
                    opt("A low-pass filter alone"),
                ),
                "EKF linearises and UKF samples around the estimate for nonlinear models.",
            ),
        ),
        "State-space control and pole placement": (
            q(
                "Full-state feedback u = -K x can place the closed-loop poles arbitrarily when?",
                (
                    opt(
                        "The system is controllable (controllability matrix has full rank)",
                        correct=True,
                    ),
                    opt("The system is unstable"),
                    opt("There are no actuators"),
                    opt("The state is unmeasured and unestimated"),
                ),
                "Controllability of (A,B) is the condition for arbitrary pole placement.",
            ),
            q(
                "The LQR designs the gain K by?",
                (
                    opt("Minimising a quadratic cost on state and input", correct=True),
                    opt("Random search over gains"),
                    opt("Setting all poles to zero"),
                    opt("Ignoring the input cost entirely"),
                ),
                "LQR minimises integral of x'Qx + u'Ru, balancing performance and effort.",
            ),
            q(
                "When the full state is not measured, the separation principle lets you?",
                (
                    opt("Design the observer and the controller independently", correct=True),
                    opt("Ignore the unmeasured states"),
                    opt("Avoid feedback altogether"),
                    opt("Only use open-loop control"),
                ),
                "An observer estimates the state; controller and observer can be designed separately.",
            ),
        ),
        "Real-time systems and the digital twin": (
            q(
                "In a hard real-time control loop, a missed deadline is?",
                (
                    opt("A failure, not merely slower performance", correct=True),
                    opt("Always acceptable"),
                    opt("Only a cosmetic issue"),
                    opt("Impossible by definition"),
                ),
                "Hard real-time means deadlines must be guaranteed; a late update is a fault.",
            ),
            q(
                "Sampling jitter is harmful to control because it?",
                (
                    opt(
                        "Injects effective noise, especially into the derivative term", correct=True
                    ),
                    opt("Always improves accuracy"),
                    opt("Has no effect on any controller"),
                    opt("Only matters for communication"),
                ),
                "Varying sample instants corrupt derivative estimates and degrade stability.",
            ),
            q(
                "A digital twin is?",
                (
                    opt("A live physics-based model fed by the real machine's data", correct=True),
                    opt("A backup copy of the firmware"),
                    opt("A second identical physical robot"),
                    opt("A static CAD drawing"),
                ),
                "It mirrors the machine in simulation for HIL testing, maintenance and safe tuning.",
            ),
        ),
        "Learning and optimization in mechatronics": (
            q(
                "The distinctive strength of Model Predictive Control (MPC) is?",
                (
                    opt(
                        "It handles hard constraints by optimising over a finite horizon each step",
                        correct=True,
                    ),
                    opt("It needs no model at all"),
                    opt("It cannot respect actuator limits"),
                    opt("It only works at steady state"),
                ),
                "MPC solves a constrained optimization every sample, respecting limits explicitly.",
            ),
            q(
                "Reinforcement learning is most attractive when?",
                (
                    opt("The dynamics are hard to model, e.g. contact and friction", correct=True),
                    opt("A perfect linear model is already known"),
                    opt("No reward signal can be defined"),
                    opt("The system must never be simulated"),
                ),
                "RL learns a policy by reward, useful for hard-to-model behaviour, often trained in sim.",
            ),
            q(
                "Auto-tuning controller gains is fundamentally?",
                (
                    opt(
                        "An optimization that minimises a cost on performance metrics", correct=True
                    ),
                    opt("A purely manual trial with no objective"),
                    opt("Unrelated to settling time or overshoot"),
                    opt("Only possible without any model"),
                ),
                "It minimises a cost (e.g. settling time, overshoot) via gradient or evolutionary search.",
            ),
        ),
        "A full mechatronic design project": (
            q(
                "The self-balancing robot is modelled as which classic system?",
                (
                    opt("An inverted pendulum on wheels", correct=True),
                    opt("A simple resistor network"),
                    opt("A static truss"),
                    opt("A heat exchanger"),
                ),
                "It is an inverted-pendulum-on-cart problem and is open-loop unstable.",
            ),
            q(
                "In the project, which block fuses the IMU and encoder signals?",
                (
                    opt("The Kalman (or complementary) filter", correct=True),
                    opt("The H-bridge"),
                    opt("The PWM timer"),
                    opt("The gearbox"),
                ),
                "Fusion produces a clean tilt estimate from noisy IMU plus drifting integration.",
            ),
            q(
                "The overarching lesson of the integrated project is that a mechatronic system succeeds?",
                (
                    opt(
                        "At the interfaces, when each discipline respects the others", correct=True
                    ),
                    opt("Only by maximising mechanical mass"),
                    opt("By avoiding feedback control"),
                    opt("By ignoring real-time constraints"),
                ),
                "Cross-domain interface design is what makes integration work.",
            ),
        ),
    },
    final=(
        q(
            "In the Kalman filter, a large measurement-noise R relative to Q makes the filter?",
            (
                opt("Trust the model more and the measurement less", correct=True),
                opt("Ignore the model entirely"),
                opt("Trust the measurement more"),
                opt("Diverge immediately"),
            ),
            "Large R means noisy sensors, so the optimal gain weights the prediction more.",
        ),
        q(
            "Pole placement via u = -K x requires the system to be?",
            (
                opt("Controllable", correct=True),
                opt("Unobservable"),
                opt("Open-loop unstable"),
                opt("Free of any actuators"),
            ),
            "Controllability of (A,B) is the prerequisite for arbitrary pole placement.",
        ),
        q(
            "Which best describes a hard real-time control task?",
            (
                opt(
                    "It must finish within its deadline every cycle or the system fails",
                    correct=True,
                ),
                opt("It can miss deadlines freely"),
                opt("It runs only once at startup"),
                opt("It has no timing requirements"),
            ),
            "Hard real-time guarantees deadlines; the loop must fit inside its period Ts.",
        ),
        q(
            "MPC differs from classical PID mainly because it?",
            (
                opt("Explicitly optimises over a horizon subject to constraints", correct=True),
                opt("Uses no model whatsoever"),
                opt("Cannot handle multivariable systems"),
                opt("Requires no computation"),
            ),
            "MPC solves a constrained optimization each step, naturally respecting limits.",
        ),
        q(
            "A digital twin enables which capability?",
            (
                opt(
                    "Hardware-in-the-loop testing and safe controller tuning in simulation",
                    correct=True,
                ),
                opt("Replacing the need for any real sensors"),
                opt("Permanently disabling the controller"),
                opt("Removing all timing constraints"),
            ),
            "A live model supports HIL, predictive maintenance and offline tuning.",
        ),
        q(
            "In the balancing-robot project, the LQR / state-feedback law computes?",
            (
                opt("Wheel torque commands from the estimated state", correct=True),
                opt("The I2C bus address"),
                opt("The ADC resolution"),
                opt("The mechanical gear ratio"),
            ),
            "State feedback maps the fused state to actuator (wheel torque) commands.",
        ),
    ),
)
