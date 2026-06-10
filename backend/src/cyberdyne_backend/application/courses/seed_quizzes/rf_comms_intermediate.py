from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Digital modulation: ASK, FSK, PSK & QAM": (
            q(
                "Which carrier property does QAM vary to carry bits?",
                (
                    opt("only amplitude"),
                    opt("only frequency"),
                    opt("both amplitude and phase", correct=True),
                    opt("only phase"),
                ),
                "QAM maps a symbol to a point in the I/Q plane, varying both amplitude and phase.",
            ),
            q(
                "How many bits per symbol does a 16-QAM constellation carry?",
                (
                    opt("2 bits"),
                    opt("4 bits", correct=True),
                    opt("8 bits"),
                    opt("16 bits"),
                ),
                "Bits per symbol is log2(M); for M=16 that is log2(16) = 4 bits.",
            ),
            q(
                "Why do modern links drop from 256-QAM to QPSK at the cell edge?",
                (
                    opt(
                        "denser constellations need more SNR for the same error rate", correct=True
                    ),
                    opt("QPSK carries more bits per symbol"),
                    opt("QPSK uses less bandwidth than 256-QAM"),
                    opt("256-QAM cannot be demodulated outdoors"),
                ),
                "Denser constellations crowd points closer, so they need higher SNR; at the edge SNR is low.",
            ),
        ),
        "Spectra & pulse shaping": (
            q(
                "What artifact does the shape of a transmitted pulse cause between neighboring symbols?",
                (
                    opt("inter-symbol interference (ISI)", correct=True),
                    opt("frequency drift"),
                    opt("carrier phase noise"),
                    opt("quantization error"),
                ),
                "The pulse shape sets bandwidth and whether neighbors smear into each other, which is ISI.",
            ),
            q(
                "What property does the raised-cosine pulse preserve while taming time-domain ringing?",
                (
                    opt("the zero-ISI (Nyquist) property", correct=True),
                    opt("a perfectly rectangular spectrum"),
                    opt("infinite bandwidth"),
                    opt("constant phase"),
                ),
                "The raised-cosine pulse keeps the zero-ISI property while trading a little excess bandwidth.",
            ),
            q(
                "Why is the pulse-shaping filter usually split as root-raised-cosine at both ends?",
                (
                    opt(
                        "the two halves multiply to a full raised cosine and the receiver half is a matched filter",
                        correct=True,
                    ),
                    opt("it doubles the symbol rate"),
                    opt("it removes the need for a carrier"),
                    opt("it eliminates all noise"),
                ),
                "Split RRC at TX and RX multiply to a full raised cosine, and the RX half acts as a matched filter maximizing SNR.",
            ),
        ),
        "Channel capacity & the Shannon limit": (
            q(
                "What is the Shannon capacity formula for a channel of bandwidth B with a given SNR?",
                (
                    opt("C = B * log2(1 + SNR)", correct=True),
                    opt("C = B * SNR"),
                    opt("C = log2(B) * SNR"),
                    opt("C = B / (1 + SNR)"),
                ),
                "Shannon's law gives C = B*log2(1 + SNR) bits per second as the error-free ceiling.",
            ),
            q(
                "How does capacity grow with power/SNR versus bandwidth?",
                (
                    opt("linearly with bandwidth but only logarithmically with SNR", correct=True),
                    opt("logarithmically with bandwidth but linearly with SNR"),
                    opt("linearly with both"),
                    opt("logarithmically with both"),
                ),
                "Capacity grows linearly with bandwidth but only logarithmically with power/SNR, so doubling power adds ~1 bit/s/Hz.",
            ),
            q(
                "What does spectral efficiency measure?",
                (
                    opt("how close a real system gets to C/B, in bits/s/Hz", correct=True),
                    opt("the total power consumed per symbol"),
                    opt("the carrier frequency in Hz"),
                    opt("the number of antennas used"),
                ),
                "Spectral efficiency in bits/s/Hz is how close a real system gets to the C/B capacity bound.",
            ),
        ),
        "Multiplexing & multiple access": (
            q(
                "What resource does FDM/FDMA use to separate signals?",
                (
                    opt("frequency bands", correct=True),
                    opt("time slots"),
                    opt("orthogonal codes"),
                    opt("spatial beams"),
                ),
                "FDM/FDMA gives each signal its own frequency band with guard bands between them.",
            ),
            q(
                "In CDMA, how does a receiver recover one user while many transmit in the same band at once?",
                (
                    opt(
                        "by correlating with that user's near-orthogonal spreading code",
                        correct=True,
                    ),
                    opt("by assigning each user a separate time slot"),
                    opt("by giving each user a separate frequency band"),
                    opt("by steering a directional beam at the user"),
                ),
                "All users share the band; correlating with one user's near-orthogonal code recovers it and treats others as noise.",
            ),
            q(
                "Which multiple-access scheme do LTE and Wi-Fi 6 use to serve many devices via frequency-and-time tiles?",
                (
                    opt("OFDMA", correct=True),
                    opt("pure TDMA"),
                    opt("pure FDMA"),
                    opt("CDMA"),
                ),
                "LTE uses OFDMA (frequency + time tiles); Wi-Fi 6 added OFDMA so an access point can serve many devices at once.",
            ),
        ),
        "Error-control coding": (
            q(
                "What can a single parity bit do for a codeword?",
                (
                    opt("detect a single flipped bit but not locate it", correct=True),
                    opt("correct a single flipped bit"),
                    opt("correct burst errors"),
                    opt("locate and fix any number of errors"),
                ),
                "A parity bit makes the count of ones even; one flip breaks parity and is detected but not located.",
            ),
            q(
                "What is the code rate of the Hamming(7,4) code?",
                (
                    opt("4/7", correct=True),
                    opt("7/4"),
                    opt("1/2"),
                    opt("3/7"),
                ),
                "Rate is data bits over total bits: Hamming(7,4) sends 4 data bits as 7, so the rate is 4/7.",
            ),
            q(
                "How does interleaving help against burst errors?",
                (
                    opt(
                        "it shuffles bits so a burst spreads into isolated errors the code can fix",
                        correct=True,
                    ),
                    opt("it adds more parity bits to the burst"),
                    opt("it retransmits the corrupted burst"),
                    opt("it increases the carrier power during bursts"),
                ),
                "Interleaving shuffles bits before transmission so a burst is spread into scattered errors the code can handle.",
            ),
        ),
        "Lab: QAM constellation with noise & an eye diagram": (
            q(
                "In the lab, which I and Q levels define the 16-QAM constellation?",
                (
                    opt("{-3, -1, 1, 3}", correct=True),
                    opt("{-1, 0, 1}"),
                    opt("{0, 1}"),
                    opt("{-2, 2}"),
                ),
                "The lab sets levels = [-3, -1, 1, 3] for both I and Q, giving the 16-point grid.",
            ),
            q(
                "What happens to the constellation when snr_dB is dropped from 25 to 10 in the lab?",
                (
                    opt("the clusters merge and symbol errors jump", correct=True),
                    opt("the clusters tighten and errors fall to zero"),
                    opt("the constellation gains more points"),
                    opt("the eye diagram opens wider"),
                ),
                "Lower SNR adds more noise, so clusters merge and the symbol error count rises.",
            ),
            q(
                "How does the lab decide which constellation point a received symbol is?",
                (
                    opt(
                        "it rounds each received value to the nearest constellation level",
                        correct=True,
                    ),
                    opt("it always picks the level 3"),
                    opt("it averages all received symbols"),
                    opt("it discards symbols with any noise"),
                ),
                "The nearest() function picks the level minimizing the distance to the received value for the I and Q rails.",
            ),
        ),
    },
    final=(
        q(
            "Which scheme packs the most bits per symbol for a given number of constellation points M?",
            (
                opt("the one with the largest M, since bits per symbol is log2(M)", correct=True),
                opt("the one with the smallest M"),
                opt("BPSK, regardless of M"),
                opt("all schemes carry the same bits per symbol"),
            ),
            "Bits per symbol is log2(M), so a larger constellation carries more bits at the cost of needing more SNR.",
        ),
        q(
            "According to Shannon, which buys capacity more cheaply for a power-starved deep-space link?",
            (
                opt("wider bandwidth, since capacity grows linearly with bandwidth", correct=True),
                opt("more transmit power, since capacity grows linearly with power"),
                opt("a denser constellation alone"),
                opt("removing all coding"),
            ),
            "Capacity grows linearly with bandwidth but only logarithmically with SNR, so bandwidth-rich power-starved links lean on bandwidth and heavy coding.",
        ),
        q(
            "What is the main role of pulse shaping such as raised-cosine in a digital link?",
            (
                opt("limit bandwidth while keeping the zero-ISI property", correct=True),
                opt("increase the carrier frequency"),
                opt("add redundancy for error correction"),
                opt("separate multiple users by code"),
            ),
            "Raised-cosine shaping controls occupied bandwidth while preserving zero ISI at the symbol sampling instants.",
        ),
        q(
            "Which technique lets many users share one band simultaneously using near-orthogonal codes?",
            (
                opt("CDMA", correct=True),
                opt("FDMA"),
                opt("TDMA"),
                opt("raised-cosine filtering"),
            ),
            "CDMA has all users transmit in the same band at once, separated by near-orthogonal spreading codes.",
        ),
        q(
            "Why do modern turbo and LDPC codes matter for approaching the Shannon limit?",
            (
                opt(
                    "they operate within a fraction of a dB of the limit, giving large coding gain",
                    correct=True,
                ),
                opt("they remove the need for any bandwidth"),
                opt("they increase the constellation size automatically"),
                opt("they eliminate inter-symbol interference"),
            ),
            "Turbo and LDPC codes get within a fraction of a dB of Shannon capacity, shifting the BER waterfall left with strong coding gain.",
        ),
    ),
)
