"""Quiz questions for the Finite Element Analysis - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Element types and shape functions": (
            q(
                "Compared with a linear element, a quadratic element lets the strain vary:",
                (
                    opt("linearly instead of being constant", correct=True),
                    opt("not at all"),
                    opt("randomly"),
                    opt("only at the nodes"),
                ),
                "A quadratic field has a linear derivative, so strain varies linearly.",
            ),
            q(
                "Triangular elements commonly use which natural coordinates?",
                (
                    opt("area (barycentric) coordinates", correct=True),
                    opt("polar coordinates"),
                    opt("logarithmic coordinates"),
                    opt("complex coordinates"),
                ),
                "Triangles are interpolated with area/barycentric coordinates.",
            ),
            q(
                "Going from linear to quadratic elements (p-refinement) generally:",
                (
                    opt("improves accuracy per element at higher cost", correct=True),
                    opt("always reduces total cost"),
                    opt("makes the element matrix non-symmetric"),
                    opt("removes the need for boundary conditions"),
                ),
                "Higher order buys accuracy but needs more integration points and DOFs.",
            ),
        ),
        "Isoparametric mapping and the Jacobian": (
            q(
                "In an isoparametric element, the same shape functions interpolate:",
                (
                    opt("both the geometry and the field", correct=True),
                    opt("only the geometry"),
                    opt("only the load vector"),
                    opt("only the boundary conditions"),
                ),
                "Isoparametric means identical N_i for x(xi) and u(xi).",
            ),
            q(
                "The determinant of the Jacobian must be:",
                (
                    opt("positive everywhere in the element", correct=True),
                    opt("exactly zero"),
                    opt("negative"),
                    opt("equal to the number of nodes"),
                ),
                "A zero or negative det(J) means a folded/inverted element.",
            ),
            q(
                "The Jacobian is used to convert:",
                (
                    opt("derivatives between reference and physical coordinates", correct=True),
                    opt("forces into displacements"),
                    opt("stress into strain"),
                    opt("temperature into pressure"),
                ),
                "dN/dx = (1/J) dN/dxi relates the two coordinate systems.",
            ),
        ),
        "Numerical integration with Gauss quadrature": (
            q(
                "An m-point Gauss-Legendre rule integrates polynomials exactly up to degree:",
                (
                    opt("2m - 1", correct=True),
                    opt("m"),
                    opt("m - 1"),
                    opt("m + 2"),
                ),
                "m Gauss points exactly integrate degree 2m-1 polynomials.",
            ),
            q(
                "Gauss quadrature approximates an integral as a:",
                (
                    opt("weighted sum of the integrand at sample points", correct=True),
                    opt("simple average of all nodal values"),
                    opt("derivative at the midpoint"),
                    opt("maximum value times the length"),
                ),
                "Integral ~ sum w_p g(xi_p) over the Gauss points.",
            ),
            q(
                "Using too few integration points (excessive reduced integration) can cause:",
                (
                    opt("spurious hourglass zero-energy modes", correct=True),
                    opt("a non-symmetric stiffness matrix"),
                    opt("an exactly correct answer always"),
                    opt("the Jacobian to vanish by design"),
                ),
                "Under-integration can introduce hourglass modes that carry no stiffness.",
            ),
        ),
        "The 2D structural element and the B-matrix": (
            q(
                "The B-matrix relates nodal displacements to:",
                (
                    opt("strains", correct=True),
                    opt("nodal forces directly"),
                    opt("the Jacobian determinant"),
                    opt("the mass matrix"),
                ),
                "epsilon = B u; B holds the shape-function derivatives.",
            ),
            q(
                "The 2D element stiffness has the form k = integral of:",
                (
                    opt("B^T D B over the element", correct=True),
                    opt("B + D + B"),
                    opt("D divided by B"),
                    opt("N^T N only"),
                ),
                "k = integral B^T D B t dOmega, with D the constitutive matrix.",
            ),
            q(
                "The constant-strain triangle (CST) has a B-matrix that is:",
                (
                    opt("constant, so its stiffness needs no quadrature", correct=True),
                    opt("quadratic in position"),
                    opt("different at every Gauss point"),
                    opt("always singular"),
                ),
                "CST strain is constant, so k = t*A*B^T D B with no numerical integration.",
            ),
        ),
        "Steady-state heat conduction by FEM": (
            q(
                "In thermal FEM, the matrix analogous to structural stiffness is the:",
                (
                    opt("conductivity matrix", correct=True),
                    opt("mass matrix"),
                    opt("damping matrix"),
                    opt("identity matrix"),
                ),
                "K_T (conductivity) plays the role of K; nodal temperatures replace displacements.",
            ),
            q(
                "A convection (Robin) boundary condition adds terms to:",
                (
                    opt("both the conductivity matrix and the load vector", correct=True),
                    opt("neither the matrix nor the load"),
                    opt("only the Jacobian"),
                    opt("only the mass matrix"),
                ),
                "Convection adds h*A to K_T and h*A*Tinf to the load.",
            ),
            q(
                "The unknowns in a steady heat-conduction FEM model are the nodal:",
                (
                    opt("temperatures", correct=True),
                    opt("displacements"),
                    opt("stresses"),
                    opt("velocities"),
                ),
                "The solve gives nodal temperatures; flux is recovered afterward.",
            ),
        ),
        "Meshing strategy and element quality": (
            q(
                "A high element aspect ratio (long, thin elements) tends to:",
                (
                    opt("reduce accuracy", correct=True),
                    opt("improve accuracy"),
                    opt("have no effect"),
                    opt("make det(J) negative by definition"),
                ),
                "Distorted, high-aspect-ratio elements degrade accuracy.",
            ),
            q(
                "A mesh convergence study involves:",
                (
                    opt("solving on finer meshes until a key result stabilises", correct=True),
                    opt("solving once on the coarsest mesh"),
                    opt("changing the material each run"),
                    opt("removing all boundary conditions"),
                ),
                "Refine the mesh and confirm the result (e.g. peak stress) stops changing.",
            ),
            q(
                "Mesh refinement should be concentrated:",
                (
                    opt("where the field changes rapidly, e.g. fillets and holes", correct=True),
                    opt("uniformly everywhere regardless of geometry"),
                    opt("only far from the loads"),
                    opt("nowhere; coarse is always fine"),
                ),
                "Local refinement at stress concentrations is more efficient than global refinement.",
            ),
        ),
    },
    final=(
        q(
            "Quadratic elements converge faster than linear elements because they:",
            (
                opt("represent the field with higher-order polynomials", correct=True),
                opt("use fewer nodes"),
                opt("ignore the Jacobian"),
                opt("require no integration"),
            ),
            "Higher polynomial order raises the convergence rate.",
        ),
        q(
            "The Jacobian determinant going to zero or negative indicates:",
            (
                opt("a distorted or inverted element", correct=True),
                opt("a perfectly shaped element"),
                opt("an exact solution"),
                opt("a converged mesh"),
            ),
            "det(J) must stay positive; otherwise the mapping is invalid.",
        ),
        q(
            "Two-point Gauss quadrature integrates exactly polynomials up to degree:",
            (
                opt("3", correct=True),
                opt("1"),
                opt("2"),
                opt("5"),
            ),
            "2m-1 with m=2 gives degree 3.",
        ),
        q(
            "The element stiffness for a 2D solid is computed from:",
            (
                opt("B^T D B integrated over the element", correct=True),
                opt("N^T N only"),
                opt("the load vector squared"),
                opt("the inverse of the mass matrix"),
            ),
            "Stiffness uses the strain-displacement matrix B and constitutive matrix D.",
        ),
        q(
            "In heat-conduction FEM, a fixed-temperature boundary is a:",
            (
                opt("Dirichlet condition", correct=True),
                opt("Neumann condition"),
                opt("Robin condition only"),
                opt("zero-energy mode"),
            ),
            "Prescribing temperature is a Dirichlet (essential) condition.",
        ),
        q(
            "The most important practical lever on FEM accuracy and cost is the:",
            (
                opt("mesh", correct=True),
                opt("choice of plotting colours"),
                opt("file format"),
                opt("name of the solver"),
            ),
            "Mesh density and quality dominate accuracy and runtime.",
        ),
    ),
)
