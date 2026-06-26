"""Quiz questions for the Deep Learning for Biology - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why deep learning for biology": (
            q(
                "What key advantage do deep networks have over classical feature engineering?",
                (
                    opt("They learn representations directly from raw data", correct=True),
                    opt("They require no data at all"),
                    opt("They never overfit"),
                    opt("They run only on quantum computers"),
                ),
                "Deep models learn features rather than relying on hand-designed ones.",
            ),
            q(
                "Which is a landmark deep-learning result in biology?",
                (
                    opt("AlphaFold predicting protein structure", correct=True),
                    opt("The discovery of the DNA double helix"),
                    opt("The invention of the microscope"),
                    opt("Mendel's pea experiments"),
                ),
                "AlphaFold is a flagship deep-learning achievement for structure prediction.",
            ),
            q(
                "What is the main practical drawback of deep networks?",
                (
                    opt("They are data-hungry and can overfit", correct=True),
                    opt("They cannot represent non-linear functions"),
                    opt("They only work on text"),
                    opt("They require no training"),
                ),
                "Flexible models need large datasets and can memorise small ones.",
            ),
        ),
        "The artificial neuron": (
            q(
                "What does an artificial neuron compute before the activation?",
                (
                    opt("A weighted sum of inputs plus a bias", correct=True),
                    opt("The median of its inputs"),
                    opt("A random number"),
                    opt("The maximum input only"),
                ),
                "It computes z = sum(w*x) + b.",
            ),
            q(
                "Why is the non-linear activation essential?",
                (
                    opt("Without it, stacked layers collapse to a single linear map", correct=True),
                    opt("It makes training slower on purpose"),
                    opt("It removes the bias term"),
                    opt("It converts inputs to integers"),
                ),
                "Non-linearity lets the network approximate complex functions.",
            ),
            q(
                "What range does the sigmoid activation output?",
                (
                    opt("Between 0 and 1", correct=True),
                    opt("Between -1 and 0"),
                    opt("Any integer"),
                    opt("Exactly 0 or 1 only"),
                ),
                "Sigmoid squashes any real input into the open interval (0,1).",
            ),
        ),
        "Layers, depth and forward propagation": (
            q(
                "What is forward propagation?",
                (
                    opt("Computing the output by passing inputs through each layer", correct=True),
                    opt("Updating weights using gradients"),
                    opt("Deleting unused neurons"),
                    opt("Shuffling the dataset"),
                ),
                "Each layer applies a linear map plus activation in sequence.",
            ),
            q(
                "Why does depth help a network?",
                (
                    opt("It lets the network build features hierarchically", correct=True),
                    opt("It removes the need for data"),
                    opt("It guarantees zero error"),
                    opt("It eliminates all weights"),
                ),
                "Early layers detect simple patterns; later layers combine them.",
            ),
            q(
                "Why is ReLU often preferred over sigmoid in deep stacks?",
                (
                    opt("It is cheap and avoids vanishing gradients", correct=True),
                    opt("It always outputs negative values"),
                    opt("It is non-differentiable everywhere"),
                    opt("It removes the need for weights"),
                ),
                "ReLU does not saturate on its positive branch.",
            ),
        ),
        "Loss functions and what we optimise": (
            q(
                "Which loss is standard for regression tasks?",
                (
                    opt("Mean squared error", correct=True),
                    opt("Cross-entropy on one-hot labels"),
                    opt("Accuracy"),
                    opt("Edit distance"),
                ),
                "MSE penalises squared deviation from the target.",
            ),
            q(
                "What does cross-entropy penalise most heavily?",
                (
                    opt("Confident but wrong predictions", correct=True),
                    opt("Predictions exactly equal to the label"),
                    opt("Using too few layers"),
                    opt("A large learning rate"),
                ),
                "As a confident probability heads the wrong way, the loss diverges.",
            ),
            q(
                "What do we minimise during training?",
                (
                    opt("The average loss over the dataset", correct=True),
                    opt("The number of layers"),
                    opt("The learning rate"),
                    opt("The batch size"),
                ),
                "Training minimises mean loss by adjusting weights.",
            ),
        ),
        "Gradient descent and learning rate": (
            q(
                "Which direction does gradient descent step?",
                (
                    opt("Opposite to the gradient of the loss", correct=True),
                    opt("In the direction of the gradient"),
                    opt("Randomly each step"),
                    opt("Toward the largest weight"),
                ),
                "We move downhill, against the gradient.",
            ),
            q(
                "What happens if the learning rate is too large?",
                (
                    opt("Training can overshoot or diverge", correct=True),
                    opt("Training always converges instantly"),
                    opt("The bias is removed"),
                    opt("The data is duplicated"),
                ),
                "Too-large steps overshoot the minimum.",
            ),
            q(
                "Why use mini-batch stochastic gradient descent?",
                (
                    opt("It is faster and its noise can escape poor minima", correct=True),
                    opt("It uses the entire dataset every step"),
                    opt("It never needs a learning rate"),
                    opt("It avoids computing any gradients"),
                ),
                "Mini-batches estimate the gradient cheaply with helpful noise.",
            ),
        ),
        "Backpropagation and overfitting": (
            q(
                "What rule does backpropagation rely on?",
                (
                    opt("The chain rule of calculus", correct=True),
                    opt("Bayes' theorem"),
                    opt("The pigeonhole principle"),
                    opt("Ohm's law"),
                ),
                "It propagates error gradients using the chain rule.",
            ),
            q(
                "What is the signature of overfitting?",
                (
                    opt("Low training loss but high validation loss", correct=True),
                    opt("High training and validation loss equally"),
                    opt("Zero loss on new data"),
                    opt("A constant output regardless of input"),
                ),
                "A gap opens between training and validation error.",
            ),
            q(
                "Which technique fights overfitting?",
                (
                    opt("Dropout", correct=True),
                    opt("Increasing the learning rate to infinity"),
                    opt("Removing the validation set"),
                    opt("Training forever"),
                ),
                "Dropout, early stopping and weight decay all regularise.",
            ),
        ),
    },
    final=(
        q(
            "What does the activation function provide to a neural network?",
            (
                opt("Non-linearity, enabling complex function approximation", correct=True),
                opt("A guarantee of zero training error"),
                opt("Removal of all weights"),
                opt("Faster data loading"),
            ),
            "Without non-linearity the network is just a linear map.",
        ),
        q(
            "Which loss suits binary classification of variants?",
            (
                opt("Binary cross-entropy", correct=True),
                opt("Mean squared error on raw counts"),
                opt("Hamming distance"),
                opt("Manhattan distance"),
            ),
            "Cross-entropy is standard for classification.",
        ),
        q(
            "The learning rate eta controls what?",
            (
                opt("The size of each weight-update step", correct=True),
                opt("The number of neurons"),
                opt("The dataset size"),
                opt("The number of classes"),
            ),
            "It scales the gradient step.",
        ),
        q(
            "Backpropagation is efficient because it:",
            (
                opt("Reuses forward-pass results via the chain rule", correct=True),
                opt("Perturbs each weight independently"),
                opt("Avoids computing any derivatives"),
                opt("Uses only random updates"),
            ),
            "Its cost is comparable to a single forward pass.",
        ),
        q(
            "Which curve indicates when to apply early stopping?",
            (
                opt("Validation error reaching its minimum then rising", correct=True),
                opt("Training error increasing from the start"),
                opt("A flat constant loss"),
                opt("The learning rate over time"),
            ),
            "Stop at the validation-error minimum.",
        ),
        q(
            "Why is deep learning well-suited to modern biology?",
            (
                opt("Large, complex datasets with non-linear structure", correct=True),
                opt("Biology has only tiny tabular datasets"),
                opt("Biological problems are all perfectly linear"),
                opt("There is no data in biology"),
            ),
            "Deep models thrive on large, complex biological data.",
        ),
    ),
)
