from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Sensor fusion & estimation": (
            q(
                "Why does fusing a gyroscope and an accelerometer work well for estimating tilt?",
                (
                    opt("Both sensors are perfectly accurate so they confirm each other"),
                    opt(
                        "They fail in opposite frequency bands: the gyro drifts at low frequency, the accel is noisy",
                        correct=True,
                    ),
                    opt("The accelerometer is faster than the gyro at every frequency"),
                    opt(
                        "The gyro provides a drift-free absolute angle and the accel provides smooth changes"
                    ),
                ),
                "The gyro is smooth and fast but drifts; the accel is drift-free but noisy, so they complement each other across frequency.",
            ),
            q(
                "In the complementary filter, what does the blend factor alpha control?",
                (
                    opt(
                        "How much weight is given to the integrated gyro vs the accelerometer angle",
                        correct=True,
                    ),
                    opt("The sample period dt of the loop"),
                    opt("The covariance of the Kalman state estimate"),
                    opt("The Hall coefficient of the magnetometer"),
                ),
                "theta = alpha*(theta + gyro*dt) + (1-alpha)*accel_angle, so alpha sets the gyro vs accel weighting.",
            ),
            q(
                "What do the two steps of the Kalman filter do each cycle?",
                (
                    opt("Calibrate then linearize the raw sensor reading"),
                    opt("Modulate then demodulate the signal at a reference frequency"),
                    opt(
                        "Predict advances the state and grows uncertainty; Update blends the measurement via the Kalman gain",
                        correct=True,
                    ),
                    opt("Average N samples then shield the wiring"),
                ),
                "The Kalman filter predicts with a motion model (uncertainty grows), then updates with the measurement weighted by gain K.",
            ),
        ),
        "Calibration, linearization & compensation": (
            q(
                "What is the purpose of linearization for a sensor?",
                (
                    opt("To remove temperature drift from the offset"),
                    opt("To improve SNR by averaging many samples"),
                    opt(
                        "To straighten a nonlinear sensor curve, e.g. via a polynomial fit or a lookup table",
                        correct=True,
                    ),
                    opt("To reject ambient light using modulated LEDs"),
                ),
                "Linearization straightens the curve using a polynomial fit or a lookup table with interpolation.",
            ),
            q(
                "Temperature compensation typically corrects which two drifting parameters?",
                (
                    opt(
                        "Offset/zero drift and span/sensitivity drift",
                        correct=True,
                    ),
                    opt("Sample rate and channel count"),
                    opt("Kalman gain and process noise"),
                    opt("Duty cycle and sleep current"),
                ),
                "Offset (zero) drift and span (sensitivity/slope) drift both wander with temperature and are compensated.",
            ),
            q(
                "Why is a two-point calibration insufficient for a curved sensor?",
                (
                    opt("It overcorrects and inverts the sensor reading"),
                    opt(
                        "It only fixes a straight line, so a curved response needs many points and a fit or LUT",
                        correct=True,
                    ),
                    opt("It requires a lock-in amplifier to function"),
                    opt("It cannot be done in software"),
                ),
                "A single gain/offset only fixes a straight line; curved sensors need multi-point calibration with a fit or LUT.",
            ),
        ),
        "Precision & low-noise measurement": (
            q(
                "By how much does averaging N uncorrelated samples improve SNR?",
                (
                    opt("By a factor of N"),
                    opt("By a factor of sqrt(N)", correct=True),
                    opt("By a factor of N squared"),
                    opt("It does not improve SNR at all"),
                ),
                "Random noise is uncorrelated between samples, so averaging N samples improves SNR by sqrt(N).",
            ),
            q(
                "How does a lock-in amplifier recover a tiny signal buried in noise?",
                (
                    opt("It averages thousands of samples at DC"),
                    opt("It increases the supply voltage to boost the signal"),
                    opt(
                        "It modulates at a reference frequency then uses synchronous detection so only components at fref survive",
                        correct=True,
                    ),
                    opt("It fits a cubic polynomial to the noisy data"),
                ),
                "The lock-in modulates at fref then multiplies by a reference and low-pass filters, so only signal at fref survives.",
            ),
            q(
                "What does chopper stabilization correct in an amplifier?",
                (
                    opt(
                        "Slow offset and 1/f noise, by modulating the signal above the noisy region",
                        correct=True,
                    ),
                    opt("The aliasing caused by undersampling"),
                    opt("The temperature span drift of a thermistor"),
                    opt("The Coriolis error of a MEMS gyro"),
                ),
                "Chopper stabilization swaps inputs to correct slow offset and 1/f noise by modulating above the noisy region.",
            ),
        ),
        "MEMS & modern sensors": (
            q(
                "What does MEMS stand for and what does it put on a silicon chip?",
                (
                    opt("Multi-Element Measurement System; multiple ADCs"),
                    opt(
                        "Micro-electro-mechanical systems; tiny mechanical structures like springs and masses",
                        correct=True,
                    ),
                    opt("Modulated Edge Measurement Sensor; a lock-in detector"),
                    opt("Magnetic Effect Motion Sensor; Hall plates only"),
                ),
                "MEMS (micro-electro-mechanical systems) put tiny mechanical structures such as springs, masses, and beams on silicon.",
            ),
            q(
                "Which MEMS sensor uses the Coriolis force acting on a vibrating mass?",
                (
                    opt("Accelerometer"),
                    opt("Gyroscope", correct=True),
                    opt("Pressure sensor"),
                    opt("Photodiode"),
                ),
                "The MEMS gyroscope measures angular rate via the Coriolis force on a vibrating mass.",
            ),
            q(
                "Why does an IMU run sensor fusion internally?",
                (
                    opt("To increase its sample rate beyond the ADC limit"),
                    opt("To reduce its power consumption by duty cycling"),
                    opt(
                        "Because a gyro drifts and an accelerometer is noisy, so fusion yields a clean drift-free orientation",
                        correct=True,
                    ),
                    opt("To convert magnetic field into a Hall voltage"),
                ),
                "An IMU fuses its accel and gyro (and often magnetometer) so the drifting gyro and noisy accel produce a clean orientation.",
            ),
        ),
        "Instrumentation systems & standards": (
            q(
                "What does a DAQ system bundle together?",
                (
                    opt(
                        "Signal conditioning, multiplexing, ADCs, and a host interface",
                        correct=True,
                    ),
                    opt("A gyro, an accelerometer, and a magnetometer"),
                    opt("A lock-in amplifier and a chopper op-amp"),
                    opt("Only a battery and a wireless radio"),
                ),
                "A DAQ system bundles signal conditioning, multiplexing, ADCs, and a host interface such as USB, Ethernet, or PCIe.",
            ),
            q(
                "What is SCADA used for?",
                (
                    opt("Linearizing a single nonlinear sensor"),
                    opt(
                        "Supervisory monitoring and control of distributed industrial processes via PLCs and RTUs",
                        correct=True,
                    ),
                    opt("Fusing a gyro and accelerometer on one chip"),
                    opt("Averaging samples to improve SNR"),
                ),
                "SCADA (Supervisory Control And Data Acquisition) monitors and controls distributed processes through PLCs and RTUs.",
            ),
            q(
                "For an IoT battery sensor, what is the defining constraint and key technique?",
                (
                    opt("Channel count; simultaneous sampling"),
                    opt("CMRR; driven-right-leg guarding"),
                    opt(
                        "Energy; duty cycling so the device sleeps most of the time and wakes briefly",
                        correct=True,
                    ),
                    opt("Hall coefficient; magnetoresistive sensing"),
                ),
                "The defining IoT constraint is energy, so duty cycling (sleep most of the time, wake briefly) extends battery life.",
            ),
        ),
        "Lab: Kalman & complementary sensor fusion": (
            q(
                "In the lab, why does the gyro-only estimate (cumsum of gyro times dt) drift away?",
                (
                    opt("Because the accelerometer angle is too noisy"),
                    opt(
                        "Because integrating the constant gyro_bias accumulates a growing error",
                        correct=True,
                    ),
                    opt("Because alpha is set too low in the complementary filter"),
                    opt("Because the Kalman gain K is fixed at 1"),
                ),
                "gyro_only integrates the gyro signal including the constant gyro_bias, so the bias accumulates and the estimate drifts.",
            ),
            q(
                "In the lab Kalman filter, what does lowering R toward Q do?",
                (
                    opt(
                        "Makes the filter trust the noisy accelerometer more, producing a noisier estimate",
                        correct=True,
                    ),
                    opt("Makes the filter ignore the accelerometer entirely"),
                    opt("Increases the gyro_bias to drift off-screen"),
                    opt("Changes the true_angle ground truth"),
                ),
                "The Try-it note: lowering R toward Q makes the Kalman filter trust the noisy accel more, giving a noisier estimate.",
            ),
            q(
                "What does the complementary filter update line in the lab compute?",
                (
                    opt("A polynomial fit of the calibration data"),
                    opt("The RMS error of each estimator"),
                    opt(
                        "comp[k] = alpha*(comp[k-1] + gyro[k]*dt) + (1-alpha)*accel_angle[k]",
                        correct=True,
                    ),
                    opt("The synchronous lock-in detection of the signal"),
                ),
                "The complementary step blends the gyro-integrated previous estimate with the accel angle using alpha = 0.98.",
            ),
        ),
        "Applications: industrial, medical, automotive & IoT": (
            q(
                "Why are 4-20 mA current loops favored for industrial sensor transmission?",
                (
                    opt("They require no power supply"),
                    opt("They are noise-immune analog transmission over long cables", correct=True),
                    opt("They are the only way to fuse multiple sensors"),
                    opt("They eliminate the need for calibration"),
                ),
                "4-20 mA current loops give noise-immune analog transmission over long cables in industrial settings.",
            ),
            q(
                "Which precision technique is used in pulse oximetry to reject ambient light?",
                (
                    opt("Lock-in style modulated LEDs", correct=True),
                    opt("Duty-cycled deep sleep"),
                    opt("4-20 mA current loops"),
                    opt("Polynomial linearization"),
                ),
                "Pulse oximetry uses an optical sensor with lock-in style modulated LEDs to reject ambient light.",
            ),
            q(
                "In a modern car, which bus commonly ties the hundreds of sensors together?",
                (
                    opt("Modbus"),
                    opt("OPC-UA"),
                    opt("CAN", correct=True),
                    opt("LoRa"),
                ),
                "A modern car ties its many sensors together over the CAN bus, with functional safety governed by ISO 26262.",
            ),
        ),
    },
    final=(
        q(
            "Which statement best captures the role of the Kalman filter in sensor fusion?",
            (
                opt("It straightens a nonlinear sensor curve using a lookup table"),
                opt(
                    "It is the optimal fusion engine for linear Gaussian systems, predicting then updating with a gain-weighted measurement",
                    correct=True,
                ),
                opt("It rejects 1/f noise by chopping the amplifier inputs"),
                opt("It extends battery life by duty cycling the radio"),
            ),
            "The Kalman filter is the optimal fusion engine for linear Gaussian systems; it predicts then updates with the gain-weighted measurement.",
        ),
        q(
            "A pressure sensor calibrated at 25 C reads wrong on a cold morning. What fixes this?",
            (
                opt("Averaging more samples"),
                opt("Increasing the modulation frequency"),
                opt(
                    "Temperature compensation that measures T and corrects offset and gain drift",
                    correct=True,
                ),
                opt("Switching from CAN to Modbus"),
            ),
            "Temperature compensation measures temperature and corrects offset and gain drift so the reading stays accurate.",
        ),
        q(
            "What is the single most powerful idea behind lock-in amplifiers, choppers, and AC bridge excitation?",
            (
                opt("Fit a higher-order polynomial to the data"),
                opt(
                    "Modulate away from DC: measure where the spectrum is quiet, then bring it back",
                    correct=True,
                ),
                opt("Sample as fast as the ADC allows"),
                opt("Use a single-point ground only"),
            ),
            "The unifying precision idea is to modulate away from DC into a quiet part of the spectrum, measure there, and bring it back.",
        ),
        q(
            "An IMU combines a 3-axis accelerometer and a 3-axis gyro (often a magnetometer). What does fusion give it?",
            (
                opt("A higher ADC resolution"),
                opt("Immunity to the Coriolis force"),
                opt("A clean, drift-free orientation estimate", correct=True),
                opt("A noise-immune 4-20 mA output"),
            ),
            "Fusing the noisy accel with the drifting gyro (and magnetometer) yields a clean, drift-free orientation estimate.",
        ),
        q(
            "Why fuse multiple sensors instead of trusting one, per the automotive example?",
            (
                opt("Fusion removes the need for any calibration"),
                opt("A single sensor is cheaper to install"),
                opt(
                    "The fused error shrinks roughly as 1/sqrt(N) compared to a single sensor's larger error",
                    correct=True,
                ),
                opt("Fusion increases the duty cycle of each sensor"),
            ),
            "The applications plot shows the fused error scaling about as 1/sqrt(N), far below a single sensor's error.",
        ),
    ),
)
