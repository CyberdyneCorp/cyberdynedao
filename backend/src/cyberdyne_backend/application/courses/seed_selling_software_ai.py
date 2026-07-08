"""Academy seed content — Surviving & Selling Software in the Age of AI.

Built around Rainer Stropek's TEDxLinz talk "What to teach when AI writes
the code" (https://www.youtube.com/watch?v=yhGzXULZkEw). The talk supplies
the human core — the grief of automation, AI as one more abstraction layer,
clarity as the new programming language — and the text lessons extend it
into the economics the title promises: what happens to a market when the
cost of building software collapses toward zero, what still commands a
price, and how to sell software when anyone can generate it.

Companion to ``seed_startups_age_of_ai`` (same module family in the
Computer Engineering path).
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
    video_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


_SELLING_SOFTWARE_AI = SeedCourse(
    slug="selling-software-in-the-age-of-ai",
    title="Surviving & Selling Software in the Age of AI",
    description=(
        "What should you do when the cost of developing software goes to "
        "zero? Anchored in Rainer Stropek's TEDx talk 'What to teach when AI "
        "writes the code', this course works through the identity shift "
        "(coder → developer), the economics of near-free code, what still "
        "commands a price — verification, trust, distribution, taste — and "
        "concrete strategies for selling software when anyone can generate it."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Welcome — the question this course answers",
            "5 min",
            """# When code becomes (almost) free

For seventy years, software was expensive to make. Whole industries — and
whole careers — were built on that scarcity: if you could turn an idea into
working code, someone would pay you well for it.

AI is collapsing that scarcity. Features that took a team a sprint now take
one person an afternoon. The marginal cost of *producing* code is heading
toward zero — and when the cost of producing something falls, the price of
selling it follows, unless you're selling something else along with it.

This course works through the two questions that fall out of that:

1. **How do you survive** — as a developer whose craft is being automated?
2. **How do you sell software** — when your customers know they could
   generate something similar themselves?

We start with the human side: an 18-minute TEDx talk by **Rainer Stropek**,
a developer and AI educator who lived through the identity crisis this shift
causes and came out the other side more capable, not less. Then five text
lessons extend his argument into economics and strategy, and a final quiz
checks what stuck.
""",
        ),
        video_lesson(
            "What to teach when AI writes the code (TEDx)",
            "https://www.youtube.com/watch?v=yhGzXULZkEw",
            duration="18 min",
        ),
        _t(
            "The talk, distilled",
            "8 min",
            """# The talk, distilled

Stropek's argument moves in five steps. Keep them — the rest of the course
builds on each one.

**1. The grief is real, and it isn't fear of technology.** His carpenter
image: a robot can shape wood faster and more precisely, and the carpenter
could learn to program the robot — but what he loved was *the process*, not
just the result. Developers who resist AI aren't Luddites; many are grieving
the part of the work they fell in love with.

**2. Code was never the point.** Looking back at his first programs on a
Commodore C128, Stropek realizes he "was never in love primarily with
coding — I was in love with developing things, with turning vague thoughts
into something real and usable. Code was just a tool." His sentence for it:
*"I'm not just a coder, I'm a developer."*

**3. AI is an abstraction layer, not a replacement.** Programming languages
already freed us from registers and machine code. AI is the next layer up.
"It doesn't shrink my role — it expands it. The goals I aim for are bigger
now." The distance between idea and reality gets drastically shorter.

**4. Coding survives the way chess survived.** Machines beat us at chess;
we still play. Engines outrun us; we still run. "Efficiency was never the
point, experience was." And practically: AI makes mistakes, and **the last
few percent between *almost correct* and *actually correct* are expensive
and valuable.** People who truly understand code close that gap.

**5. Programming is the canary in the coal mine.** Designers, writers,
lawyers, accountants, doctors — every knowledge profession is entering the
same emotional arc: denial → fear → grief → *redefinition*. Each has to find
its own "layer above": not a pixel pusher but a visual thinker; not a
sentence crafter but a storyteller.

His thesis, and this course's hinge: **"The new programming language is
clarity."** Syntax is no longer the bottleneck — describing what you want,
with constraints, examples and tests of intent, is.
""",
        ),
        _t(
            "The economics of near-free code",
            "10 min",
            """# The economics of near-free code

Treat "the cost of developing software goes to zero" as an economist would.
Three forces decide what happens to your paycheck and your product.

