"""Curated Ruby on Rails track: Basics, Intermediate, Advanced.

Teaches modern Ruby on Rails (7.x) from MVC fundamentals through Active Record,
controllers and views, on to associations and validations, and finally JSON
APIs, background jobs, Hotwire, performance, testing, and deployment. Rails
cannot run in the Academy interpreter, so all Ruby/ERB/Bash code is illustrative
(you would run it locally with ``bin/rails``); the diagrams use Mermaid to show
the request lifecycle, association schemas, and the Hotwire/job flows.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY (seed_quizzes/rails_*.py) at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


# ── Ruby on Rails — Basics ────────────────────────────────────────────────────

_RAILS_BASICS = SeedCourse(
    slug="rails-basics",
    title="Ruby on Rails — Basics",
    description=(
        "Start building web apps with Rails 7: the MVC pattern and convention "
        "over configuration, scaffolding a new app and its directory layout, "
        "Active Record models and migrations, routes and RESTful controllers, "
        "rendering with ERB views and layouts, and driving everything from the "
        "Rails console and generators - with diagrams and a quiz after each lesson."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is Rails: MVC & convention over configuration",
            "10 min",
            r"""# What is Rails: MVC & convention over configuration

**Ruby on Rails** is a full-stack web framework written in Ruby. It gives you a
database layer, a routing system, controllers, a view/templating engine, and a
mountain of conventions so you write *application* code, not plumbing. Created by
David Heinemeier Hansson in 2004, its two guiding ideas still define it:

- **Convention over Configuration (CoC).** Follow the naming conventions and
  Rails wires things up for you - a `Product` model maps to a `products` table,
  the `ProductsController` renders templates in `app/views/products/`. No XML,
  no config files for the common case.
- **Don't Repeat Yourself (DRY).** Each piece of knowledge lives in one place.

## The MVC request lifecycle

Rails is a **Model-View-Controller** framework. A browser request flows through
the router to a controller action, which talks to a model (the database) and
renders a view back to the browser.

```mermaid
flowchart LR
  Browser["Browser request"] --> Router["Router (config/routes.rb)"]
  Router --> Controller["Controller action"]
  Controller --> Model["Model (Active Record)"]
  Model --> DB[("Database")]
  Model --> Controller
  Controller --> View["View (ERB template)"]
  View --> Browser
```

- **Model** - business logic and data. In Rails that's **Active Record**: one
  class per table, e.g. `class Product < ApplicationRecord`.
- **View** - what the user sees. ERB (`.html.erb`) templates render HTML.
- **Controller** - the traffic cop. It receives the request, calls models, and
  picks a view to render.

## The pieces, named

```ruby
# app/models/product.rb        — the Model
class Product < ApplicationRecord
end

# app/controllers/products_controller.rb — the Controller
class ProductsController < ApplicationController
  def index
    @products = Product.all          # ask the model
  end                                # then render app/views/products/index.html.erb
end
```

> **Why it matters:** because everything has a conventional place, any Rails
> developer can open your project and immediately know where the model, the
> controller, and the view for "products" live. That shared vocabulary is what
> makes Rails teams fast.

**Next:** creating a brand-new app with `rails new` and touring its layout.
""",
        ),
        _t(
            "Creating an app: rails new & the directory layout",
            "10 min",
            r"""# Creating an app: rails new & the directory layout

Rails ships as a gem. Once installed (`gem install rails`), one command
scaffolds an entire working application.

```bash
# Create a new app (Rails 7+ uses importmaps + Hotwire by default)
rails new blog
cd blog

# Boot the development server on http://localhost:3000
bin/rails server         # or: bin/rails s
```

`rails new blog --css=tailwind --database=postgresql` customises the stack;
`--api` produces a slim API-only app (covered in the Advanced course).

## The directory layout

```mermaid
flowchart TD
  ROOT["blog/"] --> APP["app/ — your code"]
  ROOT --> CONFIG["config/ — routes, env, credentials"]
  ROOT --> DB["db/ — migrations & schema"]
  ROOT --> BIN["bin/ — rails, rake, setup"]
  ROOT --> TEST["test/ — tests"]
  APP --> MODELS["models/"]
  APP --> VIEWS["views/"]
  APP --> CONTROLLERS["controllers/"]
  APP --> HELPERS["helpers/"]
```

The folders you live in:

| Path | What goes here |
|------|----------------|
| `app/models/` | Active Record models (one per table) |
| `app/controllers/` | Controllers and their actions |
| `app/views/` | ERB templates, organised by controller |
| `app/helpers/` | View helper methods |
| `app/jobs/` | Background jobs (Active Job) |
| `config/routes.rb` | URL → controller mapping |
| `config/database.yml` | Database connection settings |
| `db/migrate/` | Timestamped migration files |
| `Gemfile` | Your dependencies (gems) |

## Adding a gem

```ruby
# Gemfile
gem "pg"                 # PostgreSQL driver
gem "puma"               # the web server

group :development, :test do
  gem "rspec-rails"
end
```

```bash
bundle install           # install everything in the Gemfile
```

> **Convention in action:** you didn't configure where models or views go -
> Rails already knows. `bin/rails` (the binstub) runs the project-local Rails
> so everyone on the team uses the same version.

**Next:** the M in MVC - Active Record models and migrations.
""",
        ),
        _t(
            "Active Record models & migrations",
            "12 min",
            r"""# Active Record models & migrations

**Active Record** is Rails' ORM (object-relational mapper). A Ruby class maps to
a database table; an instance maps to a row; attributes map to columns. You
rarely write SQL.

