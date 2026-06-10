from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Maxwell's equations": (
            q(
                "What does the displacement current term that Maxwell added to Ampere's law represent?",
                (
                    opt("A real flow of charges across the capacitor gap"),
                    opt(
                        "A changing electric field acting like a current to make a magnetic field",
                        correct=True,
                    ),
                    opt("The magnetic charge that closes B field loops"),
                    opt("The static charge density that diverges the E field"),
                ),
                "Maxwell's fix added the term mu0 eps0 dE/dt, so a changing electric field acts like a current and makes a magnetic field.",
            ),
            q(
                "Which Maxwell equation expresses that there are no magnetic monopoles?",
                (
                    opt("Divergence of E equals rho over eps0"),
                    opt("Divergence of B equals zero", correct=True),
                    opt("Curl of E equals minus dB/dt"),
                    opt("Curl of B equals mu0 J plus mu0 eps0 dE/dt"),
                ),
                "Gauss's law for magnetism states the divergence of B is zero, meaning B field loops close and no magnetic monopoles exist.",
            ),
            q(
                "Why is the displacement current negligible at DC but dominant at optical frequencies?",
                (
                    opt("It scales with frequency, so it grows as f increases", correct=True),
                    opt("It scales with charge density, which is zero at DC"),
                    opt("It only exists inside conductors, not in free space"),
                    opt("It is constant but is screened out at low frequency"),
                ),
                "The displacement current density depends on dE/dt and therefore scales with frequency, negligible at DC and dominant at radio and optical frequencies.",
            ),
        ),
        "The wave equation & electromagnetic waves": (
            q(
                "What speed falls out of the wave equation derived from Maxwell's curl equations in empty space?",
                (
                    opt("v = 1 over sqrt(L C)"),
                    opt("c = 1 over sqrt(mu0 eps0), about 3.00e8 m/s", correct=True),
                    opt("c = lambda over f"),
                    opt("v = mu0 eps0"),
                ),
                "Combining Maxwell's curl equations gives the wave equation with speed c = 1/sqrt(mu0 eps0), about 3.00e8 m/s, matching the measured speed of light.",
            ),
            q(
                "In a plane EM wave, how are E and B oriented relative to the direction of travel?",
                (
                    opt("Both are parallel to the direction of travel"),
                    opt(
                        "Each is perpendicular to the other and to the direction of travel (transverse)",
                        correct=True,
                    ),
                    opt("E is along the travel direction, B is perpendicular"),
                    opt("They oscillate 90 degrees out of phase in time"),
                ),
                "The plane wave is transverse: E and B are perpendicular to each other and to the direction of travel, oscillating in step.",
            ),
            q(
                "When an EM wave enters a medium of refractive index n, what happens?",
                (
                    opt("Frequency stays the same but wavelength shrinks", correct=True),
                    opt("Wavelength stays the same but frequency drops"),
                    opt("Both frequency and wavelength increase"),
                    opt("The wave speeds up to v = c times n"),
                ),
                "In a medium the wave slows to v = c/n; the frequency stays the same while the wavelength shrinks.",
            ),
        ),
        "Polarization & the electromagnetic spectrum": (
            q(
                "What distinguishes circular polarization from linear polarization?",
                (
                    opt("E oscillates along one fixed line"),
                    opt(
                        "E rotates at constant magnitude from two equal components 90 degrees out of phase",
                        correct=True,
                    ),
                    opt("E points along the direction of travel"),
                    opt("The frequency changes while the amplitude is fixed"),
                ),
                "Circular polarization is two equal linear components 90 degrees out of phase, so E rotates at constant magnitude; linear is a single fixed line.",
            ),
            q(
                "Malus's law gives the fraction of light transmitted through a polarizer as which expression?",
                (
                    opt("I = I0 sin^2(theta)"),
                    opt("I = I0 cos^2(theta)", correct=True),
                    opt("I = I0 cos(theta)"),
                    opt("I = I0 over cos^2(theta)"),
                ),
                "A polarizer passes I = I0 cos^2(theta), where theta is the angle between the polarizer axis and the incoming polarization.",
            ),
            q(
                "In the electromagnetic spectrum, which ordering goes from lower to higher frequency?",
                (
                    opt("Radio, microwave, infrared, visible, UV, X-ray, gamma", correct=True),
                    opt("Gamma, X-ray, UV, visible, infrared, microwave, radio"),
                    opt("Visible, radio, microwave, X-ray, gamma, infrared, UV"),
                    opt("Microwave, radio, visible, infrared, gamma, UV, X-ray"),
                ),
                "All EM waves are the same physics; frequency increases from radio through microwave, infrared, visible, UV, X-ray, to gamma.",
            ),
        ),
        "The Poynting vector & energy flow": (
            q(
                "What does the Poynting vector S = (1/mu0) E cross B describe?",
                (
                    opt("Power per unit area and the direction the energy flows", correct=True),
                    opt("The total charge enclosed by a surface"),
                    opt("The wavelength of the wave in a medium"),
                    opt("The reflection coefficient at a boundary"),
                ),
                "The Poynting vector gives power per unit area (W/m^2) and points in the direction the wave carries energy.",
            ),
            q(
                "How does the time-averaged intensity of a plane wave depend on the field amplitude E0?",
                (
                    opt("It is proportional to E0"),
                    opt("It is proportional to the square of E0", correct=True),
                    opt("It is independent of E0"),
                    opt("It is proportional to 1 over E0"),
                ),
                "The time-averaged intensity is (1/2) c eps0 E0^2 = E0^2 / (2 eta0), so intensity grows with the square of the field amplitude.",
            ),
            q(
                "Why does a point source's intensity fall off as 1 over r squared?",
                (
                    opt("Because the wave loses frequency as it travels"),
                    opt("Because the power spreads over a sphere of area 4 pi r^2", correct=True),
                    opt("Because the medium absorbs energy linearly with distance"),
                    opt("Because radiation pressure removes energy at each radius"),
                ),
                "A point source radiates equally in all directions, so the power P spreads over a sphere of area 4 pi r^2, giving S = P / (4 pi r^2).",
            ),
        ),
        "Reflection & refraction at boundaries": (
            q(
                "Snell's law n1 sin(theta1) = n2 sin(theta2) describes which behavior?",
                (
                    opt("How much power reflects at normal incidence"),
                    opt("How the transmitted ray bends because its speed changes", correct=True),
                    opt("The intensity drop over distance from a source"),
                    opt("The rotation of polarization at a surface"),
                ),
                "Snell's law relates the incidence and refraction angles; the transmitted wave bends because its speed changes between media.",
            ),
            q(
                "What is total internal reflection?",
                (
                    opt(
                        "Going from dense to rare medium beyond the critical angle, the wave reflects completely",
                        correct=True,
                    ),
                    opt("Going from rare to dense medium, the wave bends toward the normal"),
                    opt("At normal incidence, about 4% of the light reflects"),
                    opt("The polarization flips on reflection at any angle"),
                ),
                "Going from a denser to a rarer medium, beyond the critical angle arcsin(n2/n1) the wave cannot escape and reflects completely, as in optical fibers.",
            ),
            q(
                "At normal incidence, the reflectance is R = Gamma^2 with Gamma = (n1 - n2)/(n1 + n2). About how much reflects at a glass (n=1.5) surface in air?",
                (
                    opt("About 0%"),
                    opt("About 4% per surface", correct=True),
                    opt("About 25% per surface"),
                    opt("About 50% per surface"),
                ),
                "With n1=1 and n2=1.5, Gamma = -0.2 and R = 0.04, so glass reflects about 4% per surface, which is why lenses get anti-reflection coatings.",
            ),
        ),
        "Lab: a propagating & standing EM wave": (
            q(
                "In the lab, how is a standing wave formed from the travelling wave?",
                (
                    opt("By doubling the frequency of the forward wave"),
                    opt(
                        "By superposing a forward wave and an equal reflected wave going the other way",
                        correct=True,
                    ),
                    opt("By increasing the wavelength until it fills the domain"),
                    opt("By absorbing the wave at the right boundary"),
                ),
                "The lab adds forward cos(kz - wt) and reflected cos(kz + wt) to get the standing wave 2 cos(kz) cos(wt) with fixed nodes.",
            ),
            q(
                "For the lab's 1 GHz wave, what is the spacing between standing-wave nodes?",
                (
                    opt("One full wavelength"),
                    opt("Half a wavelength", correct=True),
                    opt("A quarter wavelength"),
                    opt("Two wavelengths"),
                ),
                "The code prints that standing-wave nodes are spaced half a wavelength apart.",
            ),
            q(
                "What does the dashed envelope plotted as 2 cos(kz) represent in the standing-wave plot?",
                (
                    opt(
                        "The maximum amplitude the standing wave reaches at each position",
                        correct=True,
                    ),
                    opt("The single forward travelling wave at t = 0"),
                    opt("The radiation pressure along the line"),
                    opt("The reflection coefficient versus position"),
                ),
                "The standing wave is 2 cos(kz) cos(wt); the dashed plus and minus 2 cos(kz) curves are the envelope bounding the oscillation at each position.",
            ),
        ),
    },
    final=(
        q(
            "Which addition by Maxwell makes electromagnetic waves self-sustaining without wires or charges?",
            (
                opt("The magnetic monopole term in Gauss's law for magnetism"),
                opt(
                    "The displacement current term mu0 eps0 dE/dt in the Ampere-Maxwell law",
                    correct=True,
                ),
                opt("The Poynting vector term in Faraday's law"),
                opt("The refractive index term in the wave equation"),
            ),
            "The displacement current lets a changing E make B and a changing B make E, a self-sustaining wave needing no wires or charges.",
        ),
        q(
            "The relations c = 1/sqrt(mu0 eps0) and c = lambda f together imply what about a fixed-frequency wave entering glass?",
            (
                opt("Its frequency rises and wavelength stays fixed"),
                opt("Its speed and wavelength both drop while frequency stays fixed", correct=True),
                opt("Its speed rises by the factor n"),
                opt("Its wavelength grows while speed stays at c"),
            ),
            "In a medium the speed drops to c/n and, since frequency is fixed, the wavelength shrinks by the same factor n.",
        ),
        q(
            "A plane wave with field amplitude E0 has time-averaged intensity proportional to E0^2; using eta0 about 377 ohm, what is eta0 called?",
            (
                opt("The reflection coefficient"),
                opt("The impedance of free space, the ratio E0/(B0 c)", correct=True),
                opt("The refractive index of vacuum"),
                opt("The critical angle for total internal reflection"),
            ),
            "eta0 = sqrt(mu0/eps0) is about 377 ohm, the impedance of free space, equal to the ratio E0/(B0 c), and intensity is E0^2/(2 eta0).",
        ),
        q(
            "At a boundary between two media, which pair of effects is governed by Snell's law and the Fresnel equations?",
            (
                opt(
                    "The bending of the transmitted ray and the reflected/transmitted fractions",
                    correct=True,
                ),
                opt("The polarization state and the radiation pressure"),
                opt("The displacement current and the wave speed in vacuum"),
                opt("The inverse-square spreading and the Poynting direction"),
            ),
            "Snell's law sets the refracted angle (bending) and the Fresnel equations give the reflected and transmitted fractions at the boundary.",
        ),
        q(
            "Superposing a forward wave cos(kz - wt) with an equal reflected wave cos(kz + wt) produces what?",
            (
                opt("A faster travelling wave at twice the speed"),
                opt(
                    "A standing wave 2 cos(kz) cos(wt) with fixed nodes a half wavelength apart",
                    correct=True,
                ),
                opt("A circularly polarized wave"),
                opt("A wave whose intensity falls as 1 over r^2"),
            ),
            "Forward plus equal reflected gives the standing wave 2 cos(kz) cos(wt), whose nodes stay put and are spaced half a wavelength apart.",
        ),
    ),
)
