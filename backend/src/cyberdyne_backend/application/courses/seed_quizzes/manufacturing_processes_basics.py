"""Quiz questions for the Manufacturing Processes - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The manufacturing process families": (
            q(
                "Which process family removes material to reach final shape?",
                (
                    opt("Casting"),
                    opt("Machining", correct=True),
                    opt("Forming"),
                    opt("Additive"),
                ),
                "Machining cuts away unwanted material; casting and forming conserve mass.",
            ),
            q(
                "As production volume rises, processes are favored when they have:",
                (
                    opt("high tooling cost but low per-part cost", correct=True),
                    opt("low tooling cost but high per-part cost"),
                    opt("no tooling and no per-part cost"),
                    opt("the highest scrap rate"),
                ),
                "High-tooling, low-per-part processes amortize tooling over large batches.",
            ),
            q(
                "Casting and forming are alike in that they:",
                (
                    opt("both melt and re-solidify the metal"),
                    opt("largely conserve mass with little waste", correct=True),
                    opt("both remove most of the starting material"),
                    opt("require no dedicated tooling"),
                ),
                "Both are mass-conserving, low-scrap families (unlike machining).",
            ),
        ),
        "Casting fundamentals": (
            q(
                "Chvorinov's rule says solidification time scales with:",
                (
                    opt("the square of the volume-to-surface (V/A) ratio", correct=True),
                    opt("the inverse of the casting weight"),
                    opt("the surface area only"),
                    opt("the pouring temperature only"),
                ),
                "t_s = B (V/A)^n with n about 2, so thick (high V/A) sections freeze last.",
            ),
            q(
                "Why must a riser (feeder) solidify after the part section it feeds?",
                (
                    opt("to keep liquid metal flowing in to fill shrinkage", correct=True),
                    opt("to cool the part faster"),
                    opt("to reduce the pouring temperature"),
                    opt("to add carbon to the casting"),
                ),
                "If the riser freezes first it cannot feed shrinkage, leaving voids.",
            ),
            q(
                "A misrun or cold shut defect is caused by:",
                (
                    opt("metal freezing before completely filling the cavity", correct=True),
                    opt("excess riser volume"),
                    opt("too slow a cooling rate"),
                    opt("over-machining the surface"),
                ),
                "Cold shuts/misruns occur when the metal solidifies before filling.",
            ),
        ),
        "Bulk and sheet forming": (
            q(
                "The strain-hardening law sigma = K epsilon^n describes:",
                (
                    opt("how flow stress rises with plastic strain", correct=True),
                    opt("elastic deflection of a beam"),
                    opt("solidification shrinkage"),
                    opt("tool wear with speed"),
                ),
                "It is the flow-stress (power) law; K is strength coefficient, n the exponent.",
            ),
            q(
                "A larger strain-hardening exponent n generally:",
                (
                    opt("improves formability by delaying necking", correct=True),
                    opt("causes the sheet to neck immediately"),
                    opt("lowers the metal's strength"),
                    opt("has no effect on forming"),
                ),
                "Higher n spreads strain and delays necking (necking near epsilon = n).",
            ),
            q(
                "Compared with cold working, hot working (above recrystallization):",
                (
                    opt("needs lower forces but gives a rougher, oxidized surface", correct=True),
                    opt("needs higher forces and gives a better finish"),
                    opt("permanently strengthens the part by hardening"),
                    opt("is only possible on sheet metal"),
                ),
                "Hot working lowers force and erases hardening, at the cost of finish.",
            ),
        ),
        "Machining: turning, milling, drilling": (
            q(
                "For turning a diameter D at spindle speed N, cutting speed v_c equals:",
                (
                    opt("pi D N", correct=True),
                    opt("D N / pi"),
                    opt("2 pi N"),
                    opt("N / D"),
                ),
                "Surface (cutting) speed is the circumference times rev rate: v_c = pi D N.",
            ),
            q(
                "Which operation uses a rotating multi-tooth cutter on a stationary workpiece?",
                (
                    opt("Milling", correct=True),
                    opt("Turning"),
                    opt("Casting"),
                    opt("Drawing"),
                ),
                "Milling rotates a multi-tooth cutter; turning rotates the work instead.",
            ),
            q(
                "Surface finish in machining generally improves with:",
                (
                    opt("smaller feed and larger tool nose radius", correct=True),
                    opt("larger feed and smaller nose radius"),
                    opt("higher depth of cut only"),
                    opt("removing the coolant"),
                ),
                "Ra is roughly f^2/(32 r), so smaller feed and bigger nose radius help.",
            ),
        ),
        "Joining and assembly overview": (
            q(
                "The heat-affected zone (HAZ) in fusion welding is:",
                (
                    opt("base metal whose microstructure changed without melting", correct=True),
                    opt("the puddle of fully molten weld metal"),
                    opt("the filler rod before use"),
                    opt("the surface oxide layer"),
                ),
                "The HAZ is unmelted base metal altered by the weld thermal cycle.",
            ),
            q(
                "Which joint is a removable (non-permanent) connection?",
                (
                    opt("Bolted joint", correct=True),
                    opt("Fusion weld"),
                    opt("Rivet"),
                    opt("Adhesive bond"),
                ),
                "Bolts/screws allow disassembly; welds, rivets and adhesives are permanent.",
            ),
            q(
                "Brazing and soldering differ from welding because they:",
                (
                    opt("melt only a lower-temperature filler, not the base metal", correct=True),
                    opt("melt the base metals together"),
                    opt("use no filler material at all"),
                    opt("require the parts to rotate"),
                ),
                "In brazing/soldering the filler wets the joint; the base stays solid.",
            ),
        ),
        "Matching process to part": (
            q(
                "In the model C_unit = c_v + C_t/Q, the tooling cost C_t:",
                (
                    opt(
                        "is amortized over the batch, so its impact falls as Q grows", correct=True
                    ),
                    opt("is paid per part regardless of volume"),
                    opt("rises with each additional part"),
                    opt("has no effect on unit cost"),
                ),
                "C_t is fixed and spread over Q parts, so per-unit it shrinks with volume.",
            ),
            q(
                "Die casting and stamping beat machining at high volume because they have:",
                (
                    opt("high fixed tooling cost but very low per-part cost", correct=True),
                    opt("zero tooling cost"),
                    opt("the highest per-part cost"),
                    opt("no break-even quantity"),
                ),
                "Their low c_v wins once volume amortizes the large tooling cost.",
            ),
            q(
                "Which is the best fit for a one-off prototype with internal channels?",
                (
                    opt("Additive manufacturing", correct=True),
                    opt("Die casting"),
                    opt("High-volume stamping"),
                    opt("Investment casting at scale"),
                ),
                "Additive needs no tooling and can build internal features for one-offs.",
            ),
        ),
    },
    final=(
        q(
            "Which family conserves mass with the least material waste?",
            (
                opt("Casting and forming", correct=True),
                opt("Machining"),
                opt("Grinding"),
                opt("Turning"),
            ),
            "Casting and forming reshape without removing much material.",
        ),
        q(
            "Chvorinov's rule relates solidification time mainly to:",
            (
                opt("the casting modulus V/A (squared)", correct=True),
                opt("the part color"),
                opt("the number of risers only"),
                opt("the machine spindle speed"),
            ),
            "t_s = B (V/A)^n; thick sections (high V/A) freeze last.",
        ),
        q(
            "In sigma = K epsilon^n, a higher n means:",
            (
                opt("better formability (delayed necking)", correct=True),
                opt("lower flow stress at all strains"),
                opt("immediate fracture"),
                opt("faster solidification"),
            ),
            "Higher strain-hardening exponent spreads strain and delays necking.",
        ),
        q(
            "Cutting speed for turning at diameter D and spindle speed N is:",
            (
                opt("v_c = pi D N", correct=True),
                opt("v_c = N/D"),
                opt("v_c = D/N"),
                opt("v_c = 2N"),
            ),
            "Surface speed equals circumference times rotation rate.",
        ),
        q(
            "A bolted joint is preferred over a weld when you need:",
            (
                opt("disassembly or service access", correct=True),
                opt("a fully permanent seal"),
                opt("to melt the base metals together"),
                opt("zero fasteners"),
            ),
            "Bolts are removable; welds are permanent.",
        ),
        q(
            "The break-even quantity in process selection is where:",
            (
                opt("two processes have equal unit cost", correct=True),
                opt("tooling cost is zero"),
                opt("the part has no tolerance"),
                opt("the machine reaches max speed"),
            ),
            "It is the volume at which a high-tooling process becomes cheaper per unit.",
        ),
    ),
)
