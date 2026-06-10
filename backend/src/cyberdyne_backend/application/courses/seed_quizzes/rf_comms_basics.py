from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Communication system overview": (
            q(
                "What are the three boxes in the universal communication system chain?",
                (
                    opt("source, sink, and amplifier"),
                    opt("transmitter, channel, and receiver", correct=True),
                    opt("modulator, antenna, and speaker"),
                    opt("encoder, decoder, and filter"),
                ),
                "Every communication system is the same three-box chain: transmitter, channel, receiver.",
            ),
            q(
                "A power gain of 10 times expressed in decibels is approximately what?",
                (
                    opt("+3 dB"),
                    opt("+20 dB"),
                    opt("+10 dB", correct=True),
                    opt("-10 dB"),
                ),
                "G_dB = 10 log10(Pout/Pin), so a 10x power ratio is +10 dB; a 2x ratio is about +3 dB.",
            ),
            q(
                "Signal quality is fundamentally set by which quantity?",
                (
                    opt("raw transmitted power alone"),
                    opt("the signal power relative to noise (SNR)", correct=True),
                    opt("the carrier frequency"),
                    opt("the length of the channel"),
                ),
                "Quality is set not by raw signal strength but by signal relative to noise, the SNR.",
            ),
        ),
        "Amplitude modulation (AM)": (
            q(
                "In AM, what does the message signal vary on the carrier?",
                (
                    opt("the carrier amplitude", correct=True),
                    opt("the carrier frequency"),
                    opt("the carrier phase"),
                    opt("the carrier bandwidth"),
                ),
                "Amplitude modulation lets the message vary the carrier amplitude via (1 + m x(t)).",
            ),
            q(
                "What happens when the AM modulation index m exceeds 1?",
                (
                    opt("the signal disappears entirely"),
                    opt("the carrier frequency doubles"),
                    opt("the signal over-modulates and the envelope distorts", correct=True),
                    opt("the bandwidth shrinks to zero"),
                ),
                "Past m = 1 the signal over-modulates: the envelope clips and a simple detector recovers garbage.",
            ),
            q(
                "A message of bandwidth B placed on an AM carrier occupies how much bandwidth?",
                (
                    opt("B"),
                    opt("2B around the carrier", correct=True),
                    opt("B/2"),
                    opt("4B"),
                ),
                "The carrier times a tone produces fc +/- fm, the two sidebands, so a message of bandwidth B occupies 2B.",
            ),
        ),
        "Frequency & phase modulation (FM/PM)": (
            q(
                "Why does FM sound hiss-free where AM crackles?",
                (
                    opt("FM uses a higher carrier frequency"),
                    opt(
                        "noise adds to amplitude, which a limiter can clip away in FM", correct=True
                    ),
                    opt("FM requires no carrier at all"),
                    opt("FM uses less bandwidth than AM"),
                ),
                "Angle modulation encodes the message in phase or frequency, so a receiver can clip and limit out amplitude noise.",
            ),
            q(
                "In frequency modulation, what follows the message signal?",
                (
                    opt("the carrier amplitude"),
                    opt("the instantaneous frequency", correct=True),
                    opt("the carrier power"),
                    opt("the sampling rate"),
                ),
                "In FM the instantaneous frequency f(t) = fc + kf x(t) follows the message, so phase is its integral.",
            ),
            q(
                "Carson's rule estimates FM bandwidth as which expression?",
                (
                    opt("B = 2(delta f + fm)", correct=True),
                    opt("B = delta f + fm"),
                    opt("B = 2 fm"),
                    opt("B = delta f / fm"),
                ),
                "Carson's rule: B is about 2(delta f + fm), using peak deviation and the highest message frequency.",
            ),
        ),
        "Sampling, quantization & PCM": (
            q(
                "The Nyquist-Shannon theorem requires the sample rate fs to satisfy what condition?",
                (
                    opt("fs > B"),
                    opt("fs > 2B", correct=True),
                    opt("fs < B/2"),
                    opt("fs = B"),
                ),
                "You can perfectly reconstruct a signal of bandwidth B if fs > 2B; otherwise aliasing occurs.",
            ),
            q(
                "Roughly how much does quantization SNR improve per added bit of resolution?",
                (
                    opt("about 1 dB per bit"),
                    opt("about 3 dB per bit"),
                    opt("about 6 dB per bit", correct=True),
                    opt("about 20 dB per bit"),
                ),
                "SNR_dB is about 6.02 n + 1.76, so the SNR climbs about 6 dB per bit.",
            ),
            q(
                "What are the three steps to digitize an analog signal in PCM?",
                (
                    opt("sample, quantize, and code into bits", correct=True),
                    opt("modulate, amplify, and filter"),
                    opt("encode, interleave, and transmit"),
                    opt("mix, integrate, and detect"),
                ),
                "PCM samples in time, quantizes in amplitude, then codes each level into a binary word.",
            ),
        ),
        "Noise & SNR": (
            q(
                "Thermal (Johnson-Nyquist) noise power is given by which formula?",
                (
                    opt("Pn = kB T B", correct=True),
                    opt("Pn = kB / (T B)"),
                    opt("Pn = T B / kB"),
                    opt("Pn = kB T / B"),
                ),
                "Any resistor at temperature T generates noise power Pn = kB T B, proportional to bandwidth.",
            ),
            q(
                "Why does the receiver front-end low-noise amplifier (LNA) matter most?",
                (
                    opt("it consumes the most power"),
                    opt(
                        "by Friis' formula the first stage dominates the cascaded noise figure",
                        correct=True,
                    ),
                    opt("it sets the carrier frequency"),
                    opt("it is the only stage that adds gain"),
                ),
                "Friis' noise formula shows the first stage dominates, so the front-end LNA matters most.",
            ),
            q(
                "For digital links, lowering the bit-error rate (BER) is achieved by raising which figure of merit?",
                (
                    opt("the carrier frequency"),
                    opt("Eb/N0, energy per bit over noise density", correct=True),
                    opt("the modulation index m"),
                    opt("the sample rate fs"),
                ),
                "Higher Eb/N0 means a lower BER, with a steep waterfall relationship.",
            ),
        ),
        "Lab: AM/FM modulate a tone & plot the spectrum": (
            q(
                "In the lab, how is the FM signal's instantaneous phase computed from the message?",
                (
                    opt("by differentiating the message"),
                    opt("by the cumulative sum (integral) of the message", correct=True),
                    opt("by squaring the message"),
                    opt("by taking the FFT of the message"),
                ),
                "The FM phase is 2 pi fc t + 2 pi kf cumsum(msg)/fs, the integral of the message.",
            ),
            q(
                "What tool does the lab use to view the AM and FM spectra?",
                (
                    opt("the FFT (np.fft.rfft)", correct=True),
                    opt("a Hilbert transform"),
                    opt("an envelope detector"),
                    opt("a phase-locked loop"),
                ),
                "Single-sided magnitude spectra are computed via np.fft.rfft and np.fft.rfftfreq.",
            ),
            q(
                "When you raise kf to 8000 in the lab, what happens to the FM spectrum?",
                (
                    opt("it narrows to a single line"),
                    opt("it spreads much wider, per Carson's rule", correct=True),
                    opt("it disappears below the noise floor"),
                    opt("it shifts down to baseband"),
                ),
                "Raising kf widens the FM spectrum, illustrating Carson's rule that bandwidth grows with deviation.",
            ),
        ),
    },
    final=(
        q(
            "Which resource is described as the most precious and finite in a communication system?",
            (
                opt("transmit power"),
                opt("bandwidth", correct=True),
                opt("antenna size"),
                opt("carrier amplitude"),
            ),
            "Bandwidth is finite and shared, so every system fights to send more bits in less of it.",
        ),
        q(
            "Which modulation scheme is most robust against amplitude noise?",
            (
                opt("amplitude modulation (AM)"),
                opt("frequency modulation (FM)", correct=True),
                opt("on-off keying"),
                opt("envelope-detected AM"),
            ),
            "Angle modulation like FM encodes the message in frequency, so amplitude noise can be limited away.",
        ),
        q(
            "An audio CD samples at 44.1 kHz primarily because of which principle?",
            (
                opt("Carson's rule"),
                opt("Friis' noise formula"),
                opt("the Nyquist rate must exceed twice the 20 kHz audio bandwidth", correct=True),
                opt("the decibel scale"),
            ),
            "44.1 kHz is above 2 x 20 kHz, satisfying fs > 2B to avoid aliasing.",
        ),
        q(
            "Decibels are useful in a signal chain mainly because they let you do what?",
            (
                opt("multiply gains and losses together"),
                opt("convert add/subtract operations into multiply/divide"),
                opt("turn multiply/divide into add/subtract so the chain is a sum", correct=True),
                opt("eliminate noise from the channel"),
            ),
            "Decibels turn multiply/divide into add/subtract, so a whole signal chain is just a sum.",
        ),
        q(
            "To improve a digital link's SNR, which of these is a valid approach?",
            (
                opt(
                    "raise transmit power, narrow bandwidth, or lower the noise figure",
                    correct=True,
                ),
                opt("increase the carrier frequency only"),
                opt("over-modulate the AM signal"),
                opt("sample below the Nyquist rate"),
            ),
            "You can raise transmit power, narrow bandwidth, lower the receiver noise figure, or add coding gain.",
        ),
    ),
)
