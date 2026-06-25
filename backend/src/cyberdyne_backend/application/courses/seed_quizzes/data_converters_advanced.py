"""Curated quiz questions for the Data Converters & PLLs - Advanced course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Phase-locked loops: the building blocks": (
            q(
                "What does the phase/frequency detector (PFD) in a PLL output?",
                (
                    opt("A smooth control voltage for the VCO"),
                    opt("UP/DOWN pulses proportional to the phase error", correct=True),
                    opt("The divided output frequency"),
                    opt("A shaped noise spectrum"),
                ),
                "The PFD compares reference and feedback phase, emitting UP/DOWN pulses proportional to the error.",
            ),
            q(
                "With a divide-by-N in the feedback path, what is the locked output frequency?",
                (
                    opt("f_ref divided by N"),
                    opt("N times f_ref", correct=True),
                    opt("f_ref minus N"),
                    opt("The VCO free-running frequency f_0"),
                ),
                "The loop drives the divided output to match the reference, so f_out = N*f_ref, a frequency multiplier.",
            ),
            q(
                "What role does the loop filter play in a PLL?",
                (
                    opt("It generates the reference clock"),
                    opt(
                        "It low-pass filters the charge into a smooth control voltage and sets the loop dynamics",
                        correct=True,
                    ),
                    opt("It divides the output frequency"),
                    opt("It compares phases"),
                ),
                "The loop filter smooths the charge-pump current into the VCO control voltage and acts as the loop's compensator.",
            ),
        ),
        "PLL dynamics: bandwidth, stability & lock time": (
            q(
                "Which damping factor is the usual sweet spot for a fast, low-overshoot PLL lock?",
                (
                    opt("zeta about 0.1"),
                    opt("zeta about 0.707", correct=True),
                    opt("zeta about 3"),
                    opt("zeta = 0"),
                ),
                "A damping of about 0.707 gives fast settling with minimal overshoot, the standard choice.",
            ),
            q(
                "A wider PLL loop bandwidth does what?",
                (
                    opt("Locks slower and rejects reference noise better"),
                    opt(
                        "Locks faster and tracks the reference, but passes more reference noise and spurs",
                        correct=True,
                    ),
                    opt("Has no effect on lock time"),
                    opt("Eliminates VCO phase noise entirely"),
                ),
                "Wide bandwidth speeds locking and cleans VCO noise but lets through more reference noise; narrow does the reverse.",
            ),
            q(
                "How does a PLL treat VCO noise versus reference noise?",
                (
                    opt("It low-passes both"),
                    opt("It high-passes both"),
                    opt(
                        "It high-pass filters VCO noise and low-pass filters reference noise",
                        correct=True,
                    ),
                    opt("It amplifies both equally"),
                ),
                "The loop suppresses low-frequency VCO noise (high-pass) and high-frequency reference noise (low-pass).",
            ),
        ),
        "Jitter & phase noise": (
            q(
                "Jitter and phase noise are best described as what?",
                (
                    opt("Two unrelated impairments"),
                    opt(
                        "Time-domain and frequency-domain views of the same phenomenon",
                        correct=True,
                    ),
                    opt("Static linearity errors"),
                    opt("Quantization effects only"),
                ),
                "Jitter (time domain) and phase noise (frequency domain) are two views of the same timing uncertainty.",
            ),
            q(
                "Phase noise is typically specified in what units?",
                (
                    opt("Volts RMS"),
                    opt("dBc/Hz at an offset from the carrier", correct=True),
                    opt("LSB"),
                    opt("Picoseconds per bit"),
                ),
                "Phase noise L(f) is the sideband power relative to the carrier per hertz, in dBc/Hz at a given offset.",
            ),
            q(
                "How does ADC aperture jitter limit SNR for a high-frequency input?",
                (
                    opt("It has no effect at high frequencies"),
                    opt(
                        "SNR falls as the input frequency rises, since timing error becomes a larger voltage error",
                        correct=True,
                    ),
                    opt("It only affects DC accuracy"),
                    opt("It improves SNR at GHz inputs"),
                ),
                "SNR = -20*log10(2*pi*f_in*sigma_t); faster inputs make the same jitter cause larger sampling errors.",
            ),
        ),
        "Frequency synthesis: integer-N & fractional-N": (
            q(
                "In an integer-N synthesizer, what sets the channel spacing (frequency resolution)?",
                (
                    opt("The VCO gain K_VCO"),
                    opt("The reference frequency f_ref", correct=True),
                    opt("The loop filter order"),
                    opt("The charge-pump current"),
                ),
                "Integer-N output steps by f_ref, so the reference frequency is the channel spacing.",
            ),
            q(
                "How does a fractional-N synthesizer achieve fine resolution with a large f_ref?",
                (
                    opt("By using two reference oscillators"),
                    opt(
                        "By dithering the integer divider so the average ratio is fractional",
                        correct=True,
                    ),
                    opt("By removing the loop filter"),
                    opt("By lowering the VCO gain"),
                ),
                "Switching the divider between N and N+1 gives a fractional average ratio while keeping f_ref large.",
            ),
            q(
                "Why is a sigma-delta modulator used in fractional-N synthesizers?",
                (
                    opt("To divide the output frequency"),
                    opt(
                        "To shape the divider-dither noise to high offsets the loop filter removes",
                        correct=True,
                    ),
                    opt("To detect phase errors"),
                    opt("To generate the reference clock"),
                ),
                "A sigma-delta modulator randomises and high-pass shapes the divider sequence, pushing fractional spurs out of band.",
            ),
        ),
        "Clock & data recovery": (
            q(
                "What problem is clock and data recovery (CDR) solving?",
                (
                    opt("Removing quantization noise from an ADC"),
                    opt(
                        "Extracting a sampling clock from data sent with no separate clock line",
                        correct=True,
                    ),
                    opt("Compensating sinc droop in a DAC"),
                    opt("Reducing INL in a converter"),
                ),
                "Serial links send data with no clock, so the CDR recovers timing from the data transitions themselves.",
            ),
            q(
                "Why do serial links use line coding like 8b/10b or scrambling?",
                (
                    opt("To increase the bit rate"),
                    opt(
                        "To guarantee enough transitions so the CDR loop stays locked",
                        correct=True,
                    ),
                    opt("To remove the loop filter"),
                    opt("To raise the VCO gain"),
                ),
                "Long runs of identical bits starve the CDR of edges, so coding ensures sufficient transition density.",
            ),
            q(
                "A bang-bang (Alexander) phase detector reports what?",
                (
                    opt("The exact phase error in degrees"),
                    opt("Only whether the clock is early or late (1-bit)", correct=True),
                    opt("The amplitude of the data signal"),
                    opt("The frequency offset in hertz"),
                ),
                "A bang-bang PD is a 1-bit quantizer in the loop, reporting only early/late, giving a robust low-power CDR.",
            ),
        ),
        "Mixed-signal layout & noise coupling": (
            q(
                "How does fast digital switching corrupt sensitive analog circuits?",
                (
                    opt("Only through radiated electromagnetic fields"),
                    opt(
                        "Through shared supplies, the substrate and parasitic capacitance",
                        correct=True,
                    ),
                    opt("By changing the quantization step size"),
                    opt("It cannot couple into analog circuits"),
                ),
                "Digital current spikes couple via shared supplies, substrate and parasitic caps, raising the noise floor and spurs.",
            ),
            q(
                "Why are analog and digital supplies and grounds often separated and joined at a star point?",
                (
                    opt("To reduce the chip area"),
                    opt(
                        "So digital return current does not flow under sensitive analog circuits",
                        correct=True,
                    ),
                    opt("To increase the clock frequency"),
                    opt("To eliminate the need for decoupling caps"),
                ),
                "Splitting AVDD/DVDD and AGND/DGND with a single star tie keeps noisy digital return current away from analog nodes.",
            ),
            q(
                "What is the purpose of local decoupling capacitors at each supply pin?",
                (
                    opt("To filter the input signal before sampling"),
                    opt(
                        "To give switching current a short local loop instead of a long noisy one",
                        correct=True,
                    ),
                    opt("To divide the output frequency"),
                    opt("To increase the VCO gain"),
                ),
                "Local bypass caps supply transient switching current nearby, shrinking the noisy current loop and supply bounce.",
            ),
        ),
    },
    final=(
        q(
            "Which block sets a PLL's loop dynamics (bandwidth and damping)?",
            (
                opt("The phase detector"),
                opt("The VCO"),
                opt("The loop filter", correct=True),
                opt("The feedback divider"),
            ),
            "The loop filter is the loop's compensator, setting bandwidth, damping and thus stability and lock time.",
        ),
        q(
            "Integrating a phase-noise curve over a frequency band yields what?",
            (
                opt("The carrier frequency"),
                opt("The RMS jitter in that band", correct=True),
                opt("The INL of the converter"),
                opt("The oversampling ratio"),
            ),
            "Integrating phase noise over an offset band gives the RMS jitter, the bridge between the two domains.",
        ),
        q(
            "What is the key advantage of fractional-N over integer-N synthesis?",
            (
                opt("It needs no VCO"),
                opt(
                    "Fine resolution with a large reference, giving faster lock and less noise multiplication",
                    correct=True,
                ),
                opt("It removes all phase noise"),
                opt("It eliminates the loop filter"),
            ),
            "Fractional-N keeps f_ref large (fast lock, low N) while a dithered divider gives fine frequency resolution.",
        ),
        q(
            "A CDR is essentially what kind of circuit?",
            (
                opt("A sigma-delta ADC"),
                opt("A flash DAC"),
                opt(
                    "A PLL whose phase detector locks to data transitions",
                    correct=True,
                ),
                opt("A resistor-string divider"),
            ),
            "A CDR is a PLL that derives its phase reference from the incoming data edges rather than a clean clock.",
        ),
        q(
            "Which layout practice most directly protects a converter's last bit and a PLL's phase noise?",
            (
                opt("Using the smallest possible transistors"),
                opt(
                    "Supply/ground separation, guard rings, and local decoupling",
                    correct=True,
                ),
                opt("Increasing the clock frequency"),
                opt("Removing the anti-alias filter"),
            ),
            "Grounding, guarding and decoupling decide the noise floor and phase noise as much as the circuit itself.",
        ),
        q(
            "For a high-frequency input, why does even femtosecond aperture jitter dominate ADC SNR?",
            (
                opt("Because jitter only affects DC levels"),
                opt(
                    "Because SNR = -20 log10(2*pi*f_in*sigma_t), so error grows with input frequency",
                    correct=True,
                ),
                opt("Because jitter increases the LSB size"),
                opt("Because jitter improves at high frequencies"),
            ),
            "Sampling-instant error becomes a larger voltage error as the signal slews faster, so jitter caps SNR at high f_in.",
        ),
    ),
)