## Generating a model

```bash
bin/rails generate model Product name:string price:decimal published:boolean
# short form: bin/rails g model Product name:string price:decimal
```

This creates the model class **and** a migration:

```ruby
# db/migrate/20260101120000_create_products.rb
class CreateProducts < ActiveRecord::Migration[7.1]
  def change
    create_table :products do |t|
      t.string  :name
      t.decimal :price, precision: 10, scale: 2
      t.boolean :published, default: false, null: false

      t.timestamps           # adds created_at and updated_at
    end
  end
end
```

**Migrations** are versioned, reversible instructions for changing the schema.
Run them with:

```bash
bin/rails db:migrate        # apply pending migrations
bin/rails db:rollback       # undo the last one
```

`db/schema.rb` is regenerated to reflect the current schema - it is the source
of truth a fresh checkout loads with `bin/rails db:schema:load`.

## Using the model (CRUD)

```ruby
# Create
product = Product.create(name: "Widget", price: 9.99)

# Read
Product.find(1)              # by primary key (raises if missing)
Product.find_by(name: "Widget")
Product.where(published: true).order(created_at: :desc)

# Update
product.update(price: 12.50)

# Delete
product.destroy
```

## The conventions that make it "just work"

```mermaid
flowchart LR
  Class["class Product"] -->|maps to| Table["products table"]
  Instance["a Product instance"] -->|maps to| Row["one row"]
  Attr["product.name"] -->|maps to| Col["name column"]
```

- Class name is **singular, CamelCase** (`Product`); table is **plural,
  snake_case** (`products`).
- The primary key is `id`; timestamps are `created_at` / `updated_at`.

> **Migrations vs. schema:** never edit `db/schema.rb` by hand. Change the
> database only through migrations so every environment - and every teammate -
> applies the *same* steps in the same order.

**Next:** routing requests to controller actions.
""",
        ),
        _t(
            "Routes & controllers",
            "12 min",
            r"""# Routes & controllers

The **router** maps an incoming HTTP request (verb + path) to a controller
**action** (a public method). It lives in `config/routes.rb`.

```mermaid
flowchart LR
  Req["GET /products/1"] --> Router["routes.rb"]
  Router --> Action["ProductsController#show"]
  Action --> Params["params[:id] == \"1\""]
  Action --> Render["render show.html.erb"]
```

## RESTful resources

One line generates the seven conventional routes for a resource:

```ruby
# config/routes.rb
Rails.application.routes.draw do
  resources :products
  root "products#index"        # GET / → ProductsController#index
end
```

`resources :products` creates:

| HTTP verb | Path | Action | Purpose |
|-----------|------|--------|---------|
| GET | `/products` | `index` | list all |
| GET | `/products/new` | `new` | blank form |
| POST | `/products` | `create` | create one |
| GET | `/products/:id` | `show` | show one |
| GET | `/products/:id/edit` | `edit` | edit form |
| PATCH/PUT | `/products/:id` | `update` | save changes |
| DELETE | `/products/:id` | `destroy` | delete one |

Inspect them anytime with `bin/rails routes`.

## The controller

```ruby
# app/controllers/products_controller.rb
class ProductsController < ApplicationController
  def index
    @products = Product.all
  end

  def show
    @product = Product.find(params[:id])
  end

  def create
    @product = Product.new(name: params[:name])
    if @product.save
      redirect_to @product, notice: "Product created."
    else
      render :new, status: :unprocessable_entity
    end
  end
end
```

Key ideas:

- **`params`** holds the request data (route segments, query string, form body).
- **Instance variables** (`@products`) set in the action are visible in the view.
- An action **renders** a view by convention (`index` → `index.html.erb`) or
  **redirects** to another URL with `redirect_to`.
- Each request gets a fresh controller instance - no state leaks between requests.

> **Path helpers:** `resources` also gives you helpers like `products_path` and
> `product_path(@product)`. Use them instead of hard-coded strings so URLs stay
> correct if routes change.

**Next:** rendering HTML with ERB views.
""",
        ),
        _t(
            "Views & ERB: layouts and partials",
            "10 min",
            r"""# Views & ERB: layouts and partials

A **view** turns controller data into HTML. Rails' default templating language
is **ERB** (Embedded Ruby): plain HTML with Ruby sprinkled in.

```erb
<%# app/views/products/index.html.erb %>
<h1>Products</h1>

<ul>
  <% @products.each do |product| %>
    <li><%= link_to product.name, product_path(product) %> — $<%= product.price %></li>
  <% end %>
</ul>
```

Two ERB tags do almost everything:

- `<%= ... %>` evaluates Ruby **and prints** the result into the page.
- `<% ... %>` evaluates Ruby **without printing** (loops, conditionals).
- `<%# ... %>` is a comment.

## Layouts: the shared shell

Every view is rendered *inside* a layout. The default is
`app/views/layouts/application.html.erb`, and `yield` is where the view's HTML is
injected:

```erb
<%# app/views/layouts/application.html.erb %>
<!DOCTYPE html>
<html>
  <head>
    <title>Blog</title>
    <%= csrf_meta_tags %>
    <%= stylesheet_link_tag "application" %>
  </head>
  <body>
    <%= yield %>          <%# the action's view goes here %>
  </body>
</html>
```

## Partials: reusable view fragments

A **partial** is a view file whose name starts with `_`. Render it to avoid
repetition:

```erb
<%# app/views/products/_product.html.erb %>
<div class="product">
  <h2><%= product.name %></h2>
  <p>$<%= product.price %></p>
</div>
```

