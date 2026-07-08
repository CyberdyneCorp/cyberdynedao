"""Academy seed content — Startups in the Age of AI.

A curated video course built on Y Combinator's Startup School playlist
(https://www.youtube.com/playlist?list=PLQ-uHSnFig5M9fW16o2l35jrfdsxGknNB).
The 29 talks are re-ordered from the playlist's reverse-chronological feed
into a curriculum arc — idea → team → building with AI → launch & customers
→ pricing & sales → metrics & fundraising — with a short text intro opening
each part and a final knowledge check.

Video lessons carry only the YouTube URL (the frontend embeds the player);
the connective tissue and the quiz are what the Academy adds on top.
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


def _yt(title: str, video_id: str, duration: str) -> SeedLesson:
    return video_lesson(title, f"https://www.youtube.com/watch?v={video_id}", duration=duration)


_STARTUPS_AGE_OF_AI = SeedCourse(
    slug="startups-in-the-age-of-ai",
    title="Startups in the Age of AI",
    description=(
        "The Y Combinator Startup School playbook, organized as a course: "
        "deciding to start, finding and evaluating ideas, co-founders and "
        "equity, building an MVP with AI leverage, launching, winning your "
        "first customers, pricing and sales, metrics, and fundraising — 29 "
        "talks from YC partners, sequenced for founders building in the AI era."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Welcome — how this course works",
            "5 min",
            """# Startups in the Age of AI

This course packages **Y Combinator's Startup School** — the talks YC gives
its own founders — into one guided arc. It matters *now* because AI has
collapsed the cost of building: a two-person team with AI tooling can ship
what used to take a funded engineering org. What hasn't changed is everything
else — picking a real problem, talking to users, charging money, and growing.

The course runs in six parts:

1. **Foundations & ideas** — should you do this, and what should you build?
2. **Co-founders & team** — the people decisions that kill or carry companies.
3. **Building with AI** — MVPs, vibe coding, and AI-native company design.
4. **Launch & first customers** — doing things that don't scale.
5. **Business models, pricing & sales** — turning users into revenue.
6. **Metrics, fundraising & YC** — measuring what matters and funding it.

Each lesson is a talk by a YC partner (in English). Watch in order — later
talks assume the vocabulary of earlier ones — and finish with the knowledge
check at the end.
""",
        ),
        # ── Part 1 — Foundations & ideas ─────────────────────────────
        _t(
            "Part 1 — Foundations & ideas",
            "2 min",
            """# Part 1 — Foundations & ideas

Before writing code: is a startup the right vehicle for you, and is the idea
worth years of your life? These four talks cover the founder decision, how to
generate and evaluate ideas (and spot **tarpit ideas** — plausible-sounding
ideas that trap thousands of founders), why depth beats idea-hopping, and the
legal/financial vocabulary you'll need from day one.
""",
        ),
        _yt("Should You Start A Startup?", "BUE-icVYRFU", "17 min"),
        _yt("How to Get and Evaluate Startup Ideas", "Th8JoIan4dg", "32 min"),
        _yt("Pick One Idea and Go Deep", "R56RJFZBasQ", "12 min"),
        _yt("Starting a Company? The Key Terms You Should Know", "wH3TKpALlw4", "18 min"),
        # ── Part 2 — Co-founders & team ──────────────────────────────
        _t(
            "Part 2 — Co-founders & team",
            "2 min",
            """# Part 2 — Co-founders & team

