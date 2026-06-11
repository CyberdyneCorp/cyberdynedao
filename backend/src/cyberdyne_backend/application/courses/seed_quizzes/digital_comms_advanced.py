from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Linear block and cyclic codes": (
            q(
                "For a linear block code, how many errors can it correct in terms of its minimum Hamming distance d_min?",
                (
                    opt("d_min errors"),
                    opt("floor((d_min - 1) / 2) errors", correct=True),
                    opt("d_min - 1 errors"),
                    opt("2 * d_min errors"),
                ),
                "A code can detect d_min - 1 errors and correct floor((d_min - 1) / 2) errors.",
            ),
            q(
                "What is the minimum Hamming distance of the Hamming(7,4) code?",
                (
                    opt("2"),
                    opt("3", correct=True),
                    opt("4"),
                    opt("7"),
                ),
                "Hamming(7,4) has d_min = 3, so it corrects any single-bit error in 7 bits.",
            ),
            q(
                "What does a CRC (Cyclic Redundancy Check) do with errors it finds?",
                (
                    opt("It corrects them using syndrome decoding"),
                    opt(
                        "It detects them so you retransmit, rather than correcting them",
                        correct=True,
                    ),
                    opt("It increases the code rate to compensate"),
                    opt("It converts them into erasures for FEC"),
                ),
                "CRCs guard Ethernet frames, ZIP files, and disk sectors by detecting errors; you then retransmit.",
            ),
        ),
        "Convolutional codes and the Viterbi algorithm": (
            q(
                "How does a convolutional code differ from a block code?",
                (
                    opt("It chops data into independent blocks"),
                    opt(
                        "It slides a shift register over the bit stream so each output depends on current and past inputs",
                        correct=True,
                    ),
                    opt("It only works on a single bit at a time with no memory"),
                    opt("It requires a parity-check matrix instead of an encoder"),
                ),
                "Convolutional codes are coding with memory: each output bit depends on the current and a few past input bits.",
            ),
            q(
                "How does the Viterbi algorithm find the maximum-likelihood path through the trellis?",
                (
                    opt("By brute-force checking every possible path"),
                    opt(
                        "In linear time, keeping only the single best surviving path at each state",
                        correct=True,
                    ),
                    opt("By using a parity-check matrix syndrome"),
                    opt("By interleaving two decoders that pass probabilities"),
                ),
                "Viterbi uses dynamic programming to find the maximum-likelihood path in linear time by keeping one survivor per state.",
            ),
            q(
                "Roughly how much coding gain does soft-decision decoding buy over hard-decision?",
                (
                    opt("About 2 dB", correct=True),
                    opt("About 10 dB"),
                    opt("Zero, they are equivalent"),
                    opt("About 0.5 dB"),
                ),
                "Soft-decision Viterbi uses the analog received values with Euclidean distance and buys roughly 2 dB of coding gain.",
            ),
        ),
        "Modern codes: turbo, LDPC & polar": (
            q(
                "What structural feature defines turbo codes?",
                (
                    opt("A single dense parity-check matrix"),
                    opt(
                        "Two convolutional encoders separated by an interleaver, decoded by passing soft probabilities",
                        correct=True,
                    ),
                    opt("Channel polarization into perfect and useless channels"),
                    opt("A shift register with no feedback"),
                ),
                "Turbo codes use two simple convolutional encoders separated by an interleaver, with decoders iterating soft probabilities.",
            ),
            q(
                "How are LDPC codes typically visualized and decoded?",
                (
                    opt("As a trellis decoded by Viterbi"),
                    opt(
                        "As a sparse parity-check matrix shown as a bipartite Tanner graph with belief message passing",
                        correct=True,
                    ),
                    opt("As an interleaver between two encoders"),
                    opt("As a polynomial division by a generator"),
                ),
                "LDPC uses a huge but sparse parity-check matrix visualized as a Tanner graph; decoding passes belief messages along edges.",
            ),
            q(
                "In 5G NR, which code is used for control channels?",
                (
                    opt("Turbo"),
                    opt("Polar", correct=True),
                    opt("LDPC"),
                    opt("Reed-Solomon"),
                ),
                "5G NR uses LDPC for data channels and polar for control channels; polar codes are provably capacity-achieving.",
            ),
        ),
        "OFDM": (
            q(
                "Why does OFDM use many narrow subcarriers instead of one wideband carrier?",
                (
                    opt("To increase the peak-to-average power ratio"),
                    opt(
                        "So each subcarrier is narrow enough that its own channel looks flat",
                        correct=True,
                    ),
                    opt("To avoid using the FFT in hardware"),
                    opt("To eliminate the need for any coding"),
                ),
                "Each subcarrier is so narrow that its channel looks flat, sidestepping frequency-selective fading.",
            ),
            q(
                "How are the orthogonal OFDM subcarriers generated and recovered cheaply?",
                (
                    opt("By an IFFT at the transmitter and an FFT at the receiver", correct=True),
                    opt("By matrix multiplication with a generator matrix"),
                    opt("By a shift-register polynomial division"),
                    opt("By beamforming weights across antennas"),
                ),
                "An inverse FFT at the transmitter and an FFT at the receiver compute the set of orthogonal tones.",
            ),
            q(
                "What is the main drawback (the catch) of OFDM?",
                (
                    opt("It cannot handle multipath at all"),
                    opt(
                        "A large peak-to-average power ratio (PAPR) that stresses the power amplifier",
                        correct=True,
                    ),
                    opt("It requires a back-channel for every symbol"),
                    opt("It only works with a single antenna"),
                ),
                "Summing many subcarriers occasionally lines them up, producing a large PAPR that hurts amplifier efficiency.",
            ),
        ),
        "MIMO and spatial multiplexing": (
            q(
                "What does spatial multiplexing do with multiple antennas?",
                (
                    opt("Sends the same data over independent paths for reliability"),
                    opt(
                        "Sends independent data streams from each antenna, multiplying capacity by min(Nt, Nr)",
                        correct=True,
                    ),
                    opt("Adds a cyclic prefix to each antenna"),
                    opt("Reduces the number of subcarriers needed"),
                ),
                "Spatial multiplexing sends independent streams; the receiver separates them, multiplying capacity by min(Nt, Nr).",
            ),
            q(
                "What does diversity provide in a MIMO system?",
                (
                    opt("More bits at the cost of bandwidth"),
                    opt(
                        "More reliability by sending the same data over independent fading paths",
                        correct=True,
                    ),
                    opt("Lower PAPR on the uplink"),
                    opt("A larger minimum Hamming distance"),
                ),
                "Diversity sends the same data over independent fading paths so it is unlikely all fade at once, improving reliability.",
            ),
            q(
                "What does beamforming do when the transmitter has channel knowledge?",
                (
                    opt(
                        "It weights the antennas so signals add in phase at the intended receiver and cancel elsewhere",
                        correct=True,
                    ),
                    opt("It physically rotates the antennas toward the user"),
                    opt("It removes the cyclic prefix from each subcarrier"),
                    opt("It switches the code from LDPC to polar"),
                ),
                "Beamforming weights the antennas so signals add in phase at the receiver and cancel elsewhere, a steerable beam with no moving parts.",
            ),
        ),
        "Lab: OFDM symbol & coding gain": (
            q(
                "In the lab, why must the multipath channel h be shorter than the cyclic prefix?",
                (
                    opt("So the IFFT runs faster"),
                    opt(
                        "So echoes only smear into the disposable prefix and each subcarrier sees a clean single multiply",
                        correct=True,
                    ),
                    opt("So the QPSK symbols have unit energy"),
                    opt("So the Hamming code can correct two errors"),
                ),
                "If delay spread is shorter than the CP, multipath echoes fall in the disposable prefix and equalization is one division per subcarrier.",
            ),
            q(
                "How does the lab equalize the recovered OFDM subcarriers?",
                (
                    opt("By a one-tap per-subcarrier divide Y / Hf", correct=True),
                    opt("By running the Viterbi algorithm"),
                    opt("By multiplying by the generator matrix G"),
                    opt("By averaging across all subcarriers"),
                ),
                "After the FFT, the lab divides Y by the channel frequency response Hf, a one-tap per-subcarrier equalizer.",
            ),
            q(
                "In the coding-gain experiment, why is each coded channel bit given Ec = (4/7) * Eb?",
                (
                    opt("Because the code adds extra power"),
                    opt(
                        "Because the rate-4/7 code spreads the same energy per information bit across more channel bits",
                        correct=True,
                    ),
                    opt("Because hard-decision decoding doubles the energy"),
                    opt("Because QPSK uses 4 bits per symbol"),
                ),
                "Both links get the same energy per information bit; the rate-4/7 Hamming code spreads Eb over 7 channel bits, so Ec = (4/7) Eb.",
            ),
        ),
        "Applications: 5G, Wi-Fi & satellite": (
            q(
                "Which waveform does 5G NR use on the uplink to lower PAPR?",
                (
                    opt("Plain OFDM"),
                    opt("DFT-spread OFDM", correct=True),
                    opt("Single-carrier QAM with no FFT"),
                    opt("MU-MIMO without OFDM"),
                ),
                "5G NR uses OFDM downlink and DFT-spread OFDM uplink to lower PAPR and save phone battery and amplifier headroom.",
            ),
            q(
                "What coding does DVB-S2 satellite use?",
                (
                    opt("Polar plus CRC"),
                    opt("LDPC plus BCH", correct=True),
                    opt("Turbo only"),
                    opt("Hamming(7,4)"),
                ),
                "Satellite is power-limited and bandwidth-rich: DVB-S2 uses LDPC + BCH with low-order modulation.",
            ),
            q(
                "Why does Wi-Fi lean on robust coding and retransmission rather than raw link margin?",
                (
                    opt("Because it has no FFT hardware"),
                    opt("Because it operates in unlicensed bands", correct=True),
                    opt("Because it only uses a single antenna"),
                    opt("Because it cannot use OFDM"),
                ),
                "Wi-Fi operates in unlicensed bands, so it relies on robust coding and a CRC + ARQ back-channel rather than raw link margin.",
            ),
        ),
    },
    final=(
        q(
            "Which property of a code determines both how many errors it can detect and correct?",
            (
                opt("The code rate k/n"),
                opt("The minimum Hamming distance d_min", correct=True),
                opt("The constraint length K"),
                opt("The number of subcarriers N"),
            ),
            "A code detects d_min - 1 errors and corrects floor((d_min - 1) / 2) errors.",
        ),
        q(
            "Which decoding approach is paired with which code family?",
            (
                opt("Viterbi for convolutional codes, message passing for LDPC", correct=True),
                opt("Viterbi for LDPC, syndrome decoding for convolutional codes"),
                opt("Polarization for turbo codes, interleaving for polar codes"),
                opt("FFT for Hamming codes, CRC for OFDM"),
            ),
            "Convolutional codes use Viterbi over a trellis; LDPC uses belief message passing on a Tanner graph.",
        ),
        q(
            "How does the cyclic prefix in OFDM provide ISI immunity?",
            (
                opt("It increases the minimum Hamming distance of the subcarriers"),
                opt(
                    "It copies the end of each symbol to its front so echoes smear only into the disposable prefix",
                    correct=True,
                ),
                opt("It doubles the energy of each subcarrier"),
                opt("It removes the need for an FFT at the receiver"),
            ),
            "If the delay spread is shorter than the CP, multipath echoes fall in the disposable prefix and each subcarrier sees a clean single multiply.",
        ),
        q(
            "What is the combined benefit of MIMO plus OFDM in a modern high-rate link?",
            (
                opt("It eliminates the need for any channel coding"),
                opt(
                    "The OFDM cyclic prefix turns the frequency-selective MIMO channel into many flat MIMO sub-channels solved one subcarrier at a time",
                    correct=True,
                ),
                opt("It removes PAPR entirely"),
                opt("It forces every system onto the Shannon limit exactly"),
            ),
            "MIMO + OFDM lets you solve a flat MIMO problem per subcarrier, the combination behind every modern high-rate link.",
        ),
        q(
            "Which 5G NR pairing of code and channel is correct?",
            (
                opt("LDPC for data, polar for control", correct=True),
                opt("Polar for data, LDPC for control"),
                opt("Turbo for data, Hamming for control"),
                opt("CRC for data, BCH for control"),
            ),
            "5G NR uses LDPC on the data channel and polar on the control channel.",
        ),
    ),
)
