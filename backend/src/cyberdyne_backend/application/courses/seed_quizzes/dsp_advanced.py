from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Adaptive filters: LMS & RLS": (
            q(
                "What defines an adaptive filter as opposed to a fixed filter?",
                (
                    opt("It has a longer impulse response"),
                    opt(
                        "It learns and adjusts its own coefficients in real time to minimise an error",
                        correct=True,
                    ),
                    opt("It always uses floating-point arithmetic"),
                    opt("It only operates in the frequency domain"),
                ),
                "An adaptive filter identifies the environment as it runs, nudging its weights to shrink the error.",
            ),
            q(
                "In the LMS update w[n+1] = w[n] + mu*e[n]*x[n], what role does the step size mu play?",
                (
                    opt("It sets the number of filter taps"),
                    opt("It only affects steady-state bias, never convergence"),
                    opt(
                        "Too small and it crawls; too large and it overshoots or diverges",
                        correct=True,
                    ),
                    opt("It is the desired signal d[n]"),
                ),
                "The step size mu is the whole game for LMS: it trades convergence speed against stability.",
            ),
            q(
                "How does RLS compare to LMS in cost and convergence?",
                (
                    opt("RLS is cheaper per sample and converges slower"),
                    opt(
                        "RLS converges in far fewer iterations at O(L^2) cost per sample versus LMS's O(L)",
                        correct=True,
                    ),
                    opt("RLS and LMS have identical per-sample cost"),
                    opt("RLS cannot be used for channel equalization"),
                ),
                "RLS uses the full correlation history to converge fast, but costs O(L^2) per sample against LMS's O(L).",
            ),
        ),
        "Spectral estimation": (
            q(
                "What is the fatal flaw of the raw periodogram?",
                (
                    opt("It cannot be computed with an FFT"),
                    opt("It always underestimates total power"),
                    opt(
                        "Its variance does not shrink as you collect more data",
                        correct=True,
                    ),
                    opt("It requires a parametric model to evaluate"),
                ),
                "More samples give finer resolution but an equally jagged, noisy estimate, so you must average.",
            ),
            q(
                "How does Welch's method reduce the variance of the spectrum estimate?",
                (
                    opt("By fitting an all-pole model to the data"),
                    opt(
                        "By chopping into overlapping segments, windowing, and averaging the periodograms",
                        correct=True,
                    ),
                    opt("By zero-padding a single long FFT"),
                    opt("By using subspace decomposition"),
                ),
                "Averaging K segments cuts the variance by about K, at the cost of coarser frequency resolution.",
            ),
            q(
                "What characterizes parametric autoregressive (AR) spectral estimation?",
                (
                    opt("It never produces false peaks regardless of model order"),
                    opt("It requires very long records to give any peaks"),
                    opt(
                        "It models the signal as white noise through an all-pole filter and gives sharp peaks from short records",
                        correct=True,
                    ),
                    opt("It is identical to Welch's method"),
                ),
                "AR methods solve Yule-Walker (or Burg) for the coefficients and can hallucinate peaks if the model order is wrong.",
            ),
        ),
        "DSP for communications": (
            q(
                "What is the matched filter optimal for, and what is its impulse response?",
                (
                    opt("Minimising latency; a unit impulse"),
                    opt(
                        "Maximising SNR at the sampling instant; the time-reversed transmit pulse",
                        correct=True,
                    ),
                    opt("Flattening the spectrum; a differentiator"),
                    opt("Removing DC offset; a highpass filter"),
                ),
                "The matched filter h[n] = s[-n] maximises output SNR and is the optimal linear detector in white noise.",
            ),
            q(
                "What does an equalizer do, and what problem does it address?",
                (
                    opt("It amplifies the carrier; it fixes timing errors"),
                    opt("It generates the transmit pulse; it sets the symbol rate"),
                    opt(
                        "It inverts the channel to reopen the eye; it counters inter-symbol interference (ISI)",
                        correct=True,
                    ),
                    opt("It downconverts RF; it removes thermal noise"),
                ),
                "A real channel smears each symbol into the next (ISI); an adaptive equalizer inverts the channel.",
            ),
            q(
                "What is the correct order of operations in the receiver chain?",
                (
                    opt("Decide, then equalize, then synchronize, then matched filter"),
                    opt(
                        "Matched filter, then synchronize, then equalize, then decide",
                        correct=True,
                    ),
                    opt("Equalize, then matched filter, then decide, then synchronize"),
                    opt("Synchronize, then decide, then matched filter, then equalize"),
                ),
                "The receiver chain is an order of operations: matched filter, then sync, then equalize, then decide.",
            ),
        ),
        "Real-time & embedded DSP": (
            q(
                "What is the multiply-accumulate (MAC) and why is it central to DSP hardware?",
                (
                    opt("A memory-access pattern that avoids cache misses"),
                    opt(
                        "The inner loop acc += h[k]*x[n-k], which DSP processors do in one cycle, often in parallel",
                        correct=True,
                    ),
                    opt("A floating-point-only instruction unavailable on MCUs"),
                    opt("A method for carrier recovery in receivers"),
                ),
                "The MAC unit multiplies and adds in a single instruction with a wide accumulator to avoid overflow.",
            ),
            q(
                "What is the trade-off when processing in blocks rather than sample-by-sample?",
                (
                    opt("Blocks reduce both latency and efficiency"),
                    opt("Blocks increase per-sample overhead with no benefit"),
                    opt(
                        "Blocks amortise overhead and unlock FFT fast convolution and SIMD, but a block of B samples adds B/fs of latency",
                        correct=True,
                    ),
                    opt("Sample-by-sample processing always has higher latency"),
                ),
                "Block processing trades added latency (B/fs) for efficiency via fast convolution and SIMD.",
            ),
            q(
                "How do fixed-point and floating-point implementations compare on real hardware?",
                (
                    opt("Fixed-point costs more power but never overflows"),
                    opt(
                        "Fixed-point is cheaper and lower power but needs careful scaling; floating-point frees you from scaling at higher power",
                        correct=True,
                    ),
                    opt("Floating-point is always cheaper than fixed-point"),
                    opt("Both have identical power and scaling characteristics"),
                ),
                "Fixed-point suits billions of low-power devices but needs scaling; floating-point avoids overflow at higher power cost.",
            ),
        ),
        "Multidimensional & modern DSP": (
            q(
                "How does 2-D DSP treat an image, and what does JPEG actually use?",
                (
                    opt("Images are 1-D signals; JPEG uses the wavelet transform"),
                    opt(
                        "An image is a 2-D signal with kernel convolution; JPEG uses the related DCT on 8x8 blocks",
                        correct=True,
                    ),
                    opt("Images cannot be convolved; JPEG uses the periodogram"),
                    opt("A Sobel kernel is a 2-D lowpass; JPEG uses raw FFT magnitudes"),
                ),
                "A blur is a 2-D lowpass, an edge detector is a 2-D highpass, and JPEG uses the DCT on 8x8 blocks.",
            ),
            q(
                "What advantage do wavelets give over the FFT?",
                (
                    opt("They eliminate the uncertainty principle entirely"),
                    opt("They give perfect frequency resolution at all scales"),
                    opt(
                        "A time-frequency view: good time resolution for high frequencies and good frequency resolution for low ones",
                        correct=True,
                    ),
                    opt("They only work on 2-D images, never time signals"),
                ),
                "The FFT tells you which frequencies are present but not when; wavelets give a time-frequency view, bounded by the uncertainty principle.",
            ),
            q(
                "How does the lesson connect a convolutional neural network to classical DSP?",
                (
                    opt("A CNN replaces convolution with matrix inversion"),
                    opt(
                        "A CNN is literally banks of learned FIR filters, with weights found by training instead of by design",
                        correct=True,
                    ),
                    opt("A CNN uses only the Yule-Walker equations"),
                    opt("A CNN avoids convolution altogether"),
                ),
                "A CNN is banks of learned FIR filters; MFCC front-ends are pure DSP feeding the model.",
            ),
        ),
        "Applications & the throughline": (
            q(
                "Which DSP technique does the lesson map to active-noise headphones?",
                (
                    opt("2-D DCT and motion-compensated prediction"),
                    opt(
                        "Adaptive filtering (NLMS) cancelling ambient noise in real time",
                        correct=True,
                    ),
                    opt("FFT-based OFDM and channel equalization"),
                    opt("Yule-Walker AR spectral estimation"),
                ),
                "Active-noise headphones use adaptive filtering (NLMS) to cancel ambient noise in real time.",
            ),
            q(
                "According to the throughline, what is the single most reusable operation across DSP?",
                (
                    opt("The Yule-Walker solve"),
                    opt("The phase-locked loop"),
                    opt(
                        "Convolution / filtering, which is the moving average, FIR filter, image kernel, and CNN layer",
                        correct=True,
                    ),
                    opt("Fixed-point scaling"),
                ),
                "Convolution / filtering is the same operation across the moving average, FIR filter, image kernel, and CNN layer.",
            ),
            q(
                "What does the lesson recommend as the fastest way to internalise DSP and find bugs?",
                (
                    opt("Increase the filter order until the spectrum is flat"),
                    opt("Switch all code to fixed-point"),
                    opt(
                        "Measure and plot at every stage: the time signal, then its spectrum, then the filtered result",
                        correct=True,
                    ),
                    opt("Avoid plotting and trust the numerical SNR alone"),
                ),
                "Most real bugs (aliasing, leakage, an unstable pole, fixed-point overflow) are obvious the moment you plot them.",
            ),
        ),
        "Lab: an LMS adaptive noise canceller": (
            q(
                "In the lab, what serves as the input to the adaptive FIR that estimates the noise at the mic?",
                (
                    opt("The clean 300 Hz signal"),
                    opt("The primary mic recording (signal + noise)"),
                    opt(
                        "The correlated noise reference (noise_ref)",
                        correct=True,
                    ),
                    opt("The unknown acoustic path coefficients"),
                ),
                "The reference noise (e.g. an outer mic) feeds the adaptive FIR, which predicts the noise at the main mic to subtract it.",
            ),
            q(
                "What does the error signal e[i] represent in this LMS noise canceller?",
                (
                    opt("The filter's estimate of the noise"),
                    opt(
                        "The cleaned output: the recovered signal plus residual",
                        correct=True,
                    ),
                    opt("The raw reference noise"),
                    opt("The acoustic path impulse response"),
                ),
                "e[i] = primary[i] - yhat[i] removes the estimated noise, leaving the recovered signal plus a residual.",
            ),
            q(
                "Per the lab's 'Try it yourself' notes, what happens if you shorten L to 4 (below the path length)?",
                (
                    opt("Convergence becomes faster with a cleaner steady state"),
                    opt(
                        "The filter cannot model the path, so cancellation gets worse",
                        correct=True,
                    ),
                    opt("The SNR improvement doubles"),
                    opt("The NLMS normalization is no longer needed"),
                ),
                "With L shorter than the path length, the adaptive FIR cannot model the path and cancellation degrades.",
            ),
        ),
    },
    final=(
        q(
            "Which pairing of algorithm and trade-off is correct?",
            (
                opt("RLS is O(L) per sample and converges slowly"),
                opt(
                    "LMS is cheap O(L) and robust; RLS converges faster at O(L^2) per sample",
                    correct=True,
                ),
                opt("Both LMS and RLS are O(L^2) per sample"),
                opt("LMS converges faster than RLS for the same cost"),
            ),
            "LMS is cheap and robust at O(L) per sample; RLS converges in fewer iterations at O(L^2) cost.",
        ),
        q(
            "For a robust general-purpose PSD estimate at a fixed record length, what does the course recommend?",
            (
                opt("Always use a single raw periodogram"),
                opt("Always use AR/MUSIC regardless of the signal"),
                opt(
                    "Use Welch, accepting that you cannot maximize both resolution and low variance at once",
                    correct=True,
                ),
                opt("Use the matched filter"),
            ),
            "Welch is the robust default; longer segments improve resolution and more segments reduce variance, but not both at once.",
        ),
        q(
            "Which describes the correct communications receiver order and the matched filter's purpose?",
            (
                opt("Equalize first; the matched filter sets the carrier frequency"),
                opt(
                    "Matched filter (max SNR), then synchronize, then equalize (undo ISI), then decide",
                    correct=True,
                ),
                opt("Decide first; the matched filter removes ISI"),
                opt("Synchronize last; the matched filter performs timing recovery"),
            ),
            "The chain is matched filter, sync, equalize, decide; the matched filter maximises SNR at the sampling instant.",
        ),
        q(
            "Which statement about real-time and modern DSP is correct?",
            (
                opt("Block processing reduces latency below sample-by-sample processing"),
                opt("A CNN abandons convolution in favour of model inversion"),
                opt(
                    "A block of B samples adds B/fs latency, and a CNN is banks of learned FIR filters",
                    correct=True,
                ),
                opt("MACs per second are irrelevant to whether a filter fits the budget"),
            ),
            "Blocks trade B/fs latency for efficiency, and a CNN is learned FIR filters: the same convolution used all course.",
        ),
        q(
            "What is the unifying throughline of the DSP track?",
            (
                opt("Every problem is best solved with a parametric AR model"),
                opt("Frequency-domain processing always beats time-domain"),
                opt(
                    "Sample (respect Nyquist), describe systems by impulse response and convolution, move to frequency with FFT, design and implement filters, then adapt, estimate spectra, and generalise to comms, real-time, images, and learned filters",
                    correct=True,
                ),
                opt("Fixed-point arithmetic is required for all DSP"),
            ),
            "The track is one story: sample, convolve, transform, design/implement, adapt, estimate spectra, and generalise to modern DSP.",
        ),
    ),
)
