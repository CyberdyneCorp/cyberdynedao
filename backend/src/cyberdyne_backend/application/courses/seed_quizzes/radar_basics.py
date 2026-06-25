"""Curated quiz questions for the Radar & Remote Sensing - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What radar is & the radar block diagram": (
            q(
                "What does a monostatic radar's duplexer do?",
                (
                    opt("It generates the transmit waveform"),
                    opt(
                        "It switches the single shared antenna between transmit and receive",
                        correct=True,
                    ),
                    opt("It converts the echo from analog to digital"),
                    opt("It removes thermal noise from the receiver"),
                ),
                "The duplexer switches the one antenna between transmitting and receiving so it does both jobs.",
            ),
            q(
                "How is range obtained from the round-trip time delay tau?",
                (
                    opt("R = c·tau"),
                    opt("R = c·tau / 2", correct=True),
                    opt("R = 2·c·tau"),
                    opt("R = tau / c"),
                ),
                "Range is c·tau/2 because the wave travels out and back, covering twice the range.",
            ),
            q(
                "Why does a monostatic radar share a local oscillator between transmit and receive?",
                (
                    opt("To increase the transmitted power"),
                    opt(
                        "To provide a coherent phase reference needed to measure Doppler",
                        correct=True,
                    ),
                    opt("To widen the antenna beam"),
                    opt("To reduce the pulse duration"),
                ),
                "A shared local oscillator gives a coherent phase reference, which is what makes Doppler measurement possible.",
            ),
        ),
        "The radar range equation": (
            q(
                "How does received echo power vary with range in the radar range equation?",
                (
                    opt("It falls as 1/R"),
                    opt("It falls as 1/R²"),
                    opt("It falls as 1/R⁴", correct=True),
                    opt("It is independent of range"),
                ),
                "Received power falls as 1/R⁴ because the spreading loss is incurred on both the outbound and return trips.",
            ),
            q(
                "Roughly how much more transmit power is needed to double the detection range, all else equal?",
                (
                    opt("2 times"),
                    opt("4 times"),
                    opt("8 times"),
                    opt("16 times", correct=True),
                ),
                "Because power scales as R⁴, doubling range needs 2⁴ = 16 times the transmit power.",
            ),
            q(
                "In the maximum-range expression, what does P_r,min represent?",
                (
                    opt("The peak transmitted power"),
                    opt("The smallest echo power the receiver can detect", correct=True),
                    opt("The target's radar cross-section"),
                    opt("The antenna gain"),
                ),
                "P_r,min is the minimum detectable echo power, set by receiver noise, which fixes the maximum range.",
            ),
        ),
        "Pulse radar & range measurement": (
            q(
                "What sets a pulsed radar's maximum unambiguous range?",
                (
                    opt("The pulse duration tau"),
                    opt("The pulse repetition interval: Rua = c/(2·PRF)", correct=True),
                    opt("The antenna gain"),
                    opt("The target's RCS"),
                ),
                "Unambiguous range is c·T/2 = c/(2·PRF); echoes arriving after the next pulse alias to a false short range.",
            ),
            q(
                "What primarily determines a simple pulsed radar's range resolution?",
                (
                    opt("A longer pulse gives finer resolution"),
                    opt("A shorter pulse gives finer resolution, ΔR = c·tau/2", correct=True),
                    opt("Higher PRF gives finer resolution"),
                    opt("Larger RCS gives finer resolution"),
                ),
                "Shorter pulses (ΔR = c·tau/2) let two close echoes stay separate, giving finer range resolution.",
            ),
            q(
                "What is the trade-off in choosing a low PRF?",
                (
                    opt("Long unambiguous range but coarse velocity measurement", correct=True),
                    opt("Short unambiguous range and fine velocity measurement"),
                    opt("Both long range and fine velocity with no penalty"),
                    opt("Higher transmit power but lower resolution"),
                ),
                "Low PRF lengthens the unambiguous range but coarsens velocity measurement; high PRF does the reverse.",
            ),
        ),
        "Radar cross-section (RCS)": (
            q(
                "What does radar cross-section measure?",
                (
                    opt("The target's physical frontal area in square metres"),
                    opt("How much power the target scatters back toward the radar", correct=True),
                    opt("The target's mass"),
                    opt("The distance to the target"),
                ),
                "RCS measures backscattered power toward the radar, not physical size, and depends on geometry, material and aspect.",
            ),
            q(
                "Halving a target's RCS reduces detection range by roughly how much?",
                (
                    opt("About 50%"),
                    opt("About 25%"),
                    opt("About 16%", correct=True),
                    opt("Not at all"),
                ),
                "Range goes as the fourth root of RCS, so halving RCS cuts range by 2^(-1/4), about 16%.",
            ),
            q(
                "Why does a target's measured RCS fluctuate from pulse to pulse?",
                (
                    opt("Because the transmit power randomly changes"),
                    opt(
                        "Because aspect angle and interference of scattering centres change",
                        correct=True,
                    ),
                    opt("Because the speed of light varies"),
                    opt("Because the PRF drifts"),
                ),
                "Changing aspect angle and the interference of multiple scattering centres make RCS fluctuate (Swerling models).",
            ),
        ),
        "Antennas, beamwidth & angular resolution": (
            q(
                "How does the half-power beamwidth relate to aperture size D and wavelength?",
                (
                    opt("θ ≈ D/λ, so larger apertures widen the beam"),
                    opt("θ ≈ λ/D, so larger apertures narrow the beam", correct=True),
                    opt("θ ≈ λ·D"),
                    opt("Beamwidth is independent of aperture"),
                ),
                "Beamwidth is about λ/D, so a larger aperture produces a narrower, higher-gain beam.",
            ),
            q(
                "Why does a radar's cross-range resolution worsen at long range?",
                (
                    opt("Because the beamwidth grows with range"),
                    opt(
                        "Because the cross-range spread of the beam, R·θ, grows with range",
                        correct=True,
                    ),
                    opt("Because the wavelength increases with range"),
                    opt("Because RCS falls with range"),
                ),
                "Cross-range separation needed is about R·θ, which grows with range, so far targets are harder to resolve in angle.",
            ),
            q(
                "What problem do antenna sidelobes cause, and how is it mitigated?",
                (
                    opt("They narrow the main beam; widen it by tapering"),
                    opt(
                        "They let off-axis targets or clutter leak in; taper the aperture to lower them",
                        correct=True,
                    ),
                    opt("They increase transmit power; reduce it electronically"),
                    opt("They have no practical effect"),
                ),
                "Sidelobes admit off-axis clutter or targets; tapering the aperture illumination lowers them at the cost of a wider main beam.",
            ),
        ),
        "The decibel link & SNR view": (
            q(
                "Why do radar engineers work in decibels?",
                (
                    opt("Because decibels increase the transmit power"),
                    opt(
                        "Because they turn the range equation's products and divisions into additions and subtractions",
                        correct=True,
                    ),
                    opt("Because they remove thermal noise"),
                    opt("Because they are required by the speed of light"),
                ),
                "Decibels are logarithmic, turning the range equation's products and divisions into a sum/difference link budget.",
            ),
            q(
                "What does coherently integrating n pulses do to SNR?",
                (
                    opt("It leaves SNR unchanged"),
                    opt("It raises SNR by a factor of n (10·log10 n dB)", correct=True),
                    opt("It lowers SNR by a factor of n"),
                    opt("It raises SNR by a factor of n²"),
                ),
                "Coherent integration of n pulses raises SNR by a factor n, often cheaper than adding transmit power.",
            ),
            q(
                "Thermal noise power in the receiver is given by which expression?",
                (
                    opt("N = k·T_s·B", correct=True),
                    opt("N = P_t·G²"),
                    opt("N = c·tau/2"),
                    opt("N = λ/D"),
                ),
                "Receiver thermal noise power is N = k·T_s·B (Boltzmann's constant, system noise temperature, bandwidth).",
            ),
        ),
    },
    final=(
        q(
            "What three measurements does a radar derive from a single echo?",
            (
                opt("Range, angle and velocity", correct=True),
                opt("Mass, charge and temperature"),
                opt("Voltage, current and resistance"),
                opt("Frequency, phase and polarization only"),
            ),
            "One echo yields range (from delay), angle (from beam pointing) and velocity (from Doppler).",
        ),
        q(
            "Detection range grows only slowly with transmit power because received power scales as which power of range?",
            (
                opt("1/R"),
                opt("1/R²"),
                opt("1/R⁴", correct=True),
                opt("1/R⁸"),
            ),
            "The two-way spreading loss makes received power fall as 1/R⁴, so range rises only as the fourth root of power.",
        ),
        q(
            "A radar's maximum unambiguous range is determined by which quantity?",
            (
                opt("The pulse duration"),
                opt("The pulse repetition frequency, via Rua = c/(2·PRF)", correct=True),
                opt("The radar cross-section"),
                opt("The antenna gain"),
            ),
            "Unambiguous range is c/(2·PRF); echoes from beyond it arrive after the next pulse and alias to false ranges.",
        ),
        q(
            "Radar cross-section primarily describes what about a target?",
            (
                opt("Its physical size in square metres"),
                opt("How strongly it scatters power back toward the radar", correct=True),
                opt("Its closing velocity"),
                opt("Its range from the radar"),
            ),
            "RCS quantifies backscattered power toward the radar and depends on geometry, material and aspect, not just size.",
        ),
        q(
            "Antenna beamwidth is approximately λ/D. What does increasing the aperture D do?",
            (
                opt("Widens the beam and lowers gain"),
                opt("Narrows the beam and improves angular resolution", correct=True),
                opt("Leaves the beam unchanged"),
                opt("Increases the radar cross-section"),
            ),
            "A larger aperture gives a narrower, higher-gain beam and finer angular resolution (θ ≈ λ/D).",
        ),
        q(
            "Which quantity, not raw echo power, ultimately decides whether a target is detectable?",
            (
                opt("The signal-to-noise ratio relative to a detection threshold", correct=True),
                opt("The pulse repetition interval alone"),
                opt("The transmit frequency alone"),
                opt("The duplexer switching speed"),
            ),
            "Detection depends on SNR exceeding a threshold; noise (N = k·T_s·B), not raw power, sets the floor.",
        ),
    ),
)
