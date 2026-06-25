"""Curated quiz questions for the Data Converters & PLLs - Intermediate course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Flash ADC": (
            q(
                "How many comparators does an N-bit flash ADC require?",
                (
                    opt("N"),
                    opt("2*N"),
                    opt("2^N - 1", correct=True),
                    opt("N^2"),
                ),
                "A flash ADC compares against every threshold at once, needing 2^N - 1 comparators.",
            ),
            q(
                "What is the flash ADC's defining advantage?",
                (
                    opt("Lowest power of all architectures"),
                    opt("Highest achievable resolution"),
                    opt("It resolves all bits in a single clock cycle (fastest)", correct=True),
                    opt("It needs no comparators"),
                ),
                "Flash compares against all thresholds simultaneously, producing a code in one cycle, the fastest architecture.",
            ),
            q(
                "Why does flash resolution stay low (about 6-8 bits)?",
                (
                    opt("It is limited by the loop filter bandwidth"),
                    opt(
                        "Comparator and resistor count doubles with each bit, becoming hot and large",
                        correct=True,
                    ),
                    opt("It cannot resolve the LSB"),
                    opt("It requires too many clock cycles"),
                ),
                "Hardware grows as 2^N, so power and area explode, capping practical flash converters around 6-8 bits.",
            ),
        ),
        "Successive-approximation (SAR) ADC": (
            q(
                "How does a SAR ADC resolve its bits?",
                (
                    opt("All at once with parallel comparators"),
                    opt("By a binary search, one bit per cycle from the MSB down", correct=True),
                    opt("By integrating the input over many cycles"),
                    opt("By shaping noise out of the band"),
                ),
                "The SAR performs a binary search, deciding one bit per clock starting from the MSB.",
            ),
            q(
                "What internal block does a SAR ADC use to test each guess?",
                (
                    opt("A second flash ADC"),
                    opt("An internal DAC (often a capacitor array)", correct=True),
                    opt("A sigma-delta modulator"),
                    opt("A phase detector"),
                ),
                "The SAR feeds its trial code to an internal DAC and compares the output to the input.",
            ),
            q(
                "What is the main cost of the SAR architecture?",
                (
                    opt("Enormous power consumption"),
                    opt("N cycles of latency per sample", correct=True),
                    opt("Hundreds of comparators"),
                    opt("It cannot reach beyond 6 bits"),
                ),
                "A SAR takes N comparison cycles per sample, the mirror image of the flash's single-cycle speed.",
            ),
        ),
        "Pipelined ADC": (
            q(
                "What does each stage of a pipelined ADC pass to the next stage?",
                (
                    opt("The full input voltage unchanged"),
                    opt("The amplified residue (the part it could not yet resolve)", correct=True),
                    opt("Only the MSB it resolved"),
                    opt("A shaped noise spectrum"),
                ),
                "Each stage resolves a few bits, then amplifies the leftover residue and hands it downstream.",
            ),
            q(
                "Why can a pipelined ADC output one sample per clock despite having many stages?",
                (
                    opt("Each stage processes the same sample sequentially"),
                    opt(
                        "Stages run concurrently on different samples, like an assembly line",
                        correct=True,
                    ),
                    opt("It uses only one comparator total"),
                    opt("It oversamples and decimates"),
                ),
                "Stages work in parallel on successive samples, so throughput is one sample per clock with deep latency.",
            ),
            q(
                "What does digital error correction (e.g. 1.5 bits per stage) buy a pipeline?",
                (
                    opt("It removes the need for a sample-and-hold"),
                    opt("It eliminates latency"),
                    opt(
                        "It relaxes inter-stage comparator accuracy by overlapping stage ranges",
                        correct=True,
                    ),
                    opt("It doubles the resolution for free"),
                ),
                "Overlapping stage ranges with redundancy let digital correction tolerate imperfect comparators.",
            ),
        ),
        "Sigma-delta: oversampling & noise shaping": (
            q(
                "What is the oversampling ratio (OSR)?",
                (
                    opt("The number of bits in the quantizer"),
                    opt("f_s divided by twice the signal bandwidth", correct=True),
                    opt("The ratio of signal to noise power"),
                    opt("The number of pipeline stages"),
                ),
                "OSR = f_s / (2*f_B); a higher OSR spreads quantization noise over a wider band.",
            ),
            q(
                "What does noise shaping do in a sigma-delta modulator?",
                (
                    opt("Removes all quantization noise entirely"),
                    opt(
                        "High-pass shapes the quantization noise, pushing it out of the signal band",
                        correct=True,
                    ),
                    opt("Adds harmonics to improve SFDR"),
                    opt("Lowers the sample rate below Nyquist"),
                ),
                "The loop feeds the error back so it is high-pass shaped, moving most noise out of band where a filter removes it.",
            ),
            q(
                "Why does sigma-delta suit lower-bandwidth signals?",
                (
                    opt("Because it uses a flash sub-ADC"),
                    opt(
                        "Because high resolution needs a high OSR, which limits usable bandwidth",
                        correct=True,
                    ),
                    opt("Because it has no digital filter"),
                    opt("Because it cannot resolve more than 8 bits"),
                ),
                "Achieving many effective bits requires a high oversampling ratio, trading away signal bandwidth.",
            ),
        ),
        "DAC reconstruction & the zero-order hold": (
            q(
                "What frequency-domain effect does the zero-order hold impose?",
                (
                    opt("A flat all-pass response"),
                    opt("A sinc envelope that droops toward the band edge", correct=True),
                    opt("A high-pass boost above Nyquist"),
                    opt("Random phase noise sidebands"),
                ),
                "Holding each sample multiplies the spectrum by sinc(f/f_s), drooping in-band and creating images.",
            ),
            q(
                "What is the purpose of the reconstruction (smoothing) filter after a DAC?",
                (
                    opt("To prevent aliasing before sampling"),
                    opt("To remove the spectral images above f_s/2", correct=True),
                    opt("To add quantization noise"),
                    opt("To freeze the input value"),
                ),
                "The reconstruction low-pass removes the images the ZOH creates around multiples of f_s.",
            ),
            q(
                "What is sinc compensation?",
                (
                    opt("Adding more bits to the DAC"),
                    opt(
                        "A pre-emphasis that flattens the in-band droop of the zero-order hold",
                        correct=True,
                    ),
                    opt("A way to increase the noise floor"),
                    opt("Removing the sample-and-hold"),
                ),
                "Sinc compensation slightly boosts high in-band frequencies to counter the ZOH's sinc droop.",
            ),
        ),
        "Converter testing & FFT-based measurement": (
            q(
                "How are dynamic specs like SNR and SFDR measured?",
                (
                    opt("By a slow ramp histogram"),
                    opt("From an FFT of the captured samples of a clean sine input", correct=True),
                    opt("By measuring the DC offset"),
                    opt("From the loop filter step response"),
                ),
                "Driving the converter with a pure sine and taking an FFT exposes SNR, SINAD, SFDR and THD.",
            ),
            q(
                "Why use coherent sampling or a window when testing converters?",
                (
                    opt("To increase the resolution of the DUT"),
                    opt("To avoid spectral leakage smearing the FFT bins", correct=True),
                    opt("To eliminate quantization noise"),
                    opt("To remove the need for a sine source"),
                ),
                "Without coherent sampling or windowing, leakage spreads energy across bins and corrupts the measurement.",
            ),
            q(
                "Which test is best for static specs like INL and DNL?",
                (
                    opt("A single-tone FFT"),
                    opt("A histogram from a slow ramp or busy sine", correct=True),
                    opt("Measuring phase noise sidebands"),
                    opt("A step response measurement"),
                ),
                "Static linearity (INL/DNL) is measured with a code-density histogram from a ramp or busy sine, not an FFT.",
            ),
        ),
    },
    final=(
        q(
            "Rank these by raw conversion speed, fastest first.",
            (
                opt("SAR, then pipelined, then flash"),
                opt("Sigma-delta, then SAR, then flash"),
                opt("Flash, then pipelined, then SAR", correct=True),
                opt("Pipelined, then flash, then sigma-delta"),
            ),
            "Flash resolves in one cycle (fastest), pipelined gives one sample per clock with latency, SAR needs N cycles per sample.",
        ),
        q(
            "Which architecture is the workhorse for low-power microcontroller ADCs at medium resolution?",
            (
                opt("Flash"),
                opt("SAR", correct=True),
                opt("Pipelined"),
                opt("Sigma-delta"),
            ),
            "SAR ADCs offer medium speed and resolution at very low power, ideal for embedded front-ends.",
        ),
        q(
            "A sigma-delta converter achieves high resolution mainly through which two techniques?",
            (
                opt("Many comparators and digital correction"),
                opt("Oversampling and noise shaping", correct=True),
                opt("Binary search and an internal DAC"),
                opt("Charge pump and loop filter"),
            ),
            "Sigma-delta wins resolution by oversampling and high-pass noise shaping, then digital decimation.",
        ),
        q(
            "At Nyquist (f = f_s/2), the zero-order-hold sinc response is about what?",
            (
                opt("0 dB (flat)"),
                opt("about -3.9 dB", correct=True),
                opt("+6 dB"),
                opt("-40 dB"),
            ),
            "The ZOH sinc droops to about -3.9 dB at the Nyquist frequency.",
        ),
        q(
            "What does ENOB derived from an FFT-based SINAD measurement tell you?",
            (
                opt("The nominal datasheet bit count"),
                opt(
                    "The real effective resolution after noise and distortion",
                    correct=True,
                ),
                opt("The oversampling ratio"),
                opt("The number of pipeline stages"),
            ),
            "ENOB = (SINAD - 1.76)/6.02 reports the converter's honest resolution including noise and distortion.",
        ),
        q(
            "Why does a pipelined ADC need digital error correction with redundant bits?",
            (
                opt("To remove the latency between stages"),
                opt("To eliminate the sample-and-hold"),
                opt(
                    "To tolerate imperfect inter-stage comparators by overlapping stage ranges",
                    correct=True,
                ),
                opt("To increase the oversampling ratio"),
            ),
            "Redundancy (e.g. 1.5 bits/stage) lets digital correction absorb comparator inaccuracy without losing codes.",
        ),
    ),
)