Co-founder conflict is one of the top startup killers — ahead of most market
risks. These talks cover where to find a co-founder and what to look for, how
to keep the relationship healthy under stress, the equity-split mistakes that
poison companies years later (split roughly equally, always with **vesting**
and a cliff), and — once something works — how to hire your first engineers
and account executives.
""",
        ),
        _yt("How To Find A Co-Founder", "Fk9BCr5pLTU", "21 min"),
        _yt("Keys To Successful Co-Founder Relationships", "A4SLDQDXdp0", "32 min"),
        _yt("Co-Founder Equity Mistakes to Avoid", "DISocTmEwiI", "20 min"),
        _yt(
            "The Startup Playbook for Hiring Your First Engineers and AEs",
            "i_PjjXKNpA4",
            "43 min",
        ),
        # ── Part 3 — Building with AI ────────────────────────────────
        _t(
            "Part 3 — Building with AI",
            "2 min",
            """# Part 3 — Building with AI

The AI-era part of the course. How to design a company around AI from day
one, why services businesses — long dismissed by venture investors — become
venture-scale when agents do the delivery, and how to get real leverage from
**vibe coding** without drowning in unreviewed slop. Then the fundamentals AI
doesn't change: what a real **MVP** is (small, fast, for your first users —
not a polished v1), and how to talk to users so they tell you the truth
instead of what you want to hear.
""",
        ),
        _yt("How To Build A Company With AI From The Ground Up", "EN7frwQIbKc", "10 min"),
        _yt("How to Build an AI-Native Services Company", "gSNFJbgoaHI", "11 min"),
        _yt("How To Get The Most Out Of Vibe Coding", "BJjsfNO5JTo", "17 min"),
        _yt("Tips For Technical Startup Founders", "rP7bpYsfa6Q", "28 min"),
        _yt("How to Build An MVP", "QRZ_l7cVzzU", "17 min"),
        _yt("How To Talk To Users", "z1iF1c8w5Lg", "18 min"),
        # ── Part 4 — Launch & first customers ────────────────────────
        _t(
            "Part 4 — Launch & first customers",
            "2 min",
            """# Part 4 — Launch & first customers

Launching is not a one-time press event — it's something you do early and
repeatedly, and almost nobody remembers your launch but you. Then the classic
YC counsel: **do things that don't scale**. Recruit your first users by hand,
one at a time; write cold emails that convert; and obsess over **retention**,
because keeping users is the only real evidence of product-market fit.
""",
        ),
        _yt("The Best Way To Launch Your Startup", "u36A-YTxiOw", "21 min"),
        _yt("How to Get Your First Customers", "hyYCn_kAngI", "23 min"),
        _yt("How to Get Your First 10 Customers", "_FBivfgOvuE", "14 min"),
        _yt("How To Convert Customers With Cold Emails", "7Kh_fpxP1yY", "33 min"),
        _yt("How To Keep Your Users", "VNxBZ7ka5J0", "29 min"),
        # ── Part 5 — Business models, pricing & sales ────────────────
        _t(
            "Part 5 — Business models, pricing & sales",
            "2 min",
            """# Part 5 — Business models, pricing & sales

Revenue turns a project into a company. These talks map the nine business
models behind most billion-dollar companies, why founders almost always
**undercharge** (price on value, not cost), how founder-led sales actually
works as a repeatable playbook, what changes when you sell to enterprises —
and a deep dive on dev-tools companies, where the user is a developer and
the playbook inverts.
""",
        ),
        _yt("Startup Business Models and Pricing", "oWZbWzAyHAE", "33 min"),
        _yt("How To Price For B2B", "4hjiRmgmHiU", "18 min"),
        _yt("The Sales Playbook For Founders", "DH7REvnQ1y4", "19 min"),
        _yt("Enterprise Sales", "0fKYVl12VTA", "23 min"),
        _yt("How To Start A Dev Tools Company", "z1aKRhRnVNk", "33 min"),
        # ── Part 6 — Metrics, fundraising & YC ───────────────────────
        _t(
            "Part 6 — Metrics, fundraising & YC",
            "2 min",
            """# Part 6 — Metrics, fundraising & YC

