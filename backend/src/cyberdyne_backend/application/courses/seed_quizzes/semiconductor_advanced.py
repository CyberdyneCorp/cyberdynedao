from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Short-channel effects & scaling": (
            q(
                "What is the room-temperature thermodynamic floor on subthreshold swing for a classical MOSFET?",
                (
                    opt("6 mV/decade"),
                    opt("60 mV/decade", correct=True),
                    opt("600 mV/decade"),
                    opt("0 mV/decade"),
                ),
                "The 60 mV/decade floor at room temperature is a thermodynamic limit for a classical MOSFET, a key reason supply voltage stopped scaling.",
            ),
            q(
                "What does DIBL (drain-induced barrier lowering) do in a short channel?",
                (
                    opt("Raises Vth as Vds rises, increasing gate control"),
                    opt(
                        "Lowers Vth as Vds rises because the drain field lowers the source barrier",
                        correct=True,
                    ),
                    opt("Eliminates subthreshold leakage entirely"),
                    opt("Forces Id to grow quadratically with overdrive"),
                ),
                "In a short channel the drain field reaches across and lowers the source barrier, so Vth drops as Vds rises and the gate loses some control.",
            ),
            q(
                "Under velocity saturation, how does drain current Id grow with overdrive once carriers hit their velocity ceiling?",
                (
                    opt("Quadratically"),
                    opt("Exponentially"),
                    opt("Linearly", correct=True),
                    opt("It stops growing entirely"),
                ),
                "When carriers hit their roughly 10^7 cm/s ceiling, Id grows only linearly with overdrive rather than quadratically.",
            ),
        ),
        "Power & wide-bandgap devices": (
            q(
                "What architecture is the IGBT (insulated-gate bipolar transistor)?",
                (
                    opt("A MOSFET gate driving a BJT output", correct=True),
                    opt("Two MOSFETs in series"),
                    opt("A BJT gate driving a MOSFET output"),
                    opt("A pure unipolar silicon power MOSFET"),
                ),
                "The IGBT combines a MOSFET gate (easy voltage drive) with a bipolar output (low conduction drop at high current), making it the workhorse from about 600 V to several kV.",
            ),
            q(
                "Why do wide-bandgap materials like SiC and GaN collapse the on-resistance for a given rated voltage?",
                (
                    opt(
                        "Their bigger bandgap gives a higher critical breakdown field, so the drift region can be thinner and more heavily doped",
                        correct=True,
                    ),
                    opt(
                        "They have a lower critical breakdown field, requiring a thicker drift region"
                    ),
                    opt("They eliminate the drift region completely"),
                    opt("They have a much higher intrinsic carrier concentration"),
                ),
                "A bigger bandgap means a higher critical field Ecrit (about 10x silicon), letting the drift region be thinner and more heavily doped for the same voltage.",
            ),
            q(
                "Which wide-bandgap material is highlighted for tiny, cool phone fast chargers and 5G RF power amplifiers?",
                (
                    opt("Silicon"),
                    opt("GaN (gallium nitride)", correct=True),
                    opt("SiC (silicon carbide)"),
                    opt("Germanium"),
                ),
                "GaN is very fast and high-frequency, used in compact fast chargers, data-center power, and RF power amplifiers in 5G base stations and radar.",
            ),
        ),
        "IC fabrication & the CMOS process flow": (
            q(
                "Which unit step is the pattern-defining step that sets the process node?",
                (
                    opt("Oxidation"),
                    opt("Photolithography", correct=True),
                    opt("Chemical-mechanical polish (CMP)"),
                    opt("Ion implantation"),
                ),
                "Lithography is the pattern-defining step; the smallest feature is limited by the exposure wavelength and optics, which is why the industry moved to EUV at 13.5 nm.",
            ),
            q(
                "In ion implantation, what does the implant energy set, and what does the dose set?",
                (
                    opt("Energy sets depth; dose sets concentration", correct=True),
                    opt("Energy sets concentration; dose sets depth"),
                    opt("Both set only the oxide thickness"),
                    opt("Energy sets the anneal time; dose sets the mask pattern"),
                ),
                "Dopants are accelerated into the wafer where energy sets the depth (projected range Rp) and dose sets the concentration, followed by an anneal to repair damage and activate.",
            ),
            q(
                "According to the Deal-Grove description, how does thermal oxide thickness grow with time for a thick film?",
                (
                    opt("Linearly forever"),
                    opt(
                        "Roughly as the square root of time as it becomes diffusion-limited",
                        correct=True,
                    ),
                    opt("Exponentially with time"),
                    opt("It stops growing after the first second"),
                ),
                "Oxide grows fast at first (reaction-limited) then slows because oxygen must diffuse across the existing oxide, following a square-root-like law in time.",
            ),
        ),
        "Device modeling & SPICE models": (
            q(
                "What does BSIM stand for and what is its role?",
                (
                    opt(
                        "Berkeley Short-channel IGFET Model, the industry-standard compact model",
                        correct=True,
                    ),
                    opt("Basic Silicon Implant Model, used only for teaching"),
                    opt("Bipolar Surface Inversion Model, for BJTs only"),
                    opt("Berkeley Standard Interconnect Model, for wiring delay"),
                ),
                "BSIM (Berkeley Short-channel IGFET Model) is the industry standard; a foundry ships a PDK with hundreds of BSIM parameters per device fit to measured silicon.",
            ),
            q(
                "How is Vth commonly extracted in the simple example given?",
                (
                    opt(
                        "As the gate-voltage intercept of the linear-region Id vs Vgs extrapolation",
                        correct=True,
                    ),
                    opt("As the peak of the subthreshold current"),
                    opt("By measuring the oxide thickness directly"),
                    opt("As the drain voltage where breakdown occurs"),
                ),
                "Vth is the gate-voltage intercept of the linear-region Id vs Vgs extrapolation; extraction fits model parameters to measured I-V and C-V curves.",
            ),
            q(
                "What do process corners such as FF, SS, FS, SF, and TT represent?",
                (
                    opt("Different photoresist colors"),
                    opt(
                        "Fast/slow combinations of N and P transistors across the manufacturing spread",
                        correct=True,
                    ),
                    opt("Five fixed temperatures for burn-in"),
                    opt("The number of metal layers in the back end"),
                ),
                "The foundry characterises fast/slow N and P transistors (FF, SS, FS, SF, TT) so designers can verify the circuit across the full manufacturing spread, not just the typical case.",
            ),
        ),
        "Reliability physics: hot carriers, electromigration, TDDB & ESD": (
            q(
                "What does electromigration (EM) do to a metal wire, and which equation describes it?",
                (
                    opt(
                        "High current density pushes metal atoms along, opening voids, set by Black's equation",
                        correct=True,
                    ),
                    opt("Heat grows the oxide thicker, set by Deal-Grove"),
                    opt("Gate bias shifts Vth, set by the Arrhenius law alone"),
                    opt("A sudden surge melts junctions, set by ESD clamps"),
                ),
                "Electromigration is high current density literally pushing metal atoms along, opening voids and growing hillocks until the wire fails, governed by Black's equation.",
            ),
            q(
                "How does lifetime (MTTF) generally depend on temperature for these wear-out mechanisms?",
                (
                    opt("It rises exponentially with temperature"),
                    opt(
                        "It falls exponentially as temperature rises, via an Arrhenius law",
                        correct=True,
                    ),
                    opt("It is independent of temperature"),
                    opt("It grows linearly with temperature"),
                ),
                "Most mechanisms accelerate with temperature via an Arrhenius law, so lifetime falls exponentially as temperature rises; a few tens of degrees can halve it.",
            ),
            q(
                "Which mechanism is the sudden killer that dumps amps into a pin in nanoseconds from a few kilovolts?",
                (
                    opt("Electrostatic discharge (ESD)", correct=True),
                    opt("Negative-bias temperature instability (NBTI)"),
                    opt("Hot-carrier injection (HCI)"),
                    opt("Electromigration (EM)"),
                ),
                "ESD is the sudden failure: a few kilovolts from a human touch dump amps into a pin in nanoseconds, blowing oxides and melting junctions, so chips include on-die clamps and diodes.",
            ),
        ),
        "Lab: MOSFET scaling & subthreshold leakage": (
            q(
                "In the lab, what central tension of scaling does lowering Vth illustrate?",
                (
                    opt(
                        "It speeds a gate up but raises off-state leakage exponentially",
                        correct=True,
                    ),
                    opt("It slows a gate down and lowers leakage"),
                    opt("It has no effect on either speed or leakage"),
                    opt("It only changes the oxide thickness"),
                ),
                "The lab simulates that lowering Vth speeds a gate up but raises off-state leakage exponentially, the central tension of scaling.",
            ),
            q(
                "In the subthreshold model used, what sets the slope of log10(Id) versus Vgs below threshold?",
                (
                    opt("The supply voltage Vdd"),
                    opt("The subthreshold swing S in mV/decade", correct=True),
                    opt("The drift-region thickness"),
                    opt("The number of metal layers"),
                ),
                "The lab computes log_id = log10(Ion) + (Vgs - Vth)/(S/1000), so the swing S in mV/decade sets the slope of the exponential subthreshold current.",
            ),
            q(
                "How is the relative gate delay estimated across nodes in the lab?",
                (
                    opt("As kappa squared"),
                    opt("As 1/kappa, since delay improves roughly as 1/kappa", correct=True),
                    opt("As constant regardless of kappa"),
                    opt("As exp(kappa)"),
                ),
                "The lab uses rel_delay = 1.0/kappa because gate delay tau ~ C*Vdd/Ion improves roughly as 1/kappa as capacitance falls with scaling.",
            ),
        ),
        "Applications & the throughline": (
            q(
                "According to the lesson, almost every device in the track is built from which core structures?",
                (
                    opt("The PN junction and the MOS structure", correct=True),
                    opt("Only the BJT base region"),
                    opt("Only the gate oxide"),
                    opt("Only the drift region"),
                ),
                "Almost everything in the track is the PN junction and the MOS structure used in different ways, from diodes and BJTs to MOSFETs and optoelectronics.",
            ),
            q(
                "Which device in the table is built from a reverse junction plus light?",
                (
                    opt("Diode / rectifier"),
                    opt("Photodiode / solar cell / image sensor", correct=True),
                    opt("MOSFET / CMOS"),
                    opt("Memory cell (DRAM/Flash)"),
                ),
                "Photodiodes, solar cells, and image sensors are built from a reverse junction plus light, powering cameras, comms, and photovoltaics.",
            ),
            q(
                "What is the throughline the lesson emphasizes stays constant as materials and dimensions change?",
                (
                    opt("The physics of bands, carriers, junctions, and fields", correct=True),
                    opt("The exact transistor count of every chip"),
                    opt("The specific lithography wavelength"),
                    opt("The brand of the foundry"),
                ),
                "The materials and dimensions change every few years, but the physics (bands, carriers, junctions, and fields) does not; master it once and every new device is a variation on the theme.",
            ),
        ),
    },
    final=(
        q(
            "Which thermodynamic limit explains why MOSFET supply voltage stopped scaling and power density plateaued?",
            (
                opt("The 60 mV/decade subthreshold swing floor at room temperature", correct=True),
                opt("The Deal-Grove oxide growth limit"),
                opt("Black's equation current-density limit"),
                opt("The 193 nm lithography wavelength"),
            ),
            "The 60 mV/decade floor at room temperature is a thermodynamic limit for a classical MOSFET and the reason for the power wall.",
        ),
        q(
            "Why do SiC and GaN power devices outperform silicon for high-voltage switching?",
            (
                opt(
                    "Their wider bandgap gives a higher critical field, allowing a thinner, more heavily doped drift region and lower Ron",
                    correct=True,
                ),
                opt("They have a smaller bandgap and higher intrinsic carrier concentration"),
                opt("They remove the need for any gate"),
                opt("They operate only at very low temperatures"),
            ),
            "A wider bandgap raises the critical breakdown field about 10x, collapsing on-resistance and letting devices run hotter with less leakage.",
        ),
        q(
            "Match the fabrication step to its purpose: which step dopes the wafer selectively?",
            (
                opt("Oxidation"),
                opt("Ion implantation followed by anneal", correct=True),
                opt("Chemical-mechanical polish"),
                opt("Photoresist develop"),
            ),
            "Ion implantation fires dopant ions where energy sets depth and dose sets concentration, then an anneal activates them and repairs lattice damage.",
        ),
        q(
            "In device modeling, what is the role of a SPICE compact model like BSIM?",
            (
                opt(
                    "It packages device physics into equations plus extracted parameters that SPICE evaluates millions of times",
                    correct=True,
                ),
                opt("It physically grows the gate oxide on the wafer"),
                opt("It only measures ESD failures"),
                opt("It replaces the need for any foundry PDK"),
            ),
            "A compact model packages the physics into equations plus extracted parameters; BSIM is the industry standard shipped in a foundry PDK fit to measured silicon.",
        ),
        q(
            "Which reliability mechanism is the instantaneous failure rather than a slow wear-out over years?",
            (
                opt("Electrostatic discharge (ESD)", correct=True),
                opt("Hot-carrier injection (HCI)"),
                opt("Bias-temperature instability (NBTI/PBTI)"),
                opt("Electromigration (EM)"),
            ),
            "ESD is the sudden killer, dumping amps into a pin in nanoseconds, while HCI, NBTI, and EM are slow wear-out mechanisms accelerated by field, temperature, and current.",
        ),
    ),
)
