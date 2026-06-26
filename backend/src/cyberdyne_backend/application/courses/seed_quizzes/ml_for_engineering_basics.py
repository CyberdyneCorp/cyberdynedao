"""Quiz questions for the Machine Learning for Engineering & Simulation - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What machine learning is for engineers": (
            q(
                "How does machine learning differ from a mechanistic model?",
                (
                    opt(
                        "It learns the mapping from data instead of deriving it from first principles",
                        correct=True,
                    ),
                    opt("It always uses Newton's laws explicitly"),
                    opt("It never needs any data"),
                    opt("It only works on linear systems"),
                ),
                "ML learns y = f(x) directly from data rather than from governing equations.",
            ),
            q(
                "When is ML most justified over a physics model?",
                (
                    opt(
                        "When the physics is unknown, too expensive, or noisy but data is plentiful",
                        correct=True,
                    ),
                    opt("When an exact cheap closed-form solution already exists"),
                    opt("When there is no data at all"),
                    opt("Whenever the system is perfectly understood"),
                ),
                "ML earns its place where mechanism is murky and data is available.",
            ),
            q(
                "Most engineering ML problems are framed as:",
                (
                    opt("supervised learning with inputs and known targets", correct=True),
                    opt("unsupervised clustering only"),
                    opt("problems with no inputs"),
                    opt("symbolic algebra"),
                ),
                "Typical engineering ML is supervised: known x and y are used to fit f.",
            ),
        ),
        "The supervised learning workflow": (
            q(
                "What is the cardinal rule of evaluation?",
                (
                    opt(
                        "Never report performance on data used to fit or tune the model",
                        correct=True,
                    ),
                    opt("Always report performance on the training set"),
                    opt("Use the same data for fitting and final reporting"),
                    opt("Never split the data"),
                ),
                "The held-out test set is the only honest estimate of generalisation.",
            ),
            q(
                "The mean squared error (MSE) loss for regression is:",
                (
                    opt(
                        "the average of squared differences between predictions and targets",
                        correct=True,
                    ),
                    opt("the maximum prediction value"),
                    opt("the number of parameters"),
                    opt("the sum of the inputs"),
                ),
                "MSE = (1/n) sum (y_i - yhat_i)^2.",
            ),
            q(
                "What is the validation set used for?",
                (
                    opt("Tuning model choices before final testing", correct=True),
                    opt("Computing the final reported accuracy"),
                    opt("Fitting the model parameters directly"),
                    opt("Storing the test labels"),
                ),
                "Validation tunes hyperparameters; the test set is reserved for final reporting.",
            ),
        ),
        "Linear regression on engineering data": (
            q(
                "The normal equations give the least-squares solution as:",
                (
                    opt("theta = (X^T X)^-1 X^T y", correct=True),
                    opt("theta = X y^-1"),
                    opt("theta = y / X always"),
                    opt("theta = X^T X y"),
                ),
                "Minimising squared error has the closed-form normal-equation solution.",
            ),
            q(
                "Fitting a line to the elastic region of a stress-strain test recovers:",
                (
                    opt("Young's modulus as the slope", correct=True),
                    opt("the yield strain as the intercept"),
                    opt("the density"),
                    opt("the Poisson ratio as the slope"),
                ),
                "In sigma = E epsilon, the slope of the elastic line is E.",
            ),
            q(
                "A key advantage of linear regression is that:",
                (
                    opt("each coefficient is interpretable as a sensitivity", correct=True),
                    opt("it can fit any nonlinear curve exactly"),
                    opt("it never needs data"),
                    opt("it has no parameters"),
                ),
                "Linear models are interpretable and a strong baseline.",
            ),
        ),
        "Polynomial features and nonlinearity": (
            q(
                "Polynomial regression stays solvable by least squares because:",
                (
                    opt("the model is still linear in its parameters", correct=True),
                    opt("the model has no parameters"),
                    opt("polynomials are always exact"),
                    opt("it ignores the data"),
                ),
                "Adding x^2, x^3 as features keeps the model linear in theta.",
            ),
            q(
                "What is the main risk of raising the polynomial degree too high?",
                (
                    opt("the curve wiggles through noisy points and overfits", correct=True),
                    opt("the model becomes too simple"),
                    opt("the model cannot fit any curve"),
                    opt("the data disappears"),
                ),
                "Excessive degree fits noise rather than signal.",
            ),
            q(
                "Cantilever tip deflection scales with beam length as:",
                (
                    opt("L^3", correct=True),
                    opt("L^0.5"),
                    opt("1/L"),
                    opt("L^-2"),
                ),
                "delta = F L^3 / (3 E I), so it grows with the cube of length.",
            ),
        ),
        "Overfitting, bias and variance": (
            q(
                "A model that is too simple tends to have:",
                (
                    opt("high bias and underfit", correct=True),
                    opt("high variance and overfit"),
                    opt("zero error always"),
                    opt("perfect generalisation"),
                ),
                "Too-simple models underfit (high bias).",
            ),
            q(
                "As model complexity increases, the validation error typically:",
                (
                    opt("decreases then increases (U-shaped)", correct=True),
                    opt("only ever decreases"),
                    opt("only ever increases"),
                    opt("stays exactly constant"),
                ),
                "Training error keeps falling but validation error turns back up.",
            ),
            q(
                "Which is a defence against overfitting?",
                (
                    opt("regularisation and cross-validation", correct=True),
                    opt("using the test set to fit parameters"),
                    opt("always using the highest possible complexity"),
                    opt("removing the validation set"),
                ),
                "Regularisation, cross-validation and simpler models reduce overfitting.",
            ),
        ),
        "Evaluating models: metrics and residuals": (
            q(
                "An R^2 of 1.0 means:",
                (
                    opt("the model explains all the variance (perfect fit)", correct=True),
                    opt("the model is no better than the mean"),
                    opt("the model has maximum error"),
                    opt("the residuals are all large"),
                ),
                "R^2 = 1 is a perfect fit; 0 is as good as predicting the mean.",
            ),
            q(
                "A curved or fanning residual plot usually signals:",
                (
                    opt("a missing feature or non-constant variance", correct=True),
                    opt("a perfectly specified model"),
                    opt("that R^2 must be 1.0"),
                    opt("that no more work is needed"),
                ),
                "Healthy residuals scatter randomly; patterns indicate model problems.",
            ),
            q(
                "Why prefer MAE over RMSE in some cases?",
                (
                    opt("MAE is more robust to outliers", correct=True),
                    opt("MAE always equals RMSE"),
                    opt("MAE ignores all errors"),
                    opt("MAE cannot be computed"),
                ),
                "MAE penalises large errors less, making it more robust to outliers.",
            ),
        ),
    },
    final=(
        q(
            "Machine learning is best described as:",
            (
                opt(
                    "learning a mapping from data rather than deriving it from first principles",
                    correct=True,
                ),
                opt("solving differential equations symbolically"),
                opt("a method that needs no data"),
                opt("a replacement for all physics"),
            ),
            "ML learns f(x) from data; it complements physics.",
        ),
        q(
            "The held-out test set should be used for:",
            (
                opt("the final honest estimate of generalisation only", correct=True),
                opt("fitting the parameters"),
                opt("tuning the polynomial degree"),
                opt("computing the training loss"),
            ),
            "Test data is reserved for the final report, never for fitting or tuning.",
        ),
        q(
            "Least-squares linear regression minimises:",
            (
                opt("the sum of squared residuals", correct=True),
                opt("the number of features"),
                opt("the maximum input value"),
                opt("the determinant of X"),
            ),
            "It minimises squared prediction error.",
        ),
        q(
            "Polynomial features let a linear model capture curvature while:",
            (
                opt("remaining linear in its parameters", correct=True),
                opt("becoming impossible to fit"),
                opt("removing all bias"),
                opt("eliminating overfitting automatically"),
            ),
            "Adding powers of x keeps the model linear in theta.",
        ),
        q(
            "The bias-variance trade-off says total error is minimised by:",
            (
                opt("balancing model simplicity and flexibility", correct=True),
                opt("always choosing the most complex model"),
                opt("always choosing the simplest model"),
                opt("ignoring the validation set"),
            ),
            "The sweet spot balances bias and variance.",
        ),
        q(
            "Which metric reports the fraction of variance explained?",
            (
                opt("R^2 (coefficient of determination)", correct=True),
                opt("MAE"),
                opt("the learning rate"),
                opt("the number of epochs"),
            ),
            "R^2 measures the fraction of variance the model explains.",
        ),
    ),
)
