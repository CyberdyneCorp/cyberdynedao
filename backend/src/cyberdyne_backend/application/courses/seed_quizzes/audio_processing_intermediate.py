"""Curated quiz questions for the Speech, Audio & Acoustics - Intermediate course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The short-time Fourier transform & spectrograms": (
            q(
                "Why is the STFT used instead of one FFT of the whole signal?",
                (
                    opt("It removes the need for windowing"),
                    opt(
                        "It shows how the frequency content changes over time, in short frames",
                        correct=True,
                    ),
                    opt("It increases the sample rate"),
                    opt("It eliminates quantization noise"),
                ),
                "The STFT FFTs short overlapping frames so you see how frequencies evolve in time.",
            ),
            q(
                "What is a spectrogram?",
                (
                    opt("A plot of pressure versus time"),
                    opt(
                        "An image of frequency vs time with energy shown as colour, built from STFT frames",
                        correct=True,
                    ),
                    opt("A single magnitude spectrum"),
                    opt("A list of filter coefficients"),
                ),
                "A spectrogram stacks STFT magnitude spectra into a time-frequency-energy image.",
            ),
            q(
                "What trade-off does the STFT window length control?",
                (
                    opt("Loudness versus pitch"),
                    opt("Bit depth versus sample rate"),
                    opt("Time resolution versus frequency resolution", correct=True),
                    opt("Analog versus digital"),
                ),
                "A long window gives fine frequency but coarse time resolution, and vice versa.",
            ),
        ),
        "Windowing & spectral leakage": (
            q(
                "What causes spectral leakage?",
                (
                    opt("Sampling above the Nyquist rate"),
                    opt(
                        "Abruptly cutting a frame (a rectangular window) splatters energy across frequency",
                        correct=True,
                    ),
                    opt("Using too many bits per sample"),
                    opt("A perfectly periodic signal"),
                ),
                "Sharp frame edges (rectangular window) spread a tone's energy across frequency as leakage.",
            ),
            q(
                "How does applying a Hann window reduce leakage?",
                (
                    opt("By increasing the frame's sample rate"),
                    opt("By tapering the frame smoothly to zero at both ends", correct=True),
                    opt("By removing the fundamental frequency"),
                    opt("By adding noise to mask the side-lobes"),
                ),
                "Tapering the frame to zero at both ends softens the edges and lowers the side-lobes.",
            ),
            q(
                "What is the trade-off when choosing a window like Hann or Blackman?",
                (
                    opt("Sample rate versus bit depth"),
                    opt(
                        "A wider main lobe (worse resolution) for lower side-lobes (less leakage)",
                        correct=True,
                    ),
                    opt("Latency versus loudness"),
                    opt("FIR versus IIR stability"),
                ),
                "Windows trade main-lobe width (frequency resolution) against side-lobe height (leakage).",
            ),
        ),
        "Digital filters for audio: FIR, IIR, EQ & shelving": (
            q(
                "What distinguishes an IIR filter from an FIR filter?",
                (
                    opt("IIR filters use only past inputs"),
                    opt(
                        "IIR filters feed back past outputs as well as inputs",
                        correct=True,
                    ),
                    opt("FIR filters are always unstable"),
                    opt("IIR filters cannot be implemented digitally"),
                ),
                "IIR filters use feedback (past outputs); FIR filters use only past inputs.",
            ),
            q(
                "What is a key advantage of an FIR filter for audio?",
                (
                    opt("It always uses fewer taps than IIR"),
                    opt("It can have exactly linear phase and is always stable", correct=True),
                    opt("It never needs windowing"),
                    opt("It cannot become unstable only because it uses feedback"),
                ),
                "FIR filters are always stable and can be designed with exactly linear phase.",
            ),
            q(
                "What does a low-shelf filter do?",
                (
                    opt("Boosts or cuts everything below a corner frequency", correct=True),
                    opt("Removes a single narrow frequency"),
                    opt("Boosts a band around a centre frequency only"),
                    opt("Inverts the entire spectrum"),
                ),
                "A low-shelf boosts or cuts all frequencies below its corner, leaving the highs flat.",
            ),
        ),
        "Reverb, delay & dynamic-range compression": (
            q(
                "What does the parameter RT60 describe?",
                (
                    opt("The sample rate of the reverb"),
                    opt("The time for the reverberation tail to drop by 60 dB", correct=True),
                    opt("The number of taps in the delay line"),
                    opt("The compressor threshold in dB"),
                ),
                "RT60 is the reverberation decay time: how long the tail takes to fall 60 dB.",
            ),
            q(
                "Above its threshold, what does a compressor with ratio R do to the level?",
                (
                    opt("Leaves it unchanged (1:1)"),
                    opt(
                        "Reduces gain so the output rises only 1/R as fast as the input",
                        correct=True,
                    ),
                    opt("Mutes the signal entirely"),
                    opt("Doubles the loud peaks"),
                ),
                "Above threshold the compressor applies a 1/R slope, pulling loud parts down.",
            ),
            q(
                "A limiter is essentially a compressor with which setting?",
                (
                    opt("A ratio of 1:1"),
                    opt("A very high (effectively infinite) ratio", correct=True),
                    opt("No threshold at all"),
                    opt("A negative gain below threshold"),
                ),
                "A limiter is a compressor with an effectively infinite ratio — a brick-wall on peaks.",
            ),
        ),
        "Speech production: the source-filter model & formants": (
            q(
                "In the source-filter model, what is the 'source' for a voiced sound?",
                (
                    opt("The resonances of the mouth"),
                    opt(
                        "The buzz of the vibrating vocal folds at the fundamental frequency",
                        correct=True,
                    ),
                    opt("Turbulent noise at the lips"),
                    opt("The radiated speech itself"),
                ),
                "For voiced sounds the source is the vocal-fold buzz at f0; the tract filters it.",
            ),
            q(
                "What are formants?",
                (
                    opt("The harmonics of the vocal-fold buzz"),
                    opt(
                        "Resonance peaks of the vocal tract that define which vowel you hear",
                        correct=True,
                    ),
                    opt("The sample rate of the recording"),
                    opt("The decay time of a room"),
                ),
                "Formants are vocal-tract resonance peaks (F1, F2, ...) that distinguish vowels.",
            ),
            q(
                "What plays the role of the 'filter' in the source-filter model?",
                (
                    opt("The lungs"),
                    opt("The vocal folds"),
                    opt("The vocal tract (throat, mouth, nasal cavity)", correct=True),
                    opt("The eardrum"),
                ),
                "The vocal tract is the acoustic filter shaping the source into recognizable speech.",
            ),
        ),
        "Pitch & fundamental-frequency estimation": (
            q(
                "What does the fundamental frequency f0 of a voiced sound correspond to?",
                (
                    opt("The loudness of the sound"),
                    opt("The vocal-fold vibration rate, perceived as pitch", correct=True),
                    opt("The highest formant"),
                    opt("The sample rate"),
                ),
                "f0 is the vocal-fold vibration rate and drives the perceived pitch.",
            ),
            q(
                "How does an autocorrelation pitch estimator find the period?",
                (
                    opt("By counting zero crossings only"),
                    opt(
                        "It finds the lag of the first strong correlation peak after lag zero",
                        correct=True,
                    ),
                    opt("By measuring the loudest formant"),
                    opt("By taking the log of the sample rate"),
                ),
                "Autocorrelation peaks again at the pitch period; that lag gives T0 = 1/f0.",
            ),
            q(
                "What is a common failure mode of pitch estimators?",
                (
                    opt("Always reporting zero"),
                    opt("Octave errors — picking 2*f0 or f0/2", correct=True),
                    opt("Reversing the time axis"),
                    opt("Increasing the bit depth"),
                ),
                "Octave errors (choosing a harmonic or sub-harmonic) are a classic pitch-tracking mistake.",
            ),
        ),
    },
    final=(
        q(
            "What is the core idea of the short-time Fourier transform?",
            (
                opt("FFT the entire signal once for maximum resolution"),
                opt(
                    "FFT short, overlapping, windowed frames to track frequencies over time",
                    correct=True,
                ),
                opt("Replace the FFT with autocorrelation"),
                opt("Increase the bit depth before analysis"),
            ),
            "The STFT analyses short windowed frames so the spectrum can be followed through time.",
        ),
        q(
            "Why do we window each frame before the FFT?",
            (
                opt("To increase the sample rate"),
                opt("To reduce spectral leakage from abrupt frame edges", correct=True),
                opt("To remove the need for the FFT"),
                opt("To convert the signal to analog"),
            ),
            "Tapering windows soften frame edges and cut the leakage caused by hard cuts.",
        ),
        q(
            "Which choice correctly contrasts FIR and IIR filters?",
            (
                opt("FIR uses feedback; IIR does not"),
                opt(
                    "FIR is always stable and can be linear-phase; IIR is efficient but can be unstable",
                    correct=True,
                ),
                opt("IIR can only be analog; FIR only digital"),
                opt("FIR always needs fewer taps than IIR"),
            ),
            "FIR: always stable, can be linear-phase, more taps. IIR: efficient via feedback, possibly unstable.",
        ),
        q(
            "What does a dynamic-range compressor do?",
            (
                opt("Shapes the spectrum like an EQ"),
                opt(
                    "Reduces gain above a threshold, narrowing the level range so the whole signal can be louder",
                    correct=True,
                ),
                opt("Adds reflections to simulate a room"),
                opt("Estimates the pitch of speech"),
            ),
            "A compressor reduces gain above a threshold by ratio R, narrowing dynamic range.",
        ),
        q(
            "In the source-filter model, what determines which vowel is heard?",
            (
                opt("The fundamental frequency f0"),
                opt("The positions of the vocal-tract resonances (formants)", correct=True),
                opt("The loudness in decibels"),
                opt("The sample rate of the recording"),
            ),
            "Vowels are distinguished by their formant (vocal-tract resonance) positions, not by f0.",
        ),
        q(
            "Which technique estimates the fundamental frequency by exploiting near-periodicity?",
            (
                opt("Quantization"),
                opt("Autocorrelation (or the cepstrum / YIN)", correct=True),
                opt("Anti-aliasing"),
                opt("Shelving EQ"),
            ),
            "Autocorrelation, cepstrum and YIN exploit the quasi-periodicity of voiced speech to find f0.",
        ),
    ),
)
