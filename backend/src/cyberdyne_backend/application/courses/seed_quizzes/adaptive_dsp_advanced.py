"""Quiz questions for the Adaptive & Array Signal Processing — Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Sensor arrays & the spatial signal model": (
            q(
                "What does a sensor array let you exploit that a single sensor cannot?",
                (
                    opt("The spatial structure of the wavefield (direction)", correct=True),
                    opt("A higher sampling rate in time"),
                    opt("Lower quantization noise"),
                    opt("A wider supply-voltage range"),
                ),
                "Multiple spatially separated sensors capture direction/phase information.",
            ),
            q(
                "For a uniform linear array, the inter-element phase shift depends on:",
                (
                    opt("the angle of arrival and element spacing", correct=True),
                    opt("only the carrier amplitude"),
                    opt("the ADC resolution"),
                    opt("the number of FFT points"),
                ),
                "The steering vector phase is `2*pi*d/lambda * sin(theta)` per element.",
            ),
            q(
                "Spacing array elements much more than half a wavelength apart causes:",
                (
                    opt("spatial aliasing (grating lobes)", correct=True),
                    opt("higher thermal noise"),
                    opt("loss of time resolution"),
                    opt("DC offset"),
                ),
                "Like temporal aliasing, under-sampling space creates ambiguous grating lobes.",
            ),
        ),
        "Beamforming: delay-and-sum & the beam pattern": (
            q(
                "Delay-and-sum beamforming steers the array by:",
                (
                    opt("applying phase/delay so a chosen direction adds coherently", correct=True),
                    opt("increasing each element's gain"),
                    opt("low-pass filtering each channel"),
                    opt("randomizing the element phases"),
                ),
                "Aligning delays makes signals from the look direction sum in phase.",
            ),
            q(
                "Increasing the number of array elements primarily:",
                (
                    opt("narrows the main beam (better angular resolution)", correct=True),
                    opt("raises the sampling rate"),
                    opt("removes all sidelobes"),
                    opt("eliminates noise entirely"),
                ),
                "Beamwidth scales inversely with aperture/element count.",
            ),
            q(
                "Amplitude tapering (windowing) across the array is used to:",
                (
                    opt("reduce sidelobe levels (at some main-beam widening)", correct=True),
                    opt("increase spatial aliasing"),
                    opt("shorten the time record"),
                    opt("add quantization noise"),
                ),
                "Same trade-off as FFT windowing: lower sidelobes vs wider main lobe.",
            ),
        ),
        "Optimal & adaptive beamforming (MVDR / LCMV)": (
            q(
                "The MVDR (Capon) beamformer minimizes output power while:",
                (
                    opt("keeping unit gain toward the desired direction", correct=True),
                    opt("maximizing total noise"),
                    opt("nulling the desired signal"),
                    opt("fixing all weights to one"),
                ),
                "MVDR: minimize variance subject to a distortionless constraint on the look angle.",
            ),
            q(
                "Compared with delay-and-sum, adaptive beamformers can:",
                (
                    opt("place deep nulls on interferers", correct=True),
                    opt("only widen the beam"),
                    opt("never reject interference"),
                    opt("work without any data"),
                ),
                "Adaptive weights use the data covariance to null interference directions.",
            ),
            q(
                "LCMV generalizes MVDR by allowing:",
                (
                    opt("multiple linear constraints on the response", correct=True),
                    opt("only a single fixed weight"),
                    opt("no constraints at all"),
                    opt("time-domain decimation"),
                ),
                "Linearly Constrained Minimum Variance imposes several response constraints.",
            ),
        ),
        "Direction-of-arrival estimation (MUSIC, ESPRIT)": (
            q(
                "MUSIC estimates directions of arrival by exploiting:",
                (
                    opt("orthogonality between signal and noise subspaces", correct=True),
                    opt("the mean of the time samples"),
                    opt("the supply current"),
                    opt("a single snapshot only"),
                ),
                "MUSIC peaks where the steering vector is orthogonal to the noise subspace.",
            ),
            q(
                "A key advantage of subspace DOA methods over beam-scanning is:",
                (
                    opt("super-resolution beyond the beamwidth limit", correct=True),
                    opt("they need no array"),
                    opt("they ignore the covariance matrix"),
                    opt("they require only one sensor"),
                ),
                "MUSIC/ESPRIT resolve closely spaced sources beyond the Rayleigh limit.",
            ),
            q(
                "ESPRIT relies on the array having:",
                (
                    opt("a rotational/translational shift-invariance structure", correct=True),
                    opt("exactly two elements always"),
                    opt("no calibration ever"),
                    opt("a logarithmic spacing"),
                ),
                "ESPRIT uses the rotational invariance of two displaced sub-arrays.",
            ),
        ),
        "High-resolution spectral estimation (parametric, AR)": (
            q(
                "Parametric (e.g. AR) spectral estimation can outperform the periodogram when:",
                (
                    opt("the data record is short and the model fits", correct=True),
                    opt("infinite data is available"),
                    opt("the signal is pure white noise"),
                    opt("the model order is zero"),
                ),
                "AR modeling gives higher resolution from short records if the model is appropriate.",
            ),
            q(
                "Choosing too high an AR model order tends to cause:",
                (
                    opt("spurious spectral peaks (overfitting)", correct=True),
                    opt("guaranteed perfect estimates"),
                    opt("zero variance"),
                    opt("loss of all peaks"),
                ),
                "Order selection (AIC/MDL) balances resolution against spurious peaks.",
            ),
            q(
                "The Yule-Walker equations relate AR coefficients to:",
                (
                    opt("the autocorrelation sequence", correct=True),
                    opt("the supply voltage"),
                    opt("the FFT twiddle factors"),
                    opt("the sampling jitter"),
                ),
                "AR parameters are solved from the signal's autocorrelation.",
            ),
        ),
        "Case study: interference nulling & source localization": (
            q(
                "To suppress a strong interferer from a known direction, an adaptive array:",
                (
                    opt("steers a null toward that direction", correct=True),
                    opt("increases gain toward it"),
                    opt("ignores the covariance matrix"),
                    opt("shuts off all elements"),
                ),
                "Adaptive nulling places a spatial null on the interferer.",
            ),
            q(
                "Combining beamforming with DOA estimation enables:",
                (
                    opt("locating sources and then spatially filtering them", correct=True),
                    opt("only louder output"),
                    opt("removing the need for sensors"),
                    opt("time reversal of causality"),
                ),
                "Estimate where sources are (DOA), then beamform/null accordingly.",
            ),
            q(
                "A practical limit on the number of interferers an N-element array can null is:",
                (
                    opt("about N-1 (degrees of freedom)", correct=True),
                    opt("unlimited"),
                    opt("exactly N+5"),
                    opt("always one"),
                ),
                "An N-element array has roughly N-1 spatial degrees of freedom for nulls.",
            ),
        ),
    },
    final=(
        q(
            "Array signal processing exploits which dimension that single-sensor DSP ignores?",
            (
                opt("space (direction of arrival)", correct=True),
                opt("supply voltage"),
                opt("clock jitter"),
                opt("bit depth"),
            ),
            "Arrays add the spatial dimension.",
        ),
        q(
            "Delay-and-sum vs MVDR: the adaptive MVDR beamformer additionally:",
            (
                opt("nulls interferers using the data covariance", correct=True),
                opt("cannot steer the beam"),
                opt("needs no data"),
                opt("only works at DC"),
            ),
            "MVDR adapts weights to minimize interference+noise power.",
        ),
        q(
            "MUSIC achieves super-resolution by using the:",
            (
                opt("noise-subspace orthogonality of the covariance matrix", correct=True),
                opt("time average of one snapshot"),
                opt("largest signal amplitude only"),
                opt("array supply current"),
            ),
            "Eigen-decomposition separates signal and noise subspaces.",
        ),
        q(
            "Spatial aliasing (grating lobes) is avoided by element spacing of:",
            (
                opt("about half a wavelength or less", correct=True),
                opt("ten wavelengths"),
                opt("any spacing"),
                opt("zero spacing"),
            ),
            "Spacing <= lambda/2 prevents spatial aliasing.",
        ),
        q(
            "An AR (parametric) spectrum is preferred over a periodogram mainly for:",
            (
                opt("short data records, given a suitable model order", correct=True),
                opt("infinite data only"),
                opt("white noise only"),
                opt("zero-order models"),
            ),
            "Parametric methods give higher resolution from limited data.",
        ),
        q(
            "An N-element adaptive array can place roughly how many independent nulls?",
            (
                opt("N - 1", correct=True),
                opt("N + 10"),
                opt("infinite"),
                opt("always 1"),
            ),
            "Degrees of freedom ~ N-1.",
        ),
    ),
)
