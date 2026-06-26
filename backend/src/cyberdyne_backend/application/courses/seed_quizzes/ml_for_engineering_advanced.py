"""Quiz questions for the Machine Learning for Engineering & Simulation - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Reduced-order models with POD": (
            q(
                "Proper orthogonal decomposition is computed via:",
                (
                    opt("the SVD of a matrix of solution snapshots", correct=True),
                    opt("gradient descent on the residual"),
                    opt("a random projection of the mesh"),
                    opt("the inverse of the stiffness matrix"),
                ),
                "POD is the SVD applied to snapshot data.",
            ),
            q(
                "POD works well when the singular values:",
                (
                    opt("decay fast, so few modes capture most energy", correct=True),
                    opt("are all equal"),
                    opt("grow without bound"),
                    opt("are all zero"),
                ),
                "Fast decay means a handful of modes hold almost all the energy.",
            ),
            q(
                "Projecting the governing equations onto the POD basis yields:",
                (
                    opt("a small reduced-order model that runs much faster", correct=True),
                    opt("the full-order system unchanged"),
                    opt("a larger system than before"),
                    opt("a neural network"),
                ),
                "Galerkin projection gives a tiny ODE system (the ROM).",
            ),
        ),
        "Physics-informed neural networks": (
            q(
                "A PINN enforces the governing physics by:",
                (
                    opt("adding the PDE residual to the training loss", correct=True),
                    opt("ignoring the PDE entirely"),
                    opt("using only labelled data"),
                    opt("solving the equations symbolically"),
                ),
                "PINNs minimise data, boundary, and PDE-residual terms together.",
            ),
            q(
                "How does a PINN obtain the derivatives needed for the PDE residual?",
                (
                    opt("by automatic differentiation of the network", correct=True),
                    opt("by finite differences on a fixed grid only"),
                    opt("by symbolic algebra by hand"),
                    opt("they are supplied as labels"),
                ),
                "Autodiff gives exact derivatives of the network output.",
            ),
            q(
                "A practical strength of PINNs is that they can:",
                (
                    opt(
                        "solve forward and inverse problems with little or no labelled data",
                        correct=True,
                    ),
                    opt("only work on regular rectangular grids"),
                    opt("never use boundary conditions"),
                    opt("avoid any optimisation"),
                ),
                "PINNs handle irregular domains and inverse problems with sparse data.",
            ),
        ),
        "Neural operators and solution maps": (
            q(
                "A neural operator differs from a PINN because it learns:",
                (
                    opt(
                        "a mapping between function spaces that generalises across instances",
                        correct=True,
                    ),
                    opt("a single solution for one problem only"),
                    opt("the mesh connectivity"),
                    opt("the learning rate schedule"),
                ),
                "Neural operators learn an operator, so a trained model handles many instances.",
            ),
            q(
                "The Fourier Neural Operator performs its global convolution in:",
                (
                    opt("the spectral (frequency) domain via the FFT", correct=True),
                    opt("the physical domain only"),
                    opt("the parameter space"),
                    opt("the loss function"),
                ),
                "FNO applies a linear transform on truncated Fourier modes.",
            ),
            q(
                "A trained neural operator evaluates a new case:",
                (
                    opt("far faster than running the full solver", correct=True),
                    opt("slower than the solver"),
                    opt("only after retraining from scratch"),
                    opt("with no input function"),
                ),
                "Inference is a single fast forward pass.",
            ),
        ),
        "Bayesian optimization for design": (
            q(
                "Bayesian optimization is most useful when each evaluation is:",
                (
                    opt("expensive, so a small evaluation budget is essential", correct=True),
                    opt("free and instant"),
                    opt("perfectly noiseless and known"),
                    opt("irrelevant to the objective"),
                ),
                "BO targets costly objectives where brute force is infeasible.",
            ),
            q(
                "The acquisition function in BO balances:",
                (
                    opt(
                        "exploration of uncertain regions and exploitation of good predictions",
                        correct=True,
                    ),
                    opt("training and test losses"),
                    opt("bias and the learning rate"),
                    opt("FFT modes and channels"),
                ),
                "Acquisition (e.g. Expected Improvement) trades exploration vs exploitation.",
            ),
            q(
                "BO typically finds a near-optimal design in:",
                (
                    opt("tens of evaluations rather than thousands", correct=True),
                    opt("millions of random trials"),
                    opt("exactly one evaluation"),
                    opt("no evaluations at all"),
                ),
                "BO is sample-efficient compared with grid or random search.",
            ),
        ),
        "ML-accelerated solvers and hybrid models": (
            q(
                "A learned turbulence closure model replaces:",
                (
                    opt("expensive or uncertain sub-grid terms in the solver", correct=True),
                    opt("the entire mesh generator"),
                    opt("the boundary conditions"),
                    opt("the post-processor only"),
                ),
                "ML closures stand in for sub-grid stress terms in RANS/LES.",
            ),
            q(
                "Multi-fidelity modelling fuses:",
                (
                    opt("many cheap low-fidelity runs with a few high-fidelity ones", correct=True),
                    opt("only high-fidelity runs"),
                    opt("only random noise"),
                    opt("test labels and training labels"),
                ),
                "Multi-fidelity corrects cheap models using sparse expensive data.",
            ),
            q(
                "When deploying a hybrid ML-solver, you should always:",
                (
                    opt(
                        "validate against held-out high-fidelity data and respect conservation laws",
                        correct=True,
                    ),
                    opt("trust ML speed over physical correctness"),
                    opt("skip validation to save time"),
                    opt("discard all numerical solvers"),
                ),
                "Speed must never cost physical correctness; validate and respect physics.",
            ),
        ),
    },
    final=(
        q(
            "Proper orthogonal decomposition extracts an optimal basis by:",
            (
                opt("taking the SVD of solution snapshots", correct=True),
                opt("training a PINN"),
                opt("running Bayesian optimization"),
                opt("inverting the mass matrix"),
            ),
            "POD = SVD of snapshots, ordered by energy.",
        ),
        q(
            "A physics-informed neural network embeds physics by:",
            (
                opt(
                    "penalising the PDE residual in the loss using autodiff derivatives",
                    correct=True,
                ),
                opt("ignoring the PDE"),
                opt("using a fixed grid solver only"),
                opt("requiring full labelled fields everywhere"),
            ),
            "PINNs add the autodiff PDE residual to the loss.",
        ),
        q(
            "A neural operator (e.g. FNO) is valuable because it:",
            (
                opt(
                    "learns a solution map that generalises across many PDE instances", correct=True
                ),
                opt("solves only a single fixed problem"),
                opt("requires no training data"),
                opt("replaces the loss function"),
            ),
            "Operators generalise across instances in one forward pass.",
        ),
        q(
            "Bayesian optimization is sample-efficient because it:",
            (
                opt(
                    "uses a surrogate and acquisition function to pick informative points",
                    correct=True,
                ),
                opt("evaluates every point on a dense grid"),
                opt("ignores past evaluations"),
                opt("never models uncertainty"),
            ),
            "BO guides search with a GP surrogate and acquisition function.",
        ),
        q(
            "Multi-fidelity modelling reduces cost by:",
            (
                opt(
                    "correcting cheap low-fidelity runs with a few high-fidelity ones", correct=True
                ),
                opt("using only high-fidelity runs"),
                opt("discarding all data"),
                opt("removing the surrogate"),
            ),
            "It fuses cheap and expensive models for accuracy at lower cost.",
        ),
        q(
            "The non-negotiable rule for hybrid ML-accelerated solvers is:",
            (
                opt(
                    "validate against high-fidelity data and respect conservation laws",
                    correct=True,
                ),
                opt("favour speed over physical correctness"),
                opt("never validate the model"),
                opt("remove all physics from the pipeline"),
            ),
            "ML speed must not compromise physical correctness.",
        ),
    ),
)
