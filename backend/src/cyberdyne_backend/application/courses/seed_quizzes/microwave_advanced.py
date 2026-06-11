from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Antenna arrays & beamforming: array factor, phased arrays & sidelobes": (
            q(
                "What happens to the main beam as you add more elements to a uniform array?",
                (
                    opt("The beam widens and sidelobes vanish"),
                    opt("The main beam narrows while sidelobes appear", correct=True),
                    opt("The pattern becomes omnidirectional"),
                    opt("Gain falls because power is split more ways"),
                ),
                "Adding elements narrows the main beam; sidelobes appear in the array factor.",
            ),
            q(
                "How does a phased array steer its beam with no moving parts?",
                (
                    opt("By physically rotating the elements"),
                    opt("By changing the operating frequency only"),
                    opt(
                        "By changing the progressive phase shift fed to each element",
                        correct=True,
                    ),
                    opt("By switching elements on and off in sequence"),
                ),
                "Changing the progressive phase beta aims the main beam electronically in microseconds.",
            ),
            q(
                "Why are array elements usually spaced about a half wavelength apart?",
                (
                    opt("To make the antenna physically smaller than a quarter wave"),
                    opt("To maximize aperture efficiency to 1.0"),
                    opt(
                        "Because spacing beyond lambda/2 produces grating lobes (false beam copies)",
                        correct=True,
                    ),
                    opt("Because tapering only works at exactly half-wave spacing"),
                ),
                "Spacing greater than lambda/2 creates grating lobes, so elements sit near a half wavelength.",
            ),
        ),
        "Aperture & specialized antennas: horn, patch & parabolic": (
            q(
                "According to the aperture gain law G = e_ap * 4 pi A / lambda^2, how does gain change?",
                (
                    opt("It falls as area and frequency rise"),
                    opt("It depends only on aperture efficiency"),
                    opt(
                        "It rises with aperture area and with frequency squared",
                        correct=True,
                    ),
                    opt("It is independent of wavelength"),
                ),
                "Gain grows with physical area and with frequency squared (inversely with lambda squared).",
            ),
            q(
                "What does the microstrip patch antenna trade away to be flat, cheap, and conformal?",
                (
                    opt("It gives up gain and bandwidth", correct=True),
                    opt("It gives up the ability to be printed"),
                    opt("It requires a parabolic reflector to work"),
                    opt("It can only operate below 1 GHz"),
                ),
                "A patch has modest gain (6-9 dBi) and narrow bandwidth, traded for being flat and printable.",
            ),
            q(
                "Which antenna is described as the gain champion, reaching 30-60 dBi?",
                (
                    opt("The microstrip patch"),
                    opt("The horn"),
                    opt("The parabolic dish", correct=True),
                    opt("The half-wave dipole"),
                ),
                "The parabolic dish collimates the feed into a pencil beam with very high gain (30-60 dBi).",
            ),
        ),
        "Microwave amplifiers & oscillators: gain, stability, noise figure & the LNA": (
            q(
                "What does the Rollet stability factor K > 1 (with |Delta| < 1) indicate?",
                (
                    opt("The amplifier has maximum transducer gain"),
                    opt("The amplifier is unconditionally stable", correct=True),
                    opt("The amplifier will always oscillate"),
                    opt("The amplifier has the lowest possible noise figure"),
                ),
                "K > 1 with |Delta| < 1 means no passive source or load can make the device oscillate.",
            ),
            q(
                "Per the Friis noise formula, why does the LNA come first in the chain?",
                (
                    opt("Because the last stage dominates the total noise figure"),
                    opt(
                        "Because the first stage dominates the noise figure, so it must have low F",
                        correct=True,
                    ),
                    opt("Because mixers add no noise and can go anywhere"),
                    opt("Because it must deliver the most output power"),
                ),
                "Friis shows the first stage dominates total noise figure, so a low-F LNA leads the chain.",
            ),
            q(
                "What condition makes an amplifier turn into an oscillator (the Barkhausen idea)?",
                (
                    opt("Output fed back out of phase with loop gain below 1"),
                    opt(
                        "Output fed back in phase through a selective network with loop gain >= 1",
                        correct=True,
                    ),
                    opt("A perfectly matched 50 ohm load on both ports"),
                    opt("A noise figure below 2 dB"),
                ),
                "In-phase feedback through a frequency-selective network with loop gain at least 1 sustains oscillation.",
            ),
        ),
        "The RF front-end & system: mixers, the receiver chain & intermodulation": (
            q(
                "In a superheterodyne receiver, what does the mixer accomplish?",
                (
                    opt("It rejects all out-of-band energy before the LNA"),
                    opt(
                        "It multiplies the RF by the LO, producing sum and difference frequencies",
                        correct=True,
                    ),
                    opt("It demodulates the signal directly to bits"),
                    opt("It sets the receiver noise floor"),
                ),
                "A mixer multiplies RF by the LO; a filter keeps the difference, the fixed IF.",
            ),
            q(
                "Why are third-order intermodulation products at 2f1 - f2 especially troublesome?",
                (
                    opt("They are far out of band and easily filtered"),
                    opt("They only appear at the noise floor"),
                    opt(
                        "They land in band and cannot be filtered out, rising 3x faster in dB",
                        correct=True,
                    ),
                    opt("They reduce the LO frequency"),
                ),
                "Third-order products fall in band and grow 3x faster (in dB), meeting the fundamental at IP3.",
            ),
            q(
                "What is the image frequency problem and how is it handled?",
                (
                    opt(
                        "A signal at the mirror of the LO lands on the IF; the preselect or image-reject mixer kills it",
                        correct=True,
                    ),
                    opt("The LO drifts; a VCO fixes it"),
                    opt("The IF filter is too wide; a wider filter fixes it"),
                    opt("Two tones create distortion; raising IP3 fixes it"),
                ),
                "A signal at the LO mirror also maps to the IF; the preselect filter or an image-reject mixer removes it.",
            ),
        ),
        "mmWave, 5G & radar: propagation, MIMO arrays & FMCW": (
            q(
                "Why does mmWave (roughly 30-300 GHz) lean heavily on phased arrays?",
                (
                    opt(
                        "Because path loss is high and beamforming recovers the link", correct=True
                    ),
                    opt("Because mmWave has very low path loss and needs no gain"),
                    opt("Because arrays lower the operating frequency"),
                    opt("Because single antennas cannot operate above 30 GHz"),
                ),
                "mmWave suffers high path loss, so high-gain phased-array beams are used to close the link.",
            ),
            q(
                "What does massive MIMO use many antennas to achieve?",
                (
                    opt("A single wider omnidirectional beam"),
                    opt(
                        "Parallel data streams over the same frequency, multiplying capacity",
                        correct=True,
                    ),
                    opt("Lower frequency operation"),
                    opt("Elimination of all atmospheric absorption"),
                ),
                "Massive MIMO sends parallel spatial streams over the same frequency, raising capacity.",
            ),
            q(
                "In FMCW radar, what is the beat frequency proportional to?",
                (
                    opt("The target's color"),
                    opt("The transmit power only"),
                    opt("The target range", correct=True),
                    opt("The LO phase noise"),
                ),
                "Mixing the delayed echo with the current chirp yields a beat frequency proportional to range.",
            ),
        ),
        "Lab: phased-array factor & beam steering": (
            q(
                "In the lab, how is the beam pointed at a chosen steer angle?",
                (
                    opt("By rotating the array physically"),
                    opt(
                        "By applying a progressive phase beta across the elements",
                        correct=True,
                    ),
                    opt("By increasing the number of elements N"),
                    opt("By changing matplotlib colors"),
                ),
                "The lab sets beta = -k*d_lam*sin(steer) so the array factor peaks at the steer angle.",
            ),
            q(
                "What does raising N from 8 to 16 do in the lab simulation?",
                (
                    opt("Widens the beam and lowers gain"),
                    opt("Narrows the beam, giving higher gain and finer steering", correct=True),
                    opt("Creates a grating lobe at broadside"),
                    opt("Has no effect on the pattern"),
                ),
                "More elements narrow the main beam, increasing gain and steering resolution.",
            ),
            q(
                "What does setting d_lam = 0.9 and steering 45 degrees produce?",
                (
                    opt("A grating lobe because spacing exceeds lambda/2", correct=True),
                    opt("A perfectly clean single beam"),
                    opt("Zero array factor everywhere"),
                    opt("A drop in the noise figure"),
                ),
                "Spacing greater than lambda/2 (0.9) at a steer angle produces a grating lobe.",
            ),
        ),
        "Applications & the throughline: from transmission line to mmWave system": (
            q(
                "In the 5G mmWave base-station case study, what recovers the harsh path loss?",
                (
                    opt("Lowering the frequency to below 1 GHz"),
                    opt("Phased-array beamforming steering narrow beams", correct=True),
                    opt("Removing the LNAs from the chain"),
                    opt("Using a single omnidirectional patch"),
                ),
                "Phased-array beamforming forms narrow high-gain beams that recover the mmWave path loss.",
            ),
            q(
                "In the satellite-link case study, what closes the link despite huge path loss?",
                (
                    opt(
                        "The Friis equation with high antenna gains and a low-noise LNB",
                        correct=True,
                    ),
                    opt("An FMCW chirp turned into range by an FFT"),
                    opt("Third-order intermodulation products"),
                    opt("Grating lobes from wide element spacing"),
                ),
                "A high-gain dish, a low-noise LNB, and the Friis budget with high gains close the satellite link.",
            ),
            q(
                "What are the four pillars the capstone says let you design any RF system?",
                (
                    opt("Mixers, oscillators, filters, and ADCs"),
                    opt(
                        "Transmission lines and matching, S-parameters, antennas, and the link budget",
                        correct=True,
                    ),
                    opt("MIMO, FMCW, mmWave, and 5G"),
                    opt("Horn, patch, dish, and dipole"),
                ),
                "The throughline names transmission lines and matching, S-parameters, antennas, and the link budget.",
            ),
        ),
    },
    final=(
        q(
            "Changing the progressive phase across array elements lets a phased array do what?",
            (
                opt("Increase the operating bandwidth"),
                opt("Steer the beam electronically with no moving parts", correct=True),
                opt("Lower the noise figure of the chain"),
                opt("Eliminate grating lobes regardless of spacing"),
            ),
            "A progressive phase shift steers the main beam electronically without moving parts.",
        ),
        q(
            "By the Friis noise formula, which stage dominates a receiver's overall noise figure?",
            (
                opt("The last IF stage"),
                opt("The mixer"),
                opt("The first stage, which is why the LNA goes first", correct=True),
                opt("The antenna feed"),
            ),
            "The first stage dominates total noise figure, so a low-F LNA leads the chain.",
        ),
        q(
            "Why do third-order intermodulation products limit a receiver's dynamic range?",
            (
                opt("They are far out of band and easily filtered"),
                opt(
                    "They fall in band, cannot be filtered, and rise 3x faster in dB until IP3",
                    correct=True,
                ),
                opt("They only appear above the IP3 point"),
                opt("They lower the antenna gain"),
            ),
            "In-band third-order products grow 3x faster in dB and meet the fundamental at the IP3 point.",
        ),
        q(
            "What pair of trade-offs defines mmWave operation around 30-300 GHz?",
            (
                opt("Low bandwidth but very long reach"),
                opt(
                    "Huge bandwidth and small antennas, but brutal path loss met with phased arrays",
                    correct=True,
                ),
                opt("No atmospheric absorption and omnidirectional coverage"),
                opt("Large antennas with low gain"),
            ),
            "mmWave offers huge bandwidth and tiny antennas but high path loss, recovered by phased-array beamforming.",
        ),
        q(
            "In FMCW radar, range is recovered from which quantity?",
            (
                opt("The transmit power"),
                opt("The beat frequency from mixing the echo with the current chirp", correct=True),
                opt("The LO phase noise"),
                opt("The aperture efficiency"),
            ),
            "Mixing the delayed echo with the current chirp gives a beat frequency proportional to range.",
        ),
    ),
)
