from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "FIR filter design": (
            q(
                "What property guarantees that an FIR filter has exactly linear phase?",
                (
                    opt("Having feedback from the output"),
                    opt("A symmetric impulse response h[n]", correct=True),
                    opt("Using a Butterworth prototype"),
                    opt("A very small number of taps"),
                ),
                "When h[n] is symmetric, every frequency is delayed by the same amount, giving exactly linear phase.",
            ),
            q(
                "Why does truncating the ideal lowpass sinc impulse response cause ripples at the band edge?",
                (
                    opt("Because of the Gibbs phenomenon", correct=True),
                    opt("Because of pole-zero cancellation"),
                    opt("Because of frequency warping"),
                    opt("Because of limit cycles"),
                ),
                "Truncating the infinitely long sinc produces Gibbs ripples; a window like Hann, Hamming, or Kaiser tames them.",
            ),
            q(
                "What does the Parks-McClellan (Remez exchange) algorithm produce for a given filter order?",
                (
                    opt("The maximally flat passband filter"),
                    opt(
                        "The optimal equiripple FIR with the shortest length meeting the spec",
                        correct=True,
                    ),
                    opt("A filter with infinite impulse response"),
                    opt("A filter guaranteed to have nonlinear phase"),
                ),
                "Parks-McClellan spreads the error evenly as equal-height ripples, giving the shortest filter that meets the spec.",
            ),
        ),
        "IIR filter design": (
            q(
                "What is the main advantage of an IIR filter over an FIR filter?",
                (
                    opt("It always has linear phase"),
                    opt("A handful of coefficients can give a razor-sharp cutoff", correct=True),
                    opt("It is always guaranteed stable"),
                    opt("It never distorts waveform shape"),
                ),
                "IIR feeds output back, so few coefficients achieve a sharp cutoff that would need hundreds of FIR taps.",
            ),
            q(
                "Which analog prototype has a maximally flat passband and the best (gentlest) phase?",
                (
                    opt("Butterworth", correct=True),
                    opt("Chebyshev I"),
                    opt("Chebyshev II"),
                    opt("Elliptic"),
                ),
                "Butterworth is maximally flat in the passband with the gentlest roll-off and the best phase among the prototypes.",
            ),
            q(
                "Why must you pre-warp the critical frequency before applying the bilinear transform?",
                (
                    opt("Because the transform makes the filter unstable otherwise"),
                    opt(
                        "Because the bilinear mapping is nonlinear and warps frequencies",
                        correct=True,
                    ),
                    opt("Because it converts FIR taps into IIR coefficients"),
                    opt("Because it removes quantization noise"),
                ),
                "The bilinear transform squashes the analog axis nonlinearly (frequency warping), so pre-warping lands the cutoff where you want.",
            ),
        ),
        "Filter structures & implementation": (
            q(
                "What distinguishes Direct Form II from Direct Form I?",
                (
                    opt(
                        "It shares the delay line between numerator and denominator, using fewer delays",
                        correct=True,
                    ),
                    opt("It removes all feedback from the filter"),
                    opt("It doubles the number of delay elements"),
                    opt("It converts the filter to lattice form"),
                ),
                "Direct Form II shares the delay line so it uses only max(M,N) delays, making it canonical (minimum memory).",
            ),
            q(
                "Why is a high-order IIR implemented as a cascade of second-order sections (biquads)?",
                (
                    opt("Because biquads have linear phase"),
                    opt(
                        "Because one big polynomial is hopelessly sensitive to tiny coefficient errors",
                        correct=True,
                    ),
                    opt("Because biquads use no multipliers"),
                    opt("Because cascades eliminate group delay"),
                ),
                "A single high-order polynomial is extremely sensitive; splitting into biquads keeps each section robust.",
            ),
            q(
                "What is the stability test for a lattice structure built from reflection coefficients k_i?",
                (
                    opt("Every |k_i| < 1", correct=True),
                    opt("The sum of all k_i equals zero"),
                    opt("All poles lie outside the unit circle"),
                    opt("Every k_i is symmetric"),
                ),
                "A lattice filter is stable if and only if every reflection coefficient satisfies |k_i| < 1.",
            ),
        ),
        "Multirate DSP": (
            q(
                "When decimating a signal by an integer factor M, what must you do before keeping every M-th sample?",
                (
                    opt("Insert L-1 zeros between samples"),
                    opt(
                        "Lowpass filter to below the new Nyquist to prevent aliasing", correct=True
                    ),
                    opt("Apply dither to the signal"),
                    opt("Pre-warp the cutoff frequency"),
                ),
                "You must lowpass filter (anti-alias) below fs/2M first, or content above it aliases down into your band.",
            ),
            q(
                "What does interpolation by L involve?",
                (
                    opt("Discarding every L-th sample"),
                    opt(
                        "Inserting L-1 zeros between samples, then lowpass filtering to remove images",
                        correct=True,
                    ),
                    opt("Quantizing to L bits"),
                    opt("Factoring H(z) into L biquads"),
                ),
                "Interpolation upsamples by inserting L-1 zeros (creating images) then anti-imaging lowpass filters them out.",
            ),
            q(
                "What does the polyphase decomposition achieve in a decimator?",
                (
                    opt("It computes only the samples you keep, an M-fold speedup", correct=True),
                    opt("It guarantees linear phase for the output"),
                    opt("It removes the need for any filtering"),
                    opt("It increases the dynamic range by 6 dB per bit"),
                ),
                "Polyphase splits the filter into M sub-filters so you compute only the samples you keep, an M-fold speedup.",
            ),
        ),
        "Fixed-point & quantization effects": (
            q(
                "According to the SQNR rule, roughly how much dynamic range does each additional ADC bit buy?",
                (
                    opt("About 1.76 dB"),
                    opt("About 6 dB", correct=True),
                    opt("About 12 dB"),
                    opt("About 98 dB"),
                ),
                "SQNR is about 6.02 B + 1.76 dB, so every bit buys roughly 6 dB of dynamic range.",
            ),
            q(
                "Why does DSP hardware often offer saturation instead of two-s-complement wraparound on overflow?",
                (
                    opt("Saturation is faster to compute"),
                    opt(
                        "Wraparound turns a big positive into a big negative, which is catastrophic",
                        correct=True,
                    ),
                    opt("Saturation removes quantization noise"),
                    opt("Wraparound increases the word length"),
                ),
                "Two-s-complement overflow wraps a big positive into a big negative; saturation clamps at the rail instead.",
            ),
            q(
                "What is the purpose of adding dither before quantizing?",
                (
                    opt("To increase the number of bits"),
                    opt(
                        "To decorrelate the quantization error from the signal, removing harmonic distortion",
                        correct=True,
                    ),
                    opt("To trap the filter in a limit cycle"),
                    opt("To pre-warp the cutoff frequency"),
                ),
                "Dither adds a tiny bit of noise before quantizing to decorrelate the error, trading faint hiss for removing ugly distortion.",
            ),
        ),
        "Lab: design & apply an FIR and IIR filter": (
            q(
                "In the lab, what does dividing the FIR coefficients by h.sum() accomplish?",
                (
                    opt("It sets unity DC gain", correct=True),
                    opt("It makes the filter unstable"),
                    opt("It converts the filter to IIR"),
                    opt("It applies the Hamming window"),
                ),
                "Dividing by h.sum() normalizes the coefficients so the FIR has unity gain at DC.",
            ),
            q(
                "The lab signal mixes a 30 Hz tone and a 200 Hz tone with an 80 Hz cutoff lowpass. What is the goal?",
                (
                    opt("Keep the 30 Hz tone and reject the 200 Hz tone", correct=True),
                    opt("Keep the 200 Hz tone and reject the 30 Hz tone"),
                    opt("Reject both tones equally"),
                    opt("Amplify the noise floor"),
                ),
                "Both filters have an 80 Hz cutoff, so they pass the 30 Hz tone and reject the 200 Hz tone.",
            ),
            q(
                "How does the lab build its IIR lowpass coefficients?",
                (
                    opt("Using the windowing method on a sinc"),
                    opt(
                        "Via the bilinear transform of a 2nd-order analog lowpass with pre-warped cutoff",
                        correct=True,
                    ),
                    opt("Using the Parks-McClellan algorithm"),
                    opt("By inserting zeros and filtering"),
                ),
                "The lab pre-warps the cutoff then applies the bilinear transform to a 2nd-order analog lowpass to get a biquad.",
            ),
        ),
    },
    final=(
        q(
            "Which filter type is always stable and can have exactly linear phase but may need many taps?",
            (
                opt("FIR", correct=True),
                opt("IIR"),
                opt("Lattice IIR"),
                opt("Elliptic analog"),
            ),
            "FIR filters have no feedback, are always stable, and can have exactly linear phase with symmetric taps.",
        ),
        q(
            "Which technique converts a stable analog prototype into a stable digital IIR filter?",
            (
                opt("The bilinear transform", correct=True),
                opt("The Parks-McClellan algorithm"),
                opt("Polyphase decomposition"),
                opt("Dithering"),
            ),
            "The bilinear transform maps left-half-plane analog poles to inside-the-unit-circle digital poles, preserving stability.",
        ),
        q(
            "What is the universally recommended way to ship a high-order IIR filter?",
            (
                opt("As a single direct-form polynomial"),
                opt(
                    "As second-order sections (biquads), e.g. transposed Direct Form II per section",
                    correct=True,
                ),
                opt("As a windowed sinc"),
                opt("As an upsampled polyphase bank"),
            ),
            "High-order IIRs are shipped as cascaded second-order sections because each pole pair is far less sensitive to quantization.",
        ),
        q(
            "What is the cardinal rule of multirate DSP?",
            (
                opt("Filter before you downsample, filter after you upsample", correct=True),
                opt("Always use floating-point arithmetic"),
                opt("Quantize coefficients before designing"),
                opt("Pre-warp every frequency twice"),
            ),
            "Skipping the anti-alias filter before downsampling causes aliasing; skipping the anti-imaging filter after upsampling leaves images.",
        ),
        q(
            "Approximately what is the best-case SQNR of a full-scale sinusoid through a 16-bit ADC?",
            (
                opt("About 74 dB"),
                opt("About 98 dB", correct=True),
                opt("About 6 dB"),
                opt("About 160 dB"),
            ),
            "SQNR is about 6.02 B + 1.76 dB, so 16 bits gives roughly 98 dB of dynamic range.",
        ),
    ),
)
