from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Delay & timing: RC model, logical effort & setup/hold": (
            q(
                "In the RC delay model, the propagation delay is approximately t_pd = 0.69 R C. What happens to delay if the load capacitance C increases?",
                (
                    opt("Delay decreases linearly"),
                    opt("Delay increases linearly", correct=True),
                    opt("Delay stays constant"),
                    opt("Delay increases quadratically"),
                ),
                "Since t_pd = 0.69 R C, delay grows linearly with the load capacitance C.",
            ),
            q(
                "In the logical-effort stage delay d = g h + p, what does g represent?",
                (
                    opt("The parasitic delay of the gate"),
                    opt("The electrical effort or fanout"),
                    opt(
                        "The logical effort, how much harder a gate is to drive than an inverter",
                        correct=True,
                    ),
                    opt("The supply voltage"),
                ),
                "g is the logical effort: INV=1, NAND2=4/3, NOR2=5/3. h is electrical effort and p is parasitic delay.",
            ),
            q(
                "A hold-time violation is caused by a path that is too fast. How is it best fixed?",
                (
                    opt("Slow the clock down"),
                    opt("Add delay to the short path", correct=True),
                    opt("Raise the clock period"),
                    opt("Speed up the logic"),
                ),
                "Hold violations come from short paths and do not go away by slowing the clock; you add delay to the fast path.",
            ),
        ),
        "Power in CMOS: dynamic, short-circuit & leakage": (
            q(
                "Dynamic power follows P_dyn = alpha C VDD^2 f. If the supply voltage VDD is halved, what happens to dynamic power?",
                (
                    opt("It is halved"),
                    opt("It is quartered", correct=True),
                    opt("It is unchanged"),
                    opt("It doubles"),
                ),
                "Because of the VDD^2 dependence, halving the voltage quarters the dynamic power, the single most important low-power lever.",
            ),
            q(
                "Which power component dominates when a chip is idle?",
                (
                    opt("Dynamic switching power"),
                    opt("Short-circuit power"),
                    opt("Leakage (static) power", correct=True),
                    opt("Clock power"),
                ),
                "Subthreshold leakage rises exponentially as Vth drops and dominates when a chip is idle.",
            ),
            q(
                "What is the purpose of power gating?",
                (
                    opt("To increase clock frequency"),
                    opt(
                        "To insert a sleep transistor that disconnects an idle block from the supply, cutting leakage",
                        correct=True,
                    ),
                    opt("To reduce short-circuit current during transitions"),
                    opt("To balance the clock tree"),
                ),
                "Power gating inserts a big sleep transistor that disconnects an unused block from the supply, cutting its leakage to nearly zero.",
            ),
        ),
        "Interconnect & wire delay": (
            q(
                "An unbuffered wire of length L has R proportional to L and C proportional to L. How does its intrinsic delay scale with length?",
                (
                    opt("Linearly with L"),
                    opt("Quadratically with L", correct=True),
                    opt("Logarithmically with L"),
                    opt("Independent of L"),
                ),
                "Since R and C each grow with L, t_wire is proportional to R C, which scales as L squared.",
            ),
            q(
                "What is the effect of inserting buffers (repeaters) along a long wire?",
                (
                    opt("It makes the delay quadratic in length"),
                    opt(
                        "It makes the delay roughly linear in length instead of quadratic",
                        correct=True,
                    ),
                    opt("It removes all delay"),
                    opt("It increases capacitance per length"),
                ),
                "Repeaters chop the wire into shorter segments, making the overall delay roughly linear in L instead of quadratic.",
            ),
            q(
                "Why do advanced chips use many metal layers?",
                (
                    opt("To reduce the number of transistors"),
                    opt(
                        "Thick low-resistance layers up top handle global routing and the power grid, thin dense layers below handle local connections",
                        correct=True,
                    ),
                    opt("To eliminate the need for repeaters"),
                    opt("To make gates faster"),
                ),
                "Chips use many metal layers: thick low-resistance layers on top for global routing and power grid, thin dense layers below for local connections.",
            ),
        ),
        "Arithmetic & datapath in VLSI": (
            q(
                "How does the delay of a ripple-carry adder scale with word width n?",
                (
                    opt("Logarithmically"),
                    opt("Linearly with n", correct=True),
                    opt("Quadratically with n"),
                    opt("Constant regardless of n"),
                ),
                "A ripple-carry adder chains full adders and the carry ripples from bit 0 to bit n-1, so delay grows linearly with width.",
            ),
            q(
                "What advantage does a carry-lookahead adder have over a ripple-carry adder?",
                (
                    opt("It uses less area"),
                    opt(
                        "It computes carries in parallel, cutting delay to roughly logarithmic in n",
                        correct=True,
                    ),
                    opt("It removes the need for full adders"),
                    opt("It consumes no power"),
                ),
                "A carry-lookahead adder computes carries in parallel, reducing delay to roughly logarithmic in n at the cost of more area.",
            ),
            q(
                "Which multiplier structure reduces partial products in O(log n) using carry-save adders?",
                (
                    opt("An array multiplier"),
                    opt("A ripple-carry multiplier"),
                    opt("A Wallace/Dadda tree", correct=True),
                    opt("A carry-select multiplier"),
                ),
                "A Wallace/Dadda tree reduces partial products in O(log n) using carry-save adders, then a final fast adder.",
            ),
        ),
        "Memory design: SRAM, DRAM, ROM & sense amplifiers": (
            q(
                "How many transistors does a standard 6T SRAM cell use, and how does it store a bit?",
                (
                    opt("One transistor and a capacitor"),
                    opt(
                        "Six transistors: cross-coupled inverters plus two access transistors",
                        correct=True,
                    ),
                    opt("Four transistors forming a single inverter"),
                    opt("Six transistors all forming a sense amplifier"),
                ),
                "A 6T SRAM cell stores a bit in cross-coupled inverters (a latch) plus two access transistors, six transistors total.",
            ),
            q(
                "Why must DRAM be refreshed every few milliseconds?",
                (
                    opt("Because it uses six transistors per bit"),
                    opt("Because the charge on its tiny capacitor leaks away", correct=True),
                    opt("Because its contents are baked into the layout"),
                    opt("Because reads are nondestructive"),
                ),
                "DRAM stores a bit as charge on a tiny capacitor (1T1C); the charge leaks, so it must be refreshed periodically, and reads are destructive.",
            ),
            q(
                "What does a sense amplifier do during a memory read?",
                (
                    opt("It refreshes the stored charge"),
                    opt(
                        "It is a fast differential comparator that amplifies the small bit-line delta-V into a full logic level",
                        correct=True,
                    ),
                    opt("It bakes contents into the layout"),
                    opt("It increases the bit-line capacitance"),
                ),
                "Bit lines develop only a tiny delta-V on a read; the sense amplifier is a fast differential comparator that amplifies it to a full logic level quickly.",
            ),
        ),
        "Lab: delay & power vs supply voltage": (
            q(
                "In the lab, what metric is minimized to find the supply-voltage sweet spot?",
                (
                    opt("Gate delay alone"),
                    opt("Energy per operation (power times delay)", correct=True),
                    opt("Leakage current alone"),
                    opt("Activity factor"),
                ),
                "The lab computes energy_per_op = p_total * delay and finds the VDD that minimizes it with np.argmin.",
            ),
            q(
                "In the lab model, what happens to gate delay as VDD drops toward Vth?",
                (
                    opt("Delay falls toward zero"),
                    opt("Delay rises sharply", correct=True),
                    opt("Delay stays constant"),
                    opt("Delay becomes negative"),
                ),
                "Delay is C*VDD/drive where drive ~ (VDD - Vth)^2, so as VDD approaches Vth the delay rises sharply.",
            ),
            q(
                "According to the lab notes, raising Ileak0 to 0.5 (a leaky process) has what effect on the energy minimum?",
                (
                    opt("It moves the energy minimum to a lower VDD"),
                    opt("It moves the energy minimum higher", correct=True),
                    opt("It eliminates the energy minimum"),
                    opt("It has no effect on the energy minimum"),
                ),
                "The lab notes state that with a leaky process (higher Ileak0) the energy minimum moves higher.",
            ),
        ),
    },
    final=(
        q(
            "Which design technique helps a setup-time violation but does NOT fix a hold-time violation?",
            (
                opt("Adding delay to the short path"),
                opt("Raising the clock period", correct=True),
                opt("Inserting a sense amplifier"),
                opt("Power gating"),
            ),
            "Raising the clock period gives slow paths more time (fixes setup), but hold violations come from fast paths and are unaffected by a slower clock.",
        ),
        q(
            "Which expression captures the dominant lever in dynamic power?",
            (
                opt("The linear dependence on frequency f"),
                opt("The VDD^2 dependence in alpha C VDD^2 f", correct=True),
                opt("The activity factor alpha only"),
                opt("The load capacitance C only"),
            ),
            "The VDD^2 term means halving the voltage quarters dynamic power, the single most important low-power lever.",
        ),
        q(
            "Both unbuffered interconnect delay and ripple-carry adder delay grow with size, but they differ. Which statement is correct?",
            (
                opt(
                    "Wire delay is linear in length while ripple-carry delay is quadratic in width"
                ),
                opt(
                    "Wire delay is quadratic in length while ripple-carry delay is linear in width",
                    correct=True,
                ),
                opt("Both are logarithmic"),
                opt("Both are constant"),
            ),
            "Unbuffered wire delay scales as L squared, while a ripple-carry adder's delay grows linearly with word width n.",
        ),
        q(
            "Which memory technology is densest because it uses one transistor and one capacitor per bit?",
            (
                opt("6T SRAM"),
                opt("ROM"),
                opt("DRAM (1T1C)", correct=True),
                opt("Flash sense amplifier"),
            ),
            "DRAM stores a bit as charge on a capacitor with one transistor (1T1C), making it far denser than 6T SRAM, which is why main memory is DRAM.",
        ),
        q(
            "In the energy-delay tradeoff explored in the lab, why is there a sweet-spot supply voltage rather than just lowering VDD as far as possible?",
            (
                opt("Because leakage current disappears at low VDD"),
                opt(
                    "Because lowering VDD cuts dynamic power but makes gates slower, so energy per operation eventually rises",
                    correct=True,
                ),
                opt("Because the activity factor grows at low VDD"),
                opt("Because short-circuit power dominates at low VDD"),
            ),
            "Lowering VDD reduces dynamic power (~VDD^2) but increases delay; the product power times delay (energy per op) has a minimum, the sweet spot.",
        ),
    ),
)
