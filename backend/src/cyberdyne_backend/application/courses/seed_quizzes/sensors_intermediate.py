from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The ADC: sampling & quantization": (
            q(
                "An ADC does two distinct things. What are they?",
                (
                    opt("Sampling in time and quantization in amplitude", correct=True),
                    opt("Amplification and filtering"),
                    opt("Multiplexing and level shifting"),
                    opt("Reconstruction and decimation"),
                ),
                "Sampling chops the signal into snapshots at rate fs; quantization rounds each snapshot to a finite set of levels.",
            ),
            q(
                "For an N-bit ADC spanning Vref, what is the least significant bit (LSB) step?",
                (
                    opt("Vref times 2^N"),
                    opt("Vref divided by 2^N", correct=True),
                    opt("2^N divided by Vref"),
                    opt("Vref divided by N"),
                ),
                "An N-bit ADC has 2^N levels over Vref, so LSB = Vref / 2^N. A 12-bit ADC over 3.3 V gives about 0.8 mV.",
            ),
            q(
                "Which ADC architecture is described as the workhorse MCU ADC using a binary search of one bit per step?",
                (
                    opt("Flash"),
                    opt("SAR", correct=True),
                    opt("Sigma-delta"),
                    opt("R-2R ladder"),
                ),
                "SAR uses a binary search resolving one bit per step at 8-18 bit resolution; flash is fastest but low resolution, sigma-delta is slow but very high resolution.",
            ),
        ),
        "The DAC & signal reconstruction": (
            q(
                "What does the zero-order hold (ZOH) do in a DAC?",
                (
                    opt(
                        "Holds each sample value constant until the next sample arrives",
                        correct=True,
                    ),
                    opt("Linearly interpolates between samples"),
                    opt("Averages the last M samples"),
                    opt("Removes high-frequency images perfectly"),
                ),
                "The ZOH holds each sample constant until the next, producing a staircase approximation of the smooth signal.",
            ),
            q(
                "Why does the staircase output of a DAC need a reconstruction filter?",
                (
                    opt("To add quantization noise back in"),
                    opt("To remove high-frequency images and smooth the steps", correct=True),
                    opt("To increase the sample rate"),
                    opt("To convert the signal back to digital"),
                ),
                "The staircase contains the wanted signal plus high-frequency images; a low-pass reconstruction filter removes those images and smooths the steps.",
            ),
            q(
                "Which DAC approach has a microcontroller toggle a pin fast and use an RC filter to average it into an analog level?",
                (
                    opt("R-2R ladder"),
                    opt("Sigma-delta"),
                    opt("PWM as a poor man's DAC", correct=True),
                    opt("Flash"),
                ),
                "PWM as a poor man's DAC toggles a pin quickly and an RC filter averages it into an analog level.",
            ),
        ),
        "Anti-aliasing & sampling theory": (
            q(
                "The Nyquist-Shannon theorem requires sampling at what rate relative to the highest frequency component?",
                (
                    opt("More than twice the highest frequency", correct=True),
                    opt("Exactly equal to the highest frequency"),
                    opt("Half the highest frequency"),
                    opt("Ten times the LSB"),
                ),
                "To capture a signal faithfully you must sample at more than twice its highest frequency; fNyquist = fs/2.",
            ),
            q(
                "What happens to signal content above fs/2 when sampled?",
                (
                    opt("It is perfectly preserved"),
                    opt("It folds back and aliases as a lower frequency", correct=True),
                    opt("It is amplified"),
                    opt("It is removed by quantization"),
                ),
                "Content above fs/2 folds back (aliases) and masquerades as a lower frequency, like the wagon wheel appearing to spin backwards.",
            ),
            q(
                "By the oversampling rule, every 4x of oversampling adds roughly how much resolution?",
                (
                    opt("About 1 bit", correct=True),
                    opt("About 6 bits"),
                    opt("About 0.1 bit"),
                    opt("About 4 bits"),
                ),
                "Delta ENOB = 0.5 log2(OSR), so a 4x oversampling ratio adds about 1 effective bit.",
            ),
        ),
        "Digital filtering of sensor data": (
            q(
                "Averaging M independent noisy samples reduces random noise by what factor?",
                (
                    opt("M"),
                    opt("square root of M", correct=True),
                    opt("M squared"),
                    opt("log2 of M"),
                ),
                "A moving average over M independent samples reduces random noise by sqrt(M); residual noise scales as 1/sqrt(M).",
            ),
            q(
                "In the exponential moving average y[n] = alpha x[n] + (1-alpha) y[n-1], what does a small alpha give?",
                (
                    opt("Heavy smoothing and slow response", correct=True),
                    opt("Light smoothing and fast response"),
                    opt("No smoothing at all"),
                    opt("Linear phase like an FIR filter"),
                ),
                "Small alpha means heavy smoothing and slow response; large alpha means light smoothing and fast response.",
            ),
            q(
                "What does the Kalman filter require that a plain average does not?",
                (
                    opt(
                        "A model of how the signal should evolve plus noisy measurements",
                        correct=True,
                    ),
                    opt("A higher sample rate than Nyquist"),
                    opt("An analog anti-aliasing filter"),
                    opt("A flash ADC architecture"),
                ),
                "The Kalman filter is optimal when you have a model of the signal's evolution plus noisy measurements, predicting then correcting weighted by uncertainties.",
            ),
        ),
        "Sensor interfaces & DAQ systems": (
            q(
                "What is the analog front-end (AFE) in a DAQ system?",
                (
                    opt(
                        "Everything between the sensor and the ADC: amplification, filtering, level shifting, often a multiplexer",
                        correct=True,
                    ),
                    opt("The digital storage and network layer"),
                    opt("The reconstruction filter after a DAC"),
                    opt("The MCU that processes samples"),
                ),
                "The AFE is everything between the sensor and the ADC: amplification, filtering/anti-aliasing, level shifting, and often a multiplexer.",
            ),
            q(
                "How do I2C and SPI buses compare?",
                (
                    opt(
                        "I2C uses 2 shared addressed wires and is slower; SPI uses 4 wires with a chip-select per device and is faster",
                        correct=True,
                    ),
                    opt("I2C is always faster than SPI"),
                    opt("SPI uses only 2 wires and addresses devices"),
                    opt("Both use exactly 3 wires and the same speed"),
                ),
                "I2C trades speed for wiring simplicity (2 shared wires, addressed); SPI is faster but needs a chip-select line per device.",
            ),
            q(
                "Why insist on simultaneous sampling rather than multiplexing for some applications?",
                (
                    opt(
                        "Multiplexed scans add channel-to-channel time skew that corrupts phase",
                        correct=True,
                    ),
                    opt("Multiplexing always lowers resolution"),
                    opt("Simultaneous sampling avoids the need for any ADC"),
                    opt("Multiplexing cannot meet Nyquist"),
                ),
                "A multiplexed scan introduces a channel-to-channel time skew; for true phase relationships (power, multi-accelerometer vibration) use simultaneous sampling.",
            ),
        ),
        "Lab: ADC quantization noise & oversampling gain": (
            q(
                "In the lab, what does the line snr_meas = 10 log10(mean(x^2)/mean(qnoise^2)) compute?",
                (
                    opt("The measured quantization signal-to-noise ratio in dB", correct=True),
                    opt("The LSB step size"),
                    opt("The Nyquist frequency"),
                    opt("The number of channels"),
                ),
                "It is the measured quantization SNR in dB, the ratio of signal power to quantization-noise power; ENOB is then (snr-1.76)/6.02.",
            ),
            q(
                "How does the lab achieve oversampling gain across the OSR list?",
                (
                    opt("It block-averages groups of OSR samples to decimate", correct=True),
                    opt("It increases the bit count N directly"),
                    opt("It adds an analog anti-aliasing filter"),
                    opt("It raises Vfs to full scale"),
                ),
                "For each OSR it reshapes the quantized samples into blocks and averages them (decimate by averaging), recovering effective bits.",
            ),
            q(
                "Per the lab's 'Try it yourself', setting N = 4 instead of 6 does what to the SNR?",
                (
                    opt("Drops it about 12 dB (2 bits times 6 dB)", correct=True),
                    opt("Raises it about 12 dB"),
                    opt("Leaves it unchanged"),
                    opt("Drops it about 1.76 dB"),
                ),
                "Each bit is worth about 6 dB, so dropping from 6 to 4 bits lowers SNR by about 12 dB.",
            ),
        ),
    },
    final=(
        q(
            "What is the maximum signal-to-noise ratio of an ideal N-bit converter?",
            (
                opt("About 6.02 N + 1.76 dB", correct=True),
                opt("About N + 1.76 dB"),
                opt("About 2^N dB"),
                opt("About Vref / 2^N dB"),
            ),
            "An ideal N-bit converter has SNR_max of about 6.02 N + 1.76 dB, so every extra bit buys about 6 dB.",
        ),
        q(
            "What does ENOB (effective number of bits) capture?",
            (
                opt("The honest resolution from measured SNR: (SNR_dB - 1.76)/6.02", correct=True),
                opt("The datasheet bit count regardless of noise"),
                opt("The number of comparators in a flash ADC"),
                opt("The oversampling ratio"),
            ),
            "ENOB = (SNR_dB - 1.76)/6.02 reflects real noise and distortion, often fewer than the datasheet bit count.",
        ),
        q(
            "Why must the anti-aliasing filter be analog and sit before the ADC?",
            (
                opt(
                    "Aliasing is irreversible after sampling, so offending high frequencies must be removed before the ADC",
                    correct=True,
                ),
                opt("Digital filters are too slow to run after sampling"),
                opt("The DAC requires it for reconstruction"),
                opt("It increases the LSB size"),
            ),
            "Aliasing cannot be undone by any DSP once it has happened, so an analog low-pass with cutoff below fs/2 must precede the ADC.",
        ),
        q(
            "Every filter trades noise reduction for what, which matters especially in a control loop?",
            (
                opt("Delay / lag", correct=True),
                opt("Resolution bits"),
                opt("Reference voltage"),
                opt("Bus speed"),
            ),
            "More smoothing always means more lag; in a control loop lag causes instability, so pick the lightest filter meeting the noise spec.",
        ),
        q(
            "In a DAQ chain, what is the correct order of building blocks from the physical phenomenon?",
            (
                opt(
                    "Sensor, analog front-end, multiplexer, sample and hold, ADC, MCU, storage",
                    correct=True,
                ),
                opt("ADC, sensor, MCU, DAC, storage"),
                opt("Sensor, ADC, anti-alias filter, MCU"),
                opt("MCU, DAC, sensor, multiplexer, ADC"),
            ),
            "The DAQ chain runs sensor to AFE (amp + filter) to multiplexer to sample and hold to ADC to MCU to storage/network.",
        ),
    ),
)
