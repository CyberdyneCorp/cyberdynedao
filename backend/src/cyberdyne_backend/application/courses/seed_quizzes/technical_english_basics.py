"""Curated quiz questions for the Technical English for Engineers — Basics
course. Keys are the EXACT content-lesson titles; the seed interleaves a
checkpoint quiz after each content lesson plus a final comprehensive quiz.

This is a language course, so quiz OPTIONS that are themselves target-English
(words/phrases under test) are wrapped in ``[[keep]]…[[/keep]]`` to survive
auto-translation; the question prompts and explanations stay translatable."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Core engineering & software vocabulary": (
            q(
                "Which word means an error in the code?",
                (
                    opt("[[keep]]a feature[[/keep]]"),
                    opt("[[keep]]a bug[[/keep]]", correct=True),
                    opt("[[keep]]a deployment[[/keep]]"),
                    opt("[[keep]]a requirement[[/keep]]"),
                ),
                "A bug is an error in the code; a feature is a capability the software offers.",
            ),
            q(
                'Choose the correct word: "We need to ___ this bug before the release."',
                (
                    opt("[[keep]]build[[/keep]]"),
                    opt("[[keep]]deploy[[/keep]]"),
                    opt("[[keep]]fix[[/keep]]", correct=True),
                    opt("[[keep]]run[[/keep]]"),
                ),
                "You fix a bug. You build software, deploy code, and run a program.",
            ),
            q(
                'Why is it wrong to say "two softwares"?',
                (
                    opt(
                        "[[keep]]software[[/keep]] is uncountable; say "
                        '[[keep]]"two pieces of software"[[/keep]]',
                        correct=True,
                    ),
                    opt("[[keep]]software[[/keep]] is always plural already"),
                    opt("[[keep]]software[[/keep]] must be written with a capital letter"),
                    opt('There is nothing wrong with "two softwares"'),
                ),
                "Software (like hardware) is uncountable; quantify it with 'a piece of software'.",
            ),
        ),
        "Describing what you build (present simple)": (
            q(
                'Choose the correct form: "The server ___ the user data."',
                (
                    opt("[[keep]]store[[/keep]]"),
                    opt("[[keep]]stores[[/keep]]", correct=True),
                    opt("[[keep]]storing[[/keep]]"),
                    opt("[[keep]]is store[[/keep]]"),
                ),
                "With 'it' / a singular subject in the present simple, add -s: the server stores.",
            ),
            q(
                "Which sentence correctly makes the present simple negative?",
                (
                    opt('[[keep]]"The cache does not store passwords."[[/keep]]', correct=True),
                    opt('[[keep]]"The cache not store passwords."[[/keep]]'),
                    opt('[[keep]]"The cache stores not passwords."[[/keep]]'),
                    opt('[[keep]]"The cache no stores passwords."[[/keep]]'),
                ),
                "Negatives use does not / do not + base verb: 'does not store'.",
            ),
            q(
                "Which is the correct present-simple question?",
                (
                    opt('[[keep]]"Does the function handle empty input?"[[/keep]]', correct=True),
                    opt('[[keep]]"Does the function handles empty input?"[[/keep]]'),
                    opt('[[keep]]"The function handles empty input?"[[/keep]]'),
                    opt('[[keep]]"Do the function handle empty input?"[[/keep]]'),
                ),
                "After 'does', the main verb stays in its base form: 'Does the function handle...'.",
            ),
        ),
        "Numbers, units & measurements": (
            q(
                "How do you read the number `3.5` aloud in English?",
                (
                    opt('[[keep]]"three comma five"[[/keep]]'),
                    opt('[[keep]]"three point five"[[/keep]]', correct=True),
                    opt('[[keep]]"three and five"[[/keep]]'),
                    opt('[[keep]]"thirty-five"[[/keep]]'),
                ),
                "English uses a point for decimals: 3.5 is 'three point five'.",
            ),
            q(
                "How do you read `50 req/s` aloud?",
                (
                    opt('[[keep]]"fifty requests slash seconds"[[/keep]]'),
                    opt('[[keep]]"fifty requests per second"[[/keep]]', correct=True),
                    opt('[[keep]]"fifty requests for second"[[/keep]]'),
                    opt('[[keep]]"five zero requests second"[[/keep]]'),
                ),
                "The symbol / is read 'per' in a rate: 'fifty requests per second'.",
            ),
            q(
                "How do you read the version `v2.10.3`?",
                (
                    opt('[[keep]]"version two point ten point three"[[/keep]]', correct=True),
                    opt('[[keep]]"version two hundred ten point three"[[/keep]]'),
                    opt('[[keep]]"version two comma ten comma three"[[/keep]]'),
                    opt('[[keep]]"version twenty-one hundred three"[[/keep]]'),
                ),
                "Read each part separately with 'point' between them: two point ten point three.",
            ),
        ),
        "Reading code & documentation aloud": (
            q(
                "What is the spoken name of the symbol `_`?",
                (
                    opt('[[keep]]"dash"[[/keep]]'),
                    opt('[[keep]]"underscore"[[/keep]]', correct=True),
                    opt('[[keep]]"hyphen"[[/keep]]'),
                    opt('[[keep]]"dot"[[/keep]]'),
                ),
                "_ is read 'underscore'. The dash/hyphen is the symbol -.",
            ),
            q(
                "How do you read the file path `src/app/main.py` aloud?",
                (
                    opt('[[keep]]"src slash app slash main dot py"[[/keep]]', correct=True),
                    opt('[[keep]]"src backslash app backslash main dot py"[[/keep]]'),
                    opt('[[keep]]"src dot app dot main slash py"[[/keep]]'),
                    opt('[[keep]]"src app main py"[[/keep]]'),
                ),
                "/ is read 'slash' and . is read 'dot': 'src slash app slash main dot py'.",
            ),
            q(
                'Choose the natural way to describe what code does: "This loop ___ over the '
                'list and prints each item."',
                (
                    opt("[[keep]]iterate[[/keep]]"),
                    opt("[[keep]]iterates[[/keep]]", correct=True),
                    opt("[[keep]]iterating[[/keep]]"),
                    opt("[[keep]]iterated[[/keep]]"),
                ),
                "Describe what code does in the present simple; 'the loop' is singular: 'iterates'.",
            ),
        ),
        "Asking questions & clarifying in meetings": (
            q(
                "You did not hear the last sentence. What is the polite thing to say?",
                (
                    opt('[[keep]]"Could you repeat that, please?"[[/keep]]', correct=True),
                    opt('[[keep]]"Repeat."[[/keep]]'),
                    opt('[[keep]]"I don\'t listen you."[[/keep]]'),
                    opt('[[keep]]"Talk again now."[[/keep]]'),
                ),
                "'Could you repeat that, please?' is polite and clear; bare commands sound rude.",
            ),
            q(
                "Which phrase confirms that you understood correctly?",
                (
                    opt(
                        '[[keep]]"So, if I understand correctly, we deploy on Friday. '
                        'Is that right?"[[/keep]]',
                        correct=True,
                    ),
                    opt('[[keep]]"I don\'t care about the details."[[/keep]]'),
                    opt('[[keep]]"Let\'s take this offline."[[/keep]]'),
                    opt('[[keep]]"That\'s all from me."[[/keep]]'),
                ),
                "Repeating it back ('if I understand correctly... is that right?') confirms understanding.",
            ),
            q(
                'Choose the correct question word: "___ is the deadline?"',
                (
                    opt("[[keep]]Who[[/keep]]"),
                    opt("[[keep]]When[[/keep]]", correct=True),
                    opt("[[keep]]Where[[/keep]]"),
                    opt("[[keep]]Why[[/keep]]"),
                ),
                "'When' asks about time, which a deadline is. 'Who' asks about a person.",
            ),
        ),
        "Email & chat / PR-comment basics": (
            q(
                'What does the PR comment "LGTM" mean?',
                (
                    opt('[[keep]]"Looks good to me"[[/keep]] — an approval', correct=True),
                    opt('[[keep]]"Let\'s get this merged"[[/keep]]'),
                    opt('[[keep]]"Leave good test materials"[[/keep]]'),
                    opt('[[keep]]"Looking great, too much"[[/keep]]'),
                ),
                "LGTM = 'Looks good to me', a common way to approve a pull request.",
            ),
            q(
                "Which is the most polite PR comment asking for a change?",
                (
                    opt(
                        '[[keep]]"Could we rename this variable to make it clearer?"[[/keep]]',
                        correct=True,
                    ),
                    opt('[[keep]]"This name is bad."[[/keep]]'),
                    opt('[[keep]]"Rename. Now."[[/keep]]'),
                    opt('[[keep]]"Why did you write this?"[[/keep]]'),
                ),
                "A question with 'Could we...' is collaborative; blunt orders feel harsh.",
            ),
            q(
                'What does the abbreviation "ASAP" mean?',
                (
                    opt('[[keep]]"as soon as possible"[[/keep]]', correct=True),
                    opt('[[keep]]"as simple as possible"[[/keep]]'),
                    opt('[[keep]]"after support and planning"[[/keep]]'),
                    opt('[[keep]]"a server and a port"[[/keep]]'),
                ),
                "ASAP = 'as soon as possible'. FYI = 'for your information'.",
            ),
        ),
    },
    final=(
        q(
            "Which sentence uses the present simple correctly?",
            (
                opt('[[keep]]"The API accepts JSON and returns JSON."[[/keep]]', correct=True),
                opt('[[keep]]"The API accept JSON and return JSON."[[/keep]]'),
                opt('[[keep]]"The API accepting JSON and returning JSON."[[/keep]]'),
                opt('[[keep]]"The API is accept JSON and is return JSON."[[/keep]]'),
            ),
            "A singular subject ('the API') takes -s in the present simple: accepts, returns.",
        ),
        q(
            'Choose the correct word: "There is a ___ in the login page."',
            (
                opt("[[keep]]bug[[/keep]]", correct=True),
                opt("[[keep]]feature[[/keep]]"),
                opt("[[keep]]deployment[[/keep]]"),
                opt("[[keep]]server[[/keep]]"),
            ),
            "An error in the code is a bug.",
        ),
        q(
            "How do you read `200 ms` aloud?",
            (
                opt('[[keep]]"two hundred milliseconds"[[/keep]]', correct=True),
                opt('[[keep]]"two hundred meters per second"[[/keep]]'),
                opt('[[keep]]"two zero zero microseconds"[[/keep]]'),
                opt('[[keep]]"twenty milliseconds"[[/keep]]'),
            ),
            "ms is milliseconds: 'two hundred milliseconds'.",
        ),
        q(
            "What is the spoken name of the symbol `.` in `main.py`?",
            (
                opt('[[keep]]"dot"[[/keep]]', correct=True),
                opt('[[keep]]"point"[[/keep]]'),
                opt('[[keep]]"period stop"[[/keep]]'),
                opt('[[keep]]"slash"[[/keep]]'),
            ),
            "In code and file names the . is read 'dot': 'main dot py'.",
        ),
        q(
            "You did not understand a word in a meeting. What is the best thing to do?",
            (
                opt(
                    "Ask politely, e.g. [[keep]]\"What do you mean by 'rollback'?\"[[/keep]]",
                    correct=True,
                ),
                opt("Stay silent and guess the meaning later"),
                opt("Pretend you understood and move on"),
                opt("Leave the meeting"),
            ),
            "Asking a clear, polite question is better than guessing wrong or staying silent.",
        ),
        q(
            "Which message is appropriately polite for team chat?",
            (
                opt('[[keep]]"Hey, quick question — is staging down?"[[/keep]]', correct=True),
                opt('[[keep]]"FIX STAGING NOW"[[/keep]]'),
                opt('[[keep]]"staging broken your fault"[[/keep]]'),
                opt('[[keep]]"why is nothing working"[[/keep]]'),
            ),
            "Chat is informal but should stay polite; a short, friendly question works well.",
        ),
    ),
)
