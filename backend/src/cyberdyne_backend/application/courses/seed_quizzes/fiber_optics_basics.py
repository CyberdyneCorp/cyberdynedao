"""Curated quiz questions for the Optical Fiber Communications - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why optical fiber & the optical link": (
            q(
                "Which property of optical fiber gives it an enormous information capacity?",
                (
                    opt("Its high electrical conductivity"),
                    opt(
                        "The very high optical carrier frequency (~200 THz), so even a small fractional bandwidth is terabits per second",
                        correct=True,
                    ),
                    opt("Its sensitivity to electromagnetic interference"),
                    opt("The thickness of the cable"),
                ),
                "The optical carrier sits near 200 THz, so a tiny fractional bandwidth already gives terabit-per-second capacity.",
            ),
            q(
                "What are the three blocks every fiber link is built from?",
                (
                    opt("Modulator, filter, and demodulator only"),
                    opt("Transmitter, fiber, and receiver", correct=True),
                    opt("Antenna, waveguide, and mixer"),
                    opt("Splitter, amplifier, and switch"),
                ),
                "Every link is a transmitter (bits to light), the fiber (carries light), and a receiver (light back to bits).",
            ),
            q(
                "Which two impairments dominate the rest of the course?",
                (
                    opt("Reflection and refraction"),
                    opt("Polarization and diffraction"),
                    opt(
                        "Attenuation (signal weakens) and dispersion (pulses spread)", correct=True
                    ),
                    opt("Voltage drop and resistance"),
                ),
                "Fiber both attenuates the signal and disperses it; managing those two gives a working link.",
            ),
        ),
        "Light guidance & total internal reflection": (
            q(
                "What index relationship between core and cladding lets a fiber guide light?",
                (
                    opt("The core index must be lower than the cladding index"),
                    opt("The core index must equal the cladding index"),
                    opt(
                        "The core index must be slightly higher than the cladding index",
                        correct=True,
                    ),
                    opt("Neither region needs a defined index"),
                ),
                "Total internal reflection requires the core index n1 to be slightly higher than the cladding index n2.",
            ),
            q(
                "What does the numerical aperture (NA) describe?",
                (
                    opt("The total length of the fiber"),
                    opt("The light-gathering acceptance cone of the fiber", correct=True),
                    opt("The attenuation per kilometre"),
                    opt("The bit rate the fiber supports"),
                ),
                "NA = sqrt(n1^2 - n2^2) sets the acceptance cone, i.e. how much light the fiber can capture.",
            ),
            q(
                "Total internal reflection occurs when light hits the boundary at angles beyond which value?",
                (
                    opt("Brewster's angle"),
                    opt("The critical angle, where sin(theta_c) = n2/n1", correct=True),
                    opt("Ninety degrees from the surface"),
                    opt("The acceptance angle of the receiver"),
                ),
                "Beyond the critical angle theta_c (sin theta_c = n2/n1) light is totally internally reflected and trapped in the core.",
            ),
        ),
        "Single-mode vs multi-mode fiber": (
            q(
                "Below which V-number does a fiber support only a single mode?",
                (
                    opt("0.5"),
                    opt("1.0"),
                    opt("2.405", correct=True),
                    opt("10.0"),
                ),
                "When the V-number is below 2.405, only one mode propagates (single-mode fiber).",
            ),
            q(
                "Why does multi-mode fiber have shorter reach than single-mode fiber?",
                (
                    opt("It absorbs far more light per kilometre"),
                    opt(
                        "Its many modes travel at slightly different speeds, smearing the pulse (modal dispersion)",
                        correct=True,
                    ),
                    opt("It cannot be used with any laser source"),
                    opt("Its core is too small to launch power into"),
                ),
                "Multi-mode fiber's modes arrive at different times, causing modal dispersion that smears pulses and limits reach.",
            ),
            q(
                "Which fiber type is used for long-haul, metro and access links?",
                (
                    opt("Multi-mode fiber, because of its large core"),
                    opt("Single-mode fiber, because it has no modal dispersion", correct=True),
                    opt("Either, since reach does not depend on fiber type"),
                    opt("Plastic optical fiber only"),
                ),
                "Single-mode fiber carries one mode (no modal dispersion), so it is the choice for long-haul, metro and access.",
            ),
        ),
        "Attenuation & the transmission windows": (
            q(
                "In what units is fiber attenuation usually expressed, and how does power fall with distance?",
                (
                    opt("In volts, falling linearly with distance"),
                    opt("In dB/km, with power falling exponentially with distance", correct=True),
                    opt("In watts, staying constant with distance"),
                    opt("In hertz, rising with distance"),
                ),
                "Attenuation is in dB/km; in linear terms power falls exponentially, P(L) = P0 * 10^(-alpha*L/10).",
            ),
            q(
                "Which wavelength window has the minimum loss and is the backbone of long-haul systems?",
                (
                    opt("850 nm"),
                    opt("1310 nm"),
                    opt("1550 nm (the C-band)", correct=True),
                    opt("650 nm"),
                ),
                "The 1550 nm third window has minimum loss (~0.2 dB/km) and is where EDFAs work, making it the long-haul backbone.",
            ),
            q(
                "What is special about the 1310 nm window for standard fiber?",
                (
                    opt("It has the highest attenuation"),
                    opt("It is where chromatic dispersion is near zero", correct=True),
                    opt("It cannot be used with single-mode fiber"),
                    opt("It coincides with the water-absorption peak"),
                ),
                "Standard fiber has near-zero chromatic dispersion at 1310 nm, the second transmission window.",
            ),
        ),
        "The optical transmitter: LED vs laser diode": (
            q(
                "How does a laser diode's spectrum compare to an LED's?",
                (
                    opt("The laser is much broader and incoherent"),
                    opt("They are identical"),
                    opt(
                        "The laser is narrow and coherent; the LED is broad and incoherent",
                        correct=True,
                    ),
                    opt("The LED emits a single wavelength"),
                ),
                "Lasers emit a narrow, coherent spectrum (good for SMF and WDM); LEDs are broad and incoherent.",
            ),
            q(
                "What does the threshold current on a laser's L-I curve mark?",
                (
                    opt("The current at which the laser burns out"),
                    opt(
                        "The current below which the laser emits essentially no coherent light",
                        correct=True,
                    ),
                    opt("The maximum safe operating current"),
                    opt("The current at which dispersion is zero"),
                ),
                "Below the threshold current the laser stays dark; above it, output power rises steeply and nearly linearly.",
            ),
            q(
                "Why are laser diodes preferred over LEDs for high-speed and WDM links?",
                (
                    opt("They are cheaper and need no alignment"),
                    opt(
                        "Their narrow, directional, coherent output couples efficiently into single-mode fiber and supports fast modulation",
                        correct=True,
                    ),
                    opt("They emit in all directions, filling the fiber"),
                    opt("They have a broader spectrum, reducing dispersion"),
                ),
                "Lasers' narrow coherent beam couples well into SMF, allows fast modulation and single-wavelength operation for WDM.",
            ),
        ),
        "The optical receiver: PIN & APD photodiodes": (
            q(
                "What does the responsivity of a photodiode measure?",
                (
                    opt("The optical power it can emit"),
                    opt(
                        "The photocurrent produced per watt of incident optical power (A/W)",
                        correct=True,
                    ),
                    opt("The reverse breakdown voltage"),
                    opt("The bit error ratio"),
                ),
                "Responsivity R = I_ph / P_opt, in amps per watt, sets how much current a given optical power produces.",
            ),
            q(
                "What advantage does an APD have over a PIN photodiode?",
                (
                    opt("It has no internal gain, keeping it simple"),
                    opt(
                        "Internal avalanche gain that improves sensitivity when following electronics are noisy",
                        correct=True,
                    ),
                    opt("It is completely insensitive to temperature"),
                    opt("It emits light as well as detecting it"),
                ),
                "An APD multiplies carriers (gain M), improving sensitivity at the cost of excess noise and temperature sensitivity.",
            ),
            q(
                "What does the transimpedance amplifier (TIA) after the photodiode do?",
                (
                    opt("It converts the small photocurrent into a usable voltage", correct=True),
                    opt("It generates the optical local oscillator"),
                    opt("It splits the signal into multiple wavelengths"),
                    opt("It compensates chromatic dispersion optically"),
                ),
                "The TIA turns the tiny photocurrent into a voltage that the decision/clock-recovery circuit can use.",
            ),
        ),
    },
    final=(
        q(
            "Which combination of advantages explains why optical fiber displaced copper for long distances?",
            (
                opt("High conductivity, low cost, and small bandwidth"),
                opt(
                    "Enormous bandwidth, very low loss (~0.2 dB/km), and immunity to electromagnetic interference",
                    correct=True,
                ),
                opt("High loss but very cheap connectors"),
                opt("Strong susceptibility to crosstalk and large size"),
            ),
            "Fiber offers huge bandwidth, ~0.2 dB/km loss, and EMI immunity in a hair-thin medium.",
        ),
        q(
            "What physical principle traps light inside the fiber core?",
            (
                opt("Diffraction at the end face"),
                opt("Total internal reflection at the core-cladding boundary", correct=True),
                opt("Electrical conduction along the core"),
                opt("Magnetic confinement"),
            ),
            "Light beyond the critical angle is totally internally reflected at the core-cladding boundary and guided along the core.",
        ),
        q(
            "Compared with multi-mode fiber, single-mode fiber offers what?",
            (
                opt("A larger core and shorter reach"),
                opt("No modal dispersion and much longer reach", correct=True),
                opt("Higher attenuation per kilometre"),
                opt("Easier coupling but no laser requirement"),
            ),
            "Single-mode fiber carries one mode, eliminating modal dispersion and enabling long reach.",
        ),
        q(
            "At 1550 nm, what is notable about standard fiber attenuation?",
            (
                opt("It is at its maximum due to water absorption"),
                opt("It is at its minimum, around 0.2 dB/km", correct=True),
                opt("It is dominated by Rayleigh scattering at its worst"),
                opt("It is undefined"),
            ),
            "The 1550 nm window is the minimum-loss window at roughly 0.2 dB/km, the long-haul backbone.",
        ),
        q(
            "Which source is best matched to a high-speed single-mode WDM link?",
            (
                opt("A broad-spectrum LED"),
                opt("A narrow-linewidth DFB laser diode", correct=True),
                opt("An incandescent lamp"),
                opt("A multi-mode LED array"),
            ),
            "A narrow-linewidth DFB laser emits essentially one wavelength and couples efficiently into SMF, ideal for WDM.",
        ),
        q(
            "Which receiver component provides internal gain to improve sensitivity?",
            (
                opt("The PIN photodiode"),
                opt("The avalanche photodiode (APD)", correct=True),
                opt("The WDM multiplexer"),
                opt("The optical splitter"),
            ),
            "The APD multiplies carriers internally (gain M), improving sensitivity when the following electronics are noisy.",
        ),
    ),
)
