from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The digital communication system": (
            q(
                "What is the job of the source coder in the communication pipeline?",
                (
                    opt("Add structured redundancy to fight errors"),
                    opt("Remove redundancy by compressing the source", correct=True),
                    opt("Map bits to a transmittable waveform"),
                    opt("Decide which symbol was sent"),
                ),
                "The source coder compresses (removes redundancy); examples are JPEG, MP3 and H.264.",
            ),
            q(
                "Bandwidth efficiency eta_bw is defined as which ratio?",
                (
                    opt("Rb over B, in bits/s per Hz", correct=True),
                    opt("B over Rb, in Hz per bit"),
                    opt("Eb over N0, energy per bit over noise density"),
                    opt("N0 over Eb, noise density over energy per bit"),
                ),
                "Bandwidth efficiency is Rb/B, how many bits per second you pack into each hertz.",
            ),
            q(
                "Which block is responsible for adding structured redundancy to correct errors?",
                (
                    opt("The modulator"),
                    opt("The source coder"),
                    opt("The channel coder", correct=True),
                    opt("The detector"),
                ),
                "The channel coder adds structured redundancy, like LDPC in 5G or Reed-Solomon on a CD.",
            ),
        ),
        "Sampling, quantization & PCM": (
            q(
                "The Nyquist-Shannon theorem requires the sampling rate fs to satisfy what condition for a signal of bandwidth B?",
                (
                    opt("fs >= 2B", correct=True),
                    opt("fs >= B"),
                    opt("fs >= B/2"),
                    opt("fs >= 4B"),
                ),
                "Perfect recovery requires fs at least twice the bandwidth, fs >= 2B.",
            ),
            q(
                "By the 6 dB per bit rule, what is the approximate SQNR of an n-bit quantizer?",
                (
                    opt("6.02 n + 1.76 dB", correct=True),
                    opt("1.76 n + 6.02 dB"),
                    opt("6.02 n only"),
                    opt("2 n + 6.02 dB"),
                ),
                "SQNR_dB is approximately 6.02 n + 1.76, so each added bit buys about 6 dB.",
            ),
            q(
                "Why does telephony use mu-law or A-law companding?",
                (
                    opt("To increase the sampling rate above Nyquist"),
                    opt("To give near-constant SNR across a wide loudness range", correct=True),
                    opt("To remove the need for an anti-alias filter"),
                    opt("To double the number of quantization bits"),
                ),
                "Companding uses a logarithmic step size so quiet and loud speech both get near-constant SNR.",
            ),
        ),
        "Baseband signaling & pulse shaping": (
            q(
                "Which line code is self-clocking and used in 10BASE-T Ethernet?",
                (
                    opt("NRZ"),
                    opt("RZ"),
                    opt("Manchester", correct=True),
                    opt("Bipolar/AMI"),
                ),
                "Manchester coding places an edge mid-bit, making it self-clocking, used in 10BASE-T Ethernet.",
            ),
            q(
                "What does the Nyquist ISI criterion say about a zero-ISI pulse?",
                (
                    opt("It must be zero at every other symbol instant", correct=True),
                    opt("It must be constant over the whole symbol"),
                    opt("It must have infinite bandwidth"),
                    opt("It must alternate polarity each symbol"),
                ),
                "A pulse causes zero ISI if it is zero at every other symbol sampling instant.",
            ),
            q(
                "For a raised-cosine pulse, how does the occupied bandwidth depend on the roll-off alpha?",
                (
                    opt("B = (Rs/2)(1 + alpha)", correct=True),
                    opt("B = (Rs/2)(1 - alpha)"),
                    opt("B = Rs(1 + alpha)"),
                    opt("B = (Rs/2) alpha"),
                ),
                "Bandwidth is B = (Rs/2)(1 + alpha); larger roll-off widens the spectrum.",
            ),
        ),
        "Digital modulation basics": (
            q(
                "In ASK, FSK and PSK, which property of the carrier varies for PSK?",
                (
                    opt("Amplitude"),
                    opt("Frequency"),
                    opt("Phase", correct=True),
                    opt("Bandwidth"),
                ),
                "PSK varies the phase; ASK varies amplitude and FSK varies frequency.",
            ),
            q(
                "How many bits per symbol does QPSK carry compared with BPSK?",
                (
                    opt("QPSK carries 2 bits/symbol vs BPSK 1 bit/symbol", correct=True),
                    opt("QPSK carries 1 bit/symbol vs BPSK 2 bits/symbol"),
                    opt("Both carry 1 bit/symbol"),
                    opt("QPSK carries 4 bits/symbol vs BPSK 2 bits/symbol"),
                ),
                "BPSK uses two antipodal points (1 bit/symbol); QPSK uses four points (2 bits/symbol).",
            ),
            q(
                "On the I/Q plane, a symbol point (I, Q) corresponds to which waveform?",
                (
                    opt("I cos(2 pi fc t) - Q sin(2 pi fc t)", correct=True),
                    opt("I sin(2 pi fc t) + Q cos(2 pi fc t)"),
                    opt("I cos(2 pi fc t) + Q cos(2 pi fc t)"),
                    opt("Q cos(2 pi fc t) - I sin(2 pi fc t)"),
                ),
                "Any symbol is I cos(2 pi fc t) - Q sin(2 pi fc t), so a point (I, Q) is a waveform.",
            ),
        ),
        "The AWGN channel & detection": (
            q(
                "In the AWGN model r = s + n, what is the received sample?",
                (
                    opt("The sent symbol plus a Gaussian noise sample", correct=True),
                    opt("The sent symbol multiplied by a fading factor"),
                    opt("Only the noise, with the symbol removed"),
                    opt("The sent symbol delayed by one symbol period"),
                ),
                "AWGN adds a Gaussian random number to the sent symbol: r = s + n.",
            ),
            q(
                "What does the matched filter maximize, making it the optimal front end for AWGN?",
                (
                    opt("The signal-to-noise ratio at the sampling instant", correct=True),
                    opt("The occupied bandwidth"),
                    opt("The number of bits per symbol"),
                    opt("The roll-off factor of the pulse"),
                ),
                "The matched filter correlates with a time-reversed pulse copy to maximize SNR at the sampling instant.",
            ),
            q(
                "For equal priors and Gaussian noise, what is the optimal decision rule?",
                (
                    opt(
                        "Pick the constellation point closest to the received sample", correct=True
                    ),
                    opt("Always pick the highest-energy symbol"),
                    opt("Pick a symbol at random weighted by prior"),
                    opt("Pick the point farthest from the received sample"),
                ),
                "The minimum-distance rule picks the nearest constellation point; for BPSK that is just r > 0 means 1.",
            ),
        ),
        "Lab: constellation, eye diagram & BER": (
            q(
                "How many bits per symbol does the QPSK lab map onto each transmitted symbol?",
                (
                    opt("1 bit"),
                    opt("2 bits", correct=True),
                    opt("4 bits"),
                    opt("8 bits"),
                ),
                "The lab generates 2*N bits and maps 2 bits per QPSK symbol.",
            ),
            q(
                "In the BER sweep, how is each received bit decided per rail?",
                (
                    opt("Compare the real and imaginary parts against zero", correct=True),
                    opt("Compare against the levels -3, -1, 1, 3"),
                    opt("Take the FFT of the received block"),
                    opt("Average over a window of 8 samples"),
                ),
                "QPSK detection slices each rail at zero: bits are (r.real > 0) and (r.imag > 0).",
            ),
            q(
                "What does the eye diagram in the lab overlay to form its picture?",
                (
                    opt(
                        "Many 2-symbol windows of the pulse-shaped baseband waveform", correct=True
                    ),
                    opt("The BER values at each Eb/N0"),
                    opt("The noisy constellation cloud points"),
                    opt("The Shannon capacity bound"),
                ),
                "The eye is built by overlaying 2-symbol windows of the smoothed baseband I-rail waveform.",
            ),
        ),
    },
    final=(
        q(
            "Order the transmit chain in the digital communication system block diagram.",
            (
                opt(
                    "source -> source coder -> channel coder -> modulator -> channel", correct=True
                ),
                opt("source -> modulator -> channel coder -> source coder -> channel"),
                opt("source -> channel coder -> source coder -> modulator -> channel"),
                opt("source -> modulator -> channel -> channel coder -> source coder"),
            ),
            "Bits are compressed, then protected with redundancy, modulated, and sent through the channel.",
        ),
        q(
            "A telephone channel carries 0-4 kHz speech. Why is it sampled at 8 kHz?",
            (
                opt("Because 8 kHz meets the Nyquist rate of 2 times 4 kHz", correct=True),
                opt("Because 8 kHz is the carrier frequency"),
                opt("Because companding requires exactly 8 kHz"),
                opt("Because 8 bits per sample forces an 8 kHz rate"),
            ),
            "Nyquist requires fs >= 2B = 8 kHz for a 4 kHz bandwidth speech signal.",
        ),
        q(
            "Why does QPSK double the data rate of BPSK without extra bandwidth or energy per bit?",
            (
                opt("It uses four I/Q points carrying 2 bits/symbol at the same Eb", correct=True),
                opt("It increases the carrier frequency by a factor of two"),
                opt("It halves the roll-off factor of the pulse shaping"),
                opt("It adds a channel code that doubles the rate"),
            ),
            "QPSK packs four constellation points (2 bits/symbol) in the same bandwidth at the same energy per bit.",
        ),
        q(
            "For BPSK and QPSK, the bit error rate Pb is given by which expression?",
            (
                opt("Q(sqrt(2 Eb/N0))", correct=True),
                opt("Q(sqrt(Eb/N0))"),
                opt("Q(2 Eb/N0)"),
                opt("Q(N0/(2 Eb))"),
            ),
            "Pb = Q(sqrt(2 Eb/N0)); the curve plunges as Eb/N0 grows, the waterfall effect.",
        ),
        q(
            "Which sequence correctly pairs each block with the impairment or job it handles?",
            (
                opt(
                    "Matched filter maximizes SNR; channel adds noise/fading; pulse shaping limits bandwidth",
                    correct=True,
                ),
                opt(
                    "Matched filter compresses the source; channel coder adds noise; modulator removes ISI"
                ),
                opt(
                    "Source coder corrects errors; channel decoder compresses; detector adds redundancy"
                ),
                opt(
                    "Pulse shaping adds noise; matched filter increases bandwidth; channel removes ISI"
                ),
            ),
            "The matched filter maximizes SNR, the channel adds AWGN and fading, and pulse shaping controls bandwidth and ISI.",
        ),
    ),
)
