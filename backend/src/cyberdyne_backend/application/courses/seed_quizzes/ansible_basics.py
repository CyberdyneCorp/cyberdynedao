"""Curated quiz questions for the Ansible - Basics course (per-lesson
checkpoints plus a final comprehensive quiz). Keys are the EXACT content-lesson
titles so the seed can interleave each checkpoint after its lesson."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is Ansible?": (
            q(
                "What is Ansible's big selling point compared to other configuration tools?",
                (
                    opt("It compiles configuration into a binary agent"),
                    opt(
                        "It is agentless and connects over plain SSH so nothing is installed on managed hosts",
                        correct=True,
                    ),
                    opt("It requires a proprietary daemon on every server"),
                    opt("It only works on a single machine at a time"),
                ),
                "Ansible is agentless: it connects over plain SSH (WinRM on Windows), so there is nothing to install on the managed hosts.",
            ),
            q(
                "What does it mean that Ansible aims to be idempotent?",
                (
                    opt("Running a playbook always recreates every resource from scratch"),
                    opt("Playbooks can only ever be run once safely"),
                    opt(
                        "Running a playbook twice leaves the system in the same state, changing only what is not already correct",
                        correct=True,
                    ),
                    opt("Each run randomly reorders the tasks it performs"),
                ),
                "Idempotent means running a playbook twice leaves the same state; it only changes what is not already correct.",
            ),
            q(
                "Besides SSH connectivity, what do managed nodes need according to the lesson?",
                (
                    opt("Python", correct=True),
                    opt("A running Ansible agent daemon"),
                    opt("A graphical desktop environment"),
                    opt("Docker installed and running"),
                ),
                "Managed nodes just need SSH plus Python; the control node pushes changes out over SSH.",
            ),
        ),
        "Playbooks & modules": (
            q(
                "In a playbook, what does each task call to do the actual unit of work?",
                (
                    opt("A play"),
                    opt("A module", correct=True),
                    opt("An inventory"),
                    opt("A handler"),
                ),
                "A playbook is YAML of plays, each running tasks, and each task calls a module which is the unit of work.",
            ),
            q(
                "What does adding become: true to a play do?",
                (
                    opt("Runs the tasks with sudo", correct=True),
                    opt("Skips any task that would change the system"),
                    opt("Switches the connection from SSH to WinRM"),
                    opt("Gathers facts about the host"),
                ),
                "become: true runs the play's tasks with sudo (privilege escalation).",
            ),
            q(
                "When a module like apt with state: present finds the package already installed, what does the task report?",
                (
                    opt("failed"),
                    opt("changed"),
                    opt("ok", correct=True),
                    opt("skipped"),
                ),
                "Declarative state such as present or started is idempotent, so already-installed or running tasks report ok, not changed.",
            ),
        ),
        "Inventory & ad-hoc commands": (
            q(
                "What does the inventory describe?",
                (
                    opt("The hosts you manage, organised into groups", correct=True),
                    opt("The list of modules available to Ansible"),
                    opt("The SSH keys used to authenticate"),
                    opt("The order in which tasks run within a play"),
                ),
                "The inventory lists the hosts you manage, organised into groups that playbooks target via hosts:.",
            ),
            q(
                "When would you use an ad-hoc command instead of a playbook?",
                (
                    opt("For complex deployments you will repeat often"),
                    opt("For one-off actions where you run a module directly", correct=True),
                    opt("Only when there is no SSH access to the host"),
                    opt("Whenever you need privilege escalation"),
                ),
                "Ad-hoc commands run a module directly for one-off actions; you write playbooks for anything you will repeat.",
            ),
            q(
                "In an ad-hoc command, what do the -m and -a flags do?",
                (
                    opt("-m sets the host group and -a sets the inventory file"),
                    opt("-m picks the module and -a passes its arguments", correct=True),
                    opt("-m enables become and -a runs the task asynchronously"),
                    opt("-m marks the run as idempotent and -a as ad-hoc"),
                ),
                "In an ad-hoc command, -m picks the module and -a passes arguments to it.",
            ),
        ),
    },
    final=(
        q(
            "Which statement best captures how Ansible reaches and changes managed nodes?",
            (
                opt("It installs a persistent agent on each node ahead of time"),
                opt(
                    "A control node pushes changes over SSH; managed nodes need only SSH and Python",
                    correct=True,
                ),
                opt("It polls a central server that nodes check into every minute"),
                opt("It rewrites the kernel on each managed host"),
            ),
            "Ansible is agentless: a control node pushes changes over SSH, and managed nodes need only SSH plus Python.",
        ),
        q(
            "What is the relationship between playbooks, plays, tasks, and modules?",
            (
                opt("A module contains plays, which contain playbooks of tasks"),
                opt(
                    "A playbook is YAML of plays; each play runs tasks on hosts, and each task calls a module",
                    correct=True,
                ),
                opt("A task is a group of playbooks run on one host"),
                opt("Modules are inventories that list the hosts to manage"),
            ),
            "A playbook is a YAML file of plays, each running a list of tasks on a set of hosts, and each task calls a module.",
        ),
        q(
            "Why does running the same idempotent playbook twice usually report ok rather than changed on the second run?",
            (
                opt("Ansible caches the first run and skips everything afterward"),
                opt("The second run silently fails without reporting"),
                opt(
                    "Declarative modules only change what is not already in the desired state",
                    correct=True,
                ),
                opt("Tasks are randomised so duplicates are dropped"),
            ),
            "Modules are declarative and idempotent, so already-correct state reports ok and only divergent state is changed.",
        ),
        q(
            "How does a playbook decide which hosts a play runs against?",
            (
                opt("It runs on every host in the inventory regardless of grouping"),
                opt(
                    "It targets an inventory group via the hosts: key, such as hosts: web",
                    correct=True,
                ),
                opt("It uses the -m flag to select the host group"),
                opt("It connects only to the control node itself"),
            ),
            "Inventory organises hosts into groups, and a play targets a group via the hosts: key (for example hosts: web).",
        ),
        q(
            "For a quick one-off connectivity check across all hosts without writing a playbook, which approach fits?",
            (
                opt("Write and run a full site.yml playbook"),
                opt("Encrypt the inventory before connecting"),
                opt(
                    "Run an ad-hoc command such as ansible all -i inventory.ini -m ping",
                    correct=True,
                ),
                opt("Install an agent on each host first"),
            ),
            "Ad-hoc commands suit quick one-off actions; ansible all -m ping is the connectivity check shown in the lesson.",
        ),
    ),
)
