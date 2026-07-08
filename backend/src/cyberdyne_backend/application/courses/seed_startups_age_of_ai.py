"""Academy seed content — Startups in the Age of AI.

A curated video course built on Y Combinator's Startup School playlist
(https://www.youtube.com/playlist?list=PLQ-uHSnFig5M9fW16o2l35jrfdsxGknNB).
The 29 talks are re-ordered from the playlist's reverse-chronological feed
into a curriculum arc — idea → team → building with AI → launch & customers
→ pricing & sales → metrics & fundraising. Every video is followed by a
"Key ideas" text lesson summarizing the talk (grounded in its transcript)
and a checkpoint quiz; the welcome and part-intro lessons carry checkpoint
quizzes too, and the course closes with a comprehensive final quiz.

Video lessons carry only the YouTube URL (the frontend embeds the player);
the summaries, quizzes and connective tissue are what the Academy adds.
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
        "The Y Combinator Startup School playbook, organized as a course: deciding to start, finding and evaluating ideas, co-founders and equity, building an MVP with AI leverage, launching, winning your first customers, pricing and sales, metrics, and fundraising — 29 talks from YC partners, sequenced for founders building in the AI era."
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
        quiz_lesson(
            "Quiz: Welcome — how this course works",
            (
                q(
                    "Why does the course argue that 'now' is a special moment to build a startup?",
                    (
                        opt("Interest rates make fundraising easier than ever"),
                        opt(
                            "AI has collapsed the cost of building — a tiny team with AI tooling can ship what once took a funded engineering org",
                            correct=True,
                        ),
                        opt("Programming skills are no longer needed at all"),
                        opt("Competition has disappeared from most markets"),
                    ),
                    "The welcome lesson's premise: AI collapsed the cost of building, so tiny teams can ship what once took a funded org — while the rest of company-building stays as hard as ever.",
                ),
                q(
                    "According to the welcome lesson, what has NOT changed in the AI era?",
                    (
                        opt("The cost of shipping software"),
                        opt("The size of team needed to build a product"),
                        opt(
                            "Picking a real problem, talking to users, charging money, and growing",
                            correct=True,
                        ),
                        opt("The speed at which MVPs can be built"),
                    ),
                    "Cheap building changes the how, not the what: real problems, honest user conversations, revenue and growth still decide outcomes.",
                ),
            ),
        ),
        # ── Part 1 — Foundations & ideas ────────────────────────────
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
        quiz_lesson(
            "Quiz: Part 1 — Foundations & ideas",
            (
                q(
                    "What two questions should you settle before writing any code?",
                    (
                        opt("Which logo and company name to use"),
                        opt("Which framework and cloud provider to pick"),
                        opt("How much funding to raise and where to office"),
                        opt(
                            "Whether a startup is the right vehicle for you, and whether the idea is worth years of your life",
                            correct=True,
                        ),
                    ),
                    "Part 1 frames the founder decision and idea evaluation as prerequisites: the startup as a vehicle for you, and the idea as worth years of your life.",
                ),
                q(
                    "Besides generating and evaluating ideas, Part 1 also equips you with…",
                    (
                        opt(
                            "the legal and financial vocabulary founders need from day one",
                            correct=True,
                        ),
                        opt("a template pitch deck for demo day"),
                        opt("venture math for pricing a Series B"),
                        opt("growth-hacking tactics for social media"),
                    ),
                    "The 'Key Terms' talk covers the legal and financial vocabulary — incorporation, equity, vesting — founders need from day one.",
                ),
            ),
        ),
        _yt("Should You Start A Startup?", "BUE-icVYRFU", "17 min"),
        _t(
            "Key ideas — Should You Start A Startup?",
            "4 min",
            """# Key ideas — Should You Start a Startup?

YC group partner Harj Taggar addresses people who don't feel ready to found a company today but may want to someday, covering who is suited to it and how to prepare.

- **Resilience is the most important founder quality**: getting your first users means pushing through personal rejection, and neither school success, work success, nor projected confidence reliably predicts it — Benchling's soft-spoken founders took about two years to make revenue and built a company worth over six billion dollars.
- **Initial motivations don't matter much**: wanting to get rich or simple curiosity are fine starting points, because motivations change; what sustains you long term is genuine interest in the problem and loving the people you work with.
- **Ask "what do I have to lose?"**: honestly work out the worst case — roughly a year with little or no salary — and only start if you can live with it, or anxiety will self-sabotage you.
- **Even failure pays off**: founders learn sales, product, and support at once, and employers like Rippling actively hire former founders.
- **Prepare by finding people, not just ideas**: talk through ideas with smart people (ideally at a startup), build and actually launch side projects, and value a few users who really love your product over many indifferent ones.

