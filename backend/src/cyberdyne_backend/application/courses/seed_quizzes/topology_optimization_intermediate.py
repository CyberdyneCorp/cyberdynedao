"""Quiz questions for the Topology Optimization - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The discrete compliance problem in FE": (
            q(
                "In FE, compliance separates as a sum over elements because:",
                (
                    opt(
                        "each element shares a reference k0 scaled by its SIMP modulus",
                        correct=True,
                    ),
                    opt("all elements have identical displacements"),
                    opt("the load is the same on every node"),
                    opt("the mesh is one element"),
                ),
                "c = sum_e E_e(rho) ue^T k0 ue separates cleanly per element.",
            ),
            q(
                "The global stiffness K is obtained by:",
                (
                    opt("assembling element contributions E_e * k0 into shared DOFs", correct=True),
                    opt("multiplying all element matrices together"),
                    opt("inverting the load vector"),
                    opt("averaging the densities"),
                ),
                "Element matrices are scattered into the global DOFs and summed.",
            ),
            q(
                "Why is a Cholesky factorisation appropriate for K u = F here?",
                (
                    opt("K is symmetric positive definite", correct=True),
                    opt("K is non-symmetric"),
                    opt("K is singular by design"),
                    opt("F is complex valued"),
                ),
                "The constrained elastic stiffness matrix is SPD.",
            ),
        ),
        "Adjoint sensitivity analysis": (
            q(
                "The adjoint method is used because it computes:",
                (
                    opt(
                        "all element sensitivities at the cost of about one extra solve",
                        correct=True,
                    ),
                    opt("only one sensitivity per run"),
                    opt("sensitivities by expensive finite differences"),
                    opt("the displacements, not the gradients"),
                ),
                "Adjoint gives the full gradient cheaply, essential for millions of variables.",
            ),
            q(
                "For minimum compliance the sensitivity dc/drho is:",
                (
                    opt("always negative: more material lowers compliance", correct=True),
                    opt("always positive"),
                    opt("always zero"),
                    opt("equal to the volume fraction"),
                ),
                "dc/drho = -p rho^(p-1)(E0-Emin) ue^T k0 ue is non-positive.",
            ),
            q(
                "Compliance is self-adjoint, which means:",
                (
                    opt("the adjoint vector equals -u, so no second solve is needed", correct=True),
                    opt("a second full linear solve is always required"),
                    opt("the gradient cannot be computed"),
                    opt("the problem has no constraints"),
                ),
                "Self-adjointness reuses the displacement field for the gradient.",
            ),
        ),
        "Sensitivity and density filtering": (
            q(
                "The sensitivity filter (Sigmund) smooths:",
                (
                    opt("the gradients before the update", correct=True),
                    opt("the displacement field"),
                    opt("the load vector"),
                    opt("the element connectivity"),
                ),
                "It averages dc/drho over a neighbourhood with cone weights.",
            ),
            q(
                "An advantage of the density filter over the sensitivity filter is:",
                (
                    opt(
                        "it is chain-rule consistent and easy to extend with projection",
                        correct=True,
                    ),
                    opt("it needs no filter radius"),
                    opt("it ignores neighbouring elements"),
                    opt("it removes the volume constraint"),
                ),
                "Smoothing densities and differentiating through is consistent and extensible.",
            ),
            q(
                "Increasing the filter radius rmin tends to produce:",
                (
                    opt("fewer, thicker members (larger minimum feature size)", correct=True),
                    opt("more, thinner members"),
                    opt("a checkerboard"),
                    opt("a singular stiffness matrix"),
                ),
                "rmin directly sets the minimum length scale.",
            ),
        ),
        "Optimality criteria and MMA updates": (
            q(
                "The Optimality Criteria (OC) update is best suited to:",
                (
                    opt("single volume-constrained compliance problems", correct=True),
                    opt("many simultaneous constraints"),
                    opt("non-differentiable objectives"),
                    opt("problems with no constraints"),
                ),
                "OC is a fast fixed-point scheme tailored to one volume constraint.",
            ),
            q(
                "In OC, the Lagrange multiplier lambda is found each iteration by:",
                (
                    opt("bisection to satisfy the volume constraint", correct=True),
                    opt("a single matrix inversion"),
                    opt("ignoring the volume entirely"),
                    opt("setting lambda = 0"),
                ),
                "A bisection on lambda enforces the target volume.",
            ),
            q(
                "The Method of Moving Asymptotes (MMA) is preferred when:",
                (
                    opt("there are many constraints (stress, multiple loads, etc.)", correct=True),
                    opt("there is exactly one volume constraint and nothing else"),
                    opt("no gradients are available"),
                    opt("the problem is one element"),
                ),
                "MMA builds a convex separable subproblem and handles many constraints.",
            ),
        ),
        "Heaviside projection for crisp designs": (
            q(
                "Heaviside projection is applied to:",
                (
                    opt("push filtered densities toward 0 or 1 around a threshold", correct=True),
                    opt("remove the volume constraint"),
                    opt("increase compliance"),
                    opt("randomise the densities"),
                ),
                "It sharpens the blurred boundary left by density filtering.",
            ),
            q(
                "As the projection sharpness beta increases, the design becomes:",
                (
                    opt("more nearly black-and-white (closer to 0/1)", correct=True),
                    opt("greyer and more blurred"),
                    opt("independent of the densities"),
                    opt("unconstrained in volume"),
                ),
                "Large beta approaches a true step function.",
            ),
            q(
                "Beta is typically increased gradually (continuation) so that:",
                (
                    opt("the problem stays smooth early and crisp late", correct=True),
                    opt("the solver never converges"),
                    opt("the volume constraint is dropped"),
                    opt("the mesh is refined automatically"),
                ),
                "Continuation avoids getting stuck in poor local minima.",
            ),
        ),
    },
    final=(
        q(
            "Compliance in the discrete FE form is written as:",
            (
                opt("a sum over elements of E_e(rho) ue^T k0 ue", correct=True),
                opt("the product of all element matrices"),
                opt("the inverse of the load vector"),
                opt("the determinant of K"),
            ),
            "Each element contributes its SIMP-scaled strain energy.",
        ),
        q(
            "The compliance sensitivity is dc/drho =",
            (
                opt("-p rho^(p-1) (E0-Emin) ue^T k0 ue", correct=True),
                opt("+p rho^(p-1) (E0-Emin) ue^T k0 ue"),
                opt("zero for all elements"),
                opt("the volume fraction"),
            ),
            "Negative and proportional to element strain energy.",
        ),
        q(
            "The key benefit of the adjoint method is:",
            (
                opt("full gradient at roughly the cost of one extra solve", correct=True),
                opt("avoiding any linear solve"),
                opt("computing only one derivative"),
                opt("eliminating the need for sensitivities"),
            ),
            "Adjoint sensitivity scales to millions of design variables.",
        ),
        q(
            "Filtering with radius rmin is needed to:",
            (
                opt("set a minimum length scale and remove checkerboards", correct=True),
                opt("make the matrix singular"),
                opt("increase compliance on purpose"),
                opt("remove the equilibrium equation"),
            ),
            "It regularises the otherwise mesh-dependent problem.",
        ),
        q(
            "Choose OC over MMA when:",
            (
                opt("the only constraint is a single volume budget", correct=True),
                opt("there are many stress constraints"),
                opt("no gradient is available"),
                opt("the objective is non-smooth"),
            ),
            "OC is the simple, fast choice for one-constraint compliance.",
        ),
        q(
            "Heaviside projection combined with robust formulations mainly delivers:",
            (
                opt("crisp 0/1 boundaries with a guaranteed minimum length scale", correct=True),
                opt("a greyer design"),
                opt("a faster linear solve"),
                opt("removal of the volume constraint"),
            ),
            "Eroded/dilated projections enforce length scale and sharpen edges.",
        ),
    ),
)
