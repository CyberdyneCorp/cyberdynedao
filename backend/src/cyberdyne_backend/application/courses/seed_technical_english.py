"""Academy seed content — the Technical English for Engineers track
(Beginner → Advanced).

* ``technical-english-basics``        — core vocabulary, present simple,
  numbers/units, reading code aloud, meeting questions, email/chat basics
* ``technical-english-intermediate``  — processes & pipelines, comparing
  trade-offs, code-review English, incident reports (past tenses),
  conditionals for debugging, standups & meetings
* ``technical-english-advanced``      — architecture discussions, presenting
  demos, negotiating decisions, writing specs/RFCs, tech idioms & phrasal
  verbs, technical-interview English

This is a LANGUAGE course: the audience reads the explanatory prose in their
own language (pt-BR / es / fr via auto-translation), but the **English being
taught** must survive translation untouched. Every span of target-English
(vocabulary words, example sentences, dialogue lines, idioms) is wrapped in
``[[keep]]…[[/keep]]`` so it is NOT translated; the surrounding explanations,
definitions, and instructions stay translatable. There are no code labs —
only ``text`` lessons.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# technical-english-basics
# ──────────────────────────────────────────────────────────────────────

_TE_BASICS = SeedCourse(
    slug="technical-english-basics",
    title="Technical English for Engineers — Basics",
    description=(
        "Start speaking and writing engineering English with confidence: the "
        "core vocabulary of software and hardware work, describing what you "
        "build in the present simple, saying numbers and units out loud, "
        "reading code and documentation aloud, asking questions in meetings, "
        "and writing clear emails, chat messages, and pull-request comments."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Core engineering & software vocabulary",
            "9 min",
            r"""# Core engineering & software vocabulary

Every field has its own words. To work in English, you first need the nouns
engineers use every day. Learn the word, its meaning, and one example sentence
you can reuse.

| English term | What it means | Example sentence |
|---|---|---|
| [[keep]]a bug[[/keep]] | an error in the code | [[keep]]"There is a bug in the login page."[[/keep]] |
| [[keep]]a feature[[/keep]] | a capability the software offers | [[keep]]"This feature lets users export data."[[/keep]] |
| [[keep]]a deployment[[/keep]] | releasing code to a server | [[keep]]"The deployment finished without errors."[[/keep]] |
| [[keep]]the codebase[[/keep]] | all of a project's source code | [[keep]]"Our codebase is written in Python."[[/keep]] |
| [[keep]]a requirement[[/keep]] | something the system must do | [[keep]]"Security is a hard requirement."[[/keep]] |
| [[keep]]a server[[/keep]] | a computer that serves requests | [[keep]]"The server is down right now."[[/keep]] |

A few high-frequency verbs go with these nouns. You **build** software, you
**fix** a bug, you **deploy** code, you **run** a program, and you **test** a
feature:

- [[keep]]"I build the back end and she builds the front end."[[/keep]]
- [[keep]]"We need to fix this bug before the release."[[/keep]]
- [[keep]]"Can you run the tests again?"[[/keep]]

Notice the difference between **hardware** ([[keep]]hardware[[/keep]] — the
physical parts you can touch) and **software** ([[keep]]software[[/keep]] — the
programs that run on it). Both words are **uncountable** in English: you never
say "*a software*" or "*two softwares*". Instead say [[keep]]"a piece of
software"[[/keep]] or [[keep]]"some software"[[/keep]].

Learn five new terms a day and use each one in a sentence out loud. Vocabulary
grows by use, not by reading alone.
""",
        ),
        _t(
            "Describing what you build (present simple)",
            "9 min",
            r"""# Describing what you build (present simple)

When you describe your normal work — what your system does every day, what your
job is — you use the **present simple** tense. This is the most common tense in
technical English.

The form is easy. With **I / you / we / they**, use the base verb. With
**he / she / it** (and singular things like *the server*, *the function*), add
**-s**:

- [[keep]]"I write tests for the payment module."[[/keep]]
- [[keep]]"The server stores the user data."[[/keep]] (it → store**s**)
- [[keep]]"The function returns a list."[[/keep]] (it → return**s**)
- [[keep]]"Our team deploys every Friday."[[/keep]] (the team → deploy**s**)

Use the present simple for **facts and routines** — things that are generally
true:

- [[keep]]"The API accepts JSON and returns JSON."[[/keep]]
- [[keep]]"This service handles about one thousand requests per second."[[/keep]]
- [[keep]]"I usually review pull requests in the morning."[[/keep]]

To make a **negative**, use *do not / does not* (don't / doesn't) + base verb:

- [[keep]]"The cache does not store passwords."[[/keep]]
- [[keep]]"We don't support Internet Explorer."[[/keep]]

To ask a **question**, start with *do* or *does*:

- [[keep]]"Does the function handle empty input?"[[/keep]]
- [[keep]]"Do you write unit tests for every feature?"[[/keep]]

