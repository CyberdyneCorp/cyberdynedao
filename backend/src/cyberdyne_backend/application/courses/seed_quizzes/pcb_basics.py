from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Components, symbols & schematics": (
            q(
                "In EDA terms, what is a net?",
                (
                    opt("the drawn shape of a part on the schematic"),
                    opt("a set of pins that are electrically the same node", correct=True),
                    opt("the part label such as R1 or U2"),
                    opt("the physical copper pads a part solders to"),
                ),
                "A net is exactly a node from circuit analysis: every pin on the same net is the same voltage.",
            ),
            q(
                "Which reference designator prefix is used for an integrated circuit?",
                (
                    opt("R"),
                    opt("C"),
                    opt("U", correct=True),
                    opt("J"),
                ),
                "The convention uses U for an integrated circuit; R is resistor, C is capacitor, J is connector.",
            ),
            q(
                "For the SENSE divider with Vin = 3.3 V, R1 = 10k and R2 = 20k, what is Vsense from Vin times R2/(R1+R2)?",
                (
                    opt("1.1 V"),
                    opt("2.2 V", correct=True),
                    opt("3.3 V"),
                    opt("0.66 V"),
                ),
                "Vsense = 3.3 times 20k/(10k+20k) = 3.3 times 2/3 = 2.2 V, the worked value in the lesson.",
            ),
        ),
        "From schematic to PCB: footprints, layers & the EDA flow": (
            q(
                "What is the difference between a symbol and a footprint?",
                (
                    opt(
                        "the symbol is the electrical shape with pin functions, the footprint is the physical copper pads",
                        correct=True,
                    ),
                    opt("the symbol is the copper pads, the footprint is the schematic drawing"),
                    opt("they are two names for the same schematic shape"),
                    opt("the symbol is the netlist and the footprint is the BOM"),
                ),
                "A symbol lives on the schematic and shows pin functions; the footprint is the physical pads, drill holes and silkscreen.",
            ),
            q(
                "What does the netlist provide as the handoff from schematic to layout?",
                (
                    opt("the temperature profile for the reflow oven"),
                    opt(
                        "an exported list of every net and which footprint pads sit on it",
                        correct=True,
                    ),
                    opt("the relative permittivity of the FR4 substrate"),
                    opt("the minimum trace width the fab can manufacture"),
                ),
                "The netlist exports every net and the footprint pads on it; the layout shows unrouted ones as the ratsnest.",
            ),
            q(
                "Copper weight is specified in ounces per square foot. About how thick is 1 oz copper?",
                (
                    opt("about 3.5 microns"),
                    opt("about 35 microns", correct=True),
                    opt("about 350 microns"),
                    opt("about 1 micron"),
                ),
                "The lesson states 1 oz copper is about 35 microns thick; thicker copper carries more current for the same width.",
            ),
        ),
        "PCB stackup & materials": (
            q(
                "What is the default PCB substrate material described in the lesson?",
                (
                    opt("Rogers PTFE laminate"),
                    opt("FR4 woven glass-epoxy laminate", correct=True),
                    opt("solid copper foil"),
                    opt("ceramic"),
                ),
                "FR4 is the default woven glass-epoxy substrate: cheap, sturdy and good to a few GHz.",
            ),
            q(
                "In the classic 4-layer workhorse stackup, what sits on the two inner layers?",
                (
                    opt("signals on both inner layers"),
                    opt("a solid GND plane and a PWR plane", correct=True),
                    opt("soldermask and silkscreen"),
                    opt("blind and buried vias only"),
                ),
                "The classic 4-layer stack puts signals on the outside and a solid GND plus PWR plane pair in the middle.",
            ),
            q(
                "Which type of via connects an inner layer to another inner layer only?",
                (
                    opt("through-hole via"),
                    opt("blind via"),
                    opt("buried via", correct=True),
                    opt("thermal via"),
                ),
                "A buried via connects inner to inner; a blind via goes outer to inner and a through-hole via goes all the way.",
            ),
        ),
        "Placement & routing basics": (
            q(
                "Why is placement called 80% of the battle?",
                (
                    opt("good placement makes routing almost draw itself", correct=True),
                    opt("placement determines the relative permittivity of the board"),
                    opt("placement sets the reflow oven temperature profile"),
                    opt("placement replaces the need for a design rule check"),
                ),
                "The lesson states placement is 80% of the battle because good placement makes routing almost draw itself.",
            ),
            q(
                "What does the DRC (Design Rule Check) do?",
                (
                    opt("exports the gerber and drill files"),
                    opt("flags every violation of the encoded design rules", correct=True),
                    opt("places parts grouped by function"),
                    opt("computes the trace impedance"),
                ),
                "The DRC flags every clearance, trace/space, annular ring or drill violation; a clean DRC is the gate before manufacturing files.",
            ),
            q(
                "Why should you avoid 90-degree corners in routing?",
                (
                    opt("they violate the BOM contract with the factory"),
                    opt("they make the netlist export fail"),
                    opt(
                        "45-degree or curved corners etch cleaner with less reflection at high speed",
                        correct=True,
                    ),
                    opt("they increase the relative permittivity of the trace"),
                ),
                "The lesson recommends 45-degree or curved corners for cleaner etch and less reflection at high speed.",
            ),
        ),
        "Manufacturing & assembly: gerbers, fab & soldering": (
            q(
                "What do Gerber files (RS-274X) describe?",
                (
                    opt("one file per layer, describing shapes as 2D apertures", correct=True),
                    opt("the X, Y and rotation of each part for the assembly robot"),
                    opt("hole positions and sizes only"),
                    opt("the chip junction temperature limits"),
                ),
                "Gerbers give one file per layer (copper, soldermask, silkscreen) describing shapes as 2D apertures; the universal fab language.",
            ),
            q(
                "In SMT reflow assembly, how is solder applied before parts are placed?",
                (
                    opt("leads are pushed through drilled holes and wave soldered"),
                    opt("a stencil deposits solder paste on the pads", correct=True),
                    opt("the board is dipped in a reflow oven of molten solder"),
                    opt("each joint is hand soldered with a ferrite"),
                ),
                "SMT reflow uses a stencil to deposit solder paste on the pads, then a robot places parts and a reflow oven melts the paste.",
            ),
            q(
                "Which assembly method is described as very mechanically strong and used for connectors and power?",
                (
                    opt("through-hole (THT)", correct=True),
                    opt("surface-mount (SMT)"),
                    opt("solder paste reflow"),
                    opt("panelization"),
                ),
                "Through-hole mounts leads through drilled holes, is very mechanically strong, and is used for connectors, power and prototyping.",
            ),
        ),
        "Lab: trace width vs current (IPC-2221)": (
            q(
                "In the IPC-2221 rule I = k times dT^0.44 times A^0.725, what does dT represent?",
                (
                    opt("the dielectric thickness in mils"),
                    opt("the allowed temperature rise in C", correct=True),
                    opt("the copper weight in ounces"),
                    opt("the trace length in mm"),
                ),
                "dT is the allowed temperature rise in C; A is the cross-sectional area and k is the layer constant.",
            ),
            q(
                "Which value of k does the lab use for an external (outer-layer) trace?",
                (
                    opt("0.024"),
                    opt("0.048", correct=True),
                    opt("0.725"),
                    opt("1.378"),
                ),
                "k = 0.048 for external (outer-layer) copper; internal (buried) traces use k = 0.024 and must be much wider.",
            ),
            q(
                "If you set oz = 2.0 instead of 1.0, what happens to the trace width needed for the same current?",
                (
                    opt("the same current needs a narrower trace", correct=True),
                    opt("the same current needs a wider trace"),
                    opt("the width is unchanged"),
                    opt("the trace can no longer carry that current"),
                ),
                "Thicker copper has more cross-sectional area per width, so the same current needs a narrower trace, as the try-it-yourself note states.",
            ),
        ),
    },
    final=(
        q(
            "Which statement correctly distinguishes a symbol from a footprint?",
            (
                opt(
                    "a symbol is the schematic electrical shape, a footprint is the physical copper pads",
                    correct=True,
                ),
                opt("a symbol is the physical pads, a footprint is the schematic drawing"),
                opt("both are exported parts of the netlist"),
                opt("a symbol is the BOM entry, a footprint is the reference designator"),
            ),
            "The symbol carries pin functions on the schematic; the footprint is the real copper pads, drills and silkscreen the part solders to.",
        ),
        q(
            "What is the dielectric height h, trace width w and FR4 permittivity used to compute in the microstrip formula?",
            (
                opt("the trace characteristic impedance Z0", correct=True),
                opt("the reflow oven peak temperature"),
                opt("the BOM cost of the board"),
                opt("the minimum annular ring"),
            ),
            "The Wheeler/IPC microstrip approximation uses w, h and er to give Z0; impedance falls as the trace gets wider relative to the dielectric.",
        ),
        q(
            "Which is the correct order of the EDA flow from capture to manufacturing files?",
            (
                opt("schematic, netlist, layout, route, DRC, gerbers", correct=True),
                opt("gerbers, DRC, route, layout, netlist, schematic"),
                opt("layout, schematic, gerbers, route, netlist, DRC"),
                opt("netlist, gerbers, schematic, DRC, route, layout"),
            ),
            "The flow captures a schematic, exports the netlist, places footprints in layout, routes copper, runs DRC, then exports gerbers, drill and BOM.",
        ),
        q(
            "In the IPC-2221 lab, computing the minimum trace width for 3 A at a 20 C rise on 1 oz outer copper requires which two steps?",
            (
                opt(
                    "invert the IPC-2221 equation for area, then divide area by the thickness in mils",
                    correct=True,
                ),
                opt("multiply current by the dielectric height, then subtract the etch tolerance"),
                opt("read Z0 from the microstrip formula, then look up the BOM"),
                opt("count the thermal vias, then divide by the copper weight"),
            ),
            "The lab inverts I = k dT^0.44 A^0.725 for area in mil^2, then width = area divided by the copper thickness in mils.",
        ),
        q(
            "Why does the lesson recommend designing with margin rather than at the absolute fab minimums?",
            (
                opt("margin yields better, assembles faster and reworks easier", correct=True),
                opt("margin lowers the relative permittivity of FR4"),
                opt("margin removes the need for a netlist"),
                opt("margin increases the reflow peak temperature"),
            ),
            "The cheapest reliability win is margin: backing off the fab minimums yields better, assembles faster and reworks easier.",
        ),
    ),
)
