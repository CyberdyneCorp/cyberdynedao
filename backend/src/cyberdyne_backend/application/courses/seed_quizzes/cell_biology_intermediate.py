"""Quiz questions for the Cell Biology - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Enzyme kinetics: Michaelis-Menten": (
            q(
                "What does Km represent in the Michaelis-Menten equation?",
                (
                    opt("The substrate concentration at half-maximal velocity", correct=True),
                    opt("The maximum reaction velocity"),
                    opt("The total enzyme concentration"),
                    opt("The product concentration at equilibrium"),
                ),
                "Km is the [S] at which v = Vmax/2; it reflects apparent substrate affinity.",
            ),
            q(
                "How does a competitive inhibitor affect the kinetic parameters?",
                (
                    opt("It raises apparent Km while leaving Vmax unchanged", correct=True),
                    opt("It lowers Vmax while leaving Km unchanged"),
                    opt("It lowers both Km and Vmax"),
                    opt("It has no effect on either parameter"),
                ),
                "Competitive inhibitors compete for the active site, raising apparent Km; Vmax is reached with excess S.",
            ),
            q(
                "The specificity constant kcat/Km is bounded by what physical limit?",
                (
                    opt("The diffusion-controlled rate of substrate encounter", correct=True),
                    opt("The speed of light"),
                    opt("The melting temperature of DNA"),
                    opt("The membrane potential"),
                ),
                "The best enzymes approach the diffusion limit (~10^8-10^9 M^-1 s^-1).",
            ),
        ),
        "Membrane transport: diffusion, Nernst and GHK": (
            q(
                "Why does carrier-mediated facilitated diffusion saturate?",
                (
                    opt("The number of carrier proteins is finite", correct=True),
                    opt("The solute runs out instantly"),
                    opt("ATP is consumed faster than made"),
                    opt("The membrane dissolves at high concentration"),
                ),
                "Finite carriers give a hyperbolic, saturating flux just like enzyme kinetics.",
            ),
            q(
                "The Nernst equation gives what for a single ion?",
                (
                    opt(
                        "The equilibrium potential at which electrical and chemical forces balance",
                        correct=True,
                    ),
                    opt("The maximum transport velocity"),
                    opt("The enzyme turnover number"),
                    opt("The osmotic pressure"),
                ),
                "E_ion = (RT/zF) ln([out]/[in]) is the potential that balances the concentration gradient.",
            ),
            q(
                "What is the stoichiometry of the Na/K-ATPase per ATP hydrolyzed?",
                (
                    opt("3 Na+ out, 2 K+ in", correct=True),
                    opt("2 Na+ out, 3 K+ in"),
                    opt("1 Na+ out, 1 K+ in"),
                    opt("3 K+ out, 2 Na+ in"),
                ),
                "It exports 3 Na+ and imports 2 K+ per ATP, an electrogenic pump.",
            ),
        ),
        "The cytoskeleton and molecular motors": (
            q(
                "Which cytoskeletal filament shows dynamic instability driven by GTP hydrolysis?",
                (
                    opt("Microtubules", correct=True),
                    opt("Intermediate filaments"),
                    opt("Microfilaments (actin)"),
                    opt("Collagen fibers"),
                ),
                "Microtubules switch stochastically between growth and catastrophe via GTP-tubulin hydrolysis.",
            ),
            q(
                "Toward which microtubule end does kinesin typically walk?",
                (
                    opt("The plus end", correct=True),
                    opt("The minus end"),
                    opt("Both ends equally"),
                    opt("It does not move along microtubules"),
                ),
                "Most kinesins are plus-end-directed; dynein moves toward the minus end.",
            ),
            q(
                "Why does motor stepping velocity saturate at high ATP?",
                (
                    opt("The ATPase cycle becomes rate-limiting", correct=True),
                    opt("The microtubule disassembles"),
                    opt("ATP becomes toxic"),
                    opt("The motor detaches permanently"),
                ),
                "Once ATP is saturating, the mechanochemical cycle limits speed, giving hyperbolic kinetics.",
            ),
        ),
        "Signal transduction and dose-response": (
            q(
                "What second messenger do many GPCRs raise via adenylyl cyclase?",
                (
                    opt("cAMP", correct=True),
                    opt("DNA"),
                    opt("Glucose"),
                    opt("Oxygen"),
                ),
                "Gs-coupled GPCRs activate adenylyl cyclase to make cAMP, which activates PKA.",
            ),
            q(
                "What does the EC50 of a dose-response curve indicate?",
                (
                    opt("The dose producing half-maximal response", correct=True),
                    opt("The lethal dose"),
                    opt("The maximum possible response"),
                    opt("The number of receptors"),
                ),
                "EC50 is the half-maximal effective concentration, a potency measure.",
            ),
            q(
                "Why is signal amplification important in transduction cascades?",
                (
                    opt(
                        "One active receptor can generate many downstream messenger molecules",
                        correct=True,
                    ),
                    opt("It slows the response to a single molecule"),
                    opt("It prevents any response from forming"),
                    opt("It destroys the ligand before binding"),
                ),
                "Each step multiplies the signal, so a few ligands produce a large intracellular effect.",
            ),
        ),
        "Bioenergetics and the proton-motive force": (
            q(
                "A reaction is spontaneous when which quantity is negative?",
                (
                    opt("The Gibbs free-energy change, delta G", correct=True),
                    opt("The temperature"),
                    opt("The enzyme concentration"),
                    opt("The molecular weight"),
                ),
                "Negative delta G means the reaction releases free energy and proceeds spontaneously.",
            ),
            q(
                "The proton-motive force combines which two components?",
                (
                    opt("The membrane potential and the pH gradient", correct=True),
                    opt("Temperature and pressure"),
                    opt("ATP and ADP concentrations only"),
                    opt("Light intensity and wavelength"),
                ),
                "delta-p = delta-psi minus a term in delta-pH, combining electrical and chemical gradients.",
            ),
            q(
                "Why is ATP hydrolysis used to drive unfavorable reactions?",
                (
                    opt("It is exergonic and can be coupled to endergonic reactions", correct=True),
                    opt("It is endergonic and absorbs energy"),
                    opt("It has zero free-energy change"),
                    opt("It only occurs in the nucleus"),
                ),
                "Coupling the highly exergonic ATP hydrolysis to an endergonic step makes the sum favorable.",
            ),
        ),
        "Protein trafficking and quality control": (
            q(
                "What does the signal recognition particle (SRP) do?",
                (
                    opt(
                        "Recognizes the signal peptide and targets the ribosome to the ER translocon",
                        correct=True,
                    ),
                    opt("Degrades all newly made proteins"),
                    opt("Replicates DNA"),
                    opt("Pumps protons into the lysosome"),
                ),
                "SRP binds the nascent signal sequence and docks the ribosome on Sec61 at the ER.",
            ),
            q(
                "Which tag directs enzymes to the lysosome?",
                (
                    opt("Mannose-6-phosphate", correct=True),
                    opt("A poly-A tail"),
                    opt("A 5' cap"),
                    opt("Ubiquitin alone"),
                ),
                "The M6P tag is recognized by receptors that route hydrolases to lysosomes.",
            ),
            q(
                "What does the unfolded protein response (UPR) sense?",
                (
                    opt("Accumulation of misfolded proteins in the ER", correct=True),
                    opt("High glucose in the cytosol"),
                    opt("DNA double-strand breaks"),
                    opt("Excess oxygen in mitochondria"),
                ),
                "ER stress from misfolded proteins triggers the UPR, and persistent stress leads to ERAD.",
            ),
        ),
    },
    final=(
        q(
            "At [S] much greater than Km, the reaction rate is approximately what?",
            (
                opt("Constant near Vmax (zero-order in substrate)", correct=True),
                opt("First-order in substrate"),
                opt("Zero"),
                opt("Negative"),
            ),
            "Far above Km the enzyme is saturated and v approaches Vmax independent of [S].",
        ),
        q(
            "Secondary active transport is powered by what?",
            (
                opt("An ion gradient (such as Na+) maintained by a primary pump", correct=True),
                opt("Direct ATP hydrolysis at the transporter"),
                opt("Light absorption"),
                opt("Simple diffusion of water"),
            ),
            "Symporters/antiporters use the energy stored in an ion gradient set up by ATP-driven pumps.",
        ),
        q(
            "Which motor protein walks along actin filaments?",
            (
                opt("Myosin", correct=True),
                opt("Kinesin"),
                opt("Dynein"),
                opt("Lamin"),
            ),
            "Myosin is the actin-based motor; kinesin and dynein use microtubules.",
        ),
        q(
            "A Hill coefficient greater than 1 indicates what?",
            (
                opt("Positive cooperativity (steeper, switch-like response)", correct=True),
                opt("No binding at all"),
                opt("Negative free energy"),
                opt("Loss of all receptors"),
            ),
            "n > 1 makes the dose-response curve steeper, reflecting cooperative binding.",
        ),
        q(
            "The membrane potential contribution to the proton-motive force is denoted by what?",
            (
                opt("delta-psi", correct=True),
                opt("Km"),
                opt("Vmax"),
                opt("EC50"),
            ),
            "delta-psi is the electrical (membrane-potential) term in the proton-motive force.",
        ),
        q(
            "Misfolded ER proteins that cannot be rescued are removed by which system?",
            (
                opt("ER-associated degradation via the ubiquitin-proteasome pathway", correct=True),
                opt("Mitochondrial fission"),
                opt("DNA replication"),
                opt("Exocytosis to the cell surface"),
            ),
            "ERAD retro-translocates terminally misfolded proteins for ubiquitin-proteasome degradation.",
        ),
    ),
)
