"""Quiz spec for the Ruby on Rails — Advanced course (per-lesson + final)."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Building a JSON API": (
            q(
                "What does `rails new storefront --api` produce?",
                (
                    opt("A static site with no controllers"),
                    opt(
                        "A slim API-only app without views and browser middleware",
                        correct=True,
                    ),
                    opt("An app that can only read, never write"),
                    opt("A frontend SPA in React"),
                ),
                "`--api` builds an API-only app whose `ApplicationController` inherits from "
                "`ActionController::API` - no view layer, cookies, or flash.",
            ),
            q(
                "Why namespace API routes under `/api/v1`?",
                (
                    opt("It is required for JSON to work"),
                    opt(
                        "To version the API so a later v2 won't break existing clients",
                        correct=True,
                    ),
                    opt("To enable Hotwire"),
                    opt("To skip strong parameters"),
                ),
                "Versioning under `/api/v1` lets you ship breaking changes as a new version "
                "without affecting current clients.",
            ),
            q(
                "What is jbuilder used for?",
                (
                    opt("Running background jobs"),
                    opt("Controlling the exact shape of a JSON response", correct=True),
                    opt("Compiling JavaScript assets"),
                    opt("Encrypting credentials"),
                ),
                "jbuilder is a template language for building JSON, giving precise control over "
                "the response structure.",
            ),
        ),
        "Active Job & background processing": (
            q(
                "What is Active Job?",
                (
                    opt("A database adapter"),
                    opt("Rails' queuing abstraction over backends like Sidekiq", correct=True),
                    opt("A templating engine"),
                    opt("A testing framework"),
                ),
                "Active Job is a queuing abstraction; you write a job once and run it on a "
                "backend such as Sidekiq, GoodJob, or Solid Queue.",
            ),
            q(
                "Why should you pass record ids (not objects) to a background job?",
                (
                    opt("Objects cannot be serialised at all"),
                    opt(
                        "Jobs are serialised to the queue; an id lets the worker load fresh data",
                        correct=True,
                    ),
                    opt("Ids run faster in Ruby"),
                    opt("Objects bypass the queue entirely"),
                ),
                "Jobs are serialised onto the queue; passing an id keeps the payload small and "
                "lets the worker fetch the current record.",
            ),
            q(
                "What method enqueues a job to run later?",
                (
                    opt("`perform_now`"),
                    opt("`perform_later`", correct=True),
                    opt("`deliver`"),
                    opt("`call`"),
                ),
                "`Job.perform_later(args)` enqueues the job and returns immediately; the work "
                "runs in a worker process.",
            ),
        ),
        "Hotwire: Turbo & Stimulus for realtime": (
            q(
                "What does Hotwire send over the wire instead of JSON?",
                (
                    opt("HTML", correct=True),
                    opt("Raw SQL"),
                    opt("Protocol buffers"),
                    opt("CSV"),
                ),
                "Hotwire ships HTML over the wire (Turbo Frames/Streams), avoiding a heavy "
                "client-side JSON framework.",
            ),
            q(
                "What does a Turbo Stream broadcast let you do?",
                (
                    opt("Cache an entire page in Redis"),
                    opt(
                        "Push DOM updates (append/replace/remove) to subscribers in realtime",
                        correct=True,
                    ),
                    opt("Run a migration on every client"),
                    opt("Encrypt the session cookie"),
                ),
                "Turbo Streams push server-rendered DOM actions over Action Cable so all "
                "subscribed browsers update without a reload.",
            ),
            q(
                "What is Stimulus used for in a Hotwire app?",
                (
                    opt("Serialising JSON responses"),
                    opt(
                        "Connecting small JavaScript controllers to HTML via data attributes",
                        correct=True,
                    ),
                    opt("Defining database migrations"),
                    opt("Running tests in CI"),
                ),
                "Stimulus wires modest JS behaviour to markup using `data-controller`, "
                "`data-action`, and target attributes.",
            ),
        ),
        "Performance: N+1, includes & caching": (
            q(
                "Which method preloads associations to eliminate N+1 queries?",
                (
                    opt("`pluck`"),
                    opt("`includes`", correct=True),
                    opt("`group`"),
                    opt("`select`"),
                ),
                "`includes(:author, :comments)` preloads associations, replacing one-query-per-"
                "record with a couple of queries.",
            ),
            q(
                "How does Russian-doll caching avoid re-rendering unchanged inner fragments?",
                (
                    opt("By disabling caching on the inner fragments"),
                    opt(
                        "By keying caches on records so only changed fragments (and wrappers) "
                        "re-render",
                        correct=True,
                    ),
                    opt("By caching only the database, never the views"),
                    opt("By rendering everything on every request"),
                ),
                "Nested `cache` blocks keyed on each record (with `touch: true`) re-render only "
                "the fragment that changed and its wrapper.",
            ),
            q(
                "What does `belongs_to :post, touch: true` do for caching?",
                (
                    opt("Deletes the post when a child changes"),
                    opt("Updates the post's `updated_at` when the child changes", correct=True),
                    opt("Disables validations on the post"),
                    opt("Eager-loads the post automatically"),
                ),
                "`touch: true` bumps the parent's `updated_at` on a child change, busting the "
                "parent's cache key for Russian-doll caching.",
            ),
        ),
        "Testing: Minitest & RSpec": (
            q(
                "Which testing framework ships built into Rails?",
                (
                    opt("RSpec"),
                    opt("Minitest", correct=True),
                    opt("Cucumber"),
                    opt("Jest"),
                ),
                "Rails ships with Minitest by default; RSpec is a popular add-on many teams "
                "prefer.",
            ),
            q(
                "What is the difference between FactoryBot's `build` and `create`?",
                (
                    opt("`build` hits the database; `create` does not"),
                    opt(
                        "`build` instantiates in memory; `create` saves to the database",
                        correct=True,
                    ),
                    opt("They are identical"),
                    opt("`create` only works in system specs"),
                ),
                "`build` makes an in-memory object (no DB write); `create` persists it - use "
                "`build` when you don't need a saved record.",
            ),
            q(
                "What does a request spec exercise?",
                (
                    opt("Only the model in isolation"),
                    opt("The full controller stack through routes", correct=True),
                    opt("Only the JavaScript layer"),
                    opt("The database schema file"),
                ),
                "Request specs hit the app through its routes and controllers, asserting on the "
                "real HTTP response.",
            ),
        ),
        "Deployment & security": (
            q(
                "What is Puma in a Rails deployment?",
                (
                    opt("The database"),
                    opt("The multi-threaded application server", correct=True),
                    opt("The asset compiler"),
                    opt("The background job queue"),
                ),
                "Puma is the threaded (optionally multi-process) application server Rails runs "
                "on, configured in `config/puma.rb`.",
            ),
            q(
                "Why must `config/master.key` never be committed to the repository?",
                (
                    opt("It is too large for git"),
                    opt(
                        "It decrypts `credentials.yml.enc`; leaking it exposes every secret",
                        correct=True,
                    ),
                    opt("It changes on every deploy"),
                    opt("It only works in development"),
                ),
                "The master key decrypts the encrypted credentials file; it is gitignored and "
                "supplied in production via `RAILS_MASTER_KEY`.",
            ),
            q(
                "Which Rails default protects HTML forms against forged cross-site requests?",
                (
                    opt("Strong parameters"),
                    opt("CSRF protection (the authenticity token)", correct=True),
                    opt("Eager loading"),
                    opt("Fragment caching"),
                ),
                "CSRF protection is on by default; `form_with` injects an authenticity token "
                "that Rails verifies on each non-GET request.",
            ),
        ),
    },
    final=(
        q(
            "In an API-only app, what does `ApplicationController` inherit from?",
            (
                opt("`ActionController::Base`"),
                opt("`ActionController::API`", correct=True),
                opt("`ActiveRecord::Base`"),
                opt("`ApplicationRecord`"),
            ),
            "API-only apps inherit from `ActionController::API`, dropping the view layer, "
            "cookies, and flash.",
        ),
        q(
            "Which call runs work off the web request via a queue?",
            (
                opt("`Job.perform_now`"),
                opt("`Job.perform_later`", correct=True),
                opt("`render json:`"),
                opt("`Model.find`"),
            ),
            "`perform_later` enqueues the job so a worker handles the slow work, letting the "
            "request respond immediately.",
        ),
        q(
            "How does Hotwire push realtime updates to multiple browsers?",
            (
                opt("By polling the server every second"),
                opt("Turbo Stream broadcasts over Action Cable (WebSockets)", correct=True),
                opt("By reloading the whole page"),
                opt("Through background jobs only"),
            ),
            "Turbo Stream broadcasts send DOM-update actions over Action Cable so every "
            "subscribed browser updates live.",
        ),
        q(
            "What is the most common cause of slow Rails pages, fixed with `includes`?",
            (
                opt("Too many partials"),
                opt("N+1 queries", correct=True),
                opt("Missing CSRF tokens"),
                opt("Excessive callbacks"),
            ),
            "N+1 queries are the typical bottleneck; eager loading with `includes` collapses "
            "them into a couple of queries.",
        ),
        q(
            "Which gem-backed factories help set up test data flexibly?",
            (
                opt("Brakeman"),
                opt("FactoryBot", correct=True),
                opt("Puma"),
                opt("Sidekiq"),
            ),
            "FactoryBot defines factories whose `build`/`create` make intent-revealing test "
            "data, an alternative to fixtures.",
        ),
        q(
            "Where do production secrets like the secret key base belong?",
            (
                opt("Hard-coded in the controller"),
                opt("In encrypted credentials, decrypted with the master key", correct=True),
                opt("In `db/schema.rb`"),
                opt("In the public assets folder"),
            ),
            "Secrets live in `config/credentials.yml.enc`, encrypted by `master.key` "
            "(supplied via `RAILS_MASTER_KEY` in production).",
        ),
    ),
)
