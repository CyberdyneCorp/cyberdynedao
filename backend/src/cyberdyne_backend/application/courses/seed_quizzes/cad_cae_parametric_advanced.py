"""Quiz questions for the Parametric & Simulation-Driven Design - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Closing the CAD-CAE loop": (
            q(
                "In simulation-driven design the model is treated as:",
                (
                    opt(
                        "a black-box function y = f(x) from design variables to responses",
                        correct=True,
                    ),
                    opt("a fixed image that never changes"),
                    opt("a single material constant"),
                    opt("only a drawing sheet"),
                ),
                "Each evaluation is a full CAD-mesh-solve cycle mapping x to performance metrics y.",
            ),
            q(
                "The central practical challenge of the CAD-CAE loop is that:",
                (
                    opt("each evaluation is expensive (a full mesh-solve cycle)", correct=True),
                    opt("parameters cannot be changed"),
                    opt("solvers return no output"),
                    opt("geometry cannot be meshed"),
                ),
                "Because each f(x) call is costly, the field focuses on minimizing evaluations.",
            ),
            q(
                "In the loop, the optimizer/sampler is responsible for:",
                (
                    opt("choosing the next set of design variables to evaluate", correct=True),
                    opt("drawing the title block"),
                    opt("painting the part"),
                    opt("printing the assembly"),
                ),
                "The human states the objective; the optimizer decides which x to try next.",
            ),
        ),
        "Design of experiments and sensitivity": (
            q(
                "A full factorial grid with L levels and k factors needs how many points?",
                (
                    opt("L^k", correct=True),
                    opt("L times k"),
                    opt("L + k"),
                    opt("k / L"),
                ),
                "Full factorials explode as L^k, which motivates space-filling designs.",
            ),
            q(
                "Latin Hypercube Sampling is used to:",
                (
                    opt("cover the design space uniformly with few points", correct=True),
                    opt("guarantee L^k points"),
                    opt("avoid sampling entirely"),
                    opt("remove all design variables"),
                ),
                "LHS gives uniform marginal coverage with far fewer points than a grid.",
            ),
            q(
                "Sobol or main-effect sensitivity indices help you:",
                (
                    opt("rank which parameters actually move the response", correct=True),
                    opt("increase the number of factors"),
                    opt("delete the solver"),
                    opt("convert results to an image"),
                ),
                "Sensitivity analysis identifies influential factors so you fix the irrelevant ones.",
            ),
        ),
        "Surrogate models and response surfaces": (
            q(
                "A surrogate (metamodel) is used to:",
                (
                    opt("approximate the expensive function so exploration is cheap", correct=True),
                    opt("replace the CAD geometry permanently"),
                    opt("increase the solver cost"),
                    opt("remove all design variables"),
                ),
                "Surrogates fit f(x) from DOE points so further evaluation is nearly free.",
            ),
            q(
                "An advantage of Kriging / Gaussian-process regression over a plain polynomial fit is that it:",
                (
                    opt("returns a predictive variance (uncertainty) at each point", correct=True),
                    opt("never needs any training data"),
                    opt("ignores the sample points"),
                    opt("only works in one dimension"),
                ),
                "GPR interpolates the samples and reports uncertainty, which drives adaptive sampling.",
            ),
            q(
                "Adaptive sampling improves a surrogate by adding points where:",
                (
                    opt("predictive uncertainty or expected improvement is largest", correct=True),
                    opt("the surrogate is already most certain"),
                    opt("the design variables are fixed"),
                    opt("the mesh is coarsest"),
                ),
                "New samples target high-uncertainty or high-improvement regions where they matter most.",
            ),
        ),
        "Optimization algorithms for design": (
            q(
                "Gradient-based optimizers (SQP, interior-point) are best suited to problems that are:",
                (
                    opt("smooth and unimodal, scaling to many variables", correct=True),
                    opt("noisy and highly multimodal"),
                    opt("completely discontinuous"),
                    opt("undefined everywhere"),
                ),
                "Gradient methods converge fast on smooth problems using the objective gradient.",
            ),
            q(
                "Genetic algorithms and particle swarm are examples of:",
                (
                    opt("gradient-free / global optimizers", correct=True),
                    opt("interpolation surrogates"),
                    opt("meshing schemes"),
                    opt("file formats"),
                ),
                "These global, gradient-free methods handle noisy, multimodal black-box responses.",
            ),
            q(
                "A common robust strategy combines:",
                (
                    opt(
                        "a global search over a surrogate, polished by a gradient step on the true model",
                        correct=True,
                    ),
                    opt("only a single random guess"),
                    opt("no optimizer at all"),
                    opt("deleting the constraints"),
                ),
                "Global search finds the basin; a gradient step then refines the true optimum.",
            ),
        ),
        "Topology and generative design": (
            q(
                "Topology optimization (SIMP) primarily computes:",
                (
                    opt(
                        "the optimal material layout (element densities) for a load path",
                        correct=True,
                    ),
                    opt("the title block layout"),
                    opt("the mesh color"),
                    opt("the bill of materials"),
                ),
                "SIMP assigns each element a density and minimizes compliance under a volume budget.",
            ),
            q(
                "In SIMP, raising the penalization exponent p (about 3) pushes element densities toward:",
                (
                    opt("solid or void (clear 0/1 material)", correct=True),
                    opt("a uniform gray midpoint"),
                    opt("negative values"),
                    opt("values above one"),
                ),
                "Penalization makes intermediate densities inefficient, driving a clean solid/void layout.",
            ),
            q(
                "Topology-optimization output usually requires:",
                (
                    opt("interpretation and smoothing into manufacturable geometry", correct=True),
                    opt("no further work at all"),
                    opt("conversion to a 2D drawing only"),
                    opt("deletion of the loads"),
                ),
                "Raw density fields must be smoothed and made buildable, respecting AM/CNC constraints.",
            ),
        ),
        "Design automation pipelines and digital twins": (
            q(
                "A design automation pipeline chains:",
                (
                    opt(
                        "CAD APIs with a mesher, solver and optimizer, orchestrated by a script",
                        correct=True,
                    ),
                    opt("only a single drawing export"),
                    opt("nothing - it is fully manual"),
                    opt("just a spreadsheet"),
                ),
                "Process-integration tools chain regenerate, mesh, solve and optimize end to end.",
            ),
            q(
                "A digital twin keeps a model in sync with a physical asset by:",
                (
                    opt("calibrating parameters to sensor data over time", correct=True),
                    opt("freezing the model at delivery"),
                    opt("deleting all sensors"),
                    opt("ignoring measurements"),
                ),
                "Continuous calibration to measurements lets the twin predict behaviour and flag drift.",
            ),
            q(
                "As calibration data accumulates, a digital twin's prediction error tends to:",
                (
                    opt("decay toward a lower level", correct=True),
                    opt("grow without bound"),
                    opt("stay exactly at its initial value"),
                    opt("become undefined"),
                ),
                "More calibration updates reduce model error as parameters track reality.",
            ),
        ),
    },
    final=(
        q(
            "Simulation-driven design automates the loop of:",
            (
                opt(
                    "set parameters, regenerate, mesh, solve, decide next parameters", correct=True
                ),
                opt("draw once and never change"),
                opt("export an image only"),
                opt("print a title block"),
            ),
            "The model becomes a black-box f(x) inside an automated optimization loop.",
        ),
        q(
            "Space-filling DOE (LHS, Sobol) is preferred over a full grid because it:",
            (
                opt("covers the space well with far fewer expensive evaluations", correct=True),
                opt("always needs L^k points"),
                opt("avoids sampling the space"),
                opt("removes the design variables"),
            ),
            "Full factorials scale as L^k; space-filling designs fit a fixed evaluation budget.",
        ),
        q(
            "A surrogate model lets you optimize cheaply by:",
            (
                opt(
                    "approximating the solver response, then verifying the optimum once",
                    correct=True,
                ),
                opt("calling the full solver thousands of times"),
                opt("ignoring all DOE data"),
                opt("deleting the geometry"),
            ),
            "Optimize on the cheap surrogate, then confirm the predicted optimum with a true run.",
        ),
        q(
            "For a noisy, multimodal black-box response you would reach for a:",
            (
                opt(
                    "global optimizer such as a genetic algorithm or Bayesian optimization",
                    correct=True,
                ),
                opt("pure gradient-descent only"),
                opt("a single finite-difference step"),
                opt("no optimizer"),
            ),
            "Global methods tolerate noise and multiple optima; gradient methods suit smooth problems.",
        ),
        q(
            "Topology optimization differs from shape tuning because it:",
            (
                opt("computes the material layout itself for a given load path", correct=True),
                opt("only adjusts a fixed set of dimensions"),
                opt("requires no loads or supports"),
                opt("produces a 2D drawing"),
            ),
            "SIMP solves for element densities, inventing the structure rather than tuning a fixed shape.",
        ),
        q(
            "A digital twin extends a simulation-driven model past delivery by:",
            (
                opt("staying calibrated to a physical asset via sensor data", correct=True),
                opt("freezing and archiving the model"),
                opt("discarding the parametric definition"),
                opt("removing all simulation"),
            ),
            "The twin is continuously validated against reality, predicting behaviour and maintenance needs.",
        ),
    ),
)
