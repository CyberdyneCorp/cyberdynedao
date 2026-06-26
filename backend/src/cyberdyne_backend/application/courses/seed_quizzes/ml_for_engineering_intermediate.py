"""Quiz questions for the Machine Learning for Engineering & Simulation - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Regularisation: ridge and lasso": (
            q(
                "What does the L1 (lasso) penalty do that L2 (ridge) does not?",
                (
                    opt(
                        "drives some coefficients to exactly zero, selecting features", correct=True
                    ),
                    opt("always increases all coefficients"),
                    opt("removes the need for data"),
                    opt("makes the model nonlinear"),
                ),
                "Lasso performs feature selection by zeroing coefficients; ridge only shrinks them.",
            ),
            q(
                "Ridge regression adds a penalty proportional to:",
                (
                    opt("the squared L2 norm of the coefficients", correct=True),
                    opt("the number of samples"),
                    opt("the maximum target value"),
                    opt("the determinant of the data matrix"),
                ),
                "Ridge adds lambda * ||theta||_2^2 to the squared-error loss.",
            ),
            q(
                "The regularisation strength lambda should be chosen by:",
                (
                    opt("cross-validation", correct=True),
                    opt("picking the largest possible value"),
                    opt("eyeballing the training fit"),
                    opt("setting it to zero always"),
                ),
                "Lambda trades fit against simplicity and is tuned by cross-validation.",
            ),
        ),
        "Feature engineering and PCA": (
            q(
                "Why standardise features before fitting?",
                (
                    opt("so no feature dominates merely because of its scale", correct=True),
                    opt("to remove all the data"),
                    opt("to make the model nonlinear"),
                    opt("to increase the number of samples"),
                ),
                "Standardisation puts features on comparable scales.",
            ),
            q(
                "Principal component analysis finds:",
                (
                    opt("an orthogonal basis ordered by variance", correct=True),
                    opt("the labels for unsupervised data"),
                    opt("the loss function"),
                    opt("the learning rate"),
                ),
                "PCA gives orthogonal components ranked by explained variance.",
            ),
            q(
                "PCA is mathematically equivalent to:",
                (
                    opt("the singular value decomposition of the centred data", correct=True),
                    opt("gradient descent"),
                    opt("a random projection"),
                    opt("the normal equations"),
                ),
                "PCA is the SVD of the centred data matrix.",
            ),
        ),
        "Gaussian process surrogates": (
            q(
                "A key advantage of a Gaussian process surrogate is that it returns:",
                (
                    opt("a predictive variance (uncertainty) alongside the mean", correct=True),
                    opt("only a point prediction with no uncertainty"),
                    opt("exact PDE solutions"),
                    opt("the training labels unchanged"),
                ),
                "GPs give both a mean and an uncertainty, valuable for trusting a surrogate.",
            ),
            q(
                "GP predictive uncertainty is largest:",
                (
                    opt("far from the training samples", correct=True),
                    opt("exactly at the training points"),
                    opt("everywhere equally"),
                    opt("only at the origin"),
                ),
                "Uncertainty grows away from observed data.",
            ),
            q(
                "Gaussian processes are especially well suited to:",
                (
                    opt("small, expensive datasets", correct=True),
                    opt("billions of cheap samples"),
                    opt("problems with no inputs"),
                    opt("purely symbolic algebra"),
                ),
                "GPs excel with small data and underpin Bayesian optimization.",
            ),
        ),
        "Neural networks and gradient descent": (
            q(
                "Backpropagation is used to:",
                (
                    opt(
                        "compute the gradient of the loss with respect to the parameters",
                        correct=True,
                    ),
                    opt("randomly reset the weights"),
                    opt("remove the activation functions"),
                    opt("increase the learning rate automatically"),
                ),
                "Backprop computes gradients used by gradient descent.",
            ),
            q(
                "If the learning rate is far too large, training tends to:",
                (
                    opt("diverge or oscillate", correct=True),
                    opt("converge instantly to the optimum"),
                    opt("ignore the loss"),
                    opt("remove all parameters"),
                ),
                "Too-large steps cause divergence; too-small steps crawl.",
            ),
            q(
                "The universal approximation idea says a neural network can:",
                (
                    opt("approximate arbitrarily complex continuous functions", correct=True),
                    opt("only fit straight lines"),
                    opt("never overfit"),
                    opt("solve any problem with no data"),
                ),
                "With enough capacity, networks approximate complex functions.",
            ),
        ),
        "Surrogate models for simulation": (
            q(
                "A surrogate model replaces an expensive simulator by:",
                (
                    opt("learning its input-output map from a modest set of runs", correct=True),
                    opt("ignoring the simulator entirely"),
                    opt("solving the full PDE faster by hand"),
                    opt("using no training data"),
                ),
                "Surrogates learn the simulator's map, then evaluate in milliseconds.",
            ),
            q(
                "Latin hypercube sampling is used to:",
                (
                    opt("spread design-space samples well for the experiment", correct=True),
                    opt("compute the loss function"),
                    opt("invert the stiffness matrix"),
                    opt("label the test set"),
                ),
                "LHS provides a space-filling design of experiments.",
            ),
            q(
                "As more simulation samples are added, surrogate accuracy typically:",
                (
                    opt("improves with diminishing returns", correct=True),
                    opt("gets monotonically worse"),
                    opt("stays exactly constant"),
                    opt("becomes random"),
                ),
                "Error falls roughly like 1/n with diminishing returns.",
            ),
        ),
    },
    final=(
        q(
            "Lasso regression is preferred over ridge when you want to:",
            (
                opt("perform automatic feature selection", correct=True),
                opt("keep every coefficient nonzero"),
                opt("avoid using any penalty"),
                opt("make the model nonlinear"),
            ),
            "L1 drives some coefficients to zero, selecting features.",
        ),
        q(
            "PCA reduces dimensionality by keeping components that:",
            (
                opt("capture the most variance", correct=True),
                opt("have the smallest singular values"),
                opt("are chosen at random"),
                opt("equal the labels"),
            ),
            "Keep top components covering most variance (e.g. 95%).",
        ),
        q(
            "Compared with a plain neural network, a Gaussian process additionally provides:",
            (
                opt("calibrated uncertainty estimates", correct=True),
                opt("a smaller training set"),
                opt("exact physics"),
                opt("a fixed learning rate"),
            ),
            "GPs return predictive variance, not just a point estimate.",
        ),
        q(
            "Parameters of a neural network are updated using:",
            (
                opt("gradient descent with gradients from backpropagation", correct=True),
                opt("random guessing only"),
                opt("the normal equations directly"),
                opt("no optimisation at all"),
            ),
            "Backprop supplies gradients; an optimiser like Adam steps downhill.",
        ),
        q(
            "The main motivation for a surrogate model is that:",
            (
                opt("the original simulation is too expensive to query many times", correct=True),
                opt("the simulation is already instant"),
                opt("there is no input data"),
                opt("physics is never needed"),
            ),
            "Surrogates enable optimization and UQ that full runs make infeasible.",
        ),
        q(
            "A space-filling design of experiments such as Latin hypercube sampling helps:",
            (
                opt("cover the design space efficiently with few runs", correct=True),
                opt("eliminate the need for a surrogate"),
                opt("compute R^2 directly"),
                opt("invert the covariance kernel"),
            ),
            "Good sampling makes the surrogate accurate with fewer expensive runs.",
        ),
    ),
)
