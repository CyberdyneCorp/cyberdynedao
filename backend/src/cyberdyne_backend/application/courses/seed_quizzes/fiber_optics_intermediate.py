"""Curated quiz questions for the Optical Fiber Communications - Intermediate course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Dispersion: modal, chromatic & PMD": (
            q(
                "Which type of dispersion exists only in multi-mode fiber?",
                (
                    opt("Chromatic dispersion"),
                    opt("Modal dispersion", correct=True),
                    opt("Polarization-mode dispersion"),
                    opt("Material absorption"),
                ),
                "Modal dispersion comes from different modes taking different path lengths, so it exists only in multi-mode fiber.",
            ),
            q(
                "Chromatic-dispersion pulse broadening scales with which quantities?",
                (
                    opt("Only the fiber attenuation"),
                    opt(
                        "The dispersion parameter D, the source linewidth Δλ, and the length L",
                        correct=True,
                    ),
                    opt("Only the receiver sensitivity"),
                    opt("The connector count alone"),
                ),
                "Chromatic broadening is Δt = D * L * Δλ: it grows with dispersion parameter, linewidth and length.",
            ),
            q(
                "How does polarization-mode dispersion (PMD) grow with fiber length?",
                (
                    opt("Linearly with L"),
                    opt("As the square root of L", correct=True),
                    opt("As L squared"),
                    opt("It does not depend on length"),
                ),
                "PMD accumulates as sqrt(L), unlike chromatic dispersion which grows linearly with L.",
            ),
        ),
        "The optical power & loss budget": (
            q(
                "Why are power-budget terms expressed in decibels?",
                (
                    opt("Because decibels make losses multiply"),
                    opt("Because in dB the losses simply add", correct=True),
                    opt("Because decibels remove the need for a margin"),
                    opt("Because launch power is always 0 dB"),
                ),
                "Working in dB turns multiplicative ratios into additions, so all losses simply sum.",
            ),
            q(
                "A link is feasible when the received power is what relative to the receiver sensitivity?",
                (
                    opt("Below the sensitivity"),
                    opt("Greater than or equal to the sensitivity", correct=True),
                    opt("Exactly zero"),
                    opt("Equal to the launch power"),
                ),
                "The link closes when received power stays at or above the receiver sensitivity (with margin).",
            ),
            q(
                "What is the purpose of the safety margin M in the power budget?",
                (
                    opt("To account for ageing, repairs and unforeseen losses", correct=True),
                    opt("To increase the bit rate"),
                    opt("To remove chromatic dispersion"),
                    opt("To define the laser wavelength"),
                ),
                "The margin (typically 3-6 dB) reserves headroom for ageing, repairs and uncertainties.",
            ),
        ),
        "Bit rate × distance product & limits": (
            q(
                "What are the two ceilings that cap a fiber link's reach?",
                (
                    opt("Voltage and current limits"),
                    opt(
                        "Loss-limited (power runs out) and dispersion-limited (pulses overlap)",
                        correct=True,
                    ),
                    opt("Connector count and splice count only"),
                    opt("Temperature and humidity"),
                ),
                "A link is bounded either by the power budget running out or by dispersion spreading pulses until they overlap.",
            ),
            q(
                "For chromatic-dispersion-limited links, how does maximum reach change if you double the bit rate?",
                (
                    opt("It doubles"),
                    opt("It stays the same"),
                    opt("It roughly halves (reach scales as 1/B)", correct=True),
                    opt("It quadruples"),
                ),
                "The bit-rate*distance product is roughly constant, so doubling B roughly halves the dispersion-limited reach.",
            ),
            q(
                "At a given bit rate, which limit determines the actual reach?",
                (
                    opt("Whichever curve gives the larger reach"),
                    opt(
                        "The lower of the loss-limited and dispersion-limited reaches", correct=True
                    ),
                    opt("Always the loss limit"),
                    opt("Always the dispersion limit"),
                ),
                "The actual reach is the smaller of the two limits at that bit rate.",
            ),
        ),
        "Intensity modulation & direct detection (IM-DD)": (
            q(
                "In IM-DD, what does the photodiode detect?",
                (
                    opt("The optical phase"),
                    opt("The optical power/intensity (it is a square-law device)", correct=True),
                    opt("The polarization state"),
                    opt("The exact wavelength"),
                ),
                "A photodiode is square-law: its current follows optical power, discarding the optical phase.",
            ),
            q(
                "What is a drawback of a directly modulated laser (DML) compared with an external modulator?",
                (
                    opt("It cannot send any data"),
                    opt(
                        "Modulating the current shifts the wavelength (chirp), worsening chromatic dispersion",
                        correct=True,
                    ),
                    opt("It requires a coherent receiver"),
                    opt("It has no threshold current"),
                ),
                "Swinging the drive current also shifts the laser wavelength (chirp), which aggravates chromatic dispersion.",
            ),
            q(
                "Because IM-DD discards phase, what kinds of formats can it use?",
                (
                    opt("Phase-shift keying like QPSK"),
                    opt("Intensity-only formats such as OOK and PAM4", correct=True),
                    opt("Polarization-multiplexed 16-QAM"),
                    opt("Any coherent constellation"),
                ),
                "Without phase, IM-DD is limited to intensity formats: on-off keying and multi-level PAM4.",
            ),
        ),
        "Noise & sensitivity: BER, Q-factor & the eye": (
            q(
                "What does the bit error ratio (BER) quantify?",
                (
                    opt("The fraction of bits decided incorrectly", correct=True),
                    opt("The launch power in dBm"),
                    opt("The number of WDM channels"),
                    opt("The splice loss per joint"),
                ),
                "BER is the fraction of bits received in error; typical pre-FEC targets are 1e-9 to 1e-12.",
            ),
            q(
                "How does the Q-factor relate to the signal levels and noise?",
                (
                    opt("It is the product of the 1 and 0 levels"),
                    opt(
                        "It is the separation of the 1 and 0 levels divided by the sum of their noise standard deviations",
                        correct=True,
                    ),
                    opt("It is the attenuation per kilometre"),
                    opt("It is the number of modes in the fiber"),
                ),
                "Q = (mu1 - mu0) / (sigma1 + sigma0): level separation measured in noise units.",
            ),
            q(
                "What does a tall, wide-open eye diagram indicate?",
                (
                    opt("A failing link with high BER"),
                    opt(
                        "Healthy margin; noise closes it vertically, jitter/dispersion horizontally",
                        correct=True,
                    ),
                    opt("That the fiber has been disconnected"),
                    opt("That the laser is below threshold"),
                ),
                "An open eye means good margin; vertical closure is noise, horizontal closure is jitter and dispersion.",
            ),
        ),
        "Connectors, splices & practical losses": (
            q(
                "Which joint type typically has the lowest insertion loss?",
                (
                    opt("Mated connector pair"),
                    opt("Mechanical splice"),
                    opt("Fusion splice", correct=True),
                    opt("Air-gap butt joint"),
                ),
                "Fusion splices melt the fibers together, giving the lowest loss (~0.02-0.1 dB).",
            ),
            q(
                "Why is angular/lateral core misalignment especially harmful in single-mode fiber?",
                (
                    opt(
                        "Because the core is very small (~9 µm), so small offsets lose a lot of light",
                        correct=True,
                    ),
                    opt("Because single-mode cores are the largest"),
                    opt("Because single-mode fiber has no cladding"),
                    opt("Because misalignment increases the bit rate"),
                ),
                "With a ~9 µm core, even small misalignments couple poorly and cause significant loss.",
            ),
            q(
                "Why are angled-polished (APC) connectors preferred where return loss matters?",
                (
                    opt("They eliminate fiber attenuation"),
                    opt(
                        "They reflect light into the cladding, greatly improving return loss",
                        correct=True,
                    ),
                    opt("They increase back-reflection toward the laser"),
                    opt("They remove the need for a power budget"),
                ),
                "APC end faces bounce reflections into the cladding, giving far better return loss than flat PC connectors.",
            ),
        ),
    },
    final=(
        q(
            "Which dispersion mechanism is eliminated by using single-mode fiber?",
            (
                opt("Chromatic dispersion"),
                opt("Modal dispersion", correct=True),
                opt("Polarization-mode dispersion"),
                opt("All dispersion"),
            ),
            "Single-mode fiber carries one mode, so modal dispersion is eliminated (CD and PMD remain).",
        ),
        q(
            "In a power budget, what does subtracting all losses and the margin from launch power give?",
            (
                opt("The bit rate"),
                opt(
                    "The received power, which must stay at or above receiver sensitivity",
                    correct=True,
                ),
                opt("The fiber's numerical aperture"),
                opt("The number of WDM channels"),
            ),
            "Received power = launch - fiber loss - connector/splice losses - margin, and must meet the sensitivity.",
        ),
        q(
            "The bit-rate*distance product captures which trade-off?",
            (
                opt("Higher bit rate allows proportionally longer reach"),
                opt(
                    "Higher bit rate forces shorter dispersion-limited reach (reach ~ 1/B)",
                    correct=True,
                ),
                opt("Reach is independent of bit rate"),
                opt("Reach grows with the square of bit rate"),
            ),
            "For dispersion-limited links the product is roughly fixed, so reach scales as 1/B.",
        ),
        q(
            "Why is IM-DD limited to intensity-only modulation formats?",
            (
                opt("Because the laser cannot be modulated"),
                opt(
                    "Because direct detection with a square-law photodiode discards optical phase",
                    correct=True,
                ),
                opt("Because fiber cannot carry phase information"),
                opt("Because the receiver has no amplifier"),
            ),
            "Direct detection measures power only, so phase-based formats are unavailable to IM-DD.",
        ),
        q(
            "Roughly what Q-factor corresponds to a BER of about 1e-9?",
            (
                opt("Q ≈ 2"),
                opt("Q ≈ 6", correct=True),
                opt("Q ≈ 12"),
                opt("Q ≈ 20"),
            ),
            "Q ≈ 6 gives BER ≈ 1e-9; Q ≈ 7 gives ≈ 1e-12.",
        ),
        q(
            "Which practical step most directly reduces back-reflection problems at connectors?",
            (
                opt("Using flat PC connectors everywhere"),
                opt("Using angled-polished APC connectors", correct=True),
                opt("Increasing the launch power"),
                opt("Adding more mechanical splices"),
            ),
            "APC connectors direct reflections into the cladding, improving return loss and laser stability.",
        ),
    ),
)