```erb
<%# render the collection — Rails infers the _product partial %>
<%= render @products %>

<%# or render one explicitly, passing a local %>
<%= render "product", product: @product %>
```

```mermaid
flowchart TD
  Layout["application.html.erb (layout)"] --> Yield["yield"]
  Yield --> View["index.html.erb"]
  View --> Partial["_product.html.erb (rendered per item)"]
```

> **DRY views:** push any repeated markup into a partial and any non-trivial
> logic into a **helper** (`app/helpers/`). Keep templates focused on
> presentation, not computation.

**Next:** exploring it all live with the console and generators.
""",
        ),
        _t(
            "The Rails console & generators",
            "10 min",
            r"""# The Rails console & generators

Two tools make Rails fast to learn and build with: an interactive console wired
into your app, and generators that write boilerplate for you.

## The Rails console

`bin/rails console` (or `bin/rails c`) opens an IRB session with your whole app
loaded - models, helpers, the database, everything.

```bash
bin/rails console
```

```ruby
# Inside the console — full access to your models:
Product.count
#=> 3

p = Product.create(name: "Gadget", price: 19.99)
#=> #<Product id: 4, name: "Gadget", ...>

Product.where("price > ?", 10).pluck(:name)
#=> ["Widget", "Gadget"]

# Use the sandbox to roll back everything you do on exit:
# bin/rails console --sandbox
```

It is the best way to learn Active Record: try a query, see the SQL Rails
generates, and inspect the result immediately.

## Generators

Generators scaffold files following all the conventions.

```bash
# A controller with given actions + matching views
bin/rails g controller Pages home about

# A migration only (no model)
bin/rails g migration AddStockToProducts stock:integer

# The big one: a full CRUD slice (model + migration + controller + views + routes)
bin/rails g scaffold Article title:string body:text
bin/rails db:migrate
```

`scaffold` is the fastest way to see a working CRUD feature end to end.
Generated something by mistake? Undo it symmetrically:

```bash
bin/rails destroy scaffold Article
```

## The everyday loop

```mermaid
flowchart LR
  Gen["bin/rails g ..."] --> Migrate["bin/rails db:migrate"]
  Migrate --> Console["bin/rails console (poke the model)"]
  Console --> Server["bin/rails server (see it in the browser)"]
  Server --> Gen
```

> **Generators are a starting point, not a cage.** Scaffold to learn the shape
> of a feature, then delete the parts you don't need and write the rest by hand.
> Read the generated code - it teaches you the conventions.

**Next (Intermediate course):** wiring models together with associations.
""",
        ),
    ),
)


# ── Ruby on Rails — Intermediate ──────────────────────────────────────────────

_RAILS_INTERMEDIATE = SeedCourse(
    slug="rails-intermediate",
    title="Ruby on Rails — Intermediate",
    description=(
        "Go beyond CRUD: Active Record associations (has_many, belongs_to, "
        "has_many :through), validations and callbacks, strong parameters and "
        "form_with, views in depth with partials and helpers, building "
        "authentication with has_secure_password and sessions, and querying with "
        "scopes, where/order, and eager loading - with diagrams and quizzes."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Associations: has_many, belongs_to, has_many :through",
            "12 min",
            r"""# Associations: has_many, belongs_to, has_many :through

Real apps have **related** data. Active Record **associations** declare those
relationships so you can navigate them with method calls instead of SQL joins.

## The one-to-many pair

A blog post has many comments; each comment belongs to one post.

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  has_many :comments, dependent: :destroy
end

# app/models/comment.rb
class Comment < ApplicationRecord
  belongs_to :post
end
```

The `belongs_to` side owns the **foreign key**. Add it in a migration:

```ruby
class CreateComments < ActiveRecord::Migration[7.1]
  def change
    create_table :comments do |t|
      t.references :post, null: false, foreign_key: true   # adds post_id + index
      t.text :body
      t.timestamps
    end
  end
end
```

Now navigation is trivial:

```ruby
post = Post.first
post.comments              # all comments for this post
post.comments.create(body: "Nice!")
comment.post               # back to the parent
```

## Many-to-many with has_many :through

A doctor has many patients through appointments, and vice versa. The **join
model** carries the relationship (and any extra columns, like the appointment
time):

```ruby
class Doctor < ApplicationRecord
  has_many :appointments
  has_many :patients, through: :appointments
end

class Appointment < ApplicationRecord
  belongs_to :doctor
  belongs_to :patient
end

class Patient < ApplicationRecord
  has_many :appointments
  has_many :doctors, through: :appointments