A useful pattern for describing a component is **subject + verb + object**:
[[keep]]"The parser reads the file and builds a tree."[[/keep]] Keep sentences
short. One idea per sentence is clearer than one long sentence with many ideas.
""",
        ),
        _t(
            "Numbers, units & measurements",
            "8 min",
            r"""# Numbers, units & measurements

Engineers say numbers out loud all day — in standups, on calls, in reviews. Say
them correctly and people trust your data.

**Decimals.** English uses a **point**, not a comma: `3.5` is read
[[keep]]"three point five"[[/keep]]. The digits after the point are read one by
one: `0.25` is [[keep]]"zero point two five"[[/keep]] (or
[[keep]]"point two five"[[/keep]]).

**Large numbers.** English groups with commas: `1,000` is
[[keep]]"one thousand"[[/keep]], `1,000,000` is [[keep]]"one million"[[/keep]],
and `1,500` is [[keep]]"one thousand five hundred"[[/keep]] or, informally,
[[keep]]"fifteen hundred"[[/keep]].

**Units and rates.** Read the unit in full, and read `/` as
[[keep]]"per"[[/keep]]:

| You see | You say |
|---|---|
| `512 MB` | [[keep]]"five hundred twelve megabytes"[[/keep]] |
| `2.4 GHz` | [[keep]]"two point four gigahertz"[[/keep]] |
| `200 ms` | [[keep]]"two hundred milliseconds"[[/keep]] |
| `50 req/s` | [[keep]]"fifty requests per second"[[/keep]] |
| `99.9 %` | [[keep]]"ninety-nine point nine percent"[[/keep]] |

**Versions.** Read each part separately, with [[keep]]"point"[[/keep]] between:
`v2.10.3` is [[keep]]"version two point ten point three"[[/keep]] — note it is
"ten", not "one zero".

**Symbols you read aloud:** `+` is [[keep]]"plus"[[/keep]], `-` is
[[keep]]"minus"[[/keep]], `=` is [[keep]]"equals"[[/keep]], `<` is
[[keep]]"less than"[[/keep]], `>` is [[keep]]"greater than"[[/keep]], and `*` is
[[keep]]"times"[[/keep]] (in math) or [[keep]]"star"[[/keep]] (as a symbol).

Practice by reading your own dashboards out loud:
[[keep]]"Latency is two hundred milliseconds at ninety-five percent."[[/keep]]
""",
        ),
        _t(
            "Reading code & documentation aloud",
            "10 min",
            r"""# Reading code & documentation aloud

To pair-program or explain a snippet on a call, you must read symbols and code
out loud in a way others understand. Every symbol has a standard spoken name.

| Symbol | Spoken name |
|---|---|
| `_` | [[keep]]"underscore"[[/keep]] |
| `-` | [[keep]]"dash"[[/keep]] or [[keep]]"hyphen"[[/keep]] |
| `.` | [[keep]]"dot"[[/keep]] |
| `/` | [[keep]]"slash"[[/keep]] |
| `\\` | [[keep]]"backslash"[[/keep]] |
| `()` | [[keep]]"parentheses"[[/keep]] (one is a [[keep]]"paren"[[/keep]]) |
| `[]` | [[keep]]"square brackets"[[/keep]] |
| `{}` | [[keep]]"curly braces"[[/keep]] |
| `:` | [[keep]]"colon"[[/keep]] |
| `;` | [[keep]]"semicolon"[[/keep]] |
| `@` | [[keep]]"at"[[/keep]] |
| `#` | [[keep]]"hash"[[/keep]] or [[keep]]"pound"[[/keep]] |
| `==` | [[keep]]"double equals"[[/keep]] or [[keep]]"equals equals"[[/keep]] |

Now read a line of code as a sentence. For `user_id = get_user(42)` you say:
[[keep]]"user underscore id equals get underscore user of forty-two"[[/keep]]
— or more naturally [[keep]]"set user id to get user of forty-two"[[/keep]].

For a file path like `src/app/main.py` say
[[keep]]"src slash app slash main dot py"[[/keep]].

When reading **documentation** aloud, use these helper phrases:

- [[keep]]"This function takes two arguments and returns a boolean."[[/keep]]
- [[keep]]"The first parameter is the file path."[[/keep]]
- [[keep]]"By default, the timeout is thirty seconds."[[/keep]]
- [[keep]]"See the example below."[[/keep]]

To talk about what code **does**, the present simple is your friend:
[[keep]]"This loop iterates over the list and prints each item."[[/keep]] Reading
slowly and naming each symbol is far clearer than rushing — your goal is to be
understood, not to be fast.
""",
        ),
        _t(
            "Asking questions & clarifying in meetings",
            "9 min",
            r"""# Asking questions & clarifying in meetings

In meetings you will not understand everything — that is normal, even for native
speakers. The skill is **asking for help politely** so the conversation keeps
moving. Memorize a few ready-made phrases.

