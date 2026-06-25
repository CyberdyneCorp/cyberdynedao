"""Curated quiz questions for the Information Theory & Coding - Advanced course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Convolutional codes & the trellis": (
            q(
                "How does a convolutional code differ from a block code?",
                (
                    opt("It has no redundancy"),
                    opt(
                        "It has memory: each output depends on the current and recent past inputs",
                        correct=True,
                    ),
                    opt("It works only on whole files at once"),
                    opt("It can only detect, never correct"),
                ),
                "A convolutional encoder is a finite-state machine with memory, so outputs depend on recent inputs.",
            ),
            q(
                "What does the constraint length K of a convolutional code measure?",
                (
                    opt("The number of parity bits per block"),
                    opt("How many input bits influence each output", correct=True),
                    opt("The total length of the message"),
                    opt("The code's minimum distance"),
                ),
                "Constraint length K is how many input bits affect each encoder output.",
            ),
            q(
                "What does a path through the trellis represent?",
                (
                    opt("A single bit error"),
                    opt("A possible codeword (sequence of states/outputs)", correct=True),
                    opt("The parity-check matrix"),
                    opt("A syndrome value"),
                ),
                "Every codeword corresponds to a path through the trellis; decoding seeks the best-matching path.",
            ),
        ),
        "Viterbi decoding": (
            q(
                "What does the Viterbi algorithm find?",
                (
                    opt("A random valid codeword"),
                    opt(
                        "The single most likely path through the trellis (the ML codeword)",
                        correct=True,
                    ),
                    opt("Every possible codeword exhaustively"),
                    opt("The shortest codeword"),
                ),
                "Viterbi is dynamic programming that finds the maximum-likelihood path without enumerating all of them.",
            ),
            q(
                "How does Viterbi avoid exponential work?",
                (
                    opt("It ignores most of the received symbols"),
                    opt(
                        "At each state it keeps only the best surviving path (add–compare–select)",
                        correct=True,
                    ),
                    opt("It tries paths at random until one fits"),
                    opt("It decodes only the first bit"),
                ),
                "By keeping just the best survivor per state at each step, the work stays linear in message length.",
            ),
            q(
                "Roughly how much coding gain does soft-decision Viterbi buy over hard decision?",
                (
                    opt("About 2 dB", correct=True),
                    opt("About 20 dB"),
                    opt("None at all"),
                    opt("It is always worse than hard decision"),
                ),
                "Feeding the decoder analog confidence (soft decision) is worth roughly 2 dB of coding gain.",
            ),
        ),
        "Turbo codes & iterative decoding": (
            q(
                "What was remarkable about turbo codes when introduced in 1993?",
                (
                    opt("They needed no redundancy"),
                    opt("They got within a fraction of a dB of the Shannon limit", correct=True),
                    opt("They could not be decoded in practice"),
                    opt("They worked only at very high SNR"),
                ),
                "Turbo codes closed most of the long-standing gap to the Shannon limit.",
            ),
            q(
                "How do the two decoders in a turbo decoder cooperate?",
                (
                    opt("They vote and take the majority"),
                    opt(
                        "They exchange soft extrinsic information iteratively, each refining the other's prior",
                        correct=True,
                    ),
                    opt("Only one decoder is ever used"),
                    opt("They run independently and never communicate"),
                ),
                "Each soft-in/soft-out decoder passes extrinsic LLRs to the other and they iterate until they agree.",
            ),
            q(
                "What is the 'turbo cliff'?",
                (
                    opt("A region where the code stops working entirely"),
                    opt(
                        "A steep drop in BER near a threshold SNR, followed by a gentler error floor",
                        correct=True,
                    ),
                    opt("The point where the code rate becomes 1"),
                    opt("A hardware failure mode"),
                ),
                "The BER falls sharply near a threshold SNR (the cliff), then flattens into an error floor.",
            ),
        ),
        "LDPC codes & belief propagation": (
            q(
                "What makes a parity-check matrix 'low-density'?",
                (
                    opt("It has very few rows"),
                    opt("It is sparse — only a few 1s per row/column", correct=True),
                    opt("It contains only zeros"),
                    opt("It is square"),
                ),
                "LDPC codes have a sparse H, which is what makes iterative decoding cheap and effective.",
            ),
            q(
                "What is a Tanner graph?",
                (
                    opt("A plot of BER versus SNR"),
                    opt(
                        "A bipartite graph of variable nodes and check nodes linked where H has a 1",
                        correct=True,
                    ),
                    opt("The trellis of a convolutional code"),
                    opt("A Huffman tree"),
                ),
                "The Tanner graph links variable nodes (code bits) to check nodes (parity equations) per the 1s of H.",
            ),
            q(
                "How does belief propagation decode an LDPC code?",
                (
                    opt("By inverting the parity-check matrix"),
                    opt(
                        "Variable and check nodes exchange soft messages (LLRs) along edges and iterate",
                        correct=True,
                    ),
                    opt("By trying every codeword in turn"),
                    opt("By a single matrix multiplication"),
                ),
                "The sum–product algorithm passes soft messages between nodes, converging via local updates.",
            ),
        ),
        "Polar codes & the capacity frontier": (
            q(
                "What is unique about polar codes?",
                (
                    opt(
                        "They are the first codes proven to achieve capacity with low complexity",
                        correct=True,
                    ),
                    opt("They cannot be decoded"),
                    opt("They only work at zero rate"),
                    opt("They require no encoder"),
                ),
                "Polar codes (Arıkan, 2009) are provably capacity-achieving with low-complexity encode/decode.",
            ),
            q(
                "What is channel polarisation?",
                (
                    opt("Aligning antenna polarisation"),
                    opt(
                        "Synthesised sub-channels split into nearly perfect and nearly useless ones",
                        correct=True,
                    ),
                    opt("Inverting the sign of every bit"),
                    opt("Doubling the transmit power"),
                ),
                "Combining channels recursively makes sub-channels polarise toward capacity 1 or capacity 0.",
            ),
            q(
                "Where does a polar encoder place the data bits?",
                (
                    opt("On the useless sub-channels"),
                    opt(
                        "On the good (near-noiseless) sub-channels, freezing the bad ones",
                        correct=True,
                    ),
                    opt("Randomly across all sub-channels"),
                    opt("Only on the parity sub-channels"),
                ),
                "Data goes on the good sub-channels; the bad ones are fixed to known frozen bits.",
            ),
        ),
        "Coding in practice": (
            q(
                "What is code concatenation?",
                (
                    opt("Using a single code twice in a row"),
                    opt(
                        "An inner code cleans the raw channel and an outer code mops up residual errors",
                        correct=True,
                    ),
                    opt("Joining two messages into one"),
                    opt("Removing all parity bits"),
                ),
                "Concatenation pairs an inner code (e.g. convolutional/LDPC) with an outer code (often RS) for residual cleanup.",
            ),
            q(
                "Why is soft-decision decoding preferred over hard decision?",
                (
                    opt("It is simpler to implement"),
                    opt(
                        "It keeps the analog confidence (LLR), worth roughly 2 dB of gain",
                        correct=True,
                    ),
                    opt("It uses fewer bits on the wire"),
                    opt("It removes the need for any code"),
                ),
                "Soft decision keeps the channel's confidence rather than quantising early, buying about 2 dB.",
            ),
            q(
                "Which codes does 5G NR use for data versus control channels?",
                (
                    opt("RS for data, Hamming for control"),
                    opt("LDPC for data, polar for control", correct=True),
                    opt("Polar for data, turbo for control"),
                    opt("Repetition codes for both"),
                ),
                "5G NR uses LDPC on the data channel and polar codes on the control channel.",
            ),
        ),
    },
    final=(
        q(
            "Both Viterbi and belief propagation share which underlying idea?",
            (
                opt("Inverting a large matrix"),
                opt(
                    "Efficient inference on a graph/trellis rather than brute-force enumeration",
                    correct=True,
                ),
                opt("Ignoring the channel's soft information"),
                opt("Adding redundancy after transmission"),
            ),
            "Viterbi (trellis DP) and BP (message passing on a Tanner graph) both avoid exhaustive search via graph inference.",
        ),
        q(
            "What do turbo, LDPC and polar codes have in common?",
            (
                opt("They are all block codes with d_min = 1"),
                opt(
                    "They approach or achieve channel capacity, unlike classical codes",
                    correct=True,
                ),
                opt("They cannot use soft information"),
                opt("They are only used for compression"),
            ),
            "All three are capacity-approaching (polar provably capacity-achieving), closing the gap classical codes left open.",
        ),
        q(
            "Why does interleaving appear inside turbo codes as well as in burst-error handling?",
            (
                opt("It compresses the data"),
                opt(
                    "It decorrelates information — separating parity streams in turbo, and spreading bursts elsewhere",
                    correct=True,
                ),
                opt("It increases the code rate to 1"),
                opt("It replaces the need for any decoder"),
            ),
            "The interleaver decorrelates: in turbo codes it makes the two parity streams independent; against bursts it scatters errors.",
        ),
        q(
            "In a concatenated system, what role does the outer Reed–Solomon code typically play?",
            (
                opt("It does the initial soft demodulation"),
                opt(
                    "It cleans up the residual errors that the inner decoder lets through",
                    correct=True,
                ),
                opt("It compresses the source"),
                opt("It generates the carrier signal"),
            ),
            "The inner code handles the raw channel; the outer RS code corrects the residual (often bursty) errors that remain.",
        ),
        q(
            "What does channel polarisation guarantee as the block length grows?",
            (
                opt("Every sub-channel becomes identical"),
                opt(
                    "The fraction of good sub-channels converges to the channel capacity C",
                    correct=True,
                ),
                opt("The code rate must drop to zero"),
                opt("All sub-channels become useless"),
            ),
            "As N grows, the fraction of near-perfect sub-channels approaches C, so data on them transmits reliably below capacity.",
        ),
        q(
            "Across the decades, what is the recurring story of channel coding?",
            (
                opt("Codes have gotten steadily worse"),
                opt(
                    "Successively closing the gap to the Shannon limit, from Hamming/RS to turbo to LDPC/polar",
                    correct=True,
                ),
                opt("Abandoning redundancy entirely"),
                opt("Replacing capacity with raw transmit power"),
            ),
            "The field's arc is progressively narrowing the gap to capacity: Hamming/RS, then turbo, then LDPC and polar.",
        ),
    ),
)
