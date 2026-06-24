"""Curated quiz questions for the Technical English for Engineers —
Intermediate course. Keys are the EXACT content-lesson titles; the seed
interleaves a checkpoint quiz after each content lesson plus a final
comprehensive quiz.

Quiz OPTIONS that are themselves target-English (words/phrases under test) are
wrapped in ``[[keep]]…[[/keep]]`` so they survive auto-translation; prompts and
explanations stay translatable."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Describing processes & pipelines (sequencing)": (
            q(
                "Which word best starts the last step of a process?",
                (
                    opt("[[keep]]First,[[/keep]]"),
                    opt("[[keep]]Then,[[/keep]]"),
                    opt("[[keep]]Finally,[[/keep]]", correct=True),
                    opt("[[keep]]Next,[[/keep]]"),
                ),
                "'Finally,' introduces the last step; 'First,' starts and 'Then/Next' link middle steps.",
            ),
            q(
                "Choose the correct passive sentence for an automatic step:",
                (
                    opt(
                        '[[keep]]"The image is built and pushed to the registry."[[/keep]]',
                        correct=True,
                    ),
                    opt('[[keep]]"The image building and pushing to the registry."[[/keep]]'),
                    opt('[[keep]]"The image build and push to the registry."[[/keep]]'),
                    opt('[[keep]]"The image is build and push to the registry."[[/keep]]'),
                ),
                "The passive is 'be' + past participle: 'is built', 'is pushed'.",
            ),
            q(
                'Choose the correct word: "The tests run ___ the deployment."',
                (
                    opt("[[keep]]before[[/keep]]", correct=True),
                    opt("[[keep]]while[[/keep]]"),
                    opt("[[keep]]during[[/keep]]"),
                    opt("[[keep]]since[[/keep]]"),
                ),
                "Tests come first, so they run 'before' the deployment.",
            ),
        ),
        "Comparing options & trade-offs": (
            q(
                'Choose the correct comparative: "Redis is ___ Postgres for caching."',
                (
                    opt("[[keep]]more fast than[[/keep]]"),
                    opt("[[keep]]faster than[[/keep]]", correct=True),
                    opt("[[keep]]the fastest than[[/keep]]"),
                    opt("[[keep]]fast than[[/keep]]"),
                ),
                "Short adjectives form the comparative with -er + than: 'faster than'.",
            ),
            q(
                "What does the word [[keep]]trade-off[[/keep]] mean?",
                (
                    opt("you gain one thing but lose another", correct=True),
                    opt("a discount on cloud services"),
                    opt("a meeting to compare prices"),
                    opt("a type of deployment"),
                ),
                "A trade-off is when improving one quality costs you another (e.g. speed vs memory).",
            ),
            q(
                "Which connector correctly contrasts two ideas?",
                (
                    opt(
                        "[[keep]]\"It's reliable; however, it's harder to set up.\"[[/keep]]",
                        correct=True,
                    ),
                    opt("[[keep]]\"It's reliable; because it's harder to set up.\"[[/keep]]"),
                    opt("[[keep]]\"It's reliable; therefore it's harder to set up.\"[[/keep]]"),
                    opt("[[keep]]\"It's reliable; so it's harder to set up.\"[[/keep]]"),
                ),
                "'however' signals a contrast; 'because/therefore/so' signal cause or result.",
            ),
        ),
        "Code-review English (polite suggestions & requests)": (
            q(
                "Which is the most polite review comment?",
                (
                    opt(
                        '[[keep]]"Would it make sense to add a test here?"[[/keep]]',
                        correct=True,
                    ),
                    opt('[[keep]]"Add a test."[[/keep]]'),
                    opt('[[keep]]"This has no tests, obviously."[[/keep]]'),
                    opt('[[keep]]"You forgot the tests again."[[/keep]]'),
                ),
                "Modal questions ('Would it make sense to...?') soften a request into a suggestion.",
            ),
            q(
                "In review comments, what does the prefix [[keep]]Nit:[[/keep]] signal?",
                (
                    opt("a tiny, optional point", correct=True),
                    opt("a change that must be made before merge"),
                    opt("a security vulnerability"),
                    opt("a question for the whole team"),
                ),
                "'Nit' marks a minor, non-blocking point; 'Blocking' marks something that must be fixed.",
            ),
            q(
                "How should you respond graciously to good feedback?",
                (
                    opt('[[keep]]"Good point, I\'ll fix that."[[/keep]]', correct=True),
                    opt('[[keep]]"That\'s not my problem."[[/keep]]'),
                    opt('[[keep]]"It works on my machine."[[/keep]]'),
                    opt('[[keep]]"You don\'t understand the code."[[/keep]]'),
                ),
                "Accepting feedback warmly ('Good point, I'll fix that') keeps the review collaborative.",
            ),
        ),
        "Incident reports & postmortems (past tenses)": (
            q(
                'Choose the correct past simple: "The service ___ at 14:30."',
                (
                    opt("[[keep]]crash[[/keep]]"),
                    opt("[[keep]]crashed[[/keep]]", correct=True),
                    opt("[[keep]]crashing[[/keep]]"),
                    opt("[[keep]]is crashing[[/keep]]"),
                ),
                "A finished action at a known time uses the past simple: 'crashed'.",
            ),
            q(
                "Which sentence correctly uses the past continuous for the background?",
                (
                    opt(
                        '[[keep]]"Traffic was increasing when the server went down."[[/keep]]',
                        correct=True,
                    ),
                    opt('[[keep]]"Traffic increasing when the server went down."[[/keep]]'),
                    opt('[[keep]]"Traffic is increasing when the server went down."[[/keep]]'),
                    opt('[[keep]]"Traffic increase when the server goes down."[[/keep]]'),
                ),
                "Past continuous = was/were + verb-ing, for the background action: 'was increasing'.",
            ),
            q(
                "What does it mean for a postmortem to be [[keep]]blameless[[/keep]]?",
                (
                    opt("it describes what failed, not who is guilty", correct=True),
                    opt("it has no conclusion"),
                    opt("nobody reads it"),
                    opt("it never mentions the outage"),
                ),
                "A blameless postmortem focuses on causes to learn from, not on blaming a person.",
            ),
        ),
        "Conditionals for debugging": (
            q(
                "Choose the correct zero conditional (a general rule):",
                (
                    opt(
                        '[[keep]]"If the input is empty, the function returns null."[[/keep]]',
                        correct=True,
                    ),
                    opt('[[keep]]"If the input is empty, the function will return null."[[/keep]]'),
                    opt(
                        '[[keep]]"If the input were empty, the function would return null."[[/keep]]'
                    ),
                    opt('[[keep]]"If the input empty, the function return null."[[/keep]]'),
                ),
                "The zero conditional uses present + present for an always-true rule.",
            ),
            q(
                'Complete the first conditional: "If we add an index, the query ___ faster."',
                (
                    opt("[[keep]]will be[[/keep]]", correct=True),
                    opt("[[keep]]would be[[/keep]]"),
                    opt("[[keep]]is[[/keep]]"),
                    opt("[[keep]]was[[/keep]]"),
                ),
                "First conditional (likely future): if + present, ... will + verb: 'will be'.",
            ),
            q(
                "Which sentence is a second conditional (hypothetical)?",
                (
                    opt(
                        '[[keep]]"If the database were down, we would see connection errors."[[/keep]]',
                        correct=True,
                    ),
                    opt(
                        '[[keep]]"If the database is down, we will see connection errors."[[/keep]]'
                    ),
                    opt('[[keep]]"If the database is down, we see connection errors."[[/keep]]'),
                    opt('[[keep]]"If the database down, we seeing connection errors."[[/keep]]'),
                ),
                "Second conditional: if + past, ... would + verb, for a hypothetical situation.",
            ),
        ),
        "Standups & meeting English": (
            q(
                "What does it mean to say you are [[keep]]blocked[[/keep]] in a standup?",
                (
                    opt("something is stopping you from making progress", correct=True),
                    opt("you finished all your work"),
                    opt("you will work from home"),
                    opt("you are on vacation"),
                ),
                "A blocker is something stopping you; saying you're blocked asks the team for help.",
            ),
            q(
                'What does [[keep]]"Let\'s take this offline"[[/keep]] mean in a meeting?',
                (
                    opt("let's discuss this later, not now", correct=True),
                    opt("let's turn off the internet"),
                    opt("let's cancel the meeting"),
                    opt("let's write it down on paper"),
                ),
                "'Take it offline' means move a long side-topic out of the current meeting.",
            ),
            q(
                'Choose the correct future form: "Today ___ start on the password-reset flow."',
                (
                    opt("[[keep]]I'll[[/keep]]", correct=True),
                    opt("[[keep]]I[[/keep]]"),
                    opt("[[keep]]I'm[[/keep]]"),
                    opt("[[keep]]I was[[/keep]]"),
                ),
                "Future plans for today use will / I'll: 'Today I'll start...'.",
            ),
        ),
    },
    final=(
        q(
            "Which sentence correctly sequences a step in a pipeline?",
            (
                opt('[[keep]]"After the build passes, we deploy."[[/keep]]', correct=True),
                opt('[[keep]]"After the build passes, we deploying."[[/keep]]'),
                opt('[[keep]]"After the build pass, we deploys."[[/keep]]'),
                opt('[[keep]]"The build passes after we will deploy."[[/keep]]'),
            ),
            "'After + present, we + present' clearly orders the steps.",
        ),
        q(
            'Choose the correct comparative: "A microservice is ___ a monolith."',
            (
                opt("[[keep]]more flexible than[[/keep]]", correct=True),
                opt("[[keep]]flexibler than[[/keep]]"),
                opt("[[keep]]more flexible that[[/keep]]"),
                opt("[[keep]]most flexible than[[/keep]]"),
            ),
            "Longer adjectives use 'more ... than': 'more flexible than'.",
        ),
        q(
            "Which review comment is polite and collaborative?",
            (
                opt(
                    '[[keep]]"What do you think about doing it this way instead?"[[/keep]]',
                    correct=True,
                ),
                opt('[[keep]]"Don\'t do it this way."[[/keep]]'),
                opt('[[keep]]"This is wrong."[[/keep]]'),
                opt('[[keep]]"Change it."[[/keep]]'),
            ),
            "Asking 'What do you think about...?' invites discussion rather than giving an order.",
        ),
        q(
            'Choose the correct past tense for a postmortem: "We ___ the change and the service '
            'recovered."',
            (
                opt("[[keep]]reverted[[/keep]]", correct=True),
                opt("[[keep]]revert[[/keep]]"),
                opt("[[keep]]reverting[[/keep]]"),
                opt("[[keep]]will revert[[/keep]]"),
            ),
            "A finished past action uses the past simple: 'reverted'.",
        ),
        q(
            "Which is a correct first conditional for a prediction?",
            (
                opt(
                    '[[keep]]"If you pass a negative number, it will throw an error."[[/keep]]',
                    correct=True,
                ),
                opt('[[keep]]"If you pass a negative number, it throws will an error."[[/keep]]'),
                opt('[[keep]]"If you passed a negative number, it will throw an error."[[/keep]]'),
                opt('[[keep]]"If you will pass a negative number, it throws an error."[[/keep]]'),
            ),
            "First conditional: if + present, ... will + base verb.",
        ),
        q(
            'Complete the standup update: "Yesterday I ___ the login API."',
            (
                opt("[[keep]]finished[[/keep]]", correct=True),
                opt("[[keep]]finish[[/keep]]"),
                opt("[[keep]]will finish[[/keep]]"),
                opt("[[keep]]am finishing[[/keep]]"),
            ),
            "'Yesterday' signals the past simple: 'I finished'.",
        ),
    ),
)
