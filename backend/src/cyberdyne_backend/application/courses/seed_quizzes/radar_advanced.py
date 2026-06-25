"""Curated quiz questions for the Radar & Remote Sensing - Advanced course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "MTI & pulse-Doppler processing": (
            q(
                "What does a single-delay MTI canceller y[n] = x[n] - x[n-1] do?",
                (
                    opt(
                        "Nulls echoes unchanged between pulses (clutter) while passing changing echoes",
                        correct=True,
                    ),
                    opt("Amplifies zero-Doppler clutter"),
                    opt("Increases the transmit power"),
                    opt("Measures the exact target range"),
                ),
                "Subtracting successive pulses cancels stationary clutter (unchanged) and passes moving-target returns (changing).",
            ),
            q(
                "What does pulse-Doppler processing add beyond simple MTI?",
                (
                    opt("It raises the carrier frequency"),
                    opt(
                        "An FFT across pulses sorts echoes into Doppler bins, measuring velocity while rejecting clutter",
                        correct=True,
                    ),
                    opt("It removes the need for an antenna"),
                    opt("It eliminates range resolution"),
                ),
                "Pulse-Doppler runs an FFT over a coherent burst per range cell, both rejecting clutter and measuring velocity.",
            ),
            q(
                "What are blind speeds, and how are they mitigated?",
                (
                    opt("Targets too slow to detect; raise transmit power"),
                    opt(
                        "Targets whose Doppler is a multiple of the PRF that alias onto the clutter notch; stagger the PRF",
                        correct=True,
                    ),
                    opt("Targets beyond the unambiguous range; lower the PRF"),
                    opt("Targets with low RCS; use a bigger antenna"),
                ),
                "Blind speeds occur when target Doppler is a multiple of the PRF and aliases into the clutter notch; PRF staggering avoids them.",
            ),
        ),
        "Synthetic aperture radar (SAR) & imaging": (
            q(
                "How does SAR achieve fine cross-range resolution?",
                (
                    opt("By using an extremely high transmit power"),
                    opt(
                        "By coherently combining echoes collected along the platform's track to synthesise a large aperture",
                        correct=True,
                    ),
                    opt("By lowering the PRF"),
                    opt("By increasing the radar cross-section"),
                ),
                "SAR moves the radar and coherently combines echoes over a long path, synthesising an aperture far larger than the real one.",
            ),
            q(
                "SAR azimuth resolution is approximately L/2. What does this imply?",
                (
                    opt("A longer real antenna gives finer resolution"),
                    opt(
                        "A shorter real antenna gives finer azimuth resolution, independent of range",
                        correct=True,
                    ),
                    opt("Resolution worsens linearly with range"),
                    opt("Resolution depends only on transmit power"),
                ),
                "Azimuth resolution ≈ L/2 means a shorter antenna (wider beam, longer synthetic aperture) resolves finer, regardless of range.",
            ),
            q(
                "What does interferometric SAR (InSAR) add over a single SAR image?",
                (
                    opt("Higher transmit power"),
                    opt(
                        "Terrain height and millimetre-scale ground deformation from two passes",
                        correct=True,
                    ),
                    opt("Removal of all clutter"),
                    opt("A narrower antenna beam"),
                ),
                "InSAR combines two passes to extract terrain elevation and measure ground deformation to the millimetre.",
            ),
        ),
        "Phased arrays & electronic beam steering": (
            q(
                "How does a phased array steer its beam without moving?",
                (
                    opt("By changing the transmit power per element"),
                    opt(
                        "By applying a progressive phase shift across the elements to tilt the wavefront",
                        correct=True,
                    ),
                    opt("By rotating each element mechanically"),
                    opt("By changing the carrier frequency only"),
                ),
                "A progressive inter-element phase shift tilts the combined wavefront, steering the beam electronically in microseconds.",
            ),
            q(
                "Why must phased-array element spacing stay near half a wavelength?",
                (
                    opt("To reduce the transmit power"),
                    opt("To avoid grating lobes, the spatial analogue of aliasing", correct=True),
                    opt("To increase thermal noise"),
                    opt("To widen the main beam at broadside"),
                ),
                "Spacing beyond about λ/2 produces grating lobes (spatial aliasing), so elements are kept near a half wavelength apart.",
            ),
            q(
                "What is scan loss in a phased array?",
                (
                    opt("Loss of data during the FFT"),
                    opt(
                        "Gain falls and the beam broadens as it steers off broadside, roughly as 1/cosθ",
                        correct=True,
                    ),
                    opt("Loss of phase coherence at the carrier"),
                    opt("Loss of all sidelobes"),
                ),
                "As the beam steers off broadside the projected aperture shrinks, so gain drops and the beam broadens (about 1/cosθ).",
            ),
        ),
        "Tracking: gates & an intro to the Kalman filter": (
            q(
                "What is the purpose of a range/Doppler gate in tracking?",
                (
                    opt("To increase the transmit power"),
                    opt(
                        "To accept only detections near a track's predicted position, easing data association",
                        correct=True,
                    ),
                    opt("To widen the antenna beam"),
                    opt("To remove thermal noise"),
                ),
                "A gate is an acceptance window around the prediction; only detections inside it are candidate updates, simplifying association.",
            ),
            q(
                "What are the two repeating steps of a Kalman filter?",
                (
                    opt("Transmit and receive"),
                    opt(
                        "Predict (propagate state) and update (blend with measurement)",
                        correct=True,
                    ),
                    opt("Amplify and threshold"),
                    opt("Steer and dwell"),
                ),
                "The Kalman filter alternates a predict step (motion model) and an update step (blend prediction with the new measurement).",
            ),
            q(
                "How does the Kalman gain weight the measurement versus the prediction?",
                (
                    opt("It always trusts the measurement fully"),
                    opt(
                        "A precise measurement gives a large gain (trust data); a noisy one gives a small gain (trust the model)",
                        correct=True,
                    ),
                    opt("It always trusts the model fully"),
                    opt("It ignores both and averages them equally"),
                ),
                "The gain reflects relative uncertainty: low-noise measurements get a large gain, noisy ones a small gain.",
            ),
        ),
        "Remote sensing & radar bands": (
            q(
                "What is the general trade-off between lower and higher radar bands?",
                (
                    opt(
                        "Lower bands penetrate weather/foliage but need large antennas; higher bands give fine resolution but suffer more attenuation",
                        correct=True,
                    ),
                    opt("Higher bands always penetrate better and need smaller antennas"),
                    opt("Lower bands give the finest resolution"),
                    opt("Band choice has no effect on antenna size"),
                ),
                "Long-wavelength bands penetrate and need big antennas with little bandwidth; short-wavelength bands are compact and wideband but attenuate more.",
            ),
            q(
                "Which application matches spaceborne SAR?",
                (
                    opt("Measuring battery voltage"),
                    opt(
                        "Mapping terrain, sea ice and crops day or night through cloud",
                        correct=True,
                    ),
                    opt("Generating the local oscillator"),
                    opt("Amplifying the receiver noise"),
                ),
                "Spaceborne SAR images terrain, ice, deforestation and crops independent of daylight and cloud cover.",
            ),
            q(
                "At what band do most modern automotive radars operate?",
                (
                    opt("HF, around 3 MHz"),
                    opt("W-band, around 77 GHz", correct=True),
                    opt("L-band, around 1 GHz"),
                    opt("S-band, around 3 GHz"),
                ),
                "Automotive radar operates around 77 GHz (W-band), enabling compact antennas, wide bandwidth and clean Doppler.",
            ),
        ),
        "System design example: detect a target at range R": (
            q(
                "Why is the design link budget computed in decibels?",
                (
                    opt("Because dB increases the transmit power"),
                    opt(
                        "Because the range equation's products and divisions become additions and subtractions",
                        correct=True,
                    ),
                    opt("Because dB removes clutter"),
                    opt("Because it is required by the Doppler effect"),
                ),
                "Working in dB turns the multiplicative range equation into an additive link budget that can be done on paper.",
            ),
            q(
                "Because detection SNR collapses as 1/R⁴, what are usually the cheapest levers to extend range?",
                (
                    opt("Raising raw transmit power as much as possible"),
                    opt("Pulse integration and lowering receiver noise", correct=True),
                    opt("Increasing the false-alarm rate"),
                    opt("Reducing the antenna gain"),
                ),
                "Because R⁴ makes power expensive, integration and noise reduction typically buy range more cheaply than raw power.",
            ),
            q(
                "When choosing the PRF for the design, what must it balance?",
                (
                    opt("Carrier phase and amplifier gain"),
                    opt(
                        "Unambiguous range (low enough to clear R) against velocity coverage (high enough)",
                        correct=True,
                    ),
                    opt("RCS and beamwidth"),
                    opt("Noise figure and aperture taper"),
                ),
                "PRF must be low enough that Rua = c/(2·PRF) clears the design range yet high enough for adequate velocity coverage (or staggered).",
            ),
        ),
    },
    final=(
        q(
            "How does pulse-Doppler processing both reject clutter and measure velocity?",
            (
                opt("By raising the transmit power"),
                opt(
                    "By running an FFT across a coherent burst of pulses to sort echoes into Doppler bins",
                    correct=True,
                ),
                opt("By narrowing the antenna beam"),
                opt("By lowering the carrier frequency"),
            ),
            "An FFT over the pulse burst sorts echoes into Doppler bins, rejecting zero-Doppler clutter while reading out velocity.",
        ),
        q(
            "SAR azimuth resolution of about L/2 means:",
            (
                opt(
                    "A shorter real antenna gives finer resolution, independent of range",
                    correct=True,
                ),
                opt("A longer real antenna gives finer resolution"),
                opt("Resolution depends only on transmit power"),
                opt("Resolution worsens with range like a real aperture"),
            ),
            "Because azimuth resolution is about L/2, a shorter antenna yields finer cross-range resolution regardless of range.",
        ),
        q(
            "A phased array steers its beam by:",
            (
                opt("Mechanically rotating the antenna"),
                opt(
                    "Applying a progressive phase shift across the elements to tilt the wavefront",
                    correct=True,
                ),
                opt("Changing only the transmit power"),
                opt("Switching the carrier off and on"),
            ),
            "Progressive inter-element phase shifts tilt the wavefront, steering the beam electronically without moving parts.",
        ),
        q(
            "In a Kalman-filter tracker, the Kalman gain decides:",
            (
                opt("The transmit pulse width"),
                opt(
                    "How much to trust the new measurement versus the model prediction, based on their uncertainties",
                    correct=True,
                ),
                opt("The antenna beamwidth"),
                opt("The pulse repetition frequency"),
            ),
            "The Kalman gain weights measurement against prediction by relative uncertainty: precise data gets a large gain.",
        ),
        q(
            "Which statement about radar band selection is correct?",
            (
                opt("Higher bands penetrate weather better and use larger antennas"),
                opt(
                    "Lower bands penetrate weather/foliage with large antennas; higher bands give fine resolution but more attenuation",
                    correct=True,
                ),
                opt("Band choice does not affect resolution or antenna size"),
                opt("All bands offer the same bandwidth"),
            ),
            "Long wavelengths penetrate and need big antennas; short wavelengths give compact, wideband, high-resolution systems that attenuate more.",
        ),
        q(
            "In the system design example, why is integration often preferred over raw power to reach the design range?",
            (
                opt("Because power has no effect on SNR"),
                opt(
                    "Because SNR falls as 1/R⁴, so integrating pulses (and lowering noise) buys range more cheaply than transmit power",
                    correct=True,
                ),
                opt("Because integration raises the false-alarm rate"),
                opt("Because integration narrows the antenna beam"),
            ),
            "The R⁴ fall-off makes raw power costly; coherent integration and reduced noise raise SNR far more economically.",
        ),
    ),
)
