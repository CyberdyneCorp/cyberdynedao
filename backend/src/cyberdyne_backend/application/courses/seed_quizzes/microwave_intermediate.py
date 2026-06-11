from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "S-parameters & network analysis": (
            q(
                "Why are S-parameters preferred over voltage/current at microwave frequencies?",
                (
                    opt("They are easier to write down on paper"),
                    opt(
                        "Probes load the circuit and standing waves make the voltage ambiguous, so we describe how the device scatters waves",
                        correct=True,
                    ),
                    opt("Voltage and current do not exist at microwave frequencies"),
                    opt("S-parameters require no calibration"),
                ),
                "At microwave frequencies probes load the circuit and standing waves make the voltage ambiguous, so devices are described by how they scatter waves.",
            ),
            q(
                "In a two-port, what does S21 represent?",
                (
                    opt("Input reflection"),
                    opt("Output reflection"),
                    opt("Forward transmission, the gain or loss through the device", correct=True),
                    opt("Reverse leakage backward"),
                ),
                "S21 is the forward transmission, the gain or loss through the device, while S11 is input reflection.",
            ),
            q(
                "How is return loss computed from S11?",
                (
                    opt("return loss = -20 log10 |S11|", correct=True),
                    opt("return loss = 20 log10 |S21|"),
                    opt("return loss = -10 log10 |S11|"),
                    opt("return loss = |S11| squared"),
                ),
                "Return loss equals -20 log10 |S11|; insertion loss equals -20 log10 |S21|.",
            ),
        ),
        "Microwave components: couplers, Wilkinson divider, circulators & filters": (
            q(
                "What characteristic impedance do the quarter-wave arms of a Wilkinson divider use in a 50 ohm system?",
                (
                    opt("50 ohm"),
                    opt("about 70.7 ohm, which is sqrt(2) times Z0", correct=True),
                    opt("100 ohm"),
                    opt("36 ohm"),
                ),
                "The Wilkinson uses two quarter-wave lines of sqrt(2)*Z0, about 70.7 ohm for a 50 ohm system, plus a 100 ohm isolation resistor.",
            ),
            q(
                "What makes a circulator non-reciprocal?",
                (
                    opt("A precision capacitor"),
                    opt(
                        "A magnetized ferrite that routes power port 1 to 2, 2 to 3, 3 to 1",
                        correct=True,
                    ),
                    opt("A quarter-wave transformer"),
                    opt("An isolation resistor"),
                ),
                "A circulator is a non-reciprocal three-port using a magnetized ferrite: power goes port 1 to 2, 2 to 3, 3 to 1.",
            ),
            q(
                "What happens when you terminate one port of a circulator?",
                (
                    opt("It becomes a power divider"),
                    opt(
                        "It becomes an isolator that passes the forward wave but absorbs the reflected one",
                        correct=True,
                    ),
                    opt("It becomes a directional coupler"),
                    opt("It stops working entirely"),
                ),
                "Terminating one port turns a circulator into an isolator that passes the forward wave but absorbs the reflected one, protecting the amplifier.",
            ),
        ),
        "Antenna fundamentals: radiation, fields, gain, directivity & beamwidth": (
            q(
                "What is the relationship between gain and directivity?",
                (
                    opt("Gain equals directivity times radiation efficiency", correct=True),
                    opt("Gain equals directivity divided by frequency"),
                    opt("Gain and directivity are always identical"),
                    opt("Gain equals directivity squared"),
                ),
                "Gain G = e_rad * D: directivity reduced by radiation efficiency from ohmic and mismatch losses, usually quoted in dBi.",
            ),
            q(
                "What defines the half-power beamwidth (HPBW)?",
                (
                    opt("Where the pattern drops 3 dB from the main lobe peak", correct=True),
                    opt("Where the sidelobes begin"),
                    opt("The width of the near field"),
                    opt("Where the gain reaches zero"),
                ),
                "The HPBW is the angular width of the main lobe where the pattern drops 3 dB from its peak.",
            ),
            q(
                "What is the trade-off implied by a narrower antenna beam?",
                (
                    opt("Lower gain but wider coverage"),
                    opt(
                        "Higher gain but reduced coverage, trading coverage for reach", correct=True
                    ),
                    opt("No change in gain or coverage"),
                    opt("Higher efficiency but lower directivity"),
                ),
                "A narrower beam means higher gain; you trade coverage for reach. You cannot have an omnidirectional high-gain antenna.",
            ),
        ),
        "The dipole & monopole: half-wave dipole, radiation resistance & pattern": (
            q(
                "What is the approximate radiation resistance of a half-wave dipole?",
                (
                    opt("about 50 ohm"),
                    opt("about 73 ohm", correct=True),
                    opt("about 36 ohm"),
                    opt("about 100 ohm"),
                ),
                "A half-wave dipole has a radiation resistance of about 73 ohm, close to 50 or 75 ohm coax, which is why it is popular.",
            ),
            q(
                "How does a monopole over a ground plane compare to a dipole?",
                (
                    opt("Its radiation resistance is double the dipole's"),
                    opt("It has the same radiation resistance as a dipole"),
                    opt(
                        "Its radiation resistance is about half the dipole's, around 36 ohm, radiating into the upper half-space",
                        correct=True,
                    ),
                    opt("It radiates equally in all directions"),
                ),
                "A lambda/4 monopole uses the ground plane image to act like a dipole, but with about half the radiation resistance, around 36 ohm, radiating into the upper half-space only.",
            ),
            q(
                "Why is a real dipole trimmed slightly shorter than half a wavelength?",
                (
                    opt("To save material cost"),
                    opt(
                        "To cancel the small inductive reactance and hit pure resonance",
                        correct=True,
                    ),
                    opt("To increase its radiation resistance to 73 ohm"),
                    opt("To widen the doughnut pattern"),
                ),
                "A real dipole is trimmed to about 0.48 lambda to cancel the small inductive reactance and reach pure resonance.",
            ),
        ),
        "The link budget & the Friis equation": (
            q(
                "By how much does free-space path loss increase when you double the distance?",
                (
                    opt("3 dB"),
                    opt("6 dB", correct=True),
                    opt("10 dB"),
                    opt("20 dB"),
                ),
                "Doubling the distance costs 6 dB; doubling the frequency also costs another 6 dB.",
            ),
            q(
                "In dB form, how is received power expressed via the Friis equation?",
                (
                    opt("Pr = Pt * Gt * Gr / FSPL"),
                    opt("Pr(dBm) = Pt + Gt + Gr - FSPL", correct=True),
                    opt("Pr(dBm) = Pt - Gt - Gr + FSPL"),
                    opt("Pr(dBm) = Pt + FSPL - Gt - Gr"),
                ),
                "In dB the Friis equation becomes pure addition: Pr(dBm) = Pt + Gt + Gr - FSPL.",
            ),
            q(
                "What does EIRP represent?",
                (
                    opt("The receiver noise floor"),
                    opt(
                        "Pt + Gt, the effective isotropic radiated power the antenna shouts in its best direction",
                        correct=True,
                    ),
                    opt("The link margin after sensitivity"),
                    opt("The cable loss in the chain"),
                ),
                "EIRP = Pt + Gt is the effective isotropic radiated power, what the antenna effectively radiates in its best direction, and what regulators cap.",
            ),
        ),
        "Lab: radiation pattern & Friis link budget": (
            q(
                "In the lab, which normalized field pattern formula is used for the half-wave dipole?",
                (
                    opt("cos(pi/2 * cos(theta)) / sin(theta)", correct=True),
                    opt("sin(theta) / cos(theta)"),
                    opt("cos(theta) squared"),
                    opt("1 / (4*pi*d)"),
                ),
                "The lab computes F = cos(pi/2*cos(theta))/sin(theta), the normalized field pattern of a half-wave dipole.",
            ),
            q(
                "How does the lab determine the usable link range?",
                (
                    opt("By fixing distance at 1 km"),
                    opt(
                        "By taking the maximum distance where received power exceeds the receiver sensitivity",
                        correct=True,
                    ),
                    opt("By doubling the transmitter power"),
                    opt("By measuring the HPBW"),
                ),
                "The lab finds max_range as the largest distance where Pr_dBm exceeds the -90 dBm sensitivity threshold.",
            ),
            q(
                "According to the lab's suggested experiment, what happens if you raise Gt to 20 dBi?",
                (
                    opt("The pattern becomes a doughnut"),
                    opt("The usable range jumps", correct=True),
                    opt("The path loss decreases by 6 dB"),
                    opt("The sensitivity improves to -130 dBm"),
                ),
                "The lab suggests raising Gt to 20 dBi with a directional antenna, which makes the usable range jump.",
            ),
        ),
    },
    final=(
        q(
            "Which pair correctly states return loss and insertion loss?",
            (
                opt(
                    "return loss = -20 log10 |S11|, insertion loss = -20 log10 |S21|", correct=True
                ),
                opt("return loss = -20 log10 |S21|, insertion loss = -20 log10 |S11|"),
                opt("return loss = 20 log10 |S11|, insertion loss = 20 log10 |S21|"),
                opt("return loss = |S11|, insertion loss = |S21|"),
            ),
            "Return loss = -20 log10 |S11| (input match) and insertion loss = -20 log10 |S21| (loss through the device).",
        ),
        q(
            "Which device protects a transmitter amplifier from a bad antenna match by absorbing the reflected wave?",
            (
                opt("A Wilkinson divider"),
                opt("An isolator, a terminated circulator", correct=True),
                opt("A branch-line hybrid"),
                opt("A band-pass filter"),
            ),
            "Terminating a circulator port makes an isolator that passes the forward wave but absorbs the reflected one, protecting the power amplifier.",
        ),
        q(
            "What is the gain of a half-wave dipole relative to isotropic?",
            (
                opt("about 0 dBi"),
                opt("about 2.15 dBi", correct=True),
                opt("about 6 dBi"),
                opt("about 25 dBi"),
            ),
            "The half-wave dipole has a gain of about 2.15 dBi, so 0 dBd equals 2.15 dBi.",
        ),
        q(
            "Using Pr(dBm) = Pt + Gt + Gr - FSPL with Pt=20, Gt=6, Gr=6 dBi and FSPL about 100 dB, what is the received power?",
            (
                opt("about -68 dBm", correct=True),
                opt("about +32 dBm"),
                opt("about -132 dBm"),
                opt("about -100 dBm"),
            ),
            "Pr = 20 + 6 + 6 - 100 = -68 dBm, the link budget worked example.",
        ),
        q(
            "Why is the link budget done entirely in dB?",
            (
                opt("Because dB values are always positive"),
                opt(
                    "Because in dB it becomes simple addition of every plus and minus, keeping a few dB of margin",
                    correct=True,
                ),
                opt("Because dB removes the need for antenna gains"),
                opt("Because dB eliminates free-space path loss"),
            ),
            "In dB the budget is bookkeeping: add every gain and subtract every loss, keeping margin for rain, fading, and aging.",
        ),
    ),
)