Bottom line: if you can live with the worst case and you've found a collaborator you love working with, make the jump.""",
        ),
        quiz_lesson(
            "Quiz: Should You Start A Startup?",
            (
                q(
                    "Which quality does Harj identify as the most important one for startup founders?",
                    (
                        opt("Being a brilliant, ruthless programmer"),
                        opt("Charismatic product genius like famous founders in movies"),
                        opt("Resilience in the face of rejection and roadblocks", correct=True),
                        opt("A strong academic and work track record"),
                    ),
                    "Harj says getting early users takes pushing through a lot of personal rejection, so resilience is the quality he thinks matters most — and stereotypes like the brilliant programmer or product genius aren't required.",
                ),
                q(
                    "What practical question does Harj recommend asking yourself before starting a startup?",
                    (
                        opt('"Is my idea guaranteed to reach a billion-dollar market?"'),
                        opt(
                            '"What do I have to lose — can I live with the worst-case scenario?"',
                            correct=True,
                        ),
                        opt('"Do I have at least five years of savings in the bank?"'),
                        opt('"Have I already raised money from investors?"'),
                    ),
                    "He advises figuring out the worst case — roughly a year with little or no salary — and being honest about whether you can live with it, since otherwise anxiety will self-sabotage your efforts.",
                ),
                q(
                    "How does the talk suggest judging whether a side project is promising as a startup idea?",
                    (
                        opt("By how many people sign up on a waitlist before launch"),
                        opt("By whether it gets immediate explosive traction"),
                        opt("By how much revenue it makes in its first month"),
                        opt(
                            "By whether a few people really love it, rather than many being indifferent",
                            correct=True,
                        ),
                    ),
                    "Quoting Paul Buchheit, Harj says it's better to make a product a few people really love than one many are indifferent to — one passionate user of a crude prototype beats a million waitlist signups.",
                ),
            ),
        ),
        _yt("How to Get and Evaluate Startup Ideas", "Th8JoIan4dg", "32 min"),
        _t(
            "Key ideas — How to Get and Evaluate Startup Ideas",
            "4 min",
            """# Key ideas — Getting and Evaluating Startup Ideas

Drawing on the top 100 YC companies, this talk gives founders conceptual tools to find and judge startup ideas.

- **Avoid the common mistakes**: building a "solution in search of a problem," getting stuck on tar pit ideas (common ideas that look easy but have structural reasons they fail, like apps to make plans with friends), jumping on your first idea, or waiting for a perfect one — an idea only needs to be a good starting point.
- **Evaluate ideas with key questions**: founder-market fit is arguably the most important criterion, alongside market size (big, or small and rapidly growing like early Coinbase), how acute the problem is (Brex), competition, timing ("why now"), proxies, and scalability.
- **Three things that look bad are actually good**: ideas that are hard to get started (Stripe and "schlep blindness"), boring spaces (Gusto's payroll software), and existing competitors (Dropbox was roughly the 20th cloud storage company but had the right insight).
- **Most great ideas come organically** — at least 70% of the top 100 YC companies — so become an expert, work at a startup, and build interesting things.
- **If generating ideas deliberately**, start from your team's expertise or problems you've personally seen (Rezi, Vetcove), or do a systematic search like AtoB interviewing truck drivers at truck stops.

Bottom line: stack the deck with a promising idea, but the only way to know for sure is to launch and find out.""",
        ),
        quiz_lesson(
            "Quiz: How to Get and Evaluate Startup Ideas",
            (
                q(
                    'What is a "tar pit idea" as defined in the talk?',
                    (
                        opt("An idea in a heavily regulated industry that requires licenses"),
                        opt(
                            "A common, appealing idea that seems easy to solve but has structural reasons it's much harder than it looks",
                            correct=True,
                        ),
                        opt("An idea that requires large amounts of hardware capital"),
                        opt("An idea copied directly from an existing successful company"),
                    ),
                    "Tar pit ideas form around widespread problems that seem easily solvable, but a structural reason makes them very hard — like the app for making plans with friends applied to YC for around 20 years.",
                ),
                q(
                    "According to the talk, why can existing competitors actually be a good sign for a startup idea?",
                    (
                        opt(
                            "Because you can acquire the competitors later and consolidate the market"
                        ),
                        opt("Because competitors will validate your pricing for you"),
                        opt("Because markets with no competitors always take longer to regulate"),
                        opt(
                            "Because they suggest the problem is real — spaces with no competitors often mean nobody wants the product",
                            correct=True,
                        ),
                    ),
                    "Jared says founders who enter spaces with no competitors often discover no one wants the product; Dropbox launched as roughly the 20th cloud file storage company but won with an insight the others missed.",
                ),
                q(
                    "Which evaluation criterion does the speaker single out as probably the most important one?",
                    (
                        opt(
                            "Founder-market fit — whether you are the right team for the idea",
                            correct=True,
                        ),
                        opt("Having no existing competition in the market"),
                        opt("Whether the idea sounds fun to work on"),
                        opt("Whether the idea can be built in a weekend"),
                    ),
                    "Jared says if he had to pick the single most important criterion it would probably be founder-market fit, illustrated by PlanGrid's team of a construction expert plus a great developer.",
                ),
            ),
        ),
        _yt("Pick One Idea and Go Deep", "R56RJFZBasQ", "12 min"),
        _t(
            "Key ideas — Pick One Idea and Go Deep",
            "4 min",
            """# Key ideas — Pick One Idea and Go Deep

A YC partner gives a rubric for founders stuck juggling multiple startup ideas: stop overthinking, commit to one, and find out fast whether it works.

- **Don't overthink it.** There is no perfect idea discoverable in the abstract — you only learn what to build by making contact with reality and getting customer feedback — and you don't need a decade of domain experience to be "allowed" to start.
- **Burn the other boats.** Working on several ideas at once produces bad data; explicitly stop the other ideas, tell customers you've pivoted, and go deep with single-minded focus — like GovDash, which changed its name and narrative with each of five pivots before winning.
- **The depth test: could you run your customer's business?** Know their daily crises, what they lose when the problem hits, and what they'd pay — as if you could teach a class on the problem.
- **Good AI-era ideas sit at the edge of what models can do today**, barely working now but clearly improving as models get better.
- **Verticalize and sell the outcome.** Don't build software for insurers — be the insurer, like Corgi, which acquired an insurance carrier during its batch.
- **Aim at the most ambitious version**, since ambitious and modest ideas cost roughly the same effort.

Bottom line: the worst failure mode isn't being wrong — it's never committing deeply enough to any idea to learn anything.""",
        ),
        quiz_lesson(
            "Quiz: Pick One Idea and Go Deep",
            (
                q(
                    'In the talk, what does it mean to "burn the other boats" when picking a startup idea?',
                    (
                        opt("Delete your old codebases so you can't be tempted to reuse them"),
                        opt("Keep the other ideas running quietly in the background as a hedge"),
                        opt(
                            "Explicitly stop working on your other ideas and commit fully to the one you chose",
                            correct=True,
                        ),
                        opt("Sell or license your other ideas to fund the main one"),
                    ),
                    "The speaker says going deep starts with explicitly foreclosing your other options — stop working on them, tell customers you've pivoted, and commit with single-minded focus to the one idea.",
                ),
                q(
                    'What does the speaker mean when he says a good idea in the AI era should "verticalize"?',
                    (
                        opt(
                            "Sell the outcome itself — be the insurer or the bank, not just software for them",
                            correct=True,
                        ),
                        opt("Focus your marketing on a single vertical industry before expanding"),
                        opt("Build a vertically integrated hardware and software stack"),
                        opt("Organize the company into vertical teams that each own a feature"),
                    ),
                    "The talk defines verticalizing as ultimately selling an outcome — for example being the insurer or the bank rather than selling software to them — because software itself is becoming cheap while trust, licenses, and outcome ownership stay valuable.",
                ),
                q(
                    'What "high watermark" question does the speaker use to test whether a founder has really gone deep on an idea?',
                    (
                        opt("Have you talked to at least 20 potential customers?"),
                        opt(
                            "Could you actually run your customer's business if dropped into it tomorrow?",
                            correct=True,
                        ),
                        opt("Have you written a detailed business plan and financial model?"),
                        opt("Has the idea already attracted interest from investors?"),
                    ),
                    "The speaker's test is whether you could actually run your customer's business — knowing their daily crises, what unanswered calls cost them, and what they would pay — not just whether you've had some customer conversations.",
                ),
            ),
        ),
        _yt("Starting a Company? The Key Terms You Should Know", "wH3TKpALlw4", "18 min"),
        _t(
            "Key ideas — Starting a Company? The Key Terms You Should Know",
            "4 min",
            """# Key ideas — Startup Terms You Should Know

Dalton, managing partner at Y Combinator, defines the vocabulary first-time founders constantly hear — from MVP to ARR — with concrete examples of what each term really means.

- **MVP — 'viable' is the key word**: a product that works but is useless isn't viable; it must be useful enough to serve some purpose for a customer.
- **Funding terms**: a seed round is usually the first money of any consequence a startup raises; Series A/B/C rounds typically have a lead investor (traditionally ~20% ownership in an A) and may involve a board seat, while angels invest their own personal money in small checks.
- **SAFE vs convertible note**: a convertible note is a debt-like instrument that can carry interest and repayment terms; the SAFE, created at YC, is an alternative with fewer terms — always read the fine print.
- **Burn rate**: how much your bank account goes down each month (start with $1M, end with $900K, and your burn is $100K) — not watching it can kill your startup.
- **Product-market fit**: the point where getting more customers is no longer your biggest problem and your priorities shift to growth and scaling.
- **TAM and valuation are estimates, not facts**: TAM calculations can badly underestimate markets (Tesla, Uber grew theirs), and private valuations aren't liquid market prices.

Bottom line: these terms get thrown around loosely, so understand what each one precisely means — and always read the fine print.""",
        ),
        quiz_lesson(
            "Quiz: Starting a Company? The Key Terms You Should Know",
            (
                q(
                    "In Dalton's example, if you start the month with $1 million in the bank and end with $900,000, what is your burn rate?",
                    (
                        opt("$900,000 per month"),
                        opt("$100,000 per month", correct=True),
                        opt("$1 million per month"),
                        opt("10% of annual recurring revenue"),
                    ),
                    "He defines burn rate as how much your bank account goes down in a month, using exactly this example: $1M dropping to $900K means a $100K burn rate.",
                ),
                q(
                    "How does Dalton describe a startup that has reached product-market fit?",
                    (
                        opt("It has raised at least a Series A from a lead investor"),
                        opt("It has become profitable with stable margins"),
                        opt(
                            "Getting more customers is no longer its biggest problem — its priorities shift to growth and scaling",
                            correct=True,
                        ),
                        opt("It has completed an IPO on a public exchange"),
                    ),
                    "He explains that post-PMF, people are using and liking the product, and needing more customers is no longer the biggest problem — the challenges become scaling, performance, and serving as many people as possible.",
                ),
                q(
                    "According to Dalton, what is a key difference between a convertible note and a SAFE?",
                    (
                        opt("A SAFE can only be used in Series B rounds or later"),
                        opt(
                            "A convertible note was invented by Y Combinator, while the SAFE is a traditional bank instrument"
                        ),
                        opt("A convertible note gives investors no rights at all"),
                        opt(
                            "A convertible note is a debt-like instrument that may carry interest or repayment terms, while a SAFE has fewer terms to worry about",
                            correct=True,
                        ),
                    ),
                    "Dalton says convertible notes are debt-like, often with interest or repayment obligations, whereas the SAFE — created at YC by Carolyn Levy — is a simpler alternative with fewer terms and rights to worry about.",
                ),
            ),
        ),
        # ── Part 2 — Co-founders & team ─────────────────────────────
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
        quiz_lesson(
            "Quiz: Part 2 — Co-founders & team",
            (
                q(
                    "Where does co-founder conflict rank among startup killers?",
                    (
                        opt("It's rare and mostly harmless"),
                        opt("It only becomes a risk after Series A"),
                        opt(
                            "Among the top startup killers — ahead of most market risks",
                            correct=True,
                        ),
                        opt("It matters less than the choice of tech stack"),
                    ),
                    "Part 2 opens with exactly this: co-founder breakups kill more startups than most market risks do — which is why the people decisions get four talks.",
                ),
                q(
                    "When does Part 2 say you hire your first engineers and account executives?",
                    (
                        opt("Immediately upon incorporating the company"),
                        opt(
                            "Once something works — after the founders have found signal",
                            correct=True,
                        ),
                        opt("Before talking to any users"),
                        opt("Only after raising a Series B"),
                    ),
                    "The hiring playbook enters 'once something works' — after the founders have found signal, not at incorporation.",
                ),
            ),
        ),
        _yt("How To Find A Co-Founder", "Fk9BCr5pLTU", "21 min"),
        _t(
            "Key ideas — How To Find A Co-Founder",
            "4 min",
            """# Key ideas — How to Find a Co-Founder

Harj, a YC group partner, explains why you need a co-founder, what actually matters when choosing one, where to find them, and how to keep the relationship from breaking — the number one reason YC startups fail.

- **Why a co-founder**: more and better work gets done, you get emotional support through the startup roller coaster, and the most successful startups — Facebook (Zuckerberg and Moskovitz), Apple (Jobs and Wozniak) — had co-founding teams.
- **The single-founder exception**: only if you have a specific idea you're uniquely qualified for AND you're an engineer who can build it — like Drew Houston, who kept building Dropbox while searching for a co-founder.
- **The most important trait is handling stress well**, and the best way to know is having worked with someone under stress before — friendship alone isn't proof.
- **Align on high-level goals early**: a founder chasing a fast-growing venture-backed company won't fit with one who wants a steady lifestyle business.
- **Always make the ask**: never assume people you know are unavailable, and branch out through projects, hackathons, open source, and the YC co-founder matching platform.
- **Protect the relationship**: split equity equally, don't delay hard conversations, and hold regular one-on-ones to release pressure before it builds up.

Bottom line: find someone you've genuinely worked with, align on goals upfront, and keep investing in the relationship.""",
        ),
        quiz_lesson(
            "Quiz: How To Find A Co-Founder",
            (
                q(
                    "What does Harj say is the most important quality to look for in a co-founder?",
                    (
                        opt("Expertise in a specific programming language"),
                        opt(
                            "That they handle stress well — ideally proven by having worked with them under stress before",
                            correct=True,
                        ),
                        opt("A large professional network for fundraising"),
                        opt("Prior experience as a CEO at another startup"),
                    ),
                    "He calls handling stress well the most important trait — even perfect complementary skills won't save a relationship that can't survive startup stress, which is why failed co-founder relationships are the top reason YC startups fail.",
                ),
                q(
                    "What is Harj's default advice on splitting equity between co-founders?",
                    (
                        opt("The person who had the idea should keep a majority stake"),
                        opt("The CEO should always hold at least 60%"),
                        opt("Base the split precisely on months of work done so far"),
                        opt(
                            "Split it equally, since early differences in work are insignificant over a 10+ year journey",
                            correct=True,
                        ),
                    ),
                    "He advises an equal split: if the startup succeeds you'll work on it for 10 years or more, so early differences in idea or effort are insignificant, and equal ownership keeps both founders equally invested.",
                ),
                q(
                    "What does Harj tell founders who claim everyone they know is unavailable to co-found?",
                    (
                        opt(
                            "Never assume availability — always make the ask, and if they decline, ask who they would pick and get an introduction",
                            correct=True,
                        ),
                        opt("Wait a year until friends leave their jobs at big companies"),
                        opt("Hire an employee first and promote them to co-founder later"),
                        opt("Start the company alone since co-founders rarely matter"),
                    ),
                    "His number one advice is that you can never assume who's available: get in the habit of asking directly, and if someone says no, ask who they'd choose as a co-founder and request an intro to branch beyond your network.",
                ),
            ),
        ),
        _yt("Keys To Successful Co-Founder Relationships", "A4SLDQDXdp0", "32 min"),
        _t(
            "Key ideas — Keys To Successful Co-Founder Relationships",
            "4 min",
            """# Key ideas — Keys To Successful Co-Founder Relationships

Two YC speakers cover why co-founders matter, how to find and evaluate one, and how to work together for the long haul.

- **Co-founders dramatically improve your odds**: they add productivity, better brainstorming, accountability, and moral support. Of YC's top 100 companies, only four had a solo founder — though YC does fund solo founders.
- **Find people through your network or YC's co-founder matching**: the platform has 40,000 profiles and passed 100,000 matches; a structured trial project (two to four weeks, defined goal and ownership) is the best way to test the working relationship.
- **Align early on the hard topics**: goals and values, handling stress, communication style, finances (how long each can go without salary), and commitment — unspoken mismatches on timelines and money broke up real founding teams in the talk.
- **Split equity equally by default**: ideas are cheap and all the work is ahead of you; getting a "good deal" off your co-founder breeds resentment.
- **If you're non-technical, don't hire a dev shop**: learn to code or find a technical co-founder — dev shops are costly and can't iterate as you learn from users.
- **Trust and structure keep decisions fast**: trust by default, create space for mistakes, name one CEO (no consensus-on-everything), define ownership areas, hold regular one-on-ones, and disagree and commit.

Bottom line: treat the co-founder relationship like a marriage — chosen carefully, aligned early, and maintained with honest communication.""",
        ),
        quiz_lesson(
            "Quiz: Keys To Successful Co-Founder Relationships",
            (
                q(
                    "What is YC's default advice on splitting equity between co-founders?",
                    (
                        opt(
                            "Split it equally, because ideas are cheap and all the work is still ahead of you",
                            correct=True,
                        ),
                        opt("Give the person who had the idea a significantly larger share"),
                        opt("Give the CEO extra equity so they can break ties"),
                        opt(
                            "Base the split on who worked on the idea longest before the other joined"
                        ),
                    ),
                    "The talk says to split equally by default: the idea is likely to change, both founders must stay motivated for 7-10+ years, and 'getting a good deal' from a co-founder starts the relationship badly.",
                ),
                q(
                    "What does the talk advise a non-technical founder who can't find a technical co-founder?",
                    (
                        opt("Hire a dev shop to build the MVP quickly"),
                        opt("Learn how to code rather than outsourcing the product", correct=True),
                        opt("Raise money first and hire engineers with it"),
                        opt("Pivot to a business that requires no software"),
                    ),
                    "The speakers say 'please don't' hire a dev shop — dev shops are costly, can't iterate as requirements change, and don't care about your users; if you truly can't find a technical co-founder, learn to code.",
                ),
                q(
                    "What went wrong at the speaker's first startup, which had four co-founders and no titles?",
                    (
                        opt("The equity split was unequal, causing lawsuits"),
                        opt("They gave one founder too much unilateral power"),
                        opt(
                            "They tried to make every decision by consensus and got stuck in gridlock",
                            correct=True,
                        ),
                        opt("They spent too much on an interpersonal coach"),
                    ),
                    "With no titles and consensus decision-making, the team 'would just spin' and get stuck in gridlock — a sign they couldn't have hard conversations; the fix is naming one CEO and clear areas of ownership.",
                ),
            ),
        ),
        _yt("Co-Founder Equity Mistakes to Avoid", "DISocTmEwiI", "20 min"),
        _t(
            "Key ideas — Co-Founder Equity Mistakes to Avoid",
            "4 min",
            """# Key ideas — Co-Founder Equity Splits

Michael Seibel shares YC's advice on splitting equity at the very start of a VC-track software startup, and on handling co-founder breakups before product-market fit.

- **Be generous and split near-equally**: equity's job is to keep co-founders motivated through years when things look like they're failing; being stingy breeds resentment and departures.
- **Equity motivates future work**: when you split, almost all the work is still ahead — equity rewards what hasn't been done yet, not the idea or a six-month head start.
- **Always use vesting and cliffs**: the standard is four-year vesting with a one-year cliff, for every founder — that is your downside protection, not fancy formulas.
- **Plan the breakup in advance**: pre-product-market fit, a founder who leaves before the cliff gets only a token amount; after the cliff, YC recommends keeping no more than 5%, resigning from the board, signing a release, and giving proxy voting rights to the remaining founders.
- **Reject bad reasons for unequal splits**: "my co-founder agreed," "it was my idea," "I started earlier," "I'm more experienced," and "I raised the money" are all short-term thinking — ideas are a dime a dozen and execution is the game.
- **Avoid performance-based or dynamic equity**: equity distribution is not the place to innovate.

Bottom line: treat equity as a tool for producing maximum motivation in a small team, not as something to hoard.""",
        ),
        quiz_lesson(
            "Quiz: Co-Founder Equity Mistakes to Avoid",
            (
                q(
                    "What is YC's core advice on co-founder equity splits at the start of a company?",
                    (
                        opt("The CEO should keep a large majority to maintain control"),
                        opt("Be generous and aim for close-to-equal splits", correct=True),
                        opt("Split in proportion to how many months each founder has worked"),
                        opt("Tie each founder's split to measurable performance goals"),
                    ),
                    "The talk's TLDR is to be generous with co-founder equity — close-to-equal splits keep strong founders motivated through the hard early years.",
                ),
                q(
                    "What vesting structure does the talk describe as the standard best practice for founder equity?",
                    (
                        opt("Two-year vesting with no cliff"),
                        opt("Immediate full ownership with a company buyback clause"),
                        opt("Vesting that applies only to non-CEO founders"),
                        opt("Four-year vesting with a one-year cliff", correct=True),
                    ),
                    "The speaker says what's extremely typical is earning your stock over four years with a one-year cliff, and that vesting and cliffs should apply to all founders.",
                ),
                q(
                    "Per the talk, how much equity should a departing founder keep if they leave after their one-year cliff but before product-market fit?",
                    (
                        opt("No more than 5% of the company", correct=True),
                        opt("Everything they have vested so far"),
                        opt("Exactly half of their original grant"),
                        opt("25%, matching an equal four-founder split"),
                    ),
                    "YC's guideline is that pre-product-market fit, a founder who leaves after the cliff should retain no more than 5%, freeing equity to motivate the people still building the company.",
                ),
            ),
        ),
        _yt(
            "The Startup Playbook for Hiring Your First Engineers and AEs", "i_PjjXKNpA4", "43 min"
        ),
        _t(
            "Key ideas — The Startup Playbook for Hiring Your First Engineers and AEs",
            "4 min",
            """# Key ideas — Hiring Your First Engineers and AEs

The co-founder and CEO of Juicebox, an AI sourcing platform, shares a playbook for sourcing and closing a startup's first engineering and sales hires.

- **Early hires define the company.** Culture is set by the first 10 people (and the next 40), so treat who you hire with as much care as speed.
- **Know which bucket a candidate leans toward** — big tech, growth stage, or startup — and only fight hard for those who genuinely want startup impact, ownership, and high-variance equity upside.
- **Sourcing is outbound sales.** The best candidates aren't applying; proactively find them via referrals (with 10-20K bonuses), targeted search signals like President's Club and quota attainment for AEs, or personal projects and open-source work for engineers.
- **Personalized, multi-step outreach wins.** Email is the default channel because it can be automated and measured; a 10-20% reply rate is good, and the interested rate matters more than raw replies. Founders — ideally the technical founder for engineers — should send the outreach.
- **Sell first, interview second.** The number-one founder mistake is jumping into interview questions instead of opening the first call by selling the company.
- **Make it a scheduled habit:** roughly 100 outreach emails and 10 candidate conversations weekly, every founder involved, and use your speed — a 7-14 day process — to beat slower companies to the offer.

Bottom line: recruit the way you sell — personalized, founder-led, relentlessly consistent.""",
        ),
        quiz_lesson(
            "Quiz: The Startup Playbook for Hiring Your First Engineers and AEs",
            (
                q(
                    "What does David identify as the number-one mistake founders make in the first interview call?",
                    (
                        opt(
                            "Making the interview process too long and losing candidates to slower companies"
                        ),
                        opt(
                            "Interviewing the candidate right away instead of first selling the company",
                            correct=True,
                        ),
                        opt("Offering too much equity before assessing the candidate"),
                        opt("Letting a recruiter run the call instead of joining personally"),
                    ),
                    "He says founders skip straight into interviewing the candidate with generic questions; the order should be flipped — sell the company first, then interview.",
                ),
                q(
                    "Why does David recommend email as the default channel for candidate outreach?",
                    (
                        opt("Because candidates check email more often than any other channel"),
                        opt("Because LinkedIn bans all recruiting messages from startups"),
                        opt("Because email is the only channel where engineers ever respond"),
                        opt(
                            "Because email can be automated into multi-step campaigns and measured with real data like reply rates",
                            correct=True,
                        ),
                    ),
                    "He explains that email can be automated into multi-step campaigns and gives real data like reply and open rates, whereas LinkedIn steps must be done manually — so a sequenced email campaign beats a single LinkedIn message.",
                ),
                q(
                    "According to the talk, what does it mean if you are not getting to at least 10 candidate conversations per week?",
                    (
                        opt(
                            "You are probably not sending enough outreach and should scale it up",
                            correct=True,
                        ),
                        opt(
                            "Your job description is too opinionated and is scaring candidates away"
                        ),
                        opt("You should immediately hire a contingency recruiter to fill the gap"),
                        opt("Your compensation packages are below market and need to be raised"),
                    ),
                    "David sets 10 candidate conversations per week as the goal and says falling short is probably a sign you're not doing enough outreach — so scale up to 150 or 200 emails per week.",
                ),
            ),
        ),
        # ── Part 3 — Building with AI ───────────────────────────────
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
        quiz_lesson(
            "Quiz: Part 3 — Building with AI",
            (
                q(
                    "Why do services businesses become venture-scale in the AI era?",
                    (
                        opt("Because services can finally bill by the hour"),
                        opt("Because venture investors lowered their return targets"),
                        opt("Because services companies need no distribution"),
                        opt(
                            "Because agents do the delivery, so revenue stops being tied to headcount",
                            correct=True,
                        ),
                    ),
                    "Long dismissed by venture investors, services turn venture-scale when agents do the delivery — revenue stops being tied to headcount.",
                ),
                q(
                    "What risk does Part 3 flag with vibe coding?",
                    (
                        opt(
                            "Drowning in unreviewed generated code instead of getting real leverage",
                            correct=True,
                        ),
                        opt("AI-generated code is always insecure"),
                        opt("Vibe coding is slower than writing by hand"),
                        opt("It only works for throwaway prototypes"),
                    ),
                    "The point of the vibe-coding talk: real leverage requires structure and review — otherwise you drown in unreviewed generated code.",
                ),
            ),
        ),
        _yt("How To Build A Company With AI From The Ground Up", "EN7frwQIbKc", "10 min"),
        _t(
            "Key ideas — How To Build A Company With AI From The Ground Up",
            "4 min",
            """# Key ideas — Building an AI-Native Company From the Ground Up

A YC partner argues that AI is not just a productivity boost but a new set of capabilities that should reshape how startups are structured and run from day one.

- **AI should be the operating system, not a tool.** Every workflow, decision, and process should flow through an intelligent layer that is constantly learning and improving.
- **Run the company as a closed loop.** Unlike old open-loop companies that rarely measured outcomes, a closed loop continuously captures results and feeds them back into the intelligence layer to self-correct.
- **Make the whole organization queryable.** Record meetings with AI note-takers, minimize DMs and email, embed agents in communication channels, and build dashboards covering everything — give models as much context as you would give an employee.
- **Adopt AI software factories.** Humans write the spec and the tests that define success; agents generate and iterate on the code — some companies' repos contain no hand-written code at all.
- **Remove human middleware.** With a queryable company, classic middle-management routing disappears; Jack Dorsey's three archetypes remain — the IC builder, the DRI who owns one outcome, and the AI-founder type leading from the front.
- **Token-max instead of headcount-max.** Accept an uncomfortably high API bill, because it replaces far more expensive teams.

Bottom line: early-stage founders have no legacy systems to unwind, so they can build AI-native from day one and move far faster than incumbents.""",
        ),
        quiz_lesson(
            "Quiz: How To Build A Company With AI From The Ground Up",
            (
                q(
                    'In the talk, what distinguishes a "closed loop" company from the old "open loop" way of operating?',
                    (
                        opt(
                            "It continuously captures outcomes and feeds them back into an intelligent system that improves the process over time",
                            correct=True,
                        ),
                        opt(
                            "It keeps all company information confidential inside a closed internal network"
                        ),
                        opt(
                            "It locks the product roadmap at the start of each year to avoid churn"
                        ),
                        opt("It routes every decision through a single manager for consistency"),
                    ),
                    "The speaker contrasts open loops — decisions executed without systematically measuring outcomes — with closed loops that continuously capture outputs and feed them back into the intelligence layer so processes self-improve.",
                ),
                q(
                    'In an "AI software factory" as described in the talk, what is the human\'s role?',
                    (
                        opt("Writing all the production code while agents handle testing"),
                        opt("Reviewing every line of agent-generated code before merge"),
                        opt(
                            "Writing the spec and tests that define success, then judging the output while agents write the code",
                            correct=True,
                        ),
                        opt("Managing a large team of engineers who supervise the agents"),
                    ),
                    "The talk says humans write a spec and a set of tests that define success and judge the output, while AI agents generate the implementation and iterate until the tests pass.",
                ),
                q(
                    'What does the speaker mean by companies that are "token maxing"?',
                    (
                        opt("Minimizing API spend by caching and compressing prompts"),
                        opt("Issuing crypto tokens to align employee incentives"),
                        opt("Hiring as many engineers as possible to maximize output"),
                        opt(
                            "Willingly running a very high AI API bill instead of growing headcount, since one person with AI tools can replace a large team",
                            correct=True,
                        ),
                    ),
                    "The talk says the critical shift is maximizing token usage rather than headcount — being willing to run an uncomfortably high API bill because it replaces a far more expensive, inflated team.",
                ),
            ),
        ),
        _yt("How to Build an AI-Native Services Company", "gSNFJbgoaHI", "11 min"),
        _t(
            "Key ideas — How to Build an AI-Native Services Company",
            "4 min",
            """# Key ideas — Building an AI-Native Services Company

This talk lays out YC's playbook for founders starting AI-native services companies — businesses like insurance carriers or law firms rebuilt from scratch with AI doing most of the work, selling the outcome rather than a co-pilot.

- **Pick markets with four traits:** low trust (work already outsourced, customer cares about the result), low judgment at the task level so most steps automate, a high intelligence threshold so the work is genuinely hard, and regulation — which raises the bar and the moat.
- **Apply the "Sam Altman test":** as models get better, does your service get stronger, or does the model commoditize you? You want the first camp.
- **The founding team needs three fluencies:** domain fluency (credibility with skeptical buyers), model fluency (design to ride the model curve), and operational rigor — the product is an operation.
- **Variance is the existential problem.** Customers fire you for inconsistent output faster than for being slower or pricier; humans in the loop must scale non-linearly with revenue.
- **Avoid the early demand trap:** cap pilots to a small handful, sell outcomes not seats, and price per unit or per outcome — never cost-plus or straight-line undercutting.
- **Don't buy your way in.** Acquiring a legacy services firm rarely works, except when you need a regulatory moat fast.

Bottom line: treat the process as the product and chase AI operating leverage toward software-like margins in markets far bigger than software.""",
        ),
        quiz_lesson(
            "Quiz: How to Build an AI-Native Services Company",
            (
                q(
                    'What is the "Sam Altman test" described in the talk?',
                    (
                        opt("Whether your startup could survive without any venture funding"),
                        opt(
                            "Whether a customer would be upset if your product disappeared tomorrow"
                        ),
                        opt("Whether your team could ship a working demo within one week"),
                        opt(
                            "Whether improving models make your service stronger or commoditize it",
                            correct=True,
                        ),
                    ),
                    "The speaker says founders should ask whether, as the models get better, their service gets stronger or the model itself commoditizes them — and you want to be in the first camp.",
                ),
                q(
                    'According to the talk, what is the "early demand trap" for AI services companies?',
                    (
                        opt("Building product features before any customer has asked for them"),
                        opt(
                            "Signing so many pilot customers that serving them with humans prevents you from building the product to scale",
                            correct=True,
                        ),
                        opt("Raising prices too early and scaring away initial customers"),
                        opt("Hiring salespeople before the product has product-market fit"),
                    ),
                    "The talk warns that it's easy to sign many pilot customers early, which overwhelms your ability to serve them and blocks building a scalable product — so cap your first pilots to a small handful.",
                ),
                q(
                    "Which pricing strategy does the speaker explicitly say to avoid?",
                    (
                        opt("Per-unit pricing, such as per return, per claim, or per loan"),
                        opt("Outcome-based pricing that aligns incentives with the customer"),
                        opt(
                            "Cost-plus pricing, because it captures your upside permanently",
                            correct=True,
                        ),
                        opt("Pricing on value relative to the cost of labor"),
                    ),
                    "The talk endorses per-unit and outcome-based pricing but names cost-plus pricing (which permanently caps your upside) and straight-line undercutting as the two strategies to avoid.",
                ),
            ),
        ),
        _yt("How To Get The Most Out Of Vibe Coding", "BJjsfNO5JTo", "17 min"),
        _t(
            "Key ideas — How To Get The Most Out Of Vibe Coding",
            "4 min",
            """# Key ideas — Getting the Most Out of Vibe Coding

Tom, a YC partner, spent a month vibe coding side projects and found it's a practice you can measurably improve at — and the best techniques are the same processes a professional software engineer would use.

- **Plan before coding**: work with the LLM to write a comprehensive plan in a markdown file, then implement it section by section, marking each section complete rather than trying to one-shot the product.
- **Use Git religiously**: start each feature from a clean slate and don't hesitate to reset and retry — repeated prompting on a broken attempt accumulates layers of bad code instead of fixing root causes.
- **Write high-level integration tests**: they catch the LLM's habit of making unnecessary changes to unrelated logic, so you know when to reset.
- **For bugs, paste the exact error message**: it's often enough on its own; for gnarly bugs, ask the LLM to consider multiple causes, add logging, and switch models if stuck.
- **Pick a stack with training data**: Ruby on Rails worked remarkably well because 20 years of conventions mean consistent training data, while friends had less success with Rust or Elixir.
- **LLMs aren't just for code**: use them as your DevOps engineer, designer, and teacher, and try screenshots and voice input to work faster.

Bottom line: treat the AI like a new kind of programming language and hold it to the disciplined processes of a good professional developer.""",
        ),
        quiz_lesson(
            "Quiz: How To Get The Most Out Of Vibe Coding",
            (
                q(
                    "What does the speaker recommend doing FIRST after picking a vibe coding tool?",
                    (
                        opt("Immediately prompt the tool to one-shot the entire product"),
                        opt(
                            "Work with the LLM to write a comprehensive plan in a markdown file, then implement it section by section",
                            correct=True,
                        ),
                        opt("Set up an MCP server to access online documentation"),
                        opt("Hire a professional developer to review the codebase"),
                    ),
                    "He says the first step is not to write code but to create a plan with the AI, keep it in a markdown file in the project, and step through it piece by piece, committing working sections to Git.",
                ),
                q(
                    "When the LLM repeatedly fails to fix a bug, what does the speaker advise?",
                    (
                        opt("Keep prompting the same model until it eventually succeeds"),
                        opt("Manually rewrite the whole feature yourself without the AI"),
                        opt("Delete the tests so the failing checks stop blocking progress"),
                        opt(
                            "Git reset to a clean state, add logging, and try again — possibly with a different model",
                            correct=True,
                        ),
                    ),
                    "He warns that repeated fix attempts layer 'crap' on top of bad code; instead you should reset, add logging, and switch models, then apply the eventual solution to a clean codebase.",
                ),
                q(
                    "Why did the speaker get such good AI results with Ruby on Rails?",
                    (
                        opt(
                            "Rails is a 20-year-old framework with well-established conventions, so there's lots of consistent, high-quality training data",
                            correct=True,
                        ),
                        opt("Rails is the only framework the AI tools officially support"),
                        opt("Rails apps don't require any tests, which makes generation simpler"),
                        opt(
                            "Rails code runs faster, so the AI can evaluate its output more quickly"
                        ),
                    ),
                    "He attributes the strong performance to Rails' age and conventions — many Rails codebases look similar, giving models tons of consistent training data, unlike newer or rarer languages such as Rust or Elixir.",
                ),
            ),
        ),
        _yt("Tips For Technical Startup Founders", "rP7bpYsfa6Q", "28 min"),
        _t(
            "Key ideas — Tips For Technical Startup Founders",
            "4 min",
            """# Key ideas — Tips for Technical Startup Founders

Diana, a YC group partner and former startup CTO, explains what a technical founder actually does and how to build at each early stage.

- **A technical founder is a partner, not "someone to build my app"**: they do all the tech — front end, back end, DevOps, even IT — while also talking to users, biased toward good-enough over perfect architecture.
- **Ideating stage: build a prototype in days**, using Figma mockups, quick scripts, or 3D renderings — Optimizely's first visual editor was a JavaScript file only the founders could run, yet it excited marketers.
- **MVP stage: launch in weeks and do things that don't scale** — Stripe's founders manually filled in bank forms to process payments; DoorDash launched in an afternoon with a static page, Google Forms as the "back end," and Find My Friends tracking deliveries.
- **Build a 90/10 solution**: not buggy code, but a product restricted to limited dimensions (users, data types, geography) — DoorDash's Palo Alto-only focus helped it nail suburban delivery economics early.
- **Choose your stack for iteration speed** and lean on third-party tools; the only tech choices that truly matter are the ones tied to your customer promises.
- **After launch, iterate with hard and soft data**, keep launching (Segment shipped five launches in a month), and accept tech debt — Pokémon Go's broken login didn't kill it.

Bottom line: at every stage, the technical founder's job is to move quickly.""",
        ),
        quiz_lesson(
            "Quiz: Tips For Technical Startup Founders",
            (
                q(
                    "What did DoorDash use as its 'back end' when it first launched as Palo Alto Delivery?",
                    (
                        opt(
                            "Google Forms and Google Docs, with Find My Friends used to track deliveries",
                            correct=True,
                        ),
                        opt("A custom Django application deployed on Heroku"),
                        opt("A scalable microservices architecture on Kubernetes"),
                        opt(
                            "A PHP order-management dashboard the founders wrote over several months"
                        ),
                    ),
                    "The talk describes a static HTML/CSS page with PDF menus and a founder's phone number, with Google Forms and Google Docs coordinating orders and Find My Friends on iPhone tracking deliveries — assembled in one afternoon.",
                ),
                q(
                    "Why does the speaker discourage hiring engineers to build the MVP before launch?",
                    (
                        opt("Engineers are too expensive before a seed round"),
                        opt(
                            "Hiring takes over a month and slows you down, and founders miss key insights about their own product when others build it",
                            correct=True,
                        ),
                        opt("YC rules prohibit startups from hiring before launch"),
                        opt("Early employees always demand too much equity"),
                    ),
                    "She explains that finding someone good takes over a month, which slows the launch, and — more insidiously — if someone other than the founders builds the product, the founders miss key learnings and insights about their own tech.",
                ),
                q(
                    "In this talk, what does building a '90/10 solution' mean?",
                    (
                        opt("Shipping with 90% of features working and 10% of them buggy"),
                        opt("Spending 90% of the time on architecture and 10% on features"),
                        opt("Building 90% of the full product vision before showing it to anyone"),
                        opt(
                            "Restricting the product to limited dimensions (users, data, geography) so you can launch quickly — without shipping bugs",
                            correct=True,
                        ),
                    ),
                    "Diana clarifies that a 90/10 solution doesn't mean creating bugs — it means restricting the product to work on limited dimensions (type of users, data, functionality, or geography) so you can launch quickly.",
                ),
            ),
        ),
        _yt("How to Build An MVP", "QRZ_l7cVzzU", "17 min"),
        _t(
            "Key ideas — How to Build An MVP",
            "4 min",
            """# Key ideas — How to Build An MVP

The smartest move for an early founder is also the simplest: launch quickly and iterate, instead of researching and polishing for a year.

- **Learning starts when users touch the product**: surveys and interviews reveal the pain, but customers are experts in their problem, not the solution — only putting an MVP in front of them starts the real conversation.
- **Early adopters tolerate rough products**: they have a real problem and try new software anyway. In the "hair on fire" analogy, a desperate customer will use your brick — an imperfect solution.
- **Don't be a "fake Steve Jobs"**: even Apple iterated. The first iPhone had no App Store, no video recording, and only 2G internet; great products emerge from iteration, not a perfect first release.
- **Famous MVPs were tiny**: Airbnb launched with no payments, no map view, air beds only, and only worked for conferences; Twitch was one page streaming one person; Stripe's first version was so bare-bones only early YC startups could use it.
- **Ship fast with discipline**: set a specific deadline, write down the spec, cut every feature a desperate customer doesn't need, and don't fall in love with your MVP — fall in love with the customer.

Bottom line: it's far better to have a hundred people who love your product than a hundred thousand who kind of like it, and a fast, imperfect MVP is how you get there.""",
        ),
        quiz_lesson(
            "Quiz: How to Build An MVP",
            (
                q(
                    "In the 'hair on fire' analogy, what does the brick represent?",
                    (
                        opt("A distraction that founders should never offer customers"),
                        opt("The perfect, polished product every customer really wants"),
                        opt("A competitor's product that steals your desperate customers"),
                        opt(
                            "An imperfect MVP that a desperate customer will still use because their problem is urgent",
                            correct=True,
                        ),
                    ),
                    "The speaker says a person whose hair is on fire would buy a brick and smother the fire with it — customers in enough pain will use a non-perfect solution, and those are the customers to target first.",
                ),
                q(
                    "How does the talk use the first iPhone to argue against waiting to build a 'perfect' product?",
                    (
                        opt(
                            "The first iPhone shipped without an App Store, without video recording, and with only 2G internet — even Steve Jobs iterated",
                            correct=True,
                        ),
                        opt(
                            "The iPhone was perfect on day one, proving visionaries can skip iteration"
                        ),
                        opt("Apple ran 600 user interviews before writing any code"),
                        opt("The iPhone succeeded only because Apple spent a decade in stealth"),
                    ),
                    "The talk calls founders who think they can envision the perfect product 'fake Steve Jobs' and points out the iPhone people remember was really the third or fourth iteration.",
                ),
                q(
                    "Why does the speaker say surveys can't replace launching an MVP?",
                    (
                        opt("Because surveys are too expensive for early-stage startups"),
                        opt(
                            "Because customers are experts in their problem but not in how to solve it — that's the founder's job",
                            correct=True,
                        ),
                        opt("Because customers always lie in surveys"),
                        opt("Because investors refuse to fund companies that run surveys"),
                    ),
                    "Per the talk, surveys can help you understand the customer's pain, but the conversation about the solution only starts when you put a product — even a crappy MVP — in front of them.",
                ),
            ),
        ),
        _yt("How To Talk To Users", "z1iF1c8w5Lg", "18 min"),
        _t(
            "Key ideas — How To Talk To Users",
            "4 min",
            """# Key ideas — How to Talk to Users

YC group partner Gustaf, an early Airbnb employee, walks through how founders should interview users before and after building anything.

- **The best founders talk to users throughout the life of the company** — Airbnb's Brian Chesky lived in 50 different Airbnbs so he could talk with hosts every day, and the founders put their personal phone numbers on the website.
- **Find users** through your network, co-workers, LinkedIn, Reddit, Slack or Discord communities, and in-person events; interview them live over video, phone, or in person rather than surveys.
- **Don't introduce your idea** until the end of the call, or at all — doing it early biases the answers. Your role is to listen, using open-ended follow-ups like "tell me more about that."
- **Ask about problems, not features**: how do you do X today, what's hardest, why, how often, and why it matters. Avoid "Will you use our product?", feature wish lists, yes/no questions, and double questions.
- **Users have good problems but bad solutions** — early Gmail users asked to see inbox and email together only because Gmail was slow — so extract the problem and design the solution yourself.
- **Test value before building**: check whether people already pay for solutions, watch users click through a prototype without coaching them, and keep early interviewees involved in a group.

Bottom line: deeply understanding user problems through unbiased conversations is what turns a hypothesis into the right MVP.""",
        ),
        quiz_lesson(
            "Quiz: How To Talk To Users",
            (
                q(
                    "Why did Airbnb CEO Brian Chesky give up his apartment and live in 50 different Airbnbs?",
                    (
                        opt("To save money while the company was low on cash"),
                        opt("To generate press coverage for a fundraising round"),
                        opt(
                            "To talk to each host directly and get honest feedback on the product every day",
                            correct=True,
                        ),
                        opt("To secretly evaluate competitors' rental listings"),
                    ),
                    "Gustaf explains that the experiment gave Brian the chance to talk to every one of those 50 hosts each day, an incredible source of honest product feedback.",
                ),
                q(
                    "According to the talk, when should you introduce your own product idea during a user interview?",
                    (
                        opt(
                            "Near the end of the call, or not at all, to avoid biasing the answers",
                            correct=True,
                        ),
                        opt("At the very start, so the user knows the context"),
                        opt("Right after building rapport, before asking questions"),
                        opt("Only in written follow-ups, never on a live call"),
                    ),
                    "Gustaf says introducing your idea too early can bias interviewees; your role is to listen, so hold the pitch until the end or skip it entirely.",
                ),
                q(
                    "Which of these is one of the recommended interview questions from the talk?",
                    (
                        opt('"Will you use our product?"'),
                        opt('"Which features would make our product better?"'),
                        opt('"How would a better version of this product look to you?"'),
                        opt('"Tell me how you do X today."', correct=True),
                    ),
                    '"Tell me how you do X today" is the first of Gustaf\'s suggested questions; the other three are explicitly listed as questions NOT to ask because they invite biased or unhelpful answers.',
                ),
            ),
        ),
        # ── Part 4 — Launch & first customers ───────────────────────
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
        quiz_lesson(
            "Quiz: Part 4 — Launch & first customers",
            (
                q(
                    "When should your startup launch for the first time?",
                    (
                        opt("Once the product feels perfect"),
                        opt("Early — and then keep launching repeatedly", correct=True),
                        opt("Only alongside a fundraise announcement"),
                        opt("After hiring a PR agency"),
                    ),
                    "Launching is not a one-time press event — launch early, keep launching, and remember almost nobody but you remembers your launch.",
                ),
                q(
                    "How does Part 4 tell you to recruit your earliest users?",
                    (
                        opt("Through paid acquisition from day one"),
                        opt("By waiting for organic search traffic to compound"),
                        opt("By hand, one at a time — doing things that don't scale", correct=True),
                        opt("By listing on app marketplaces and waiting"),
                    ),
                    "The classic YC counsel — do things that don't scale: recruit users by hand, one at a time, and learn from every conversation.",
                ),
            ),
        ),
        _yt("The Best Way To Launch Your Startup", "u36A-YTxiOw", "21 min"),
        _t(
            "Key ideas — The Best Way To Launch Your Startup",
            "4 min",
            """# Key ideas — The Best Way To Launch Your Startup

YC's head of Outreach argues that launching isn't one perfect moment — it's something you do continually, starting as soon as possible.

- **Launch ASAP, then launch again**: the worst case is that nobody cares, and the answer is to iterate and relaunch — Airbnb launched three times before it got real users.
- **A few users who love you beats many who are lukewarm**: per Gmail creator Paul Buchheit, make a few people really happy rather than many semi-happy; even 10 users who love you is a foundation to expand.
- **Lead with what, not why**: your one-liner should say plainly what you do and for whom (like Pave's compensation-tools description), with no backstory, no rambling, and no jargon like "know-how and synergy platform."
- **Use "X for Y" only carefully**: X must be a household name, it must be clear why Y wants X, and Y must be a huge market.
- **There are many launch types**: silent launch (a simple landing page with a call to action), friends and family, strangers (DoorDash interviewed ~200 small business owners), online communities like Hacker News — where a random post got Robinhood 10,000 waitlist signups in one day — plus pre-orders.
- **Don't count on press**: it's hard to land early and isn't a scalable path to users or product-market fit.

Bottom line: stop treating launch as a single shot — ship, learn, and launch again and again.""",
        ),
        quiz_lesson(
            "Quiz: The Best Way To Launch Your Startup",
            (
                q(
                    "What is the talk's core advice about when and how often to launch?",
                    (
                        opt(
                            "Wait until the product and messaging are perfect, because you only get one shot"
                        ),
                        opt("Launch only after raising at least $1M so press will cover you"),
                        opt(
                            "Launch as soon as possible and keep launching continually, iterating each time",
                            correct=True,
                        ),
                        opt("Launch once a year, timed to a major tech conference"),
                    ),
                    "The speaker says most founders overthink a single launch; you should launch ASAP, and if no one cares, iterate and launch again — as Airbnb did three times.",
                ),
                q(
                    "According to the talk, how should a strong one-line company description start?",
                    (
                        opt("With the company name and what it does, stated plainly", correct=True),
                        opt("With the founder's personal story of discovering the problem"),
                        opt("With ambitious language about changing the world"),
                        opt("With the technology stack, such as 'ML-driven platform'"),
                    ),
                    "The talk says to lead with what, not why: give context up front with the name and what you do, avoid jargon and marketing speak, and save the backstory for follow-up questions.",
                ),
                q(
                    "What happened when Robinhood's simple waitlist page was posted to Hacker News?",
                    (
                        opt("It was ignored because the site was too simple"),
                        opt("Investors forced them to take the page down before launch"),
                        opt(
                            "They converted every waitlist signup into a paying customer that week"
                        ),
                        opt(
                            "It hit number one and they got 10,000 signups the first day, over 50,000 within a week",
                            correct=True,
                        ),
                    ),
                    "Someone randomly posted Robinhood's commission-free-trading waitlist page on Hacker News; it reached number one and drove 10,000 signups on day one and 50,000+ over the next week.",
                ),
            ),
        ),
        _yt("How to Get Your First Customers", "hyYCn_kAngI", "23 min"),
        _t(
            "Key ideas — How to Get Your First Customers",
            "4 min",
            """# Key ideas — How to Get Your First Customers

YC group partner Gustav explains how founders close their first paying customers by doing things that don't scale.

- **Founders make startups take off**: you must manually recruit your first customers, as Paul Graham's 'Do Things That Don't Scale' essay and Airbnb show; writing more code is a common way to avoid this.
- **Founders should do sales themselves**: don't hire a sales team until you know how to sell your own product — only then do you know what good looks like.
- **Write short, plain sales emails**: six to eight sentences, no jargon, no HTML, address the customer's problem, add social proof and a clear call to action — like Brex's email recruiting beta customers from its YC batch.
- **Go after the easiest customers first**: sell to your network and to startups (short decision lines); most people are not early adopters, so outbound is a numbers game.
- **Charge from the start**: if they don't pay, they're not a customer; in B2B, skip free trials for a money-back guarantee or opt-out, and raise prices until customers complain but still pay.
- **Work backwards from your goal**: 500 emails might yield 2 customers, so 100 emails proving 'sales doesn't work' is a data-free mistake — track every funnel step in a simple CRM.

Bottom line: early sales is founder-led, high-volume, and hands-on — track the funnel, charge real money, and onboard every customer you close.""",
        ),
        quiz_lesson(
            "Quiz: How to Get Your First Customers",
            (
                q(
                    "Who does the talk say should be doing sales in a startup's earliest days?",
                    (
                        opt("An outsourced sales agency that specializes in cold outreach"),
                        opt("An experienced VP of Sales hired as early as possible"),
                        opt(
                            "The founders themselves, until they know what good sales looks like",
                            correct=True,
                        ),
                        opt("The investors, since they have the strongest networks"),
                    ),
                    "The talk says sales must be part of the founders' DNA, like engineering: you shouldn't hire a sales team until you've learned to sell yourself, because only then do you know what good looks like.",
                ),
                q(
                    "A founder sends 100 outreach emails, gets zero customers, and concludes that sales doesn't work. What does the talk say about this?",
                    (
                        opt("It's the correct conclusion — they should switch to marketing or SEO"),
                        opt(
                            "It proves the product needs another year of development before selling"
                        ),
                        opt("It means their email copy was fine but their pricing was too high"),
                        opt(
                            "They simply didn't send enough emails to get real conversion data — sales is a numbers game",
                            correct=True,
                        ),
                    ),
                    "With typical funnel drop-offs, 500 emails might produce only 2 customers, so 100 emails yielding zero proves nothing; the talk calls this the mistake founders make 'on and on again.'",
                ),
                q(
                    "What does the talk recommend instead of free trials when selling B2B?",
                    (
                        opt(
                            "Charge, but offer a money-back guarantee or the ability to opt out of an annual contract",
                            correct=True,
                        ),
                        opt("Offer unpaid pilots until the customer sees clear ROI"),
                        opt("Keep the product free until you reach product-market fit"),
                        opt("Undercut competitors with the lowest possible price"),
                    ),
                    "If customers don't pay, they aren't customers; the talk says B2B founders should skip free trials and instead charge with a money-back guarantee or opt-out, raising prices until customers complain but still pay.",
                ),
            ),
        ),
        _yt("How to Get Your First 10 Customers", "_FBivfgOvuE", "14 min"),
        _t(
            "Key ideas — How to Get Your First 10 Customers",
            "4 min",
            """# Key ideas — Getting Your First 10 Customers

This talk compiles tactics from dozens of YC founders on how they actually landed their first 10 customers — and why that phase looks nothing like scaled sales.

- **Go where your buyer actually spends time.** Cold email and LinkedIn only work for buyers who live on a laptop; one founder closed more at a trade show in 3 days than in 3 months of cold email to a legacy industry.
- **Start with your warm network.** Customers 1-3 almost always come from friends, former colleagues, classmates, or people one intro away — early buyers are betting on trust in you as a founder.
- **Show up in person.** Flying out to buyers, stacking 15-minute meetings at small conferences, and hosting micro dinners for 6-10 prospects convert better than almost anything else.
- **Find the public pain.** Reddit threads, Facebook groups, and industry forums where customers already complain are a real customer source — some founders DM'd commenters one by one.
- **Give before you ask, and keep it human.** Frame outreach as advice, audits, or feedback sessions (only if genuine), keep emails under 75 words with one clear call to action, and follow up 3-4 times.
- **Save the tools for later.** Apollo, Clay, and email sequences start making sense around customers 10-50, once your pitch is refined.

Bottom line: your first 10 customers come from you personally doing unscalable things, not from any tool.""",
        ),
        quiz_lesson(
            "Quiz: How to Get Your First 10 Customers",
            (
                q(
                    "According to the talk, where do a founder's first two or three customers almost always come from?",
                    (
                        opt("Automated cold email sequences with well-tested subject lines"),
                        opt(
                            "The founder's personal network — friends, former colleagues, and people one introduction away",
                            correct=True,
                        ),
                        opt("Paid advertising targeted at the ideal customer profile"),
                        opt("Inbound leads from a product launch on Reddit"),
                    ),
                    "The speaker's survey of YC founders found essentially no counterexamples: customers 1-3 come from the warm network, because early buyers are betting on trust in the founder.",
                ),
                q(
                    "What happened when the YC founder selling into a legacy industry finally attended an industry trade show?",
                    (
                        opt("He confirmed that cold email was still his best-performing channel"),
                        opt(
                            "He got kicked out and concluded in-person sales don't work in legacy industries"
                        ),
                        opt(
                            "He collected business cards but closed nothing until he followed up by email"
                        ),
                        opt(
                            "He closed more in 3 days at the show than in 3 months of sending cold emails",
                            correct=True,
                        ),
                    ),
                    "The talk describes a founder whose email and LinkedIn outreach had terrible open and reply rates; walking a trade show floor for 3 days closed more customers than 3 months of cold email.",
                ),
                q(
                    "When does the talk say prospecting and outreach tools like Apollo and Clay actually start to matter?",
                    (
                        opt(
                            "Only after you have roughly 10 to 20 quality customers and a message worth scaling",
                            correct=True,
                        ),
                        opt("From day one, since automation frees the founder to focus on product"),
                        opt("Only after raising a Series A, when you can afford the paid tiers"),
                        opt("Never — the talk says founders should avoid outbound tools entirely"),
                    ),
                    "The speaker says these tools only start to matter once you have 10-20 quality customers, and that customers 10-50 are when higher-volume outreach tools make sense — before that, founders should work their network and do unscalable things.",
                ),
            ),
        ),
        _yt("How To Convert Customers With Cold Emails", "7Kh_fpxP1yY", "33 min"),
        _t(
            "Key ideas — How To Convert Customers With Cold Emails",
            "4 min",
            """# Key ideas — Cold Emails That Convert

Aaron Epstein explains how founders can write cold outreach that actually gets responses — for sales, recruiting, partnerships, or user research.

- **Warm intros beat everything**: a warm introduction converts two to three times better than a cold email, so mine LinkedIn, alumni networks, and past coworkers first.
- **Map your funnel backwards**: in his sample B2B funnel, getting one customer required roughly 800 emails sent — plan to send dozens per day, manually and personalized, before automating anything.
- **Targeting drives open rates**: 100 well-targeted emails beat 1,000 untargeted ones, and conversion rates decline as you scale, so fix them early.
- **Follow seven copy principles**: one focused goal, be human, personalize (find "uncommon commonalities"), keep it short, establish credibility, make it all about the reader, and end with a clear call to action.
- **You are the brand**: early on your company name opens no doors — personal effort, personalization, and founder-sent emails are what make people bet on you.
- **Follow up persistently**: plan two to four follow-ups spaced a few days apart, get creative, and never get angry when someone doesn't reply.

Bottom line: most cold emails are terrible, so doing the manual, personalized work puts you in the top 5% of emails and turns cold outreach into customers.""",
        ),
        quiz_lesson(
            "Quiz: How To Convert Customers With Cold Emails",
            (
                q(
                    "According to the talk, what is the single most effective 'hack' for getting people to respond to your outreach?",
                    (
                        opt(
                            "Writing a longer, more detailed email that explains your whole product"
                        ),
                        opt("Sending messages on LinkedIn instead of email"),
                        opt("Getting a warm intro through your network", correct=True),
                        opt("Offering a discount in the first email"),
                    ),
                    "The speaker opens with the all-time best outreach hack: get a warm intro, which converts two to three times better than a regular cold email.",
                ),
                q(
                    "In the example B2B conversion funnel, roughly how many emails did the founder need to send to land one customer?",
                    (
                        opt("40"),
                        opt("800", correct=True),
                        opt("8,000"),
                        opt("100"),
                    ),
                    "Working backwards through the sample funnel (demo, response, open, and send conversion rates), the talk concludes you need to send about 800 emails per customer.",
                ),
                q(
                    "What does the speaker say is the highest-leverage way to increase your email open rates?",
                    (
                        opt("Better targeting of who you send to", correct=True),
                        opt("Clever subject lines with emojis"),
                        opt("Sending from your company's brand name instead of your own"),
                        opt("Automating sends so you can reach thousands more people"),
                    ),
                    "The talk says the highest ROI for open rates comes from better targeting — 100 targeted emails beat 1,000 untargeted ones that mostly get deleted.",
                ),
            ),
        ),
        _yt("How To Keep Your Users", "VNxBZ7ka5J0", "29 min"),
        _t(
            "Key ideas — How To Keep Your Users",
            "4 min",
            """# Key ideas — Keeping Your Users with Cohort Retention

David Lee shows how cohort retention quantitatively answers "did we make something people want?", drawing on his experience at Bump and Google Photos.

- **Track cohorts, not blended users**: group new users by when they joined and measure what fraction comes back in each later period, rather than mixing the whole user base together.
- **Pick the right three ingredients**: a way to group cohorts (usually week or month of signup), an action truly correlated with getting value (Google Photos used viewing a photo full screen), and a time period that matches how the product is meant to be used.
- **Flat curves are the only thing that matters**: whether the curve flattens matters far more than its absolute height; curves sliding toward zero mean you haven't yet made something people want.
- **Don't fool yourself**: widening the time period, picking too easy an action (like just opening the app), quoting a single point like "80% week-over-week retention," or blindly trusting analytics dashboards all disguise bad retention.
- **Ways to improve**: a better product, acquiring better-matched users, stronger onboarding, and network effects — and slice cohorts by country, device, or customer type to see what's working.

Bottom line: flat or rising cohort curves that stack into a growing "layer cake" of active users are the strongest quantitative evidence you've made something people want.""",
        ),
        quiz_lesson(
            "Quiz: How To Keep Your Users",
            (
                q(
                    "When reading cohort retention curves, what does the speaker say is the only thing that really matters?",
                    (
                        opt("The retention number in the first week"),
                        opt("The total number of registered users"),
                        opt("The absolute height of the curve"),
                        opt("Whether the curves flatten out over time", correct=True),
                    ),
                    "The core insight of the talk is that the shape of the curve — whether it gets flat — is what matters, far more than the absolute number where it flattens.",
                ),
                q(
                    "Why does the speaker caution against using 'is paying' alone as your active-user action?",
                    (
                        opt(
                            "Users typically stop using a product before they stop paying for it",
                            correct=True,
                        ),
                        opt("Payment data is too hard to collect"),
                        opt("Paying users are too small a group to chart"),
                        opt("Revenue only matters after product-market fit"),
                    ),
                    "He notes people keep paying for services like Netflix long after they stop using them, so pairing 'is paying' with actual product usage is a better measure.",
                ),
                q(
                    "How did the team at Bump fool themselves about their retention?",
                    (
                        opt("They counted notification-driven opens as active use"),
                        opt("They only surveyed their happiest users"),
                        opt(
                            "They widened the measurement period from weekly to monthly and then quarterly until the curves looked good",
                            correct=True,
                        ),
                        opt("They excluded international users from their cohorts"),
                    ),
                    "The speaker admits Bump's weekly curves looked bad, so before investor meetings they widened the period to monthly and then quarterly — deluding themselves, since Bump was meant to be used frequently.",
                ),
            ),
        ),
        # ── Part 5 — Business models, pricing & sales ───────────────
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
        quiz_lesson(
            "Quiz: Part 5 — Business models, pricing & sales",
            (
                q(
                    "What does Part 5 say about how founders typically price?",
                    (
                        opt(
                            "They almost always undercharge — price on value, not cost",
                            correct=True,
                        ),
                        opt("They almost always overcharge and lose deals"),
                        opt("They usually price exactly right by instinct"),
                        opt("Pricing doesn't matter until Series A"),
                    ),
                    "Founders almost always undercharge; the fix is pricing on the value created, not on cost or fear.",
                ),
                q(
                    "Why do dev-tools companies get a dedicated talk?",
                    (
                        opt("Because dev tools can't make money"),
                        opt("Because they never need a sales team"),
                        opt(
                            "Because when the customer is a developer, the usual playbook inverts",
                            correct=True,
                        ),
                        opt("Because they are immune to competition"),
                    ),
                    "When the user is a developer, the usual go-to-market playbook inverts — which deserves its own treatment.",
                ),
            ),
        ),
        _yt("Startup Business Models and Pricing", "oWZbWzAyHAE", "33 min"),
        _t(
            "Key ideas — Startup Business Models and Pricing",
            "4 min",
            """# Key ideas — Business Models and Pricing

YC group partner Aaron Epstein explains which business models build the biggest companies and how early-stage founders should think about pricing.

- **Copy a proven business model**: nearly every billion-dollar company uses one of nine models (SaaS, transactional, marketplace, hard tech, usage-based, enterprise, advertising, e-commerce, bio). Innovate on your product, not your business model.
- **SaaS, transactional, and marketplaces dominate**: together they make up 67% of the top 100 YC companies. Marketplaces are five of the top ten because network effects make them winner-take-all, and transactional businesses win by sitting directly in the flow of funds.
- **Recurring revenue with strong retention** creates winners: with 95% monthly retention, 100 customers shrink to 54 in a year — you can't scale a leaky bucket.
- **You should charge, and price on value, not cost**: charging teaches you who wants your product and how much; cost-plus pricing ignores the perceived value customers see.
- **Most startups undercharge**: keep raising prices until customers complain but still pay, and remember pricing isn't permanent — Netflix repeatedly raised prices, and Segment went from $120 to $18,000 a year by asking.
- **Keep pricing simple** so it never adds friction to paying you.

Bottom line: pick a proven, recurring, defensible business model and treat pricing as a learning tool you can keep raising as you build more value.""",
        ),
        quiz_lesson(
            "Quiz: Startup Business Models and Pricing",
            (
                q(
                    "According to the talk, which three business models together account for 67% of the top 100 YC companies?",
                    (
                        opt("Advertising, e-commerce, and hard tech"),
                        opt("SaaS, transactional, and marketplaces", correct=True),
                        opt("Enterprise, bio, and usage-based"),
                        opt("Consulting, affiliate, and hardware"),
                    ),
                    "Aaron shows that SaaS (31%), transactional (22%), and marketplaces (14%) together make up 67% of the top 100 YC companies, while advertising and e-commerce barely register.",
                ),
                q(
                    "In the retention example, a startup with 95% monthly retention starts the year with 100 customers. What happens by year-end?",
                    (
                        opt("It keeps 95 of its original customers because retention is 95%"),
                        opt("It roughly doubles its customer base through compounding"),
                        opt("It keeps about 90 customers, losing only 10"),
                        opt("It keeps only about 54 of its original customers", correct=True),
                    ),
                    "Losing 5% of customers every month compounds: of 100 customers, only 54 remain after a year, which is why you can't scale a leaky bucket.",
                ),
                q(
                    "Why did early Stripe set its price at 5% per transaction when competitors charged around 3%?",
                    (
                        opt(
                            "To test how much value customers saw in features like quick setup and great developer documentation",
                            correct=True,
                        ),
                        opt("Because its costs per transaction were higher than competitors'"),
                        opt("To undercut the competition and win price-sensitive customers"),
                        opt("Because regulators required a minimum transaction fee"),
                    ),
                    "Rather than undercutting competitors, Stripe deliberately priced higher to prove customers valued things like one-click signup and in-depth developer API docs.",
                ),
            ),
        ),
        _yt("How To Price For B2B", "4hjiRmgmHiU", "18 min"),
        _t(
            "Key ideas — How To Price For B2B",
            "4 min",
            """# Key ideas — Pricing for B2B

Tom explains how founders can pick and justify a price for B2B software instead of freezing when a customer asks.

- **Start with the value equation**: write out with your champion, step by step, the cost savings, time savings, or revenue increase your product delivers; it becomes the document they take to their CFO.
- **Charge 25-50% of the value**: the customer keeps roughly two-thirds — a $2M saving supports a contract around $700K — and the equation also gives you the success metrics for a short pilot.
- **Cost is only a floor**: never do cost-plus pricing; aim for 80-90% software margins and treat cloud and LLM credits as a real cash cost.
- **Don't fight price wars**: undercutting a competitor triggers a race to the bottom — differentiate on functionality and value instead (the commodity airline business, at about 2.7% net margin, shows where that race ends).
- **Prefer committed recurring revenue**: mirror how the customer already pays for software, keep pricing simple, convert usage-based customers to monthly commitments, and keep enterprise pricing off your website since value differs per customer.
- **When in doubt, iterate up**: pick a number, raise it about 50% with each new pitch, and stop when you lose more than roughly 25% of deals on price alone.

Bottom line: over-optimizing pricing early is a mistake — write the value equation, pick a number, and keep experimenting upward.""",
        ),
        quiz_lesson(
            "Quiz: How To Price For B2B",
            (
                q(
                    "Using the 'value equation,' what share of the value you deliver does the speaker suggest charging the customer?",
                    (
                        opt("100% — capture all the value you create"),
                        opt("5-10%, to make the deal an easy yes"),
                        opt("About 25-50%, so the customer keeps roughly two-thirds", correct=True),
                        opt("Whatever covers your costs plus 10%"),
                    ),
                    "The talk recommends pricing at 25-50% of the value delivered — in the example, about $700K of a $2M saving — so it's a great deal for both sides.",
                ),
                q(
                    "What role should your own costs play in setting your price?",
                    (
                        opt("The starting point: add a standard margin on top of cost"),
                        opt(
                            "A floor to stay above, while aiming for 80-90% software margins",
                            correct=True,
                        ),
                        opt("No role — costs are irrelevant to pricing"),
                        opt("A ceiling you should never price above"),
                    ),
                    "The speaker warns never to start with cost-plus pricing; cost should only ever be a floor, with a target of 80-90% gross margins.",
                ),
                q(
                    "A direct competitor with an equivalent product undercuts your price by half. What does the talk recommend?",
                    (
                        opt("Match their price immediately to stay competitive"),
                        opt("Undercut them even further to win market share"),
                        opt("Exit the market, since first movers always win"),
                        opt(
                            "Differentiate your product on functionality and value instead of fighting a price war",
                            correct=True,
                        ),
                    ),
                    "The talk says competing solely on price is a race to the bottom; you should set your product apart so it's not an apples-to-apples comparison.",
                ),
            ),
        ),
        _yt("The Sales Playbook For Founders", "DH7REvnQ1y4", "19 min"),
        _t(
            "Key ideas — The Sales Playbook For Founders",
            "4 min",
            """# Key ideas — The Sales Playbook for Founders

This talk maps the progression B2B founders go through when closing their first contracts — and argues most founders move through it far too slowly.

- **Design partnerships are the most common trap**: they run 3-6 months, are poorly defined in scope, and suffer low engagement because the customer is not paying for your time.
- **Build a narrow wedge product**: observe customers, find a burning problem, build a wedge in as little as 48 hours, and sell it to ~10 similar customers instead of overbuilding a broad platform.
- **Pilots need defined success metrics** tied to a value equation (e.g., proving you can solve 20% of support queries) so your internal champion can show the CFO a clear return on investment.
- **Paid pilots beat free ones**: an upfront financial commitment makes customers take the pilot seriously — keep it short and track "time to first value" like a north-star metric.
- **The pro move is a recurring contract with a 30-60 day opt-out**: one sales process that converts into recurring revenue by default (just be clear with investors when reporting ARR).
- **Practical tips**: start SOC 2 early, treat your champion like a co-founder, visit customers in person, and only fight contract clauses that are company-ending.

Bottom line: advance to paid, tightly scoped commitments as fast as you can — don't stay stuck in free, open-ended engagements.""",
        ),
        quiz_lesson(
            "Quiz: The Sales Playbook For Founders",
            (
                q(
                    "According to the talk, what is the biggest problem with typical design partnerships?",
                    (
                        opt(
                            "They are too long and poorly defined, with low customer engagement because the customer isn't paying",
                            correct=True,
                        ),
                        opt("They legally obligate the startup to give the customer equity"),
                        opt("They require expensive security certifications before starting"),
                        opt("They only work for companies selling to law and accounting firms"),
                    ),
                    "The speaker says design partnerships often last 3-6 months, are vague in scope, and suffer low engagement since the customer isn't paying for the founders' time — making them the most common way B2B founders get stuck.",
                ),
                q(
                    "What metric does the speaker suggest tracking like a north-star during pilots?",
                    (
                        opt("Number of features shipped during the pilot"),
                        opt("Time to first value — reducing it from weeks to hours", correct=True),
                        opt("Total number of design partners signed"),
                        opt("Number of NDA redlines resolved per week"),
                    ),
                    "He says reducing time to first value from weeks to hours is often the single biggest lever for improving pilot-to-paid conversion, even if it means doing janky things like Excel imports instead of full API integrations.",
                ),
                q(
                    "What does the speaker describe as the 'pro move' for closing B2B deals?",
                    (
                        opt("Offering the product free for a year to land big logos"),
                        opt(
                            "Running several consecutive free proof-of-concepts before discussing price"
                        ),
                        opt(
                            "A recurring revenue contract with a 30-60 day opt-out period that converts automatically",
                            correct=True,
                        ),
                        opt("Skipping pilots entirely and demanding multi-year contracts upfront"),
                    ),
                    "The pro move is a monthly or annual recurring contract with a 30 or 60-day money-back/opt-out period at the start — one sales process that becomes a full recurring contract by default if the customer is happy.",
                ),
            ),
        ),
        _yt("Enterprise Sales", "0fKYVl12VTA", "23 min"),
        _t(
            "Key ideas — Enterprise Sales",
            "4 min",
            """# Key ideas — Enterprise Sales for Founders

Pete Koomen walks through the enterprise sales funnel — prospecting, outreach, qualification, demos, pricing, closing, and implementation — from his experience co-founding Optimizely.

- **Founders must sell**: sales before product-market fit is entrepreneurial, requiring vision, credibility, and a tight feedback loop with the product — you can't hire it out, and technical founders' expertise and conviction are real advantages.
- **Prospect from a hypothesis**: "customer X has problem Y and our product will help them solve it" tells you exactly which companies and which specific humans to contact.
- **Qualify ruthlessly**: don't chase prospects who are merely easy to talk to; feedback from people who will never buy is useless at best. On the first call, ask lots of questions instead of pitching.
- **Demo like a movie script**: tell a personalized story of how the customer solves their problem, with magic moments — never a screen-by-screen feature tour.
- **Treat pricing as experiments**: charge more than feels comfortable; high prices make customers serious — Optimizely once quoted 5x what a prospect would pay and still closed the deal.
- **Closing and implementation are your job**: ask upfront how the company buys software, run procurement steps in parallel, and project-manage the customer's implementation — a signed contract with an unused product won't renew.

Bottom line: sales is a learnable skill about helping people solve their problems, and the only way to learn it is to just get started.""",
        ),
        quiz_lesson(
            "Quiz: Enterprise Sales",
            (
                q(
                    "Why does the speaker say early-stage founders can't simply hire a salesperson to sell their product?",
                    (
                        opt("Experienced salespeople are too expensive before revenue"),
                        opt(
                            "Sales before product-market fit is entrepreneurial work requiring founder vision, credibility, and a tight product feedback loop",
                            correct=True,
                        ),
                        opt("Good salespeople only join late-stage companies"),
                        opt("Investors expect the technical founders to run sales themselves"),
                    ),
                    "The talk explains that pre-product-market-fit sales is fundamentally entrepreneurial — a founder's role — so if you can't sell it yourself, a hired salesperson won't either.",
                ),
                q(
                    "According to the talk, what is your job on the first call with a prospect?",
                    (
                        opt(
                            "Ask questions to qualify them and schedule a follow-up demo",
                            correct=True,
                        ),
                        opt("Deliver your full pitch and product demo immediately"),
                        opt("Quote a price so you don't waste anyone's time"),
                        opt("Get the contract signed while interest is high"),
                    ),
                    "The first call is not for selling: it's for qualifying whether the prospect has the problem, budget, and authority — and for booking the demo.",
                ),
                q(
                    "What does the speaker call the single biggest mistake founders make at the implementation stage?",
                    (
                        opt("Charging extra for implementation services"),
                        opt("Starting implementation before the contract is signed"),
                        opt("Assigning implementation to a junior engineer"),
                        opt(
                            "Assuming implementation is the customer's job instead of project-managing it themselves",
                            correct=True,
                        ),
                    ),
                    "At Optimizely, six-figure customers never ran a single test because the founders left installation to them; the lesson is to treat implementation as your own high-priority project.",
                ),
            ),
        ),
        _yt("How To Start A Dev Tools Company", "z1aKRhRnVNk", "33 min"),
        _t(
            "Key ideas — How To Start A Dev Tools Company",
            "4 min",
            """# Key ideas — How to Start a Dev Tools Company

Nicolas, YC group partner and Algolia co-founder, walks through picking a dev tool idea, building the prototype and MVP, and running a developer-focused go-to-market.

- **Runtime beats build-time ideas**: build-time tools (docs, QA, testing) are nice-to-have and crowded, while runtime products like APIs are must-have and their usage grows with the customer — aligned incentives, as with Stripe.
- **You don't need a business co-founder**: 74% of YC dev tool companies had only technical founders; learning to sell is easier than teaching a salesperson to talk to developers.
- **Prototype quick and dirty**: assume 90% of your code gets thrown away; Algolia closed a $2,000/month contract demoing with just a command line and a simple web page.
- **Outreach plus launches**: nobody knows you at first, so personalize outreach and launch repeatedly on Hacker News (Show HN), the way Ollama did — and do things that don't scale, like Stripe implementing its product side by side with customers.
- **Consider open source**: it's essentially required for libraries/frameworks and sensitive-data tools; monetize via hosting or open core, but avoid charging for support and services.
- **Founders sell and developers market**: show demos instead of sales decks, make documentation and engineer-run support first-class marketing, and wait until roughly $1M ARR to hire your first salesperson.

Bottom line: start now, iterate fast with real developer users, and stay the best salesperson and marketer for your own product as long as you can.""",
        ),
        quiz_lesson(
            "Quiz: How To Start A Dev Tools Company",
            (
                q(
                    "Why does the speaker say runtime ideas are better than build-time ideas for dev tools?",
                    (
                        opt(
                            "Runtime products are must-have and critical — customers can't run their product without them — and usage grows as customers grow",
                            correct=True,
                        ),
                        opt("Runtime products never have any competitors"),
                        opt("Build-time tools are impossible to build with modern technology"),
                        opt("Runtime products don't require any sales or marketing effort"),
                    ),
                    "He explains that build-time tools like docs and QA are mostly nice-to-have and noisy markets, while runtime products (like an API) are critical to operate, and incentives align because customer growth drives more usage — his Stripe example.",
                ),
                q(
                    "When does the speaker suggest hiring your first salesperson?",
                    (
                        opt("Before writing any code, so sales can validate the idea"),
                        opt("Immediately after your first Hacker News launch"),
                        opt(
                            "As a rule of thumb, around $1 million in ARR — and even then prefer technical hires",
                            correct=True,
                        ),
                        opt("Only after hiring a traditional CMO to lead go-to-market"),
                    ),
                    "He advises founders to sell themselves as long as possible and, as a rule of thumb, wait until about $1M ARR before the first sales hire, favoring people who are technical or understand developers.",
                ),
                q(
                    "Which open source monetization approach does the speaker discourage?",
                    (
                        opt("Offering a hosted cloud version of the open source product"),
                        opt("An open core model with enterprise features like SSO and audit logs"),
                        opt("Usage-based pricing for an API"),
                        opt("Charging for support and services", correct=True),
                    ),
                    "He warns that charging for support and services creates a bad incentive to build the most complex product possible, and if the product doesn't need much support, customers churn off their support contracts.",
                ),
            ),
        ),
        # ── Part 6 — Metrics, fundraising & YC ──────────────────────
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
        quiz_lesson(
            "Quiz: Part 6 — Metrics, fundraising & YC",
            (
                q(
                    "Which metrics anchor consumer vs B2B companies, per Part 6?",
                    (
                        opt("Downloads for both"),
                        opt(
                            "Consumer companies live by retention curves; B2B companies by revenue growth and churn",
                            correct=True,
                        ),
                        opt("Press mentions for consumer, headcount for B2B"),
                        opt("The same dashboard works for every company"),
                    ),
                    "Consumer companies live and die by retention curves; B2B companies by revenue growth and churn — with one primary metric per company.",
                ),
                q(
                    "Which fundraising instrument does Part 6 introduce?",
                    (
                        opt("Bank loans with personal guarantees"),
                        opt("Revenue-based financing only"),
                        opt("Direct-to-IPO listings"),
                        opt(
                            "SAFEs — along with dilution and milestone-based raising", correct=True
                        ),
                    ),
                    "The fundraising talk explains how SAFEs, dilution and milestone-based raising actually work.",
                ),
            ),
        ),
        _yt("Consumer Startup Metrics", "fdD4y4Civp4", "22 min"),
        _t(
            "Key ideas — Consumer Startup Metrics",
            "4 min",
            """# Key ideas — Consumer Startup Metrics

Drawing on his experience founding Monzo and working with dozens of consumer companies at YC, Tom Blomfield walks through the metrics that matter most for consumer startups.

- **Growth rate**: 15% month-over-month growth in active users is the target (roughly 5x per year), 10% is okay, and 5% or lower is unlikely to reach breakout success.
- **Organic vs paid growth**: the best consumer companies get 80%+ of sign-ups organically through virality (users spread the product by using it, like Facebook photo tags) and network effects (the product gets better as more people join, like WhatsApp). Over-relying on paid ads hands your margin to Google and Meta.
- **Customer acquisition cost** must be tracked per channel and measured to an active, monetized, retained user — not a mere sign-up — and recorded forever, since seemingly cheap channels can deliver deeply unprofitable users.
- **Unit economics** (revenue per customer minus variable costs) must turn positive before you scale; Monzo burned a lot of capital scaling at negative unit economics.
- **Retention and magic moments**: find the behavior that predicts long-term retention (Facebook's seven friends in ten days) and re-engineer onboarding so users hit it fast.
- **Net Promoter Score**: +50 is the minimum baseline for a new consumer company, and the collection method must stay consistent.

Bottom line: engineer organic loops, fix unit economics before scaling, and obsess over retention.""",
        ),
        quiz_lesson(
            "Quiz: Consumer Startup Metrics",
            (
                q(
                    "According to the talk, what month-over-month growth rate in users is described as good for a consumer startup?",
                    (
                        opt("5% month over month"),
                        opt("15% month over month", correct=True),
                        opt("50% month over month"),
                        opt("15% week over week"),
                    ),
                    "The talk sets 15% month-over-month as a good growth rate (about 5x per year), calls 10% okay, and says 5% or lower is unlikely to reach breakout success.",
                ),
                q(
                    "How does the talk distinguish a network effect from virality?",
                    (
                        opt(
                            "A network effect is just another name for a paid referral scheme like Uber's free rides"
                        ),
                        opt(
                            "Virality means the product improves as more people join, while a network effect spreads the product through advertising"
                        ),
                        opt(
                            "A network effect means the product gets better as more people use it, while virality means users introduce the product to others through their use of it",
                            correct=True,
                        ),
                        opt(
                            "They are identical concepts and the talk says the terms can be used interchangeably"
                        ),
                    ),
                    "Virality is when one user's use of the product introduces it to new users (like Facebook photo tagging), while a network effect means the product becomes more valuable as more people join (like WhatsApp).",
                ),
                q(
                    "How does the speaker say customer acquisition cost (CAC) should be measured?",
                    (
                        opt(
                            "Per channel, measured to an active, monetized, retained user rather than a mere sign-up",
                            correct=True,
                        ),
                        opt("As a single blended average cost per sign-up across all channels"),
                        opt(
                            "Only for paid channels, since organic users have no acquisition cost worth tracking"
                        ),
                        opt(
                            "Including fixed costs like engineering salaries and office rent in each user's cost"
                        ),
                    ),
                    "He stresses measuring CAC per channel to an active, monetized, retaining user (like Monzo's weekly active user), not to a sign-up, because 80-90% of sign-ups may drop off in the first week.",
                ),
            ),
        ),
        _yt("B2B Startup Metrics", "_mKeVGSqQac", "24 min"),
        _t(
            "Key ideas — B2B Startup Metrics",
            "4 min",
            """# Key ideas — B2B Startup Metrics

Tom Blomfield, YC group partner and Monzo founder, explains which metrics B2B founders should track and the traps that fool founders into thinking they are succeeding.

- **Build metrics before you launch**: pick four or five key metrics with agreed, written definitions and keep them consistent — launching blind is like flying a plane with no instruments, and changing definitions later only fools yourself.
- **Avoid vanity metrics** like GMV or gross transaction value; for most B2B companies **revenue** is the key metric, and every investor update should lead with revenue, **burn rate**, and **runway**.
- **Retention** decides whether monthly cohorts stack into a growing "layer cake" of recurring revenue or leak out of a bucket you can never fill; what matters most is that retention flattens out.
- **Net dollar retention** nets upsells against churned revenue within a cohort; above 100% means cohorts grow over time, and early-stage B2B SaaS should target well above 100% (125-150%).
- **Gross margin** (revenue minus cost of goods sold) now matters even for software — AI companies' payments to foundation-model providers are real COGS, and free credits merely hide that cost.
- **Don't scale a negative-margin business**; fix unit economics first, as Monzo did before becoming profitable.

Bottom line: track a few honestly defined metrics — revenue, retention, and gross margin — and fix them before you scale.""",
        ),
        quiz_lesson(
            "Quiz: B2B Startup Metrics",
            (
                q(
                    "Which three metrics does the speaker say should be at the top of every investor update?",
                    (
                        opt("Revenue, burn rate, and runway", correct=True),
                        opt("Gross merchandise value, page views, and unique visitors"),
                        opt("Net promoter score, customer acquisition cost, and lifetime value"),
                        opt("Sign-ups, daily active users, and churn rate"),
                    ),
                    "He says revenue, burn rate, and runway are absolutely crucial, and if they are not at the top of an investor update he assumes the founder has something to hide.",
                ),
                q(
                    "In the talk's example, a January cohort starts at $100K MRR, loses two $10K customers, and upsells three customers by an extra $10K each. What is its net dollar retention?",
                    (
                        opt("80%, because two of the ten customers churned"),
                        opt("100%, because the gains and losses cancel out"),
                        opt("130%, counting only the upsold revenue"),
                        opt(
                            "110%, because the $30K gained nets against the $20K lost", correct=True
                        ),
                    ),
                    "Losing $20K and gaining $30K nets to +$10K, so the cohort goes from $100K to $110K of monthly revenue — 110% net dollar retention, meaning the cohort is growing over time.",
                ),
                q(
                    "According to the talk, why are free credits from AI model providers dangerous for a startup's metrics?",
                    (
                        opt(
                            "Free credits count as revenue and artificially inflate growth numbers"
                        ),
                        opt("Investors refuse to fund any company that accepts free credits"),
                        opt(
                            "The credits hide a real cost of goods sold, so gross margins will collapse when the credits run out",
                            correct=True,
                        ),
                        opt(
                            "Using free credits locks the startup into a single model provider forever"
                        ),
                    ),
                    "He warns that free credits don't mean the cost of goods sold doesn't exist — they just hide it, so companies claiming huge gross margins face a nasty shock when the credits run out.",
                ),
            ),
        ),
        _yt("Setting KPIs and Goals", "6DTK9yDP6p0", "27 min"),
        _t(
            "Key ideas — Setting KPIs and Goals",
            "4 min",
            """# Key ideas — Setting KPIs and Goals

Divya, a two-time YC founder and visiting group partner, explains how choosing the right KPIs and prioritizing ruthlessly speeds up the journey to product-market fit.

- **Primary KPI = revenue growth** for the vast majority of launched startups; exceptions include marketplaces (sign-ups/GMV) and hardware, biotech, or long-sales-cycle enterprise businesses (letters of intent, milestones) — but audit those frequently.
- **Keep three to five secondary KPIs** — like retention/churn, unit economics, and CAC payback — to make sure you aren't cheating on your primary KPI.
- **Work only on the biggest bottleneck**: Super Daily found high-intent users churned because a specific milk brand was missing; onboarding it lifted conversion by 50% — no sign-up-screen polish required.
- **Beware fake progress**: passive investor coffees, conference attendance, arbitrary technical milestones, and perfectionism feel productive and boost your ego but don't move you toward product-market fit.
- **Set targets both top-down and bottom-up**: per Paul Graham's growth essay, 5-7% week-over-week growth is good for a YC company and 10% is exceptional — and early growth compounds, like Airbnb's goals written on the bathroom mirror.
- **Don't hedge between two hard goals**: Rickshaw split focus between growth and unit economics and landed in a "no man's land" of slow growth, while DoorDash stayed laser-focused on order volume.

Bottom line: pick the right primary KPI, attack only its biggest blocker, and be honest with yourself when it isn't moving.""",
        ),
        quiz_lesson(
            "Quiz: Setting KPIs and Goals",
            (
                q(
                    "In the Super Daily example, why were high-intent users dropping out of the sign-up funnel?",
                    (
                        opt("The sign-up screen had too much UX friction and needed a redesign"),
                        opt(
                            "The app didn't carry a specific milk brand that users wanted",
                            correct=True,
                        ),
                        opt("Delivery fees were too high compared to competitors"),
                        opt("The mobile app crashed frequently during checkout"),
                    ),
                    "The talk explains it wasn't a UX friction or app issue — users wanted a specific milk brand Super Daily didn't carry, and onboarding that brand increased conversion by 50%.",
                ),
                q(
                    "Citing Paul Graham's classic essay on growth, what weekly growth rate does the talk call good for a company going through YC, and what rate is exceptional?",
                    (
                        opt("5-7% month over month is good; 10% monthly is exceptional"),
                        opt("15% week over week is the minimum acceptable rate"),
                        opt("1-2% week over week is good; 5% is exceptional"),
                        opt("5-7% week over week is good; 10% is exceptional", correct=True),
                    ),
                    "The talk cites Paul Graham's essay: 5-7% week-over-week growth is good for a YC company, and 10% week-over-week is exceptional.",
                ),
                q(
                    "What lesson does the speaker draw from comparing her startup Rickshaw with DoorDash?",
                    (
                        opt(
                            "Splitting focus between growth and unit economics put Rickshaw in a no man's land of slow growth — choose one primary KPI",
                            correct=True,
                        ),
                        opt(
                            "Rickshaw failed because order volume was the wrong metric to track at demo day"
                        ),
                        opt("Rickshaw scaled paid acquisition too early and ran out of money"),
                        opt(
                            "DoorDash won purely because it launched in a bigger city than Rickshaw"
                        ),
                    ),
                    "After fundraising trouble, Rickshaw tried to optimize for both growth and unit economics at once; this split focus put it in a 'no man's land' of slow growth, while DoorDash kept a laser focus on top-line order volume.",
                ),
            ),
        ),
        _yt("How Startup Fundraising Works", "zBUhQPPS9AY", "28 min"),
        _t(
            "Key ideas — How Startup Fundraising Works",
            "4 min",
            """# Key ideas — How Startup Fundraising Works

YC group partner Brad Flora, a former founder and investor, debunks seven myths that make new founders think fundraising "isn't for them."

- **Fundraising is a grind, not glamour**: real rounds are one-on-one coffee chats and Zoom calls, not Shark Tank. Freshpaint met about 160 investors over four-plus months to raise $1.6M in checks from $5K to $200K.
- **Build before you raise**: make a simple first version and get users first. Solugen built a desk-sized reactor and sold hydrogen peroxide to hot tub supply stores, then raised $4M.
- **Convince, don't impress**: there are no magic words. Retool's founder skipped the deck, demoed the product, and talked plainly about early customers — that won the check.
- **SAFEs make raising fast, cheap, and founder-controlled**: five pages, essentially two terms (amount and valuation cap), no lawyers, no board seats. Zapier raised about $1M once on this basis, ran the company its own way, and never raised again.
- **You don't need a fancy network**: investors care about companies making money — Podium sold review software to tire shops with no Silicon Valley connections.
- **Rejection means nothing by itself**: Envision's founder was rejected 50+ times; Whatnot raised only a fraction of its seed goal and became a multi-billion-dollar company.

Bottom line: fundraising is just a lot of plain conversations about something people want — anyone who builds first can do it.""",
        ),
        quiz_lesson(
            "Quiz: How Startup Fundraising Works",
            (
                q(
                    "According to the talk, what does early-stage fundraising actually look like in practice?",
                    (
                        opt(
                            "A single high-pressure pitch to a panel of investors, like Shark Tank"
                        ),
                        opt(
                            "A long grind of one-on-one coffee chats and Zoom calls with many investors",
                            correct=True,
                        ),
                        opt("A press-driven launch event that attracts inbound offers"),
                        opt("A formal business plan competition judged by VCs"),
                    ),
                    "The speaker says pitch competitions and Shark Tank are 'just for show'; real fundraising is repeated one-on-one meetings, as Freshpaint's map of ~160 investor meetings shows.",
                ),
                q(
                    "The talk says nobody really uses the discount term anymore. Which two terms do founders actually negotiate when closing a SAFE?",
                    (
                        opt("Board seats and information rights"),
                        opt("Interest rate and maturity date"),
                        opt("Founder salary and vesting schedule"),
                        opt("The investment amount and the valuation cap", correct=True),
                    ),
                    "The SAFE is a five-page document with three terms — amount, valuation cap, and discount — and since 'nobody does discounts,' only the amount and cap are really discussed.",
                ),
                q(
                    "What did Solugen do before raising money, in contrast to founders who pitch a deck asking for $20M?",
                    (
                        opt(
                            "They built a small working reactor and sold hydrogen peroxide to early customers",
                            correct=True,
                        ),
                        opt(
                            "They hired an experienced fundraising advisor to pitch investors for them"
                        ),
                        opt(
                            "They waited until a large pharma partner committed to buy their output"
                        ),
                        opt("They bootstrapped for a decade to avoid investors entirely"),
                    ),
                    "Solugen built a desk-sized reactor, then a slightly larger one, and was making about $10K/month selling hydrogen peroxide to hot tub supply stores — progress that let them raise $4M.",
                ),
            ),
        ),
        _yt("How to Apply And Succeed at Y Combinator", "B5tU2447OK8", "25 min"),
        _t(
            "Key ideas — How to Apply And Succeed at Y Combinator",
            "4 min",
            """# Key ideas — How to Apply and Succeed at Y Combinator

Dalton, a YC group partner, demystifies the YC application and interview and argues that applying is a tiny time commitment with uncapped upside.

- **Applying creates luck**: putting yourself out there in situations with surprising upside makes you luckier; avoiding rejection shrinks your surface area for luck.
- **Most reasons not to apply are wrong**: there's no such thing as "too early" (many admitted companies pivoted after getting in), founders with significant revenue or prior funding still get in, and reapplying multiple times is a plus that shows persistence.
- **Write a clear application**: fill everything out, follow the directions, and be concise — a strong application lets the reader tell a simple story about the founders, what they've built, and the evidence people want it (GitLab's application is the model).
- **Honesty is non-negotiable**: misrepresenting revenue, traction, or your background is automatically disqualifying, and extraordinary claims require extraordinary evidence.
- **Technical talent matters most**: teams with a founder hireable into a technical role at a top YC company have roughly 5x better odds of an interview — and no warm intros are needed, since YC is built to fund complete strangers.
- **The interview is a 10-minute Zoom conversation**, not an adversarial pitch: memorized speeches and coached obfuscation backfire, because the interviewers are the people you'd be working with.

Bottom line: don't overthink it — apply, be clear and honest, and address the feedback if you reapply.""",
        ),
        quiz_lesson(
            "Quiz: How to Apply And Succeed at Y Combinator",
            (
                q(
                    "According to the talk, what is probably the biggest variable in whether an applicant is selected for a YC interview?",
                    (
                        opt("Having a warm introduction from a YC alum"),
                        opt("Submitting a polished pitch deck along with the application"),
                        opt(
                            "The quality and quantity of technical talent on the founding team",
                            correct=True,
                        ),
                        opt("How much revenue the company has already generated"),
                    ),
                    "Dalton says teams with at least one founder skilled enough to be hired into a technical role at a top YC company have 5x better odds of being selected for an interview.",
                ),
                q(
                    "How does the speaker say YC views founders who have applied before without getting in?",
                    (
                        opt(
                            "It's a plus — reapplying shows persistence, especially when each application shows more progress",
                            correct=True,
                        ),
                        opt("It counts against them, since rejection signals a weak idea"),
                        opt("They must wait at least two years before applying again"),
                        opt("Previous applications are deleted, so it has no effect either way"),
                    ),
                    "He stresses that applying multiple times is actually a plus, not a negative — recent batches include founders who applied five, six, or seven times, showing persistence and character, especially when each application shows more progress.",
                ),
                q(
                    "What does the talk say is the best way to behave in the YC interview itself?",
                    (
                        opt(
                            "Open with a rehearsed, memorized pitch to make sure you cover everything"
                        ),
                        opt(
                            "Answer the basic questions directly and be yourself in a natural conversation",
                            correct=True,
                        ),
                        opt(
                            "Treat it as an adversarial negotiation and reveal as little as possible"
                        ),
                        opt("Present a slide deck and product demo video during the call"),
                    ),
                    "The interview is a 10-minute Zoom with basic, context-dependent questions; memorized speeches and adversarial tactics backfire, because the interviewers are likely the people you'd work with — so answer directly and be yourself.",
                ),
            ),
        ),
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
                    "Ideas grounded in problems the founders have lived produce founder/market fit; 'thought of' ideas tend toward tarpits — plausible, popular, and already tried by thousands of teams.",
                ),
                q(
                    "What is a 'tarpit idea'?",
                    (
                        opt("An idea in a heavily regulated industry"),
                        opt("An idea that requires deep technical expertise"),
                        opt(
                            "A common idea that seems appealing and novel but has trapped many founders before, usually because a structural problem makes it much harder than it looks",
                            correct=True,
                        ),
                        opt("An idea that only works with venture funding"),
                    ),
                    "Tarpit ideas (e.g. an app to discover things to do with friends) look under-served but have consumed thousands of teams — the demand or distribution structurally isn't there.",
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
                    "Near-equal splits keep every founder fully motivated for a decade-long journey; vesting (typically 4 years with a 1-year cliff) protects the company if someone leaves early.",
                ),
                q(
                    "What is the defining property of a good MVP in YC's framing?",
                    (
                        opt("It is polished enough that early users can't tell it's v1"),
                        opt(
                            "It is built fast (weeks, not months) and put in front of real users so you can start learning",
                            correct=True,
                        ),
                        opt("It already includes the features enterprise buyers will need"),
                        opt("It is fully automated end to end before anyone sees it"),
                    ),
                    "The point of an MVP is learning velocity: ship something minimal to your first users, iterate from what they do — not what they say.",
                ),
                q(
                    "When talking to users, which question style yields the most reliable signal?",
                    (
                        opt("'Would you use a product that did X?'"),
                        opt("'How much would you pay for X?'"),
                        opt(
                            "Questions about their life and past behavior — how they hit the problem, what it costs them, what they've already tried",
                            correct=True,
                        ),
                        opt("A demo followed by asking whether they liked it"),
                    ),
                    "Hypotheticals invite polite lies. Specifics about past behavior — the core of talking to users well — reveal whether the problem is real, frequent, and worth money.",
                ),
                q(
                    "YC's advice on launching is to…",
                    (
                        opt("wait until the product is complete, then do one big press launch"),
                        opt(
                            "launch early and launch repeatedly — almost nobody remembers your launch, and real feedback starts when users arrive",
                            correct=True,
                        ),
                        opt("stay in private beta until a journalist agrees to cover you"),
                        opt("time the launch to coincide with a fundraise"),
                    ),
                    "Launches are cheap and forgettable; treat them as a repeatable channel for learning, not a one-shot event to be perfected.",
                ),
                q(
                    "'Do things that don't scale' means your first customers should come from…",
                    (
                        opt("paid advertising tuned by an agency"),
                        opt("waiting for organic search traffic to compound"),
                        opt(
                            "manually recruiting individual users — direct outreach, personal onboarding, and hand-holding",
                            correct=True,
                        ),
                        opt("a self-serve funnel with no human contact"),
                    ),
                    "Early on, recruiting users one at a time is faster than building scalable acquisition, and the direct contact is itself the best source of product feedback.",
                ),
                q(
                    "What is the most common B2B pricing mistake YC sees founders make?",
                    (
                        opt(
                            "Charging too little — pricing from cost or fear instead of the value delivered",
                            correct=True,
                        ),
                        opt("Charging too much and pricing out the market"),
                        opt("Using annual contracts instead of monthly"),
                        opt("Publishing prices on the website"),
                    ),
                    "Underpricing starves the company and signals a non-serious product. Price against the value created (and competitors' cost of the problem), then iterate upward.",
                ),
                q(
                    "Which single signal is the strongest evidence of product-market fit?",
                    (
                        opt("Total registered accounts"),
                        opt("Press coverage and social-media mentions"),
                        opt(
                            "Retention — cohort curves that flatten because users keep coming back (or revenue that keeps renewing)",
                            correct=True,
                        ),
                        opt("Winning startup pitch competitions"),
                    ),
                    "Acquisition can be bought and signups can be hyped; only retention shows the product delivers recurring value. Consumer and B2B metrics talks both anchor on it.",
                ),
                q(
                    "In the AI-native company talks, what do AI agents change about the traditional services business model?",
                    (
                        opt("Nothing — services still scale only by hiring more people"),
                        opt(
                            "Delivery work that used to require headcount can be done by software, giving services companies software-like margins and venture-scale potential",
                            correct=True,
                        ),
                        opt("AI removes the need to charge for services at all"),
                        opt("Agents make services companies cheaper to run but slower to grow"),
                    ),
                    "When agents do the delivery, revenue decouples from headcount — the reason YC now funds AI-native services companies it would once have passed on.",
                ),
                q(
                    "What is YC's core guidance for getting real leverage out of vibe coding?",
                    (
                        opt("Let the model ship whatever runs — reading the output slows you down"),
                        opt(
                            "Plan before prompting, keep changes small, review and test what the AI produces — you remain the engineer of record",
                            correct=True,
                        ),
                        opt("Only use it for throwaway prototypes, never production code"),
                        opt("Fine-tune your own model before using AI on your codebase"),
                    ),
                    "AI coding multiplies output, but unreviewed generated code compounds into unmaintainable systems; structure, small iterations, and review keep the speed without the debt.",
                ),
                q(
                    "How does a SAFE (Simple Agreement for Future Equity) work?",
                    (
                        opt("It is a loan that accrues interest until repaid"),
                        opt(
                            "The investor pays now and receives shares later, when a priced round converts it — typically subject to a valuation cap and/or discount",
                            correct=True,
                        ),
                        opt("It grants equity immediately at a negotiated share price"),
                        opt("It guarantees the investor a board seat"),
                    ),
                    "SAFEs defer the valuation negotiation: money in now, equity at the next priced round on cap/discount terms — the standard instrument for early fundraising.",
                ),
            ),
            duration="10 min",
        ),
    ),
)


STARTUPS_AGE_OF_AI_COURSES: tuple[SeedCourse, ...] = (_STARTUPS_AGE_OF_AI,)
