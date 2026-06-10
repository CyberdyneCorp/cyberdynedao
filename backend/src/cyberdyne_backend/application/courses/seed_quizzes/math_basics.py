"""Curated quiz questions for the Mathematics - Basics course (per-lesson
checkpoints keyed by EXACT content-lesson title, plus a final comprehensive
quiz). Kept beside the course module so the content stays readable."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Sets, logic & functions": (
            q(
                "Which Python operator gives the intersection of two sets A and B?",
                (
                    opt("A | B"),
                    opt("A & B", correct=True),
                    opt("A - B"),
                    opt("x in A"),
                ),
                "The lesson maps intersection (A cap B) to the Python operator A & B.",
            ),
            q(
                "According to the lesson, what does a function f guarantee about its mapping?",
                (
                    opt("It maps each input to exactly one output", correct=True),
                    opt("It maps each input to several possible outputs"),
                    opt("It only returns 0 or 1"),
                    opt("It changes its output for the same input over time"),
                ),
                "A function maps each input to exactly one output, like a pure function: same input gives same output.",
            ),
            q(
                "The lesson says a SQL JOIN corresponds to which set operation?",
                (
                    opt("A union"),
                    opt("A difference"),
                    opt("An intersection", correct=True),
                    opt("A complement"),
                ),
                "Databases are set machines: a SQL JOIN is an intersection and UNION is a union.",
            ),
        ),
        "Algebra: growth, exponentials & logs": (
            q(
                "At n = 8, how many steps does the quadratic n^2 curve need according to the lesson?",
                (
                    opt("256"),
                    opt("64", correct=True),
                    opt("16"),
                    opt("128"),
                ),
                "The lesson states that at n = 8 the quadratic needs 64 steps while the exponential needs 256.",
            ),
            q(
                "What is the logarithm log_b the inverse of?",
                (
                    opt("The polynomial x^n"),
                    opt("The exponential b^x", correct=True),
                    opt("The factorial n!"),
                    opt("The square root of x"),
                ),
                "The lesson defines log_b as the inverse of b^x, answering how many doublings.",
            ),
            q(
                "In the decay model e^(-kt), what happens when the rate k is raised?",
                (
                    opt("It decays faster, giving a shorter half-life", correct=True),
                    opt("It decays slower, giving a longer half-life"),
                    opt("It grows instead of decaying"),
                    opt("Nothing changes because k is a constant"),
                ),
                "Raising k makes the curve decay faster, since a larger rate means a shorter half-life t_1/2 = ln 2 / k.",
            ),
        ),
        "Graphs & transforming functions": (
            q(
                "In y = A sin(w x + phi) + c, which knob is the amplitude?",
                (
                    opt("A", correct=True),
                    opt("w"),
                    opt("phi"),
                    opt("c"),
                ),
                "The lesson labels A as the amplitude, the vertical stretch of the wave.",
            ),
            q(
                "What does the lesson call the points where a curve crosses y = 0?",
                (
                    opt("Its peaks"),
                    opt("Its roots", correct=True),
                    opt("Its asymptotes"),
                    opt("Its offsets"),
                ),
                "Where a curve crosses y = 0 are its roots, that is its solutions.",
            ),
            q(
                "In the wave family, which knob applies a horizontal shift?",
                (
                    opt("The amplitude A"),
                    opt("The offset c"),
                    opt("The phase phi", correct=True),
                    opt("The frequency w"),
                ),
                "Phase is the horizontal shift, while offset c is the vertical shift.",
            ),
        ),
        "Rates of change: the derivative": (
            q(
                "Geometrically, the derivative f'(x) is the slope of what?",
                (
                    opt("The secant line between two far points"),
                    opt("The tangent line at a point", correct=True),
                    opt("The horizontal axis"),
                    opt("The area under the curve"),
                ),
                "The derivative is the instantaneous rate of change, the slope of the tangent line at a point.",
            ),
            q(
                "Using the rules table, what is the derivative of x^n?",
                (
                    opt("n x^(n-1)", correct=True),
                    opt("x^(n-1)"),
                    opt("n x^(n+1)"),
                    opt("1/x"),
                ),
                "The rule table gives the derivative of x^n as n x^(n-1).",
            ),
            q(
                "Where the derivative f' equals 0, what does the lesson say about the curve?",
                (
                    opt("It is steepest"),
                    opt("It is flat, a maximum or minimum", correct=True),
                    opt("It is undefined"),
                    opt("It crosses the x-axis"),
                ),
                "Where f' = 0 the curve is flat, indicating a maximum or minimum, which is why optimization seeks those points.",
            ),
        ),
    },
    final=(
        q(
            "Which three foundational ideas does the course say almost everything in math and programming is built from?",
            (
                opt("Sets, logic, and functions", correct=True),
                opt("Vectors, matrices, and tensors"),
                opt("Loops, branches, and recursion"),
                opt("Addition, multiplication, and division"),
            ),
            "The first lesson states everything is built from sets, logic, and functions.",
        ),
        q(
            "Why does choosing an n log n algorithm over a 2^n one matter for large inputs?",
            (
                opt("Exponential growth dominates and explodes as n grows", correct=True),
                opt("Logarithmic growth always uses more memory"),
                opt("Quadratic growth is faster than linear growth"),
                opt("All growth rates are equal for large n"),
            ),
            "The algebra lesson shows exponential growth explodes, so the cheaper curve is what algorithm design is about.",
        ),
        q(
            "The derivative f'(x) is described as the instantaneous what?",
            (
                opt("Accumulated total"),
                opt("Rate of change", correct=True),
                opt("Average value"),
                opt("Maximum height"),
            ),
            "The derivative is the instantaneous rate of change, the slope of the curve at a point.",
        ),
        q(
            "Logarithms are useful because they turn multiplication into which operation?",
            (
                opt("Subtraction"),
                opt("Addition", correct=True),
                opt("Division"),
                opt("Exponentiation"),
            ),
            "The algebra lesson notes logarithms turn multiplication into addition and tame huge ranges.",
        ),
        q(
            "In y = A sin(w x + phi) + c, which knob controls the vertical offset?",
            (
                opt("A"),
                opt("w"),
                opt("phi"),
                opt("c", correct=True),
            ),
            "The offset c is the vertical shift in the wave transformation family.",
        ),
    ),
)
