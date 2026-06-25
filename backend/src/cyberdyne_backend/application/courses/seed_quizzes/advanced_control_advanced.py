"""Quiz questions for the Advanced Control Systems - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Nonlinear control: feedback linearization & sliding mode": (
            q(
                "Feedback linearization works by:",
                (
                    opt("cancelling nonlinear terms via a control transform", correct=True),
                    opt("ignoring the nonlinearity"),
                    opt("adding random noise"),
                    opt("removing all feedback"),
                ),
                "It transforms nonlinear dynamics into linear ones via cancellation.",
            ),
            q(
                "A defining feature of sliding-mode control is:",
                (
                    opt("robust switching onto a sliding surface", correct=True),
                    opt("a fixed linear gain"),
                    opt("no feedback"),
                    opt("open-loop operation"),
                ),
                "The state is forced onto and along a sliding manifold.",
            ),
            q(
                "A practical drawback of ideal sliding mode is:",
                (
                    opt("chattering from high-frequency switching", correct=True),
                    opt("zero robustness"),
                    opt("inability to reject disturbances"),
                    opt("needing no model"),
                ),
                "Switching causes chattering, mitigated by boundary layers.",
            ),
        ),
        "Model predictive control (MPC)": (
            q(
                "MPC computes control by:",
                (
                    opt("optimizing over a finite receding horizon each step", correct=True),
                    opt("a single fixed gain"),
                    opt("random search"),
                    opt("ignoring constraints"),
                ),
                "It solves a constrained optimization over a moving horizon.",
            ),
            q(
                "A major advantage of MPC is:",
                (
                    opt("explicit handling of input/state constraints", correct=True),
                    opt("no computation needed"),
                    opt("guaranteed for unstable plants only"),
                    opt("ignoring the model"),
                ),
                "MPC handles constraints directly.",
            ),
            q(
                "MPC's main cost is:",
                (
                    opt("online computational load", correct=True),
                    opt("lack of a model"),
                    opt("no tuning knobs"),
                    opt("inability to predict"),
                ),
                "Solving an optimization every step is expensive.",
            ),
        ),
        "Robust control & uncertainty (H-infinity)": (
            q(
                "Robust control explicitly accounts for:",
                (
                    opt("model uncertainty and disturbances", correct=True),
                    opt("only nominal models"),
                    opt("the sampling clock"),
                    opt("actuator color"),
                ),
                "Robust design guarantees performance despite uncertainty.",
            ),
            q(
                "H-infinity control minimizes:",
                (
                    opt("the worst-case gain from disturbance to output", correct=True),
                    opt("the number of states"),
                    opt("the pole count"),
                    opt("the input offset"),
                ),
                "It bounds the worst-case (infinity-norm) gain.",
            ),
            q(
                "There is a fundamental trade-off in robust control between:",
                (
                    opt("robustness and nominal performance", correct=True),
                    opt("poles and zeros only"),
                    opt("input and output names"),
                    opt("color and size"),
                ),
                "More robustness often costs nominal performance.",
            ),
        ),
        "Adaptive control": (
            q(
                "Adaptive control is useful when:",
                (
                    opt("plant parameters are unknown or vary over time", correct=True),
                    opt("the model is perfectly known"),
                    opt("there are no inputs"),
                    opt("the plant is static"),
                ),
                "It adjusts the controller online as parameters change.",
            ),
            q(
                "Model-reference adaptive control (MRAC) drives the plant to behave like:",
                (
                    opt("a chosen reference model", correct=True),
                    opt("an integrator only"),
                    opt("an open loop"),
                    opt("a random system"),
                ),
                "MRAC matches a desired reference model.",
            ),
            q(
                "A key concern in adaptive control is:",
                (
                    opt("stability of the adaptation law", correct=True),
                    opt("the wire color"),
                    opt("the sample bit depth"),
                    opt("the display"),
                ),
                "Adaptation must remain stable (e.g. via Lyapunov design).",
            ),
        ),
        "Optimal estimation & LQG (the Kalman filter)": (
            q(
                "The Kalman filter is the optimal estimator for:",
                (
                    opt("linear systems with Gaussian noise", correct=True),
                    opt("nonlinear chaotic-only systems"),
                    opt("noise-free systems only"),
                    opt("static signals only"),
                ),
                "It is the optimal linear-Gaussian state estimator.",
            ),
            q(
                "LQG combines:",
                (
                    opt("an LQR controller with a Kalman filter", correct=True),
                    opt("two LQR controllers"),
                    opt("two observers"),
                    opt("no estimator"),
                ),
                "LQG = LQR + Kalman estimator (by separation).",
            ),
            q(
                "The Kalman filter balances:",
                (
                    opt("model prediction against measurement via the Kalman gain", correct=True),
                    opt("only measurements"),
                    opt("only the model"),
                    opt("neither"),
                ),
                "The gain weights prediction vs measurement by their covariances.",
            ),
        ),
        "A design case study": (
            q(
                "A sensible control design workflow is:",
                (
                    opt("model -> analyze -> design -> simulate -> validate", correct=True),
                    opt("deploy first, model never"),
                    opt("random tuning only"),
                    opt("ignore the plant"),
                ),
                "Iterative model-based design and validation.",
            ),
            q(
                "When the full state is unmeasured, the design adds:",
                (
                    opt("an observer/estimator", correct=True),
                    opt("more sensors than states"),
                    opt("nothing"),
                    opt("a larger reference"),
                ),
                "Estimate the state for feedback.",
            ),
            q(
                "Robustness should be verified against:",
                (
                    opt("model uncertainty and disturbances", correct=True),
                    opt("only the nominal model"),
                    opt("the UI theme"),
                    opt("the compiler"),
                ),
                "Check performance under uncertainty.",
            ),
        ),
    },
    final=(
        q(
            "Feedback linearization:",
            (
                opt("cancels nonlinearities via a control law", correct=True),
                opt("adds noise"),
                opt("removes feedback"),
                opt("is open loop"),
            ),
            "Transforms to linear dynamics.",
        ),
        q(
            "MPC's key strength:",
            (
                opt("constraint handling over a horizon", correct=True),
                opt("no computation"),
                opt("fixed gain"),
                opt("ignores model"),
            ),
            "Receding-horizon constrained optimization.",
        ),
        q(
            "H-infinity minimizes:",
            (
                opt("worst-case disturbance-to-output gain", correct=True),
                opt("pole count"),
                opt("offset"),
                opt("bandwidth"),
            ),
            "Worst-case norm.",
        ),
        q(
            "Adaptive control suits:",
            (
                opt("unknown/time-varying parameters", correct=True),
                opt("perfectly known plants"),
                opt("static signals"),
                opt("no-input plants"),
            ),
            "Online parameter adaptation.",
        ),
        q(
            "The Kalman filter is optimal for:",
            (
                opt("linear Gaussian systems", correct=True),
                opt("nonlinear only"),
                opt("noise-free only"),
                opt("static only"),
            ),
            "Linear-Gaussian optimal estimator.",
        ),
        q(
            "LQG =",
            (
                opt("LQR + Kalman filter", correct=True),
                opt("two observers"),
                opt("no controller"),
                opt("PID only"),
            ),
            "By the separation principle.",
        ),
    ),
)
