"""Academy seed content — the English for Brazilians track (Beginner →
Advanced), tailored to the specific difficulties Brazilian Portuguese speakers
face when learning engineering & programming English.

* ``english-br-basics``        — false cognates ("falsos cognatos"), the sounds
  that don't exist in Portuguese (TH/H/final consonants), articles & plurals,
  word order, the third-person ``-s``, and survival English for engineers
* ``english-br-intermediate``  — the intermediate false-friend set, the tenses
  Brazilians mix up (present perfect/continuous), prepositions in/on/at, word
  stress & the three sounds of ``-ed``, writing without literal translation,
  and make/do · say/tell collocations
* ``english-br-advanced``      — idioms & natural phrasing (don't translate
  literally), fluency/fillers/hedging, minimal pairs (ship/sheep), conditionals
  & reported speech, meeting/interview English, and fixing the classic mistakes

This is a LANGUAGE course written for a Brazilian audience: the explanatory
prose is delivered in **Portuguese (pt-BR)** via auto-translation, but every
literal *language token* — the English being taught **and** the specific
Portuguese words named as false friends/examples — is wrapped in
``[[keep]]…[[/keep]]`` so it survives translation untouched. Diagrams use
``mermaid`` (also preserved by the translator). Only ``text`` lessons; there are
no code labs. It is translated to **pt-BR only** — a Brazil-specific course has
no audience in es/fr.
"""
# ruff: noqa: RUF001, RUF003 — IPA symbols (ɪ, iː) are intentional in a
# pronunciation course and must not be "corrected" to ASCII look-alikes.

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# english-br-basics
# ──────────────────────────────────────────────────────────────────────

