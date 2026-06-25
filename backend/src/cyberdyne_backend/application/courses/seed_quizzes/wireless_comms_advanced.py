"""Curated quiz questions for the Wireless & Mobile Communications - Advanced course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Diversity & combining": (
            q(
                "What is the core idea behind diversity?",
                (
                    opt("Transmitting at the highest possible power"),
                    opt(
                        "Sending the same information over independent channels so they are unlikely to all fade at once",
                        correct=True,
                    ),
                    opt("Using a single antenna with a narrow beam"),
                    opt("Lowering the data rate until errors vanish"),
                ),
                "Diversity sends information over independent channels (time, frequency or space) that rarely fade simultaneously.",
            ),
            q(
                "Which combining method weights each branch by its SNR and is optimal?",
                (
                    opt("Selection combining"),
                    opt("Maximal-ratio combining (MRC)", correct=True),
                    opt("Equal-loss combining"),
                    opt("Zero-forcing combining"),
                ),
                "MRC weights branches by their SNR and sums them; the combined SNR is the sum of branch SNRs, which is optimal.",
            ),
            q(
                "Roughly how far apart must antennas be to give independent space diversity?",
                (
                    opt("Less than a tenth of a wavelength"),
                    opt("More than about half a wavelength", correct=True),
                    opt("Exactly one full wavelength only"),
                    opt("Several kilometres"),
                ),
                "Antennas separated by more than about half a wavelength see decorrelated fades, providing space diversity.",
            ),
        ),
        "MIMO & spatial multiplexing": (
            q(
                "How does spatial multiplexing differ from diversity?",
                (
                    opt("It uses the extra antennas for reliability rather than throughput"),
                    opt(
                        "It sends independent data streams over the same time and frequency for more throughput",
                        correct=True,
                    ),
                    opt("It uses only one antenna at each end"),
                    opt("It lowers the SNR on purpose"),
                ),
                "Spatial multiplexing uses the antennas to carry independent parallel streams, raising throughput rather than reliability.",
            ),
            q(
                "Up to how many independent streams can a MIMO channel carry?",
                (
                    opt("Always exactly one"),
                    opt(
                        "Up to the minimum of the transmit and receive antenna counts", correct=True
                    ),
                    opt("Up to the sum of transmit and receive antennas"),
                    opt("Unlimited, regardless of antennas"),
                ),
                "The number of streams is the channel rank, at most min(Nt, Nr).",
            ),
            q(
                "How does MIMO capacity scale with the number of streams?",
                (
                    opt("Logarithmically with the stream count"),
                    opt("It does not change with streams"),
                    opt(
                        "Roughly linearly with min(Nt, Nr), for no extra bandwidth or power",
                        correct=True,
                    ),
                    opt("It falls as streams are added"),
                ),
                "Capacity grows roughly linearly with the number of streams min(Nt, Nr), without extra bandwidth or power.",
            ),
        ),
        "Massive MIMO & beamforming": (
            q(
                "How does beamforming focus energy toward a user?",
                (
                    opt("By increasing the carrier frequency"),
                    opt(
                        "By adjusting the phase at each antenna so wavefronts add constructively toward the user and cancel elsewhere",
                        correct=True,
                    ),
                    opt("By using only a single antenna"),
                    opt("By lowering the transmit power everywhere"),
                ),
                "Beamforming sets per-antenna phases so the array steers a focused beam toward the user and creates nulls elsewhere.",
            ),
            q(
                "Why is beamforming essential for mmWave?",
                (
                    opt("Because mmWave has unlimited range"),
                    opt(
                        "Because the focused beam recovers range lost to the severe path loss at high frequencies",
                        correct=True,
                    ),
                    opt("Because mmWave penetrates walls easily"),
                    opt("Because mmWave needs no antennas"),
                ),
                "mmWave suffers severe path loss, so the high gain of a focused beam is needed to recover usable range.",
            ),
            q(
                "How does massive MIMO estimate the downlink channel efficiently in TDD?",
                (
                    opt("By guessing it randomly"),
                    opt(
                        "By exploiting channel reciprocity to infer the downlink from uplink pilots, avoiding huge feedback overhead",
                        correct=True,
                    ),
                    opt("By assuming the channel never changes"),
                    opt("By using a separate frequency band for every antenna"),
                ),
                "TDD reciprocity lets the base station estimate the downlink from uplink pilots, avoiding crippling feedback overhead.",
            ),
        ),
        "LTE/4G architecture & resource blocks": (
            q(
                "Which LTE element handles mobility and signalling?",
                (
                    opt("The eNodeB"),
                    opt("The MME", correct=True),
                    opt("The P-GW"),
                    opt("The HSS"),
                ),
                "The MME (Mobility Management Entity) handles signalling and mobility in the Evolved Packet Core.",
            ),
            q(
                "What is an LTE resource block?",
                (
                    opt("A single subcarrier over the whole frame"),
                    opt(
                        "12 subcarriers (180 kHz) over a 0.5 ms slot, the unit the scheduler allocates",
                        correct=True,
                    ),
                    opt("The entire 20 MHz channel for one user"),
                    opt("A block of spreading codes"),
                ),
                "A resource block is 12 subcarriers (180 kHz) over a 0.5 ms slot, the basic scheduling unit.",
            ),
            q(
                "On what basis does the LTE scheduler assign resource blocks each millisecond?",
                (
                    opt("Alphabetical order of the users"),
                    opt(
                        "Each user's reported channel quality (CQI), for opportunistic sharing in frequency and time",
                        correct=True,
                    ),
                    opt("A fixed permanent assignment per user"),
                    opt("The transmit power of the handset only"),
                ),
                "The scheduler uses reported CQI to allocate RBs opportunistically in both frequency and time.",
            ),
        ),
        "5G NR: numerology, mmWave & slicing": (
            q(
                "What does 5G NR numerology allow that LTE did not?",
                (
                    opt("A single fixed 15 kHz subcarrier spacing"),
                    opt(
                        "Scalable subcarrier spacing of 15 x 2^mu kHz, chosen to fit the band and service",
                        correct=True,
                    ),
                    opt("Analog modulation of the carrier"),
                    opt("Removal of OFDMA"),
                ),
                "NR numerology allows scalable spacing (15 x 2^mu kHz), unlike LTE's fixed 15 kHz, to trade latency against robustness.",
            ),
            q(
                "Why does mmWave in 5G require beamforming and dense small cells?",
                (
                    opt("Because mmWave travels extremely far"),
                    opt(
                        "Because mmWave suffers severe path loss and blockage, so focused beams and short ranges are needed",
                        correct=True,
                    ),
                    opt("Because mmWave has very little bandwidth"),
                    opt("Because mmWave cannot carry data"),
                ),
                "mmWave's high path loss and blockage force the use of beamforming and dense small cells to maintain coverage.",
            ),
            q(
                "What is network slicing?",
                (
                    opt("Splitting the spectrum into licensed and unlicensed bands"),
                    opt(
                        "Partitioning one physical 5G network into multiple virtual networks, each tuned to a use case",
                        correct=True,
                    ),
                    opt("Cutting cells into smaller cells"),
                    opt("Dividing a symbol into a cyclic prefix"),
                ),
                "Slicing partitions a single physical 5G network into virtual networks (eMBB, URLLC, mMTC) tuned per use case.",
            ),
        ),
        "Case study: link budget & throughput": (
            q(
                "In the case study, how is the downlink SNR obtained?",
                (
                    opt("By adding received power to the noise floor"),
                    opt(
                        "By subtracting the noise floor from the received power, both in dBm",
                        correct=True,
                    ),
                    opt("By dividing transmit power by bandwidth"),
                    opt("By multiplying the antenna gains"),
                ),
                "SNR (in dB) is received power minus the noise floor; in the example -69 - (-94) = 25 dB.",
            ),
            q(
                "Why does adding MIMO streams beat simply raising SNR for throughput?",
                (
                    opt("Because higher SNR reduces capacity"),
                    opt(
                        "Because SNR buys only a logarithmic gain, while extra streams multiply capacity linearly",
                        correct=True,
                    ),
                    opt("Because MIMO streams need no antennas"),
                    opt("Because SNR has no effect on capacity"),
                ),
                "Capacity grows only logarithmically with SNR but linearly with the number of MIMO streams, so streams scale better.",
            ),
            q(
                "Which three levers does 5G combine to maximise throughput?",
                (
                    opt("Lower power, fewer antennas, narrower bandwidth"),
                    opt(
                        "Massive MIMO (more streams), beamforming (better SNR) and wide mmWave bandwidth",
                        correct=True,
                    ),
                    opt("Analog voice, single carrier and FDMA"),
                    opt("Only raising the transmit power"),
                ),
                "5G chases more streams (massive MIMO), better SNR (beamforming) and more bandwidth (mmWave) together.",
            ),
        ),
    },
    final=(
        q(
            "What distinguishes diversity from spatial multiplexing in a multi-antenna system?",
            (
                opt("Diversity adds streams for throughput; multiplexing adds reliability"),
                opt(
                    "Diversity uses the antennas for reliability against fading; multiplexing sends independent streams for throughput",
                    correct=True,
                ),
                opt("Both reduce the number of antennas to one"),
                opt("Neither depends on the number of antennas"),
            ),
            "Diversity spends antennas on reliability against fading; spatial multiplexing spends them on parallel streams for throughput.",
        ),
        q(
            "A 4x4 MIMO link in rich scattering can approach how many independent streams?",
            (
                opt("1"),
                opt("2"),
                opt("4", correct=True),
                opt("8"),
            ),
            "With 4 transmit and 4 receive antennas, the channel can support up to min(4, 4) = 4 streams.",
        ),
        q(
            "What makes massive MIMO and beamforming the headline capacity tools of 5G?",
            (
                opt("They lower the bandwidth and power needed to near zero"),
                opt(
                    "Many antennas let the base station steer focused beams and serve many users simultaneously on the same time and frequency",
                    correct=True,
                ),
                opt("They remove the need for cells"),
                opt("They make the channel matrix singular"),
            ),
            "With many antennas, the base station forms focused beams (high SNR, low interference) and serves many users at once (MU-MIMO).",
        ),
        q(
            "Which LTE structure does 5G NR keep but make configurable via numerology?",
            (
                opt("Analog FM voice"),
                opt("CDMA spreading codes"),
                opt("The OFDMA resource-block grid", correct=True),
                opt("The 1G frequency plan"),
            ),
            "5G keeps the OFDMA/resource-block structure of LTE but adds scalable numerology to make it flexible.",
        ),
        q(
            "Which slice type targets ultra-reliable low-latency communication?",
            (
                opt("eMBB"),
                opt("URLLC", correct=True),
                opt("mMTC"),
                opt("FDMA"),
            ),
            "URLLC is the 5G slice tuned for ultra-reliable low-latency control (e.g. vehicles, automation).",
        ),
        q(
            "The link-budget/throughput case study concludes that 5G boosts throughput mainly by...",
            (
                opt("raising SNR alone, since capacity grows linearly with SNR"),
                opt(
                    "combining more MIMO streams and more mmWave bandwidth, since SNR only gives logarithmic gains",
                    correct=True,
                ),
                opt("switching back to analog modulation"),
                opt("reducing the number of antennas and cells"),
            ),
            "Because capacity is only logarithmic in SNR, 5G multiplies it with more streams (massive MIMO) and more bandwidth (mmWave).",
        ),
    ),
)
