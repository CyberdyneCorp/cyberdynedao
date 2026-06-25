"""Curated quiz questions for the Radar & Remote Sensing - Intermediate course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The Doppler effect & moving targets": (
            q(
                "What is the round-trip Doppler shift for a radial velocity v at wavelength λ?",
                (
                    opt("fd = v/λ"),
                    opt("fd = 2v/λ", correct=True),
                    opt("fd = v/(2λ)"),
                    opt("fd = λ/v"),
                ),
                "The Doppler shift is 2v/λ; the factor of 2 comes from the two-way path.",
            ),
            q(
                "Why does the factor of 2 appear in the radar Doppler formula?",
                (
                    opt("Because two antennas are always used"),
                    opt(
                        "Because the moving target both receives a shifted wave and re-radiates a further-shifted one",
                        correct=True,
                    ),
                    opt("Because the radar transmits two pulses"),
                    opt("Because velocity is always measured twice"),
                ),
                "The target receives an already-shifted wave and re-radiates it shifted again, doubling the shift on the round trip.",
            ),
            q(
                "Where does stationary ground clutter appear in the Doppler spectrum?",
                (
                    opt("At the highest Doppler frequency"),
                    opt("At zero Doppler", correct=True),
                    opt("Spread evenly across all frequencies"),
                    opt("At the PRF frequency"),
                ),
                "Stationary clutter sits at zero Doppler, so a moving target can be separated from it by its nonzero shift.",
            ),
        ),
        "CW & FMCW radar": (
            q(
                "Why can a plain CW radar not measure range?",
                (
                    opt("Because it has no timing marker on its continuous tone", correct=True),
                    opt("Because its power is too low"),
                    opt("Because its antenna is too small"),
                    opt("Because it cannot detect Doppler"),
                ),
                "An unmodulated CW tone has no time reference, so there is no way to extract the round-trip delay.",
            ),
            q(
                "In FMCW radar, the beat frequency obtained by mixing transmit and echo is proportional to what?",
                (
                    opt("The target's RCS"),
                    opt("The target's range", correct=True),
                    opt("The antenna gain"),
                    opt("The transmit power"),
                ),
                "The delayed echo is offset from the transmit ramp by a beat frequency proportional to range: fb = (2B/cTc)·R.",
            ),
            q(
                "How does an FMCW radar separate range and velocity for a moving target?",
                (
                    opt("It cannot; only range is measurable"),
                    opt(
                        "It uses two or more chirps so the Doppler term can be separated from the range beat",
                        correct=True,
                    ),
                    opt("It increases transmit power"),
                    opt("It narrows the antenna beam"),
                ),
                "A moving target adds a Doppler term to the beat; multiple chirps (a fast/slow-time grid) separate range from velocity.",
            ),
        ),
        "Pulse compression & the matched filter": (
            q(
                "What does pulse compression achieve?",
                (
                    opt(
                        "The energy of a long pulse with the range resolution of a short one",
                        correct=True,
                    ),
                    opt("Higher transmit frequency"),
                    opt("A narrower antenna beam"),
                    opt("Elimination of all clutter"),
                ),
                "Transmitting a long chirp and matched-filtering it gives long-pulse energy and short-pulse (bandwidth-set) resolution.",
            ),
            q(
                "After pulse compression, what sets the range resolution?",
                (
                    opt("The pulse length tau"),
                    opt("The waveform bandwidth B, via ΔR = c/(2B)", correct=True),
                    opt("The PRF"),
                    opt("The antenna aperture"),
                ),
                "Compressed range resolution is c/(2B), determined by bandwidth rather than pulse length.",
            ),
            q(
                "Why is a transmitted chirp usually windowed (tapered) before the matched filter?",
                (
                    opt("To increase the transmitted energy"),
                    opt(
                        "To suppress range sidelobes that could mask a weak target near a strong one",
                        correct=True,
                    ),
                    opt("To shorten the pulse"),
                    opt("To raise the PRF"),
                ),
                "Windowing trades a slightly wider main lobe for much lower range sidelobes, preventing strong returns from masking weak ones.",
            ),
        ),
        "Range & velocity resolution": (
            q(
                "Range resolution depends on which waveform property?",
                (
                    opt("Pulse repetition frequency"),
                    opt("Bandwidth B, via ΔR = c/(2B)", correct=True),
                    opt("Carrier frequency only"),
                    opt("Transmit power"),
                ),
                "Range resolution is c/(2B); more bandwidth gives finer range cells.",
            ),
            q(
                "Velocity (Doppler) resolution depends on which quantity?",
                (
                    opt("The coherent dwell time Td, via Δv = λ/(2·Td)", correct=True),
                    opt("The bandwidth"),
                    opt("The radar cross-section"),
                    opt("The antenna sidelobe level"),
                ),
                "Doppler resolution is 1/Td, so velocity resolution Δv = λ/(2·Td) improves with longer coherent dwell.",
            ),
            q(
                "What general Fourier principle ties both resolutions together?",
                (
                    opt("Resolution equals the square of the observation extent"),
                    opt(
                        "Resolution is the reciprocal of the observation extent (frequency for range, time for velocity)",
                        correct=True,
                    ),
                    opt("Resolution is independent of observation extent"),
                    opt("Resolution grows linearly with transmit power"),
                ),
                "Resolution is the reciprocal of the observation extent: bandwidth for range, dwell time for velocity.",
            ),
        ),
        "Clutter, noise & the radar equation with losses": (
            q(
                "What does the loss factor L in the SNR equation collect?",
                (
                    opt("Only the target's RCS"),
                    opt(
                        "Atmospheric, hardware, beam-shape, integration and processing losses",
                        correct=True,
                    ),
                    opt("Only thermal noise"),
                    opt("The Doppler shift"),
                ),
                "L lumps together atmospheric attenuation, waveguide/radome, beam-shape, integration and processing losses.",
            ),
            q(
                "Why does raising transmit power not help a clutter-limited target?",
                (
                    opt("Because power has no effect on echoes"),
                    opt(
                        "Because more power lifts the target and the clutter together, leaving their ratio unchanged",
                        correct=True,
                    ),
                    opt("Because clutter scales as R⁴ and target as R²"),
                    opt("Because clutter is always at the carrier frequency"),
                ),
                "Power raises both target and clutter equally, so the signal-to-clutter ratio (not SNR) is unchanged.",
            ),
            q(
                "What is the main way radar discriminates a moving target from strong stationary clutter?",
                (
                    opt("Raising transmit power"),
                    opt(
                        "Doppler filtering, since stationary clutter sits at zero Doppler",
                        correct=True,
                    ),
                    opt("Lowering the antenna gain"),
                    opt("Increasing the pulse length"),
                ),
                "Doppler discrimination filters out the zero-Doppler clutter while passing the moving target's shifted echo.",
            ),
        ),
        "Detection theory: threshold, Pd/Pfa & CFAR": (
            q(
                "What does the probability of false alarm Pfa describe?",
                (
                    opt("A real target falling below the threshold"),
                    opt("Noise alone exceeding the detection threshold", correct=True),
                    opt("The probability the radar is switched off"),
                    opt("The Doppler shift of clutter"),
                ),
                "Pfa is the probability that noise by itself crosses the threshold and is mistaken for a target.",
            ),
            q(
                "What is the consequence of lowering the detection threshold?",
                (
                    opt("Both Pd and Pfa fall"),
                    opt("Pd rises but Pfa also rises (more false alarms)", correct=True),
                    opt("Pd falls and Pfa rises"),
                    opt("Neither Pd nor Pfa changes"),
                ),
                "A lower threshold catches more weak targets (higher Pd) but lets more noise through (higher Pfa).",
            ),
            q(
                "What does CFAR processing accomplish?",
                (
                    opt(
                        "It keeps the false-alarm rate constant as the background level varies",
                        correct=True,
                    ),
                    opt("It increases the transmit power adaptively"),
                    opt("It eliminates the need for a threshold"),
                    opt("It removes the Doppler shift"),
                ),
                "CFAR estimates the local background from reference cells and sets an adaptive threshold to hold Pfa constant.",
            ),
        ),
    },
    final=(
        q(
            "A target closing at radial velocity v produces a Doppler shift of:",
            (
                opt("v/λ"),
                opt("2v/λ", correct=True),
                opt("λ/(2v)"),
                opt("v·λ"),
            ),
            "The round-trip Doppler shift is 2v/λ, the factor of 2 coming from the two-way geometry.",
        ),
        q(
            "Why is FMCW used instead of plain CW radar?",
            (
                opt("FMCW transmits more power"),
                opt(
                    "Sweeping the frequency provides a timing marker so range can be measured from the beat frequency",
                    correct=True,
                ),
                opt("FMCW needs no antenna"),
                opt("FMCW eliminates Doppler"),
            ),
            "FMCW ramps the frequency, so the echo's delay produces a beat frequency proportional to range, which CW cannot provide.",
        ),
        q(
            "Pulse compression lets a radar simultaneously achieve:",
            (
                opt(
                    "Long-pulse energy and short-pulse (bandwidth-set) range resolution",
                    correct=True,
                ),
                opt("Higher carrier frequency and lower noise"),
                opt("A narrower beam and lower PRF"),
                opt("Zero clutter and infinite range"),
            ),
            "A long chirp carries energy while the matched filter compresses it to a resolution set by bandwidth (ΔR = c/2B).",
        ),
        q(
            "Which pairing of resolution to its governing quantity is correct?",
            (
                opt("Range ← dwell time; velocity ← bandwidth"),
                opt(
                    "Range ← bandwidth (ΔR = c/2B); velocity ← dwell time (Δv = λ/2Td)",
                    correct=True,
                ),
                opt("Both depend only on transmit power"),
                opt("Both depend only on the PRF"),
            ),
            "Range resolution comes from bandwidth and velocity resolution from coherent dwell time.",
        ),
        q(
            "At short range a target is often clutter-limited rather than noise-limited because:",
            (
                opt(
                    "Clutter usually grows more slowly with range than the target's R⁴ fall-off, so clutter dominates close in",
                    correct=True,
                ),
                opt("Thermal noise vanishes at short range"),
                opt("The target's RCS becomes negative"),
                opt("Doppler shift disappears at short range"),
            ),
            "Clutter scales as about R² (or less) while target SNR falls as R⁴, so near the radar clutter, not noise, limits detection.",
        ),
        q(
            "What problem does CFAR solve in the detection stage?",
            (
                opt("It boosts the transmit power"),
                opt(
                    "A fixed threshold gives a varying false-alarm rate when background level changes; CFAR adapts to hold Pfa constant",
                    correct=True,
                ),
                opt("It removes the matched filter"),
                opt("It widens the antenna beam"),
            ),
            "CFAR estimates the local noise/clutter from reference cells and adapts the threshold, keeping the false-alarm rate constant.",
        ),
    ),
)
