"""Quizzes for the Django — Advanced course (per-lesson checkpoints + a final)."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Django REST Framework": (
            q(
                "What is the role of a DRF serializer?",
                (
                    opt("It routes URLs to viewsets"),
                    opt(
                        "It converts model instances to JSON and validates incoming JSON",
                        correct=True,
                    ),
                    opt("It applies database migrations"),
                    opt("It renders HTML templates"),
                ),
                "A serializer is the API analogue of a form: it serialises model instances to JSON "
                "and validates/deserialises request data.",
            ),
            q(
                "What does registering a `ModelViewSet` with a router generate?",
                (
                    opt("A single read-only endpoint"),
                    opt(
                        "Full CRUD routes (list/create/retrieve/update/destroy) automatically",
                        correct=True,
                    ),
                    opt("A new database table"),
                    opt("An admin registration"),
                ),
                "A `DefaultRouter` turns one `register(...)` call into the full set of list, create, "
                "retrieve, update, and destroy URLs.",
            ),
            q(
                "Why set `permission_classes` explicitly on a ViewSet?",
                (
                    opt("It speeds up serialization"),
                    opt(
                        "To control who may read or write; the default-open API is unsafe in "
                        "production",
                        correct=True,
                    ),
                    opt("It is required for the router to work"),
                    opt("It disables CSRF for the API"),
                ),
                "Permissions like `IsAuthenticatedOrReadOnly` scope access; relying on permissive "
                "defaults exposes write access in production.",
            ),
        ),
        "Middleware & the request/response lifecycle": (
            q(
                "How does a request and response flow through the middleware stack?",
                (
                    opt("Top to bottom both ways"),
                    opt(
                        "Top to bottom on the request, then bottom to top on the response",
                        correct=True,
                    ),
                    opt("Randomly, depending on load"),
                    opt("Only the first middleware ever runs"),
                ),
                "Middleware wraps the view like an onion: the request descends the list to the view, "
                "and the response ascends back up in reverse order.",
            ),
            q(
                "In custom middleware, which code runs on the way *out* (response phase)?",
                (
                    opt("Code in `__init__`"),
                    opt("Code after the `self.get_response(request)` call", correct=True),
                    opt("Code before `self.get_response(request)`"),
                    opt("Nothing; middleware only sees requests"),
                ),
                "`get_response(request)` calls the next layer/view; code before it runs on the way "
                "in, code after it runs on the way out.",
            ),
            q(
                "Why should middleware avoid per-request database queries?",
                (
                    opt("Queries are not allowed in middleware"),
                    opt(
                        "Middleware runs on every request, so the cost is paid site-wide",
                        correct=True,
                    ),
                    opt("It would break CSRF protection"),
                    opt("Databases cannot be reached from middleware"),
                ),
                "Because every request passes through the stack, expensive middleware work multiplies "
                "across all traffic, so keep it cheap.",
            ),
        ),
        "Signals": (
            q(
                "When does a `post_save` receiver with `if created:` actually run its body?",
                (
                    opt("On every save"),
                    opt("Only when the row was just inserted for the first time", correct=True),
                    opt("Only on delete"),
                    opt("Never; `created` is always False"),
                ),
                "`created` is `True` only on the initial insert, so `if created:` guards "
                "first-time-only logic.",
            ),
            q(
                "Where do you import your signal handlers so they get connected at startup?",
                (
                    opt("In `settings.py`"),
                    opt("In the app config's `ready()` method", correct=True),
                    opt("In every template"),
                    opt("In `manage.py`"),
                ),
                "Importing the signals module in `AppConfig.ready()` registers the `@receiver` "
                "handlers once Django finishes loading apps.",
            ),
            q(
                "What is a common downside of using signals?",
                (
                    opt("They cannot be connected to model events"),
                    opt(
                        "They hide control flow, making it harder to see why something happened",
                        correct=True,
                    ),
                    opt("They run synchronously, which is always wrong"),
                    opt("They require Redis"),
                ),
                "Signals decouple sender and receiver, which obscures cause and effect; for logic "
                "that always accompanies a save, overriding `save()` is often clearer.",
            ),
        ),
        "Performance & avoiding N+1": (
            q(
                "What is the N+1 query problem?",
                (
                    opt("Running N queries in parallel"),
                    opt(
                        "One query for a list, then an extra query per item to follow a relation",
                        correct=True,
                    ),
                    opt("Caching too aggressively"),
                    opt("Indexing every column"),
                ),
                "N+1 is one query to fetch N rows plus one extra query per row when a related object "
                "is accessed in a loop.",
            ),
            q(
                "Which method fixes N+1 for a `ForeignKey` by using a SQL JOIN?",
                (
                    opt("`prefetch_related`"),
                    opt("`select_related`", correct=True),
                    opt("`annotate`"),
                    opt("`only`"),
                ),
                "`select_related` follows forward FK/OneToOne links with a JOIN in a single query; "
                "`prefetch_related` handles M2M and reverse FK with a second query.",
            ),
            q(
                "Which tool best reveals exactly which queries a page runs in development?",
                (
                    opt("`collectstatic`"),
                    opt("django-debug-toolbar", correct=True),
                    opt("`makemigrations`"),
                    opt("The `safe` template filter"),
                ),
                "django-debug-toolbar shows the per-request SQL, making N+1 patterns and slow "
                "queries obvious so you measure before optimising.",
            ),
        ),
        "Testing": (
            q(
                "How does Django's `TestCase` keep tests isolated from each other?",
                (
                    opt("It uses a separate process per test"),
                    opt(
                        "It wraps each test in a transaction that is rolled back afterward",
                        correct=True,
                    ),
                    opt("It disables the database entirely"),
                    opt("It deletes the production database between tests"),
                ),
                "`TestCase` runs each test inside a transaction and rolls it back, so the database is "
                "clean for the next test without recreating it.",
            ),
            q(
                "What does the test client let you do?",
                (
                    opt("Deploy the app to production"),
                    opt("Simulate HTTP requests to views without a running server", correct=True),
                    opt("Generate migrations"),
                    opt("Collect static files"),
                ),
                "`self.client.get(...)` / `.post(...)` exercise views and return responses you can "
                "assert on, with no live server needed.",
            ),
            q(
                "Why prefer `setUpTestData` over `setUp` for shared read-only objects?",
                (
                    opt("`setUp` does not exist"),
                    opt(
                        "`setUpTestData` creates the objects once per class, so the suite runs "
                        "faster",
                        correct=True,
                    ),
                    opt("`setUpTestData` runs after each test"),
                    opt("It disables rollback"),
                ),
                "`setUpTestData` builds shared data once at the class level (inside a transaction) "
                "rather than re-creating it before every test method.",
            ),
        ),
        "Deployment & security": (
            q(
                "Why must `DEBUG = False` in production?",
                (
                    opt("It makes the site faster only"),
                    opt(
                        "With DEBUG=True, error pages leak settings, source, and SQL to anyone",
                        correct=True,
                    ),
                    opt("It is required to run migrations"),
                    opt("It enables the admin site"),
                ),
                "`DEBUG=True` exposes detailed error pages with sensitive internals; production must "
                "use `DEBUG=False` (which then requires `ALLOWED_HOSTS`).",
            ),
            q(
                "What is the difference between WSGI and ASGI entry points?",
                (
                    opt("WSGI is for templates, ASGI is for models"),
                    opt(
                        "WSGI is the synchronous interface; ASGI is async (WebSockets, async views)",
                        correct=True,
                    ),
                    opt("They are identical"),
                    opt("ASGI only works in development"),
                ),
                "WSGI (`wsgi.py`, run by gunicorn) is synchronous; ASGI (`asgi.py`, run by uvicorn/"
                "daphne) supports async views and WebSockets.",
            ),
            q(
                "Which management command audits production security settings?",
                (
                    opt("`python manage.py test`"),
                    opt("`python manage.py check --deploy`", correct=True),
                    opt("`python manage.py migrate`"),
                    opt("`python manage.py runserver`"),
                ),
                "`check --deploy` warns about insecure settings (DEBUG, missing HSTS, insecure "
                "cookies, etc.) so you catch them before release.",
            ),
        ),
    },
    final=(
        q(
            "In DRF, which component automatically generates CRUD URLs from a registered ViewSet?",
            (
                opt("A serializer"),
                opt("A router (e.g. DefaultRouter)", correct=True),
                opt("A middleware"),
                opt("A signal"),
            ),
            "A router maps a registered ViewSet to the full set of list/detail CRUD URLs.",
        ),
        q(
            "Why does the order of entries in `MIDDLEWARE` matter?",
            (
                opt("It does not matter at all"),
                opt(
                    "Request flows top-to-bottom and response bottom-to-top, so order changes "
                    "behaviour",
                    correct=True,
                ),
                opt("Only the last middleware ever executes"),
                opt("It only affects template rendering"),
            ),
            "Middleware wraps the view in order; reordering security/session/auth layers can change "
            "behaviour and even open vulnerabilities.",
        ),
        q(
            "Which built-in signal fires after a model instance is saved?",
            (
                opt("`pre_delete`"),
                opt("`post_save`", correct=True),
                opt("`request_started`"),
                opt("`m2m_changed` only"),
            ),
            "`post_save` is dispatched after `save()`, with a `created` flag indicating insert vs. "
            "update.",
        ),
        q(
            "You loop over articles and access `article.author.name`. Which fix removes the N+1?",
            (
                opt("Add a database index on name"),
                opt('Use `Article.objects.select_related("author")`', correct=True),
                opt("Wrap the loop in a transaction"),
                opt("Set DEBUG=False"),
            ),
            '`select_related("author")` JOINs the author in the same query, so the loop costs one '
            "query instead of N+1.",
        ),
        q(
            'What does `self.client.get(reverse("blog:create"))` returning status 302 typically '
            "indicate in a test?",
            (
                opt("A server error"),
                opt(
                    "A redirect, e.g. an unauthenticated user sent to the login page", correct=True
                ),
                opt("A successful render"),
                opt("A 404 not found"),
            ),
            "302 is a redirect; for a login-protected create view it means the anonymous client was "
            "sent to the login page.",
        ),
        q(
            "Which setting blocks Host-header attacks by rejecting requests for unknown hosts?",
            (
                opt("`SECRET_KEY`"),
                opt("`ALLOWED_HOSTS`", correct=True),
                opt("`STATIC_ROOT`"),
                opt("`INSTALLED_APPS`"),
            ),
            "`ALLOWED_HOSTS` lists the valid hostnames; Django refuses requests whose Host header is "
            "not in it (required when DEBUG=False).",
        ),
    ),
)
