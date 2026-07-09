"""Academy seed content — Startups in the Age of AI.

A curated video course built on Y Combinator's Startup School playlist
(https://www.youtube.com/playlist?list=PLQ-uHSnFig5M9fW16o2l35jrfdsxGknNB).
The 29 talks are re-ordered from the playlist's reverse-chronological feed
into a curriculum arc — idea → team → building with AI → launch & customers
→ pricing & sales → metrics & fundraising. Every video lesson carries a
markdown companion body rendered below the player — a complete summary,
the main ideas, and a Mermaid mindmap of the talk, all grounded in its
transcript — and is followed by a checkpoint quiz; the welcome and
part-intro lessons carry checkpoint quizzes too, and the course closes
with a comprehensive final quiz.

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


def _yt(title: str, video_id: str, duration: str, body: str) -> SeedLesson:
    return video_lesson(
        title,
        f"https://www.youtube.com/watch?v={video_id}",
        duration=duration,
        body=body,
    )


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
        _yt(
            "Should You Start A Startup?",
            "BUE-icVYRFU",
            "17 min",
            """# Should You Start A Startup?

## Summary
Harj Taggar, a Y Combinator group partner, addresses people who do not feel ready to start a startup today but think they might someday, splitting the question into who is suited to being a founder and how to prepare. There is no simple test: after working with almost a thousand founders he is still surprised by who takes to startup life, and stereotypes like the ruthless brilliant programmer or the charismatic product genius mislead; success in school or at work also matters much less than he expected when he began reading YC applications in 2010. The quality that matters most is resilience, because convincing even a single user to care takes blood, sweat, and tears, and rejection feels personal in a way it does not at a big company. Confidence turns out to be a poor proxy for resilience: some of the quietest founders prove the most resilient, like Saji of Benchling, a softly spoken engineer whom investors doubted could sell to biotech companies; Benchling made no revenue for about two years after YC but is now worth over six billion dollars. Initial motivations matter less than people think, since wanting to get rich or simple curiosity are fine reasons to start and motivations change over time; what endures is genuine interest in the problem and love for the people you work with. His practical advice is to ask, literally, what do I have to lose: figure out the worst case, typically a year without salary before you know whether the startup is promising, and be honest about whether you can live with it, because constant anxiety will self-sabotage the effort. The analysis should also count how much you learn as a founder, doing sales, product, and customer support at once; startup experience improves careers even when startups fail, as employers at his startup Triplebyte explicitly sought ex-founders, Rippling employs around fifty former founders to run product divisions, and Nick Grandy went from a shut-down 2008 startup to being Airbnb's first employee to founding Outschool, now valued over three billion dollars. To prepare, treat finding an idea and a co-founder as one task: seek out smart people you enjoy discussing ideas with, join a startup to meet them, and turn moments of thinking someone should build X into launched side projects, learning just enough code for a version one. Citing Paul Buchheit, a few users who really love a crude prototype beat a million indifferent waitlist signups; if your day job drains you while side projects energize you, and a collaborator you love working with wants to build a company, make the jump.

## Main ideas
- **There is no founder test**: even after 15 years, YC partners are surprised by who thrives, and depictions in books and movies mislead.
- **Resilience matters most**, because getting the first users takes blood, sweat, and tears, and rejection at your own startup feels personal.
- **Confidence is a poor proxy**: quiet, softly spoken founders like Benchling's, who took two years to reach revenue, can be the most resilient.
- **Any starting motivation is fine**: wanting money or plain curiosity is enough, because motivations change and enduring ones come from the problem and the people.
- **Ask what you have to lose**: plan for the worst case of roughly a year without salary and be honest about whether you can live with it.
- **Founders learn fast**: doing sales, product, and support at once clarifies your career, and companies like Rippling actively hire former founders.
- **Careers are not linear**: Nick Grandy's failed startup led to being Airbnb's first employee and later founding Outschool.
- **Find ideas and co-founders together**: talk about ideas with smart people, join a startup to meet them, and launch side projects however small.
- **A few users who love it** beat a million indifferent waitlist signups, and when side projects energize you more than your job, make the jump.

## Mindmap
```mermaid
mindmap
  root((Starting A Startup))
    Who Is Suited
      No simple test
      Stereotypes mislead
      Resilience matters most
      Confidence poor proxy
      Benchling founders example
    Motivations
      Money is fine
      Curiosity is enough
      Motivations change over time
      Love problem and people
    Worst Case Thinking
      A year without salary
      Different for everyone
      Anxiety can self-sabotage
    Learning Payoff
      Try many work types
      Employers value ex-founders
      Rippling hires former founders
      Careers are not linear
    Preparing Yourself
      Idea plus co-founder together
      Talk with smart people
      Join a startup
      Launch side projects
      Learn enough to code
    When To Leap
      Few users who love
      Energy over traction
      Great collaborator ready
```
""",
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
        _yt(
            "How to Get and Evaluate Startup Ideas",
            "Th8JoIan4dg",
            "32 min",
            """# How to Get and Evaluate Startup Ideas

## Summary
This talk gives founders conceptual tools for thinking about startup ideas the way YC does, drawing on an analysis of how the top 100 YC companies found their ideas, Paul Graham's essay How to Get Startup Ideas, experience helping YC startups pivot, and thousands of rejected applications. Jared first covers four common mistakes. The worst is building a solution in search of a problem, such as deciding AI is cool and then hunting for something to apply it to, which yields made-up problems nobody cares about; instead, fall in love with a specific, high quality problem. Second are tar pit ideas: widespread, plausible-seeming problems like an app for making plans with friends, which have trapped founders for twenty years because structural difficulties make them far harder than they look; at minimum, Google your idea and talk to people who tried it. The remaining mistakes are opposites: jumping on the first idea without asking whether it is a business, and waiting forever for a perfect idea that does not exist, since ideas are starting points that morph anyway. He then offers ten questions for evaluating any idea: founder-market fit, the most important criterion, illustrated by PlanGrid's construction-expert and developer team; market size, either big now or small and fast growing like Coinbase's 2012 bitcoin market; problem acuity, like Brex offering credit cards startups literally could not get; competition, which counter-intuitively is usually good; whether you or people you know want it; whether it only recently became possible or necessary, like Checkr's background check API riding the delivery boom; proxies, such as DoorDash validating Rappi; willingness to work on it for years; scalability, which pure software gets for free; and whether it sits in a fertile idea space, since fintech infrastructure and vertical SaaS have had far higher hit rates than consumer hardware or ad tech, as Fivetran's repeated pivots within data tooling show. Three qualities make ideas look bad but actually good: being hard to start, like Stripe and schlep blindness; being boring, like Gusto's payroll software; and having existing competitors, like Dropbox entering as roughly the twentieth player with a real insight about syncing through the operating system. Finally, at least 70 percent of top YC companies found their ideas organically, so become an expert, work at a startup, or build interesting things like Replit; otherwise use his seven recipes, from leveraging team expertise like Rezi to systematically interviewing an industry the way AtoB did at truck stops, and when still unsure, just launch and find out.

## Main ideas
- **Fall in love with a problem**: the most common mistake is a solution in search of a problem that users do not really care about.
- **Avoid tar pit ideas**: common, plausible ideas like friend meetup apps have structural reasons they have stayed unsolved for twenty years.
- **Ideas are starting points**: do not grab the first idea or wait for a perfect one, because any good idea will morph.
- **Founder-market fit comes first**: pick an idea your team is unusually suited to execute, like PlanGrid's construction and engineering founders.
- **Markets can be small but growing**: Coinbase started in a tiny 2012 bitcoin market that would clearly be huge if bitcoin succeeded.
- **Competition is usually good**: Dropbox was roughly the twentieth entrant but won with an insight all the incumbents had missed.
- **Bad-looking ideas can be great**: hard-to-start ideas like Stripe, boring ones like Gusto payroll, and competitive spaces get left on the table for smarter founders.
- **Organic ideas win most**: at least 70 percent of top YC companies found ideas organically, so become an expert, join a startup, or build interesting things.
- **Systematic search can work**: AtoB picked trucking as a fertile idea space and interviewed drivers at truck stops until they found fuel cards.
- **Just launch**: the only way to know for sure whether a startup idea is good is to launch it and find out.

## Mindmap
```mermaid
mindmap
  root((Startup Ideas))
    Common Mistakes
      Solution seeking a problem
      Tar pit ideas
      Jumping on first idea
      Waiting for perfect idea
    Evaluating Ideas
      Founder market fit
      Big or growing market
      Acute problem
      New enabling change
      Fertile idea space
    Deceptively Good Ideas
      Hard to start
      Boring spaces
      Existing competitors
    Organic Ideas
      Most top ideas organic
      Become an expert
      Work at a startup
      Build interesting things
    Idea Recipes
      Use team expertise
      Problems you encountered
      Things you wish existed
      Recent world changes
      Talk to an industry
    Final Advice
      Launch to find out
      Execution beats the idea
```
""",
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
        _yt(
            "Pick One Idea and Go Deep",
            "R56RJFZBasQ",
            "12 min",
            """# Pick One Idea and Go Deep

## Summary
John, a partner at YC, addresses founders who juggle several ideas or wait for the best one before committing, offering a rubric to stop overthinking, pick an idea, and figure out fast whether it is working. He first names two common overthinking failure modes. The first is searching for the perfect idea, which is impossible to identify in the abstract because you can only learn what to work on by making contact with reality and getting customer feedback. The second is asking whether you are the perfect founder for the idea: founder-market fit matters, but founders — especially second-time founders — weaponize it against themselves, convinced they need a decade of domain experience. He cites Blake Scholl, who worked on ad tech at Amazon and Groupon before founding Boom Supersonic, now a billion-dollar company. Next, he argues for committing to exactly one idea. Working on multiple ideas at once produces bad data: without going deep you get weak signal, so you may prematurely abandon a good idea or persist with a bad one. Going deep means burning the other boats — explicitly foreclosing the alternatives, telling customers you have pivoted — and should feel like wearing a new skin: changing the company name, emails, website, and internal narrative. GovDash, which helps customers win government contracts, pivoted at least five times and changed its name and email addresses each time; its fifth idea worked so well the team could barely keep up with demand and recently raised a Series B. The high watermark for depth is whether you could actually run your customer's business — knowing their daily crises, whether the problem is top five, and what they would pay to solve it — or teach a class on the problem. Rather than obsessing over hundreds of interviews before writing code, run a tight loop of customer understanding and product delivery. He then describes three qualities of good ideas in the AI era: they sit at the edge of what models can do today and improve as models improve; they verticalize by selling an outcome — be the insurer or the bank, like Corgi Insurance, which acquired an insurance carrier during its YC batch to own the full commercial insurance stack; and they are the most ambitious version of themselves, since ambitious and modest startups cost roughly the same. Even if the idea fails, you gain unambiguous customer data, conviction for a pivot, and often the better idea underneath. The worst failure mode is not being wrong but never deciding.

## Main ideas
- **Do not overthink the choice**: the perfect idea cannot be identified in the abstract; only contact with reality and customer feedback reveals what you should work on.
- **You do not need a decade of experience**: founder-market fit is often weaponized as self-doubt, yet Blake Scholl went from ad tech at Amazon and Groupon to building Boom Supersonic.
- **Multiple ideas produce bad data**: juggling ideas yields weak signal, so you may quit a good idea early or keep a bad one alive.
- **Burn the other boats**: explicitly foreclose alternatives, tell customers you pivoted, and change your name, emails, website, and internal narrative — like GovDash did through five pivots.
- **The run-their-business test**: you have gone deep enough when you could run your customer's business tomorrow or teach a class on the problem.
- **Work in a tight loop**: alternate deep customer understanding with product delivery instead of collecting hundreds of interviews before writing code.
- **Build at the model frontier**: good AI-era ideas barely work on today's frontier models and clearly improve as the models get better.
- **Verticalize and sell outcomes**: as software costs go to zero, value shifts to trust, licenses, and outcome ownership — be the insurer, not software for insurers, like Corgi Insurance.
- **Choose the most ambitious version**: ambitious and modest startups are equally hard, but the ambitious one attracts talent, deters competitors, and builds a moat.
- **Failure still pays**: a failed deep dive leaves you with unambiguous data and usually reveals the better structural problem underneath.

## Mindmap
```mermaid
mindmap
  root((Pick One Idea))
    Stop Overthinking
      No perfect idea exists
      Contact with reality
      Founder fit not required
      Boom Supersonic example
    Commit To One
      Multiple ideas give bad data
      Burn the other boats
      Wear a new skin
      GovDash pivoted five times
    Go Deep Test
      Run the customers business
      Teach a class on it
      Tight loop with product
    Good AI Era Ideas
      Edge of model ability
      Verticalize and sell outcomes
      Be the insurer
      Most ambitious version
    If It Fails
      Unambiguous customer data
      Conviction for a pivot
      Better idea underneath
```
""",
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
        _yt(
            "Starting a Company? The Key Terms You Should Know",
            "wH3TKpALlw4",
            "18 min",
            """# Starting a Company? The Key Terms You Should Know

## Summary
Dalton, a managing partner at Y Combinator, walks through common startup terminology. He starts with MVP, stressing that the keyword is viable: a product must be useful enough to serve some purpose for a customer, not merely simple. Venture capital invests small amounts for equity in risky startups hoping a few huge winners repay the whole portfolio many times over; he traces the model to the whaling industry, where backers funded multiple ships so one successful hunt paid for the failed expeditions. Angel investors are early-stage individuals writing smaller personal checks, say $20,000 or $50,000, usually not as a full-time job. Profitability means making more than you spend, but founders should study how margins change with scale: Google made no revenue for its first few years, yet online advertising's high margins made it enormously profitable once monetization turned on. Burn rate is how much the bank account drops each month, so $1 million falling to $900,000 means a $100,000 burn, and ignoring it can put you out of business.

A seed round is loosely the first meaningful money a startup raises, anywhere from $300,000 on a safe to a celebrity-founded company raising $100 million on a billion-dollar valuation. Series A, B and C rounds typically involve a lead investor who may take a board seat and around 20% ownership in an A. Product-market fit means people use and love what you built, and getting more customers is no longer your biggest problem; priorities differ sharply between the pre- and post-PMF modes. Bootstrapping means building from personal funds and revenue without venture capital, a great option for businesses likely to reach around $5-10 million a year and not grow far beyond that.

Convertible notes are debt-like instruments that may carry interest or repayment terms, while the SAFE, created at Y Combinator by Carolyn Levy, is a simpler alternative with fewer terms; either way, read the fine print. Equity is ownership in the company; employees often receive stock options instead, a right to future equity. TAM, total addressable market, is a thought experiment about how big the market could be, and it can badly underestimate reality, as with Tesla and Uber, whose products grew their own markets. Valuation reflects what the last investor paid rather than a liquid market price, and highly valued startups do not always succeed. An IPO sells shares to public markets like NASDAQ or the New York Stock Exchange, providing liquidity for founders, employees and investors. Finally, ARR is annual recurring revenue, so ten $100,000 yearly contracts equal $1 million of ARR, while monthly subscriptions are quoted as MRR.

