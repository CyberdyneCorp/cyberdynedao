"""Curated quiz questions for the Vector Calculus - Basics course (per-lesson
checkpoints keyed by EXACT content-lesson title, plus a final comprehensive
quiz). Kept beside the course module so the content stays readable."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Scalar & vector fields": (
            q(
                "According to the lesson, what does a scalar field assign to every point in space?",
                (
                    opt("A whole arrow with magnitude and direction"),
                    opt("One number per point, such as temperature or altitude", correct=True),
                    opt("A rotation rate around the point"),
                    opt("A unit normal vector"),
                ),
                "A scalar field gives one number per point, like temperature, altitude, pressure, or a loss value.",
            ),
            q(
                "How does the lesson describe a vector field?",
                (
                    opt("It gives a single height value per point"),
                    opt(
                        "It gives a whole arrow with magnitude and direction per point",
                        correct=True,
                    ),
                    opt("It gives only the sign of the divergence per point"),
                    opt("It gives a level curve through each point"),
                ),
                "A vector field gives a whole arrow (magnitude plus direction) per point, like wind, water flow, or a force.",
            ),
            q(
                "Which example does the lesson use to illustrate a vector field that swirls?",
                (
                    opt("F = (-y, x)", correct=True),
                    opt("F = (x, y)"),
                    opt("F = (2x, 2y)"),
                    opt("f(x,y) = x^2 + y^2"),
                ),
                "The lesson shows the swirl vector field F = (-y, x) as its vector-field example.",
            ),
        ),
        "Partial derivatives & the gradient": (
            q(
                "What does a partial derivative of f with respect to x measure?",
                (
                    opt("The slope when you change only x and hold the rest fixed", correct=True),
                    opt("The total change when every variable moves together"),
                    opt("The rotation of the field around the x axis"),
                    opt("The flux of the field across the x axis"),
                ),
                "A partial derivative is the slope if you change only x and hold the other variables fixed.",
            ),
            q(
                "What two facts make the gradient central, according to the lesson?",
                (
                    opt("It points downhill and its length is the curvature"),
                    opt(
                        "It points in the direction of steepest increase and its length is the steepness",
                        correct=True,
                    ),
                    opt("It is always perpendicular to itself and has unit length"),
                    opt("It points toward the minimum and its length is the area"),
                ),
                "The gradient points in the direction of steepest increase, and its length is the steepness there.",
            ),
            q(
                "For the bowl f(x,y) = x^2 + y^2, what is the gradient?",
                (
                    opt("(-y, x)"),
                    opt("(2x, 2y)", correct=True),
                    opt("(x, y)"),
                    opt("(2, 2)"),
                ),
                "The gradient of f = x^2 + y^2 is (2x, 2y), pointing outward away from the minimum.",
            ),
        ),
        "Directional derivatives & level curves": (
            q(
                "How does the lesson express the directional derivative of f in a unit direction u?",
                (
                    opt("As the cross product of the gradient with u"),
                    opt("As the dot product of the gradient with u", correct=True),
                    opt("As the sum of the partial derivatives"),
                    opt("As the magnitude of the gradient times the area"),
                ),
                "The directional derivative is the dot product of the gradient with the unit direction u.",
            ),
            q(
                "When is the directional derivative zero, according to the lesson?",
                (
                    opt("When you walk along the gradient"),
                    opt("When you walk perpendicular to the gradient", correct=True),
                    opt("When the gradient has unit length"),
                    opt("When the field has zero divergence"),
                ),
                "Walking perpendicular to the gradient gives a zero directional derivative, so f stays constant.",
            ),
            q(
                "What is the key geometric fact stated about the gradient and level curves?",
                (
                    opt("The gradient is parallel to the level curves"),
                    opt("The gradient is always perpendicular to the level curves", correct=True),
                    opt("The gradient points along the level curves"),
                    opt("The gradient has zero length on a level curve"),
                ),
                "The gradient is always perpendicular to the level curves (contour lines).",
            ),
        ),
        "Steepest ascent & descent": (
            q(
                "To minimise a loss or energy f, which direction does the lesson say you step along?",
                (
                    opt("Along +grad f"),
                    opt("Along -grad f", correct=True),
                    opt("Perpendicular to grad f"),
                    opt("Along a level curve"),
                ),
                "To minimise f you step along -grad f, the steepest-downhill direction, which is gradient descent.",
            ),
            q(
                "What name does the lesson give to repeatedly stepping along -grad f?",
                (
                    opt("Gradient descent", correct=True),
                    opt("Line integration"),
                    opt("Divergence theorem"),
                    opt("Level-curve tracing"),
                ),
                "Stepping along -grad f is gradient descent, the workhorse of optimisation and machine learning.",
            ),
            q(
                "What does the lesson say about the step size eta in gradient descent?",
                (
                    opt("Larger is always faster and safer"),
                    opt("Too small is slow and too large overshoots", correct=True),
                    opt("It has no effect on convergence"),
                    opt("It must equal the gradient length"),
                ),
                "The step size eta is a trade-off: too small is slow, too large overshoots.",
            ),
        ),
    },
    final=(
        q(
            "Which best distinguishes a scalar field from a vector field?",
            (
                opt(
                    "A scalar field gives one number per point while a vector field gives an arrow per point",
                    correct=True,
                ),
                opt("A scalar field gives an arrow while a vector field gives a number"),
                opt("Both give arrows but with different colors"),
                opt("A scalar field only exists in 3D and a vector field only in 2D"),
            ),
            "A scalar field assigns one number per point, while a vector field assigns a whole arrow (magnitude and direction).",
        ),
        q(
            "What are the two defining properties of the gradient covered in the course?",
            (
                opt("It points downhill and its length is the curvature"),
                opt(
                    "It points in the direction of steepest increase and its length is the steepness",
                    correct=True,
                ),
                opt("It is perpendicular to the gradient and has unit length"),
                opt("It measures rotation and its length is the area enclosed"),
            ),
            "The gradient points in the direction of steepest increase, and its length equals the steepness.",
        ),
        q(
            "The directional derivative grad f dot u is zero when walking in which direction?",
            (
                opt("Along the gradient"),
                opt("Perpendicular to the gradient, tracing a level curve", correct=True),
                opt("Straight uphill"),
                opt("In the direction of steepest descent"),
            ),
            "Walking perpendicular to the gradient gives a zero directional derivative and keeps f constant along a level curve.",
        ),
        q(
            "Which update rule does the course give for gradient descent?",
            (
                opt("x_{n+1} = x_n + eta * grad f(x_n)"),
                opt("x_{n+1} = x_n - eta * grad f(x_n)", correct=True),
                opt("x_{n+1} = x_n - eta * f(x_n)"),
                opt("x_{n+1} = grad f(x_n)"),
            ),
            "Gradient descent updates x_{n+1} = x_n - eta * grad f(x_n), stepping along the steepest-downhill direction.",
        ),
        q(
            "For f(x,y) = x^2 + y^2, what is the gradient and how does it relate to the level curves?",
            (
                opt(
                    "(2x, 2y), pointing outward and perpendicular to the circular level curves",
                    correct=True,
                ),
                opt("(2x, 2y), pointing inward and parallel to the level curves"),
                opt("(-y, x), swirling along the level curves"),
                opt("(x, y), tangent to the level curves"),
            ),
            "The gradient of x^2 + y^2 is (2x, 2y), pointing outward and perpendicular to the circular level curves.",
        ),
    ),
)
