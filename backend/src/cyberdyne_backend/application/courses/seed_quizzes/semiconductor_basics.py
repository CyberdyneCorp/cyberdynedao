from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Crystal structure & energy bands": (
            q(
                "In a semiconductor at absolute zero, what separates the valence band from the conduction band?",
                (
                    opt("An overlap of the two bands"),
                    opt("The forbidden bandgap Eg", correct=True),
                    opt("A region full of free electrons"),
                    opt("The Fermi-Dirac distribution"),
                ),
                "The valence and conduction bands are separated by the forbidden bandgap Eg; an electron must gain at least Eg to cross it.",
            ),
            q(
                "What roughly is the bandgap of silicon at room temperature?",
                (
                    opt("about 0 eV (bands overlap)"),
                    opt("about 1.1 eV", correct=True),
                    opt("about 1.42 eV"),
                    opt("about 9 eV"),
                ),
                "Silicon has a bandgap of roughly 1.12 eV; GaAs is about 1.42 eV and SiO2 (an insulator) is about 9 eV.",
            ),
            q(
                "When an electron is excited across the gap, what is left behind in the valence band?",
                (
                    opt("A hole that behaves like a mobile positive charge", correct=True),
                    opt("A second free electron"),
                    opt("An ionised donor atom"),
                    opt("Nothing, the bond stays full"),
                ),
                "Exciting an electron leaves an empty bond, a hole, which behaves like a mobile positive charge; both electrons and holes carry current.",
            ),
        ),
        "Intrinsic & extrinsic semiconductors": (
            q(
                "Doping silicon with phosphorus or arsenic (group V) produces what kind of material?",
                (
                    opt("p-type, with holes as majority carriers"),
                    opt("n-type, with electrons as majority carriers", correct=True),
                    opt("intrinsic material with ni unchanged"),
                    opt("an insulator"),
                ),
                "Group V donors add spare electrons, making n-type material whose majority carriers are electrons (n is about equal to Nd).",
            ),
            q(
                "What does the law of mass action state for a semiconductor in thermal equilibrium?",
                (
                    opt("n + p = ni"),
                    opt("n * p = ni^2", correct=True),
                    opt("n = p at all doping levels"),
                    opt("n * p depends only on the doping"),
                ),
                "In equilibrium n*p = ni^2, fixed by the material and temperature; doping one carrier up drives the other down.",
            ),
            q(
                "How does doping a sample n-type move the Fermi level EF?",
                (
                    opt("It rises toward the conduction band", correct=True),
                    opt("It falls toward the valence band"),
                    opt("It stays pinned at mid-gap"),
                    opt("It moves out of the bandgap entirely"),
                ),
                "For n-type material EF rises toward the conduction band; for p-type it falls toward the valence band.",
            ),
        ),
        "Carrier transport: drift, diffusion & mobility": (
            q(
                "Drift velocity relates to the applied electric field by which expression?",
                (
                    opt("vd = mu * E", correct=True),
                    opt("vd = D * dn/dx"),
                    opt("vd = q * n * mu"),
                    opt("vd = E / mu"),
                ),
                "Under an applied field carriers reach an average drift velocity vd = mu * E, where mu is the mobility.",
            ),
            q(
                "The Einstein relation ties the diffusion coefficient to the mobility as D/mu equals what?",
                (
                    opt("q / kT"),
                    opt("kT / q, the thermal voltage VT (about 0.0259 V at 300 K)", correct=True),
                    opt("the mobility squared"),
                    opt("the conductivity sigma"),
                ),
                "The Einstein relation gives D/mu = kT/q = VT, about 0.0259 V at 300 K.",
            ),
            q(
                "Which carriers are nimbler in silicon according to the lesson?",
                (
                    opt("Electrons (mu_n about 1350) over holes (mu_p about 480)", correct=True),
                    opt("Holes (mu_p about 1350) over electrons (mu_p about 480)"),
                    opt("Both have equal mobility"),
                    opt("Neither moves; only diffusion occurs"),
                ),
                "Electrons are nimbler than holes in silicon, with mu_n about 1350 versus mu_p about 480 cm^2/V.s.",
            ),
        ),
        "Generation, recombination & the continuity equation": (
            q(
                "After excess carriers are injected and left alone, how do they return to equilibrium?",
                (
                    opt("Linearly with time"),
                    opt("Exponentially, as exp(-t/tau) with lifetime tau", correct=True),
                    opt("Instantly"),
                    opt("They never decay"),
                ),
                "Excess carriers decay exponentially back to equilibrium with the minority-carrier lifetime tau: Dn(t) = Dn0 exp(-t/tau).",
            ),
            q(
                "The diffusion length L is related to the diffusion coefficient D and lifetime tau by which expression?",
                (
                    opt("L = D * tau"),
                    opt("L = sqrt(D * tau)", correct=True),
                    opt("L = D / tau"),
                    opt("L = tau / D"),
                ),
                "A carrier diffuses an average diffusion length L = sqrt(D*tau) before it recombines.",
            ),
            q(
                "In a fast switching diode, what lifetime tau is desired and why?",
                (
                    opt(
                        "Short tau, so stored charge clears quickly for reverse recovery",
                        correct=True,
                    ),
                    opt("Long tau, so carriers reach the junction before recombining"),
                    opt("Long tau, to maximise radiative emission"),
                    opt("tau is irrelevant to switching speed"),
                ),
                "Fast switching diodes want short tau so stored charge clears quickly (reverse recovery); long tau is wanted in solar cells.",
            ),
        ),
        "The PN junction at equilibrium": (
            q(
                "What is the depletion region of a PN junction at equilibrium?",
                (
                    opt(
                        "A region swept clean of mobile carriers, exposing ionised dopant charge",
                        correct=True,
                    ),
                    opt("A region crowded with both electrons and holes"),
                    opt("A metal contact between the two sides"),
                    opt("The region where the Fermi level is steepest"),
                ),
                "The depletion (space-charge) region is swept clean of mobile carriers, leaving exposed ionised donors and acceptors that set up the built-in field.",
            ),
            q(
                "At equilibrium, what condition defines the standoff across the junction?",
                (
                    opt(
                        "Drift exactly cancels diffusion, and the Fermi level is flat", correct=True
                    ),
                    opt("Diffusion stops completely and drift drives all current"),
                    opt("The bands are flat across the whole device"),
                    opt("The built-in potential is zero"),
                ),
                "Equilibrium is the standoff where drift exactly cancels diffusion and the Fermi level is flat across the device.",
            ),
            q(
                "What happens to the depletion width W when the junction is reverse-biased?",
                (
                    opt("It widens", correct=True),
                    opt("It shrinks"),
                    opt("It stays fixed"),
                    opt("It disappears entirely"),
                ),
                "Reverse bias adds to the built-in voltage and widens W; forward bias shrinks it. The voltage-dependent width acts like a capacitor.",
            ),
        ),
        "Lab: carrier concentration & Fermi-Dirac vs temperature": (
            q(
                "In the lab, how is the intrinsic carrier concentration ni computed as a function of temperature?",
                (
                    opt("ni = sqrt(Nc_T * Nv_T) * exp(-Eg/(2*kT))", correct=True),
                    opt("ni = Nc * Nv * exp(-Eg/kT)"),
                    opt("ni = Nd + Na"),
                    opt("ni = 1 / (1 + exp(E/kT))"),
                ),
                "The lab computes ni = sqrt(Nc_T * Nv_T) * exp(-Eg/(2*kT)), with the effective DOS scaling as T^1.5.",
            ),
            q(
                "What does the Fermi-Dirac occupation f(E) equal in the lab code?",
                (
                    opt("1 / (1 + exp(E/(kB*T)))", correct=True),
                    opt("exp(-E/(kB*T))"),
                    opt("sqrt(Nc*Nv)"),
                    opt("E / (kB*T)"),
                ),
                "The lab uses the Fermi-Dirac distribution f(E) = 1 / (1 + exp(E/(kB*Tx))), with E measured from the Fermi level.",
            ),
            q(
                "One try-it-yourself suggestion raises Eg to 3.26 (SiC). What does the lab note happens to ni?",
                (
                    opt("ni plummets, which is why wide-bandgap parts handle heat", correct=True),
                    opt("ni rises sharply with the larger gap"),
                    opt("ni is unchanged by the bandgap"),
                    opt("ni becomes negative"),
                ),
                "Raising Eg to 3.26 eV (SiC) makes ni plummet, which is why wide-bandgap parts handle heat better.",
            ),
        ),
    },
    final=(
        q(
            "Which material classification matches a bandgap of about 9 eV at room temperature?",
            (
                opt("Conductor (metal)"),
                opt("Semiconductor (Si)"),
                opt("Insulator such as SiO2", correct=True),
                opt("Intrinsic GaAs"),
            ),
            "A bandgap of about 9 eV, as in SiO2, means essentially no free carriers, making it an insulator.",
        ),
        q(
            "A silicon sample is doped n-type with Nd = 1e17 (ni = 1e10). What is the minority hole concentration?",
            (
                opt("about 1e17 cm^-3"),
                opt("about 1e3 cm^-3", correct=True),
                opt("about 1e10 cm^-3"),
                opt("about 1e20 cm^-3"),
            ),
            "By mass action p = ni^2/Nd = (1e10)^2 / 1e17 = 1e3 cm^-3, the minority hole concentration.",
        ),
        q(
            "Which pair correctly names the two carrier transport mechanisms?",
            (
                opt("Drift (driven by a field) and diffusion (down a gradient)", correct=True),
                opt("Generation and recombination"),
                opt("Accumulation and inversion"),
                opt("Avalanche and tunneling"),
            ),
            "Every device current is drift (carriers pushed by a field) and/or diffusion (carriers spreading down a concentration gradient).",
        ),
        q(
            "What does the built-in potential Vbi of a PN junction depend on?",
            (
                opt(
                    "The doping levels Na and Nd and ni, via Vbi = (kT/q) ln(Na*Nd/ni^2)",
                    correct=True,
                ),
                opt("Only the applied reverse bias"),
                opt("The mobility of electrons alone"),
                opt("The minority-carrier lifetime tau"),
            ),
            "Vbi = (kT/q) ln(Na*Nd/ni^2); for typical silicon doping it is about 0.6 to 0.8 V and grows only logarithmically with doping.",
        ),
        q(
            "Why is the minority-carrier lifetime tau important for a solar cell or photodiode?",
            (
                opt(
                    "A long tau and L let photogenerated carriers reach the junction before recombining",
                    correct=True,
                ),
                opt("A short tau maximises the collected photocurrent"),
                opt("tau sets the bandgap and therefore the colour"),
                opt("tau determines the dopant type"),
            ),
            "For photodiodes and solar cells you want long tau and diffusion length L so generated carriers reach the junction before recombining.",
        ),
    ),
)
