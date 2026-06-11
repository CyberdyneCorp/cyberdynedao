from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Optical fibers: modes and numerical aperture": (
            q(
                "In an optical fiber, what traps light inside the core?",
                (
                    opt("Diffraction off the cladding boundary"),
                    opt("Total internal reflection at the core-cladding interface", correct=True),
                    opt("Absorption by erbium ions"),
                    opt("Avalanche multiplication"),
                ),
                "The high-index core guides light by total internal reflection against the lower-index cladding.",
            ),
            q(
                "When the V-number is below 2.405, how many modes propagate?",
                (
                    opt("Zero modes"),
                    opt("Exactly one mode (single-mode fiber)", correct=True),
                    opt("Two modes"),
                    opt("Roughly V squared over two modes"),
                ),
                "For V < 2.405 only one mode propagates, giving single-mode fiber with a tiny ~9 um core.",
            ),
            q(
                "How is the numerical aperture (NA) of a fiber expressed?",
                (
                    opt("NA equals n_core times n_clad"),
                    opt(
                        "NA equals the square root of n_core squared minus n_clad squared",
                        correct=True,
                    ),
                    opt("NA equals 2 pi a over lambda"),
                    opt("NA equals the difference of the indices divided by lambda"),
                ),
                "NA = sqrt(n_core^2 - n_clad^2) = sin(theta_max), the light-gathering acceptance cone.",
            ),
        ),
        "Fiber loss and dispersion": (
            q(
                "Around which wavelength does modern silica fiber have its lowest loss (~0.2 dB/km)?",
                (
                    opt("980 nm"),
                    opt("1310 nm"),
                    opt("1550 nm", correct=True),
                    opt("850 nm"),
                ),
                "The best low-loss window is around 1550 nm at ~0.2 dB/km, which is why long-haul systems live there.",
            ),
            q(
                "Which dispersion type occurs only in multimode fiber and is killed by going single-mode?",
                (
                    opt("Modal dispersion", correct=True),
                    opt("Chromatic dispersion"),
                    opt("Material absorption"),
                    opt("Shot noise"),
                ),
                "Modal dispersion comes from different modes taking different path lengths; single-mode or graded-index removes it.",
            ),
            q(
                "A fiber rated at 500 MHz*km carries roughly what bandwidth over 2 km?",
                (
                    opt("500 MHz"),
                    opt("1000 MHz"),
                    opt("250 MHz", correct=True),
                    opt("125 MHz"),
                ),
                "The bandwidth-distance product is fixed: 500 MHz*km over 2 km gives about 250 MHz.",
            ),
        ),
        "Sources and detectors for communications": (
            q(
                "Why is a DFB laser preferred for long-haul DWDM links?",
                (
                    opt("It emits a broad ~50 nm spectrum"),
                    opt(
                        "It emits a single, ultra-pure wavelength via a built-in grating",
                        correct=True,
                    ),
                    opt("It has internal avalanche gain"),
                    opt("It is the cheapest source available"),
                ),
                "A DFB laser builds a grating in so it emits one ultra-pure wavelength, ideal for packing WDM channels and fighting dispersion.",
            ),
            q(
                "What distinguishes an APD from a PIN photodiode?",
                (
                    opt(
                        "The APD provides internal gain via avalanche multiplication", correct=True
                    ),
                    opt("The APD emits light instead of detecting it"),
                    opt("The PIN needs a very high reverse bias"),
                    opt("The PIN has lower noise only at high power"),
                ),
                "A high reverse bias makes each photo-electron trigger an avalanche, giving the APD internal gain (M of 10-100x).",
            ),
            q(
                "In the link budget, what is the margin?",
                (
                    opt("The launch power minus the fiber loss only"),
                    opt("The received power minus the receiver sensitivity", correct=True),
                    opt("The connector loss plus the splice loss"),
                    opt("The transmitter power minus the connector loss"),
                ),
                "Margin is P_rx minus the receiver sensitivity; keep a few dB spare for aging and repairs.",
            ),
        ),
        "Optical modulation and detection": (
            q(
                "What is the main drawback of direct modulation of a laser?",
                (
                    opt("It requires a separate Mach-Zehnder device"),
                    opt("It cannot represent a 1 bit"),
                    opt(
                        "Switching the drive current causes chirp that worsens dispersion",
                        correct=True,
                    ),
                    opt("It eliminates all shot noise"),
                ),
                "Turning a laser on/off fast smears its wavelength (chirp), worsening dispersion, so direct modulation suits shorter or slower links.",
            ),
            q(
                "In On-Off Keying (OOK), how does the detector photocurrent relate to optical power?",
                (
                    opt("I equals R times P, with R the responsivity", correct=True),
                    opt("I equals P squared"),
                    opt("I is independent of P"),
                    opt("I equals the square root of P"),
                ),
                "The photocurrent follows the optical power as I = R*P, where R is the detector responsivity.",
            ),
            q(
                "Which noise source scales with the square root of the photocurrent?",
                (
                    opt("Thermal (Johnson) noise"),
                    opt("Shot noise", correct=True),
                    opt("Modal dispersion"),
                    opt("Connector loss"),
                ),
                "Shot noise arises because light arrives as discrete photons; it scales with the square root of the current.",
            ),
        ),
        "Optical components: couplers, WDM, isolators and EDFAs": (
            q(
                "What does wavelength-division multiplexing (WDM) do?",
                (
                    opt(
                        "Sends many channels at different wavelengths down one fiber", correct=True
                    ),
                    opt("Splits one fiber into many homes equally"),
                    opt("Blocks reflections back into the laser"),
                    opt("Converts the optical signal to electricity"),
                ),
                "WDM sends independent channels at different wavelengths down a single fiber, multiplying its capacity.",
            ),
            q(
                "What is the function of an optical isolator?",
                (
                    opt("It amplifies all WDM channels at once"),
                    opt("It passes the forward beam and blocks back-reflections", correct=True),
                    opt("It splits one fiber into several"),
                    opt("It separates colors at the receiver"),
                ),
                "An isolator is a one-way valve for light, blocking reflections that would destabilize a laser.",
            ),
            q(
                "How does an EDFA amplify a signal?",
                (
                    opt("By converting light to electricity and back"),
                    opt(
                        "By pumping erbium-doped fiber so signal photons trigger stimulated emission",
                        correct=True,
                    ),
                    opt("By using avalanche multiplication in a photodiode"),
                    opt("By a 1:2 coupler that doubles the power"),
                ),
                "A 980 or 1480 nm pump creates a population inversion in erbium-doped fiber; signal photons trigger stimulated emission and are amplified optically.",
            ),
        ),
        "Lab: fiber pulse broadening and link budget": (
            q(
                "In Part A of the lab, how is the broadened pulse width computed?",
                (
                    opt("As t0 plus D times L times dlam"),
                    opt("As the square root of t0 squared plus spread squared", correct=True),
                    opt("As D times L times dlam alone"),
                    opt("As t0 times the distance"),
                ),
                "The lab uses width = sqrt(t0^2 + spread^2), where spread = D*L*dlam.",
            ),
            q(
                "In Part B, how does the lab compute the maximum reach distance?",
                (
                    opt("(Ptx - conn - sens) / alpha", correct=True),
                    opt("Ptx times alpha minus sens"),
                    opt("(Ptx + sens) / conn"),
                    opt("alpha times L plus conn"),
                ),
                "reach = (Ptx - conn - sens) / alpha is the distance where received power equals the sensitivity.",
            ),
            q(
                "Per the lab comments, what happens if you lower dlam to 0.01 nm (a DFB laser)?",
                (
                    opt("The link budget margin disappears"),
                    opt("Dispersion broadening nearly vanishes", correct=True),
                    opt("The fiber loss alpha doubles"),
                    opt("The maximum reach drops to zero"),
                ),
                "A narrow DFB linewidth (dlam = 0.01 nm) makes the chromatic-dispersion broadening nearly vanish.",
            ),
        ),
    },
    final=(
        q(
            "Which condition produces a single-mode fiber?",
            (
                opt("V-number above 10"),
                opt("V-number below 2.405", correct=True),
                opt("A 50-62.5 um core"),
                opt("A graded-index profile only"),
            ),
            "Single-mode propagation requires V < 2.405, achieved with a tiny ~9 um core.",
        ),
        q(
            "Why is the 1550 nm window combined with EDFAs key to transoceanic links?",
            (
                opt(
                    "1550 nm has the lowest loss and EDFAs amplify all WDM channels optically there",
                    correct=True,
                ),
                opt("1550 nm eliminates modal dispersion in multimode fiber"),
                opt("EDFAs convert the signal to electricity for regeneration"),
                opt("1550 nm needs no link budget"),
            ),
            "The ~0.2 dB/km loss at 1550 nm plus EDFA optical gain across that band let one fiber span oceans without electrical repeaters.",
        ),
        q(
            "An external Mach-Zehnder modulator is preferred over direct modulation because it",
            (
                opt("provides internal avalanche gain"),
                opt(
                    "keeps the laser running steadily with low chirp for long-haul high-speed",
                    correct=True,
                ),
                opt("removes the need for a detector"),
                opt("increases the source linewidth"),
            ),
            "External modulation keeps a clean narrow CW line and gates it separately, giving low chirp suited to long-haul high-speed links.",
        ),
        q(
            "For a link with Ptx = 0 dBm, alpha = 0.22 dB/km over 80 km, and 2 dB connector loss, what is the received power?",
            (
                opt("-17.6 dBm"),
                opt("-19.6 dBm", correct=True),
                opt("-2 dBm"),
                opt("-28 dBm"),
            ),
            "Prx = 0 - 0.22*80 - 2 = -19.6 dBm, comfortably above a -28 dBm sensitivity.",
        ),
        q(
            "Which pairing of detector and noise source is correct?",
            (
                opt("APD has internal gain; shot noise scales with sqrt of current", correct=True),
                opt("PIN has avalanche gain; thermal noise scales with sqrt of current"),
                opt("APD emits light; shot noise is from the load resistor"),
                opt("PIN provides 10-100x gain; chromatic dispersion adds noise"),
            ),
            "The APD provides internal avalanche gain, and shot noise (from discrete photon arrival) scales with the square root of the photocurrent.",
        ),
    ),
)