## Main ideas
- **Viable is the key word in MVP** — a minimum product must still be useful enough to serve some purpose for a customer, not just simple.
- **Venture capital is a portfolio bet** — a few huge winners like Google or Facebook pay for all the failures, a model dating back to whaling expeditions.
- **Angel investors write personal checks** — typically $20,000 to $50,000 of their own money, as a hobby or side activity rather than a full-time job.
- **Watch margins and burn rate** — profitability at scale matters more than early losses, and a bank balance dropping $100,000 a month is a burn rate you must control.
- **Round names are loose conventions** — a seed round is the first meaningful money raised, while Series A, B and C usually add a lead investor, a board seat and roughly 20% ownership.
- **Product-market fit changes your job** — before PMF you test assumptions and talk to customers; after PMF you focus on keeping it while growing and scaling.
- **Bootstrapping suits non-venture businesses** — funding growth from personal money and revenue keeps full control and fits companies aiming at $5-10 million a year.
- **Read the fine print on instruments** — convertible notes are debt-like with interest terms, while the YC-created SAFE has fewer terms; know whether you hold equity or stock options.
- **TAM is a thought experiment** — total addressable market estimates can be wildly wrong, as Tesla and Uber grew their markets far beyond initial calculations.
- **ARR requires actual recurrence** — ten $100,000 annual renewing contracts equal $1 million ARR, and monthly billing should be quoted as MRR instead.

## Mindmap
```mermaid
mindmap
  root((Startup Key Terms))
    Product Terms
      MVP must be viable
      Product market fit modes
      TAM thought experiment
    Investors
      Venture capital portfolios
      Angel personal checks
      Whaling industry origin
    Fundraising Rounds
      Seed first money raised
      Series A lead investor
      Valuation not liquid
      IPO public shares
    Instruments
      Convertible note debt
      SAFE created by YC
      Equity and stock options
      Read the fine print
    Money Metrics
      Profit margins at scale
      Burn rate watch closely
      ARR recurring yearly
      MRR monthly billing
```
""",
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
        _yt(
            "How To Find A Co-Founder",
            "Fk9BCr5pLTU",
            "21 min",
            """# How To Find A Co-Founder

## Summary
Harj Taggar, a YC group partner, covers why you need a co-founder, when to start without one, what to look for, where to find one, and how to keep the relationship healthy. He gives three reasons to have one: startups involve an enormous amount of work, and a co-founder with complementary skills doubles working hours, challenges your ideas, and raises the quality of your work; the emotional roller coaster of moments where you think you will take over the world followed by moments where you are convinced you are about to die needs support from someone equally all-in; and pattern matching, since the most successful startups had co-founding teams, from Facebook, which Mark Zuckerberg co-founded with Dustin Moskovitz, to Apple, where Steve Jobs literally could not have built the first computer without Steve Wozniak. In 90% of cases you should spend your effort finding a co-founder first; the 10% exception is when you have a specific idea you are passionate about, domain experience that uniquely qualifies you, and engineering skills to build alone. Drew Houston applied to YC as a single founder with Dropbox, was initially rejected, kept building, and brought on Arash as a co-founder.

The most important trait in a co-founder is handling stress well, since failed co-founder relationships are the number one reason startups fail at YC; the best test is having already worked together under stress, which friendships and big-company jobs often never provide. Co-founders also need the same high-level goals, a fast-growing venture-backed company versus a lifestyle business, so ask directly why they want to start a company and what success looks like. Don't fixate on today's specific skills; care about trajectory, intelligence, and willingness to learn as the startup grows.

To find co-founders, cultivate potential partners through projects long before starting, and never assume people you know are unavailable: always make the ask, and if they decline, ask who they would pick as a co-founder and get an introduction. Hackathons, open-source work, developer meetups, and YC's co-founder matching platform also help, where the matches that work best look like people who would have met anyway. If you don't know each other well, have a dating period of evening and weekend projects, and once committed, split equity equally, since ten or more years of future work dwarfs early contributions. Breakups stem from lost respect between sales and technical co-founders, multiple people wanting to be CEO, and mismatched work-ethic expectations. Prevent them by never delaying hard conversations and holding regular monthly one-on-ones to release pressure gradually.

## Main ideas
- **Startups are too hard alone** — a co-founder adds working hours, complementary skills, and someone smart to challenge bad ideas and surface good ones.
- **Emotional support is essential** — only someone equally all-in can bring you up during the moments you are convinced the startup is about to die.
- **Successful startups pattern-match to teams** — Facebook had Zuckerberg and Moskovitz, and Jobs could not have built the first Apple computer without Wozniak.
- **Going solo is a rare exception** — only about 10% of cases qualify, requiring a specific idea, unique domain experience, and the engineering skill to build it yourself, as Drew Houston did with Dropbox.
- **Stress handling is the top trait** — failed co-founder relationships are the number one reason YC startups fail, and only working together under stress reveals it.
- **Align on high-level goals** — a founder chasing a fast-growing venture-scale company will clash with one wanting a slow, steady lifestyle business.
- **Trajectory beats current skills** — what matters is whether a co-founder is smart, adaptable, and able to grow with the startup, not their exact technical stack today.
- **Always make the ask** — never assume people you know are unavailable, and when someone declines, ask who they would pick and get introduced.
- **Split equity equally** — over ten or more years of work, early differences in contribution become insignificant, and equal ownership keeps both founders invested.
- **Never delay hard conversations** — postponed disagreements build up like death by a thousand cuts, so hold regular monthly one-on-ones to release pressure.

## Mindmap
```mermaid
mindmap
  root((Finding A Co-Founder))
    Why Co-Founders
      More work done
      Complementary skills
      Emotional support
      Successful teams pattern
    Going Solo
      Rare 10 percent exception
      Passion plus domain expertise
      Dropbox Drew Houston example
    What To Look For
      Handles stress well
      Shared high level goals
      Trajectory over skills
    Where To Find
      Always make the ask
      Projects with friends
      Hackathons and meetups
      YC matching platform
    Working Together
      Dating period first
      Split equity equally
    Avoiding Breakups
      Respect each other
      One CEO only
      Aligned work ethic
      Regular one-on-ones
```
""",
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
        _yt(
            "Keys To Successful Co-Founder Relationships",
            "A4SLDQDXdp0",
            "32 min",
            """# Keys To Successful Co-Founder Relationships

## Summary
Kat, who leads YC's startup school team, and visiting group partner Divya cover the full co-founder lifecycle: what a co-founder is, where to find one, how to evaluate them, and how to work together. A co-founder starts the company with you — YC counts anyone with at least 10 percent equity. Solo founding is possible but really hard; co-founders bring productivity, higher-quality brainstorming, accountability, and moral support through the ups and downs. Empirically, Microsoft had Paul Allen, Apple had Steve Wozniak plus a third founder, Ronald Wayne, Facebook had four co-founders besides Zuckerberg, and only four of YC's top 100 companies were solo-founded — and those founders could all make progress alone. To find one, look to friends, classmates, and colleagues, and test the relationship with a project first; YC's co-founder matching platform, with 40,000 profiles and 100,000 matches, adds filters, messaging, and a speed-dating feature. Success stories include Sequin, whose founders matched perfectly on paper (a Visa PM building credit tools for women and a PayPal engineer who cared about gender equity), met daily for a week, and raised 5.7 million dollars, and Kiwi Biosciences, whose founders worked through a 50-question questionnaire and a month-long trial before committing and raising 1.5 million. Platform tips: fill out your profile completely, brag rather than be humble, and meet fast — 70 percent of meetings happen within two weeks of matching. Evaluating a co-founder is like evaluating a marriage: align early on goals and values, stress handling, communication, finances, and commitment. Complementary skills are overrated since fundraising, marketing, and sales are learnable, but non-technical founders should find a technical co-founder or learn to code rather than hire a dev shop, which is costly and cannot iterate. Split equity equally by default: ideas are cheap, all the work is ahead, and outcomes are bimodal, so do not jeopardize the relationship over a few percent. Working together depends on expectations and trust: Divya's four-founder first startup was blindsided when one founder's unspoken timeline for going viral led him to quit, and unspoken salary needs pushed them toward lowball acqui-hire offers. Trust people by default, communicate early when you will miss commitments, create space for mistakes, and spend time physically together. Avoid consensus decision-making and missing titles — name a CEO, define ownership areas, and set accountability structures. Know each other's stress styles (attack versus retreat), hold regular one-on-ones with bi-directional feedback, take hard conversations early, consider a coach, avoid personal attacks, and disagree and commit — you are on the same team.

## Main ideas
- **Co-founders multiply your odds**: they bring productivity, better brainstorming, accountability, and moral support, and only four of YC's top 100 companies had a solo founder.
- **Famous solo founders were not solo**: Microsoft, Apple, and Facebook all had multiple co-founders, including Apple's little-known third founder Ronald Wayne.
- **Find co-founders through work, not just talk**: try friends, classmates, and colleagues, and run a trial project — someone willing to build on weekends is good co-founder material.
- **Co-founder matching works at scale**: YC's platform has 40,000 profiles and crossed 100,000 matches, and over a dozen matched teams have been accepted into YC.
- **Sell yourself on your profile and meet fast**: brag about accomplishments, show progress you made alone, and note that 70 percent of meetings happen within two weeks of matching.
- **Align early on the marriage-level questions**: goals, stress handling, communication, finances, and commitment matter more than complementary skills, which are learnable.
- **Do not hire a dev shop**: they are expensive, cannot iterate with changing requirements, and do not care about your users — get a technical co-founder or learn to code.
- **Split equity equally by default**: ideas are cheap, the work is all ahead, and squeezing a co-founder breeds resentment in a bimodal-outcome game.
- **Trust by default and communicate expectations**: unspoken timelines and salary needs blew up Divya's first startup, and micromanagement destroyed another team overnight.
- **Structure decision-making**: consensus and no titles lead to gridlock, so name a CEO, define ownership areas, hold one-on-ones with feedback, and disagree and commit.

## Mindmap
```mermaid
mindmap
  root((Co-Founder Keys))
    Why A Co-Founder
      Productivity and brainstorming
      Accountability and moral support
      Top companies had several
    Finding One
      Friends classmates colleagues
      Trial projects together
      YC matching platform
    Evaluating Fit
      Like a marriage
      Align goals and finances
      Technical co-founder matters
    Splitting Equity
      Default to equal
      Ideas are cheap
      Avoid future resentment
    Working Together
      Set expectations early
      Trust by default
      Name a CEO
      Disagree and commit
```
""",
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
        _yt(
            "Co-Founder Equity Mistakes to Avoid",
            "DISocTmEwiI",
            "20 min",
            """# Co-Founder Equity Mistakes to Avoid

## Summary
Michael Seibel scopes his advice to VC-funded tech software startups at the very beginning, pre-product-market fit. The core message: be generous with co-founder equity. Equity exists to keep the founding team motivated through the first couple of years when things look like they are not working, and the biggest mistake is being stingy during this delicate time, causing people to leave while something big is still possible. Both the "Jedi" founder and the "dumb" founder split generously; only the midwit runs complicated calculations over skill sets, contributions, time commitments, and networks. Since founder equity typically vests over four years, a CEO must think about what keeps a co-founder motivated in years two, three, and four, not just what they will accept today, so YC recommends close-to-equal splits.

Vesting and cliffs should apply to all founders: four-year vesting with a one-year cliff is standard, and equity distribution is not something to innovate on. Life happens — people get sick, family circumstances change, people underperform — and vesting with a cliff lets founders leave or be let go without destroying the cap table. Co-founders must be essential: the founding team is the smallest group that can build an MVP and get it to customers, and teams arriving at YC with five, six, or seven co-founders signal a conversation that never happened. The CEO must retain the ability to fire non-performing founders, and responsible teams discuss breakups upfront. YC's guidelines: a founder leaving before the one-year cliff keeps only a token amount of equity; after the cliff but pre-product-market fit they should retain no more than 5% of the company, often giving equity back so it can motivate the people still building; one to three months of severance is reasonable if fired; and every departing founder should resign from the board, sign a release, and grant proxy voting rights to the remaining founders.

He then dismantles common justifications for lopsided splits: "my co-founder agreed" (optimizing for today, not year three), "it was my idea" (YC sees almost 30,000 applications every six months; ideas are a dime a dozen and execution is the game), "I started six months earlier" (99% of the work remains on a potentially 10-to-30-year journey), "they need a salary and I don't" (salary covers living, equity drives motivation), "I'm older and more experienced," and "I hired them after raising money or after launch" — all flavors of short-term thinking. Bad advice includes performance-based equity, part-time founders (not really founders), and dynamic equity schemes; vesting and cliffs are the real protection. Even when one founder, like Bezos or Zuckerberg, stays longest, the early co-founders supplied the activation energy the company needed to be in the game at all.

## Main ideas
- **Be generous with co-founder equity** — Equity's job is to keep the founding team working extremely hard through the years when things look like they are failing.
- **Motivate for all four years** — A CEO should ask what keeps a co-founder excited in year three when everything sucks, not what they will agree to today.
- **Close-to-equal splits** — Splits do not have to be exactly equal, but the more generous you are, the more a strong founder stays motivated.
- **Always use vesting and cliffs** — Four-year vesting with a one-year cliff is the standard protection, and equity distribution is not an area to innovate on.
- **Co-founders must be essential** — The founding team is the smallest number of people who can build an MVP and get it to customers, so the title should not be handed out freely.
- **Breakup guidelines exist** — Before the cliff a departing founder keeps a token amount; after the cliff pre-product-market fit they should retain no more than 5% and resign the board, sign a release, and grant proxy voting rights.
- **Ideas are a dime a dozen** — Seeing nearly 30,000 YC applications every six months shows execution, not the idea, is the game, so "it was my idea" does not justify 90/10.
- **Salary and equity are different tools** — Salary is what someone needs to live; equity is what motivates them to work extremely hard, so never trade one for the other.
- **Avoid fancy schemes** — Performance-based equity, part-time founders, and dynamic agreements fail because early goals are unknowable and motivation needs certainty.
- **Early years create the value** — Most companies die in the first four to six years, so co-founders who provide that activation energy deserve generosity even if one founder stays longest.

## Mindmap
```mermaid
mindmap
  root((Co-Founder Equity))
    Core Advice
      Be generous with equity
      Motivate for four years
      Near equal splits
    Vesting And Cliffs
      Four year vesting
      One year cliff
      Do not innovate here
      Protects the cap table
    Breakup Guidelines
      Token equity before cliff
      Max five percent after
      Severance if fired
      Resign board sign release
    Bad Reasons
      My co-founder agreed
      It was my idea
      I started earlier
      Salary versus equity
      Experience or funding timing
    Bad Advice
      Performance based equity
      Part-time founders
      Dynamic equity schemes
    Long Term View
      Early years create value
      Co-founders are activation energy
```
""",
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
            "The Startup Playbook for Hiring Your First Engineers and AEs",
            "i_PjjXKNpA4",
            "43 min",
            """# The Startup Playbook for Hiring Your First Engineers and AEs

