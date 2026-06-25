"""Quiz questions for the High-Voltage Engineering - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "HV testing techniques & standards": (
            q(
                "HV type tests follow standards such as:",
                (
                    opt("IEC / IEEE", correct=True),
                    opt("HTTP"),
                    opt("USB"),
                    opt("JSON"),
                ),
                "International HV test standards (IEC 60060 etc.).",
            ),
            q(
                "A withstand test confirms insulation:",
                (
                    opt("survives a specified voltage without breakdown", correct=True),
                    opt("fails immediately"),
                    opt("heats up"),
                    opt("changes color"),
                ),
                "Pass = no breakdown at the test level.",
            ),
            q(
                "Test voltages are usually expressed relative to:",
                (
                    opt("rated/system voltage", correct=True),
                    opt("ambient temperature"),
                    opt("the encoder"),
                    opt("the bus current"),
                ),
                "Multiples of rated voltage.",
            ),
        ),
        "Partial discharge measurement & diagnostics": (
            q(
                "Partial discharge (PD) is:",
                (
                    opt(
                        "a localized breakdown that does not fully bridge the insulation",
                        correct=True,
                    ),
                    opt("a full flashover"),
                    opt("steady leakage current"),
                    opt("thermal expansion"),
                ),
                "PD bridges only part of the gap.",
            ),
            q(
                "PD is harmful because it:",
                (
                    opt("gradually degrades insulation", correct=True),
                    opt("improves insulation"),
                    opt("cools the device"),
                    opt("adds capacitance"),
                ),
                "Cumulative damage leads to failure.",
            ),
            q(
                "PD is commonly detected via:",
                (
                    opt("high-frequency current/acoustic/UHF sensing", correct=True),
                    opt("a voltmeter only"),
                    opt("weight"),
                    opt("color"),
                ),
                "PD emits HF pulses, sound, and UHF.",
            ),
        ),
        "Gas-insulated switchgear (GIS) & SF6": (
            q(
                "GIS uses SF6 gas because it has:",
                (
                    opt("high dielectric strength", correct=True),
                    opt("low cost only"),
                    opt("high conductivity"),
                    opt("no insulating ability"),
                ),
                "SF6 is an excellent insulator/arc quencher.",
            ),
            q(
                "A major drawback of SF6 is:",
                (
                    opt("it is a potent greenhouse gas", correct=True),
                    opt("it conducts electricity"),
                    opt("it is flammable"),
                    opt("it is radioactive"),
                ),
                "High global-warming potential drives alternatives.",
            ),
            q(
                "GIS is favored where:",
                (
                    opt("space is limited / harsh environments", correct=True),
                    opt("cost is the only factor"),
                    opt("no insulation needed"),
                    opt("outdoors only"),
                ),
                "Compact and weather-sealed.",
            ),
        ),
        "HVDC insulation & converter stations": (
            q(
                "HVDC insulation differs from AC because field distribution is governed by:",
                (
                    opt("conductivity (resistive) rather than permittivity", correct=True),
                    opt("frequency"),
                    opt("color"),
                    opt("inductance"),
                ),
                "DC fields follow resistivity, sensitive to temperature.",
            ),
            q(
                "A converter station's core component is the:",
                (
                    opt("power-electronic converter (LCC/VSC)", correct=True),
                    opt("a simple transformer only"),
                    opt("an encoder"),
                    opt("a fuse"),
                ),
                "Converters change AC<->DC.",
            ),
            q(
                "HVDC is chosen for:",
                (
                    opt("long-distance / submarine bulk transmission", correct=True),
                    opt("short urban feeders only"),
                    opt("lighting"),
                    opt("logic circuits"),
                ),
                "Lower losses over long distances.",
            ),
        ),
        "Cable, bushing & transformer insulation": (
            q(
                "Modern HV cables commonly use insulation of:",
                (
                    opt("cross-linked polyethylene (XLPE)", correct=True),
                    opt("bare air"),
                    opt("cotton"),
                    opt("water"),
                ),
                "XLPE is the standard solid dielectric.",
            ),
            q(
                "A bushing's job is to:",
                (
                    opt("bring a conductor through a grounded barrier safely", correct=True),
                    opt("store energy"),
                    opt("switch current"),
                    opt("measure speed"),
                ),
                "Insulated feedthrough.",
            ),
            q(
                "Transformer insulation health is monitored by:",
                (
                    opt("dissolved gas analysis (DGA) of the oil", correct=True),
                    opt("paint inspection"),
                    opt("weighing it"),
                    opt("listening for music"),
                ),
                "DGA detects incipient faults.",
            ),
        ),
        "Condition monitoring & a HV test case study": (
            q(
                "Condition monitoring aims to:",
                (
                    opt("detect degradation before failure", correct=True),
                    opt("wait for failure"),
                    opt("increase voltage"),
                    opt("reduce ratings"),
                ),
                "Predictive maintenance.",
            ),
            q(
                "A common online diagnostic is:",
                (
                    opt("partial-discharge monitoring", correct=True),
                    opt("repainting"),
                    opt("manual disconnection"),
                    opt("guesswork"),
                ),
                "PD trends indicate insulation health.",
            ),
            q(
                "Commissioning tests are performed:",
                (
                    opt("before energizing new equipment", correct=True),
                    opt("only after failure"),
                    opt("never"),
                    opt("randomly during operation"),
                ),
                "Verify integrity before service.",
            ),
        ),
    },
    final=(
        q(
            "HV tests follow:",
            (
                opt("IEC/IEEE standards", correct=True),
                opt("HTTP"),
                opt("USB"),
                opt("JSON"),
            ),
            "International standards.",
        ),
        q(
            "Partial discharge is:",
            (
                opt("partial localized breakdown", correct=True),
                opt("full flashover"),
                opt("steady leakage"),
                opt("expansion"),
            ),
            "Does not fully bridge.",
        ),
        q(
            "GIS uses SF6 for its:",
            (
                opt("high dielectric strength", correct=True),
                opt("conductivity"),
                opt("flammability"),
                opt("weight"),
            ),
            "Strong insulator.",
        ),
        q(
            "HVDC insulation fields follow:",
            (
                opt("conductivity (resistive)", correct=True),
                opt("permittivity"),
                opt("color"),
                opt("frequency"),
            ),
            "Resistive field grading.",
        ),
        q(
            "HV cables use:",
            (
                opt("XLPE", correct=True),
                opt("bare air"),
                opt("cotton"),
                opt("water"),
            ),
            "Cross-linked PE.",
        ),
        q(
            "Transformer oil is monitored by:",
            (
                opt("dissolved gas analysis", correct=True),
                opt("painting"),
                opt("weighing"),
                opt("listening"),
            ),
            "DGA.",
        ),
    ),
)
