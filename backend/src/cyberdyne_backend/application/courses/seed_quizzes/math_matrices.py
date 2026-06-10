from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What a matrix is (and represents)": (
            q(
                "What does the shape m x n of a matrix refer to?",
                (
                    opt("m columns and n rows"),
                    opt("m rows and n columns", correct=True),
                    opt("the number of nonzero entries"),
                    opt("the determinant times the trace"),
                ),
                "The lesson defines a matrix as a grid with m rows and n columns, its shape m x n.",
            ),
            q(
                "According to the lesson, where do the basis vectors land under a matrix?",
                (
                    opt("on the rows of the matrix"),
                    opt("on the diagonal of the matrix"),
                    opt("on the columns of the matrix", correct=True),
                    opt("at the origin"),
                ),
                "The key fact is that the columns of a matrix are where the basis vectors land.",
            ),
            q(
                "Which special matrix leaves vectors unchanged?",
                (
                    opt("the zero matrix"),
                    opt("a diagonal matrix"),
                    opt("the identity matrix I", correct=True),
                    opt("an orthogonal matrix"),
                ),
                "The lesson states the identity I leaves vectors unchanged.",
            ),
        ),
        "Core operations in MATLAB & Python": (
            q(
                "How does indexing differ between MATLAB and NumPy?",
                (
                    opt("MATLAB is 1-indexed, NumPy is 0-indexed", correct=True),
                    opt("MATLAB is 0-indexed, NumPy is 1-indexed"),
                    opt("both are 0-indexed"),
                    opt("both are 1-indexed"),
                ),
                "The lesson warns that MATLAB is 1-indexed while NumPy is 0-indexed.",
            ),
            q(
                "In NumPy, which operator performs the matrix product?",
                (
                    opt("the * operator"),
                    opt("the @ operator", correct=True),
                    opt("the .* operator"),
                    opt("the backslash operator"),
                ),
                "In NumPy @ is the matrix product while * is element-wise; in MATLAB they are flipped.",
            ),
            q(
                "For a matrix product (m x n)(n x p), what must hold?",
                (
                    opt("the outer dimensions must match"),
                    opt("both matrices must be square"),
                    opt("the inner dimensions must match", correct=True),
                    opt("the determinants must be equal"),
                ),
                "The lesson states the inner dimensions must match, giving an m x p result.",
            ),
        ),
        "Matrices as transformations": (
            q(
                "How do you compose two transformations?",
                (
                    opt("by adding their matrices"),
                    opt("by multiplying their matrices", correct=True),
                    opt("by taking their determinants"),
                    opt("by transposing one of them"),
                ),
                "Composing transformations is multiplying their matrices, applied right-to-left.",
            ),
            q(
                "What does a determinant of 0 mean for a transformation?",
                (
                    opt("space is rotated without distortion"),
                    opt("space is squashed flat and the matrix is non-invertible", correct=True),
                    opt("the matrix is the identity"),
                    opt("areas are doubled"),
                ),
                "A determinant of 0 means space is squashed flat, so the matrix is non-invertible.",
            ),
            q(
                "A 2 x 2 matrix maps the unit circle to what shape?",
                (
                    opt("a square"),
                    opt("a line"),
                    opt("an ellipse", correct=True),
                    opt("a parabola"),
                ),
                "Because a matrix is defined by where it sends the basis, it maps the unit circle to an ellipse.",
            ),
        ),
        "Solving linear systems": (
            q(
                "Geometrically, what is the solution of a 2 x 2 linear system?",
                (
                    opt("the point where the two lines cross", correct=True),
                    opt("the sum of the two lines"),
                    opt("the area between the lines"),
                    opt("the slope of the first line"),
                ),
                "Each row is a line and the solution is where they meet, the crossing point.",
            ),
            q(
                "What happens when det A = 0 for a system?",
                (
                    opt("there is always a unique solution"),
                    opt("the matrix is singular with no or infinite solutions", correct=True),
                    opt("the system is always overdetermined"),
                    opt("the lines always cross at the origin"),
                ),
                "When det A = 0 the matrix is singular, giving no or infinite solutions.",
            ),
            q(
                "For an overdetermined noisy system, which approach is used?",
                (
                    opt("matrix inversion"),
                    opt("the least-squares best fit", correct=True),
                    opt("eigenvalue decomposition"),
                    opt("the identity transform"),
                ),
                "Overdetermined systems have no exact solution, so we take the least-squares best fit.",
            ),
        ),
        "Eigenvalues & where ML uses matrices": (
            q(
                "What defines an eigenvector of a matrix A?",
                (
                    opt("it is sent to the zero vector"),
                    opt("it stays on its own line and is merely scaled", correct=True),
                    opt("it is always a column of the identity"),
                    opt("it changes direction by 90 degrees"),
                ),
                "Eigenvectors stay on their own line and are merely scaled by the eigenvalue lambda.",
            ),
            q(
                "In machine learning, how is a dataset typically represented as a matrix X?",
                (
                    opt("rows are features, columns are samples"),
                    opt("rows are samples, columns are features", correct=True),
                    opt("rows and columns are both weights"),
                    opt("it is always a single column vector"),
                ),
                "The lesson says data is a matrix X with rows as samples and columns as features.",
            ),
            q(
                "What does a dense fully-connected layer compute?",
                (
                    opt("the determinant of the inputs"),
                    opt("the matrix-vector product y = W x + b", correct=True),
                    opt("the inverse of the weights"),
                    opt("an element-wise product only"),
                ),
                "A dense layer computes y = W x + b, a matrix-vector product with learned weights W.",
            ),
        ),
        "Lab: matrix operations from scratch": (
            q(
                "In the lab, how is each entry of the product C = A * B computed?",
                (
                    opt("by multiplying matching entries element by element"),
                    opt("as a row of A dotted with a column of B", correct=True),
                    opt("by adding a row of A to a column of B"),
                    opt("as the determinant of a 2 x 2 block"),
                ),
                "Each entry is a row of A dotted with a column of B.",
            ),
            q(
                "How does the lab compute the determinant of the 2 x 2 matrix A?",
                (
                    opt("A[0][0] * A[1][1] - A[0][1] * A[1][0]", correct=True),
                    opt("A[0][0] + A[1][1]"),
                    opt("A[0][0] * A[0][1] - A[1][0] * A[1][1]"),
                    opt("A[0][1] * A[1][0]"),
                ),
                "The lab computes det as A[0][0]*A[1][1] - A[0][1]*A[1][0].",
            ),
            q(
                "What does the lab note happens if you make A singular with rows [1,2] and [2,4]?",
                (
                    opt("the product A * B becomes the identity"),
                    opt("det = 0, so there is no unique solution", correct=True),
                    opt("the transpose equals A"),
                    opt("the solver returns two distinct solutions"),
                ),
                "The lab notes that making A singular gives det = 0, so there is no unique solution.",
            ),
        ),
    },
    final=(
        q(
            "Which of the three roles of a matrix unlocks the others according to the course?",
            (
                opt("a table of data"),
                opt("a system of equations"),
                opt("a linear transformation", correct=True),
                opt("a determinant value"),
            ),
            "The transformation view is described as the one that unlocks everything else.",
        ),
        q(
            "Which operator pairing is correct for the matrix product?",
            (
                opt("MATLAB uses .* and NumPy uses *"),
                opt("MATLAB uses * and NumPy uses @", correct=True),
                opt("both use @"),
                opt("MATLAB uses @ and NumPy uses .*"),
            ),
            "In MATLAB * is the matrix product; in NumPy @ is the matrix product.",
        ),
        q(
            "What does a zero determinant indicate about a matrix?",
            (
                opt("it is orthogonal"),
                opt("it is the identity"),
                opt("it is singular and non-invertible", correct=True),
                opt("it doubles all areas"),
            ),
            "A determinant of 0 means the matrix squashes space flat and is singular, hence non-invertible.",
        ),
        q(
            "Which technique generalises eigen-analysis to any matrix?",
            (
                opt("the determinant"),
                opt("the SVD", correct=True),
                opt("Gaussian elimination"),
                opt("the transpose"),
            ),
            "The lesson states the SVD generalises eigen-analysis to any matrix.",
        ),
        q(
            "Why do GPUs and TPUs matter for machine learning per the course?",
            (
                opt("they store data as spreadsheets"),
                opt("they are giant matrix-multiply engines", correct=True),
                opt("they compute determinants in parallel"),
                opt("they invert matrices faster than solvers"),
            ),
            "The course explains GPUs and TPUs exist because they are giant matrix-multiply engines.",
        ),
    ),
)
