"""Curated quiz questions for the Circuit Analysis - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Ohm's law, power & sign conventions": (
            q(
                "Ohm's law for a resistor relates voltage, current and resistance as:",
                (
                    opt("$v = R/i$"),
                    opt("$v = R\\,i$", correct=True),
                    opt("$i = R\\,v$"),
                    opt("$R = v\\,i$"),
                ),
                "Ohm's law is $v = R\\,i$, equivalently $i = v/R$ and $R = v/i$.",
            ),
            q(
                "Which expression is NOT a valid form for the power dissipated in a resistor?",
                (
                    opt("$p = v\\,i$"),
                    opt("$p = i^2 R$"),
                    opt("$p = v^2 / R$"),
                    opt("$p = i / v$", correct=True),
                ),
                "Resistor power is $p = vi = i^2R = v^2/R$; $i/v$ is not a power expression.",
            ),
            q(
                "Using the passive sign convention (current into the + terminal), $p = vi > 0$ means:",
                (
                    opt("the element absorbs power", correct=True),
                    opt("the element delivers power to the circuit"),
                    opt("the element stores energy losslessly"),
                    opt("the reference arrows were drawn incorrectly"),
                ),
                "With current entering the + terminal, positive power means the element absorbs power.",
            ),
        ),
        "Kirchhoff's laws (KVL & KCL)": (
            q(
                "Kirchhoff's Current Law (KCL) states that:",
                (
                    opt("the sum of voltages around any loop is zero"),
                    opt("the algebraic sum of currents entering a node is zero", correct=True),
                    opt("current is the same in every branch of a circuit"),
                    opt("the product of voltage and current is conserved"),
                ),
                "KCL: the algebraic sum of currents into any node is zero (charge does not accumulate).",
            ),
            q(
                "Kirchhoff's Voltage Law (KVL) is a statement of:",
                (
                    opt("conservation of charge"),
                    opt("conservation of energy around a closed loop", correct=True),
                    opt("Ohm's law applied to a single element"),
                    opt("the maximum power transfer theorem"),
                ),
                "KVL — the sum of voltages around any closed loop is zero — follows from energy conservation.",
            ),
            q(
                "For a source $V_s$ driving $R_1$ and $R_2$ in a single series loop, KVL gives the loop current:",
                (
                    opt("$i = V_s (R_1 + R_2)$"),
                    opt("$i = V_s / (R_1 + R_2)$", correct=True),
                    opt("$i = V_s / (R_1 R_2)$"),
                    opt("$i = V_s (R_1 - R_2)$"),
                ),
                "KVL: $V_s = i(R_1+R_2)$, so $i = V_s/(R_1+R_2)$.",
            ),
        ),
        "Series, parallel & dividers": (
            q(
                "Two resistors in parallel combine as:",
                (
                    opt("$R_1 + R_2$"),
                    opt("$R_1 R_2 / (R_1 + R_2)$", correct=True),
                    opt("$(R_1 + R_2)/2$"),
                    opt("$\\sqrt{R_1 R_2}$"),
                ),
                "Parallel resistance is $R_1 R_2/(R_1+R_2)$, always smaller than the smallest branch.",
            ),
            q(
                "In a series voltage divider, the voltage across $R_2$ is:",
                (
                    opt("$V_s\\,R_1/(R_1+R_2)$"),
                    opt("$V_s\\,R_2/(R_1+R_2)$", correct=True),
                    opt("$V_s\\,(R_1+R_2)/R_2$"),
                    opt("$V_s\\,R_2/R_1$"),
                ),
                "The divider output across $R_2$ is $v_2 = V_s\\,R_2/(R_1+R_2)$.",
            ),
            q(
                "In a current divider, current splits between parallel branches:",
                (
                    opt("in proportion to each branch resistance"),
                    opt(
                        "inversely to each branch resistance, so more current takes the smaller-R branch",
                        correct=True,
                    ),
                    opt("equally regardless of resistance"),
                    opt("entirely through the larger resistor"),
                ),
                "Current divides inversely to resistance — the easier (smaller-R) branch carries more current.",
            ),
        ),
        "Nodal analysis": (
            q(
                "Nodal analysis solves a circuit by finding:",
                (
                    opt("the node voltages, by applying KCL at each node", correct=True),
                    opt("the mesh currents, by applying KVL around each loop"),
                    opt("the Thevenin resistance of every branch"),
                    opt("the power dissipated in each element"),
                ),
                "Nodal analysis writes KCL at each node and solves for the node voltages.",
            ),
            q(
                "The first step of nodal analysis is to:",
                (
                    opt("short all the sources"),
                    opt(
                        "choose a reference (ground) node and set its voltage to zero", correct=True
                    ),
                    opt("combine every resistor in series"),
                    opt("assign a clockwise current to each loop"),
                ),
                "You pick a reference node (0 V) and label the other node voltages relative to it.",
            ),
            q(
                "In the conductance-matrix form $\\mathbf{G}\\mathbf{v}=\\mathbf{i}$, a diagonal entry of $\\mathbf{G}$ is:",
                (
                    opt("minus the conductance shared with another node"),
                    opt("the sum of all conductances connected to that node", correct=True),
                    opt("the source current at that node"),
                    opt("always equal to one"),
                ),
                "Diagonal = sum of conductances at the node; off-diagonal = minus the shared conductance.",
            ),
        ),
        "Mesh analysis": (
            q(
                "Mesh analysis solves for:",
                (
                    opt("node voltages via KCL"),
                    opt("mesh (loop) currents via KVL", correct=True),
                    opt("the open-circuit voltage at the terminals"),
                    opt("branch conductances"),
                ),
                "Mesh analysis assigns a circulating current to each mesh and writes KVL around it.",
            ),
            q(
                "A resistor shared between two adjacent meshes carries a current equal to:",
                (
                    opt("the sum of the two mesh currents"),
                    opt("the difference of the two mesh currents", correct=True),
                    opt("either mesh current alone"),
                    opt("zero, since the meshes cancel"),
                ),
                "A shared resistor carries the difference of the two (same-direction) mesh currents.",
            ),
            q(
                "When choosing between nodal and mesh analysis, you generally pick the one that:",
                (
                    opt("uses the larger resistors"),
                    opt("yields fewer equations for that circuit", correct=True),
                    opt("avoids using Ohm's law"),
                    opt("ignores the sources"),
                ),
                "Both are exact; pick whichever produces fewer simultaneous equations.",
            ),
        ),
        "Thevenin & Norton equivalents": (
            q(
                "A Thevenin equivalent of a linear two-terminal network is:",
                (
                    opt("a current source in parallel with a resistance"),
                    opt(
                        "a voltage source $V_{th}$ in series with a resistance $R_{th}$",
                        correct=True,
                    ),
                    opt("a single resistor only"),
                    opt("two voltage sources in series"),
                ),
                "Thevenin: a voltage source $V_{th}$ in series with $R_{th}$ (Norton is its parallel dual).",
            ),
            q(
                "To find $R_{th}$ you look into the terminals after:",
                (
                    opt("shorting the load"),
                    opt(
                        "zeroing the independent sources (short voltage sources, open current sources)",
                        correct=True,
                    ),
                    opt("removing all resistors"),
                    opt("doubling every source value"),
                ),
                "$R_{th}$ is the resistance seen with independent sources zeroed: V-sources shorted, I-sources opened.",
            ),
            q(
                "Maximum power is delivered to a load $R_L$ connected to a Thevenin source when:",
                (
                    opt("$R_L = 0$"),
                    opt("$R_L \\to \\infty$"),
                    opt("$R_L = R_{th}$", correct=True),
                    opt("$R_L = 2R_{th}$"),
                ),
                "Maximum power transfer occurs at the matched load $R_L = R_{th}$.",
            ),
        ),
    },
    final=(
        q(
            "Which set of three relationships are all valid forms of Ohm's law and resistor power?",
            (
                opt("$v=Ri$, $p=vi$, $p=i^2R$", correct=True),
                opt("$v=R/i$, $p=v/i$, $p=iR^2$"),
                opt("$i=Rv$, $p=R/v$, $p=v^2 R$"),
                opt("$R=vi$, $p=i/v$, $p=v/R^2$"),
            ),
            "Ohm: $v=Ri$. Resistor power: $p=vi=i^2R=v^2/R$.",
        ),
        q(
            "Which pairing of Kirchhoff's laws with the conserved quantity is correct?",
            (
                opt("KCL conserves energy; KVL conserves charge"),
                opt(
                    "KCL conserves charge (currents at a node); KVL conserves energy (voltages in a loop)",
                    correct=True,
                ),
                opt("Both KCL and KVL conserve power"),
                opt("KCL and KVL are restatements of Ohm's law only"),
            ),
            "KCL (charge) sums currents at a node to zero; KVL (energy) sums voltages around a loop to zero.",
        ),
        q(
            "Three equal resistors $R$ are placed in parallel. The total resistance is:",
            (
                opt("$3R$"),
                opt("$R/3$", correct=True),
                opt("$R$"),
                opt("$R/9$"),
            ),
            "$n$ equal resistors in parallel give $R/n$, so three give $R/3$.",
        ),
        q(
            "Nodal and mesh analysis are best described as:",
            (
                opt("two different physical laws that sometimes disagree"),
                opt(
                    "systematic applications of KCL (nodal) and KVL (mesh) respectively",
                    correct=True,
                ),
                opt("methods that work only for AC circuits"),
                opt("approximations that ignore the sources"),
            ),
            "Nodal is organised KCL (node voltages); mesh is organised KVL (loop currents).",
        ),
        q(
            "A Norton equivalent consists of:",
            (
                opt(
                    "a current source $I_N$ in parallel with $R_{th}$, where $I_N = V_{th}/R_{th}$",
                    correct=True,
                ),
                opt("a voltage source in series with $R_{th}$"),
                opt("two resistors in series"),
                opt("an ideal current source with no resistance"),
            ),
            "Norton = current source $I_N=V_{th}/R_{th}$ in parallel with the same $R_{th}$ as Thevenin.",
        ),
        q(
            "For a series voltage divider with $R_1 = R_2$, the output across $R_2$ is:",
            (
                opt("the full source voltage"),
                opt("half the source voltage", correct=True),
                opt("zero"),
                opt("twice the source voltage"),
            ),
            "With $R_1=R_2$, $v_2 = V_s R_2/(R_1+R_2) = V_s/2$.",
        ),
    ),
)
