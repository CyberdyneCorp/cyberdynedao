"""Curated quiz questions for the Wireless & Mobile Communications - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The wireless channel & spectrum": (
            q(
                "How does wavelength relate to carrier frequency?",
                (
                    opt("Wavelength equals frequency divided by the speed of light"),
                    opt(
                        "Wavelength equals the speed of light divided by the frequency",
                        correct=True,
                    ),
                    opt("Wavelength equals frequency times the speed of light"),
                    opt("Wavelength is independent of frequency"),
                ),
                "Wavelength = c / f, so higher frequencies have shorter wavelengths.",
            ),
            q(
                "What is the main trade-off of using high (mmWave) frequency bands?",
                (
                    opt("They travel very far but carry little data"),
                    opt(
                        "They offer huge bandwidth and high data rates but have short range and are blocked by walls",
                        correct=True,
                    ),
                    opt("They penetrate walls best of all bands"),
                    opt("They have unlimited range with low bandwidth"),
                ),
                "High bands give large bandwidth (fast data) but short range and poor wall penetration.",
            ),
            q(
                "Why is the radio spectrum described as the scarce resource?",
                (
                    opt("Because radios are expensive to build"),
                    opt(
                        "Because frequencies are limited and must be split into licensed or unlicensed bands shared by many users",
                        correct=True,
                    ),
                    opt("Because electromagnetic waves do not exist above 100 GHz"),
                    opt("Because only one device can transmit on Earth at a time"),
                ),
                "Spectrum is finite, divided into bands, and shared among many users, making it the scarce resource.",
            ),
        ),
        "Radio propagation & path loss": (
            q(
                "In free space, how does received power change when distance doubles?",
                (
                    opt("It halves (drops by 3 dB)"),
                    opt("It falls to one quarter (drops by 6 dB)", correct=True),
                    opt("It stays the same"),
                    opt("It falls to one eighth (drops by 9 dB)"),
                ),
                "Free-space power falls with the square of distance, so doubling distance gives a quarter of the power (-6 dB).",
            ),
            q(
                "What does a larger path-loss exponent n indicate?",
                (
                    opt("Power falls more slowly with distance"),
                    opt(
                        "Power falls more steeply with distance, as in dense urban areas",
                        correct=True,
                    ),
                    opt("The carrier frequency is lower"),
                    opt("There is no path loss at all"),
                ),
                "Power falls as d to the power -n, so a larger n means a steeper drop, typical of urban/indoor settings.",
            ),
            q(
                "Why do engineers express path loss in decibels?",
                (
                    opt("Because decibels make the numbers larger and more impressive"),
                    opt(
                        "Because the values span huge ranges and dB turns multiplication of gains and losses into addition",
                        correct=True,
                    ),
                    opt("Because decibels remove the dependence on frequency"),
                    opt("Because power cannot be measured in watts wirelessly"),
                ),
                "Decibels compress huge dynamic ranges and let gains and losses be added rather than multiplied.",
            ),
        ),
        "The cellular concept": (
            q(
                "What is a frequency-reuse cluster?",
                (
                    opt("A single cell that uses every available frequency"),
                    opt(
                        "A group of cells that together use all the channels once, after which the frequencies are reused",
                        correct=True,
                    ),
                    opt("The set of all base stations in a country"),
                    opt("A cell that never reuses any frequency"),
                ),
                "A cluster is a group of cells using all channels once; spectrum is reused every cluster.",
            ),
            q(
                "Why do dense cities use very small cells?",
                (
                    opt("Small cells need no base stations"),
                    opt("Smaller cells reduce path loss to zero"),
                    opt(
                        "More reuse of the spectrum across many small cells gives more total capacity",
                        correct=True,
                    ),
                    opt("Small cells eliminate handover entirely"),
                ),
                "Smaller cells let the same spectrum be reused more often, multiplying total capacity.",
            ),
            q(
                "What is a handover (handoff)?",
                (
                    opt("Permanently dropping a call when signal weakens"),
                    opt(
                        "Transferring an active call to a new base station before the old link dies as the user moves",
                        correct=True,
                    ),
                    opt("Splitting one cell into a cluster"),
                    opt("Assigning a frequency to a new subscriber"),
                ),
                "Handover transfers an active call to a stronger base station as the user moves between cells.",
            ),
        ),
        "Link budget & receiver sensitivity": (
            q(
                "What does a link budget compute?",
                (
                    opt("The monetary cost of a cellular subscription"),
                    opt(
                        "The sum of all gains and losses between transmitter and receiver to check the signal arrives strong enough",
                        correct=True,
                    ),
                    opt("The number of users a cell can hold"),
                    opt("The wavelength of the carrier"),
                ),
                "A link budget adds gains and subtracts losses to confirm the received power clears the sensitivity threshold.",
            ),
            q(
                "What determines a receiver's sensitivity floor?",
                (
                    opt("The transmitter power alone"),
                    opt("The carrier wavelength alone"),
                    opt(
                        "Noise: the floor is set by kTB plus the receiver's noise figure",
                        correct=True,
                    ),
                    opt("The number of cells in the cluster"),
                ),
                "Sensitivity is limited by the noise floor N = kTB + noise figure.",
            ),
            q(
                "According to Shannon, how does capacity grow as SNR increases?",
                (
                    opt("Linearly without limit"),
                    opt("It decreases with SNR"),
                    opt("Only logarithmically, so each extra dB buys less", correct=True),
                    opt("It is independent of SNR"),
                ),
                "Shannon capacity is log2(1 + SNR), so it grows only logarithmically with SNR.",
            ),
        ),
        "From 1G to 5G: the cellular generations": (
            q(
                "What was the defining change from 1G to 2G?",
                (
                    opt("A move from digital to analog voice"),
                    opt(
                        "A move from analog voice to digital voice, enabling encryption, error correction and SMS",
                        correct=True,
                    ),
                    opt("The introduction of mmWave bands"),
                    opt("The removal of all data services"),
                ),
                "2G digitised voice, which brought encryption, error correction, SMS and a small data pipe.",
            ),
            q(
                "Which generation is characterised as all-IP broadband using OFDMA and MIMO?",
                (
                    opt("1G"),
                    opt("2G"),
                    opt("4G / LTE", correct=True),
                    opt("0G"),
                ),
                "4G/LTE is the all-IP broadband generation built on OFDMA and MIMO, with voice as data (VoLTE).",
            ),
            q(
                "What is the deeper pattern across the generations?",
                (
                    opt("A move from digital bits back toward analog waveforms"),
                    opt(
                        "A move from analog (the waveform is the message) to digital (bits protected by coding and recoverable from noise)",
                        correct=True,
                    ),
                    opt("A reduction in data rates over time"),
                    opt("Abandoning cells in favour of a single transmitter"),
                ),
                "The throughline is analog-to-digital: messages became bits protected by coding and recoverable from a noisy waveform.",
            ),
        ),
        "Multiple access: FDMA, TDMA, CDMA, OFDMA": (
            q(
                "Which resource does TDMA divide among users?",
                (
                    opt("Frequency"),
                    opt("Time slots", correct=True),
                    opt("Spreading codes"),
                    opt("Antennas"),
                ),
                "TDMA gives users turns in time slots on a shared frequency.",
            ),
            q(
                "How does CDMA separate users?",
                (
                    opt("By giving each a different frequency"),
                    opt("By giving each a different time slot"),
                    opt(
                        "By orthogonal spreading codes, while all share the same frequency and time",
                        correct=True,
                    ),
                    opt("By assigning each a different antenna"),
                ),
                "CDMA lets everyone transmit at once on the same frequency, separated by orthogonal spreading codes.",
            ),
            q(
                "Why is OFDMA the modern multiple-access winner?",
                (
                    opt("It divides only by frequency like FDMA"),
                    opt(
                        "It assigns blocks of narrow subcarriers in both frequency and time, giving flexible, spectrally efficient scheduling",
                        correct=True,
                    ),
                    opt("It requires no scheduling at all"),
                    opt("It uses a single wide carrier per user"),
                ),
                "OFDMA splits the band into many subcarriers and schedules them per user in frequency and time, the flexible modern choice.",
            ),
        ),
    },
    final=(
        q(
            "A 2.4 GHz signal and a 600 MHz signal differ in wavelength because...",
            (
                opt("wavelength rises with frequency, so 2.4 GHz has the longer wavelength"),
                opt(
                    "wavelength is c/f, so the higher-frequency 2.4 GHz signal has the shorter wavelength",
                    correct=True,
                ),
                opt("wavelength does not depend on frequency"),
                opt("both have exactly the same wavelength"),
            ),
            "Since wavelength = c/f, the higher 2.4 GHz frequency has the shorter wavelength.",
        ),
        q(
            "In a dense urban area the path-loss exponent is about 3 to 4 rather than 2. This means...",
            (
                opt("power falls more slowly than in free space"),
                opt("power falls more steeply than the free-space square law", correct=True),
                opt("there is no path loss"),
                opt("the signal gains power with distance"),
            ),
            "A higher exponent (3-4) means power falls faster than the free-space square law (n = 2).",
        ),
        q(
            "Why does splitting coverage into many small cells increase total capacity?",
            (
                opt("Because each small cell needs less power and so carries more data"),
                opt(
                    "Because the spectrum can be reused in more cells that are far enough apart not to interfere",
                    correct=True,
                ),
                opt("Because small cells remove the need for a link budget"),
                opt("Because handover is no longer required"),
            ),
            "More small cells means the spectrum is reused more times across non-interfering cells, multiplying capacity.",
        ),
        q(
            "If received power is -69 dBm and the noise floor is -94 dBm, the SNR is...",
            (
                opt("-163 dB"),
                opt("25 dB", correct=True),
                opt("163 dB"),
                opt("-25 dB"),
            ),
            "SNR in dB is received power minus noise floor: -69 - (-94) = 25 dB.",
        ),
        q(
            "Which statement correctly orders the generations by their hallmark?",
            (
                opt("1G all-IP broadband, 4G analog voice, 5G digital voice"),
                opt(
                    "1G analog voice, 2G digital voice, 3G mobile data, 4G all-IP broadband, 5G mmWave/massive MIMO",
                    correct=True,
                ),
                opt("2G mmWave, 3G analog voice, 5G SMS only"),
                opt("All generations used identical technology"),
            ),
            "The progression is analog voice (1G), digital voice (2G), mobile data (3G), all-IP broadband (4G), mmWave/massive MIMO (5G).",
        ),
        q(
            "Which multiple-access scheme assigns users blocks of subcarriers in both frequency and time?",
            (
                opt("FDMA"),
                opt("TDMA"),
                opt("CDMA"),
                opt("OFDMA", correct=True),
            ),
            "OFDMA schedules narrow-subcarrier blocks across both frequency and time, used in 4G/5G.",
        ),
    ),
)
