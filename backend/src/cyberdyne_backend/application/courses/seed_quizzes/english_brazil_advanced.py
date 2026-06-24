"""Curated quiz questions for the English for Brazilians — Advanced course.
Keys are the EXACT content-lesson titles; the seed interleaves a checkpoint quiz
after each content lesson plus a final comprehensive quiz.

Language course for a Brazilian audience: target-English (and the named
Portuguese expressions) in the OPTIONS are wrapped in ``[[keep]]…[[/keep]]`` so
they survive auto-translation; prompts/explanations stay translatable (pt-BR)."""
# ruff: noqa: RUF001, RUF003 — IPA symbols (ɪ, iː) are intentional pronunciation content.

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Don't translate literally: idioms & natural phrasing": (
            q(
                'What is the natural English for "colocar a mão na massa"?',
                (
                    opt("[[keep]]to put the hand in the dough[[/keep]]"),
                    opt(
                        "[[keep]]to roll up your sleeves / get your hands dirty[[/keep]]",
                        correct=True,
                    ),
                    opt("[[keep]]to put hands in the mass[[/keep]]"),
                    opt("[[keep]]to make the dough[[/keep]]"),
                ),
                "Idioms don't translate literally; the English equivalent is 'roll up your sleeves'.",
            ),
            q(
                'When a program "travou", a natural English sentence is:',
                (
                    opt("[[keep]]It locked.[[/keep]]"),
                    opt("[[keep]]It froze / it hung / it crashed.[[/keep]]", correct=True),
                    opt("[[keep]]It blocked itself.[[/keep]]"),
                    opt("[[keep]]It trapped.[[/keep]]"),
                ),
                "'travar' is not 'to lock'; say 'it froze', 'it hung', or 'it crashed'.",
            ),
            q(
                'To say you "cobrou alguém por uma resposta", you say:',
                (
                    opt("[[keep]]I charged him for an answer.[[/keep]]"),
                    opt("[[keep]]I followed up with him for an update.[[/keep]]", correct=True),
                    opt("[[keep]]I collected him.[[/keep]]"),
                    opt("[[keep]]I billed him an answer.[[/keep]]"),
                ),
                "'cobrar' someone is 'to follow up / chase for an update', not 'to charge'.",
            ),
        ),
        "Fluency: thinking in English, fillers & hedging": (
            q(
                "Which is a hedged, professional way to disagree?",
                (
                    opt("[[keep]]You are wrong.[[/keep]]"),
                    opt(
                        "[[keep]]I'm not sure that's quite right — could we double-check?[[/keep]]",
                        correct=True,
                    ),
                    opt("[[keep]]That is incorrect, obviously.[[/keep]]"),
                    opt("[[keep]]No.[[/keep]]"),
                ),
                "English prefers indirectness; hedging keeps the disagreement collaborative.",
            ),
            q(
                "Your goal when you can't remember a word mid-sentence is to:",
                (
                    opt("stop and apologize for your English"),
                    opt("describe around it ('the thing that schedules jobs…')", correct=True),
                    opt("switch entirely to Portuguese"),
                    opt("stay silent until it comes back"),
                ),
                "Fluency means keeping the conversation flowing — describe around a missing word.",
            ),
            q(
                "Which is a useful filler to buy thinking time?",
                (
                    opt("[[keep]]That's a good question.[[/keep]]", correct=True),
                    opt("[[keep]]Wait, I translate.[[/keep]]"),
                    opt("[[keep]]I don't know nothing.[[/keep]]"),
                    opt("(silence)"),
                ),
                "Fillers like 'That's a good question' buy time instead of an awkward silence.",
            ),
        ),
        "Minimal pairs & intonation (ship/sheep, live/leave)": (
            q(
                'In "Let\'s ship it", the word "ship" has which vowel?',
                (
                    opt("the short [[keep]]/ɪ/[[/keep]] (ship)", correct=True),
                    opt("the long [[keep]]/iː/[[/keep]] (sheep)"),
                    opt("the same as in [[keep]]eat[[/keep]]"),
                    opt("the same as in [[keep]]bean[[/keep]]"),
                ),
                "'ship' (release it) uses the short /ɪ/; 'sheep' uses the long /iː/.",
            ),
            q(
                "Which pair are different words a Brazilian might merge?",
                (
                    opt("[[keep]]live[[/keep]] and [[keep]]leave[[/keep]]", correct=True),
                    opt("[[keep]]code[[/keep]] and [[keep]]code[[/keep]]"),
                    opt("[[keep]]push[[/keep]] and [[keep]]push[[/keep]]"),
                    opt("[[keep]]run[[/keep]] and [[keep]]ran[[/keep]]"),
                ),
                "'live' /ɪ/ vs 'leave' /iː/ is a classic minimal pair Brazilians merge.",
            ),
            q(
                "A rising tone at the end of a sentence usually signals:",
                (
                    opt("a yes/no question", correct=True),
                    opt("a finished statement"),
                    opt("a wh-question"),
                    opt("an order"),
                ),
                "Rising intonation ↗ marks a yes/no question: 'The build passed?'",
            ),
        ),
        "Conditionals & reported speech": (
            q(
                "Which sentence is correct?",
                (
                    opt("[[keep]]If it fails, I will retry.[[/keep]]", correct=True),
                    opt("[[keep]]If it will fail, I will retry.[[/keep]]"),
                    opt("[[keep]]If it will fail, I retry.[[/keep]]"),
                    opt("[[keep]]If it fail, I will retry.[[/keep]]"),
                ),
                "Don't use 'will' inside the if-clause: 'If it fails, I will retry.'",
            ),
            q(
                'Report this: "I fixed it" (she said).',
                (
                    opt("[[keep]]She said she had fixed it.[[/keep]]", correct=True),
                    opt("[[keep]]She said she fix it.[[/keep]]"),
                    opt("[[keep]]She told she had fixed it.[[/keep]]"),
                    opt("[[keep]]She said me she fixed it.[[/keep]]"),
                ),
                "Reported speech shifts the tense back: 'She said she had fixed it.'",
            ),
            q(
                'Report this question: "Is the server up?" (he asked).',
                (
                    opt("[[keep]]He asked if the server was up.[[/keep]]", correct=True),
                    opt("[[keep]]He asked is the server up.[[/keep]]"),
                    opt("[[keep]]He asked if was the server up?[[/keep]]"),
                    opt("[[keep]]He asked the server is up.[[/keep]]"),
                ),
                "Reported questions use statement order and no question mark: 'asked if the server was up'.",
            ),
        ),
        "Meetings, presentations & interviews in English": (
            q(
                "What does STAR stand for in a behavioral interview?",
                (
                    opt("[[keep]]Situation, Task, Action, Result[[/keep]]", correct=True),
                    opt("[[keep]]Story, Topic, Answer, Review[[/keep]]"),
                    opt("[[keep]]Start, Test, Apply, Report[[/keep]]"),
                    opt("[[keep]]System, Tools, Architecture, Run[[/keep]]"),
                ),
                "STAR = Situation, Task, Action, Result — a structure for behavioral answers.",
            ),
            q(
                "In many English-speaking teams, staying silent in a meeting is read as:",
                (
                    opt("disagreement"),
                    opt("agreement", correct=True),
                    opt("confusion"),
                    opt("respect"),
                ),
                "Silence is often read as agreement; if you disagree, say so politely but clearly.",
            ),
            q(
                "Which phrase politely takes a turn to speak?",
                (
                    opt("[[keep]]Can I jump in here?[[/keep]]", correct=True),
                    opt("[[keep]]Stop, my turn.[[/keep]]"),
                    opt("[[keep]]Listen to me now.[[/keep]]"),
                    opt("[[keep]]I will talk.[[/keep]]"),
                ),
                "'Can I jump in here?' is a polite way to take a turn.",
            ),
        ),
        "Fixing the classic mistakes (people is, I have 30 years)": (
            q(
                "How do you say your age in English?",
                (
                    opt("[[keep]]I have 30 years.[[/keep]]"),
                    opt("[[keep]]I am 30 years old.[[/keep]]", correct=True),
                    opt("[[keep]]I have 30 years old.[[/keep]]"),
                    opt("[[keep]]I am 30 years.[[/keep]]"),
                ),
                "English uses 'be ... years old': 'I am 30 years old' (not 'have').",
            ),
            q(
                "Which sentence is correct?",
                (
                    opt("[[keep]]I didn't see anything.[[/keep]]", correct=True),
                    opt("[[keep]]I didn't see nothing.[[/keep]]"),
                    opt("[[keep]]I not saw nothing.[[/keep]]"),
                    opt("[[keep]]I didn't saw anything.[[/keep]]"),
                ),
                "English uses a single negative: 'I didn't see anything.'",
            ),
            q(
                "Which sentence is correct?",
                (
                    opt("[[keep]]Can you explain this to me?[[/keep]]", correct=True),
                    opt("[[keep]]Can you explain me this?[[/keep]]"),
                    opt("[[keep]]Can you me explain this?[[/keep]]"),
                    opt("[[keep]]Can you explain to me this?[[/keep]] (best order)"),
                ),
                "'explain' takes 'to + person': 'explain this to me' (not 'explain me this').",
            ),
        ),
    },
    final=(
        q(
            "Which sentence is correct?",
            (
                opt("[[keep]]People are ready to deploy.[[/keep]]", correct=True),
                opt("[[keep]]People is ready to deploy.[[/keep]]"),
                opt("[[keep]]The people is ready to deploy.[[/keep]]"),
                opt("[[keep]]People ready is to deploy.[[/keep]]"),
            ),
            "'people' is plural: 'People are ready.'",
        ),
        q(
            'The natural English for "deixa comigo" is:',
            (
                opt("[[keep]]Leave with me.[[/keep]]"),
                opt("[[keep]]I'll take care of it. / I've got this.[[/keep]]", correct=True),
                opt("[[keep]]Let with me.[[/keep]]"),
                opt("[[keep]]Stay with me.[[/keep]]"),
            ),
            "Don't translate literally; say 'I'll take care of it' or 'I've got this'.",
        ),
        q(
            "Which is correct?",
            (
                opt(
                    "[[keep]]If we had tested it, we wouldn't have shipped the bug.[[/keep]]",
                    correct=True,
                ),
                opt("[[keep]]If we would test it, we wouldn't ship the bug.[[/keep]]"),
                opt("[[keep]]If we tested it, we wouldn't have shipped the bug.[[/keep]]"),
                opt("[[keep]]If we had test it, we wouldn't shipped the bug.[[/keep]]"),
            ),
            "Third conditional (past regret): 'If we had tested..., we wouldn't have shipped...'.",
        ),
        q(
            'In "live" vs "leave", which has the long /iː/ sound?',
            (
                opt("[[keep]]leave[[/keep]]", correct=True),
                opt("[[keep]]live[[/keep]] (verb)"),
                opt("both the same"),
                opt("neither"),
            ),
            "'leave' = long /iː/; 'live' (verb) = short /ɪ/.",
        ),
        q(
            "How do you correctly ask a question?",
            (
                opt("[[keep]]Can I ask a question?[[/keep]]", correct=True),
                opt("[[keep]]Can I make a question?[[/keep]]"),
                opt("[[keep]]Can I do a question?[[/keep]]"),
                opt("[[keep]]Can I take a question?[[/keep]]"),
            ),
            "You 'ask a question' in English, never 'make a question'.",
        ),
        q(
            'Report this: "We will deploy" (they said).',
            (
                opt("[[keep]]They said they would deploy.[[/keep]]", correct=True),
                opt("[[keep]]They said they will deploy.[[/keep]]"),
                opt("[[keep]]They told they would deploy.[[/keep]]"),
                opt("[[keep]]They said us they deploy.[[/keep]]"),
            ),
            "Reported speech shifts 'will' → 'would': 'They said they would deploy.'",
        ),
    ),
)
