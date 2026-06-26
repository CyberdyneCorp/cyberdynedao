"""Quiz questions for the Finite Element Analysis - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Convergence, consistency and error estimation": (
            q(
                "For an order-p element on a mesh of size h, the a-priori energy error scales like:",
                (
                    opt("h^p", correct=True),
                    opt("h^(-p)"),
                    opt("p^h"),
                    opt("a constant independent of h"),
                ),
                "The energy-norm error bound is C h^p |u|, so finer h lowers error.",
            ),
            q(
                "An a-posteriori error estimator (e.g. Zienkiewicz-Zhu) is used to:",
                (
                    opt("flag where error is large and drive adaptive refinement", correct=True),
                    opt("compute the exact solution"),
                    opt("remove all boundary conditions"),
                    opt("replace the mesh with one element"),
                ),
                "A-posteriori estimates guide where to refine since the exact error is unknown.",
            ),
            q(
                "The patch test checks that an element can reproduce a:",
                (
                    opt("constant strain (consistency/completeness)", correct=True),
                    opt("singular stress field"),
                    opt("negative Jacobian"),
                    opt("zero-energy mode"),
                ),
                "Passing the patch test (constant-strain reproduction) is needed for convergence.",
            ),
        ),
        "Nonlinear FEM and Newton-Raphson": (
            q(
                "Newton-Raphson drives which quantity to zero?",
                (
                    opt("the residual r = F_int - F_ext", correct=True),
                    opt("the mass matrix"),
                    opt("the Jacobian determinant"),
                    opt("the number of elements"),
                ),
                "Equilibrium is reached when the residual vanishes.",
            ),
            q(
                "The matrix updated each Newton iteration is the:",
                (
                    opt("tangent stiffness matrix", correct=True),
                    opt("identity matrix"),
                    opt("damping matrix"),
                    opt("permutation matrix"),
                ),
                "K_T = d F_int / d u is the tangent stiffness.",
            ),
            q(
                "With an exact tangent, Newton-Raphson converges:",
                (
                    opt("quadratically", correct=True),
                    opt("linearly"),
                    opt("never"),
                    opt("only after one step always"),
                ),
                "Quadratic convergence: the residual norm roughly squares each iteration.",
            ),
        ),
        "Dynamic and modal analysis": (
            q(
                "Modal analysis solves which type of problem?",
                (
                    opt("a generalized eigenvalue problem K phi = w^2 M phi", correct=True),
                    opt("a single linear static solve"),
                    opt("a topology optimization loop"),
                    opt("a Gauss quadrature sum"),
                ),
                "Natural frequencies and mode shapes come from the K-M eigenproblem.",
            ),
            q(
                "The equation of motion in dynamic FEM adds which matrices to K?",
                (
                    opt("mass M and damping C", correct=True),
                    opt("only the Jacobian"),
                    opt("only the B-matrix"),
                    opt("the conductivity matrix"),
                ),
                "M u'' + C u' + K u = F(t).",
            ),
            q(
                "Resonance occurs when the forcing frequency approaches the:",
                (
                    opt("natural frequency", correct=True),
                    opt("zero frequency"),
                    opt("Gauss point"),
                    opt("aspect ratio"),
                ),
                "Dynamic amplification peaks near a natural frequency.",
            ),
        ),
        "Verification, validation and result interpretation": (
            q(
                "Verification asks whether you:",
                (
                    opt("solved the equations correctly", correct=True),
                    opt("chose the right physical model"),
                    opt("matched a physical experiment"),
                    opt("used the prettiest colour map"),
                ),
                "Verification = solving the equations right; validation = solving the right equations.",
            ),
            q(
                "At a sharp re-entrant corner, the reported peak stress:",
                (
                    opt("diverges as the mesh is refined (singularity)", correct=True),
                    opt("converges to a finite value quickly"),
                    opt("is always zero"),
                    opt("equals the yield strength exactly"),
                ),
                "Stress singularities do not converge; use a fillet or a structural-stress method.",
            ),
            q(
                "Large stress jumps between adjacent elements usually indicate:",
                (
                    opt("an under-resolved mesh", correct=True),
                    opt("a perfectly converged result"),
                    opt("a correct singular field"),
                    opt("an error-free solution"),
                ),
                "Big inter-element discontinuities flag insufficient mesh resolution.",
            ),
        ),
        "Reduced-order models and ML surrogates": (
            q(
                "Proper orthogonal decomposition (POD) builds a reduced basis from:",
                (
                    opt("snapshots of full solutions via the SVD", correct=True),
                    opt("random noise only"),
                    opt("the mass matrix inverse"),
                    opt("a single coarse mesh"),
                ),
                "POD takes the dominant SVD modes of snapshot solutions.",
            ),
            q(
                "Reduced-order models are most valuable for:",
                (
                    opt("many-query tasks like optimization and digital twins", correct=True),
                    opt("a single one-off linear solve"),
                    opt("eliminating the need for any FEM data"),
                    opt("increasing the number of DOFs"),
                ),
                "ROMs pay off when the model is evaluated many times.",
            ),
            q(
                "Machine-learning surrogates and PINNs in FEM are best described as:",
                (
                    opt("complements trained on and validated against FEM", correct=True),
                    opt("exact replacements that never need FEM data"),
                    opt("unrelated to the governing physics"),
                    opt("methods that remove all boundary conditions"),
                ),
                "Surrogates are trained on FEM results and must be validated against them.",
            ),
        ),
        "Topology optimization and design-driven FEM": (
            q(
                "The SIMP method assigns each element a:",
                (
                    opt("density between 0 and 1, penalised toward 0 or 1", correct=True),
                    opt("fixed unit density always"),
                    opt("negative stiffness"),
                    opt("random temperature"),
                ),
                "SIMP uses E = rho^p E0 to push densities to black-and-white designs.",
            ),
            q(
                "The typical topology optimization objective is to minimise:",
                (
                    opt("compliance (maximise stiffness) under a mass constraint", correct=True),
                    opt("the number of nodes"),
                    opt("the Jacobian determinant"),
                    opt("the convergence rate"),
                ),
                "Minimum compliance for a fixed volume fraction is the classic problem.",
            ),
            q(
                "A density filter is applied in topology optimization to:",
                (
                    opt("avoid checkerboarding artifacts", correct=True),
                    opt("increase the residual"),
                    opt("make the Jacobian negative"),
                    opt("remove the load vector"),
                ),
                "Filtering suppresses checkerboard patterns and mesh dependence.",
            ),
        ),
    },
    final=(
        q(
            "Higher-order elements improve the convergence rate because the error scales as:",
            (
                opt("h^p with larger p", correct=True),
                opt("h regardless of order"),
                opt("1/h"),
                opt("a constant"),
            ),
            "The exponent p in h^p grows with element order.",
        ),
        q(
            "Geometric nonlinearity, plasticity and contact require:",
            (
                opt("iterative solution, e.g. Newton-Raphson", correct=True),
                opt("a single linear solve"),
                opt("removing the stiffness matrix"),
                opt("only modal analysis"),
            ),
            "Nonlinear problems need iteration because stiffness depends on the solution.",
        ),
        q(
            "Natural frequencies and mode shapes come from:",
            (
                opt("the generalized eigenvalue problem with K and M", correct=True),
                opt("a topology optimization loop"),
                opt("Gauss quadrature"),
                opt("the load vector alone"),
            ),
            "Solve K phi = w^2 M phi for frequencies and modes.",
        ),
        q(
            "A stress singularity at a sharp corner should be handled by:",
            (
                opt("adding a realistic fillet or using a structural-stress method", correct=True),
                opt("refining until the peak is reported"),
                opt("ignoring all boundary conditions"),
                opt("multiplying by the factor of safety"),
            ),
            "The singular peak never converges; model the real geometry instead.",
        ),
        q(
            "A reduced-order model accelerates analysis by:",
            (
                opt("projecting the system onto a small basis", correct=True),
                opt("adding more degrees of freedom"),
                opt("refining the mesh everywhere"),
                opt("removing the physics"),
            ),
            "ROMs solve a tiny reduced system instead of the full one.",
        ),
        q(
            "Topology optimization coupled with additive manufacturing enables:",
            (
                opt("lightweight, organically shaped, production-ready parts", correct=True),
                opt("only rectangular blocks"),
                opt("parts that cannot be manufactured at all"),
                opt("removal of the FEM solve"),
            ),
            "Optimized free-form geometries are realised by additive manufacturing.",
        ),
    ),
)
