"""Curated quiz for the Mathematics - Optimization & Backpropagation course.

Keys in ``per_lesson`` are the EXACT content-lesson titles from
``seed_math`` (slug ``math-optimization``); the seed interleaves a checkpoint
quiz after each content lesson plus the final comprehensive quiz.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The chain rule & computational graphs": (
            q(
                "According to the chain rule as stated, the derivative of f(g(x)) equals what?",
                (
                    opt("f'(x) times g'(x)"),
                    opt("f'(g(x)) times g'(x)", correct=True),
                    opt("f(g'(x)) plus g(f'(x))"),
                    opt("f'(g(x)) plus g'(x)"),
                ),
                "The chain rule multiplies the outer slope evaluated at g(x) by the inner slope g'(x).",
            ),
            q(
                "For h(x) = sin(x^2), what does the lesson give as h'(x)?",
                (
                    opt("cos(x^2) times 2x", correct=True),
                    opt("sin(2x) times x^2"),
                    opt("2x times sin(x^2)"),
                    opt("cos(2x)"),
                ),
                "Following the path x -> x^2 -> sin, the slope is cos(x^2) times the inner derivative 2x.",
            ),
            q(
                "In the multivariable chain rule on a computational graph, what do you do when a quantity feeds several paths?",
                (
                    opt("Take the maximum contribution among the paths"),
                    opt("Multiply the contributions from all paths together"),
                    opt("Add the contributions from each path", correct=True),
                    opt("Average the contributions across the paths"),
                ),
                "The lesson says if a quantity feeds several paths you add the contributions from each path.",
            ),
        ),
        "Backpropagation: gradients through a graph": (
            q(
                "How does backpropagation organize the chain rule to be cheap?",
                (
                    opt("It recomputes every path from scratch each time"),
                    opt("It sweeps the graph once forward then once backward", correct=True),
                    opt("It only ever sweeps the graph forward"),
                    opt("It randomly samples a subset of paths each step"),
                ),
                "Backprop does a single forward pass then a single backward pass instead of recomputing every path.",
            ),
            q(
                "What value does the backward pass start with at the loss node?",
                (
                    opt("dL/dL = 1", correct=True),
                    opt("dL/dL = 0"),
                    opt("the learning rate eta"),
                    opt("the squared error of the prediction"),
                ),
                "The backward pass begins with dL/dL = 1 and pushes gradients right to left.",
            ),
            q(
                "For a linear neuron yhat = wx + b with L = (yhat - y)^2, what is dL/dw?",
                (
                    opt("2(yhat - y)"),
                    opt("2(yhat - y) times x", correct=True),
                    opt("(yhat - y)^2 times x"),
                    opt("x squared"),
                ),
                "The lesson gives dL/dw = 2(yhat - y) times x.",
            ),
        ),
        "Linear optimization (Linear Programming)": (
            q(
                "In a linear program, where does the optimum sit?",
                (
                    opt("At the centre of the feasible region"),
                    opt("At a corner (vertex) of the feasible region", correct=True),
                    opt("Anywhere along an edge with equal value"),
                    opt("Outside the feasible region where cost is highest"),
                ),
                "Pushing the objective contours as far as possible lands the optimum at a vertex of the feasible region.",
            ),
            q(
                "Why does the simplex algorithm walk from vertex to vertex?",
                (
                    opt(
                        "Because the optimum of an LP sits at a corner of the region", correct=True
                    ),
                    opt("Because the feasible region has no interior points"),
                    opt("Because the objective is nonlinear"),
                    opt("Because vertices are the only feasible points"),
                ),
                "Since the LP optimum is always at a vertex, simplex just walks vertex to vertex.",
            ),
            q(
                "What do the dual variables of an LP represent, per the lesson?",
                (
                    opt("The number of constraints"),
                    opt(
                        "The shadow prices, how much the optimum improves per unit of relaxed constraint",
                        correct=True,
                    ),
                    opt("The slack in each inequality"),
                    opt("The coordinates of the optimal vertex"),
                ),
                "The dual variables are the shadow prices: the gain in the optimum per unit of relaxed constraint.",
            ),
        ),
        "Quadratic optimization & Lagrange multipliers": (
            q(
                "When Q is positive (semi)definite in a QP, what is true of the objective?",
                (
                    opt(
                        "It is a convex bowl, so any local minimum is the global one", correct=True
                    ),
                    opt("It has many disconnected minima"),
                    opt("It is linear in the variables"),
                    opt("It is unbounded below"),
                ),
                "A positive (semi)definite Q makes the objective a convex bowl, so a local minimum is global.",
            ),
            q(
                "What kind of optimization problem is least-squares line fitting?",
                (
                    opt("A linear program"),
                    opt("An unconstrained convex QP", correct=True),
                    opt("A nonconvex constrained problem"),
                    opt("An integer program"),
                ),
                "Minimising the sum of squared residuals is an unconstrained convex QP solved by the normal equations.",
            ),
            q(
                "At the optimum of f subject to an equality constraint g(x) = 0, the Lagrange condition states that the gradients are what?",
                (
                    opt("Orthogonal: grad f dotted with grad g is zero"),
                    opt("Parallel: grad f = lambda grad g", correct=True),
                    opt("Both zero at the optimum"),
                    opt("Equal in magnitude but opposite in sign"),
                ),
                "Tangency of the contour and the constraint means the gradients are parallel: grad f = lambda grad g.",
            ),
        ),
        "Lab: backprop & a constrained QP in code": (
            q(
                "In the lab, fitting yhat = w*x + b by gradient descent is described as backprop for what?",
                (
                    opt("A two-layer network"),
                    opt("A 1-neuron net", correct=True),
                    opt("A convolutional layer"),
                    opt("A decision tree"),
                ),
                "The lab comments that linear regression by gradient descent is backprop for a 1-neuron net.",
            ),
            q(
                "For the equality-constrained QP min x^2 + y^2 s.t. x + y = c, what is the optimum?",
                (
                    opt("x = 0, y = c"),
                    opt("x = y = c/2", correct=True),
                    opt("x = c, y = c"),
                    opt("x = y = c"),
                ),
                "Lagrange gives 2x = 2y = lambda so x = y, and x + y = c yields x = y = c/2.",
            ),
            q(
                "How does the lab sanity-check the QP optimum numerically?",
                (
                    opt(
                        "By projected gradient descent: step downhill then project onto the line x+y=c",
                        correct=True,
                    ),
                    opt("By exhaustively trying every integer pair"),
                    opt("By calling a library QP solver"),
                    opt("By inverting the matrix Q directly"),
                ),
                "The lab steps downhill on x^2+y^2 and projects back onto x+y=c each iteration (projected gradient descent).",
            ),
        ),
    },
    final=(
        q(
            "What is backpropagation, fundamentally?",
            (
                opt("A way to randomly perturb weights until the loss drops"),
                opt(
                    "The chain rule organised into one forward and one backward sweep of the graph",
                    correct=True,
                ),
                opt("A method that only works without any hidden composition"),
                opt("A replacement for gradient descent that needs no derivatives"),
            ),
            "Backprop is the chain rule arranged as a single forward pass plus a single backward pass.",
        ),
        q(
            "Which statement correctly contrasts a linear program (LP) with a quadratic program (QP)?",
            (
                opt(
                    "An LP has a linear objective; a QP has a quadratic objective with linear constraints",
                    correct=True,
                ),
                opt("An LP has a quadratic objective; a QP has a linear objective"),
                opt("Both have quadratic objectives and nonlinear constraints"),
                opt("Neither can have inequality constraints"),
            ),
            "An LP optimises a linear objective subject to linear inequalities; a QP minimises a quadratic objective under linear constraints.",
        ),
        q(
            "Why is training a network with millions of weights about as cheap as one forward pass?",
            (
                opt(
                    "Because every parameter's gradient comes out of a single backward sweep",
                    correct=True,
                ),
                opt("Because gradients are estimated rather than computed exactly"),
                opt("Because only one weight is updated per epoch"),
                opt("Because the loss surface is always a perfect bowl"),
            ),
            "A single backward sweep yields all gradients at once, so cost is comparable to one forward pass.",
        ),
        q(
            "Which condition characterises a constrained optimum via Lagrange multipliers for an equality constraint?",
            (
                opt("grad f = lambda grad g, the gradients are parallel at tangency", correct=True),
                opt("grad f equals zero on its own"),
                opt("grad g equals zero on its own"),
                opt("grad f and grad g are perpendicular"),
            ),
            "At a constrained optimum the objective contour is tangent to the constraint, so grad f = lambda grad g.",
        ),
        q(
            "Per the lesson, which real-world tasks are quadratic programs?",
            (
                opt("Dijkstra shortest path and BFS traversal"),
                opt(
                    "SVM margin maximisation and the Markowitz minimum-variance portfolio",
                    correct=True,
                ),
                opt("Sorting and hashing"),
                opt("Computing an adjacency matrix"),
            ),
            "The lesson lists the SVM margin and the Markowitz portfolio (and MPC) as QP applications.",
        ),
    ),
)