## Summary
David Paffenholz, co-founder and CEO of Juicebox — an AI sourcing platform backed by Sequoia and used by Ramp, Cursor, and Perplexity — presents a playbook for sourcing and hiring your first engineers and account executives, followed by a discussion with Harj. He opens by stressing that early hires define the culture, velocity, and future of the business: culture is set by the first 10 people and the next 40 after that, and Juicebox itself put deep thought into its first and second tens. Hiring is brutally competitive — engineers are flooded with recruiter outbound — so your message must stand out. Candidates weigh three buckets: big tech, with strong compensation and stability but slower pace; growth-stage companies like Stripe, OpenAI, and Anthropic, with predictable upside but layers of structure; and startups, offering the chance to shape culture and product with the largest equity grants and highest variance. Figure out each candidate's leaning early, then pitch why your startup specifically: mission, equity upside, a hard problem space, or culture and team. He covers three candidate sources: referrals, including reviewing a new hire's connections on day one and paying $10-20K referral bonuses; job distribution, like Work at a Startup, where Juicebox made its first hire, with short, opinionated job descriptions that spend at least 30% selling the company; and sourcing, which he treats as outbound sales — prospecting, cold outreach, and pipeline tracking. For AEs, look for experience selling to the same buyer persona, quota attainment signals like President's Club and 100%+ attainment, and fast promotions within one company; for engineers, exploit founder-specific advantages (David reached out to fellow Germans in the Bay Area), open-source contributions, personal projects, and communities like Discord and GitHub. Outreach should be personalized, multi-step, and multi-channel: automated emails plus manual LinkedIn touches, kept short with a clear call to action. Juicebox's own pre-Series A campaigns got 10-18% reply rates; 10-20% is good, some customers reach 40%+ through five-minute-per-message personalization, and the interested rate — roughly half of replies — is the metric that matters. Make sourcing a scheduled commitment: around 100 emails weekly (he does Sunday evenings), 10 candidate conversations a week, with every founder involved. In interviews, sell first and interview second — skipping the sell is the top founder mistake; AEs do mock demos while founders role-play the customer, engineers get cheat-resistant case studies and a six-hour on-site. Close with speed, running the process in 7 to 14 days, and remember hiring is a repeated game — one candidate joined six months after declining. Bring in contract, contingency (20-25% fees), or in-house recruiters once you are hiring more than two roles at a time.

## Main ideas
- **Early hires define the company**: culture, velocity, and trajectory are shaped by the first 10 people and the next 40, so who they are matters as much as speed.
- **Candidates weigh three buckets**: big tech offers comp and stability, growth-stage offers predictable upside with structure, and startups offer ownership, impact, and high-variance equity.
- **Know why your startup specifically**: pitch one or two of mission, equity upside, hard problem space, or culture and team, varying by candidate.
- **Sourcing is outbound sales**: proactively find candidates who are not applying, run prospecting, cold outreach, and pipeline tracking just like early sales.
- **Signal-based targeting works**: for AEs look for quota attainment, President's Club, and fast in-company promotions; for engineers look at open source, side projects, and shared background.
- **Personalization drives response rates**: 10-20% reply rates are good, and customers hitting 40%+ spend up to five minutes personalizing each message; watch the interested rate, roughly half of replies.
- **Founders must send the outreach**: the more senior the sender, the better the response, and the technical founder should personally reach out to engineering candidates.
- **Commit to a schedule**: send around 100 sourcing emails per week and aim for 10 candidate conversations weekly, with every founder participating.
- **Sell before you interview**: the number one founder mistake is jumping into assessment; the first call should sell the company and gather the candidate's selling points.
- **Speed and persistence close offers**: run the whole process in 7 to 14 days, personalize the offer, enlist investors to reach out, and remember hiring is a repeated game.

## Mindmap
```mermaid
mindmap
  root((First Startup Hires))
    Why Hires Matter
      First 10 define culture
      Hiring is competitive
      Candidates weigh three buckets
      Sell your unique story
    Finding Candidates
      Referrals with bonuses
      Post on job boards
      Sourcing like outbound sales
      AE quota signals
      Engineer community signals
    Outreach Campaigns
      Personalized multi step emails
      Manual LinkedIn touches
      Founders send the outreach
      Track interested rate
    Making It Happen
      100 emails weekly
      Ten candidate calls weekly
      All founders involved
    Interviews And Offers
      Sell before interviewing
      Mock demos and case studies
      Move fast on offers
      Hiring is repeated game
    Recruiter Options
      In house recruiter
      Contract embedded recruiter
      Contingency percentage fees
      Help beyond two roles
```
""",
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
        _yt(
            "How To Build A Company With AI From The Ground Up",
            "EN7frwQIbKc",
            "10 min",
            """# How To Build A Company With AI From The Ground Up

## Summary
Diana, a partner at YC, argues that AI will not just change how quickly software gets built — it will fundamentally change how startups are run, from what roles exist to what products are possible. Most people frame AI in terms of productivity, adding copilots to existing workflows to ship more features, but that framing misses the shift: this is about entirely new capabilities, where the right person with AI tools can build features that used to require a whole team or were simply impossible. Her high-level principle is that AI should not be a tool the company uses but the operating system the company runs on, with every workflow, decision, and process flowing through an intelligent layer that constantly learns and improves. Concretely, every important process should be captured by an intelligent closed loop. Borrowing from control systems, she notes that companies historically ran as lossy open loops — decisions were made and executed without systematically measuring outcomes — whereas closed loops continuously monitor output and self-correct. Building them requires making the entire company queryable and legible to AI: every important action should produce an artifact, meetings should be recorded with AI note-takers, DMs and emails minimized, agents embedded across communication channels, and custom dashboards built covering revenue, sales, engineering, hiring, and ops. Her concrete example is sprint planning: an agent with access to Linear tickets, Slack engineering channels, customer feedback from email, Pylon, and GitHub, Notion plans, and stand-up recordings can analyze what actually shipped and propose far more accurate sprint plans; she has seen teams cut sprint time in half and get close to 10x more done. The governing principle is to give models as much context as you would give an employee. She then describes AI software factories, the next evolution of test-driven development: humans write specs and tests defining success, and agents generate and iterate on code until tests pass — some repos contain no hand-written code, and Strong DM's team built a factory where scenario-based validations drive agents to a probabilistic satisfaction threshold, realizing Steve Yegge's 1000x engineer. One implication is that classic management hierarchy no longer makes sense: the intelligence layer replaces human middleware that routed information. Citing Jack Dorsey at Block, she outlines three employee archetypes — the IC builder-operator, the DRI owning one outcome, and the AI founder leading from the front. Companies should maximize token usage rather than headcount, running an uncomfortably high API bill instead of inflated teams. Founders cannot outsource conviction — they must sit with coding agents until their priors break — and early-stage startups, free of legacy systems and org charts, can operate 1,000 times faster than incumbents.

## Main ideas
- **New capabilities, not productivity**: the shift is not faster engineers but one person with AI tools building what used to take an entire team or was impossible.
- **AI as the operating system**: AI should not be a tool the company uses but the layer every workflow, decision, and process flows through.
- **Run the company as closed loops**: unlike lossy open loops, closed loops capture outcomes, feed them back to intelligent systems, and improve processes over time.
- **Make the organization queryable**: every important action should produce an artifact — recorded meetings, minimized DMs, embedded agents, and dashboards for everything.
- **Context equals capability**: give models as much context as you would give an employee, as in the sprint-planning agent with access to Linear, Slack, Pylon, GitHub, and Notion.
- **AI software factories**: humans write specs and tests, agents write and iterate the code until tests pass — some repos contain no hand-written code at all.
- **No human middleware**: with a queryable, artifact-rich company, the intelligence layer replaces middle managers, and every removed routing layer is a direct speed gain.
- **Three employee archetypes**: Jack Dorsey's model of the IC builder-operator, the DRI responsible for one outcome, and the AI founder leading by example.
- **Token maxing over headcount**: run an uncomfortably high API bill, because one person with AI tools replaces a far more expensive team.
- **Startups have the edge**: no legacy systems, entrenched org charts, or retraining burden means new companies can be built AI-native from day one and operate 1,000x faster.

## Mindmap
```mermaid
mindmap
  root((AI Native Company))
    New Capabilities
      Not just productivity
      One person builds features
      AI as operating system
    Closed Loops
      Open loops are lossy
      Feedback improves process
      Self regulating systems
    Queryable Company
      Every action leaves artifacts
      AI note takers
      Dashboards for everything
      Sprint planning agents
    Software Factories
      Specs and tests first
      Agents write the code
      Strong DM example
      The 1000x engineer
    Flat Organization
      No human middleware
      IC DRI and founder
      Token maxing over headcount
    Startup Advantage
      No legacy systems
      Build right from day one
      Faster than incumbents
```
""",
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
        _yt(
            "How to Build an AI-Native Services Company",
            "gSNFJbgoaHI",
            "11 min",
            """# How to Build an AI-Native Services Company

## Summary
This talk argues that some of the biggest companies of the next decade will not be software businesses at all but AI-native services companies — insurance carriers, law firms, and tax or audit practices rebuilt from scratch with AI doing most of the work — in markets worth trillions of dollars. The playbook is aimed at founders starting from scratch. On picking a market, beyond loving the customers, market, or technical problem enough for a decade, the best AI services markets share four traits: low trust, meaning the work is already outsourced and the customer only cares about the final product, so you displace a vendor rather than change behavior; low judgment at the task level, so most steps are automatable with humans in the loop at a few points; a high intelligence threshold, where the work is hard enough that models plus humans are needed; and regulation, which raises the bar and the moat — Panacea, a current YC company, pairs experienced FDA consultants with an AI platform to deliver faster FDA approvals. Founders should apply the Sam Altman test — does your service get stronger as models improve, or do they commoditize you — avoid anything involving equipment and onsite labor, and honestly ask whether humans are there for genuine judgment or to paper over product gaps. On teams, the best founders combine domain fluency, model fluency, and operational rigor; the general legal team, an AI-native law firm YC backed, mixes Cooley and Fenwick law firm experience with CaseText technical leadership and uses shift work to cut cycle times. On product, the setup inverts software: the human is the interface and the product scales their work non-linearly, so throughput and cycle time become product metrics to track like daily active users, and variance is the existential problem because inconsistency destroys trust and causes churn — automating the process is the product. On sales, avoid the early demand trap by capping pilot customers to a small handful, sell outcomes rather than seats or tokens, and price against labor with per-unit or outcome-based pricing while avoiding cost-plus and straight-line undercutting. The P&L walkthrough stresses obsessing over COGS — model costs, hosting, and humans in the loop each need a number, a trend line, and an owner — and the core bet of AI operating leverage: traditional services top out around 30% margins, but these companies can approach software margins of 50% plus on markets two to three times bigger. Finally, do not buy your way in: you cannot acquire product-market fit, and the only decent reason is a fast regulatory moat.

## Main ideas
- **Services rebuilt with AI are the opportunity**: instead of selling copilots, AI-native companies deliver the outcome itself in trillion-dollar markets like tax, audit, insurance, and law.
- **Four traits mark good markets**: low trust in already-outsourced work, low judgment at the task level, a high intelligence threshold, and regulation that raises the moat.
- **The Sam Altman test**: ask whether better models make your service stronger or commoditize you, and only build in the first camp.
- **Teams need three fluencies**: domain fluency for credibility with skeptical buyers, model fluency to ride the capability curve, and operational rigor because the product is an operation.
- **The human is the interface**: unlike software, the product's job is to scale humans non-linearly, so throughput and cycle time are product metrics tracked like daily active users.
- **Variance is the existential problem**: customers fire you for inconsistent output faster than for being slower or more expensive than incumbents.
- **Avoid the early demand trap**: cap the first pilot customers to a small handful or humans will drown you and the product will never get built.
- **Price on value against labor**: per-unit and outcome-based pricing work, while cost-plus permanently caps upside and straight-line undercutting makes work seem cheap.
- **Obsess over COGS from day one**: model costs, hosting, and humans in the loop each need a number, a trend line, and an owner, because AI operating leverage is the whole bet.
- **Build, do not buy**: acquiring a legacy services business almost never works because you cannot acquire product-market fit; the exception is a needed regulatory moat.

## Mindmap
```mermaid
mindmap
  root((AI Native Services))
    Picking The Market
      Low trust outsourced work
      Low judgment per task
      High intelligence threshold
      Regulation as a moat
      Sam Altman test
    Founding Team
      Domain fluency
      Model fluency
      Operational rigor
    Building The Product
      Human is the interface
      Throughput as product metric
      Variance destroys trust
      Automate the process
    Sales And Pricing
      Avoid early demand trap
      Sell outcomes not seats
      Price against labor cost
      Never cost plus
    Profit And Loss
      Obsess over COGS
      AI operating leverage
      Judged on operating income
      Target software margins
    Build Dont Buy
      Cant acquire product fit
      Legacy expectations persist
      Regulatory moat exception
```
""",
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
        _yt(
            "How To Get The Most Out Of Vibe Coding",
            "BJjsfNO5JTo",
            "17 min",
            """# How To Get The Most Out Of Vibe Coding

## Summary
Tom, a YC partner, spent a month vibe coding side projects and found it both remarkably good and a practice you can measurably improve at, much like prompt engineering a year or two ago. The best techniques mirror what a professional software engineer would do. The talk opens with tips from founders in the just-started YC Spring Batch: when an AI IDE loops on a bug, paste the code into the LLM's website directly; run Cursor and Windsurf on the same project in parallel and pick the better front-end iteration; treat AI as a new kind of programming language that needs detailed context; handcraft your own test cases as guardrails before letting the LLM generate code; spend an unreasonable amount of time in a pure LLM scoping the architecture before touching a coding tool; and watch for rabbit holes, stepping back when you find yourself endlessly pasting error messages.

Tom then shares his own advice. Complete beginners should start with Replit or Lovable, though these struggle with backend logic; anyone who has coded before can go straight to Windsurf, Cursor, or Claude Code. Do not dive into code first: write a comprehensive plan in a markdown file, prune it, mark features as too complicated or ideas for later, then implement section by section, checking each works and committing to Git before moving on. Use Git religiously and reset hard rather than letting failed prompts accumulate layers of bad code. Have the LLM write high-level integration tests that simulate clicking through the app, since these catch its habit of changing unrelated logic. LLMs also handle non-coding work: Claude configured his DNS and Heroku hosting, and ChatGPT created a favicon that Claude then resized into six formats with a throwaway script.

For bugs, copy-pasting the error message alone is often enough; for complex ones, ask the LLM for three or four possible causes before writing code, reset after each failed fix, add logging, and switch models, since Claude Sonnet 3.7, OpenAI models, and Gemini each succeed where others fail. Further tips: write instruction files such as Cursor rules, download API docs into a local folder, use the LLM as a teacher, build complex features as standalone reference implementations first, keep files small and modular, and favor established stacks like Ruby on Rails over Rust or Elixir because of richer training data. Screenshots, voice input via Aqua at 140 words per minute, frequent refactoring backed by tests, and constant experimentation with new models round out the playbook.

## Main ideas
- **Vibe coding is a learnable skill** — like prompt engineering a year or two ago, you get measurably better by tinkering and adopting the practices of professional software engineers.
- **Plan before you code** — develop a comprehensive markdown plan with the LLM, prune it, and implement it section by section rather than trying to one-shot the product.
- **Git is your safety net** — reset hard to a clean state after failed attempts instead of letting the LLM pile up layers and layers of bad code.
- **Write high-level integration tests** — simulate a user clicking through the app to catch the LLM's habit of changing unrelated logic.
- **Error messages are powerful prompts** — copy-pasting the error alone is often enough for the AI to identify and fix a bug without any explanation.
- **Switch models when stuck** — Claude Sonnet 3.7, OpenAI models, and Gemini each succeed where the others fail, with Gemini strong at planning and Sonnet at implementation.
- **LLMs go beyond coding** — they configured DNS servers, set up Heroku hosting, and produced favicon assets, acting as DevOps engineer and designer.
- **Small modular files help everyone** — clear API boundaries and modular architecture make codebases easier for both humans and LLMs to change safely.
- **Pick well-documented stacks** — Ruby on Rails performed impressively thanks to 20 years of consistent conventions and training data, unlike Rust or Elixir.
- **Use screenshots and voice** — pasting UI screenshots and dictating instructions through Aqua at 140 words per minute doubles input speed.

