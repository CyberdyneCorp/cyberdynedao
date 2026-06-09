"""Curated C# courses: a three-level track from the language fundamentals up
to building, persisting and testing real ASP.NET Core services.

Grounded in the user's Obsidian ``Programming/CSharp`` vault (the C# language
note and the ASP.NET Core note). Lessons are ``text`` with syntax-highlighted
code fences (csharp / bash / json) — there's no .NET runtime in the Academy, so
code is illustrative. Each course ends with a knowledge-check quiz.

Examples use modern C# (top-level statements, records, pattern matching,
collection expressions, minimal APIs) targeting .NET 8.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="3 min")


# ── C# — Basics ──────────────────────────────────────────────────────────────

_CSHARP_BASICS = SeedCourse(
    slug="csharp-basics",
    title="C# — Basics",
    description=(
        "Start writing C#: what C# and .NET are, variables and types, control "
        "flow and pattern matching, the everyday collections, methods, classes "
        "and objects, and handling errors — the language fundamentals every "
        ".NET developer builds on."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is C# and .NET?",
            "8 min",
            """\
# What is C# and .NET?

**C#** is a modern, statically-typed, object-oriented language from Microsoft.
**.NET** is the platform it runs on: your code compiles to an intermediate
language (IL) that the **Common Language Runtime (CLR)** just-in-time compiles
and runs — with a garbage collector managing memory for you.

```mermaid
flowchart LR
  S[Program.cs] --> C[C# compiler] --> IL[IL + metadata in a .dll]
  IL --> JIT[CLR / JIT] --> N[native code runs]
```

It's cross-platform (Windows, Linux, macOS) and powers console tools, web APIs
(ASP.NET Core), desktop, mobile (MAUI), games (Unity) and cloud services.

## The dotnet CLI

Everything starts from the `dotnet` command:

```bash
dotnet --version            # check the installed SDK
dotnet new console -n MyApp # scaffold a console app
cd MyApp
dotnet run                  # build and run
dotnet build                # compile only
dotnet publish -c Release   # produce a deployable build
```

## Hello, World — then and now

Older C# wrapped everything in a namespace and a `Main` method:

```csharp
using System;
namespace HelloWorld
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello, World!");
        }
    }
}
```

Modern C# (9+) lets a file *be* the program with **top-level statements** — the
compiler generates the boilerplate:

```csharp
Console.WriteLine("Hello, World!");
```

That single line is a complete program. The rest of this course builds on it.

**Next:** the values you store — variables and types.
""",
        ),
        _t(
            "Variables & types",
            "11 min",
            """\
# Variables & types

C# is **statically typed**: every variable has a type known at compile time.
You can write the type, or let the compiler infer it with `var`.

```csharp
int age = 30;
double precise = 3.14159;
decimal money = 100.50m;     // m suffix — exact, for currency
bool isActive = true;
char letter = 'A';
string name = "Alice";

var number = 42;             // inferred as int
var text = "Hello";          // inferred as string
```

## The core numeric types

| C# type | .NET type | Size | Notes |
|---------|-----------|------|-------|
| `int` | Int32 | 4 bytes | the default integer |
| `long` | Int64 | 8 bytes | big integers |
| `float` | Single | 4 bytes | ~7 digits |
| `double` | Double | 8 bytes | ~15 digits, default real |
| `decimal` | Decimal | 16 bytes | ~28 digits — money, no rounding error |
| `bool` | Boolean | 1 byte | `true` / `false` |
| `char` | Char | 2 bytes | one Unicode character |

## Value vs. reference types

`int`, `double`, `bool`, `struct` are **value types** — the variable holds the
data. `string`, arrays, and `class` instances are **reference types** — the
variable holds a reference to data on the heap. Assigning a value type copies
it; assigning a reference copies the pointer.

## Null safety

