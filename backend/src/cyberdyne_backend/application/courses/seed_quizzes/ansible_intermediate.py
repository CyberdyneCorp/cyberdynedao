"""Curated quiz questions for the Ansible - Intermediate course (per-lesson
checkpoints keyed by exact content-lesson title, plus a final comprehensive
quiz). Kept beside the course module so the seed stays readable."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Variables, facts & templates": (
            q(
                "What does the syntax {{ app_port }} represent inside an Ansible play?",
                (
                    opt("A shell environment variable expansion"),
                    opt("A Jinja2 expression that substitutes the variable value", correct=True),
                    opt("A reserved keyword that must never be quoted"),
                    opt("A comment that Ansible ignores at run time"),
                ),
                "The lesson states that {{ }} is Jinja2, used to substitute the value of a variable.",
            ),
            q(
                "What are Ansible facts as described in the lesson?",
                (
                    opt(
                        "Auto-gathered details about each host such as OS, IP, and CPU",
                        correct=True,
                    ),
                    opt("Manually written assertions that a play must satisfy"),
                    opt("Encrypted secrets stored in an external vault"),
                    opt("Default variables that live in the defaults directory"),
                ),
                "Ansible auto-gathers facts about each host such as OS, IP, and CPU, usable in conditionals and templates.",
            ),
            q(
                "What does the template module do?",
                (
                    opt("Installs a package and starts its service"),
                    opt(
                        "Renders a .j2 file with variables and copies it to the host", correct=True
                    ),
                    opt("Encrypts a configuration file before committing it to git"),
                    opt("Gathers facts from the managed host"),
                ),
                "The lesson says the template module renders a .j2 file with variables and copies it to the host.",
            ),
        ),
        "Roles": (
            q(
                "What is a role in Ansible?",
                (
                    opt("A single task that must run before any play begins"),
                    opt(
                        "A package of tasks, variables, templates, files, and handlers in a standard layout",
                        correct=True,
                    ),
                    opt("A user account that defines who can run a playbook"),
                    opt("An encrypted file holding the playbook secrets"),
                ),
                "A role packages tasks, variables, templates, files, and handlers into a reusable, standard directory layout.",
            ),
            q(
                "Which directory inside a role holds overridable default variables?",
                (
                    opt("tasks/"),
                    opt("handlers/"),
                    opt("defaults/", correct=True),
                    opt("templates/"),
                ),
                "The lesson states that defaults/ holds overridable defaults while tasks/main.yml is the entry point.",
            ),
            q(
                "How do you share and reuse community roles according to the lesson?",
                (
                    opt("Through Ansible Galaxy using ansible-galaxy role install", correct=True),
                    opt("By copying the role files manually over SSH"),
                    opt("By encrypting them with ansible-vault first"),
                    opt("By committing them to the defaults directory"),
                ),
                "The lesson shows ansible-galaxy role install to share and reuse community roles via Ansible Galaxy.",
            ),
        ),
        "Conditionals, loops & handlers": (
            q(
                "Which keyword runs a task only when a condition is met?",
                (
                    opt("loop"),
                    opt("when", correct=True),
                    opt("notify"),
                    opt("rescue"),
                ),
                "The when keyword runs tasks conditionally, for example when ansible_facts os_family equals Debian.",
            ),
            q(
                "What is special about how a handler runs?",
                (
                    opt("It runs before every task in the play"),
                    opt("It runs once, at the end, only if it was notified", correct=True),
                    opt("It runs in parallel on every host immediately"),
                    opt("It runs only when the playbook is started with --check"),
                ),
                "Handlers run once, at the end, and only if a task notified them.",
            ),
            q(
                "What is the purpose of a block / rescue construct?",
                (
                    opt("To repeat a task over a list of items"),
                    opt(
                        "To handle errors by running rescue tasks when the block fails",
                        correct=True,
                    ),
                    opt("To delay a task until a handler is notified"),
                    opt("To encrypt the variables used inside the block"),
                ),
                "block / rescue is for error handling: rescue tasks run when the block fails, for example to roll back.",
            ),
        ),
    },
    final=(
        q(
            "Where can variables be defined or supplied for a play?",
            (
                opt("Only inside the template files themselves"),
                opt("In the play, in group_vars/, host_vars/, or passed with -e", correct=True),
                opt("Only through Ansible Galaxy"),
                opt("Only inside a handler definition"),
            ),
            "The lesson lists defining variables in the play, in group_vars/, host_vars/, or passing them with -e.",
        ),
        q(
            "Which keyword on a task triggers a handler such as restart nginx?",
            (
                opt("when"),
                opt("loop"),
                opt("notify", correct=True),
                opt("become"),
            ),
            "A task uses notify to trigger a handler, for example notify restart nginx after deploying a config.",
        ),
        q(
            "What does the loop keyword do in a task?",
            (
                opt("Repeats the task once for each item in a list", correct=True),
                opt("Runs the task only when a condition is true"),
                opt("Renders a Jinja2 template to the host"),
                opt("Encrypts each item before use"),
            ),
            "loop repeats a task, for example creating each user in the list ada, bob, cara.",
        ),
        q(
            "What is the benefit of packaging automation into roles?",
            (
                opt(
                    "They keep playbooks short and make automation composable across projects",
                    correct=True,
                ),
                opt("They remove the need to gather facts on hosts"),
                opt("They encrypt all variables automatically"),
                opt("They force every task to run in lockstep"),
            ),
            "Roles keep playbooks short and make automation composable and reusable across projects.",
        ),
        q(
            "How can you run only part of a playbook?",
            (
                opt("By using tags, for example --tags deploy", correct=True),
                opt("By removing the handlers section"),
                opt("By encrypting the unwanted tasks with vault"),
                opt("By setting loop to an empty list"),
            ),
            "The lesson notes that tags let you run only part of a playbook, for example --tags deploy.",
        ),
    ),
)
