"""Curated quiz questions for the Analog Communications - Advanced course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Noise in AM systems": (
            q(
                "What is the detection gain of DSB-SC with coherent detection?",
                (
                    opt("About 3 (a 3x improvement)"),
                    opt("1 (it neither helps nor hurts versus baseband)", correct=True),
                    opt("Zero"),
                    opt("It grows with the square of bandwidth"),
                ),
                "DSB-SC with coherent detection has detection gain 1 — the same output SNR as sending baseband.",
            ),
            q(
                "What is the threshold effect in an envelope-detected AM receiver?",
                (
                    opt("The output SNR rises faster than linearly at all levels"),
                    opt(
                        "Below a certain input SNR the recovered signal collapses abruptly rather than degrading gracefully",
                        correct=True,
                    ),
                    opt("The carrier disappears above a certain power"),
                    opt("The bandwidth doubles at low SNR"),
                ),
                "Once noise is comparable to the carrier, the envelope detector's output collapses abruptly — the threshold effect.",
            ),
            q(
                "Why is envelope-detected AM a few dB worse than coherent DSB-SC?",
                (
                    opt("Because it occupies less bandwidth"),
                    opt(
                        "Because power is wasted in the carrier and it suffers a threshold effect",
                        correct=True,
                    ),
                    opt("Because it has no sidebands"),
                    opt("Because it uses a PLL"),
                ),
                "AM wastes power in the carrier and has a threshold effect, making it worse than coherent DSB-SC.",
            ),
        ),
        "Noise in FM systems & the FM advantage": (
            q(
                "How does FM output SNR scale with the modulation index β (above threshold)?",
                (
                    opt("Linearly with β"),
                    opt("With the square of β (∝ β²)", correct=True),
                    opt("Inversely with β"),
                    opt("It is independent of β"),
                ),
                "Above threshold the FM output SNR grows roughly as β², so more bandwidth buys a quadratic SNR gain.",
            ),
            q(
                "What is the capture effect in FM?",
                (
                    opt("The receiver locks onto the noise floor"),
                    opt(
                        "When two FM signals share a channel, the stronger is demodulated and the weaker is suppressed",
                        correct=True,
                    ),
                    opt("The carrier captures all the message power"),
                    opt("The IF captures the image frequency"),
                ),
                "The capture effect means an FM receiver demodulates the stronger signal and suppresses the weaker one.",
            ),
            q(
                "What is the fundamental trade FM makes that AM cannot?",
                (
                    opt("It trades carrier power for sidebands"),
                    opt("It trades bandwidth for SNR", correct=True),
                    opt("It trades amplitude for phase with no benefit"),
                    opt("It trades sampling rate for bit depth"),
                ),
                "FM spends extra bandwidth (larger β) to gain output SNR — a trade AM cannot make.",
            ),
        ),
        "Pre-emphasis & de-emphasis": (
            q(
                "Why does FM need pre-emphasis and de-emphasis?",
                (
                    opt("Because the carrier is too weak"),
                    opt(
                        "Because FM noise power density rises with frequency, hurting high-frequency SNR",
                        correct=True,
                    ),
                    opt("Because the message has no low frequencies"),
                    opt("To increase the modulation index"),
                ),
                "After the discriminator the noise PSD rises with frequency (parabolic), so the highs need protection.",
            ),
            q(
                "What does the de-emphasis filter at the receiver do?",
                (
                    opt("It boosts the high frequencies further"),
                    opt(
                        "It is the inverse low-pass of pre-emphasis, cutting the highs and the high-frequency noise",
                        correct=True,
                    ),
                    opt("It re-inserts the carrier"),
                    opt("It samples the signal"),
                ),
                "De-emphasis is the inverse of pre-emphasis; it flattens the message and attenuates the un-boosted high-frequency noise.",
            ),
            q(
                "What is the net effect of the matched pre-/de-emphasis pair on the message?",
                (
                    opt("The message high frequencies are permanently boosted"),
                    opt(
                        "The message response is flat, but high-frequency noise is reduced",
                        correct=True,
                    ),
                    opt("The message is converted to digital"),
                    opt("The bandwidth is halved"),
                ),
                "The two filters are reciprocals, so the message is unchanged (flat) while channel noise meets only the de-emphasis cut.",
            ),
        ),
        "Sampling & pulse-amplitude modulation": (
            q(
                "What does the Nyquist sampling theorem require?",
                (
                    opt("fs ≥ B"),
                    opt("fs ≥ 2B (at least twice the bandwidth)", correct=True),
                    opt("fs ≥ fc"),
                    opt("fs equal to the carrier frequency"),
                ),
                "A signal of bandwidth B can be reconstructed exactly if sampled at fs ≥ 2B.",
            ),
            q(
                "What is aliasing?",
                (
                    opt("Noise added by the quantizer"),
                    opt(
                        "High frequencies masquerading as low ones when the sampling rate is too low",
                        correct=True,
                    ),
                    opt("The carrier appearing at the image frequency"),
                    opt("Loss of the DC component"),
                ),
                "Sampling too slowly makes high frequencies masquerade as low ones — aliasing — which is irreversible.",
            ),
            q(
                "What is pulse-amplitude modulation (PAM)?",
                (
                    opt("A fully digital bit stream"),
                    opt(
                        "A pulse train whose heights equal the sample values: discrete in time, still analog in amplitude",
                        correct=True,
                    ),
                    opt("Modulation of the carrier phase"),
                    opt("A method to remove aliasing"),
                ),
                "PAM is a pulse train with heights equal to the samples — discrete in time but still continuous in amplitude.",
            ),
        ),
        "PCM & the analog-to-digital bridge": (
            q(
                "What step does PCM add beyond PAM to complete A/D conversion?",
                (
                    opt("It re-modulates onto a carrier"),
                    opt(
                        "It quantizes each sample to one of 2^n levels and encodes it as an n-bit codeword",
                        correct=True,
                    ),
                    opt("It applies pre-emphasis"),
                    opt("It removes the sidebands"),
                ),
                "PCM quantizes each PAM sample to 2^n levels and encodes it as n bits, finishing analog-to-digital conversion.",
            ),
            q(
                "What does the '6 dB per bit' rule express?",
                (
                    opt("Each extra bit halves the bandwidth"),
                    opt(
                        "Each extra bit adds about 6 dB to the signal-to-quantization-noise ratio",
                        correct=True,
                    ),
                    opt("Each extra bit adds 6 dB of carrier power"),
                    opt("Six bits are needed per sample"),
                ),
                "SNRq ≈ 6.02·n + 1.76 dB, so each added bit roughly doubles the levels and adds about 6 dB.",
            ),
            q(
                "What is quantization noise?",
                (
                    opt("Noise from the channel only"),
                    opt(
                        "The unavoidable error from rounding each sample to the nearest discrete level",
                        correct=True,
                    ),
                    opt("The same as aliasing"),
                    opt("Noise added by pre-emphasis"),
                ),
                "Quantization noise is the rounding error to the nearest level, bounded by half a step.",
            ),
        ),
        "Multiplexing (FDM/TDM) & a system case study": (
            q(
                "How does frequency-division multiplexing (FDM) share a channel?",
                (
                    opt("By giving each signal its own time slot"),
                    opt("By giving each signal its own slice of the spectrum", correct=True),
                    opt("By quantizing each signal to fewer bits"),
                    opt("By using a single carrier for all signals"),
                ),
                "FDM gives each signal its own frequency slice (each modulates a different carrier).",
            ),
            q(
                "How does time-division multiplexing (TDM) share a channel?",
                (
                    opt("By giving each signal its own frequency band"),
                    opt(
                        "By interleaving the signals' samples in time, each in its own time slot",
                        correct=True,
                    ),
                    opt("By varying the carrier amplitude"),
                    opt("By using the image frequency"),
                ),
                "TDM interleaves samples in time, giving each signal its own time slot in one fast stream.",
            ),
            q(
                "In the FM-stereo case study, how is the L−R difference signal carried?",
                (
                    opt("As the mono baseband at audio frequencies"),
                    opt(
                        "DSB-SC-modulated onto a 38 kHz subcarrier (with a 19 kHz pilot reference)",
                        correct=True,
                    ),
                    opt("On the 10.7 MHz IF directly"),
                    opt("As a separate PCM bit stream"),
                ),
                "FM stereo puts L−R on a DSB-SC 38 kHz subcarrier above the mono audio, with a 19 kHz pilot marking the reference.",
            ),
        ),
    },
    final=(
        q(
            "Which statement about AM noise performance is correct?",
            (
                opt("AM with envelope detection is always better than baseband"),
                opt(
                    "Coherent DSB-SC matches baseband (gain 1); envelope AM is worse and has a threshold effect",
                    correct=True,
                ),
                opt("AM output SNR grows with the square of bandwidth"),
                opt("AM has no threshold effect"),
            ),
            "Coherent DSB-SC has detection gain 1; envelope-detected AM is a few dB worse and adds a threshold effect.",
        ),
        q(
            "Why does FM outperform AM in noise above threshold?",
            (
                opt("Because FM uses less bandwidth"),
                opt(
                    "Because output SNR scales with β², so spending bandwidth buys a quadratic SNR gain",
                    correct=True,
                ),
                opt("Because FM removes the carrier"),
                opt("Because FM is immune to all thresholds"),
            ),
            "FM trades bandwidth for SNR: output SNR rises as β², the advantage AM cannot achieve (FM still has its own threshold).",
        ),
        q(
            "How does the pre-/de-emphasis pair improve FM without altering the message?",
            (
                opt("It boosts the message highs permanently"),
                opt(
                    "Pre-emphasis boosts highs at TX, de-emphasis (the inverse) flattens the message and cuts un-boosted high-frequency noise",
                    correct=True,
                ),
                opt("It quantizes the message to bits"),
                opt("It doubles the sampling rate"),
            ),
            "The reciprocal filters leave the message flat but the de-emphasis low-pass attenuates the high-frequency noise.",
        ),
        q(
            "What does the Nyquist theorem guarantee, and what corruption occurs if it is violated?",
            (
                opt("It guarantees zero quantization noise; violation causes clipping"),
                opt(
                    "Exact reconstruction when fs ≥ 2B; sampling too slowly causes aliasing",
                    correct=True,
                ),
                opt("It guarantees image rejection; violation causes capture"),
                opt("It guarantees a flat message; violation causes de-emphasis"),
            ),
            "Nyquist guarantees exact reconstruction at fs ≥ 2B; too-slow sampling causes irreversible aliasing.",
        ),
        q(
            "By the '6 dB per bit' rule, why was PCM the decisive step into the digital era?",
            (
                opt("It uses less bandwidth than analog"),
                opt(
                    "Each bit adds about 6 dB of fidelity, and a bit stream can be regenerated perfectly at each repeater",
                    correct=True,
                ),
                opt("It removes the need for sampling"),
                opt("It eliminates quantization noise entirely"),
            ),
            "PCM gains about 6 dB per bit and, being bits, can be regenerated perfectly at repeaters — the decisive digital advantage.",
        ),
        q(
            "Which chain of techniques does the FM-stereo case study combine?",
            (
                opt("Only FM and sampling"),
                opt(
                    "FDM, DSB-SC, pre-emphasis, FM, superheterodyne reception, PLL detection and de-emphasis",
                    correct=True,
                ),
                opt("Only PCM and TDM"),
                opt("Only SSB and VSB"),
            ),
            "FM stereo stacks FDM (mono/pilot/subcarrier), DSB-SC, pre-emphasis, FM, superhet + PLL, and de-emphasis.",
        ),
    ),
)
