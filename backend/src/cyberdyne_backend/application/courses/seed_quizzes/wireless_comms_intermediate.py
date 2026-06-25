"""Curated quiz questions for the Wireless & Mobile Communications - Intermediate course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Large-scale vs small-scale fading": (
            q(
                "What characterises large-scale fading?",
                (
                    opt("Fast, deep dips over fractions of a wavelength"),
                    opt(
                        "A slow trend over tens or hundreds of metres from path loss plus shadowing, setting coverage",
                        correct=True,
                    ),
                    opt("Interference from neighbouring cells only"),
                    opt("The Doppler shift from mobility"),
                ),
                "Large-scale fading is the slow trend (path loss + shadowing) that sets coverage.",
            ),
            q(
                "What causes small-scale fading?",
                (
                    opt("Buildings and hills blocking the signal over long distances"),
                    opt(
                        "Multipath waves adding constructively or destructively over fractions of a wavelength",
                        correct=True,
                    ),
                    opt("The receiver's noise figure"),
                    opt("The choice of carrier frequency only"),
                ),
                "Small-scale fading comes from multipath components interfering as the receiver moves a fraction of a wavelength.",
            ),
            q(
                "Why can a link drop even when the average received power is fine?",
                (
                    opt("Because the noise floor disappears"),
                    opt(
                        "Because the receiver can sit in a deep small-scale fade despite an adequate average power",
                        correct=True,
                    ),
                    opt("Because large-scale fading raises the power too high"),
                    opt("Because handover always fails at high power"),
                ),
                "A deep small-scale fade can drop the link momentarily even when the average power is adequate, which is why diversity is added.",
            ),
        ),
        "Multipath & delay spread": (
            q(
                "What is delay spread?",
                (
                    opt("The time a base station takes to schedule a user"),
                    opt(
                        "The spread in arrival times between the first and last meaningful multipath copies",
                        correct=True,
                    ),
                    opt("The delay before a handover triggers"),
                    opt("The width of a single subcarrier"),
                ),
                "Delay spread is the time spread between the earliest and latest significant multipath arrivals.",
            ),
            q(
                "When does multipath cause intersymbol interference (ISI)?",
                (
                    opt("When the symbol period is much longer than the delay spread"),
                    opt(
                        "When the symbol period is comparable to or shorter than the delay spread, so echoes land on the next symbol",
                        correct=True,
                    ),
                    opt("Only in free space with no reflections"),
                    opt("Only when the carrier frequency is below 1 GHz"),
                ),
                "ISI arises when symbols are short relative to the delay spread, so a symbol's echoes overlap the next symbol.",
            ),
            q(
                "What does the coherence bandwidth tell you?",
                (
                    opt("The total spectrum a country has licensed"),
                    opt(
                        "The frequency range over which the channel fades together; signals wider than it see frequency-selective fading",
                        correct=True,
                    ),
                    opt("The maximum transmit power allowed"),
                    opt("The number of antennas needed"),
                ),
                "Coherence bandwidth (about 1/delay spread) is the band over which fading is correlated; wider signals fade selectively.",
            ),
        ),
        "Rayleigh & Rician fading": (
            q(
                "When is the Rayleigh distribution the right model for the fading envelope?",
                (
                    opt("When a strong line-of-sight path dominates"),
                    opt(
                        "When there is no dominant path, only scattered non-line-of-sight components",
                        correct=True,
                    ),
                    opt("When there is no multipath at all"),
                    opt("Only when the receiver is stationary"),
                ),
                "Rayleigh fading models the envelope when no dominant (line-of-sight) component exists, only scatter.",
            ),
            q(
                "What does a large Rician K-factor imply?",
                (
                    opt("Deep fades become more frequent"),
                    opt(
                        "A strong line-of-sight component, so fades are shallow and the link behaves almost like free space",
                        correct=True,
                    ),
                    opt("The channel reverts exactly to Rayleigh"),
                    opt("The Doppler shift goes to zero"),
                ),
                "A large K-factor means the LOS component dominates the scatter, giving shallow fades near free-space behaviour.",
            ),
            q(
                "What does the Doppler shift fd = v / lambda determine?",
                (
                    opt("How deep the fades are"),
                    opt("How fast the fading changes as the receiver moves", correct=True),
                    opt("The path-loss exponent"),
                    opt("The number of multipath components"),
                ),
                "Doppler shift (speed over wavelength) sets how rapidly the fading varies in time.",
            ),
        ),
        "Digital modulation & BER: PSK and QAM": (
            q(
                "How does PSK encode bits?",
                (
                    opt("In the carrier's amplitude only"),
                    opt("In the carrier's phase", correct=True),
                    opt("In the carrier's frequency only"),
                    opt("In the spreading code"),
                ),
                "Phase-shift keying encodes bits in the carrier's phase (e.g. BPSK 2 phases, QPSK 4 phases).",
            ),
            q(
                "Why does a denser constellation such as 256-QAM need more SNR for the same BER?",
                (
                    opt("Because it uses a lower carrier frequency"),
                    opt(
                        "Because its points sit closer together, so noise more easily pushes a symbol into a neighbour's region",
                        correct=True,
                    ),
                    opt("Because it carries fewer bits per symbol"),
                    opt("Because it ignores the channel entirely"),
                ),
                "More constellation points sit closer together, so a given noise level more easily causes an error, demanding higher SNR.",
            ),
            q(
                "What is the idea behind adaptive modulation in LTE/5G?",
                (
                    opt("Always use the densest modulation regardless of channel"),
                    opt(
                        "Use dense modulation (256-QAM) when SNR is high for speed, and fall back to QPSK when SNR drops to stay connected",
                        correct=True,
                    ),
                    opt("Use a fixed modulation for every user forever"),
                    opt("Switch to analog when SNR is low"),
                ),
                "Adaptive modulation picks the densest constellation the current SNR supports, trading speed for robustness as the channel changes.",
            ),
        ),
        "OFDM: why & how": (
            q(
                "How does OFDM avoid intersymbol interference from a fast data stream?",
                (
                    opt("By sending one very fast carrier"),
                    opt(
                        "By sending many slow subcarriers in parallel, so each symbol is long compared to the delay spread",
                        correct=True,
                    ),
                    opt("By removing all multipath from the channel"),
                    opt("By lowering the transmit power"),
                ),
                "OFDM splits the stream across many slow subcarriers, so each symbol is long and the channel looks flat per subcarrier.",
            ),
            q(
                "What does the cyclic prefix do?",
                (
                    opt("It encrypts the OFDM symbol"),
                    opt(
                        "It pastes a copy of the symbol's tail to its front as a guard interval that absorbs multipath echoes and removes ISI",
                        correct=True,
                    ),
                    opt("It increases the carrier frequency"),
                    opt("It removes the need for an FFT"),
                ),
                "The cyclic prefix is a guard interval (a copy of the symbol tail) that absorbs echoes within it, eliminating ISI.",
            ),
            q(
                "Why are the OFDM subcarriers called orthogonal?",
                (
                    opt("Because they are on completely separate frequency bands with large gaps"),
                    opt(
                        "Because they are spaced so each one's peak sits on the others' nulls, so they overlap yet do not interfere",
                        correct=True,
                    ),
                    opt("Because they each use a different antenna"),
                    opt("Because they are transmitted at different times"),
                ),
                "Orthogonal spacing places each subcarrier's peak on the others' spectral nulls, allowing overlap without interference.",
            ),
        ),
        "Equalization & the ISI problem": (
            q(
                "What is the job of an equalizer?",
                (
                    opt("To add noise to the signal"),
                    opt(
                        "To undo the channel's distortion, applying roughly the inverse of H(f)",
                        correct=True,
                    ),
                    opt("To increase the transmit power"),
                    opt("To assign frequencies to users"),
                ),
                "An equalizer reverses the channel's filtering by applying approximately 1/H(f) to flatten the response.",
            ),
            q(
                "What is the drawback of a zero-forcing equalizer?",
                (
                    opt("It cannot remove any ISI"),
                    opt(
                        "Where the channel has a deep null, inverting it blows up and amplifies the noise",
                        correct=True,
                    ),
                    opt("It requires no training symbols"),
                    opt("It only works in free space"),
                ),
                "Zero-forcing inverts H exactly, but at channel nulls 1/H becomes huge and amplifies noise; MMSE balances this.",
            ),
            q(
                "Why does equalization collapse to one complex multiply per subcarrier in OFDM?",
                (
                    opt("Because OFDM has no channel"),
                    opt(
                        "Because the cyclic prefix makes each narrow subcarrier see flat fading, so per-tone division suffices",
                        correct=True,
                    ),
                    opt("Because OFDM uses no modulation"),
                    opt("Because the receiver ignores ISI"),
                ),
                "With the cyclic prefix, each subcarrier sees a flat channel, so equalization is a single per-tone complex division.",
            ),
        ),
    },
    final=(
        q(
            "Which pairing of fading scale and its cause is correct?",
            (
                opt("Large-scale fading is caused by multipath over a fraction of a wavelength"),
                opt(
                    "Large-scale fading comes from path loss and shadowing; small-scale fading comes from multipath interference",
                    correct=True,
                ),
                opt("Small-scale fading is caused by hills and buildings over hundreds of metres"),
                opt("Both scales are caused only by the noise figure"),
            ),
            "Large-scale = path loss + shadowing (coverage); small-scale = multipath interference over fractions of a wavelength.",
        ),
        q(
            "A channel has a large delay spread relative to the symbol period. What follows?",
            (
                opt("The channel is flat and ISI-free"),
                opt(
                    "It is frequency-selective and causes intersymbol interference",
                    correct=True,
                ),
                opt("Coherence bandwidth becomes infinite"),
                opt("Multipath disappears"),
            ),
            "A delay spread comparable to or larger than the symbol period gives frequency-selective fading and ISI.",
        ),
        q(
            "Compared to a Rician channel with large K, a Rayleigh channel...",
            (
                opt("has a stronger line-of-sight path"),
                opt("has shallower fades"),
                opt(
                    "has no dominant path and suffers more frequent deep fades",
                    correct=True,
                ),
                opt("has zero Doppler shift"),
            ),
            "Rayleigh (no dominant path) suffers deeper, more frequent fades than a high-K Rician (strong LOS) channel.",
        ),
        q(
            "Why does QPSK stay connected at lower SNR than 256-QAM?",
            (
                opt("QPSK uses a higher carrier frequency"),
                opt(
                    "QPSK has fewer, more widely spaced constellation points, so noise is less likely to cause an error",
                    correct=True,
                ),
                opt("QPSK carries more bits per symbol"),
                opt("QPSK does not use a constellation"),
            ),
            "QPSK's sparse, well-separated constellation tolerates more noise, so it works at lower SNR than dense 256-QAM.",
        ),
        q(
            "What two ideas make OFDM robust to multipath?",
            (
                opt("High transmit power and a single fast carrier"),
                opt(
                    "Orthogonal narrow subcarriers and a cyclic prefix that absorbs echoes",
                    correct=True,
                ),
                opt("Analog modulation and no guard interval"),
                opt("Removing the FFT and ignoring the channel"),
            ),
            "OFDM uses orthogonal slow subcarriers plus a cyclic prefix guard interval to absorb multipath and eliminate ISI.",
        ),
        q(
            "Why is OFDM equalization so simple compared to time-domain equalization?",
            (
                opt("Because OFDM signals never face a channel"),
                opt(
                    "Because the cyclic prefix turns the channel into a flat per-subcarrier multiply, so each tone is fixed by one division",
                    correct=True,
                ),
                opt("Because zero-forcing never amplifies noise"),
                opt("Because OFDM removes all noise"),
            ),
            "The cyclic prefix makes each subcarrier flat, reducing equalization to one complex division per tone instead of time-domain deconvolution.",
        ),
    ),
)
