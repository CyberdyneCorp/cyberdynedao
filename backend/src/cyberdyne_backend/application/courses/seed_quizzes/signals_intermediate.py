from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Systems & their properties": (
            q(
                "What two properties together define an LTI system?",
                (
                    opt("Causal and stable"),
                    opt("Linear and time-invariant", correct=True),
                    opt("Bounded and periodic"),
                    opt("Continuous and discrete"),
                ),
                "LTI stands for linear and time-invariant, the class the course is built around.",
            ),
            q(
                "Which property does the system y = x^2 fail?",
                (
                    opt("Linearity, because superposition does not hold", correct=True),
                    opt("Time-invariance, because behaviour drifts in time"),
                    opt("Causality, because it uses future inputs"),
                    opt("Stability, because bounded inputs blow up"),
                ),
                "Squaring breaks superposition, so it is nonlinear.",
            ),
            q(
                "Why is the LTI class so important?",
                (
                    opt("It is the only class of systems that is causal"),
                    opt("Its inputs are always bounded"),
                    opt(
                        "It is fully described by its impulse response and acts as multiplication in frequency",
                        correct=True,
                    ),
                    opt("It never has any output delay"),
                ),
                "An LTI system is completely described by one signal, its impulse response, and multiplies in the frequency domain.",
            ),
        ),
        "Impulse response & convolution": (
            q(
                "What is the impulse response of an LTI system?",
                (
                    opt("The output when the input is an impulse", correct=True),
                    opt("The output when the input is a step"),
                    opt("The frequency where the system peaks"),
                    opt("The delay between input and output"),
                ),
                "The impulse response h is what comes out when the system is hit with an impulse.",
            ),
            q(
                "How is the output of an LTI system computed from any input?",
                (
                    opt("By multiplying the input by a constant gain"),
                    opt("By convolving the input with the impulse response", correct=True),
                    opt("By adding the impulse response to the input"),
                    opt("By taking the derivative of the input"),
                ),
                "For any input, the output is the input convolved with the impulse response h.",
            ),
            q(
                "Convolution can be described as which sequence of steps on h?",
                (
                    opt("Differentiate, integrate, then add"),
                    opt("Scale, square, then sum"),
                    opt(
                        "Flip h, slide it across x, and multiply-and-sum the overlap", correct=True
                    ),
                    opt("Delay h, invert it, then subtract"),
                ),
                "Convolution flips h, slides it across x, and at each position multiplies and sums the overlap.",
            ),
        ),
        "Fourier series: building signals from sinusoids": (
            q(
                "According to Fourier, any periodic signal can be written as a sum of what?",
                (
                    opt("Impulses at random times"),
                    opt("Sinusoids at harmonics of the fundamental frequency", correct=True),
                    opt("Exponentially decaying pulses"),
                    opt("Constant DC offsets only"),
                ),
                "Fourier showed a periodic signal is a sum of sinusoids at multiples of its fundamental frequency.",
            ),
            q(
                "Which harmonics appear in the Fourier series of a square wave?",
                (
                    opt("Only the fundamental"),
                    opt("All integer harmonics"),
                    opt("Only even harmonics"),
                    opt("Only odd harmonics with shrinking amplitude", correct=True),
                ),
                "A square wave is built from odd harmonics with coefficients 1/k that shrink as k grows.",
            ),
            q(
                "What is the Gibbs phenomenon?",
                (
                    opt("An overshoot near the edges that never fully disappears", correct=True),
                    opt("The loss of the fundamental frequency"),
                    opt("An infinite delay in the partial sum"),
                    opt("The doubling of the signal period"),
                ),
                "The Gibbs phenomenon is the persistent overshoot at sharp edges of the partial sum.",
            ),
        ),
        "The Fourier transform & the spectrum": (
            q(
                "What does the Fourier transform produce from a time signal?",
                (
                    opt("Its frequency content", correct=True),
                    opt("Its impulse response"),
                    opt("Its time derivative"),
                    opt("Its running average"),
                ),
                "The Fourier transform turns a time signal into its frequency content.",
            ),
            q(
                "On a computer the DFT is computed quickly by which algorithm?",
                (
                    opt("The convolution algorithm"),
                    opt("The FFT", correct=True),
                    opt("The moving average"),
                    opt("Gaussian elimination"),
                ),
                "The DFT is computed fast by the FFT algorithm.",
            ),
            q(
                "For a real signal sampled at fs over N points, what is the bin spacing of the spectrum?",
                (
                    opt("fs times N"),
                    opt("N divided by fs"),
                    opt("fs divided by N", correct=True),
                    opt("fs divided by 2"),
                ),
                "Bin spacing is fs/N, while the highest representable frequency is fs/2 (Nyquist).",
            ),
        ),
        "Lab: the FFT of a signal": (
            q(
                "In the lab, why is np.fft.rfft used instead of np.fft.fft?",
                (
                    opt("It keeps only the positive frequencies of a real signal", correct=True),
                    opt("It runs convolution instead of a transform"),
                    opt("It doubles the sampling rate"),
                    opt("It removes the DC component automatically"),
                ),
                "For a real signal the spectrum is symmetric, so rfft keeps just the positive half.",
            ),
            q(
                "At which frequencies does the two-tone lab signal show spikes?",
                (
                    opt("5 Hz and 20 Hz", correct=True),
                    opt("1 Hz and 2 Hz"),
                    opt("50 Hz and 60 Hz"),
                    opt("250 Hz and 500 Hz"),
                ),
                "The lab signal is a sum of a 5 Hz tone and a 20 Hz tone, so it peaks at 5 and 20 Hz.",
            ),
            q(
                "With fs = 500, what is the Nyquist frequency reported by the lab?",
                (
                    opt("100 Hz"),
                    opt("500 Hz"),
                    opt("250 Hz", correct=True),
                    opt("40 Hz"),
                ),
                "Nyquist is fs/2, which is 500/2 = 250 Hz.",
            ),
        ),
        "Filtering basics": (
            q(
                "What is a filter in signal processing terms?",
                (
                    opt(
                        "An LTI system that keeps some frequencies and rejects others", correct=True
                    ),
                    opt("A nonlinear squaring device"),
                    opt("A transform that removes the time axis"),
                    opt("A system that only delays the input"),
                ),
                "A filter is an LTI system that keeps some frequencies and rejects others.",
            ),
            q(
                "Which filter type is used to kill 50/60 Hz mains hum?",
                (
                    opt("Low-pass"),
                    opt("High-pass"),
                    opt("Band-stop (notch)", correct=True),
                    opt("All-pass"),
                ),
                "A band-stop or notch filter passes everything except a narrow band, ideal for mains hum.",
            ),
            q(
                "A moving-average filter acts as which kind of filter?",
                (
                    opt("High-pass"),
                    opt("Band-pass"),
                    opt("Low-pass", correct=True),
                    opt("Band-stop"),
                ),
                "Averaging neighbours smooths fast wiggles while keeping the slow trend, so it is a low-pass filter.",
            ),
        ),
    },
    final=(
        q(
            "Which pair of properties makes a system LTI?",
            (
                opt("Causal and stable"),
                opt("Linear and time-invariant", correct=True),
                opt("Periodic and bounded"),
                opt("Real and even"),
            ),
            "LTI means linear and time-invariant.",
        ),
        q(
            "The output of an LTI system equals the input convolved with what?",
            (
                opt("Its impulse response", correct=True),
                opt("Its Fourier series"),
                opt("Its Nyquist frequency"),
                opt("Its DC offset"),
            ),
            "Any LTI output is the input convolved with the impulse response h.",
        ),
        q(
            "Convolution in time corresponds to what operation in the frequency domain?",
            (
                opt("Addition of spectra"),
                opt("Multiplication of spectra", correct=True),
                opt("Subtraction of spectra"),
                opt("Differentiation of spectra"),
            ),
            "The convolution theorem says convolving in time equals multiplying spectra.",
        ),
        q(
            "What does the magnitude spectrum |X(f)| from an FFT show?",
            (
                opt("The strength of each frequency in the signal", correct=True),
                opt("The impulse response over time"),
                opt("The phase delay of the system"),
                opt("The sampling rate of the signal"),
            ),
            "The magnitude spectrum shows the strength of each frequency present in the signal.",
        ),
        q(
            "A long-window moving-average low-pass filter has what main drawback?",
            (
                opt("It amplifies high-frequency noise"),
                opt("It adds a DC offset"),
                opt("It lags more and blurs real features", correct=True),
                opt("It is not an LTI system"),
            ),
            "A longer window smooths more but lags and blurs real features, a trade-off made in the frequency domain.",
        ),
    ),
)
