from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Advanced modulation and coherent optics": (
            q(
                "How many bits per symbol does 16-QAM carry?",
                (
                    opt("2 bits/symbol"),
                    opt("4 bits/symbol", correct=True),
                    opt("6 bits/symbol"),
                    opt("8 bits/symbol"),
                ),
                "16-QAM carries 4 bits/symbol; QPSK carries 2 and 64-QAM carries 6.",
            ),
            q(
                "What does a coherent receiver do that direct detection does not?",
                (
                    opt("It only measures optical power"),
                    opt(
                        "It mixes the incoming light with a local-oscillator laser to recover amplitude and phase",
                        correct=True,
                    ),
                    opt("It converts wavelengths optically without electronics"),
                    opt("It increases the number of polarizations to four"),
                ),
                "A coherent receiver beats the signal against a local-oscillator laser, recovering both I and Q.",
            ),
            q(
                "Which impairments does DSP compensate after the signal is digitized?",
                (
                    opt(
                        "Chromatic and polarization-mode dispersion plus laser phase noise",
                        correct=True,
                    ),
                    opt("Only thermal noise in the detector"),
                    opt("The bandgap of the source laser"),
                    opt("The fill factor of the fiber"),
                ),
                "DSP compensates chromatic and polarization-mode dispersion, tracks phase noise, and equalizes the channel.",
            ),
        ),
        "WDM and optical networking": (
            q(
                "Roughly how many wavelengths does DWDM pack onto one fiber on a standard grid?",
                (
                    opt("About 4 to 8"),
                    opt("About 40 to 96", correct=True),
                    opt("About 500 to 1000"),
                    opt("Exactly 2 (one per polarization)"),
                ),
                "DWDM packs roughly 40 to 96 wavelengths on a standard grid such as 50 GHz spacing around 1550 nm.",
            ),
            q(
                "What does a ROADM let a network node do under software control?",
                (
                    opt(
                        "Add, drop, or pass through individual wavelengths without converting to electrical signals",
                        correct=True,
                    ),
                    opt("Generate new laser wavelengths on demand"),
                    opt("Convert every wavelength to an electrical signal for routing"),
                    opt("Increase the fiber bandgap to add capacity"),
                ),
                "A ROADM adds, drops, or passes through wavelengths via wavelength-selective switches, staying in the optical domain.",
            ),
            q(
                "What happens to a channel's OSNR as it passes more amplified spans?",
                (
                    opt("It improves with each amplifier"),
                    opt("It degrades as it passes more amplifiers", correct=True),
                    opt("It stays constant regardless of span count"),
                    opt("It depends only on the polarization"),
                ),
                "OSNR degrades with accumulated noise as the channel passes more amplifiers, limiting reach before regeneration.",
            ),
        ),
        "Integrated photonics and silicon photonics": (
            q(
                "Why are lasers bonded on from III-V materials in silicon photonics?",
                (
                    opt("Silicon cannot emit light efficiently", correct=True),
                    opt("Silicon has too low a refractive index to guide light"),
                    opt("III-V materials are cheaper than silicon"),
                    opt("Silicon waveguides cannot be etched"),
                ),
                "Silicon cannot emit light efficiently, so lasers come from III-V materials while everything else integrates in silicon.",
            ),
            q(
                "What produces the sharp periodic notches in a ring resonator's bus transmission?",
                (
                    opt(
                        "Wavelengths whose round-trip equals a whole number of wavelengths build up resonance and are dropped",
                        correct=True,
                    ),
                    opt("The grating coupler reflecting light back"),
                    opt("Polarization multiplexing of two channels"),
                    opt("The diode saturation current of the loop"),
                ),
                "Resonant wavelengths (round-trip equal to a whole number of wavelengths) build up and are dropped, making periodic notches spaced by the FSR.",
            ),
            q(
                "How can a ring resonator act as a compact modulator or tunable filter?",
                (
                    opt(
                        "A heater or charge-injection junction shifts the ring's index, moving the resonance",
                        correct=True,
                    ),
                    opt("By physically rotating the ring"),
                    opt("By increasing the illumination on the chip"),
                    opt("By stacking different bandgaps in the ring"),
                ),
                "Tuning the ring's index with a heater or charge injection shifts the resonance, giving a low-power modulator or tunable filter.",
            ),
        ),
        "Solar cells and energy harvesting": (
            q(
                "In the solar-cell I-V equation, what does the term I_L represent?",
                (
                    opt("The light-generated current", correct=True),
                    opt("The diode saturation current"),
                    opt("The thermal voltage"),
                    opt("The open-circuit voltage"),
                ),
                "The I-V curve is a diode curve shifted down by the light-generated current I_L.",
            ),
            q(
                "Where on the I-V curve is the maximum power point located?",
                (
                    opt("At short circuit where V equals zero"),
                    opt("At open circuit where I equals zero"),
                    opt("Between the two ends, where power peaks", correct=True),
                    opt("Always at exactly half the open-circuit voltage"),
                ),
                "Power is zero at both ends (short circuit and open circuit) and peaks in between at the maximum power point.",
            ),
            q(
                "What caps a single-junction silicon cell near about 33 percent efficiency?",
                (
                    opt("The Shockley-Queisser limit", correct=True),
                    opt("The fill factor limit"),
                    opt("The free spectral range"),
                    opt("The Doppler limit"),
                ),
                "The Shockley-Queisser limit caps single-junction silicon near 33 percent because low-energy photons are unabsorbed and high-energy ones waste excess as heat.",
            ),
        ),
        "Emerging photonics: LiDAR, sensing and quantum": (
            q(
                "What does LiDAR measure to build a 3D point cloud?",
                (
                    opt("The times the echo of laser pulses takes to return", correct=True),
                    opt("The fill factor of a solar cell"),
                    opt("The free spectral range of a ring"),
                    opt("The OSNR of a DWDM channel"),
                ),
                "LiDAR fires laser pulses and times the echo, using d = c*dt/2 to build a 3D point cloud.",
            ),
            q(
                "What does FMCW LiDAR measure that time-of-flight LiDAR does not?",
                (
                    opt("Velocity via Doppler", correct=True),
                    opt("Bandgap energy"),
                    opt("Fill factor"),
                    opt("Coupling depth"),
                ),
                "FMCW LiDAR, borrowed from coherent optics, also measures velocity via Doppler.",
            ),
            q(
                "Why do single photons make excellent qubits in quantum photonics?",
                (
                    opt("They travel at light speed and barely decohere", correct=True),
                    opt("They have a very high refractive index"),
                    opt("They carry exactly 4 bits per symbol"),
                    opt("They absorb low-energy photons efficiently"),
                ),
                "Single photons travel at light speed and barely decohere, powering quantum key distribution and one approach to quantum computing.",
            ),
        ),
        "Lab: ring-resonator response and solar-cell IV curve": (
            q(
                "In the lab, what does raising the round-trip amplitude transmission a toward 1.0 do to the ring notches?",
                (
                    opt("Makes them sharper, raising the Q", correct=True),
                    opt("Makes them disappear entirely"),
                    opt("Doubles the solar cell power"),
                    opt("Shifts the open-circuit voltage"),
                ),
                "Raising a toward 1.0 (lower loss) makes the ring notches sharper, giving a higher Q.",
            ),
            q(
                "In the solar-cell part of the lab, how is the maximum power point found?",
                (
                    opt("By taking the index of the maximum of P = V*I", correct=True),
                    opt("By taking the minimum of the through-port transmission"),
                    opt("By taking the maximum of the round-trip phase"),
                    opt("By taking the average of I and V"),
                ),
                "The lab uses imp = np.argmax(P) on P = V*I to locate the maximum power point.",
            ),
            q(
                "In the lab, what happens to Voc when you double the light-generated current IL?",
                (
                    opt("Voc barely moves while the MPP power roughly doubles", correct=True),
                    opt("Voc roughly doubles as well"),
                    opt("Voc drops to zero"),
                    opt("Voc becomes negative"),
                ),
                "Doubling IL roughly doubles the MPP power, but Voc barely moves.",
            ),
        ),
        "Applications and the photonics throughline": (
            q(
                "In the photonic value chain, which stage uses MZM, ring, or coherent QAM?",
                (
                    opt("Modulate", correct=True),
                    opt("Generate"),
                    opt("Guide"),
                    opt("Detect"),
                ),
                "The modulate stage uses a Mach-Zehnder modulator, ring, or coherent QAM in the generate-guide-modulate-network-detect-use chain.",
            ),
            q(
                "Which photonics technology secures some banking and government links in the Security domain?",
                (
                    opt("Quantum key distribution", correct=True),
                    opt("DWDM with ROADMs"),
                    opt("Maximum power point tracking"),
                    opt("Silicon-photonic transceivers"),
                ),
                "Quantum key distribution provides the security domain's photonics, securing some banking and government links over fiber.",
            ),
            q(
                "Which physics relationships does the lesson say never change across applications?",
                (
                    opt(
                        "c = lambda f, E = hf, Snell, and gain above threshold",
                        correct=True,
                    ),
                    opt("Fill factor, OSNR, and free spectral range"),
                    opt("QPSK, 16-QAM, and 64-QAM only"),
                    opt("Only the Shockley-Queisser limit"),
                ),
                "The throughline notes the devices change but the physics (c = lambda f, E = hf, Snell, gain above threshold) never does.",
            ),
        ),
    },
    final=(
        q(
            "Polarization-multiplexed 16-QAM at 64 Gbaud reaches roughly what per-wavelength rate?",
            (
                opt("About 64 Gb/s"),
                opt("About 128 Gb/s"),
                opt("About 512 Gb/s", correct=True),
                opt("About 38 Tb/s"),
            ),
            "4 bits/symbol times 64 Gbaud times 2 polarizations is about 512 Gb/s per wavelength.",
        ),
        q(
            "Which combination forms the physical internet backbone described in the track?",
            (
                opt("DWDM plus ROADMs", correct=True),
                opt("Solar cells plus MPPT"),
                opt("LiDAR plus FMCW"),
                opt("Quantum key distribution plus spectroscopy"),
            ),
            "DWDM plus ROADMs are the physical internet backbone and cloud inter-data-center links.",
        ),
        q(
            "Why does silicon photonics confine light tightly into micron-scale waveguides?",
            (
                opt("Silicon's high refractive index (about 3.5)", correct=True),
                opt("Silicon's efficient light emission"),
                opt("The low coupling depth of rings"),
                opt("The high fill factor of CMOS"),
            ),
            "Silicon's high index (n about 3.5) confines light tightly, shrinking waveguides and devices to microns.",
        ),
        q(
            "A solar cell's fill factor describes which property of its I-V curve?",
            (
                opt("How square the curve is", correct=True),
                opt("How many wavelengths it absorbs"),
                opt("Its round-trip phase"),
                opt("Its OSNR after 20 spans"),
            ),
            "Fill factor FF = Vmp*Imp / (Voc*Isc) measures how square the I-V curve is.",
        ),
        q(
            "Which emerging-photonics application uses the relation d = c*dt/2?",
            (
                opt("LiDAR ranging", correct=True),
                opt("Photonic matrix multiplication"),
                opt("DWDM channel spacing"),
                opt("Maximum power point tracking"),
            ),
            "LiDAR times the echo of laser pulses and computes range as d = c*dt/2.",
        ),
    ),
)
