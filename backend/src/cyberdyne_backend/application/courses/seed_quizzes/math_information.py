from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Information & entropy": (
            q(
                "According to Shannon, what is the information content of an outcome with probability p?",
                (
                    opt("log2 p bits"),
                    opt("-log2 p bits", correct=True),
                    opt("p log2 p bits"),
                    opt("1 - p bits"),
                ),
                "The information content of an outcome is I = -log2 p bits, so rarer events carry more information.",
            ),
            q(
                "How much information does an event of probability 1 carry?",
                (
                    opt("0 bits", correct=True),
                    opt("1 bit"),
                    opt("Infinite bits"),
                    opt("Exactly 2 bits"),
                ),
                "A certain event (probability 1) is no surprise, so it carries 0 bits of information.",
            ),
            q(
                "When is entropy H(X) maximised?",
                (
                    opt("When one outcome is certain"),
                    opt("When every outcome is equally likely", correct=True),
                    opt("When there are exactly two outcomes"),
                    opt("When the source is fully predictable"),
                ),
                "Entropy is maximised when every outcome is equally likely, which is the most uncertain case.",
            ),
        ),
        "Coding & compression": (
            q(
                "What does Shannon's source coding theorem say about the average code length?",
                (
                    opt(
                        "It can get arbitrarily close to the entropy H but never below it",
                        correct=True,
                    ),
                    opt("It can always be driven below the entropy H"),
                    opt("It must equal exactly twice the entropy"),
                    opt("It is independent of the entropy of the source"),
                ),
                "The average code length can approach the entropy H arbitrarily closely but never drop below it.",
            ),
            q(
                "What property defines a prefix code?",
                (
                    opt("Every codeword has the same fixed length"),
                    opt("No codeword is a prefix of another", correct=True),
                    opt("Every codeword starts with the same bit"),
                    opt("The shortest codeword is assigned to the rarest symbol"),
                ),
                "A prefix code has no codeword that is a prefix of another, which makes it instantly decodable.",
            ),
            q(
                "How does Huffman coding build the optimal prefix code?",
                (
                    opt("By repeatedly merging the two least likely symbols", correct=True),
                    opt("By assigning all symbols a fixed-length code"),
                    opt("By splitting the most likely symbol in half"),
                    opt("By randomly shuffling codewords until decodable"),
                ),
                "Huffman coding builds the optimal prefix code by repeatedly merging the two least likely symbols.",
            ),
        ),
        "Cross-entropy & KL divergence": (
            q(
                "What does cross-entropy H(p, q) represent?",
                (
                    opt(
                        "The cost paid when predicting with a model q while the truth is p",
                        correct=True,
                    ),
                    opt("The entropy of the model q alone"),
                    opt("The information content of a single certain event"),
                    opt("The capacity of a noisy channel"),
                ),
                "Cross-entropy is the cost you pay when you compress or predict with model q while the true distribution is p.",
            ),
            q(
                "When is the KL divergence D_KL(p || q) equal to zero?",
                (
                    opt("When q is uniform"),
                    opt("Only when q equals p", correct=True),
                    opt("When p has maximum entropy"),
                    opt("When the channel is noiseless"),
                ),
                "KL divergence is always at least zero and equals zero only when the model q equals the truth p.",
            ),
            q(
                "Why do classifiers minimise cross-entropy loss?",
                (
                    opt(
                        "Because minimising H(p, q) over q is exactly minimising D_KL(p || q)",
                        correct=True,
                    ),
                    opt("Because cross-entropy is always symmetric in p and q"),
                    opt("Because it maximises the entropy of the data"),
                    opt("Because it increases the channel capacity"),
                ),
                "Minimising cross-entropy over the model q is exactly minimising the KL divergence, pulling the model toward the data distribution.",
            ),
        ),
        "Mutual information & channel capacity": (
            q(
                "What does mutual information I(X;Y) = H(X) - H(X|Y) measure?",
                (
                    opt("How much observing Y reduces uncertainty about X", correct=True),
                    opt("The total entropy of the combined source X and Y"),
                    opt("The redundancy removed by Huffman coding"),
                    opt("The average code length of a prefix code"),
                ),
                "Mutual information measures how much observing Y reduces your uncertainty about X.",
            ),
            q(
                "In a binary symmetric channel, what happens to each bit?",
                (
                    opt("It flips with probability p", correct=True),
                    opt("It is always inverted"),
                    opt("It is duplicated exactly once"),
                    opt("It is dropped with probability p"),
                ),
                "In a binary symmetric channel each bit flips with probability p.",
            ),
            q(
                "What is the capacity of a binary symmetric channel with flip probability p?",
                (
                    opt("C = 1 - H(p)", correct=True),
                    opt("C = H(p)"),
                    opt("C = 1 + H(p)"),
                    opt("C = -log2 p"),
                ),
                "The capacity of a binary symmetric channel is C = 1 - H(p), zero at p = 0.5 and full at p = 0 or p = 1.",
            ),
        ),
        "Lab: entropy, KL divergence & cross-entropy": (
            q(
                "For the source probs [0.5, 0.25, 0.125, 0.125], what entropy does the lab report?",
                (
                    opt("1.75 bits", correct=True),
                    opt("2.0 bits"),
                    opt("1.0 bit"),
                    opt("4.0 bits"),
                ),
                "The lab states this dyadic source has entropy H(p) = 1.75 bits.",
            ),
            q(
                "Against a uniform model q = 1/4 each, what cross-entropy H(p, q) does the lab use?",
                (
                    opt("2 bits, since log2(1/4) = -2", correct=True),
                    opt("1.75 bits, equal to the entropy"),
                    opt("0 bits, since q is uniform"),
                    opt("4 bits, one per symbol"),
                ),
                "With a uniform model log2(1/4) = -2 exactly, so the cross-entropy H(p, q) is 2 bits.",
            ),
            q(
                "According to the lab, what happens to KL if you make probs uniform [0.25, 0.25, 0.25, 0.25]?",
                (
                    opt("H hits its max of 2 bits and KL goes to 0", correct=True),
                    opt("H drops to 0 and KL grows without bound"),
                    opt("Both H and KL become negative"),
                    opt("KL stays at 0.25 bits"),
                ),
                "Making the source uniform matches the model, so H reaches its maximum of 2 bits and KL goes to 0.",
            ),
        ),
    },
    final=(
        q(
            "What is the information content of an outcome with probability p?",
            (
                opt("-log2 p bits", correct=True),
                opt("log2 p bits"),
                opt("p log2 p bits"),
                opt("1 - p bits"),
            ),
            "Information content is I = -log2 p bits, capturing the surprise of an outcome.",
        ),
        q(
            "What is the hard limit on lossless compression of a source?",
            (
                opt("Its entropy H", correct=True),
                opt("Its cross-entropy with a uniform model"),
                opt("Its channel capacity"),
                opt("Its mutual information with the receiver"),
            ),
            "Entropy is the floor on lossless compression; average code length can approach H but never go below it.",
        ),
        q(
            "How is cross-entropy related to entropy and KL divergence?",
            (
                opt("H(p, q) = H(p) + D_KL(p || q)", correct=True),
                opt("H(p, q) = H(p) - D_KL(p || q)"),
                opt("H(p, q) = D_KL(p || q) - H(p)"),
                opt("H(p, q) = H(p) times D_KL(p || q)"),
            ),
            "Cross-entropy equals the entropy plus the KL divergence, so the extra cost over H(p) is exactly D_KL(p || q).",
        ),
        q(
            "What is the capacity of a binary symmetric channel with bit-flip probability p?",
            (
                opt("C = 1 - H(p)", correct=True),
                opt("C = H(p)"),
                opt("C = -log2 p"),
                opt("C = 1 + H(p)"),
            ),
            "The binary symmetric channel has capacity C = 1 - H(p), which is zero at p = 0.5.",
        ),
        q(
            "Why do classifiers minimise cross-entropy loss?",
            (
                opt(
                    "It is equivalent to minimising the KL divergence between the model and the data",
                    correct=True,
                ),
                opt("It maximises the entropy of the predictions"),
                opt("It increases the redundancy of the code"),
                opt("It raises the channel capacity toward 1"),
            ),
            "Minimising cross-entropy over the model is exactly minimising D_KL(p || q), pulling the model toward the data distribution.",
        ),
    ),
)
