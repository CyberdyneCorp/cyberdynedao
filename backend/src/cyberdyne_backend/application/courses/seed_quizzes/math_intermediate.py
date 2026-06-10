"""Curated quiz questions for the math-intermediate course. Keys are the EXACT
content-lesson titles; questions are grounded in each lesson body."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Vectors & linear algebra": (
            q(
                "What does the lesson say a vector is?",
                (
                    opt("A grid of numbers that transforms other vectors"),
                    opt("A list of numbers with direction and magnitude", correct=True),
                    opt("A single scalar rate of change"),
                    opt("The area accumulated under a curve"),
                ),
                "The lesson defines a vector as a list of numbers with direction and magnitude.",
            ),
            q(
                "How do vectors add according to the lesson?",
                (
                    opt("Component by component only after normalizing them"),
                    opt("By multiplying matching components together"),
                    opt("Tip-to-tail, closing the triangle", correct=True),
                    opt("By taking the cosine of the angle between them"),
                ),
                "The lesson states vectors add tip-to-tail so that u + v closes the triangle.",
            ),
            q(
                "What does the dot product measure?",
                (
                    opt("Alignment between two vectors", correct=True),
                    opt("The total area under a curve"),
                    opt("The rotation angle of a basis vector"),
                    opt("The number of components in a vector"),
                ),
                "The lesson says the dot product measures alignment and powers similarity and projections.",
            ),
        ),
        "Matrices, systems & transformations": (
            q(
                "What is a matrix described as in the lesson?",
                (
                    opt("A list of numbers with direction and magnitude"),
                    opt("A grid of numbers that transforms vectors", correct=True),
                    opt("The running area under a curve"),
                    opt("A single partial derivative"),
                ),
                "The lesson defines a matrix as a grid of numbers that transforms vectors via y = A x.",
            ),
            q(
                "What do the columns of a rotation matrix represent?",
                (
                    opt("The eigenvalues of the transformation"),
                    opt("Where the basis vectors land", correct=True),
                    opt("The area under the rotated curve"),
                    opt("The dot product of the inputs"),
                ),
                "The lesson notes that a matrix's columns are where the basis vectors land.",
            ),
            q(
                "What question does solving A x = b answer?",
                (
                    opt("What input produces this output?", correct=True),
                    opt("How aligned are two vectors?"),
                    opt("Which direction is steepest uphill?"),
                    opt("What is the total accumulated area?"),
                ),
                "The lesson frames A x = b as asking what input produces the given output.",
            ),
        ),
        "Derivatives, gradients & optimization": (
            q(
                "In which direction does the gradient point?",
                (
                    opt("Uphill, the direction of steepest increase", correct=True),
                    opt("Downhill, toward the minimum"),
                    opt("Tip-to-tail along the input axis"),
                    opt("Perpendicular to every basis vector"),
                ),
                "The lesson says the gradient points uphill, in the direction of steepest increase.",
            ),
            q(
                "What does the chain rule enable in deep networks?",
                (
                    opt("Solving linear systems by elimination"),
                    opt("Backpropagation to push gradients through the network", correct=True),
                    opt("Rotating the basis vectors of an image"),
                    opt("Computing the area under a loss curve"),
                ),
                "The lesson states the chain rule is what lets backpropagation push gradients through a deep network.",
            ),
            q(
                "What is the gradient descent update rule given in the lesson?",
                (
                    opt("Step uphill by adding the gradient"),
                    opt("Step downhill: x becomes x minus eta times f prime of x", correct=True),
                    opt("Replace x with the matrix inverse times b"),
                    opt("Set x to the dot product of the inputs"),
                ),
                "The lesson minimizes by stepping downhill: x is updated to x minus eta times the derivative.",
            ),
        ),
        "Integrals: accumulation & area": (
            q(
                "What does the integral represent if the derivative is a rate?",
                (
                    opt("The total accumulated, the area under a curve", correct=True),
                    opt("The direction of steepest increase"),
                    opt("The alignment between two vectors"),
                    opt("The eigenvalues of a transformation"),
                ),
                "The lesson says if the derivative is a rate, the integral is the total accumulated area under a curve.",
            ),
            q(
                "What does the Fundamental Theorem of Calculus tie together?",
                (
                    opt("Vectors and their dot products"),
                    opt("Integrating a rate recovers the quantity", correct=True),
                    opt("Matrices and their eigenvalues"),
                    opt("Gradients and basis vectors"),
                ),
                "The lesson states the Fundamental Theorem of Calculus shows integrating a rate recovers the quantity.",
            ),
            q(
                "How is integration usually done in code per the lesson?",
                (
                    opt("By inverting a matrix"),
                    opt("By summing many thin slices, a Riemann sum", correct=True),
                    opt("By taking partial derivatives"),
                    opt("By computing a single dot product"),
                ),
                "The lesson explains that in code you sum many thin slices, a Riemann sum, as numpy.trapz does.",
            ),
        ),
    },
    final=(
        q(
            "Which quantity measures the alignment between two vectors?",
            (
                opt("The dot product", correct=True),
                opt("The gradient"),
                opt("The Riemann sum"),
                opt("The rotation matrix"),
            ),
            "The dot product measures alignment between two vectors.",
        ),
        q(
            "A matrix in this course is best described as what?",
            (
                opt("A list of numbers with direction and magnitude"),
                opt("A grid of numbers that transforms vectors", correct=True),
                opt("The area under a curve"),
                opt("A single rate of change"),
            ),
            "A matrix is a grid of numbers that transforms vectors via y = A x.",
        ),
        q(
            "To minimize a loss with gradient descent, which way do you step?",
            (
                opt("Uphill, by adding the gradient"),
                opt("Downhill, against the derivative", correct=True),
                opt("Tip-to-tail along the basis"),
                opt("Toward the largest eigenvalue"),
            ),
            "Gradient descent steps downhill, updating x to x minus eta times the derivative.",
        ),
        q(
            "What does the integral of a rate give you?",
            (
                opt("The accumulated total, the area under the curve", correct=True),
                opt("The direction of steepest increase"),
                opt("The alignment of two vectors"),
                opt("The columns of a rotation matrix"),
            ),
            "The integral accumulates a rate into a total, the area under the curve.",
        ),
        q(
            "Which equation asks what input produces a given output?",
            (
                opt("A x = b", correct=True),
                opt("The dot product of u and v"),
                opt("The gradient of f"),
                opt("The integral from a to b"),
            ),
            "Solving A x = b asks what input produces the given output b.",
        ),
    ),
)
