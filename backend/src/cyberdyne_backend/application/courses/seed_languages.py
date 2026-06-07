"""Curated programming-language courses (basics + intermediate) for six
languages: modern C++, Swift, Go, Rust, JavaScript, TypeScript.

Grounded in the user's Obsidian `Programming` vault. Lessons are `text` with
syntax-highlighted code fences — these languages don't run on the Academy's
Python/MATLAB interpreters, so the code is illustrative rather than runnable.
Each course ends with a knowledge-check quiz (questions authored via the quiz
API, like the other courses).
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="3 min")


# ── C ────────────────────────────────────────────────────────────────────────

_C_BASICS = SeedCourse(
    slug="c-basics",
    title="C — Basics",
    description=(
        "The language behind operating systems, embedded devices and every other "
        "language's runtime: compiling a program, types and operators, and control "
        "flow with functions. Small, close to the machine, everywhere."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Getting started with C",
            "8 min",
            """\
# Getting started with C

C is a small, compiled, statically-typed language that maps closely to how the
machine actually works — which is why Unix, Linux, and most language runtimes
are written in it.

```c
#include <stdio.h>

int main(void) {
    printf("Hello, Cyberdyne!\\n");
    return 0;   // 0 means success
}
```

Compile, then run:

```bash
gcc -Wall -std=c17 hello.c -o hello && ./hello
```

- `#include <stdio.h>` pulls in declarations for `printf`.
- `main` is the entry point and returns an `int`.
- `\\n` is a newline; statements end with `;`.
- `-Wall` turns on warnings — always keep it on.

**Next:** types, variables, and operators.
""",
        ),
        _t(
            "Types, variables & operators",
            "9 min",
            """\
# Types, variables & operators

Every variable has a fixed type and must be declared before use.

```c
int    count = 42;       // whole number
double ratio = 3.14;     // floating point
char   grade = 'A';      // a single character (a small integer)
const int MAX = 100;     // can't be reassigned
```

## printf format specifiers

`printf` needs a specifier per value — mismatches are a classic bug:

```c
printf("%d items, %.2f ratio, grade %c\\n", count, ratio, grade);
//      %d int    %f double      %c char     (%s for strings, %p pointer)
```

## Operators

```c
a + b   a - b   a * b   a / b   a % b      // arithmetic (% is remainder)
==  !=  <  >  <=  >=                        // comparison
&&  ||  !                                   // logical
++a   a--                                   // increment / decrement
```

Watch out: integer division truncates — `7 / 2` is `3`, not `3.5`. Use a
`double` to get `3.5`.

**Next:** control flow and functions.
""",
        ),
        _t(
            "Control flow & functions",
            "9 min",
            """\
# Control flow & functions

```c
if (score >= 90) grade = 'A';
else if (score >= 80) grade = 'B';
else grade = 'C';

for (int i = 0; i < 5; i++) printf("%d ", i);

while (x < 10) x++;
do { read(); } while (more());     // body runs at least once

switch (grade) {
    case 'A': puts("great"); break;   // break stops fall-through
    default:  puts("ok");
}
```

## Functions

Declare the prototype before use (often in a header), then define it:

```c
int add(int a, int b);          // declaration (prototype)

int add(int a, int b) {         // definition
    return a + b;
}
```