_BR_BASICS = SeedCourse(
    slug="english-br-basics",
    title="English for Brazilians — Basics",
    description=(
        "English built for Brazilians, using engineering and programming "
        "examples. Start with the traps that catch Portuguese speakers first: "
        "false cognates ('falsos cognatos'), the sounds that don't exist in "
        "Portuguese, articles and plurals, English word order, the "
        "third-person -s we always forget, and the survival phrases you need "
        "on day one of a tech job."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Falsos cognatos: the words that trick Brazilians",
            "10 min",
            r"""# Falsos cognatos: the words that trick Brazilians

A **false cognate** ([[keep]]false friend[[/keep]], in Portuguese
[[keep]]falso cognato[[/keep]]) is an English word that looks like a Portuguese
word but means something different. These cause the most embarrassing mistakes
for Brazilians — so learn them first.

| English word | Looks like | But really means | Careful! |
|---|---|---|---|
| [[keep]]push[[/keep]] | [[keep]]puxar[[/keep]] | [[keep]]empurrar[[/keep]] | the opposite! [[keep]]pull[[/keep]] = [[keep]]puxar[[/keep]] |
| [[keep]]pretend[[/keep]] | [[keep]]pretender[[/keep]] | [[keep]]fingir[[/keep]] | "intend" = [[keep]]pretender[[/keep]] |
| [[keep]]actually[[/keep]] | [[keep]]atualmente[[/keep]] | [[keep]]na verdade[[/keep]] | "currently" = [[keep]]atualmente[[/keep]] |
| [[keep]]library[[/keep]] | [[keep]]livraria[[/keep]] | [[keep]]biblioteca[[/keep]] | "bookstore" = [[keep]]livraria[[/keep]] |
| [[keep]]push[[/keep]] | [[keep]]puxar[[/keep]] | [[keep]]empurrar[[/keep]] | also used in Git! |
| [[keep]]parents[[/keep]] | [[keep]]parentes[[/keep]] | [[keep]]pais[[/keep]] | "relatives" = [[keep]]parentes[[/keep]] |
| [[keep]]push[[/keep]] | — | — | — |

In programming this matters every day. A code [[keep]]library[[/keep]] is a
[[keep]]biblioteca[[/keep]] of reusable code — not a [[keep]]livraria[[/keep]].
And in Git you [[keep]]push[[/keep]] your code ([[keep]]empurrar[[/keep]] /
enviar), you don't [[keep]]puxar[[/keep]] it.

A few more that bite engineers:

- [[keep]]to realize[[/keep]] means [[keep]]perceber[[/keep]] / dar-se conta —
  **not** [[keep]]realizar[[/keep]] (which is "to carry out / to do").
- [[keep]]to push a commit[[/keep]] sends it to the remote; remember
  [[keep]]push[[/keep]] = [[keep]]empurrar[[/keep]].
- [[keep]]eventually[[/keep]] means [[keep]]por fim[[/keep]] / no final — **not**
  [[keep]]eventualmente[[/keep]] ("occasionally").

```mermaid
flowchart TD
    A["You see an English word<br/>that looks Portuguese"] --> B{"Falso cognato?"}
    B -->|"push, pretend,<br/>library, actually"| C["Stop — check the<br/>real meaning"]
    B -->|"normal word"| D["Trust the resemblance"]
    C --> E["Learn it as a pair:<br/>push = empurrar"]
```

The fix is simple: whenever an English word looks "too Portuguese", pause and
check. Learn each false friend as a **pair** — [[keep]]push = empurrar[[/keep]],
[[keep]]pretend = fingir[[/keep]] — and the trap disappears.
""",
        ),
        _t(
            "Sounds that don't exist in Portuguese (TH, H, final consonants)",
            "10 min",
            r"""# Sounds that don't exist in Portuguese (TH, H, final consonants)

Some English sounds simply do not exist in Portuguese, so Brazilians replace
them with the closest Portuguese sound. People still understand you — but
training these sounds makes you much clearer on calls.

**1. The [[keep]]TH[[/keep]] sound.** There is no [[keep]]th[[/keep]] in
Portuguese, so many say [[keep]]"free"[[/keep]] instead of [[keep]]"three"[[/keep]],
or [[keep]]"dis"[[/keep]] instead of [[keep]]"this"[[/keep]]. Put your tongue
lightly between your teeth and blow:

- [[keep]]think[[/keep]], [[keep]]three[[/keep]], [[keep]]thread[[/keep]] (a
  thread of execution!) — soft, voiceless.
- [[keep]]this[[/keep]], [[keep]]that[[/keep]], [[keep]]the[[/keep]] — with
  voice.

**2. The [[keep]]H[[/keep]] sound.** In Portuguese the letter [[keep]]h[[/keep]]
is silent ([[keep]]hora[[/keep]], [[keep]]hotel[[/keep]]). In English it is a
real puff of air. Don't drop it:

- [[keep]]host[[/keep]], [[keep]]hardware[[/keep]], [[keep]]hash[[/keep]],
  [[keep]]hosting[[/keep]] — breathe the [[keep]]h[[/keep]] out.

**3. Final consonants.** Portuguese words rarely end in a hard consonant, so
Brazilians add a vowel: [[keep]]"bug-ee"[[/keep]] for [[keep]]bug[[/keep]],
[[keep]]"GitHub-ee"[[/keep]] for [[keep]]GitHub[[/keep]]. Stop the word on the
consonant — no extra [[keep]]"i"[[/keep]] at the end.

**4. The [[keep]]-ING[[/keep]] ending** is [[keep]]"-ing"[[/keep]], not
[[keep]]"-in"[[/keep]] and not [[keep]]"-ingui"[[/keep]]:
[[keep]]running[[/keep]], [[keep]]testing[[/keep]], [[keep]]deploying[[/keep]].

**5. Initial [[keep]]S + consonant[[/keep]].** Portuguese adds an [[keep]]e[[/keep]]:
we say [[keep]]"estart"[[/keep]] for [[keep]]start[[/keep]] and
[[keep]]"estack"[[/keep]] for [[keep]]stack[[/keep]]. In English the word begins
directly on the [[keep]]s[[/keep]]: [[keep]]start[[/keep]], [[keep]]stack[[/keep]],
[[keep]]script[[/keep]], [[keep]]string[[/keep]].

```mermaid
flowchart LR
    A["A hard English word"] --> B{"What's the trap?"}
    B -->|"th"| C["tongue between teeth:<br/>three, this"]
    B -->|"silent h?"| D["breathe it: host, hash"]
    B -->|"ends in consonant"| E["no extra 'i':<br/>bug, not bug-ee"]
    B -->|"starts s+consonant"| F["no 'e' before:<br/>start, not e-start"]
```

You will not perfect these in a day, and a Brazilian accent is perfectly fine.
The goal is only to be **clearly understood** — pick one sound per week, say the
example words out loud, and it will slowly become automatic.
""",
        ),
        _t(
            "Articles, plurals & uncountables (a / an / the)",
            "9 min",
            r"""# Articles, plurals & uncountables (a / an / the)

Articles work differently in Portuguese, so Brazilians often drop them or use
the wrong one. English has three: [[keep]]a[[/keep]], [[keep]]an[[/keep]], and
[[keep]]the[[/keep]].

**[[keep]]a[[/keep]] / [[keep]]an[[/keep]]** mean "one, some" (like
[[keep]]um[[/keep]] / [[keep]]uma[[/keep]]). Use [[keep]]an[[/keep]] before a
**vowel sound**:

- [[keep]]a server[[/keep]], [[keep]]a function[[/keep]], [[keep]]a bug[[/keep]]
- [[keep]]an error[[/keep]], [[keep]]an API[[/keep]] (sounds like "ay-pee-eye"),
  [[keep]]an hour[[/keep]] (silent h → vowel sound!)

**[[keep]]the[[/keep]]** points to a *specific* thing (like [[keep]]o[[/keep]] /
[[keep]]a[[/keep]]): [[keep]]"the server crashed"[[/keep]] = a specific server we
both know.

Unlike Portuguese, English does **not** use [[keep]]the[[/keep]] for general
statements. Say [[keep]]"Programmers write code"[[/keep]] (general), **not**
"*The programmers write the code*" when you mean programmers in general.

**Uncountable nouns** are the biggest trap. Some English words have **no
plural** and take **no** [[keep]]a[[/keep]]. These are wrong for Brazilians very
often:

| Don't say | Say instead |
|---|---|
| [[keep]]an information[[/keep]] / [[keep]]informations[[/keep]] | [[keep]]some information[[/keep]] / [[keep]]a piece of information[[/keep]] |
| [[keep]]a feedback[[/keep]] / [[keep]]feedbacks[[/keep]] | [[keep]]some feedback[[/keep]] / [[keep]]a piece of feedback[[/keep]] |
| [[keep]]a software[[/keep]] / [[keep]]softwares[[/keep]] | [[keep]]a piece of software[[/keep]] / [[keep]]some software[[/keep]] |
| [[keep]]a hardware[[/keep]] / [[keep]]hardwares[[/keep]] | [[keep]]some hardware[[/keep]] |
| [[keep]]advices[[/keep]] | [[keep]]some advice[[/keep]] |

So in a stand-up you say [[keep]]"I have some feedback on your pull
request"[[/keep]] — never "*a feedback*". And [[keep]]"I need more
information"[[/keep]] — never "*more informations*".

A quick rule: if you can't count it with a number (you can't say "*two
informations*"), it is uncountable — use [[keep]]some[[/keep]],
[[keep]]much[[/keep]], or [[keep]]a piece of[[/keep]], and never add
[[keep]]-s[[/keep]].
""",
        ),
        _t(
            "Word order: adjectives before nouns, and S-V-O",
            "9 min",
            r"""# Word order: adjectives before nouns, and S-V-O

English word order is stricter than Portuguese, and two habits from Portuguese
cause most mistakes.

**1. Adjectives go BEFORE the noun.** In Portuguese we say
[[keep]]"código limpo"[[/keep]] (noun + adjective). In English the order is
reversed — adjective first:

- [[keep]]clean code[[/keep]] (not "*code clean*")
- [[keep]]a fast server[[/keep]] (not "*a server fast*")
- [[keep]]a critical bug[[/keep]], [[keep]]an open source library[[/keep]]

**2. The sentence order is Subject → Verb → Object (S-V-O).** English rarely
drops the subject, while Portuguese often does ([[keep]]"está funcionando"[[/keep]]
has no visible subject). In English you must include it:

- [[keep]]"It is working."[[/keep]] (not "*Is working*")
- [[keep]]"The test passed."[[/keep]] (subject + verb + …)
- [[keep]]"The parser reads the file."[[/keep]] (subject → verb → object)

```mermaid
flowchart LR
    S["Subject<br/>The function"] --> V["Verb<br/>returns"]
    V --> O["Object<br/>a list"]
    O --> R["The function returns a list."]
```

**3. Always keep the subject — even an empty 'it'.** English uses a "dummy"
[[keep]]it[[/keep]] or [[keep]]there[[/keep]] where Portuguese uses nothing:

- [[keep]]"It is raining."[[/keep]] / [[keep]]"It works."[[/keep]]
- [[keep]]"There is a bug in the code."[[/keep]] ([[keep]]há / existe[[/keep]] →
  [[keep]]there is[[/keep]] / [[keep]]there are[[/keep]])
- [[keep]]"There are three tests failing."[[/keep]]

**4. Questions invert or use do/does.** Portuguese asks with intonation only
([[keep]]"O servidor está no ar?"[[/keep]]). English needs a structure:

- [[keep]]"Is the server up?"[[/keep]] (be-verb moves to the front)
- [[keep]]"Does the build pass?"[[/keep]] (add do/does)

Read your sentences and check three things: is there a subject, is the verb
right after it, and are the adjectives in front of their nouns? Those three
checks fix most Brazilian word-order slips.
""",
        ),
        _t(
            "Present simple & the third-person -s we forget",
            "9 min",
            r"""# Present simple & the third-person -s we forget

The single most common Brazilian grammar mistake in English is **forgetting the
-s** on the verb with [[keep]]he[[/keep]], [[keep]]she[[/keep]], or
[[keep]]it[[/keep]]. Portuguese conjugates differently, so our ear doesn't miss
it — but English speakers notice immediately.

The **present simple** describes routines and facts. The form is the base verb,
but with [[keep]]he[[/keep]] / [[keep]]she[[/keep]] / [[keep]]it[[/keep]] (and
any single thing like *the server*, *the function*), you add [[keep]]-s[[/keep]]:

| Subject | Verb |
|---|---|
| [[keep]]I / you / we / they[[/keep]] | [[keep]]write, run, deploy[[/keep]] |
| [[keep]]he / she / it[[/keep]] | [[keep]]writes, runs, deploys[[/keep]] |

- [[keep]]"I write tests."[[/keep]] → [[keep]]"She writes tests."[[/keep]]
- [[keep]]"The server stores the data."[[/keep]] (it → store**s**)
- [[keep]]"The function returns a list."[[/keep]] (it → return**s**)

**Negatives and questions use do/does** — and here the [[keep]]-s[[/keep]] jumps
onto [[keep]]does[[/keep]], so the main verb goes back to its base form:

- [[keep]]"The cache does not store passwords."[[/keep]] (not "*does not
  stores*")
- [[keep]]"Does the function handle empty input?"[[/keep]] (not "*Does … handles*")

```mermaid
flowchart TD
    A["Subject?"] --> B{"he / she / it<br/>or one thing?"}
    B -->|"yes"| C["add -s:<br/>the server stores"]
    B -->|"no (I/you/we/they)"| D["base verb:<br/>we store"]
    C --> E{"negative or question?"}
    D --> E
    E -->|"yes"| F["use do/does +<br/>BASE verb:<br/>does it store?"]
    E -->|"no"| G["keep the -s where it is"]
```

There is no future-tense trap here, just one habit to build: every time the
subject is [[keep]]he[[/keep]], [[keep]]she[[/keep]], [[keep]]it[[/keep]], or a
single noun, your verb needs [[keep]]-s[[/keep]] — unless [[keep]]do[[/keep]] or
[[keep]]does[[/keep]] already took it. Say [[keep]]"it works, she runs, the build
passes"[[/keep]] out loud until the [[keep]]-s[[/keep]] feels natural.
""",
        ),
        _t(
            "Survival English for engineers (greetings, numbers, daily phrases)",
            "9 min",
            r"""# Survival English for engineers (greetings, numbers, daily phrases)

These are the ready-made phrases you need on your first day — the ones that keep
a conversation moving even when your grammar is not perfect yet.

**Greetings and small talk:**

- [[keep]]"Hi, how are you?"[[/keep]] → answer [[keep]]"I'm good, thanks. And
  you?"[[/keep]]
- [[keep]]"Nice to meet you."[[/keep]] (first time you meet someone)
- [[keep]]"Have a good weekend!"[[/keep]]

**Joining a call / stand-up:**

- [[keep]]"Can you hear me?"[[/keep]] / [[keep]]"You're on mute."[[/keep]]
- [[keep]]"Sorry, can you repeat that?"[[/keep]]
- [[keep]]"That's all from me."[[/keep]]

**Numbers** — English uses a **point** for decimals, not a comma. `3.5` is
[[keep]]"three point five"[[/keep]] (in Portuguese we'd write 3,5). Big numbers
group with commas: `1,000` = [[keep]]"one thousand"[[/keep]]. Read a rate's `/`
as [[keep]]"per"[[/keep]]: `50 req/s` = [[keep]]"fifty requests per second"[[/keep]].

**Watch the days and the date format.** Brazilians write [[keep]]day/month[[/keep]];
Americans write [[keep]]month/day[[/keep]]. So `03/04` is the 4th of March in the
US, not the 3rd of April. To avoid confusion, say the month by name:
[[keep]]"March fourth"[[/keep]] or [[keep]]"the fourth of March"[[/keep]].

**Polite magic words** soften everything — English feels rude without them:

- [[keep]]"Could you…?"[[/keep]] instead of [[keep]]"Can you…?"[[/keep]] for
  requests.
- [[keep]]"please"[[/keep]] and [[keep]]"thank you"[[/keep]] in almost every
  request.
- [[keep]]"I'm sorry, I don't understand."[[/keep]] is always OK to say.

**When you're stuck for a word**, don't freeze — describe it:
[[keep]]"It's the thing that… / It's like a… / How do you say…?"[[/keep]] A
native speaker will usually give you the word.

Keep a personal list of the phrases you use most and practice saying them out
loud. Fluency on day one is not the goal — being friendly, polite, and
understood is. The grammar gets better every week; the phrases get you through
today.
""",
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# english-br-intermediate
# ──────────────────────────────────────────────────────────────────────

_BR_INTERMEDIATE = SeedCourse(
    slug="english-br-intermediate",
    title="English for Brazilians — Intermediate",
    description=(
        "Go beyond survival English. Tackle the intermediate false friends, the "
        "tenses Brazilians mix up (present perfect and continuous), the "
        "in/on/at prepositions, word stress and the three sounds of -ed, how to "
        "write work messages without translating word-for-word, and the "
        "make/do and say/tell collocations that trip Portuguese speakers."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "More false friends (the intermediate set)",
            "10 min",
            r"""# More false friends (the intermediate set)

You know [[keep]]push[[/keep]] and [[keep]]library[[/keep]]. Here is the next
layer of false cognates — the ones that slip into *intermediate* speech and
quietly change your meaning.

| English word | Looks like | Really means | The trap |
|---|---|---|---|
| [[keep]]eventually[[/keep]] | [[keep]]eventualmente[[/keep]] | [[keep]]por fim / no final[[/keep]] | "occasionally" ≈ [[keep]]eventualmente[[/keep]] |
| [[keep]]to realize[[/keep]] | [[keep]]realizar[[/keep]] | [[keep]]perceber / dar-se conta[[/keep]] | "to carry out" = [[keep]]realizar[[/keep]] |
| [[keep]]to support[[/keep]] | [[keep]]suportar[[/keep]] | [[keep]]apoiar / dar suporte[[/keep]] | "to tolerate/bear" = [[keep]]suportar[[/keep]] |
| [[keep]]to attend[[/keep]] | [[keep]]atender[[/keep]] | [[keep]]comparecer / participar[[/keep]] | "to answer/help" = [[keep]]atender[[/keep]] |
| [[keep]]sensible[[/keep]] | [[keep]]sensível[[/keep]] | [[keep]]sensato / razoável[[/keep]] | "sensitive" = [[keep]]sensível[[/keep]] |
| [[keep]]comprehensive[[/keep]] | [[keep]]compreensivo[[/keep]] | [[keep]]completo / abrangente[[/keep]] | "understanding" = [[keep]]compreensivo[[/keep]] |
| [[keep]]to push[[/keep]] | [[keep]]puxar[[/keep]] | [[keep]]empurrar[[/keep]] | still the classic! |

Watch how these change a technical sentence:

- [[keep]]"The library eventually loads the cache."[[/keep]] means it loads
  [[keep]]por fim[[/keep]] / no final — **not** "occasionally".
- [[keep]]"We support Postgres."[[/keep]] means we [[keep]]damos suporte[[/keep]]
  to Postgres — not that we "tolerate" it.
- [[keep]]"I realized the test was wrong."[[/keep]] = [[keep]]percebi[[/keep]],
  not [[keep]]realizei[[/keep]].
- [[keep]]"a sensible default"[[/keep]] = [[keep]]um padrão sensato[[/keep]] — a
  reasonable default, not a "sensitive" one.

```mermaid
mindmap
  root(("Falsos<br/>cognatos"))
    eventually
      "por fim, NOT eventualmente"
    realize
      "perceber, NOT realizar"
    support
      "apoiar, NOT suportar"
    attend
      "comparecer, NOT atender"
    sensible
      "sensato, NOT sensível"
```

The pattern is always the same: the word that *sounds* Portuguese is the trap.
When you reach for a fancy Latin-looking word, pause and confirm it means what
you think. Keep a running list of the ones that catch you, and review it weekly.
""",
        ),
        _t(
            "Tenses Brazilians mix up (present perfect & continuous)",
            "11 min",
            r"""# Tenses Brazilians mix up (present perfect & continuous)

Two English tenses have **no exact match** in Portuguese, so Brazilians map them
to the wrong thing. Getting them right makes your English sound far more native.

**1. Present continuous vs present simple.** Portuguese uses the present for
both "now" and "in general". English splits them:

- **Now / temporary:** [[keep]]be[[/keep]] + verb-[[keep]]ing[[/keep]] →
  [[keep]]"The server is restarting right now."[[/keep]]
- **Routine / fact:** present simple → [[keep]]"The server restarts every
  night."[[/keep]]

So [[keep]]"I'm working on the login bug"[[/keep]] (right now / these days) is
different from [[keep]]"I work on the backend"[[/keep]] (my general job).

**2. The present perfect** — the big one. Form:
[[keep]]have / has[[/keep]] + past participle. It connects the **past to now**.
Portuguese usually translates it as a simple past, which is why we under-use it.

Use it for an action whose *result matters now*:

- [[keep]]"I have fixed the bug."[[/keep]] (it's fixed now — result matters)
  vs. [[keep]]"I fixed the bug yesterday."[[/keep]] (finished, specific past time)
- [[keep]]"The build has finished."[[/keep]] (so we can deploy now)
- [[keep]]"Have you deployed yet?"[[/keep]]

Use it for duration up to now — and here Brazilians make a famous mistake.
English uses [[keep]]for[[/keep]] + a length of time and [[keep]]since[[/keep]] +
a start point, with the **present perfect** — never the present:

- ✅ [[keep]]"I have worked here for three years."[[/keep]]
- ✅ [[keep]]"I have worked here since 2022."[[/keep]]
- ❌ [[keep]]"I work here since three years."[[/keep]] (direct from
  [[keep]]"trabalho aqui há três anos"[[/keep]] — wrong in English!)

```mermaid
timeline
    title Past → Now with the present perfect
    2022 : Started the job ("since 2022")
    ... : "have worked" (still true)
    Now : Still here ("for three years")
```

**3. [[keep]]for[[/keep]] vs [[keep]]since[[/keep]]:** [[keep]]for[[/keep]] + a
**duration** ([[keep]]for two hours[[/keep]], [[keep]]for a week[[/keep]]);
[[keep]]since[[/keep]] + a **point in time** ([[keep]]since Monday[[/keep]],
[[keep]]since 9 a.m.[[/keep]]).

When you want to say [[keep]]"faço isso há X tempo"[[/keep]], reach for
[[keep]]"I have done this for X"[[/keep]] — present perfect, not present. That
one switch removes the most common intermediate-level Brazilian error.
""",
        ),
        _t(
            "Prepositions of time & place (in / on / at)",
            "9 min",
            r"""# Prepositions of time & place (in / on / at)

Prepositions almost never map one-to-one between languages, so memorizing rules
beats translating. Three English prepositions — [[keep]]in[[/keep]],
[[keep]]on[[/keep]], [[keep]]at[[/keep]] — cause most of the trouble.

**For TIME**, think big → small:

| Preposition | Use for | Example |
|---|---|---|
| [[keep]]in[[/keep]] | months, years, long periods | [[keep]]in June[[/keep]], [[keep]]in 2026[[/keep]], [[keep]]in the morning[[/keep]] |
| [[keep]]on[[/keep]] | days and dates | [[keep]]on Monday[[/keep]], [[keep]]on June 24th[[/keep]] |
| [[keep]]at[[/keep]] | clock times, precise moments | [[keep]]at 3 p.m.[[/keep]], [[keep]]at night[[/keep]], [[keep]]at noon[[/keep]] |

- [[keep]]"The release is on Friday at 2 p.m."[[/keep]]
- [[keep]]"We launched in March."[[/keep]]

**For PLACE**, the same big → small idea:

| Preposition | Use for | Example |
|---|---|---|
| [[keep]]in[[/keep]] | enclosed / large areas | [[keep]]in the file[[/keep]], [[keep]]in Brazil[[/keep]], [[keep]]in the repo[[/keep]] |
| [[keep]]on[[/keep]] | surfaces / lines / platforms | [[keep]]on the server[[/keep]], [[keep]]on line 42[[/keep]], [[keep]]on GitHub[[/keep]] |
| [[keep]]at[[/keep]] | a specific point | [[keep]]at the office[[/keep]], [[keep]]at the endpoint[[/keep]] |

So you say [[keep]]"the bug is on line 42 in the parser"[[/keep]] and
[[keep]]"the code is on GitHub"[[/keep]] and [[keep]]"it runs on the
server"[[/keep]].

```mermaid
flowchart TD
    A["Talking about time?"] -->|"month / year"| B["in"]
    A -->|"day / date"| C["on"]
    A -->|"clock time"| D["at"]
    E["Talking about place?"] -->|"inside / area"| F["in"]
    E -->|"surface / line / platform"| G["on"]
    E -->|"a precise point"| H["at"]
```

A few must-memorize tech collocations that don't follow the rule neatly:
[[keep]]on a call[[/keep]], [[keep]]in a meeting[[/keep]], [[keep]]on the
team[[/keep]], [[keep]]at work[[/keep]], [[keep]]in production[[/keep]],
[[keep]]on staging[[/keep]]. Don't translate [[keep]]"em"[[/keep]] — it can become
[[keep]]in[[/keep]], [[keep]]on[[/keep]], or [[keep]]at[[/keep]]. Learn the
English pairs as fixed chunks and the guessing stops.
""",
        ),
        _t(
            "Pronunciation 2: word stress & the three sounds of -ed",
            "10 min",
            r"""# Pronunciation 2: word stress & the three sounds of -ed

Portuguese stresses words fairly evenly; English has one **strong** syllable and
reduces the rest. Put the stress in the wrong place and a clear word can become
hard to recognise.

**Word stress.** The capital letters show the stressed syllable:

- [[keep]]DE-ve-lop-er[[/keep]] (not de-ve-LO-per)
- [[keep]]PA-ra-me-ter[[/keep]], [[keep]]va-RI-a-ble[[/keep]]
- [[keep]]da-ta-BASE[[/keep]] or [[keep]]DA-ta-base[[/keep]] (both heard),
  [[keep]]CON-fig[[/keep]]
- [[keep]]de-PLOY[[/keep]] (verb) — the stress is on the second syllable.

Some words **change stress** depending on whether they are a noun or a verb:

- a [[keep]]RE-cord[[/keep]] (noun) vs to [[keep]]re-CORD[[/keep]] (verb)
- an [[keep]]IM-port[[/keep]] (noun) vs to [[keep]]im-PORT[[/keep]] (verb)

**The unstressed sound — the schwa.** Reduced syllables become a lazy
[[keep]]"uh"[[/keep]] sound. That's why [[keep]]"the"[[/keep]] often sounds like
[[keep]]"thuh"[[/keep]]. Don't force every vowel to be strong like in Portuguese.

**The three sounds of [[keep]]-ed[[/keep]].** The regular past ending is written
the same but pronounced **three** different ways — and it is almost never a full
[[keep]]"-ed"[[/keep]] syllable:

| Sound of -ed | When | Examples |
|---|---|---|
| [[keep]]/t/[[/keep]] | after voiceless sounds (p, k, s, sh, ch, f) | [[keep]]pushed[[/keep]], [[keep]]worked[[/keep]], [[keep]]fixed[[/keep]] (= "fixt") |
| [[keep]]/d/[[/keep]] | after voiced sounds | [[keep]]deployed[[/keep]], [[keep]]logged[[/keep]], [[keep]]called[[/keep]] |
| [[keep]]/ɪd/[[/keep]] | only after a [[keep]]t[[/keep]] or [[keep]]d[[/keep]] | [[keep]]started[[/keep]], [[keep]]tested[[/keep]], [[keep]]needed[[/keep]] |

```mermaid
flowchart TD
    A["A regular past verb (-ed)"] --> B{"Last sound before -ed?"}
    B -->|"t or d"| C["/ɪd/ — started, tested"]
    B -->|"voiceless: p,k,s,f..."| D["/t/ — pushed, fixed"]
    B -->|"voiced / vowel"| E["/d/ — deployed, logged"]
```

So [[keep]]"I fixed the bug"[[/keep]] sounds like [[keep]]"fixt"[[/keep]], and
[[keep]]"I tested it"[[/keep]] has the extra syllable [[keep]]"test-id"[[/keep]].
Only [[keep]]t[[/keep]]/[[keep]]d[[/keep]] verbs get the extra syllable — the rest
just add a quick [[keep]]/t/[[/keep]] or [[keep]]/d/[[/keep]]. Practising this
makes your past-tense sentences sound natural instead of robotic.
""",
        ),
        _t(
            "Writing work messages without translating literally",
            "10 min",
            r"""# Writing work messages without translating literally

The fastest way to sound foreign in writing is to translate a Portuguese
sentence word-for-word. English has its own ready-made phrases for work
messages. Learn the English chunk, don't build it from Portuguese.

**Don't translate the structure — use the English one:**

| Portuguese instinct | Word-for-word (wrong) | Natural English |
|---|---|---|
| [[keep]]"Segue em anexo…"[[/keep]] | [[keep]]"Follows attached…"[[/keep]] | [[keep]]"Please find attached…"[[/keep]] / [[keep]]"I've attached…"[[/keep]] |
| [[keep]]"Estou enviando…"[[/keep]] | [[keep]]"I am sending you…"[[/keep]] | [[keep]]"Here is…"[[/keep]] / [[keep]]"I'm sharing…"[[/keep]] |
| [[keep]]"Fico no aguardo"[[/keep]] | [[keep]]"I stay waiting"[[/keep]] | [[keep]]"Looking forward to your reply."[[/keep]] |
| [[keep]]"Qualquer dúvida…"[[/keep]] | [[keep]]"Any doubt…"[[/keep]] | [[keep]]"Let me know if you have any questions."[[/keep]] |
| [[keep]]"Desde já agradeço"[[/keep]] | [[keep]]"Since now I thank"[[/keep]] | [[keep]]"Thanks in advance."[[/keep]] |

Note [[keep]]"doubt"[[/keep]] ≠ [[keep]]"dúvida"[[/keep]]. A [[keep]]doubt[[/keep]]
is strong disbelief; a [[keep]]dúvida[[/keep]] you want clarified is a
[[keep]]question[[/keep]]. Say [[keep]]"I have a question"[[/keep]], not "*I have
a doubt*".

**A clean work email** is short and direct (English values brevity more than
Portuguese formality):

> [[keep]]"Hi Ana,
> I've attached the report. Let me know if you have any questions.
> Thanks,
> Leo"[[/keep]]

**Useful fixed phrases** to reuse verbatim:

- Asking: [[keep]]"Could you please review my PR?"[[/keep]]
- Updating: [[keep]]"Just a quick update:"[[/keep]] / [[keep]]"Heads up:"[[/keep]]
- Following up: [[keep]]"Just following up on this."[[/keep]] /
  [[keep]]"Gentle reminder:"[[/keep]]
- Closing: [[keep]]"Thanks!"[[/keep]] / [[keep]]"Best,"[[/keep]] /
  [[keep]]"Cheers,"[[/keep]] (informal)

Build a snippet file of these English chunks. When you write, **pick the English
phrase that fits**, instead of translating the Portuguese one you were about to
type. Your messages will instantly read as natural.
""",
        ),
        _t(
            "make vs do, say vs tell & common collocations",
            "9 min",
            r"""# make vs do, say vs tell & common collocations

Portuguese has one verb [[keep]]fazer[[/keep]] where English has **two** —
[[keep]]make[[/keep]] and [[keep]]do[[/keep]] — and one verb [[keep]]dizer/falar[[/keep]]
covering [[keep]]say[[/keep]] and [[keep]]tell[[/keep]]. Choosing wrong is a
classic Brazilian giveaway.

**[[keep]]make[[/keep]] vs [[keep]]do[[/keep]].** Rough rule:
[[keep]]make[[/keep]] = create/produce a result; [[keep]]do[[/keep]] = perform an
activity or task. But many are fixed pairs you must memorise:

| Use [[keep]]make[[/keep]] | Use [[keep]]do[[/keep]] |
|---|---|
| [[keep]]make a decision[[/keep]] | [[keep]]do your work[[/keep]] |
| [[keep]]make a change[[/keep]] | [[keep]]do a task[[/keep]] |
| [[keep]]make a mistake[[/keep]] | [[keep]]do research[[/keep]] |
| [[keep]]make progress[[/keep]] | [[keep]]do a code review[[/keep]] |
| [[keep]]make a release[[/keep]] | [[keep]]do the testing[[/keep]] |

A frequent error: [[keep]]"make a question"[[/keep]] is **wrong**. In English you
[[keep]]ask a question[[/keep]]. And you [[keep]]make a decision[[/keep]], you
don't "*take*" one (that's the Portuguese
[[keep]]"tomar uma decisão"[[/keep]]).

**[[keep]]say[[/keep]] vs [[keep]]tell[[/keep]].** Use [[keep]]tell[[/keep]] with
a **person** (tell someone); use [[keep]]say[[/keep]] without one:

- [[keep]]"He told me the build failed."[[/keep]] (tell + person)
- [[keep]]"He said the build failed."[[/keep]] (say, no person)
- ❌ [[keep]]"He said me…"[[/keep]] / ❌ [[keep]]"He told that…"[[/keep]]

Fixed expressions: [[keep]]tell the truth[[/keep]], [[keep]]tell a story[[/keep]],
[[keep]]tell the difference[[/keep]]; [[keep]]say yes/no[[/keep]],
[[keep]]say sorry[[/keep]].

```mermaid
flowchart TD
    A["fazer →"] --> B{"create a result?"}
    B -->|"yes"| C["make<br/>(a decision, a change)"]
    B -->|"perform a task?"| D["do<br/>(a task, research)"]
    E["dizer/falar →"] --> F{"is a person named?"}
    F -->|"yes"| G["tell<br/>(tell me, tell her)"]
    F -->|"no"| H["say<br/>(he said it works)"]
```

These don't follow logic you can derive from Portuguese — they are
**collocations**, fixed word partnerships. Learn the whole pair
([[keep]]make a decision[[/keep]], [[keep]]tell me[[/keep]]) as one unit, and
you'll stop translating [[keep]]fazer[[/keep]] and [[keep]]falar[[/keep]] on the
fly.
""",
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# english-br-advanced
# ──────────────────────────────────────────────────────────────────────

_BR_ADVANCED = SeedCourse(
    slug="english-br-advanced",
    title="English for Brazilians — Advanced",
    description=(
        "Polish your English to a professional, near-native level. Stop "
        "translating idioms literally, build real fluency with fillers and "
        "hedging, master the minimal pairs Brazilians confuse (ship/sheep), "
        "use conditionals and reported speech, handle meetings, presentations "
        "and interviews in English, and fix the persistent grammar mistakes "
        "that survive into advanced speech."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Don't translate literally: idioms & natural phrasing",
            "11 min",
            r"""# Don't translate literally: idioms & natural phrasing

At an advanced level, the remaining giveaway is **literal translation of
Portuguese expressions**. Idioms almost never survive a word-for-word move.
Learn the English equivalent as a whole.

**Portuguese expressions and their real English equivalents:**

| Portuguese | Literal (wrong) | Natural English |
|---|---|---|
| [[keep]]"pisar na bola"[[/keep]] | [[keep]]"step on the ball"[[/keep]] | [[keep]]"to drop the ball"[[/keep]] |
| [[keep]]"colocar a mão na massa"[[/keep]] | [[keep]]"put the hand in the dough"[[/keep]] | [[keep]]"to get your hands dirty"[[/keep]] / [[keep]]"to roll up your sleeves"[[/keep]] |
| [[keep]]"quebrar o galho"[[/keep]] | [[keep]]"break the branch"[[/keep]] | [[keep]]"a quick workaround"[[/keep]] |
| [[keep]]"viajar na maionese"[[/keep]] | [[keep]]"travel in the mayonnaise"[[/keep]] | [[keep]]"to overthink it"[[/keep]] / [[keep]]"to go off on a tangent"[[/keep]] |
| [[keep]]"deixa comigo"[[/keep]] | [[keep]]"leave with me"[[/keep]] | [[keep]]"I'll take care of it."[[/keep]] / [[keep]]"I've got this."[[/keep]] |

**Single words Brazilians translate too literally:**

- [[keep]]"travar"[[/keep]] (a program) → not "to lock"; say
  [[keep]]"it froze"[[/keep]] / [[keep]]"it hung"[[/keep]] /
  [[keep]]"it crashed"[[/keep]].
- [[keep]]"puxar"[[/keep]] a branch → not "to pull" socially; in Git it really
  is [[keep]]pull[[/keep]], but for files you [[keep]]fetch[[/keep]] or
  [[keep]]download[[/keep]].
- [[keep]]"cobrar"[[/keep]] someone → not "to charge"; say
  [[keep]]"to follow up with someone"[[/keep]] or
  [[keep]]"to chase someone for an update"[[/keep]].
- [[keep]]"aproveitar"[[/keep]] → not "to profit"; say
  [[keep]]"to take advantage of"[[/keep]] or [[keep]]"while we're at it"[[/keep]].

The native-sounding **tech idioms** to use instead:

- [[keep]]"Let's not reinvent the wheel."[[/keep]]
- [[keep]]"That's a band-aid / a quick fix."[[/keep]]
- [[keep]]"It's technical debt."[[/keep]]
- [[keep]]"Let's circle back to that."[[/keep]]
- [[keep]]"We're going down a rabbit hole."[[/keep]]

When an expression comes to mind in Portuguese, **don't translate it** — ask
yourself "what would a native say here?" If you don't know, say the plain meaning
instead ([[keep]]"I'll handle it"[[/keep]] rather than a broken idiom). Plain and
correct always beats clever and wrong.
""",
        ),
        _t(
            "Fluency: thinking in English, fillers & hedging",
            "10 min",
            r"""# Fluency: thinking in English, fillers & hedging

Fluency is not speed — it's not freezing. Advanced speakers use small phrases to
**buy time, stay polite, and keep talking** while they think. Brazilians often
go silent or translate in their head; these tools fix that.

**Fillers buy thinking time** (instead of silence or a Portuguese
[[keep]]"é…"[[/keep]]):

- [[keep]]"Well…"[[/keep]], [[keep]]"So…"[[/keep]], [[keep]]"Let me think…"[[/keep]]
- [[keep]]"That's a good question."[[/keep]]
- [[keep]]"How can I put this…"[[/keep]]

**Hedging softens claims** so you sound thoughtful, not arrogant — English
prefers indirectness:

- [[keep]]"I think…"[[/keep]], [[keep]]"It seems like…"[[/keep]],
  [[keep]]"It looks like…"[[/keep]]
- [[keep]]"I'm not 100% sure, but…"[[/keep]]
- [[keep]]"It might be a race condition."[[/keep]] (instead of "It is")
- [[keep]]"We probably want to cache this."[[/keep]]

Compare: [[keep]]"You are wrong."[[/keep]] (too blunt) vs
[[keep]]"I'm not sure that's quite right — could we double-check?"[[/keep]]
(professional). The hedged version is what gets you heard in meetings.

**Think in English, don't translate.** Two habits help:

1. **Describe around** a missing word instead of stopping:
   [[keep]]"It's the thing that schedules the jobs…"[[/keep]] →
   [[keep]]"the scheduler!"[[/keep]]
2. **Build from chunks** you already own
   ([[keep]]"Looking forward to…"[[/keep]], [[keep]]"It depends on…"[[/keep]])
   rather than assembling word-by-word from Portuguese.

```mermaid
flowchart LR
    A["Question arrives"] --> B["Filler:<br/>'That's a good question…'"]
    B --> C["Hedge:<br/>'It seems like…'"]
    C --> D["Answer in chunks<br/>you already know"]
    D --> E["Missing a word?<br/>describe around it"]
```

**Self-correct lightly and move on** — natives do too:
[[keep]]"He don't… sorry, he doesn't have access."[[/keep]] Don't apologise for
your English or stop the conversation. The goal of fluency is to keep the
conversation flowing; a small mistake mid-sentence matters far less than going
silent.
""",
        ),
        _t(
            "Minimal pairs & intonation (ship/sheep, live/leave)",
            "10 min",
            r"""# Minimal pairs & intonation (ship/sheep, live/leave)

A **minimal pair** is two words that differ by one sound. Portuguese doesn't
distinguish some of these sounds, so Brazilians merge them — and meaning gets
lost. Train your ears and mouth on the pairs that matter.

**Long vs short [[keep]]i[[/keep]]** — the most important pair for Brazilians.
English has a tense [[keep]]/iː/[[/keep]] and a lax [[keep]]/ɪ/[[/keep]];
Portuguese has only one:

| Short [[keep]]/ɪ/[[/keep]] | Long [[keep]]/iː/[[/keep]] |
|---|---|
| [[keep]]ship[[/keep]] | [[keep]]sheep[[/keep]] |
| [[keep]]live[[/keep]] (verb) | [[keep]]leave[[/keep]] |
| [[keep]]bit[[/keep]] | [[keep]]beat[[/keep]] |
| [[keep]]it[[/keep]] | [[keep]]eat[[/keep]] |
| [[keep]]bin[[/keep]] | [[keep]]bean[[/keep]] |

This is not academic: [[keep]]"Let's ship it"[[/keep]] (release it) vs
[[keep]]"Let's sheep it"[[/keep]] (nonsense), and [[keep]]"I live here"[[/keep]]
vs [[keep]]"I leave here"[[/keep]] are completely different messages.

**Other merged pairs:**

- [[keep]]/æ/[[/keep]] vs [[keep]]/ɛ/[[/keep]]: [[keep]]bad[[/keep]] /
  [[keep]]bed[[/keep]], [[keep]]man[[/keep]] / [[keep]]men[[/keep]]
- voiced final consonants: [[keep]]back[[/keep]] / [[keep]]bag[[/keep]],
  [[keep]]cap[[/keep]] / [[keep]]cab[[/keep]] (Brazilians often devoice the end)

**Intonation carries meaning** in English more than in Portuguese.

- **Rising** at the end = a yes/no question:
  [[keep]]"The build passed?"[[/keep]] ↗
- **Falling** = a statement or a wh-question:
  [[keep]]"The build passed."[[/keep]] ↘ / [[keep]]"When did it pass?"[[/keep]] ↘
- **Stressing a different word changes the meaning:**
  [[keep]]"*I* didn't break it"[[/keep]] (someone else did) vs
  [[keep]]"I didn't break *it*"[[/keep]] (I broke something else).

```mermaid
flowchart TD
    A["End of sentence"] --> B{"Yes/no question?"}
    B -->|"yes"| C["rising tone ↗<br/>'It works?'"]
    B -->|"statement / wh-question"| D["falling tone ↘<br/>'It works.'"]
```

Practise minimal pairs out loud in twos ([[keep]]"ship — sheep, live —
leave"[[/keep]]) and exaggerate the difference at first. Once your mouth can make
both sounds on purpose, your everyday speech becomes much easier to understand.
""",
        ),
        _t(
            "Conditionals & reported speech",
            "10 min",
            r"""# Conditionals & reported speech

Two advanced structures let you reason precisely and relay what others said —
both have Portuguese equivalents that don't line up perfectly.

**Conditionals** — "if this, then that". The level of *reality* changes the
tense:

- **Zero** (always true): [[keep]]if[[/keep]] + present, present →
  [[keep]]"If the input is empty, the function returns null."[[/keep]]
- **First** (real future): [[keep]]if[[/keep]] + present, [[keep]]will[[/keep]] →
  [[keep]]"If we add an index, the query will be faster."[[/keep]]
- **Second** (hypothetical): [[keep]]if[[/keep]] + past, [[keep]]would[[/keep]] →
  [[keep]]"If the DB were down, we would see timeouts."[[/keep]]
- **Third** (past regret): [[keep]]if[[/keep]] + past perfect,
  [[keep]]would have[[/keep]] → [[keep]]"If we had tested it, we wouldn't have
  shipped the bug."[[/keep]]

A frequent Brazilian slip: using [[keep]]will[[/keep]] **inside** the if-clause.
English doesn't — say [[keep]]"If it fails, I will retry."[[/keep]], never
"*If it will fail*…".

**Reported (indirect) speech** — relaying what someone said. The tense usually
shifts **one step back** into the past:

| Direct | Reported |
|---|---|
| [[keep]]"The build is green."[[/keep]] | [[keep]]"He said the build was green."[[/keep]] |
| [[keep]]"I fixed it."[[/keep]] | [[keep]]"She said she had fixed it."[[/keep]] |
| [[keep]]"We will deploy."[[/keep]] | [[keep]]"They said they would deploy."[[/keep]] |

Remember [[keep]]tell[[/keep]] needs a person, [[keep]]say[[/keep]] doesn't (from
the intermediate lesson): [[keep]]"She told me the build was green."[[/keep]]

**Reported questions** drop the question word-order and use no question mark:

- Direct: [[keep]]"Is the server up?"[[/keep]] →
  Reported: [[keep]]"He asked if the server was up."[[/keep]] (not "*asked is the
  server up*")
- Direct: [[keep]]"When did it fail?"[[/keep]] →
  Reported: [[keep]]"She asked when it had failed."[[/keep]]

```mermaid
flowchart LR
    A["Direct speech<br/>'I fixed it.'"] --> B["shift tense back"]
    B --> C["Reported<br/>'She said she had fixed it.'"]
```

These structures appear constantly in stand-ups ("he said the API was down") and
postmortems ("if we had alerted earlier…"). Drill the tense-shift until it's
automatic, and your retellings will sound precise and native.
""",
        ),
        _t(
            "Meetings, presentations & interviews in English",
            "11 min",
            r"""# Meetings, presentations & interviews in English

This lesson gathers the high-stakes situations into one toolkit, with notes on
the cultural differences Brazilians notice most.

**Meetings.** English-speaking work culture is direct and turn-based. Useful
moves:

- Take a turn: [[keep]]"Can I jump in here?"[[/keep]] /
  [[keep]]"I'd like to add something."[[/keep]]
- Disagree politely: [[keep]]"I see your point, but…"[[/keep]] /
  [[keep]]"That's fair, however…"[[/keep]]
- Park a topic: [[keep]]"Let's take this offline."[[/keep]]
- Check understanding: [[keep]]"Just to confirm, we deploy on Friday?"[[/keep]]

A cultural note: in many English-speaking teams, **silence is read as
agreement**. If you disagree, you usually need to say so — politely, but
clearly.

**Presentations & demos.** Signpost so the audience can follow:

- Open: [[keep]]"Today I'll walk you through the new search feature."[[/keep]]
- Move on: [[keep]]"Now let's look at the demo."[[/keep]] /
  [[keep]]"Moving on to…"[[/keep]]
- Point: [[keep]]"As you can see here…"[[/keep]]
- Close: [[keep]]"To sum up,"[[/keep]] / [[keep]]"To wrap up,"[[/keep]]

Narrate a live demo in the **present simple**: [[keep]]"I type the query, I hit
enter, and the results appear instantly."[[/keep]]

**Interviews.** Two formats:

- **Technical / system design** — think aloud:
  [[keep]]"Before I start, can I ask a few questions about the
  requirements?"[[/keep]] then [[keep]]"My first thought is to put a load
  balancer in front of several servers."[[/keep]]
- **Behavioral** — use **STAR**:
  [[keep]]Situation, Task, Action, Result[[/keep]]:
  > [[keep]]"In my last project, we had a slow API (situation/task). I profiled
  > it and added an index (action), and latency dropped by 70% (result)."[[/keep]]

Buy time gracefully: [[keep]]"That's a great question — let me think for a
moment."[[/keep]] And it's fine not to know: [[keep]]"I'm not sure off the top of
my head, but I'd check the docs and test it."[[/keep]]

```mermaid
flowchart LR
    A["Behavioral question"] --> S["Situation"]
    S --> T["Task"]
    T --> Ac["Action"]
    Ac --> R["Result"]
```

A final cultural tip: English speakers value **concise, confident, honest**
answers. Don't over-apologise for your English and don't undersell yourself —
[[keep]]"I led the migration"[[/keep]] is a fact, not bragging. Prepare your key
phrases in advance, and these situations stop being scary.
""",
        ),
        _t(
            "Fixing the classic mistakes (people is, I have 30 years)",
            "10 min",
            r"""# Fixing the classic mistakes (people is, I have 30 years)

These specific errors survive all the way into advanced Brazilian English
because they come straight from Portuguese grammar. Fix these and you remove the
last obvious tells.

**1. [[keep]]people[[/keep]] is plural.** It takes a plural verb:

- ✅ [[keep]]"People are waiting."[[/keep]] / [[keep]]"Many people use this
  API."[[/keep]]
- ❌ [[keep]]"People is waiting."[[/keep]] (from [[keep]]"as pessoas"[[/keep]]
  thinking)

**2. Age uses [[keep]]be[[/keep]], not [[keep]]have[[/keep]].** Portuguese
[[keep]]"ter X anos"[[/keep]] becomes English [[keep]]be X years old[[/keep]]:

- ✅ [[keep]]"I am 30 years old."[[/keep]] / [[keep]]"The project is two years
  old."[[/keep]]
- ❌ [[keep]]"I have 30 years."[[/keep]]

**3. [[keep]]ask a question[[/keep]], never "make a question".**

- ✅ [[keep]]"Can I ask a question?"[[/keep]]
- ❌ [[keep]]"Can I make a question?"[[/keep]]

**4. Duration: present perfect + [[keep]]for[[/keep]]/[[keep]]since[[/keep]], not
the present + "since".**

- ✅ [[keep]]"I have worked here for three years."[[/keep]]
- ❌ [[keep]]"I work here since three years."[[/keep]]
  (from [[keep]]"trabalho aqui há três anos"[[/keep]])

**5. No double negatives.** Portuguese allows [[keep]]"não vi nada"[[/keep]];
English uses **one** negative:

- ✅ [[keep]]"I didn't see anything."[[/keep]] / [[keep]]"I saw nothing."[[/keep]]
- ❌ [[keep]]"I didn't see nothing."[[/keep]]

**6. [[keep]]explain[[/keep]] / [[keep]]say[[/keep]] don't take a person
directly.** Use [[keep]]to[[/keep]]:

- ✅ [[keep]]"Can you explain this to me?"[[/keep]]
- ❌ [[keep]]"Can you explain me this?"[[/keep]]

**7. [[keep]]-s[[/keep]] on the third person** (the basics lesson, still the most
common): [[keep]]"it works"[[/keep]], [[keep]]"she runs"[[/keep]],
[[keep]]"the build passes"[[/keep]].

| Don't say | Say |
|---|---|
| [[keep]]"People is ready."[[/keep]] | [[keep]]"People are ready."[[/keep]] |
| [[keep]]"I have 30 years."[[/keep]] | [[keep]]"I'm 30 years old."[[/keep]] |
| [[keep]]"Make a question"[[/keep]] | [[keep]]"Ask a question"[[/keep]] |
| [[keep]]"Explain me this"[[/keep]] | [[keep]]"Explain this to me"[[/keep]] |
| [[keep]]"I work here since 2022"[[/keep]] | [[keep]]"I've worked here since 2022"[[/keep]] |

Keep this table somewhere visible. Each of these is a single, fixable habit —
catch yourself a few times and the correct form takes over. Clearing this list
is what moves your English from "clearly a Brazilian" to "fluent professional".
""",
        ),
    ),
)


ENGLISH_BRAZIL_COURSES = (_BR_BASICS, _BR_INTERMEDIATE, _BR_ADVANCED)