## 1. Price follows marginal cost — for commodities

In a competitive market, price gets pushed toward the marginal cost of
production. If generating a CRUD app costs minutes of GPU time, *generic*
CRUD apps will sell for roughly that: nothing. Anything whose entire value
is "it's working code" is becoming a commodity.

## 2. Demand explodes — the Jevons effect

When steam engines got more efficient, coal consumption went *up*, not
down: cheaper use of a resource multiplies the uses people find for it
(the **Jevons paradox**). Software is the same. At near-zero build cost,
custom software becomes viable for problems that never justified a
developer before — the one-person business, the niche workflow, the
throwaway tool. Total demand for *software outcomes* grows enormously,
even as the price of *code* falls.

## 3. Value migrates to the complements

When one input becomes free, the money moves to whatever is **scarce and
complementary** to it (the classic strategy: *commoditize your complement*
— when browsers became free, value moved to what browsers reach). If code
is the free input, the scarce complements are:

- **Knowing what to build** — problem discovery, taste, judgment.
- **Verification** — Stropek's "last few percent"; someone must be
  accountable that it's *actually correct*, secure, and compliant.
- **Distribution** — reaching the person with the problem still costs
  what it always did.
- **Trust & accountability** — a name that stands behind the software
  when it breaks at 3 a.m.
- **Data and context** — the proprietary knowledge the model doesn't have.

**Survival, in one sentence: stop selling the thing whose price is going
to zero, and start owning one of its scarce complements.**
""",
        ),
        _t(
            "What still commands a price",
            "9 min",
            """# What still commands a price

Run any software offering through this filter. The pieces below stay
expensive precisely because AI makes everything around them cheap.

**Judgment about *what* to build.** Generation is cheap; deciding is not.
When everyone can ship anything, the scarce skill is choosing the right
problem, the right scope, the right trade-offs — and saying no. This is
taste, and taste doesn't come out of a prompt.

**Verification and accountability.** "Almost correct" is free; "actually
correct" is not. Someone must read the generated system, know where it's
wrong, and sign their name to it — for security, for compliance, for the
regulator, for the customer's auditor. Liability cannot be delegated to a
model. This is the direct market value of still understanding code deeply.

**Integration into messy reality.** The demo is the easy 80%. The remaining
20% — the legacy ERP, the weird tax rule, the offline factory floor, the
human workflow nobody documented — is where projects actually live or die,
and where domain experts stay unreplaceable.

**Proprietary data and context.** Models are trained on the public
internet. Your customer's order history, your industry's failure modes,
your accumulated evals — those are moats a competitor can't prompt into
existence.

**Distribution and trust.** A thousand AI-generated competitors can
appear in a weekend, and that is exactly why nobody installs software from
strangers anymore. An audience, a sales channel, a brand that has been
right before — these get *more* valuable as supply explodes.

**The experience itself.** Stropek's chess point cuts both ways
commercially: people already pay premiums for handmade, intentional,
human-crafted goods. "Maybe one day we'll even start valuing software that
was handmade — because it is not efficient, it's intentional."
""",
        ),
        _t(
            "How to sell software when anyone can generate it",
            "10 min",
            """# How to sell software when anyone can generate it

Strategies that survive zero-cost generation — each one prices a scarce
complement, not the code.

**1. Sell outcomes, not artifacts.** Nobody wanted code; they wanted the
invoice paid, the shift scheduled, the lead answered. Price the outcome
("collected invoices", "resolved tickets") and AI-cheap production becomes
your margin instead of your competitor's weapon. This is why AI-native
services companies work: agents do the delivery, so revenue decouples from
headcount while you charge for the *result*.

**2. Own the workflow, not the feature.** A feature can be regenerated in
an afternoon; a system of record cannot. Once your product holds the
customer's data, history, integrations and habits, "I could rebuild this"
stops being true in any way that matters. Depth in one niche workflow
beats breadth every time — the Jevons explosion means there are now
thousands of niches worth serving.

**3. Sell verification and accountability.** Audits, SLAs, compliance,
security review, "a human who answers when it breaks". As more of the
world's software is generated, *someone who is liable for it* becomes the
product. The deep-code-understanding career doesn't die — it converts into
this.

**4. Move at the speed of trust, not the speed of code.** When everyone
ships fast, shipping fast is not a moat. Distribution is: the newsletter,
the community, the marketplace position, the reference customers. Budget
as much creativity for reaching people as for building — the building was
never the hard part again.

