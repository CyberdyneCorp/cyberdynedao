from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Transmission lines: impedance, reflection & VSWR": (
            q(
                "What is the characteristic impedance Z0 of a line in terms of its per-unit-length L and C?",
                (
                    opt("L times C"),
                    opt("square root of L over C", correct=True),
                    opt("square root of C over L"),
                    opt("L divided by C"),
                ),
                "Z0 = sqrt(L/C), set by the line geometry and dielectric.",
            ),
            q(
                "A load equal to Z0 produces what reflection coefficient gamma?",
                (
                    opt("gamma = 1 (total reflection)"),
                    opt("gamma = -1 (short-like)"),
                    opt("gamma = 0 (no reflection)", correct=True),
                    opt("gamma = 0.5"),
                ),
                "A matched load ZL = Z0 gives gamma = (ZL - Z0)/(ZL + Z0) = 0, no reflection.",
            ),
            q(
                "VSWR equals which expression in terms of the magnitude of gamma?",
                (
                    opt("(1 + |gamma|)/(1 - |gamma|)", correct=True),
                    opt("(1 - |gamma|)/(1 + |gamma|)"),
                    opt("|gamma|/(1 - |gamma|)"),
                    opt("1 + |gamma| squared"),
                ),
                "VSWR = (1 + |gamma|)/(1 - |gamma|); it blows up as |gamma| approaches 1.",
            ),
        ),
        "The Smith chart & impedance matching": (
            q(
                "Where on the Smith chart is a perfect match (Z = Z0)?",
                (
                    opt("on the rim of the disk"),
                    opt("at the center", correct=True),
                    opt("at the top edge"),
                    opt("outside the unit disk"),
                ),
                "The center is gamma = 0, Z = Z0; the rim is |gamma| = 1, total reflection.",
            ),
            q(
                "A quarter-wave transformer matching Z0 to a real load ZL uses a line of what impedance?",
                (
                    opt("Z0 plus ZL"),
                    opt("square root of Z0 times ZL", correct=True),
                    opt("Z0 times ZL"),
                    opt("the average of Z0 and ZL"),
                ),
                "A lambda/4 line of Z = sqrt(Z0 * ZL) inverts impedance to match two real impedances.",
            ),
            q(
                "Which matching technique is described as a shorted or open line length placed in shunt?",
                (
                    opt("L-network"),
                    opt("stub", correct=True),
                    opt("quarter-wave transformer"),
                    opt("isolator"),
                ),
                "A stub is a shorted/open line in shunt, a distributed technique good for microwave.",
            ),
        ),
        "Antennas: the dipole, gain & radiation patterns": (
            q(
                "What is the approximate resonant feed impedance of a half-wave dipole?",
                (
                    opt("about 50 ohms"),
                    opt("about 73 ohms", correct=True),
                    opt("about 300 ohms"),
                    opt("about 8 ohms"),
                ),
                "At resonance the half-wave dipole presents about 73 ohms, close to 50 ohm cable.",
            ),
            q(
                "How does gain G relate to directivity D and efficiency e?",
                (
                    opt("G = e times D", correct=True),
                    opt("G = D divided by e"),
                    opt("G = D minus e"),
                    opt("G = e plus D"),
                ),
                "Gain G = e*D, directivity times efficiency, usually quoted in dBi.",
            ),
            q(
                "In the Friis transmission equation, how does received power scale with range R?",
                (
                    opt("as 1/R"),
                    opt("as 1/R squared", correct=True),
                    opt("as 1/R to the fourth"),
                    opt("as R squared"),
                ),
                "Friis gives Pr/Pt = Gt Gr (lambda/(4 pi R))^2, a 1/R^2 free-space spreading loss.",
            ),
        ),
        "Waveguides & microwave components": (
            q(
                "What happens to a wave below a waveguide's cutoff frequency?",
                (
                    opt("it propagates with low loss"),
                    opt("it cannot propagate and decays", correct=True),
                    opt("it travels faster than light carrying information"),
                    opt("it reflects with gain"),
                ),
                "Below cutoff the wave cannot propagate; the guide acts as a high-pass filter.",
            ),
            q(
                "For the dominant rectangular mode, the cutoff frequency fc is approximately given by?",
                (
                    opt("c times 2a"),
                    opt("c divided by 2a", correct=True),
                    opt("2a divided by c"),
                    opt("c divided by a squared"),
                ),
                "fc = c/(2a), where a is the broad-wall width; cutoff is when width is about half a wavelength.",
            ),
            q(
                "Which microwave component routes power one way to protect a transmitter?",
                (
                    opt("directional coupler"),
                    opt("circulator or isolator", correct=True),
                    opt("cavity resonator"),
                    opt("attenuator"),
                ),
                "A circulator/isolator routes power one way, protecting transmitters from reflections.",
            ),
        ),
        "Numerical EM, EMC & shielding": (
            q(
                "Which numerical method steps the fields forward in time on a grid?",
                (
                    opt("FEM"),
                    opt("FDTD", correct=True),
                    opt("MoM"),
                    opt("VSWR"),
                ),
                "FDTD (finite-difference time-domain) leapfrogs E and B forward in time on a grid.",
            ),
            q(
                "What does the Courant condition constrain in an FDTD simulation?",
                (
                    opt("the maximum stable time step relative to cell size", correct=True),
                    opt("the antenna gain"),
                    opt("the load impedance"),
                    opt("the shielding thickness"),
                ),
                "The Courant condition c dt <= dx/sqrt(d) ties the time step to cell size, so finer grids need smaller dt.",
            ),
            q(
                "According to EMC, what are the three levers to reduce interference?",
                (
                    opt("increase voltage, current, and frequency"),
                    opt(
                        "reduce the source, break the coupling path, or harden the victim",
                        correct=True,
                    ),
                    opt("add gain, reduce loss, raise impedance"),
                    opt("widen the waveguide, shorten the stub, lower VSWR"),
                ),
                "EMC works by reducing the source, breaking the coupling path, or hardening the victim circuit.",
            ),
        ),
        "Lab: transmission-line reflection & VSWR": (
            q(
                "In the lab, what value of ZL gives a matched line with VSWR = 1?",
                (
                    opt("ZL = 0 (short)"),
                    opt("ZL = 50 ohm (equal to Z0)", correct=True),
                    opt("ZL = open"),
                    opt("ZL = 100 ohm"),
                ),
                "With Z0 = 50 ohm, setting ZL = 50 gives gamma = 0 and VSWR = 1, a matched line.",
            ),
            q(
                "The lab computes the reflected power fraction as which quantity?",
                (
                    opt("|gamma| squared", correct=True),
                    opt("gamma divided by VSWR"),
                    opt("1 minus VSWR"),
                    opt("Z0 divided by ZL"),
                ),
                "Reflected power fraction = |gamma|^2, as printed by the lab script.",
            ),
            q(
                "Per the lab note, setting ZL = 0 (a short) does what to VSWR and the |V(z)| pattern?",
                (
                    opt("VSWR goes to 1, flat pattern"),
                    opt("VSWR goes to infinity, deep nulls in |V(z)|", correct=True),
                    opt("VSWR halves, no standing wave"),
                    opt("VSWR becomes negative"),
                ),
                "A short gives |gamma| = 1 so VSWR goes to infinity, producing deep nulls in the standing-wave pattern.",
            ),
        ),
        "Applications: RF, radar, wireless, MRI & fiber": (
            q(
                "The radar equation makes returned power fall off as which power of range?",
                (
                    opt("1/R squared"),
                    opt("1/R to the fourth", correct=True),
                    opt("1/R"),
                    opt("R squared"),
                ),
                "Radar power falls as 1/R^4 (out and back), far steeper than a one-way 1/R^2 link.",
            ),
            q(
                "An MRI RF coil operates at the Larmor frequency, which scales with field B0 as?",
                (
                    opt("f = gamma divided by B0"),
                    opt("f = gamma times B0", correct=True),
                    opt("f = B0 squared"),
                    opt("f is independent of B0"),
                ),
                "The Larmor frequency f = gamma * B0 scales linearly with field, about 64 MHz at 1.5 T.",
            ),
            q(
                "What physical effect traps light in the higher-index core of an optical fiber?",
                (
                    opt("total internal reflection", correct=True),
                    opt("waveguide cutoff"),
                    opt("Doppler shift"),
                    opt("impedance matching"),
                ),
                "Light is trapped by total internal reflection in a core of slightly higher index than the cladding.",
            ),
        ),
    },
    final=(
        q(
            "A 50 ohm line feeds a 75 ohm load. What is the VSWR?",
            (
                opt("1.0"),
                opt("1.5", correct=True),
                opt("2.0"),
                opt("0.2"),
            ),
            "gamma = (75-50)/(75+50) = 0.2, so VSWR = (1+0.2)/(1-0.2) = 1.5.",
        ),
        q(
            "Which statement about the Smith chart is correct?",
            (
                opt("the center is total reflection"),
                opt("the rim represents |gamma| = 1, total reflection", correct=True),
                opt("it maps only inductive loads"),
                opt("it cannot represent a matched load"),
            ),
            "The Smith chart maps the impedance plane onto the unit disk; the rim is |gamma| = 1 and the center is a match.",
        ),
        q(
            "Why do waveguides replace coaxial cable at high microwave frequencies?",
            (
                opt("they are cheaper to manufacture"),
                opt(
                    "cables get lossy from dielectric and skin effect, so guides cut loss",
                    correct=True,
                ),
                opt("they support every frequency including DC"),
                opt("they eliminate the need for any matching"),
            ),
            "At high microwave frequencies cables are lossy; a hollow metal waveguide carries the wave with very low loss.",
        ),
        q(
            "A long-range radar link and a one-way wireless link differ in range dependence how?",
            (
                opt("radar falls as 1/R^4 while the one-way link falls as 1/R^2", correct=True),
                opt("both fall as 1/R^2"),
                opt("radar falls as 1/R^2 while the link falls as 1/R^4"),
                opt("neither depends on range"),
            ),
            "Radar power goes out and back (1/R^4) while a one-way Friis link spreads only once (1/R^2).",
        ),
        q(
            "Which tool or method is best suited to broadband, transient, and antenna problems?",
            (
                opt("FEM in the frequency domain"),
                opt("FDTD time-domain stepping", correct=True),
                opt("a quarter-wave transformer"),
                opt("a Faraday cage"),
            ),
            "FDTD steps the fields in time and is well suited to broadband, transients, and antennas.",
        ),
    ),
)