## Mindmap
```mermaid
mindmap
  root((Vibe Coding))
    Getting Started
      Replit or Lovable beginners
      Cursor Windsurf Claude Code
      Plan in markdown first
      Implement section by section
    Version Control
      Use Git religiously
      Reset after failed attempts
      Avoid layered bad code
    Testing
      High level integration tests
      Catch unrelated regressions
      Handcraft test cases
    Debugging
      Paste error messages
      Ask for possible causes
      Add logging
      Switch models
    Workflow Boosters
      Instruction files for agents
      Local documentation folders
      Screenshots and voice input
      LLM as teacher
    Architecture
      Small modular files
      Clean reference implementations
      Established frameworks like Rails
```
""",
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
        _yt(
            "Tips For Technical Startup Founders",
            "rP7bpYsfa6Q",
            "28 min",
            """# Tips For Technical Startup Founders

## Summary
Diana, a YC group partner and former CTO of an augmented reality SDK startup that sold to Niantic, distills advice from many YC technical founders for each early stage. A technical founder is not somebody hired to build the app but a partner committed to the company's success: leading product building, talking to users, doing all the tech things from front end to devops and even IT, and favoring good-enough architecture, bias to action, and comfort with technical debt over big-company perfectionism.

In the ideating stage the goal is a prototype in a matter of days, built on prototyping tools: clickable Figma mockups for software, an afternoon terminal script for devtools, or 3D renderings for hardware, as with Remora's truck-mounted carbon capture. Optimizely, after abandoning a Twitter referral widget, built a visual A/B-testing prototype as a JavaScript file on S3 that only the founders could operate, yet it thrilled marketers. Mistakes here are overbuilding toward a full MVP, not showing users soon enough, and clinging to bad ideas. In the MVP stage the goal is launching in weeks and getting commitment, ideally payment. Hiring now usually backfires: finding someone good takes over a month, and outsourcing the build costs founders key product insights; Justin.tv's four founders built everything themselves before later hiring overlooked misfit engineers. Her principles: do things that don't scale, like Stripe's founders manually filling bank forms for every payment; build a 90/10 solution (Paul Buchheit's term) by restricting dimensions, the way DoorDash launched as Palo Alto Delivery with PDF menus, a founder's phone number, Google Forms as the back end, and Find My Friends for driver tracking, its Palo Alto focus nailing suburban unit economics before scaling; and choose the tech stack for iteration speed, leaning on third-party tools like Auth0, Stripe, React Native, and Firebase. Facebook scaled PHP later with the HipHop transpiler, and WayUp's self-taught CTO chose Django over the then far more popular Rails. The only tech choices that matter are those tied to customer promises.

After launch, iterate toward product-market fit by marrying hard data from simple analytics (Google Analytics, Amplitude, Mixpanel) with soft data from user conversations: WePay pivoted from a Venmo-like consumer product to a payments API after learning GoFundMe only wanted the payments. Continuously launch, as Segment did with five launches in about a month after pivoting from classroom analytics, and tolerate tech debt: Pokemon Go's launch login failures at Twitter-scale load did not kill a game that still earns over a billion dollars a year. Post product-market fit, the role shifts to refactoring, hiring, and engineering culture, with coding time shrinking from about 70% on a small team toward none beyond ten engineers.

## Main ideas
- **A partner, not just a dev**: the technical founder leads building and user conversations, does every tech job, and commits to whatever it takes.
- **Prototype in days**: use clickable Figma mockups, quick scripts, or 3D renderings purely to show and demo to users, as Optimizely and Remora did.
- **Do not overbuild**: thinking you need a full MVP at the ideating stage and clinging to bad ideas are the classic prototype mistakes.
- **Delay hiring**: early hires slow the launch and cost founders key product insights; Justin.tv's founders built the MVP entirely themselves.
- **Do things that don't scale**: Stripe's founders manually processed payments and filled bank forms so they could launch sooner.
- **Build 90/10 solutions**: restrict the problem's dimensions like DoorDash's static-page, Google-Forms Palo Alto launch assembled in one afternoon.
- **Choose tech for iteration speed**: pick what you are dangerous enough with and lean on third-party tools like Auth0, Stripe, and Firebase; Facebook fixed PHP scaling later.
- **Iterate with hard and soft data**: marry simple analytics with continual user conversations, as WePay did when pivoting to a payments API for GoFundMe.
- **Continuously launch and tolerate tech debt**: Segment launched five times in a month, and Pokemon Go's broken launch did not kill it.
- **The role evolves after PMF**: refactor, hire, and shape engineering culture as founder coding time shrinks from 70% toward zero.

## Mindmap
```mermaid
mindmap
  root((Technical Founder Tips))
    Founder Role
      Partner not just dev
      Do all tech things
      Talk to users
      Good enough beats perfect
    Ideating Stage
      Prototype in days
      Clickable Figma demos
      Renderings for hardware
      Do not overbuild
    MVP Stage
      Launch in weeks
      Things that do not scale
      90 10 solutions
      Avoid early hiring
    Tech Stack
      Choose for iteration speed
      Use third party tools
      Choices tied to promises
    After Launch
      Hard and soft data
      Continuously launch
      Tech debt is fine
      Balance building and fixing
    After PMF
      Refactor and scale
      Hire and delegate
      Coding time shrinks
```
""",
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
        _yt(
            "How to Build An MVP",
            "QRZ_l7cVzzU",
            "17 min",
            """# How to Build An MVP

## Summary
Using the midwit meme, the talk argues that both the naive first-time founder and the Jedi-level founder land on the same right answer: launch something quickly and iterate. The wrong answer is the seemingly smart middle path of 100 surveys, 600 user interviews, a year of fundraising, and hiring 100 people. You only really start learning about your user when you put a product in front of them; the MVP probably will not work, but it is the best way to start the conversation about solving their problems. So get a product out fast, talk to initial customers, iterate, and repeat — after three to six iterations the product will look very different, and you will learn ten times more than by talking to your co-founders or thinking in your head. The talk then attacks two fears. First, the fear that a bad first impression kills the company: early adopters use imperfect products all the time, respond to the pitch of improving it together, and the people who would flee a broken demo were never going to try a new product anyway. Founders should lean into the fear and ask what actually happens in the worst case — the company does not die, and you can reach back out a week later with a better product. Second, the fake Steve Jobs misconception: even Jobs iterated, since the first iPhone had no App Store, could not take video, and only had 2G internet, and the first iPod's physical scroll wheel got sand stuck in it and broke. Three famous MVPs illustrate the pattern of fast to build, very limited functionality, and appeal to a small set of users: Airbnb launched with no payments, no map view, air beds only, and only for conferences; Twitch began as Justin.tv, a single page with one streamer and ridiculously expensive CDN streaming; Stripe started as slash dev slash payments, filing manual bank paperwork every night and serving only early YC startups that wanted simple credit card payments. The right first customers have their hair on fire — they are in so much pain they will buy a brick to smother the flames rather than wait for the perfect solution. Surveys cannot replace this, because customers are experts in their problem but not in its solution. Practical tricks for speed: set a specific deadline, write the spec down, cut features a truly desperate customer does not need, and do not fall in love with the MVP — fall in love with the customer. It is far better to have a hundred people love your product than a hundred thousand who kind of like it.

## Main ideas
- **Launch quickly and iterate**: the Jedi move is shipping a product into customers' hands and improving it, not surveys, interviews, and a year of building.
- **Learning starts at contact with users**: you only begin understanding your user when a real product is in front of them, and the MVP opens that conversation.
- **Early adopters tolerate broken products**: they talk to startups because they have a real problem, so a rough first version will not scare them away.
- **Fear of launching should be interrogated**: imagine the worst case — a failed demo does not kill the company, and acting on that fear is what hurts.
- **Even Steve Jobs iterated**: the first iPhone had no App Store, no video, and 2G, so no founder should expect to nail the perfect product in one try.
- **Great companies started tiny**: Airbnb had no payments and only air beds at conferences, Twitch was one streamer on one page, and Stripe filed bank paperwork by hand.
- **Sell to hair-on-fire customers**: desperate customers will use an imperfect solution, like hitting themselves with a brick, so target them first.
- **Surveys are not a shortcut**: customers are experts in their pain but cannot design the solution — that is the product builder's job.
- **Build the MVP fast**: set a deadline, write the spec, cut it hard, and do not fall in love with a product that is going to change.

## Mindmap
```mermaid
mindmap
  root((Build An MVP))
    Launch and Iterate
      Ship quickly then learn
      Talk to users
      Improve over iterations
    Handle the Fear
      Company will not die
      Early adopters forgive flaws
      Act despite fear
    Fake Steve Jobs
      Jobs iterated products too
      First iPhone lacked features
      iPod scroll wheel broke
    Famous First Versions
      Airbnb air beds only
      Twitch one streamer page
      Stripe manual bank paperwork
    Hair On Fire
      Sell to desperate customers
      A brick still helps
      Skip non desperate users
    Build It Fast
      Set a deadline
      Write and cut spec
      Dont fall in love
```
""",
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
        _yt(
            "How To Talk To Users",
            "z1iF1c8w5Lg",
            "18 min",
            """# How To Talk To Users

## Summary
Gustav, a Y Combinator group partner since 2017 who worked at Airbnb and was a YC founder in 2007, explains why and how founders should talk to users. Most people imagine new products emerging from a lazy Sunday or a late night coding session, as in The Social Network movie, but the best founders learn directly from users throughout the life of the company, because paying customers are the only stakeholders who will keep you honest. He illustrates this with Airbnb: a real photo of Brian Chesky with Amal, Airbnb's very first guest, and Chesky's 2010 experiment of living in 50 different Airbnbs so he could talk with every host each day; the founders even put their personal phone numbers on the website, in contrast to the do-not-reply emails most companies hide behind. To find users, start with friends and former co-workers, then reach beyond your circle through LinkedIn, Reddit forums, Slack or Discord communities, and in-person events. Using a mock startup around helping companies reduce carbon emissions, he shows outreach messages that briefly introduce the project and ask for a 20 minute call. In interviews, prefer video, phone, or in-person conversations over surveys, since a five minute interview teaches more than 5,000 survey responses; build rapport, take notes, and crucially do not introduce your idea until the end, or at all, to avoid biasing answers. Good questions include: tell me how you do X today, what is the hardest thing about it, why is it hard, how often do you do it, why is it important to your company, and what do you do to solve it now, ideally watching users show their actual workflow. Avoid asking whether they would use your product, which features would make it better, yes or no questions, and double questions. Users have good problems but bad solutions, as when Gmail users asked to see the inbox and email together because the product was slow, or Airbnb guests wanted host phone numbers because the platform had not built enough trust. Afterwards, organize notes into problem buckets, write conclusions, and move fast to an MVP, checking that the problem is valuable: are people paying for other solutions, are entrenched tools like Excel already good enough, and is the audience easy to sell to, since plumbers are far harder than startups. Finally, test prototypes without instructing users, have them speak their mind, and keep early interviewees involved through exclusive Slack or WhatsApp groups so they see the product react to their feedback.

## Main ideas
- **Talk to users forever**: the best founders learn directly from users throughout the lifetime of the company because customers are the only stakeholders paying you.
- **Get personal like Airbnb**: Chesky lived in 50 Airbnbs and the founders put their personal phone numbers on the website to hear from hosts.
- **Find users beyond your circle**: friends and co-workers first, then LinkedIn, Reddit forums, Slack or Discord communities, and in-person events.
- **Interviews beat surveys**: a five minute video call teaches more than 5,000 survey responses.
- **Hide your idea** until the end of the interview, or never mention it, so you do not bias the answers.
- **Ask about problems, not features**: questions like how do you do X today and why is it hard reveal behavior, and users have good problems but bad solutions.
- **Validate that the problem is valuable** by checking whether people already pay for solutions, whether Excel is good enough, and whether the audience is easy to sell to.
- **Test prototypes silently**: hand over the prototype, give a goal like making a booking, never explain the screens, and have users think aloud.
- **Keep early users involved** in exclusive Slack or WhatsApp groups, shipping visible reactions to their feedback to build trust.

## Mindmap
```mermaid
mindmap
  root((Talking To Users))
    Why Talk To Users
      Users keep you honest
      Only stakeholders paying you
      Chesky lived in Airbnbs
      Learn across company lifetime
    Finding Users
      Friends and coworkers
      LinkedIn and communities
      In-person events
    Interview Technique
      Prefer live calls
      Build rapport first
      Hide your idea
      Ask open follow-ups
      Take notes always
    Questions To Ask
      How you do X today
      Hardest thing about X
      Why it is hard
      Why it matters
      Current workarounds
    Questions To Avoid
      Will you use it
      Feature wish lists
      Yes or no questions
      Double questions
    Toward An MVP
      Bucket the learnings
      Check problem value
      Test prototypes silently
      Keep users involved
```
""",
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
        _yt(
            "The Best Way To Launch Your Startup",
            "u36A-YTxiOw",
            "21 min",
            """# The Best Way To Launch Your Startup

## Summary
YC's head of Outreach, who has watched more than 3,500 companies go through the program over nine years, wants founders to stop treating a launch as one perfect, high-stakes moment. Most founders lovingly prepare a launch for months, yet most launches are met with silence — and if it took six months to get a first version in front of anyone, the startup may die before it gets another chance. Instead, in the spirit of always be shipping, launching should be continuous: launch, see what happens, iterate, and launch again, as Airbnb did three times before users arrived. Echoing Paul Buchheit, it is better to make a few people really happy than many people semi-happy; even ten users who truly love the product give morale, focus, and a base to expand cockroach-style. Before any launch, founders need a strong one-sentence pitch built on clarity of vision, because clear ideas spread by word of mouth, the cheapest growth channel. Lead with what you do, not why: Pave's line — pave lets companies plan, communicate, and benchmark compensation in real time — beats a backstory about confused friends with stock options. Avoid meaningless jargon, which Garry Tan calls the number one issue he fights; a know-how and synergy platform could be literally anything. Do not ramble. The X-for-Y construction works only when X is a household name, it is clear why Y wants X, and Y is a huge market — buffer for Snapchat fails that test, while Airbnb for dance and movement classes paints a fast picture. The talk then walks through launch types: the silent launch (a landing page with name, description, contact, and a call to action — half of the startup school companies sampled lacked one); friends and family, as early Reddit circulated in the first YC batch, though you should not linger there; launching to strangers, as DoorDash did after a macaron store manager named Chloe showed pages of delivery orders, leading to 200 small-business interviews and an MVP built in hours; online communities like YC's Bookface with over 6,000 founders and Hacker News' Show HN, where a random Friday-night post sent Robinhood's commission-free-trading waitlist to 10,000 signups in a day and 50,000 in a week; social media, like Anja Health's founder hitting 10,000 TikTok followers in a month; pre-order campaigns for physical products; and waitlist launches like Superhuman's, though converting a waitlist gets harder the longer you sit on it. Press, by contrast, is nearly impossible before raising a million dollars and is never a scalable path to product-market fit; building your own community and email list, then launching again and again through every channel like Stripe does, is what works.

## Main ideas
- **Launching is continuous, not one shot**: most launches get no attention, so iterate and launch again like Airbnb, which launched three times before getting users.
- **Launch ASAP**: founders lie to themselves with theoretical convictions, and only putting the product out shows whether the problem is big enough that people will pay or use it.
- **A few users who love you beat many who shrug**: per Paul Buchheit, even ten users who really love the product put you on the right track.
- **Lead with what, not why**: give context up front with the company name and what it does, as Pave's compensation one-liner shows, and save the backstory for follow-up questions.
- **Kill jargon and rambling**: a know-how and synergy platform says nothing — a good one-liner tells the listener what they would have to build to reproduce your product.
- **Use X for Y carefully**: it needs a household-name X, an obvious reason Y wants it, and a huge Y market, or a plain description works better.
- **Match the launch to the stage**: silent landing page, friends and family, strangers, online communities, social media, pre-orders, and waitlists each fit different moments.
- **Communities can ignite growth**: Robinhood's random Hacker News post produced 10,000 signups in a day; launch authentically in communities you genuinely engage with.
- **Press is not a silver bullet**: it is hard to land before raising a million dollars and cannot be counted on for sustained growth, so build your own community instead.

## Mindmap
```mermaid
mindmap
  root((Launching Your Startup))
    Launch Continually
      Launch ASAP
      No one caring is fine
      Airbnb launched three times
    One Line Pitch
      Lead with what
      No jargon or rambling
      X for Y with care
    Early Launch Types
      Silent landing page
      Friends and family first
      Strangers like DoorDash did
    Community Launches
      Hacker News Show HN
      Robinhood waitlist surge
      TikTok community building
    Press Reality
      Hard for unfunded startups
      Not a silver bullet
      Build your own community
```
""",
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
        _yt(
            "How to Get Your First Customers",
            "hyYCn_kAngI",
            "23 min",
            """# How to Get Your First Customers

## Summary
Gustav, a YC group partner, explains how to go from talking to users to landing your first customers. He starts with Paul Graham's essay Do Things That Don't Scale: many founders wrongly believe a good product grows by itself, but good products are built together with customers, startups take off because founders make them take off, and you must manually recruit customers rather than hide behind writing more code. The startup curve — launch, trough of sorrow, wiggles of false hope, then product-market fit — shows that at every early moment the founders are what separates success from failure. Founders should do sales themselves: talking to customers and selling are two sides of the same coin, doing sales gives you control of your destiny, and you should not hire a sales team until you know what good looks like. Sales is arguably the easiest job in a startup to learn, because knowing the problem, the product, and the market makes you an expert in the customer's eyes; Tony from DoorDash, Mathilde from Front, Tracy from PlanGrid, and Steve Jobs all did it. Brex is the model case: during YC Winter 17 they recruited their first ten customers from their own batch with a short email offering ten beta spots, a virtual card, no personal guarantee, and zero fees, with a founder onboarding every customer himself. A great sales email is six to eight sentences, plain text with no HTML, jargon-free, addresses the customer's problem, includes social proof and a simple website link or short video, and ends with a clear call to action. The sales funnel is simple: make a list, reach out, run demos, talk pricing, close, and then onboard — skipping onboarding causes churn. Go after the easiest customers first: your network, other startups with short decision lines, and true early adopters, since most people simply archive cold email; be willing to fire slow-moving prospects. Charge from the start — if they do not pay, they are not a customer — and in B2B prefer a money-back guarantee or an opt-out over free trials, raising prices until customers complain but still pay. Finally, work backwards from your goal: 500 emails at a 50 percent open rate, 5 percent response, and typical demo conversion yield about two customers, so 100 emails yielding zero proves nothing about whether sales works. Track conversions in a simple CRM like Apollo, Close, or Pipedrive, read Founding Sales and Lenny Rachitsky's newsletter, and remember that scalable channels like SEO and referrals are end states — Airbnb did not start there.

## Main ideas
- **Do things that don't scale**: startups take off because founders manually recruit customers one by one, not because a good product grows by itself.
- **The founders are the difference**: at every stage of the startup curve, from launch through the trough of sorrow, it is the founders who switch markets and learn sales.
- **Founders must do sales themselves**: selling and talking to users are the same coin, and you should not hire salespeople until you know what good looks like.
- **Your expertise sells**: if you know the problem, the product, and the market intimately, customers see you as an expert and want to hear from you.
- **Write short, plain sales emails**: six to eight sentences, no jargon or HTML, social proof, a simple website link, and a clear call to action, like Brex's ten-beta-spots email.
- **Run the full funnel including onboarding**: list, outreach, demo, pricing, close, then onboard — early products are hard to use and skipped onboarding becomes churn.
- **Chase the easiest customers first**: your network, other startups with short decision lines, and early adopters; most recipients just archive cold email, so volume matters.
- **Charge real money**: a non-paying user is not a customer; use money-back guarantees instead of B2B free trials and raise prices until customers complain but still pay.
- **Work backwards from your goal**: 100 emails yielding zero customers proves nothing — track every conversion rate in a CRM so you know what to fix.
- **Scalable channels come later**: SEO, ads, and referrals are end-state growth; Airbnb's first customers came from unscalable manual work.

## Mindmap
```mermaid
mindmap
  root((First Customers))
    Things That Dont Scale
      Founders make takeoff happen
      Recruit customers manually
      Startup curve grind
    Founders Do Sales
      Know your customer
      Dont outsource sales
      Brex batch emails
    Sales Emails
      Short plain text
      Social proof included
      Clear call to action
    Funnel Discipline
      List email demo close
      Onboard to prevent churn
      Track conversion rates
    Charging and Targets
      Free means no customer
      Money back guarantee
      Raise price until complaints
      Work backwards from goals
```
""",
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
        _yt(
            "How to Get Your First 10 Customers",
            "_FBivfgOvuE",
            "14 min",
            """# How to Get Your First 10 Customers

## Summary
Max, a visiting partner at Y Combinator, compiles tactical lessons from dozens of YC founders who shared on Bookface how they actually landed their first 10 customers. He begins with the question founders must answer before touching any tool: where does the target customer actually spend their time? Cold email and LinkedIn feel productive but fail for buyers like school district administrators, property managers, or truck dispatchers who do not live in an inbox; one founder spent three months on cold outreach to a legacy industry with terrible reply rates, then closed more in three days of walking a trade show floor. If you cannot describe your buyer's average day, conference habits, and preferred channels, you have not spent enough time with real customers. Next, he insists the first two or three customers almost always come from the warm network — friends in the industry, former colleagues, classmates, people one introduction away — because early buyers are betting on trust in the founder, not just the product. Work personal contacts first, then second-degree LinkedIn connections (one founder got intros to about half the customers she closed during her batch), then AI network search tools like Happenstance, and make every intro request specific. He then highlights the surprising power of showing up in person: a founder who flew to one executive four weeks in a row until he closed, another kicked out after eight minutes in Hawaii who still won that account, a conference playbook of back-to-back 15-minute Calendly slots filled by emailing the attendee list, and micro dinners of six to ten prospects at $50 to $100 a head. For consumer and SMB products, he recommends finding where the pain is expressed publicly — especially Reddit, where lurkers quietly sign up, one founder DMed every commenter on old complaint threads, and a healthcare founder posted two to five times a day and got shadowbanned along the way. For true outbound he covers Apollo, Clay, and LinkedIn Premium, plus outreach framings that are not sales pitches: mentorship asks, 200 user-research calls before building, free whiteboard sessions, and even paying lawyers $100 to $200 an hour for feedback, which about 30% accepted. Copy advice: under 75 words, a clear call to action, read it aloud to a friend, give something before asking, and follow up three or four times. His closing frame: customers 1-3 come from your network, 4-10 from unscalable founder effort, and 10-50 from the scalable playbook.

## Main ideas
- **Know where your buyer lives**: before picking channels or tools, spend an hour answering concrete questions about your buyer's average day, inbox habits, conferences, and communities.
- **Cold email is a default, not a strategy**: one founder got more customers in three days at a trade show than in three months of refining email copy to a legacy industry.
- **Customers 1-3 come from warm networks**: friends, former colleagues, classmates, and second-degree intros work because early buyers trust the founder, not the unproven product.
- **Showing up in person outperforms everything**: flying out repeatedly, walking into offices uninvited, and stacking 15-minute conference meetings converts far better than cold outreach.
- **Micro events beat large ones**: dinners or happy hours for six to ten ideal-profile prospects at $50-100 a head consistently convert better than big gatherings.
- **Find public pain in communities**: Reddit threads, Facebook groups, and forums where customers already complain are a durable source, since threads persist in Google for years.
- **Frame outreach as something other than sales**: genuine asks for mentorship, advice, whiteboard sessions, or paid expert feedback open doors that pitches cannot.
- **Copy rules that matter**: keep it under 75 words, include one clear call to action, read it out loud to a friend, and follow up three or four times.
- **Give before you ask**: 20 minutes of prospect-specific work, like a vulnerability scan or audit note, is a reasonable trade for 30 minutes of their time.
- **Prospecting tools come later**: Apollo, Clay, and email sequences only start to make sense around customers 10-50, once the pitch and value prop are proven.

## Mindmap
```mermaid
mindmap
  root((First 10 Customers))
    Find Your Buyer
      Where they spend time
      Cold email often fails
      Trade show beat email
      Map their average day
    Warm Network First
      Friends and former colleagues
      Second degree LinkedIn intros
      AI network search tools
      Trust in the founder
    Show Up In Person
      Fly out to close
      Small industry conferences
      Calendly slots all day
      Micro dinners for prospects
    Online Communities
      Reddit complaint threads
      DM every commenter
      Facebook groups and Discord
      Threads persist in Google
    Outbound And Framing
      Apollo Clay LinkedIn Premium
      Ask for advice framing
      Pay experts for feedback
      Give value before asking
    Outreach Copy
      Under 75 words
      Clear call to action
      Read it aloud test
      Follow up several times
```
""",
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
        _yt(
            "How To Convert Customers With Cold Emails",
            "7Kh_fpxP1yY",
            "33 min",
            """# How To Convert Customers With Cold Emails

## Summary
Aaron Epstein, a YC group partner, opens with the all-time best outreach hack: get a warm intro, which converts two to three times better than a regular cold email. Mine LinkedIn, friends of friends, current and former coworkers, and school and employer alumni networks. Since warm intros are not always possible, the talk focuses on cold email, and the good news is that most cold emails are terrible, so the bar to stand out is low. He maps the funnel by working backwards from a goal: to land one customer with a 10% demo-to-customer rate you need 10 demos; at 25% response-to-demo you need 40 responses; at 10% open-to-response you need 400 opens; at a 50% open rate you must send 800 emails. So plan on dozens per day, written manually and personalized before any automation, with each email aiming only at the next funnel step, not the sale. Track conversion rates to find weak steps, and expect rates to worsen as you scale past your most ideal targets.

To raise open rates, targeting is the highest-leverage move: 100 targeted emails beat 1,000 untargeted ones. Send from your personal name with short, simple subject lines like "quick question"; email usually beats LinkedIn, and texting needs explicit permission. Find addresses through mutual contacts, LinkedIn Sales Navigator, personal sites, guessing company formats, or tools like Apollo.io, Hunter.io, and Clearbit. Early on, you are the brand, and even sharing your cell number signals you care.

For responses, he gives seven principles of effective copy: one focused goal per email; be human (informal tone, emotion, even an animated GIF of the sender waving a whiteboard with his name on it); personalize with specifics and "uncommon commonalities" like a shared college; keep it short enough to answer from a phone; establish credibility via schools, employers, customer logos, or shared connections; make it about the reader, reframing "I" as "you" and using customers' own language; and end with a clear, standalone call to action. One email is rarely enough: follow up two to four times, spaced by days, getting creative (a "free donuts" subject line plus real donuts worked), and move on without anger if ignored. He critiques three real bad emails (a mistargeted shipping pitch, a generic "hey there" spam, an all-about-me freelancer) and three good ones (a "go terps" alumni note, his templated-but-special Creative Market seller invite, and a smoothie company rewrite offering a free smoothie party). Final advice: founders themselves should send the emails, do the work manually, and scale only after it converts.

## Main ideas
- **Warm intros win** — A warm introduction converts two to three times better than a cold email, so exhaust your network before going cold.
- **Work backwards through the funnel** — With typical conversion rates it takes roughly 800 sent emails to produce one customer, so a handful of emails per week will not cut it.
- **Targeting beats volume** — Better targeting is the highest-leverage way to raise open rates, since 100 targeted emails outperform 1,000 untargeted ones.
- **One focused goal** — Every word should drive toward a single action, because multiple asks create a paradox of choice and get the email deleted.
- **Be human and personalize** — Write how you talk to a friend, use the recipient's name, and find uncommon commonalities like a shared college.
- **Keep it short and credible** — Emails should be answerable from a phone in seconds, and credibility comes from schools, past companies, customer logos, and shared connections.
- **About the reader, not you** — Reframe "I" as "you", tell your story as a quest to solve the reader's problem, and never make demands.
- **Clear call to action** — End with one concrete next step as its own standalone sentence right before you sign off.
- **Follow up persistently** — Plan to follow up two to four times with days between, get creative like the free donuts email, and move on without anger.
- **Founders send manually first** — Recipients take founders far more seriously than automated sequences, and manual sending is how you learn what works before scaling.

## Mindmap
```mermaid
mindmap
  root((Cold Email Conversion))
    Funnel Math
      Work backwards from goal
      800 emails per customer
      Track conversion rates
      Rates drop at scale
    Open Rates
      Targeting is highest leverage
      Personal name as sender
      Short simple subject lines
      Tools to find emails
    Seven Copy Principles
      One focused goal
      Be human and personal
      Uncommon commonalities
      Keep it short
      Credibility and clear CTA
    Follow Up
      Two to four times
      Get creative like donuts
      Never get angry
    Examples
      Bad targeting always fails
      Templated but special feel
      Smoothie party rewrite
    Final Advice
      Manual before automation
      Founders should send
      Dozens per day
```
""",
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
        _yt(
            "How To Keep Your Users",
            "VNxBZ7ka5J0",
            "29 min",
            """# How To Keep Your Users

## Summary
David Lee, a YC group partner, asks how you know you have actually made something people want, and argues the best quantitative answer is cohort retention: tracking what fraction of new users keep using your product over time. He co-founded Bump (YC summer 2009), one of the first mobile apps past 100 million users, which failed as a business; after pivots it was acquired by Google, where his photo app became the basis for Google Photos, now serving well over a billion users. He admits he once gave a handwavy answer about cohort retention while pitching a prestigious VC for his Series A, then googled the term after the meeting.

Measuring it requires three definitions: cohorts (group new users by first-use week or month, later slicing by country, device, or acquisition channel), the action that counts someone as active (not merely opening the app — Instagram might use viewing three or more posts, Uber a completed ride, Google Photos viewing a photo full screen), and a time period matching intended usage (daily for social apps, weekly for utilities, quarterly or longer for travel products like Airbnb). He walks through a triangle chart — 12 January users, six back in February, four in March — likening it to tagging party guests with stickers for their arrival month, with the diagonal representing one calendar month; dividing by cohort size yields percentage curves best drawn as line graphs.

The core insight, shown through products A and B: the only thing that matters is whether curves get flat, not the absolute number. A curve trending to zero means you churn everyone; a curve flat even at 20% lets users accumulate. Google Photos' weekly curves flattened between 20% and 40%, giving him confidence six weeks after launch that 20% of all humans could eventually use it. He then lists ways to fool yourself, all mistakes he made: widening the time period (Bump went weekly to monthly to quarterly before investor meetings), picking too easy an action (Google+ counted clicks on a notification bell), treating payment as activity (people stop watching Netflix before they cancel), quoting a single point like "80% week-over-week retention" without knowing which week, and trusting analytics tools instead of building the curves yourself with scripts or Google Sheets. To improve retention: improve the product, acquire better-matched users (Google's Gen Z marketing push produced poorly retaining cohorts), slice cohorts by dimension, invest in onboarding, and build network effects. The holy grail is curves that flatten and then rise, and the layer cake chart of stacked cohorts driving growth is the most beautiful chart a startup can see.

