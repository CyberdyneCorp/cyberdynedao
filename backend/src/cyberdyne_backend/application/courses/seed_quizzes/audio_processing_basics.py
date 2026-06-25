"""Curated quiz questions for the Speech, Audio & Acoustics - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Sound & acoustics: pressure waves, frequency, decibels": (
            q(
                "What physically is a sound wave in air?",
                (
                    opt("A flow of electrons through the air"),
                    opt(
                        "A small, fast fluctuation of air pressure travelling from a vibrating source",
                        correct=True,
                    ),
                    opt("A standing electromagnetic field"),
                    opt("A change in the temperature of the air only"),
                ),
                "Sound is a fluctuation of air pressure propagating outward from a vibrating source.",
            ),
            q(
                "For a pure tone, what does the frequency f determine?",
                (
                    opt("How loud the tone is"),
                    opt("How high or low the pitch is", correct=True),
                    opt("The speed of sound in air"),
                    opt("The decibel reference pressure"),
                ),
                "Frequency sets pitch (how high/low); amplitude sets loudness.",
            ),
            q(
                "Why is sound level measured in decibels (a logarithmic scale)?",
                (
                    opt("Because pressure is always negative"),
                    opt("Because frequencies are spaced linearly"),
                    opt(
                        "Because audible pressures span a huge range and the ear responds logarithmically",
                        correct=True,
                    ),
                    opt("Because decibels are easier to add than to multiply"),
                ),
                "The dB scale is logarithmic to match the enormous pressure range and the ear's logarithmic response.",
            ),
        ),
        "Digital audio: sampling, bit depth & Nyquist": (
            q(
                "What does the Nyquist frequency equal?",
                (
                    opt("Twice the sample rate"),
                    opt("Half the sample rate", correct=True),
                    opt("The sample rate itself"),
                    opt("The bit depth times the sample rate"),
                ),
                "The Nyquist frequency is half the sample rate; only frequencies below it are captured faithfully.",
            ),
            q(
                "What is aliasing?",
                (
                    opt("Noise added by quantization rounding"),
                    opt(
                        "Frequencies above Nyquist folding back and masquerading as lower tones",
                        correct=True,
                    ),
                    opt("The smoothing done by the reconstruction filter"),
                    opt("The loss of bits when audio is compressed"),
                ),
                "Frequencies above the Nyquist limit fold back and appear as false lower frequencies — aliasing.",
            ),
            q(
                "What does increasing the bit depth primarily improve?",
                (
                    opt("The highest frequency that can be captured"),
                    opt("The dynamic range / quiet noise floor (about 6 dB per bit)", correct=True),
                    opt("The speed of sound"),
                    opt("The number of audio channels"),
                ),
                "Bit depth sets quantization-noise floor and dynamic range (~6 dB per bit); sample rate sets the frequency limit.",
            ),
        ),
        "The human ear & psychoacoustics": (
            q(
                "Roughly which frequency range is the ear most sensitive to?",
                (
                    opt("20 to 60 Hz"),
                    opt("About 2 to 5 kHz", correct=True),
                    opt("15 to 20 kHz"),
                    opt("Above 20 kHz"),
                ),
                "Equal-loudness contours show peak sensitivity around 2-5 kHz, the speech range.",
            ),
            q(
                "What does the cochlea do, in signal-processing terms?",
                (
                    opt("It amplifies all frequencies by the same fixed gain"),
                    opt(
                        "It acts as a bank of tuned filters, mapping frequency to position",
                        correct=True,
                    ),
                    opt("It converts pressure into temperature"),
                    opt("It removes the fundamental frequency"),
                ),
                "The cochlea maps frequency to position along its length, behaving like a biological filter bank.",
            ),
            q(
                "Raising a note by one octave corresponds to what change in frequency?",
                (
                    opt("Adding a fixed number of hertz"),
                    opt("Doubling the frequency", correct=True),
                    opt("Halving the amplitude"),
                    opt("Adding 6 dB"),
                ),
                "Pitch is logarithmic: one octave is a doubling of frequency, regardless of the starting note.",
            ),
        ),
        "Time vs frequency: the FFT & the spectrum": (
            q(
                "What does the magnitude spectrum of a signal show?",
                (
                    opt("Pressure as a function of time"),
                    opt("Energy as a function of frequency", correct=True),
                    opt("The sample rate over time"),
                    opt("The bit depth of each sample"),
                ),
                "The spectrum is the Fourier magnitude: how much energy sits at each frequency.",
            ),
            q(
                "Why is the FFT so important for audio?",
                (
                    opt("It increases the sample rate"),
                    opt(
                        "It computes the DFT in O(N log N) instead of O(N^2)",
                        correct=True,
                    ),
                    opt("It removes all quantization noise"),
                    opt("It doubles the dynamic range"),
                ),
                "The FFT computes the discrete Fourier transform efficiently, in O(N log N) time.",
            ),
            q(
                "How are the time and frequency domains related?",
                (
                    opt("They are unrelated representations"),
                    opt(
                        "They are two views of the same signal, linked by the FFT and its inverse",
                        correct=True,
                    ),
                    opt("The frequency domain only exists for noise"),
                    opt("The time domain is an approximation of the frequency domain"),
                ),
                "Time and frequency are equivalent views of one signal, connected by the (inverse) Fourier transform.",
            ),
        ),
        "Basic audio filtering & equalization": (
            q(
                "Which filter would you use to remove 50/60 Hz mains hum from a recording?",
                (
                    opt("A low-pass filter"),
                    opt("A high-pass filter"),
                    opt("A band-stop / notch filter", correct=True),
                    opt("A band-pass filter"),
                ),
                "A notch (band-stop) filter removes one narrow frequency such as mains hum.",
            ),
            q(
                "What is the cutoff frequency of a low-pass filter conventionally defined as?",
                (
                    opt("The frequency of maximum gain"),
                    opt("The -3 dB (half-power) point", correct=True),
                    opt("The frequency where gain is zero"),
                    opt("Twice the sample rate"),
                ),
                "The cutoff is the -3 dB point, where the filter passes half the power.",
            ),
            q(
                "What is a parametric equalizer, in essence?",
                (
                    opt("A single fixed low-pass filter"),
                    opt(
                        "A set of filters where you choose centre frequency, gain and bandwidth (Q)",
                        correct=True,
                    ),
                    opt("A device that only changes loudness"),
                    opt("An analog-to-digital converter"),
                ),
                "A parametric EQ is a bank of filters with adjustable centre frequency, gain and Q.",
            ),
        ),
        "The audio signal chain: mic to speaker": (
            q(
                "What is the correct order of the core digital audio chain?",
                (
                    opt("Speaker -> DAC -> DSP -> ADC -> microphone"),
                    opt(
                        "Microphone -> ADC -> DSP -> DAC -> speaker",
                        correct=True,
                    ),
                    opt("ADC -> microphone -> speaker -> DAC -> DSP"),
                    opt("DSP -> microphone -> ADC -> speaker -> DAC"),
                ),
                "Sound is captured by the mic, digitized by the ADC, processed by DSP, converted back by the DAC, and played by the speaker.",
            ),
            q(
                "What is the role of the anti-alias filter in the chain?",
                (
                    opt("It boosts the bass after the DAC"),
                    opt(
                        "It removes frequencies above Nyquist before the ADC samples",
                        correct=True,
                    ),
                    opt("It converts numbers back into voltage"),
                    opt("It increases the bit depth"),
                ),
                "The anti-alias low-pass filter sits before the ADC to strip content above the Nyquist limit.",
            ),
            q(
                "What does a microphone do?",
                (
                    opt("Converts a voltage into acoustic pressure"),
                    opt("Converts acoustic pressure into a voltage (a transducer)", correct=True),
                    opt("Samples and quantizes the signal"),
                    opt("Amplifies the digital bitstream"),
                ),
                "A microphone is a transducer turning acoustic pressure into an electrical voltage.",
            ),
        ),
    },
    final=(
        q(
            "Which quantity is measured on a logarithmic decibel scale?",
            (
                opt("Frequency"),
                opt("Sound level (loudness)", correct=True),
                opt("Sample index"),
                opt("Filter order"),
            ),
            "Sound-pressure level is expressed in decibels, a logarithmic scale matching the ear.",
        ),
        q(
            "A CD uses a 44.1 kHz sample rate. What is the highest frequency it can represent?",
            (
                opt("About 11 kHz"),
                opt("About 22 kHz", correct=True),
                opt("About 44 kHz"),
                opt("About 88 kHz"),
            ),
            "The Nyquist limit is half the sample rate, so about 22 kHz.",
        ),
        q(
            "Which statement about the human ear is correct?",
            (
                opt("It responds equally to all frequencies at a given level"),
                opt(
                    "It is most sensitive around 2-5 kHz and perceives pitch and loudness logarithmically",
                    correct=True,
                ),
                opt("It hears best below 50 Hz"),
                opt("It perceives loudness linearly in pressure"),
            ),
            "The ear peaks in sensitivity around 2-5 kHz and is logarithmic in both pitch and loudness.",
        ),
        q(
            "What does the FFT compute, and why does it matter for audio?",
            (
                opt("The time-domain waveform from the spectrum, slowly"),
                opt(
                    "The spectrum (DFT) efficiently in O(N log N), enabling frequency analysis",
                    correct=True,
                ),
                opt("The bit depth needed for a recording"),
                opt("The speed of sound at a given temperature"),
            ),
            "The FFT computes the discrete Fourier transform efficiently, making real-time spectral analysis practical.",
        ),
        q(
            "Which filter keeps a band such as telephone speech (300-3400 Hz) and rejects the rest?",
            (
                opt("Low-pass"),
                opt("High-pass"),
                opt("Band-pass", correct=True),
                opt("Notch"),
            ),
            "A band-pass filter passes a chosen band and rejects frequencies above and below it.",
        ),
        q(
            "In the audio signal chain, what marks the boundary between the analog and digital worlds?",
            (
                opt("The microphone and the speaker"),
                opt("The pre-amp and the power amp"),
                opt("The ADC (in) and the DAC (out)", correct=True),
                opt("The anti-alias and reconstruction filters"),
            ),
            "The ADC and DAC form the digital boundary: analog on the outside, numbers in between.",
        ),
    ),
)
