from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is a signal?": (
            q(
                "What is a signal, as defined in this lesson?",
                (
                    opt("A circuit that amplifies voltage"),
                    opt(
                        "A function that carries information by varying with an independent variable, almost always time",
                        correct=True,
                    ),
                    opt("A constant value that never changes over time"),
                    opt("A purely random sequence with no information"),
                ),
                "A signal is a function carrying information by varying with an independent variable, usually time.",
            ),
            q(
                "How is a discrete-time signal usually obtained from a continuous-time one?",
                (
                    opt("By integrating it over all time"),
                    opt("By sampling the continuous-time signal", correct=True),
                    opt("By reversing its time axis"),
                    opt("By adding random noise to it"),
                ),
                "A discrete-time signal x[n] is usually obtained by sampling a continuous-time signal x(t).",
            ),
            q(
                "In the sinusoid x(t) = A cos(2 pi f t + phi), what does f represent?",
                (
                    opt("The amplitude of the wave"),
                    opt("The phase offset in radians"),
                    opt("The frequency in Hz", correct=True),
                    opt("The time index"),
                ),
                "In A cos(2 pi f t + phi), f is the frequency in Hz, A is amplitude, and phi is the phase.",
            ),
        ),
        "Elementary signals": (
            q(
                "For the real exponential x(t) = e^(a t), what happens when a is negative?",
                (
                    opt("The signal decays toward zero", correct=True),
                    opt("The signal grows without bound"),
                    opt("The signal oscillates forever"),
                    opt("The signal stays constant at 1"),
                ),
                "A negative rate a makes e^(a t) decay, like an RC circuit discharging.",
            ),
            q(
                "What does the unit step u(t) model?",
                (
                    opt("An instantaneous kick of unit area"),
                    opt("A steadily rising input"),
                    opt("A switch turning on, jumping from 0 to 1 at t=0", correct=True),
                    opt("A pure oscillation"),
                ),
                "The unit step u(t) jumps from 0 to 1 at t=0, modeling a switch turning on.",
            ),
            q(
                "In discrete time, the unit impulse delta[n] equals what?",
                (
                    opt("1 for all n greater than or equal to 0"),
                    opt("1 at n=0 and 0 everywhere else", correct=True),
                    opt("n times u[n]"),
                    opt("e raised to the power a n"),
                ),
                "The discrete unit impulse delta[n] is 1 at n=0 and 0 elsewhere.",
            ),
        ),
        "Signal operations": (
            q(
                "Which operation produces y(t) = x(t - t0) with t0 greater than 0?",
                (
                    opt("A time reversal"),
                    opt("An amplitude scaling"),
                    opt("A shift to the right, a delay", correct=True),
                    opt("A time compression"),
                ),
                "x(t - t0) with t0 greater than 0 shifts the signal right, which is a delay.",
            ),
            q(
                "What does time reversal y(t) = x(-t) do to a signal?",
                (
                    opt("Plays it backwards", correct=True),
                    opt("Doubles its amplitude"),
                    opt("Delays it by one second"),
                    opt("Compresses it in time"),
                ),
                "Time reversal y(t) = x(-t) flips the time axis, playing the signal backwards.",
            ),
            q(
                "For y(t) = x(a t - t0), what is the correct order of operations?",
                (
                    opt("Scale then shift"),
                    opt("Shift then scale", correct=True),
                    opt("Only scale, never shift"),
                    opt("Reverse then scale"),
                ),
                "For x(a t - t0) you shift then scale, since it equals x(a(t - t0/a)).",
            ),
        ),
        "Sampling & the discrete world": (
            q(
                "What does the relation x[n] = x(n Ts) describe?",
                (
                    opt("Sampling a continuous signal every Ts seconds", correct=True),
                    opt("Reversing the time axis of a signal"),
                    opt("Convolving a signal with an impulse"),
                    opt("Amplifying the signal by a factor Ts"),
                ),
                "x[n] = x(n Ts) means taking samples of x(t) every Ts seconds.",
            ),
            q(
                "By the Nyquist-Shannon theorem, how fast must you sample a signal whose highest frequency is fmax?",
                (
                    opt("At fs greater than fmax"),
                    opt("At fs greater than 2 fmax", correct=True),
                    opt("At fs equal to fmax divided by 2"),
                    opt("At any rate, sampling rate does not matter"),
                ),
                "Nyquist-Shannon requires fs greater than 2 fmax to capture the signal.",
            ),
            q(
                "What happens when a signal is sampled too slowly?",
                (
                    opt("The signal is amplified"),
                    opt("Nothing changes, it is always safe"),
                    opt("High frequencies masquerade as low ones, called aliasing", correct=True),
                    opt("The signal is delayed by Ts"),
                ),
                "Sampling too slowly causes aliasing, where high frequencies appear as lower ones.",
            ),
        ),
        "Lab: synthesize & plot a signal": (
            q(
                "In the lab, what does np.arange(0, 1, 1/fs) create?",
                (
                    opt("A time vector of 1 second at sampling rate fs", correct=True),
                    opt("A frequency axis in Hz"),
                    opt("A single scalar value"),
                    opt("The magnitude spectrum of the signal"),
                ),
                "np.arange(0, 1, 1/fs) builds a 1 second time vector sampled at rate fs.",
            ),
            q(
                "The lab signal combines two sinusoids at which frequencies?",
                (
                    opt("3 Hz and 12 Hz"),
                    opt("5 Hz and 20 Hz", correct=True),
                    opt("50 Hz and 60 Hz"),
                    opt("4 Hz and 80 Hz"),
                ),
                "The lab builds x = sin(2 pi 5 t) + 0.5 sin(2 pi 20 t), so 5 Hz and 20 Hz.",
            ),
            q(
                "What is added to the two-tone signal in the lab?",
                (
                    opt("A constant DC offset"),
                    opt("A small amount of random noise", correct=True),
                    opt("A third sinusoid at 60 Hz"),
                    opt("An exponential decay"),
                ),
                "The lab adds 0.2 times random noise via np.random.randn to the two tones.",
            ),
        ),
    },
    final=(
        q(
            "Which statement best distinguishes continuous-time from discrete-time signals?",
            (
                opt("CT signals are random while DT signals are deterministic"),
                opt(
                    "CT signals are defined for every instant x(t); DT signals only at integer indices x[n]",
                    correct=True,
                ),
                opt("CT signals carry no information but DT signals do"),
                opt("CT signals have no frequency, DT signals do"),
            ),
            "CT signals x(t) are defined at every instant; DT signals x[n] only at integer indices.",
        ),
        q(
            "A signal that is infinitely narrow with unit area, the idealized tap, is the:",
            (
                opt("unit step"),
                opt("ramp"),
                opt("unit impulse", correct=True),
                opt("real exponential"),
            ),
            "The unit impulse delta(t) is infinitely narrow with unit area, the idealized tap.",
        ),
        q(
            "To capture a 20 kHz audio signal, why does CD audio sample at 44.1 kHz?",
            (
                opt("Because 44.1 kHz is below the audio band"),
                opt("Because it exceeds twice the 20 kHz limit, satisfying Nyquist", correct=True),
                opt("Because sampling rate has no effect on quality"),
                opt("Because it equals exactly the highest frequency"),
            ),
            "44.1 kHz is greater than 2 times the roughly 20 kHz hearing limit, satisfying Nyquist.",
        ),
        q(
            "Which expression correctly delays a signal by t0 seconds, with t0 greater than 0?",
            (
                opt("y(t) = x(-t)"),
                opt("y(t) = x(t + t0)"),
                opt("y(t) = x(t - t0)", correct=True),
                opt("y(t) = c x(t)"),
            ),
            "A delay shifts right, given by y(t) = x(t - t0) for t0 greater than 0.",
        ),
        q(
            "The two languages used side by side throughout this track are:",
            (
                opt("C and Rust"),
                opt("MATLAB and Python", correct=True),
                opt("Java and JavaScript"),
                opt("Fortran and Julia"),
            ),
            "The track presents every concept in both MATLAB and Python side by side.",
        ),
    ),
)