## Main ideas
- **Cohort retention answers the core question** — Tracking what fraction of each group of new users keeps coming back is the most quantitative way to know if you made something people want.
- **Three definitions come first** — You must choose how to isolate cohorts, which action counts a user as active, and the time period for measuring subsequent usage.
- **Pick a value-correlated action** — The action should correlate with real value, like viewing a photo full screen in Google Photos or completing an Uber ride, not just opening the app.
- **Match the period to intended usage** — Social apps should measure daily, utilities weekly, and travel products quarterly or longer.
- **Flat curves are the only thing that matters** — The shape of the curve beats the absolute number, because flat curves mean you accumulate users instead of running on a treadmill.
- **Do not fool yourself** — Widening time periods, easy actions like notification clicks, paying as a proxy for active, and single-point numbers all delude founders, and Lee made every one of these mistakes.
- **Build the curves yourself** — Analytics tools often measure something other than what you think, so compute cohorts from your logs or Google Sheets to develop intuition.
- **Improve product or acquisition** — Flatter, higher curves come from product improvements, better-targeted users, sliced cohorts, stronger onboarding, and network effects.
- **The holy grail is rising curves** — The best products show cohorts that flatten and then rise, stacking into a growing layer cake of retained users.

## Mindmap
```mermaid
mindmap
  root((Cohort Retention))
    Setup Definitions
      Cohorts by start month
      Action showing real value
      Period matches intended usage
    Reading The Charts
      Triangle chart of cohorts
      Percentages as line graphs
      Diagonal is calendar month
    Key Insight
      Flat curves are everything
      Shape beats absolute number
      Flat means users accumulate
    Ways To Fool Yourself
      Too large time period
      Too easy action
      Paying is not active
      Single point in time
      Blind trust in tools
    Improving Retention
      Improve the product
      Acquire better users
      Slice cohorts by dimension
      Better onboarding
      Network effects
    Holy Grail
      Curves that rise
      Layer cake growth
      Talk to users
```
""",
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
        _yt(
            "Startup Business Models and Pricing",
            "oWZbWzAyHAE",
            "33 min",
            """# Startup Business Models and Pricing

