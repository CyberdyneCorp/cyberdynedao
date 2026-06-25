"""Quiz questions for the Advanced Control Systems — Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "From classical to modern control": (
            q(
                "A key limitation of classical (transfer-function) control that state space addresses is:",
                (
                    opt("handling MIMO systems and internal states directly", correct=True),
                    opt("it cannot represent a gain"),
                    opt("it only works in discrete time"),
                    opt("it ignores stability entirely"),
                ),
                "State space naturally handles multi-input/multi-output systems and internal dynamics.",
            ),
            q(
                "Classical control is usually framed in which domain?",
                (
                    opt("the frequency / Laplace domain (transfer functions)", correct=True),
                    opt("the state-space time domain only"),
                    opt("the z-only domain"),
                    opt("no domain"),
                ),
                "Classical methods use transfer functions and frequency response.",
            ),
            q(
                "State-space control represents a system using:",
                (
                    opt("first-order differential equations in state variables", correct=True),
                    opt("only a single output equation"),
                    opt("Bode plots exclusively"),
                    opt("truth tables"),
                ),
                "The state equations are a set of coupled first-order ODEs.",
            ),
        ),
        "State-space representation (A, B, C, D)": (
            q(
                "In x' = Ax + Bu, the matrix A is the:",
                (
                    opt("system (state) matrix governing the internal dynamics", correct=True),
                    opt("input matrix"),
                    opt("output matrix"),
                    opt("feedthrough matrix"),
                ),
                "A is the state matrix; B is input, C is output, D is feedthrough.",
            ),
            q(
                "The output equation is:",
                (
                    opt("y = Cx + Du", correct=True),
                    opt("y = Ax + Bu"),
                    opt("x' = Cx"),
                    opt("u = Ax"),
                ),
                "Outputs are y = Cx + Du.",
            ),
            q(
                "The 'state' of a system is:",
                (
                    opt(
                        "the minimal information needed to predict its future given inputs",
                        correct=True,
                    ),
                    opt("only the output value"),
                    opt("the input signal"),
                    opt("the sampling rate"),
                ),
                "State captures all memory needed for future evolution.",
            ),
        ),
        "Solving the state equation & the transition matrix": (
            q(
                "The state-transition matrix for an LTI system is:",
                (
                    opt("the matrix exponential e^(At)", correct=True),
                    opt("the inverse of B"),
                    opt("C times D"),
                    opt("always the identity"),
                ),
                "The homogeneous solution is x(t) = e^(At) x(0).",
            ),
            q(
                "The full solution includes a convolution of e^(A(t-tau)) with:",
                (
                    opt("B u(tau)", correct=True),
                    opt("C x"),
                    opt("the eigenvalues"),
                    opt("the identity matrix"),
                ),
                "The forced response convolves the input through B.",
            ),
            q(
                "Eigenvalues of A appear in the response as:",
                (
                    opt("modal exponentials e^(lambda*t)", correct=True),
                    opt("constant offsets only"),
                    opt("the input amplitude"),
                    opt("the sample period"),
                ),
                "Each eigenvalue gives a natural mode.",
            ),
        ),
        "Stability via eigenvalues": (
            q(
                "A continuous-time LTI system is asymptotically stable iff all eigenvalues of A have:",
                (
                    opt("negative real parts", correct=True),
                    opt("positive real parts"),
                    opt("magnitude greater than 1"),
                    opt("zero imaginary parts"),
                ),
                "Left-half-plane eigenvalues mean stability.",
            ),
            q(
                "An eigenvalue on the imaginary axis (purely imaginary) gives:",
                (
                    opt("marginal stability / sustained oscillation", correct=True),
                    opt("exponential growth"),
                    opt("guaranteed decay"),
                    opt("no dynamics"),
                ),
                "Poles on the jw-axis are marginally stable.",
            ),
            q(
                "For discrete-time systems, stability requires eigenvalues:",
                (
                    opt("inside the unit circle (|z| < 1)", correct=True),
                    opt("with negative real parts"),
                    opt("on the real axis"),
                    opt("greater than 1"),
                ),
                "Discrete stability uses the unit circle.",
            ),
        ),
        "Controllability": (
            q(
                "A system is controllable if:",
                (
                    opt(
                        "any state can be reached from any initial state with suitable input",
                        correct=True,
                    ),
                    opt("its output is always zero"),
                    opt("it has no inputs"),
                    opt("A is diagonal"),
                ),
                "Controllability = ability to drive the state anywhere.",
            ),
            q(
                "Controllability is tested via the rank of:",
                (
                    opt("the controllability matrix [B AB A^2B ...]", correct=True),
                    opt("the matrix C only"),
                    opt("the identity matrix"),
                    opt("the D matrix"),
                ),
                "Full rank of the controllability matrix means controllable.",
            ),
            q(
                "An uncontrollable mode means:",
                (
                    opt("some state direction cannot be influenced by the input", correct=True),
                    opt("the system has no output"),
                    opt("the system is always unstable"),
                    opt("the input is too large"),
                ),
                "Uncontrollable modes can't be moved by feedback.",
            ),
        ),
        "Observability": (
            q(
                "A system is observable if:",
                (
                    opt("the initial state can be determined from the outputs", correct=True),
                    opt("it has no sensors"),
                    opt("the input is zero"),
                    opt("A is singular"),
                ),
                "Observability = state can be inferred from outputs.",
            ),
            q(
                "Observability is tested via the rank of:",
                (
                    opt("the observability matrix [C; CA; CA^2; ...]", correct=True),
                    opt("the matrix B"),
                    opt("the D matrix"),
                    opt("the input vector"),
                ),
                "Full rank of the observability matrix means observable.",
            ),
            q(
                "Controllability and observability are related by:",
                (
                    opt("duality (one is the other for the transposed system)", correct=True),
                    opt("being identical always"),
                    opt("being unrelated"),
                    opt("the sampling rate"),
                ),
                "They are dual properties.",
            ),
        ),
    },
    final=(
        q(
            "What primarily distinguishes modern (state-space) from classical control?",
            (
                opt("internal state & native MIMO handling", correct=True),
                opt("use of Bode plots"),
                opt("only single-input single-output"),
                opt("ignoring stability"),
            ),
            "State space exposes internal states and handles MIMO.",
        ),
        q(
            "In y = Cx + Du, D represents:",
            (
                opt("direct feedthrough from input to output", correct=True),
                opt("the state dynamics"),
                opt("the controllability"),
                opt("the eigenvalues"),
            ),
            "D is the feedthrough term.",
        ),
        q(
            "The homogeneous state solution is:",
            (
                opt("x(t) = e^(At) x(0)", correct=True),
                opt("x(t) = C x(0)"),
                opt("x(t) = B u"),
                opt("x(t) = D"),
            ),
            "Via the state-transition matrix e^(At).",
        ),
        q(
            "Continuous-time stability requires eigenvalues with:",
            (
                opt("negative real parts", correct=True),
                opt("positive real parts"),
                opt("|z| > 1"),
                opt("zero value"),
            ),
            "Left-half-plane poles.",
        ),
        q(
            "Controllability is checked with the rank of:",
            (
                opt("[B AB A^2B ...]", correct=True),
                opt("[C; CA; ...]"),
                opt("D"),
                opt("the identity"),
            ),
            "The controllability matrix.",
        ),
        q(
            "Observability and controllability are:",
            (
                opt("dual properties", correct=True),
                opt("the same property"),
                opt("unrelated"),
                opt("both about inputs"),
            ),
            "Dual via transposition.",
        ),
    ),
)