**5. Charge for taste.** Curation, defaults, opinionated design — "we made
the decisions so you don't have to" is a product. The counter-intuitive
pricing rule from the startup world still holds: underpricing signals a
non-serious product. Value-price even when your costs approach zero;
customers are paying for judgment, not compute.

**Anti-strategies** — things that no longer work: billing by the hour for
code production; competing on feature count; "it's like X but cheaper"
(someone is already generating X for free); secrecy as a moat for anything
a model can re-derive.
""",
        ),
        _t(
            "Your layer above — a survival worksheet",
            "8 min",
            """# Your layer above — a survival worksheet

Stropek's answer to automation grief is not to fight the tool but to
**find the layer above it**: "I'm not just a coder, I'm a developer."
This lesson turns that into an exercise you can actually do. Write your
answers down — the final quiz doesn't ask for them, but your career will.

**1. Separate what you loved from what you did.** The carpenter loved
shaping ideas into objects, not sandpaper. List what you'd miss if AI did
all your typing: the modeling? the debugging hunt? seeing users succeed?
That list is your essence; everything else is syntax.

**2. Write your sentence.** *"I'm not just a ____, I'm a ____."* It must
name a value that survives generation — developer, product thinker,
verifier, storyteller, healer. If the second blank is still an artifact
("...a prompt engineer"), go one layer higher.

**3. Retrain the bottleneck skill: clarity.** Since natural language is
now a programming interface, practice what Stropek calls the new
superpower — turning fuzzy ideas into precise intent:

- describe what you want *with constraints and non-goals*;
- give examples of good and bad output;
- define how you'll test that the result matches the intent.

That skill compounds across every tool you'll ever use, and it is exactly
the spec-writing muscle that selling outcomes (previous lesson) runs on.

**4. Keep one handmade practice.** Chess survived engines. Keep writing
some code by hand — not for efficiency, but because it maintains the
mental models that make you a credible *verifier*, and because the joy
was the point.