## Summary
Aaron Epstein, a group partner at Y Combinator, explains how business models and pricing shape startup outcomes. He begins with the claim that nearly every billion dollar company uses one of nine business models: SaaS, transactional, marketplace, hard tech, usage-based, enterprise, advertising, e-commerce, and bio. Rather than reinventing how you make money, founders should copy a proven model and innovate on the product. Analyzing the top 100 YC companies by value, he finds SaaS makes up 31 percent, transactional 22 percent, and marketplaces 14 percent, together 67 percent of the list. Value follows a power law: half the total value comes from the top ten companies, five of which are marketplaces such as Airbnb, Instacart, and DoorDash. Marketplaces are hard to start because of the chicken-and-egg problem, but once they hit an inflection point, network effects make them winner-take-all, so 14 percent of the companies create 30 percent of the value. Transactional businesses like Stripe, Coinbase, and Brex outperform because they sit directly in the flow of funds and become critical infrastructure, while SaaS wins through predictable recurring revenue. Advertising is only 3 percent of the list and should be avoided unless you expect to be a top ten site on the internet. Absent entirely are consulting, affiliate, hardware, and platform-dependent businesses, which suffer from low margins, distance from the transaction, capital intensity, or platform risk. Epstein stresses retention: with 95 percent monthly retention, 100 customers shrink to 54 in a year, and at 90 percent to just 28, so a five point retention gap can be life or death. Durable winners build moats through network effects, lock-in, technical innovation, economies of scale, and organic distribution. The pricing half offers five insights. First, charge: charging teaches you who will pay and how much, as when Stripe priced at 5 percent versus competitors at 3 percent to test its value. Second, price on value, not cost-plus. Third, most startups undercharge, and raising prices is the easiest way to grow revenue since price itself signals value. Fourth, pricing is not permanent: Netflix repeatedly raised prices on its 221 million subscribers. Fifth, keep pricing simple, like GitLab with three clear plans versus the cluttered Quicken page. He closes with Segment, which went from charging 10 dollars a month to an 18,000 dollar deal after asking for 120,000 dollars, and eventually sold to Twilio for more than 3 billion dollars.

## Main ideas
- **Nine proven business models** account for nearly every billion dollar company, so copy a proven model and put your innovation into the product instead.
- **SaaS, transactional, and marketplaces dominate**, together making up 67 percent of the top 100 YC companies.
- **Marketplaces become winner-take-all** because network effects after the chicken-and-egg phase make them 30 percent of total value from only 14 percent of companies.
- **Stay close to the transaction**: businesses in the flow of funds, like Stripe and Brex, take their cut easily and become critical infrastructure.
- **Recurring revenue needs retention**: 95 versus 90 percent monthly retention is the difference between 54 and 28 remaining customers after one year.
- **Moats create dominant winners**, through network effects, lock-in and switching costs, technical innovation, economies of scale, and organic distribution.
- **You should charge**, because charging is the fastest way to learn who wants your product and how much value it delivers.
- **Price on value, not cost**: cost-plus pricing ignores perceived value, and the gap between price and value is your room to raise prices.
- **Most startups undercharge**, and raising prices is the easiest way to grow revenue, as Segment's 150x price increase shows.
- **Keep pricing simple**: complex pages like Quicken's add friction, while GitLab's three clear plans reduce it.

## Mindmap
```mermaid
mindmap
  root((Business Models and Pricing))
    Winning Models
      SaaS recurring revenue
      Transactional in money flow
      Marketplaces network effects
      Advertising rarely wins
    Top 100 Lessons
      Top ten hold half value
      No consulting or affiliate
      Hardware needs heavy capital
      Platform risk kills startups
    Moats
      Network effects
      Lock-in and switching costs
      Technical innovation
      Organic distribution
    Retention
      Recurring revenue compounds
      Churn makes leaky bucket
      Five point gap decides
    Pricing Insights
      You should charge
      Price on value
      Most startups undercharge
      Pricing is not permanent
      Keep pricing simple
    Segment Story
      Started free product
      Advisor demanded 120k ask
      Closed 18k deal
      Sold for three billion
```
""",
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
        _yt(
            "How To Price For B2B",
            "4hjiRmgmHiU",
            "18 min",
            """# How To Price For B2B

## Summary
Tom, a YC partner, addresses the moment a promising sales call ends with the customer asking for pricing and the founder freezes, defaulting to ludicrously low numbers like $19 or $49 a month because larger asks feel impossible to say with a straight face. His framework has three core elements. First and by far most important is the value equation: sit with your champion and write down, step by step, the value your product delivers — a cost saving, a time saving, or a revenue increase — and have them challenge the assumptions, since the document becomes their tool for justifying the purchase to their boss or CFO. His example: a company with 100 customer support agents at $100,000 fully loaded cost each spends $10 million; an AI tool eliminating 20% of query time saves $2 million. Price at 25% to 50% of delivered value — roughly $700,000 here — so the customer keeps about two-thirds. The equation also supplies pilot success metrics: run 10 agents for a month and verify the 20% saving, adjusting price with the measured result.

Second is cost, which should only ever be a floor, never a cost-plus starting point; aim for 80% to 90% software margins, treat AWS and OpenAI credits as cash costs, and know that pricing below cost is a risky land-grab bet that costs will fall. Third is competition: do not enter price wars, because undercutting spirals into a race to the bottom, and commodity markets like airlines end up with 2.7% net margins — differentiate on functionality and value instead.

For structure and tactics: mirror how customers already pay for similar software, keep pricing simple, and prefer committed monthly or annual recurring revenue over pure usage pricing, whose revenue can fall off a cliff in a downturn. One technique: run usage-based pricing for a month or two (say $15,000 a month), then offer a $12,000 flat monthly fee on a 12-month contract. Ask your champion's signing authority and keep pilot pricing under it, like $14,999 under a $15,000 limit. Since enterprise value equations differ per customer, keep cheap self-serve plans public but gate features enterprises cannot live without — SOC 2 reports, single sign-on, audit logs — behind contact-sales pricing, sometimes 10 times higher. Pricing dictates sales channels: with a 5:1 ratio of new ARR to sales compensation, a $100,000 salesperson must close $500,000 a year, feasible with large or $25,000 contracts but not with $1,000 contracts. Keep pilots short with clear success criteria, or sign annual contracts with 30-to-60-day money-back opt-outs. If all else fails, pick a comparable number and raise it 50% each pitch until more than 25% of deals are lost on price alone.

## Main ideas
- **The value equation comes first** — Write down with your champion the cost saving, time saving, or revenue increase your product delivers, and let them challenge every assumption.
- **Price at a third of value** — Charge roughly 25% to 50% of the value delivered so the customer keeps about two-thirds and the CFO sees a clear return.
- **The equation defines pilot metrics** — The written value assumptions become the success criteria a short pilot must prove, and price can adjust with the measured results.
- **Cost is only a floor** — Never build cost-plus pricing; target 80% to 90% gross margins and treat cloud and AI credits as real cash costs.
- **Never fight a price war** — Undercutting a competitor spirals into a race to the bottom, so differentiate on functionality and value instead of matching a commodity price.
- **Mirror familiar pricing structures** — Ask what customers already pay for similar software and how it is structured, then keep your own pricing simple.
- **Prefer committed recurring revenue** — Monthly or annual commitments protect revenue in downturns, and usage-based customers can be converted to flat monthly minimums with volume discounts.
- **Stay under signing authority** — Learn what your champion can approve alone and keep pilot pricing below that threshold to keep deals moving fast.
- **Gate enterprise features** — Publish cheap self-serve plans but hold SOC 2, single sign-on, and audit logs behind contact-sales pricing that can run 10 times higher.
- **Experiment upward** — Pick a number, raise it 50% with each new pitch, and know you are in the right ballpark when over a quarter of deals are lost purely on price.

## Mindmap
```mermaid
mindmap
  root((B2B Pricing))
    Value Equation
      Write it with champion
      Cost time or revenue
      Price a third of value
      Gives pilot success metrics
    Cost
      Only a floor
      Target 80-90 percent margins
      Credits are cash costs
      Below cost is risky
    Competition
      Avoid price wars
      Differentiate your product
      Commodities lose margin
    Pricing Structure
      Mirror familiar structures
      Keep it simple
      Prefer committed recurring revenue
      Stay under signing authority
    Enterprise Plans
      Value differs per customer
      Gate compliance features
      Contact sales pricing
    Practical Tactics
      Pricing dictates sales channels
      Short pilots clear criteria
      Raise price each pitch
```
""",
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
        _yt(
            "The Sales Playbook For Founders",
            "DH7REvnQ1y4",
            "19 min",
            """# The Sales Playbook For Founders

## Summary
This talk lays out the typical progression a B2B founder goes through when closing their first contracts, from poorly defined, overly long unpaid design partnerships to the pro move: a rapid, tightly run sales process that produces contractually recurring revenue straight off the bat. Ninety percent of the time founders get stuck in the earliest stages, while only 5-10% try to speedrun the sequence before their product or social proof is ready. Design partnerships sound good in theory, spending time in a big-logo customer's office co-designing the product, but they often run three to six months with vague scope and low engagement, since the customer is not paying and has their own business to run. The speaker recommends using time on site to identify a narrow burning problem, asking what part of the job the customer hates most, doing the work manually, or even going undercover as an auditor or accountant, then building a narrow wedge product in as little as 48 hours and selling it to ten similar customers instead of overbuilding a broad platform.

The next stages are free trials, pilots, and proofs of concept. These again tend to be too long, at two or three months, with no target. A well-designed pilot proves a defined value equation: a customer-service AI that solves 20% of inbound queries might let the customer shrink a 100-person team to 80, saving $1 million in salaries and justifying a $200,000 price. Techniques include back testing on historical data, side-by-side trials, taking 1% of volume, or starting in a small geography, and founders must have the willingness-to-pay conversation. Paid trials work better: a financial commitment, even a $10,000-$20,000 charge a champion can approve on a corporate card, makes customers take the pilot seriously. Founders should wait for a live project, insist on dedicated people and data, schedule check-ins every couple of days, keep the trial to seven to 14 days, and track time to first value like a north-star metric, avoiding API integrations in favor of Excel imports or email.

The pro move is a recurring contract with a 30- or 60-day opt-out that converts automatically, one sales process yielding recurring revenue, though founders should report such ARR carefully to investors. The talk closes with customer success (a company that signed $4 million in contracts but implemented under $2 million) and tips: start SOC 2 early, treat your champion like a co-founder, map every stakeholder, get on a plane to visit customers, accept any contract terms that are not company-ending, and use scarcity.

## Main ideas
- **Progression to recurring revenue** — founders should advance as fast as possible from unpaid design partnerships to tightly run sales processes that close new ARR every week.
- **Design partnerships usually fail** — they run three to six months with vague scope and low customer engagement because the customer is not paying for your time.
- **Narrow wedge products win** — identify one burning problem, build a wedge in as little as 48 hours, and sell it to ten similar customers instead of overbuilding a broad platform.
- **Pilots need defined success metrics** — agree a value equation upfront, like solving 20% of customer queries to save $1 million in salaries for a $200,000 price.
- **Paid trials create commitment** — even a $10,000-$20,000 charge a champion can approve on a corporate card makes the customer take the pilot seriously.
- **Time to first value is the north-star metric** — reducing it from weeks to hours, using janky Excel or email flows instead of API integrations, is the biggest lever for pilot conversion.
- **Recurring contracts with opt-outs are the pro move** — a 30- or 60-day money-back period turns one sales process into a recurring contract with no second negotiation.
- **Customer success matters after signing** — one company signed $4 million in contracts but implemented less than $2 million for lack of a customer success function.
- **Practical closing tips** — start SOC 2 immediately, treat your internal champion like a co-founder, map all stakeholders, visit customers in person, and use scarcity.

