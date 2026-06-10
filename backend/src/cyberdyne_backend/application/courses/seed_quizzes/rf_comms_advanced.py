from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "RF front-end & transceiver architecture": (
            q(
                "Why must the LNA be the first stage of a receiver and add almost no noise of its own?",
                (
                    opt("Because it must boost the signal to watts before transmission"),
                    opt(
                        "Because by Friis' formula the first stage sets the whole receiver's noise figure",
                        correct=True,
                    ),
                    opt("Because it converts the signal to baseband I/Q directly"),
                    opt("Because it rejects the image frequency on its own"),
                ),
                "By Friis' formula the first stage dominates the receiver's overall noise figure, so the LNA must add almost no noise.",
            ),
            q(
                "What does a mixer do to a signal?",
                (
                    opt("Amplifies it to watts for transmission"),
                    opt("Adds noise to set the noise figure"),
                    opt(
                        "Multiplies it by a local oscillator, creating sum and difference frequencies",
                        correct=True,
                    ),
                    opt("Splits it into orthogonal subcarriers"),
                ),
                "A mixer multiplies the signal by the local oscillator, producing sum and difference frequencies - the heterodyne principle.",
            ),
            q(
                "What is the main weakness of the superheterodyne architecture?",
                (
                    opt("DC offset and LO leakage"),
                    opt("High peak-to-average power ratio"),
                    opt(
                        "The image frequency, a second band that also lands on the IF and must be filtered out",
                        correct=True,
                    ),
                    opt("It cannot be integrated into silicon"),
                ),
                "Superheterodyne suffers from the image frequency, a band 2 f_IF away that also maps onto the IF and must be filtered before mixing.",
            ),
        ),
        "The RF link budget & propagation": (
            q(
                "Why is the link budget expressed in dB?",
                (
                    opt("Because dB removes the need for antenna gains"),
                    opt(
                        "Because in dB every gain and loss is just added together",
                        correct=True,
                    ),
                    opt("Because dB converts power to frequency"),
                    opt("Because dB eliminates multipath fading"),
                ),
                "Working in dB turns the chain of multiplicative gains and losses into simple addition.",
            ),
            q(
                "According to the Friis equation, how does free-space received power change with distance?",
                (
                    opt("It rises with the square of distance"),
                    opt("It is independent of distance"),
                    opt(
                        "It falls as the inverse square of distance",
                        correct=True,
                    ),
                    opt("It falls linearly with distance"),
                ),
                "In free space power spreads over a sphere, so received power falls as the inverse square of distance.",
            ),
            q(
                "What causes a deep multipath fade?",
                (
                    opt("The LNA adding too much noise"),
                    opt(
                        "Reflections arriving with different delays and phases that interfere and cancel",
                        correct=True,
                    ),
                    opt("The transmit power being too high"),
                    opt("The cyclic prefix being too long"),
                ),
                "Multipath reflections arrive with different delays and phases and interfere; where they cancel the signal drops into a deep fade.",
            ),
        ),
        "Antennas & arrays for comms": (
            q(
                "What does antenna gain (dBi) actually describe?",
                (
                    opt("How much electrical power the antenna adds like an amplifier"),
                    opt(
                        "How it concentrates power in a direction relative to an isotropic radiator",
                        correct=True,
                    ),
                    opt("How much noise the antenna adds to the receiver"),
                    opt("How many spatial streams it can carry"),
                ),
                "Gain is not amplification; it measures how the antenna concentrates power in a direction relative to an isotropic radiator (dBi).",
            ),
            q(
                "How does a phased array steer its beam electronically?",
                (
                    opt("By physically rotating the antenna elements"),
                    opt("By increasing the transmit power on one element"),
                    opt(
                        "By feeding elements with progressive phase shifts so wavefronts add up in a chosen direction",
                        correct=True,
                    ),
                    opt("By adding a cyclic prefix to the signal"),
                ),
                "Progressive phase shifts across the elements make the wavefronts add up in a chosen direction, steering the beam with no moving parts.",
            ),
            q(
                "How does MIMO turn multipath into an asset?",
                (
                    opt("It uses multipath to lower the receiver noise figure"),
                    opt(
                        "Independent paths form parallel spatial streams, multiplying capacity without more bandwidth or power",
                        correct=True,
                    ),
                    opt("It removes multipath entirely using the cyclic prefix"),
                    opt("It converts multipath into extra transmit power"),
                ),
                "MIMO uses independent multipath paths as parallel spatial streams, multiplying capacity without extra bandwidth or power.",
            ),
        ),
        "OFDM & modern wireless": (
            q(
                "How does OFDM combat frequency-selective fading and ISI?",
                (
                    opt("By using a single very fast wideband subcarrier"),
                    opt(
                        "By splitting one fast data stream across many slow, narrow subcarriers in parallel",
                        correct=True,
                    ),
                    opt("By raising the transmit power on every symbol"),
                    opt("By removing the local oscillator"),
                ),
                "OFDM splits one fast stream into many slow, narrow subcarriers so each sees a flat channel and a deep fade kills only a few.",
            ),
            q(
                "What is the purpose of the cyclic prefix in OFDM?",
                (
                    opt("To increase the peak-to-average power ratio"),
                    opt("To add antenna gain at both ends of the link"),
                    opt(
                        "To absorb multipath echoes of the previous symbol so the FFT sees a clean periodic symbol",
                        correct=True,
                    ),
                    opt("To convert QAM symbols into spatial streams"),
                ),
                "The cyclic prefix copies the symbol tail to its front; if delay spread is shorter than the CP, prior-symbol echoes decay within it.",
            ),
            q(
                "What is the main catch of OFDM that stresses the power amplifier?",
                (
                    opt("Its high receiver noise figure"),
                    opt(
                        "A high peak-to-average power ratio (PAPR) from summing many subcarriers",
                        correct=True,
                    ),
                    opt("Its inability to use the FFT"),
                    opt("Its dependence on physical beam steering"),
                ),
                "Summing many subcarriers can momentarily peak high, giving a high PAPR that stresses the power amplifier.",
            ),
        ),
        "Software-defined radio & DSP in comms": (
            q(
                "What is the core idea of software-defined radio?",
                (
                    opt("Keep every function in dedicated analog hardware"),
                    opt(
                        "Digitize close to the antenna and do filtering, mixing, and demodulation in software/DSP",
                        correct=True,
                    ),
                    opt("Replace antennas with phased arrays only"),
                    opt("Use only the superheterodyne architecture"),
                ),
                "SDR digitizes as close to the antenna as possible and performs filtering, mixing, modulation, and demodulation in software/DSP.",
            ),
            q(
                "In an SDR I/Q sample stream, multiplying a complex sample by e^(j*theta) does what?",
                (
                    opt("Filters it with FIR taps"),
                    opt("Decimates the sample rate by M"),
                    opt(
                        "Rotates it, acting as a tunable digital mixer",
                        correct=True,
                    ),
                    opt("Adds a cyclic prefix"),
                ),
                "Multiplying a complex sample by e^(j*theta) rotates it in the I/Q plane, which is a tunable digital mixer.",
            ),
            q(
                "What does decimation do in an SDR receiver?",
                (
                    opt("It boosts transmit power to watts"),
                    opt(
                        "It filters then keeps every M-th sample to focus on the channel at a manageable rate",
                        correct=True,
                    ),
                    opt("It adds noise to set the noise figure"),
                    opt("It steers the antenna beam electronically"),
                ),
                "After a wideband ADC, the DSP filters then decimates (keeps every M-th sample) to focus on the channel at a manageable rate.",
            ),
        ),
        "Lab: link budget & an OFDM symbol": (
            q(
                "In the lab, how is receiver sensitivity computed?",
                (
                    opt("Transmit power minus antenna gains"),
                    opt(
                        "Thermal noise floor plus noise figure plus the required SNR",
                        correct=True,
                    ),
                    opt("Path loss minus the cyclic prefix length"),
                    opt("The Doppler shift times the carrier frequency"),
                ),
                "Sensitivity is the thermal noise floor (-174 + 10*log10(B)) plus noise figure plus the required SNR.",
            ),
            q(
                "In the OFDM part of the lab, how are the subcarriers recovered after the channel?",
                (
                    opt("By convolving the received signal with the channel taps"),
                    opt("By adding a second cyclic prefix"),
                    opt(
                        "By removing the cyclic prefix, taking the FFT, and dividing by H (a 1-tap equalize)",
                        correct=True,
                    ),
                    opt("By multiplying by a local oscillator e^(j*theta)"),
                ),
                "The lab removes the CP, takes the FFT, and divides by H = fft(channel) - a one-tap per-subcarrier equalizer.",
            ),
            q(
                "According to the lab, what happens if you raise NF or the required SNR?",
                (
                    opt("The link closes at a longer range"),
                    opt(
                        "Sensitivity worsens and the maximum range shrinks",
                        correct=True,
                    ),
                    opt("The cyclic prefix becomes longer"),
                    opt("The OFDM recovery error goes to zero"),
                ),
                "Raising NF or required SNR worsens sensitivity, so the link closes over a shorter maximum range.",
            ),
        ),
        "Applications: 5G, satellite, IoT & radar": (
            q(
                "Why do LEO constellations such as Starlink fly low (about 550 km)?",
                (
                    opt("To increase the peak-to-average power ratio"),
                    opt(
                        "To cut latency and path loss compared to a geostationary orbit",
                        correct=True,
                    ),
                    opt("To avoid using phased arrays"),
                    opt("To raise the receiver noise figure"),
                ),
                "LEO satellites fly low (about 550 km) to cut latency and path loss versus geostationary orbit at about 36,000 km.",
            ),
            q(
                "What do IoT/LPWAN radios optimize for, and how?",
                (
                    opt("Peak throughput, using 256-QAM and massive MIMO"),
                    opt(
                        "Energy per bit, using narrow bandwidth, heavy coding, and tiny duty cycles",
                        correct=True,
                    ),
                    opt("Latency, using millimeter-wave bands and dense cells"),
                    opt("Beam steering, using large phased arrays"),
                ),
                "IoT/LPWAN technologies optimize energy per bit with narrow bandwidth, heavy coding, and tiny duty cycles to reach kilometers at milliwatts.",
            ),
            q(
                "How does radar determine a target's range and velocity?",
                (
                    opt("Range from antenna gain and velocity from transmit power"),
                    opt(
                        "Range from round-trip delay (d = c*tau/2) and velocity from the Doppler shift",
                        correct=True,
                    ),
                    opt("Both from the cyclic prefix length"),
                    opt("Range from the noise figure and velocity from the SNR"),
                ),
                "Radar gets range from round-trip delay (d = c*tau/2) and velocity from the Doppler shift of the echo.",
            ),
        ),
    },
    final=(
        q(
            "Which architecture mixes the signal straight to baseband, avoiding the image problem but suffering DC offset and LO leakage?",
            (
                opt("Superheterodyne"),
                opt("Direct conversion (zero-IF)", correct=True),
                opt("Phased array"),
                opt("Massive MIMO"),
            ),
            "Direct conversion (zero-IF) mixes straight to baseband, avoiding the image problem but suffering DC offset and LO leakage.",
        ),
        q(
            "In a link budget P_rx = P_tx + G_tx + G_rx - L_path - L_misc, what determines whether the link closes?",
            (
                opt("Whether P_rx equals the transmit power"),
                opt(
                    "Whether P_rx exceeds the receiver sensitivity with margin to spare",
                    correct=True,
                ),
                opt("Whether the cyclic prefix exceeds the delay spread"),
                opt("Whether the Doppler shift is zero"),
            ),
            "The link closes when received power exceeds the receiver sensitivity (noise floor plus required SNR) with margin to spare.",
        ),
        q(
            "What lets OFDM subcarriers overlap in frequency without interfering with each other?",
            (
                opt("They are spread by a CDMA code"),
                opt("They are carried on separate antennas"),
                opt(
                    "They are orthogonal: each subcarrier's spectrum is zero at every other's center",
                    correct=True,
                ),
                opt("They use a high peak-to-average power ratio"),
            ),
            "OFDM subcarriers are orthogonal - spaced so each one's spectrum is zero at every other's center - so they overlap without interfering.",
        ),
        q(
            "Which constants does the course present as the unchanging foundation across radio systems?",
            (
                opt("The cyclic prefix, PAPR, and decimation"),
                opt(
                    "Shannon, Friis, and the decibel",
                    correct=True,
                ),
                opt("LoRa, NB-IoT, and Sigfox"),
                opt("LNA, mixer, and power amplifier"),
            ),
            "The throughline of the course is that bands and standards change but Shannon, Friis, and the decibel do not.",
        ),
        q(
            "How does a phased array sharpen its main beam as the number of elements N grows?",
            (
                opt("It raises the transmit power per element"),
                opt(
                    "The array factor narrows the beamwidth as N increases",
                    correct=True,
                ),
                opt("It adds a cyclic prefix per element"),
                opt("It lowers the carrier frequency"),
            ),
            "The array factor for N elements sharpens as N grows, narrowing the main beam.",
        ),
    ),
)
