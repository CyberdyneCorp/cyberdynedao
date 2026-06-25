"""Quiz questions for the High-Voltage Engineering - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Generation of high voltages": (
            q(
                "High AC test voltages are commonly generated with:",
                (
                    opt("cascaded transformers", correct=True),
                    opt("a single 9V battery"),
                    opt("a logic gate"),
                    opt("an op-amp"),
                ),
                "Cascade/test transformers reach high AC voltage.",
            ),
            q(
                "High DC voltages can be produced by a:",
                (
                    opt("Cockcroft-Walton multiplier", correct=True),
                    opt("simple resistor"),
                    opt("single diode at mains"),
                    opt("encoder"),
                ),
                "Voltage-multiplier rectifier circuits.",
            ),
            q(
                "Impulse voltages are generated using a:",
                (
                    opt("Marx generator", correct=True),
                    opt("linear amplifier"),
                    opt("V/f drive"),
                    opt("Hall sensor"),
                ),
                "Marx generators stack charged capacitors.",
            ),
        ),
        "Measurement of high voltages": (
            q(
                "High voltages are measured with:",
                (
                    opt("resistive/capacitive dividers", correct=True),
                    opt("a normal multimeter directly"),
                    opt("an encoder"),
                    opt("a thermocouple only"),
                ),
                "Dividers scale HV down safely.",
            ),
            q(
                "A sphere gap measures peak voltage via:",
                (
                    opt("its breakdown distance", correct=True),
                    opt("its resistance"),
                    opt("its color"),
                    opt("its weight"),
                ),
                "Breakdown voltage relates to gap spacing.",
            ),
            q(
                "Capacitive dividers are preferred for:",
                (
                    opt("fast impulse measurements", correct=True),
                    opt("DC only"),
                    opt("audio"),
                    opt("logic levels"),
                ),
                "Good high-frequency/impulse response.",
            ),
        ),
        "Impulse voltage waveforms": (
            q(
                "A standard lightning impulse is specified by its:",
                (
                    opt("front and tail times (e.g. 1.2/50 us)", correct=True),
                    opt("RMS value only"),
                    opt("frequency"),
                    opt("duty cycle"),
                ),
                "Defined by rise (front) and 50% tail times.",
            ),
            q(
                "Switching impulses have, vs lightning impulses:",
                (
                    opt("much longer front times", correct=True),
                    opt("shorter fronts"),
                    opt("no tail"),
                    opt("higher frequency"),
                ),
                "Switching surges are slower.",
            ),
            q(
                "Impulse testing verifies:",
                (
                    opt("insulation withstand to transient overvoltages", correct=True),
                    opt("steady-state heating"),
                    opt("power factor"),
                    opt("efficiency"),
                ),
                "Checks transient withstand.",
            ),
        ),
        "Insulation coordination": (
            q(
                "Insulation coordination matches equipment withstand to:",
                (
                    opt("expected overvoltages and protection levels", correct=True),
                    opt("the paint color"),
                    opt("the load current only"),
                    opt("the ambient light"),
                ),
                "Coordinates BIL with surge protection.",
            ),
            q(
                "BIL stands for:",
                (
                    opt("Basic Insulation Level", correct=True),
                    opt("Bus Input Line"),
                    opt("Breaker Internal Latch"),
                    opt("Bidirectional Logic"),
                ),
                "Basic Insulation Level (impulse withstand).",
            ),
            q(
                "Surge arresters help coordination by:",
                (
                    opt("clamping overvoltages below equipment BIL", correct=True),
                    opt("increasing voltage"),
                    opt("adding inductance"),
                    opt("removing grounding"),
                ),
                "They limit transient voltage.",
            ),
        ),
        "Overvoltages: lightning & switching surges": (
            q(
                "Lightning overvoltages are characterized as:",
                (
                    opt("fast, high-magnitude transients", correct=True),
                    opt("slow DC drifts"),
                    opt("steady AC"),
                    opt("low-frequency hum"),
                ),
                "Microsecond-scale steep transients.",
            ),
            q(
                "Switching surges arise from:",
                (
                    opt("breaker operations / network switching", correct=True),
                    opt("sunlight"),
                    opt("encoder noise"),
                    opt("paint"),
                ),
                "Energizing/de-energizing causes surges.",
            ),
            q(
                "Temporary overvoltages differ by being:",
                (
                    opt("longer-duration power-frequency overvoltages", correct=True),
                    opt("nanosecond spikes"),
                    opt("DC only"),
                    opt("negative only"),
                ),
                "Sustained power-frequency overvoltages.",
            ),
        ),
        "Surge arresters & protection": (
            q(
                "A modern surge arrester uses:",
                (
                    opt("metal-oxide varistors (ZnO)", correct=True),
                    opt("a fixed linear resistor"),
                    opt("a fuse only"),
                    opt("a capacitor only"),
                ),
                "ZnO MOV arresters clamp surges.",
            ),
            q(
                "An arrester's nonlinear V-I characteristic means it:",
                (
                    opt("conducts heavily only above a threshold", correct=True),
                    opt("is linear"),
                    opt("blocks DC"),
                    opt("is a pure inductor"),
                ),
                "High resistance normally, low during surge.",
            ),
            q(
                "Arresters are placed:",
                (
                    opt("close to protected equipment", correct=True),
                    opt("far away only"),
                    opt("in series with the load"),
                    opt("randomly"),
                ),
                "Proximity limits lead inductance effects.",
            ),
        ),
    },
    final=(
        q(
            "High DC is made with a:",
            (
                opt("Cockcroft-Walton multiplier", correct=True),
                opt("single resistor"),
                opt("logic gate"),
                opt("encoder"),
            ),
            "Voltage multiplier.",
        ),
        q(
            "HV is measured with:",
            (
                opt("dividers", correct=True),
                opt("a plain multimeter"),
                opt("an encoder"),
                opt("a thermocouple"),
            ),
            "Resistive/capacitive dividers.",
        ),
        q(
            "Lightning impulse is e.g.:",
            (
                opt("1.2/50 us front/tail", correct=True),
                opt("50 Hz"),
                opt("unit step"),
                opt("a square wave"),
            ),
            "Standard waveform.",
        ),
        q(
            "BIL means:",
            (
                opt("Basic Insulation Level", correct=True),
                opt("Bus Input Line"),
                opt("Breaker Latch"),
                opt("Binary Level"),
            ),
            "Impulse withstand level.",
        ),
        q(
            "Switching surges come from:",
            (
                opt("breaker/network switching", correct=True),
                opt("sunlight"),
                opt("paint"),
                opt("encoders"),
            ),
            "Switching events.",
        ),
        q(
            "Modern arresters use:",
            (
                opt("ZnO metal-oxide varistors", correct=True),
                opt("linear resistors"),
                opt("fuses"),
                opt("capacitors"),
            ),
            "MOV clamping.",
        ),
    ),
)
