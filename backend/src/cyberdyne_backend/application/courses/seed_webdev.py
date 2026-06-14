"""Academy seed content — the Web Development track (Beginner → Advanced).

* ``webdev-basics``        — how the web works, HTML, CSS, JavaScript, the DOM, forms
* ``webdev-intermediate``  — SPAs vs SSR, frameworks, REST APIs, auth, ORMs
* ``webdev-advanced``      — performance, caching, security, GraphQL, real-time, scaling

The web's own languages (HTML/CSS/JS) appear as read-only illustrative blocks,
while runnable ``code`` lessons use Python (the sandbox language) to build the
*logic* behind the web — query-string parsing, a template renderer, a REST
router, request validation, and HTML escaping to stop XSS.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, ×) in diagrams and labels.
# ruff: noqa: RUF001, RUF003

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# webdev-basics
# ──────────────────────────────────────────────────────────────────────

_WEB_BASICS = SeedCourse(
    slug="webdev-basics",
    title="Web Development — Basics",
    description=(
        "Build for the web from first principles: how a page actually loads, the "
        "three core languages — HTML for structure, CSS for style, JavaScript "
        "for behaviour — the DOM, and forms. With runnable labs that build the "
        "logic behind query strings and templating."
    ),
    level="Beginner",
    lessons=(
        _t(
            "How the web works",
            "10 min",
            r"""# How the web works

Before writing a line of code, picture what happens when you open a page. You
type `cyberdynecorp.ai`; in under a second:

1. **DNS** turns the name into an IP address (Networking track).
2. Your browser opens a connection (TCP + **TLS** for HTTPS) and sends an
   **HTTP request**: `GET / HTTP/1.1`.
3. A **server** responds with an **HTTP response** — a status code and a body,
   usually an **HTML** document.
4. The browser **parses the HTML**, discovers it needs more files (CSS,
   JavaScript, images) and fetches each with more requests.
