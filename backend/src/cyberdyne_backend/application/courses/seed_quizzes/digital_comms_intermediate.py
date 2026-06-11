from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "M-ary and quadrature modulation": (
            q(
                "How many bits per symbol does an M-ary scheme carry?",
                (
                    opt("M bits per symbol"),
                    opt("log2(M) bits per symbol", correct=True),
                    opt("sqrt(M) bits per symbol"),
                    opt("M/2 bits per symbol"),
                ),
                "An M-ary scheme carries log2(M) bits per symbol, so 16-QAM carries 4 bits.",
            ),
            q(
                "What does Gray coding achieve in the bit-to-symbol mapping?",
                (
                    opt("It packs more points into the constellation"),
                    opt("It makes adjacent symbols differ in exactly one bit", correct=True),
                    opt("It spreads points evenly around a circle"),
                    opt("It increases the bits per symbol"),
                ),
                "Gray coding assigns bit patterns so adjacent symbols differ in one bit, "
                "so the most likely error flips only one bit.",
            ),
            q(
                "How does QAM differ from M-PSK in arranging constellation points?",
                (
                    opt("QAM uses a grid varying both amplitude and phase", correct=True),
                    opt("QAM spreads points evenly around a circle"),
                    opt("QAM varies only the phase"),
                    opt("QAM varies only the amplitude"),
                ),
                "QAM uses a grid of points varying both amplitude and phase, while M-PSK "
                "spreads points evenly around a circle.",
            ),
        ),
        "Performance over channels": (
            q(
                "What is the bandwidth efficiency eta of an M-ary scheme (before pulse shaping)?",
                (
                    opt("eta = M bits/s/Hz"),
                    opt("eta = log2(M) bits/s/Hz", correct=True),
                    opt("eta = sqrt(M) bits/s/Hz"),
                    opt("eta = M/2 bits/s/Hz"),
                ),
                "Bandwidth efficiency is eta = log2(M) bits/s/Hz before pulse-shaping overhead.",
            ),
            q(
                "Why do denser constellations need more Eb/N0 to hit the same BER?",
                (
                    opt("Their points sit closer together", correct=True),
                    opt("They carry fewer bits per symbol"),
                    opt("They use more bandwidth"),
                    opt("They have no waterfall curve"),
                ),
                "Higher-order QAM points sit closer together, so they need more Eb/N0 to "
                "reach the same BER.",
            ),
            q(
                "Which strategy fits a power-limited regime such as deep space or IoT?",
                (
                    opt("High-order QAM"),
                    opt("Low-order modulation plus heavy coding", correct=True),
                    opt("Maximize bits/s/Hz with dense modulation"),
                    opt("256-QAM with no coding"),
                ),
                "Power-limited links (Voyager, LoRa, NB-IoT) use low-order modulation plus "
                "heavy coding.",
            ),
        ),
        "Information theory": (
            q(
                "What does the entropy H(X) of a source represent?",
                (
                    opt("The maximum channel rate"),
                    opt("The average information per symbol, in bits", correct=True),
                    opt("The signal-to-noise ratio"),
                    opt("The bandwidth in Hz"),
                ),
                "Entropy H(X) = -sum p_i log2 p_i is the average information per symbol in bits.",
            ),
            q(
                "What is the Shannon capacity of an AWGN channel of bandwidth B and ratio S/N?",
                (
                    opt("C = B log2(1 + S/N)", correct=True),
                    opt("C = B (S/N)"),
                    opt("C = log2(B + S/N)"),
                    opt("C = B + log2(S/N)"),
                ),
                "The Shannon capacity bound is C = B log2(1 + S/N) bits/s, the maximum "
                "error-free rate.",
            ),
            q(
                "How does Shannon capacity grow with bandwidth versus power?",
                (
                    opt("Linearly with bandwidth, logarithmically with power", correct=True),
                    opt("Logarithmically with bandwidth, linearly with power"),
                    opt("Linearly with both"),
                    opt("Logarithmically with both"),
                ),
                "Capacity grows linearly with bandwidth but only logarithmically with power.",
            ),
        ),
        "Source coding": (
            q(
                "What is the prefix property required for variable-length codes?",
                (
                    opt("Every codeword has the same length"),
                    opt("No codeword is a prefix of another", correct=True),
                    opt("All codewords start with the same bit"),
                    opt("Codewords are separated by markers"),
                ),
                "The prefix property means no codeword is a prefix of another, so a stream "
                "decodes unambiguously without separators.",
            ),
            q(
                "How does Huffman's algorithm build the optimal prefix code?",
                (
                    opt("By dividing the message by a generator polynomial"),
                    opt(
                        "By repeatedly merging the two least-likely symbols into a tree",
                        correct=True,
                    ),
                    opt("By replacing repeats with back-references"),
                    opt("By counting runs of repeated symbols"),
                ),
                "Huffman repeatedly merges the two least-likely symbols into a binary tree "
                "to build the optimal prefix code.",
            ),
            q(
                "Which compression method replaces repeats with back-references?",
                (
                    opt("Huffman coding"),
                    opt("Arithmetic / range coding"),
                    opt("LZ77 / LZ78", correct=True),
                    opt("Run-length encoding"),
                ),
                "LZ77 / LZ78 replace repeats with back-references and are used in gzip, "
                "PNG, and ZIP.",
            ),
        ),
        "Channel impairments": (
            q(
                "What causes fading on a real wireless link?",
                (
                    opt(
                        "Many paths add with different delays and phases, sometimes destructively",
                        correct=True,
                    ),
                    opt("The transmitter switches off periodically"),
                    opt("The entropy of the source increases"),
                    opt("The cyclic prefix is removed"),
                ),
                "A signal reaches the receiver via many paths that add with different delays "
                "and phases, sometimes destructively, producing fading.",
            ),
            q(
                "What does an equalizer do to a frequency-selective channel?",
                (
                    opt(
                        "It estimates the channel and applies its inverse to reopen the eye",
                        correct=True,
                    ),
                    opt("It compresses the source to its entropy"),
                    opt("It spreads the signal across more bandwidth"),
                    opt("It adds parity bits for error correction"),
                ),
                "An equalizer estimates the channel and applies its inverse so the eye "
                "reopens, undoing ISI.",
            ),
            q(
                "Which synchronization type aligns the frequency and phase of the carrier?",
                (
                    opt("Carrier sync, using a PLL or Costas loop", correct=True),
                    opt("Symbol/timing sync, using early-late"),
                    opt("Frame sync, using a known preamble"),
                    opt("Doppler sync, using an FFT"),
                ),
                "Carrier sync aligns the frequency and phase of the carrier using a PLL or "
                "Costas loop.",
            ),
        ),
        "Lab: QAM BER curves & the Shannon bound": (
            q(
                "In the lab, why does 16-QAM show a worse BER than QPSK at 10 dB?",
                (
                    opt("It is a denser constellation", correct=True),
                    opt("It carries fewer bits per symbol"),
                    opt("It uses no Gray mapping"),
                    opt("It uses a wider bandwidth"),
                ),
                "The lab prints that 16-QAM BER at 10 dB is worse because it is a denser "
                "constellation.",
            ),
            q(
                "What Eb/N0 floor does the lab mark as the Shannon limit?",
                (
                    opt("0 dB"),
                    opt("-1.59 dB", correct=True),
                    opt("10 dB"),
                    opt("-3 dB"),
                ),
                "The lab draws a line at -1.59 dB: no scheme works below this Eb/N0 floor.",
            ),
            q(
                "How does the lab suggest getting the QAM theory curves directly in MATLAB?",
                (
                    opt("Use berawgn(EbN0, 'qam', M)", correct=True),
                    opt("Use the FFT of the received samples"),
                    opt("Use a Huffman tree"),
                    opt("Use a zero-forcing equalizer"),
                ),
                "The lab notes that the MATLAB way is berawgn(EbN0, 'qam', M), which gives "
                "the theory curves directly.",
            ),
        ),
    },
    final=(
        q(
            "How many bits per symbol does 256-QAM carry?",
            (
                opt("6 bits/symbol"),
                opt("8 bits/symbol", correct=True),
                opt("4 bits/symbol"),
                opt("10 bits/symbol"),
            ),
            "256-QAM carries log2(256) = 8 bits per symbol.",
        ),
        q(
            "Which choice correctly states the Shannon capacity bound?",
            (
                opt("C = B log2(1 + S/N)", correct=True),
                opt("C = B log2(S/N)"),
                opt("C = log2(1 + B S/N)"),
                opt("C = B (1 + S/N)"),
            ),
            "The Shannon capacity bound for an AWGN channel is C = B log2(1 + S/N) bits/s.",
        ),
        q(
            "For the source with probabilities 0.5, 0.25, 0.125, 0.125, what is the entropy?",
            (
                opt("2.0 bits/symbol"),
                opt("1.75 bits/symbol", correct=True),
                opt("1.0 bits/symbol"),
                opt("3.0 bits/symbol"),
            ),
            "H = 0.5(1) + 0.25(2) + 0.125(3) + 0.125(3) = 1.75 bits/symbol, matching the "
            "Huffman average length.",
        ),
        q(
            "What gives OFDM its per-subcarrier flat-channel advantage against fading?",
            (
                opt("Sending many narrow subcarriers, each seeing a flat channel", correct=True),
                opt("Sending one wideband carrier with heavy coding"),
                opt("Spreading the signal over a Tanner graph"),
                opt("Removing the carrier sync stage"),
            ),
            "OFDM sends many narrow subcarriers in parallel, each so narrow that its own "
            "channel looks flat, sidestepping frequency-selective fading.",
        ),
        q(
            "Which modulation strategy suits a bandwidth-limited urban cellular or cable link?",
            (
                opt("High-order QAM such as 256-QAM", correct=True),
                opt("Low-order modulation with heavy coding"),
                opt("Spread spectrum at low order"),
                opt("BPSK with maximum redundancy"),
            ),
            "Bandwidth-limited links (5G mid-band, DOCSIS) crank QAM as high as the SNR allows.",
        ),
    ),
)
