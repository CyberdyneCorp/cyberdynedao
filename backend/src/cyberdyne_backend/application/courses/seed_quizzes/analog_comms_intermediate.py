"""Curated quiz questions for the Analog Communications - Intermediate course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "SSB & VSB modulation": (
            q(
                "How much bandwidth does SSB occupy relative to a message of bandwidth B?",
                (
                    opt("2B, like DSB-SC"),
                    opt("B (the message bandwidth), since one sideband is dropped", correct=True),
                    opt("4B"),
                    opt("Half the carrier frequency"),
                ),
                "SSB transmits only one sideband, halving occupied bandwidth to the message bandwidth B.",
            ),
            q(
                "Why does SSB save bandwidth without losing information?",
                (
                    opt("Because the carrier carries the message"),
                    opt(
                        "Because the two DSB sidebands are mirror images, so one is redundant",
                        correct=True,
                    ),
                    opt("Because the noise cancels between sidebands"),
                    opt("Because SSB is a digital format"),
                ),
                "The two sidebands of DSB-SC are mirror images, so transmitting just one loses nothing.",
            ),
            q(
                "What problem does VSB solve compared with SSB?",
                (
                    opt("It removes the need for a carrier"),
                    opt(
                        "It avoids the impossible sharp filter when the message has energy near DC, by passing a vestige of the second sideband",
                        correct=True,
                    ),
                    opt("It halves the bandwidth again"),
                    opt("It eliminates all channel noise"),
                ),
                "VSB passes one full sideband plus a vestige of the other, making the filter realizable for near-DC content.",
            ),
        ),
        "Frequency modulation (FM) & Carson's rule": (
            q(
                "In FM, what does the message control?",
                (
                    opt("The carrier amplitude"),
                    opt("The instantaneous frequency of the carrier", correct=True),
                    opt("The carrier's bandwidth directly"),
                    opt("The number of sidebands only"),
                ),
                "In FM the instantaneous frequency deviates in proportion to the message; amplitude stays constant.",
            ),
            q(
                "What is Carson's rule for the bandwidth of an FM signal?",
                (
                    opt("B ≈ 2·fm only"),
                    opt("B ≈ 2·(Δf + fm) = 2·(β + 1)·fm", correct=True),
                    opt("B ≈ Δf / fm"),
                    opt("B ≈ fc + fm"),
                ),
                "Carson's rule estimates FM bandwidth as 2·(Δf + fm) = 2·(β + 1)·fm.",
            ),
            q(
                "Which property of the FM waveform stays constant?",
                (
                    opt("Its instantaneous frequency"),
                    opt("Its amplitude (envelope)", correct=True),
                    opt("Its phase"),
                    opt("Its bandwidth as β changes"),
                ),
                "FM has a constant envelope; information lives in the changing spacing of the zero crossings.",
            ),
        ),
        "Phase modulation (PM)": (
            q(
                "What is the relationship between FM and PM?",
                (
                    opt("They are unrelated modulation families"),
                    opt(
                        "FM is PM of the integral of the message; PM is FM of the derivative",
                        correct=True,
                    ),
                    opt("PM varies amplitude while FM varies phase"),
                    opt("PM is digital and FM is analog"),
                ),
                "FM and PM are both angle modulation; FM = PM of the integral of m, PM = FM of the derivative.",
            ),
            q(
                "What virtue do both FM and PM share?",
                (
                    opt("They occupy only B of bandwidth"),
                    opt(
                        "A constant envelope, so amplitude noise and amplifier nonlinearity barely matter",
                        correct=True,
                    ),
                    opt("They need no carrier"),
                    opt("They are immune to the threshold effect"),
                ),
                "Both are angle modulation with constant envelope, allowing efficient saturating amplifiers and amplitude-noise immunity.",
            ),
            q(
                "In PM, the instantaneous frequency is proportional to what?",
                (
                    opt("The message m(t) itself"),
                    opt("The integral of the message"),
                    opt("The derivative of the message m'(t)", correct=True),
                    opt("A constant"),
                ),
                "For PM the instantaneous frequency follows the derivative of the message, so it emphasizes fast changes.",
            ),
        ),
        "FM generation & detection": (
            q(
                "How does a VCO generate FM directly?",
                (
                    opt("By multiplying the message by the carrier"),
                    opt(
                        "Its output frequency is a linear function of input voltage, so feeding the message gives fi = fc + kf·m(t)",
                        correct=True,
                    ),
                    opt("By sampling the message at the Nyquist rate"),
                    opt("By filtering out one sideband"),
                ),
                "A VCO's frequency tracks its control voltage, so feeding the message produces FM by construction.",
            ),
            q(
                "Why does a frequency discriminator need a limiter before it?",
                (
                    opt("To increase the bandwidth"),
                    opt(
                        "To strip residual amplitude variation, since the discriminator converts amplitude changes too",
                        correct=True,
                    ),
                    opt("To add a carrier back"),
                    opt("To sample the signal"),
                ),
                "A discriminator converts frequency to amplitude, so a limiter must first remove any amplitude (noise) variation.",
            ),
            q(
                "In a PLL FM detector, which signal is the recovered message?",
                (
                    opt("The phase-detector output before filtering"),
                    opt("The VCO output frequency"),
                    opt(
                        "The loop-filter (control voltage) that keeps the VCO locked", correct=True
                    ),
                    opt("The incoming RF directly"),
                ),
                "The loop filter's control voltage that tracks the input frequency is exactly the demodulated message.",
            ),
        ),
        "The superheterodyne receiver": (
            q(
                "What is the central idea of a superheterodyne receiver?",
                (
                    opt("Demodulate every station at its RF frequency"),
                    opt(
                        "Shift every station down to one fixed intermediate frequency where filtering and gain are easy",
                        correct=True,
                    ),
                    opt("Use a tunable IF filter for each station"),
                    opt("Avoid using a local oscillator"),
                ),
                "The superhet converts every station to a fixed IF, so the high-gain, sharp filter never has to retune.",
            ),
            q(
                "How is the intermediate frequency produced?",
                (
                    opt("By amplifying the RF signal directly"),
                    opt(
                        "As the difference frequency from mixing the RF with the local oscillator",
                        correct=True,
                    ),
                    opt("By sampling at the Nyquist rate"),
                    opt("By the antenna preselector alone"),
                ),
                "Mixing RF with the LO gives sum and difference frequencies; the difference is the fixed IF.",
            ),
            q(
                "To tune a different station in a superhet, what is changed?",
                (
                    opt("The IF filter center frequency"),
                    opt(
                        "The local oscillator frequency, keeping the difference at the IF",
                        correct=True,
                    ),
                    opt("The audio amplifier gain"),
                    opt("The antenna length"),
                ),
                "Only the LO retunes so the RF–LO difference stays at the fixed IF; the IF stage never changes.",
            ),
        ),
        "Mixing, image frequency & IF": (
            q(
                "What is the image frequency in a superheterodyne receiver?",
                (
                    opt("The carrier frequency itself"),
                    opt(
                        "An unwanted frequency at fRF + 2·fIF that also produces the IF",
                        correct=True,
                    ),
                    opt("The audio output frequency"),
                    opt("Twice the local oscillator frequency"),
                ),
                "The image at fRF + 2·fIF mixes to the same IF as the wanted signal and falls into the IF passband.",
            ),
            q(
                "Which defence against the image must act before the mixer?",
                (
                    opt("The IF amplifier"),
                    opt("The RF preselector (front-end band-pass) filter", correct=True),
                    opt("The audio amplifier"),
                    opt("The de-emphasis filter"),
                ),
                "An RF preselector before the mixer passes the wanted signal and attenuates the image 2·fIF away.",
            ),
            q(
                "Why might a receiver choose a higher IF?",
                (
                    opt("To make the audio louder"),
                    opt(
                        "To push the image further from the wanted signal, easing image rejection",
                        correct=True,
                    ),
                    opt("To reduce the local oscillator frequency"),
                    opt("To eliminate the need for a preselector entirely"),
                ),
                "A higher IF moves the image further away, easing image rejection — but trades against adjacent-channel selectivity.",
            ),
        ),
    },
    final=(
        q(
            "Which scheme is the most spectrum- and power-efficient analog amplitude scheme?",
            (
                opt("Standard AM"),
                opt("DSB-SC"),
                opt("SSB", correct=True),
                opt("VSB"),
            ),
            "SSB sends only one sideband, occupying B and putting all power into information.",
        ),
        q(
            "FM and PM are collectively known as what?",
            (
                opt("Amplitude modulation"),
                opt("Angle modulation", correct=True),
                opt("Pulse modulation"),
                opt("Single-sideband modulation"),
            ),
            "FM and PM both vary the carrier's angle (phase/frequency), so they are angle modulation.",
        ),
        q(
            "What does Carson's rule estimate, and what does broadcast FM's wide bandwidth buy?",
            (
                opt("The carrier power; nothing useful"),
                opt(
                    "The FM bandwidth ≈ 2·(Δf + fm); the wide bandwidth buys a large SNR improvement",
                    correct=True,
                ),
                opt("The IF frequency; better image rejection"),
                opt("The modulation index; lower bandwidth"),
            ),
            "Carson's rule gives FM bandwidth ≈ 2·(Δf + fm); FM trades that bandwidth for an SNR gain.",
        ),
        q(
            "Which detector is the dominant modern FM demodulator?",
            (
                opt("The envelope detector"),
                opt("The coherent multiplier"),
                opt("The phase-locked loop (PLL)", correct=True),
                opt("The anti-alias filter"),
            ),
            "The PLL tracks the incoming phase; its control voltage is the demodulated message — robust and integrable.",
        ),
        q(
            "Why does the superheterodyne architecture use a fixed IF?",
            (
                opt("Because the antenna only works at the IF"),
                opt(
                    "So a sharp, high-gain filter and amplifier can stay fixed while only the LO retunes",
                    correct=True,
                ),
                opt("To avoid mixing entirely"),
                opt("Because the message has no bandwidth at RF"),
            ),
            "A fixed IF lets the expensive selective, high-gain stages stay put; only the LO retunes to pick a station.",
        ),
        q(
            "What trade-off governs the choice of IF frequency?",
            (
                opt("Carrier power versus bandwidth"),
                opt(
                    "Image rejection (favoured by a high IF) versus adjacent-channel selectivity (favoured by a low IF)",
                    correct=True,
                ),
                opt("Modulation index versus deviation"),
                opt("Sampling rate versus bit depth"),
            ),
            "A high IF eases image rejection; a low IF eases adjacent-channel selectivity — hence the IF is a balance.",
        ),
    ),
)