**When you did not hear or understand:**

- [[keep]]"Sorry, could you repeat that?"[[/keep]]
- [[keep]]"Could you say that again, please?"[[/keep]]
- [[keep]]"I didn't catch the last part."[[/keep]]
- [[keep]]"Could you speak a little more slowly, please?"[[/keep]]

**When you want to confirm you understood correctly** — repeat it back in your
own words:

- [[keep]]"So, if I understand correctly, we deploy on Friday. Is that right?"[[/keep]]
- [[keep]]"Just to confirm, you want the API to return JSON?"[[/keep]]
- [[keep]]"Let me make sure I got that..."[[/keep]]

**When you want to ask a question:**

- [[keep]]"Can I ask a quick question?"[[/keep]]
- [[keep]]"What do you mean by 'rollback'?"[[/keep]]
- [[keep]]"Why do we need this change?"[[/keep]]
- [[keep]]"When is the deadline?"[[/keep]]

The **question words** are essential: [[keep]]what[[/keep]] (thing),
[[keep]]who[[/keep]] (person), [[keep]]where[[/keep]] (place),
[[keep]]when[[/keep]] (time), [[keep]]why[[/keep]] (reason),
[[keep]]how[[/keep]] (way/method), and [[keep]]how much / how many[[/keep]]
(quantity).

It is always better to ask than to stay silent and guess wrong. A simple
[[keep]]"Sorry, I didn't understand. Could you explain that again?"[[/keep]]
makes you look careful, not weak. Most people are happy to repeat themselves.
""",
        ),
        _t(
            "Email & chat / PR-comment basics",
            "10 min",
            r"""# Email & chat / PR-comment basics

Most engineering communication is written — email, chat, and pull-request
comments. Each has its own level of formality.

**Email** is the most formal. Use a greeting and a sign-off:

- Greeting: [[keep]]"Hi Maria,"[[/keep]] or, more formally,
  [[keep]]"Dear Mr. Silva,"[[/keep]]
- Sign-off: [[keep]]"Best regards,"[[/keep]] or [[keep]]"Thanks,"[[/keep]]
  then your name.

A clear request email is short and direct:

> [[keep]]"Hi Maria, could you review my pull request when you have a moment?
> It fixes the login bug. Thanks, Leo"[[/keep]]

**Chat** (Slack, Teams) is informal and fast. Short messages are fine, but stay
polite:

- [[keep]]"Hey, quick question — is staging down?"[[/keep]]
- [[keep]]"Sure, I'll take a look now."[[/keep]]
- [[keep]]"Sounds good, thanks!"[[/keep]]

**Pull-request (PR) comments** should be **specific and kind**. You are
commenting on the code, not the person. Some common, friendly phrases:

- [[keep]]"Nice work on this!"[[/keep]] (praise)
- [[keep]]"Could we rename this variable to make it clearer?"[[/keep]] (request)
- [[keep]]"Just a small thing: there's a typo here."[[/keep]] (minor note)
- [[keep]]"LGTM"[[/keep]] — this means [[keep]]"Looks good to me"[[/keep]], an
  approval.

A few common chat **abbreviations**: [[keep]]"FYI"[[/keep]] means
[[keep]]"for your information"[[/keep]]; [[keep]]"ASAP"[[/keep]] means
[[keep]]"as soon as possible"[[/keep]]; [[keep]]"WIP"[[/keep]] means
[[keep]]"work in progress"[[/keep]]; and [[keep]]"PTAL"[[/keep]] means
[[keep]]"please take a look"[[/keep]].

Whatever the channel, the rule is the same: be clear, be brief, and be kind.
Written words have no tone of voice, so add a [[keep]]"please"[[/keep]] and a
[[keep]]"thanks"[[/keep]] to keep messages warm.
""",
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# technical-english-intermediate
# ──────────────────────────────────────────────────────────────────────

_TE_INTERMEDIATE = SeedCourse(
    slug="technical-english-intermediate",
    title="Technical English for Engineers — Intermediate",
    description=(
        "Move from single sentences to real engineering conversations: "
        "describing processes and pipelines step by step, comparing options "
        "and trade-offs, giving polite code-review feedback, writing incident "
        "reports in the past tense, using conditionals to reason about bugs, "
        "and speaking up in standups and meetings."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Describing processes & pipelines (sequencing)",
            "10 min",
            r"""# Describing processes & pipelines (sequencing)

A pipeline is a sequence of steps. To explain one clearly, you need **sequencing
words** that put the steps in order.

| Stage | Sequencing words |
|---|---|
| start | [[keep]]"First,"[[/keep]] / [[keep]]"To begin,"[[/keep]] |
| middle | [[keep]]"Then,"[[/keep]] / [[keep]]"Next,"[[/keep]] / [[keep]]"After that,"[[/keep]] |
| end | [[keep]]"Finally,"[[/keep]] / [[keep]]"In the end,"[[/keep]] |

