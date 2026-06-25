"""Curated Django track: Basics, Intermediate, Advanced.

Teaches the Django web framework (modern 4.x/5.x) from the MTV pattern and the
ORM through forms and class-based views to Django REST Framework, signals,
performance tuning, testing, and production deployment.

There is NO live Python runtime in the Academy (the restricted interpreter
cannot run Django), so all code is illustrative -- you would run it locally with
``python manage.py``. The interactivity comes from Mermaid diagrams of the
request/response lifecycle, the MTV architecture, ORM relationships, URL
routing, and the DRF flow.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY (seed_quizzes/django_*.py) at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


# ── Django — Basics ───────────────────────────────────────────────────────────

_DJANGO_BASICS = SeedCourse(
    slug="django-basics",
    title="Django — Basics",
    description=(
        "Build your first Django site: the MTV pattern and request/response "
        "lifecycle, project vs. app structure, models and the ORM, views and URL "
        "routing, templates with inheritance, and the built-in admin - with "
        "architecture diagrams and a quiz after every lesson."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is Django & the MTV pattern",
            "10 min",
            r"""# What is Django & the MTV pattern

**Django** is a high-level Python web framework that ships with everything you
need to build a database-backed website: an ORM, a URL router, a templating
engine, forms, authentication, and an automatic admin. Its motto is
*"the web framework for perfectionists with deadlines"* - it favours
**convention over configuration** and **"batteries included"**.

## The MTV pattern

Django organises code into **Model - Template - View** (MTV), its take on the
classic MVC idea:

- **Model** - your data and business rules, mapped to database tables by the ORM.
- **Template** - the presentation layer: HTML with placeholders.
- **View** - the glue: it receives a request, talks to models, and returns a
  response (often a rendered template).

The URL **router** sits in front, mapping a URL to the view that handles it.

```mermaid
flowchart LR
  REQ["HTTP request"] --> URLS["urls.py (router)"]
  URLS --> VIEW["View (Python function/class)"]
  VIEW --> MODEL["Model (ORM -> database)"]
  MODEL --> VIEW
  VIEW --> TPL["Template (HTML)"]
  TPL --> RESP["HTTP response"]
```

## The request/response lifecycle

Every request flows through middleware, the router, your view, and back:

```mermaid
sequenceDiagram
  participant B as Browser
  participant M as Middleware
  participant U as URLconf
  participant V as View
  participant D as Database
  B->>M: GET /articles/5/
  M->>U: resolve path
  U->>V: call article_detail(request, pk=5)
  V->>D: Article.objects.get(pk=5)
  D-->>V: row
  V-->>B: 200 OK (rendered HTML)
```

## Install and check the version

```bash
python -m venv .venv
source .venv/bin/activate
pip install "Django>=5.0"
python -m django --version   # 5.x
```

> **Why Django?** Instagram, Mozilla, and many others run on it. You get a
> secure, well-trodden path: it handles CSRF, SQL-injection-safe queries, and
> password hashing for you, so you spend time on *your* features.

**Next:** how a Django project is laid out - projects and apps.
""",
        ),
        _t(
            "Project & app structure",
            "10 min",
            r"""# Project & app structure

A Django **project** is the whole site; an **app** is a reusable, focused module
within it (e.g. `blog`, `accounts`, `payments`). One project contains many apps.

## Create a project and an app

```bash
django-admin startproject mysite      # creates the project
cd mysite
python manage.py startapp blog        # creates an app
python manage.py runserver            # dev server at http://127.0.0.1:8000/
```

The layout you get:

```text
mysite/
  manage.py              # CLI entry point (runserver, migrate, ...)
  mysite/                # the "project package"
    __init__.py
    settings.py          # configuration
    urls.py              # root URL router
    asgi.py / wsgi.py    # server entry points
  blog/                  # an app
    __init__.py
    admin.py             # admin registrations
    apps.py              # app config
    models.py            # data models
    views.py             # request handlers
    migrations/          # schema changes over time
    tests.py
```

```mermaid
flowchart TD
  PROJ["Project: mysite"] --> S["settings.py"]
  PROJ --> RU["root urls.py"]
  PROJ --> A1["app: blog"]
  PROJ --> A2["app: accounts"]
  A1 --> M1["models.py"]
  A1 --> V1["views.py"]
  A1 --> U1["urls.py"]
```

## Register the app

An app only becomes active once it is listed in `settings.py`:

```python
# mysite/settings.py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",            # <-- your app
]
```

## manage.py: your control panel

`manage.py` is a thin wrapper around `django-admin` that knows your settings:

```bash
python manage.py runserver        # start the dev server
python manage.py makemigrations   # generate migration files from model changes
python manage.py migrate          # apply migrations to the database
python manage.py createsuperuser  # make an admin login
python manage.py shell            # interactive shell with Django loaded
```

