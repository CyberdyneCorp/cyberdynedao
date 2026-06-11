from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The MOSFET as an analog device": (
            q(
                "In which region of operation are analog amplifiers nearly always biased?",
                (
                    opt("Cut-off"),
                    opt("Triode (linear)"),
                    opt("Saturation (active)", correct=True),
                    opt("Breakdown"),
                ),
                "Amplifiers bias the device in saturation, where Id depends strongly on Vgs and weakly on Vds, behaving like a current source steered by the gate.",
            ),
            q(
                "What does the transconductance gm represent?",
                (
                    opt("How much drain current changes per change in gate voltage", correct=True),
                    opt("How much drain current changes per change in drain voltage"),
                    opt("The ratio of gate width to length"),
                    opt("The threshold voltage of the device"),
                ),
                "gm = dId/dVgs is the slope of the Id-Vgs curve: how much the drain current wiggles per gate-voltage wiggle, the gain engine of the device.",
            ),
            q(
                "What does a higher output resistance ro indicate about the transistor as a current source?",
                (
                    opt("It is a less ideal current source"),
                    opt("It is a more ideal current source and gives higher gain", correct=True),
                    opt("It carries more drain current"),
                    opt("It has a larger overdrive voltage"),
                ),
                "ro = 1/(lambda Id); a higher ro means Id depends less on Vds, so the device is a more ideal current source and yields higher amplifier gain.",
            ),
        ),
        "Single-stage amplifiers": (
            q(
                "Which single-stage amplifier gives the most voltage gain and inverts the signal?",
                (
                    opt("Common-source", correct=True),
                    opt("Common-gate"),
                    opt("Common-drain (source follower)"),
                    opt("Cascode buffer"),
                ),
                "The common-source stage drives the gate and taps the drain, giving the intrinsic gain -gm*ro with an inverting (minus) sign.",
            ),
            q(
                "What is the approximate input resistance of a common-gate stage?",
                (
                    opt("Infinite"),
                    opt("1/gm", correct=True),
                    opt("gm*ro"),
                    opt("ro in parallel with Rd"),
                ),
                "The common-gate stage is a current buffer with low input resistance equal to 1/gm and high output resistance.",
            ),
            q(
                "What is the voltage gain of a common-drain (source follower) stage?",
                (
                    opt("Just below 1", correct=True),
                    opt("Equal to gm*ro"),
                    opt("Negative and large"),
                    opt("Exactly zero"),
                ),
                "The source follower has gain gm*Rs/(1 + gm*Rs), which is just below 1; it buffers voltage with high input and low output resistance.",
            ),
        ),
        "Current mirrors and biasing": (
            q(
                "How do two matched transistors in a basic current mirror copy a current?",
                (
                    opt(
                        "By sharing the same gate-source voltage so they carry the same Id",
                        correct=True,
                    ),
                    opt("By sharing the same drain voltage"),
                    opt("By using a precise on-chip resistor between them"),
                    opt("By being biased in the triode region"),
                ),
                "Matched transistors sharing the same Vgs carry the same Id, so the output transistor mirrors the reference current.",
            ),
            q(
                "What advantage does a cascode mirror have over a basic mirror?",
                (
                    opt("It needs less voltage headroom"),
                    opt(
                        "It boosts output resistance to roughly gm*ro^2 for a more ideal current source",
                        correct=True,
                    ),
                    opt("It removes the need for a reference current"),
                    opt("It works only in the triode region"),
                ),
                "Stacking a second transistor boosts the output resistance to about gm*ro^2, making a far more ideal current source at the cost of headroom.",
            ),
            q(
                "If a mirror has a width ratio (W/L)_2 / (W/L)_1 of 2 and Iref is 50 uA, what is Iout?",
                (
                    opt("25 uA"),
                    opt("50 uA"),
                    opt("100 uA", correct=True),
                    opt("200 uA"),
                ),
                "Iout = Iref * ratio = 50 uA * 2 = 100 uA; scaling the width ratio scales the copied current.",
            ),
        ),
        "The differential pair": (
            q(
                "What does a differential pair share between its two matched transistors?",
                (
                    opt("A tail current source", correct=True),
                    opt("A single drain node"),
                    opt("A common gate connection"),
                    opt("One shared threshold voltage adjustment"),
                ),
                "The two matched transistors share a tail current source; the differential input steers that tail current between the two branches.",
            ),
            q(
                "What does the common-mode rejection ratio (CMRR) measure?",
                (
                    opt("How much voltage gain the stage provides"),
                    opt(
                        "How well the pair amplifies the difference while ignoring the common input",
                        correct=True,
                    ),
                    opt("The bandwidth of the amplifier"),
                    opt("The tail current magnitude"),
                ),
                "CMRR = Adm/Acm; it measures how well the pair amplifies the difference of its inputs while rejecting what they have in common.",
            ),
            q(
                "What does replacing the two load resistors with a current-mirror active load achieve?",
                (
                    opt(
                        "It converts the differential signal to single-ended and doubles the effective output current",
                        correct=True,
                    ),
                    opt("It lowers the gain to below one"),
                    opt("It removes the need for a tail current source"),
                    opt("It forces both transistors into cut-off"),
                ),
                "A current-mirror active load converts the differential signal to single-ended and doubles the effective output current, giving gain gm*(ro_n || ro_p).",
            ),
        ),
        "Frequency response of amplifiers": (
            q(
                "How fast does gain roll off above a single RC pole?",
                (
                    opt("-20 dB/decade", correct=True),
                    opt("-40 dB/decade"),
                    opt("It stays flat"),
                    opt("It rises at +20 dB/decade"),
                ),
                "A single pole gives flat gain below it and falls at -20 dB/decade above, with -45 degrees of phase right at the pole frequency.",
            ),
            q(
                "What does the gain-bandwidth product (GBW) of a common-source stage equal?",
                (
                    opt("gm*ro"),
                    opt("gm/(2*pi*C)", correct=True),
                    opt("1/(2*pi*R*C)"),
                    opt("Cgd*(1 + Av)"),
                ),
                "GBW = A0 * fp = gm/(2*pi*C), independent of R; pushing for more gain costs bandwidth one-for-one.",
            ),
            q(
                "What is the Miller effect on an inverting gain stage?",
                (
                    opt(
                        "The gate-drain cap looks far larger from the input, multiplied by the gain",
                        correct=True,
                    ),
                    opt("It increases the output resistance"),
                    opt("It removes the dominant pole"),
                    opt("It eliminates channel-length modulation"),
                ),
                "A bridging Cgd looks like Cgd*(1 + |Av|) at the input, so a small cap on a high-gain stage crushes the bandwidth; the cascode avoids it.",
            ),
        ),
        "Lab: common-source Bode and diff-pair transfer curve": (
            q(
                "In the lab, what shape is the differential-pair current-steering transfer curve?",
                (
                    opt("A straight line at all input levels"),
                    opt("A tanh-like curve that saturates at plus or minus Iss", correct=True),
                    opt("A parabola opening upward"),
                    opt("A step function"),
                ),
                "The long-tailed pair steering is linear for small signals and saturates near plus or minus the tail current Iss for large differential inputs, a tanh-like shape.",
            ),
            q(
                "What single-pole transfer function does the lab use for the common-source amplifier?",
                (
                    opt("H = A0 / (1 + j*f/fp)", correct=True),
                    opt("H = A0 * (1 + j*f/fp)"),
                    opt("H = A0 / (1 + (f/fp)^2)"),
                    opt("H = A0 * j*f/fp"),
                ),
                "The lab models the stage as a single dominant pole: H = A0 / (1 + j*f/fp), with A0 = gm*R and fp = 1/(2*pi*R*Cl).",
            ),
            q(
                "Per the lab's 'try it yourself', what happens when you raise Rd from 20k to 200k?",
                (
                    opt(
                        "More gain and a lower pole, with GBW staying about constant", correct=True
                    ),
                    opt("Less gain and a higher pole"),
                    opt("The diff-pair curve stretches wider"),
                    opt("Both gain and bandwidth increase together"),
                ),
                "Raising Rd gives more gain and a lower pole while GBW stays roughly constant, illustrating the gain-bandwidth tradeoff.",
            ),
        ),
    },
    final=(
        q(
            "Why is a smaller overdrive voltage Vov a key analog design tradeoff?",
            (
                opt(
                    "It gives more gm for a given current but worse headroom and matching",
                    correct=True,
                ),
                opt("It puts the device into the triode region"),
                opt("It increases the threshold voltage"),
                opt("It always lowers the drain current to zero"),
            ),
            "For a given current, gm = 2*Id/Vov, so a smaller overdrive gives more gm (good for gain) but costs headroom and matching.",
        ),
        q(
            "Which stage is used as the input of nearly every op-amp because it rejects common-mode noise?",
            (
                opt("Common-source stage"),
                opt("The differential pair", correct=True),
                opt("A basic current mirror"),
                opt("Source follower"),
            ),
            "The differential pair amplifies the difference of its inputs and rejects the common-mode signal, making it the front door of op-amps, comparators, and high-speed links.",
        ),
        q(
            "On a chip, why are current mirrors preferred over precise resistors for biasing?",
            (
                opt("Resistors cannot be fabricated on silicon at all"),
                opt(
                    "You make one good reference current and copy it everywhere by matching Vgs",
                    correct=True,
                ),
                opt("Mirrors require no reference current"),
                opt("Mirrors only work in cut-off"),
            ),
            "Precise resistors are hard on a chip, so designers make one good reference current and copy it with mirrors that share Vgs across matched devices.",
        ),
        q(
            "What is the intrinsic gain of a single transistor, the maximum a common-source stage can reach?",
            (
                opt("gm/ro"),
                opt("gm*ro", correct=True),
                opt("1/gm"),
                opt("gm*Cgd"),
            ),
            "The intrinsic gain gm*ro is the most voltage gain one transistor can give, reached by a common-source stage as Rd goes to infinity.",
        ),
        q(
            "Why is a plain common-source stage slow at high gain, and what circuit fixes it?",
            (
                opt(
                    "The Miller-multiplied Cgd crushes bandwidth; a cascode holds the drain still to fix it",
                    correct=True,
                ),
                opt("The tail current is too small; a bigger mirror fixes it"),
                opt("The threshold voltage drifts; a bandgap fixes it"),
                opt("Output resistance is too low; a source follower fixes it"),
            ),
            "Miller multiplication makes Cgd look like Cgd*(1+|Av|) at the input; a cascode holds the drain nearly still so there is little swing across Cgd to multiply.",
        ),
    ),
)
