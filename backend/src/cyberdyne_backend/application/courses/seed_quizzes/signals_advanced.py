from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The Laplace transform & transfer functions": (
            q(
                "In the Laplace transform, what does the complex variable s equal?",
                (
                    opt("j*omega only, with no real part"),
                    opt("sigma + j*omega, a real part plus an imaginary part", correct=True),
                    opt("e to the power j*omega"),
                    opt("the sum from n=0 of x[n] times z to the minus n"),
                ),
                "Laplace uses the complex frequency s = sigma + j*omega, generalising the Fourier transform.",
            ),
            q(
                "A continuous-time LTI system is stable if and only if every pole has what property?",
                (
                    opt("a positive real part"),
                    opt("a negative real part, lying in the left half-plane", correct=True),
                    opt("magnitude less than one"),
                    opt("zero imaginary part"),
                ),
                "Continuous LTI stability requires all poles in the left half-plane, i.e. Re(s) < 0.",
            ),
            q(
                "In the transfer function H(s) = Y(s)/X(s), what are the roots of the numerator called?",
                (
                    opt("poles"),
                    opt("zeros", correct=True),
                    opt("taps"),
                    opt("residues"),
                ),
                "Numerator roots are the zeros; denominator roots are the poles.",
            ),
        ),
        "The z-transform & difference equations": (
            q(
                "For a discrete-time system, the z-transform is defined as which sum?",
                (
                    opt("the integral from 0 of x(t) times e to the minus s*t dt"),
                    opt("the sum from n=0 of x[n] times z to the minus n", correct=True),
                    opt("the sum of b_k times x[n-k]"),
                    opt("20 times log base 10 of the magnitude of H"),
                ),
                "The z-transform is X(z) = sum over n of x[n] times z to the minus n.",
            ),
            q(
                "A discrete-time system is stable when its poles lie where?",
                (
                    opt("in the left half-plane"),
                    opt("inside the unit circle, with magnitude of z less than one", correct=True),
                    opt("on the imaginary axis"),
                    opt("outside the unit circle"),
                ),
                "Discrete stability requires all poles inside the unit circle, |z| < 1.",
            ),
            q(
                "What is a difference equation in this context?",
                (
                    opt("an integral relating a signal to its spectrum"),
                    opt(
                        "each output sample computed from past inputs and outputs",
                        correct=True,
                    ),
                    opt("the truncation of an ideal sinc response"),
                    opt("a plot of magnitude versus log-frequency"),
                ),
                "A digital filter is a difference equation giving y[n] from past inputs and outputs.",
            ),
        ),
        "Frequency response & Bode plots": (
            q(
                "How do you obtain the frequency response of a continuous transfer function?",
                (
                    opt("evaluate it at s = j*omega along the frequency axis", correct=True),
                    opt("take the roots of its denominator"),
                    opt("integrate it from zero to infinity"),
                    opt("convolve it with a windowed sinc"),
                ),
                "Setting s = j*omega evaluates H on the frequency axis to give H(j*omega).",
            ),
            q(
                "On a Bode plot the magnitude is plotted in decibels using which expression?",
                (
                    opt("10 times log base 10 of the magnitude of H"),
                    opt("20 times log base 10 of the magnitude of H", correct=True),
                    opt("the square root of one plus omega squared"),
                    opt("the angle of H in degrees"),
                ),
                "Bode magnitude in dB is 20 times log base 10 of the magnitude of H.",
            ),
            q(
                "At the cutoff frequency omega_c of a first-order low-pass, the magnitude equals what?",
                (
                    opt("one, full passband gain"),
                    opt("about 0.707, the -3 dB half-power point", correct=True),
                    opt("zero"),
                    opt("about 1.414"),
                ),
                "At omega_c the magnitude is 1/sqrt(2), about 0.707, the -3 dB half-power point.",
            ),
        ),
        "FIR & IIR filter design": (
            q(
                "Which statement about FIR filters is correct?",
                (
                    opt("they use feedback and can be unstable"),
                    opt("they have no feedback and are always stable", correct=True),
                    opt("they always have nonlinear phase"),
                    opt("they are cheapest for a sharp cutoff"),
                ),
                "FIR filters have no feedback (a_k = 0), so they are always stable.",
            ),
            q(
                "A practical FIR low-pass is built from which design?",
                (
                    opt("a Butterworth analog prototype"),
                    opt("a windowed sinc: an ideal sinc truncated and tapered", correct=True),
                    opt("a recursive difference equation with feedback"),
                    opt("a Chebyshev recursion"),
                ),
                "A practical FIR low-pass is a windowed sinc: the ideal sinc truncated and tapered.",
            ),
            q(
                "When should you prefer an IIR filter over an FIR filter?",
                (
                    opt("when you need exactly linear phase for audio or comms"),
                    opt("when you need a sharp cutoff cheaply, as in control loops", correct=True),
                    opt("when you need guaranteed stability"),
                    opt("when you want no feedback"),
                ),
                "IIR is chosen for a sharp cutoff cheaply; FIR is chosen for linear phase.",
            ),
        ),
        "Lab: design & apply a low-pass filter": (
            q(
                "In the lab, how is the FIR low-pass impulse response h constructed?",
                (
                    opt("a sinc multiplied by a Hamming window, then normalised", correct=True),
                    opt("a Butterworth recursion run with feedback"),
                    opt("the roots of a denominator polynomial"),
                    opt("an FFT of the noisy signal"),
                ),
                "The lab builds h as np.sinc times np.hamming, then divides by its sum.",
            ),
            q(
                "Why is the filter h divided by its sum (h /= h.sum())?",
                (
                    opt("to set unit DC gain so the passband level is preserved", correct=True),
                    opt("to make the filter unstable"),
                    opt("to convert it to an IIR filter"),
                    opt("to shift the cutoff to the Nyquist frequency"),
                ),
                "Dividing by the sum normalises to unit DC gain so the wanted signal level is kept.",
            ),
            q(
                "The lab signal mixes a wanted 4 Hz sine with what interference?",
                (
                    opt("an 80 Hz sine removed by the low-pass", correct=True),
                    opt("a 4 Hz sine that the filter amplifies"),
                    opt("white noise that the FFT cannot see"),
                    opt("a DC offset added by the window"),
                ),
                "The noisy signal is 4 Hz plus 0.6 times an 80 Hz sine, which the low-pass removes.",
            ),
        ),
        "Applications & use cases": (
            q(
                "Which application is built directly on the FFT according to the lesson?",
                (
                    opt("OFDM in Wi-Fi, 5G and LTE", correct=True),
                    opt("a Butterworth control loop"),
                    opt("a windowed-sinc taper"),
                    opt("a pole-zero stability check"),
                ),
                "The lesson states OFDM (Wi-Fi, 5G, LTE) is built directly on the FFT.",
            ),
            q(
                "In biomedical pipelines like ECG and EEG, what does a notch filter do?",
                (
                    opt("removes 50/60 Hz mains hum", correct=True),
                    opt("compresses images with the DCT"),
                    opt("shifts a message up to a carrier"),
                    opt("performs Doppler processing"),
                ),
                "ECG/EEG pipelines notch out 50/60 Hz mains hum and band-pass the physiological band.",
            ),
            q(
                "Which four ideas does the lesson call the whole subject?",
                (
                    opt("Laplace, z-transform, Bode plots and windows"),
                    opt("sampling, spectra, convolution and poles/zeros", correct=True),
                    opt("FIR, IIR, FFT and DCT"),
                    opt("audio, biomedical, radar and control"),
                ),
                "The throughline names sampling, spectra, convolution and poles/zeros as the whole subject.",
            ),
        ),
    },
    final=(
        q(
            "Match each transform to its domain: Laplace and z-transform handle what?",
            (
                opt("Laplace is discrete-time and the z-transform is continuous-time"),
                opt(
                    "Laplace is continuous-time and the z-transform is discrete-time",
                    correct=True,
                ),
                opt("both are continuous-time only"),
                opt("both are discrete-time only"),
            ),
            "Laplace generalises Fourier for continuous signals; the z-transform plays that role for discrete signals.",
        ),
        q(
            "How do continuous and discrete stability conditions differ?",
            (
                opt("both require poles in the left half-plane"),
                opt(
                    "continuous needs poles in the left half-plane; discrete needs poles inside the unit circle",
                    correct=True,
                ),
                opt(
                    "continuous needs poles inside the unit circle; discrete needs the left half-plane"
                ),
                opt("both require poles outside the unit circle"),
            ),
            "Continuous stability is Re(s) < 0 (left half-plane); discrete stability is |z| < 1 (inside the unit circle).",
        ),
        q(
            "A first-order low-pass rolls off above its cutoff at what rate?",
            (
                opt("-20 dB per decade", correct=True),
                opt("-3 dB per decade"),
                opt("+20 dB per decade"),
                opt("0 dB per decade"),
            ),
            "A first-order low-pass rolls off above its cutoff at -20 dB per decade.",
        ),
        q(
            "Which trade-off correctly contrasts FIR and IIR filters?",
            (
                opt("FIR can be unstable; IIR is always stable"),
                opt(
                    "FIR can give exactly linear phase; IIR can give a sharp cutoff cheaply",
                    correct=True,
                ),
                opt("FIR uses feedback; IIR uses none"),
                opt("FIR is cheapest for sharp cutoffs; IIR needs more taps"),
            ),
            "FIR offers linear phase and guaranteed stability; IIR offers a cheap sharp cutoff via feedback.",
        ),
        q(
            "Why does shaping a signal with an LTI filter work as described in the track?",
            (
                opt("convolution in time equals multiplication in frequency", correct=True),
                opt("convolution in time equals addition in frequency"),
                opt("filtering moves all poles into the right half-plane"),
                opt("the z-transform converts FIR filters into IIR filters"),
            ),
            "An LTI filter shapes a spectrum because convolution in time equals multiplication in frequency.",
        ),
    ),
)