## Mindmap
```mermaid
mindmap
  root((B2B Sales Playbook))
    Design Partnerships
      Too long and vague
      Observe customer work onsite
      Magic wand question
      Build narrow wedge fast
    Free Pilots
      Define success metrics
      Prove the value equation
      Low risk trial designs
      Willingness to pay talk
    Paid Pilots
      Upfront financial commitment
      Champion approvable amounts
      Short seven day trials
      Track time to value
    Recurring Contracts
      Opt-out period magic
      One sales process
      Careful ARR reporting
    Closing Tips
      Start SOC 2 early
      Champion as co-founder
      Visit customers in person
      Use scarcity
```
""",
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
        _yt(
            "Enterprise Sales",
            "0fKYVl12VTA",
            "23 min",
            """# Enterprise Sales

## Summary
Pete Koomen, YC group partner and Optimizely co-founder and CTO (winter 2010), walks through closing your first enterprise customers via the funnel stages: prospecting, outreach, qualification, pricing, closing, and implementation. He opens with two lessons: sales is learnable — he and co-founder Dan figured it out by trial and error — and before product-market fit, only founders can sell, because such sales is entrepreneurial, requiring vision, credibility, experimentation, and a tight product feedback loop. Nor is a business co-founder needed: technical founders bring expertise and conviction, and sales is not tricks but helping people solve problems.

Prospecting starts with a hypothesis — customer X has problem Y — like Optimizely's: marketers at small and medium tech, media, and e-commerce companies want A/B tests without writing code. Build company lists, filter them (Optimizely used BuiltWith to spot analytics tools), and find the right humans with Apollo or LinkedIn Sales Navigator. For outreach, inbound demand is easiest — launch often, publish technical content, build self-serve demos, answer forum questions, attend conferences — then seek warm intros, and write cold emails by hand: short, specific, with a clear ask; only send emails you would be excited to read. He warns against chasing whoever is easiest to talk to: selling enterprise software to startups, or going bottom-up with top-down products like hospital software, yields feedback that is useless at best.

The first call is for qualifying, not pitching: ask about the problem, its cost, the budget, and who makes the buying decision, because you sell to a human, not a monolith. Treat the demo as a movie script: recap the main character and her problem, tell a story instead of a feature tour, include magic moments, and personalize everything — Optimizely built demos running on the prospect's own website and watched marketers' eyes light up. On pricing, treat every conversation as an experiment; the commonest mistake is charging too little. Dan once quoted $10,000 a month, was negotiated down to $2,000 — five times the initial expectation — and the customer still bought; the Collison brothers priced Stripe above competitors. Since key pricing conversations happen without you in the room, arm your champion with a one-pager. Closing means surviving procurement: ask upfront how they buy, parallelize security questionnaires, use Common Paper's open-source templates, and lean on your champion. Finally, implementation is your job, not the customer's — Optimizely closed six-figure deals whose buyers never ran a single test — so project-manage onboarding with shared roadmaps, owners, and check-ins; the funnel ends only when usage is habitual. He recommends Peter Kazanjy's book Founding Sales and urges founders to just get started.

## Main ideas
- **Sales is learnable and founders must do it** — Pre-product-market fit sales requires vision, credibility, and a tight product feedback loop, so it cannot be hired out to salespeople.
- **Technical founders have an edge** — Expertise in the problem and sincere conviction matter more than tricks, because sales is about helping people solve problems.
- **Prospecting needs a hypothesis** — A clear statement that customer X has problem Y makes it obvious which companies and which humans to target.
- **Inbound beats cold outreach** — Launching often, technical content, self-serve demos, forums, and conferences get prospects to reach out to you.
- **Only send emails you would love to read** — Handwritten, short, specific cold emails with a clear ask survive people's built-in spam filters.
- **Avoid easy but bad customers** — Talking to startups about enterprise products or going bottom-up on top-down products creates the illusion of progress with useless feedback.
- **Qualify before you pitch** — The first call is for questions about the problem, budget, and decision-making authority, not for a product pitch.
- **Demo like a movie script** — Recap the customer's problem, tell a story with magic moments, and personalize the demo down to their own website and logo.
- **Charge more than feels comfortable** — Customers who truly need your product are hard to scare away with high prices, and higher prices test seriousness.
- **Implementation is your job** — Deals only succeed when you project-manage onboarding with roadmaps, owners, and check-ins until usage becomes habitual.

## Mindmap
```mermaid
mindmap
  root((Enterprise Sales))
    Founders Must Sell
      Sales is learnable
      Pre PMF needs founders
      Expertise and conviction
      Helping not tricking
    Prospecting
      Start with hypothesis
      Filter company lists
      Find the right humans
    Outreach
      Generate inbound demand
      Warm intros first
      Handwritten short cold emails
      Avoid easy bad customers
    First Call And Demo
      Qualify with questions
      Sell to humans
      Demo as movie script
      Personalize with magic moments
    Pricing
      Experiment with price points
      Charging too little hurts
      High prices test seriousness
      Arm your champion
    Closing And Implementation
      Ask how they buy
      Parallelize procurement steps
      Implementation is your job
      Project manage onboarding
```
""",
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
        _yt(
            "How To Start A Dev Tools Company",
            "z1aKRhRnVNk",
            "33 min",
            """# How To Start A Dev Tools Company

## Summary
Nicolas, a YC group partner and co-founder and CEO of Algolia, explains how to start a dev tools company across three phases: founding team and idea, prototype to MVP, and go-to-market. Dev tools are software that helps developers build products: IDEs like VS Code, APIs like Stripe, Twilio and Algolia, libraries and frameworks like React or LangChain, and infrastructure like AWS. YC has funded hundreds, including public companies GitLab and PagerDuty. Founding teams should be developers, since you are your own audience, and 74% of YC dev tools companies had only technical co-founders versus 45% of other companies, so you do not need a business founder. On ideas, build-time tools like documentation, QA and testing are obvious, noisy, nice-to-haves, while runtime ideas such as APIs are must-haves whose usage grows with customers, as with Stripe. Libraries are hard to monetize except via hosting, as Next.js does with Vercel. Crowded spaces like LLM observability demand differentiation, but the bigger mistakes are waiting for the perfect idea, sticking with a wrong one too long (50% of YC companies pivot), and hiring too early.

For the prototype, build quick and dirty, assume you will throw away 90% of the code, and aim to be 10x better on a tiny thing a niche cares about. Algolia began as a glorified autocomplete and closed a $2,000-a-month contract from a demo using only a command line and a simple web page. Find users through personalized outreach starting with your network, and launch repeatedly on Hacker News's Show HN, as Segment and Ollama did; do things that don't scale, like Stripe engineers implementing the product side by side with early customers.

On go-to-market, open source is essentially mandatory for libraries, frameworks, and tools touching sensitive data, and it builds awareness, differentiation (Supabase versus Firebase, PostHog versus Amplitude), and enterprise trust: Medplum's open source arguably shortened enterprise sales cycles by a year or more. Monetize via hosting or an open-core enterprise tier with SSO, audit logs and SLAs, but avoid charging for support, which rewards building complexity. Closed tools use usage-based pricing or good-better-best plans. Founders should sell themselves until roughly $1 million ARR, then hire technical salespeople; Algolia's called themselves product specialists, and PostHog's CTO leads sales. Show demos instead of decks: Algolia had no sales deck before $10 million ARR, and leaning technical won more deals. Marketing means being helpful in communities, launching often like Supabase's quarterly launch weeks, treating documentation as a first-class product written by developers, and having engineers do support, one of whom fixed and deployed a customer's bug in 20 minutes. Founders should lead marketing for a long time, since traditional CMOs rarely understand developers.

## Main ideas
- **All-technical founding teams work** — 74% of YC dev tools companies had only technical co-founders, and learning to sell is easier than teaching someone to speak to developers.
- **Runtime beats build time** — build-time ideas like docs and QA are crowded nice-to-haves, while runtime products like APIs are critical must-haves whose usage grows with the customer.
- **Start before the idea is perfect** — waiting is a mistake, 50% of YC companies pivot anyway, and doing the reps leads you to the right idea.
- **Prototype quick and dirty** — assume 90% of the code gets thrown away and be 10x better on a tiny thing; Algolia closed $2,000 a month from a command-line demo.
- **Launch early and often on Hacker News** — Show HN is the ideal venue, and Segment and Ollama both took off from repeated launches there.
- **Open source is a go-to-market** — mandatory for frameworks and sensitive data, it builds trust with enterprises and differentiates you, monetized through hosting or open-core tiers.
- **Founders sell until 1 million ARR** — no one else can sell your product early, and the first sales hires should be technical, like Algolia's product specialists.
- **Show, don't tell** — developers hate sales decks, so demo the product; Algolia had no deck before $10 million ARR.
- **Documentation and support are marketing** — docs should be first-class and written by developers, and engineers doing support delights users and improves the product.
- **Founders lead marketing** — traditional CMOs disappoint dev tools companies, and Algolia's best marketing came from engineers doing monthly marketing hacks.

## Mindmap
```mermaid
mindmap
  root((Dev Tools Startups))
    Founding
      All technical teams work
      Runtime beats build time
      Avoid crowded obvious ideas
      Start before perfect idea
    Prototype To MVP
      Quick and dirty builds
      Throw away most code
      10x better on niche
      Talk with users early
    Finding Users
      Personalized outreach first
      Launch on Hacker News
      Launch again and again
      Do unscalable things
    Open Source
      Must for frameworks
      Trust for enterprises
      Monetize hosting or core
      Avoid support revenue
    Sales
      Founders sell first
      Hire technical salespeople
      Show demos not decks
      Bottom up adoption
    Marketing
      Docs are marketing
      Engineers do support
      Be helpful in communities
      Founders lead marketing
```
""",
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
        _yt(
            "Consumer Startup Metrics",
            "fdD4y4Civp4",
            "22 min",
            """# Consumer Startup Metrics

## Summary
Tom Blomfield, founder of the online bank Monzo and a veteran of the YC dating startup Grouper, walks through the metrics that matter most for consumer companies. He starts with headline user growth: 15% month over month is good (about 5x per year), 10% is okay (roughly tripling annually), and 5% or lower is unlikely to reach breakout success. He then splits growth into organic and paid. Monzo reached a million customers before spending on marketing, powered by virality (one user introducing others through product use, as with Facebook photo-tagging emails or Wordle score sharing) and network effects (Metcalfe's law: the product improves with more nodes, as with WhatsApp messaging or Monzo's Venmo-style transfers, joint accounts, and holiday pots). He urges founders to find shareable moments and shift from single-player to multiplayer thinking, since viral loops and network effects pay back forever while ad spend is gone the next day. Paid referral schemes should be treated as paid acquisition, watching for cannibalization and fraud; a friend milked Zipcar's referral scheme via cheap Google Ads and drove free for a year before a lifetime ban.

For paid growth, track where every user comes from using UTM referrers or by simply asking, compute customer acquisition cost per channel, and record each user's source forever: a money-saving blog sent Monzo cheap signups whose lifetime value was negative because they withdrew cash at ATMs. CAC must be measured to an active, monetized, retaining user, not a mere signup, since first-week drop-off can hit 80-90%. The best consumer companies get 80% or more of growth organically; below a 50/50 split is worrisome because ad platforms extract margins and platform shifts like iOS tracking changes can wipe out a business overnight.