**5. Pick your complement.** From the economics lessons: judgment,
verification, integration, data, distribution, trust, taste. Choose the
one nearest your strengths and invest deliberately. Surviving the age of
AI is not about outrunning the model — it's about standing where the
money lands when code is free.
""",
        ),
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is the central thesis of Stropek's TEDx talk?",
                    (
                        opt("AI will eliminate the need to learn programming at all"),
                        opt("The new programming language is clarity", correct=True),
                        opt("Developers should refuse to adopt AI tools"),
                        opt("Only low-level systems programming will survive"),
                    ),
                    "Syntax is no longer the bottleneck — expressing precise intent "
                    "(descriptions, constraints, examples, tests of intent) is the skill "
                    "that now programs the machine.",
                ),
                q(
                    "In the carpenter metaphor, what exactly is lost when the robot "
                    "takes over the work?",
                    (
                        opt("The quality of the finished furniture"),
                        opt("The carpenter's income, permanently"),
                        opt(
                            "The process — the part of the craft the carpenter loved",
                            correct=True,
                        ),
                        opt("Nothing; the metaphor argues nothing is lost"),
                    ),
                    "The robot matches the result. What disappears is the experience of "
                    "the craft — which is why Stropek calls developers' resistance grief, "
                    "not fear of technology.",
                ),
                q(
                    "Why does Stropek say programmers are 'the canary in the coal mine'?",
                    (
                        opt("Programming jobs are the only ones AI threatens"),
                        opt(
                            "Programming is the first profession forced through the "
                            "denial → fear → grief → redefinition arc that other knowledge "
                            "work will follow",
                            correct=True,
                        ),
                        opt("Programmers detect AI bugs before anyone else"),
                        opt("Coding bootcamps collapsed before other schools"),
                    ),
                    "Designers, writers, lawyers, accountants and doctors are entering the "
                    "same emotional journey; programming just got there first.",
                ),
                q(
                    "How does the talk frame AI relative to programming languages?",
                    (
                        opt("As a replacement that makes developers obsolete"),
                        opt("As a passing fad like earlier no-code tools"),
                        opt(
                            "As the next abstraction layer — like languages freed us from "
                            "machine code, it changes the level you work at and expands "
                            "your reach",
                            correct=True,
                        ),
                        opt("As a tool useful only for prototyping"),
                    ),
                    "\"It doesn't replace what I do. It changes the level at which I do "
                    'it… The goals I aim for are bigger now."',
                ),
                q(
                    "Per the talk, why do people who deeply understand code stay "
                    "valuable even when AI writes most of it?",
                    (
                        opt("They can type faster than the model can generate"),
                        opt(
                            "The last few percent between almost correct and actually "
                            "correct are expensive — someone must debug, verify, and close "
                            "that gap",
                            correct=True,
                        ),
                        opt("Regulation will ban generated code in most industries"),
                        opt("Models cannot produce working code without supervision"),
                    ),
                    "AI's error rate falls but never reaches zero, and correctness is "
                    "where the value (and the liability) concentrates.",
                ),
                q(
                    "When the marginal cost of producing generic code falls toward zero, "
                    "what does basic economics predict?",
                    (
                        opt("The price of generic code falls with it", correct=True),
                        opt("The price of generic code rises due to higher demand"),
                        opt("Salaries for writing generic code rise"),
                        opt("Nothing changes as long as demand is stable"),
                    ),
                    "Competition pushes price toward marginal cost, so value must be "
                    "captured in scarce complements instead of in the code itself.",
                ),
                q(
                    "What does the Jevons paradox suggest about total demand for "
                    "software as building it gets dramatically cheaper?",
                    (
                        opt("Demand shrinks because existing software gets reused"),
                        opt(
                            "Demand expands — cheap production makes software viable for "
                            "countless problems that never justified a developer before",
                            correct=True,
                        ),
                        opt("Demand stays constant while prices fall"),
                        opt("Demand moves entirely to hardware"),
                    ),
                    "Like efficient steam engines increasing coal consumption: cheaper "
                    "software multiplies the uses people find for it, exploding the number "
                    "of niches worth serving.",
                ),
                q(
                    "'Commoditize your complement' applied to the age of AI means…",
                    (
                        opt("give your own product away and hope for donations"),
                        opt(
                            "when code becomes the free commodity, position yourself to own "
                            "a scarce complement — distribution, trust, data, verification, "
                            "judgment",
                            correct=True,
                        ),
                        opt("sell the same commodity cheaper than competitors"),
                        opt("bundle unrelated products together"),
                    ),
                    "Money migrates to whatever stays scarce next to the free input. If "
                    "code is free, sell what code is useless without.",
                ),
                q(
                    "Which pricing approach does the course recommend when your "
                    "production costs approach zero?",
                    (
                        opt("Bill by the hour for generation time"),
                        opt("Price slightly above compute cost to stay competitive"),
                        opt(
                            "Value-based pricing on the outcome delivered — customers pay "
                            "for judgment and results, not compute",
                            correct=True,
                        ),
                        opt("Free forever, monetized by ads"),
                    ),
                    "Sell outcomes, not artifacts: near-zero production cost becomes your "
                    "margin, and underpricing signals a non-serious product.",
                ),
                q(
                    "Why does 'shipping fast' stop being a moat, and what replaces it?",
                    (
                        opt(
                            "Everyone ships fast when generation is cheap; distribution and "
                            "trust — audience, channels, brand, reference customers — become "
                            "the scarce advantage",
                            correct=True,
                        ),
                        opt("Speed still wins; nothing replaces it"),
                        opt("Patents replace speed as the primary moat"),
                        opt("Only venture funding determines winners now"),
                    ),
                    "When a thousand competitors can appear in a weekend, reaching people "
                    "who trust you is what can't be generated.",
                ),
                q(
                    "What is the 'layer above' exercise from the final lesson?",
                    (
                        opt("Learning the next programming framework before it's popular"),
                        opt(
                            "Redefining your identity around the value that survives "
                            "generation — 'I'm not just a coder, I'm a developer' — and "
                            "investing in a scarce complement near your strengths",
                            correct=True,
                        ),
                        opt("Moving from engineering into management"),
                        opt("Automating your own job before someone else does"),
                    ),
                    "The answer to automation grief is not fighting the tool but naming "
                    "the essence of your work above the artifact — then retraining the "
                    "clarity muscle that operates every layer below it.",
                ),
            ),
            duration="8 min",
        ),
    ),
)

SELLING_SOFTWARE_AI_COURSES: tuple[SeedCourse, ...] = (_SELLING_SOFTWARE_AI,)
