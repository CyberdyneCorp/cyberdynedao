"""Quiz questions for the Topology Optimization - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Level-set and phase-field methods": (
            q(
                "A level-set method represents the structure as:",
                (
                    opt("the zero contour of a function phi: solid where phi >= 0", correct=True),
                    opt("a density per element only"),
                    opt("a fixed mesh of bars"),
                    opt("a single global scalar"),
                ),
                "Material is defined by the sign of the level-set function phi.",
            ),
            q(
                "The boundary evolves by solving which equation?",
                (
                    opt("a Hamilton-Jacobi advection equation driven by Vn", correct=True),
                    opt("the heat equation with no source"),
                    opt("Bernoulli's equation"),
                    opt("the ideal gas law"),
                ),
                "phi_t + Vn |grad phi| = 0 moves the boundary by the shape derivative.",
            ),
            q(
                "A classic limitation of basic level-set methods is:",
                (
                    opt(
                        "difficulty nucleating new holes without topological derivatives",
                        correct=True,
                    ),
                    opt("producing only grey boundaries"),
                    opt("being unable to represent any boundary"),
                    opt("requiring no shape derivative"),
                ),
                "Topological derivatives or phase-field terms restore hole nucleation.",
            ),
        ),
        "Stress-constrained topology optimization": (
            q(
                "Minimum-compliance design alone does not guarantee:",
                (
                    opt("that stresses stay below the yield limit (strength)", correct=True),
                    opt("that the structure is stiff"),
                    opt("that the volume constraint is met"),
                    opt("that K u = F holds"),
                ),
                "Stiffness is not strength; stress constraints must be added explicitly.",
            ),
            q(
                "The stress singularity phenomenon refers to:",
                (
                    opt(
                        "relaxed stress constraints in voids blocking convergence to 0/1",
                        correct=True,
                    ),
                    opt("the load going to infinity"),
                    opt("the mesh becoming infinitely fine"),
                    opt("the volume becoming negative"),
                ),
                "qp- or epsilon-relaxation is used to handle the singularity.",
            ),
            q(
                "Aggregating many local stress constraints with a p-norm or KS function:",
                (
                    opt(
                        "approximates the maximum stress with a few smooth constraints",
                        correct=True,
                    ),
                    opt("removes all stress constraints"),
                    opt("makes the problem non-differentiable"),
                    opt("increases the number of constraints to millions"),
                ),
                "As P grows the p-norm tends to the true max while staying smooth.",
            ),
        ),
        "Manufacturing constraints and additive overhang": (
            q(
                "The additive-manufacturing overhang constraint enforces:",
                (
                    opt(
                        "self-supporting surfaces above a critical angle (about 45 deg)",
                        correct=True,
                    ),
                    opt("a minimum part mass"),
                    opt("maximum compliance"),
                    opt("a single hole only"),
                ),
                "Down-facing surfaces steeper than the critical angle print without supports.",
            ),
            q(
                "A casting/moulding constraint typically requires:",
                (
                    opt("no enclosed voids and a valid draw direction", correct=True),
                    opt("as many enclosed voids as possible"),
                    opt("ignoring the mould geometry"),
                    opt("a maximum compliance objective"),
                ),
                "The part must be extractable from the mould without trapped cavities.",
            ),
            q(
                "Minimum length scale on members is usually achieved via:",
                (
                    opt("filtering plus robust (eroded/dilated) projection", correct=True),
                    opt("increasing the load"),
                    opt("removing the volume constraint"),
                    opt("using a single finite element"),
                ),
                "Robust formulations guarantee a controllable minimum feature size.",
            ),
        ),
        "Large-scale 3D and multiphysics design": (
            q(
                "The dominant per-iteration cost in large 3D topology optimization is:",
                (
                    opt("solving the linear system K u = F", correct=True),
                    opt("printing the part"),
                    opt("reading the mesh file"),
                    opt("evaluating the volume fraction"),
                ),
                "With 10^7+ elements the linear solve dominates.",
            ),
            q(
                "The field-standard solver for such problems is:",
                (
                    opt("matrix-free PCG with geometric multigrid preconditioning", correct=True),
                    opt("dense Gaussian elimination"),
                    opt("explicit time stepping"),
                    opt("a single LU factorisation per run"),
                ),
                "Matrix-free multigrid PCG scales to distributed clusters and GPUs.",
            ),
            q(
                "Extending to multiphysics (thermal, fluid, EM) mainly requires:",
                (
                    opt("an extra state equation and its adjoint per physics", correct=True),
                    opt("abandoning SIMP and filtering"),
                    opt("removing all constraints"),
                    opt("switching to hand calculation"),
                ),
                "The density + adjoint + filter + MMA scaffold is reused per physics.",
            ),
        ),
        "Machine learning and generative design": (
            q(
                "A CNN/U-Net surrogate for topology optimization typically:",
                (
                    opt("predicts a near-optimal density field in one forward pass", correct=True),
                    opt("replaces the laws of mechanics"),
                    opt("requires no training data"),
                    opt("outputs the load vector"),
                ),
                "It maps loads/BCs/volume fraction to a density, then is fine-tuned.",
            ),
            q(
                "Generative models (GANs, VAEs, diffusion) are used mainly to:",
                (
                    opt(
                        "explore diverse optimal-quality designs for the same problem", correct=True
                    ),
                    opt("guarantee a single unique solution"),
                    opt("eliminate the volume constraint"),
                    opt("compute exact stresses analytically"),
                ),
                "They support human-in-the-loop generative design with design variety.",
            ),
            q(
                "Adding a physics (compliance) term to the ML training loss ensures predictions are:",
                (
                    opt("mechanically plausible, not just visually similar", correct=True),
                    opt("always solid"),
                    opt("independent of the loads"),
                    opt("free of any error"),
                ),
                "A physics-informed loss keeps surrogate outputs structurally valid.",
            ),
        ),
    },
    final=(
        q(
            "Compared with SIMP, the chief advantage of level-set methods is:",
            (
                opt("a crisp, smooth boundary at every iteration", correct=True),
                opt("more grey elements"),
                opt("no need for any solve"),
                opt("guaranteed hole nucleation without extra terms"),
            ),
            "Clean boundaries ease stress evaluation and CAD export.",
        ),
        q(
            "Stress-constrained problems are hard mainly because of:",
            (
                opt(
                    "singularity, locality (many constraints) and nonlinear sensitivities",
                    correct=True,
                ),
                opt("having too few elements"),
                opt("the absence of any objective"),
                opt("a fixed topology"),
            ),
            "Relaxation plus aggregation tackle these difficulties.",
        ),
        q(
            "The AM overhang constraint is usually set around:",
            (
                opt("a 45-degree self-support angle", correct=True),
                opt("a 5-degree angle"),
                opt("a 90-degree angle only"),
                opt("any angle is fine"),
            ),
            "Surfaces above the critical angle print without sacrificial supports.",
        ),
        q(
            "Billion-element 3D designs are enabled mostly by:",
            (
                opt(
                    "matrix-free multigrid-preconditioned conjugate gradient solvers", correct=True
                ),
                opt("dense direct factorisation"),
                opt("hand calculation"),
                opt("removing the equilibrium equation"),
            ),
            "Scalable iterative solvers make extreme-scale optimization feasible.",
        ),
        q(
            "Across level-set, stress, manufacturing and multiphysics extensions, what stays constant?",
            (
                opt("the density/level-set + adjoint + filter + optimiser scaffold", correct=True),
                opt("the absence of any constraints"),
                opt("a single fixed mesh of one element"),
                opt("the lack of a sensitivity analysis"),
            ),
            "The same gradient-based loop is reused with new state equations.",
        ),
        q(
            "ML surrogates accelerate topology optimization primarily by:",
            (
                opt(
                    "predicting good initial layouts so fewer real iterations are needed",
                    correct=True,
                ),
                opt("replacing equilibrium with random guesses"),
                opt("removing the volume constraint"),
                opt("guaranteeing zero error without training"),
            ),
            "A learned initial density cuts the number of expensive FE solves.",
        ),
    ),
)
