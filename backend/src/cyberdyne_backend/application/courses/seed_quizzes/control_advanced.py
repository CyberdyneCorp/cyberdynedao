from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "State-space & modern control": (
            q(
                "In the state-space model x-dot = Ax + Bu, what does the matrix A represent?",
                (
                    opt("How the inputs enter the system"),
                    opt("The system dynamics", correct=True),
                    opt("What you measure as outputs"),
                    opt("The direct feedthrough term"),
                ),
                "A is the system dynamics matrix; B is how inputs enter, C is what you measure.",
            ),
            q(
                "Controllability is checked by the rank of which matrix?",
                (
                    opt("The observability matrix"),
                    opt("[B AB A^2 B ...]", correct=True),
                    opt("The matrix C alone"),
                    opt("The feedthrough matrix D"),
                ),
                "Controllability is the rank of the controllability matrix [B AB A^2 B ...]; full rank means the inputs can steer every state.",
            ),
            q(
                "A system mode that is unobservable means you cannot:",
                (
                    opt("Reconstruct that state from the outputs", correct=True),
                    opt("Move that state with the inputs"),
                    opt("Compute the system eigenvalues"),
                    opt("Apply any control input at all"),
                ),
                "Unobservable means you cannot see (reconstruct) the state from the outputs; uncontrollable means you cannot move it.",
            ),
        ),
        "Pole placement & LQR": (
            q(
                "State feedback u = -Kx lets you place the closed-loop poles anywhere, provided the system is:",
                (
                    opt("Observable"),
                    opt("Controllable", correct=True),
                    opt("Single-input single-output"),
                    opt("Time-varying"),
                ),
                "Arbitrary pole placement via u = -Kx requires controllability.",
            ),
            q(
                "In the LQR cost J = integral of (x'Qx + u'Ru), what does a large R penalise?",
                (
                    opt("State error"),
                    opt("Control effort", correct=True),
                    opt("Measurement noise"),
                    opt("Sampling delay"),
                ),
                "R penalises control effort; a big R gives gentle, energy-saving action. Q penalises state error.",
            ),
            q(
                "What is the main advantage of LQR over manual pole placement?",
                (
                    opt("It does not require a model of the plant"),
                    opt("A cost function picks the optimal, guaranteed-stable gain", correct=True),
                    opt("It eliminates the need to measure any states"),
                    opt("It works only for unstable systems"),
                ),
                "LQR automates the judgement of where to put the poles by minimising a cost, returning the optimal guaranteed-stable K.",
            ),
        ),
        "Observers & the Kalman filter": (
            q(
                "Why do you need an observer in state feedback control?",
                (
                    opt("To make the system controllable"),
                    opt("You usually measure only a few outputs, not the full state", correct=True),
                    opt("To slow down the closed-loop response"),
                    opt("To remove the need for the B matrix"),
                ),
                "An observer reconstructs the full state from the few measured outputs by running a model in parallel and correcting with the measurement error.",
            ),
            q(
                "When you account for process and measurement noise covariances, the optimal observer gain L becomes the:",
                (
                    opt("LQR gain"),
                    opt("Kalman gain", correct=True),
                    opt("Pole-placement gain"),
                    opt("Slew limit"),
                ),
                "Accounting for the noise covariances makes the optimal L the Kalman gain, turning the observer into the Kalman filter.",
            ),
            q(
                "What does the separation principle let you do when building LQG control?",
                (
                    opt("Design the regulator and the estimator independently", correct=True),
                    opt("Ignore process noise entirely"),
                    opt("Skip the controllability check"),
                    opt("Use a single gain for both estimation and control"),
                ),
                "The separation principle says the LQR regulator and the Kalman estimator can be designed independently.",
            ),
        ),
        "Model Predictive Control (MPC)": (
            q(
                "What is the receding-horizon idea at the core of MPC?",
                (
                    opt(
                        "Predict over a horizon, apply only the first move, then repeat",
                        correct=True,
                    ),
                    opt("Apply all the planned moves at once and stop"),
                    opt("React only to the present output like PID"),
                    opt("Solve the optimization once at startup"),
                ),
                "MPC predicts N steps ahead, applies only the first move, then re-measures and repeats: receding-horizon control.",
            ),
            q(
                "What is described as MPC's superpower compared to PID?",
                (
                    opt("Zero compute cost"),
                    opt("Handling hard constraints natively while staying optimal", correct=True),
                    opt("Requiring no model of the plant"),
                    opt("Working only on single-input systems"),
                ),
                "MPC handles input, slew, and output constraints natively while staying optimal; PID only fakes this with clamps.",
            ),
            q(
                "What is the main price you pay for using MPC?",
                (
                    opt("It cannot handle MIMO systems"),
                    opt(
                        "You must solve an optimization every sample, needing a good model and compute",
                        correct=True,
                    ),
                    opt("It ignores any known future reference"),
                    opt("It cannot enforce input limits"),
                ),
                "MPC solves an optimization every sample, so it needs a decent model and a compute budget.",
            ),
        ),
        "Active Disturbance Rejection Control (ADRC)": (
            q(
                "What is the central idea of ADRC?",
                (
                    opt("Build the most accurate transfer function possible"),
                    opt(
                        "Lump everything unknown into a total disturbance, estimate it, and cancel it",
                        correct=True,
                    ),
                    opt("Replace feedback with pure feedforward"),
                    opt("Use an infinite prediction horizon"),
                ),
                "ADRC lumps unmodeled dynamics, nonlinearities, and external disturbances into a single total disturbance f, estimates it in real time, and cancels it.",
            ),
            q(
                "What does the Extended State Observer (ESO) estimate that an ordinary observer does not?",
                (
                    opt("The total disturbance f as an extra state", correct=True),
                    opt("The controllability matrix rank"),
                    opt("The measurement noise covariance"),
                    opt("The prediction horizon length"),
                ),
                "The ESO treats the total disturbance f as an extra state and estimates it alongside the real states.",
            ),
            q(
                "In Linear ADRC, the observer bandwidth wo is typically set relative to the controller bandwidth wc as:",
                (
                    opt("wo about equal to wc"),
                    opt("wo about 3 to 5 times wc", correct=True),
                    opt("wo about one tenth of wc"),
                    opt("wo always fixed at 1 rad/s"),
                ),
                "LADRC parameterises everything by two bandwidths, with wo set to roughly 3 to 5 times wc.",
            ),
        ),
        "Lab: PID vs ADRC disturbance rejection": (
            q(
                "In the lab, what event happens at t = 5 seconds?",
                (
                    opt("A step load disturbance hits the plant", correct=True),
                    opt("The reference is set to zero"),
                    opt("The controller is switched off"),
                    opt("The sample time is doubled"),
                ),
                "A step load disturbance d of 1.5 is applied at t = 5, and the lab compares how PID and ADRC reject it.",
            ),
            q(
                "What is the ONLY model information the ADRC controller in the lab uses?",
                (
                    opt("The exact values of true a and b"),
                    opt("A rough input gain b0", correct=True),
                    opt("The full pole locations"),
                    opt("The measurement noise covariance"),
                ),
                "The ADRC controller knows only the rough input gain b0; the true a and b are only roughly known to it.",
            ),
            q(
                "Raising the observer bandwidth wo in the ADRC lab is expected to:",
                (
                    opt("Reject the disturbance even harder", correct=True),
                    opt("Make the controller ignore the disturbance"),
                    opt("Turn ADRC into a fixed PID"),
                    opt("Eliminate the need for b0"),
                ),
                "The lab notes that raising wo to 25 makes ADRC reject the disturbance even harder.",
            ),
        ),
        "Deployment & use cases": (
            q(
                "What sampling rate does the deployment checklist recommend relative to closed-loop bandwidth?",
                (
                    opt("About the same as the bandwidth"),
                    opt("10 to 20 times the closed-loop bandwidth", correct=True),
                    opt("About one tenth of the bandwidth"),
                    opt("Exactly twice the bandwidth"),
                ),
                "Discretize at 10 to 20 times the closed-loop bandwidth; too slow adds delay that erodes phase margin.",
            ),
            q(
                "What technique handles a plant whose dynamics change with operating point such as airspeed or load?",
                (
                    opt("Gain scheduling", correct=True),
                    opt("Removing the observer"),
                    opt("Disabling anti-windup"),
                    opt("Increasing the feedthrough term D"),
                ),
                "Gain scheduling blends a set of controllers by a measured variable when the plant changes with operating point.",
            ),
            q(
                "According to the throughline, what is the unchanging idea behind every controller?",
                (
                    opt("Measure, compare, correct", correct=True),
                    opt("Predict, optimize, discard"),
                    opt("Model, simulate, deploy"),
                    opt("Filter, delay, saturate"),
                ),
                "Whatever the controller, the loop is the same idea Watt built in 1788: measure, compare, correct.",
            ),
        ),
    },
    final=(
        q(
            "Which pair of properties must both hold for full state feedback with estimation to work?",
            (
                opt("Linearity and time-invariance"),
                opt("Controllability and observability", correct=True),
                opt("Stability and passivity"),
                opt("Causality and minimum-phase"),
            ),
            "An uncontrollable mode cannot be moved and an unobservable mode cannot be seen; both must hold.",
        ),
        q(
            "How does LQR decide where to place the closed-loop poles?",
            (
                opt("By minimising a quadratic cost with the Q/R trade-off", correct=True),
                opt("By having the engineer pick exact pole locations"),
                opt("By solving an optimization every sample"),
                opt("By estimating a total disturbance"),
            ),
            "LQR picks the optimal gain by minimising the quadratic cost, where Q penalises state error and R penalises control effort.",
        ),
        q(
            "Combining an LQR controller with a Kalman-filter estimator gives which control scheme?",
            (
                opt("MPC"),
                opt("ADRC"),
                opt("LQG", correct=True),
                opt("Pure PID"),
            ),
            "LQR plus a Kalman filter is LQG (Linear-Quadratic-Gaussian) control, justified by the separation principle.",
        ),
        q(
            "Which controller looks ahead over a horizon and handles hard constraints natively?",
            (
                opt("MPC", correct=True),
                opt("Classic PID"),
                opt("Pole placement"),
                opt("A plain Luenberger observer"),
            ),
            "MPC predicts over a horizon and enforces input, slew, and output constraints natively as part of the optimization.",
        ),
        q(
            "Which controller is nearly model-free, needing only the system order and a rough input gain b0?",
            (
                opt("LQG"),
                opt("ADRC", correct=True),
                opt("LQR"),
                opt("MPC"),
            ),
            "ADRC needs only the system order and a rough b0 because its ESO estimates and cancels the total disturbance.",
        ),
    ),
)