C passes arguments **by value** — the function gets a copy, so changes to a
parameter don't affect the caller's variable. (To change the caller's data you
pass a pointer — next course.)

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_C_INTERMEDIATE = SeedCourse(
    slug="c-intermediate",
    title="C — Intermediate",
    description=(
        "The heart of C: pointers, arrays and strings, manual memory management "
        "with malloc/free, and structs plus the preprocessor and multi-file builds."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Pointers",
            "11 min",
            """\
# Pointers

A **pointer** holds the memory address of another variable. They're the
defining feature of C — and the most common source of bugs.

```c
int x = 42;
int *p = &x;     // & = "address of"; p points at x
printf("%d\\n", *p);   // * = "dereference" -> 42
*p = 99;               // writes through the pointer; x is now 99
```

## Why pointers matter: pass-by-reference

C copies arguments, so to let a function modify the caller's variable you pass
its address:

```c
void increment(int *n) { (*n)++; }

int count = 5;
increment(&count);     // count is now 6
```

## NULL and dangling pointers

```c
int *p = NULL;         // points at nothing — check before use
if (p != NULL) *p = 1;
```

Dereferencing `NULL`, or a pointer to freed/out-of-scope memory ("dangling"),
is undefined behaviour — typically a crash. Pointer discipline is C discipline.

**Next:** arrays, strings, and dynamic memory.
""",
        ),
        _t(
            "Arrays, strings & dynamic memory",
            "11 min",
            """\
# Arrays, strings & dynamic memory

An array is a contiguous block; its name decays to a pointer to the first
element.

```c
int nums[3] = {1, 2, 3};
nums[0] = 10;                 // no bounds checking — your job!
```

## Strings are char arrays ending in '\\0'

```c
char name[] = "Ada";          // 4 bytes: 'A' 'd' 'a' '\\0'
printf("%zu\\n", strlen(name)); // 3   (#include <string.h>)
```

The terminating `\\0` is how C knows where a string ends — forget it and
functions read past the end.

## Dynamic memory: malloc / free

For memory whose size or lifetime isn't known at compile time, allocate on the
**heap** and free it yourself:

```c
#include <stdlib.h>
int *arr = malloc(n * sizeof(int));   // allocate
if (arr == NULL) { /* out of memory */ }
// ... use arr ...
free(arr);                            // release — or you leak
arr = NULL;                           // avoid a dangling pointer
```

Every `malloc` needs exactly one `free`. Leaks and double-frees are classic C
bugs — tools like Valgrind and AddressSanitizer catch them.

**Next:** structs and the build process.
""",
        ),
        _t(
            "Structs & the build process",
            "10 min",
            """\
# Structs & the build process

A **struct** groups related fields into one type:

```c
struct Point { int x; int y; };

struct Point p = {1, 2};
p.x = 10;                      // dot access
struct Point *pp = &p;
pp->y = 20;                    // -> when you have a pointer

typedef struct { int x, y; } Point;   // typedef drops the `struct` keyword
Point q = {3, 4};
```

## The preprocessor

Runs before compilation — textual substitution:

```c
#include <stdio.h>     // paste in a header
#define PI 3.14159     // constant macro
#define SQ(a) ((a)*(a)) // function-like macro (parenthesise args!)
```

## Multi-file builds

Split declarations into a **header** (`.h`) and code into a `.c`:

```c
// mathutil.h
int add(int a, int b);

// mathutil.c
#include "mathutil.h"
int add(int a, int b) { return a + b; }
```

```bash
gcc -c mathutil.c        # compile -> mathutil.o
gcc main.o mathutil.o -o app   # link objects into a binary
```

Compile each `.c` to an object file, then **link** them — this separate
compilation is how large C projects build.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── C++ (modern) ───────────────────────────────────────────────────────────

_CPP_BASICS = SeedCourse(
    slug="cpp-basics",
    title="Modern C++ — Basics",
    description=(
        "Start modern C++ (C++17/20): compiling a program, types and references, "
        "control flow, functions and lambdas — the foundation for systems, games, "
        "and high-performance code."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Getting started with modern C++",
            "8 min",
            """\
# Getting started with modern C++

C++ is a compiled, statically-typed language for performance-critical software
— games, browsers, trading systems, embedded. "Modern C++" (C++11 and later)
is far friendlier than its reputation.

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, Cyberdyne!\\n";
    return 0;
}
```

You compile, then run:

```bash
g++ -std=c++20 hello.cpp -o hello && ./hello
```

- `#include` pulls in a header; `std::` is the standard-library namespace.
- `main` returns an `int` (0 = success).
- `auto` lets the compiler infer a type: `auto x = 42;` is an `int`.

**Next:** variables, types, and the reference vs pointer distinction.
""",
        ),
        _t(
            "Types, variables & references",
            "9 min",
            """\
# Types, variables & references

C++ is statically typed — every variable has a fixed type, checked at compile
time.

```cpp
int count = 42;
double ratio = 3.14;
bool ready = true;
std::string name = "Ada";   // #include <string>
const int MAX = 100;        // can't change
auto total = count * 2;     // inferred as int
```

## References vs pointers

A **reference** is an alias for an existing variable; a **pointer** holds an
address and can be reseated or null.

```cpp
int x = 10;
int& ref = x;     // ref IS x
ref = 20;         // x is now 20

int* ptr = &x;    // ptr holds x's address
*ptr = 30;        // dereference to change x
```

Prefer references for "must refer to something"; reach for pointers (or, better,
smart pointers — intermediate course) only when you need nullability or
reseating.

**Next:** making decisions and looping.
""",
        ),
        _t(
            "Control flow, functions & lambdas",
            "9 min",
            """\
# Control flow, functions & lambdas

```cpp
if (score >= 90) grade = 'A';
else if (score >= 80) grade = 'B';
else grade = 'C';

for (int i = 0; i < 5; ++i) std::cout << i;

std::vector<int> v{1, 2, 3};
for (int n : v) std::cout << n;   // range-based for
```

## Functions

```cpp
int add(int a, int b) {
    return a + b;
}
```

## Lambdas (anonymous functions)

Lambdas let you pass behaviour around — essential with the STL algorithms:

```cpp
auto square = [](int x) { return x * x; };
square(5);   // 25

int factor = 10;
auto scale = [factor](int x) { return x * factor; };  // captures factor
```

`[]` is the capture list: `[=]` copies, `[&]` captures by reference.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_CPP_INTERMEDIATE = SeedCourse(
    slug="cpp-intermediate",
    title="Modern C++ — Intermediate",
    description=(
        "The C++ that separates beginners from pros: RAII and ownership, smart "
        "pointers and move semantics, and templates with the STL."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Memory & RAII",
            "9 min",
            """\
# Memory & RAII

C++ gives you manual control of memory — and the discipline to manage it.

- **Stack**: automatic, fast, freed when scope ends. Default choice.
- **Heap**: manual (`new`/`delete`), lives until you free it. Easy to leak.

```cpp
int a = 5;             // stack — gone at end of scope
int* p = new int(5);   // heap — YOU must `delete p;`
```

## RAII — the core C++ idea

**Resource Acquisition Is Initialization**: tie a resource's lifetime to an
object's scope, so the destructor frees it automatically — no manual `delete`,
no leaks even when exceptions fire.

```cpp
{
    std::vector<int> data(1000);   // acquires memory
}   // <- destructor runs here, memory freed automatically
```

Files, locks, sockets, memory — all managed by RAII wrappers. The takeaway:
**don't write raw `new`/`delete`**; let objects own their resources.

**Next:** the smart pointers that make RAII effortless.
""",
        ),
        _t(
            "Smart pointers & move semantics",
            "10 min",
            """\
# Smart pointers & move semantics

Smart pointers are RAII for heap memory — they free it automatically.

```cpp
#include <memory>

auto u = std::make_unique<int>(42);   // sole owner; freed at scope end
auto s = std::make_shared<int>(42);   // shared; freed when last owner drops
```

- **`unique_ptr`** — exclusive ownership, zero overhead. Your default.
- **`shared_ptr`** — reference-counted shared ownership. Use only when needed.

## Move semantics

Copying can be expensive. **Moving** transfers ownership of the guts instead of
duplicating them:

```cpp
std::vector<int> a{1, 2, 3};
std::vector<int> b = std::move(a);   // b steals a's buffer; no copy
// a is now empty
```

`std::move` casts to an rvalue so the move constructor runs. `unique_ptr` is
move-only — you transfer it, never copy it.

**Next:** writing generic code with templates.
""",
        ),
        _t(
            "Templates & the STL",
            "10 min",
            """\
# Templates & the STL

**Templates** let you write code once that works for any type — the compiler
stamps out a version per type used.

```cpp
template <typename T>
T max_of(T a, T b) {
    return (a > b) ? a : b;
}
max_of(3, 7);       // int
max_of(2.5, 1.0);   // double
```

## The Standard Template Library

Battle-tested generic containers and algorithms:

```cpp
#include <vector>
#include <map>
#include <algorithm>

std::vector<int> v{5, 2, 8, 1};
std::sort(v.begin(), v.end());                 // 1 2 5 8
auto it = std::find(v.begin(), v.end(), 8);

std::map<std::string, int> ages{{"Ada", 36}};
ages["Bob"] = 40;
```

Containers (`vector`, `map`, `set`, `unordered_map`) + algorithms (`sort`,
`find`, `transform`, `accumulate`) cover most day-to-day needs — reach for them
before hand-rolling.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Swift ────────────────────────────────────────────────────────────────────

_SWIFT_BASICS = SeedCourse(
    slug="swift-basics",
    title="Swift — Basics",
    description=(
        "Apple's modern language for iOS, macOS and the server: variables and type "
        "inference, the optionals that make Swift safe, and control flow with "
        "closures and collections."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Getting started with Swift",
            "7 min",
            """\
# Getting started with Swift

Swift is a safe, fast, expressive language — primarily for Apple platforms, but
also server-side. Types are inferred, so it reads cleanly.

```swift
let name = "Ada"        // constant (immutable) — prefer this
var age = 36            // variable (mutable)
let pi: Double = 3.14   // explicit type when you want it

print("\\(name) is \\(age)")   // string interpolation -> Ada is 36
```

- `let` vs `var`: reach for `let` by default; use `var` only when it changes.
- Types are inferred (`name` is a `String`) but you can annotate with `: Type`.
- No semicolons needed.

**Next:** optionals — Swift's headline safety feature.
""",
        ),
        _t(
            "Optionals: Swift's nil-safety",
            "9 min",
            """\
# Optionals: Swift's nil-safety

A value that might be missing has an **Optional** type (`T?`). The compiler
forces you to handle the `nil` case, so you can't accidentally use a missing
value.

```swift
var nickname: String? = nil      // might hold a String, might be nil
nickname = "Ada"
```

## Unwrapping safely

```swift
if let name = nickname {
    print("Hi \\(name)")          // runs only if non-nil
}

guard let name = nickname else { return }   // early-exit if nil
print(name)                                  // name is non-optional here

let shown = nickname ?? "Guest"  // ?? supplies a default
```

Optional chaining stops at the first `nil`: `user?.profile?.email`. Avoid
force-unwrap (`name!`) — it crashes if `nil`.

**Next:** control flow, functions, and closures.
""",
        ),
        _t(
            "Control flow, functions & collections",
            "9 min",
            """\
# Control flow, functions & collections

```swift
if score >= 90 { grade = "A" } else { grade = "B" }

for i in 1...5 { print(i) }      // 1,2,3,4,5 (closed range)

switch grade {
case "A": print("great")
default:  print("ok")
}
```

## Functions and closures

```swift
func add(_ a: Int, _ b: Int) -> Int { a + b }

let square = { (x: Int) -> Int in x * x }   // a closure
square(5)   // 25
```

## Collections

```swift
var nums = [1, 2, 3]                 // Array
nums.append(4)
let user = ["name": "Ada"]           // Dictionary
let doubled = nums.map { $0 * 2 }    // [2,4,6,8]  ($0 = first arg)
```

`map`, `filter`, and `reduce` take closures and are everywhere in Swift.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_SWIFT_INTERMEDIATE = SeedCourse(
    slug="swift-intermediate",
    title="Swift — Intermediate",
    description=(
        "Level up Swift: value vs reference types, protocol-oriented programming "
        "with extensions, and modern async/await concurrency."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Structs vs classes",
            "9 min",
            """\
# Structs vs classes

Both bundle data and behaviour, but they differ in a way that shapes Swift
design:

| | `struct` | `class` |
|--|----------|---------|
| Semantics | **value** (copied) | **reference** (shared) |
| Identity | none | `===` identity |
| Inheritance | no | yes |

```swift
struct Point { var x = 0; var y = 0 }
var a = Point(x: 1, y: 2)
var b = a          // a COPY
b.x = 99           // a.x is still 1

class Counter { var n = 0 }
let c1 = Counter()
let c2 = c1        // same instance
c2.n = 5           // c1.n is also 5
```

Swift favours **structs** (predictable, no shared-mutable-state bugs). A method
that mutates a struct's own properties must be marked `mutating`. Reach for a
`class` when you need shared identity or inheritance.

**Next:** protocols.
""",
        ),
        _t(
            "Protocols & extensions",
            "9 min",
            """\
# Protocols & extensions

A **protocol** is a contract of requirements a type can adopt — like an
interface.

```swift
protocol Describable {
    var summary: String { get }
}

struct Dog: Describable {
    var name: String
    var summary: String { "Dog named \\(name)" }
}
```

## Protocol-oriented programming

**Extensions** add behaviour to existing types — even ones you don't own — and
can give protocols default implementations:

```swift
extension Describable {
    func announce() { print(summary) }   // free for every conformer
}

extension Int {
    var squared: Int { self * self }     // 5.squared == 25
}
```

This "compose with protocols + extensions" style is idiomatic Swift —
preferred over deep class hierarchies.

**Next:** concurrency with async/await.
""",
        ),
        _t(
            "Concurrency: async/await",
            "9 min",
            """\
# Concurrency: async/await

Modern Swift expresses asynchronous work with `async`/`await` — code that reads
top-to-bottom but doesn't block the thread.

```swift
func fetchUser() async throws -> User {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// call it from an async context:
Task {
    let user = try await fetchUser()
    print(user.name)
}
```

- `await` suspends until the result is ready, freeing the thread meanwhile.
- `Task { }` starts asynchronous work from sync code.
- Run independent work in parallel with `async let`:

```swift
async let a = fetchA()
async let b = fetchB()
let both = try await (a, b)   // both run concurrently
```

**actors** protect shared mutable state from data races — the next thing to
explore.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Go ───────────────────────────────────────────────────────────────────────

_GO_BASICS = SeedCourse(
    slug="go-basics",
    title="Go — Basics",
    description=(
        "Google's pragmatic language for backends and cloud tooling: a tiny syntax, "
        "static types with inference, multiple returns, and the struct/slice/map "
        "trio."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Getting started with Go",
            "7 min",
            """\
# Getting started with Go

Go is small, compiled, and fast to build — designed for readable backend and
cloud software. There's essentially one way to write things, and `gofmt`
formats it for you.

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, Cyberdyne!")
}
```

```bash
go run main.go      # compile + run
go build            # produce a binary
```

- Every file belongs to a `package`; `main` is the entry point.
- `:=` declares and infers: `name := "Ada"`.
- Unused imports/variables are **compile errors** — Go keeps things tidy.

**Next:** types, variables, and Go's multiple-return functions.
""",
        ),
        _t(
            "Types, variables & functions",
            "9 min",
            """\
# Types, variables & functions

```go
var count int = 42      // explicit
ratio := 3.14           // inferred (float64)
const Max = 100
```

Every type has a **zero value** (`0`, `""`, `false`, `nil`) — variables are
never uninitialised.

## Functions and multiple returns

Go functions can return several values — the idiom for "result + error":

```go
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("divide by zero")
    }
    return a / b, nil
}

q, err := divide(10, 2)
if err != nil {
    // handle it
}
```

You handle errors explicitly with `if err != nil` rather than exceptions —
verbose but very clear.

**Next:** control flow and Go's core data structures.
""",
        ),
        _t(
            "Control flow & data structures",
            "9 min",
            """\
# Control flow & data structures

`for` is Go's only loop (it covers while too):

```go
for i := 0; i < 5; i++ { }      // classic
for x < 10 { x++ }              // "while"
for i, v := range items { }     // iterate

if n := compute(); n > 0 { }    // if with a short statement
switch day { case "sat", "sun": ... }
```

## Structs, slices, maps

```go
type Point struct{ X, Y int }
p := Point{X: 1, Y: 2}

nums := []int{1, 2, 3}          // slice (dynamic array)
nums = append(nums, 4)

ages := map[string]int{"Ada": 36}
ages["Bob"] = 40
v, ok := ages["Ada"]            // ok = whether the key existed
```

Slices and maps are the workhorses; structs group related fields (no classes in
Go).

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_GO_INTERMEDIATE = SeedCourse(
    slug="go-intermediate",
    title="Go — Intermediate",
    description=(
        "What makes Go shine: interfaces, first-class concurrency with goroutines "
        "and channels, and idiomatic error handling with defer/panic/recover."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Interfaces & methods",
            "9 min",
            """\
# Interfaces & methods

You attach **methods** to your own types with a receiver:

```go
type Rect struct{ W, H int }

func (r Rect) Area() int { return r.W * r.H }
```

## Interfaces are satisfied implicitly

An **interface** lists method signatures. A type satisfies it just by having
those methods — no `implements` keyword:

```go
type Shape interface {
    Area() int
}

func describe(s Shape) { fmt.Println(s.Area()) }

describe(Rect{W: 3, H: 4})   // Rect is a Shape automatically
```

This "structural" typing keeps packages decoupled. The empty interface
`any` (alias for `interface{}`) holds any value.

**Next:** Go's signature feature — concurrency.
""",
        ),
        _t(
            "Goroutines & channels",
            "10 min",
            """\
# Goroutines & channels

A **goroutine** is a function running concurrently — extremely cheap (thousands
are fine). Just prefix a call with `go`:

```go
go doWork()   // runs concurrently; main continues
```

## Channels

Goroutines communicate by passing values over **channels** (don't share memory
— share by communicating):

```go
ch := make(chan int)

go func() { ch <- 42 }()   // send
v := <-ch                  // receive (blocks until a value arrives)

// fan-in with select:
select {
case v := <-ch1: use(v)
case v := <-ch2: use(v)
}
```

Use `sync.WaitGroup` to wait for many goroutines, and buffered channels
(`make(chan int, 10)`) when you don't want sends to block.

**Next:** errors, defer, and modules.
""",
        ),
        _t(
            "Errors, defer & modules",
            "9 min",
            """\
# Errors, defer & modules

`error` is just an interface; return it as the last value and wrap for context:

```go
if err != nil {
    return fmt.Errorf("loading config: %w", err)   // %w wraps
}
```

## defer / panic / recover

`defer` schedules cleanup that runs when the function returns — perfect for
closing resources:

```go
f, err := os.Open(name)
if err != nil { return err }
defer f.Close()        // runs no matter how we return
```

`panic` is for truly unrecoverable bugs; `recover` (inside a deferred func) can
catch one. Prefer returned errors for anything expected.

## Modules

```bash
go mod init example.com/app   # start a module
go get github.com/some/dep    # add a dependency
```

`go.mod` pins your dependencies — reproducible builds.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Rust ─────────────────────────────────────────────────────────────────────

_RUST_BASICS = SeedCourse(
    slug="rust-basics",
    title="Rust — Basics",
    description=(
        "Rust gives you C-level performance with memory safety and no garbage "
        "collector: cargo, immutable-by-default variables, expression-based control "
        "flow, and structs/enums with pattern matching."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Getting started with Rust",
            "8 min",
            """\
# Getting started with Rust

Rust is a systems language focused on **safety** and **performance** — no
garbage collector, no data races, errors caught at compile time. `cargo` is its
build tool and package manager.

```bash
cargo new hello && cd hello
cargo run
```

```rust
fn main() {
    let name = "Cyberdyne";       // immutable by default
    let mut count = 0;            // `mut` to allow change
    count += 1;
    println!("Hello, {name}! ({count})");   // println! is a macro
}
```

- Variables are **immutable by default** — add `mut` to change them.
- **Shadowing** lets you reuse a name: `let x = 5; let x = x + 1;`.
- `!` marks a macro (`println!`, `vec!`).

**Next:** types and control flow.
""",
        ),
        _t(
            "Types & control flow",
            "9 min",
            """\
# Types & control flow

```rust
let n: i32 = 42;        // integers: i32, u64, usize, ...
let pi = 3.14_f64;
let ok: bool = true;
let pair: (i32, &str) = (1, "a");   // tuple
let arr = [1, 2, 3];                // fixed array
```

Rust is **expression-based** — `if` and `match` return values:

```rust
let grade = if score >= 90 { "A" } else { "B" };

loop { break; }         // infinite loop
while x < 10 { x += 1; }
for i in 0..5 { }        // 0..5 is a range (5 excluded)
```

## match — exhaustive pattern matching

```rust
match n {
    0 => println!("zero"),
    1..=9 => println!("single digit"),
    _ => println!("big"),       // _ is the catch-all; match must be exhaustive
}
```

**Next:** modelling data with structs and enums.
""",
        ),
        _t(
            "Structs, enums & pattern matching",
            "9 min",
            """\
# Structs, enums & pattern matching

```rust
struct Point { x: i32, y: i32 }
let p = Point { x: 1, y: 2 };

impl Point {                      // methods go in an impl block
    fn dist(&self) -> f64 {
        ((self.x.pow(2) + self.y.pow(2)) as f64).sqrt()
    }
}
```

## Enums carry data

Rust enums are powerful — each variant can hold different data:

```rust
enum Shape {
    Circle(f64),            // radius
    Rect { w: f64, h: f64 },
}

let s = Shape::Circle(2.0);
let area = match s {
    Shape::Circle(r) => 3.14 * r * r,
    Shape::Rect { w, h } => w * h,
};
```

`Option<T>` and `Result<T, E>` (next course) are just enums — which is why
`match` is everywhere in Rust.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_RUST_INTERMEDIATE = SeedCourse(
    slug="rust-intermediate",
    title="Rust — Intermediate",
    description=(
        "The ideas that make Rust unique: ownership and borrowing, error handling "
        "with Result/Option and `?`, and traits with generics."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Ownership & borrowing",
            "11 min",
            """\
# Ownership & borrowing

Rust has no garbage collector and no manual `free` — memory is managed by
**ownership**, checked at compile time. Three rules:

1. each value has a single **owner**;
2. when the owner goes out of scope, the value is dropped (freed);
3. ownership can **move** to a new owner.

```rust
let s1 = String::from("hi");
let s2 = s1;          // ownership MOVES to s2
// println!("{s1}");  // ERROR: s1 no longer valid
```

## Borrowing

Instead of moving, you can **borrow** with references:

```rust
fn len(s: &String) -> usize { s.len() }   // & = shared borrow
let n = len(&s2);                          // s2 still usable

let mut t = String::from("hi");
t.push_str("!");                           // needs &mut to mutate
```

The rule: **many shared (`&`) borrows OR one mutable (`&mut`) borrow** — never
both. This is how Rust prevents data races at compile time.

**Next:** handling errors without exceptions.
""",
        ),
        _t(
            "Error handling: Result, Option & ?",
            "9 min",
            """\
# Error handling: Result, Option & ?

Rust has no exceptions. Fallible operations return an enum you must handle.

```rust
enum Option<T> { Some(T), None }          // a value that may be absent
enum Result<T, E> { Ok(T), Err(E) }       // success or failure
```

```rust
fn find(v: &[i32], x: i32) -> Option<usize> {
    v.iter().position(|&n| n == x)
}

match find(&nums, 7) {
    Some(i) => println!("at {i}"),
    None => println!("missing"),
}
```

## The `?` operator

`?` propagates an error early — return it if `Err`, otherwise unwrap the `Ok`:

```rust
fn read_count(path: &str) -> Result<i32, std::io::Error> {
    let text = std::fs::read_to_string(path)?;   // returns Err on failure
    Ok(text.trim().parse().unwrap_or(0))
}
```

This keeps the happy path clean while forcing every error to be handled.

**Next:** generics and traits.
""",
        ),
        _t(
            "Traits & generics",
            "9 min",
            """\
# Traits & generics

**Generics** write code over any type; **traits** are shared behaviour (like
interfaces) you can require.

```rust
trait Area {
    fn area(&self) -> f64;
}

struct Circle { r: f64 }
impl Area for Circle {
    fn area(&self) -> f64 { 3.14 * self.r * self.r }
}
```

## Generic functions with trait bounds

```rust
fn print_area<T: Area>(shape: &T) {     // T must implement Area
    println!("{}", shape.area());
}
```

Common derivable traits save boilerplate:

```rust
#[derive(Debug, Clone, PartialEq)]
struct Point { x: i32, y: i32 }
```

Traits + generics give Rust zero-cost abstraction: generic code compiles down
to the same machine code you'd write by hand.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── JavaScript ───────────────────────────────────────────────────────────────

_JS_BASICS = SeedCourse(
    slug="javascript-basics",
    title="JavaScript — Basics",
    description=(
        "The language of the web: variables and types, functions and scope, control "
        "flow, and interacting with the page (DOM + events)."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Getting started with JavaScript",
            "7 min",
            """\
# Getting started with JavaScript

JavaScript runs in every browser and (via Node.js) on servers. It's
dynamically typed — variables don't declare a type.

```javascript
const name = "Ada";     // can't be reassigned — prefer this
let age = 36;           // reassignable
// avoid `var` (old, function-scoped)

console.log(`${name} is ${age}`);   // template literal -> Ada is 36
```

## Types

```javascript
typeof "hi";     // "string"
typeof 42;       // "number"  (one number type for ints + floats)
typeof true;     // "boolean"
typeof undefined;// "undefined"
let nothing = null;
```

Beware loose equality: use `===` (strict), not `==` (coerces types).

**Next:** functions and scope.
""",
        ),
        _t(
            "Functions, scope, arrays & objects",
            "9 min",
            """\
# Functions, scope, arrays & objects

```javascript
function add(a, b) { return a + b; }
const square = (x) => x * x;          // arrow function

// `let`/`const` are block-scoped:
if (true) { let x = 1; }
// x is not visible here
```

## Arrays (like Python lists)

```javascript
const nums = [1, 2, 3];
nums.push(4);
const doubled = nums.map((n) => n * 2);     // [2,4,6,8]
const evens = nums.filter((n) => n % 2 === 0);
```

## Objects (like Python dicts)

```javascript
const user = { name: "Ada", role: "admin" };
user.role;            // "admin"
user.active = true;   // add a key
const { name } = user; // destructuring -> name = "Ada"
```

**Next:** control flow and the DOM.
""",
        ),
        _t(
            "Control flow & the DOM",
            "8 min",
            """\
# Control flow & the DOM

```javascript
if (score >= 90) grade = "A";
else grade = "B";

for (const n of nums) console.log(n);   // for...of iterates values
while (x < 10) x++;
```

## Talking to the page

In the browser, the **DOM** is the live tree of elements. JavaScript reads and
changes it:

```javascript
const btn = document.querySelector("#go");
btn.textContent = "Click me";

btn.addEventListener("click", () => {
    alert("clicked!");
});
```

- `querySelector` finds an element by CSS selector.
- `addEventListener` runs a callback on events (`click`, `input`, `submit`…).

This event-driven model is the heart of interactive web pages.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_JS_INTERMEDIATE = SeedCourse(
    slug="javascript-intermediate",
    title="JavaScript — Intermediate",
    description=(
        "The concepts that trip people up: asynchronous JavaScript (promises and "
        "async/await), closures and `this`, and modules with functional patterns."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Asynchronous JavaScript",
            "10 min",
            """\
# Asynchronous JavaScript

JavaScript is single-threaded, so slow work (network, timers) runs
**asynchronously** — you get the result later via a **Promise**.

```javascript
// Old style: callbacks (can nest into "callback hell")
setTimeout(() => console.log("later"), 1000);

// Promises:
fetch("/api/user")
    .then((res) => res.json())
    .then((user) => console.log(user))
    .catch((err) => console.error(err));
```

## async / await

Syntactic sugar that makes async code read like sync code:

```javascript
async function loadUser() {
    try {
        const res = await fetch("/api/user");
        const user = await res.json();
        return user;
    } catch (err) {
        console.error(err);
    }
}
```

`await` pauses until the Promise resolves; run things in parallel with
`Promise.all([a, b])`.

**Next:** closures and `this`.
""",
        ),
        _t(
            "Closures, this & prototypes",
            "9 min",
            """\
# Closures, this & prototypes

A **closure** is a function that remembers the variables from where it was
created — the basis of private state and callbacks:

```javascript
function counter() {
    let n = 0;
    return () => ++n;        // closes over n
}
const next = counter();
next(); next();   // 1, 2
```

## `this`

`this` depends on **how a function is called**. Arrow functions don't have
their own `this` — they inherit it, which is usually what you want in
callbacks:

```javascript
const obj = {
    items: [1, 2],
    show() { this.items.forEach((i) => console.log(this.items)); } // arrow keeps `this`
};
```

## Prototypes

Objects inherit from other objects via the **prototype chain**; `class` is
modern sugar over it:

```javascript
class Animal {
    constructor(name) { this.name = name; }
    speak() { return `${this.name} makes a sound`; }
}
```

**Next:** modules and functional patterns.
""",
        ),
        _t(
            "Modules & functional patterns",
            "8 min",
            """\
# Modules & functional patterns

Split code across files with ES **modules**:

```javascript
// math.js
export function add(a, b) { return a + b; }
export const PI = 3.14159;

// app.js
import { add, PI } from "./math.js";
```

## Functional patterns

Transform data without mutating it:

```javascript
const nums = [1, 2, 3, 4];
const total = nums.reduce((sum, n) => sum + n, 0);   // 10
const doubled = nums.map((n) => n * 2);
const evens = nums.filter((n) => n % 2 === 0);
```

## Spread & destructuring

```javascript
const merged = { ...defaults, ...overrides };   // spread
const [first, ...rest] = nums;                   // rest
const { name, age = 0 } = user;                  // defaults
```

These immutable, declarative patterns dominate modern JS (and React).

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── TypeScript ───────────────────────────────────────────────────────────────

_TS_BASICS = SeedCourse(
    slug="typescript-basics",
    title="TypeScript — Basics",
    description=(
        "JavaScript with a type system that catches bugs before you run: why TS, "
        "the basic types, interfaces for objects, and typed functions with unions."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why TypeScript",
            "7 min",
            """\
# Why TypeScript

TypeScript is JavaScript plus **static types**. The compiler (`tsc`) catches
type mistakes before your code runs, then erases the types to produce plain JS.

```typescript
let name: string = "Ada";
let age: number = 36;
let ready: boolean = true;

function greet(person: string): string {
    return `Hi ${person}`;
}

greet(42);   // compile error: number is not a string
```

- Annotate with `: type`; often TS **infers** it, so you write less.
- All valid JavaScript is valid TypeScript — you adopt it gradually.

```bash
tsc app.ts        # type-check and compile to app.js
```

**Next:** the basic types and interfaces.
""",
        ),
        _t(
            "Basic types & interfaces",
            "9 min",
            """\
# Basic types & interfaces

```typescript
let id: number = 1;
let tags: string[] = ["a", "b"];      // array
let pair: [string, number] = ["x", 1]; // tuple
let data: any;                         // opt out of checking (avoid)
let value: unknown;                    // safe "any" — must narrow first
```

## Interfaces describe object shapes

```typescript
interface User {
    name: string;
    age: number;
    email?: string;        // optional
    readonly id: number;   // can't be reassigned
}

const u: User = { name: "Ada", age: 36, id: 1 };
```

If an object has the required properties, it fits the interface (structural
typing). `type` aliases do much the same: `type ID = string | number;`.

**Next:** typed functions and union types.
""",
        ),
        _t(
            "Functions & union types",
            "8 min",
            """\
# Functions & union types

```typescript
function add(a: number, b: number): number {
    return a + b;
}

const greet = (name: string, greeting = "Hi"): string =>
    `${greeting}, ${name}`;
```

## Union & literal types

A **union** allows several types; **literal types** restrict to exact values:

```typescript
let id: string | number;     // either
id = "abc"; id = 123;

type Direction = "up" | "down";   // only these two strings
function move(dir: Direction) { } // move("left") is an error
```

Functions can return unions too — and TypeScript forces callers to handle each
case (next course: narrowing). Optional and default parameters keep call sites
clean.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_TS_INTERMEDIATE = SeedCourse(
    slug="typescript-intermediate",
    title="TypeScript — Intermediate",
    description=(
        "Make the type system work for you: generics, narrowing and type guards, "
        "and the built-in utility types — plus classes and enums."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Generics",
            "9 min",
            """\
# Generics

Generics write reusable code that keeps its types instead of falling back to
`any`:

```typescript
function first<T>(arr: T[]): T | undefined {
    return arr[0];
}

first([1, 2, 3]);       // T = number  -> number | undefined
first(["a", "b"]);      // T = string  -> string | undefined
```

## Generic interfaces & constraints

```typescript
interface Box<T> { value: T; }
const b: Box<number> = { value: 42 };

function longest<T extends { length: number }>(a: T, b: T): T {
    return a.length >= b.length ? a : b;   // T must have .length
}
```

`extends` constrains what `T` can be, so you can safely use its members.
Generics are how typed collections, promises (`Promise<T>`), and APIs stay
type-safe.

**Next:** narrowing.
""",
        ),
        _t(
            "Narrowing & type guards",
            "9 min",
            """\
# Narrowing & type guards

When a value is a union, TypeScript **narrows** it to a specific type as you
check it — so member access is safe.

```typescript
function format(x: string | number): string {
    if (typeof x === "number") {
        return x.toFixed(2);   // here x is a number
    }
    return x.toUpperCase();    // here x is a string
}
```

Guards: `typeof` (primitives), `instanceof` (classes), `in` (property exists),
and truthiness checks.

## Discriminated unions

A shared literal tag lets TS narrow object unions exhaustively:

```typescript
type Shape =
    | { kind: "circle"; r: number }
    | { kind: "rect"; w: number; h: number };

function area(s: Shape): number {
    switch (s.kind) {
        case "circle": return Math.PI * s.r ** 2;
        case "rect":   return s.w * s.h;
    }
}
```

**Next:** utility types and classes.
""",
        ),
        _t(
            "Utility types & classes",
            "8 min",
            """\
# Utility types & classes

TypeScript ships **utility types** that transform existing types — no need to
re-declare:

```typescript
interface User { id: number; name: string; email: string; }

type Draft = Partial<User>;          // all properties optional
type Public = Omit<User, "email">;   // drop email
type NameOnly = Pick<User, "name">;  // keep only name
type ById = Record<number, User>;    // { [id: number]: User }
```

## Classes & enums

```typescript
class Account {
    private balance = 0;             // access modifier
    constructor(readonly owner: string) {}
    deposit(n: number) { this.balance += n; }
}

enum Status { Active, Disabled }     // named constants
let s: Status = Status.Active;
```

`private`/`protected`/`public` and `readonly` are checked at compile time.
Together, utility types + generics let you describe almost any shape precisely.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


LANGUAGE_COURSES: tuple[SeedCourse, ...] = (
    _C_BASICS,
    _C_INTERMEDIATE,
    _CPP_BASICS,
    _CPP_INTERMEDIATE,
    _SWIFT_BASICS,
    _SWIFT_INTERMEDIATE,
    _GO_BASICS,
    _GO_INTERMEDIATE,
    _RUST_BASICS,
    _RUST_INTERMEDIATE,
    _JS_BASICS,
    _JS_INTERMEDIATE,
    _TS_BASICS,
    _TS_INTERMEDIATE,
)

__all__ = ["LANGUAGE_COURSES"]
