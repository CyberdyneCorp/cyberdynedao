"""Curated quiz questions for the Adaptive & Array Signal Processing - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "DSP, correlation & the FFT recap": (
            q(
                "What completely describes a linear time-invariant (LTI) filter?",
                (
                    opt("Its largest output sample"),
                    opt("Its impulse response h[n]", correct=True),
                    opt("Its sampling rate alone"),
                    opt("The number of bits per sample"),
                ),
                "An LTI filter is fully characterized by its impulse response h[n]; its output is the input convolved with h[n].",
            ),
            q(
                "Why are adaptive filters almost always implemented as FIR filters?",
                (
                    opt("Because IIR filters cannot be sampled"),
                    opt(
                        "Because the FIR weights are exactly the quantities being learned, and FIR is unconditionally stable",
                        correct=True,
                    ),
                    opt("Because FIR filters need no input"),
                    opt("Because FIR filters have infinite impulse responses"),
                ),
                "FIR filters expose their tap weights directly (and are always stable), so the adaptive algorithm can learn them safely.",
            ),
            q(
                "What does the cross-correlation r_xy[l] measure?",
                (
                    opt("The total energy of a single signal"),
                    opt("How much two signals line up at lag l", correct=True),
                    opt("The sampling rate of the FFT"),
                    opt("The number of filter taps"),
                ),
                "Cross-correlation measures how well two signals align at a given lag; autocorrelation is a signal with itself.",
            ),
        ),
        "Random signals & power spectra recap": (
            q(
                "A wide-sense stationary (WSS) signal has which property?",
                (
                    opt("Its values are identical at every time instant"),
                    opt(
                        "Its mean is constant and its autocorrelation depends only on the lag, not absolute time",
                        correct=True,
                    ),
                    opt("It has zero power"),
                    opt("Its spectrum is always a single spike"),
                ),
                "WSS means a constant mean and an autocorrelation that depends only on the lag between samples.",
            ),
            q(
                "By the Wiener-Khinchin theorem, the power spectral density is the Fourier transform of what?",
                (
                    opt("The impulse response"),
                    opt("The autocorrelation function", correct=True),
                    opt("The step response"),
                    opt("The number of samples"),
                ),
                "The PSD is the Fourier transform of the autocorrelation r_xx[l].",
            ),
            q(
                "What is the power spectral density of white noise?",
                (
                    opt("A single sharp spike"),
                    opt("Flat (constant) across all frequencies", correct=True),
                    opt("A smooth low-pass shape"),
                    opt("Zero everywhere"),
                ),
                "White noise has a flat PSD because its autocorrelation is an impulse, so there is no structure to exploit.",
            ),
        ),
        "Optimal Wiener filtering & the normal equations": (
            q(
                "What is the Wiener (Wiener-Hopf) solution for the optimal FIR weights?",
                (
                    opt("w = R p"),
                    opt(
                        "w = R^{-1} p, the inverse autocorrelation matrix times the cross-correlation vector",
                        correct=True,
                    ),
                    opt("w = p - R"),
                    opt("w = p / sigma_d^2"),
                ),
                "Setting the MSE gradient to zero gives the normal equations R w = p, so w_o = R^{-1} p.",
            ),
            q(
                "What kind of function is the mean-square error J(w) in the filter weights?",
                (
                    opt("Linear"),
                    opt("Quadratic, giving a single bowl-shaped minimum", correct=True),
                    opt("Periodic"),
                    opt("Discontinuous"),
                ),
                "J(w) is a quadratic in w, so its surface is a paraboloid with one global minimum at the Wiener solution.",
            ),
            q(
                "Why do we still need adaptive algorithms if the Wiener solution is optimal?",
                (
                    opt("Because the Wiener solution is always wrong"),
                    opt(
                        "Because the statistics R and p are usually unknown and changing, and inverting R online is costly",
                        correct=True,
                    ),
                    opt("Because adaptive filters are slower"),
                    opt("Because the Wiener solution needs no data"),
                ),
                "The Wiener solution needs known statistics and a matrix inverse; adaptive methods find it online from data without inverting anything.",
            ),
        ),
        "The mean-square-error surface & gradient descent": (
            q(
                "What is the geometric shape of the MSE surface for a two-weight filter?",
                (
                    opt("A flat plane"),
                    opt("An elliptical bowl (paraboloid) with a single minimum", correct=True),
                    opt("A saddle with no minimum"),
                    opt("A staircase"),
                ),
                "Because J(w) is quadratic, the surface is an elliptical bowl whose single minimum is the Wiener solution.",
            ),
            q(
                "In steepest descent, what role does the step size mu play?",
                (
                    opt("It has no effect on convergence"),
                    opt(
                        "Too small crawls; too large overshoots and diverges; stability needs mu < 1/lambda_max",
                        correct=True,
                    ),
                    opt("It only changes the final minimum location"),
                    opt("It must always equal 1"),
                ),
                "mu controls speed and stability: too small is slow, too large diverges, and stability requires mu below 1/lambda_max.",
            ),
            q(
                "What sets the convergence rate of the slowest mode of steepest descent?",
                (
                    opt("The number of output samples"),
                    opt(
                        "The eigenvalue spread lambda_max/lambda_min of R (how coloured the input is)",
                        correct=True,
                    ),
                    opt("The sign of the desired signal"),
                    opt("The filter's output power only"),
                ),
                "The slowest mode is governed by the eigenvalue spread of R; coloured inputs (large spread) converge slowly.",
            ),
        ),
        "Introduction to adaptive filtering": (
            q(
                "What is the defining feature of an adaptive filter?",
                (
                    opt("It uses a fixed set of weights chosen offline"),
                    opt(
                        "It adjusts its own weights sample by sample to minimise an error, without preset statistics",
                        correct=True,
                    ),
                    opt("It never uses feedback"),
                    opt("It requires a matrix inversion every sample"),
                ),
                "An adaptive filter updates its weights online from the data to minimise an error, no preset statistics required.",
            ),
            q(
                "In the canonical adaptive loop, how is the error e[n] formed?",
                (
                    opt("As the sum of input and output"),
                    opt(
                        "As the desired signal minus the filter output, e[n] = d[n] - y[n]",
                        correct=True,
                    ),
                    opt("As the product of input and weights"),
                    opt("As the autocorrelation of the input"),
                ),
                "The error is the desired signal minus the filter output; it is fed back to update the weights.",
            ),
            q(
                "What does a large step size trade away?",
                (
                    opt("Nothing; large mu is always best"),
                    opt(
                        "It acquires and tracks fast but leaves more residual error (misadjustment)",
                        correct=True,
                    ),
                    opt("It guarantees zero error"),
                    opt("It removes the need for a desired signal"),
                ),
                "Large mu speeds acquisition and tracking but increases misadjustment; small mu is precise but slow.",
            ),
        ),
        "Applications map: where adaptive filters live": (
            q(
                "In adaptive noise cancellation, what serves as the input to the filter?",
                (
                    opt("The clean signal"),
                    opt(
                        "A reference sensor carrying a correlated copy of the noise alone",
                        correct=True,
                    ),
                    opt("The filter's own output"),
                    opt("A random training sequence"),
                ),
                "The reference input is a noise-correlated signal; the primary (signal + noise) is the desired d[n].",
            ),
            q(
                "In system identification, what plays the role of the desired signal d[n]?",
                (
                    opt("The probe input itself"),
                    opt("The unknown system's output", correct=True),
                    opt("The filter's error"),
                    opt("A delayed copy of the weights"),
                ),
                "Driving the unknown system and the filter with the same input and using the system's output as d[n] makes the filter converge to a model of the system.",
            ),
            q(
                "During the training phase of an adaptive equalizer, what is used as the desired signal?",
                (
                    opt("The received noisy samples"),
                    opt("A known transmitted training sequence", correct=True),
                    opt("The channel's impulse response"),
                    opt("White noise"),
                ),
                "A known training sequence supplies d[n] so the equalizer can converge to the channel inverse before switching to decision-directed mode.",
            ),
        ),
    },
    final=(
        q(
            "What do the matrices/vectors R and p in the normal equations represent?",
            (
                opt("R is the cross-correlation vector and p the autocorrelation matrix"),
                opt(
                    "R is the input autocorrelation matrix and p the cross-correlation between desired and input",
                    correct=True,
                ),
                opt("R is the step size and p the error"),
                opt("They are both the filter output"),
            ),
            "R = E{x x^T} is the input autocorrelation matrix and p = E{d x} is the cross-correlation vector; w_o = R^{-1} p.",
        ),
        q(
            "Why does a more coloured (correlated) input slow down a gradient-descent adaptive filter?",
            (
                opt("It increases the filter length"),
                opt(
                    "It increases the eigenvalue spread of R, slowing the slowest mode",
                    correct=True,
                ),
                opt("It removes the minimum of the MSE surface"),
                opt("It makes the input white"),
            ),
            "Coloured inputs have a large eigenvalue spread in R, and the slowest convergence mode is set by that spread.",
        ),
        q(
            "Which statement about the standard error / step-size stability bound is correct?",
            (
                opt("Any positive mu converges"),
                opt(
                    "Stability of steepest descent requires roughly 0 < mu < 1/lambda_max",
                    correct=True,
                ),
                opt("Larger mu always reduces the final error"),
                opt("mu must exceed lambda_max"),
            ),
            "Convergence of steepest descent requires the step size to stay below the inverse of the largest eigenvalue of R.",
        ),
        q(
            "What is the unifying objective shared by noise cancellation, echo cancellation and equalization?",
            (
                opt("Maximising the output power"),
                opt("Minimising the mean-square error E{e^2[n]} online", correct=True),
                opt("Inverting R offline once"),
                opt("Keeping the weights fixed"),
            ),
            "All adaptive applications reduce to minimising the mean-square error online by adjusting the weights.",
        ),
        q(
            "In adaptive noise cancellation, why does minimising e^2 leave the signal intact?",
            (
                opt("Because the signal is added back afterwards"),
                opt(
                    "Because the signal is uncorrelated with the noise, so the only way to reduce error is to cancel the noise",
                    correct=True,
                ),
                opt("Because the filter ignores the reference"),
                opt("Because the desired signal is the noise"),
            ),
            "Since the signal is uncorrelated with the reference noise, the filter cannot reduce error by touching the signal; it can only cancel the correlated noise.",
        ),
        q(
            "What is the power spectral density of a signal, per the Wiener-Khinchin theorem?",
            (
                opt("The Fourier transform of the impulse response"),
                opt("The Fourier transform of the autocorrelation function", correct=True),
                opt("The square of the sampling rate"),
                opt("The inverse of the step size"),
            ),
            "The PSD is the Fourier transform of the autocorrelation; white noise gives a flat PSD, coloured signals give peaked ones.",
        ),
    ),
)
