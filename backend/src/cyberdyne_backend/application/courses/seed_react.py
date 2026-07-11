"""Academy seed content — React — Basics.

A hands-on introduction to React with modern function components and
hooks: what React is and why it exists, JSX, components and props, state
with useState, events and controlled forms, lists and conditional
rendering, effects and data fetching, and composition by lifting state
up. Every lesson is a direct explanation with runnable-style examples and
a mermaid diagram, followed by a checkpoint quiz; the course closes with
a comprehensive final quiz.
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


_REACT_BASICS = SeedCourse(
    slug="react-basics",
    title="React — Basics",
    description=(
        "Build user interfaces with React from zero: components, JSX, props, "
        "state, events, controlled forms, lists, effects and data fetching - "
        "explained directly, with small realistic examples (a profile card, a "
        "counter, a todo list) and a diagram in every lesson."
    ),
    level="Beginner",
    lessons=(
        # ── Welcome ──────────────────────────────────────────────────
        _t(
            "Welcome — how this course works",
            "4 min",
            """# React — Basics

React is the most widely used library for building user interfaces in
JavaScript. If you know basic HTML, CSS and JavaScript, this course takes
you to the point where you can build a real interactive app.

The approach here is **small and concrete**: every lesson explains one
idea directly, shows it in a short example you could paste into a project,
and draws the idea as a diagram. After each lesson there is a short quiz;
at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **What React is** and the mental model behind it
2. **JSX** — writing markup in JavaScript
3. **Components and props** — the building blocks
4. **State** — making the UI interactive with `useState`
5. **Events and forms** — reacting to the user
6. **Lists and conditional rendering** — real UIs are collections
7. **Effects** — talking to the outside world with `useEffect`
8. **Composition** — lifting state up and structuring an app

