"""Quizzes for the Django — Basics course (per-lesson checkpoints + a final)."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is Django & the MTV pattern": (
            q(
                "In Django's MTV pattern, what does the View do?",
                (
                    opt("Defines the database tables and business rules"),
                    opt(
                        "Receives the request, talks to models, and returns a response",
                        correct=True,
                    ),
                    opt("Holds the HTML markup with placeholders"),
                    opt("Maps URLs to handlers"),
                ),
                "In MTV the View is the glue: it handles the request, queries models, and returns a "
                "response (often a rendered template). Models hold data, Templates hold HTML.",
            ),
            q(
                "Which Django letter corresponds to the 'Controller' of classic MVC?",
                (
                    opt("Model"),
                    opt("Template"),
                    opt("View", correct=True),
                    opt("Migration"),
                ),
                "Django's View plays the role MVC calls the controller; Django's 'template' is MVC's "
                "view. The naming differs, the responsibilities are the same.",
            ),
            q(
                "What security protections does Django give you out of the box?",
                (
                    opt("Only CSS minification"),
                    opt(
                        "CSRF protection, SQL-injection-safe queries, and password hashing",
                        correct=True,
                    ),
                    opt("Automatic load balancing across servers"),
                    opt("Nothing; security is entirely manual"),
                ),
                "Django's 'batteries included' philosophy ships CSRF protection, an ORM that "
                "parameterises queries, and salted password hashing by default.",
            ),
        ),
        "Project & app structure": (
            q(
                "What is the relationship between a Django project and an app?",
                (
                    opt("An app contains many projects"),
                    opt(
                        "A project is the whole site; an app is a focused module within it",
                        correct=True,
                    ),
                    opt("They are two words for the same thing"),
                    opt("A project can contain only one app"),
                ),
                "A project is the entire site and can contain many apps; each app is a reusable, "
                "single-purpose module such as `blog` or `accounts`.",
            ),
            q(
                "Which command creates a new app called `blog`?",
                (
                    opt("`django-admin startproject blog`"),
                    opt("`python manage.py startapp blog`", correct=True),
                    opt("`python manage.py runserver blog`"),
                    opt("`python manage.py migrate blog`"),
                ),
                "`startapp` scaffolds an app; `startproject` scaffolds the project. `runserver` and "
                "`migrate` do unrelated jobs.",
            ),
            q(
                "Until you do what, will a new app not be active in the project?",
                (
                    opt("Run `collectstatic`"),
                    opt("Add it to `INSTALLED_APPS` in settings.py", correct=True),
                    opt("Create a superuser"),
                    opt("Delete its migrations folder"),
                ),
                "An app only becomes active once its name is listed in `INSTALLED_APPS`. Until then "
                "Django ignores its models, templates, and admin registrations.",
            ),
        ),
        "Models & the ORM": (
            q(
                "What does a Django model class map to?",
                (
                    opt("A URL route"),
                    opt("A database table, with each attribute a column", correct=True),
                    opt("An HTML template"),
                    opt("A middleware layer"),
                ),
                "A model is a Python class that maps to a database table; each field attribute "
                "becomes a column.",
            ),
            q(
                "What do `makemigrations` and `migrate` each do?",
                (
                    opt("`makemigrations` applies changes; `migrate` records them"),
                    opt(
                        "`makemigrations` records what changed; `migrate` applies it to the database",
                        correct=True,
                    ),
                    opt("Both create the database from scratch every time"),
                    opt("Both only print SQL without changing anything"),
                ),
                "`makemigrations` detects model changes and writes migration files; `migrate` runs "
                "those files against the actual database.",
            ),
            q(
                'Given `author = models.ForeignKey(Author, related_name="articles")`, how do you '
                "get all of an author's articles?",
                (
                    opt("`author.article_set_all()`"),
                    opt("`author.articles.all()`", correct=True),
                    opt("`Author.articles(author)`"),
                    opt('`author.foreignkey("articles")`'),
                ),
                '`related_name="articles"` names the reverse relation, so `author.articles.all()` '
                "returns that author's articles.",
            ),
        ),
        "Views & URL routing": (
            q(
                "What must a Django view return?",
                (
                    opt("A model instance"),
                    opt("An HttpResponse (e.g. via `render`)", correct=True),
                    opt("A migration file"),
                    opt("A settings dict"),
                ),
                "A view takes an `HttpRequest` and must return an `HttpResponse`; `render(...)` "
                "produces one from a template and context.",
            ),
            q(
                'In `path("<int:pk>/", views.article_detail)`, what does `<int:pk>` do?',
                (
                    opt("Declares a template block named pk"),
                    opt(
                        "Matches an integer in the URL and passes it to the view as `pk`",
                        correct=True,
                    ),
                    opt("Limits the view to POST requests"),
                    opt("Registers the view in the admin"),
                ),
                "`<int:pk>` is a path converter: it matches an integer segment and passes it to the "
                "view as the keyword argument `pk`.",
            ),
            q(
                'Why use `reverse("blog:detail", ...)` instead of hard-coding `/articles/5/`?',
                (
                    opt("It is faster at runtime"),
                    opt(
                        "URLs can change structure without breaking links built by name",
                        correct=True,
                    ),
                    opt("Hard-coded URLs are forbidden by Python"),
                    opt("`reverse` automatically logs the user in"),
                ),
                "Reversing by name decouples links from the URL structure, so you can change the "
                "paths later without editing every view and template.",
            ),
        ),
        "Templates": (
            q(
                "Which template feature lets a child template reuse a shared header and footer?",
                (
                    opt("`{% include %}` only"),
                    opt("Template inheritance via `{% extends %}` and `{% block %}`", correct=True),
                    opt("The `safe` filter"),
                    opt("Path converters"),
                ),
                "A base template defines `{% block %}`s and child templates `{% extends %}` it, "
                "overriding those blocks - the core of template inheritance.",
            ),
            q(
                "What is the syntax to output a variable's value in a Django template?",
                (
                    opt("`{% article.title %}`"),
                    opt("`{{ article.title }}`", correct=True),
                    opt("`${article.title}`"),
                    opt("`<article.title>`"),
                ),
                "Double curly braces `{{ ... }}` print a variable; `{% ... %}` is for tags (logic) "
                "like loops and conditionals.",
            ),
            q(
                "Why is `{{ user_input }}` safe against XSS by default?",
                (
                    opt("Django blocks all POST requests"),
                    opt("The template language auto-escapes variable output", correct=True),
                    opt("Variables are rendered server-side only"),
                    opt("The `safe` filter is applied automatically"),
                ),
                "The Django template language auto-escapes variables, so HTML in user input is "
                "rendered harmless unless you explicitly mark it `safe`.",
            ),
        ),
        "The admin site": (
            q(
                "What do you get by calling `admin.site.register(Article)`?",
                (
                    opt("A REST API for Article"),
                    opt(
                        "Auto-generated list, add, edit, and delete pages for Article", correct=True
                    ),
                    opt("A new database migration"),
                    opt("A public-facing detail page"),
                ),
                "Registering a model gives it a full CRUD interface in the admin - list, add, edit, "
                "and delete - with no custom HTML.",
            ),
            q(
                "Which `ModelAdmin` option controls the columns shown in the change list?",
                (
                    opt("`search_fields`"),
                    opt("`list_display`", correct=True),
                    opt("`list_filter`"),
                    opt("`ordering`"),
                ),
                "`list_display` sets the columns; `list_filter` adds the sidebar filters, "
                "`search_fields` adds the search box, and `ordering` sets the default sort.",
            ),
            q(
                "Who is the Django admin intended for?",
                (
                    opt("End users / the general public"),
                    opt("Trusted staff doing back-office work", correct=True),
                    opt("Search engine crawlers"),
                    opt("Automated API clients"),
                ),
                "The admin exposes your data model directly and is meant for trusted staff. Build "
                "separate, permission-scoped views for the public.",
            ),
        ),
    },
    final=(
        q(
            "What does the M, T, and V stand for in Django's MTV?",
            (
                opt("Module, Test, Validation"),
                opt("Model, Template, View", correct=True),
                opt("Migration, Tag, ViewSet"),
                opt("Middleware, Template, Variable"),
            ),
            "MTV is Model (data), Template (presentation), View (request handling) - Django's take "
            "on classic MVC.",
        ),
        q(
            "Which command applies pending schema changes to the database?",
            (
                opt("`python manage.py makemigrations`"),
                opt("`python manage.py migrate`", correct=True),
                opt("`python manage.py runserver`"),
                opt("`python manage.py collectstatic`"),
            ),
            "`migrate` applies migration files to the database; `makemigrations` only generates "
            "them from model changes.",
        ),
        q(
            "How does the root URLconf hand a path off to an app's own urls.py?",
            (
                opt("With `register()`"),
                opt('With `path("articles/", include("blog.urls"))`', correct=True),
                opt("By importing the app's views directly into settings.py"),
                opt("Automatically, with no configuration"),
            ),
            '`include("blog.urls")` delegates matching paths to the app\'s URLconf, keeping routing '
            "modular.",
        ),
        q(
            "What does `get_object_or_404(Article, pk=5)` do when no row matches?",
            (
                opt("Returns None silently"),
                opt("Raises Http404, producing a clean 404 response", correct=True),
                opt("Creates a new Article"),
                opt("Raises a 500 server error"),
            ),
            "`get_object_or_404` fetches the row or raises `Http404`, which Django turns into a "
            "proper 404 page.",
        ),
        q(
            "Which template tag is required inside a POST form?",
            (
                opt("`{% load static %}`"),
                opt("`{% csrf_token %}`", correct=True),
                opt("`{% block content %}`"),
                opt("`{% url %}`"),
            ),
            "Django rejects POST forms that lack `{% csrf_token %}`, protecting against cross-site "
            "request forgery.",
        ),
        q(
            "Why should every model define a `__str__` method?",
            (
                opt("It is required or the model will not save"),
                opt(
                    "It controls how the object displays in the admin and shell",
                    correct=True,
                ),
                opt("It creates the database table"),
                opt("It registers the model with the URL router"),
            ),
            "`__str__` gives a readable representation, turning 'Article object (5)' into the "
            "actual title in the admin and the shell.",
        ),
    ),
)
