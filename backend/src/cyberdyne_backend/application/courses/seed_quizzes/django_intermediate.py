"""Quizzes for the Django — Intermediate course (per-lesson checkpoints + final)."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Forms & validation": (
            q(
                "What is the advantage of `forms.ModelForm` over `forms.Form`?",
                (
                    opt("It renders without any HTML"),
                    opt(
                        "It builds its fields automatically from a model and can `save()` rows",
                        correct=True,
                    ),
                    opt("It skips all validation"),
                    opt("It only works inside the admin"),
                ),
                "A `ModelForm` derives its fields from a model's `Meta.fields` and provides `save()` "
                "to write the row, removing boilerplate.",
            ),
            q(
                "Where do you put validation for a single field named `title`?",
                (
                    opt("In a method called `validate_title`"),
                    opt(
                        "In a method called `clean_title` that returns the cleaned value",
                        correct=True,
                    ),
                    opt("In the model's `__str__`"),
                    opt("In `settings.py`"),
                ),
                "A `clean_<field>` method (here `clean_title`) validates one field and must return "
                "the cleaned value; `clean()` validates across fields.",
            ),
            q(
                "Why redirect after a successful POST (POST-redirect-GET)?",
                (
                    opt("It is faster than rendering"),
                    opt(
                        "It prevents the browser re-submitting the form on refresh",
                        correct=True,
                    ),
                    opt("It is required to call `form.save()`"),
                    opt("It disables CSRF protection"),
                ),
                "Redirecting after a successful POST means a refresh re-requests the redirect target, "
                "not the form submission, avoiding duplicate writes.",
            ),
        ),
        "Class-based views": (
            q(
                "What does `ListView` handle for you?",
                (
                    opt("Only URL routing"),
                    opt("The query, pagination, and context for a list of objects", correct=True),
                    opt("Database migrations"),
                    opt("Password hashing"),
                ),
                "`ListView` runs the queryset, paginates it, and supplies the object list to the "
                "template context.",
            ),
            q(
                "Why use `reverse_lazy` (not `reverse`) for a CBV's `success_url`?",
                (
                    opt("It is shorter to type"),
                    opt(
                        "URLs are not yet loaded when the class body is evaluated at import time",
                        correct=True,
                    ),
                    opt("`reverse` does not exist in Django"),
                    opt("It encrypts the URL"),
                ),
                "Class attributes are evaluated at import time, before the URLconf is ready, so "
                "`reverse_lazy` defers resolution until the URL is actually needed.",
            ),
            q(
                "How is a class-based view connected to a URL pattern?",
                (
                    opt('`path("", views.ArticleListView)`'),
                    opt('`path("", views.ArticleListView.as_view())`', correct=True),
                    opt('`path("", register(ArticleListView))`'),
                    opt('`path("", ArticleListView.render())`'),
                ),
                "CBVs are wired with `.as_view()`, which returns a callable that the URL resolver "
                "can invoke per request.",
            ),
        ),
        "QuerySets & relationships": (
            q(
                "What does it mean that QuerySets are 'lazy'?",
                (
                    opt("They cache the entire database in memory"),
                    opt(
                        "No query runs until the QuerySet is iterated, sliced, or evaluated",
                        correct=True,
                    ),
                    opt("They always run on a background thread"),
                    opt("They can only be used once"),
                ),
                "A QuerySet builds a query but does not hit the database until you evaluate it "
                "(iterate, slice, call `list()`, etc.).",
            ),
            q(
                'What does `Article.objects.filter(author__email__endswith=".org")` show about '
                "the double underscore?",
                (
                    opt("It only ever negates a condition"),
                    opt(
                        "It both spans relationships (`author__email`) and selects a lookup "
                        "(`__endswith`)",
                        correct=True,
                    ),
                    opt("It joins two separate querysets"),
                    opt("It is a typo for a single dot"),
                ),
                "`__` traverses relations (`author__email`) and also names field lookups "
                "(`__endswith`, `__icontains`, `__gte`).",
            ),
            q(
                "Which tool lets you build an OR condition in a filter?",
                (
                    opt("`F` expressions"),
                    opt("`Q` objects, e.g. `filter(Q(a) | Q(b))`", correct=True),
                    opt("`annotate`"),
                    opt("`select_related`"),
                ),
                "`Q` objects combine with `|` (OR), `&` (AND), and `~` (NOT) to build complex "
                "filter conditions.",
            ),
        ),
        "Authentication & users": (
            q(
                "Why must you use `create_user` / `set_password` rather than assigning to "
                "`password` directly?",
                (
                    opt("They are shorter to type"),
                    opt("They hash the password instead of storing it in plain text", correct=True),
                    opt("They send a confirmation email"),
                    opt("They are required to create a username"),
                ),
                "`create_user`/`set_password` run the configured password hasher; assigning to "
                "`password` directly would store the raw string.",
            ),
            q(
                "What does the `@login_required` decorator do?",
                (
                    opt("Grants every permission to the user"),
                    opt("Redirects unauthenticated users to the login page", correct=True),
                    opt("Logs the user out after the view runs"),
                    opt("Creates a new user automatically"),
                ),
                "`@login_required` blocks anonymous users, redirecting them to the login URL before "
                "the view runs.",
            ),
            q(
                "Which mixin enforces login on a class-based view?",
                (
                    opt("`ListView`"),
                    opt("`LoginRequiredMixin`", correct=True),
                    opt("`ModelForm`"),
                    opt("`CsrfViewMiddleware`"),
                ),
                "`LoginRequiredMixin` (placed before the generic view base) enforces authentication "
                "on a CBV, the class equivalent of `@login_required`.",
            ),
        ),
        "Migrations in depth": (
            q(
                "What does a migration's `dependencies` list express?",
                (
                    opt("The Python packages it imports"),
                    opt("The migrations that must be applied before it", correct=True),
                    opt("The templates it renders"),
                    opt("The URLs it registers"),
                ),
                "`dependencies` declares the prior migrations (in this or other apps) that must run "
                "first, forming an ordered graph.",
            ),
            q(
                'Inside a data migration, why use `apps.get_model("blog", "Article")` instead '
                "of importing the model?",
                (
                    opt("It is faster"),
                    opt(
                        "It returns the model as it existed at that point in history, matching the "
                        "schema",
                        correct=True,
                    ),
                    opt("Imports are forbidden in migrations"),
                    opt("It avoids hashing the password"),
                ),
                "Historical models from `apps.get_model` match the schema at that migration, so data "
                "migrations stay correct even as the current model changes.",
            ),
            q(
                "What is the rule about an already-applied migration?",
                (
                    opt("Edit it freely whenever the model changes"),
                    opt("Never edit it; generate a new migration instead", correct=True),
                    opt("Delete it after applying"),
                    opt("Rename it to mark it as done"),
                ),
                "Editing an applied migration desynchronises history across environments; create a "
                "new migration to make further changes.",
            ),
        ),
        "Settings, static & media files": (
            q(
                "What is the difference between static files and media files?",
                (
                    opt("Static files are uploaded by users; media files ship with code"),
                    opt(
                        "Static files ship with your code; media files are uploaded by users at "
                        "runtime",
                        correct=True,
                    ),
                    opt("They are the same thing"),
                    opt("Media files are only CSS and JS"),
                ),
                "Static files (CSS/JS/images) are authored and ship with the code; media files are "
                "user uploads stored at runtime under `MEDIA_ROOT`.",
            ),
            q(
                "What does `python manage.py collectstatic` do?",
                (
                    opt("Deletes all uploaded media"),
                    opt(
                        "Gathers all static files into `STATIC_ROOT` for serving in production",
                        correct=True,
                    ),
                    opt("Compiles templates to HTML"),
                    opt("Applies database migrations"),
                ),
                "`collectstatic` copies every app's static files into `STATIC_ROOT`, where a web "
                "server or CDN serves them in production.",
            ),
            q(
                "Where should secrets like `SECRET_KEY` and DB passwords be stored?",
                (
                    opt("Hard-coded in settings.py committed to git"),
                    opt("In environment variables, kept out of source control", correct=True),
                    opt("In a public README"),
                    opt("In the template files"),
                ),
                "Secrets belong in environment variables (or a secrets manager), never committed in "
                "`settings.py`, so the same code runs safely everywhere.",
            ),
        ),
    },
    final=(
        q(
            "Which form method validates across multiple fields at once?",
            (
                opt("`clean_<field>`"),
                opt("`clean()`", correct=True),
                opt("`save()`"),
                opt("`is_bound()`"),
            ),
            "A `clean_<field>` method validates one field; an overall `clean()` method validates "
            "relationships between fields.",
        ),
        q(
            "Which generic view both shows a form on GET and validates/saves on POST?",
            (
                opt("`ListView`"),
                opt("`CreateView`", correct=True),
                opt("`DetailView`"),
                opt("`TemplateView`"),
            ),
            "`CreateView` (and `UpdateView`) build a ModelForm and handle GET (display) and POST "
            "(validate and save) for you.",
        ),
        q(
            'What is the result of `Article.objects.filter(title__icontains="django")`?',
            (
                opt("An exact, case-sensitive match on the whole title"),
                opt("A case-insensitive substring match on title", correct=True),
                opt("A delete of matching rows"),
                opt("An OR across two fields"),
            ),
            "`__icontains` is a case-insensitive substring (LIKE) lookup, matching any title "
            "containing 'django'.",
        ),
        q(
            "How do you check whether a user has a specific permission?",
            (
                opt("`user.is_staff`"),
                opt('`user.has_perm("blog.change_article")`', correct=True),
                opt("`user.check_password(...)`"),
                opt("`user.groups.all()`"),
            ),
            '`has_perm("app.codename")` returns whether the user holds that permission, directly or '
            "via a group.",
        ),
        q(
            "Which migration operation runs Python code, e.g. to backfill data?",
            (
                opt("`AddField`"),
                opt("`RunPython`", correct=True),
                opt("`AlterModelOptions`"),
                opt("`DeleteModel`"),
            ),
            "`migrations.RunPython` runs a Python function (a data migration), typically using "
            "historical models from `apps.get_model`.",
        ),
        q(
            "In templates, how do you reference a static file path?",
            (
                opt("`{% media 'css/site.css' %}`"),
                opt("`{% load static %}` then `{% static 'css/site.css' %}`", correct=True),
                opt("`{{ STATIC_ROOT }}/css/site.css`"),
                opt("`{% collectstatic 'css/site.css' %}`"),
            ),
            "Load the static tag library, then use `{% static 'path' %}` to build the correct URL "
            "for a static asset.",
        ),
    ),
)
