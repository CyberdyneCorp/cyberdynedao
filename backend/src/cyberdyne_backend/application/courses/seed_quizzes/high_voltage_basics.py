"""Curated quiz questions for the High-Voltage Engineering - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why high voltage: transmission efficiency": (
            q(
                "For a fixed delivered power, how does line loss change if the transmission voltage is increased ten times?",
                (
                    opt("It drops to one tenth"),
                    opt("It drops to one hundredth", correct=True),
                    opt("It stays the same"),
                    opt("It increases one hundred times"),
                ),
                "Loss is proportional to 1/V², so a ten-times higher voltage cuts the loss by one hundred.",
            ),
            q(
                "Which expression gives the power lost as heat in a transmission line?",
                (
                    opt("V times I"),
                    opt("I squared times R", correct=True),
                    opt("V squared times R"),
                    opt("R divided by I squared"),
                ),
                "Line loss is I²R, the resistive heating in the conductors.",
            ),
            q(
                "What is the main cost paid for raising the transmission voltage?",
                (
                    opt("Higher conductor resistance"),
                    opt("More insulation, because the electric field is stronger", correct=True),
                    opt("Lower delivered power"),
                    opt("Greater line current"),
                ),
                "Higher voltage means stronger fields, so more insulation (material or distance) is needed.",
            ),
        ),
        "Electric fields, stress & insulation": (
            q(
                "What actually causes a dielectric to break down?",
                (
                    opt("The applied voltage alone, regardless of geometry"),
                    opt(
                        "The electric field strength (dielectric stress) exceeding the breakdown strength",
                        correct=True,
                    ),
                    opt("The current flowing through it"),
                    opt("The temperature of the surrounding air"),
                ),
                "Insulation fails when the field strength (V/m) exceeds the material's breakdown strength, not from voltage alone.",
            ),
            q(
                "For a uniform field between parallel plates a distance d apart at voltage V, the field is:",
                (
                    opt("V times d"),
                    opt("V divided by d", correct=True),
                    opt("d divided by V"),
                    opt("V squared divided by d"),
                ),
                "In a uniform gap the field is E = V/d.",
            ),
            q(
                "Why does a sharp point or thin wire weaken an insulation design?",
                (
                    opt("It lowers the breakdown strength of the whole material"),
                    opt(
                        "It concentrates the field, raising the peak stress at the surface",
                        correct=True,
                    ),
                    opt("It increases the average field uniformly"),
                    opt("It reduces the voltage across the gap"),
                ),
                "Curvature concentrates the field (E ∝ 1/x near the surface), so the peak stress is highest at the conductor.",
            ),
        ),
        "Breakdown in gases & Paschen's law": (
            q(
                "Paschen's law states that the breakdown voltage of a gas gap depends on:",
                (
                    opt("the gap distance d alone"),
                    opt("the gas pressure p alone"),
                    opt("the product of pressure and distance, p·d", correct=True),
                    opt("the applied current"),
                ),
                "Paschen's law makes breakdown voltage a function of the product p·d.",
            ),
            q(
                "What is the self-sustaining multiplication of electrons that triggers gas breakdown called?",
                (
                    opt("An electron avalanche", correct=True),
                    opt("Dielectric absorption"),
                    opt("A water tree"),
                    opt("Thermal runaway"),
                ),
                "A free electron knocks out more electrons in collisions, forming a self-sustaining avalanche.",
            ),
            q(
                "Why does breakdown voltage rise again at very small p·d (left of the Paschen minimum)?",
                (
                    opt("The gas becomes a perfect conductor"),
                    opt(
                        "Electrons rarely collide with molecules, so an avalanche cannot start",
                        correct=True,
                    ),
                    opt("Pressure becomes infinite"),
                    opt("The field reverses direction"),
                ),
                "At small p·d there are too few collisions to build an avalanche, so a higher voltage is needed.",
            ),
        ),
        "Breakdown in liquid & solid dielectrics": (
            q(
                "How does breakdown in solid dielectrics differ from breakdown in gases?",
                (
                    opt("Solids recover instantly, gases do not"),
                    opt(
                        "Solid breakdown causes permanent damage, while gases recover", correct=True
                    ),
                    opt("Solids never break down"),
                    opt("Gas breakdown is always permanent"),
                ),
                "Gases recover after a flashover, but breakdown in solids is permanent damage.",
            ),
            q(
                "What most commonly causes real transformer oil to break down well below its pure strength?",
                (
                    opt("Excess hydrostatic pressure"),
                    opt(
                        "Impurities, moisture and suspended particles bridging the gap",
                        correct=True,
                    ),
                    opt("Too low a temperature"),
                    opt("The colour of the oil"),
                ),
                "Moisture, particles and bubbles align with the field and bridge the gap, lowering oil strength.",
            ),
            q(
                "What is electrical 'treeing' in a solid dielectric?",
                (
                    opt("A repair technique for damaged insulation"),
                    opt(
                        "Partial discharges in voids slowly carving conducting paths until failure",
                        correct=True,
                    ),
                    opt("The cooling of the dielectric under load"),
                    opt("A method of grading the field"),
                ),
                "Treeing is the slow growth of conducting 'trees' from partial discharges in voids, an ageing failure mechanism.",
            ),
        ),
        "High voltage in the power grid": (
            q(
                "Which voltage range is described as EHV (extra-high voltage)?",
                (
                    opt("230 V to 400 V"),
                    opt("11 kV to 33 kV"),
                    opt("345 kV to 765 kV", correct=True),
                    opt("under 1 kV"),
                ),
                "EHV covers roughly 345, 400, 500 and 765 kV for bulk transmission.",
            ),
            q(
                "Why do EHV lines above about 345 kV use bundled conductors?",
                (
                    opt("To carry direct current"),
                    opt("To lower the conductor surface field and reduce corona", correct=True),
                    opt("To increase the line resistance"),
                    opt("To make the towers shorter"),
                ),
                "Bundling lowers the surface field, reducing corona noise, interference and loss.",
            ),
            q(
                "What sets each grid voltage level?",
                (
                    opt("Only the colour code of the cables"),
                    opt(
                        "A trade-off between line losses and the cost of insulation, towers and right-of-way",
                        correct=True,
                    ),
                    opt("The frequency of the supply"),
                    opt("The number of customers"),
                ),
                "Each level balances lower losses against the higher cost of insulation and corridors.",
            ),
        ),
        "Safety, clearances & creepage": (
            q(
                "What is the difference between clearance and creepage?",
                (
                    opt("Clearance is along a surface; creepage is through air"),
                    opt(
                        "Clearance is the shortest distance through air; creepage is along an insulator surface",
                        correct=True,
                    ),
                    opt("They are two names for the same distance"),
                    opt("Clearance applies only to DC, creepage only to AC"),
                ),
                "Clearance is the shortest path through air; creepage is the shortest path along a solid surface.",
            ),
            q(
                "Why must creepage distance generally be longer than clearance?",
                (
                    opt(
                        "Surfaces collect pollution and moisture that let current track along them",
                        correct=True,
                    ),
                    opt("Air is a better insulator than vacuum"),
                    opt("Surfaces are always at a higher voltage"),
                    opt("Clearance does not matter outdoors"),
                ),
                "Pollution, salt and moisture on a surface allow tracking, so creepage must exceed clearance, especially in dirty environments.",
            ),
            q(
                "What is the correct safe sequence before working on a de-energised HV line?",
                (
                    opt("Touch it first to check it is dead"),
                    opt("Isolate, lock-out, test for dead, then apply earths", correct=True),
                    opt("Apply earths only after starting work"),
                    opt("Energise it briefly to confirm the source"),
                ),
                "The rule is isolate, lock-out/tag-out, test for dead, then earth before touching, because stored charge and induction remain dangerous.",
            ),
        ),
    },
    final=(
        q(
            "Why is bulk electric power transmitted at high voltage?",
            (
                opt("Because high voltage is safer to touch"),
                opt(
                    "Because line loss is proportional to 1/V², so higher voltage drastically cuts I²R loss",
                    correct=True,
                ),
                opt("Because it lowers the conductor resistance"),
                opt("Because transformers only work at high voltage"),
            ),
            "For fixed power, current is P/V and loss is I²R ∝ 1/V², so raising voltage sharply reduces losses.",
        ),
        q(
            "What determines whether a dielectric breaks down?",
            (
                opt("The applied voltage alone"),
                opt(
                    "The peak electric field strength exceeding the material's breakdown strength",
                    correct=True,
                ),
                opt("The colour of the insulator"),
                opt("The frequency of the supply only"),
            ),
            "Breakdown is governed by field strength (dielectric stress) exceeding E_b, concentrated at the weakest point.",
        ),
        q(
            "Paschen's law expresses the breakdown voltage of a gas gap as a function of:",
            (
                opt("distance only"),
                opt(
                    "the product of pressure and distance, p·d, with a characteristic minimum",
                    correct=True,
                ),
                opt("current only"),
                opt("temperature only"),
            ),
            "Paschen's law is V_b = f(p·d), and the curve has a minimum below which voltage rises again.",
        ),
        q(
            "Which statement about breakdown in liquids and solids is correct?",
            (
                opt("Both recover fully like gases after a flashover"),
                opt(
                    "Solid breakdown is permanent, and treeing from void discharges ages solids over time",
                    correct=True,
                ),
                opt("Liquids are immune to moisture and particles"),
                opt("Solids fail only from the colour of the material"),
            ),
            "Solid breakdown is permanent damage; partial discharges in voids cause treeing that ages insulation toward failure.",
        ),
        q(
            "Which is an example of an EHV transmission voltage?",
            (
                opt("230 V"),
                opt("11 kV"),
                opt("400 kV", correct=True),
                opt("48 V"),
            ),
            "EHV levels are around 345 to 765 kV; 400 kV is a typical example.",
        ),
        q(
            "Why does creepage distance usually need to exceed clearance?",
            (
                opt("Because air conducts better than the insulator surface"),
                opt(
                    "Because surface pollution and moisture allow current to track along the insulator",
                    correct=True,
                ),
                opt("Because clearance is irrelevant indoors"),
                opt("Because creepage applies only to DC"),
            ),
            "Contaminated, moist surfaces permit tracking, so the surface path (creepage) must be longer than the air path (clearance).",
        ),
    ),
)
