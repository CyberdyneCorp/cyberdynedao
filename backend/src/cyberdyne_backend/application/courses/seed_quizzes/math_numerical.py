from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Floating point, error & conditioning": (
            q(
                "Why does the lesson say 0.1 + 0.2 is not exactly equal to 0.3?",
                (
                    opt("Python rounds all decimals up by default"),
                    opt(
                        "Computers store reals in finite precision, so most numbers are slightly rounded",
                        correct=True,
                    ),
                    opt("Addition is not associative on real numbers"),
                    opt("The numbers exceed the maximum representable value"),
                ),
                "Floating point stores reals in finite precision, so almost every number is slightly rounded.",
            ),
            q(
                "How does round-off error behave as the step size gets smaller?",
                (
                    opt(
                        "It rises, because more operations accumulate tiny representation errors",
                        correct=True,
                    ),
                    opt("It falls, like truncation error"),
                    opt("It stays constant regardless of step size"),
                    opt("It disappears entirely"),
                ),
                "Round-off is accumulated tiny representation errors and gets worse with more operations and smaller steps.",
            ),
            q(
                "What is catastrophic cancellation as described in the lesson?",
                (
                    opt("Multiplying two very large numbers and overflowing"),
                    opt(
                        "Subtracting two nearly-equal numbers, which destroys significant digits",
                        correct=True,
                    ),
                    opt("Dividing by a number close to zero"),
                    opt("Rounding a number to the nearest integer"),
                ),
                "Catastrophic cancellation is subtracting two nearly-equal numbers, which destroys significant digits.",
            ),
        ),
        "Root-finding: bisection & Newton": (
            q(
                "What does the lesson say about bisection's convergence?",
                (
                    opt("It always converges, gaining one bit of accuracy per step", correct=True),
                    opt("It converges quadratically, doubling correct digits per step"),
                    opt("It only converges when f is differentiable"),
                    opt("It may diverge from a bad starting point"),
                ),
                "Bisection always converges if f changes sign across the interval, gaining one bit of accuracy per step.",
            ),
            q(
                "What is the Newton update formula given in the lesson?",
                (
                    opt("x_{n+1} = x_n + f(x_n)/f'(x_n)"),
                    opt("x_{n+1} = x_n - f(x_n)/f'(x_n)", correct=True),
                    opt("x_{n+1} = (a + b)/2"),
                    opt("x_{n+1} = x_n - f'(x_n)/f(x_n)"),
                ),
                "Newton's method follows the tangent down to the axis using x_{n+1} = x_n - f(x_n)/f'(x_n).",
            ),
            q(
                "When can Newton's method diverge according to the lesson?",
                (
                    opt("Only when the function has no real root"),
                    opt(
                        "From a bad start or where the derivative is approximately zero",
                        correct=True,
                    ),
                    opt("Whenever the interval does not change sign"),
                    opt("Only on polynomials of degree higher than two"),
                ),
                "Newton can diverge from a bad start or where f' is approximately zero, so robust solvers blend it with bisection.",
            ),
        ),
        "Interpolation & curve fitting": (
            q(
                "How does the lesson distinguish interpolation from fitting?",
                (
                    opt(
                        "Interpolation passes a curve through the points, while fitting finds a curve near noisy points",
                        correct=True,
                    ),
                    opt("Interpolation only works on linear data, fitting on nonlinear data"),
                    opt("Interpolation uses least squares, fitting passes through every point"),
                    opt("They are two names for the same operation"),
                ),
                "Interpolation passes through the points; least-squares fitting finds a simple curve near noisy points without hitting each one.",
            ),
            q(
                "What is the Runge phenomenon?",
                (
                    opt(
                        "A single high-degree polynomial oscillates wildly between the data points",
                        correct=True,
                    ),
                    opt("Splines fail to connect smoothly at the knots"),
                    opt("Round-off error grows as the step size shrinks"),
                    opt("A least-squares fit ignores outliers in the data"),
                ),
                "Fitting a single high-degree polynomial to many points oscillates wildly between them, the Runge phenomenon.",
            ),
            q(
                "What fix does the lesson recommend for the Runge trap?",
                (
                    opt("Use an even higher-degree polynomial"),
                    opt(
                        "Use cubic splines, low-degree polynomials stitched smoothly piece by piece",
                        correct=True,
                    ),
                    opt("Add more data points and refit a single polynomial"),
                    opt("Switch from interpolation to Newton's method"),
                ),
                "The fix is cubic splines, low-degree polynomials stitched smoothly piece by piece.",
            ),
        ),
        "Stability & integrating ODEs": (
            q(
                "What is the explicit Euler step given in the lesson?",
                (
                    opt("y_{n+1} = y_n + h f(t_n, y_n)", correct=True),
                    opt("y_{n+1} = y_n - f(y_n)/f'(y_n)"),
                    opt("y_{n+1} = (y_n + y_{n-1})/2"),
                    opt("y_{n+1} = y_n times e raised to minus k h"),
                ),
                "The simplest stepper is explicit Euler: y_{n+1} = y_n + h f(t_n, y_n).",
            ),
            q(
                "For decay y' = -k y, what is the Euler stability condition?",
                (
                    opt("h < 1/k"),
                    opt("h < 2/k", correct=True),
                    opt("h > 2/k"),
                    opt("h equals k/2"),
                ),
                "Euler multiplies by (1 - kh) each step, so it is stable only when |1 - kh| < 1, meaning h < 2/k.",
            ),
            q(
                "What does the lesson recommend for stiff systems with very different time scales?",
                (
                    opt("Explicit Euler with a tiny fixed step"),
                    opt(
                        "Implicit methods like backward Euler, which stay stable at large h",
                        correct=True,
                    ),
                    opt("Bisection on the time axis"),
                    opt("Cubic spline interpolation of the solution"),
                ),
                "Stiff systems force tiny explicit steps, so implicit methods like backward Euler are used to stay stable at large h.",
            ),
        ),
        "Lab: root-finding & a stable integrator": (
            q(
                "In the lab, which equation is solved for its root sqrt(2)?",
                (
                    opt("f(x) = x^2 - 2 = 0", correct=True),
                    opt("f(x) = 1/(1 + 25 x^2)"),
                    opt("y' = -k y"),
                    opt("f(x) = 2x"),
                ),
                "The lab solves f(x) = x^2 - 2 = 0, whose root is sqrt(2) = 1.41421356.",
            ),
            q(
                "What does the lab note about Newton versus bisection step counts?",
                (
                    opt(
                        "Newton reaches full precision in about 5 steps while bisection needs about 50",
                        correct=True,
                    ),
                    opt("Both reach full precision in about 8 steps"),
                    opt("Bisection is faster, needing only about 5 steps"),
                    opt("Newton needs 50 steps and bisection needs 5"),
                ),
                "The lab notes Newton reaches full precision in about 5 steps while bisection needs about 50.",
            ),
            q(
                "Why does the lab's Euler run with h = 0.6 oscillate and explode?",
                (
                    opt(
                        "Because k h = 2.4, so |1 - k h| = 1.4 which is greater than 1",
                        correct=True,
                    ),
                    opt("Because round-off error dominates at large steps"),
                    opt("Because the true answer e^(-8) is negative"),
                    opt("Because bisection failed to bracket the root"),
                ),
                "With k = 4 and h = 0.6, k h = 2.4 so |1 - k h| = 1.4 > 1, making the result oscillate and explode.",
            ),
        ),
    },
    final=(
        q(
            "Which pairing of error sources matches the lesson's U-shaped total error?",
            (
                opt("Round-off rises as the step shrinks while truncation falls", correct=True),
                opt("Both round-off and truncation fall as the step shrinks"),
                opt("Truncation rises as the step shrinks while round-off falls"),
                opt("Both round-off and truncation are independent of step size"),
            ),
            "Shrinking the step lowers truncation but raises round-off, so total error is U-shaped with a sweet spot.",
        ),
        q(
            "Which statement about root-finding methods is correct?",
            (
                opt("Bisection converges quadratically and Newton always converges"),
                opt(
                    "Bisection always converges but is slow while Newton converges quadratically when it works",
                    correct=True,
                ),
                opt("Both bisection and Newton gain one bit of accuracy per step"),
                opt("Newton always converges and never needs a derivative"),
            ),
            "Bisection always converges but slowly; Newton converges quadratically when it works but can diverge.",
        ),
        q(
            "What is the recommended remedy for the Runge phenomenon?",
            (
                opt("Higher-degree single polynomials"),
                opt("Cubic splines, low-degree polynomials stitched smoothly", correct=True),
                opt("Catastrophic cancellation"),
                opt("Backward Euler integration"),
            ),
            "Cubic splines avoid the wild oscillation of a single high-degree polynomial in the Runge phenomenon.",
        ),
        q(
            "For y' = -k y integrated with explicit Euler, when does the simulation stay stable?",
            (
                opt("When h is greater than 2/k"),
                opt("When |1 - kh| < 1, equivalently h < 2/k", correct=True),
                opt("When h equals 1/k exactly"),
                opt("Always, regardless of step size"),
            ),
            "Explicit Euler is stable for decay only when |1 - kh| < 1, which means h < 2/k.",
        ),
        q(
            "Which method does the lesson highlight for far less error at the same step size h?",
            (
                opt("Bisection"),
                opt("RK4 (Runge-Kutta), using cleverly weighted sub-steps", correct=True),
                opt("Explicit Euler with a larger h"),
                opt("Linear interpolation"),
            ),
            "Higher-order methods like RK4 take cleverly weighted sub-steps for far less error at the same h.",
        ),
    ),
)