5. It builds the **DOM** (the page's tree), applies **CSS** to style it, runs
   **JavaScript** to make it interactive, and **paints** pixels to the screen.

Two roles, always:

- **Frontend (client-side)** — what runs in the browser: HTML, CSS, JavaScript.
  It's about presentation and interaction.
- **Backend (server-side)** — what runs on the server: application code and
  databases that produce the data and HTML. It's about logic, storage, and
  security.

They talk over **HTTP**, the request/response protocol that underpins everything
(methods like GET/POST, status codes like 200/404, headers, and a body). HTTP is
**stateless** — each request stands alone — so apps track who you are with
**cookies** or tokens.

The three frontend languages divide cleanly, and keeping them separate is the
foundation of maintainable web work:

- **HTML** — *structure & content* (the nouns).
- **CSS** — *presentation* (the looks).
- **JavaScript** — *behaviour* (the verbs).

You'll learn each in turn, then how the backend serves them.
""",
        ),
        _t(
            "HTML: structure & semantics",
            "10 min",
            r"""# HTML: structure & semantics

**HTML** (HyperText Markup Language) describes the **structure and content** of a
page using **elements** written as **tags**. An element usually has an opening
tag, content, and a closing tag, and can carry **attributes**:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>My Page</title>
  </head>
  <body>
    <h1>Welcome</h1>
    <p>A paragraph with a <a href="/courses">link</a>.</p>
    <img src="logo.png" alt="Company logo" />
  </body>
</html>
```

Elements **nest** to form a tree — that tree becomes the **DOM**. `<head>` holds
metadata (title, character set, links to CSS); `<body>` holds what's shown.

**Semantic HTML** means choosing tags by *meaning*, not appearance:

```html
<header>, <nav>, <main>, <article>, <section>, <footer>
<h1>…<h6>  headings   <ul>/<ol>/<li>  lists   <button>  actions
<form>, <input>, <label>  user input
```

Why semantics matter (this is the mark of a real web developer, not just
making-it-look-right):

- **Accessibility** — screen readers rely on real `<button>`, `<nav>`, and
  headings to navigate; a `<div>` you styled to look like a button is invisible
  to them.
- **SEO** — search engines understand semantic structure.
- **Maintainability** — `<nav>` says what it is; `<div class="nav">` doesn't.

The golden rule: **HTML is for meaning, not looks.** Never reach for a tag because
of how it renders — use the tag that describes the content, then style it with
CSS (next). Get the structure right and everything else has something solid to
build on.
""",
        ),
        _t(
            "CSS: styling & layout",
            "11 min",
            r"""# CSS: styling & layout

**CSS** (Cascading Style Sheets) controls **presentation**. You write **rules**: a
**selector** picks elements, and **declarations** set properties.

```css
/* selector { property: value; } */
h1 { color: #2563eb; font-size: 2rem; }
.card { padding: 16px; border-radius: 8px; }
#hero { background: black; }
nav a:hover { text-decoration: underline; }
```

Selectors target by **tag** (`h1`), **class** (`.card`, reusable), **id**
(`#hero`, unique), and combinations/states (`:hover`). When rules conflict, the
**cascade** decides by **specificity** (id > class > tag) and source order.

**The box model** — every element is a box of four layers, and understanding it
ends 90% of layout confusion:

```
+--------- margin ---------+
|  +------ border ------+  |
|  |  +-- padding --+   |  |
|  |  |  content    |   |  |
|  |  +-------------+   |  |
|  +-------------------+  |
+-------------------------+
```

`content` → `padding` (inside the border) → `border` → `margin` (space outside).

**Modern layout** uses two systems instead of old hacks:

- **Flexbox** — one-dimensional (a row or column). Great for toolbars, nav, and
  distributing space: `display: flex; justify-content: space-between;`.
- **Grid** — two-dimensional (rows *and* columns). Great for page layouts:
  `display: grid; grid-template-columns: 1fr 3fr;`.

**Responsive design** adapts to screen size with **media queries** and relative
units (`rem`, `%`, `vw`) instead of fixed pixels:

```css
@media (max-width: 600px) { .sidebar { display: none; } }
```

The mental model: **HTML is the skeleton, CSS is the skin and pose.** Keep style
*out* of HTML (no inline `style=` everywhere) so a design change is one CSS edit,
not a hundred. Flexbox + Grid + media queries cover almost everything you'll
build.
""",
        ),
        _t(
            "JavaScript fundamentals",
            "11 min",
            r"""# JavaScript fundamentals

**JavaScript (JS)** adds **behaviour** — it's the programming language of the
browser (and, via Node.js, the server). The essentials:

```js
// Variables: prefer const; use let when you must reassign. Avoid var.
const name = "Ada";
let count = 0;
count = count + 1;

// Types: string, number, boolean, null, undefined, object, array
const user = { name: "Ada", admin: true };   // object
const nums = [1, 2, 3];                        // array

// Functions (arrow form is idiomatic)
const square = (x) => x * x;
function greet(who) { return "Hi " + who; }
```

Control flow is C-like (`if/else`, `for`, `while`), plus powerful **array
methods** you'll use constantly:

```js
const doubled = nums.map((n) => n * 2);          // [2,4,6]
const evens   = nums.filter((n) => n % 2 === 0); // [2]
const total   = nums.reduce((a, n) => a + n, 0); // 6
```

Two gotchas worth knowing early:

- **`===` not `==`.** Use **strict equality** (`===`) — `==` does surprising type
  coercion (`0 == ""` is true!).
- **Truthiness.** `0`, `""`, `null`, `undefined`, `NaN` are **falsy**; almost
  everything else is **truthy**.

**Asynchronous JS** is central, because the browser must never freeze waiting for
the network. Modern code uses **promises** with `async/await`:

```js
async function loadCourses() {
  const res = await fetch("/api/courses");   // returns a Promise
  const data = await res.json();
  return data;
}
```

`await` pauses *this function* until the promise resolves, without blocking the
page. This is how you call backends (next courses).

JS runs on a **single thread** with an **event loop**: synchronous code runs to
completion, and async callbacks (timers, network, clicks) are queued and run when
the stack is clear. Internalising **non-blocking, event-driven** execution is the
key to thinking in JavaScript — you'll run web logic in code shortly.
""",
        ),
        _t(
            "The DOM & events",
            "10 min",
            r"""# The DOM & events

When the browser parses your HTML it builds the **DOM** (Document Object Model) —
a live **tree of objects**, one per element. JavaScript manipulates this tree to
change the page *after* it has loaded, which is what makes pages interactive.

**Selecting and changing elements:**

```js
const title = document.querySelector("h1");     // CSS-selector lookup
title.textContent = "Updated!";                  // change content
title.classList.add("highlight");                // change styling
const items = document.querySelectorAll(".item"); // a list
```

**Creating and inserting:**

```js
const li = document.createElement("li");
li.textContent = "New item";
document.querySelector("ul").appendChild(li);
```

**Events** are how you respond to the user — clicks, typing, submitting, scrolling.
You **add a listener**, a function that runs when the event fires:

```js
const button = document.querySelector("#buy");
button.addEventListener("click", (event) => {
  event.preventDefault();        // stop the default action (e.g. form submit)
  addToCart();
});
```

Two ideas make event handling scale:

- **The event object** carries details (which key, which element, mouse position)
  and methods like `preventDefault()` and `stopPropagation()`.
- **Event bubbling & delegation** — an event fires on the target then **bubbles
  up** through its ancestors. So instead of 100 listeners on 100 list items, you
  put **one** listener on the parent `<ul>` and check `event.target`. That's
  **event delegation** — fewer listeners, and it works for elements added later.

The big-picture pattern of all interactive UIs: **state changes → update the
DOM.** Naïve apps poke the DOM directly (as above); this gets unmanageable fast,
which is exactly the problem **frontend frameworks** (React, Svelte, Vue) solve by
letting you describe the UI as a function of state and updating the DOM for you —
the Intermediate course. First, you'll build core web logic by hand.
""",
        ),
        _code(
            "Parse a URL query string",
            "12 min",
            r"""# Every web request carries data in the URL's query string
# (?name=Ada&role=admin). Servers must parse it into structured data. Build the
# parser by hand (the same logic every web framework runs). Pure builtins.

def parse_query(qs):
    # Drop a leading '?' if present.
    if qs.startswith("?"):
        qs = qs[1:]
    params = {}
    for pair in qs.split("&"):
        if pair == "":
            continue
        if "=" in pair:
            key, value = pair.split("=", 1)
        else:
            key, value = pair, ""          # a bare flag like ?debug
        # Repeated keys (?tag=a&tag=b) collect into a list.
        if key in params:
            existing = params[key]
            if isinstance(existing, list):
                params[key] = existing + [value]
            else:
                params[key] = [existing, value]
        else:
            params[key] = value
    return params

print(parse_query("?name=Ada&role=admin"))
print(parse_query("q=web+dev&page=2&tag=js&tag=css"))
print(parse_query("?debug&verbose"))
# Real frameworks also URL-decode %20 etc. and split on ';' — same core idea.
""",
        ),
        _t(
            "HTTP, forms & talking to the server",
            "10 min",
            r"""# HTTP, forms & talking to the server

Everything the browser and server exchange rides on **HTTP** (Networking track,
now from the app side). A request has a **method**, a **path**, **headers**, and
sometimes a **body**; a response has a **status code**, **headers**, and a
**body**.

**Methods** map to intent (the basis of REST, next course):

- **GET** — read; no side effects; parameters go in the **query string**.
- **POST** — create/submit; data goes in the **body**.
- **PUT/PATCH** — update. **DELETE** — remove.

**Status codes** tell you what happened: **2xx** success, **3xx** redirect, **4xx**
your fault (400 bad request, 401 unauthorised, 404 not found), **5xx** server's
fault.

**HTML forms** are the classic way users send data:

```html
<form action="/signup" method="post">
  <label>Email <input type="email" name="email" required /></label>
  <button type="submit">Sign up</button>
</form>
```

On submit, the browser bundles the fields and sends them to `action` using
`method`. The **`name`** attributes become the keys the server reads.

Modern apps often skip the full-page submit and call the server from JavaScript
with **`fetch`**, sending/receiving **JSON** — the lingua franca of web APIs:

```js
const res = await fetch("/api/signup", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email })
});
const data = await res.json();
```

Because HTTP is **stateless**, the server can't tell two requests come from the
same user on its own — it uses **cookies** (a token echoed on every request) or
an **Authorization** header to maintain a **session** (auth is covered in the
Intermediate course). Two takeaways: **pick the method that matches intent**, and
**never trust input** — anything from the client (form fields, query strings,
JSON) can be forged, so the server must always **validate** it (you'll see how
soon).
""",
        ),
        _code(
            "Build a tiny template engine",
            "12 min",
            r"""# Servers turn data + a template into HTML. Template engines (Jinja, Handlebars,
# JSX) all do the same core job: substitute {{ placeholders }} with values and
# escape them so data can't inject markup. Build a minimal one. Pure builtins.

def render(template, data):
    result = template
    for key in data:
        # Always escape interpolated data so it can't inject markup.
        raw = str(data[key])
        value = raw.replace("&", "&amp;").replace("<", "&lt;")
        value = value.replace(">", "&gt;").replace(chr(34), "&quot;")
        token = "{{" + key + "}}"
        result = result.replace(token, value)
    return result

page = "<h1>Hello {{name}}</h1><p>Role: {{role}}. Posts: {{posts}}.</p>"
print(render(page, {"name": "Ada", "role": "admin", "posts": 42}))

# Escaping is what stops a name like '<script>' from becoming live HTML:
attack = {"name": "<script>alert('xss')</script>", "role": "guest", "posts": 0}
print(render(page, attack))
# The script tag is rendered as harmless text, not executed — that's XSS defence.
""",
        ),
        quiz_lesson(
            "Quiz: Web Development Basics",
            (
                q(
                    "What is the role of HTML, CSS, and JavaScript respectively?",
                    (
                        opt(
                            "HTML = structure/content, CSS = presentation/style, JavaScript = behaviour",
                            correct=True,
                        ),
                        opt("HTML = style, CSS = behaviour, JavaScript = structure"),
                        opt("They all do the same thing"),
                        opt("HTML = behaviour, CSS = structure, JavaScript = style"),
                    ),
                    "Keep them separate: HTML for meaning, CSS for looks, JS for interaction — the foundation of maintainable front-end work.",
                ),
                q(
                    "Why use semantic HTML (<nav>, <button>, <article>) instead of styled <div>s?",
                    (
                        opt(
                            "Accessibility, SEO, and maintainability — semantics convey meaning to screen readers and search engines",
                            correct=True,
                        ),
                        opt("Semantic tags render faster"),
                        opt("It is required by the compiler"),
                        opt("There is no difference"),
                    ),
                    "Real <button>/<nav>/headings are navigable by assistive tech and understood by search engines; a styled <div> is not.",
                ),
                q(
                    "In the CSS box model, what is the order of layers from inside out?",
                    (
                        opt("content → padding → border → margin", correct=True),
                        opt("margin → border → padding → content"),
                        opt("border → content → margin → padding"),
                        opt("padding → content → margin → border"),
                    ),
                    "Content sits inside padding, wrapped by the border, with margin as the outer space — understanding this resolves most layout confusion.",
                ),
                q(
                    "Why does browser JavaScript use async/await and an event loop?",
                    (
                        opt(
                            "So the single-threaded page never freezes while waiting on the network or timers",
                            correct=True,
                        ),
                        opt("To run code on multiple CPU cores"),
                        opt("To make the code run slower"),
                        opt("Because synchronous code is impossible in JS"),
                    ),
                    "JS is single-threaded; async lets network/timer work happen without blocking the UI, with callbacks run via the event loop.",
                ),
                q(
                    "What is event delegation in the DOM?",
                    (
                        opt(
                            "Putting one listener on a parent and using event bubbling to handle many children",
                            correct=True,
                        ),
                        opt("Adding a separate listener to every element"),
                        opt("Disabling all events"),
                        opt("Running events on the server"),
                    ),
                    "Events bubble up to ancestors, so a single parent listener can handle many children — fewer listeners, and it works for new elements.",
                ),
                q(
                    "When rendering user data into HTML, why must you escape it?",
                    (
                        opt(
                            "To prevent it from being interpreted as live markup/script (XSS)",
                            correct=True,
                        ),
                        opt("To make it load faster"),
                        opt("To compress the response"),
                        opt("Escaping is optional and only cosmetic"),
                    ),
                    "Escaping <, >, &, and quotes turns data like <script> into harmless text instead of executable HTML — the core XSS defence.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# webdev-intermediate
# ──────────────────────────────────────────────────────────────────────

_WEB_INTERMEDIATE = SeedCourse(
    slug="webdev-intermediate",
    title="Web Development — Intermediate",
    description=(
        "From pages to applications: client-server architectures (SPA vs SSR), "
        "component frameworks and reactivity, building and consuming REST APIs, "
        "authentication (cookies, sessions, JWT, OAuth), and databases/ORMs — "
        "with runnable REST-router and request-validation labs."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Architectures: SSR, SPA & beyond",
            "10 min",
            r"""# Architectures: SSR, SPA & beyond

How a web app splits work between server and browser is its **rendering
architecture**, and it shapes performance, SEO, and complexity.

- **Multi-page app (MPA) / classic SSR** — the **server renders full HTML** for
  each page; every navigation is a fresh request. Simple, great SEO and fast
  first paint, but whole-page reloads feel less fluid. (PHP, Rails, Django,
  classic.)
- **Single-page app (SPA)** — the server sends a near-empty HTML shell plus a
  **JavaScript bundle**; the browser renders everything and fetches **data** (JSON)
  via APIs, swapping views **without full reloads**. Fluid and app-like, but a
  heavier initial download, and SEO/first-paint need care. (React/Vue/Svelte
  SPAs.)
- **Modern SSR + hydration** — render HTML on the server **and** ship JS that
  "**hydrates**" it into an interactive SPA. Best of both: fast first paint + SEO +
  rich interactivity. (Next.js, SvelteKit, Nuxt.)
- **SSG / ISR** — pre-render pages at **build time** (static site generation) and
  optionally revalidate (incremental static regeneration). Fastest and cheapest
  for content that changes rarely.

The trade-off axis is **where rendering happens** (server vs client) and **when**
(build, request, or runtime):

```
SSR/SSG: fast first paint, SEO-friendly, server cost
SPA:     fluid interaction, simple hosting, slower first paint, SEO effort
```

A crucial consequence of any architecture where the browser holds logic: **the
client is untrusted.** Whatever the frontend does — validation, hiding admin
buttons — can be bypassed, so **security and validation must live on the server**.
The frontend is for *experience*; the backend is for *truth*. Most teams now reach
for a **meta-framework** (Next/SvelteKit) that lets you choose SSR/SSG/SPA
**per route**, which is the pragmatic default.
""",
        ),
        _t(
            "Frontend frameworks & reactivity",
            "11 min",
            r"""# Frontend frameworks & reactivity

Updating the DOM by hand (Basics course) collapses under real app complexity. The
fix that won: **component-based frameworks** built on **reactivity** — you
describe the UI as a function of **state**, and the framework updates the DOM when
state changes.

**Components** are reusable, self-contained UI pieces (a button, a card, a whole
page) with their own markup, style, and logic — composed into a tree:

```jsx
// React-style component
function Counter() {
  const [count, setCount] = useState(0);          // reactive state
  return <button onClick={() => setCount(count + 1)}>Clicked {count}</button>;
}
```

```svelte
<!-- Svelte: reactivity built into the language -->
<script> let count = 0; </script>
<button on:click={() => count++}>Clicked {count}</button>
```

**Reactivity** is the core idea: when `count` changes, *only the parts of the DOM
that depend on it* re-render — you never write `document.querySelector(...)`. How
frameworks track those dependencies differs:

- **React** — a **Virtual DOM**: re-run the component, diff a lightweight tree
  against the previous one, and patch only the differences. Explicit `useState`.
- **Svelte** — a **compiler** that, at build time, generates precise DOM-updating
  code (no virtual DOM, tiny runtime).
- **Vue/Solid/Signals** — fine-grained **signals** that track exactly which UI
  depends on which value.

Shared concepts across all of them: **props** (data passed parent → child),
**state** (data a component owns), **one-way data flow** (data down, events up),
and a **component lifecycle** (mount/update/unmount). Learn these *ideas* and any
framework is a syntax change.

Frameworks also bring **client-side routing** (swap views without reloads),
**conditional/list rendering**, and an ecosystem of tooling. The win is
**declarative UI**: you say *what* the UI should look like for a given state, and
the framework handles the imperative DOM work — far less error-prone than manual
updates. Managing **state** as it grows is the next challenge.
""",
        ),
        _t(
            "Building & consuming REST APIs",
            "11 min",
            r"""# Building & consuming REST APIs

The frontend gets its data from the backend over an **API**. The dominant style
is **REST** — model your domain as **resources** addressed by URLs, manipulated
with HTTP methods.

**Resource-oriented design:**

```
GET    /courses          → list courses
POST   /courses          → create a course
GET    /courses/42       → fetch course 42
PUT    /courses/42       → replace course 42
PATCH  /courses/42       → update fields of course 42
DELETE /courses/42       → delete course 42
GET    /courses/42/lessons → sub-resource
```

Good REST conventions (they make an API predictable):

- **Nouns, not verbs** in paths (`/courses`, not `/getCourses`); the **method** is
  the verb.
- **Correct status codes** — 200 OK, 201 Created, 204 No Content, 400, 401, 403,
  404, 409 (conflict), 422 (validation), 500.
- **JSON** request/response bodies; consistent field naming.
- **Statelessness** — each request carries everything needed (auth token,
  params); the server keeps no per-client session in memory (scales horizontally).
- **Versioning** (`/api/v1/...`) so you can evolve without breaking clients.
- **Pagination, filtering, sorting** via query params for list endpoints.

**Consuming** an API from the frontend uses `fetch` and handles the **async,
fallible** nature of the network:

```js
async function getCourse(id) {
  const res = await fetch(`/api/v1/courses/${id}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);   // check status!
  return res.json();
}
```

Always handle **loading**, **error**, and **empty** states — the request *will*
sometimes be slow or fail. Beyond REST you'll meet **GraphQL** (clients request
exactly the fields they need — Advanced course) and **gRPC** (binary RPC between
services). REST remains the default for public/web APIs because it's simple,
cacheable, and rides plain HTTP. You'll implement the heart of an API — a
**router** that maps method + path to a handler — next.
""",
        ),
        _code(
            "A REST request router",
            "13 min",
            r"""# Every web framework has a ROUTER: it maps an incoming (method, path) to the
# right handler, capturing path parameters like /courses/42. Build one with plain
# string matching (no regex). Pure builtins.

# Routes are (method, pattern) -> handler name. ':x' marks a path parameter.
routes = [
    ("GET", "/courses", "list_courses"),
    ("POST", "/courses", "create_course"),
    ("GET", "/courses/:id", "get_course"),
    ("DELETE", "/courses/:id", "delete_course"),
    ("GET", "/courses/:id/lessons/:lessonId", "get_lesson"),
]

def match(method, path, routes):
    path_parts = path.strip("/").split("/")
    for route_method, pattern, handler in routes:
        if route_method != method:
            continue
        pattern_parts = pattern.strip("/").split("/")
        if len(pattern_parts) != len(path_parts):
            continue
        params = {}
        ok = True
        for i in range(len(pattern_parts)):
            seg = pattern_parts[i]
            if seg.startswith(":"):
                params[seg[1:]] = path_parts[i]      # capture the parameter
            elif seg != path_parts[i]:
                ok = False
                break
        if ok:
            return handler, params
    return None, None

for method, path in [
    ("GET", "/courses"),
    ("GET", "/courses/42"),
    ("DELETE", "/courses/42"),
    ("GET", "/courses/42/lessons/7"),
    ("POST", "/courses/42"),        # no matching route -> 404
]:
    handler, params = match(method, path, routes)
    if handler is None:
        print(method, path, "-> 404 Not Found")
    else:
        print(method, path, "->", handler, params)
""",
        ),
        _t(
            "Authentication & sessions",
            "11 min",
            r"""# Authentication & sessions

HTTP is **stateless**, so the server can't inherently tell that two requests come
from the same logged-in user. **Authentication** answers *who are you?* and
**authorization** answers *what may you do?* — and the app must carry that identity
across stateless requests.

First, **never store passwords in plaintext.** Hash them with a slow, salted
algorithm (**bcrypt/argon2**) so a database leak doesn't expose them (Security
track).

Two dominant ways to carry identity after login:

- **Session cookies (stateful).** On login the server creates a **session**,
  stores it (in memory/Redis/DB), and sends a **cookie** with the session ID. The
  browser auto-attaches the cookie to every request; the server looks it up.
  Easy to **revoke** (delete the session), but the server must **store** sessions
  (state to scale).
- **Tokens / JWT (stateless).** On login the server returns a **signed token**
  (**JWT**) containing claims (user id, roles, expiry). The client sends it in the
  `Authorization: Bearer ...` header; the server **verifies the signature** —
  **no server-side lookup**, so it scales and works across services. Downsides:
  **hard to revoke** before expiry, and you must store it safely on the client.

**Cookie security flags** matter enormously: `HttpOnly` (JS can't read it → blunts
XSS theft), `Secure` (HTTPS only), `SameSite` (limits cross-site sending → blunts
CSRF).

**OAuth 2.0 / OpenID Connect** handle "**log in with Google/GitHub**": your app
redirects to the provider, the user approves, and you receive a token proving
identity — so you never handle their password. Common for third-party login and
delegated API access.

The non-negotiable principle: **enforce auth on the server, every time.** Hiding
an admin button in the frontend is UX, not security — the client is untrusted, so
every protected endpoint must independently check identity and permissions. You'll
practise the server's first duty — **validating untrusted input** — next.
""",
        ),
        _code(
            "Validate & sanitize untrusted input",
            "12 min",
            r"""# The #1 rule of backend web dev: never trust the client. Every request body
# must be validated before use. Build a small validator for a signup payload.
# Pure builtins.

def validate_signup(data):
    errors = []

    # Required fields present?
    for field in ["email", "username", "age"]:
        if field not in data or data[field] == "":
            errors.append("missing field: " + field)

    # Email looks plausible (a real app uses a stricter check).
    email = data.get("email", "")
    if email != "" and ("@" not in email or "." not in email):
        errors.append("invalid email")

    # Username length and characters.
    username = data.get("username", "")
    if username != "" and (len(username) < 3 or len(username) > 20):
        errors.append("username must be 3-20 chars")

    # Age must be an integer in range (clients send strings!).
    age = data.get("age", "")
    if str(age).isdigit():
        if int(age) < 13 or int(age) > 120:
            errors.append("age out of range")
    elif age != "":
        errors.append("age must be a number")

    return errors

good = {"email": "ada@example.com", "username": "ada99", "age": "30"}
bad = {"email": "not-an-email", "username": "x", "age": "200"}
missing = {"email": "bob@x.com"}

for name, payload in [("good", good), ("bad", bad), ("missing", missing)]:
    errs = validate_signup(payload)
    print(name, "->", "OK" if not errs else errs)
# Reject invalid input with 400/422 BEFORE it touches your database or logic.
""",
        ),
        _t(
            "Databases & ORMs in web apps",
            "10 min",
            r"""# Databases & ORMs in web apps

Behind almost every web app is a **database** holding the durable state — users,
posts, orders. The backend reads and writes it on each request. (The Databases
track goes deep; here's the web-developer's view.)

**SQL vs NoSQL** in brief: **relational** databases (PostgreSQL, MySQL) store
**tables** with a fixed schema and give you **joins** and **ACID transactions** —
the right default for most apps with related data and correctness needs.
**NoSQL** (MongoDB, DynamoDB, Redis) trades joins/strong schema for flexibility,
scale, or speed — pick it for specific access patterns, caching, or huge scale.

Most code talks to the database through an **ORM** (Object-Relational Mapper) —
SQLAlchemy, Prisma, ActiveRecord — which maps **tables to objects/classes** so you
write application code instead of raw SQL:

```js
// ORM-style (pseudocode)
const user = await User.create({ email, name });
const courses = await Course.where({ published: true }).limit(10);
```

ORMs give productivity, safety, and portability — but mind the famous traps:

- **The N+1 query problem** — looping over N records and lazily loading a relation
  fires **1 + N** queries (one per item) instead of **one** join. The classic web
  performance killer; fix with **eager loading**.
- **SQL injection** — never build queries by string-concatenating user input. Use
  **parameterised queries / the ORM's binding** (`WHERE id = $1`), which the ORM
  does for you (Security track).
- **Migrations** — schema changes are version-controlled, ordered scripts
  (`add column`, `create index`) applied consistently across environments — never
  edit a production schema by hand.

Two web-relevant performance levers: **indexes** (a missing index turns a fast
lookup into a full-table scan — the first thing to check when a query is slow) and
a **cache** in front of hot reads (Redis), as in the System Design track. The
data layer is where correctness (transactions), security (parameterisation), and
performance (indexes, N+1, caching) all meet — handle it with care.
""",
        ),
        quiz_lesson(
            "Quiz: Apps, APIs & Auth",
            (
                q(
                    "What's the key trade-off between an SPA and server-side rendering (SSR)?",
                    (
                        opt(
                            "SPA gives fluid interaction but slower first paint and SEO effort; SSR gives fast first paint and SEO at server cost",
                            correct=True,
                        ),
                        opt("SSR cannot produce HTML"),
                        opt("SPAs are always faster in every way"),
                        opt("They are identical"),
                    ),
                    "SPAs render in the browser (app-like, heavier first load); SSR renders HTML on the server (fast first paint, SEO). Meta-frameworks mix per route.",
                ),
                q(
                    "What does reactivity in a frontend framework mean?",
                    (
                        opt(
                            "You describe UI as a function of state, and the framework updates only the DOM parts that depend on changed state",
                            correct=True,
                        ),
                        opt("The page reloads fully on every change"),
                        opt("You manually call querySelector for every update"),
                        opt("It disables JavaScript"),
                    ),
                    "Declarative UI: state changes drive precise DOM updates (via virtual DOM, a compiler, or signals) — no manual DOM poking.",
                ),
                q(
                    "Which is a core REST convention?",
                    (
                        opt(
                            "Use nouns in paths and HTTP methods as the verbs (GET /courses, not /getCourses)",
                            correct=True,
                        ),
                        opt("Put verbs in the path and ignore status codes"),
                        opt("Always use POST for everything"),
                        opt("Keep per-client session state on the server"),
                    ),
                    "REST models resources (nouns) acted on by methods (verbs), with correct status codes, JSON, statelessness, and versioning.",
                ),
                q(
                    "What's the main difference between session cookies and JWT tokens for auth?",
                    (
                        opt(
                            "Sessions are stateful and easy to revoke (server stores them); JWTs are stateless and scale but are hard to revoke before expiry",
                            correct=True,
                        ),
                        opt("JWTs store passwords in plaintext"),
                        opt("Sessions cannot use cookies"),
                        opt("They are the same thing"),
                    ),
                    "Session = server-stored id in a cookie (revocable, stateful); JWT = signed self-contained token (stateless, scalable, hard to revoke).",
                ),
                q(
                    "Why must input validation happen on the server even if the frontend validates too?",
                    (
                        opt(
                            "The client is untrusted — frontend checks can be bypassed, so the server is the only place to enforce correctness and security",
                            correct=True,
                        ),
                        opt("Server validation is faster"),
                        opt("Frontend validation is impossible"),
                        opt("It isn't necessary if the frontend validates"),
                    ),
                    "Anything from the client can be forged; the server must independently validate every request (reject with 400/422).",
                ),
                q(
                    "What is the N+1 query problem?",
                    (
                        opt(
                            "Looping over N records and lazily loading a relation fires 1+N queries instead of a single join",
                            correct=True,
                        ),
                        opt("Running out of database connections"),
                        opt("A type of SQL injection"),
                        opt("Having one extra column"),
                    ),
                    "Lazy-loading a relation per item is a classic performance killer; fix it with eager loading / a join.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# webdev-advanced
# ──────────────────────────────────────────────────────────────────────

_WEB_ADVANCED = SeedCourse(
    slug="webdev-advanced",
    title="Web Development — Advanced",
    description=(
        "Production web engineering: performance and Core Web Vitals, HTTP "
        "caching and CDNs, the web security model (XSS, CSRF, CORS, CSP), "
        "GraphQL vs REST, real-time (WebSockets/SSE), and scaling/deployment — "
        "with a runnable XSS-defence lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Web performance & Core Web Vitals",
            "11 min",
            r"""# Web performance & Core Web Vitals

Performance is a feature: faster sites convert better, rank higher, and cost less.
The browser turns your files into pixels via the **critical rendering path** —
parse HTML → build DOM, parse CSS → build CSSOM, run JS, combine into the render
tree, **layout**, **paint**. Anything that blocks this delays what the user sees.

Google's **Core Web Vitals** are the metrics that matter (and affect SEO):

- **LCP (Largest Contentful Paint)** — when the main content appears. Target
  **< 2.5 s**. Hurt by slow servers, render-blocking resources, big images.
- **INP (Interaction to Next Paint)** — responsiveness to input. Target
  **< 200 ms**. Hurt by heavy JavaScript blocking the main thread.
- **CLS (Cumulative Layout Shift)** — visual stability (things jumping around).
  Target **< 0.1**. Fixed by reserving space for images/ads.

The biggest levers, roughly in order of impact:

- **Ship less JavaScript.** JS is the most expensive resource (download + parse +
  execute on the main thread). **Code-split** and **lazy-load** so each route
  loads only what it needs; **tree-shake** dead code.
- **Optimise images** — modern formats (WebP/AVIF), correct sizes, `loading="lazy"`.
  Images are usually the heaviest bytes.
- **Minify & compress** (gzip/Brotli) all text assets; **bundle** to cut requests
  (less critical with HTTP/2 multiplexing).
- **Load critical things first, defer the rest** — `async`/`defer` scripts, inline
  critical CSS, preload key assets.
- **Cache** aggressively (next lesson) and serve from a **CDN** near the user.

Page weight has a roughly linear cost in load time on slower connections, so every
kilobyte you cut helps the users who need it most:

```plot
{"title": "Load time grows with JS bundle size (≈3G, ~1.5 MB/s effective)", "xLabel": "JS bundle size (MB)", "yLabel": "approx load+parse (s)", "xRange": [0, 5], "yRange": [0, 8], "functions": [{"expr": "x * 1.5", "label": "≈ size × (download + parse)", "color": "#dc2626"}]}
```

The mindset: **measure, then fix the biggest thing.** Use Lighthouse/WebPageTest,
watch the Vitals on real users (RUM), and remember the cheapest byte is the one
you never send.
""",
        ),
        _t(
            "HTTP caching & CDNs",
            "10 min",
            r"""# HTTP caching & CDNs

The fastest request is one you never make. **Caching** stores responses so they
can be reused, and the web has a rich, layered caching model built into HTTP.

**Browser caching via headers** — the server tells the browser how long a response
is fresh and how to revalidate:

- **`Cache-Control`** — the main control: `max-age=3600` (fresh for an hour),
  `no-store` (never cache — for sensitive/dynamic data), `private` vs `public`,
  `immutable`.
- **Validators** — when a cached copy *might* be stale, the browser revalidates
  cheaply with **`ETag`** (a content fingerprint) or **`Last-Modified`**; the
  server replies **304 Not Modified** (no body) if nothing changed.

**Cache-busting for static assets** — the standard trick: give built files
**content-hashed names** (`app.9f3a2.js`) and serve them with a long
`max-age=immutable`. New deploy → new hash → new URL, so caches never serve stale
code, yet unchanged files stay cached forever.

**CDNs (Content Delivery Networks)** push your content to **edge servers** in
hundreds of cities, so users fetch from a nearby node (Networking/System Design
tracks). They slash latency, offload your origin, absorb traffic spikes, and help
defend against DDoS — increasingly they cache not just images/JS/CSS but whole
pages and even API responses at the edge.

**Where caching lives** (layered, each catching what it can):

```
Browser cache → CDN/edge → reverse proxy → application cache (Redis) → DB cache
```

The subtle, eternal hazard is **invalidation** — making sure nobody serves stale
data after an update (System Design's "two hard things"). Strategies: short TTLs,
**purging** the CDN on deploy, content-hashed URLs for immutable assets, and
`no-store` for anything user-specific or sensitive. Get caching right and you cut
latency and cost dramatically; get invalidation wrong and users see yesterday's
data — so cache **static, public, slow-changing** things hardest, and be careful
with the rest.
""",
        ),
        _t(
            "The web security model",
            "11 min",
            r"""# The web security model

The browser runs untrusted code from everywhere, so it enforces a strict security
model — and your app must cooperate. The essentials every web dev must know
(Security track goes deeper):

- **XSS (Cross-Site Scripting)** — an attacker gets **their** JavaScript to run in
  **your** page (e.g. a comment containing `<script>`), stealing cookies or acting
  as the user. **Defence:** **escape/encode** all user data on output (Basics
  lab), prefer framework auto-escaping, and set a **Content-Security-Policy**.
- **CSRF (Cross-Site Request Forgery)** — a malicious site tricks the user's
  browser into making a **state-changing request** to your app using their
  logged-in cookies. **Defence:** **`SameSite` cookies**, **CSRF tokens**, and
  requiring a custom header for sensitive actions.
- **The Same-Origin Policy (SOP)** — the browser's bedrock rule: a page can't read
  responses from a **different origin** (scheme + host + port) unless allowed.
  This is why one site's JS can't read another's data.
- **CORS (Cross-Origin Resource Sharing)** — the controlled **exception** to SOP:
  a server opts in with `Access-Control-Allow-Origin` headers so a browser app on
  `app.example.com` may call `api.example.com`. CORS is enforced **by the
  browser**, configured **by the server** — and frequently misunderstood (it's not
  a server-side firewall).
- **CSP (Content-Security-Policy)** — a header that whitelists where scripts/styles
  may load from, sharply reducing XSS impact even if a hole exists.
- **HTTPS everywhere** — TLS encrypts and authenticates traffic; serve it on every
  route (`Strict-Transport-Security` to enforce it). No exceptions for login pages.

The unifying principles: **never trust client input** (validate + escape),
**defence in depth** (multiple layers, so one failure isn't fatal), and **least
privilege** (cookies `HttpOnly`/`Secure`/`SameSite`, minimal CORS, tight CSP).
Most breaches exploit a handful of these basics — knowing them is the difference
between an app that's merely working and one that's safe to ship. You'll implement
the core XSS defence next.
""",
        ),
        _code(
            "Stop XSS: escape on output",
            "12 min",
            r"""# XSS happens when user data is inserted into a page as live HTML. The defence
# is context-aware escaping. Build an escaper and an attribute-safe encoder and
# watch a payload get neutralised. Pure builtins.

def escape_html(text):
    # For inserting text into element content.
    out = text.replace("&", "&amp;")
    out = out.replace("<", "&lt;")
    out = out.replace(">", "&gt;")
    return out

def escape_attr(text):
    # For inserting into an attribute value (quotes matter too).
    out = text.replace("&", "&amp;")
    out = out.replace("<", "&lt;")
    out = out.replace(">", "&gt;")
    out = out.replace(chr(34), "&quot;")     # "
    out = out.replace("'", "&#39;")
    return out

payloads = [
    "<script>steal(document.cookie)</script>",
    "\" onmouseover=\"alert(1)",              # tries to break out of an attribute
    "normal user text",
]

print("rendering user input into <div> content and an attribute:")
for p in payloads:
    print()
    print("  raw      :", p)
    print("  in body  : <div>" + escape_html(p) + "</div>")
    print("  in attr  : <input value=" + chr(34) + escape_attr(p) + chr(34) + ">")
# After escaping, the angle brackets and quotes are inert text — the browser can
# no longer be tricked into starting a <script> or a new attribute.
""",
        ),
        _t(
            "GraphQL & API design at scale",
            "9 min",
            r"""# GraphQL & API design at scale

REST is great, but it has two friction points at scale: **over-fetching**
(an endpoint returns more than you need) and **under-fetching** (you must call
several endpoints to build one screen, the "waterfall"). **GraphQL** (and other
approaches) address these.

**GraphQL** exposes a single endpoint and a **typed schema**; the **client asks
for exactly the fields it wants**, in one request:

```graphql
query {
  course(id: 42) {
    title
    lessons { title duration }     # exactly these fields, one round-trip
  }
}
```

- **Pros** — no over/under-fetching; one request for nested data; a strongly-typed,
  self-documenting schema; great for diverse clients (web/mobile) with different
  needs.
- **Cons** — **caching is harder** (it's POST to one URL, not cacheable URLs like
  REST); you can write expensive/nested queries (need depth limits & cost
  analysis); the classic **N+1** resolver problem (solved with **DataLoader**
  batching); more server complexity.

**When to choose what:**

- **REST** — public APIs, simple resources, when HTTP caching/CDN matters, broad
  tooling. Still the default.
- **GraphQL** — complex, nested data with many client shapes (dashboards, mobile +
  web), a large frontend org iterating fast.
- **gRPC** — high-performance **service-to-service** RPC (binary protobuf,
  streaming); not browser-native.

Beyond the style, **good API design** is the same everywhere: clear and
**consistent** naming, **versioning** to evolve without breaking clients,
**pagination** for lists, thoughtful **error formats**, **rate limiting** (System
Design), **idempotency** for retried writes (Distributed Systems), and solid
**docs** (OpenAPI/GraphQL schema). The protocol is a detail; a **predictable,
evolvable contract** between client and server is the real goal.
""",
        ),
        _t(
            "Real-time: WebSockets, SSE & polling",
            "9 min",
            r"""# Real-time: WebSockets, SSE & polling

Plain HTTP is **client-pull**: the browser asks, the server answers. But chat,
live dashboards, notifications, collaborative editing, and games need the
**server to push** updates as they happen. The options, from simplest to most
capable:

- **Short polling** — the client repeatedly asks "anything new?" on a timer.
  Trivial to build, but wasteful (most responses are empty) and laggy (updates
  wait for the next poll). Fine for low-frequency, non-critical updates.
- **Long polling** — the client asks and the server **holds the request open**
  until it has data (or a timeout), then the client immediately re-asks. Near
  real-time over plain HTTP; a reasonable fallback.
- **Server-Sent Events (SSE)** — a **one-way** stream from server → client over a
  single long-lived HTTP connection (`EventSource`). Simple, auto-reconnects,
  perfect for **feeds/notifications/live scores** where only the server pushes.
- **WebSockets** — a **full-duplex, persistent** connection: after an HTTP
  **upgrade** handshake, both sides send messages anytime with low overhead. The
  right tool for **bidirectional, high-frequency** apps: chat, multiplayer games,
  collaborative editing, trading.

How to choose:

```
Only server → client, simple?      → SSE
Two-way, frequent, low latency?    → WebSockets
Occasional updates, must be simple? → long polling
```

Real-time adds operational weight: **persistent connections hold server
resources** (you can't keep millions cheaply — plan capacity and use a pub/sub
backend like Redis to fan out across servers), they need **reconnection/heartbeat**
logic, and they complicate **horizontal scaling** (a stateful connection is pinned
to one server, so you broadcast via a shared bus). Higher-level libraries
(Socket.IO, Phoenix Channels) and managed services (Pusher, Ably) handle much of
this. Start with the **simplest mechanism that meets the latency need** — often
SSE or even long polling — and reach for WebSockets when you truly need two-way,
high-frequency communication.
""",
        ),
        _t(
            "Deploying & scaling web apps",
            "10 min",
            r"""# Deploying & scaling web apps

Shipping is a feature too. Getting a web app to users reliably and keeping it fast
under load pulls together the whole stack.

**The delivery pipeline (CI/CD):**

- **CI (Continuous Integration)** — on every push, automatically **build, lint,
  type-check, and test**. Catch breakage before it merges (you've seen this on
  this very platform).
- **CD (Continuous Delivery/Deployment)** — automatically deploy passing builds.
  Use **safe rollout** strategies — **blue-green** (switch traffic between two
  environments) or **canary** (send a small % of traffic to the new version
  first) — so a bad release is caught and rolled back fast.

**Where it runs:**

- **Static frontends** → a CDN/static host (Vercel, Netlify, Cloudflare Pages) —
  cheap, global, fast.
- **Backends** → containers (**Docker**) orchestrated (Kubernetes) or a PaaS;
  **serverless** functions for spiky/event workloads.

**Scaling the stack** reuses System Design directly:

- **Stateless app servers** behind a **load balancer** → scale out horizontally;
  keep **sessions** in Redis/JWT, **files** in object storage, so any server
  handles any request.
- **Cache** hot data (Redis) and **CDN** static/edge content.
- **Scale the database** last and carefully — read replicas, then sharding;
  it's the hardest tier (Databases/System Design tracks).
- **Autoscale** on load; design for **graceful degradation** under spikes.

**Operate what you ship — observability:**

- **Logs** (structured), **metrics** (latency, error rate, throughput,
  saturation), and **distributed tracing** to follow a request across services.
- **Alerting** on **SLOs/error budgets** (System Design), plus real-user
  monitoring of the **Core Web Vitals**.

The throughline of advanced web development: a great app isn't just well-coded,
it's **fast (performance + caching + CDN)**, **safe (the security model)**,
**resilient (stateless, redundant, observable)**, and **continuously deliverable**.
Those properties — not any single framework — are what make web software
production-grade.
""",
        ),
        quiz_lesson(
            "Quiz: Production Web Engineering",
            (
                q(
                    "Which usually has the biggest impact on web performance?",
                    (
                        opt(
                            "Shipping less JavaScript (code-splitting, lazy-loading, tree-shaking)",
                            correct=True,
                        ),
                        opt("Adding more CSS files"),
                        opt("Using more semantic tags"),
                        opt("Renaming variables"),
                    ),
                    "JS is the most expensive resource (download + parse + main-thread execution); cutting it most improves LCP/INP.",
                ),
                q(
                    "How do content-hashed asset names (app.9f3a2.js) help caching?",
                    (
                        opt(
                            "Files can be cached forever (immutable); a new deploy changes the hash/URL so caches never serve stale code",
                            correct=True,
                        ),
                        opt("They make files smaller"),
                        opt("They encrypt the files"),
                        opt("They disable the CDN"),
                    ),
                    "Immutable, long-cached URLs that change only when content changes give perfect caching without staleness.",
                ),
                q(
                    "What is the defence against XSS?",
                    (
                        opt(
                            "Escape/encode user data on output and apply a Content-Security-Policy",
                            correct=True,
                        ),
                        opt("Allow all inline scripts"),
                        opt("Disable HTTPS"),
                        opt("Store passwords in cookies"),
                    ),
                    "Context-aware escaping (plus CSP and framework auto-escaping) stops injected markup from executing.",
                ),
                q(
                    "What problem does CORS address?",
                    (
                        opt(
                            "It's the controlled exception to the Same-Origin Policy, letting a server opt in to cross-origin browser requests",
                            correct=True,
                        ),
                        opt("It encrypts traffic"),
                        opt("It is a server-side firewall"),
                        opt("It speeds up the database"),
                    ),
                    "The browser blocks cross-origin reads by default (SOP); CORS headers from the server selectively allow them.",
                ),
                q(
                    "When is GraphQL a better fit than REST?",
                    (
                        opt(
                            "Complex, nested data with many client shapes that suffer over/under-fetching from REST",
                            correct=True,
                        ),
                        opt("When HTTP URL caching is the top priority"),
                        opt("For the simplest possible CRUD resource"),
                        opt("When you want no schema at all"),
                    ),
                    "GraphQL lets clients fetch exactly the fields they need in one request; REST is simpler and more cacheable for plain resources.",
                ),
                q(
                    "Which real-time mechanism fits a two-way, high-frequency app like chat or multiplayer games?",
                    (
                        opt("WebSockets — a full-duplex, persistent connection", correct=True),
                        opt("Short polling"),
                        opt("Server-Sent Events (one-way only)"),
                        opt("A plain GET request"),
                    ),
                    "WebSockets give low-overhead bidirectional messaging; SSE is server→client only, and polling is laggy/wasteful.",
                ),
            ),
        ),
    ),
)


WEBDEV_COURSES = (_WEB_BASICS, _WEB_INTERMEDIATE, _WEB_ADVANCED)
