"""Academy seed content — Svelte — Basics.

A hands-on introduction to modern Svelte (version 5, runes): what makes
Svelte a compiler rather than a runtime, single-file components, reactive
state with $state and $derived, props, events and two-way bindings, logic
blocks for lists and conditions, effects and data loading, and composing
an app by lifting state up. Every lesson is a direct explanation with
runnable-style examples and a mermaid diagram, followed by a checkpoint
quiz; the course closes with a comprehensive final quiz.

Companion to ``seed_react`` — the two courses walk the same example apps
(profile card, counter, signup form, todo list) so learners can compare
the frameworks side by side.
"""

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


_SVELTE_BASICS = SeedCourse(
    slug="svelte-basics",
    title="Svelte — Basics",
    description=(
        "Build user interfaces with modern Svelte (runes) from zero: "
        "single-file components, reactive state with $state and $derived, "
        "props, events, two-way bindings, lists, effects and data loading - "
        "explained directly, with small realistic examples (a profile card, "
        "a counter, a todo list) and a diagram in every lesson."
    ),
    level="Beginner",
    lessons=(
        # ── Welcome ──────────────────────────────────────────────────
        _t(
            "Welcome — how this course works",
            "4 min",
            """# Svelte — Basics

Svelte is a framework for building user interfaces with a twist: it is a
**compiler**. Instead of shipping a library that interprets your app in
the browser, Svelte compiles your components into small, fast JavaScript
at build time. The result: less code to write, less code to ship.

The approach here is **small and concrete**: every lesson explains one
idea directly, shows it in a short example you could paste into a
project, and draws the idea as a diagram. After each lesson there is a
short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **What Svelte is** and why the compiler approach matters
2. **Single-file components** - markup, logic and style in one file
3. **Reactivity with runes** - `$state` and `$derived`
4. **Props** - passing data into components with `$props`
5. **Events and bindings** - `onclick` and `bind:value`
6. **Logic in markup** - `{#if}` and `{#each}` blocks
7. **Effects** - `$effect` and loading data
8. **Composition** - lifting state up and structuring an app

All examples use **modern Svelte (version 5) with runes**. To follow
along locally, create a project with `npx sv create` (or
`npm create vite@latest` with the Svelte template).
""",
        ),
        quiz_lesson(
            "Quiz: Welcome — how this course works",
            (
                q(
                    "What version and style of Svelte does this course teach?",
                    (
                        opt("Svelte 3 with reactive $: statements"),
                        opt("Modern Svelte (version 5) with runes", correct=True),
                        opt("Svelte with class components"),
                        opt("SvelteKit server routes only"),
                    ),
                    "All examples use the runes API ($state, $derived, $props, "
                    "$effect) - how Svelte has been written since version 5.",
                ),
                q(
                    "What is the headline difference between Svelte and most other UI frameworks?",
                    (
                        opt("It only runs on the server"),
                        opt("It requires TypeScript"),
                        opt(
                            "It is a compiler: components become plain JavaScript at "
                            "build time instead of being interpreted at runtime",
                            correct=True,
                        ),
                        opt("It renders to canvas instead of the DOM"),
                    ),
                    "Svelte moves the framework's work to the build step, shipping "
                    "small, direct DOM-updating code to the browser.",
                ),
            ),
        ),
        # ── 1. What is Svelte ────────────────────────────────────────
        _t(
            "What is Svelte and why a compiler?",
            "8 min",
            """# What is Svelte and why a compiler?

Frameworks like React ship a **runtime**: a library that lives in the
browser, holds a virtual DOM, and diffs it on every change to decide what
to update. Svelte took a different bet: since your components are known
at build time, a **compiler** can figure out exactly which DOM node each
piece of state touches - and generate code that updates only that.

```svelte
<script>
  let count = $state(0);
</script>

<button onclick={() => count++}>
  Clicked {count} times
</button>
```

That is a complete, working component. Notice what is missing: no
`setCount`, no re-render of the whole component - `count++` just works,
because the compiler saw that `{count}` in the markup depends on `count`
and wired a direct update.

What the compiler approach buys you:

- **Less boilerplate.** State is a variable; changing it is an
  assignment.
- **Small bundles.** There is no framework runtime to ship - your
  compiled components are the app.
- **Surgical updates.** No virtual DOM diffing: changed state updates
  the exact text node or attribute that uses it.

The mental model is the same one-way loop as any modern UI framework -
only the machinery underneath differs:

```mermaid
graph LR
    SRC["Svelte component source"] --> CP["Compiler at build time"]
    CP --> JS["Plain JavaScript output"]
    JS --> DOM["Direct DOM updates"]
    ST["State assignment"] --> JS
```

The one thing to remember: in Svelte, the framework disappears at build
time - you write declarative components, the browser receives plain,
targeted JavaScript.
""",
        ),
        quiz_lesson(
            "Quiz: What is Svelte and why a compiler?",
            (
                q(
                    "How does Svelte update the page when state changes?",
                    (
                        opt("It re-renders the whole app and diffs a virtual DOM"),
                        opt(
                            "The compiler generated code that updates exactly the DOM "
                            "nodes that depend on the changed state",
                            correct=True,
                        ),
                        opt("It reloads the page section via AJAX"),
                        opt("It queries the DOM for elements marked dirty"),
                    ),
                    "Because components are compiled, Svelte knows at build time which "
                    "node uses which state - no runtime diffing needed.",
                ),
                q(
                    "In the counter example, why does count++ update the button text "
                    "without any setter function?",
                    (
                        opt("Svelte polls all variables every animation frame"),
                        opt("The ++ operator is overloaded by the framework at runtime"),
                        opt("It does not - a setter is still required"),
                        opt(
                            "count is declared with $state, so the compiler wires "
                            "assignments to the DOM updates that depend on it",
                            correct=True,
                        ),
                    ),
                    "$state marks the variable as reactive; from then on plain "
                    "assignments are the update API.",
                ),
                q(
                    "Which is a direct consequence of having no framework runtime?",
                    (
                        opt("Smaller JavaScript bundles shipped to the browser", correct=True),
                        opt("Svelte apps cannot use npm packages"),
                        opt("Components must be written in plain HTML files"),
                        opt("The browser must support WebAssembly"),
                    ),
                    "The compiled components are the app - there is no library "
                    "interpreting them, which keeps payloads small.",
                ),
            ),
        ),
        # ── 2. Single-file components ────────────────────────────────
        _t(
            "Single-file components",
            "9 min",
            """# Single-file components

A Svelte component is a `.svelte` file with up to three sections -
**logic, markup and style** - and the file name (capitalized) is the
component's name:

```svelte
<!-- ProfileCard.svelte -->
<script>
  const user = { name: "Grace Hopper", role: "Rear Admiral", online: true };
</script>

<h2 class="card-title">{user.name}</h2>
<p>{user.role}</p>
<span>{user.online ? "online" : "offline"}</span>

<style>
  .card-title {
    color: navy;
  }
</style>
```

The rules that make this pleasant:

- **Markup is HTML.** Unlike JSX there is no `className`, no mandatory
  single root, no self-closing requirements beyond HTML's own. `{...}`
  embeds any JavaScript expression, exactly like you would hope.
- **Styles are scoped by default.** That `.card-title` rule applies only
  to this component - the compiler adds a unique class under the hood,
  so components never leak CSS into each other.
- **The script runs once per component instance**, setting up its state
  and functions.

Using a component is an import plus a tag:

```svelte
<!-- App.svelte -->
<script>
  import ProfileCard from "./ProfileCard.svelte";
</script>

<main>
  <ProfileCard />
  <ProfileCard />
</main>
```

```mermaid
graph TD
    F["ProfileCard.svelte"] --> SC["script - logic"]
    F --> MK["markup - HTML plus braces"]
    F --> ST["style - scoped CSS"]
    APP["App.svelte"] --> I["import ProfileCard"]
    I --> U["Use as a tag"]
```

One file, three concerns, zero configuration - that is the component
model.
""",
        ),
        quiz_lesson(
            "Quiz: Single-file components",
            (
                q(
                    "What are the three sections a .svelte file can contain?",
                    (
                        opt("template, controller and module"),
                        opt("script, markup and style", correct=True),
                        opt("header, body and footer"),
                        opt("state, props and events"),
                    ),
                    "Logic in <script>, HTML markup, and a <style> block - all "
                    "optional, all in one file.",
                ),
                q(
                    "What happens to CSS written in a component's <style> block?",
                    (
                        opt("It applies globally to the whole app"),
                        opt("It must be imported by every other component"),
                        opt(
                            "It is scoped to that component only - the compiler makes "
                            "sure it cannot leak",
                            correct=True,
                        ),
                        opt("It is ignored unless marked with !important"),
                    ),
                    "Scoped styles by default: each component's rules are rewritten "
                    "with a unique class so components never fight over CSS.",
                ),
                q(
                    "How does Svelte markup differ from React's JSX?",
                    (
                        opt(
                            "It is plain HTML - class works, multiple root elements are "
                            "fine, and braces embed expressions",
                            correct=True,
                        ),
                        opt("It uses XML namespaces for every tag"),
                        opt("Expressions are embedded with %% instead of braces"),
                        opt("It requires a single root div per component"),
                    ),
                    "Svelte templates stay close to real HTML; the compiler handles the rest.",
                ),
            ),
        ),
        # ── 3. Reactivity with runes ─────────────────────────────────
        _t(
            "Reactivity — $state and $derived",
            "10 min",
            """# Reactivity — $state and $derived

Runes are Svelte's reactivity primitives - compiler keywords that start
with `$`. The two you will use constantly:

**`$state`** declares reactive data. Assign to it and every place that
uses it updates:

```svelte
<script>
  let count = $state(0);
  let todos = $state([]);

  function addTodo(text) {
    todos.push({ id: Date.now(), text, done: false });
  }
</script>
```

Note the contrast with other frameworks: `todos.push(...)` **just
works**. `$state` wraps objects and arrays in a deep reactive proxy, so
mutations are tracked - no spread-and-replace ceremony required.

**`$derived`** declares data computed from other state. It re-computes
automatically when its dependencies change:

```svelte
<script>
  let todos = $state([]);
  let remaining = $derived(todos.filter((t) => !t.done).length);
</script>

<p>{remaining} tasks remaining</p>
```

The rules:

- **Declare state with `$state`, change it with plain assignments and
  mutations.** The compiler tracks reads and writes.
- **Never store what you can derive.** `remaining` is not a second piece
  of state to keep in sync - it is a formula that stays correct by
  construction.
- **`$derived` is read-only.** Assigning to it is an error; change the
  state it derives from.
- Runes exist at compile time - you do not import them; they are part of
  the language inside `.svelte` (and `.svelte.js`/`.svelte.ts`) files.

```mermaid
graph LR
    S["todos state"] --> D["remaining derived"]
    S --> M["List markup"]
    D --> P["Counter markup"]
    A["Assignment or mutation"] --> S
```

State is what you own; derived is what follows from it; the markup
follows both - automatically.
""",
        ),
        quiz_lesson(
            "Quiz: Reactivity — $state and $derived",
            (
                q(
                    "How do you update an array declared with $state in Svelte?",
                    (
                        opt("Only by replacing it with a spread: todos = [...todos, x]"),
                        opt("By calling setTodos with a new array"),
                        opt(
                            "Plain mutations like todos.push(x) work - $state proxies "
                            "track them deeply",
                            correct=True,
                        ),
                        opt("Arrays cannot be reactive in Svelte"),
                    ),
                    "$state wraps objects and arrays in a deep reactive proxy, so "
                    "ordinary JavaScript mutations trigger updates.",
                ),
                q(
                    "What is $derived for?",
                    (
                        opt(
                            "Values computed from other state that re-compute "
                            "automatically when their dependencies change",
                            correct=True,
                        ),
                        opt("Importing state from another component"),
                        opt("Persisting state to localStorage"),
                        opt("Declaring props with default values"),
                    ),
                    "remaining = $derived(todos.filter(...).length) stays correct by "
                    "construction - no manual syncing.",
                ),
                q(
                    "Why should the remaining-tasks count be $derived instead of its own $state?",
                    (
                        opt("$state cannot hold numbers"),
                        opt(
                            "Storing derivable data creates a second source of truth "
                            "that can drift out of sync",
                            correct=True,
                        ),
                        opt("$derived is the only rune allowed in markup"),
                        opt("It renders faster on the first paint"),
                    ),
                    "Derive what you can, store only what you must - the same "
                    "principle as every declarative framework.",
                ),
            ),
        ),
        # ── 4. Props ─────────────────────────────────────────────────
        _t(
            "Props — component inputs with $props",
            "9 min",
            """# Props — component inputs with $props

Props are the data a component receives from its parent. In modern
Svelte you declare them by destructuring **`$props()`**, with plain
JavaScript defaults:

```svelte
<!-- Badge.svelte -->
<script>
  let { label, color = "gray" } = $props();
</script>

<span style="background: {color}">{label}</span>
```

```svelte
<!-- App.svelte -->
<script>
  import Badge from "./Badge.svelte";
</script>

<header>
  <Badge label="New" color="green" />
  <Badge label="Sale" color="red" />
  <Badge label="Draft" />   <!-- uses the gray default -->
</header>
```

The rules mirror every component system:

- **Data flows down.** The parent chooses the values; the child reads
  them. A child does not reassign its own props.
- **Defaults are destructuring defaults** - `color = "gray"` applies
  when the parent omits the prop.
- **`children` is a snippet prop.** Content nested between a component's
  tags arrives as `children`, rendered with `{@render}`:

```svelte
<!-- Card.svelte -->
<script>
  let { title, children } = $props();
</script>

<section class="card">
  <h3>{title}</h3>
  {@render children()}
</section>
```

```svelte
<Card title="About">
  <p>Svelte was released in 2016.</p>
</Card>
```

```mermaid
graph TD
    A["App"] --> B1["Badge label New"]
    A --> B2["Badge label Sale"]
    A --> C["Card title About"]
    C --> CH["children snippet rendered"]
```

Same one-way rule as everywhere: values go down as props; changes go up
as events - which is the next lesson.
""",
        ),
        quiz_lesson(
            "Quiz: Props — component inputs with $props",
            (
                q(
                    "How does a modern Svelte component declare its props?",
                    (
                        opt("export let label - one export per prop"),
                        opt("this.props.label inside a class"),
                        opt("let { label, color = 'gray' } = $props()", correct=True),
                        opt("Reading window.svelteProps at mount"),
                    ),
                    "Destructuring $props() declares the inputs, with plain "
                    "destructuring defaults for optional ones.",
                ),
                q(
                    "How do you give a prop a default value?",
                    (
                        opt(
                            "A destructuring default: let { color = 'gray' } = $props()",
                            correct=True,
                        ),
                        opt("A separate defaults.json file"),
                        opt("Calling setDefault('color', 'gray')"),
                        opt("Props cannot have defaults in Svelte"),
                    ),
                    "It is plain JavaScript destructuring - the default applies when "
                    "the parent omits the prop.",
                ),
                q(
                    "What does {@render children()} do in a component?",
                    (
                        opt("Re-renders the whole component tree"),
                        opt(
                            "Renders the content the parent nested between the "
                            "component's opening and closing tags",
                            correct=True,
                        ),
                        opt("Renders the component's own markup recursively"),
                        opt("Imports a child component by name"),
                    ),
                    "Nested content arrives as the children snippet prop; @render "
                    "places it - the basis of wrapper components like Card.",
                ),
            ),
        ),
        # ── 5. Events & bindings ─────────────────────────────────────
        _t(
            "Events and two-way bindings",
            "10 min",
            """# Events and two-way bindings

**Events** are plain DOM attributes with a function value: `onclick`,
`oninput`, `onsubmit`. Lowercase, like HTML - not camelCase:

```svelte
<script>
  let count = $state(0);
  function handleClick() {
    count++;
  }
</script>

<button onclick={handleClick}>Clicked {count} times</button>
<button onclick={() => (count = 0)}>Reset</button>
```

The same classic mistake applies as in every framework:
`onclick={handleClick}` passes the function; `onclick={handleClick()}`
calls it during render. Wrap in an arrow to pass arguments.

**Bindings** are Svelte's shortcut for forms. Where React requires the
value/onChange pair, Svelte gives you **`bind:value`** - two-way binding
between an input and state:

```svelte
<script>
  let email = $state("");

  function handleSubmit(event) {
    event.preventDefault(); // stop the browser's page reload
    console.log("subscribing", email);
    email = "";
  }
</script>

<form onsubmit={handleSubmit}>
  <input type="email" bind:value={email} placeholder="you@example.com" />
  <button disabled={email === ""}>Subscribe</button>
</form>
```

Typing updates `email`; assigning to `email` updates the field. One
source of truth, zero plumbing - the disabled button and the one-line
reset come for free.

Other useful bindings: `bind:checked` (checkboxes), `bind:group` (radio
sets), `bind:this` (a reference to the DOM element).

```mermaid
graph LR
    T["User types"] --> B["bind value"]
    B --> S["email state"]
    S --> V["Input displays state"]
    S --> D["Button disabled logic"]
    SET["Assignment email equals empty"] --> S
```

Events react to the user; bindings keep state and inputs in lockstep -
both with plain HTML-looking syntax.
""",
        ),
        quiz_lesson(
            "Quiz: Events and two-way bindings",
            (
                q(
                    "How are click handlers written in modern Svelte?",
                    (
                        opt("onClick={handler} - camelCase like JSX"),
                        opt("onclick={handler} - lowercase, like an HTML attribute", correct=True),
                        opt("on:click|handler as a directive with a pipe"),
                        opt("addEventListener inside the style block"),
                    ),
                    "Svelte 5 events are plain lowercase attributes taking a function value.",
                ),
                q(
                    "What does bind:value={email} on an input do?",
                    (
                        opt("Validates the input as an email address"),
                        opt("Copies the input's initial value into state once"),
                        opt(
                            "Two-way binds the field and the state: typing updates "
                            "email, assigning to email updates the field",
                            correct=True,
                        ),
                        opt("Prevents the input from being edited"),
                    ),
                    "bind:value replaces the manual value/onChange pair - one source "
                    "of truth in both directions.",
                ),
                q(
                    "Why call event.preventDefault() in a form's onsubmit handler?",
                    (
                        opt(
                            "To stop the browser's default full-page reload on submit", correct=True
                        ),
                        opt("To prevent Svelte from recompiling"),
                        opt("To clear all $state in the component"),
                        opt("To disable the submit button permanently"),
                    ),
                    "Browsers navigate on form submit by default; an app handling "
                    "the data itself cancels that.",
                ),
            ),
        ),
        # ── 6. Logic blocks ──────────────────────────────────────────
        _t(
            "Logic in markup — if and each blocks",
            "9 min",
            """# Logic in markup — if and each blocks

Svelte markup has **logic blocks** - template syntax for the two things
every UI does: show things conditionally and render lists.

**Conditions** use `{#if}` / `{:else if}` / `{:else}`:

```svelte
<script>
  let { messages, loading } = $props();
</script>

{#if loading}
  <p>Loading...</p>
{:else if messages.length === 0}
  <p>No messages.</p>
{:else}
  <ul>...</ul>
{/if}
```

Read the delimiters once and you know them all: `#` opens a block, `:`
continues it, `/` closes it.

**Lists** use `{#each}` with a **key in parentheses** so Svelte can track
items across reorders, inserts and deletes:

```svelte
<script>
  let todos = $state([
    { id: 1, text: "Learn blocks", done: true },
    { id: 2, text: "Build an app", done: false },
  ]);
</script>

<ul>
  {#each todos as todo (todo.id)}
    <li class:done={todo.done}>{todo.text}</li>
  {:else}
    <li>Nothing to do!</li>
  {/each}
</ul>
```

Two details worth noticing:

- **`(todo.id)` is the key.** Without it, Svelte matches items by
  position - reorder the array and per-row state (like a focused input)
  sticks to the wrong row. Use the data's own id, not the index.
- **`{:else}` on an each block** renders when the list is empty - the
  empty state lives right next to the list, no separate condition.
- **`class:done={todo.done}`** toggles a CSS class from a boolean - a
  tiny directive you will use constantly.

```mermaid
graph TD
    D["Data"] --> IFB["if block chooses a branch"]
    D --> EB["each block with key per item"]
    EB --> LI["List items tracked by id"]
    EB --> EMP["else branch when empty"]
```

Conditions choose a branch, each-blocks map data to rows, and keys give
rows identity - dynamic rendering in three delimiters.
""",
        ),
        quiz_lesson(
            "Quiz: Logic in markup — if and each blocks",
            (
                q(
                    "What do the #, : and / prefixes mean in Svelte blocks?",
                    (
                        opt("# opens a block, : continues it, / closes it", correct=True),
                        opt("They are comment markers of different priorities"),
                        opt("# is for CSS ids, : for pseudo-classes, / for paths"),
                        opt("They mark compile errors to fix"),
                    ),
                    "{#if} ... {:else} ... {/if} and {#each} ... {/each} all follow "
                    "the same open/continue/close grammar.",
                ),
                q(
                    "In {#each todos as todo (todo.id)}, what is (todo.id)?",
                    (
                        opt("A filter that skips items without an id"),
                        opt("The sort order for the list"),
                        opt(
                            "The key - a stable identity so reorders and inserts update "
                            "the right rows",
                            correct=True,
                        ),
                        opt("A performance hint with no behavioral effect"),
                    ),
                    "Keyed each-blocks track items by identity instead of position - "
                    "the same reason React lists need key props.",
                ),
                q(
                    "How do you render an empty state when an each block's list has no items?",
                    (
                        opt("Wrap the list in a try/catch block"),
                        opt("An {:else} branch inside the each block", correct=True),
                        opt("Svelte renders 'empty' automatically"),
                        opt("A second component with a media query"),
                    ),
                    "{#each} ... {:else} <empty state/> {/each} keeps the empty case "
                    "next to the list it belongs to.",
                ),
            ),
        ),
        # ── 7. Effects & data ────────────────────────────────────────
        _t(
            "$effect and loading data",
            "10 min",
            """# $effect and loading data

Rendering is pure; talking to the outside world is not. **`$effect`**
runs a function after the component is on screen and re-runs it when any
state it **reads** changes - dependencies are tracked automatically, no
dependency array to maintain:

```svelte
<script>
  let { userId } = $props();
  let user = $state(null);

  $effect(() => {
    let cancelled = false;
    fetch(`/api/users/${userId}`)
      .then((res) => res.json())
      .then((data) => {
        if (!cancelled) user = data;
      });
    return () => {
      cancelled = true; // cleanup: ignore late responses
    };
  });
</script>

{#if user}
  <h2>{user.name}</h2>
{:else}
  <p>Loading...</p>
{/if}
```

Because the effect reads `userId`, it re-runs when `userId` changes -
automatically. The **returned function is the cleanup**: it runs before
each re-run and when the component is destroyed, the place to cancel
requests, clear intervals and unsubscribe.

For simple page-load fetches there is an even more direct tool - the
**`{#await}` block** renders a promise's three states inline:

```svelte
<script>
  let postsPromise = fetch("/api/posts").then((r) => r.json());
</script>

{#await postsPromise}
  <p>Loading posts...</p>
{:then posts}
  <ul>
    {#each posts as post (post.id)}
      <li>{post.title}</li>
    {/each}
  </ul>
{:catch error}
  <p>Failed: {error.message}</p>
{/await}
```

When to use which: `{#await}` for fire-once page data; `$effect` when
the work depends on changing state or needs cleanup.

One warning, same as every framework: **do not use `$effect` for derived
values**. `let total = $derived(items.length)` - not an effect that
assigns state, which invites loops and sync bugs.

```mermaid
graph TD
    R["Component on screen"] --> E["effect runs"]
    E --> F["fetch or subscribe"]
    F --> S["state assignment"]
    S --> UI["Markup updates"]
    DEP["Read state changes"] --> CL["Cleanup runs"]
    CL --> E
```

Effects synchronize you with the outside world; awaits render a promise;
derived values need neither.
""",
        ),
        quiz_lesson(
            "Quiz: $effect and loading data",
            (
                q(
                    "How does $effect know when to re-run?",
                    (
                        opt("You pass it a dependency array as the second argument"),
                        opt(
                            "It tracks which reactive state the function reads and "
                            "re-runs when any of it changes",
                            correct=True,
                        ),
                        opt("It re-runs on every animation frame"),
                        opt("It never re-runs - effects fire once"),
                    ),
                    "Dependencies are tracked automatically from what the effect "
                    "actually reads - no array to maintain or lie about.",
                ),
                q(
                    "What renders each of a promise's three states inline in markup?",
                    (
                        opt("{#promise} ... {/promise}"),
                        opt("{#if loading} with a manual flag only"),
                        opt(
                            "{#await promise} ... {:then value} ... {:catch error} ... {/await}",
                            correct=True,
                        ),
                        opt("A try/catch around the markup"),
                    ),
                    "The await block handles pending, resolved and rejected states "
                    "right where the data is used.",
                ),
                q(
                    "What is the function returned from a $effect for?",
                    (
                        opt(
                            "Cleanup - it runs before the effect re-runs and when the "
                            "component is destroyed",
                            correct=True,
                        ),
                        opt("It becomes the effect's derived value"),
                        opt("It renders the loading fallback"),
                        opt("It is called to validate the effect's dependencies"),
                    ),
                    "Effects that start something must stop it: cancel fetches, clear "
                    "timers, unsubscribe - in the returned cleanup.",
                ),
            ),
        ),
        # ── 8. Composition ───────────────────────────────────────────
        _t(
            "Composition — lifting state up",
            "10 min",
            """# Composition — lifting state up

When two components need the **same data** - a form that adds todos and
a list that shows them - the state moves to their closest common parent,
which passes **values down and callbacks up**. The same tiny todo app as
the React course, in Svelte:

```svelte
<!-- TodoInput.svelte -->
<script>
  let { onAdd } = $props();
  let text = $state("");
</script>

<form
  onsubmit={(e) => {
    e.preventDefault();
    if (text.trim() === "") return;
    onAdd(text);
    text = "";
  }}
>
  <input bind:value={text} />
  <button>Add</button>
</form>
```

```svelte
<!-- TodoList.svelte -->
<script>
  let { todos, onToggle } = $props();
</script>

<ul>
  {#each todos as t (t.id)}
    <li onclick={() => onToggle(t.id)} class:done={t.done}>
      {t.text}
    </li>
  {/each}
</ul>
```

```svelte
<!-- TodoApp.svelte -->
<script>
  import TodoInput from "./TodoInput.svelte";
  import TodoList from "./TodoList.svelte";

  let todos = $state([]);
  let remaining = $derived(todos.filter((t) => !t.done).length);

  function addTodo(text) {
    todos.push({ id: Date.now(), text, done: false });
  }
  function toggleTodo(id) {
    const todo = todos.find((t) => t.id === id);
    if (todo) todo.done = !todo.done;
  }
</script>

<main>
  <TodoInput onAdd={addTodo} />
  <TodoList {todos} onToggle={toggleTodo} />
  <p>{remaining} remaining</p>
</main>
```

The shape to internalize:

- **One owner.** `TodoApp` holds `todos`; the input and list stay simple
  and reusable because they own nothing shared.
- **Values down, callbacks up.** Children receive `todos` and call
  `onAdd`/`onToggle`; they never edit shared data themselves.
- **Mutations are fine here** - `todos.push(...)` and `todo.done = !todo.done`
  work because `$state` is deeply reactive. Notice also the `{todos}`
  shorthand for `todos={todos}`.
- **Derived stays derived.** `remaining` is a formula, not a second
  state.

```mermaid
graph TD
    APP["TodoApp owns todos state"] --> IN["TodoInput"]
    APP --> LI["TodoList"]
    APP --> CT["remaining derived"]
    IN -- "onAdd text" --> APP
    LI -- "onToggle id" --> APP
```

Find who needs the data, put the state one level above them, hand values
down and callbacks up - the universal shape of component apps.
""",
        ),
        quiz_lesson(
            "Quiz: Composition — lifting state up",
            (
                q(
                    "Two sibling components need to share changing data. Where does the $state go?",
                    (
                        opt("Duplicated in both, synced with effects"),
                        opt("In the closest common parent, passed down as props", correct=True),
                        opt("In the browser's sessionStorage"),
                        opt("In a global window variable"),
                    ),
                    "Lifting state up: one owner, one source of truth, siblings "
                    "receive values and callbacks.",
                ),
                q(
                    "How does TodoInput add a todo it does not own?",
                    (
                        opt("It pushes directly into the todos prop"),
                        opt("It emits a DOM CustomEvent the parent listens to"),
                        opt(
                            "It calls the onAdd callback prop so the owner updates its own state",
                            correct=True,
                        ),
                        opt("It re-imports TodoApp and mutates its module state"),
                    ),
                    "Values down, callbacks up: the parent hands a function; the "
                    "child calls it with the new text.",
                ),
                q(
                    "Why is toggleTodo allowed to write todo.done = !todo.done directly?",
                    (
                        opt("It is a bug that happens to work in dev mode"),
                        opt("Svelte re-renders everything every second anyway"),
                        opt("done is not reactive, so no update is needed"),
                        opt(
                            "$state is deeply reactive - mutating a proxied object "
                            "triggers the exact updates that depend on it",
                            correct=True,
                        ),
                    ),
                    "Deep reactivity is a Svelte signature: plain JavaScript mutation "
                    "is the update API, with the owner still in control.",
                ),
            ),
        ),
        # ── Final quiz ───────────────────────────────────────────────
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What fundamentally distinguishes Svelte from runtime frameworks like React?",
                    (
                        opt(
                            "Components compile to plain JavaScript at build time that "
                            "updates the DOM directly - no virtual DOM diffing at runtime",
                            correct=True,
                        ),
                        opt("Svelte runs components in a Web Worker"),
                        opt("Svelte apps cannot run in the browser"),
                        opt("Svelte re-renders the full page on every change"),
                    ),
                    "The framework disappears at build time; the browser receives "
                    "small, targeted update code.",
                ),
                q(
                    "Which snippet declares reactive component state in modern Svelte?",
                    (
                        opt("let count = $state(0)", correct=True),
                        opt("const [count, setCount] = useState(0)"),
                        opt("let count = reactive(0)"),
                        opt("$: count = 0"),
                    ),
                    "$state is the rune for reactive data; assignments and mutations "
                    "then drive updates.",
                ),
                q(
                    "Where does scoped CSS for a component live?",
                    (
                        opt("In a .module.css file next to the component"),
                        opt("In the component's <style> block - scoped by default", correct=True),
                        opt("Inline on every element, required by the compiler"),
                        opt("In a global stylesheet with data attributes you write"),
                    ),
                    "Each .svelte file's style block applies only to that component - "
                    "no leaking, no configuration.",
                ),
                q(
                    "How does a component declare an optional prop with a default?",
                    (
                        opt("let { color = 'gray' } = $props()", correct=True),
                        opt("export let color default 'gray'"),
                        opt("defineProps({ color: 'gray' })"),
                        opt("this.color = this.props.color or 'gray'"),
                    ),
                    "Destructure $props() with a plain destructuring default.",
                ),
                q(
                    "Which is the correct two-way binding between an input and state?",
                    (
                        opt("<input value={email} onChange={setEmail} />"),
                        opt("<input model='email' />"),
                        opt("<input bind:value={email} />", correct=True),
                        opt("<input sync={email} />"),
                    ),
                    "bind:value keeps the field and the state in lockstep in both "
                    "directions - Svelte's form shortcut.",
                ),
                q(
                    "In an each block, why write {#each todos as todo (todo.id)} "
                    "instead of omitting the parentheses?",
                    (
                        opt(
                            "The key gives rows identity so reorders and inserts update the right rows",
                            correct=True,
                        ),
                        opt("It sorts the list by id automatically"),
                        opt("The syntax is invalid without it"),
                        opt("It caches the list between page loads"),
                    ),
                    "Unkeyed lists match by position; keyed lists match by identity - "
                    "essential once the list can change shape.",
                ),
                q(
                    "todos is $state([]). Which update is WRONG in Svelte?",
                    (
                        opt("todos.push(newTodo)"),
                        opt("todos = [...todos, newTodo]"),
                        opt("todos[0].done = true"),
                        opt("None of them - all three are valid reactive updates", correct=True),
                    ),
                    "Deep $state proxies make mutation and replacement both valid - "
                    "unlike frameworks where only replacement triggers updates.",
                ),
                q(
                    "What is the main difference between $derived and $effect?",
                    (
                        opt("They are aliases for the same rune"),
                        opt("$derived runs only once; $effect runs continuously"),
                        opt(
                            "$derived computes a value from state; $effect performs "
                            "side effects like fetching or subscribing",
                            correct=True,
                        ),
                        opt("$effect is for CSS, $derived for JavaScript"),
                    ),
                    "Compute values with $derived; reach outside the component with "
                    "$effect - and never use an effect to compute what a derived "
                    "can express.",
                ),
                q(
                    "A component fetches /api/users/{userId} in a $effect. The parent "
                    "changes userId. What happens?",
                    (
                        opt("Nothing - effects ignore prop changes"),
                        opt(
                            "The cleanup runs, then the effect re-runs with the new "
                            "userId, because the effect reads it",
                            correct=True,
                        ),
                        opt("The component unmounts and remounts"),
                        opt("Svelte throws unless a dependency array lists userId"),
                    ),
                    "Automatic dependency tracking: reading userId inside the effect "
                    "subscribes to it; cleanup runs before each re-run.",
                ),
                q(
                    "The todo app keeps todos in TodoApp and hands TodoInput an onAdd "
                    "callback. What principle is that?",
                    (
                        opt("Server-side rendering"),
                        opt("Dependency injection via context"),
                        opt(
                            "Lifting state up: one owner, values down as props, changes "
                            "up as callbacks",
                            correct=True,
                        ),
                        opt("Publish-subscribe with a global event bus"),
                    ),
                    "The universal composition shape: the closest common parent owns "
                    "the shared state.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

SVELTE_COURSES: tuple[SeedCourse, ...] = (_SVELTE_BASICS,)