All examples use **modern React**: function components and hooks only.
To follow along locally, create a project with `npm create vite@latest`
and pick the React template.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome — how this course works",
            (
                q(
                    "What style of React does this course teach?",
                    (
                        opt("Class components with lifecycle methods"),
                        opt("Modern function components with hooks", correct=True),
                        opt("Server-side templates rendered by PHP"),
                        opt("jQuery-style direct DOM manipulation"),
                    ),
                    "All examples use function components and hooks - the way React "
                    "has been written since hooks arrived, and the only style new "
                    "code should use.",
                ),
                q(
                    "What prior knowledge does the course assume?",
                    (
                        opt("None at all - it teaches programming from zero"),
                        opt("Deep TypeScript and build-tooling experience"),
                        opt("Basic HTML, CSS and JavaScript", correct=True),
                        opt("A previous UI framework such as Angular"),
                    ),
                    "React builds directly on the web platform: you write JavaScript "
                    "that produces HTML-like markup, so the basics of all three are "
                    "the prerequisite.",
                ),
            ),
        ),
        # ── 1. What is React ─────────────────────────────────────────
        _t(
            "What is React and why does it exist?",
            "8 min",
            """# What is React and why does it exist?

Before React, interactive pages were built by **manually updating the
DOM**: find an element, change its text, add a class, remove a child.
As apps grew, keeping the page in sync with the data became the main
source of bugs - every piece of code could touch every part of the page.

React's core idea is **declarative UI**: you do not describe *how* to
update the page, you describe *what the page should look like* for a
given data. When the data changes, React re-renders your description and
updates only the parts of the real DOM that actually changed.

```jsx
// Imperative (without React): how to change the page
const el = document.querySelector("#count");
el.textContent = String(count);

// Declarative (React): what the page is
function Counter({ count }) {
  return <p id="count">{count}</p>;
}
```

Three concepts carry the whole library:

- **Components** - reusable functions that return markup. An app is a
  tree of components, like HTML is a tree of tags.
- **Props** - the inputs a component receives from its parent.
- **State** - data owned by a component that can change over time; when
  it changes, React re-renders that component.

The flow is always the same one-way loop: **state changes cause a
render, the render produces the UI, the UI fires events, events change
state**.

```mermaid
graph LR
    S["State"] --> R["Render"]
    R --> U["UI on screen"]
    U --> E["User event"]
    E --> S
```

The one thing to remember: in React you never edit the page - you change
the data, and the page follows.
""",
        ),
        quiz_lesson(
            "Quiz: What is React and why does it exist?",
            (
                q(
                    "What does 'declarative UI' mean in React?",
                    (
                        opt(
                            "You describe what the UI should look like for given data, "
                            "and React applies the DOM changes",
                            correct=True,
                        ),
                        opt("You write step-by-step DOM update instructions"),
                        opt("The UI is declared in XML configuration files"),
                        opt("Every component must declare its CSS inline"),
                    ),
                    "React inverts the old model: instead of imperative DOM edits you "
                    "return the desired markup, and React reconciles the real DOM to "
                    "match it.",
                ),
                q(
                    "Which is the correct direction of React's data flow loop?",
                    (
                        opt("UI changes state directly, state edits the DOM"),
                        opt(
                            "State change -> render -> UI -> user event -> state change",
                            correct=True,
                        ),
                        opt("Events edit the DOM, the DOM updates the state"),
                        opt("Render happens once; afterwards only the DOM changes"),
                    ),
                    "It is a one-way loop: data drives the render, the render produces "
                    "the UI, and user events feed back into the data.",
                ),
                q(
                    "What are the three concepts the lesson says carry all of React?",
                    (
                        opt("Routers, reducers and middlewares"),
                        opt("Templates, controllers and services"),
                        opt("Components, props and state", correct=True),
                        opt("Classes, mixins and decorators"),
                    ),
                    "Components are the building blocks, props are their inputs, and "
                    "state is the data that changes over time.",
                ),
            ),
        ),
        # ── 2. JSX ───────────────────────────────────────────────────
        _t(
            "JSX — markup inside JavaScript",
            "9 min",
            """# JSX — markup inside JavaScript

JSX is the syntax that lets you write HTML-like markup inside JavaScript.
It is not a template language: **it compiles to plain JavaScript function
calls**, so everything JavaScript can do is available inside it.

```jsx
const name = "Ada";
const element = <h1 className="title">Hello, {name}!</h1>;
```

The rules that differ from HTML - these cause 90% of beginner errors:

- **`{expression}` embeds JavaScript.** Anything inside braces is
  evaluated: `{user.name}`, `{2 + 2}`, `{items.length > 0 ? "yes" : "no"}`.
  Statements (`if`, `for`) do not go inside braces - use expressions.
- **`className`, not `class`** - and `htmlFor`, not `for` - because JSX
  attributes are JavaScript property names.
- **Every tag closes.** `<img />`, `<br />`, `<input />` - self-closing
  is mandatory.
- **One root element per return.** Wrap siblings in a fragment
  `<>...</>` when you do not want an extra `<div>`.
- **Attributes take expressions too**: `<img src={user.avatarUrl} />`,
  `<button disabled={isSaving}>`.

A realistic example - a profile card written only with JSX rules:

```jsx
function ProfileCard() {
  const user = { name: "Grace Hopper", role: "Rear Admiral", online: true };
  return (
    <>
      <h2 className="card-title">{user.name}</h2>
      <p>{user.role}</p>
      <span>{user.online ? "online" : "offline"}</span>
    </>
  );
}
```

How the pieces relate:

```mermaid
graph TD
    J["JSX source"] --> C["Compiler build step"]
    C --> F["JavaScript function calls"]
    F --> V["React element tree"]
    V --> D["Real DOM updates"]
```

Remember: JSX is JavaScript wearing HTML clothes - braces switch you
back to code, and the compiler turns the whole thing into function calls.
""",
        ),
        quiz_lesson(
            "Quiz: JSX — markup inside JavaScript",
            (
                q(
                    "What do curly braces { } do inside JSX?",
                    (
                        opt("Define a CSS block scoped to the component"),
                        opt("Embed any JavaScript expression into the markup", correct=True),
                        opt("Mark a section as HTML comments"),
                        opt("Create a new component automatically"),
                    ),
                    "Braces evaluate a JavaScript expression - a variable, a ternary, "
                    "a function call - and place its result in the markup.",
                ),
                q(
                    "Why is it className instead of class in JSX?",
                    (
                        opt("It is a typo React kept for compatibility"),
                        opt("className applies CSS faster than class"),
                        opt("JSX only accepts camelCase words"),
                        opt(
                            "JSX attributes are JavaScript property names, and class is "
                            "a reserved word in JavaScript",
                            correct=True,
                        ),
                    ),
                    "JSX compiles to JavaScript, where class already means something "
                    "else - so the DOM property name className is used.",
                ),
                q(
                    "A component needs to return two sibling elements without adding an "
                    "extra wrapper div. What do you use?",
                    (
                        opt("A fragment: <>...</>", correct=True),
                        opt("Two separate return statements"),
                        opt("A semicolon between the elements"),
                        opt("It is impossible - JSX requires a div wrapper"),
                    ),
                    "A return has one root element; fragments group siblings without "
                    "rendering any extra DOM node.",
                ),
            ),
        ),
        # ── 3. Components & props ────────────────────────────────────
        _t(
            "Components and props",
            "9 min",
            """# Components and props

A **component** is a JavaScript function whose name starts with a capital
letter and that returns JSX. That is the entire definition. You build an
app by composing components the way you compose HTML tags.

**Props** are the component's inputs: a single object passed as the
function's first argument. The parent decides the values; the child just
reads them.

```jsx
function Badge({ label, color }) {
  return <span style={{ background: color }}>{label}</span>;
}

function App() {
  return (
    <header>
      <Badge label="New" color="green" />
      <Badge label="Sale" color="red" />
    </header>
  );
}
```

The rules that keep components predictable:

- **Props are read-only.** A component never modifies its own props - if
  it needs data that changes, that is state (next lesson).
- **Data flows down.** Parents pass props to children; there is no way
  for a child to reach up and edit the parent. This one-way flow is what
  makes React apps debuggable.
- **`children` is a prop too.** Whatever you nest between a component's
  tags arrives as `props.children`:

```jsx
function Card({ title, children }) {
  return (
    <section className="card">
      <h3>{title}</h3>
      {children}
    </section>
  );
}

// usage: the paragraph becomes Card's children prop
<Card title="About">
  <p>React was released in 2013.</p>
</Card>
```

```mermaid
graph TD
    A["App"] --> H["Header"]
    A --> M["Main"]
    H --> B1["Badge label New"]
    H --> B2["Badge label Sale"]
    M --> C["Card title About"]
    C --> P["Paragraph children"]
```

Think of a component as a function of its props: same props in, same
markup out.
""",
        ),
        quiz_lesson(
            "Quiz: Components and props",
            (
                q(
                    "What makes a JavaScript function a React component?",
                    (
                        opt("It must extend the React.Component class"),
                        opt("It must be registered in a components.json file"),
                        opt(
                            "It starts with a capital letter and returns JSX",
                            correct=True,
                        ),
                        opt("It must live in a file ending in .component.js"),
                    ),
                    "That is the whole contract: a capitalized function returning "
                    "markup. The capital letter is how JSX tells components from "
                    "HTML tags.",
                ),
                q(
                    "A child component wants to change a prop it received. What is the "
                    "correct React answer?",
                    (
                        opt("Assign to it: props.label = 'new value'"),
                        opt(
                            "It cannot - props are read-only; changing data is the "
                            "parent's job via state",
                            correct=True,
                        ),
                        opt("Call props.update() with the new value"),
                        opt("Clone the props object and mutate the clone into the DOM"),
                    ),
                    "One-way data flow: children read props, parents own changes. "
                    "Data that changes over time belongs in state.",
                ),
                q(
                    "What is props.children?",
                    (
                        opt("A list of every component in the app"),
                        opt("The component's internal state"),
                        opt("An array of the component's CSS child selectors"),
                        opt(
                            "Whatever the parent nested between the component's opening "
                            "and closing tags",
                            correct=True,
                        ),
                    ),
                    "Nesting content inside <Card>...</Card> delivers it to Card as "
                    "the children prop - the basis of wrapper components.",
                ),
            ),
        ),
        # ── 4. State ─────────────────────────────────────────────────
        _t(
            "State — making it interactive with useState",
            "10 min",
            """# State — making it interactive with useState

Props come from outside; **state is data a component owns**. When state
changes, React re-renders the component so the screen always matches the
data. The `useState` hook gives a component one piece of state:

```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0); // 0 is the initial value
  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
```

`useState` returns a pair: the **current value** and a **setter**. The
rules:

- **Never assign to state directly.** `count = 5` changes a local
  variable and React never knows. Only the setter (`setCount(5)`)
  triggers a re-render.
- **State updates are replacements, not edits.** For objects and arrays,
  create a new one instead of mutating:

```jsx
const [todos, setTodos] = useState([]);

// right: a new array
setTodos([...todos, { id: 3, text: "Learn state" }]);

// wrong: React cannot see this mutation
todos.push({ id: 3, text: "Learn state" });
```

- **Updates based on the previous value use the function form**, which is
  safe even when several updates happen together:
  `setCount(prev => prev + 1)`.
- **Each component instance has its own state.** Render three `Counter`
  components and you get three independent counts.
- **Hooks are called at the top level** of the component - never inside
  an `if` or a loop - so React can match them between renders.

```mermaid
graph LR
    I["Initial value"] --> V["count value"]
    V --> R["Rendered UI"]
    R --> K["Click event"]
    K --> SET["setCount called"]
    SET --> RR["React re-renders"]
    RR --> V
```

The whole trick of React is here: call the setter, get a fresh render,
and the UI is never out of sync with the data.
""",
        ),
        quiz_lesson(
            "Quiz: State — making it interactive with useState",
            (
                q(
                    "What does useState(0) return?",
                    (
                        opt("The number 0 only"),
                        opt("A pair: the current value and a setter function", correct=True),
                        opt("An object with .get() and .set() methods"),
                        opt("A promise that resolves to the state"),
                    ),
                    "const [count, setCount] = useState(0) - array destructuring of "
                    "the value/setter pair is the idiom.",
                ),
                q(
                    "Why does count = count + 1 fail to update the UI?",
                    (
                        opt("Numbers are immutable in JavaScript"),
                        opt("The variable is a const and throws at compile time"),
                        opt(
                            "React only re-renders when the setter is called - a plain "
                            "assignment is invisible to it",
                            correct=True,
                        ),
                        opt("It works, but only in development mode"),
                    ),
                    "Renders are driven by setter calls. Without setCount, React has "
                    "no idea anything changed.",
                ),
                q(
                    "You have const [items, setItems] = useState([]). What is the "
                    "correct way to add an element?",
                    (
                        opt("items.push(newItem)"),
                        opt("setItems(items.push(newItem))"),
                        opt("setItems([...items, newItem])", correct=True),
                        opt("items = items.concat(newItem)"),
                    ),
                    "State updates are replacements: build a new array with spread "
                    "and pass it to the setter. Mutating the existing array skips "
                    "the re-render.",
                ),
            ),
        ),
        # ── 5. Events & forms ────────────────────────────────────────
        _t(
            "Events and controlled forms",
            "10 min",
            """# Events and controlled forms

React events look like DOM events in camelCase: `onClick`, `onChange`,
`onSubmit`. You pass a **function**, not a string, and React hands it an
event object:

```jsx
function SearchButton() {
  function handleClick(event) {
    console.log("clicked", event.target);
  }
  return <button onClick={handleClick}>Search</button>;
}
```

Two classics to avoid:

- `onClick={handleClick}` passes the function. `onClick={handleClick()}`
  **calls it immediately** during render - a bug every beginner hits once.
- To pass arguments, wrap in an arrow: `onClick={() => remove(item.id)}`.

**Controlled inputs** are the React way to do forms: the input's value
lives in state, and every keystroke updates that state. The input shows
state; typing changes state - one source of truth.

```jsx
import { useState } from "react";

function SignupForm() {
  const [email, setEmail] = useState("");

  function handleSubmit(event) {
    event.preventDefault(); // stop the browser's page reload
    console.log("subscribing", email);
    setEmail("");
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@example.com"
      />
      <button disabled={email === ""}>Subscribe</button>
    </form>
  );
}
```

Notice what one source of truth buys you for free: the button disables
itself while the field is empty, and clearing the form is one setter call.

```mermaid
graph LR
    T["User types"] --> OC["onChange fires"]
    OC --> SS["setEmail updates state"]
    SS --> RE["Re-render"]
    RE --> IV["Input shows state value"]
    IV --> T
```

Remember: in a controlled form, the state is the form - the DOM just
displays it.
""",
        ),
        quiz_lesson(
            "Quiz: Events and controlled forms",
            (
                q(
                    "What is wrong with <button onClick={save()}>?",
                    (
                        opt("onClick must be written onclick in JSX"),
                        opt(
                            "save() runs immediately during render instead of on click - "
                            "pass the function itself or an arrow",
                            correct=True,
                        ),
                        opt("Buttons cannot receive onClick in React"),
                        opt("Nothing - that is the recommended form"),
                    ),
                    "The braces evaluate the expression at render time, so save() "
                    "executes right away. onClick={save} or onClick={() => save()} "
                    "is correct.",
                ),
                q(
                    "What makes an input 'controlled'?",
                    (
                        opt("It has the disabled attribute managed by CSS"),
                        opt("It is inside a <form> element"),
                        opt("It validates itself with the required attribute"),
                        opt(
                            "Its value comes from state and onChange writes every "
                            "keystroke back to that state",
                            correct=True,
                        ),
                    ),
                    "value={email} plus onChange={...setEmail...} makes state the "
                    "single source of truth for what the input shows.",
                ),
                q(
                    "Why call event.preventDefault() in a form's onSubmit handler?",
                    (
                        opt(
                            "To stop the browser's default full-page reload on submit", correct=True
                        ),
                        opt("To prevent React from re-rendering"),
                        opt("To disable the submit button permanently"),
                        opt("To clear all state in the component"),
                    ),
                    "Browsers submit forms with a page navigation by default; a React "
                    "app handles the data itself, so it cancels that.",
                ),
            ),
        ),
        # ── 6. Lists & conditional rendering ─────────────────────────
        _t(
            "Rendering lists and conditions",
            "9 min",
            """# Rendering lists and conditions

Real UIs are mostly lists of things that appear and disappear. In React
both are plain JavaScript - no special template syntax.

**Lists** are `array.map()` returning elements. Each element needs a
**stable `key`** so React can tell items apart between renders:

```jsx
function TodoList({ todos }) {
  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  );
}
```

Why `key={todo.id}` and **not** `key={index}`? If the array is
reordered, filtered or has items inserted, indexes shift - React then
matches the wrong items, and state attached to rows (like a checked
checkbox) sticks to the wrong row. Use the data's own id.

**Conditions** are ordinary expressions:

```jsx
function Inbox({ messages, loading }) {
  if (loading) return <Spinner />;           // early return

  return (
    <div>
      {messages.length === 0 && <p>No messages.</p>}      /* AND: render or skip */
      {messages.length > 0 ? (
        <MessageList items={messages} />
      ) : (
        <EmptyState />
      )}                                                  /* ternary: either/or */
    </div>
  );
}
```

Three tools, one rule each:

- **early `return`** - for whole-component switches like loading states
- **`condition && <El />`** - render or render nothing
- **`condition ? <A /> : <B />`** - render one of two

One caution with `&&`: a count like `items.length && <List />` renders
the number `0` when the list is empty - make the left side a real
boolean (`items.length > 0 && ...`).

```mermaid
graph TD
    D["Data array"] --> M["map with key per item"]
    M --> L["List items"]
    D --> C["Condition checks"]
    C --> Y["Render branch A"]
    C --> N["Render branch B or nothing"]
```

Lists are maps, conditions are expressions, and keys are identities -
that is all of dynamic rendering.
""",
        ),
        quiz_lesson(
            "Quiz: Rendering lists and conditions",
            (
                q(
                    "Why does each element in a rendered list need a key prop?",
                    (
                        opt("Keys are required for CSS styling of list items"),
                        opt(
                            "React uses keys to identify items across renders so "
                            "reorders and inserts update the right rows",
                            correct=True,
                        ),
                        opt("Keys make the list render faster on the first paint only"),
                        opt("The browser requires keys on <li> elements"),
                    ),
                    "Keys are identities. Without stable keys, React matches items by "
                    "position and per-row state can stick to the wrong row.",
                ),
                q(
                    "When is key={index} a problem?",
                    (
                        opt("Always - React throws an error for numeric keys"),
                        opt("Never - index is the recommended key"),
                        opt(
                            "When the list can be reordered, filtered or have items "
                            "inserted, because indexes shift identity",
                            correct=True,
                        ),
                        opt("Only in production builds"),
                    ),
                    "Index keys are acceptable for static lists, but any mutation of "
                    "order breaks the identity mapping - use the data's own id.",
                ),
                q(
                    "What can go wrong with {items.length && <List />}?",
                    (
                        opt("It renders the number 0 when the array is empty", correct=True),
                        opt("It crashes when items is undefined only in dev mode"),
                        opt("&& is not allowed inside JSX braces"),
                        opt("It renders the list twice"),
                    ),
                    "JavaScript's && returns the left value when falsy - and 0 is "
                    "renderable. Write items.length > 0 && ... instead.",
                ),
            ),
        ),
        # ── 7. Effects & data fetching ───────────────────────────────
        _t(
            "useEffect and fetching data",
            "10 min",
            """# useEffect and fetching data

Rendering must be pure: same props and state in, same JSX out. But real
apps also need **side effects** - fetching data, setting timers, talking
to the browser outside the component. `useEffect` is the escape hatch:
it runs your function **after** the render is on screen.

```jsx
import { useEffect, useState } from "react";

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetch(`/api/users/${userId}`)
      .then((res) => res.json())
      .then((data) => {
        if (!cancelled) setUser(data);
      });
    return () => {
      cancelled = true; // cleanup: ignore late responses
    };
  }, [userId]); // re-run only when userId changes

  if (!user) return <p>Loading...</p>;
  return <h2>{user.name}</h2>;
}
```

The second argument - the **dependency array** - decides when the effect
runs:

- `[]` - once, after the first render (mount)
- `[userId]` - after the first render and again whenever `userId` changes
- omitted - after **every** render (almost never what you want)

The **cleanup function** you return runs before the effect re-runs and
when the component unmounts - the place to cancel requests, clear
intervals, and unsubscribe. The `cancelled` flag above prevents a slow
old response from overwriting a newer one.

Common beginner traps:

- Setting state unconditionally inside an effect with no dependency
  array - render, effect, setState, render, effect... an **infinite
  loop**.
- Lying about dependencies. If the effect uses a value, list it.
- Reaching for `useEffect` for derived data. `const total = items.length`
  needs no effect - compute it during render.

```mermaid
graph TD
    R["Render commits to screen"] --> E["Effect runs"]
    E --> F["fetch or subscribe"]
    F --> S["setState with result"]
    S --> R2["Re-render with data"]
    DEP["Dependency change"] --> CL["Cleanup runs"]
    CL --> E
```

Think of useEffect as: after showing this on screen, synchronize me with
the outside world - and here is how to undo it.
""",
        ),
        quiz_lesson(
            "Quiz: useEffect and fetching data",
            (
                q(
                    "When does an effect with dependency array [] run?",
                    (
                        opt("Before every render"),
                        opt("Once, after the component's first render", correct=True),
                        opt("Only when the component unmounts"),
                        opt("Every time any state in the app changes"),
                    ),
                    "An empty array means no dependency can change, so the effect "
                    "runs once after mount - the classic place for an initial fetch.",
                ),
                q(
                    "What is the function returned from an effect for?",
                    (
                        opt("It renders a fallback UI while loading"),
                        opt("It is called immediately to validate the effect"),
                        opt(
                            "Cleanup - it runs before the effect re-runs and on "
                            "unmount, to cancel timers, requests and subscriptions",
                            correct=True,
                        ),
                        opt("It memoizes the effect's result"),
                    ),
                    "Effects that start something must be able to stop it; the "
                    "returned cleanup is where that happens.",
                ),
                q(
                    "An effect with no dependency array calls setCount(count + 1). What happens?",
                    (
                        opt("React batches it into a single update"),
                        opt("Nothing - effects cannot call setters"),
                        opt("The count updates once and stops"),
                        opt(
                            "An infinite loop: every render triggers the effect, which "
                            "triggers another render",
                            correct=True,
                        ),
                    ),
                    "No dependency array means run after every render - and the "
                    "setter causes the next render. Constrain effects with "
                    "dependencies.",
                ),
            ),
        ),
        # ── 8. Composition ───────────────────────────────────────────
        _t(
            "Composition — lifting state up",
            "10 min",
            """# Composition — lifting state up

Sooner or later two components need the **same data**: a search box and
the list it filters, a form and the summary next to it. The React answer
is always the same - **lift the state up** to the closest common parent
and pass it down as props.

A tiny, complete todo app shows the whole pattern:

```jsx
import { useState } from "react";

function TodoInput({ onAdd }) {
  const [text, setText] = useState("");
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (text.trim() === "") return;
        onAdd(text);
        setText("");
      }}
    >
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <button>Add</button>
    </form>
  );
}

function TodoList({ todos, onToggle }) {
  return (
    <ul>
      {todos.map((t) => (
        <li key={t.id} onClick={() => onToggle(t.id)}>
          {t.done ? <s>{t.text}</s> : t.text}
        </li>
      ))}
    </ul>
  );
}

function TodoApp() {
  const [todos, setTodos] = useState([]);

  function addTodo(text) {
    setTodos([...todos, { id: Date.now(), text, done: false }]);
  }
  function toggleTodo(id) {
    setTodos(todos.map((t) => (t.id === id ? { ...t, done: !t.done } : t)));
  }

  return (
    <main>
      <TodoInput onAdd={addTodo} />
      <TodoList todos={todos} onToggle={toggleTodo} />
      <p>{todos.filter((t) => !t.done).length} remaining</p>
    </main>
  );
}
```

Read the shape of it:

- **State lives in one place** - `TodoApp` owns `todos`. The input and
  the list are simple and reusable because they own nothing shared.
- **Data flows down** as props (`todos`), **events flow up** as callback
  props (`onAdd`, `onToggle`). A child never edits shared data - it asks
  the owner to.
- **Derived values are computed, not stored**: the remaining count is a
  `filter().length` during render, not a second piece of state to keep
  in sync.

```mermaid
graph TD
    APP["TodoApp owns todos state"] --> IN["TodoInput"]
    APP --> LI["TodoList"]
    APP --> CT["Remaining count derived"]
    IN -- "onAdd text" --> APP
    LI -- "onToggle id" --> APP
```

This is 90% of structuring a React app: find who needs the data, put the
state one level above them, hand values down and callbacks up.
""",
        ),
        quiz_lesson(
            "Quiz: Composition — lifting state up",
            (
                q(
                    "Two sibling components need to share the same changing data. "
                    "Where does the state go?",
                    (
                        opt("Duplicated in both components, kept in sync manually"),
                        opt("In the closest common parent, passed down as props", correct=True),
                        opt("In a global variable outside React"),
                        opt("In the browser's localStorage"),
                    ),
                    "Lifting state up: one owner, one source of truth, both siblings "
                    "receive it as props.",
                ),
                q(
                    "How does a child like TodoInput change the todos it does not own?",
                    (
                        opt("It mutates the todos prop directly"),
                        opt("It re-renders the parent with new props"),
                        opt(
                            "It calls a callback prop (onAdd) so the owner updates its own state",
                            correct=True,
                        ),
                        opt("It dispatches a DOM event that React intercepts"),
                    ),
                    "Data down, events up: the parent passes a function, the child "
                    "calls it, the owner performs the state update.",
                ),
                q(
                    "Why is the remaining count computed with filter() during render "
                    "instead of stored in its own useState?",
                    (
                        opt(
                            "Derived data is computed from existing state - storing it "
                            "separately creates two sources of truth to keep in sync",
                            correct=True,
                        ),
                        opt("useState cannot hold numbers"),
                        opt("filter() is faster than reading state"),
                        opt("Storing it would require a second component"),
                    ),
                    "If it can be calculated from state you already have, calculate "
                    "it - fewer states, fewer sync bugs.",
                ),
            ),
        ),
        # ── Final quiz ───────────────────────────────────────────────
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is the core promise of React's declarative model?",
                    (
                        opt("The DOM is never updated after the first render"),
                        opt(
                            "You describe the UI for a given state and React keeps the "
                            "real DOM in sync when state changes",
                            correct=True,
                        ),
                        opt("All rendering happens on the server"),
                        opt("CSS is generated automatically from the markup"),
                    ),
                    "Change the data, and the page follows - React reconciles the DOM "
                    "to match what you declared.",
                ),
                q(
                    "Which JSX snippet is valid?",
                    (
                        opt('<img class="pic" src=url>'),
                        opt('<img className="pic" src={url} />', correct=True),
                        opt('<img className="pic" src={url}>'),
                        opt("<image class={pic} src='{url}' />"),
                    ),
                    "className instead of class, braces for expressions, and every "
                    "tag self-closes.",
                ),
                q(
                    "A component receives { title } as a prop and needs it to change "
                    "when the user clicks. What is the React-correct design?",
                    (
                        opt("Reassign: title = newTitle inside the click handler"),
                        opt("Store a copy in a global and edit that"),
                        opt(
                            "The owner of title keeps it in state and passes a callback "
                            "the child calls on click",
                            correct=True,
                        ),
                        opt("Use document.querySelector to update the heading"),
                    ),
                    "Props are read-only; changing data is the state owner's job - "
                    "data down, events up.",
                ),
                q(
                    "setCount(count + 1) is called three times in one click handler. "
                    "What guarantees all three increments apply?",
                    (
                        opt(
                            "Calling the setter with the function form: setCount(p => p + 1)",
                            correct=True,
                        ),
                        opt("Adding await before each call"),
                        opt("Calling setCount(count + 3) is the only possible fix"),
                        opt("Wrapping the handler in useEffect"),
                    ),
                    "The function form receives the latest value, so queued updates "
                    "compose instead of all reading the same stale count.",
                ),
                q(
                    "Why must state arrays be replaced (spread) instead of mutated (push)?",
                    (
                        opt("push is deprecated in modern JavaScript"),
                        opt("Spread is faster than push"),
                        opt(
                            "React detects changes by comparing references - a mutated "
                            "array is the same reference, so no re-render happens",
                            correct=True,
                        ),
                        opt("Mutation is fine; both work identically"),
                    ),
                    "New data means new object/array identity. Same reference reads as no change.",
                ),
                q(
                    "In a controlled input, what is the single source of truth for "
                    "what the field displays?",
                    (
                        opt("The DOM element's internal value"),
                        opt("The component's state, bound via value and onChange", correct=True),
                        opt("The browser's autofill store"),
                        opt("The form's action attribute"),
                    ),
                    "value={state} + onChange={setState} - the state is the form; the "
                    "input just renders it.",
                ),
                q(
                    "Which key choice is safest for a reorderable todo list?",
                    (
                        opt("key={Math.random()}"),
                        opt("key={index}"),
                        opt("key={todo.id}", correct=True),
                        opt("No key - React infers identity"),
                    ),
                    "Stable, data-owned ids preserve item identity across reorders; "
                    "random keys remount every row and index keys shift identity.",
                ),
                q(
                    "You need to load data from an API when the component first "
                    "appears. Where does the fetch go?",
                    (
                        opt("Directly in the component body, before the return"),
                        opt("Inside useEffect with an empty dependency array", correct=True),
                        opt("Inside the onClick of the root element"),
                        opt("In a setTimeout at module load"),
                    ),
                    "Render must stay pure; side effects like fetching run in "
                    "useEffect - [] scopes it to after the first render.",
                ),
                q(
                    "What runs when a component using useEffect unmounts?",
                    (
                        opt("The effect body runs one final time"),
                        opt("Nothing - unmount is not observable"),
                        opt("The component's initial state is restored"),
                        opt("The effect's returned cleanup function", correct=True),
                    ),
                    "Cleanup runs on unmount (and before each re-run) - cancelling "
                    "subscriptions, timers and in-flight requests.",
                ),
                q(
                    "The remaining-items counter in the todo app is derived with "
                    "filter().length instead of stored in useState because…",
                    (
                        opt("numbers cannot be stored in state"),
                        opt(
                            "storing derivable data creates a second source of truth "
                            "that can drift out of sync",
                            correct=True,
                        ),
                        opt("filter() memoizes automatically"),
                        opt("useState is limited to five per component"),
                    ),
                    "Compute what you can, store only what you must - the fewer "
                    "states, the fewer sync bugs.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

REACT_COURSES: tuple[SeedCourse, ...] = (_REACT_BASICS,)
