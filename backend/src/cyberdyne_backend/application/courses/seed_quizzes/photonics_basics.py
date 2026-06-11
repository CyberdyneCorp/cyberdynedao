from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Light fundamentals for engineers": (
            q(
                "In vacuum, how are wavelength (lambda) and frequency (f) related to the speed of light c?",
                (
                    opt("c = lambda + f"),
                    opt("c = lambda * f", correct=True),
                    opt("c = f / lambda"),
                    opt("c = lambda / f"),
                ),
                "In vacuum the wavelength and frequency multiply to the speed of light: c = lambda f, with c about 3e8 m/s.",
            ),
            q(
                "Using the engineer's rule E(eV) = 1240 / lambda(nm), how does photon energy change as wavelength gets shorter (toward the blue)?",
                (
                    opt("It stays constant regardless of wavelength"),
                    opt("It decreases"),
                    opt("It increases", correct=True),
                    opt("It drops to zero"),
                ),
                "Shorter wavelength means higher frequency and more energetic photons, so E climbs as you move toward the blue.",
            ),
            q(
                "Inside a material with refractive index n, what happens to the speed of light?",
                (
                    opt("It slows to v = c / n", correct=True),
                    opt("It speeds up to v = c * n"),
                    opt("It is unchanged at c"),
                    opt("It becomes v = n / c"),
                ),
                "In a material light slows to v = c / n; a higher index means slower light and a shorter wavelength inside the material.",
            ),
        ),
        "Reflection, refraction and guiding light": (
            q(
                "Snell's law n1 sin(theta1) = n2 sin(theta2) measures the angle theta from what reference?",
                (
                    opt("The surface itself"),
                    opt("The surface normal", correct=True),
                    opt("The horizontal axis"),
                    opt("The direction of the reflected ray"),
                ),
                "In Snell's law the angle theta is measured from the surface normal.",
            ),
            q(
                "What is the critical angle for total internal reflection equal to?",
                (
                    opt("arcsin(n1/n2)"),
                    opt("arccos(n2/n1)"),
                    opt("arcsin(n2/n1)", correct=True),
                    opt("arctan(n1/n2)"),
                ),
                "The critical angle is theta_c = arcsin(n2/n1), beyond which light reflects completely back.",
            ),
            q(
                "How does an optical fiber trap light along its length?",
                (
                    opt(
                        "A high-index core surrounded by lower-index cladding causes total internal reflection",
                        correct=True,
                    ),
                    opt("A low-index core surrounded by higher-index cladding"),
                    opt("Mirrors coating the outside of the cladding"),
                    opt("Absorbing the light and re-emitting it forward"),
                ),
                "A high-index glass core surrounded by lower-index cladding keeps light bouncing by total internal reflection for kilometres.",
            ),
        ),
        "LEDs and electroluminescence": (
            q(
                "An LED emits light through which process when current flows through its PN junction?",
                (
                    opt("Electroluminescence", correct=True),
                    opt("The photoelectric effect"),
                    opt("Stimulated emission"),
                    opt("Total internal reflection"),
                ),
                "An LED is a PN-junction diode that emits light by electroluminescence: electricity in, light out.",
            ),
            q(
                "In a direct-bandgap LED, what sets the color of the emitted photon?",
                (
                    opt("The series resistor value"),
                    opt("The material's bandgap Eg", correct=True),
                    opt("The forward current alone"),
                    opt("The ambient temperature"),
                ),
                "Each recombination releases a photon whose energy equals the bandgap Eg, so the bandgap sets the color (lambda about 1240/Eg nm).",
            ),
            q(
                "Why should you never drive an LED directly from a voltage source?",
                (
                    opt(
                        "A tiny voltage change makes a huge current change past the forward knee",
                        correct=True,
                    ),
                    opt("The LED would emit the wrong color"),
                    opt("Voltage sources cannot supply enough power"),
                    opt("It would lower the luminous efficacy permanently"),
                ),
                "Current grows steeply past the forward voltage knee, so a tiny voltage change makes a huge current change; you set current with a series resistor or current driver.",
            ),
        ),
        "Photodetectors and the photoelectric effect": (
            q(
                "What underlying effect lets a photodetector turn light into electricity?",
                (
                    opt("Electroluminescence"),
                    opt("The photoelectric effect", correct=True),
                    opt("Total internal reflection"),
                    opt("Population inversion"),
                ),
                "The foundation is the photoelectric effect: a photon with enough energy frees an electron (explained by Einstein in 1905).",
            ),
            q(
                "Why does a PIN photodiode place an intrinsic layer between the P and N regions?",
                (
                    opt("To block all reverse current"),
                    opt(
                        "To widen the depletion region so it absorbs more light and responds fast",
                        correct=True,
                    ),
                    opt("To raise the forward voltage knee"),
                    opt("To convert the diode into a light emitter"),
                ),
                "The wide intrinsic (undoped) depletion region absorbs more light and responds fast, which is why PINs dominate optical receivers.",
            ),
            q(
                "Responsivity R = eta q lambda / (hc). How does ideal responsivity behave as wavelength increases up to the cutoff?",
                (
                    opt("It rises linearly with wavelength", correct=True),
                    opt("It falls linearly with wavelength"),
                    opt("It stays flat at all wavelengths"),
                    opt("It oscillates with wavelength"),
                ),
                "Responsivity rises with wavelength (more photons per watt) until it falls off a cliff at the material's cutoff.",
            ),
        ),
        "Laser basics: stimulated emission and gain": (
            q(
                "In stimulated emission, what does the second emitted photon look like relative to the incoming one?",
                (
                    opt(
                        "An exact clone with the same wavelength, direction, and phase",
                        correct=True,
                    ),
                    opt("A photon of double the energy"),
                    opt("A photon emitted in a random direction"),
                    opt("A photon of a complementary color"),
                ),
                "An incoming photon triggers the atom to emit a second photon that is an exact clone in wavelength, direction, and phase, so light is amplified.",
            ),
            q(
                "What condition is required for a laser medium to show net gain?",
                (
                    opt("A population inversion with more atoms excited than not", correct=True),
                    opt("More atoms in the ground state than excited"),
                    opt("Equal numbers of excited and ground-state atoms"),
                    opt("All atoms in the ground state"),
                ),
                "You need a population inversion, achieved by pumping, so stimulated emission wins over absorption and the medium shows gain.",
            ),
            q(
                "Lasing begins once which condition is met in the optical cavity?",
                (
                    opt("Gain exceeds loss, the threshold", correct=True),
                    opt("Loss exceeds gain"),
                    opt("Both mirrors are fully reflective"),
                    opt("The drive current is below threshold"),
                ),
                "Two mirrors form a resonant cavity; lasing starts once gain exceeds loss, the threshold, after which output climbs almost linearly with pump current.",
            ),
        ),
        "Lab: blackbody, LED spectrum and photodiode responsivity": (
            q(
                "The lab models the silicon photodiode responsivity with a hard cutoff at which wavelength?",
                (
                    opt("Around 630 nm"),
                    opt("Around 850 nm"),
                    opt("Around 1100 nm", correct=True),
                    opt("Around 1550 nm"),
                ),
                "Silicon responsivity is computed as eta*q*lambda/(hc) and then zeroed for lam_nm >= 1100, a hard cutoff past silicon's band.",
            ),
            q(
                "The lab models the LED emission spectrum centered at 630 nm using what shape?",
                (
                    opt("A flat constant line"),
                    opt("A narrow Gaussian bump", correct=True),
                    opt("An exponential decay"),
                    opt("A linear ramp"),
                ),
                "The LED spectrum is a narrow Gaussian-ish bump centered at 630 nm with about 25 nm width.",
            ),
            q(
                "According to the lab's try-it-yourself note, raising the blackbody temperature to 5800 K (the Sun) does what to its spectral peak?",
                (
                    opt("Shifts the peak into the visible", correct=True),
                    opt("Shifts the peak deeper into the infrared"),
                    opt("Removes the peak entirely"),
                    opt("Leaves the peak unchanged"),
                ),
                "Raising T to 5800 K (the Sun) shifts the blackbody peak into the visible, as the comment suggests trying.",
            ),
        ),
    },
    final=(
        q(
            "Which relation correctly links a photon's energy to its wavelength?",
            (
                opt("E = h c lambda"),
                opt("E = h c / lambda", correct=True),
                opt("E = lambda / (h c)"),
                opt("E = h / (c lambda)"),
            ),
            "The Planck relation gives E = h f = h c / lambda, so shorter wavelength means higher energy.",
        ),
        q(
            "Total internal reflection, which traps light in a fiber, occurs when light goes from a denser medium toward a less dense one past the critical angle theta_c equal to:",
            (
                opt("arcsin(n2/n1)", correct=True),
                opt("arcsin(n1/n2)"),
                opt("arccos(n2/n1)"),
                opt("arctan(n2/n1)"),
            ),
            "Beyond theta_c = arcsin(n2/n1) light reflects completely, which is how a high-index core with lower-index cladding guides light.",
        ),
        q(
            "Which statement correctly contrasts an LED with a photodiode?",
            (
                opt(
                    "An LED converts electricity to light by electroluminescence, while a photodiode converts light to current via the photoelectric effect",
                    correct=True,
                ),
                opt("Both convert light into electricity"),
                opt("An LED converts light to current, while a photodiode emits light"),
                opt("Both rely on population inversion to operate"),
            ),
            "An LED emits light from current (electroluminescence); a photodiode does the opposite, generating photocurrent from absorbed photons via the photoelectric effect.",
        ),
        q(
            "What makes a laser's light coherent compared with an LED's?",
            (
                opt(
                    "Stimulated emission produces identical photons, while spontaneous emission sends them every which way",
                    correct=True,
                ),
                opt("A laser uses a wider bandgap material than an LED"),
                opt("A laser has no threshold current"),
                opt("An LED amplifies light while a laser does not"),
            ),
            "Spontaneous emission (LED) sends photons in random directions, while stimulated emission (laser) makes them identical, giving coherence.",
        ),
        q(
            "For a silicon photodiode with responsivity R = eta q lambda / (hc), responsivity rises with wavelength until what happens?",
            (
                opt("It keeps rising forever"),
                opt("It falls off a cliff at the material's cutoff wavelength", correct=True),
                opt("It doubles past the cutoff"),
                opt("It becomes negative"),
            ),
            "Responsivity climbs with wavelength because longer-wavelength photons are more numerous per watt, then drops to zero at the cutoff (about 1100 nm for silicon).",
        ),
    ),
)
