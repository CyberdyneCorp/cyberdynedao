"""Curated quiz questions for the English for Brazilians — Intermediate course.
Keys are the EXACT content-lesson titles; the seed interleaves a checkpoint quiz
after each content lesson plus a final comprehensive quiz.

Language course for a Brazilian audience: target-English (and the named
Portuguese words) in the OPTIONS are wrapped in ``[[keep]]…[[/keep]]`` so they
survive auto-translation; prompts/explanations stay translatable (pt-BR)."""
# ruff: noqa: RUF001, RUF003 — IPA symbols (ɪ, iː) are intentional pronunciation content.

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "More false friends (the intermediate set)": (
            q(
                'The English word "eventually" means:',
                (
                    opt("[[keep]]eventualmente[[/keep]]"),
                    opt("[[keep]]por fim / no final[[/keep]]", correct=True),
                    opt("[[keep]]talvez[[/keep]]"),
                    opt("[[keep]]de vez em quando[[/keep]]"),
                ),
                "eventually = por fim/no final; 'occasionally' ≈ eventualmente.",
            ),
            q(
                '"We support Postgres" means we:',
                (
                    opt("[[keep]]suportamos (toleramos) o Postgres[[/keep]]"),
                    opt("[[keep]]damos suporte ao / apoiamos o Postgres[[/keep]]", correct=True),
                    opt("[[keep]]aguentamos o Postgres[[/keep]]"),
                    opt("[[keep]]substituímos o Postgres[[/keep]]"),
                ),
                "to support = apoiar / dar suporte; 'to tolerate/bear' = suportar.",
            ),
            q(
                '"I realized the test was wrong" means:',
                (
                    opt("[[keep]]percebi / me dei conta[[/keep]]", correct=True),
                    opt("[[keep]]realizei[[/keep]]"),
                    opt("[[keep]]executei[[/keep]]"),
                    opt("[[keep]]consertei[[/keep]]"),
                ),
                "to realize = perceber / dar-se conta; 'to carry out' = realizar.",
            ),
        ),
        "Tenses Brazilians mix up (present perfect & continuous)": (
            q(
                'How do you say "trabalho aqui há três anos" correctly in English?',
                (
                    opt("[[keep]]I work here since three years.[[/keep]]"),
                    opt("[[keep]]I have worked here for three years.[[/keep]]", correct=True),
                    opt("[[keep]]I am working here since three years.[[/keep]]"),
                    opt("[[keep]]I work here for three years ago.[[/keep]]"),
                ),
                "Duration up to now uses the present perfect + 'for': 'have worked ... for three years'.",
            ),
            q(
                "Which uses `for` vs `since` correctly?",
                (
                    opt(
                        "[[keep]]for two hours[[/keep]] and [[keep]]since Monday[[/keep]]",
                        correct=True,
                    ),
                    opt("[[keep]]since two hours[[/keep]] and [[keep]]for Monday[[/keep]]"),
                    opt("[[keep]]for Monday[[/keep]] and [[keep]]for two hours[[/keep]]"),
                    opt("[[keep]]since two hours[[/keep]] and [[keep]]since a week[[/keep]]"),
                ),
                "'for' + duration (for two hours); 'since' + a start point (since Monday).",
            ),
            q(
                'Which best expresses "estou trabalhando no bug agora"?',
                (
                    opt("[[keep]]I'm working on the bug right now.[[/keep]]", correct=True),
                    opt("[[keep]]I work on the bug right now.[[/keep]]"),
                    opt("[[keep]]I have worked on the bug right now.[[/keep]]"),
                    opt("[[keep]]I working on the bug right now.[[/keep]]"),
                ),
                "Something happening now uses the present continuous: 'I'm working on...'.",
            ),
        ),
        "Prepositions of time & place (in / on / at)": (
            q(
                'Choose the correct preposition: "The release is ___ Friday."',
                (
                    opt("[[keep]]in[[/keep]]"),
                    opt("[[keep]]on[[/keep]]", correct=True),
                    opt("[[keep]]at[[/keep]]"),
                    opt("[[keep]]to[[/keep]]"),
                ),
                "Days take 'on': on Friday.",
            ),
            q(
                'Choose the correct preposition: "The bug is ___ line 42."',
                (
                    opt("[[keep]]in[[/keep]]"),
                    opt("[[keep]]on[[/keep]]", correct=True),
                    opt("[[keep]]at[[/keep]]"),
                    opt("[[keep]]by[[/keep]]"),
                ),
                "A line is treated as a surface/line: 'on line 42'.",
            ),
            q(
                'Choose the correct preposition: "Let\'s meet ___ 3 p.m."',
                (
                    opt("[[keep]]in[[/keep]]"),
                    opt("[[keep]]on[[/keep]]"),
                    opt("[[keep]]at[[/keep]]", correct=True),
                    opt("[[keep]]by[[/keep]]"),
                ),
                "Clock times take 'at': at 3 p.m.",
            ),
        ),
        "Pronunciation 2: word stress & the three sounds of -ed": (
            q(
                'How is the `-ed` in "started" pronounced?',
                (
                    opt("[[keep]]/ɪd/[[/keep]] — an extra syllable (start-id)", correct=True),
                    opt("[[keep]]/t/[[/keep]] — like 'start'"),
                    opt("[[keep]]/d/[[/keep]] — like 'stard'"),
                    opt("it is silent"),
                ),
                "After a t or d, -ed adds the extra syllable /ɪd/: 'start-id'.",
            ),
            q(
                'How is the `-ed` in "fixed" pronounced?',
                (
                    opt("[[keep]]/t/[[/keep]] — sounds like 'fixt'", correct=True),
                    opt("[[keep]]/ɪd/[[/keep]] — an extra syllable 'fix-id'"),
                    opt("[[keep]]/d/[[/keep]] — sounds like 'fixd'"),
                    opt("a full [[keep]]-ed[[/keep]] syllable"),
                ),
                "After a voiceless sound, -ed is /t/: 'fixed' = 'fixt' (no extra syllable).",
            ),
            q(
                "Word stress: which is the natural stress for 'developer'?",
                (
                    opt("[[keep]]DE-ve-lop-er[[/keep]]", correct=True),
                    opt("[[keep]]de-ve-LO-per[[/keep]]"),
                    opt("[[keep]]de-VE-lop-ER[[/keep]]"),
                    opt("[[keep]]DE-VE-LOP-ER[[/keep]] (all equal)"),
                ),
                "English reduces unstressed syllables; the stress is on 'DE-ve-lop-er'.",
            ),
        ),
        "Writing work messages without translating literally": (
            q(
                'The natural English for "qualquer dúvida, me avise" is:',
                (
                    opt("[[keep]]Any doubt, warn me.[[/keep]]"),
                    opt("[[keep]]Let me know if you have any questions.[[/keep]]", correct=True),
                    opt("[[keep]]Whatever doubt, advise me.[[/keep]]"),
                    opt("[[keep]]Any doubt, tell me.[[/keep]]"),
                ),
                "Don't translate literally; a 'dúvida' is a 'question', not a 'doubt'.",
            ),
            q(
                'The natural English for "segue em anexo o relatório" is:',
                (
                    opt("[[keep]]Follows attached the report.[[/keep]]"),
                    opt("[[keep]]I've attached the report.[[/keep]]", correct=True),
                    opt("[[keep]]Follow in attachment the report.[[/keep]]"),
                    opt("[[keep]]Goes attached the report.[[/keep]]"),
                ),
                "Use the English chunk 'I've attached…' / 'Please find attached…'.",
            ),
            q(
                'Which is correct — translating "tenho uma dúvida"?',
                (
                    opt("[[keep]]I have a doubt.[[/keep]]"),
                    opt("[[keep]]I have a question.[[/keep]]", correct=True),
                    opt("[[keep]]I have a question doubt.[[/keep]]"),
                    opt("[[keep]]I am with a doubt.[[/keep]]"),
                ),
                "A 'dúvida' you want clarified is a 'question'; 'doubt' is strong disbelief.",
            ),
        ),
        "make vs do, say vs tell & common collocations": (
            q(
                "Which collocation is correct?",
                (
                    opt("[[keep]]make a decision[[/keep]]", correct=True),
                    opt("[[keep]]do a decision[[/keep]]"),
                    opt("[[keep]]take a decision[[/keep]]"),
                    opt("[[keep]]make a question[[/keep]]"),
                ),
                "You 'make a decision' (and 'ask a question', never 'make a question').",
            ),
            q(
                'Choose the correct verb: "He ___ me the build failed."',
                (
                    opt("[[keep]]said[[/keep]]"),
                    opt("[[keep]]told[[/keep]]", correct=True),
                    opt("[[keep]]say[[/keep]]"),
                    opt("[[keep]]spoke[[/keep]]"),
                ),
                "'tell' takes a person: 'told me'. 'say' has no person: 'said the build failed'.",
            ),
            q(
                "How do you correctly ask a question in English?",
                (
                    opt("[[keep]]Can I make a question?[[/keep]]"),
                    opt("[[keep]]Can I ask a question?[[/keep]]", correct=True),
                    opt("[[keep]]Can I do a question?[[/keep]]"),
                    opt("[[keep]]Can I take a question?[[/keep]]"),
                ),
                "In English you 'ask a question' — never 'make' a question.",
            ),
        ),
    },
    final=(
        q(
            'How do you say "trabalho aqui desde 2022" correctly?',
            (
                opt("[[keep]]I work here since 2022.[[/keep]]"),
                opt("[[keep]]I have worked here since 2022.[[/keep]]", correct=True),
                opt("[[keep]]I am working here since 2022.[[/keep]]"),
                opt("[[keep]]I worked here since 2022.[[/keep]]"),
            ),
            "Use the present perfect with 'since' for duration up to now.",
        ),
        q(
            '"to realize" means:',
            (
                opt("[[keep]]realizar / executar[[/keep]]"),
                opt("[[keep]]perceber / dar-se conta[[/keep]]", correct=True),
                opt("[[keep]]idealizar[[/keep]]"),
                opt("[[keep]]planejar[[/keep]]"),
            ),
            "to realize = perceber; the false friend 'realizar' is 'to carry out'.",
        ),
        q(
            'Choose the preposition: "It runs ___ the server, ___ production."',
            (
                opt("[[keep]]on[[/keep]] … [[keep]]in[[/keep]]", correct=True),
                opt("[[keep]]in[[/keep]] … [[keep]]on[[/keep]]"),
                opt("[[keep]]at[[/keep]] … [[keep]]on[[/keep]]"),
                opt("[[keep]]on[[/keep]] … [[keep]]at[[/keep]]"),
            ),
            "Fixed pairs: 'on the server' and 'in production'.",
        ),
        q(
            'How is the `-ed` in "tested" pronounced?',
            (
                opt("[[keep]]/ɪd/[[/keep]] — extra syllable (test-id)", correct=True),
                opt("[[keep]]/t/[[/keep]]"),
                opt("[[keep]]/d/[[/keep]]"),
                opt("it is silent"),
            ),
            "After a t/d, -ed is the extra syllable /ɪd/: 'test-id'.",
        ),
        q(
            "Which collocation is correct?",
            (
                opt("[[keep]]She told me she was blocked.[[/keep]]", correct=True),
                opt("[[keep]]She said me she was blocked.[[/keep]]"),
                opt("[[keep]]She told that she was blocked.[[/keep]]"),
                opt("[[keep]]She spoke me she was blocked.[[/keep]]"),
            ),
            "'tell' takes a person directly: 'told me'.",
        ),
        q(
            'The natural English for "fico no aguardo" is:',
            (
                opt("[[keep]]I stay in the wait.[[/keep]]"),
                opt("[[keep]]Looking forward to your reply.[[/keep]]", correct=True),
                opt("[[keep]]I am on hold.[[/keep]]"),
                opt("[[keep]]I wait for the answer.[[/keep]]"),
            ),
            "Use the fixed English chunk 'Looking forward to your reply.'",
        ),
    ),
)
