"""Quiz questions for the Hydraulics & Pneumatics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Proportional and servo valves": (
            q(
                "Compared with a proportional valve, a servo valve typically has:",
                (
                    opt("near-zero deadband and higher bandwidth", correct=True),
                    opt("a larger overlap and deadband"),
                    opt("no electrical command"),
                    opt("lower precision"),
                ),
                "Servo valves use a pilot stage for near-zero lap and high bandwidth, at the cost of leakage.",
            ),
            q(
                "A servo valve's spool-to-command dynamics are commonly modelled as:",
                (
                    opt("a second-order system with natural frequency and damping", correct=True),
                    opt("a pure time delay only"),
                    opt("a constant gain"),
                    opt("a first-order integrator"),
                ),
                "x_v/u = wn^2 / (s^2 + 2 zeta wn s + wn^2).",
            ),
            q(
                "Rated flow of a valve at a different pressure drop scales with:",
                (
                    opt("the square root of the drop ratio", correct=True),
                    opt("the drop ratio directly"),
                    opt("the square of the drop ratio"),
                    opt("the inverse of the drop ratio"),
                ),
                "Q = Q_R sqrt(dp/dp_R), the orifice law.",
            ),
        ),
        "Dynamic modelling of the valve-cylinder-load system": (
            q(
                "The hydraulic natural frequency omega_h increases when:",
                (
                    opt("oil bulk modulus or piston area increases", correct=True),
                    opt("trapped volume or load mass increases"),
                    opt("hose compliance increases"),
                    opt("entrained air increases"),
                ),
                "omega_h = sqrt(4 beta A^2 / (Vt m)): higher beta and A raise it; larger Vt and m lower it.",
            ),
            q(
                "Why is the hydraulic natural frequency the key dynamic limit of a servo axis?",
                (
                    opt("it caps the achievable closed-loop bandwidth", correct=True),
                    opt("it sets the steady-state force"),
                    opt("it determines the reservoir size"),
                    opt("it fixes the pump displacement"),
                ),
                "Loop gain must stay below omega_h to avoid exciting the oil-column resonance.",
            ),
            q(
                "Entrained air or compliant hoses harm performance because they:",
                (
                    opt("lower the effective bulk modulus and omega_h", correct=True),
                    opt("raise the bulk modulus"),
                    opt("increase the piston area"),
                    opt("remove the load mass"),
                ),
                "They soften the oil column, dropping beta and the resonance frequency.",
            ),
        ),
        "Closed-loop position and force control": (
            q(
                "In a position servo, raising the loop gain Kv tends to:",
                (
                    opt("increase bandwidth but reduce damping", correct=True),
                    opt("increase both bandwidth and damping"),
                    opt("reduce both bandwidth and steady error"),
                    opt("have no effect on response"),
                ),
                "Higher Kv is faster but more oscillatory as it approaches omega_h.",
            ),
            q(
                "Velocity/acceleration feedforward is added mainly to:",
                (
                    opt("reduce following error during motion", correct=True),
                    opt("increase the deadband"),
                    opt("lower the bulk modulus"),
                    opt("disable the relief valve"),
                ),
                "Feedforward cuts tracking lag without raising feedback gain.",
            ),
            q(
                "For contact tasks, the appropriate control strategy is often:",
                (
                    opt("force or impedance / hybrid position-force control", correct=True),
                    opt("pure open-loop position"),
                    opt("constant pump speed only"),
                    opt("relief-valve cracking control"),
                ),
                "Contact tasks regulate force or impedance rather than position alone.",
            ),
        ),
        "Energy-efficient hydraulics: load sensing and digital": (
            q(
                "A load-sensing pump delivers a pressure equal to:",
                (
                    opt("the highest load pressure plus a small margin", correct=True),
                    opt("the maximum relief setting at all times"),
                    opt("atmospheric pressure"),
                    opt("zero until the actuator stalls"),
                ),
                "LS holds p_load + delta_p_margin, so output tracks demand.",
            ),
            q(
                "Digital hydraulics achieves near-proportional control by:",
                (
                    opt("switching banks of fast on/off valves in PWM/PCM patterns", correct=True),
                    opt("using a single throttling orifice"),
                    opt("varying the oil temperature"),
                    opt("changing the reservoir level"),
                ),
                "Parallel on/off valves switched digitally approximate proportional flow with binary efficiency.",
            ),
            q(
                "The efficiency advantage of load sensing is largest at:",
                (
                    opt("partial load, where throttling waste is worst", correct=True),
                    opt("full load only"),
                    opt("zero flow"),
                    opt("the relief setting"),
                ),
                "Fixed systems waste most at partial load; LS tracks demand there.",
            ),
        ),
        "Accumulators and transient analysis": (
            q(
                "The gas side of an accumulator follows:",
                (
                    opt("a polytropic law p V^n = const", correct=True),
                    opt("a linear pressure-volume relation"),
                    opt("Pascal's law"),
                    opt("the orifice equation"),
                ),
                "Gas behaviour is polytropic, n from ~1 (slow) to 1.4 (fast).",
            ),
            q(
                "The Joukowsky pressure surge from sudden valve closure is:",
                (
                    opt("rho times wave speed times velocity change", correct=True),
                    opt("rho times velocity squared"),
                    opt("bulk modulus times area"),
                    opt("flow divided by area"),
                ),
                "dp = rho a dv, with a = sqrt(beta/rho).",
            ),
            q(
                "Water-hammer surges are severe in hydraulics mainly because oil is:",
                (
                    opt("nearly incompressible with a high wave speed", correct=True),
                    opt("highly compressible like air"),
                    opt("very low density"),
                    opt("a perfect insulator"),
                ),
                "Low compressibility gives a wave speed of ~1200-1400 m/s, so abrupt stops spike pressure.",
            ),
        ),
        "Simulation, model-based design and optimisation": (
            q(
                "System simulators such as Simscape Fluids or Amesim solve:",
                (
                    opt("the coupled stiff ODE/DAE for pressures and flows", correct=True),
                    opt("only steady-state algebraic balances"),
                    opt("electrical circuits exclusively"),
                    opt("structural finite-element meshes"),
                ),
                "They integrate the coupled component DAEs, capturing compressibility and dynamics.",
            ),
            q(
                "Which optimisation method suits a black-box fluid-power simulator?",
                (
                    opt("genetic algorithms or Bayesian optimisation", correct=True),
                    opt("hand tuning only"),
                    opt("closed-form linear least squares"),
                    opt("Gaussian elimination"),
                ),
                "Gradient-free GA/BO methods handle non-differentiable simulator objectives.",
            ),
            q(
                "Validating a system model before building hardware lets engineers:",
                (
                    opt("catch cavitation, instability and sizing errors early", correct=True),
                    opt("eliminate the need for any testing"),
                    opt("remove the relief valve"),
                    opt("ignore compressibility"),
                ),
                "Model-based design exposes problems before metal is cut.",
            ),
        ),
    },
    final=(
        q(
            "The main difference between a servo and a proportional valve is:",
            (
                opt(
                    "the servo's pilot stage gives near-zero deadband and higher bandwidth",
                    correct=True,
                ),
                opt("the servo has no electrical input"),
                opt("the proportional valve has higher bandwidth"),
                opt("the servo cannot meter flow"),
            ),
            "Servo valves use a torque-motor pilot for precise, fast, low-lap control.",
        ),
        q(
            "The hydraulic natural frequency is given by:",
            (
                opt("sqrt(4 beta A^2 / (Vt m))", correct=True),
                opt("sqrt(Vt m / (4 beta A^2))"),
                opt("beta A / (Vt m)"),
                opt("4 beta / (A Vt)"),
            ),
            "omega_h = sqrt(4 beta A^2 / (Vt m)) sets the bandwidth limit.",
        ),
        q(
            "Raising the position-loop gain Kv generally makes the response:",
            (
                opt("faster but less damped", correct=True),
                opt("slower and more damped"),
                opt("unchanged"),
                opt("perfectly critically damped"),
            ),
            "Higher Kv increases bandwidth toward omega_h, reducing damping.",
        ),
        q(
            "A load-sensing system saves energy by:",
            (
                opt("supplying only the load pressure plus a small margin", correct=True),
                opt("running the pump at full pressure always"),
                opt("throttling all surplus flow to tank"),
                opt("increasing the relief setting"),
            ),
            "LS matches pump output to demand, cutting throttling loss.",
        ),
        q(
            "The Joukowsky surge from abrupt valve closure equals:",
            (
                opt("rho a dv", correct=True),
                opt("rho dv^2"),
                opt("beta / a"),
                opt("a / dv"),
            ),
            "dp = rho a dv, the pressure wave from stopping flow.",
        ),
        q(
            "Model-based design with system simulators is valuable because it:",
            (
                opt("predicts dynamics and faults before hardware is built", correct=True),
                opt("replaces all physical components"),
                opt("eliminates the need for sensors"),
                opt("guarantees zero pressure loss"),
            ),
            "Simulation captures coupled dynamics and supports optimisation pre-build.",
        ),
    ),
)
