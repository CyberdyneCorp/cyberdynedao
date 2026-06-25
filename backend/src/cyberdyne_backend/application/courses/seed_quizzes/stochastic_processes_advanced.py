"""Curated quiz questions for the Random & Stochastic Processes - Advanced course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Poisson processes & shot noise": (
            q(
                "For a Poisson process, the count N(t) over an interval of length t has:",
                (
                    opt("Mean λt and variance λt", correct=True),
                    opt("Mean 1/λ and variance 1/λ^2"),
                    opt("Mean λ and variance λ^2"),
                    opt("Zero mean"),
                ),
                "A Poisson count has equal mean and variance, both λt.",
            ),
            q(
                "What is the shot-noise mean-square current over bandwidth B?",
                (
                    opt("4kTB"),
                    opt("2q·I_dc·B", correct=True),
                    opt("q/B"),
                    opt("I_dc^2·B"),
                ),
                "Shot noise has mean-square current 2q·I_dc·B with a flat low-frequency PSD.",
            ),
            q(
                "What characterises the inter-arrival times of a Poisson process?",
                (
                    opt("They are Gaussian"),
                    opt("They are exponential and memoryless", correct=True),
                    opt("They are uniform"),
                    opt("They are constant"),
                ),
                "Poisson arrivals have exponential, memoryless inter-arrival times.",
            ),
        ),
        "Markov chains & steady state": (
            q(
                "What is the Markov property?",
                (
                    opt("The future depends on the entire history"),
                    opt("The future depends on the present state only", correct=True),
                    opt("All states are equally likely"),
                    opt("The chain never changes state"),
                ),
                "A Markov chain's next state depends only on the current state, not the past.",
            ),
            q(
                "How is the stationary distribution π of a Markov chain characterised?",
                (
                    opt("π = Pπ with entries summing to zero"),
                    opt("π = πP with entries summing to 1", correct=True),
                    opt("π = P^2"),
                    opt("π equals the first row of P"),
                ),
                "The stationary distribution satisfies π = πP and sums to 1.",
            ),
            q(
                "For the two-state Good/Bad chain with P(Good→Bad)=0.2 and P(Bad→Good)=0.4, the steady-state probability of Good is:",
                (
                    opt("1/2"),
                    opt("2/3", correct=True),
                    opt("1/3"),
                    opt("0.2"),
                ),
                "Balance gives π_Good = 0.4/(0.2 + 0.4) = 2/3.",
            ),
        ),
        "Thermal & electronic noise": (
            q(
                "What is the open-circuit thermal-noise voltage mean square of a resistor R?",
                (
                    opt("2q·I·B"),
                    opt("4·k_B·T·R·B", correct=True),
                    opt("k_B·T/R"),
                    opt("R·B^2"),
                ),
                "Johnson-Nyquist noise gives mean-square voltage 4 k_B T R B.",
            ),
            q(
                "What is the available thermal-noise power, and what does it depend on?",
                (
                    opt("k_B·T·B, independent of R", correct=True),
                    opt("4·k_B·T·R·B, proportional to R"),
                    opt("Zero"),
                    opt("q·I·B"),
                ),
                "Available noise power is k_B·T·B and does not depend on the resistance.",
            ),
            q(
                "What does the noise figure F measure?",
                (
                    opt("The gain of an amplifier"),
                    opt("The degradation of SNR through a stage (SNR_in / SNR_out)", correct=True),
                    opt("The bandwidth of a filter"),
                    opt("The resistance of the source"),
                ),
                "Noise figure is the ratio of input to output SNR; a noiseless stage has F = 1.",
            ),
        ),
        "The matched filter & optimal detection": (
            q(
                "What is the impulse response of the matched filter for a known pulse s(t)?",
                (
                    opt("h(t) = s(t)"),
                    opt("h(t) = s(T - t), the time-reversed delayed copy", correct=True),
                    opt("h(t) = 1/s(t)"),
                    opt("h(t) = s'(t)"),
                ),
                "The matched filter is the time-reversed, delayed replica of the signal.",
            ),
            q(
                "The peak SNR of the matched filter depends only on:",
                (
                    opt("The pulse shape"),
                    opt("The signal energy E, as 2E/N0", correct=True),
                    opt("The bandwidth alone"),
                    opt("The sampling rate"),
                ),
                "Max SNR is 2E/N0 and depends only on signal energy, not the pulse shape.",
            ),
            q(
                "In binary detection over Gaussian noise, the error probability decreases as:",
                (
                    opt("The signal separation d/(2σ) increases", correct=True),
                    opt("The noise σ increases"),
                    opt("The separation d decreases"),
                    opt("The bandwidth increases"),
                ),
                "P_e = Q(d/2σ), so more separation or less noise lowers the error probability.",
            ),
        ),
        "Wiener filtering intro": (
            q(
                "What does the Wiener filter minimise?",
                (
                    opt("The peak output SNR"),
                    opt("The mean-squared estimation error E[(X - X_hat)^2]", correct=True),
                    opt("The bandwidth"),
                    opt("The signal energy"),
                ),
                "The Wiener filter is the minimum-mean-squared-error linear estimator.",
            ),
            q(
                "For signal plus uncorrelated noise, the Wiener filter gain is:",
                (
                    opt("H(f) = S_X / (S_X + S_N)", correct=True),
                    opt("H(f) = S_N / S_X"),
                    opt("H(f) = |S_X|^2"),
                    opt("H(f) = 1 for all f"),
                ),
                "The Wiener filter is the PSD ratio S_X/(S_X + S_N).",
            ),
            q(
                "Where the noise dominates the spectrum, the Wiener filter gain tends to:",
                (
                    opt("1"),
                    opt("0", correct=True),
                    opt("infinity"),
                    opt("-1"),
                ),
                "Where S_N ≫ S_X the gain approaches 0, suppressing noise-dominated bands.",
            ),
        ),
        "Queueing & birth-death processes": (
            q(
                "In a birth-death process, transitions occur:",
                (
                    opt("To any state instantly"),
                    opt("Only to neighbouring states (up by birth, down by death)", correct=True),
                    opt("Never"),
                    opt("Only downward"),
                ),
                "A birth-death process moves only to adjacent states at rates λ (up) and μ (down).",
            ),
            q(
                "For an M/M/1 queue with utilisation ρ = λ/μ, what is the mean number in the system?",
                (
                    opt("ρ"),
                    opt("ρ/(1 - ρ)", correct=True),
                    opt("1 - ρ"),
                    opt("λμ"),
                ),
                "L = ρ/(1 - ρ), which blows up as ρ approaches 1.",
            ),
            q(
                "What does Little's law state?",
                (
                    opt(
                        "L = λW (mean number equals arrival rate times mean time in system)",
                        correct=True,
                    ),
                    opt("L = μ/λ"),
                    opt("W = ρ^2"),
                    opt("L = 1 - ρ"),
                ),
                "Little's law relates average number in system to arrival rate and mean delay: L = λW.",
            ),
        ),
    },
    final=(
        q(
            "A Poisson process count over interval t has mean and variance:",
            (
                opt("Both λt", correct=True),
                opt("λt and (λt)^2"),
                opt("1/λ and 1/λ^2"),
                opt("0 and λ"),
            ),
            "Poisson counts have equal mean and variance, λt.",
        ),
        q(
            "The stationary distribution of an irreducible aperiodic Markov chain satisfies:",
            (
                opt("π = πP, summing to 1", correct=True),
                opt("π = P only"),
                opt("π = 0"),
                opt("π equals the initial distribution"),
            ),
            "The steady state satisfies π = πP with probabilities summing to 1.",
        ),
        q(
            "The available thermal noise power k_B·T·B is notable because it:",
            (
                opt("Depends strongly on resistance R"),
                opt("Is independent of R and sets the noise floor", correct=True),
                opt("Is always zero"),
                opt("Scales with the square of bandwidth"),
            ),
            "Available noise power k_B T B is independent of R and defines the receiver noise floor.",
        ),
        q(
            "The matched filter maximises output SNR by:",
            (
                opt("Differentiating the input"),
                opt(
                    "Correlating the input against a time-reversed copy of the known signal",
                    correct=True,
                ),
                opt("Amplifying all frequencies equally"),
                opt("Removing the signal"),
            ),
            "The matched filter h(t) = s(T - t) correlates against the known template, achieving 2E/N0.",
        ),
        q(
            "The Wiener filter gain S_X/(S_X + S_N) behaves as a:",
            (
                opt("Constant gain of 1 everywhere"),
                opt(
                    "Frequency-by-frequency trust gauge that passes signal-dominated bands",
                    correct=True,
                ),
                opt("High-pass differentiator"),
                opt("Pure delay"),
            ),
            "It passes bands where the signal dominates and suppresses noise-dominated bands.",
        ),
        q(
            "In an M/M/1 queue, as utilisation ρ approaches 1 the mean number in system L:",
            (
                opt("Approaches zero"),
                opt("Grows without bound", correct=True),
                opt("Stays constant"),
                opt("Equals ρ"),
            ),
            "L = ρ/(1 - ρ) diverges as ρ → 1, which is why systems are sized with headroom.",
        ),
    ),
)
