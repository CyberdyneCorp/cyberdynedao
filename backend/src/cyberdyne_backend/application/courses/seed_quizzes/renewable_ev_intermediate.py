"""Quiz questions for the Renewable Energy & EV Powertrains - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "PV system design: modules, strings & MPPT": (
            q(
                "Connecting PV modules in series increases the:",
                (
                    opt("string voltage", correct=True),
                    opt("current only"),
                    opt("temperature"),
                    opt("color"),
                ),
                "Series adds voltage; parallel adds current.",
            ),
            q(
                "An MPPT algorithm (e.g. perturb-and-observe) adjusts operating point to:",
                (
                    opt("track the maximum power point as conditions change", correct=True),
                    opt("fix the voltage forever"),
                    opt("minimize power"),
                    opt("disconnect"),
                ),
                "It hunts for the MPP.",
            ),
            q(
                "Partial shading of a string can cause:",
                (
                    opt("multiple local maxima on the P-V curve", correct=True),
                    opt("higher output"),
                    opt("no effect"),
                    opt("constant power"),
                ),
                "Bypass diodes and global MPPT help.",
            ),
        ),
        "Wind turbine systems & generators (DFIG, PMSG)": (
            q(
                "A DFIG wind turbine uses a:",
                (
                    opt("doubly-fed induction generator with a partial converter", correct=True),
                    opt("full converter always"),
                    opt("DC generator"),
                    opt("no generator"),
                ),
                "DFIG needs only a fractional-rated converter.",
            ),
            q(
                "A PMSG-based turbine typically uses:",
                (
                    opt("a full-scale power converter", correct=True),
                    opt("no converter"),
                    opt("a gearbox only"),
                    opt("a battery only"),
                ),
                "Permanent-magnet synchronous generator, full converter.",
            ),
            q(
                "Variable-speed turbines improve:",
                (
                    opt("energy capture and reduce mechanical stress", correct=True),
                    opt("nothing"),
                    opt("only noise"),
                    opt("only color"),
                ),
                "They track optimal tip-speed ratio.",
            ),
        ),
        "Power converters for renewable integration": (
            q(
                "A grid-following inverter relies on:",
                (
                    opt("an existing grid voltage to synchronize", correct=True),
                    opt("its own reference only"),
                    opt("DC only"),
                    opt("no grid"),
                ),
                "Most PV inverters are grid-following.",
            ),
            q(
                "DC-DC converters in PV systems are used for:",
                (
                    opt("boosting/MPPT before the inverter", correct=True),
                    opt("AC conversion"),
                    opt("metering"),
                    opt("painting"),
                ),
                "Stage the voltage and track MPP.",
            ),
            q(
                "Converters must meet grid codes for:",
                (
                    opt("power quality and ride-through", correct=True),
                    opt("color"),
                    opt("weight"),
                    opt("font"),
                ),
                "Harmonics, reactive support, ride-through.",
            ),
        ),
        "The EV powertrain architecture": (
            q(
                "The core EV powertrain chain is:",
                (
                    opt("battery -> inverter -> motor", correct=True),
                    opt("engine -> gearbox -> wheels only"),
                    opt("solar -> grid"),
                    opt("fuel -> tank"),
                ),
                "Battery DC to inverter to traction motor.",
            ),
            q(
                "The traction inverter's job is to:",
                (
                    opt("convert battery DC to AC for the motor", correct=True),
                    opt("store energy"),
                    opt("charge from the grid only"),
                    opt("measure speed"),
                ),
                "Drives the AC traction motor.",
            ),
            q(
                "Most modern EV traction motors are:",
                (
                    opt("permanent-magnet synchronous or induction", correct=True),
                    opt("brushed DC only"),
                    opt("stepper motors"),
                    opt("universal motors"),
                ),
                "PMSM/induction dominate.",
            ),
        ),
        "EV charging: AC/DC levels & fast charging": (
            q(
                "AC (onboard) charging is limited by:",
                (
                    opt("the onboard charger's power rating", correct=True),
                    opt("the battery color"),
                    opt("the motor size"),
                    opt("nothing"),
                ),
                "Onboard charger sets AC charge rate.",
            ),
            q(
                "DC fast charging bypasses the onboard charger by:",
                (
                    opt("feeding DC directly to the battery", correct=True),
                    opt("using AC to the motor"),
                    opt("charging the inverter"),
                    opt("using the grid AC directly"),
                ),
                "Off-board converter supplies DC.",
            ),
            q(
                "Charging standards include:",
                (
                    opt("CCS, CHAdeMO and NACS", correct=True),
                    opt("HTTP and FTP"),
                    opt("USB only"),
                    opt("none"),
                ),
                "EV charging connector standards.",
            ),
        ),
        "Battery management systems: SoC & SoH": (
            q(
                "A BMS primarily ensures:",
                (
                    opt("safe operation within voltage/current/temperature limits", correct=True),
                    opt("faster charging only"),
                    opt("more range only"),
                    opt("paint quality"),
                ),
                "Safety and longevity management.",
            ),
            q(
                "State of Charge (SoC) represents:",
                (
                    opt("remaining capacity (like a fuel gauge)", correct=True),
                    opt("total lifetime"),
                    opt("temperature"),
                    opt("voltage only"),
                ),
                "Available charge fraction.",
            ),
            q(
                "Cell balancing is needed because:",
                (
                    opt("cells drift apart in charge over time", correct=True),
                    opt("all cells are identical forever"),
                    opt("balancing wastes range only"),
                    opt("it is illegal"),
                ),
                "Keeps series cells matched.",
            ),
        ),
    },
    final=(
        q(
            "Series PV modules increase:",
            (
                opt("voltage", correct=True),
                opt("current"),
                opt("temperature"),
                opt("color"),
            ),
            "Series adds voltage.",
        ),
        q(
            "A DFIG uses a:",
            (
                opt("partial converter", correct=True),
                opt("full converter"),
                opt("DC generator"),
                opt("no generator"),
            ),
            "Fractional converter.",
        ),
        q(
            "Most PV inverters are:",
            (
                opt("grid-following", correct=True),
                opt("grid-forming"),
                opt("DC-only"),
                opt("off-grid only"),
            ),
            "Synchronize to grid.",
        ),
        q(
            "EV powertrain chain:",
            (
                opt("battery->inverter->motor", correct=True),
                opt("engine->gearbox"),
                opt("solar->grid"),
                opt("fuel->tank"),
            ),
            "DC to AC to motor.",
        ),
        q(
            "DC fast charging:",
            (
                opt("feeds DC to the battery", correct=True),
                opt("uses AC to motor"),
                opt("charges inverter"),
                opt("uses grid AC"),
            ),
            "Bypasses onboard charger.",
        ),
        q(
            "SoC represents:",
            (
                opt("remaining capacity", correct=True),
                opt("lifetime"),
                opt("temperature"),
                opt("voltage only"),
            ),
            "Fuel-gauge equivalent.",
        ),
    ),
)