With **nullable reference types** (C# 8+) the compiler tracks what may be null.
A `?` marks a type as nullable:

```csharp
int? maybe = null;                 // nullable value type
string? nickname = null;           // nullable reference

int value = maybe ?? 0;            // ?? supplies a default when null
int? len = nickname?.Length;       // ?. short-circuits to null
```

## Constants and string interpolation

```csharp
const double Pi = 3.14159;         // compile-time constant
string who = "Ada";
Console.WriteLine($"Hello, {who}! Pi is about {Pi:F2}");  // $ = interpolation
```

**Next:** making decisions and repeating work.
""",
        ),
        _t(
            "Control flow & pattern matching",
            "11 min",
            """\
# Control flow & pattern matching

## if / else and the ternary

```csharp
if (age >= 18)
    Console.WriteLine("Adult");
else if (age >= 13)
    Console.WriteLine("Teenager");
else
    Console.WriteLine("Child");

string status = age >= 18 ? "Adult" : "Minor";   // ternary
```

## switch — statement and expression

The classic `switch` statement still works, but modern C# prefers the **switch
expression**, which *returns* a value and is exhaustive (`_` is the default):

```csharp
string dayName = dayOfWeek switch
{
    1 => "Monday",
    2 => "Tuesday",
    6 or 7 => "Weekend",
    _ => "Invalid",
};
```

## Pattern matching

`is` tests a value and can bind it to a new variable in one step. Switch
expressions can match on type, with `when` guards for extra conditions:

```csharp
if (obj is string s)
    Console.WriteLine($"a string of length {s.Length}");

string Describe(object o) => o switch
{
    int n when n > 0 => "positive integer",
    int        => "non-positive integer",
    string str   => $"string: {str}",
    null         => "null",
    _            => "something else",
};
```

## Loops

```csharp
for (int i = 0; i < 5; i++)        // count-controlled
    Console.WriteLine(i);

foreach (var name in names)        // over a collection
    Console.WriteLine(name);

int count = 0;
while (count < 5) count++;         // condition first

do { count--; } while (count > 0); // body runs at least once
```

`break` leaves a loop immediately; `continue` skips to the next iteration:

```csharp
for (int i = 0; i < 10; i++)
{
    if (i == 3) continue;          // skip 3
    if (i == 7) break;             // stop at 7
    Console.WriteLine(i);
}
```

**Next:** storing many values — collections.
""",
        ),
        _t(
            "Collections: arrays, lists & dictionaries",
            "11 min",
            """\
# Collections: arrays, lists & dictionaries

## Arrays — fixed size

```csharp
int[] numbers = new int[5];           // five zeros
int[] primes  = { 2, 3, 5, 7, 11 };   // initialised
int[] more    = [13, 17, 19];         // collection expression (C# 12)

numbers[0] = 10;
int first  = primes[0];
int length = primes.Length;

Array.Sort(numbers);
bool any = Array.Exists(primes, x => x > 10);
```

## `List<T>` — the everyday resizable list

```csharp
using System.Collections.Generic;

List<string> names = new() { "Alice", "Bob" };   // target-typed new (C# 9)
names.Add("Charlie");
names.AddRange(["Dana", "Eve"]);
names.Insert(0, "First");
names.Remove("Bob");
names.RemoveAll(n => n.StartsWith("A"));

bool has = names.Contains("Charlie");
string? found = names.Find(n => n.Length > 5);
int n = names.Count;
```

## `Dictionary<TKey, TValue>` — look-ups by key

```csharp
Dictionary<string, int> ages = new()
{
    ["Alice"] = 30,
    ["Bob"]   = 25,
};

ages.Add("Charlie", 35);
ages["Alice"] = 31;                    // update

if (ages.TryGetValue("Dana", out int danaAge))   // safe lookup, no throw
    Console.WriteLine(danaAge);

foreach (var (name, age) in ages)      // deconstruction
    Console.WriteLine($"{name}: {age}");
```

## Picking a collection

| Need | Use |
|------|-----|
| fixed-size, fast index | `int[]` |
| ordered, resizable | `List<T>` |
| key → value lookup | `Dictionary<K,V>` |
| unique items / set math | `HashSet<T>` |
| FIFO / LIFO | `Queue<T>` / `Stack<T>` |

**Next:** packaging logic into methods.
""",
        ),
        _t(
            "Methods",
            "10 min",
            """\
# Methods

A **method** is a named, reusable block. It has a return type (`void` if it
returns nothing), a name, and a parameter list.

```csharp
public int Add(int a, int b)
{
    return a + b;
}

public int Multiply(int a, int b) => a * b;   // expression-bodied (C# 6+)

public void Greet(string name) => Console.WriteLine($"Hi, {name}");
```

## Optional and named arguments

```csharp
public void Greet(string name, string greeting = "Hello")   // default value
    => Console.WriteLine($"{greeting}, {name}!");

Greet("Ada");                       // Hello, Ada!
Greet("Ada", "Welcome");            // Welcome, Ada!
Greet(greeting: "Hi", name: "Bob"); // named — order-independent
```

## `params` — a variable number of arguments

```csharp
public int Sum(params int[] values)
{
    int total = 0;
    foreach (var v in values) total += v;
    return total;
}

int t = Sum(1, 2, 3, 4, 5);         // 15
```

## ref and out

By default arguments pass **by value** (a copy). `ref` lets a method modify the
caller's variable; `out` returns extra values — the classic `Try...` pattern:

```csharp
void Double(ref int x) => x *= 2;
int num = 5;
Double(ref num);                    // num is now 10

if (int.TryParse("42", out int parsed))
    Console.WriteLine(parsed);      // 42
```

## Local functions

A method can declare a helper **inside** it — handy for recursion or to keep a
helper private to one method:

```csharp
public int Factorial(int n)
{
    int Fac(int x) => x <= 1 ? 1 : x * Fac(x - 1);
    return Fac(n);
}
```

**Next:** the heart of C# — classes and objects.
""",
        ),
        _t(
            "Classes & objects",
            "12 min",
            """\
# Classes & objects

A **class** is a blueprint for objects. It bundles **data** (fields and
properties) with **behaviour** (methods).

```csharp
public class Person
{
    // Auto-implemented property — get/set with a hidden backing field.
    public string Name { get; set; }

    // Property with logic in the setter.
    private int _age;
    public int Age
    {
        get => _age;
        set => _age = value >= 0 ? value : throw new ArgumentException("age < 0");
    }

    // Init-only — settable only during construction (C# 9+).
    public string Id { get; init; }

    // Computed (read-only) property.
    public string Label => $"{Name} ({Age})";

    // Constructor.
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }

    public void Greet() => Console.WriteLine($"Hi, I'm {Name}");
}

var p = new Person("Alice", 30) { Id = "P001" };   // object initialiser
p.Greet();
Console.WriteLine(p.Label);                         // Alice (30)
```

## Inheritance

A class can **inherit** from a base class, reusing and extending it. Mark a
method `virtual` to allow a subclass to `override` it — this is **polymorphism**:

```csharp
public class Animal
{
    public string Name { get; set; }
    public Animal(string name) => Name = name;
    public virtual void Speak() => Console.WriteLine("...");
}

public class Dog : Animal
{
    public Dog(string name) : base(name) { }       // call the base constructor
    public override void Speak() => Console.WriteLine("Woof!");
}

Animal a = new Dog("Rex");
a.Speak();                                          // Woof!  (runtime type wins)
```

## Abstract classes

An **abstract** class can't be instantiated and may leave members for
subclasses to implement:

```csharp
public abstract class Shape
{
    public abstract double Area { get; }            // no body — subclass must supply
}

public class Circle : Shape
{
    public double Radius { get; set; }
    public override double Area => Math.PI * Radius * Radius;
}
```

The four OOP pillars in one screen: **encapsulation** (properties guard fields),
**inheritance** (`Dog : Animal`), **polymorphism** (`override`), and
**abstraction** (`abstract`). Interfaces — the next level up — come in the
Intermediate course.

**Next:** dealing with things that go wrong.
""",
        ),
        _t(
            "Exception handling",
            "9 min",
            """\
# Exception handling

When something fails, C# **throws an exception** — an object describing the
error that unwinds the call stack until something **catches** it.

```csharp
try
{
    int x = int.Parse("not a number");   // throws FormatException
}
catch (FormatException ex)
{
    Console.WriteLine($"bad input: {ex.Message}");
}
catch (Exception ex)                     // catch-all — put it last
{
    Console.WriteLine($"unexpected: {ex.Message}");
    throw;                               // re-throw, preserving the stack trace
}
finally
{
    Console.WriteLine("always runs — cleanup goes here");
}
```

Catch the **most specific** exception types first; a bare `catch (Exception)`
last. `throw;` (no argument) rethrows while keeping the original stack trace —
`throw ex;` would reset it.

## Throwing your own

```csharp
public void SetAge(int age)
{
    if (age < 0)
        throw new ArgumentOutOfRangeException(nameof(age), "age cannot be negative");
}
```

Modern guard helpers make common checks one-liners:

```csharp
ArgumentNullException.ThrowIfNull(input);
ArgumentException.ThrowIfNullOrEmpty(name);
```

## `using` — deterministic cleanup

Types holding unmanaged resources (files, sockets, DB connections) implement
`IDisposable`. A `using` declaration disposes them automatically when the scope
ends — even if an exception is thrown:

```csharp
using StreamReader reader = new("data.txt");
string text = reader.ReadToEnd();
// reader.Dispose() runs here, guaranteed
```

> Use exceptions for the *exceptional* — not for ordinary control flow. For
> "might fail" parsing, prefer the `TryParse` pattern you saw with methods.

**Next:** check your knowledge.
""",
        ),
        _quiz(),
    ),
)


# ── C# — Intermediate ────────────────────────────────────────────────────────

_CSHARP_INTERMEDIATE = SeedCourse(
    slug="csharp-intermediate",
    title="C# — Intermediate",
    description=(
        "Level up your C#: interfaces and abstraction, records and value "
        "equality, generics, LINQ, delegates and events, asynchronous code with "
        "async/await, and working with JSON and files — the toolkit for writing "
        "real applications."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Interfaces & abstraction",
            "10 min",
            """\
# Interfaces & abstraction

An **interface** is a contract: a list of members a type promises to provide,
with no implementation. It's how C# does polymorphism without inheritance — a
class can implement *many* interfaces.

```csharp
public interface IMovable
{
    int Speed { get; set; }
    void Move(int x, int y);

    void Stop() => Console.WriteLine("stopped");   // default impl (C# 8+)
}

public interface IDrawable
{
    void Draw();
}

public class Car : IMovable, IDrawable             // implement several
{
    public int Speed { get; set; }
    public void Move(int x, int y) => Console.WriteLine($"-> ({x},{y}) @ {Speed}");
    public void Draw() => Console.WriteLine("drawing car");
}
```

## Program to the interface

Depend on the interface, not the concrete type — code stays decoupled and
testable:

```csharp
void Relocate(IMovable thing) => thing.Move(10, 20);

Relocate(new Car { Speed = 60 });        // works for ANY IMovable
```

## Interface vs. abstract class

| | Interface | Abstract class |
|--|-----------|----------------|
| Multiple inheritance | yes — implement many | no — one base only |
| State (fields) | no | yes |
| Constructors | no | yes |
| Use when | "can do X" capability | shared base + partial implementation |

A common idiom: an interface (`IRepository`) for the contract, an abstract or
concrete class for shared plumbing. **Next:** records — concise data types.
""",
        ),
        _t(
            "Records & value equality",
            "9 min",
            """\
# Records & value equality

A **record** (C# 9+) is a reference type built for **immutable data**. One line
gives you a constructor, properties, value-based equality, a readable
`ToString`, and deconstruction:

```csharp
public record Person(string Name, int Age);     // positional record

var a = new Person("Alice", 30);
var b = new Person("Alice", 30);

Console.WriteLine(a == b);          // True — compares VALUES, not references
Console.WriteLine(a);               // Person { Name = Alice, Age = 30 }
```

Compare that to a `class`, where `a == b` would be `False` (different objects).

## Non-destructive mutation: `with`

Records are immutable by default; `with` makes a **copy** with some properties
changed:

```csharp
var older = a with { Age = 31 };    // a is unchanged; older is a new record
```

## Deconstruction and extra members

```csharp
var (name, age) = a;                // pulls the positional values out

public record Employee(string Name, string Dept)
{
    public string Title => $"{Name} — {Dept}";   // add computed members too
}
```

A `record struct` (C# 10) gives the same value semantics as a *value* type:

```csharp
public readonly record struct Point(int X, int Y);
```

> Reach for a **record** for DTOs, API models, events and any "bag of values"
> where equality should mean "same contents". Use a **class** when identity and
> mutable state matter.

**Next:** writing one piece of code that works for many types — generics.
""",
        ),
        _t(
            "Generics",
            "10 min",
            """\
# Generics

**Generics** let you write a type or method parameterised by *another* type —
type-safe and without boxing. `List<T>` and `Dictionary<K,V>` are generic; you
can write your own.

```csharp
public class Repository<T>
{
    private readonly List<T> _items = new();
    public void Add(T item) => _items.Add(item);
    public T? Get(int i) => i < _items.Count ? _items[i] : default;
    public IEnumerable<T> All() => _items;
}

var people = new Repository<Person>();
people.Add(new Person("Ada", 36));   // T is Person — fully type-checked
```

## Generic methods

```csharp
public T Max<T>(T a, T b) where T : IComparable<T>
    => a.CompareTo(b) > 0 ? a : b;

int big = Max(3, 7);                  // T inferred as int
```

## Constraints — `where`

Constraints tell the compiler what `T` is allowed to be, unlocking operations
on it:

```csharp
public class Factory<T>
    where T : class, new()            // reference type with a parameterless ctor
{
    public T Create() => new T();
}
```

| Constraint | Means |
|------------|-------|
| `where T : class` | T is a reference type |
| `where T : struct` | T is a value type |
| `where T : new()` | T has a public parameterless constructor |
| `where T : IComparable<T>` | T implements that interface |
| `where T : notnull` | T is non-nullable |

## Variance (a peek)

`out` makes a generic interface **covariant** (producer), `in` makes it
**contravariant** (consumer) — which is why an `IEnumerable<Dog>` is usable as
`IEnumerable<Animal>`:

```csharp
public interface IProducer<out T> { T Produce(); }
public interface IConsumer<in T> { void Consume(T item); }
```

**Next:** querying data fluently — LINQ.
""",
        ),
        _t(
            "LINQ",
            "12 min",
            """\
# LINQ

**Language Integrated Query** brings SQL-like querying to any
`IEnumerable<T>` — in-memory collections, databases (via EF Core), XML, more.
Two equivalent syntaxes:

```csharp
using System.Linq;
List<int> nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Query syntax
var evensQ = from n in nums
             where n % 2 == 0
             orderby n descending
             select n;

// Method syntax (more common) — a chain of extension methods + lambdas
var evensM = nums.Where(n => n % 2 == 0)
                 .OrderByDescending(n => n)
                 .ToList();
```

## The operators you'll use constantly

```csharp
nums.Where(n => n > 5);          // filter
nums.Select(n => n * 2);         // transform (map)
nums.First(n => n > 3);          // first match (throws if none)
nums.FirstOrDefault(n => n > 99);// first match or default
nums.Any(n => n > 5);            // does any match?
nums.All(n => n > 0);            // do all match?
nums.Count(n => n % 2 == 0);     // count matches
nums.Sum();  nums.Average();  nums.Min();  nums.Max();
nums.Distinct();  nums.Take(3);  nums.Skip(3);  nums.OrderBy(n => n);
```

## Grouping, joining, flattening

```csharp
// Group people by age -> IGrouping<int, Person>
var byAge = people.GroupBy(p => p.Age);
foreach (var g in byAge)
    Console.WriteLine($"{g.Key}: {string.Join(", ", g.Select(p => p.Name))}");

// Join two sequences on a key
var rows = customers.Join(orders,
    c => c.Id, o => o.CustomerId,
    (c, o) => new { c.Name, o.Total });

// Flatten nested collections
var allItems = customers.SelectMany(c => c.Orders);
```

## Deferred execution — the gotcha

A LINQ query is a *recipe*, not a result. It runs only when you enumerate it
(`foreach`, `.ToList()`, `.Count()`). So this re-runs the query each time:

```csharp
var q = nums.Where(n => n > 5);   // nothing happens yet
var list = q.ToList();            // NOW it executes
```

Call `.ToList()` / `.ToArray()` to **materialise** when you need a stable
snapshot or will iterate more than once.

**Next:** functions as values — delegates, lambdas and events.
""",
        ),
        _t(
            "Delegates, lambdas & events",
            "10 min",
            """\
# Delegates, lambdas & events

A **delegate** is a type-safe reference to a method — a function you can store
in a variable and pass around. A **lambda** (`=>`) is an inline function.

```csharp
public delegate int MathOp(int a, int b);

MathOp add = (a, b) => a + b;
MathOp mul = (a, b) => a * b;
Console.WriteLine(add(2, 3));      // 5
```

## You rarely declare your own — use the built-ins

```csharp
Func<int, int, int> sum   = (a, b) => a + b;   // takes ints, returns int
Action<string>      print = msg => Console.WriteLine(msg);  // returns void
Predicate<int>      isEven = n => n % 2 == 0;  // returns bool
```

`Func<...,TResult>` returns a value, `Action<...>` returns nothing, `Predicate<T>`
is a bool test. These power LINQ — `Where` takes a `Func<T,bool>`.

## Events — the publish/subscribe pattern

An **event** is a delegate a class exposes for others to subscribe to. The
class raises it; subscribers react. It's the basis of UI clicks, message
handling, and decoupled notifications.

```csharp
public class Button
{
    public event EventHandler? Clicked;          // the event

    public void Press() => Clicked?.Invoke(this, EventArgs.Empty);  // raise it
}

var b = new Button();
b.Clicked += (sender, e) => Console.WriteLine("clicked!");   // subscribe
b.Clicked += OnClick;
b.Press();                                        // fires both handlers
b.Clicked -= OnClick;                             // unsubscribe

void OnClick(object? sender, EventArgs e) => Console.WriteLine("handler 2");
```

The `?.Invoke` guards against raising an event with **no** subscribers (which
would be null). Custom event data subclasses `EventArgs` and is delivered via
`EventHandler<TArgs>`.

**Next:** doing work without blocking — async/await.
""",
        ),
        _t(
            "Asynchronous programming",
            "12 min",
            """\
# Asynchronous programming

I/O — network calls, disk, databases — is slow. **async/await** lets a method
*await* a slow operation without blocking the thread, so your app stays
responsive and scales.

```csharp
using System.Threading.Tasks;

public async Task<string> FetchAsync(string url)
{
    using HttpClient client = new();
    string body = await client.GetStringAsync(url);   // yields the thread while waiting
    return body;
}
```

- A method marked **`async`** returns a `Task` (or `Task<T>`, or `ValueTask`).
- **`await`** unwraps the result when the awaited task completes, resuming the
  method where it left off.
- `Task` is "a promise of future work"; `Task<T>` carries a result.

```mermaid
flowchart LR
  A[caller] -->|await FetchAsync| B[I/O starts]
  B -.thread freed.-> C[other work runs]
  B ==>|I/O done| D[method resumes, returns]
```

## Sequential vs. concurrent

Awaiting one after another is sequential. To run independent work **at the same
time**, start the tasks first, then await them together:

```csharp
// Sequential — total time = t1 + t2
var a = await FetchAsync("url1");
var b = await FetchAsync("url2");

// Concurrent — total time ~= max(t1, t2)
Task<string> t1 = FetchAsync("url1");
Task<string> t2 = FetchAsync("url2");
string[] both = await Task.WhenAll(t1, t2);
```

`Task.WhenAny` completes when the *first* task finishes — useful for timeouts.

## Cancellation

Pass a `CancellationToken` so long work can be stopped cooperatively:

```csharp
public async Task WorkAsync(CancellationToken ct)
{
    for (int i = 0; i < 100; i++)
    {
        ct.ThrowIfCancellationRequested();
        await Task.Delay(100, ct);
    }
}

using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(5));
try { await WorkAsync(cts.Token); }
catch (OperationCanceledException) { Console.WriteLine("cancelled"); }
```

> Golden rule: **async all the way down** — `await` async calls rather than
> blocking on `.Result` or `.Wait()`, which can deadlock. The Advanced course
> covers `ValueTask`, async streams and `ConfigureAwait`.

**Next:** moving data in and out — files and JSON.
""",
        ),
        _t(
            "Files & JSON",
            "9 min",
            """\
# Files & JSON

## Reading and writing files

The `System.IO.File` helpers cover the common cases in one call — and have
async siblings you should prefer in server code:

```csharp
using System.IO;

string text   = File.ReadAllText("notes.txt");
string[] lines = File.ReadAllLines("notes.txt");
File.WriteAllText("out.txt", "hello");
File.AppendAllText("log.txt", "more\\n");

// Async — don't block a thread on disk I/O
string content = await File.ReadAllTextAsync("notes.txt");
await File.WriteAllTextAsync("out.txt", content);
```

For large files, stream instead of loading it all:

```csharp
using StreamReader reader = new("big.log");
string? line;
while ((line = await reader.ReadLineAsync()) is not null)
    Console.WriteLine(line);
```

`Path.Combine` builds paths portably; `Directory` creates/lists folders:

```csharp
string p = Path.Combine("data", "2026", "report.txt");
Directory.CreateDirectory("data/2026");
foreach (var f in Directory.GetFiles("data", "*.txt")) { /* ... */ }
```

## JSON with System.Text.Json

The built-in serializer turns objects to JSON and back:

```csharp
using System.Text.Json;

var person = new Person("Alice", 30);

string json = JsonSerializer.Serialize(person);
Person? back = JsonSerializer.Deserialize<Person>(json);

var opts = new JsonSerializerOptions
{
    WriteIndented = true,
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
};
string pretty = JsonSerializer.Serialize(person, opts);
```

Attributes customise the mapping:

```csharp
public class Product
{
    [JsonPropertyName("product_name")] public string Name { get; set; } = "";
    [JsonIgnore] public string InternalId { get; set; } = "";
}
```

Stream straight to/from a file, asynchronously:

```csharp
await using FileStream fs = File.Create("data.json");
await JsonSerializer.SerializeAsync(fs, person);
```

> `System.Text.Json` is the modern, fast, built-in choice (the older
> `Newtonsoft.Json` is still common in legacy code).

**Next:** check your knowledge.
""",
        ),
        _quiz(),
    ),
)


# ── C# — Advanced ────────────────────────────────────────────────────────────

_CSHARP_ADVANCED = SeedCourse(
    slug="csharp-advanced",
    title="C# — Advanced: ASP.NET Core & .NET in Production",
    description=(
        "Build production .NET services: dependency injection and the host, a "
        "REST API with ASP.NET Core, data access with Entity Framework Core, the "
        "middleware pipeline and auth, advanced async and performance, testing, "
        "and the design patterns and modern language features that tie it together."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Dependency injection & the host",
            "11 min",
            """\
# Dependency injection & the host

**Dependency injection (DI)** means a class declares the services it needs in
its constructor, and a **container** supplies them. It's built into .NET and is
the backbone of every ASP.NET Core app.

```csharp
public interface IEmailService { Task SendAsync(string to, string body); }

public class SmtpEmailService : IEmailService
{
    public Task SendAsync(string to, string body) => Task.CompletedTask;
}

public class UserService
{
    private readonly IEmailService _email;
    public UserService(IEmailService email) => _email = email;   // injected
}
```

## Registering services

You map an interface to an implementation in a `ServiceCollection`, choosing a
**lifetime**:

```csharp
var services = new ServiceCollection();

services.AddSingleton<IEmailService, SmtpEmailService>();  // one for the app
services.AddScoped<IUserRepository, UserRepository>();     // one per request
services.AddTransient<IValidator, Validator>();            // new every time

var provider = services.BuildServiceProvider();
var users = provider.GetRequiredService<UserService>();
```

| Lifetime | One instance per | Typical use |
|----------|------------------|-------------|
| **Singleton** | whole application | caches, config, stateless helpers |
| **Scoped** | request (web) | DbContext, per-request work |
| **Transient** | every resolve | lightweight, stateless services |

## Why it matters

DI **inverts control**: `UserService` doesn't `new` its dependencies, so you
can swap `SmtpEmailService` for a fake in tests, or a different implementation
in production — without touching `UserService`. Loose coupling, by design.

> Pitfall: never inject a **scoped** service into a **singleton** — the scoped
> object would outlive its scope. The container will warn you in development.

**Next:** exposing it over HTTP — a REST API.
""",
        ),
        _t(
            "Building a REST API with ASP.NET Core",
            "12 min",
            """\
# Building a REST API with ASP.NET Core

`dotnet new webapi` scaffolds a web service. Everything is configured in
**`Program.cs`** using the minimal hosting model: register services on the
*builder*, then build the *app* and wire the request pipeline.

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddScoped<IUserService, UserService>();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

## Controllers

A controller groups related endpoints. Attributes map HTTP verbs and routes;
the framework injects services and binds request data:

```csharp
[ApiController]
[Route("api/[controller]")]                       // -> /api/users
public class UsersController : ControllerBase
{
    private readonly IUserService _users;
    public UsersController(IUserService users) => _users = users;

    [HttpGet]                                      // GET /api/users
    public async Task<ActionResult<IEnumerable<UserDto>>> GetAll()
        => Ok(await _users.GetAllAsync());

    [HttpGet("{id:int}")]                          // GET /api/users/42
    public async Task<ActionResult<UserDto>> Get(int id)
    {
        var u = await _users.GetByIdAsync(id);
        return u is null ? NotFound() : Ok(u);
    }

    [HttpPost]                                     // POST /api/users
    public async Task<ActionResult<UserDto>> Create([FromBody] CreateUserDto dto)
    {
        var u = await _users.CreateAsync(dto);
        return CreatedAtAction(nameof(Get), new { id = u.Id }, u);  // 201 + Location
    }
}
```

Helpers like `Ok()`, `NotFound()`, `CreatedAtAction()` return the right status
codes. `[FromBody]`, `[FromQuery]`, `[FromRoute]` say where to bind data from.

## Minimal APIs

For small services you can skip controllers and map endpoints directly —
dependencies are just lambda parameters:

```csharp
var users = app.MapGroup("/api/users");

users.MapGet("/", (IUserService s) => s.GetAllAsync());
users.MapGet("/{id:int}", async (int id, IUserService s) =>
    await s.GetByIdAsync(id) is { } u ? Results.Ok(u) : Results.NotFound());
users.MapPost("/", async (CreateUserDto dto, IUserService s) =>
{
    var u = await s.CreateAsync(dto);
    return Results.Created($"/api/users/{u.Id}", u);
});
```

**Next:** persisting data with Entity Framework Core.
""",
        ),
        _t(
            "Data access with Entity Framework Core",
            "12 min",
            """\
# Data access with Entity Framework Core

**EF Core** is the standard ORM: you model tables as C# classes and query them
with LINQ — it generates the SQL. The hub is a **`DbContext`** exposing a
`DbSet<T>` per table.

```csharp
using Microsoft.EntityFrameworkCore;

public class User
{
    public int Id { get; set; }                    // convention: Id is the PK
    public string Name { get; set; } = "";
    public string Email { get; set; } = "";
    public List<Order> Orders { get; set; } = new();   // navigation property
}

public class AppDbContext : DbContext
{
    public DbSet<User> Users => Set<User>();
    public DbSet<Order> Orders => Set<Order>();

    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    protected override void OnModelCreating(ModelBuilder b)
    {
        b.Entity<User>(e =>
        {
            e.Property(x => x.Email).IsRequired().HasMaxLength(255);
            e.HasIndex(x => x.Email).IsUnique();
            e.HasMany(x => x.Orders).WithOne(o => o.User).HasForeignKey(o => o.UserId);
        });
    }
}
```

Register it (here scoped, as DbContext should be), pointing at a provider:

```csharp
builder.Services.AddDbContext<AppDbContext>(o =>
    o.UseSqlServer(builder.Configuration.GetConnectionString("Default")));
```

## Querying — it's just LINQ

```csharp
// Read — async, with related data eager-loaded
var users = await _db.Users
    .Include(u => u.Orders)            // JOIN in the generated SQL
    .Where(u => u.Email.EndsWith("@acme.com"))
    .OrderBy(u => u.Name)
    .ToListAsync();

var one = await _db.Users.FindAsync(id);   // by primary key

// Create / update / delete — staged, then committed in one SaveChanges
_db.Users.Add(new User { Name = "Ada", Email = "ada@acme.com" });
await _db.SaveChangesAsync();
```

`SaveChangesAsync` writes all pending changes in a single transaction. EF Core
**tracks** entities it loads, so editing a loaded object and calling
`SaveChangesAsync` issues the `UPDATE` for you.

## Migrations

Your C# model is the source of truth; **migrations** evolve the database schema
to match:

```bash
dotnet ef migrations add InitialCreate   # generate a migration from model changes
dotnet ef database update                # apply pending migrations to the DB
```

> Beware the **N+1** trap: lazy-loading `user.Orders` inside a loop fires one
> query per user. Use `.Include(...)` (or a projection with `.Select`) to fetch
> in one round trip.

**Next:** the request pipeline — middleware and auth.
""",
        ),
        _t(
            "Middleware, auth & cross-cutting concerns",
            "11 min",
            """\
# Middleware, auth & cross-cutting concerns

Every request flows through a **pipeline** of **middleware** — each component
can inspect the request, short-circuit it, or pass it to the `next` one and then
act on the response. Order matters.

```mermaid
flowchart LR
  R[request] --> M1[Exception handler] --> M2[HTTPS redirect] --> M3[Auth] --> E[endpoint]
  E --> M3 --> M2 --> M1 --> P[response]
```

```csharp
app.UseExceptionHandler("/error");
app.UseHttpsRedirection();
app.UseAuthentication();          // who are you?
app.UseAuthorization();           // are you allowed?
app.MapControllers();
```

## Writing custom middleware

A middleware is a class with an `InvokeAsync(HttpContext, ...)` that calls
`_next`. This one times every request:

```csharp
public class RequestTimingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestTimingMiddleware> _log;

    public RequestTimingMiddleware(RequestDelegate next, ILogger<RequestTimingMiddleware> log)
        => (_next, _log) = (next, log);

    public async Task InvokeAsync(HttpContext ctx)
    {
        var sw = Stopwatch.StartNew();
        try { await _next(ctx); }                  // run the rest of the pipeline
        finally
        {
            sw.Stop();
            _log.LogInformation("{Method} {Path} -> {Status} in {Ms}ms",
                ctx.Request.Method, ctx.Request.Path, ctx.Response.StatusCode,
                sw.ElapsedMilliseconds);
        }
    }
}

app.UseMiddleware<RequestTimingMiddleware>();
```

A centralised **exception-handling** middleware turns thrown exceptions into
clean JSON error responses — so controllers don't each repeat try/catch.

## Authentication & authorization

`UseAuthentication` establishes *who* the caller is (e.g. from a **JWT** bearer
token); `UseAuthorization` enforces *what* they may do. Attributes gate
endpoints:

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(o => o.TokenValidationParameters = new()
    {
        ValidateIssuer = true, ValidateAudience = true,
        ValidateLifetime = true, ValidateIssuerSigningKey = true,
        ValidIssuer = config["Jwt:Issuer"],
        ValidAudience = config["Jwt:Audience"],
        IssuerSigningKey = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(config["Jwt:Key"]!)),
    });

[Authorize(Roles = "Admin")]      // only admins
[HttpDelete("{id:int}")]
public async Task<IActionResult> Delete(int id) { /* ... */ }
```

Config and secrets come from `appsettings.json` + environment + the **Options
pattern** (`IOptions<T>`), keeping `Jwt:Key` out of code.

**Next:** making it fast and correct — advanced async & performance.
""",
        ),
        _t(
            "Advanced async & performance",
            "11 min",
            """\
# Advanced async & performance

## ValueTask — skip the allocation on the hot path

Every `Task` is a heap allocation. For a method that *often* completes
synchronously (e.g. a cache hit), `ValueTask<T>` avoids that allocation:

```csharp
public ValueTask<int> GetAsync(string key)
    => _cache.TryGetValue(key, out var v)
        ? new ValueTask<int>(v)                 // synchronous, no allocation
        : new ValueTask<int>(LoadAsync(key));   // falls back to a real Task
```

Use `ValueTask` only for high-frequency methods, and await it **once**.

## Async streams

`IAsyncEnumerable<T>` streams items as they become available — `await foreach`
consumes them without buffering everything:

```csharp
public async IAsyncEnumerable<int> ReadAsync()
{
    for (int i = 0; i < 10; i++) { await Task.Delay(50); yield return i; }
}

await foreach (var n in ReadAsync())
    Console.WriteLine(n);
```

## Deadlocks and ConfigureAwait

Blocking on async code — `.Result` / `.Wait()` — can **deadlock** when the
continuation needs a context the blocked thread holds. Don't block; await. In
libraries, `ConfigureAwait(false)` says "I don't need the original context",
avoiding the trap and reducing overhead:

```csharp
string body = await client.GetStringAsync(url).ConfigureAwait(false);
```

## Spans and allocation awareness

The GC is fast, but allocations add up in hot paths. `Span<T>` /
`ReadOnlySpan<T>` give a typed window over memory — array, stack, or string —
with **no copy**:

```csharp
ReadOnlySpan<char> s = "2026-06-09";
ReadOnlySpan<char> year = s[..4];      // "2026" — no substring allocation
int y = int.Parse(year);
```

> Performance order of attack: don't block threads (async I/O), don't allocate
> in tight loops (reuse buffers, `Span`), and **measure** with BenchmarkDotNet
> before optimising. Correct-and-clear first; fast where it's proven to matter.

**Next:** proving it works — testing.
""",
        ),
        _t(
            "Testing .NET applications",
            "10 min",
            """\
# Testing .NET applications

## Unit tests with xUnit

**xUnit** is the de-facto test framework. `[Fact]` is a single test;
`[Theory]` + `[InlineData]` runs the same test over many inputs:

```csharp
using Xunit;

public class CalculatorTests
{
    [Fact]
    public void Add_returns_sum()
    {
        var calc = new Calculator();
        Assert.Equal(5, calc.Add(2, 3));
    }

    [Theory]
    [InlineData(2, 3, 5)]
    [InlineData(-1, 1, 0)]
    [InlineData(0, 0, 0)]
    public void Add_various(int a, int b, int expected)
        => Assert.Equal(expected, new Calculator().Add(a, b));
}
```

Run them with `dotnet test`. A good test follows **Arrange-Act-Assert**.

## Mocking dependencies with Moq

To test a class in isolation, replace its dependencies with **mocks** —
fakes you program and verify:

```csharp
using Moq;

[Fact]
public async Task GetUser_reads_from_repository()
{
    var repo = new Mock<IUserRepository>();
    repo.Setup(r => r.GetByIdAsync(1))
        .ReturnsAsync(new User { Id = 1, Name = "Alice" });

    var service = new UserService(repo.Object);

    var user = await service.GetByIdAsync(1);

    Assert.Equal("Alice", user!.Name);
    repo.Verify(r => r.GetByIdAsync(1), Times.Once);   // it was called exactly once
}
```

This is exactly why DI (depending on `IUserRepository`, not a concrete class)
makes code testable.

## Integration tests with WebApplicationFactory

For an ASP.NET Core app, spin up the whole pipeline in-memory and hit it with a
real `HttpClient` — no network, no port:

```csharp
public class UsersApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    public UsersApiTests(WebApplicationFactory<Program> f) => _client = f.CreateClient();

    [Fact]
    public async Task GET_users_succeeds()
    {
        var resp = await _client.GetAsync("/api/users");
        resp.EnsureSuccessStatusCode();
    }
}
```

> Pyramid of tests: many fast **unit** tests, fewer **integration** tests across
> components, and a thin top of end-to-end tests. Test behaviour, not
> implementation details.

**Next:** patterns and the modern language features that tie it together.
""",
        ),
        _t(
            "Design patterns & modern C#",
            "10 min",
            """\
# Design patterns & modern C#

## A few patterns you'll meet constantly

**Singleton** — one shared instance (though DI's `AddSingleton` is the idiomatic
way now):

```csharp
public sealed class Config
{
    private static readonly Lazy<Config> _i = new(() => new Config());
    public static Config Instance => _i.Value;
    private Config() { }
}
```

**Factory** — centralise object creation behind a method:

```csharp
public class VehicleFactory
{
    public IVehicle Create(string kind) => kind switch
    {
        "car" => new Car(),
        "bike" => new Motorcycle(),
        _ => throw new ArgumentException($"unknown: {kind}"),
    };
}
```

**Builder** — assemble a complex object step by step with a fluent chain:

```csharp
var email = new EmailBuilder()
    .To("user@acme.com")
    .Subject("Hi")
    .Body("Welcome")
    .Build();
```

**Repository** (you've used it) abstracts data access behind an interface so the
domain doesn't depend on EF Core directly.

## Modern language features worth adopting

```csharp
// File-scoped namespace (C# 10) — one less level of nesting:
namespace MyApp.Services;

// Primary constructor (C# 12) — parameters available across the class:
public class UserService(IUserRepository repo, ILogger<UserService> log)
{
    public Task<User?> GetAsync(int id) => repo.GetByIdAsync(id);
}

// Required members (C# 11) — must be set at construction:
public class Order
{
    public required string Sku { get; init; }
    public required decimal Total { get; init; }
}

// Pattern matching keeps branching declarative:
decimal Discount(Customer c) => c switch
{
    { Tier: "Gold", Years: > 5 } => 0.20m,
    { Tier: "Gold" }             => 0.10m,
    _                            => 0m,
};
```

And **nullable reference types** (`<Nullable>enable</Nullable>` in the
`.csproj`) make "can this be null?" a compile-time conversation — the single
biggest defence against `NullReferenceException`.

> You now have the arc: language → LINQ/async → DI, web APIs, EF Core,
> middleware, testing, and the patterns that organise it. That's a production
> .NET service.

**Next:** check your knowledge.
""",
        ),
        _quiz(),
    ),
)


CSHARP_COURSES: tuple[SeedCourse, ...] = (
    _CSHARP_BASICS,
    _CSHARP_INTERMEDIATE,
    _CSHARP_ADVANCED,
)

__all__ = ["CSHARP_COURSES"]
