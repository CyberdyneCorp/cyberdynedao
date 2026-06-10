from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Isolated converters: flyback, forward & bridges": (
            q(
                "What does a transformer provide in an isolated converter?",
                (
                    opt("galvanic isolation and a voltage-scaling turns ratio n", correct=True),
                    opt("zero-voltage switching only"),
                    opt("a fixed duty cycle"),
                    opt("a feedback loop"),
                ),
                "The transformer galvanically isolates input from output and its turns ratio n is an extra voltage-scaling knob.",
            ),
            q(
                "How does a flyback converter handle energy?",
                (
                    opt(
                        "the transformer stores energy when on and releases it when off",
                        correct=True,
                    ),
                    opt("it transfers energy directly while the switch is on"),
                    opt("it never uses a magnetic component"),
                    opt("it uses four switches to drive the transformer both ways"),
                ),
                "A flyback stores energy in the transformer (coupled inductors) while on and releases it to the output when off; it is the star of low-power isolated supplies under about 100 W.",
            ),
            q(
                "By power level, which topology takes over above roughly 500 W to kW and beyond?",
                (
                    opt("half-bridge / full-bridge", correct=True),
                    opt("flyback"),
                    opt("a single diode"),
                    opt("a linear regulator"),
                ),
                "Half-bridge and full-bridge topologies use two or four switches to drive the transformer both ways and take over at higher power where a flyback's peak currents become impractical.",
            ),
        ),
        "Resonant converters & soft switching": (
            q(
                "What is the defining benefit of soft switching in resonant converters?",
                (
                    opt(
                        "a switch turns on at zero voltage (ZVS) or off at zero current (ZCS), giving near-zero transition loss",
                        correct=True,
                    ),
                    opt("the duty cycle is fixed at 50 percent"),
                    opt("the transformer is removed entirely"),
                    opt("conduction loss is eliminated"),
                ),
                "An LC tank shapes the waveforms so switching happens at zero voltage or zero current, nearly eliminating the transition (switching) loss.",
            ),
            q(
                "How is the LLC resonant converter primarily controlled?",
                (
                    opt("by varying the switching frequency around resonance", correct=True),
                    opt("by varying the duty cycle"),
                    opt("by varying the firing angle alpha"),
                    opt("by varying the turns ratio in real time"),
                ),
                "The LLC is controlled by frequency, not duty cycle: its gain peaks near the resonant frequency and the controller moves around it to regulate.",
            ),
            q(
                "Which soft-switching mode is favoured for MOSFETs and used by the LLC?",
                (
                    opt("ZVS, zero-voltage switching", correct=True),
                    opt("ZCS, zero-current switching"),
                    opt("hard switching"),
                    opt("phase-angle switching"),
                ),
                "ZVS turns the switch on when its voltage is already zero, avoiding dumping the output capacitance energy; LLC is a ZVS topology. ZCS is favoured for IGBTs and thyristors with slow turn-off tails.",
            ),
        ),
        "Inverters: DC to AC": (
            q(
                "What conversion does an inverter perform?",
                (
                    opt("DC to AC", correct=True),
                    opt("AC to DC"),
                    opt("DC to DC"),
                    opt("AC to AC"),
                ),
                "An inverter synthesizes AC from DC, the conversion behind solar systems, UPSs, EV traction, and motor drives.",
            ),
            q(
                "In sinusoidal PWM (SPWM), what two signals are compared to set the switching?",
                (
                    opt(
                        "a low-frequency sine reference and a high-frequency triangle carrier",
                        correct=True,
                    ),
                    opt("two triangle carriers"),
                    opt("a DC level and a square wave"),
                    opt("a sine reference and the firing angle"),
                ),
                "SPWM switches high when the sine reference is above the triangle carrier and low when below, so the filtered average traces a sine.",
            ),
            q(
                "What happens when the modulation index ma is pushed above 1 (overmodulation)?",
                (
                    opt(
                        "amplitude is gained at the cost of added low-order harmonics", correct=True
                    ),
                    opt("the output frequency doubles"),
                    opt("switching loss falls to zero"),
                    opt("the inverter becomes a rectifier"),
                ),
                "ma is sine amplitude over carrier amplitude; pushing ma above 1 gains output amplitude but adds low-order harmonics (distortion).",
            ),
        ),
        "Motor drives & variable-frequency drives": (
            q(
                "What conversion chain does a variable-frequency drive (VFD) use?",
                (
                    opt("AC to DC to AC", correct=True),
                    opt("DC to AC to DC"),
                    opt("AC to AC only"),
                    opt("DC to DC only"),
                ),
                "A VFD rectifies the mains to a DC bus, then inverts it to adjustable frequency and voltage: AC to DC to AC.",
            ),
            q(
                "How does V/f (scalar) control differ from field-oriented control (FOC)?",
                (
                    opt(
                        "V/f keeps voltage proportional to frequency (simple, open-loop); FOC decouples torque and flux currents for precise control",
                        correct=True,
                    ),
                    opt("V/f gives precise torque control; FOC is open-loop"),
                    opt("both are identical control methods"),
                    opt("V/f is used only for DC motors"),
                ),
                "V/f scales voltage with frequency to hold flux roughly constant (fine for pumps and fans); FOC mathematically decouples torque- and flux-producing currents for precise torque and dynamics, the standard for EVs and servos.",
            ),
            q(
                "What does regeneration allow in a motor drive?",
                (
                    opt(
                        "a motor being slowed feeds energy back, e.g. regenerative braking returning energy to the battery",
                        correct=True,
                    ),
                    opt("the motor spins only in one direction"),
                    opt("the DC bus is removed"),
                    opt("the inverter becomes unidirectional"),
                ),
                "Because the bridge is bidirectional, a decelerating motor can feed energy back; regenerative braking in EVs returns energy to the battery instead of burning it in friction brakes.",
            ),
        ),
        "Wide-bandgap devices, thermal & EMI": (
            q(
                "What is a key advantage of wide-bandgap devices (SiC and GaN) over silicon?",
                (
                    opt(
                        "lower losses, higher switching frequency, and higher temperature operation",
                        correct=True,
                    ),
                    opt("they cannot block high voltage"),
                    opt("they require larger magnetics"),
                    opt("they only work at very low frequency"),
                ),
                "Their wider bandgap blocks more voltage in less material and switches far faster, giving lower losses, higher frequency (smaller magnetics), and higher-temperature operation.",
            ),
            q(
                "Which equation gives the junction temperature from loss and thermal resistance?",
                (
                    opt("Tj = Tambient + Ploss times Rth", correct=True),
                    opt("Tj = Tambient minus Ploss times Rth"),
                    opt("Tj = Ploss divided by Rth"),
                    opt("Tj = Tambient times Ploss"),
                ),
                "Heat flows through a chain of thermal resistances like Ohm's law, so Tj = Tambient + Ploss times (Rth,jc + Rth,cs + Rth,sa).",
            ),
            q(
                "How do wide-bandgap devices affect EMI?",
                (
                    opt(
                        "their faster switching edges make EMI harder to manage, not easier",
                        correct=True,
                    ),
                    opt("they eliminate EMI entirely"),
                    opt("they have no effect on EMI"),
                    opt("they only reduce conducted EMI"),
                ),
                "Fast dv/dt and di/dt radiate and conduct interference; wide-bandgap's faster edges make EMI harder, requiring input filters, careful layout, and shielding.",
            ),
        ),
        "Lab: a sinusoidal-PWM inverter": (
            q(
                "In the SPWM lab, what does the modulation index ma represent?",
                (
                    opt("sine amplitude divided by carrier amplitude", correct=True),
                    opt("the carrier frequency divided by the output frequency"),
                    opt("the DC bus voltage"),
                    opt("the low-pass filter time constant"),
                ),
                "ma = sine amp / carrier amp; the lab sets ma = 0.8 and the filtered amplitude comes out near ma.",
            ),
            q(
                "In the lab, what happens when you raise the carrier frequency f_carrier to 8000?",
                (
                    opt("the filtered sine gets cleaner with fewer ripples", correct=True),
                    opt("the output frequency changes to 8000 Hz"),
                    opt("the modulation index doubles"),
                    opt("the sine reference disappears"),
                ),
                "A higher carrier frequency pushes the switching ripple further from the 50 Hz output, so the low-pass filter recovers a cleaner sine.",
            ),
            q(
                "In the lab, what does setting ma = 1.2 (overmodulation) do to the output?",
                (
                    opt("the peak flattens, adding distortion", correct=True),
                    opt("the output amplitude drops to zero"),
                    opt("the carrier frequency increases"),
                    opt("switching loss disappears"),
                ),
                "Overmodulation (ma above 1) flattens the peak and adds distortion, trading clean waveform shape for amplitude.",
            ),
        ),
        "Applications & the throughline": (
            q(
                "Which device technology powers a modern EV traction inverter?",
                (
                    opt("SiC (silicon carbide)", correct=True),
                    opt("mercury-arc valves"),
                    opt("linear regulators"),
                    opt("thyristors only"),
                ),
                "SiC dominates high-voltage/high-power applications such as EV traction inverters, solar, and grid.",
            ),
            q(
                "What is the throughline shared by every converter in the track?",
                (
                    opt(
                        "switch fully on/off, store and filter energy, control duty or frequency with feedback, and manage heat and EMI",
                        correct=True,
                    ),
                    opt("drop excess voltage across a resistor as heat"),
                    opt("avoid using any feedback control"),
                    opt("use only linear regulators"),
                ),
                "Every converter switches a device fully on and off, stores and filters energy with L, C, and transformers, controls the duty cycle or frequency via feedback, and manages the resulting heat and EMI.",
            ),
            q(
                "Why are VFDs called the biggest single energy-saving technology in industry?",
                (
                    opt(
                        "fan/pump power scales with the cube of speed, so a small speed reduction saves a lot",
                        correct=True,
                    ),
                    opt("they convert DC directly to DC"),
                    opt("they eliminate the need for any motor"),
                    opt("they run motors only at full speed"),
                ),
                "Fan and pump power scales with the cube of speed, so a modest speed reduction via a VFD saves a large amount of energy.",
            ),
        ),
    },
    final=(
        q(
            "Which isolated topology stores energy in its transformer when the switch is on and releases it when off?",
            (
                opt("flyback", correct=True),
                opt("forward"),
                opt("full-bridge"),
                opt("push-pull"),
            ),
            "The flyback stores energy in the transformer (coupled inductors) while on and releases it when off; the forward transfers energy directly while on.",
        ),
        q(
            "An LLC resonant converter regulates its output by varying what?",
            (
                opt("the switching frequency around resonance", correct=True),
                opt("the duty cycle"),
                opt("the turns ratio"),
                opt("the ambient temperature"),
            ),
            "The LLC is controlled by frequency: its gain peaks near resonance and the controller moves around it. ZVS soft switching lets it run at high frequency and high efficiency at once.",
        ),
        q(
            "In sinusoidal PWM, comparing a sine reference to a triangle carrier and pushing ma above 1 causes what?",
            (
                opt(
                    "overmodulation, gaining amplitude at the cost of low-order harmonics",
                    correct=True,
                ),
                opt("a perfect harmonic-free sine"),
                opt("a switch to ZCS operation"),
                opt("the carrier frequency to double"),
            ),
            "ma is sine amplitude over carrier amplitude; overmodulation (ma above 1) adds amplitude but introduces low-order harmonics.",
        ),
        q(
            "A variable-frequency drive uses an AC-DC-AC chain. Which control method decouples torque and flux currents for precise control?",
            (
                opt("field-oriented control (FOC / vector control)", correct=True),
                opt("V/f scalar control"),
                opt("phase-angle firing control"),
                opt("open-loop duty control"),
            ),
            "FOC uses the Park/Clarke transforms to decouple torque- and flux-producing currents, giving precise torque and dynamics; V/f is the simpler open-loop scalar method.",
        ),
        q(
            "With Ploss = 25 W, Rth = 1.5 C/W, and Tamb = 40 C, what is the junction temperature Tj?",
            (
                opt("77.5 C", correct=True),
                opt("40 C"),
                opt("25 C"),
                opt("16.7 C"),
            ),
            "Tj = Tamb + Ploss times Rth = 40 + 25 times 1.5 = 77.5 C. Thermal management like this often limits how much power a converter can deliver.",
        ),
    ),
)
