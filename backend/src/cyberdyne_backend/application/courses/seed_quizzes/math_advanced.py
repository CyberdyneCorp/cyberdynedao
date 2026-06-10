"""Curated quiz questions for the Mathematics - Advanced course
(slug ``math-advanced``): a checkpoint quiz after each content lesson plus a
final comprehensive quiz. Keys are the EXACT content-lesson titles."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Ordinary differential equations (ODEs)": (
            q(
                "What does an ODE relate?",
                (
                    opt("A function to partial derivatives in several variables"),
                    opt("A function to its own derivatives", correct=True),
                    opt("Two unrelated functions of time"),
                    opt("A matrix to its eigenvalues"),
                ),
                "An ODE relates a function to its own derivatives, describing how a quantity evolves given the rule for its rate.",
            ),
            q(
                "What is the solution of the first-order ODE dy/dt = k*y?",
                (
                    opt("An exponential y = y0 * e^(k t)", correct=True),
                    opt("A straight line y = k t"),
                    opt("A logistic S-curve"),
                    opt("A damped cosine"),
                ),
                "When the rate of change is proportional to the amount, the solution is the exponential y = y0 * e^(k t).",
            ),
            q(
                "In the second-order ODE m*x'' + c*x' + k*x = 0, what does the damping c decide?",
                (
                    opt("The total mass of the system"),
                    opt("The spring stiffness"),
                    opt("Whether the system rings or settles smoothly", correct=True),
                    opt("The amplitude of the driving force"),
                ),
                "The damping c decides whether the second-order system rings (oscillates) or settles smoothly.",
            ),
        ),
        "Partial differential equations (PDEs)": (
            q(
                "How does a PDE differ from an ODE?",
                (
                    opt("It involves partial derivatives in several variables", correct=True),
                    opt("It only ever has exponential solutions"),
                    opt("It cannot depend on time"),
                    opt("It relates a function to a single derivative only"),
                ),
                "A PDE involves partial derivatives in several variables, usually space and time, unlike an ODE.",
            ),
            q(
                "In the wave equation, what happens to disturbances?",
                (
                    opt("They smooth out and flatten over time"),
                    opt("They travel at speed c without changing shape", correct=True),
                    opt("They grow exponentially without bound"),
                    opt("They stay fixed in place forever"),
                ),
                "In the wave equation, disturbances travel at speed c without changing shape, like sound or light.",
            ),
            q(
                "What characterises the behaviour of the heat (diffusion) equation?",
                (
                    opt("Sharp features smooth out over time", correct=True),
                    opt("A disturbance travels at constant speed"),
                    opt("The solution oscillates forever"),
                    opt("Energy is added at every point"),
                ),
                "In the heat equation, sharp features smooth out over time, the same math as a Gaussian blur.",
            ),
        ),
        "Graphs & graph theory": (
            q(
                "What is a graph composed of?",
                (
                    opt("Rows and columns of numbers only"),
                    opt("Nodes (vertices) joined by edges", correct=True),
                    opt("A single continuous curve"),
                    opt("A set of partial derivatives"),
                ),
                "A graph is a set of nodes (vertices) joined by edges, modelling networks of all kinds.",
            ),
            q(
                "How is a graph stored as an adjacency matrix?",
                (
                    opt("A_ij = 1 if nodes i and j are connected", correct=True),
                    opt("A_ij equals the distance squared between nodes"),
                    opt("Each row lists the degree of every node"),
                    opt("It stores only the shortest path lengths"),
                ),
                "The adjacency matrix sets A_ij = 1 when nodes i and j are connected, linking graphs back to linear algebra.",
            ),
            q(
                "Which algorithm is named for computing a shortest path?",
                (
                    opt("Euler's method"),
                    opt("Dijkstra", correct=True),
                    opt("The simplex method"),
                    opt("Gradient descent"),
                ),
                "Dijkstra (and A*) computes shortest paths, used in GPS routing and network packets.",
            ),
        ),
        "Numerical lab: solve it in code": (
            q(
                "How does Euler's method step an ODE forward?",
                (
                    opt("y_next = y + (dy/dt)*dt", correct=True),
                    opt("y_next = y * dt"),
                    opt("y_next = y - lr * grad"),
                    opt("y_next = (y + dt) / 2"),
                ),
                "Euler's method steps forward in tiny increments: y_next = y + (dy/dt)*dt.",
            ),
            q(
                "What is the gradient-descent update used to minimise f(x) = (x-3)^2?",
                (
                    opt("x_next = x + lr * f'(x)"),
                    opt("x_next = x - lr * f'(x)", correct=True),
                    opt("x_next = x * f'(x)"),
                    opt("x_next = f'(x) / lr"),
                ),
                "Gradient descent steps downhill: x_next = x - lr * f'(x), converging to the true minimum at 3.",
            ),
            q(
                "How does the lab compute the numerical integral of sin(x) on [0, pi]?",
                (
                    opt("By a Riemann sum using the midpoint rule", correct=True),
                    opt("By Euler's method on a second-order ODE"),
                    opt("By projecting onto a constraint line"),
                    opt("By taking a single tangent slope"),
                ),
                "The lab sums many thin slices via a Riemann sum with the midpoint rule, giving the exact answer of 2.",
            ),
        ),
    },
    final=(
        q(
            "Which equation is the canonical first-order ODE whose solution is exponential?",
            (
                opt("dy/dt = k*y", correct=True),
                opt("d2u/dt2 = c^2 * d2u/dx2"),
                opt("du/dt = alpha * d2u/dx2"),
                opt("nabla^2 u = 0"),
            ),
            "dy/dt = k*y is the first-order ODE, with exponential solution y = y0 * e^(k t).",
        ),
        q(
            "Which PDE describes a hot spot spreading and flattening over time?",
            (
                opt("The wave equation"),
                opt("The heat (diffusion) equation", correct=True),
                opt("Laplace's equation"),
                opt("The logistic equation"),
            ),
            "The heat (diffusion) equation makes sharp features smooth out, spreading a hot spot over time.",
        ),
        q(
            "What does the logistic equation y' = r*y*(1 - y/K) produce?",
            (
                opt("A travelling wave"),
                opt("A bounded S-curve that saturates", correct=True),
                opt("Unbounded exponential growth"),
                opt("A straight line"),
            ),
            "The logistic equation gives a saturating S-curve, modelling epidemics and product adoption.",
        ),
        q(
            "In graph theory, what do powers of the adjacency matrix A^n count?",
            (
                opt("The number of nodes"),
                opt("Paths of length n", correct=True),
                opt("The total edge weight"),
                opt("The eigenvalues of the graph"),
            ),
            "Powers of the adjacency matrix, A^n, count paths of length n between nodes.",
        ),
        q(
            "Which three numerical workhorses does the Advanced code lab implement from scratch?",
            (
                opt("Euler's method, gradient descent, and a Riemann-sum integral", correct=True),
                opt("Backpropagation, the simplex method, and Bayes' rule"),
                opt("Matrix inversion, eigen-decomposition, and FFT"),
                opt("Dijkstra, BFS, and DFS"),
            ),
            "The lab implements Euler's method for an ODE, gradient descent, and a Riemann-sum integral of sin.",
        ),
    ),
)
