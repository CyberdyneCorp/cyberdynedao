"""Quiz questions for the QSAR & Pharmacophore Modeling - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Hansch and Free-Wilson analysis": (
            q(
                "The Hansch approach uses which kind of descriptors?",
                (
                    opt("continuous physicochemical descriptors", correct=True),
                    opt("only integer atom counts"),
                    opt("additive substituent indicator variables"),
                    opt("3D field grids"),
                ),
                "Hansch is the linear free-energy approach using logP, sigma, Es, etc.",
            ),
            q(
                "Why does the Hansch equation often include a (logP)^2 term?",
                (
                    opt(
                        "activity rises then falls with lipophilicity, giving a parabola",
                        correct=True,
                    ),
                    opt("to make the equation longer"),
                    opt("because logP is always negative"),
                    opt("to remove all electronic effects"),
                ),
                "The optimum logP* = a/2b reflects the parabolic membrane-penetration trade-off.",
            ),
            q(
                "A limitation of the Free-Wilson approach is that it:",
                (
                    opt("cannot predict substituents it has never seen", correct=True),
                    opt("requires quantum calculations"),
                    opt("ignores the scaffold entirely"),
                    opt("only works for proteins"),
                ),
                "Free-Wilson sums learned substituent constants, so novel substituents have no value.",
            ),
        ),
        "Collinearity and PLS regression": (
            q(
                "What problem arises when descriptors are collinear and p > n?",
                (
                    opt("ordinary least squares becomes unstable or undefined", correct=True),
                    opt("the assay fails"),
                    opt("the molecules become insoluble"),
                    opt("R^2 is always zero"),
                ),
                "(X^T X) is ill-conditioned or singular, so OLS coefficients are unreliable.",
            ),
            q(
                "What does PLS regression do?",
                (
                    opt(
                        "extracts latent components that maximize covariance with activity",
                        correct=True,
                    ),
                    opt("deletes all descriptors"),
                    opt("randomizes the activities"),
                    opt("fits a separate model per molecule"),
                ),
                "PLS regresses on a few orthogonal components, sidestepping collinearity and p>n.",
            ),
            q(
                "How is the number of PLS components typically chosen?",
                (
                    opt("by maximizing cross-validated q^2", correct=True),
                    opt("always exactly equal to the number of compounds"),
                    opt("by minimizing molecular weight"),
                    opt("by using all available components"),
                ),
                "Too few underfit, too many refit noise; q^2 peaks at the right count.",
            ),
        ),
        "Regularization and feature selection": (
            q(
                "Which penalty drives coefficients exactly to zero, performing feature selection?",
                (
                    opt("L1 (lasso)", correct=True),
                    opt("L2 (ridge)"),
                    opt("no penalty"),
                    opt("L0 only"),
                ),
                "Lasso's L1 penalty zeroes out coefficients; ridge's L2 only shrinks them.",
            ),
            q(
                "As the regularization strength lambda increases, the model gains:",
                (
                    opt("more bias but often better generalization up to a point", correct=True),
                    opt("zero bias and zero variance"),
                    opt("infinite variance"),
                    opt("guaranteed perfect prediction"),
                ),
                "Lambda controls the bias-variance trade-off; tune it by cross-validation.",
            ),
            q(
                "A common rule of thumb for a parsimonious QSAR model is:",
                (
                    opt("at least about 5 compounds per descriptor", correct=True),
                    opt("at least 5 descriptors per compound"),
                    opt("exactly one descriptor total"),
                    opt("more descriptors than compounds is ideal"),
                ),
                "Keeping the compounds-to-descriptors ratio high guards against overfitting.",
            ),
        ),
        "Nonlinear and machine-learning QSAR": (
            q(
                "Random forests build predictions by:",
                (
                    opt(
                        "averaging many decision trees on bootstrap samples and random feature subsets",
                        correct=True,
                    ),
                    opt("fitting a single straight line"),
                    opt("taking the median molecular weight"),
                    opt("using one deep tree only"),
                ),
                "Bagging plus feature randomness makes them robust and good at interactions.",
            ),
            q(
                "A graph neural network for QSAR primarily:",
                (
                    opt("learns descriptors directly from the molecular graph", correct=True),
                    opt("requires no data at all"),
                    opt("ignores bonds and atoms"),
                    opt("only works on 1D spectra"),
                ),
                "GNNs do message passing over atoms and bonds to learn task-specific features.",
            ),
            q(
                "What is the main risk of very flexible nonlinear models?",
                (
                    opt("they can fit noise (overfit) if data are limited", correct=True),
                    opt("they cannot fit any pattern"),
                    opt("they always underfit"),
                    opt("they require no validation"),
                ),
                "Flexibility must be matched to dataset size via the bias-variance trade-off.",
            ),
        ),
        "Internal validation and cross-validation": (
            q(
                "What does k-fold cross-validation estimate?",
                (
                    opt("predictive performance using only the training data", correct=True),
                    opt("the synthesis yield"),
                    opt("the assay pH"),
                    opt("the patent expiry date"),
                ),
                "It rotates held-out folds to estimate generalization internally.",
            ),
            q(
                "A model is generally considered acceptable when its q^2 is:",
                (
                    opt("greater than about 0.5", correct=True),
                    opt("less than 0"),
                    opt("exactly equal to R^2 always"),
                    opt("greater than 2.0"),
                ),
                "q^2 > 0.5 is the common threshold; a large R^2 minus q^2 gap signals overfitting.",
            ),
            q(
                "What does y-randomization (Y-scrambling) check?",
                (
                    opt("that the model is not a chance correlation", correct=True),
                    opt("the solubility of the compounds"),
                    opt("the number of descriptors"),
                    opt("the assay temperature"),
                ),
                "Permuting activities should ruin the model; if not, the original fit was luck.",
            ),
        ),
        "External validation and statistics": (
            q(
                "The gold standard for assessing a QSAR's predictivity is:",
                (
                    opt("external validation on a held-out test set", correct=True),
                    opt("a high training R^2"),
                    opt("counting descriptors"),
                    opt("the molecular weight range"),
                ),
                "The test set must never touch training, selection or tuning.",
            ),
            q(
                "Tropsha's criteria require external R^2 to exceed roughly:",
                (
                    opt("0.6", correct=True),
                    opt("0.1"),
                    opt("2.0"),
                    opt("-0.5"),
                ),
                "Common thresholds: q^2 > 0.5 and external R^2 > 0.6 with slope near 1.",
            ),
            q(
                "RMSE reports prediction error in:",
                (
                    opt("the original activity units (e.g. pIC50)", correct=True),
                    opt("percent of descriptors used"),
                    opt("degrees Celsius"),
                    opt("arbitrary units only"),
                ),
                "RMSE is the root mean square error in the response's own units.",
            ),
        ),
    },
    final=(
        q(
            "The Free-Wilson approach models activity as:",
            (
                opt("an additive sum of substituent contributions", correct=True),
                opt("a parabola in logP"),
                opt("a 3D field grid"),
                opt("a random forest"),
            ),
            "Each substituent at each position adds a fixed increment to a base scaffold.",
        ),
        q(
            "PLS regression is especially useful when:",
            (
                opt("descriptors are collinear and outnumber compounds", correct=True),
                opt("there is only one descriptor"),
                opt("activities are unknown"),
                opt("the data are perfectly orthogonal already"),
            ),
            "PLS latent components handle collinearity and p>n.",
        ),
        q(
            "Lasso differs from ridge regression because lasso:",
            (
                opt("can set coefficients exactly to zero (feature selection)", correct=True),
                opt("never changes coefficients"),
                opt("uses an L2 penalty"),
                opt("increases all coefficients"),
            ),
            "L1 yields sparse models; L2 only shrinks.",
        ),
        q(
            "Which model learns its own descriptors from the bonded structure?",
            (
                opt("a graph neural network", correct=True),
                opt("multiple linear regression"),
                opt("Free-Wilson analysis"),
                opt("ridge regression"),
            ),
            "GNNs do message passing over the molecular graph.",
        ),
        q(
            "A large gap between R^2 and q^2 indicates:",
            (
                opt("overfitting", correct=True),
                opt("a perfectly predictive model"),
                opt("low molecular weight"),
                opt("a successful external validation"),
            ),
            "Fit far exceeding cross-validated prediction is a red flag.",
        ),
        q(
            "External validation requires the test set to be:",
            (
                opt("untouched during training, feature selection and tuning", correct=True),
                opt("the same as the training set"),
                opt("used to pick hyperparameters"),
                opt("larger than the entire dataset"),
            ),
            "Only a truly unseen test set gives an honest predictivity estimate.",
        ),
    ),
)
