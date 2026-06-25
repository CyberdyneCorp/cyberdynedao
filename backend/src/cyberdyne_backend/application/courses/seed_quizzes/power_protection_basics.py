"""Quiz questions for the Power System Protection & Relaying - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why we protect power systems": (
            q(
                "The primary purpose of protection is to:",
                (
                    opt("isolate faults quickly to protect people and equipment", correct=True),
                    opt("increase voltage"),
                    opt("raise efficiency"),
                    opt("change frequency"),
                ),
                "Fast fault clearing limits damage and hazard.",
            ),
            q(
                "An ideal protection scheme is:",
                (
                    opt("selective, fast, sensitive and reliable", correct=True),
                    opt("slow but cheap"),
                    opt("always tripping"),
                    opt("never tripping"),
                ),
                "Key attributes: selectivity, speed, sensitivity, reliability.",
            ),
            q(
                "Selectivity means:",
                (
                    opt("only the faulted section is disconnected", correct=True),
                    opt("the whole grid trips"),
                    opt("nothing trips"),
                    opt("random tripping"),
                ),
                "Minimize the outage area.",
            ),
        ),
        "Types of faults": (
            q(
                "The most common power-system fault is:",
                (
                    opt("single-line-to-ground", correct=True),
                    opt("three-phase"),
                    opt("line-to-line-to-line"),
                    opt("open conductor"),
                ),
                "~70-80% are single-line-to-ground.",
            ),
            q(
                "The most severe (highest current) fault is usually:",
                (
                    opt("the three-phase fault", correct=True),
                    opt("a high-impedance ground fault"),
                    opt("an open circuit"),
                    opt("a small load"),
                ),
                "Symmetrical three-phase faults give the largest current.",
            ),
            q(
                "Faults are broadly classified as:",
                (
                    opt("symmetrical and asymmetrical", correct=True),
                    opt("AC and DC only"),
                    opt("big and small"),
                    opt("red and blue"),
                ),
                "Balanced (3-phase) vs unbalanced.",
            ),
        ),
        "Fault current & the role of impedance": (
            q(
                "Fault current magnitude is mainly limited by:",
                (
                    opt("the source and line impedance", correct=True),
                    opt("the load resistance only"),
                    opt("the paint"),
                    opt("the frequency only"),
                ),
                "I_fault ~ V / Z to the fault.",
            ),
            q(
                "A fault closer to the source generally gives:",
                (
                    opt("higher fault current", correct=True),
                    opt("lower fault current"),
                    opt("zero current"),
                    opt("constant current"),
                ),
                "Less impedance -> more current.",
            ),
            q(
                "Fault studies compute currents to:",
                (
                    opt("set relays and rate breakers", correct=True),
                    opt("choose cable color"),
                    opt("measure efficiency"),
                    opt("tune audio"),
                ),
                "Sizing and coordination.",
            ),
        ),
        "Instrument transformers: CTs & VTs": (
            q(
                "A current transformer (CT) provides relays with:",
                (
                    opt("a scaled-down current proportional to line current", correct=True),
                    opt("line voltage"),
                    opt("temperature"),
                    opt("frequency only"),
                ),
                "CTs step current down for measurement.",
            ),
            q(
                "A voltage transformer (VT/PT) provides:",
                (
                    opt("a scaled-down voltage", correct=True),
                    opt("scaled current"),
                    opt("torque"),
                    opt("speed"),
                ),
                "VTs step voltage down.",
            ),
            q(
                "CT saturation is a problem because it:",
                (
                    opt("distorts the secondary current during heavy faults", correct=True),
                    opt("improves accuracy"),
                    opt("adds voltage"),
                    opt("cools the CT"),
                ),
                "Saturation corrupts relay measurements.",
            ),
        ),
        "Protection zones & backup": (
            q(
                "Protection zones are arranged to:",
                (
                    opt("overlap so no point is unprotected", correct=True),
                    opt("leave gaps"),
                    opt("cover only loads"),
                    opt("cover only sources"),
                ),
                "Overlapping zones ensure full coverage.",
            ),
            q(
                "Backup protection acts when:",
                (
                    opt("primary protection fails to clear", correct=True),
                    opt("the primary works fine"),
                    opt("there is no fault"),
                    opt("the load is light"),
                ),
                "Backup is the safety net.",
            ),
            q(
                "Backup is often provided by:",
                (
                    opt("time-delayed upstream relays", correct=True),
                    opt("faster relays only"),
                    opt("no relays"),
                    opt("fuses only"),
                ),
                "Upstream relays trip after a delay.",
            ),
        ),
        "Fuses & circuit breakers": (
            q(
                "A fuse protects by:",
                (
                    opt("melting to interrupt overcurrent", correct=True),
                    opt("switching electronically"),
                    opt("measuring voltage"),
                    opt("cooling the line"),
                ),
                "A fusible element melts and clears.",
            ),
            q(
                "A circuit breaker differs from a fuse because it:",
                (
                    opt("can be reset/reclosed", correct=True),
                    opt("is single-use always"),
                    opt("cannot interrupt current"),
                    opt("measures speed"),
                ),
                "Breakers are reusable switching devices.",
            ),
            q(
                "Breaker interrupting rating must exceed:",
                (
                    opt("the maximum prospective fault current", correct=True),
                    opt("the load current only"),
                    opt("the paint rating"),
                    opt("the ambient light"),
                ),
                "It must safely break the largest fault.",
            ),
        ),
    },
    final=(
        q(
            "Protection's purpose:",
            (
                opt("isolate faults fast", correct=True),
                opt("raise voltage"),
                opt("raise efficiency"),
                opt("change frequency"),
            ),
            "Protect people/equipment.",
        ),
        q(
            "Most common fault:",
            (
                opt("single-line-to-ground", correct=True),
                opt("three-phase"),
                opt("open conductor"),
                opt("none"),
            ),
            "~75% SLG.",
        ),
        q(
            "Fault current is limited by:",
            (
                opt("source/line impedance", correct=True),
                opt("load only"),
                opt("paint"),
                opt("frequency"),
            ),
            "I = V/Z.",
        ),
        q(
            "A CT provides:",
            (
                opt("scaled current", correct=True),
                opt("voltage"),
                opt("torque"),
                opt("speed"),
            ),
            "Current scaling.",
        ),
        q(
            "Protection zones should:",
            (
                opt("overlap", correct=True),
                opt("leave gaps"),
                opt("cover loads only"),
                opt("cover sources only"),
            ),
            "Full coverage.",
        ),
        q(
            "A breaker vs fuse:",
            (
                opt("can be reset", correct=True),
                opt("is single-use"),
                opt("cannot interrupt"),
                opt("measures speed"),
            ),
            "Reusable.",
        ),
    ),
)
