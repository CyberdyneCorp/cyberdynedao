from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Sampling and quantization for converters": (
            q(
                "What does the Nyquist criterion require for a signal to be sampled exactly?",
                (
                    opt("Its bandwidth is below fs/2", correct=True),
                    opt("Its bandwidth is above fs/2"),
                    opt("Its bandwidth equals fs"),
                    opt("It has no anti-alias filter"),
                ),
                "Sampling at fs captures a signal exactly only if its bandwidth is below fs/2, the Nyquist frequency.",
            ),
            q(
                "What is the ideal SNR of an N-bit converter?",
                (
                    opt("6.02 N + 1.76 dB", correct=True),
                    opt("1.76 N + 6.02 dB"),
                    opt("3 N dB"),
                    opt("10 log10(N) dB"),
                ),
                "Modeling quantization as uniform white noise gives the ideal SNR = 6.02 N + 1.76 dB, about 6 dB per bit.",
            ),
            q(
                "How is the effective number of bits (ENOB) computed from a measured SNDR?",
                (
                    opt("(SNDR - 1.76) / 6.02", correct=True),
                    opt("(SNDR + 1.76) / 6.02"),
                    opt("6.02 SNDR + 1.76"),
                    opt("SNDR / 2"),
                ),
                "ENOB inverts the ideal formula on the measured SNDR: ENOB = (SNDR - 1.76) / 6.02.",
            ),
        ),
        "DAC architectures": (
            q(
                "What is the main weakness of a binary-weighted DAC?",
                (
                    opt("Huge element spread and poor matching", correct=True),
                    opt("It needs three resistor values"),
                    opt("It is the slowest architecture"),
                    opt("It cannot drive a load resistor"),
                ),
                "Binary-weighted DACs sum currents or charges of 1, 2, 4, ... which gives a huge element spread and poor matching.",
            ),
            q(
                "What does a DNL worse than -1 LSB indicate?",
                (
                    opt("A missing code and possible non-monotonicity", correct=True),
                    opt("Perfect monotonicity"),
                    opt("Zero integral nonlinearity"),
                    opt("A faster conversion rate"),
                ),
                "DNL worse than -1 LSB means a missing code and possible non-monotonicity, which is fatal in a feedback loop.",
            ),
            q(
                "Why are most high-resolution DACs segmented?",
                (
                    opt(
                        "Thermometer MSBs give monotonicity and low glitch while binary LSBs save area",
                        correct=True,
                    ),
                    opt("To use only two resistor values"),
                    opt("To eliminate the need for current sources"),
                    opt("To avoid any digital decoding"),
                ),
                "Segmented DACs use thermometer-coded MSBs for monotonicity and low glitch plus binary LSBs for area efficiency.",
            ),
        ),
        "Nyquist-rate ADCs": (
            q(
                "Why is a flash ADC practical only to about 6-8 bits?",
                (
                    opt("Comparator count, power, and area grow as 2^N", correct=True),
                    opt("It needs N clock cycles per sample"),
                    opt("It cannot resolve the MSB"),
                    opt("It requires oversampling"),
                ),
                "A flash ADC compares against all 2^N-1 thresholds at once, so comparator count, power, and area grow as 2^N.",
            ),
            q(
                "How does a SAR ADC perform a conversion?",
                (
                    opt(
                        "A binary search testing the MSB then each lower bit over N clock cycles",
                        correct=True,
                    ),
                    opt("It compares all thresholds in one clock"),
                    opt("It oversamples and shapes noise"),
                    opt("It amplifies a residue through pipeline stages"),
                ),
                "A successive-approximation ADC does a binary search, halving the uncertainty each step over N clock cycles.",
            ),
            q(
                "What makes a pipeline ADC sustain high throughput at 12-14 bits?",
                (
                    opt(
                        "Stages work concurrently on different samples, each resolving a few bits and amplifying the residue",
                        correct=True,
                    ),
                    opt("A single comparator tests every bit"),
                    opt("It uses a 1-bit quantizer in a feedback loop"),
                    opt("It has no digital alignment or correction"),
                ),
                "A pipeline ADC splits conversion into stages that work concurrently, each resolving a few bits and passing the amplified residue down.",
            ),
        ),
        "Delta-sigma converters": (
            q(
                "What are the two key mechanisms of a delta-sigma converter?",
                (
                    opt("Oversampling and noise shaping", correct=True),
                    opt("Binary search and residue amplification"),
                    opt("Thermometer decoding and segmentation"),
                    opt("Anti-aliasing and decimation only"),
                ),
                "Delta-sigma wins resolution by oversampling massively and noise shaping to push quantization noise out of the signal band.",
            ),
            q(
                "What does the decimation filter do to the modulator output?",
                (
                    opt(
                        "Low-pass-filters and downsamples the fast coarse stream into slow high-resolution words",
                        correct=True,
                    ),
                    opt("High-pass-filters the signal band"),
                    opt("Adds quantization noise to the signal"),
                    opt("Converts words back into a 1-bit stream"),
                ),
                "The decimation filter low-pass-filters and downsamples the fast coarse bitstream into slow high-resolution words at the Nyquist rate.",
            ),
            q(
                "Why is a 1-bit DAC in a delta-sigma loop inherently linear?",
                (
                    opt("It has only two points", correct=True),
                    opt("It uses thermometer coding"),
                    opt("It oversamples its own output"),
                    opt("It has perfectly matched current sources"),
                ),
                "A 1-bit DAC is inherently linear because two points always define a straight line, enabling 20-24 bit resolution with simple analog.",
            ),
        ),
        "PLLs and frequency synthesis": (
            q(
                "What does the divide-by-N block in the feedback path enable?",
                (
                    opt(
                        "Synthesizing fout = N fref, the basis of frequency synthesis", correct=True
                    ),
                    opt("Removing the need for a loop filter"),
                    opt("Doubling the reference phase"),
                    opt("Eliminating jitter entirely"),
                ),
                "The /N divider in feedback makes the loop synthesize fout = N fref, the basis of frequency synthesis.",
            ),
            q(
                "What sets the loop bandwidth and stability in a PLL?",
                (
                    opt(
                        "The loop filter integrating the charge-pump current into the control voltage",
                        correct=True,
                    ),
                    opt("The VCO gain alone"),
                    opt("The divider modulus alone"),
                    opt("The phase detector output frequency"),
                ),
                "The loop filter (an RC network) integrates the charge into the control voltage, setting loop bandwidth and stability.",
            ),
            q(
                "What is the consequence of too-high PLL loop bandwidth?",
                (
                    opt("Reference noise passes through and the loop can ring", correct=True),
                    opt("The VCO noise passes through and tracking is slow"),
                    opt("The divider stops working"),
                    opt("Quantization noise is shaped to high frequency"),
                ),
                "Too-high loop bandwidth lets reference noise through and can ring, while too-low bandwidth tracks slowly and lets VCO noise through.",
            ),
        ),
        "Lab: ADC ENOB and delta-sigma noise shaping": (
            q(
                "What method does the lab use to measure the ADC SNDR and ENOB?",
                (
                    opt("A coherent FFT of the quantized sine", correct=True),
                    opt("A time-domain step response"),
                    opt("A DC sweep of the input"),
                    opt("A binary search on the residue"),
                ),
                "The lab quantizes a coherent sine and uses an FFT (Hanning-windowed) to split signal and noise power, then computes SNDR and ENOB.",
            ),
            q(
                "According to the lab, what happens if you raise N_bits from 10 to 14?",
                (
                    opt(
                        "The noise floor drops about 24 dB and ENOB rises about 4 bits",
                        correct=True,
                    ),
                    opt("The noise floor rises 24 dB and ENOB falls 4 bits"),
                    opt("Nothing changes because it is coherent"),
                    opt("The delta-sigma noise stops shaping"),
                ),
                "Raising N_bits to 14 drops the noise floor about 24 dB and raises ENOB about 4 bits, consistent with 6 dB per bit.",
            ),
            q(
                "In the lab, how does the first-order delta-sigma modulator distribute quantization noise?",
                (
                    opt("Noise rises with frequency, shaped toward high frequency", correct=True),
                    opt("Noise is flat across the band"),
                    opt("Noise concentrates near DC"),
                    opt("Noise is removed without a decimator"),
                ),
                "The delta-sigma noise rises with frequency (shaping); a real decimator low-pass-filters it away to leave high in-band resolution.",
            ),
        ),
        "Applications and the throughline": (
            q(
                "Which converter does the worked sensor-to-digital chain use to set resolution?",
                (
                    opt("A delta-sigma ADC that oversamples and noise-shapes", correct=True),
                    opt("A flash ADC"),
                    opt("A binary-weighted DAC"),
                    opt("A pipeline ADC"),
                ),
                "The sensor-to-digital chain uses a delta-sigma ADC to oversample and noise-shape, followed by a decimation filter for 24-bit words.",
            ),
            q(
                "What do the Walden and Schreier figures-of-merit capture?",
                (
                    opt("Energy per conversion-step and SNR-bandwidth per watt", correct=True),
                    opt("Only the chip die area"),
                    opt("The number of resistor values used"),
                    opt("The PLL lock time"),
                ),
                "The Walden and Schreier ADC figures-of-merit express energy per conversion-step and SNR-bandwidth per watt as a comparable number.",
            ),
            q(
                "What is the unifying throughline from a single transistor to a 24-bit audio chip?",
                (
                    opt(
                        "The same handful of ideas: gm ro, feedback, matching, noise, and sampling",
                        correct=True,
                    ),
                    opt("A new physical principle at every level"),
                    opt("Only digital decimation filtering"),
                    opt("Only the Nyquist criterion"),
                ),
                "From a MOSFET transconductor up to a converter, it is the same ideas composed repeatedly: gm ro, feedback, matching, noise, and sampling.",
            ),
        ),
    },
    final=(
        q(
            "By how much does each extra bit of resolution improve the ideal converter SNR?",
            (
                opt("About 6 dB", correct=True),
                opt("About 1.76 dB"),
                opt("About 3 dB"),
                opt("About 10 dB"),
            ),
            "From SNR = 6.02 N + 1.76 dB, every extra bit buys about 6 dB.",
        ),
        q(
            "Which ADC architecture is fastest but limited to roughly 6-8 bits by its 2^N comparator count?",
            (
                opt("Flash", correct=True),
                opt("SAR"),
                opt("Pipeline"),
                opt("Delta-sigma"),
            ),
            "Flash ADCs compare against all 2^N-1 thresholds in one clock, the fastest but practical only to about 6-8 bits.",
        ),
        q(
            "What two techniques let a delta-sigma converter reach 20-24 bits with simple analog?",
            (
                opt("Oversampling and noise shaping", correct=True),
                opt("Thermometer coding and segmentation"),
                opt("Binary search and residue amplification"),
                opt("Charge pumping and frequency division"),
            ),
            "Delta-sigma oversamples and noise-shapes, and its 1-bit DAC is inherently linear, enabling 20-24 bits with robust analog.",
        ),
        q(
            "In a PLL, what relationship does the feedback divider set between output and reference frequency?",
            (
                opt("fout = N fref", correct=True),
                opt("fout = fref / N"),
                opt("fout = fref + N"),
                opt("fout = Kvco fref"),
            ),
            "A /N divider in feedback makes the loop synthesize fout = N fref, the basis of frequency synthesis.",
        ),
        q(
            "How is ENOB derived from a converter's measured SNDR?",
            (
                opt("ENOB = (SNDR - 1.76) / 6.02", correct=True),
                opt("ENOB = 6.02 SNDR + 1.76"),
                opt("ENOB = (SNDR + 1.76) / 6.02"),
                opt("ENOB = SNDR / 6.02"),
            ),
            "Inverting the ideal SNR formula on the measured SNDR gives ENOB = (SNDR - 1.76) / 6.02.",
        ),
    ),
)