Put them together to describe a CI/CD pipeline:

> [[keep]]"First, the CI server checks out the code. Then it installs the
> dependencies. Next, it runs the tests. After that, it builds the image.
> Finally, it deploys to staging."[[/keep]]

Two more useful patterns. To say one step depends on another, use
[[keep]]"before"[[/keep]] and [[keep]]"after"[[/keep]]:

- [[keep]]"The tests run before the deployment."[[/keep]]
- [[keep]]"After the build passes, we deploy."[[/keep]]

To describe steps that happen automatically, the **passive voice** is common in
technical writing — *be* + past participle. We use it when *who* does the action
does not matter, only *what happens*:

- [[keep]]"The code is checked out."[[/keep]] (not "someone checks it out")
- [[keep]]"The image is built and pushed to the registry."[[/keep]]
- [[keep]]"Once the tests pass, the artifact is deployed."[[/keep]]

```mermaid
flowchart LR
    A["Checkout code"] --> B["Install deps"]
    B --> C["Run tests"]
    C --> D["Build image"]
    D --> E["Deploy to staging"]
```

When you present a diagram like this, narrate it with your sequencing words:
[[keep]]"First we check out the code, then we install the dependencies..."[[/keep]]
The diagram and your words together make the process easy to follow.
""",
        ),
        _t(
            "Comparing options & trade-offs",
            "9 min",
            r"""# Comparing options & trade-offs

Engineering is full of choices: which database, which framework, which approach.
To discuss them you need the language of **comparison**.

**Comparative adjectives** compare two things. Short adjectives add **-er**;
longer ones use **more**:

- [[keep]]"Redis is faster than Postgres for caching."[[/keep]] (fast → faster)
- [[keep]]"This approach is simpler but slower."[[/keep]] (simple → simpler)
- [[keep]]"A microservice is more flexible than a monolith."[[/keep]]
- [[keep]]"Option A is more expensive than Option B."[[/keep]]

**Superlatives** compare three or more, using **-est** or **most**:

- [[keep]]"This is the fastest option we tested."[[/keep]]
- [[keep]]"That's the most reliable solution."[[/keep]]

To weigh **pros and cons**, use these connectors:

- [[keep]]"On the one hand, it's fast; on the other hand, it uses more memory."[[/keep]]
- [[keep]]"The advantage is speed, but the drawback is complexity."[[/keep]]
- [[keep]]"It's reliable; however, it's harder to set up."[[/keep]]
- [[keep]]"It scales well, whereas the old system did not."[[/keep]]

The word **trade-off** ([[keep]]a trade-off[[/keep]]) is essential: it means you
gain one thing but lose another. [[keep]]"There's a trade-off between speed and
memory."[[/keep]]

To give your recommendation at the end:

- [[keep]]"Overall, I'd go with Option B because it's simpler to maintain."[[/keep]]
- [[keep]]"I'd recommend Postgres, since we already know it well."[[/keep]]

A balanced comparison names the options, lists pros and cons, names the
trade-off, and ends with a clear recommendation. That structure works in speech
and in a design document.
""",
        ),
        _t(
            "Code-review English (polite suggestions & requests)",
            "10 min",
            r"""# Code-review English (polite suggestions & requests)

Code review can feel harsh if the words are too direct. English softens requests
with **modal verbs** and **hedging phrases** so feedback sounds collaborative,
not commanding.

Compare a **direct** order with a **polite** request — both ask for the same
change:

| Too direct (avoid) | Polite (use this) |
|---|---|
| [[keep]]"Rename this variable."[[/keep]] | [[keep]]"Could we rename this variable?"[[/keep]] |
| [[keep]]"This is wrong."[[/keep]] | [[keep]]"I think there might be an issue here."[[/keep]] |
| [[keep]]"Add a test."[[/keep]] | [[keep]]"Would it make sense to add a test here?"[[/keep]] |
| [[keep]]"Don't do it this way."[[/keep]] | [[keep]]"What do you think about doing it this way instead?"[[/keep]] |

The magic words are the **modals** [[keep]]could[[/keep]],
[[keep]]would[[/keep]], and [[keep]]might[[/keep]], plus softeners like
[[keep]]"maybe"[[/keep]], [[keep]]"perhaps"[[/keep]], and
[[keep]]"I think"[[/keep]]. They turn a command into a suggestion.

It also helps to make suggestions **optional** when they are not blocking. Many
teams use prefixes:

- [[keep]]"Nit: missing a space here."[[/keep]] ([[keep]]nit[[/keep]] = a tiny,
  optional point)
- [[keep]]"Suggestion: we could extract this into a helper."[[/keep]]
- [[keep]]"Question: is this case handled anywhere?"[[/keep]]
- [[keep]]"Blocking: this will break in production."[[/keep]] (must be fixed)