> **Practical insight:** keep apps **small and single-purpose** so they can be
> reused across projects. A good rule: an app should do one thing
> (authentication, a blog, a cart) and be describable in a sentence.

**Next:** describing your data - models and the ORM.
""",
        ),
        _t(
            "Models & the ORM",
            "12 min",
            r"""# Models & the ORM

A **model** is a Python class that maps to a database table; each attribute is a
column. Django's **ORM** (Object-Relational Mapper) lets you query the database
in Python instead of writing SQL.

```python
# blog/models.py
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    published = models.DateField(auto_now_add=True)
    is_draft = models.BooleanField(default=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="articles"
    )

    class Meta:
        ordering = ["-published"]

    def __str__(self):
        return self.title
```

## Relationships as an ER diagram

`ForeignKey` is a one-to-many link. Django also offers `OneToOneField` and
`ManyToManyField`.

```mermaid
erDiagram
  AUTHOR ||--o{ ARTICLE : writes
  AUTHOR {
    int id PK
    string name
    string email
  }
  ARTICLE {
    int id PK
    string title
    text body
    date published
    bool is_draft
    int author_id FK
  }
```

## Migrations: turning models into tables

Models are just Python until you create and apply **migrations**:

```bash
python manage.py makemigrations   # writes blog/migrations/0001_initial.py
python manage.py migrate          # creates/updates the actual tables
```

`makemigrations` records *what changed*; `migrate` *applies* those changes to
the database. Migrations are versioned files you commit to git.

## Querying with the ORM

```python
# python manage.py shell
from blog.models import Article, Author

# Create
ed = Author.objects.create(name="Ada", email="ada@example.com")
Article.objects.create(title="Hello", body="...", author=ed, is_draft=False)

# Read
Article.objects.all()                          # every row
Article.objects.filter(is_draft=False)         # WHERE is_draft = false
Article.objects.get(pk=1)                       # one row by primary key
ed.articles.all()                               # reverse FK via related_name

# Update / delete
Article.objects.filter(pk=1).update(is_draft=True)
Article.objects.filter(is_draft=True).delete()
```

> **Practical insight:** always define `__str__` on a model - it controls how
> objects appear in the admin and the shell, turning "Article object (5)" into
> the actual title.

**Next:** turning a request into a response - views and URLs.
""",
        ),
        _t(
            "Views & URL routing",
            "11 min",
            r"""# Views & URL routing

A **view** takes an `HttpRequest` and returns an `HttpResponse`. The simplest
view is a plain function.

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Article


def article_list(request):
    articles = Article.objects.filter(is_draft=False)
    return render(request, "blog/article_list.html", {"articles": articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, "blog/article_detail.html", {"article": article})
```

`render(request, template, context)` loads a template, fills it with the
**context** dict, and returns an `HttpResponse`. `get_object_or_404` fetches a
row or raises a clean 404.

## Wiring URLs

Each app gets its own `urls.py`, included from the project's root router.

```python
# blog/urls.py
from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.article_list, name="list"),
    path("<int:pk>/", views.article_detail, name="detail"),
]
```

```python
# mysite/urls.py (root)
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("articles/", include("blog.urls")),   # delegates to the app
]
```

## Path converters & routing flow

`<int:pk>` is a **path converter**: it matches an integer and passes it to the
view as `pk`. Others include `<str:slug>`, `<slug:slug>`, and `<uuid:id>`.

```mermaid
flowchart TD
  REQ["GET /articles/5/"] --> ROOT["root urls.py"]
  ROOT -->|include blog.urls| APP["blog/urls.py"]
  APP -->|"match &lt;int:pk&gt;"| VIEW["article_detail(request, pk=5)"]
  VIEW --> RESP["HttpResponse (rendered)"]
