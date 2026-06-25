"""Curated quiz questions for the Information Theory & Coding - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Information, entropy & the bit": (
            q(
                "How is the information content of an outcome with probability p defined?",
                (
                    opt("p log2 p"),
                    opt("log2(1/p) bits", correct=True),
                    opt("1 minus p"),
                    opt("p times the number of outcomes"),
                ),
                "Information is log2(1/p): rarer outcomes (smaller p) carry more bits of surprise.",
            ),
            q(
                "Where does the binary entropy function H(p) reach its maximum, and what is that value?",
                (
                    opt("At p = 0, with value 1 bit"),
                    opt("At p = 0.5, with value 1 bit", correct=True),
                    opt("At p = 1, with value 0 bits"),
                    opt("At p = 0.5, with value 0.5 bits"),
                ),
                "H(p) peaks at p = 0.5 (maximum uncertainty) where it equals exactly 1 bit, and is 0 at p = 0 or 1.",
            ),
            q(
                "What does the entropy of a source represent for compression?",
                (
                    opt("The maximum number of bits any code must use"),
                    opt(
                        "The lower bound (floor) on the average bits needed to describe it",
                        correct=True,
                    ),
                    opt("The number of distinct symbols in the source"),
                    opt("The probability of the most likely symbol"),
                ),
                "Entropy is the information-theoretic floor: no lossless code can use fewer bits per symbol on average.",
            ),
        ),
        "Mutual information & the noisy channel": (
            q(
                "Mutual information I(X;Y) is defined as which of the following?",
                (
                    opt("H(X) + H(Y)"),
                    opt("H(X) − H(X | Y)", correct=True),
                    opt("H(Y | X) − H(X)"),
                    opt("H(X) times H(Y)"),
                ),
                "I(X;Y) = H(X) − H(X|Y): the input entropy minus what remains uncertain after seeing the output.",
            ),
            q(
                "In a binary symmetric channel, what happens at a flip probability of p = 0.5?",
                (
                    opt("All information is preserved"),
                    opt("The mutual information is zero and the bit is destroyed", correct=True),
                    opt("The channel becomes noiseless"),
                    opt("The capacity is maximised"),
                ),
                "At p = 0.5 the output is independent of the input, so I(X;Y) = 0 and no information gets through.",
            ),
            q(
                "For a BSC, how much information (in bits) does the noise destroy per bit?",
                (
                    opt("Exactly p bits"),
                    opt("The binary entropy H(p) of the flip probability", correct=True),
                    opt("Always 1 bit"),
                    opt("Zero, since the channel is symmetric"),
                ),
                "The information lost to a BSC equals H(p), the binary entropy of its flip probability.",
            ),
        ),
        "Channel capacity & Shannon's theorem": (
            q(
                "What does Shannon's noisy-channel coding theorem guarantee?",
                (
                    opt("Any rate is achievable with enough power"),
                    opt(
                        "For any rate below capacity C, codes exist with arbitrarily small error",
                        correct=True,
                    ),
                    opt("Error-free communication is impossible on any noisy channel"),
                    opt("Capacity can always be exceeded with a good enough code"),
                ),
                "Below C, arbitrarily reliable codes exist; above C, reliable communication is impossible.",
            ),
            q(
                "In the Shannon–Hartley law C = B log2(1 + SNR), how does capacity scale with SNR?",
                (
                    opt("Linearly with SNR"),
                    opt("Logarithmically with SNR (diminishing returns)", correct=True),
                    opt("Quadratically with SNR"),
                    opt("It is independent of SNR"),
                ),
                "Capacity grows only logarithmically with SNR, so raw power gives diminishing returns.",
            ),
            q(
                "What happens if you try to transmit at a rate R greater than capacity C?",
                (
                    opt("Reliable communication becomes impossible", correct=True),
                    opt("The error rate stays arbitrarily small"),
                    opt("Capacity simply increases to match R"),
                    opt("The channel doubles its bandwidth"),
                ),
                "Shannon's theorem says no code can achieve reliable communication when R exceeds C.",
            ),
        ),
        "Source coding & data compression": (
            q(
                "What is a prefix code?",
                (
                    opt("A code where every codeword has the same length"),
                    opt("A code where no codeword is the beginning of another", correct=True),
                    opt("A code that prefixes each symbol with a parity bit"),
                    opt("A code that only works for the first symbol"),
                ),
                "In a prefix code no codeword is a prefix of another, so the stream decodes instantly without separators.",
            ),
            q(
                "How does Huffman coding assign codeword lengths?",
                (
                    opt("Short codewords to rare symbols, long to frequent"),
                    opt("Short codewords to frequent symbols, long to rare", correct=True),
                    opt("Equal length to every symbol"),
                    opt("Lengths chosen at random"),
                ),
                "Huffman gives short codewords to frequent symbols and long ones to rare symbols, minimising average length.",
            ),
            q(
                "How does source coding relate to error-correction coding?",
                (
                    opt("Both add redundancy to the data"),
                    opt(
                        "Source coding strips redundancy; error coding adds controlled redundancy back",
                        correct=True,
                    ),
                    opt("They are two names for the same operation"),
                    opt("Error coding always runs before source coding"),
                ),
                "Compression removes redundancy; error correction adds structured redundancy back — opposite goals, applied in that order.",
            ),
        ),
        "The need for error control": (
            q(
                "What is the key difference between error detection and error correction?",
                (
                    opt("Detection fixes errors; correction only notices them"),
                    opt(
                        "Detection only notices errors; correction reconstructs the original",
                        correct=True,
                    ),
                    opt("They are identical in cost and capability"),
                    opt("Detection needs more overhead than correction"),
                ),
                "Detection only flags that something is wrong (then you retransmit); correction (FEC) rebuilds the data without asking again.",
            ),
            q(
                "What is the limitation of a single parity bit?",
                (
                    opt("It can correct any single bit error"),
                    opt(
                        "It detects a single flip but cannot locate or fix it, and misses even numbers of flips",
                        correct=True,
                    ),
                    opt("It detects all possible error patterns"),
                    opt("It can correct bursts of errors"),
                ),
                "A single parity bit detects one flip but cannot say which bit, cannot correct, and misses an even number of flips.",
            ),
            q(
                "What does the code rate R = k/n measure?",
                (
                    opt("The number of errors a code can correct"),
                    opt(
                        "The fraction of transmitted bits that carry the actual message",
                        correct=True,
                    ),
                    opt("The probability of a bit flip"),
                    opt("The channel's bandwidth"),
                ),
                "R = k/n is the ratio of message bits k to transmitted bits n — the efficiency price of the redundancy.",
            ),
        ),
        "Hamming distance & block codes": (
            q(
                "What is the Hamming distance between two binary words?",
                (
                    opt("The number of 1s in their sum"),
                    opt("The number of positions at which they differ", correct=True),
                    opt("The length of the shorter word"),
                    opt("The number of codewords between them"),
                ),
                "Hamming distance counts the positions where two equal-length words differ.",
            ),
            q(
                "How many errors can a code with minimum distance d_min correct?",
                (
                    opt("d_min errors"),
                    opt("floor((d_min − 1) / 2) errors", correct=True),
                    opt("d_min − 1 errors"),
                    opt("2 times d_min errors"),
                ),
                "A code corrects up to floor((d_min − 1)/2) errors and detects up to d_min − 1.",
            ),
            q(
                "What is the minimum distance of a 3-times repetition code, and how many errors does it correct?",
                (
                    opt("d_min = 2, corrects 0 errors"),
                    opt("d_min = 3, corrects 1 error", correct=True),
                    opt("d_min = 1, corrects 1 error"),
                    opt("d_min = 3, corrects 2 errors"),
                ),
                "Repetition-3 has d_min = 3, so it corrects 1 error by majority vote — at the cost of rate 1/3.",
            ),
        ),
    },
    final=(
        q(
            "Why does the binary entropy function equal zero at p = 0 and p = 1?",
            (
                opt("Because the bit is maximally uncertain there"),
                opt(
                    "Because the outcome is certain, so there is no surprise/information",
                    correct=True,
                ),
                opt("Because log2 of 1 equals 1"),
                opt("Because entropy is always zero for a single bit"),
            ),
            "At p = 0 or p = 1 the outcome is certain, carrying no information, so H(p) = 0.",
        ),
        q(
            "Which statement best captures the central tension of information theory?",
            (
                opt("Maximise both power and bandwidth simultaneously"),
                opt(
                    "Pack information tightly (compression) yet survive noise (error correction)",
                    correct=True,
                ),
                opt("Always use the longest possible codewords"),
                opt("Avoid adding any redundancy under all conditions"),
            ),
            "The subject balances stripping redundancy for compression against adding it for noise resilience.",
        ),
        q(
            "What is channel capacity C?",
            (
                opt("The number of bits in a single codeword"),
                opt("The maximum mutual information over all input distributions", correct=True),
                opt("The flip probability of the channel"),
                opt("The minimum distance of the best code"),
            ),
            "Capacity is the largest mutual information any input distribution can achieve — the ceiling on reliable bits.",
        ),
        q(
            "A code carries 4 message bits in 7 transmitted bits with d_min = 3. What can it do?",
            (
                opt("Correct 2 errors at rate 7/4"),
                opt("Correct 1 error at rate 4/7", correct=True),
                opt("Only detect errors, never correct"),
                opt("Correct 3 errors at rate 1/3"),
            ),
            "Rate is k/n = 4/7, and d_min = 3 means it corrects floor((3−1)/2) = 1 error.",
        ),
        q(
            "Why does increasing transmit power give diminishing returns on capacity?",
            (
                opt("Because capacity falls as SNR rises"),
                opt("Because capacity grows only logarithmically with SNR", correct=True),
                opt("Because power has no effect on capacity"),
                opt("Because bandwidth shrinks as power grows"),
            ),
            "C = B log2(1 + SNR) grows logarithmically, so doubling SNR adds less and less capacity — coding matters, not just watts.",
        ),
        q(
            "Why does a prefix code need no separators between codewords?",
            (
                opt("Because all codewords are the same length"),
                opt(
                    "Because no codeword is a prefix of another, so each decodes unambiguously as it arrives",
                    correct=True,
                ),
                opt("Because it always uses a parity bit as a delimiter"),
                opt("Because the decoder waits for the end of the stream"),
            ),
            "The prefix-free property means the decoder always knows when a codeword ends, so no separators are required.",
        ),
    ),
)
