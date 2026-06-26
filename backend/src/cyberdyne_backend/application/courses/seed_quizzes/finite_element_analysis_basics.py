"""Quiz questions for the Finite Element Analysis - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why discretise: from continuum to elements": (
            q(
                "The finite element method replaces a continuous body with:",
                (
                    opt("a mesh of small elements joined at nodes", correct=True),
                    opt("a single large element"),
                    opt("an exact closed-form solution"),
                    opt("a random cloud of points with no connectivity"),
                ),
                "FEM discretises the domain into elements connected at nodes.",
            ),
            q(
                "As the mesh is refined with more, smaller elements, the discretisation error generally:",
                (
                    opt("decreases", correct=True),
                    opt("increases"),
                    opt("stays exactly the same"),
                    opt("becomes negative"),
                ),
                "Smaller elements track the true field better, lowering error (at higher cost).",
            ),
            q(
                "FEM is needed because most real engineering PDEs:",
                (
                    opt("have no closed-form solution on complex geometry", correct=True),
                    opt("are always linear and trivial"),
                    opt("can only be solved by hand"),
                    opt("never have boundary conditions"),
                ),
                "On realistic geometry analytical solutions usually do not exist, so we discretise.",
            ),
        ),
        "Nodes, elements and interpolation": (
            q(
                "Inside an element the field is approximated as:",
                (
                    opt("a weighted sum of nodal values using shape functions", correct=True),
                    opt("a single constant equal to the average load"),
                    opt("the exact analytical solution"),
                    opt("the determinant of the stiffness matrix"),
                ),
                "u(x) = sum N_i(x) u_i interpolates the nodal values.",
            ),
            q(
                "The Kronecker-delta property of a shape function N_i means it equals:",
                (
                    opt("1 at its own node and 0 at every other node", correct=True),
                    opt("0 everywhere"),
                    opt("1 everywhere"),
                    opt("the nodal force at node i"),
                ),
                "N_i is 1 at node i and 0 at all other nodes.",
            ),
            q(
                "For a 2-node linear bar element, the strain inside the element is:",
                (
                    opt("constant", correct=True),
                    opt("quadratic in x"),
                    opt("cubic in x"),
                    opt("discontinuous at the centre"),
                ),
                "Linear interpolation gives a constant derivative, hence constant strain.",
            ),
        ),
        "Strong form vs weak form": (
            q(
                "The weak (variational) form is obtained from the strong form by:",
                (
                    opt(
                        "multiplying by a test function, integrating and integrating by parts",
                        correct=True,
                    ),
                    opt("differentiating twice more"),
                    opt("ignoring the boundary conditions"),
                    opt("setting all derivatives to zero"),
                ),
                "Weighting and integration by parts produce the weak form and lower smoothness needs.",
            ),
            q(
                "An advantage of the weak form is that it:",
                (
                    opt("requires less smoothness of the solution u", correct=True),
                    opt("requires u to be infinitely differentiable"),
                    opt("eliminates the need for a mesh"),
                    opt("removes all boundary conditions"),
                ),
                "Integration by parts moves a derivative onto the test function, so u can be less smooth.",
            ),
            q(
                "Essential (Dirichlet) boundary conditions in FEM prescribe the:",
                (
                    opt("value of the field, e.g. displacement", correct=True),
                    opt("applied flux or force only"),
                    opt("number of Gauss points"),
                    opt("element aspect ratio"),
                ),
                "Dirichlet conditions fix the field value; Neumann conditions fix the flux/force.",
            ),
        ),
        "The 1D bar element": (
            q(
                "The 1D bar element stiffness matrix is proportional to:",
                (
                    opt("EA/L", correct=True),
                    opt("L/(EA)"),
                    opt("EA*L"),
                    opt("E/(A*L)"),
                ),
                "k = (EA/L) [[1,-1],[-1,1]]; it behaves like a spring of stiffness EA/L.",
            ),
            q(
                "An unconstrained bar element stiffness matrix is:",
                (
                    opt("singular, because rigid-body translation is possible", correct=True),
                    opt("always invertible"),
                    opt("non-symmetric"),
                    opt("negative definite"),
                ),
                "Without boundary conditions the bar can translate freely, so K is singular.",
            ),
            q(
                "The bar element behaves physically like a:",
                (
                    opt("linear spring", correct=True),
                    opt("rigid body"),
                    opt("damper"),
                    opt("point mass"),
                ),
                "Its force-elongation law F = (EA/L) delta is that of a linear spring.",
            ),
        ),
        "Assembly into a global system": (
            q(
                "Assembly builds the global stiffness matrix by:",
                (
                    opt("scatter-adding each element matrix into global node slots", correct=True),
                    opt("multiplying all element matrices together"),
                    opt("inverting each element matrix first"),
                    opt("discarding shared-node contributions"),
                ),
                "Element contributions superpose at shared nodes (scatter-add).",
            ),
            q(
                "Before applying boundary conditions, the raw global stiffness matrix is:",
                (
                    opt("singular due to rigid-body modes", correct=True),
                    opt("always diagonal"),
                    opt("guaranteed positive definite"),
                    opt("equal to the identity matrix"),
                ),
                "Rigid-body motion makes K singular until constraints are applied.",
            ),
            q(
                "At a node shared by two elements, the stiffness contributions:",
                (
                    opt("add together (superpose)", correct=True),
                    opt("cancel out"),
                    opt("are averaged"),
                    opt("are ignored"),
                ),
                "Overlapping entries from both elements are summed during assembly.",
            ),
        ),
        "Where FEM is used: a first workflow": (
            q(
                "The standard FEM workflow has three phases:",
                (
                    opt("pre-processing, solution, post-processing", correct=True),
                    opt("meshing, meshing, meshing"),
                    opt("guess, check, give up"),
                    opt("compile, link, run"),
                ),
                "Pre-process (mesh/BCs), solve K u = F, then post-process and validate.",
            ),
            q(
                "A result from an FEM solver should always be:",
                (
                    opt("validated against theory, hand calculations or tests", correct=True),
                    opt("accepted without question"),
                    opt("reported only as a colour plot"),
                    opt("multiplied by the factor of safety to fix errors"),
                ),
                "Validation against known checks is mandatory before trusting results.",
            ),
            q(
                "Which of these is a widely used FEM software package?",
                (
                    opt("ANSYS", correct=True),
                    opt("Photoshop"),
                    opt("Excel macros only"),
                    opt("a word processor"),
                ),
                "ANSYS, Abaqus, COMSOL and CalculiX are common FEM tools.",
            ),
        ),
    },
    final=(
        q(
            "In FEM, the unknown field is represented by values at the:",
            (
                opt("nodes", correct=True),
                opt("Gauss weights"),
                opt("element centroids only"),
                opt("load vector entries"),
            ),
            "Nodal values are interpolated by shape functions over each element.",
        ),
        q(
            "Shape functions satisfy the partition-of-unity property, meaning they:",
            (
                opt("sum to 1 everywhere in the element", correct=True),
                opt("sum to 0 everywhere"),
                opt("are all equal to each other"),
                opt("equal the stiffness matrix"),
            ),
            "Summing to 1 lets the element reproduce a constant field exactly.",
        ),
        q(
            "The global FEM equation that is solved is:",
            (
                opt("K u = F", correct=True),
                opt("u = K F"),
                opt("F = u / K"),
                opt("K = u F"),
            ),
            "Assembled stiffness times nodal unknowns equals the load vector.",
        ),
        q(
            "The weak form is preferred over the strong form because it:",
            (
                opt("needs less smoothness and suits piecewise interpolation", correct=True),
                opt("requires infinitely smooth solutions"),
                opt("avoids boundary conditions entirely"),
                opt("gives no boundary terms at all"),
            ),
            "It lowers the differentiability required of the field, matching FEM functions.",
        ),
        q(
            "A 2-node linear bar element produces strain that is:",
            (
                opt("constant within the element", correct=True),
                opt("always zero"),
                opt("cubic"),
                opt("infinite at the nodes"),
            ),
            "Linear displacement gives a constant derivative, so constant strain.",
        ),
        q(
            "The raw, unconstrained global stiffness matrix is singular until:",
            (
                opt("boundary conditions remove rigid-body motion", correct=True),
                opt("it is multiplied by the load"),
                opt("the mesh is deleted"),
                opt("the factor of safety is applied"),
            ),
            "Applying Dirichlet constraints makes the reduced system solvable.",
        ),
    ),
)
