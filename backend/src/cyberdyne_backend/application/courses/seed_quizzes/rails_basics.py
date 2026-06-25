"""Quiz spec for the Ruby on Rails — Basics course (per-lesson + final)."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is Rails: MVC & convention over configuration": (
            q(
                "What does Convention over Configuration mean in Rails?",
                (
                    opt("Every project must define its layout in an XML config file"),
                    opt(
                        "Following naming conventions lets Rails wire things up "
                        "with no configuration",
                        correct=True,
                    ),
                    opt("You must configure each model before it can map to a table"),
                    opt("Conventions only apply to controllers, not models or views"),
                ),
                "By following conventions (a `Product` model maps to the `products` table), "
                "Rails wires things up automatically, so you write app code, not plumbing.",
            ),
            q(
                "In MVC, what is the controller's job?",
                (
                    opt("Define the database schema and validations"),
                    opt("Render the final HTML the user sees"),
                    opt(
                        "Receive the request, call models, and pick a view to render",
                        correct=True,
                    ),
                    opt("Store the application's business data"),
                ),
                "The controller is the traffic cop: it handles the request, talks to models, "
                "and chooses which view to render.",
            ),
            q(
                "Which Rails layer is implemented by Active Record?",
                (
                    opt("The View"),
                    opt("The Model", correct=True),
                    opt("The Router"),
                    opt("The Controller"),
                ),
                "Active Record is the Model layer: one class per database table, e.g. "
                "`class Product < ApplicationRecord`.",
            ),
        ),
        "Creating an app: rails new & the directory layout": (
            q(
                "Which command scaffolds a brand-new Rails application named `blog`?",
                (
                    opt("`bin/rails generate blog`"),
                    opt("`rails new blog`", correct=True),
                    opt("`bundle create blog`"),
                    opt("`rails server blog`"),
                ),
                "`rails new blog` scaffolds a complete working application; `bin/rails server` "
                "then boots it.",
            ),
            q(
                "Where do Active Record models live in a Rails app?",
                (
                    opt("`config/models/`"),
                    opt("`db/migrate/`"),
                    opt("`app/models/`", correct=True),
                    opt("`lib/models/`"),
                ),
                "Models live in `app/models/`, one file per table; controllers and views sit "
                "alongside in `app/`.",
            ),
            q(
                "What file lists your application's gem dependencies?",
                (
                    opt("`config/routes.rb`"),
                    opt("`Gemfile`", correct=True),
                    opt("`db/schema.rb`"),
                    opt("`config/database.yml`"),
                ),
                "The `Gemfile` declares dependencies; `bundle install` installs them.",
            ),
        ),
        "Active Record models & migrations": (
            q(
                "What is a migration in Rails?",
                (
                    opt(
                        "A versioned, reversible instruction for changing the schema", correct=True
                    ),
                    opt("A copy of the production database"),
                    opt("A controller action that updates records"),
                    opt("A view that renders database tables"),
                ),
                "Migrations are versioned, reversible steps for changing the schema, applied "
                "with `bin/rails db:migrate`.",
            ),
            q(
                "Given the model class `Product`, what table does Active Record expect?",
                (
                    opt("`Product`"),
                    opt("`product`"),
                    opt("`products`", correct=True),
                    opt("`tbl_products`"),
                ),
                "The class name is singular CamelCase (`Product`); the table is plural "
                "snake_case (`products`).",
            ),
            q(
                "Why should you never edit `db/schema.rb` by hand?",
                (
                    opt("It is encrypted and cannot be edited"),
                    opt(
                        "It is regenerated from migrations; change the DB only through migrations",
                        correct=True,
                    ),
                    opt("Editing it deletes all your data"),
                    opt("It only exists in production"),
                ),
                "`schema.rb` is regenerated from migrations; changing the database through "
                "migrations keeps every environment in sync.",
            ),
        ),
        "Routes & controllers": (
            q(
                "What does `resources :products` generate in `config/routes.rb`?",
                (
                    opt("Only a single GET route for the index"),
                    opt("The seven conventional RESTful routes for the resource", correct=True),
                    opt("A migration to create the products table"),
                    opt("A model class named Product"),
                ),
                "`resources :products` creates the seven RESTful routes (index, new, create, "
                "show, edit, update, destroy).",
            ),
            q(
                "Inside a controller action, where does request data live?",
                (
                    opt("In the `session` object"),
                    opt("In the `params` hash", correct=True),
                    opt("In `db/schema.rb`"),
                    opt("In the `Gemfile`"),
                ),
                "`params` holds request data: route segments, query string, and form body.",
            ),
            q(
                "Which controller action does `GET /products/:id` map to by convention?",
                (
                    opt("`index`"),
                    opt("`create`"),
                    opt("`show`", correct=True),
                    opt("`edit`"),
                ),
                "`GET /products/:id` routes to the `show` action, which renders one record.",
            ),
        ),
        "Views & ERB: layouts and partials": (
            q(
                "What is the difference between `<%= %>` and `<% %>` in ERB?",
                (
                    opt(
                        "`<%= %>` evaluates and prints; `<% %>` evaluates without printing",
                        correct=True,
                    ),
                    opt("`<%= %>` is a comment; `<% %>` runs Ruby"),
                    opt("They are identical"),
                    opt("`<% %>` prints the result; `<%= %>` does not"),
                ),
                "`<%= %>` evaluates Ruby and prints the result; `<% %>` runs Ruby (loops, "
                "conditionals) without printing.",
            ),
            q(
                "In a layout, what does `<%= yield %>` do?",
                (
                    opt("Pauses rendering until the database responds"),
                    opt("Injects the action's view HTML into the layout", correct=True),
                    opt("Renders every partial in the app"),
                    opt("Returns control to the router"),
                ),
                "`yield` is the placeholder in the layout where the rendered view is injected.",
            ),
            q(
                "How does Rails recognise a view file as a partial?",
                (
                    opt("Its name ends in `.partial`"),
                    opt(
                        "Its name starts with an underscore, e.g. `_product.html.erb`", correct=True
                    ),
                    opt("It is stored in `app/partials/`"),
                    opt("It is declared in `config/routes.rb`"),
                ),
                "Partial filenames start with an underscore (`_product.html.erb`) and are "
                "rendered with `render`.",
            ),
        ),
        "The Rails console & generators": (
            q(
                "What does `bin/rails console` give you?",
                (
                    opt("A read-only view of the production logs"),
                    opt(
                        "An interactive session with your whole app and models loaded", correct=True
                    ),
                    opt("A web server on port 3000"),
                    opt("A new migration file"),
                ),
                "The console opens an IRB session with the full app loaded - models, the "
                "database, helpers - ideal for trying Active Record queries.",
            ),
            q(
                "Which generator creates a full CRUD slice (model, migration, controller, "
                "views, routes)?",
                (
                    opt("`bin/rails g model`"),
                    opt("`bin/rails g controller`"),
                    opt("`bin/rails g scaffold`", correct=True),
                    opt("`bin/rails g migration`"),
                ),
                "`scaffold` generates the whole CRUD slice end to end; `destroy scaffold` undoes it.",
            ),
            q(
                "How do you undo files created by a generator?",
                (
                    opt("Delete them manually one by one only"),
                    opt("`bin/rails destroy <generator> <name>`", correct=True),
                    opt("`bin/rails db:rollback`"),
                    opt("`bundle remove`"),
                ),
                "`bin/rails destroy` symmetrically removes whatever the matching `generate` "
                "command created.",
            ),
        ),
    },
    final=(
        q(
            "What are the three layers of Rails' MVC architecture?",
            (
                opt("Module, Variable, Class"),
                opt("Model, View, Controller", correct=True),
                opt("Migration, View, Cache"),
                opt("Method, Validation, Callback"),
            ),
            "Rails is Model-View-Controller: models hold data/logic, views render output, "
            "controllers coordinate.",
        ),
        q(
            "Which command applies pending migrations to the database?",
            (
                opt("`bin/rails db:migrate`", correct=True),
                opt("`bin/rails server`"),
                opt("`bundle install`"),
                opt("`bin/rails console`"),
            ),
            "`bin/rails db:migrate` applies pending migrations; `db:rollback` undoes the last one.",
        ),
        q(
            "What does the router do in Rails?",
            (
                opt("Stores user passwords securely"),
                opt("Maps an HTTP verb and path to a controller action", correct=True),
                opt("Renders ERB templates into HTML"),
                opt("Defines validations on a model"),
            ),
            "The router (`config/routes.rb`) maps each request's verb + path to a controller "
            "action.",
        ),
        q(
            "How do you pass a controller's data into its view?",
            (
                opt("By returning it from the action"),
                opt("By setting instance variables like `@products`", correct=True),
                opt("By writing it to `db/schema.rb`"),
                opt("By storing it in the Gemfile"),
            ),
            "Instance variables set in the action (`@products`) are visible in the rendered view.",
        ),
        q(
            "Given `class Comment < ApplicationRecord`, which table does Rails map it to?",
            (
                opt("`Comment`"),
                opt("`comment`"),
                opt("`comments`", correct=True),
                opt("`tbl_comment`"),
            ),
            "Convention maps the singular CamelCase class `Comment` to the plural snake_case "
            "table `comments`.",
        ),
        q(
            "Which ERB tag prints its evaluated result into the page?",
            (
                opt("`<% %>`"),
                opt("`<%= %>`", correct=True),
                opt("`<%# %>`"),
                opt("`{{ }}`"),
            ),
            "`<%= %>` evaluates Ruby and prints the result; `<% %>` runs code without printing.",
        ),
    ),
)