Always pair criticism with **something positive** and ask, don't tell:

> [[keep]]"Nice solution overall! One small thing — could we add a check for
> empty input? Otherwise this looks great to me."[[/keep]]

And when you **receive** feedback, respond graciously:
[[keep]]"Good point, I'll fix that."[[/keep]] or
[[keep]]"Thanks for catching that!"[[/keep]] Polite review English keeps the
team friendly and the code improving.
""",
        ),
        _t(
            "Incident reports & postmortems (past tenses)",
            "10 min",
            r"""# Incident reports & postmortems (past tenses)

When something breaks, you write a report describing what **happened**. This
means the **past tense**. Two past tenses do most of the work.

The **past simple** describes a finished action at a known time — add **-ed** to
regular verbs (and learn the irregular ones):

- [[keep]]"The service crashed at 14:30."[[/keep]] (crash → crashed)
- [[keep]]"We deployed a fix and restarted the server."[[/keep]]
- [[keep]]"The database ran out of connections."[[/keep]] (run → ran, irregular)

The **past continuous** (*was/were* + verb-**ing**) describes what was happening
*around* that moment — often the background to the problem:

- [[keep]]"Traffic was increasing when the server went down."[[/keep]]
- [[keep]]"Users were reporting timeouts during the incident."[[/keep]]

A clear postmortem has a standard structure. Each section uses the past tense:

- **What happened:** [[keep]]"At 14:30, the API started returning 500 errors."[[/keep]]
- **Impact:** [[keep]]"Around 20% of users could not log in for 15 minutes."[[/keep]]
- **Root cause:** [[keep]]"A bad config change reduced the connection pool to
  zero."[[/keep]]
- **Resolution:** [[keep]]"We reverted the change and the service recovered."[[/keep]]
- **Action items:** [[keep]]"We will add an alert for low connection counts."[[/keep]]

Two useful irregular verbs appear constantly in reports:
[[keep]]"go → went"[[/keep]] ([[keep]]"the service went down"[[/keep]]) and
[[keep]]"begin → began"[[/keep]] ([[keep]]"the errors began at noon"[[/keep]]).

A good postmortem is **blameless**: it describes *what* failed, not *who* is
guilty. Write [[keep]]"the config change caused the outage"[[/keep]], not
"Maria broke it". The goal is to learn, not to blame.
""",
        ),
        _t(
            "Conditionals for debugging",
            "9 min",
            r"""# Conditionals for debugging

Debugging is reasoning about cause and effect: *if this, then that*. English
**conditionals** express exactly that, and engineers use them constantly.

The **zero conditional** states a general truth or a rule that is always true.
Form: *if* + present, ... present. Use it for how systems behave:

- [[keep]]"If the input is empty, the function returns null."[[/keep]]
- [[keep]]"If the cache is full, it evicts the oldest entry."[[/keep]]
- [[keep]]"The build fails if a test fails."[[/keep]]

The **first conditional** talks about a real, likely future situation. Form:
*if* + present, ... *will* + verb. Use it for plans and predictions:

- [[keep]]"If we add an index, the query will be faster."[[/keep]]
- [[keep]]"If the server restarts, we will lose the in-memory cache."[[/keep]]
- [[keep]]"If you pass a negative number, it will throw an error."[[/keep]]

The **second conditional** talks about a hypothetical or unlikely situation —
useful for "what if" debugging. Form: *if* + past, ... *would* + verb:

- [[keep]]"If the database were down, we would see connection errors."[[/keep]]
- [[keep]]"If I had more memory, the job wouldn't crash."[[/keep]]
- [[keep]]"What would happen if two requests arrived at the same time?"[[/keep]]

Notice the pattern for reasoning about a bug:

> [[keep]]"If the timeout were too short, we would see these errors. We do see
> them — so the timeout is probably too short."[[/keep]]