end
```

```mermaid
erDiagram
  DOCTOR ||--o{ APPOINTMENT : has
  PATIENT ||--o{ APPOINTMENT : has
  DOCTOR {
    int id
    string name
  }
  PATIENT {
    int id
    string name
  }
  APPOINTMENT {
    int id
    int doctor_id
    int patient_id
    datetime scheduled_at
  }
```

```ruby
doctor.patients            # everyone this doctor sees, via appointments
patient.doctors            # the reverse, for free
```

> **`dependent:` matters.** `has_many :comments, dependent: :destroy` deletes a
> post's comments when the post is destroyed; without it you orphan rows. Prefer
> `has_many :through` over the older `has_and_belongs_to_many` so the join table
> is a real model you can extend.

**Next:** keeping data correct with validations and callbacks.
""",
        ),
        _t(
            "Validations & callbacks",
            "11 min",
            r"""# Validations & callbacks

**Validations** keep bad data out of the database. They run automatically on
`save`, `create`, and `update`, and populate an `errors` object when they fail.

```ruby
class User < ApplicationRecord
  validates :email, presence: true,
                    uniqueness: { case_sensitive: false },
                    format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :name, presence: true, length: { minimum: 2, maximum: 50 }
  validates :age, numericality: { greater_than_or_equal_to: 0 }, allow_nil: true
end
```

Checking the result:

```ruby
user = User.new(email: "")
user.save                  #=> false (validation failed)
user.valid?                #=> false
user.errors.full_messages  #=> ["Email can't be blank", "Name can't be blank"]

user.save!                 # the bang version raises on failure
```

`save` returns `true`/`false`; the bang versions (`save!`, `create!`) raise
`ActiveRecord::RecordInvalid`. Use the bang form when failure is exceptional.

## Custom validations

```ruby
class Event < ApplicationRecord
  validate :ends_after_it_starts

  private

  def ends_after_it_starts
    return if ends_at.blank? || starts_at.blank?
    errors.add(:ends_at, "must be after the start time") if ends_at <= starts_at
  end
end
```

## Callbacks: hooks in the lifecycle

**Callbacks** run code at points in an object's life - before validation, before
save, after create, and so on.

```mermaid
flowchart LR
  New["new / build"] --> BV["before_validation"]
  BV --> Valid["validations"]
  Valid --> BS["before_save"]
  BS --> Write["INSERT / UPDATE"]
  Write --> AS["after_save"]
  AS --> AC["after_commit"]
```

```ruby
class User < ApplicationRecord
  before_validation :normalize_email
  after_create_commit :send_welcome_email

  private

  def normalize_email
    self.email = email.to_s.strip.downcase
  end

  def send_welcome_email
    WelcomeMailer.with(user: self).welcome.deliver_later
  end
end
```

> **Use callbacks sparingly.** They're great for normalising data
> (`before_validation`), but heavy side effects (emails, external APIs) hidden in
> callbacks make models hard to reason about. Prefer `after_commit` for side
> effects so they only fire once the transaction actually succeeds, and consider
> moving complex logic into a service object.

**Next:** safely accepting user input - strong parameters and forms.
""",
        ),
        _t(
            "Strong parameters & forms",
            "11 min",
            r"""# Strong parameters & forms

Web forms send user-controlled data. **Strong parameters** force you to
explicitly list which attributes a controller will accept - blocking
**mass-assignment** attacks where a malicious user sets fields you never
intended (like `admin: true`).

## The pattern

```ruby
class ProductsController < ApplicationController
  def create
    @product = Product.new(product_params)
    if @product.save
      redirect_to @product, notice: "Created."
    else
      render :new, status: :unprocessable_entity
    end
  end

  def update
    @product = Product.find(params[:id])
    if @product.update(product_params)
      redirect_to @product
    else
      render :edit, status: :unprocessable_entity
    end
  end

  private

  # require the :product key, permit only these attributes
  def product_params
    params.require(:product).permit(:name, :price, :published)
  end
end
```

- **`require(:product)`** insists the params contain a `product` hash.
- **`permit(...)`** whitelists the attributes; anything else is silently dropped.

## Building the form with form_with

`form_with` builds a form bound to a model. It knows whether to POST (create) or
PATCH (update) based on whether the record is already saved.

```erb
<%# app/views/products/_form.html.erb %>
<%= form_with model: @product do |form| %>
  <% if @product.errors.any? %>
    <div class="errors">
      <h2><%= pluralize(@product.errors.count, "error") %> stopped this save:</h2>
      <ul>
        <% @product.errors.full_messages.each do |msg| %>
          <li><%= msg %></li>
        <% end %>
      </ul>
    </div>
  <% end %>

  <div>
    <%= form.label :name %>
    <%= form.text_field :name %>
  </div>
  <div>
    <%= form.label :price %>
    <%= form.number_field :price, step: 0.01 %>
  </div>

  <%= form.submit %>
<% end %>
```

This generates fields named `product[name]`, `product[price]`, ... - exactly the
nested structure `params.require(:product).permit(...)` expects.

```mermaid
flowchart LR
  Form["form_with (product[name]=...)"] --> Submit["POST /products"]
  Submit --> Controller["create action"]
  Controller --> SP["product_params (require + permit)"]
  SP --> Save["@product.save"]
```

> **Security default:** strong parameters are mandatory in Rails for a reason -
> never pass raw `params` to `Model.new`. Permit nested attributes explicitly
> too: `permit(:name, tags: [], variant_attributes: [:size, :color])`.

**Next:** views in depth - partials, helpers, and layouts.
""",
        ),
        _t(
            "Views in depth: partials, helpers & layouts",
            "10 min",
            r"""# Views in depth: partials, helpers & layouts

You met partials, helpers, and layouts in Basics. Here's how to use them well so
your views stay clean as the app grows.

## Partials with locals (and a collection)

Pass data into a partial as **locals** - explicit beats relying on instance
variables:

```erb
<%# app/views/products/_card.html.erb %>
<article class="card">
  <h3><%= product.name %></h3>
  <p class="price"><%= number_to_currency(product.price) %></p>
  <% if highlight %>
    <span class="badge">Featured</span>
  <% end %>
</article>
```

```erb
<%# render one with locals %>
<%= render "card", product: @product, highlight: true %>

<%# render a collection efficiently (Rails caches the lookup) %>
<%= render partial: "card", collection: @products, as: :product, locals: { highlight: false } %>
```

## Helpers: logic out of templates

Helper methods live in `app/helpers/` and are available in every view. Move any
formatting or branching out of ERB:

```ruby
# app/helpers/products_helper.rb
module ProductsHelper
  def stock_badge(product)
    if product.stock.zero?
      content_tag(:span, "Sold out", class: "badge badge-red")
    else
      content_tag(:span, "In stock", class: "badge badge-green")
    end
  end
end
```

```erb
<%= stock_badge(@product) %>
```

Built-in helpers do a lot already: `link_to`, `form_with`, `number_to_currency`,
`pluralize`, `time_ago_in_words`, `truncate`, `image_tag`.

## Multiple layouts and content_for

A layout can capture content from a view with `content_for`/`yield(:name)`:

```erb
<%# in a view %>
<% content_for :sidebar do %>
  <nav>...</nav>
<% end %>
```

```erb
<%# in the layout %>
<aside><%= yield :sidebar %></aside>
<main><%= yield %></main>
```

```mermaid
flowchart TD
  Action["controller action"] --> Layout["layout (yield, yield :sidebar)"]
  Layout --> View["view template"]
  View --> P1["_card partial (per product)"]
  View --> H1["helper methods"]
```

> **A clean view does no thinking.** If an ERB template has `if/else` branches or
> calculations, that logic belongs in a **helper** (presentation) or the
> **model/decorator** (domain). Templates should read like markup with values
> dropped in.

**Next:** letting users sign in - authentication.
""",
        ),
        _t(
            "Authentication: has_secure_password & sessions",
            "12 min",
            r"""# Authentication: has_secure_password & sessions

Authentication answers "who is this user?" Rails gives you the cryptographic
pieces to build it yourself with **`has_secure_password`**, backed by **sessions**
for staying logged in.

## Storing passwords safely

Never store plaintext passwords. `has_secure_password` hashes them with **bcrypt**
and gives you an `authenticate` method.

```ruby
# Gemfile
gem "bcrypt"
```

```ruby
# A migration adds a password_digest column (note the name):
# bin/rails g migration AddPasswordDigestToUsers password_digest:string

class User < ApplicationRecord
  has_secure_password           # requires a password_digest column

  validates :email, presence: true, uniqueness: { case_sensitive: false }
end
```

```ruby
user = User.create(email: "a@b.com", password: "secret", password_confirmation: "secret")
user.authenticate("wrong")     #=> false
user.authenticate("secret")    #=> the user (truthy)
```

`password` and `password_confirmation` are virtual attributes; only the bcrypt
**digest** is ever stored.

## Sessions: staying logged in

A **session** is per-user server-side state keyed by an encrypted cookie. Log a
user in by storing their id; log out by clearing it.

```ruby
class SessionsController < ApplicationController
  def create
    user = User.find_by(email: params[:email].to_s.downcase)
    if user&.authenticate(params[:password])
      session[:user_id] = user.id          # logged in
      redirect_to root_path, notice: "Welcome back!"
    else
      flash.now[:alert] = "Invalid email or password"
      render :new, status: :unprocessable_entity
    end
  end

  def destroy
    session.delete(:user_id)               # logged out
    redirect_to root_path
  end
end
```

A helper exposes the current user everywhere:

```ruby
class ApplicationController < ActionController::Base
  helper_method :current_user

  private

  def current_user
    @current_user ||= User.find_by(id: session[:user_id])
  end

  def require_login
    redirect_to login_path, alert: "Please sign in" unless current_user
  end
end
```

```mermaid
flowchart LR
  Login["POST /login (email, password)"] --> Auth["user.authenticate(password)"]
  Auth -->|ok| Session["session[:user_id] = user.id"]
  Session --> Cookie["encrypted session cookie"]
  Cookie --> Next["current_user on every request"]
```

> **Roll your own only to learn it.** In production most teams reach for
> **Devise** (or Rails 8's built-in authentication generator), which bundles
> sign-up, password reset, lockout, and confirmation. But knowing the
> `has_secure_password` + `session` mechanism underneath makes those gems far
> less mysterious.

**Next:** asking the database good questions - querying.
""",
        ),
        _t(
            "Querying: scopes, where, order & eager loading",
            "11 min",
            r"""# Querying: scopes, where, order & eager loading

Active Record's query interface builds SQL from chained Ruby methods. The chain
is **lazy** - no query runs until you actually need the data.

## The building blocks

```ruby
Product.where(published: true)                 # WHERE published = true
Product.where("price > ?", 10)                 # bound parameter (safe from SQL injection)
Product.where(category: %w[books toys])        # WHERE category IN (...)
Product.where.not(category: "books")
Product.order(created_at: :desc).limit(5)
Product.select(:id, :name)
Product.find_each { |p| ... }                  # batches, for large tables

Product.count
Product.sum(:price)
Product.group(:category).count                 #=> {"books"=>3, "toys"=>5}
```

Chaining returns an `ActiveRecord::Relation`, so you compose freely:

```ruby
Product.where(published: true).where("price < ?", 50).order(:name)
```

## Scopes: named, reusable queries

A **scope** packages a common query as a method on the model:

```ruby
class Product < ApplicationRecord
  scope :published, -> { where(published: true) }
  scope :cheaper_than, ->(amount) { where("price < ?", amount) }
  scope :recent, -> { order(created_at: :desc) }
end

Product.published.cheaper_than(50).recent     # reads like English, composes like SQL
```

## The N+1 problem and eager loading

Iterating an association without preloading fires **one query per record** - the
infamous **N+1**:

```ruby
# BAD: 1 query for posts + N queries (one per post) for comments
Post.all.each { |post| puts post.comments.count }

# GOOD: 2 queries total — includes preloads the association
Post.includes(:comments).each { |post| puts post.comments.size }
```

```mermaid
flowchart TD
  Bad["Post.all (1 query)"] --> Loop["loop over N posts"]
  Loop --> NQ["+ N queries for comments (N+1!)"]
  Good["Post.includes(:comments)"] --> Two["2 queries total, preloaded"]
```

`includes` lets Rails decide between a separate preload query and a `LEFT JOIN`;
`preload` forces separate queries; `eager_load` forces the join (needed when you
filter on the associated table).

> **Find N+1 before users do.** Add the **Bullet** gem in development - it warns
> in the browser whenever a query pattern would benefit from `includes`. Eager
> loading is the single biggest easy win for Rails performance.

**Next (Advanced course):** exposing your data as a JSON API.
""",
        ),
    ),
)


# ── Ruby on Rails — Advanced ──────────────────────────────────────────────────

_RAILS_ADVANCED = SeedCourse(
    slug="rails-advanced",
    title="Ruby on Rails — Advanced",
    description=(
        "Ship production Rails 7: build a JSON API (API-only mode, jbuilder), "
        "run work off-request with Active Job and Sidekiq, add realtime with "
        "Hotwire (Turbo & Stimulus) over Action Cable, kill N+1s and cache with "
        "Russian-doll fragments, test with Minitest and RSpec, and deploy "
        "securely with Puma, encrypted credentials, and CSRF protection."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Building a JSON API",
            "12 min",
            r"""# Building a JSON API

Rails makes a great backend for mobile apps and SPAs. Generate a slim,
**API-only** app that drops views and browser middleware:

```bash
rails new storefront --api
```

An API-only `ApplicationController` inherits from `ActionController::API` - no
cookies, no flash, no view layer, just the bits an API needs.

## A JSON controller

```ruby
# app/controllers/api/v1/products_controller.rb
module Api
  module V1
    class ProductsController < ApplicationController
      def index
        products = Product.published.order(:name)
        render json: products
      end

      def show
        product = Product.find(params[:id])
        render json: product
      end

      def create
        product = Product.new(product_params)
        if product.save
          render json: product, status: :created, location: api_v1_product_url(product)
        else
          render json: { errors: product.errors.full_messages },
                 status: :unprocessable_entity
        end
      end

      private

      def product_params
        params.require(:product).permit(:name, :price, :published)
      end
    end
  end
end
```

Namespace the routes to keep versions tidy:

```ruby
# config/routes.rb
namespace :api do
  namespace :v1 do
    resources :products
  end
end
```

## Shaping the JSON with jbuilder

`render json: product` calls `to_json`. For control over the exact shape, use
**jbuilder** (a view template for JSON) or a serializer:

```ruby
# app/views/api/v1/products/show.json.jbuilder
json.id     @product.id
json.name   @product.name
json.price  @product.price.to_f
json.reviews @product.reviews do |review|
  json.rating review.rating
  json.body   review.body
end
```

```mermaid
flowchart LR
  Client["API client / SPA"] --> Route["api/v1/products"]
  Route --> Ctrl["Api::V1::ProductsController"]
  Ctrl --> Model["Product (Active Record)"]
  Ctrl --> JSON["jbuilder / serializer"]
  JSON --> Client
```

> **Version from day one.** Namespacing under `/api/v1` lets you ship a `v2`
> later without breaking existing clients. Return proper status codes
> (`:created`, `:unprocessable_entity`, `:not_found`) - clients rely on them far
> more than on the response body.

**Next:** doing slow work off the request - background jobs.
""",
        ),
        _t(
            "Active Job & background processing",
            "11 min",
            r"""# Active Job & background processing

Slow work - sending email, calling an API, resizing an image - should never
block an HTTP response. **Active Job** is Rails' queuing abstraction; you write
the job once and run it on a backend like **Sidekiq**, GoodJob, or Solid Queue.

## Defining and enqueuing a job

```ruby
# bin/rails g job ProcessUpload
class ProcessUploadJob < ApplicationJob
  queue_as :default

  retry_on Net::OpenTimeout, wait: :polynomially_longer, attempts: 5
  discard_on ActiveJob::DeserializationError

  def perform(upload_id)
    upload = Upload.find(upload_id)
    upload.process!            # the slow part — runs off the web request
  end
end
```

```ruby
# Enqueue it (returns immediately, work happens later):
ProcessUploadJob.perform_later(upload.id)

# Or schedule it:
ProcessUploadJob.set(wait: 5.minutes).perform_later(upload.id)
```

> **Pass ids, not objects.** Jobs are serialised to the queue; pass `upload.id`
> and look it up in `perform`, so the worker reads fresh data (Active Job's
> GlobalID does this for you when you pass a record, but ids are explicit and safe).

## The flow

```mermaid
flowchart LR
  Req["controller action"] --> Enq["Job.perform_later(id)"]
  Enq --> Queue[("Redis queue")]
  Queue --> Worker["Sidekiq worker process"]
  Worker --> Perform["job.perform — the slow work"]
  Req -->|responds immediately| User["user"]
```

## Wiring up Sidekiq

```ruby
# Gemfile
gem "sidekiq"
```

```ruby
# config/application.rb
config.active_job.queue_adapter = :sidekiq
```

```bash
# Sidekiq needs Redis; run a worker process alongside your web server:
bundle exec sidekiq
```

Common Active Job uses: `deliver_later` for mailers (it enqueues a job),
scheduled cleanups, webhooks, and any third-party API call.

> **Idempotency wins.** A job can run twice (retries, crashes). Write `perform`
> so running it again is harmless - check "already done?" before doing the work,
> or use a unique lock. Monitor the queue (Sidekiq's web UI) so backlogs don't
> hide.

**Next:** pushing updates to the browser in realtime - Hotwire.
""",
        ),
        _t(
            "Hotwire: Turbo & Stimulus for realtime",
            "12 min",
            r"""# Hotwire: Turbo & Stimulus for realtime

**Hotwire** is Rails' default approach to rich, fast UIs without a heavy
JavaScript framework. It ships HTML over the wire instead of JSON. Three parts:
**Turbo Drive**, **Turbo Frames**, **Turbo Streams**, plus **Stimulus** for the
sprinkles of JS you still need.

## Turbo Frames: independent page regions

Wrap part of a page in a frame and links/forms inside it update *only* that
region:

```erb
<%# app/views/products/show.html.erb %>
<%= turbo_frame_tag "inventory" do %>
  <p>In stock: <%= @product.stock %></p>
  <%= link_to "Refresh", product_path(@product) %>
<% end %>
```

## Turbo Streams: server-pushed DOM updates

A controller can respond with **Turbo Stream** actions that append, replace, or
remove DOM nodes - perfect for realtime over **Action Cable** (WebSockets).

```ruby
# app/models/comment.rb
class Comment < ApplicationRecord
  belongs_to :post
  # broadcast to everyone subscribed to this post's stream
  after_create_commit { broadcast_append_to post, target: "comments" }
end
```

```erb
<%# subscribe the page to the stream %>
<%= turbo_stream_from @post %>

<div id="comments">
  <%= render @post.comments %>
</div>
```

Now when *any* user adds a comment, every viewer's `#comments` list gets the new
node appended over a WebSocket - no page reload, no custom JS.

```mermaid
flowchart LR
  User1["User A submits comment"] --> Save["Comment.create"]
  Save --> Broadcast["after_create_commit → broadcast_append_to"]
  Broadcast --> Cable["Action Cable (WebSocket)"]
  Cable --> User1b["User A browser"]
  Cable --> User2["User B browser"]
```

## Stimulus: modest JavaScript

For client-side behaviour, **Stimulus** connects small controllers to your HTML
via `data-` attributes:

```javascript
// app/javascript/controllers/toggle_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["content"]

  toggle() {
    this.contentTarget.classList.toggle("hidden")
  }
}
```

```erb
<div data-controller="toggle">
  <button data-action="click->toggle#toggle">Details</button>
  <div data-toggle-target="content" class="hidden">...</div>
</div>
```

> **Reach for JSON only when you need it.** For server-rendered Rails apps,
> Turbo gives you SPA-like speed with plain controllers and ERB. Keep Stimulus
> controllers tiny and behavioural; if you're rebuilding lots of state in JS,
> that's a signal you actually want an API + frontend framework instead.

**Next:** making it fast - performance and caching.
""",
        ),
        _t(
            "Performance: N+1, includes & caching",
            "11 min",
            r"""# Performance: N+1, includes & caching

Two techniques cover most Rails performance work: eliminating **N+1 queries** and
**caching** rendered output.

## Killing N+1 with includes

As seen in the Intermediate course, looping an association without preloading
fires one query per record. Preload with `includes`:

```ruby
# BAD — N+1
@posts = Post.all
# in the view: post.author.name and post.comments.size → extra queries each

# GOOD — preload both associations up front
@posts = Post.includes(:author, :comments)
```

Detect them automatically with the **Bullet** gem in development; for nested
associations preload deeply: `includes(comments: :author)`.

## Fragment caching

Cache a rendered chunk of a view keyed by the record. When the record changes,
its `updated_at` changes, the cache key changes, and Rails re-renders just that
fragment:

```erb
<% cache @product do %>
  <article>
    <h2><%= @product.name %></h2>
    <p><%= number_to_currency(@product.price) %></p>
  </article>
<% end %>
```

## Russian-doll caching

Nest caches so an inner change only busts the inner fragment, while the outer
fragment reuses the unchanged inner ones. Set up `touch` so a child change
bumps the parent's `updated_at`:

```ruby
class Comment < ApplicationRecord
  belongs_to :post, touch: true     # editing a comment touches the post
end
```

```erb
<% cache @post do %>                    <%# outer doll %>
  <h1><%= @post.title %></h1>
  <% @post.comments.each do |comment| %>
    <% cache comment do %>              <%# inner dolls %>
      <%= render comment %>
    <% end %>
  <% end %>
<% end %>
```

```mermaid
flowchart TD
  Outer["cache @post (outer doll)"] --> Inner1["cache comment 1"]
  Outer --> Inner2["cache comment 2"]
  Inner2 --> Edit["edit comment 2 → touch: true bumps post.updated_at"]
  Edit --> Rebuild["only comment 2 + outer wrapper re-render"]
```

Other levers: `counter_cache` to avoid `COUNT` queries, database indexes on
columns you filter/sort by, and a low-level cache for expensive computations:

```ruby
Rails.cache.fetch("stats/top_products", expires_in: 1.hour) do
  Product.expensive_ranking      # runs only on a cache miss
end
```

> **Measure first.** Use the development log (it prints every query and its time)
> and tools like `rack-mini-profiler` to find the real bottleneck. Most slowness
> is N+1 queries or a missing index - fix those before reaching for caching.

**Next:** proving it works - testing.
""",
        ),
        _t(
            "Testing: Minitest & RSpec",
            "12 min",
            r"""# Testing: Minitest & RSpec

Rails takes testing seriously. It ships with **Minitest** built in; many teams
prefer **RSpec**. Both test the same layers - models, controllers/requests,
systems (end-to-end in a browser).

## Minitest (the default)

Tests live under `test/`; fixtures provide sample data.

```ruby
# test/models/product_test.rb
require "test_helper"

class ProductTest < ActiveSupport::TestCase
  test "is invalid without a name" do
    product = Product.new(price: 1)
    assert_not product.valid?
    assert_includes product.errors[:name], "can't be blank"
  end

  test "published scope returns only published products" do
    assert_equal [products(:widget)], Product.published.to_a
  end
end
```

```yaml
# test/fixtures/products.yml
widget:
  name: Widget
  price: 9.99
  published: true
```

Run the suite:

```bash
bin/rails test                 # all tests
bin/rails test test/models     # one directory
```

## RSpec + factories

```ruby
# Gemfile
group :development, :test do
  gem "rspec-rails"
  gem "factory_bot_rails"
end
```

```ruby
# spec/models/product_spec.rb
require "rails_helper"

RSpec.describe Product, type: :model do
  it "is invalid without a name" do
    product = build(:product, name: nil)
    expect(product).not_to be_valid
    expect(product.errors[:name]).to include("can't be blank")
  end
end
```

```ruby
# spec/factories/products.rb — factories beat fixtures for flexibility
FactoryBot.define do
  factory :product do
    sequence(:name) { |n| "Product #{n}" }
    price { 9.99 }
    published { true }
  end
end
```

## Request and system specs

```ruby
# A request spec hits the full controller stack
RSpec.describe "Products API", type: :request do
  it "returns published products as JSON" do
    create(:product, name: "Widget")
    get "/api/v1/products"
    expect(response).to have_http_status(:ok)
    expect(response.parsed_body.first["name"]).to eq("Widget")
  end
end
```

```mermaid
flowchart TD
  Unit["model specs (fast, isolated)"] --> Req["request specs (controller + routes)"]
  Req --> Sys["system specs (real browser, slow)"]
  Sys --> CI["CI: run on every push"]
```

> **Fixtures vs. factories:** fixtures are fast but rigid; **factories**
> (`build` doesn't hit the DB, `create` does) make intent clear and let each test
> set up exactly the data it needs. Either way, lean on fast model/request tests
> and reserve slow system tests for critical user flows.

**Next:** getting it live - deployment and security.
""",
        ),
        _t(
            "Deployment & security",
            "11 min",
            r"""# Deployment & security

Shipping Rails means running it under a production web server, managing secrets,
and keeping the security defaults switched on.

## Puma: the application server

Rails runs on **Puma**, a multi-threaded (and optionally multi-process) server,
configured in `config/puma.rb`. In front of it you typically put Nginx (or a
platform's load balancer) for TLS and static files.

```ruby
# config/puma.rb (essentials)
workers Integer(ENV.fetch("WEB_CONCURRENCY", 2))    # processes
threads 5, 5                                          # threads per process
preload_app!
```

## Encrypted credentials

Secrets (API keys, the secret key base) go in an **encrypted** file, not in the
repo. Rails encrypts `config/credentials.yml.enc` with `config/master.key`.

```bash
# Edit secrets (decrypts in your editor, re-encrypts on save):
bin/rails credentials:edit
```

```ruby
# config/credentials.yml.enc (decrypted view)
secret_key_base: 3a1f...        # generated for you
aws:
  access_key_id: AKIA...
  secret_access_key: ...
```

```ruby
# Read them anywhere:
Rails.application.credentials.aws[:access_key_id]
```

> **Never commit `master.key`.** It's gitignored by default; provide it in
> production via the `RAILS_MASTER_KEY` environment variable. Lose it and you
> lose access to every secret in the file.

## The security defaults to keep on

```mermaid
flowchart LR
  Req["incoming request"] --> CSRF["CSRF token check (forms)"]
  CSRF --> SP["strong params (mass-assignment guard)"]
  SP --> SQL["bound params (SQL-injection safe)"]
  SQL --> Action["controller action"]
```

- **CSRF protection** - `protect_from_forgery` is on by default; `form_with`
  injects the token, and `csrf_meta_tags` exposes it to Turbo/JS. (API-only apps
  use token/JWT auth instead of cookies.)
- **Strong parameters** - always `require`/`permit`; never mass-assign raw params.
- **SQL injection** - use bound parameters (`where("price > ?", x)`), never string
  interpolation.
- **Force HTTPS** - `config.force_ssl = true` in production.
- **Escaping** - ERB auto-escapes output; only use `raw`/`html_safe` on content
  you fully trust.

## A typical deploy

```bash
# Precompile assets, run migrations, then boot Puma:
RAILS_ENV=production bin/rails assets:precompile
RAILS_ENV=production bin/rails db:migrate
RAILS_ENV=production bin/rails server
```

Modern options: **Kamal** (Rails' own Docker-based deploy tool), Heroku, Fly.io,
or a PaaS. Whatever the host, the checklist is the same: set `RAILS_MASTER_KEY`,
run migrations, precompile assets, run multiple Puma workers, and put TLS in
front.

> **Production is a config, not a hope.** Set `config.force_ssl`, real database
> pooling, log levels, and a `WEB_CONCURRENCY` that matches your CPU. Run the
> **brakeman** gem in CI to catch security regressions before they ship.

**Next:** the final check.
""",
        ),
    ),
)


RAILS_COURSES = (_RAILS_BASICS, _RAILS_INTERMEDIATE, _RAILS_ADVANCED)

__all__ = ["RAILS_COURSES"]
