"""Curated quiz questions for the English for Brazilians — Basics course. Keys
are the EXACT content-lesson titles; the seed interleaves a checkpoint quiz
after each content lesson plus a final comprehensive quiz.

This is a language course for a Brazilian audience: quiz OPTIONS that are
themselves target-English (or the Portuguese words named in the lesson) are
wrapped in ``[[keep]]…[[/keep]]`` so they survive auto-translation; the question
prompts and explanations stay translatable (delivered in pt-BR)."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Falsos cognatos: the words that trick Brazilians": (
            q(
                'In English, the verb "to push" means:',
                (
                    opt("[[keep]]puxar[[/keep]]"),
                    opt("[[keep]]empurrar[[/keep]]", correct=True),
                    opt("[[keep]]fingir[[/keep]]"),
                    opt("[[keep]]perceber[[/keep]]"),
                ),
                "push = empurrar (the opposite of puxar, which is 'pull').",
            ),
            q(
                'What is a code "library" in Portuguese?',
                (
                    opt("[[keep]]livraria[[/keep]]"),
                    opt("[[keep]]biblioteca[[/keep]]", correct=True),
                    opt("[[keep]]biblioteconomia[[/keep]]"),
                    opt("[[keep]]bibliografia[[/keep]]"),
                ),
                "library = biblioteca; a bookstore (livraria) is a 'bookstore'.",
            ),
            q(
                'The English word "actually" means:',
                (
                    opt("[[keep]]atualmente[[/keep]]"),
                    opt("[[keep]]na verdade[[/keep]]", correct=True),
                    opt("[[keep]]eventualmente[[/keep]]"),
                    opt("[[keep]]realmente agora[[/keep]]"),
                ),
                "actually = na verdade; 'currently' = atualmente.",
            ),
        ),
        "Sounds that don't exist in Portuguese (TH, H, final consonants)": (
            q(
                'How should the word "host" be pronounced by a Brazilian who wants to be clear?',
                (
                    opt("with a silent h, like the Portuguese [[keep]]hora[[/keep]]"),
                    opt("with a real puff of air on the [[keep]]h[[/keep]]", correct=True),
                    opt("as [[keep]]oste[[/keep]] with an extra vowel"),
                    opt("with a [[keep]]r[[/keep]] sound instead of h"),
                ),
                "In English the h is pronounced (a puff of air); it is not silent like in Portuguese.",
            ),
            q(
                'A common Brazilian mistake is to pronounce "start" as:',
                (
                    opt("[[keep]]e-start[[/keep]] (adding an 'e' at the beginning)", correct=True),
                    opt("[[keep]]start[[/keep]] (correct)"),
                    opt("[[keep]]sta[[/keep]] (dropping the t)"),
                    opt("[[keep]]tart[[/keep]] (dropping the s)"),
                ),
                "Portuguese adds an 'e' before s+consonant; English begins directly on the s.",
            ),
            q(
                'Why do Brazilians often say "bug-ee" instead of "bug"?',
                (
                    opt(
                        "Portuguese words rarely end in a hard consonant, so we add a vowel",
                        correct=True,
                    ),
                    opt("[[keep]]bug[[/keep]] has two syllables in English"),
                    opt("the [[keep]]g[[/keep]] is silent in English"),
                    opt("it is the correct American pronunciation"),
                ),
                "Stop the word on the final consonant — no extra 'i' sound at the end.",
            ),
        ),
        "Articles, plurals & uncountables (a / an / the)": (
            q(
                "Which is correct?",
                (
                    opt("[[keep]]I need more informations.[[/keep]]"),
                    opt("[[keep]]I need more information.[[/keep]]", correct=True),
                    opt("[[keep]]I need a information.[[/keep]]"),
                    opt("[[keep]]I need an informations.[[/keep]]"),
                ),
                "'information' is uncountable: no plural and no 'a/an'. Use 'some information'.",
            ),
            q(
                'Choose the correct article: "We hit ___ error."',
                (
                    opt("[[keep]]a[[/keep]]"),
                    opt("[[keep]]an[[/keep]]", correct=True),
                    opt("[[keep]]the[[/keep]] (always)"),
                    opt("(no article needed)"),
                ),
                "'error' begins with a vowel sound, so use 'an error'.",
            ),
            q(
                "How do you give feedback correctly?",
                (
                    opt("[[keep]]I have some feedback on your PR.[[/keep]]", correct=True),
                    opt("[[keep]]I have a feedback on your PR.[[/keep]]"),
                    opt("[[keep]]I have feedbacks on your PR.[[/keep]]"),
                    opt("[[keep]]I have an feedbacks on your PR.[[/keep]]"),
                ),
                "'feedback' is uncountable: 'some feedback', never 'a feedback' or 'feedbacks'.",
            ),
        ),
        "Word order: adjectives before nouns, and S-V-O": (
            q(
                'How do you say "código limpo" in English?',
                (
                    opt("[[keep]]code clean[[/keep]]"),
                    opt("[[keep]]clean code[[/keep]]", correct=True),
                    opt("[[keep]]the code clean[[/keep]]"),
                    opt("[[keep]]cleanly code[[/keep]]"),
                ),
                "English adjectives go BEFORE the noun: clean code (not 'code clean').",
            ),
            q(
                'How do you say there is a bug, translating "há um bug no código"?',
                (
                    opt("[[keep]]There is a bug in the code.[[/keep]]", correct=True),
                    opt("[[keep]]Has a bug in the code.[[/keep]]"),
                    opt("[[keep]]Have a bug in the code.[[/keep]]"),
                    opt("[[keep]]It has a bug in the code.[[/keep]] (for 'há')"),
                ),
                "English uses 'there is / there are' for 'há / existe', not 'has'.",
            ),
            q(
                "Which sentence keeps the required subject?",
                (
                    opt("[[keep]]It is working.[[/keep]]", correct=True),
                    opt("[[keep]]Is working.[[/keep]]"),
                    opt("[[keep]]Working now.[[/keep]]"),
                    opt("[[keep]]Are working.[[/keep]]"),
                ),
                "English rarely drops the subject; use a dummy 'it': 'It is working.'",
            ),
        ),
        "Present simple & the third-person -s we forget": (
            q(
                'Choose the correct form: "She ___ tests every morning."',
                (
                    opt("[[keep]]write[[/keep]]"),
                    opt("[[keep]]writes[[/keep]]", correct=True),
                    opt("[[keep]]writing[[/keep]]"),
                    opt("[[keep]]is write[[/keep]]"),
                ),
                "With he/she/it, add -s in the present simple: she writes.",
            ),
            q(
                "Which negative is correct?",
                (
                    opt("[[keep]]The cache does not store passwords.[[/keep]]", correct=True),
                    opt("[[keep]]The cache does not stores passwords.[[/keep]]"),
                    opt("[[keep]]The cache not store passwords.[[/keep]]"),
                    opt("[[keep]]The cache don't stores passwords.[[/keep]]"),
                ),
                "After 'does', the verb returns to its base form: 'does not store'.",
            ),
            q(
                "Which question is correct?",
                (
                    opt("[[keep]]Does the function handle empty input?[[/keep]]", correct=True),
                    opt("[[keep]]Does the function handles empty input?[[/keep]]"),
                    opt("[[keep]]Do the function handles empty input?[[/keep]]"),
                    opt("[[keep]]The function handle empty input?[[/keep]]"),
                ),
                "Use 'does' + base verb: 'Does the function handle...?'",
            ),
        ),
        "Survival English for engineers (greetings, numbers, daily phrases)": (
            q(
                "How do you read the number `3.5` aloud in English?",
                (
                    opt("[[keep]]three comma five[[/keep]]"),
                    opt("[[keep]]three point five[[/keep]]", correct=True),
                    opt("[[keep]]three and a half point[[/keep]]"),
                    opt("[[keep]]thirty-five[[/keep]]"),
                ),
                "English uses a point for decimals (Portuguese would write 3,5).",
            ),
            q(
                "In the US, the date `03/04` means:",
                (
                    opt("the 3rd of April"),
                    opt("the 4th of March", correct=True),
                    opt("the 3rd of March"),
                    opt("the 4th of April"),
                ),
                "Americans write month/day, so 03/04 = March 4th. Say the month by name to be safe.",
            ),
            q(
                "What is the most polite way to ask a colleague for something?",
                (
                    opt("[[keep]]Could you review my PR, please?[[/keep]]", correct=True),
                    opt("[[keep]]Review my PR.[[/keep]]"),
                    opt("[[keep]]You review my PR now.[[/keep]]"),
                    opt("[[keep]]Review my PR, obligatory.[[/keep]]"),
                ),
                "'Could you... please?' is polite; bare commands sound rude in English.",
            ),
        ),
    },
    final=(
        q(
            'The Git command "push" means, in Portuguese:',
            (
                opt("[[keep]]puxar[[/keep]]"),
                opt("[[keep]]empurrar / enviar[[/keep]]", correct=True),
                opt("[[keep]]fingir[[/keep]]"),
                opt("[[keep]]apagar[[/keep]]"),
            ),
            "push = empurrar/enviar; the false friend 'puxar' is actually 'pull'.",
        ),
        q(
            "Which is correct?",
            (
                opt("[[keep]]People are waiting.[[/keep]]", correct=True),
                opt("[[keep]]People is waiting.[[/keep]]"),
                opt("[[keep]]The people is waiting.[[/keep]]"),
                opt("[[keep]]People waiting is.[[/keep]]"),
            ),
            "'people' is plural and takes a plural verb: 'People are waiting.'",
        ),
        q(
            'How do you translate "código rápido"?',
            (
                opt("[[keep]]code fast[[/keep]]"),
                opt("[[keep]]fast code[[/keep]]", correct=True),
                opt("[[keep]]the fast the code[[/keep]]"),
                opt("[[keep]]code fastly[[/keep]]"),
            ),
            "Adjective before noun: 'fast code'.",
        ),
        q(
            'Choose the correct verb form: "The server ___ the data."',
            (
                opt("[[keep]]store[[/keep]]"),
                opt("[[keep]]stores[[/keep]]", correct=True),
                opt("[[keep]]storing[[/keep]]"),
                opt("[[keep]]store's[[/keep]]"),
            ),
            "A singular subject (the server / it) takes -s: 'stores'.",
        ),
        q(
            "Which sentence is correct?",
            (
                opt("[[keep]]I need some information.[[/keep]]", correct=True),
                opt("[[keep]]I need an information.[[/keep]]"),
                opt("[[keep]]I need informations.[[/keep]]"),
                opt("[[keep]]I need a informations.[[/keep]]"),
            ),
            "'information' is uncountable: 'some information', no plural, no 'a/an'.",
        ),
        q(
            'The English word "library" most often means, for a developer:',
            (
                opt("[[keep]]biblioteca[[/keep]] (a collection of reusable code)", correct=True),
                opt("[[keep]]livraria[[/keep]] (a shop that sells books)"),
                opt("[[keep]]bibliografia[[/keep]]"),
                opt("[[keep]]biblioteconomia[[/keep]]"),
            ),
            "library = biblioteca; a code library is a reusable code collection.",
        ),
    ),
)