What you measure is what you optimize. Consumer companies live and die by
retention curves; B2B companies by revenue growth and churn; every company
needs one primary metric and honest KPIs. With that in place, fundraising:
how SAFEs, dilution and milestone-based raising actually work — and, if you
want it, how to put your best foot forward applying to Y Combinator.
""",
        ),
        _yt("Consumer Startup Metrics", "fdD4y4Civp4", "22 min"),
        _yt("B2B Startup Metrics", "_mKeVGSqQac", "24 min"),
        _yt("Setting KPIs and Goals", "6DTK9yDP6p0", "27 min"),
        _yt("How Startup Fundraising Works", "zBUhQPPS9AY", "28 min"),
        _yt("How to Apply And Succeed at Y Combinator", "B5tU2447OK8", "25 min"),
        # ── Final quiz ───────────────────────────────────────────────
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "According to YC, what is the best source of startup ideas?",
                    (
                        opt("Brainstorming sessions aimed at inventing 'the next big thing'"),
                        opt(
                            "Problems you have experienced yourself and understand deeply",
                            correct=True,
                        ),
                        opt("Copying whatever category most VCs are funding this year"),
                        opt("Keyword research to find high-traffic search terms"),
                    ),
                    "Ideas grounded in problems the founders have lived produce founder/market "
                    "fit; 'thought of' ideas tend toward tarpits — plausible, popular, and "
                    "already tried by thousands of teams.",
                ),
                q(
                    "What is a 'tarpit idea'?",
                    (
                        opt("An idea in a heavily regulated industry"),
                        opt("An idea that requires deep technical expertise"),
                        opt(
                            "A common idea that seems appealing and novel but has trapped "
                            "many founders before, usually because a structural problem "
                            "makes it much harder than it looks",
                            correct=True,
                        ),
                        opt("An idea that only works with venture funding"),
                    ),
                    "Tarpit ideas (e.g. an app to discover things to do with friends) look "
                    "under-served but have consumed thousands of teams — the demand or "
                    "distribution structurally isn't there.",
                ),
                q(
                    "How does YC recommend splitting equity between co-founders?",
                    (
                        opt("Proportional to each founder's initial capital contribution"),
                        opt("Whoever had the idea keeps a controlling majority"),
                        opt(
                            "Roughly equal splits, always subject to vesting with a cliff",
                            correct=True,
                        ),
                        opt("Decide later, once the company has revenue"),
                    ),
                    "Near-equal splits keep every founder fully motivated for a decade-long "
                    "journey; vesting (typically 4 years with a 1-year cliff) protects the "
                    "company if someone leaves early.",
                ),
                q(
                    "What is the defining property of a good MVP in YC's framing?",
                    (
                        opt("It is polished enough that early users can't tell it's v1"),
                        opt(
                            "It is built fast (weeks, not months) and put in front of real "
                            "users so you can start learning",
                            correct=True,
                        ),
                        opt("It already includes the features enterprise buyers will need"),
                        opt("It is fully automated end to end before anyone sees it"),
                    ),
                    "The point of an MVP is learning velocity: ship something minimal to your "
                    "first users, iterate from what they do — not what they say.",
                ),
                q(
                    "When talking to users, which question style yields the most reliable signal?",
                    (
                        opt("'Would you use a product that did X?'"),
                        opt("'How much would you pay for X?'"),
                        opt(
                            "Questions about their life and past behavior — how they hit the "
                            "problem, what it costs them, what they've already tried",
                            correct=True,
                        ),
                        opt("A demo followed by asking whether they liked it"),
                    ),
                    "Hypotheticals invite polite lies. Specifics about past behavior — the "
                    "core of talking to users well — reveal whether the problem is real, "
                    "frequent, and worth money.",
                ),
                q(
                    "YC's advice on launching is to…",
                    (
                        opt("wait until the product is complete, then do one big press launch"),
                        opt(
                            "launch early and launch repeatedly — almost nobody remembers "
                            "your launch, and real feedback starts when users arrive",
                            correct=True,
                        ),
                        opt("stay in private beta until a journalist agrees to cover you"),
                        opt("time the launch to coincide with a fundraise"),
                    ),
                    "Launches are cheap and forgettable; treat them as a repeatable channel "
                    "for learning, not a one-shot event to be perfected.",
                ),
                q(
                    "'Do things that don't scale' means your first customers should come from…",
                    (
                        opt("paid advertising tuned by an agency"),
                        opt("waiting for organic search traffic to compound"),
                        opt(
                            "manually recruiting individual users — direct outreach, personal "
                            "onboarding, and hand-holding",
                            correct=True,
                        ),
                        opt("a self-serve funnel with no human contact"),
                    ),
                    "Early on, recruiting users one at a time is faster than building scalable "
                    "acquisition, and the direct contact is itself the best source of product "
                    "feedback.",
                ),
                q(
                    "What is the most common B2B pricing mistake YC sees founders make?",
                    (
                        opt(
                            "Charging too little — pricing from cost or fear instead of the "
                            "value delivered",
                            correct=True,
                        ),
                        opt("Charging too much and pricing out the market"),
                        opt("Using annual contracts instead of monthly"),
                        opt("Publishing prices on the website"),
                    ),
                    "Underpricing starves the company and signals a non-serious product. "
                    "Price against the value created (and competitors' cost of the problem), "
                    "then iterate upward.",
                ),
                q(
                    "Which single signal is the strongest evidence of product-market fit?",
                    (
                        opt("Total registered accounts"),
                        opt("Press coverage and social-media mentions"),
                        opt(
                            "Retention — cohort curves that flatten because users keep coming "
                            "back (or revenue that keeps renewing)",
                            correct=True,
                        ),
                        opt("Winning startup pitch competitions"),
                    ),
                    "Acquisition can be bought and signups can be hyped; only retention shows "
                    "the product delivers recurring value. Consumer and B2B metrics talks "
                    "both anchor on it.",
                ),
                q(
                    "In the AI-native company talks, what do AI agents change about the "
                    "traditional services business model?",
                    (
                        opt("Nothing — services still scale only by hiring more people"),
                        opt(
                            "Delivery work that used to require headcount can be done by "
                            "software, giving services companies software-like margins and "
                            "venture-scale potential",
                            correct=True,
                        ),
                        opt("AI removes the need to charge for services at all"),
                        opt("Agents make services companies cheaper to run but slower to grow"),
                    ),
                    "When agents do the delivery, revenue decouples from headcount — the "
                    "reason YC now funds AI-native services companies it would once have "
                    "passed on.",
                ),
                q(
                    "What is YC's core guidance for getting real leverage out of vibe coding?",
                    (
                        opt(
                            "Let the model ship whatever runs — reading the output slows you down",
                        ),
                        opt(
                            "Plan before prompting, keep changes small, review and test what "
                            "the AI produces — you remain the engineer of record",
                            correct=True,
                        ),
                        opt("Only use it for throwaway prototypes, never production code"),
                        opt("Fine-tune your own model before using AI on your codebase"),
                    ),
                    "AI coding multiplies output, but unreviewed generated code compounds "
                    "into unmaintainable systems; structure, small iterations, and review "
                    "keep the speed without the debt.",
                ),
                q(
                    "How does a SAFE (Simple Agreement for Future Equity) work?",
                    (
                        opt("It is a loan that accrues interest until repaid"),
                        opt(
                            "The investor pays now and receives shares later, when a priced "
                            "round converts it — typically subject to a valuation cap and/or "
                            "discount",
                            correct=True,
                        ),
                        opt("It grants equity immediately at a negotiated share price"),
                        opt("It guarantees the investor a board seat"),
                    ),
                    "SAFEs defer the valuation negotiation: money in now, equity at the next "
                    "priced round on cap/discount terms — the standard instrument for early "
                    "fundraising.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

STARTUPS_AGE_OF_AI_COURSES: tuple[SeedCourse, ...] = (_STARTUPS_AGE_OF_AI,)
