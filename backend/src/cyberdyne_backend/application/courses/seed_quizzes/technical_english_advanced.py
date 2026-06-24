"""Curated quiz questions for the Technical English for Engineers — Advanced
course. Keys are the EXACT content-lesson titles; the seed interleaves a
checkpoint quiz after each content lesson plus a final comprehensive quiz.

Quiz OPTIONS that are themselves target-English (words/phrases under test) are
wrapped in ``[[keep]]…[[/keep]]`` so they survive auto-translation; prompts and
explanations stay translatable."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Architecture & design-doc discussions": (
            q(
                "What does [[keep]]a bottleneck[[/keep]] mean in a system?",
                (
                    opt("the slowest part that limits the whole system", correct=True),
                    opt("a component that has no dependencies"),
                    opt("the user interface layer"),
                    opt("a backup server"),
                ),
                "A bottleneck is the slowest stage that caps overall throughput.",
            ),
            q(
                'Choose the correct word: "The auth service ___ on the user database."',
                (
                    opt("[[keep]]depends[[/keep]]", correct=True),
                    opt("[[keep]]routes[[/keep]]"),
                    opt("[[keep]]decouples[[/keep]]"),
                    opt("[[keep]]scales[[/keep]]"),
                ),
                "'depends on' expresses a dependency; you route requests and scale load.",
            ),
            q(
                "Which sentence states a design decision with its justification?",
                (
                    opt(
                        '[[keep]]"We chose an event-driven design so that services stay '
                        'loosely coupled."[[/keep]]',
                        correct=True,
                    ),
                    opt('[[keep]]"We chose an event-driven design."[[/keep]]'),
                    opt('[[keep]]"Event-driven design loosely coupled."[[/keep]]'),
                    opt('[[keep]]"So that services event-driven we chose."[[/keep]]'),
                ),
                "A decision + 'so that...' gives both the choice and its reason.",
            ),
        ),
        "Presenting technical work & demos": (
            q(
                "Which phrase is a signpost that moves the audience to the next section?",
                (
                    opt('[[keep]]"Now let\'s move on to the demo."[[/keep]]', correct=True),
                    opt('[[keep]]"I don\'t know what to say."[[/keep]]'),
                    opt('[[keep]]"This is boring."[[/keep]]'),
                    opt('[[keep]]"Maybe later."[[/keep]]'),
                ),
                "Signposting phrases like 'Now let's move on to...' tell listeners where you are.",
            ),
            q(
                "How should you narrate a live demo of actions you perform?",
                (
                    opt(
                        'in the present simple, e.g. [[keep]]"I type a query and hit '
                        'enter."[[/keep]]',
                        correct=True,
                    ),
                    opt('in the past simple, e.g. "I typed a query and hit enter."'),
                    opt('in the future, e.g. "I will type a query and will hit enter."'),
                    opt("with no verbs at all"),
                ),
                "Live narration uses the present simple to describe each action as it happens.",
            ),
            q(
                "An audience member asks something you can't answer. What is a good response?",
                (
                    opt(
                        '[[keep]]"Good point — I\'ll look into that and get back to you."[[/keep]]',
                        correct=True,
                    ),
                    opt('[[keep]]"That\'s not important."[[/keep]]'),
                    opt('[[keep]]"I already said that."[[/keep]]'),
                    opt('[[keep]]"Ask someone else."[[/keep]]'),
                ),
                "It's fine not to know; promising to follow up keeps you credible and polite.",
            ),
        ),
        "Disagreeing & negotiating technical decisions": (
            q(
                "Which sentence disagrees diplomatically?",
                (
                    opt(
                        "[[keep]]\"I see your point, but I'm worried about the performance "
                        'impact."[[/keep]]',
                        correct=True,
                    ),
                    opt('[[keep]]"No, that\'s a bad idea."[[/keep]]'),
                    opt('[[keep]]"You\'re wrong."[[/keep]]'),
                    opt('[[keep]]"That will never work."[[/keep]]'),
                ),
                "The polite pattern is acknowledge ('I see your point') + 'but' + your concern.",
            ),
            q(
                'What does the phrase [[keep]]"disagree and commit"[[/keep]] describe?',
                (
                    opt(
                        "supporting the team's decision fully even though you preferred "
                        "another option",
                        correct=True,
                    ),
                    opt("refusing to follow the decision"),
                    opt("forcing your own opinion on the team"),
                    opt("avoiding the discussion entirely"),
                ),
                "'Disagree and commit' means once the group decides, you back it fully.",
            ),
            q(
                "Which phrase proposes a compromise (middle ground)?",
                (
                    opt(
                        '[[keep]]"What if we ship the simple version first and improve it '
                        'later?"[[/keep]]',
                        correct=True,
                    ),
                    opt('[[keep]]"We\'ll do it my way."[[/keep]]'),
                    opt('[[keep]]"There\'s no other option."[[/keep]]'),
                    opt('[[keep]]"I refuse to change anything."[[/keep]]'),
                ),
                "'What if we... first and ... later?' offers a middle path both sides can accept.",
            ),
        ),
        "Writing precise specs & RFCs": (
            q(
                "In RFC keywords, what does [[keep]]MUST[[/keep]] mean?",
                (
                    opt("an absolute requirement", correct=True),
                    opt("a recommendation with allowed exceptions"),
                    opt("something completely optional"),
                    opt("a suggestion for the future"),
                ),
                "MUST is an absolute requirement; SHOULD is recommended; MAY is optional.",
            ),
            q(
                "Which requirement is precise enough for a spec?",
                (
                    opt(
                        '[[keep]]"Responses MUST return in under 200 ms at p99."[[/keep]]',
                        correct=True,
                    ),
                    opt('[[keep]]"Responses should be fast."[[/keep]]'),
                    opt('[[keep]]"It should handle a lot of users."[[/keep]]'),
                    opt('[[keep]]"It should be secure."[[/keep]]'),
                ),
                "Precise specs use measurable terms ('under 200 ms at p99') instead of vague words.",
            ),
            q(
                'Choose the correct keyword: "Clients ___ retry on a 503 response." '
                "(recommended, but exceptions are allowed)",
                (
                    opt("[[keep]]SHOULD[[/keep]]", correct=True),
                    opt("[[keep]]MUST[[/keep]]"),
                    opt("[[keep]]MUST NOT[[/keep]]"),
                    opt("[[keep]]MAY[[/keep]]"),
                ),
                "SHOULD = recommended with allowed exceptions, which fits a retry guideline.",
            ),
        ),
        'Tech idioms & phrasal verbs ("spin up", "roll back", "ship it")': (
            q(
                "What does the phrasal verb [[keep]]roll back[[/keep]] mean?",
                (
                    opt("return to a previous version", correct=True),
                    opt("release gradually to users"),
                    opt("start a new server"),
                    opt("split a task into smaller parts"),
                ),
                "'roll back' = revert to a previous version; 'roll out' = release gradually.",
            ),
            q(
                'What does the idiom [[keep]]"Let\'s not reinvent the wheel"[[/keep]] mean?',
                (
                    opt("don't rebuild something that already exists", correct=True),
                    opt("let's redesign the whole system"),
                    opt("let's buy new hardware"),
                    opt("let's roll back the release"),
                ),
                "It advises reusing an existing solution instead of building one from scratch.",
            ),
            q(
                "With a pronoun, which word order is correct?",
                (
                    opt('[[keep]]"roll it back"[[/keep]]', correct=True),
                    opt('[[keep]]"roll back it"[[/keep]]'),
                    opt('[[keep]]"back roll it"[[/keep]]'),
                    opt('[[keep]]"it roll back"[[/keep]]'),
                ),
                "A pronoun must go between the verb and particle: 'roll it back'.",
            ),
        ),
        "Technical interview English (system design + behavioral)": (
            q(
                "In a system-design interview, what should you usually do first?",
                (
                    opt(
                        'clarify, e.g. [[keep]]"Can I ask a few questions about the '
                        'requirements?"[[/keep]]',
                        correct=True,
                    ),
                    opt("immediately start drawing the database"),
                    opt("give the final answer in one sentence"),
                    opt("say you need more time and stop"),
                ),
                "Clarifying requirements before designing shows structured thinking.",
            ),
            q(
                "What do the letters in the [[keep]]STAR[[/keep]] method stand for?",
                (
                    opt("[[keep]]Situation, Task, Action, Result[[/keep]]", correct=True),
                    opt("[[keep]]System, Test, API, Release[[/keep]]"),
                    opt("[[keep]]Story, Topic, Answer, Reason[[/keep]]"),
                    opt("[[keep]]Start, Try, Adjust, Repeat[[/keep]]"),
                ),
                "STAR = Situation, Task, Action, Result — a structure for behavioral answers.",
            ),
            q(
                "How can you politely buy thinking time in an interview?",
                (
                    opt(
                        '[[keep]]"That\'s a good question. Let me think for a moment."[[/keep]]',
                        correct=True,
                    ),
                    opt("stay completely silent for a minute"),
                    opt('[[keep]]"I have no idea."[[/keep]]'),
                    opt("change the subject"),
                ),
                "A short phrase like 'Let me think for a moment' buys time without awkward silence.",
            ),
        ),
    },
    final=(
        q(
            "Which word describes how tightly two components depend on each other?",
            (
                opt("[[keep]]coupling[[/keep]]", correct=True),
                opt("[[keep]]scalability[[/keep]]"),
                opt("[[keep]]a layer[[/keep]]"),
                opt("[[keep]]a bottleneck[[/keep]]"),
            ),
            "Coupling measures how tightly parts depend on each other; loose coupling is usually preferred.",
        ),
        q(
            "Which is a good signpost phrase for closing a presentation?",
            (
                opt('[[keep]]"To sum up,"[[/keep]]', correct=True),
                opt('[[keep]]"First, let me give you some context."[[/keep]]'),
                opt('[[keep]]"Now let\'s move on to the demo."[[/keep]]'),
                opt('[[keep]]"Let me give you some background."[[/keep]]'),
            ),
            "'To sum up' / 'To wrap up' signals the closing summary.",
        ),
        q(
            "Which sentence disagrees most diplomatically?",
            (
                opt(
                    "[[keep]]\"That's a fair point. That said, I think there's a simpler "
                    'option."[[/keep]]',
                    correct=True,
                ),
                opt('[[keep]]"That\'s wrong."[[/keep]]'),
                opt('[[keep]]"I don\'t like it."[[/keep]]'),
                opt('[[keep]]"No."[[/keep]]'),
            ),
            "Acknowledging first ('That's a fair point') before 'that said' softens the disagreement.",
        ),
        q(
            "Choose the correct keyword for an absolute prohibition in a spec: "
            '"The API ___ store passwords in plain text."',
            (
                opt("[[keep]]MUST NOT[[/keep]]", correct=True),
                opt("[[keep]]SHOULD[[/keep]]"),
                opt("[[keep]]MAY[[/keep]]"),
                opt("[[keep]]MIGHT[[/keep]]"),
            ),
            "MUST NOT is an absolute prohibition, which fits a security rule.",
        ),
        q(
            "What does the phrasal verb [[keep]]spin up[[/keep]] mean?",
            (
                opt("start a new server or service", correct=True),
                opt("shut a service down"),
                opt("return to a previous version"),
                opt("investigate a bug"),
            ),
            "'spin up' means to start a new server/service; 'look into' means to investigate.",
        ),
        q(
            "Best way to answer a behavioral question with a clear structure:",
            (
                opt("use the [[keep]]STAR[[/keep]] method and the past tense", correct=True),
                opt("describe the whole company history"),
                opt("answer only 'yes' or 'no'"),
                opt("talk about future plans only"),
            ),
            "STAR (Situation, Task, Action, Result) gives a structured, concrete answer in the past tense.",
        ),
    ),
)
