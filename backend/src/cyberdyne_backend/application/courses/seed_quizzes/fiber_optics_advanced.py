"""Curated quiz questions for the Optical Fiber Communications - Advanced course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Wavelength-division multiplexing (WDM/DWDM)": (
            q(
                "What does WDM do on a single fiber?",
                (
                    opt("Sends one channel at the maximum possible power"),
                    opt(
                        "Carries many independent channels, each on a different wavelength",
                        correct=True,
                    ),
                    opt("Converts the optical signal to electrical at every span"),
                    opt("Splits one signal among many homes"),
                ),
                "WDM multiplexes several wavelengths onto one fiber, each carrying an independent channel.",
            ),
            q(
                "How does DWDM differ from CWDM?",
                (
                    opt("DWDM uses wide 20 nm spacing and no temperature control"),
                    opt(
                        "DWDM uses tight ITU-grid spacing (e.g. 50/100 GHz), packing dozens to 100+ channels",
                        correct=True,
                    ),
                    opt("DWDM carries only a single wavelength"),
                    opt("DWDM works only with multi-mode fiber"),
                ),
                "DWDM packs many closely spaced channels on the ITU grid; CWDM is coarse with wide 20 nm spacing.",
            ),
            q(
                "What does a ROADM do in a DWDM network?",
                (
                    opt("Amplifies all channels at once"),
                    opt(
                        "Routes individual wavelengths through a mesh without converting to electronics",
                        correct=True,
                    ),
                    opt("Generates the local oscillator for coherent receivers"),
                    opt("Splits one wavelength among many subscribers"),
                ),
                "A ROADM adds, drops and routes individual wavelengths optically, without electronic conversion.",
            ),
        ),
        "Optical amplifiers: EDFA & Raman": (
            q(
                "What key advantage do optical amplifiers have over electrical repeaters?",
                (
                    opt("They regenerate each channel digitally"),
                    opt(
                        "They amplify all WDM channels together in the optical domain", correct=True
                    ),
                    opt("They remove all noise from the signal"),
                    opt("They eliminate chromatic dispersion"),
                ),
                "An optical amplifier boosts every wavelength at once optically, unlike per-channel electrical repeaters.",
            ),
            q(
                "Why is the EDFA so well matched to DWDM long-haul systems?",
                (
                    opt(
                        "It amplifies across the C-band, exactly the DWDM band, with high gain",
                        correct=True,
                    ),
                    opt("It works only at 850 nm"),
                    opt("It adds no noise at all"),
                    opt("It converts wavelengths to a single channel"),
                ),
                "The EDFA provides high gain across the 1530-1565 nm C-band, the DWDM operating band.",
            ),
            q(
                "What does each EDFA add that degrades the chain's OSNR?",
                (
                    opt("Chromatic dispersion"),
                    opt("Amplified spontaneous emission (ASE) noise", correct=True),
                    opt("Modal dispersion"),
                    opt("Connector loss"),
                ),
                "Every EDFA injects ASE noise, so OSNR degrades step by step along the amplifier chain.",
            ),
        ),
        "Coherent optical communication & DSP": (
            q(
                "What does coherent detection recover that IM-DD discards?",
                (
                    opt("Only the optical power"),
                    opt(
                        "The full complex field: amplitude and phase on both polarizations",
                        correct=True,
                    ),
                    opt("Only the wavelength"),
                    opt("Only the bit rate"),
                ),
                "Mixing with a local oscillator recovers amplitude and phase on both polarizations.",
            ),
            q(
                "Because the coherent receiver has the full field, what can the DSP do?",
                (
                    opt("Eliminate fiber attenuation"),
                    opt(
                        "Equalize chromatic dispersion and PMD and recover carrier phase numerically",
                        correct=True,
                    ),
                    opt("Increase the launch power automatically"),
                    opt("Remove the need for any laser"),
                ),
                "DSP can undo CD and PMD and track laser phase noise, replacing optical dispersion compensation.",
            ),
            q(
                "Why does higher-order QAM (e.g. 64-QAM) require a higher OSNR?",
                (
                    opt("Because it uses more fiber"),
                    opt(
                        "Because its constellation points sit closer together, so noise flips them more easily",
                        correct=True,
                    ),
                    opt("Because it lowers the bit rate"),
                    opt("Because it removes polarization multiplexing"),
                ),
                "Packing more points crowds the constellation, so a higher OSNR is needed to keep them separable.",
            ),
        ),
        "Nonlinear effects: SPM, XPM & FWM": (
            q(
                "Fiber nonlinearity arises because the refractive index depends on what?",
                (
                    opt("Temperature only"),
                    opt("Optical intensity (the Kerr effect, n = n0 + n2*I)", correct=True),
                    opt("Fiber colour"),
                    opt("Connector type"),
                ),
                "The Kerr effect makes the index intensity-dependent, the root of SPM, XPM and FWM.",
            ),
            q(
                "Which nonlinear effect generates new tones that land on other channels as crosstalk?",
                (
                    opt("Self-phase modulation (SPM)"),
                    opt("Cross-phase modulation (XPM)"),
                    opt("Four-wave mixing (FWM)", correct=True),
                    opt("Rayleigh scattering"),
                ),
                "FWM mixes wavelengths to create new tones (fi + fj - fk) that interfere with other channels.",
            ),
            q(
                "Why is there an optimal launch power per channel rather than just turning the laser up?",
                (
                    opt("Because more power always improves performance"),
                    opt(
                        "Too little power means noise/OSNR dominates; too much triggers nonlinear penalties, so total penalty is U-shaped",
                        correct=True,
                    ),
                    opt("Because launch power has no effect on performance"),
                    opt("Because attenuation increases with power"),
                ),
                "Low power is noise-limited and high power is nonlinearity-limited, giving a U-shaped penalty with an optimum.",
            ),
        ),
        "Passive optical networks (PON) & FTTH access": (
            q(
                "What makes a PON 'passive'?",
                (
                    opt("It uses no fiber"),
                    opt(
                        "It splits the signal with a passive optical splitter that needs no power or electronics",
                        correct=True,
                    ),
                    opt("It carries no upstream traffic"),
                    opt("It uses only electrical repeaters"),
                ),
                "A passive splitter (no power, no electronics) fans one feeder fiber out to many subscribers.",
            ),
            q(
                "How do multiple ONTs share the upstream wavelength without colliding?",
                (
                    opt("Each broadcasts continuously"),
                    opt("By TDMA, with the OLT granting each ONT a time slot", correct=True),
                    opt("By using a different fiber each"),
                    opt("By coherent detection only"),
                ),
                "Upstream is shared by TDMA: the OLT schedules time slots so ONT bursts do not collide.",
            ),
            q(
                "Roughly how much loss does a 1:N optical splitter impose?",
                (
                    opt("Zero, since it is passive"),
                    opt("About 10*log10(N) dB", correct=True),
                    opt("Exactly N dB"),
                    opt("It adds gain, not loss"),
                ),
                "Splitting divides the light, costing about 10*log10(N) dB, which caps the split ratio and reach.",
            ),
        ),
        "System design: long-haul & datacenter examples": (
            q(
                "For a 1500 km long-haul DWDM link, which technology set is appropriate?",
                (
                    opt("MMF at 850 nm with IM-DD and no amplifiers"),
                    opt(
                        "C-band SMF with EDFAs every ~80 km plus coherent detection, DSP and FEC",
                        correct=True,
                    ),
                    opt("Plastic fiber with LEDs"),
                    opt("A single unamplified span"),
                ),
                "Long-haul uses C-band SMF, periodic EDFAs, and coherent/DSP/FEC to close both OSNR and dispersion budgets.",
            ),
            q(
                "What dominates the design of a short datacenter interconnect?",
                (
                    opt("Maximizing reach with coherent optics"),
                    opt("Cost and power per bit, favouring cheap IM-DD with PAM4", correct=True),
                    opt("Chromatic dispersion compensation"),
                    opt("Raman amplification"),
                ),
                "Over hundreds of metres to a few km, dispersion is negligible; cost and power per bit drive IM-DD/PAM4 choices.",
            ),
            q(
                "What is the common discipline behind both design examples?",
                (
                    opt("Always use the most expensive components"),
                    opt(
                        "List every gain and loss, confirm the worst case still has margin, then pick the cheapest technology that closes both budgets",
                        correct=True,
                    ),
                    opt("Ignore the power budget for short links"),
                    opt("Use coherent detection everywhere"),
                ),
                "Both regimes sum gains and losses, verify worst-case margin, and choose the lowest-cost technology that closes the budgets.",
            ),
        ),
    },
    final=(
        q(
            "What is the primary benefit of DWDM on a single fiber?",
            (
                opt("Lower attenuation per kilometre"),
                opt(
                    "Multiplying capacity by carrying dozens to 100+ wavelength channels",
                    correct=True,
                ),
                opt("Eliminating the need for any receiver"),
                opt("Removing all dispersion"),
            ),
            "DWDM packs many closely spaced channels onto one fiber, scaling capacity into the tens of Tb/s.",
        ),
        q(
            "Why did the EDFA revolutionise long-haul transmission?",
            (
                opt("It detects and retimes each channel electrically"),
                opt(
                    "It amplifies all C-band DWDM channels together in the optical domain",
                    correct=True,
                ),
                opt("It removes ASE noise from the link"),
                opt("It works only with multi-mode fiber"),
            ),
            "The EDFA boosts every C-band wavelength at once optically, replacing per-channel electrical repeaters.",
        ),
        q(
            "What capability does coherent detection plus DSP add over IM-DD?",
            (
                opt("It lowers the laser cost to near zero"),
                opt(
                    "It recovers amplitude and phase (enabling QAM) and equalizes dispersion/PMD in software",
                    correct=True,
                ),
                opt("It removes the need for optical amplifiers"),
                opt("It eliminates fiber nonlinearity"),
            ),
            "Coherent + DSP recovers the full field for high-order QAM and undoes CD/PMD numerically.",
        ),
        q(
            "Which statement about launch power and nonlinearity is correct?",
            (
                opt("Higher launch power always improves OSNR with no penalty"),
                opt(
                    "There is an optimum: too little power is noise-limited, too much triggers nonlinear penalties",
                    correct=True,
                ),
                opt("Nonlinearity only matters in multi-mode fiber"),
                opt("Launch power has no effect on a DWDM line"),
            ),
            "Total penalty is U-shaped; nonlinearity sets an upper bound on usable launch power.",
        ),
        q(
            "In a PON, how is downstream traffic delivered to the ONTs?",
            (
                opt("Each ONT gets a dedicated fiber"),
                opt(
                    "The OLT broadcasts to all ONTs, which select their own (encrypted) packets",
                    correct=True,
                ),
                opt("Upstream TDMA is used for downstream too"),
                opt("Coherent detection separates the homes"),
            ),
            "Downstream is a broadcast on one wavelength; each ONT filters out its own encrypted packets.",
        ),
        q(
            "What single discipline closes both long-haul and datacenter link designs?",
            (
                opt("Maximizing bit rate regardless of cost"),
                opt(
                    "Summing all gains and losses, ensuring worst-case margin, and choosing the cheapest technology that closes the budgets",
                    correct=True,
                ),
                opt("Always adding more amplifiers"),
                opt("Ignoring receiver sensitivity"),
            ),
            "Both designs reduce to closing the power and dispersion/OSNR budgets with margin at lowest cost.",
        ),
    ),
)
