"""Quiz questions for the Machine Learning for Life Sciences - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Imbalanced and noisy data in biology": (
            q(
                "Why is plain accuracy misleading on heavily imbalanced data?",
                (
                    opt(
                        "Always predicting the majority class can look highly accurate yet be useless",
                        correct=True,
                    ),
                    opt("Accuracy cannot be computed"),
                    opt("It always reports zero"),
                    opt("It ignores the majority class"),
                ),
                "With rare positives, a trivial classifier scores high accuracy but misses them.",
            ),
            q(
                "What does SMOTE do to address class imbalance?",
                (
                    opt(
                        "Oversamples the minority class by interpolating new examples", correct=True
                    ),
                    opt("Deletes the minority class"),
                    opt("Removes all features"),
                    opt("Shuffles the labels randomly"),
                ),
                "SMOTE synthesises minority examples between existing ones.",
            ),
            q(
                "To avoid leakage, resampling such as SMOTE must be applied where?",
                (
                    opt("Inside each cross-validation training fold", correct=True),
                    opt("On the whole dataset before splitting"),
                    opt("On the test fold only"),
                    opt("After deployment"),
                ),
                "Resampling before splitting leaks synthetic information into the test set.",
            ),
        ),
        "Deep learning for sequences and images": (
            q(
                "Convolutional neural networks are especially well suited to what data?",
                (
                    opt("Grid-like data such as images and DNA read as a sequence", correct=True),
                    opt("Only small tabular tables"),
                    opt("Only categorical labels"),
                    opt("Data with no structure"),
                ),
                "CNNs exploit local spatial/sequential structure with convolutions.",
            ),
            q(
                "Which technique halts training at the minimum validation loss?",
                (
                    opt("Early stopping", correct=True),
                    opt("Increasing the learning rate forever"),
                    opt("Removing the validation set"),
                    opt("Disabling backpropagation"),
                ),
                "Early stopping prevents the network from memorising as validation loss rises.",
            ),
            q(
                "Which is a regularisation technique for deep networks?",
                (
                    opt("Dropout", correct=True),
                    opt("Increasing parameters without limit"),
                    opt("Training on the test set"),
                    opt("Removing all hidden layers"),
                ),
                "Dropout, weight decay and augmentation reduce overfitting.",
            ),
        ),
        "Transfer learning and foundation models": (
            q(
                "What is the core idea of transfer learning?",
                (
                    opt(
                        "Reuse representations learned on large data, then fine-tune on a small task",
                        correct=True,
                    ),
                    opt("Always train from scratch"),
                    opt("Discard pretrained weights"),
                    opt("Use only unlabelled test data"),
                ),
                "Pretrained features transfer to data-scarce downstream tasks.",
            ),
            q(
                "ESM and similar protein language models are pretrained how?",
                (
                    opt("Self-supervised on large unlabelled sequence databases", correct=True),
                    opt("Fully supervised on tiny labelled sets"),
                    opt("With no data"),
                    opt("Only on image pixels"),
                ),
                "They learn from abundant unlabelled protein sequences.",
            ),
            q(
                "The main practical benefit of fine-tuning a foundation model is what?",
                (
                    opt("Reaching good accuracy with far fewer labelled examples", correct=True),
                    opt("Eliminating the need for any validation"),
                    opt("Guaranteeing no distribution shift"),
                    opt("Removing the need for a loss function"),
                ),
                "Pretrained representations give strong sample efficiency.",
            ),
        ),
        "Interpretability: SHAP, attention and saliency": (
            q(
                "SHAP values are based on what principle?",
                (
                    opt("Shapley values from cooperative game theory", correct=True),
                    opt("Random guessing"),
                    opt("Maximising the loss"),
                    opt("Deleting all features"),
                ),
                "SHAP fairly attributes a prediction across features via Shapley values.",
            ),
            q(
                "A local interpretability method explains what?",
                (
                    opt("An individual prediction", correct=True),
                    opt("Only the whole model globally"),
                    opt("The training schedule"),
                    opt("The hardware used"),
                ),
                "LIME and SHAP explain single predictions; permutation importance is global.",
            ),
            q(
                "An important caution about feature importance in biology is that it indicates what?",
                (
                    opt("Association, not proven causation", correct=True),
                    opt("Guaranteed causal mechanism"),
                    opt("Perfect calibration"),
                    opt("The true random seed"),
                ),
                "Explanations flag associations and must not be read as causal proof.",
            ),
        ),
        "Calibration and uncertainty for clinical decisions": (
            q(
                "A well-calibrated model means what?",
                (
                    opt("Predicted probabilities match observed outcome frequencies", correct=True),
                    opt("It has the highest possible AUROC"),
                    opt("It never makes any error"),
                    opt("It ignores probabilities entirely"),
                ),
                "Among cases given risk 0.8, about 80% should have the outcome.",
            ),
            q(
                "Which method recalibrates an overconfident deep network cheaply?",
                (
                    opt("Temperature scaling", correct=True),
                    opt("Increasing the number of epochs"),
                    opt("Adding more raw features"),
                    opt("Removing the validation set"),
                ),
                "Temperature scaling rescales logits to fix overconfidence.",
            ),
            q(
                "What does conformal prediction provide?",
                (
                    opt("Prediction sets/intervals with coverage guarantees", correct=True),
                    opt("Only a single point prediction"),
                    opt("A faster training loop"),
                    opt("Automatic feature scaling"),
                ),
                "Conformal methods give calibrated uncertainty and can flag abstention.",
            ),
        ),
        "Pitfalls: reproducibility, bias and validation": (
            q(
                "Which is the most common cause of irreproducible biomedical ML results?",
                (
                    opt("Data leakage", correct=True),
                    opt("Using too little compute"),
                    opt("Reporting subgroup metrics"),
                    opt("External validation"),
                ),
                "Leakage, including preprocessing before splitting, inflates accuracy.",
            ),
            q(
                "Batch effects can cause a model to learn what instead of biology?",
                (
                    opt("The scanner, site or sequencing centre", correct=True),
                    opt("The true causal pathway"),
                    opt("Perfectly calibrated probabilities"),
                    opt("Nothing at all"),
                ),
                "Splitting by batch/site and adjusting confounders mitigates this.",
            ),
            q(
                "The strongest evidence that a clinical model generalises is what?",
                (
                    opt("External validation on an independent cohort", correct=True),
                    opt("A high internal accuracy on one cohort"),
                    opt("A large number of features"),
                    opt("A complex architecture"),
                ),
                "Independent-cohort validation guards against optimistic single-cohort estimates.",
            ),
        ),
    },
    final=(
        q(
            "On imbalanced data, which approach helps the minority class?",
            (
                opt("Class-weighting the loss or resampling within CV folds", correct=True),
                opt("Maximising plain accuracy"),
                opt("Deleting the minority class"),
                opt("Ignoring the threshold"),
            ),
            "Weighting, resampling and threshold tuning address imbalance.",
        ),
        q(
            "Which prevents a deep network from overfitting as training continues?",
            (
                opt("Early stopping at minimum validation loss", correct=True),
                opt("Training forever"),
                opt("Removing regularisation"),
                opt("Using the test set to train"),
            ),
            "Early stopping (with dropout, augmentation) curbs overfitting.",
        ),
        q(
            "Foundation models such as ESM and scGPT are valuable mainly because they enable what?",
            (
                opt("High accuracy from few labels via self-supervised pretraining", correct=True),
                opt("Training without any data"),
                opt("Removal of distribution shift"),
                opt("Elimination of validation"),
            ),
            "They learn general representations transferable to small labelled tasks.",
        ),
        q(
            "SHAP and saliency maps are tools for what?",
            (
                opt("Interpretability of model predictions", correct=True),
                opt("Data augmentation"),
                opt("Hyperparameter search"),
                opt("Class balancing"),
            ),
            "They attribute predictions to features or input regions.",
        ),
        q(
            "A model with high AUROC but poor calibration is risky because what?",
            (
                opt("Its probabilities do not match real outcome frequencies", correct=True),
                opt("It cannot rank cases"),
                opt("It has no parameters"),
                opt("It always abstains"),
            ),
            "Good ranking does not guarantee trustworthy probabilities for decisions.",
        ),
        q(
            "Which pitfall most often inflates reported ML performance in biology?",
            (
                opt("Data leakage and batch confounding", correct=True),
                opt("Reporting subgroup metrics"),
                opt("Using external validation"),
                opt("Fixing the random seed"),
            ),
            "Leakage and batch effects, absent external validation, drive optimism.",
        ),
    ),
)
