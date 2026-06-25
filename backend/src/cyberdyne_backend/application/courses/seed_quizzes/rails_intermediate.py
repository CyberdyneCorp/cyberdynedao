"""Quiz spec for the Ruby on Rails — Intermediate course (per-lesson + final)."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Associations: has_many, belongs_to, has_many :through": (
            q(
                "In a one-to-many association, which side holds the foreign key?",
                (
                    opt("The `has_many` side"),
                    opt("The `belongs_to` side", correct=True),
                    opt("Neither; the foreign key lives in a join table"),
                    opt("Both sides hold a copy of it"),
                ),
                "The `belongs_to` side owns the foreign key (e.g. `comments.post_id`); add it "
                "with `t.references :post`.",
            ),
            q(
                "What does `has_many :comments, dependent: :destroy` do?",
                (
                    opt("Prevents comments from ever being deleted"),
                    opt("Deletes the post's comments when the post is destroyed", correct=True),
                    opt("Creates a new comment automatically"),
                    opt("Makes comments read-only"),
                ),
                "`dependent: :destroy` removes the associated comments when the parent post is "
                "destroyed, avoiding orphaned rows.",
            ),
            q(
                "Which construct models a many-to-many relationship through a join model?",
                (
                    opt("`belongs_to`"),
                    opt("`has_one`"),
                    opt("`has_many :through`", correct=True),
                    opt("`validates :uniqueness`"),
                ),
                "`has_many :through` uses a real join model (e.g. Appointment) so the "
                "relationship can carry extra columns.",
            ),
        ),
        "Validations & callbacks": (
            q(
                "When do Active Record validations run by default?",
                (
                    opt("Only when you call `valid?` manually"),
                    opt("On `save`, `create`, and `update`", correct=True),
                    opt("Only in the test environment"),
                    opt("Never; they must be triggered by a callback"),
                ),
                "Validations run automatically on `save`, `create`, and `update`, populating "
                "`errors` on failure.",
            ),
            q(
                "What is the difference between `save` and `save!`?",
                (
                    opt("`save` raises on failure; `save!` returns false"),
                    opt("`save` returns true/false; `save!` raises on failure", correct=True),
                    opt("They are identical"),
                    opt("`save!` skips validations entirely"),
                ),
                "`save` returns true or false; the bang `save!` raises "
                "`ActiveRecord::RecordInvalid` when validation fails.",
            ),
            q(
                "Why is `after_commit` often preferred for side effects like sending email?",
                (
                    opt("It runs before validations, so it is faster"),
                    opt("It fires only once the transaction actually succeeds", correct=True),
                    opt("It skips the database write"),
                    opt("It is the only callback that can access `self`"),
                ),
                "`after_commit` runs after the transaction commits, so side effects don't fire "
                "if the save is rolled back.",
            ),
        ),
        "Strong parameters & forms": (
            q(
                "What attack do strong parameters defend against?",
                (
                    opt("SQL injection"),
                    opt("Cross-site scripting"),
                    opt("Mass assignment of unintended attributes", correct=True),
                    opt("Denial of service"),
                ),
                "Strong parameters whitelist attributes, preventing mass-assignment of fields a "
                "user shouldn't set (like `admin: true`).",
            ),
            q(
                "What does `params.require(:product).permit(:name, :price)` do?",
                (
                    opt("Creates a product with name and price"),
                    opt(
                        "Insists on a `product` key and allows only `name` and `price`",
                        correct=True,
                    ),
                    opt("Validates that name and price are present"),
                    opt("Renders a form for name and price"),
                ),
                "`require` insists the `product` hash is present; `permit` whitelists the "
                "allowed attributes and drops the rest.",
            ),
            q(
                "How does `form_with model: @product` decide between POST and PATCH?",
                (
                    opt("It always uses POST"),
                    opt("Based on whether the record is already persisted", correct=True),
                    opt("Based on the current user's role"),
                    opt("You must specify the method manually every time"),
                ),
                "`form_with` POSTs for a new (unsaved) record and PATCHes for a persisted one, "
                "automatically.",
            ),
        ),
        "Views in depth: partials, helpers & layouts": (
            q(
                "What is the recommended way to pass data into a partial?",
                (
                    opt("Global variables"),
                    opt('Locals (e.g. `render "card", product: @product`)', correct=True),
                    opt("Session storage"),
                    opt("Database columns"),
                ),
                "Passing explicit locals keeps partials self-contained and clearer than relying "
                "on instance variables.",
            ),
            q(
                "Where should non-trivial presentation logic in a view go?",
                (
                    opt("Inline in the ERB template"),
                    opt("In a helper method under `app/helpers/`", correct=True),
                    opt("In `config/routes.rb`"),
                    opt("In a migration"),
                ),
                "Helpers move formatting and branching out of templates; views should read like "
                "markup with values dropped in.",
            ),
            q(
                "What does `content_for :sidebar` paired with `yield :sidebar` enable?",
                (
                    opt("Caching the sidebar fragment"),
                    opt(
                        "Capturing content in a view and placing it elsewhere in the layout",
                        correct=True,
                    ),
                    opt("Running JavaScript in the layout"),
                    opt("Validating sidebar data"),
                ),
                "`content_for` captures markup in the view; `yield :name` injects it into the "
                "layout at a chosen spot.",
            ),
        ),
        "Authentication: has_secure_password & sessions": (
            q(
                "What column does `has_secure_password` require?",
                (
                    opt("`password`"),
                    opt("`encrypted_password`"),
                    opt("`password_digest`", correct=True),
                    opt("`password_hash`"),
                ),
                "`has_secure_password` stores the bcrypt hash in a `password_digest` column; the "
                "plaintext password is never saved.",
            ),
            q(
                "How does a Rails app remember that a user is logged in across requests?",
                (
                    opt("By storing the user's password in a cookie"),
                    opt("By storing the user id in the `session`", correct=True),
                    opt("By saving the request to `db/schema.rb`"),
                    opt("By keeping a global variable on the server"),
                ),
                "Storing `session[:user_id]` keeps the user logged in; the session is held in an "
                "encrypted cookie.",
            ),
            q(
                "What does `user.authenticate(password)` return on a wrong password?",
                (
                    opt("`nil`"),
                    opt("`false`", correct=True),
                    opt("The user record"),
                    opt("It raises an exception"),
                ),
                "`authenticate` returns `false` for a wrong password and the user object (truthy) "
                "for the correct one.",
            ),
        ),
        "Querying: scopes, where, order & eager loading": (
            q(
                "What is a scope in Active Record?",
                (
                    opt("A named, reusable, chainable query defined on the model", correct=True),
                    opt("A validation rule"),
                    opt("A type of migration"),
                    opt("A view helper"),
                ),
                "A scope packages a common query as a chainable method, e.g. "
                "`scope :published, -> { where(published: true) }`.",
            ),
            q(
                "What is an N+1 query problem?",
                (
                    opt("Running one query that returns N+1 rows"),
                    opt(
                        "Firing one query for the parents plus one per child record",
                        correct=True,
                    ),
                    opt("A query that exceeds the connection pool"),
                    opt("A migration applied N+1 times"),
                ),
                "N+1 happens when iterating an association fires one extra query per record; "
                "preloading with `includes` fixes it.",
            ),
            q(
                "Which method preloads an association to avoid N+1 queries?",
                (
                    opt("`select`"),
                    opt("`where`"),
                    opt("`includes`", correct=True),
                    opt("`order`"),
                ),
                "`includes(:comments)` preloads the association in a couple of queries instead "
                "of one per record.",
            ),
        ),
    },
    final=(
        q(
            "Which pair of associations models 'a post has many comments'?",
            (
                opt("Post `belongs_to :comments`, Comment `has_many :post`"),
                opt("Post `has_many :comments`, Comment `belongs_to :post`", correct=True),
                opt("Both use `has_many :through`"),
                opt("Post `has_one :comment`, Comment `has_one :post`"),
            ),
            "The parent declares `has_many :comments` and each child declares `belongs_to "
            ":post`, which owns the foreign key.",
        ),
        q(
            "What populates `record.errors` when a save fails?",
            (
                opt("Callbacks"),
                opt("Validations", correct=True),
                opt("Migrations"),
                opt("Scopes"),
            ),
            "Failing validations add messages to the `errors` object, which the form can then "
            "display.",
        ),
        q(
            "Why must you use strong parameters instead of passing raw `params` to `Model.new`?",
            (
                opt("Raw params are slower to read"),
                opt("To prevent mass-assignment of attributes a user shouldn't set", correct=True),
                opt("Because `params` is read-only"),
                opt("To enable eager loading"),
            ),
            "Strong parameters whitelist attributes, blocking mass-assignment attacks like "
            "setting `admin: true`.",
        ),
        q(
            "What does `has_secure_password` use to hash passwords?",
            (
                opt("MD5"),
                opt("Base64 encoding"),
                opt("bcrypt", correct=True),
                opt("Plaintext with a salt column"),
            ),
            "`has_secure_password` hashes passwords with bcrypt and stores only the digest.",
        ),
        q(
            "Which writes a reusable, chainable query on a model?",
            (
                opt("A callback"),
                opt("A scope", correct=True),
                opt("A partial"),
                opt("A layout"),
            ),
            "A scope (`scope :recent, -> { order(created_at: :desc) }`) is a named, chainable "
            "query.",
        ),
        q(
            "What is the single biggest easy win for Rails query performance?",
            (
                opt("Adding more callbacks"),
                opt("Eliminating N+1 queries with eager loading (`includes`)", correct=True),
                opt("Using `save!` instead of `save`"),
                opt("Rendering more partials"),
            ),
            "Preloading associations with `includes` removes N+1 queries, usually the largest "
            "easy performance gain.",
        ),
    ),
)