```

## Reversing URLs

Never hard-code paths. Use the `name` to build URLs:

```python
from django.urls import reverse
reverse("blog:detail", kwargs={"pk": 5})   # -> "/articles/5/"
```

In templates: `{% raw %}{% url 'blog:detail' article.pk %}{% endraw %}`.

> **Practical insight:** namespacing with `app_name` plus `name=` lets you change
> URL structure later without touching every template and view - reverse by name,
> not by string.

**Next:** rendering HTML - templates.
""",
        ),
        _t(
            "Templates",
            "10 min",
            r"""# Templates

Templates are HTML files with the **Django Template Language** (DTL) - a small,
deliberately limited language so logic stays in views, not markup.

## Variables, tags, and filters

- **Variables**: `{% raw %}{{ article.title }}{% endraw %}`
- **Tags** (logic): `{% raw %}{% for %}{% endraw %}`, `{% raw %}{% if %}{% endraw %}`, `{% raw %}{% url %}{% endraw %}`
- **Filters** (transform): `{% raw %}{{ article.published|date:"Y-m-d" }}{% endraw %}`

```html+django
{% raw %}{# blog/templates/blog/article_list.html #}
<h1>Articles</h1>
<ul>
  {% for article in articles %}
    <li>
      <a href="{% url 'blog:detail' article.pk %}">{{ article.title }}</a>
      <small>{{ article.published|date:"M d, Y" }}</small>
    </li>
  {% empty %}
    <li>No articles yet.</li>
  {% endfor %}
</ul>{% endraw %}
```

## Template inheritance

The most important feature: a **base** template defines `block`s that child
templates override. This is how you share a header, nav, and footer.

```html+django
{% raw %}{# templates/base.html #}
<!doctype html>
<html>
<head><title>{% block title %}My Site{% endblock %}</title></head>
<body>
  <nav>...</nav>
  <main>{% block content %}{% endblock %}</main>
</body>
</html>{% endraw %}
```

```html+django
{% raw %}{# blog/templates/blog/article_detail.html #}
{% extends "base.html" %}

{% block title %}{{ article.title }}{% endblock %}

{% block content %}
  <h1>{{ article.title }}</h1>
  <p>by {{ article.author.name }}</p>
  <div>{{ article.body }}</div>
{% endblock %}{% endraw %}
```

```mermaid
flowchart TD
  BASE["base.html (blocks: title, content)"] --> CHILD1["article_list.html (extends base)"]
  BASE --> CHILD2["article_detail.html (extends base)"]
```

## How templates are found

With `APP_DIRS=True` (the default), Django searches each app's `templates/`
folder. The convention `app/templates/app/file.html` namespaces templates so
two apps can both have an `index.html`.

> **Practical insight:** DTL **auto-escapes** variables, so `{% raw %}{{ user_input }}{% endraw %}`
> is XSS-safe by default. Only mark output safe with the `safe` filter when you
> are certain it contains trusted HTML.

**Next:** the free CRUD UI - the admin site.
""",
        ),
        _t(
            "The admin site",
            "9 min",
            r"""# The admin site

Django generates a complete, production-grade **admin interface** for your models
- a CRUD UI your team can use immediately, with zero custom HTML.

## Enable it

The admin app is in `INSTALLED_APPS` by default. Create a login and run the
server:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# visit http://127.0.0.1:8000/admin/
```

## Register your models

```python
# blog/admin.py
from django.contrib import admin
from .models import Author, Article

admin.site.register(Author)
admin.site.register(Article)
```

That alone gives you list, add, edit, and delete pages for both models.

## Customising with ModelAdmin

For real control, use the `@admin.register` decorator with a `ModelAdmin` class:

```python
from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published", "is_draft")
    list_filter = ("is_draft", "published")
    search_fields = ("title", "body")
    ordering = ("-published",)
    list_editable = ("is_draft",)
```

- `list_display` - columns in the change list.
- `list_filter` - a sidebar of filters.
- `search_fields` - a search box.
- `list_editable` - edit fields right in the list.

```mermaid
flowchart LR
  M["Model (Article)"] --> R["admin.register(Article, ArticleAdmin)"]
  R --> UI["Auto-generated admin: list, add, edit, delete, search, filter"]
```

> **Practical insight:** the admin is for **trusted staff**, not end users -
> it exposes your data model directly. Build separate, permission-scoped views
> for the public; use the admin for internal back-office work.

**Next:** the Intermediate course - forms, class-based views, and querysets.
""",
        ),
    ),
)


# ── Django — Intermediate ─────────────────────────────────────────────────────

_DJANGO_INTERMEDIATE = SeedCourse(
    slug="django-intermediate",
    title="Django — Intermediate",
    description=(
        "Go beyond the basics: forms and validation, class-based generic views, "
        "advanced QuerySets and relationships, authentication and permissions, "
        "migrations in depth, and managing settings, static, and media files - "
        "with diagrams of the form and CBV flows."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Forms & validation",
            "11 min",
            r"""# Forms & validation

Django **forms** render HTML inputs, parse submitted data, and **validate** it -
in one place. There are two kinds: `forms.Form` (standalone) and
`forms.ModelForm` (tied to a model).

## A ModelForm

```python
# blog/forms.py
from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "body", "is_draft"]

    def clean_title(self):
        title = self.cleaned_data["title"]
        if "spam" in title.lower():
            raise forms.ValidationError("Title may not contain 'spam'.")
        return title
```

`ModelForm` builds fields automatically from the model. `clean_<field>` methods
validate individual fields; a `clean()` method validates across fields.

## Handling a form in a view

```python
from django.shortcuts import redirect, render
from .forms import ArticleForm


def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():                     # runs all validation
            form.save()                         # ModelForm writes the row
            return redirect("blog:list")
    else:
        form = ArticleForm()                    # empty form for GET
    return render(request, "blog/article_form.html", {"form": form})
```

```mermaid
flowchart TD
  GET["GET request"] --> EMPTY["render empty form"]
  POST["POST request"] --> BIND["form = ArticleForm(request.POST)"]
  BIND --> VALID{"form.is_valid()?"}
  VALID -->|yes| SAVE["form.save() -> redirect"]
  VALID -->|no| ERRORS["re-render with errors"]
```

## Rendering the form

```html+django
{% raw %}<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Save</button>
</form>{% endraw %}
```

The `{% raw %}{% csrf_token %}{% endraw %}` tag is **required** for POST forms -
Django rejects unprotected POSTs to prevent cross-site request forgery.

> **Practical insight:** the **POST-redirect-GET** pattern (redirect after a
> successful POST) stops the browser re-submitting the form on refresh. Always
> redirect after `save()`, never render directly.

**Next:** writing less view code - class-based views.
""",
        ),
        _t(
            "Class-based views",
            "11 min",
            r"""# Class-based views

**Class-based views (CBVs)** package common patterns - listing, showing,
creating, updating, deleting - into reusable classes, so you write far less code
than function views for standard CRUD.

## Generic display views

```python
# blog/views.py
from django.views.generic import ListView, DetailView
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(is_draft=False)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
```

`ListView` handles the query, pagination, and context; `DetailView` fetches one
object by `pk` (or `slug`) from the URL.

## Generic editing views

```python
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ["title", "body", "is_draft"]
    success_url = reverse_lazy("blog:list")


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy("blog:list")
```

`CreateView`/`UpdateView` build a `ModelForm` for you and handle GET (show form)
and POST (validate and save). Use `reverse_lazy` for `success_url` because URLs
aren't loaded when the class body runs.

## Wiring CBVs to URLs

CBVs are connected via `.as_view()`:

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list"),
    path("<int:pk>/", views.ArticleDetailView.as_view(), name="detail"),
    path("new/", views.ArticleCreateView.as_view(), name="create"),
]
```

```mermaid
flowchart TD
  BASE["View / TemplateView"] --> LIST["ListView"]
  BASE --> DETAIL["DetailView"]
  BASE --> CREATE["CreateView"]
  BASE --> UPDATE["UpdateView"]
  BASE --> DELETE["DeleteView"]
```

> **Practical insight:** reach for a CBV when your view matches a generic pattern
> (list, detail, CRUD) and override hooks like `get_queryset` or
> `get_context_data`. For genuinely custom logic, a function view is clearer -
> use the right tool, not the fanciest one.

**Next:** querying data well - QuerySets and relationships.
""",
        ),
        _t(
            "QuerySets & relationships",
            "12 min",
            r"""# QuerySets & relationships

A **QuerySet** is a lazy, chainable representation of a database query. Nothing
hits the database until you iterate, slice, or otherwise evaluate it.

## Filtering and excluding

```python
Article.objects.filter(is_draft=False)              # WHERE is_draft = false
Article.objects.exclude(author__name="Ada")         # WHERE NOT ...
Article.objects.filter(is_draft=False).order_by("title")
```

## Field lookups

Lookups use the `field__lookup=value` syntax:

```python
Article.objects.filter(title__icontains="django")   # case-insensitive LIKE
Article.objects.filter(published__year=2026)         # by year
Article.objects.filter(published__gte="2026-01-01")  # >=
Article.objects.filter(author__email__endswith=".org")  # span relationship
```

The double underscore `__` both spans relationships (`author__email`) and
selects a lookup (`__icontains`).

## Relationships: FK, O2O, M2M

```python
class Tag(models.Model):
    name = models.CharField(max_length=50)


class Article(models.Model):
    # ... ForeignKey to Author from earlier ...
    tags = models.ManyToManyField(Tag, related_name="articles")
```

```mermaid
erDiagram
  AUTHOR ||--o{ ARTICLE : writes
  ARTICLE }o--o{ TAG : "tagged with"
  TAG {
    int id PK
    string name
  }
```

Traversing them:

```python
article.author.name                  # follow ForeignKey
author.articles.all()                # reverse FK (related_name)
article.tags.all()                    # M2M forward
tag.articles.all()                    # M2M reverse
article.tags.add(tag1, tag2)          # link
```

## Aggregation and Q objects

```python
from django.db.models import Count, Q

Author.objects.annotate(n=Count("articles"))         # count per author
Article.objects.filter(Q(is_draft=False) | Q(author__name="Ada"))  # OR
```

`Q` objects let you build complex `AND`/`OR`/`NOT` conditions; `annotate` adds
computed columns per row.

> **Practical insight:** QuerySets are **lazy and cached** - assign one to a
> variable and reuse it, and the query runs once. But calling `.filter()` again
> builds a *new* query. Knowing when a QuerySet hits the database is the key to
> avoiding surprise queries.

**Next:** knowing who's logged in - authentication.
""",
        ),
        _t(
            "Authentication & users",
            "11 min",
            r"""# Authentication & users

Django ships a full **auth system**: a `User` model, login/logout views,
password hashing, sessions, and a permission framework.

## The User model

`django.contrib.auth.models.User` has `username`, `email`, `password` (hashed),
`is_staff`, `is_superuser`, and more.

```python
from django.contrib.auth.models import User

User.objects.create_user("ada", "ada@example.com", "s3cret")  # hashes password
user = User.objects.get(username="ada")
user.check_password("s3cret")   # True
```

## Login and logout

```python
# accounts/urls.py - reuse Django's built-in auth views
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
```

```mermaid
sequenceDiagram
  participant U as User
  participant L as LoginView
  participant A as authenticate()
  participant S as Session
  U->>L: POST username + password
  L->>A: check credentials
  A-->>L: User or None
  L->>S: login(request, user) sets session cookie
  S-->>U: redirect, now authenticated
```

## Restricting access

```python
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@permission_required("blog.add_article", raise_exception=True)
def create_article(request):
    ...
```

For class-based views, use the mixins `LoginRequiredMixin` and
`PermissionRequiredMixin`:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ["title", "body"]
```

## Permissions and groups

Each model gets `add`, `change`, `delete`, and `view` permissions automatically.
Bundle them into **groups** and assign groups to users via the admin or code:

```python
request.user.has_perm("blog.change_article")   # True / False
request.user.is_authenticated                   # check inside templates too
```

> **Practical insight:** never store or compare raw passwords. Always use
> `create_user`/`set_password` (which hash) and `check_password`. If you need
> extra profile fields, set a **custom user model** early - it is painful to
> change after the first migration.

**Next:** evolving the schema safely - migrations in depth.
""",
        ),
        _t(
            "Migrations in depth",
            "10 min",
            r"""# Migrations in depth

**Migrations** are versioned, ordered files that describe how to evolve your
database schema. Each is a Python file in an app's `migrations/` folder.

## The two commands

```bash
python manage.py makemigrations     # detect model changes, write a migration
python manage.py migrate            # apply unapplied migrations to the DB
python manage.py showmigrations     # see what's applied (and what isn't)
python manage.py sqlmigrate blog 0002   # preview the SQL a migration runs
```

## Dependencies and ordering

Migrations form a directed graph. Each migration declares the ones it depends
on, so Django applies them in a consistent order even across apps:

```python
# blog/migrations/0002_article_tags.py
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),       # this app's previous migration
        ("auth", "0012_alter_user_first_name_max_length"),  # cross-app dep
    ]
    operations = [
        migrations.AddField(
            model_name="article",
            name="views",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
```

```mermaid
flowchart LR
  M1["0001_initial"] --> M2["0002_add_tags"]
  M2 --> M3["0003_add_index"]
  AUTH["auth.0012"] --> M2
```

## Data migrations

Schema migrations change structure; **data migrations** change *content* (e.g.
backfilling a new column). Use `RunPython` with the historical model:

```python
from django.db import migrations


def set_default_slugs(apps, schema_editor):
    Article = apps.get_model("blog", "Article")     # historical version
    for article in Article.objects.all():
        article.slug = article.title.lower().replace(" ", "-")
        article.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [("blog", "0003_article_slug")]
    operations = [
        migrations.RunPython(set_default_slugs, migrations.RunPython.noop),
    ]
```

Always use `apps.get_model(...)` inside data migrations - it gives the model as
it existed *at that point in history*, not your current code.

> **Practical insight:** commit migration files to git and **never edit an
> applied migration** - generate a new one instead. Provide a reverse function
> (or `noop`) so migrations can roll back cleanly.

**Next:** configuration and assets - settings, static, and media files.
""",
        ),
        _t(
            "Settings, static & media files",
            "10 min",
            r"""# Settings, static & media files

`settings.py` configures everything: the database, installed apps, middleware,
templates, and where files live.

## Key settings

```python
# mysite/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]     # never hard-code in prod
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"
ALLOWED_HOSTS = ["example.com", "www.example.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mysite",
        "USER": "mysite",
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

## Static vs. media files

These are different and often confused:

- **Static files** - CSS, JS, images that *ship with your code*. Authored by you.
- **Media files** - files *uploaded by users* at runtime (avatars, attachments).

```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"   # where collectstatic gathers them
STATICFILES_DIRS = [BASE_DIR / "static"] # extra source dirs in dev

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"          # where uploads are stored
```

```mermaid
flowchart LR
  DEV["dev: app static/ dirs"] -->|collectstatic| SR["STATIC_ROOT (staticfiles/)"]
  SR --> WEB["web server / CDN serves /static/"]
  UPL["user upload"] --> MR["MEDIA_ROOT (media/)"]
  MR --> WEB2["served at /media/"]
```

## Using static files in templates

```html+django
{% raw %}{% load static %}
<link rel="stylesheet" href="{% static 'css/site.css' %}">
<img src="{% static 'img/logo.png' %}" alt="logo">{% endraw %}
```

## Collecting static for production

```bash
python manage.py collectstatic    # copies all static files into STATIC_ROOT
```

In production a web server (nginx) or a CDN serves `STATIC_ROOT` directly -
Django itself does not serve static files efficiently.

> **Practical insight:** keep secrets (`SECRET_KEY`, DB passwords, API keys) in
> **environment variables**, never in `settings.py` in git. Split settings into
> `base`/`dev`/`prod` or read from the environment so the same code runs safely
> everywhere.

**Next:** the Advanced course - DRF, middleware, signals, performance, testing,
and deployment.
""",
        ),
    ),
)


# ── Django — Advanced ─────────────────────────────────────────────────────────

_DJANGO_ADVANCED = SeedCourse(
    slug="django-advanced",
    title="Django — Advanced",
    description=(
        "Production Django: building APIs with Django REST Framework, the "
        "middleware request/response lifecycle, signals, performance tuning "
        "(select_related/prefetch_related, caching, indexing, avoiding N+1), "
        "testing with TestCase and the test client, and secure deployment with "
        "WSGI/ASGI and gunicorn."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Django REST Framework",
            "13 min",
            r"""# Django REST Framework

**Django REST Framework (DRF)** is the standard library for building web APIs on
Django. It adds serializers, class-based API views, viewsets, routers, auth, and
a browsable API.

```bash
pip install djangorestframework
# add "rest_framework" to INSTALLED_APPS
```

## Serializers

A **serializer** converts model instances to JSON (and validates JSON on the way
in) - the API equivalent of a form.

```python
# blog/serializers.py
from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "body", "is_draft", "author", "author_name"]
        read_only_fields = ["id"]
```

## ViewSets and routers

A **ViewSet** bundles list/create/retrieve/update/destroy; a **router** wires the
URLs automatically.

```python
# blog/api.py
from rest_framework import viewsets, permissions
from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related("author").all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
```

```python
# mysite/urls.py
from rest_framework.routers import DefaultRouter
from blog.api import ArticleViewSet

router = DefaultRouter()
router.register("articles", ArticleViewSet)

urlpatterns = [path("api/", include(router.urls))]
```

The router generates `GET/POST /api/articles/` and
`GET/PUT/PATCH/DELETE /api/articles/{id}/` from that one registration.

## The DRF request flow

```mermaid
flowchart LR
  REQ["HTTP request"] --> ROUTER["Router -> ViewSet"]
  ROUTER --> AUTH["Authentication + Permissions"]
  AUTH --> VIEW["ViewSet action (list/create/...)"]
  VIEW --> SER["Serializer (validate / serialize)"]
  SER --> MODEL["QuerySet / Model"]
  MODEL --> SER
  SER --> RESP["JSON response"]
```

> **Practical insight:** scope each ViewSet's `queryset` to what the user may see
> and set `permission_classes` explicitly - the default open API is convenient in
> dev but unsafe in production. `select_related`/`prefetch_related` on the
> queryset keeps list endpoints fast (next lesson).

**Next:** what wraps every request - middleware.
""",
        ),
        _t(
            "Middleware & the request/response lifecycle",
            "11 min",
            r"""# Middleware & the request/response lifecycle

**Middleware** is a stack of components that wrap every request and response.
Each one can inspect or modify the request on the way in and the response on the
way out - like layers of an onion around your view.

## The default stack

```python
# settings.py
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

Order matters: request flows **top to bottom** before the view, response flows
**bottom to top** after.

```mermaid
flowchart TD
  REQ["Request"] --> SEC["SecurityMiddleware"]
  SEC --> SESS["SessionMiddleware"]
  SESS --> AUTH["AuthenticationMiddleware"]
  AUTH --> VIEW["View"]
  VIEW --> AUTH2["Auth (response phase)"]
  AUTH2 --> SESS2["Session (response phase)"]
  SESS2 --> SEC2["Security (response phase)"]
  SEC2 --> RESP["Response"]
```

## Writing custom middleware

Modern middleware is a callable factory:

```python
# blog/middleware.py
import time


class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response       # called once at startup

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)  # call the next layer / the view
        elapsed = time.monotonic() - start
        response["X-Elapsed-Ms"] = f"{elapsed * 1000:.1f}"
        return response
```

Register it in `MIDDLEWARE`. The code **before** `get_response` runs on the way
in; the code **after** runs on the way out.

## Hooks

Middleware can also define `process_view`, `process_exception`, and
`process_template_response` for finer control over those phases.

> **Practical insight:** middleware runs on **every** request, so keep it cheap
> and avoid per-request database queries there. Put security-sensitive middleware
> (security, session, auth) in the documented order - reordering them can open
> real vulnerabilities.

**Next:** reacting to model events - signals.
""",
        ),
        _t(
            "Signals",
            "10 min",
            r"""# Signals

**Signals** let decoupled code react to events elsewhere in Django - "when X
happens, also do Y" - without the sender knowing about the receiver.

## Built-in model signals

The most common are `pre_save`, `post_save`, `pre_delete`, and `post_delete`.

```python
# blog/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:                       # only on the first save (insert)
        Profile.objects.create(user=instance)
```

`@receiver(post_save, sender=User)` connects the function; `created` is `True`
only when the row was just inserted.

```mermaid
sequenceDiagram
  participant V as View / code
  participant M as Model.save()
  participant S as post_save signal
  participant R as Receiver(s)
  V->>M: user.save()
  M->>S: dispatch post_save(sender=User, created=True)
  S->>R: create_profile(...)
  R-->>S: done
```

## Connecting them at startup

Import your signals in the app's `AppConfig.ready()` so they register when Django
starts:

```python
# blog/apps.py
from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = "blog"

    def ready(self):
        from . import signals   # noqa: F401  (registers the receivers)
```

## Custom signals

You can define and send your own:

```python
import django.dispatch

article_published = django.dispatch.Signal()
# later:  article_published.send(sender=Article, article=instance)
```

> **Practical insight:** signals are powerful but **hide control flow** - it can
> be hard to see *why* something happened. For logic that always runs with a save
> (like creating a related row), prefer overriding `save()` or a service function;
> reserve signals for genuinely cross-cutting, decoupled reactions.

**Next:** making it fast - performance and avoiding N+1 queries.
""",
        ),
        _t(
            "Performance & avoiding N+1",
            "12 min",
            r"""# Performance & avoiding N+1

The single most common Django performance bug is the **N+1 query**: one query to
fetch a list, then one extra query per item to follow a relationship.

## The N+1 problem

```python
# BAD: 1 query for articles, then 1 per article for its author = N+1 queries
for article in Article.objects.all():
    print(article.author.name)        # hits the DB every iteration
```

## select_related and prefetch_related

- **`select_related`** - for `ForeignKey`/`OneToOne`. Does a SQL **JOIN**, so the
  related object comes back in one query.
- **`prefetch_related`** - for `ManyToMany` and reverse FK. Does a **second**
  query and joins in Python.

```python
# GOOD: 1 query total (JOIN) instead of N+1
for article in Article.objects.select_related("author"):
    print(article.author.name)

# M2M / reverse FK: 2 queries total instead of N+1
authors = Author.objects.prefetch_related("articles")
```

```mermaid
flowchart TD
  NAIVE["Naive loop: 1 + N queries"] -->|select_related FK| ONE["1 query (JOIN)"]
  NAIVE -->|prefetch_related M2M| TWO["2 queries (separate + join in Python)"]
```

## Caching

Cache expensive results so you don't recompute them every request:

```python
# settings.py
CACHES = {"default": {
    "BACKEND": "django.core.cache.backends.redis.RedisCache",
    "LOCATION": "redis://127.0.0.1:6379",
}}
```

```python
from django.core.cache import cache

data = cache.get("top_articles")
if data is None:
    data = list(Article.objects.filter(is_draft=False)[:10])
    cache.set("top_articles", data, timeout=300)   # 5 minutes
```

## Indexing

Add database **indexes** on columns you filter or order by often:

```python
class Article(models.Model):
    slug = models.SlugField(db_index=True)
    published = models.DateField()

    class Meta:
        indexes = [models.Index(fields=["is_draft", "published"])]
```

## Measuring

Use `.only()`/`.defer()` to limit columns, and inspect queries:

```python
from django.db import connection
print(len(connection.queries))     # query count (DEBUG=True)
print(Article.objects.all().query) # the SQL Django will run
```

> **Practical insight:** measure before optimising. Install **django-debug-toolbar**
> in dev to see the exact queries each page runs - the N+1 culprits jump out.
> Fix them with `select_related`/`prefetch_related` first; reach for caching only
> once the queries themselves are tight.

**Next:** proving it works - testing.
""",
        ),
        _t(
            "Testing",
            "11 min",
            r"""# Testing

Django builds on Python's `unittest` with a **`TestCase`** that wraps each test
in a database transaction (rolled back after), plus a **test client** that
simulates requests without a running server.

## Model and ORM tests

```python
# blog/tests.py
from django.test import TestCase
from .models import Author, Article


class ArticleModelTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Ada", email="ada@x.com")

    def test_str_is_title(self):
        article = Article.objects.create(
            title="Hello", body="...", author=self.author, is_draft=False
        )
        self.assertEqual(str(article), "Hello")

    def test_default_is_draft(self):
        article = Article.objects.create(title="X", body="...", author=self.author)
        self.assertTrue(article.is_draft)
```

## The test client: testing views

```python
from django.test import TestCase
from django.urls import reverse


class ArticleViewTests(TestCase):
    def test_list_page_returns_200(self):
        response = self.client.get(reverse("blog:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/article_list.html")

    def test_create_requires_login(self):
        response = self.client.get(reverse("blog:create"))
        self.assertEqual(response.status_code, 302)   # redirect to login
```

```mermaid
flowchart LR
  TEST["TestCase"] --> TX["open transaction"]
  TX --> RUN["run test (client.get / ORM)"]
  RUN --> ASSERT["assertions"]
  ASSERT --> ROLLBACK["rollback -> clean DB for next test"]
```

## Fixtures and factories

Load known data with **fixtures** (`loaddata`) or, more commonly, build objects
in code (often with `factory_boy`):

```python
# load from blog/fixtures/articles.json
class WithFixtures(TestCase):
    fixtures = ["articles.json"]
```

## Running tests

```bash
python manage.py test                 # run the whole suite
python manage.py test blog            # one app
python manage.py test blog.tests.ArticleViewTests.test_list_page_returns_200
```

> **Practical insight:** use `setUpTestData` (class-level) instead of `setUp`
> (per-test) for shared read-only objects - it creates them once per class, so
> the suite runs far faster. Every bug fix should ship with a regression test
> that fails before the fix and passes after.

**Next:** shipping it - deployment and security.
""",
        ),
        _t(
            "Deployment & security",
            "12 min",
            r"""# Deployment & security

Production Django is *not* `runserver`. You run your app behind a real WSGI/ASGI
server and a web server, with security settings locked down.

## WSGI vs. ASGI

- **WSGI** (`wsgi.py`) - the classic synchronous interface; run with **gunicorn**
  or uWSGI.
- **ASGI** (`asgi.py`) - the async interface for WebSockets and async views; run
  with **uvicorn** or **daphne**.

```mermaid
flowchart LR
  CLIENT["Client"] --> NGINX["nginx (TLS, static files)"]
  NGINX --> GUNICORN["gunicorn (WSGI workers)"]
  GUNICORN --> DJANGO["Django app (wsgi.py)"]
  DJANGO --> DB["PostgreSQL"]
  NGINX --> STATIC["/static, /media (served directly)"]
```

## Running with gunicorn

```bash
pip install gunicorn
gunicorn mysite.wsgi:application --workers 3 --bind 0.0.0.0:8000
python manage.py collectstatic --noinput   # gather static for nginx/CDN
python manage.py migrate --noinput          # apply migrations on deploy
```

## The production security checklist

```python
# settings.py (production)
DEBUG = False                                  # never True in production
ALLOWED_HOSTS = ["example.com"]                # required when DEBUG=False
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]   # from the environment, kept secret

SECURE_SSL_REDIRECT = True                     # force HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000                 # tell browsers HTTPS-only
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

Django can audit this for you:

```bash
python manage.py check --deploy     # warns about insecure settings
```

## Why each setting matters

- **`DEBUG = False`** - with `DEBUG=True`, errors leak your settings, source, and
  SQL to anyone who triggers them. This is the #1 production mistake.
- **`ALLOWED_HOSTS`** - blocks Host-header attacks; Django refuses requests for
  hosts not in the list.
- **`SECRET_KEY`** - signs sessions and tokens. If it leaks, sessions can be
  forged - keep it out of source control and rotate it if exposed.
- **Secure cookies + HTTPS** - stop session cookies and CSRF tokens from being
  sniffed or sent over plain HTTP.

> **Practical insight:** treat deployment as code. Run `migrate` and
> `collectstatic` on every release, keep secrets in the environment, and run
> `manage.py check --deploy` in CI so an insecure setting fails the build before
> it reaches production.

**Next:** the final check.
""",
        ),
    ),
)


DJANGO_COURSES = (_DJANGO_BASICS, _DJANGO_INTERMEDIATE, _DJANGO_ADVANCED)

__all__ = ["DJANGO_COURSES"]
