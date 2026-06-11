from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Discrete-time signals & systems": (
            q(
                "What does the Nyquist-Shannon theorem require to capture a signal with no frequency above f_max?",
                (
                    opt("Sample at exactly f_max"),
                    opt("Sample faster than twice f_max, fs > 2 f_max", correct=True),
                    opt("Sample slower than f_max"),
                    opt("Sample at any rate as long as a filter is used"),
                ),
                "To capture a signal with no frequency above f_max you must sample faster than twice that, fs > 2 f_max; breaking the rule causes aliasing.",
            ),
            q(
                "An LTI system is completely described by which quantity?",
                (
                    opt("Its step response to u[n]"),
                    opt("Its impulse response h[n]", correct=True),
                    opt("Its largest output sample"),
                    opt("Its sampling rate fs"),
                ),
                "An LTI system is completely described by its impulse response h[n]; poke it with the unit impulse and any output is the input convolved with h[n].",
            ),
            q(
                "Why put an anti-aliasing filter in front of the ADC?",
                (
                    opt("Because aliasing cannot be undone after sampling", correct=True),
                    opt("To increase the sampling rate automatically"),
                    opt("To remove the DC component of every signal"),
                    opt("To convert the signal back to continuous time"),
                ),
                "Aliasing cannot be undone after sampling, so an anti-aliasing filter must ensure nothing above fs/2 reaches the ADC.",
            ),
        ),
        "Convolution & difference equations": (
            q(
                "In convolution, what operations are applied to the impulse response h relative to the input x?",
                (
                    opt("Differentiate h then add it to x"),
                    opt(
                        "Flip h, slide it across x, and at each position multiply and sum the overlap",
                        correct=True,
                    ),
                    opt("Square h then multiply by x"),
                    opt("Reverse x while holding h fixed and subtract"),
                ),
                "Convolution flips h, slides it across x, and at each position multiplies and sums the overlap.",
            ),
            q(
                "What distinguishes a FIR filter from an IIR filter in a difference equation?",
                (
                    opt(
                        "FIR has all feedback coefficients a_k zero (no feedback); IIR has some a_k nonzero (feedback)",
                        correct=True,
                    ),
                    opt("FIR always uses more coefficients than IIR"),
                    opt("FIR feeds the output back while IIR does not"),
                    opt("IIR is always linear phase while FIR is not"),
                ),
                "If all a_k are zero the output is a finite sum of inputs, a FIR filter; if some a_k are nonzero the output feeds back, an IIR filter whose h[n] rings on forever.",
            ),
            q(
                "Which statement about FIR versus IIR filters is correct per the lesson?",
                (
                    opt("FIR filters can go unstable while IIR filters never can"),
                    opt(
                        "FIR filters are always stable and can have exactly linear phase; IIR do more with fewer coefficients but can go unstable",
                        correct=True,
                    ),
                    opt("IIR filters always have linear phase"),
                    opt("FIR filters need fewer coefficients than IIR for the same sharpness"),
                ),
                "FIR filters are always stable and can have exactly linear phase; IIR filters do far more with fewer coefficients but can go unstable and distort phase.",
            ),
        ),
        "The z-transform & the system function": (
            q(
                "Under the z-transform, a one-sample delay x[n-1] becomes which expression?",
                (
                    opt("z X(z)"),
                    opt("z^-1 X(z)", correct=True),
                    opt("X(z) / n"),
                    opt("e^jw X(z)"),
                ),
                "The magic substitution is the delay: a one-sample delay x[n-1] becomes z^-1 X(z), turning difference equations into ratios of polynomials.",
            ),
            q(
                "When is a causal system stable in terms of its poles?",
                (
                    opt(
                        "If and only if every pole is inside the unit circle, |z| < 1", correct=True
                    ),
                    opt("If and only if every pole is outside the unit circle"),
                    opt("If at least one pole lies on the unit circle"),
                    opt("If all zeros are inside the unit circle"),
                ),
                "A causal system is stable if and only if every pole is inside the unit circle (|z| < 1); a pole on or outside it makes the impulse response stop decaying.",
            ),
            q(
                "How do you obtain the frequency response from the system function H(z)?",
                (
                    opt("Set z = 0 in H(z)"),
                    opt("Evaluate H(z) on the unit circle, z = e^jw", correct=True),
                    opt("Take the derivative of H(z) at z = 1"),
                    opt("Sum the poles and zeros of H(z)"),
                ),
                "Evaluating H(z) on the unit circle, z = e^jw, gives the frequency response, the gain and phase applied at each frequency.",
            ),
        ),
        "The DFT & FFT": (
            q(
                "What is the frequency resolution (bin spacing) of an N-point DFT at sampling rate fs?",
                (
                    opt("fs / N", correct=True),
                    opt("N / fs"),
                    opt("fs * N"),
                    opt("2 fs / N"),
                ),
                "The bin spacing is delta f = fs/N, which is the frequency resolution; collecting more samples (bigger N) gives finer resolution.",
            ),
            q(
                "What is the computational cost advantage of the FFT over a direct DFT?",
                (
                    opt("O(N) instead of O(log N)"),
                    opt("O(N log N) instead of O(N^2)", correct=True),
                    opt("O(N^2) instead of O(N log N)"),
                    opt("O(1) regardless of N"),
                ),
                "A direct DFT costs O(N^2) multiplications, while the FFT computes the same result in O(N log N) by recursively splitting the sum.",
            ),
            q(
                "To get finer frequency resolution, the lesson advises you to do what?",
                (
                    opt("Sample faster with the same N"),
                    opt("Record longer (use a bigger N)", correct=True),
                    opt("Use a smaller record length"),
                    opt("Increase the amplitude of the tone"),
                ),
                "Resolution is fs/N, so to get finer resolution you should record longer (bigger N), not just sample faster, which only spreads the same bins over a wider range.",
            ),
        ),
        "Spectral analysis in practice": (
            q(
                "What causes spectral leakage in the DFT?",
                (
                    opt("The signal having too low an amplitude"),
                    opt(
                        "A discontinuity at the wrap-around when the tone does not fit a whole number of cycles",
                        correct=True,
                    ),
                    opt("Using a power-of-2 record length"),
                    opt("Sampling above the Nyquist rate"),
                ),
                "The DFT assumes the N samples are one period of a periodic signal; when a tone does not fit a whole number of cycles it sees a discontinuity at the wrap-around and energy smears across bins.",
            ),
            q(
                "What is the fundamental trade-off when applying a tapered window?",
                (
                    opt(
                        "Lower side lobes (less leakage) at the cost of a wider main lobe (less ability to separate close tones)",
                        correct=True,
                    ),
                    opt("Higher side lobes in exchange for a narrower main lobe"),
                    opt("More frequency resolution at the cost of amplitude accuracy"),
                    opt("Faster FFT at the cost of more memory"),
                ),
                "A tapered window lowers the side lobes (less leakage) at the cost of a wider main lobe, meaning less ability to separate two close tones.",
            ),
            q(
                "What does zero-padding before the FFT actually do?",
                (
                    opt("Adds real frequency resolution by recording more data"),
                    opt(
                        "Interpolates the existing spectrum onto a finer grid without adding information",
                        correct=True,
                    ),
                    opt("Removes spectral leakage entirely"),
                    opt("Separates two tones the record length cannot resolve"),
                ),
                "Appending zeros does not add information or resolution; it interpolates the existing spectrum onto a finer grid and cannot separate tones the record length cannot resolve.",
            ),
        ),
        "Lab: compute an FFT with windowing": (
            q(
                "In the lab, what does applying the Hann window accomplish for the two-tone signal?",
                (
                    opt("It removes the strong 100 Hz tone"),
                    opt(
                        "It tames leakage so the weak 120 Hz tone next to the strong one shows up",
                        correct=True,
                    ),
                    opt("It doubles the frequency resolution"),
                    opt("It eliminates the broadband noise completely"),
                ),
                "The lab shows a Hann window taming leakage so the weak tone next to the strong one emerges, whereas the rectangular case hides the 120 Hz tone in leakage.",
            ),
            q(
                "How does the lab compute the frequency resolution df?",
                (
                    opt("df = N / fs"),
                    opt("df = fs / N", correct=True),
                    opt("df = fs * N"),
                    opt("df = 1 / N"),
                ),
                "The lab computes df = fs / N as the bin resolution and prints it; doubling N to 1024 halves df and sharpens the peaks.",
            ),
            q(
                "According to the lab's try-it-yourself notes, what happens if you drop the window and use x instead of x*w?",
                (
                    opt("The 120 Hz tone vanishes in leakage", correct=True),
                    opt("The resolution df is halved"),
                    opt("The strong 100 Hz tone disappears"),
                    opt("The noise floor drops by 6 dB"),
                ),
                "The first try-it-yourself step notes that dropping the window (using x instead of x*w) makes the 120 Hz tone vanish in leakage.",
            ),
        ),
    },
    final=(
        q(
            "Which sampling rule keeps sampling safe and prevents aliasing?",
            (
                opt("Sample slower than f_max"),
                opt("Sample faster than twice the highest frequency, fs > 2 f_max", correct=True),
                opt("Sample at exactly the Nyquist frequency"),
                opt("Sample at the DC component only"),
            ),
            "Nyquist-Shannon requires fs > 2 f_max; otherwise high frequencies alias as low ones, and aliasing cannot be undone after sampling.",
        ),
        q(
            "An LTI system's output equals which operation between the input and its impulse response?",
            (
                opt("The product x[n] times h[n]"),
                opt("The convolution of x[n] with h[n]", correct=True),
                opt("The sum x[n] plus h[n]"),
                opt("The ratio x[n] over h[n]"),
            ),
            "An LTI system's output is the input convolved with its impulse response: y[n] = (x * h)[n].",
        ),
        q(
            "In the z-plane, a causal system is stable when its poles are located where?",
            (
                opt("Inside the unit circle, |z| < 1", correct=True),
                opt("Outside the unit circle, |z| > 1"),
                opt("Exactly on the unit circle"),
                opt("At the origin only"),
            ),
            "Stability lives inside the unit circle: a causal system is stable if and only if every pole satisfies |z| < 1.",
        ),
        q(
            "Why was the FFT so transformative compared to the direct DFT?",
            (
                opt("It produces a different result that is more accurate"),
                opt("It computes the same result in O(N log N) instead of O(N^2)", correct=True),
                opt("It removes the need for any sampling"),
                opt("It increases frequency resolution without more samples"),
            ),
            "The FFT computes the same DFT result in O(N log N) instead of the direct DFT's O(N^2), a massive speedup for large N.",
        ),
        q(
            "For general-purpose spectral analysis of real-world data, which window does the lesson recommend as the safe default?",
            (
                opt("Rectangular (no taper)"),
                opt("Hann", correct=True),
                opt("Flat-top"),
                opt("No window at all"),
            ),
            "The lesson recommends defaulting to a Hann window for general analysis, flat-top for accurate amplitudes, and rectangular only to resolve two equal close tones.",
        ),
    ),
)
