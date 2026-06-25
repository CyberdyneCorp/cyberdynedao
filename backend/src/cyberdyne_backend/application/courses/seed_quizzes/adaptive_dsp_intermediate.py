"""Curated quiz questions for the Adaptive & Array Signal Processing - Intermediate course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The LMS algorithm": (
            q(
                "What is the LMS weight update rule?",
                (
                    opt("w[n+1] = w[n] - R^{-1} p"),
                    opt("w[n+1] = w[n] + mu e[n] x[n]", correct=True),
                    opt("w[n+1] = w[n] x[n]"),
                    opt("w[n+1] = mu / (e[n] x[n])"),
                ),
                "LMS replaces the true gradient with its instantaneous value, giving the update w[n+1] = w[n] + mu e[n] x[n].",
            ),
            q(
                "What is the per-sample computational cost of LMS for an M-tap filter?",
                (
                    opt("O(M^2)"),
                    opt("O(M log M)"),
                    opt("O(M)", correct=True),
                    opt("O(M^3)"),
                ),
                "LMS needs only O(M) multiplies per sample, with no matrix operations.",
            ),
            q(
                "What is 'misadjustment' in LMS?",
                (
                    opt("The filter converging to the wrong length"),
                    opt(
                        "The excess MSE caused by the weights jittering around the optimum due to the noisy gradient, growing with mu",
                        correct=True,
                    ),
                    opt("A bias in the desired signal"),
                    opt("The delay before adaptation starts"),
                ),
                "Misadjustment is the excess steady-state MSE from the noisy gradient; it grows with the step size mu.",
            ),
        ),
        "Normalized LMS & variants": (
            q(
                "What problem does normalized LMS (NLMS) solve compared to plain LMS?",
                (
                    opt("It removes the need for a desired signal"),
                    opt(
                        "It makes the effective step size independent of input power by dividing by ||x||^2",
                        correct=True,
                    ),
                    opt("It always converges to a different solution"),
                    opt("It eliminates all computation"),
                ),
                "NLMS normalises the step by the input energy, so stability no longer depends on the (possibly unknown, changing) input power.",
            ),
            q(
                "What is the stability range for the normalized step size in NLMS?",
                (
                    opt("0 < mu_tilde < 2", correct=True),
                    opt("0 < mu_tilde < lambda_max"),
                    opt("mu_tilde > 10"),
                    opt("any negative value"),
                ),
                "Because the step is normalised by input energy, the dimensionless step is simply bounded by 0 < mu_tilde < 2.",
            ),
            q(
                "Why does NLMS include a small constant epsilon in the denominator?",
                (
                    opt("To increase the filter length"),
                    opt(
                        "To guard against dividing by zero (or near-zero) input energy during silence",
                        correct=True,
                    ),
                    opt("To bias the weights toward zero"),
                    opt("To slow convergence on loud inputs"),
                ),
                "The epsilon prevents division by a near-zero input energy during silent passages.",
            ),
        ),
        "The RLS algorithm": (
            q(
                "Roughly how fast does RLS converge?",
                (
                    opt(
                        "In about 2M iterations, largely independent of eigenvalue spread",
                        correct=True,
                    ),
                    opt("Slower than LMS in all cases"),
                    opt("Only after infinite iterations"),
                    opt("Exactly M^2 iterations regardless of M"),
                ),
                "RLS converges in roughly 2M iterations and is essentially insensitive to the eigenvalue spread that slows LMS.",
            ),
            q(
                "What is the role of the forgetting factor lambda in RLS?",
                (
                    opt("It sets the filter length"),
                    opt(
                        "It down-weights old data (0 < lambda <= 1), giving a memory of about 1/(1-lambda) samples",
                        correct=True,
                    ),
                    opt("It is the LMS step size"),
                    opt("It is the number of sensors"),
                ),
                "lambda exponentially down-weights past errors, controlling the effective memory window of about 1/(1-lambda) samples.",
            ),
            q(
                "What is the main cost of RLS relative to LMS?",
                (
                    opt("It cannot track changes"),
                    opt(
                        "O(M^2) computation per sample, an M x M matrix to store, and possible numerical instability",
                        correct=True,
                    ),
                    opt("It needs the desired signal to be white"),
                    opt("It only works offline"),
                ),
                "RLS costs O(M^2) per sample, stores an M x M matrix, and can be numerically fragile, motivating square-root/QR forms.",
            ),
        ),
        "Adaptive noise cancellation": (
            q(
                "In adaptive noise cancellation, what is the cleaned output that we keep?",
                (
                    opt("The filter output y[n]"),
                    opt(
                        "The error signal e[n] = d[n] - y[n], which approximates the clean signal",
                        correct=True,
                    ),
                    opt("The reference input"),
                    opt("The weight vector"),
                ),
                "The error e[n] = d[n] - y[n] is approximately the signal s[n], so the error itself is the desired clean output.",
            ),
            q(
                "What must be true of the reference input for noise cancellation to work?",
                (
                    opt("It must be uncorrelated with the noise"),
                    opt("It must be a copy of the clean signal"),
                    opt(
                        "It must be correlated with the noise but ideally free of the signal",
                        correct=True,
                    ),
                    opt("It must be white noise"),
                ),
                "The reference must be correlated with the corrupting noise (so the filter can predict it) and ideally contain none of the signal.",
            ),
            q(
                "What happens if the reference input also contains some of the signal?",
                (
                    opt("Convergence speeds up"),
                    opt(
                        "The filter cancels part of the signal too, causing signal distortion",
                        correct=True,
                    ),
                    opt("Nothing changes"),
                    opt("The noise is amplified"),
                ),
                "Signal leakage into the reference causes the filter to cancel part of the signal, distorting the output.",
            ),
        ),
        "Adaptive echo cancellation": (
            q(
                "Acoustic echo cancellation is an instance of which adaptive-filter configuration?",
                (
                    opt("Inverse modelling"),
                    opt(
                        "System identification, where the filter models the unknown echo path",
                        correct=True,
                    ),
                    opt("Prediction"),
                    opt("Noise whitening"),
                ),
                "The filter, driven by the known loudspeaker signal, identifies the room's echo-path impulse response.",
            ),
            q(
                "Why is a double-talk detector (DTD) needed in echo cancellation?",
                (
                    opt("To increase the sampling rate"),
                    opt(
                        "To freeze adaptation when the near-end speaks, so near-end speech does not corrupt the weights",
                        correct=True,
                    ),
                    opt("To lengthen the filter"),
                    opt("To remove the loudspeaker signal"),
                ),
                "During double-talk the near-end speech looks like a large error; the DTD freezes adaptation to protect the weights.",
            ),
            q(
                "Why are echo cancellers often implemented with frequency-domain / block NLMS?",
                (
                    opt("Because echo paths are very short"),
                    opt(
                        "Because reverberant echo paths can be thousands of taps, and block/FFT methods cut the cost",
                        correct=True,
                    ),
                    opt("Because NLMS cannot run in the time domain"),
                    opt("Because the desired signal is unknown"),
                ),
                "Room echo paths are long (thousands of taps), so FFT-based block processing makes the long filter affordable.",
            ),
        ),
        "Adaptive equalization & channel tracking": (
            q(
                "What impairment does an adaptive equalizer combat?",
                (
                    opt("Quantization noise only"),
                    opt(
                        "Inter-symbol interference (ISI) caused by the channel smearing symbols together",
                        correct=True,
                    ),
                    opt("Loudspeaker nonlinearity"),
                    opt("Sampling jitter only"),
                ),
                "An equalizer inverts the channel to undo inter-symbol interference, reopening the eye diagram.",
            ),
            q(
                "After the training phase, how does a decision-directed equalizer obtain its desired signal?",
                (
                    opt("It keeps using the original training sequence forever"),
                    opt(
                        "It uses its own hard decisions as the desired symbols and keeps adapting",
                        correct=True,
                    ),
                    opt("It stops adapting entirely"),
                    opt("It uses white noise"),
                ),
                "Once the eye is open and errors are low, the receiver trusts its own decisions as d[n] to track slow channel drift.",
            ),
            q(
                "Why can a zero-forcing (pure inverse) equalizer be undesirable?",
                (
                    opt("It cannot remove ISI"),
                    opt(
                        "Where the channel has a deep null, the inverse has huge gain and amplifies noise (noise enhancement)",
                        correct=True,
                    ),
                    opt("It requires no training"),
                    opt("It only works with RLS"),
                ),
                "A pure inverse spikes wherever the channel dips, amplifying noise there; the MMSE equalizer balances ISI against noise instead.",
            ),
        ),
    },
    final=(
        q(
            "Which best summarises the LMS vs RLS trade-off?",
            (
                opt("RLS is cheaper and slower than LMS"),
                opt(
                    "LMS is O(M) and slow on coloured inputs; RLS is O(M^2) but converges fast and is spread-insensitive",
                    correct=True,
                ),
                opt("They have identical cost and speed"),
                opt("LMS needs a matrix inverse and RLS does not"),
            ),
            "LMS is cheap (O(M)) but eigenvalue-spread limited; RLS converges in ~2M iterations regardless of spread, at O(M^2) cost.",
        ),
        q(
            "What makes NLMS preferable to plain LMS for speech-like, time-varying-power inputs?",
            (
                opt("It uses a fixed step independent of the data"),
                opt(
                    "Its step is normalised by input energy, so it stays stable and fast as input power varies",
                    correct=True,
                ),
                opt("It ignores the error signal"),
                opt("It requires no reference input"),
            ),
            "NLMS divides by the input energy, keeping the effective step size and stability independent of the changing input power.",
        ),
        q(
            "Across noise cancellation, echo cancellation and equalization, what supplies the desired signal d[n]?",
            (
                opt("Always white noise"),
                opt(
                    "The wiring of each problem: the noisy primary, the mic, or known training/decisions respectively",
                    correct=True,
                ),
                opt("The filter's own weights"),
                opt("A fixed constant"),
            ),
            "Each application constructs d[n] from its structure: the noisy primary, the echo-carrying mic, or known training symbols / decisions.",
        ),
        q(
            "What is the danger of double-talk in an echo canceller, and the fix?",
            (
                opt("It speeds convergence; no fix needed"),
                opt(
                    "Near-end speech corrupts the weights; a double-talk detector freezes adaptation",
                    correct=True,
                ),
                opt("It mutes the far end; increase mu"),
                opt("It shortens the echo path; lengthen the filter"),
            ),
            "Simultaneous near-end speech corrupts the adaptive weights, so a DTD freezes adaptation during double-talk.",
        ),
        q(
            "Why does inverting a channel with a deep spectral null cause trouble?",
            (
                opt("It removes all signal"),
                opt("The equalizer gain spikes at the null, enhancing noise there", correct=True),
                opt("It converts ISI into white noise"),
                opt("It makes the channel time-invariant"),
            ),
            "The inverse 1/C spikes wherever C dips, amplifying noise at those frequencies; MMSE equalization trades ISI against this noise enhancement.",
        ),
        q(
            "What is the role of the forgetting factor lambda when RLS is used to track a changing channel?",
            (
                opt("It fixes the number of taps"),
                opt(
                    "It down-weights old data so the filter follows recent changes, with memory about 1/(1-lambda)",
                    correct=True,
                ),
                opt("It is the same as the LMS step size bound"),
                opt("It guarantees zero misadjustment"),
            ),
            "lambda controls how quickly old data is forgotten, setting the tracking window of roughly 1/(1-lambda) samples.",
        ),
    ),
)
