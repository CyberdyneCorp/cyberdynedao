from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Signals, sinusoids & complex exponentials": (
            q(
                "In the sinusoid x(t) = A cos(wt + phi), what does the symbol A represent?",
                (
                    opt("The phase"),
                    opt("The amplitude", correct=True),
                    opt("The angular frequency"),
                    opt("The period"),
                ),
                "In x(t) = A cos(wt + phi), A is the amplitude of the sinusoid.",
            ),
            q(
                "What does Euler's formula e^(i*theta) equal?",
                (
                    opt("cos(theta) - i sin(theta)"),
                    opt("sin(theta) + i cos(theta)"),
                    opt("cos(theta) + i sin(theta)", correct=True),
                    opt("i cos(theta) - sin(theta)"),
                ),
                "Euler's formula states e^(i*theta) = cos(theta) + i sin(theta).",
            ),
            q(
                "The lesson describes a sinusoid as the shadow of a spinning phasor. Which part of the rotating complex exponential gives the cosine?",
                (
                    opt("The imaginary part"),
                    opt("The magnitude"),
                    opt("The real (horizontal) part", correct=True),
                    opt("The phase angle"),
                ),
                "A sinusoid is the real part (the horizontal shadow) of the rotating phasor, tracing a cosine.",
            ),
        ),
        "Fourier series: building waves from sinusoids": (
            q(
                "According to Fourier's idea, any periodic signal can be written as a sum of what?",
                (
                    opt("Sinusoids: a fundamental plus its harmonics", correct=True),
                    opt("Random noise samples"),
                    opt("Exponentially decaying pulses"),
                    opt("Straight line segments"),
                ),
                "Fourier's idea is that any periodic signal is a sum of sinusoids, a fundamental plus its harmonics.",
            ),
            q(
                "A square wave is built from which harmonics?",
                (
                    opt("Only the fundamental"),
                    opt("The even harmonics"),
                    opt("The odd harmonics", correct=True),
                    opt("All harmonics with equal weight"),
                ),
                "The lesson shows a square wave is built from the odd harmonics (sin t, sin 3t, sin 5t, ...).",
            ),
            q(
                "What is the name of the little overshoot at the edges that never quite goes away as harmonics are added?",
                (
                    opt("The Nyquist effect"),
                    opt("The Gibbs phenomenon", correct=True),
                    opt("Aliasing"),
                    opt("The Euler ripple"),
                ),
                "The persistent overshoot at the corners of the partial sums is called the Gibbs phenomenon.",
            ),
        ),
        "The Fourier transform & the frequency domain": (
            q(
                "What does the Fourier transform do to a signal?",
                (
                    opt("It rewrites a function of time as a function of frequency", correct=True),
                    opt("It removes all high frequencies from the signal"),
                    opt("It converts a frequency spectrum back into samples"),
                    opt("It doubles the amplitude of every harmonic"),
                ),
                "The Fourier transform rewrites a function of time as a function of frequency, revealing which frequencies it contains.",
            ),
            q(
                "For a signal that is the sum of two tones, what does its spectrum look like?",
                (
                    opt("A single broad hump"),
                    opt(
                        "Two spikes at those frequencies with heights equal to the amplitudes",
                        correct=True,
                    ),
                    opt("A flat line at zero"),
                    opt("A smooth rising ramp"),
                ),
                "The spectrum of a two-tone signal shows exactly two spikes at those frequencies, with heights equal to the amplitudes.",
            ),
            q(
                "Which application is given as an example of using the frequency domain?",
                (
                    opt("Sorting a list of numbers"),
                    opt("Allocating memory on a heap"),
                    opt(
                        "JPEG/MP3 compression by dropping inaudible or invisible frequencies",
                        correct=True,
                    ),
                    opt("Encrypting a password hash"),
                ),
                "The frequency domain powers JPEG/MP3 compression, which drops the inaudible or invisible frequencies.",
            ),
        ),
        "Sampling, the DFT & aliasing": (
            q(
                "How do computers store signals according to the lesson?",
                (
                    opt("As continuous analog waveforms"),
                    opt("As samples taken every Ts seconds", correct=True),
                    opt("As a single average value"),
                    opt("As Fourier coefficients only"),
                ),
                "Computers store signals as samples taken every Ts seconds, where the sample rate is fs = 1/Ts.",
            ),
            q(
                "What is the Nyquist frequency, the highest frequency you can faithfully capture?",
                (
                    opt("Twice the sample rate"),
                    opt("The full sample rate fs"),
                    opt("Half the sample rate, fs/2", correct=True),
                    opt("One quarter of the sample rate"),
                ),
                "You can only faithfully capture frequencies below half the sample rate (fs/2), the Nyquist frequency.",
            ),
            q(
                "How much faster is the FFT than the naive DFT computation?",
                (
                    opt("It runs in O(N log N) instead of O(N^2)", correct=True),
                    opt("It runs in O(N) instead of O(N log N)"),
                    opt("It runs in O(N^2) instead of O(N^3)"),
                    opt("It runs in O(1) instead of O(N)"),
                ),
                "The FFT computes the DFT in O(N log N) instead of O(N^2).",
            ),
        ),
        "Filtering & convolution": (
            q(
                "What does a low-pass filter do?",
                (
                    opt("Sharpens by removing slow drift"),
                    opt("Smooths by removing high-frequency noise", correct=True),
                    opt("Isolates a narrow band of frequencies"),
                    opt("Amplifies every frequency equally"),
                ),
                "A low-pass filter smooths a signal by removing high-frequency noise.",
            ),
            q(
                "In the time domain, a linear time-invariant filter is described as which operation?",
                (
                    opt("Convolution with the filter's impulse response", correct=True),
                    opt("Differentiation of the signal"),
                    opt("Multiplication by a constant gain"),
                    opt("Addition of white noise"),
                ),
                "In the time domain an LTI filter is convolution with the filter's impulse response h.",
            ),
            q(
                "What is the central theorem stated to tie the course together?",
                (
                    opt("Multiplication in time equals addition in frequency"),
                    opt("Convolution in time equals multiplication in frequency", correct=True),
                    opt("Sampling in time equals filtering in frequency"),
                    opt("Convolution in frequency equals addition in time"),
                ),
                "The central theorem is that convolution in time equals multiplication in frequency.",
            ),
        ),
        "Signals lab: filter a signal & find its period": (
            q(
                "Which filter does the lab use to smooth the signal as a low-pass filter?",
                (
                    opt("A moving average over a window of 3 samples", correct=True),
                    opt("A high-pass differencing filter"),
                    opt("A median filter over 5 samples"),
                    opt("An exponential decay filter"),
                ),
                "The lab uses a moving-average low-pass filter with window 3, a convolution with [1/3, 1/3, 1/3].",
            ),
            q(
                "How does the lab find the period of the signal?",
                (
                    opt("By counting zero crossings"),
                    opt(
                        "By finding the lag that best matches the signal to a shifted copy of itself",
                        correct=True,
                    ),
                    opt("By taking the maximum sample value"),
                    opt("By summing all the samples"),
                ),
                "The lag that best matches the signal to a shifted copy of itself, via the average squared difference, is the period.",
            ),
            q(
                "Before the period analysis, what does the lab do to the signal?",
                (
                    opt("Normalises it to unit amplitude"),
                    opt("Centers it by subtracting its mean", correct=True),
                    opt("Squares every sample"),
                    opt("Reverses the sample order"),
                ),
                "The lab centers the signal by subtracting its mean before running the period analysis.",
            ),
        ),
    },
    final=(
        q(
            "What is Euler's formula, the basis for representing sinusoids as phasors?",
            (
                opt("e^(i*theta) = cos(theta) + i sin(theta)", correct=True),
                opt("e^(i*theta) = sin(theta) + i cos(theta)"),
                opt("e^(i*theta) = cos(theta) - i sin(theta)"),
                opt("e^(i*theta) = i cos(theta) + sin(theta)"),
            ),
            "Euler's formula e^(i*theta) = cos(theta) + i sin(theta) packs cosine and sine into one rotating exponential.",
        ),
        q(
            "A Fourier series builds a periodic signal from a fundamental plus its harmonics. What are harmonics?",
            (
                opt("Random frequencies unrelated to the base"),
                opt("Integer multiples of the base frequency", correct=True),
                opt("Half the base frequency"),
                opt("The decaying envelope of the signal"),
            ),
            "Harmonics are integer multiples of the base (fundamental) frequency.",
        ),
        q(
            "Sampling a high frequency too slowly makes it masquerade as a low one. What is this called?",
            (
                opt("The Gibbs phenomenon"),
                opt("Convolution"),
                opt("Aliasing", correct=True),
                opt("Quantization"),
            ),
            "Sampling below the Nyquist rate causes aliasing, where a high frequency masquerades as a low one.",
        ),
        q(
            "Which statement is the central theorem connecting filtering, convolution and the frequency domain?",
            (
                opt("Convolution in time equals multiplication in frequency", correct=True),
                opt("The FFT is O(N^2)"),
                opt("Entropy is the limit of lossless compression"),
                opt("Amplitude equals angular frequency"),
            ),
            "Convolution in time equals multiplication in frequency, the theorem that ties the course together.",
        ),
        q(
            "The Fourier transform reveals what about a signal?",
            (
                opt("Its total duration in seconds"),
                opt("Which frequencies it contains", correct=True),
                opt("Its average sample value"),
                opt("The number of samples stored"),
            ),
            "The Fourier transform rewrites a time signal as a function of frequency, revealing which frequencies it contains.",
        ),
    ),
)
