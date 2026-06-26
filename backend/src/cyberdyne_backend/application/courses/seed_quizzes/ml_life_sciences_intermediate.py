"""Quiz questions for the Machine Learning for Life Sciences - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Cross-validation for small biological datasets": (
            q(
                "In k-fold cross-validation, how is each example used?",
                (
                    opt("It is tested exactly once across the rotation of folds", correct=True),
                    opt("It is never tested"),
                    opt("It is tested in every fold"),
                    opt("It is only used for scaling"),
                ),
                "Each fold serves as the held-out test once while the rest train.",
            ),
            q(
                "Where must preprocessing such as scaling be fit in cross-validation?",
                (
                    opt("Inside each training fold only", correct=True),
                    opt("On the full dataset before splitting"),
                    opt("On the test folds only"),
                    opt("It does not matter"),
                ),
                "Fitting on the full data leaks test information into training.",
            ),
            q(
                "Why is stratified cross-validation used for imbalanced classes?",
                (
                    opt("It preserves class proportions in each fold", correct=True),
                    opt("It removes the minority class"),
                    opt("It doubles the dataset"),
                    opt("It eliminates the need for a test set"),
                ),
                "Stratification keeps each fold representative of the class balance.",
            ),
        ),
        "Regularisation: ridge, lasso and elastic net": (
            q(
                "Which regularisation can drive some coefficients exactly to zero?",
                (
                    opt("Lasso (L1)", correct=True),
                    opt("Ridge (L2)"),
                    opt("No penalty"),
                    opt("Standardisation"),
                ),
                "The L1 penalty yields sparse solutions, selecting features.",
            ),
            q(
                "Ridge regression (L2) handles correlated features by doing what?",
                (
                    opt(
                        "Shrinking all weights smoothly without forcing them to zero", correct=True
                    ),
                    opt("Deleting all but one feature"),
                    opt("Increasing weights without limit"),
                    opt("Ignoring the loss term"),
                ),
                "L2 shrinks coefficients gradually and spreads weight across correlates.",
            ),
            q(
                "As the regularisation strength lambda increases, coefficient magnitudes do what?",
                (
                    opt("Shrink toward zero", correct=True),
                    opt("Grow without bound"),
                    opt("Stay exactly constant"),
                    opt("Become negative infinity"),
                ),
                "Stronger penalties push weights toward zero (the regularisation path).",
            ),
        ),
        "Classification metrics and ROC/PR curves": (
            q(
                "Sensitivity (recall) is defined as which ratio?",
                (
                    opt("TP / (TP + FN)", correct=True),
                    opt("TN / (TN + FP)"),
                    opt("TP / (TP + FP)"),
                    opt("FP / (FP + TN)"),
                ),
                "Recall is the fraction of true positives correctly identified.",
            ),
            q(
                "An AUROC of 0.5 indicates what?",
                (
                    opt("Performance no better than random", correct=True),
                    opt("A perfect classifier"),
                    opt("Perfect calibration"),
                    opt("Zero false positives"),
                ),
                "0.5 is chance; 1.0 is perfect ranking.",
            ),
            q(
                "For very rare positives, which curve is more informative than ROC?",
                (
                    opt("Precision-recall (PR) curve", correct=True),
                    opt("ROC curve"),
                    opt("Scree plot"),
                    opt("Dendrogram"),
                ),
                "PR focuses on positives and is not flattered by abundant true negatives.",
            ),
        ),
        "Tree ensembles: random forests and gradient boosting": (
            q(
                "How does a random forest reduce error compared with a single tree?",
                (
                    opt("By averaging many decorrelated trees, lowering variance", correct=True),
                    opt("By adding trees sequentially to fit residuals"),
                    opt("By using a single very deep tree"),
                    opt("By removing all randomness"),
                ),
                "Bagging and random feature subsets decorrelate trees and cut variance.",
            ),
            q(
                "Gradient boosting builds its trees in what manner?",
                (
                    opt("Sequentially, each fitting the current residual errors", correct=True),
                    opt("All in parallel on bootstrap samples"),
                    opt("Randomly with no objective"),
                    opt("As a single linear model"),
                ),
                "Boosting adds trees that correct the ensemble's mistakes, reducing bias.",
            ),
            q(
                "Feature importance from tree ensembles indicates what?",
                (
                    opt("Association, not proven causation", correct=True),
                    opt("Definitive causal effects"),
                    opt("The true biological mechanism"),
                    opt("Nothing useful at all"),
                ),
                "Importance flags predictive features but does not prove causality.",
            ),
        ),
        "Unsupervised structure: PCA and clustering": (
            q(
                "Principal component analysis finds directions that do what?",
                (
                    opt("Capture maximal variance in the data", correct=True),
                    opt("Maximise the number of features"),
                    opt("Require labels to compute"),
                    opt("Minimise the variance"),
                ),
                "PCs are orthogonal axes of greatest variance.",
            ),
            q(
                "Why should clustering be done on the data rather than a UMAP/t-SNE embedding?",
                (
                    opt("Non-linear embeddings distort global distances", correct=True),
                    opt("Embeddings have more samples"),
                    opt("Embeddings are always labelled"),
                    opt("Clustering cannot use numbers"),
                ),
                "UMAP/t-SNE are for visualisation and warp distances.",
            ),
            q(
                "A scree plot of cumulative variance explained typically shows what?",
                (
                    opt("First components capture most variance, then it saturates", correct=True),
                    opt("Variance increasing without bound"),
                    opt("All components equally important"),
                    opt("Variance decreasing to negative values"),
                ),
                "Most signal concentrates in the leading components.",
            ),
        ),
        "Feature selection without leakage": (
            q(
                "Lasso and tree importance are which kind of feature selection?",
                (
                    opt("Embedded (selection happens during fitting)", correct=True),
                    opt("Filter (univariate ranking)"),
                    opt("Wrapper (subset search)"),
                    opt("No selection"),
                ),
                "Embedded methods select features as part of model training.",
            ),
            q(
                "Selection leakage occurs when features are chosen how?",
                (
                    opt("Using the whole dataset before cross-validation", correct=True),
                    opt("Inside each training fold only"),
                    opt("On an independent dataset"),
                    opt("After the model is deployed"),
                ),
                "Choosing features on all data, including test, inflates performance.",
            ),
            q(
                "As more features are screened, the best chance correlation tends to do what?",
                (
                    opt("Rise, making false discovery likely without correction", correct=True),
                    opt("Fall toward zero"),
                    opt("Stay exactly constant"),
                    opt("Become impossible to occur"),
                ),
                "More comparisons raise the maximum spurious correlation expected.",
            ),
        ),
    },
    final=(
        q(
            "What is the main advantage of k-fold cross-validation over a single split?",
            (
                opt(
                    "It uses scarce data efficiently and gives a more stable estimate", correct=True
                ),
                opt("It guarantees zero error"),
                opt("It removes the need for a model"),
                opt("It always uses 50% for testing"),
            ),
            "Rotating folds tests every example and averages the scores.",
        ),
        q(
            "Which method performs automatic feature selection via sparsity?",
            (
                opt("Lasso (L1)", correct=True),
                opt("Ridge (L2)"),
                opt("k-means"),
                opt("PCA"),
            ),
            "L1 drives some coefficients exactly to zero.",
        ),
        q(
            "For imbalanced classification, which metric is most appropriate?",
            (
                opt("Area under the precision-recall curve (AUPRC)", correct=True),
                opt("Plain accuracy"),
                opt("Number of features"),
                opt("Training loss only"),
            ),
            "PR-based metrics reflect performance on rare positives.",
        ),
        q(
            "Random forests primarily reduce which source of error?",
            (
                opt("Variance, via averaging decorrelated trees", correct=True),
                opt("Bias, via sequential residual fitting"),
                opt("Irreducible noise"),
                opt("Label leakage"),
            ),
            "Bagging lowers variance; boosting targets bias.",
        ),
        q(
            "PCA is best described as which kind of technique?",
            (
                opt("Unsupervised dimensionality reduction", correct=True),
                opt("Supervised classification"),
                opt("A regularisation penalty"),
                opt("A resampling method"),
            ),
            "PCA compresses features by variance without using labels.",
        ),
        q(
            "To avoid leakage, feature selection in a CV workflow must be placed where?",
            (
                opt("Inside each training fold", correct=True),
                opt("Once on the full dataset beforehand"),
                opt("On the held-out test fold"),
                opt("After reporting the final score"),
            ),
            "Re-selecting features per training fold keeps the estimate honest.",
        ),
    ),
)