On unit economics (per-customer revenue minus variable costs like plastic cards, customer service, and fraud), Monzo generated about $50 of revenue per customer but scaled at negative 30-40 pounds per customer to half a million users before fixing it; fix economics before scaling. On retention, define the right activity period (a weekly transaction for Monzo) and find the magic moment that predicts long-term retention: seven friends in ten days for Facebook, three phone-book friends for Monzo, then re-engineer onboarding around it without obsessing over the exact threshold. Finally, net promoter score (promoters scoring 9-10 minus detractors scoring 0-6) should exceed +50 for a new consumer company; Monzo sat at 75-80 and Tesla at 96. Collect it in a consistent way (Grouper's score dropped 20 points overnight after a method change) and improve it by fixing what detractors report.

## Main ideas
- **Growth benchmarks**: 15% month-over-month user growth is good, 10% is okay, and 5% or less is unlikely to reach breakout success.
- **Virality**: design shareable moments where users naturally introduce the product to others, like Facebook photo tagging or Wordle score posts.
- **Network effects**: make the product better with each new user, shifting from single-player to multiplayer thinking as Monzo did with transfers and joint accounts.
- **Organic beats paid**: viral loops and network effects pay back for the life of the company, while ad spend must be repeated; the best consumer companies are 80%+ organic.
- **Referral schemes are paid acquisition**: watch for cannibalization of referrals that would have happened anyway and for fraud like the Zipcar ads scheme.
- **CAC to good users**: measure acquisition cost per channel to an active, monetized, retaining user, and record each user's source in your database forever.
- **Unit economics first**: track per-customer revenue minus variable costs and fix negative economics before scaling, unlike early Monzo at minus 30-40 pounds per customer.
- **Magic moment**: find the behavior that predicts long-term retention, like seven friends in ten days at Facebook, and re-engineer onboarding so users hit it fast.
- **NPS above +50**: a new consumer company needs a sky-high net promoter score, gathered with a consistent method and improved by fixing detractor complaints.

## Mindmap
```mermaid
mindmap
  root((Consumer Startup Metrics))
    Growth Rate
      15 percent monthly is good
      10 percent is okay
      5 percent rarely breaks out
    Organic Growth
      Virality shareable moments
      Network effects Metcalfe law
      Loops pay back forever
      Referrals are paid acquisition
    Paid Growth
      Track every user source
      CAC per channel
      Measure to retained users
      Over 80 percent organic
    Unit Economics
      Revenue minus variable costs
      Fix before scaling
      Monzo negative then positive
    Retention
      Choose right activity period
      Find the magic moment
      Reengineer onboarding flow
    Net Promoter Score
      Promoters minus detractors
      Plus 50 minimum
      Consistent collection method
      Fix detractor complaints
```
""",
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
        _yt(
            "B2B Startup Metrics",
            "_mKeVGSqQac",
            "24 min",
            """# B2B Startup Metrics

## Summary
Tom Blomfield, YC group partner and Monzo founder, opens by comparing metrics to an airplane's instruments: without them you are flying blind. He has seen founders launch on Hacker News and Product Hunt with hundreds of users yet no idea whether they are new or returning, daily or weekly active, or churning instantly, so basic metrics should be built in before launch. Two warnings bracket the talk: the opposite extreme of a 500-metric pre-launch dashboard is also bad, since small startups lack the data volume to split test button colors (though big decisions like an $80 versus $200 price are worth testing), and metrics must never replace talking to customers; Airbnb's Brian still hosts guests in his home.

Getting started means picking four or five key metrics, using the simplest analytics available (plain SQL queries or PostHog's SQL tool), and agreeing on written, centralized definitions so marketing and sales stop fighting over what counts as a lead. Definitions must stay consistent; switching from weekly to monthly actives to flatter the numbers only fools yourself. He warns against vanity metrics like page views, GMV, or gross transaction value: a Middle East neobank he advised showed GTV growing 50% every two weeks while revenue stayed flat, because big customers were being bought with massive cashback. Revenue is the right core metric for most B2B companies, and one impressive founder sent ten straight investor updates topped by a big zero, keeping herself honest. Every investor update needs revenue, burn rate (monthly costs minus revenue), and runway: a million dollars in the bank at $100,000 monthly burn means ten months to bankruptcy.

The deep dives cover retention and gross margin. Cohorts whose retention flattens stack into a layer cake of recurring revenue, as at his payments company GoCardless, while cohorts that churn to zero make growth a leaky bucket and a futile endeavor. Net dollar retention nets upsells against churn: ten customers at $10K MRR who lose two but upsell three to $20K end the year at $110K, or 110% NDR. Early B2B SaaS should target 125-150% because initial pricing is too low, features keep shipping, and sales improves; below 100% means fix churn rather than pour money into sales. Gross margin is revenue minus cost of goods sold; AI companies' payments to OpenAI or Anthropic are real COGS even when hidden by free credits, and operational businesses at 5-15% margins need far more revenue than 95%-margin software. Blitzscaling negative-margin businesses, as Uber did with capital as a weapon, left a wasteland of startups; Monzo lost 30-40 pounds per customer before flipping its unit economics and eventually reaching profitability.

## Main ideas
- **Metrics are instruments**: launching without metrics is flying blind, so build basic tracking into the product before launch.
- **Four or five key metrics**: pick a handful, use the simplest analytics solution such as SQL queries or PostHog, and grow the list over time.
- **Agreed, stable definitions**: written centralized definitions prevent internal fights, and changing definitions to flatter numbers only fools yourself.
- **Avoid vanity metrics**: GMV or gross transaction value can grow while revenue stays flat, as with the neobank buying volume through cashback rebates.
- **Revenue, burn rate, runway**: the three numbers that belong at the top of every investor update; hiding them suggests something to hide.
- **Retention layer cake**: cohorts whose retention flattens stack into ever-growing revenue, while churn-to-zero cohorts make a leaky bucket you can never fill.
- **Net dollar retention**: upsells netted against churn should be well above 100% for early B2B SaaS, ideally 125-150%; below 100% means fix the product, not sales.
- **Gross margin matters**: AI model costs are real cost of goods sold even when hidden by free credits, and operational businesses run far below software's 95%.
- **Do not scale negative margins**: the zero-interest-rate blitzscaling era left a wasteland of startups; Monzo fixed its per-customer losses before scaling profitably.
- **Talk to customers anyway**: run the startup on a blend of metrics, customer conversations, and product intuition.

## Mindmap
```mermaid
mindmap
  root((B2B Startup Metrics))
    Why Metrics
      Instruments not flying blind
      Build before launch
      Impresses investors
      Still talk to customers
    Getting Started
      Pick four or five
      Simple SQL analytics
      Agreed written definitions
      Keep definitions consistent
    Core Numbers
      Revenue is key
      Burn rate monthly
      Runway in months
      Avoid vanity metrics
    Retention
      Cohort layer cake
      Leaky bucket churn
      Net dollar retention
      Target above 100 percent
    Gross Margin
      Revenue minus COGS
      AI model costs count
      Free credits hide cost
      Do not scale negative
```
""",
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
        _yt(
            "Setting KPIs and Goals",
            "6DTK9yDP6p0",
            "27 min",
            """# Setting KPIs and Goals

## Summary
Divya, a two-time YC founder and visiting group partner, explains how KPIs and prioritization speed the journey to product-market fit. As a founder nobody tells you how to spend your time: KPIs are the metrics you track and report internally and externally, and prioritization decides the order of work and, crucially, which important tasks you skip today. She warns against fake progress such as optimizing paperwork, perfectionism on features nobody uses, premature scaling, and choosing intellectually hard problems over what users want, recalling how her own team felt busy and flattered being taken to lunches by law firms before they had even launched. Moving slowly burns money, gives competitors time to copy you, and carries emotional and fundraising costs.

Her prioritization method: identify your top KPI (revenue growth once launched), set a weekly goal that ladders up to longer-term targets, as Airbnb's founders did by writing weekly goals on their bathroom mirror, and find the single biggest bottleneck. Super Daily, an Indian grocery subscription startup sold to Swiggy in 2018, saw high-intent users churn late in signup because a specific milk brand was missing; onboarding that brand raised conversion 50%, no UX beautification needed. Then write ideas down before chasing them, rank by probability of success and then complexity, pick only a couple, run honest retros, and fail fast, because indecision is worse than a wrong pick. Task lists should center on talking to users and building from their feedback, not passive fundraising coffees, conference attendance, or arbitrary technical milestones like an unrequested Android app. She catalogs mental traps: low-leverage tasks that give a satisfying sense of accomplishment, fooling yourself that slow growth is product-market fit (growth at DoorDash felt fundamentally different), perfectionism and indecision, over-investing in downside protection instead of chasing upside (spreadsheets are fine until they break), and chipping at small problems while an existential one looms, like building one-click ordering for 150 churning users.

The primary KPI should be revenue growth, with exceptions such as marketplace GMV or signups and letters of intent for long-sales-cycle enterprise; keep three to five secondary KPIs like retention, unit economics, and CAC payback. Comparing her startup Rickshaw with DoorDash: both focused on order volume with similar early traction, but Rickshaw later hedged between growth and unit economics and landed in a no man's land of slow growth before being acquired by DoorDash in 2017. Per Paul Graham, 5-7% weekly growth is good and 10% exceptional; set targets both top-down and bottoms-up. Scribd grew a free product for four years, then charged in mid-2010, lost over 90% of users, and revenue grew by infinity percent. Homework: write down your KPIs, set ambitious targets, and audit your task list.

## Main ideas
- **KPIs drive prioritization**: choose the right key performance indicators, then spend your finite time only on the tasks most likely to move them.
- **Revenue growth is the primary KPI**: after launch a non-revenue KPI is rarely right, with narrow exceptions like marketplace GMV or enterprise letters of intent.
- **Attack the biggest bottleneck**: Super Daily lifted conversion 50% by onboarding a missing milk brand instead of beautifying its signup screen.
- **A simple framework**: write ideas down, rank by probability of success then complexity, pick a couple, run honest retros, and fail fast.
- **Fake progress feels good**: paperwork optimization, passive investor coffees, conferences, and arbitrary technical milestones boost ego without advancing product-market fit.
- **Beware mental traps**: low-leverage tasks, mistaking slow growth for fit, perfectionism, downside protection over upside chasing, and dodging existential problems.
- **Do not hedge on two goals**: Rickshaw split focus between growth and unit economics and landed in a no man's land of slow growth.
- **Set targets both ways**: combine top-down milestones like $5,000 MRR by a deadline with bottoms-up weekly projections; 5-7% weekly growth is good, 10% exceptional.
- **Charge from day one**: free users give the wrong feedback; Scribd lost over 90% of users when it started charging but finally had a business.

## Mindmap
```mermaid
mindmap
  root((KPIs and Goals))
    Why Prioritize
      Time is finite
      Speed to market matters
      Busy is not progress
    Choosing KPIs
      Revenue growth primary
      Retention and churn secondary
      Unit economics and CAC
      Avoid vanity metrics
    Prioritization Framework
      Find biggest bottleneck
      Rank ideas by success
      Honest weekly retros
      Fail fast keep moving
    Mental Traps
      Low leverage tasks
      Fooling yourself on growth
      Perfectionism and indecision
      Ignoring existential problems
    Setting Targets
      5 to 7 percent weekly
      Top down milestones
      Bottoms up projections
    Exceptions
      Marketplaces GMV or signups
      Enterprise letters of intent
      Payback period over LTV
      Charge from day one
```
""",
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
        _yt(
            "How Startup Fundraising Works",
            "zBUhQPPS9AY",
            "28 min",
            """# How Startup Fundraising Works

## Summary
Brad Flora, a YC group partner who founded Perfect Audience (YC Summer 11, acquired in 2014) and later invested in 150 YC companies through his fund, dismantles seven myths about startup fundraising. Myth one: fundraising is glamorous. Shark Tank and pitch competitions are marketing shows; real fundraising looks like quiet coffee chats and repeated one-on-one Zoom meetings. YC company Freshpaint met 160 investors, got 39 yeses with checks ranging from 5K to 200K dollars, and took four months and 18 days to raise 1.6 million — a grind, but straightforward. Myth two: you must raise money before starting. The best founders build a first version, get users, and only then raise; Solugen built a desktop-sized reactor, sold hydrogen peroxide to hot tub supply stores for 10,000 dollars a month, raised 4 million to get started, and has since raised 400 million. Myth three: you must impress investors. You need to convince, not impress — the best startups sound terrible at first (Airbnb, DoorDash, OpenSea). Flora recalls Sequoia's Michael Moritz stopping his prepared pitch to just talk about the business, and Retool's founder winning his check with a crude live demo instead of a deck, en route to a 4-billion-dollar valuation. Myth four: fundraising is complicated, slow, and expensive. Big series A and growth rounds dominate headlines, but typical seed rounds of 500K to a couple million close in days or weeks using YC's safe — a five-page document with essentially two terms to negotiate and no legal fees. Myth five: raising means losing control. Safes grant no board seats, create no shareholders until the next round, and carry no information rights; founders sell 10 to 20 percent and keep control, like Zapier, which raised about a million dollars once, went fully remote a decade before it was cool, never raised again, and reached 100 million in revenue. Bootstrapping forever, Flora argues, just stretches fundraising pain across the whole life of the company. Myth six: you need a fancy network. Investors are coin-operated lizard people who care about making money; Podium, two founders from Utah selling review software to tire shops, raised more than 200 million. Myth seven: rejection means your startup is bad. Envision's founder was rejected more than 50 times before landing a 25K check, and the company sold for 275 million; Whatnot raised only a fraction of its seed goal yet was worth 3.7 billion two and a half years later. The big myth underneath them all — this is not for you — is false: there has never been a better time to raise.

## Main ideas
- **Fundraising is a grind, not glamour**: real rounds are coffee chats and Zoom calls repeated over and over, as Freshpaint's 160 investor meetings over four-plus months show.
- **Build first, raise second**: the best founders make a simple product and get users before talking to investors, because investors want to jump on trains already in motion.
- **Convince, do not impress**: there are no magic words — make something people want and explain in plain language how there is even a one percent chance it gets huge.
- **Safes make seed rounds fast and cheap**: a five-page standard document with only an amount and a valuation cap to discuss lets founders close millions in clicks without lawyers.
- **Seed founders keep control**: safes involve no board seats, no shareholders yet, and no information rights, so founders selling 10 to 20 percent still call all the shots.
- **Bootstrapping forever stretches the pain**: funding only from revenue is scary, miserable, and distracting, so rip off the Band-Aid and raise once up front.
- **No fancy network required**: Podium's founders had no Silicon Valley connections, but tens of thousands of dollars a month in revenue made investors notice.
- **Rejection is part of the process**: Envision and Whatnot were rejected repeatedly and still reached huge outcomes — you only need a few investors to believe.

## Mindmap
```mermaid
mindmap
  root((Fundraising Myths))
    Reality of Raising
      Coffee chats not Shark Tank
      Freshpaint met 160 investors
      Fundraising is a grind
    Build Before Raising
      Product and users first
      Investors back momentum
      Solugen desktop reactor
    Convince Not Impress
      Great startups sound terrible
      Plain simple language
      Retool live demo
    Safes Make It Easy
      Five page document
      Two terms to discuss
      No lawyers needed
      Founders keep control
    Network and Rejection
      Investors care about traction
      Podium sold to tire shops
      Envision rejected 50 times
      Rejection is normal
```
""",
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
        _yt(
            "How to Apply And Succeed at Y Combinator",
            "B5tU2447OK8",
            "25 min",
            """# How to Apply And Succeed at Y Combinator

## Summary
Dalton explains why and how to apply to Y Combinator. Applying is worth it because answering the application questions organizes and clarifies your thinking about your own business, and the cost-benefit is lopsided: a deliberately fast application against potentially enormous upside. He frames applying as luck creation: you become luckier by putting yourself out there and taking risks, while avoiding rejection shrinks your surface area for good surprises. He then dismantles common excuses. There is no such thing as too early, since many great YC companies pivoted after getting in or had not written code; nor too far along, since YC accepts companies with half a million dollars in annual recurring revenue or a million dollars raised. Watching YC videos is not the batch, which offers one-on-one office hours, secrets never said on the internet, and internal tools and fundraising data. When gatekeepers discourage you, ask pointed questions: an investor who says skip YC should be asked whether they will invest themselves and on what terms. YC funds every vertical and country, funds multiple companies in the same space, and counts repeat applications as a plus; some batch members applied five, six, or seven times. Good reasons not to apply: wanting to work on the company only briefly, not wanting venture capital, or running a non-technology business.

For the application itself: apply on the website with no warm intros, decks, or emails needed. Fill everything out including founder biographies, mind grammar, make a founder video that follows the directions since instruction-following is weighed in selection, and keep answers clear and concise. As a reader, Dalton asks who the founders are, what the idea is, what exists today, whether there is evidence people want it, whether the founders are serious, and what is impressive or unique. A good application lets him tell a story; GitLab's explained in a few sentences what it was and that a hundred thousand organizations used it, while weak applications obfuscate everything. Dishonesty about revenue, traction, or background is automatically disqualifying, and extraordinary claims require extraordinary evidence. The biggest variable for interview odds is technical talent: a founding team hireable into a technical role at a top YC company has 5x better odds, while non-technical teams on unlaunched tarpit ideas have the lowest; co-founder matching helps, and paid connectors claiming YC access are scammers. The interview is a ten-minute Zoom with basic, context-dependent questions, not an adversarial pitch: interviewers are the people you would work with, so avoid memorized speeches, listen, show mastery of numbers and risks, be honest and self-aware, and be yourself rather than performing Shark Tank. Rejected interviewees get actionable feedback, and addressing it in a future application is heavily weighted in your favor.

## Main ideas
- **Applying creates luck**: putting yourself out there where rejection is possible expands the surface area for surprising upside.
- **Low cost, huge upside**: the application is intentionally fast to fill out, so the trade-off of applying is strongly positive.
- **No such thing as too early or too late**: YC accepts founders who have not written code and companies with $500K ARR or a million dollars raised.
- **Question the gatekeepers**: if an investor discourages applying, ask whether they will invest themselves and on what terms.
- **Repeat applications are a plus**: some accepted founders applied five to seven times, and progress between applications shows seriousness.
- **Tell a clear story**: strong applications like GitLab's let the reader grasp founders, product, and traction in a few sentences, while weak ones obfuscate.
- **Honesty is non-negotiable**: misrepresenting revenue, traction, or background is automatically disqualifying, and extraordinary claims need extraordinary evidence.
- **Technical talent is the biggest variable**: teams hireable into technical roles at top YC companies have 5x better interview odds.
- **The interview is not adversarial**: ten minutes of basic, context-dependent questions from future colleagues, so listen, be natural, and skip the memorized speeches.
- **Internalize rejection feedback**: addressing interviewer feedback in a later application is heavily weighted in your favor.

## Mindmap
```mermaid
mindmap
  root((Applying to YC))
    Why Apply
      Clarifies your thinking
      Tiny cost huge upside
      Creates luck
    Bad Excuses
      Too early
      Too far along
      Videos replace the batch
      Discouraging gatekeepers
    Application Tips
      Fill everything out
      Follow video directions
      Clear concise answers
      Tell a clear story
      Honesty is required
    Improving Odds
      Technical talent 5x odds
      Cofounder matching works
      No warm intros needed
      Beware scammers
    Interview
      Ten minute Zoom call
      Basic context questions
      Not adversarial
      Be yourself
      Address rejection feedback
```
""",
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