Two phrases help you talk through a theory out loud:
[[keep]]"It looks like..."[[/keep]] ([[keep]]"It looks like the cache is
stale."[[/keep]]) and [[keep]]"It might be..."[[/keep]] ([[keep]]"It might be a
race condition."[[/keep]]). Conditionals turn a guess into a clear, testable
statement.
""",
        ),
        _t(
            "Standups & meeting English",
            "9 min",
            r"""# Standups & meeting English

The daily standup is a short meeting where each person answers three questions.
Have a simple template ready so you can speak smoothly.

The three classic standup questions:

1. What did you do **yesterday**? (past tense)
2. What will you do **today**? (future)
3. Are you **blocked** by anything? ([[keep]]a blocker[[/keep]] = something
   stopping you)

A complete standup update sounds like this:

> [[keep]]"Yesterday I finished the login API and wrote the tests. Today I'll
> start on the password-reset flow. I'm blocked on the email service — I need
> the API key from the ops team."[[/keep]]

Note the tenses: [[keep]]"Yesterday I finished..."[[/keep]] (past),
[[keep]]"Today I'll..."[[/keep]] (future with *will / I'll*), and
[[keep]]"I'm blocked on..."[[/keep]] (present for your current state).

Useful phrases to **manage the meeting**:

- To take a turn: [[keep]]"I'll go next."[[/keep]] /
  [[keep]]"Can I jump in?"[[/keep]]
- To postpone a long topic: [[keep]]"Let's take this offline."[[/keep]] (discuss
  it later, not now)
- To agree: [[keep]]"Sounds good."[[/keep]] /
  [[keep]]"That works for me."[[/keep]]
- To disagree gently: [[keep]]"I'm not sure about that — can we discuss it?"[[/keep]]
- To finish: [[keep]]"That's all from me."[[/keep]] /
  [[keep]]"Nothing else from my side."[[/keep]]

If you are blocked, say so clearly and say **what you need**:
[[keep]]"I'm blocked. I need access to the staging database to continue."[[/keep]]
A standup is not a status report to impress people; it is a quick sync to find
and remove blockers. Be brief, be honest, and ask for help when you need it.
""",
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# technical-english-advanced
# ──────────────────────────────────────────────────────────────────────

_TE_ADVANCED = SeedCourse(
    slug="technical-english-advanced",
    title="Technical English for Engineers — Advanced",
    description=(
        "Communicate like a senior engineer in English: discuss architecture "
        "and design docs, present technical work and demos, disagree and "
        "negotiate decisions diplomatically, write precise specs and RFCs, "
        "use the tech idioms and phrasal verbs native speakers rely on, and "
        "handle system-design and behavioral interview questions in English."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Architecture & design-doc discussions",
            "10 min",
            r"""# Architecture & design-doc discussions

Discussing architecture means talking about the system at a high level: its
parts, how they connect, and why. You need precise nouns and the language of
structure.

Key vocabulary for describing a system:

| English term | What it means |
|---|---|
| [[keep]]a component[[/keep]] | a distinct part of the system |
| [[keep]]a layer[[/keep]] | a horizontal level (e.g. data, logic, UI) |
| [[keep]]a dependency[[/keep]] | something a component relies on |
| [[keep]]coupling[[/keep]] | how tightly two parts depend on each other |
| [[keep]]scalability[[/keep]] | the ability to handle more load |
| [[keep]]a bottleneck[[/keep]] | the slowest part that limits the whole |

To describe how parts **relate**, use these verbs:

- [[keep]]"The gateway routes requests to the right service."[[/keep]]
- [[keep]]"The auth service depends on the user database."[[/keep]]
- [[keep]]"These two components communicate over a message queue."[[/keep]]
- [[keep]]"This layer is decoupled from the database."[[/keep]]

To explain **design decisions**, the language of reasoning matters. State the
decision, then justify it:

- [[keep]]"We chose an event-driven design so that services stay loosely
  coupled."[[/keep]]
- [[keep]]"The reason we split this out is to scale it independently."[[/keep]]
- [[keep]]"We decided against a monolith because deployments would be too
  risky."[[/keep]]

A design doc usually opens with **context and goals**, then **options
considered**, then the **chosen approach** and its **trade-offs**. Useful
section-opener phrases:

- [[keep]]"The goal of this design is to..."[[/keep]]
- [[keep]]"We considered three options..."[[/keep]]
- [[keep]]"The main risk is..."[[/keep]]
- [[keep]]"For these reasons, we propose..."[[/keep]]

Speak about the system in the **present simple** ([[keep]]"the gateway
routes..."[[/keep]]) even when it is not built yet — in design docs this
"timeless present" describes how the system *will work* by describing how it
*works*.
""",
        ),
        _t(
            "Presenting technical work & demos",
            "10 min",
            r"""# Presenting technical work & demos

A good demo tells a small story: here is the problem, here is what I built, here
is it working. The English follows a clear arc with **signposting** phrases that
tell the audience where you are.

**Open** by setting context and an agenda:

- [[keep]]"Thanks for joining. Today I'll show you the new search feature."[[/keep]]
- [[keep]]"I'll start with the problem, then give a quick demo, and finish with
  next steps."[[/keep]]

**Signpost** as you move between sections so listeners can follow:

- [[keep]]"First, let me give you some context."[[/keep]]
- [[keep]]"Now let's move on to the demo."[[/keep]]
- [[keep]]"As you can see here, the results load instantly."[[/keep]]
- [[keep]]"Let me walk you through what happens."[[/keep]]
- [[keep]]"To sum up,"[[/keep]] / [[keep]]"To wrap up,"[[/keep]]

**Narrate a live demo** in the present simple, describing each action as you do
it:

> [[keep]]"So I type a query here, I hit enter, and you can see the results
> appear in under a second. If I filter by date, the list updates immediately."[[/keep]]

**Handle questions** with confidence — and it is fine not to know everything:

- [[keep]]"That's a great question."[[/keep]]
- [[keep]]"Good point — I'll look into that and get back to you."[[/keep]]
- [[keep]]"Let me come back to that at the end."[[/keep]]
- [[keep]]"I'm not sure, but my guess is..."[[/keep]]

**Close** with a clear summary and a call to action:

> [[keep]]"To sum up, the new search is faster and easier to use. Next, we'll run
> a beta with a few users. Any questions?"[[/keep]]

The secret to a calm demo is **signposting**: when the audience always knows
where you are, small language mistakes barely matter. Practice the opening and
closing lines until they are automatic.
""",
        ),
        _t(
            "Disagreeing & negotiating technical decisions",
            "10 min",
            r"""# Disagreeing & negotiating technical decisions

Senior engineers disagree all the time — politely. The goal is to push back on
the **idea** while respecting the **person**, and to reach a decision the team
can support.

**Disagree diplomatically.** Never start with a flat "no". Acknowledge first,
then offer your view:

- [[keep]]"I see your point, but I'm worried about the performance impact."[[/keep]]
- [[keep]]"That's a fair point. That said, I think there's a simpler option."[[/keep]]
- [[keep]]"I'm not sure I agree. Could you walk me through the reasoning?"[[/keep]]
- [[keep]]"I hear you, but have we considered the maintenance cost?"[[/keep]]

The pattern is **acknowledge + 'but/however' + your concern**. The word
[[keep]]"but"[[/keep]] (or the softer [[keep]]"that said"[[/keep]] /
[[keep]]"however"[[/keep]]) signals the turn.

**Ask questions instead of attacking.** A question invites discussion; a
statement invites defense:

- [[keep]]"What happens if the traffic doubles?"[[/keep]]
- [[keep]]"Have we thought about how this scales?"[[/keep]]
- [[keep]]"What's the trade-off here?"[[/keep]]

**Negotiate toward agreement.** Look for the shared goal and a middle path:

- [[keep]]"Can we find a middle ground?"[[/keep]]
- [[keep]]"What if we ship the simple version first and improve it later?"[[/keep]]
- [[keep]]"I'm OK with that as long as we add monitoring."[[/keep]]
- [[keep]]"Let's agree to revisit this in a month."[[/keep]]

**Disagree and commit** when a decision is made against your view. This is a
professional, respected stance:

> [[keep]]"I still prefer the other approach, but I'm happy to go with the
> team's decision and make it work."[[/keep]]

Strong opinions, loosely held: argue your case clearly, listen genuinely, and
once the group decides, support it fully. That combination earns trust.
""",
        ),
        _t(
            "Writing precise specs & RFCs",
            "10 min",
            r"""# Writing precise specs & RFCs

A specification (spec) or RFC ([[keep]]Request for Comments[[/keep]]) must be
**unambiguous**: every reader should understand the same thing. Precision in
English comes from a few specific words and habits.

**Requirement keywords** carry exact meaning (from RFC 2119) — use them
deliberately:

| Keyword | Meaning |
|---|---|
| [[keep]]MUST[[/keep]] | an absolute requirement |
| [[keep]]MUST NOT[[/keep]] | an absolute prohibition |
| [[keep]]SHOULD[[/keep]] | recommended, but exceptions are allowed |
| [[keep]]MAY[[/keep]] | optional, truly the author's choice |

Examples:

- [[keep]]"The API MUST reject requests without a valid token."[[/keep]]
- [[keep]]"Clients SHOULD retry on a 503 response."[[/keep]]
- [[keep]]"The response MAY include a cache header."[[/keep]]

**Avoid vague words.** Replace fuzzy terms with measurable ones:

| Vague (avoid) | Precise (use) |
|---|---|
| [[keep]]"fast"[[/keep]] | [[keep]]"under 200 ms at p99"[[/keep]] |
| [[keep]]"a lot of users"[[/keep]] | [[keep]]"up to 10,000 concurrent users"[[/keep]] |
| [[keep]]"soon"[[/keep]] | [[keep]]"within 24 hours"[[/keep]] |
| [[keep]]"it should be secure"[[/keep]] | [[keep]]"all traffic MUST use TLS 1.2 or higher"[[/keep]] |

**Define your terms** so words are not open to interpretation:
[[keep]]"In this document, 'request' means a single HTTP call to the public
API."[[/keep]]

A typical RFC structure: **Summary**, **Motivation** (why), **Detailed design**
(how, with MUST/SHOULD requirements), **Alternatives considered**, and **Open
questions**. Opener phrases:

- [[keep]]"This document proposes..."[[/keep]]
- [[keep]]"The motivation for this change is..."[[/keep]]
- [[keep]]"This is out of scope for this RFC."[[/keep]]

Write so that a reader cannot misunderstand you, not merely so they *can*
understand you. Precise English prevents expensive mistakes.
""",
        ),
        _t(
            'Tech idioms & phrasal verbs ("spin up", "roll back", "ship it")',
            "10 min",
            r"""# Tech idioms & phrasal verbs

Native engineers speak in **phrasal verbs** (verb + small word) and **idioms**.
These rarely translate literally, so learn them as whole units. Here are the
ones you will hear daily.

**Phrasal verbs** — the meaning changes with the little word:

| Phrasal verb | Meaning | Example |
|---|---|---|
| [[keep]]spin up[[/keep]] | start a new server/service | [[keep]]"Let's spin up a test server."[[/keep]] |
| [[keep]]roll back[[/keep]] | return to a previous version | [[keep]]"We had to roll back the release."[[/keep]] |
| [[keep]]roll out[[/keep]] | release gradually | [[keep]]"We'll roll out the feature to 10% first."[[/keep]] |
| [[keep]]break down[[/keep]] | split into smaller parts | [[keep]]"Let's break down the task."[[/keep]] |
| [[keep]]look into[[/keep]] | investigate | [[keep]]"I'll look into the bug."[[/keep]] |
| [[keep]]come up with[[/keep]] | invent / produce | [[keep]]"We came up with a workaround."[[/keep]] |
| [[keep]]figure out[[/keep]] | understand / solve | [[keep]]"I can't figure out why it fails."[[/keep]] |

**Common idioms** — fixed expressions with a non-literal meaning:

- [[keep]]"Ship it!"[[/keep]] — release it; it's ready to go.
- [[keep]]"It works on my machine."[[/keep]] — a joke about a bug only others
  can reproduce.
- [[keep]]"Let's not reinvent the wheel."[[/keep]] — don't rebuild what already
  exists.
- [[keep]]"That's a band-aid."[[/keep]] — a temporary, shallow fix.
- [[keep]]"It's technical debt."[[/keep]] — shortcuts now that cost effort
  later.
- [[keep]]"Let's circle back to that."[[/keep]] — return to this topic later.
- [[keep]]"This is a rabbit hole."[[/keep]] — a distraction that pulls you deep
  into details.
- [[keep]]"Let's get on the same page."[[/keep]] — make sure we all agree /
  understand the same thing.

A word of caution: phrasal verbs are **separable** sometimes —
[[keep]]"roll the release back"[[/keep]] and [[keep]]"roll back the
release"[[/keep]] are both correct, but [[keep]]"roll it back"[[/keep]] (pronoun
in the middle) is the only correct order with a pronoun. Learn each phrase by
hearing it in context, and soon they will sound natural.
""",
        ),
        _t(
            "Technical interview English (system design + behavioral)",
            "11 min",
            r"""# Technical interview English (system design + behavioral)

Interviews test communication as much as knowledge. Whether you are designing a
system out loud or answering "tell me about a time...", the right phrases let
you show your thinking clearly.

**System-design interviews** reward thinking aloud. Narrate your process:

- Clarify first: [[keep]]"Before I start, can I ask a few questions about the
  requirements?"[[/keep]]
- State assumptions: [[keep]]"Let's assume we have about one million users."[[/keep]]
- Think aloud: [[keep]]"My first thought is to use a load balancer in front of
  several servers."[[/keep]]
- Weigh options: [[keep]]"We could use SQL or NoSQL here. I'd lean toward SQL
  because the data is relational."[[/keep]]
- Acknowledge trade-offs: [[keep]]"This adds complexity, but it improves
  scalability."[[/keep]]

**Behavioral interviews** ask about past experience. Answer with the **STAR**
method — [[keep]]Situation, Task, Action, Result[[/keep]] — and use past
tenses:

> [[keep]]"In my last project (Situation), we had a slow API (Task). I profiled
> the code and added an index (Action), and the response time dropped by 70%
> (Result)."[[/keep]]

Common behavioral prompts and how to open your answer:

- [[keep]]"Tell me about a time you faced a difficult bug."[[/keep]] →
  [[keep]]"Sure. A while ago, we had a bug that..."[[/keep]]
- [[keep]]"How do you handle disagreement?"[[/keep]] →
  [[keep]]"I usually try to understand the other view first, and then..."[[/keep]]
- [[keep]]"What's a project you're proud of?"[[/keep]] →
  [[keep]]"One project I'm proud of is..."[[/keep]]

**Buy thinking time** politely instead of going silent:

- [[keep]]"That's a good question. Let me think for a moment."[[/keep]]
- [[keep]]"Just to make sure I understand the question..."[[/keep]]

And if you do not know something, be honest and show how you would find out:
[[keep]]"I'm not sure off the top of my head, but I would check the
documentation and test it."[[/keep]] Interviewers value clear, calm
communication and honest reasoning far more than a perfect accent.
""",
        ),
    ),
)


TECHNICAL_ENGLISH_COURSES = (_TE_BASICS, _TE_INTERMEDIATE, _TE_ADVANCED)
