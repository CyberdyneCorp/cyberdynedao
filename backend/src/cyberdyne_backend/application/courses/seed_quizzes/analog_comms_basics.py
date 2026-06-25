"""Curated quiz questions for the Analog Communications - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Signals, spectra & bandwidth": (
            q(
                "What does the bandwidth of a signal describe?",
                (
                    opt("The maximum voltage the signal can reach"),
                    opt("The span of frequencies the signal occupies", correct=True),
                    opt("The total energy carried by the signal"),
                    opt("How long the signal lasts in time"),
                ),
                "Bandwidth is the span of frequencies a signal occupies, limiting channel capacity and rate.",
            ),
            q(
                "Why must a baseband signal be shifted up to a carrier frequency before transmission?",
                (
                    opt("To reduce the amount of noise in the channel"),
                    opt("To make the signal narrower in bandwidth"),
                    opt(
                        "Because baseband signals cannot radiate efficiently from an antenna; the shift is modulation",
                        correct=True,
                    ),
                    opt("Because the Fourier transform requires it"),
                ),
                "Baseband signals can't travel far as radio, so we shift them to a carrier frequency; that shift is modulation.",
            ),
            q(
                "Which two views describe the same signal?",
                (
                    opt("The analog domain and the digital domain"),
                    opt("The time domain and the frequency domain (spectrum)", correct=True),
                    opt("The carrier domain and the message domain"),
                    opt("The transmit domain and the receive domain"),
                ),
                "A signal can be viewed in the time domain or the frequency domain (its spectrum); Fourier links them.",
            ),
        ),
        "The communication-system block diagram": (
            q(
                "What does the modulator do in the communication chain?",
                (
                    opt("It removes noise added by the channel"),
                    opt(
                        "It impresses the message onto a high-frequency carrier so it can radiate efficiently",
                        correct=True,
                    ),
                    opt("It amplifies the message to a higher voltage only"),
                    opt("It converts the message from analog to digital"),
                ),
                "The modulator impresses m(t) onto a high-frequency carrier so the signal can radiate from an antenna.",
            ),
            q(
                "Which two figures of merit recur when comparing analog modulation schemes?",
                (
                    opt("Voltage and current"),
                    opt("Bandwidth consumed and signal-to-noise ratio delivered", correct=True),
                    opt("Carrier frequency and antenna length"),
                    opt("Sampling rate and bit depth"),
                ),
                "Analog schemes are trades between the bandwidth they consume and the SNR they deliver.",
            ),
            q(
                "What does the channel contribute to the transmitted signal?",
                (
                    opt("It demodulates the signal back to baseband"),
                    opt(
                        "It adds noise and attenuation, and sometimes interference and fading",
                        correct=True,
                    ),
                    opt("It increases the signal's bandwidth on purpose"),
                    opt("It synchronizes the local oscillator"),
                ),
                "The channel carries the signal but adds noise, attenuation, and sometimes interference and fading.",
            ),
        ),
        "Amplitude modulation (AM) basics": (
            q(
                "In standard AM, what does the carrier's envelope trace out?",
                (
                    opt("The carrier frequency"),
                    opt("The message (as 1 + μ·m(t))", correct=True),
                    opt("The noise power spectrum"),
                    opt("A constant amplitude"),
                ),
                "In standard AM the envelope is 1 + μ·m(t), so it literally traces the message.",
            ),
            q(
                "A single message tone produces how many spectral lines in standard AM?",
                (
                    opt("One: just the carrier"),
                    opt("Two: the two sidebands only"),
                    opt("Three: the carrier plus an upper and a lower sideband", correct=True),
                    opt("Infinitely many sidebands"),
                ),
                "AM of one tone gives the carrier at fc plus sidebands at fc ± fm — three lines.",
            ),
            q(
                "How much spectrum does AM of a message of bandwidth B occupy?",
                (
                    opt("B (the message bandwidth)"),
                    opt("2B (twice the message bandwidth)", correct=True),
                    opt("Half of B"),
                    opt("It depends only on the carrier frequency"),
                ),
                "AM keeps both sidebands, so it occupies 2B — twice the message bandwidth.",
            ),
        ),
        "DSB-SC & coherent detection": (
            q(
                "What is removed in DSB-SC compared with standard AM?",
                (
                    opt("Both sidebands"),
                    opt(
                        "The carrier line (no added DC), so all power carries information",
                        correct=True,
                    ),
                    opt("The upper sideband only"),
                    opt("The noise"),
                ),
                "DSB-SC suppresses the carrier line, so all transmitted power carries information.",
            ),
            q(
                "Why can't a simple envelope detector recover a DSB-SC signal?",
                (
                    opt("Because DSB-SC has no sidebands"),
                    opt(
                        "Because the envelope follows |m(t)| and flips phase at zero crossings, not m(t)",
                        correct=True,
                    ),
                    opt("Because the carrier frequency is too high"),
                    opt("Because DSB-SC is a digital signal"),
                ),
                "Without a carrier the envelope tracks |m(t)| and flips phase at zero crossings, so it isn't m(t).",
            ),
            q(
                "What happens in coherent detection if the local oscillator has a 90 degree phase error?",
                (
                    opt("The output doubles in amplitude"),
                    opt("The output is unchanged"),
                    opt(
                        "The recovered signal disappears (the quadrature-null effect)", correct=True
                    ),
                    opt("The carrier reappears"),
                ),
                "A phase error φ scales the output by cos φ; at 90 degrees cos φ = 0, so the signal vanishes.",
            ),
        ),
        "Envelope detection & modulation index": (
            q(
                "What condition on the modulation index keeps an envelope detector working without distortion?",
                (
                    opt("μ must be greater than 1"),
                    opt("μ must be less than or equal to 1 (≤ 100%)", correct=True),
                    opt("μ must equal the carrier frequency"),
                    opt("μ must be exactly zero"),
                ),
                "The envelope stays positive only when 1 + μ·m(t) > 0, which requires μ ≤ 1.",
            ),
            q(
                "What is over-modulation?",
                (
                    opt("Using too high a carrier frequency"),
                    opt(
                        "μ > 1, so the envelope folds through zero and the detector distorts the message",
                        correct=True,
                    ),
                    opt("Adding too much noise to the channel"),
                    opt("Sampling the signal too fast"),
                ),
                "When μ > 1 the envelope goes negative (folds through zero), causing severe detector distortion.",
            ),
            q(
                "Why is broadcast AM considered power-inefficient even at full modulation?",
                (
                    opt("The sidebands carry no information"),
                    opt(
                        "Most transmitted power sits in the carrier; even at μ = 1 only about a third is in the sidebands",
                        correct=True,
                    ),
                    opt("The envelope detector consumes most of the power"),
                    opt("The bandwidth is only B"),
                ),
                "Efficiency is μ²/(2+μ²); even at μ = 1 that is only 33%, the rest is the wasted carrier.",
            ),
        ),
        "Intro to noise & SNR in comms": (
            q(
                "What is the dominant noise model used for a communication channel?",
                (
                    opt("Periodic interference at the carrier frequency"),
                    opt("Additive white Gaussian noise (thermal noise)", correct=True),
                    opt("Quantization noise"),
                    opt("Phase noise from the modulator"),
                ),
                "Thermal noise is modelled as additive white Gaussian noise: flat in frequency, Gaussian in amplitude.",
            ),
            q(
                "By roughly how much does the SNR change when you double the signal power?",
                (
                    opt("It increases by about 3 dB", correct=True),
                    opt("It increases by about 10 dB"),
                    opt("It decreases by about 3 dB"),
                    opt("It does not change"),
                ),
                "Doubling power adds about 3 dB; halving receiver bandwidth (when allowed) also adds about 3 dB.",
            ),
            q(
                "Why does a wider receiver bandwidth hurt SNR?",
                (
                    opt("It lowers the carrier frequency"),
                    opt("Noise power is N0·B, so more bandwidth lets in more noise", correct=True),
                    opt("It reduces the signal power"),
                    opt("It increases the modulation index"),
                ),
                "Noise power grows as N0·B, so a wider receiver admits more noise, lowering SNR.",
            ),
        ),
    },
    final=(
        q(
            "What is modulation, fundamentally?",
            (
                opt("Removing noise from a received signal"),
                opt(
                    "Shifting a baseband message up onto a carrier so it can radiate efficiently",
                    correct=True,
                ),
                opt("Converting an analog signal to bits"),
                opt("Amplifying a signal to a higher voltage"),
            ),
            "Modulation shifts a baseband message onto a carrier so it can radiate from an antenna.",
        ),
        q(
            "How does the bandwidth occupied by standard AM compare with DSB-SC?",
            (
                opt("AM uses B, DSB-SC uses 2B"),
                opt("Both occupy 2B; DSB-SC just drops the carrier line", correct=True),
                opt("DSB-SC uses 4B, AM uses 2B"),
                opt("Both occupy only B"),
            ),
            "Both keep two sidebands and occupy 2B; DSB-SC simply suppresses the carrier line.",
        ),
        q(
            "Which detection method does DSB-SC require, and why?",
            (
                opt("Envelope detection, because the envelope tracks m(t)"),
                opt(
                    "Coherent detection with a phase-locked local oscillator, because the envelope no longer tracks m(t)",
                    correct=True,
                ),
                opt("No detection is needed"),
                opt("Digital sampling, because DSB-SC is digital"),
            ),
            "DSB-SC needs coherent (synchronous) detection with a phase-locked oscillator since the envelope isn't m(t).",
        ),
        q(
            "Why does standard AM keep a full carrier despite the power waste?",
            (
                opt("To increase the modulation index"),
                opt("To enable the extremely cheap envelope detector", correct=True),
                opt("To reduce the occupied bandwidth"),
                opt("To remove the need for an antenna"),
            ),
            "The full carrier lets a cheap diode-RC envelope detector recover the message — no local oscillator needed.",
        ),
        q(
            "Which statement about SNR is correct?",
            (
                opt("SNR is the noise power divided by the signal power"),
                opt(
                    "SNR is signal power over noise power; doubling signal power adds about 3 dB",
                    correct=True,
                ),
                opt("SNR is unaffected by receiver bandwidth"),
                opt("SNR is measured only in linear units, never in dB"),
            ),
            "SNR = signal power / noise power; doubling signal power adds about 3 dB, expressed as 10·log10 SNR.",
        ),
        q(
            "What limits how much power in standard AM actually carries information?",
            (
                opt("The receiver bandwidth"),
                opt(
                    "The carrier conveys no information; only the sidebands do, so efficiency is low",
                    correct=True,
                ),
                opt("The Fourier transform"),
                opt("The antenna length"),
            ),
            "The carrier line carries no message; only the sidebands do, which is why AM efficiency is poor.",
        ),
    ),
)
