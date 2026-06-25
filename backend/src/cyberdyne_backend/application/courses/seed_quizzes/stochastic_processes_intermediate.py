"""Curated quiz questions for the Random & Stochastic Processes - Intermediate
course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Stationarity: strict & wide-sense": (
            q(
                "What two conditions define a wide-sense stationary (WSS) process?",
                (
                    opt("All joint distributions are shift-invariant"),
                    opt(
                        "Constant mean and an autocorrelation depending only on the lag τ",
                        correct=True,
                    ),
                    opt("Zero mean and zero variance"),
                    opt("A Gaussian marginal at every time"),
                ),
                "WSS requires a constant mean and R_X depending only on the lag τ = t2 - t1.",
            ),
            q(
                "What is the relationship between strict-sense (SSS) and wide-sense (WSS) stationarity?",
                (
                    opt("WSS implies SSS in general"),
                    opt("SSS implies WSS; the converse holds for Gaussian processes", correct=True),
                    opt("They are always equivalent"),
                    opt("Neither implies the other"),
                ),
                "SSS implies WSS; for Gaussian processes the two notions coincide.",
            ),
            q(
                "A process whose mean grows as 0.3t is:",
                (
                    opt("Wide-sense stationary"),
                    opt("Non-stationary, because its mean is not constant", correct=True),
                    opt("Strict-sense stationary"),
                    opt("Ergodic by definition"),
                ),
                "A time-varying mean violates the constant-mean condition for WSS.",
            ),
        ),
        "Autocorrelation & autocovariance": (
            q(
                "What does R_X(0) represent for a WSS process?",
                (
                    opt("The mean of the process"),
                    opt("The average power E[X^2(t)]", correct=True),
                    opt("Always zero"),
                    opt("The bandwidth"),
                ),
                "R_X(0) = E[X^2(t)] is the average power and the maximum of the autocorrelation.",
            ),
            q(
                "Which symmetry does the autocorrelation of a real WSS process have?",
                (
                    opt("Odd: R_X(-τ) = -R_X(τ)"),
                    opt("Even: R_X(-τ) = R_X(τ)", correct=True),
                    opt("It is periodic with period τ"),
                    opt("It has no particular symmetry"),
                ),
                "Autocorrelation of a real process is an even function of the lag.",
            ),
            q(
                "How does autocovariance relate to autocorrelation?",
                (
                    opt("C_X(τ) = R_X(τ) + μ_X^2"),
                    opt("C_X(τ) = R_X(τ) - μ_X^2", correct=True),
                    opt("C_X(τ) = R_X(τ) · μ_X"),
                    opt("They are identical for all processes"),
                ),
                "Autocovariance subtracts the squared mean: C_X(τ) = R_X(τ) - μ_X^2.",
            ),
        ),
        "Power spectral density & Wiener-Khinchin": (
            q(
                "What does the Wiener-Khinchin theorem state?",
                (
                    opt("The PSD is the derivative of the autocorrelation"),
                    opt("The PSD is the Fourier transform of the autocorrelation", correct=True),
                    opt("The autocorrelation is the square of the PSD"),
                    opt("The PSD equals the mean of the process"),
                ),
                "S_X(f) is the Fourier transform of R_X(τ), and vice versa.",
            ),
            q(
                "How is the total average power obtained from the PSD?",
                (
                    opt("It is the peak value of S_X(f)"),
                    opt("It is the area under S_X(f) over all frequencies", correct=True),
                    opt("It is S_X(0)"),
                    opt("It is the slope of S_X(f) at the origin"),
                ),
                "Total power E[X^2] = R_X(0) = ∫ S_X(f) df, the area under the PSD.",
            ),
            q(
                "What is the PSD of white noise?",
                (
                    opt("A narrow spike at f = 0"),
                    opt("Flat (constant) over all frequencies", correct=True),
                    opt("A Lorentzian low-pass shape"),
                    opt("Zero everywhere"),
                ),
                "White noise has a flat PSD, N0/2, constant across all frequencies.",
            ),
        ),
        "LTI systems with random inputs": (
            q(
                "How does an LTI system transform the input PSD?",
                (
                    opt("S_Y(f) = H(f)·S_X(f)"),
                    opt("S_Y(f) = |H(f)|^2·S_X(f)", correct=True),
                    opt("S_Y(f) = S_X(f) + |H(f)|^2"),
                    opt("S_Y(f) = S_X(f)/H(f)"),
                ),
                "The output PSD is the input PSD scaled by the squared magnitude response.",
            ),
            q(
                "How does the mean of the output relate to the input mean for an LTI system?",
                (
                    opt("μ_Y = μ_X · H(0), the DC gain", correct=True),
                    opt("μ_Y = μ_X always"),
                    opt("μ_Y = 0 for any LTI system"),
                    opt("μ_Y = |H(0)|^2 · μ_X"),
                ),
                "The output mean is the input mean scaled by the DC gain H(0).",
            ),
            q(
                "Feeding white noise into a low-pass filter produces an output whose spectrum:",
                (
                    opt("Stays flat"),
                    opt("Takes the shape of |H(f)|^2", correct=True),
                    opt("Becomes a single impulse"),
                    opt("Has negative regions"),
                ),
                "S_Y(f) = |H(f)|^2 (N0/2), so the output spectrum follows the filter shape.",
            ),
        ),
        "Gaussian processes": (
            q(
                "A Gaussian process is completely specified by:",
                (
                    opt("Its mean and autocorrelation (covariance) functions", correct=True),
                    opt("Its skewness and kurtosis"),
                    opt("Its peak value alone"),
                    opt("Its bandwidth only"),
                ),
                "Jointly Gaussian statistics depend only on the mean and covariance structure.",
            ),
            q(
                "For a Gaussian process, what does WSS imply?",
                (
                    opt("Nothing beyond constant mean"),
                    opt("It is also strict-sense stationary", correct=True),
                    opt("It must be white"),
                    opt("It cannot be ergodic"),
                ),
                "For Gaussian processes WSS and SSS coincide.",
            ),
            q(
                "For jointly Gaussian variables, uncorrelated implies:",
                (
                    opt("Nothing in particular"),
                    opt("Independent", correct=True),
                    opt("Identically distributed"),
                    opt("Equal means"),
                ),
                "For jointly Gaussian RVs, zero correlation does imply independence.",
            ),
        ),
        "Ergodicity & time averages": (
            q(
                "What does ergodicity allow you to do in practice?",
                (
                    opt("Ignore the noise entirely"),
                    opt(
                        "Replace ensemble averages with time averages of one sample path",
                        correct=True,
                    ),
                    opt("Treat any process as Gaussian"),
                    opt("Remove the need for a PSD"),
                ),
                "Ergodicity lets a single long recording's time average stand in for the ensemble average.",
            ),
            q(
                "What condition typically supports ergodicity?",
                (
                    opt("The mean must be zero"),
                    opt("Distant samples must decorrelate, C_X(τ) → 0 as τ → ∞", correct=True),
                    opt("The process must be periodic"),
                    opt("The variance must be infinite"),
                ),
                "Ergodicity needs mixing: the autocovariance must decay to zero with lag.",
            ),
            q(
                "Why is a process with a random-but-fixed DC offset per realization non-ergodic in the mean?",
                (
                    opt("Because it has no variance"),
                    opt(
                        "Each path's time average reports its own offset, never the ensemble mean",
                        correct=True,
                    ),
                    opt("Because its PSD is flat"),
                    opt("Because it is Gaussian"),
                ),
                "Each realization keeps its own offset, so time averages differ from the ensemble mean.",
            ),
        ),
    },
    final=(
        q(
            "Which is the practical (second-order) definition of stationarity?",
            (
                opt("Strict-sense stationarity"),
                opt(
                    "Wide-sense stationarity: constant mean and lag-only autocorrelation",
                    correct=True,
                ),
                opt("Ergodicity"),
                opt("Whiteness"),
            ),
            "WSS — constant mean and R_X(τ) depending only on lag — is the workhorse condition.",
        ),
        q(
            "R_X(0) for a WSS process equals:",
            (
                opt("The mean"),
                opt("The average power E[X^2]", correct=True),
                opt("Zero"),
                opt("The bandwidth"),
            ),
            "Zero-lag autocorrelation is the average power.",
        ),
        q(
            "The power spectral density is obtained from the autocorrelation by:",
            (
                opt("Differentiation"),
                opt("The Fourier transform (Wiener-Khinchin)", correct=True),
                opt("Squaring"),
                opt("Integration over time"),
            ),
            "Wiener-Khinchin: PSD is the Fourier transform of the autocorrelation.",
        ),
        q(
            "The single most useful LTI-with-noise formula is:",
            (
                opt("S_Y(f) = |H(f)|^2 S_X(f)", correct=True),
                opt("S_Y(f) = H(f) + S_X(f)"),
                opt("R_Y(τ) = R_X(τ)"),
                opt("μ_Y = 0"),
            ),
            "An LTI system shapes the input PSD by its squared magnitude response.",
        ),
        q(
            "A key property unique to Gaussian processes is that:",
            (
                opt("They are never stationary"),
                opt("Uncorrelated implies independent, and WSS implies SSS", correct=True),
                opt("They cannot pass through LTI systems"),
                opt("Their PSD is always flat"),
            ),
            "For Gaussian processes uncorrelated means independent and WSS coincides with SSS.",
        ),
        q(
            "Ergodicity is important because it lets you:",
            (
                opt("Avoid measuring anything"),
                opt("Estimate ensemble statistics from a single long sample path", correct=True),
                opt("Make any process Gaussian"),
                opt("Eliminate the standard error"),
            ),
            "Ergodicity bridges theory and measurement: one recording's time average matches the ensemble.",
        ),
    ),
)
