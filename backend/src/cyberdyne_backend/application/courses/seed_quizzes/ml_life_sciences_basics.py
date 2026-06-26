"""Quiz questions for the Machine Learning for Life Sciences - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What machine learning is and why biology needs it": (
            q(
                "What distinguishes machine learning from traditional programming?",
                (
                    opt(
                        "Models learn patterns from data instead of using hand-coded rules",
                        correct=True,
                    ),
                    opt("It never makes mistakes"),
                    opt("It requires no data at all"),
                    opt("It only works on text"),
                ),
                "ML fits a model to data by minimising a loss, rather than following explicit rules.",
            ),
            q(
                "Why does modern biology increasingly need machine learning?",
                (
                    opt(
                        "Assays produce high-dimensional data with patterns no human can hand-code",
                        correct=True,
                    ),
                    opt("Biologists no longer run experiments"),
                    opt("Computers replaced all laboratories"),
                    opt("Data has become smaller and simpler"),
                ),
                "Omics, imaging and sequencing generate data too complex for manual rules.",
            ),
            q(
                "During training, the model parameters are updated to do what?",
                (
                    opt("Minimise a loss measuring prediction error", correct=True),
                    opt("Maximise the loss"),
                    opt("Keep the loss constant"),
                    opt("Ignore the training data"),
                ),
                "Learning iteratively reduces the loss between predictions and truth.",
            ),
        ),
        "Examples, features and labels": (
            q(
                "In a design matrix X of shape n x p, what are the columns?",
                (
                    opt("Features describing each example", correct=True),
                    opt("Examples such as patients"),
                    opt("Loss values"),
                    opt("Model parameters"),
                ),
                "Rows are examples; columns are features.",
            ),
            q(
                "Standardising a feature to zero mean and unit variance prevents what?",
                (
                    opt("One large-magnitude feature from dominating others", correct=True),
                    opt("The model from ever training"),
                    opt("Labels from existing"),
                    opt("Examples from being rows"),
                ),
                "Scaling (z = (x - mu)/sigma) puts features on comparable scales.",
            ),
            q(
                "The 'large p, small n' regime in biology means what?",
                (
                    opt("Far more features than samples, raising overfitting risk", correct=True),
                    opt("Far more samples than features"),
                    opt("No features at all"),
                    opt("Equal features and samples always"),
                ),
                "Thousands of genes with few samples makes fitting noise easy.",
            ),
        ),
        "Types of learning: supervised, unsupervised, reinforcement": (
            q(
                "Which learning type uses labelled examples to predict an output?",
                (
                    opt("Supervised learning", correct=True),
                    opt("Unsupervised learning"),
                    opt("Reinforcement learning"),
                    opt("No learning"),
                ),
                "Supervised learning maps X to a known label y.",
            ),
            q(
                "Clustering single cells into groups without labels is an example of what?",
                (
                    opt("Unsupervised learning", correct=True),
                    opt("Supervised classification"),
                    opt("Supervised regression"),
                    opt("Reinforcement learning"),
                ),
                "Clustering finds structure in unlabelled data.",
            ),
            q(
                "Predicting a continuous biomarker value is which supervised task?",
                (
                    opt("Regression", correct=True),
                    opt("Classification"),
                    opt("Clustering"),
                    opt("Dimensionality reduction"),
                ),
                "Regression predicts a number; classification predicts a category.",
            ),
        ),
        "Overfitting and the bias-variance trade-off": (
            q(
                "An overfit model behaves how?",
                (
                    opt("Fits training data well but generalises poorly to new data", correct=True),
                    opt("Fits both training and new data poorly"),
                    opt("Fits new data better than training data"),
                    opt("Ignores the training data"),
                ),
                "Overfitting means memorising training noise and failing to generalise.",
            ),
            q(
                "High bias is associated with which problem?",
                (
                    opt("Underfitting from an over-simple model", correct=True),
                    opt("Overfitting from an over-complex model"),
                    opt("Perfect generalisation"),
                    opt("Zero training error"),
                ),
                "Bias is error from a model too simple to capture the signal.",
            ),
            q(
                "As model complexity increases, expected test error typically does what?",
                (
                    opt("Falls then rises (U-shaped)", correct=True),
                    opt("Always falls"),
                    opt("Always rises"),
                    opt("Stays constant"),
                ),
                "Bias falls and variance grows, giving a U-shaped test error.",
            ),
        ),
        "Splitting data: train, validation and test": (
            q(
                "What is the validation set used for?",
                (
                    opt("Tuning hyperparameters", correct=True),
                    opt("Fitting model parameters"),
                    opt("Reporting the final unbiased score"),
                    opt("Generating new raw data"),
                ),
                "Validation tunes choices like regularisation; the test set is touched once.",
            ),
            q(
                "Putting replicates of the same patient in both train and test causes what?",
                (
                    opt("Data leakage that inflates apparent accuracy", correct=True),
                    opt("More honest evaluation"),
                    opt("Smaller datasets"),
                    opt("Better calibration"),
                ),
                "Leakage lets the model see test information, overstating performance.",
            ),
            q(
                "The test set should be used how often?",
                (
                    opt("Once, for the final unbiased estimate", correct=True),
                    opt("Repeatedly to tune the model"),
                    opt("To fit parameters"),
                    opt("Never at all"),
                ),
                "Reusing the test set to tune choices reintroduces optimism.",
            ),
        ),
        "First models: linear, logistic and k-NN": (
            q(
                "Despite its name, logistic regression is used for what?",
                (
                    opt("Classification (predicting a probability/class)", correct=True),
                    opt("Only predicting continuous numbers"),
                    opt("Clustering"),
                    opt("Dimensionality reduction"),
                ),
                "It squashes a linear score through a sigmoid to give a probability.",
            ),
            q(
                "How does k-nearest neighbours make a prediction?",
                (
                    opt("By majority vote of the k closest training examples", correct=True),
                    opt("By fitting a weighted sum of features"),
                    opt("By applying a sigmoid"),
                    opt("By building a decision tree"),
                ),
                "k-NN relies on a distance and the labels of nearby points.",
            ),
            q(
                "The sigmoid function maps a real score to what range?",
                (
                    opt("Between 0 and 1", correct=True),
                    opt("Between -1 and 1"),
                    opt("Any real number"),
                    opt("Only integers"),
                ),
                "p = 1/(1+e^-z) lies in (0,1), interpretable as a probability.",
            ),
        ),
    },
    final=(
        q(
            "Machine learning models are best described as functions that do what?",
            (
                opt("Learn patterns from data by minimising a loss", correct=True),
                opt("Follow only hand-written rules"),
                opt("Require no data"),
                opt("Never change after creation"),
            ),
            "A model f_theta is fitted to data by reducing a loss.",
        ),
        q(
            "In a design matrix, rows and columns correspond to what?",
            (
                opt("Rows are examples; columns are features", correct=True),
                opt("Rows are features; columns are labels"),
                opt("Rows are losses; columns are examples"),
                opt("Rows and columns are both labels"),
            ),
            "Each example (row) is described by features (columns).",
        ),
        q(
            "Which is an unsupervised learning task?",
            (
                opt("Clustering cells with no labels", correct=True),
                opt("Predicting disease from labelled data"),
                opt("Regression on a labelled biomarker"),
                opt("Classifying tumours with known labels"),
            ),
            "Unsupervised methods find structure without labels.",
        ),
        q(
            "Overfitting in the 'large p, small n' biological regime is mainly driven by which term?",
            (
                opt("High variance", correct=True),
                opt("High bias"),
                opt("Zero irreducible noise"),
                opt("Low complexity"),
            ),
            "Many features and few samples make variance dominate.",
        ),
        q(
            "Why must data be split before preprocessing like scaling?",
            (
                opt("To avoid leaking test information into training", correct=True),
                opt("To make the model train faster"),
                opt("Because scaling is optional"),
                opt("To increase the number of samples"),
            ),
            "Fitting scalers on the whole dataset leaks test statistics.",
        ),
        q(
            "Which model outputs a calibrated probability via a sigmoid?",
            (
                opt("Logistic regression", correct=True),
                opt("Linear regression"),
                opt("k-NN"),
                opt("k-means"),
            ),
            "Logistic regression squashes a linear score into (0,1).",
        ),
    ),
)
