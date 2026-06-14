"""Academy seed content — the Concurrency & Parallelism track (Beginner → Advanced).

* ``concurrency-basics``        — concurrency vs parallelism, threads/processes, races, the GIL, vectorization
* ``concurrency-intermediate``  — thread pools, reduction, patterns, deadlock, Amdahl/Gustafson, memory models
* ``concurrency-advanced``      — the CUDA/GPU model, kernels, scan/reduction/tiling, lock-free, multi-GPU/MPI

Focus languages: **Python** (threads/GIL, asyncio, multiprocessing, numpy) and
**modern C++** (``std::thread``/``std::atomic``) with **CUDA**. The sandbox runs
Python+numpy only and blocks threading/asyncio, so runnable ``code`` lessons
*simulate* concurrency deterministically (race interleavings, parallel reduction,
producer-consumer, deadlock graphs, CUDA index math, prefix scan) and use numpy
for real data parallelism; real threading/C++/CUDA appears as read-only blocks.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, ², ×) in diagrams and labels.
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
# concurrency-basics
# ──────────────────────────────────────────────────────────────────────

_CC_BASICS = SeedCourse(
    slug="concurrency-basics",
    title="Concurrency & Parallelism — Basics",
    description=(
        "The foundations: how concurrency differs from parallelism, processes vs "
        "threads, why shared state causes race conditions, synchronization, "
        "Python's threading/GIL/asyncio model and modern C++ threads, and data "
        "parallelism with numpy. With runnable race-condition and vectorization "
        "labs."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Concurrency vs parallelism",
            "10 min",
            r"""# Concurrency vs parallelism

These two words are used interchangeably and they shouldn't be — the distinction
is the foundation of everything that follows.

- **Concurrency** is about **dealing with many things at once** — *structure*. A
  program is concurrent if it has multiple independent **tasks in progress** that
  can be interleaved. One CPU core can be concurrent by rapidly switching between
  tasks (time-slicing): nothing runs *simultaneously*, but progress is made on
  many things.
- **Parallelism** is about **doing many things at once** — *execution*. A program
  is parallel if multiple computations literally run **at the same instant**, which
  requires multiple hardware execution units (cores, or thousands of GPU lanes).

Rob Pike's line: *"Concurrency is not parallelism."* Concurrency is a way to
**structure** a program as independent tasks; parallelism is **running** them
simultaneously. You can have:

```
Concurrent, not parallel:  1 core switching between tasks (async I/O)
Parallel, (implicitly) concurrent: many cores running tasks at once
Neither:                   one task, start to finish
```

**Why each matters:**

- **Concurrency** shines for **I/O-bound** work — waiting on the network, disk, or
  user. While one task waits, others run. (A web server handling thousands of
  slow connections needs concurrency, not necessarily many cores.)
- **Parallelism** shines for **CPU-bound** work — crunching numbers, rendering,
  training models. To go faster you must use more cores/GPUs *at the same time*.

This split drives every later decision: an I/O-bound Python service reaches for
**asyncio** (concurrency on one thread); a CPU-bound numerical job reaches for
**multiprocessing**, **numpy vectorization**, C++ **threads**, or **CUDA**
(true parallelism). Knowing whether your bottleneck is **waiting** or
**computing** tells you which tool you need — and using the wrong one (threads for
CPU work in Python, say) gives no speedup at all. Keep this distinction in mind
through the whole track.
""",
        ),
        _t(
            "Processes, threads & the OS",
            "11 min",
            r"""# Processes, threads & the OS

To run tasks concurrently the operating system gives you two units of execution
(Operating Systems track, here from the concurrency angle):

- **Process** — an independent program with its **own private memory space**. Two
  processes are **isolated**: one crashing or corrupting memory can't directly
  harm another. Communication needs explicit **IPC** (pipes, sockets, shared
  memory). Heavier to create.
- **Thread** — a unit of execution **inside** a process. Threads of one process
  **share the same memory** (heap, globals), so they communicate cheaply by
  reading/writing shared data — but that shared memory is exactly what makes
  threads **dangerous** (races, next lesson). Lighter to create; each has its own
  stack and registers.

```
Process A                      Process B
 ├─ shared heap (threads see)   ├─ separate heap
 ├─ Thread 1 (own stack)        └─ Thread 1
 └─ Thread 2 (own stack)
```

**Context switching** is how one core runs many threads: the OS **scheduler**
saves a thread's registers/state, loads another's, and resumes it — fast, but not
free (it costs cycles and cache misses, so spawning thousands of OS threads has
real overhead). On an N-core machine, up to N threads run **truly in parallel**;
beyond that they're **interleaved**.

The crucial trade-off you choose constantly:

- **Threads (shared memory)** — fast communication, low overhead, but you must
  **synchronise** access to shared data (the hard part). Best for closely
  cooperating tasks.
- **Processes (isolated memory)** — safe by isolation, no data races, but
  communication is explicit and heavier. Best for independent tasks or fault
  isolation (and, in Python, to escape the GIL — soon).

Modern systems also add lighter abstractions on top — **green threads /
coroutines** (asyncio tasks, Go goroutines) scheduled in **user space** without an
OS thread each, so you can have *millions* of concurrent tasks cheaply. But under
everything sits this reality: **isolated processes vs shared-memory threads**, and
the OS scheduler interleaving them onto a finite number of cores.
""",
        ),
        _t(
            "Race conditions & shared state",
            "11 min",
            r"""# Race conditions & shared state

Here's why concurrency is genuinely hard. When multiple threads **share mutable
state**, the *interleaving* of their operations is **non-deterministic** — and
some interleavings produce **wrong answers**. That's a **race condition**.

The classic example: two threads each increment a shared counter. The innocent
line `counter += 1` is **not atomic** — it's really three steps:

```
1. READ   counter into a register      (temp = counter)
2. MODIFY  add 1 in the register        (temp = temp + 1)
3. WRITE   store back to counter        (counter = temp)
```

If two threads interleave those steps, an update is **lost**:

```
Thread A: READ counter (0)
Thread B: READ counter (0)          <- both saw 0
Thread A: temp=1, WRITE counter=1
Thread B: temp=1, WRITE counter=1   <- B overwrites; one increment vanished!
```

Two increments, but `counter` ends at **1**, not 2. Run it a million times across
threads and you lose a random number of updates every run.

What makes races so insidious:

- **Non-deterministic** — they depend on timing/scheduling, so the bug appears
  *sometimes*, often not under a debugger ("Heisenbug").
- **Invisible in the source** — the code *looks* correct; the danger is in what
  the hardware/runtime is allowed to interleave and reorder.

A **data race** specifically = two threads access the **same memory**, **at least
one writes**, and there's **no synchronisation** ordering them. In C++ a data race
is **undefined behaviour** (anything can happen); in Python the GIL prevents memory
corruption but `+=` can still lose updates.

The cause is always the same trio: **shared + mutable + concurrent**. Remove any
one and the race is gone — which is the key to the cures:

- **Don't share** — give each thread its own data (or use processes/immutability).
- **Don't mutate** — use immutable data and message passing.
- **Synchronise** — make the critical section **atomic** with a lock (next lesson).

You'll watch a lost update happen, deterministically, in the next lab.
""",
        ),
        _code(
            "Simulate a race condition",
            "12 min",
            r"""# A race condition: 'counter += 1' is really READ, MODIFY, WRITE. If two threads
# interleave those steps, an update is LOST. We model the interleaving explicitly
# (a schedule) so the bug is deterministic and visible. Pure builtins.

# --- A BAD interleaving: both read before either writes ---
shared = 0
local = {"T1": 0, "T2": 0}
schedule = [
    ("T1", "read"), ("T2", "read"),     # both read shared = 0
    ("T1", "modify"), ("T2", "modify"), # both compute 0 + 1 = 1
    ("T1", "write"), ("T2", "write"),   # both store 1 -> one increment lost
]
for thread, step in schedule:
    if step == "read":
        local[thread] = shared
    elif step == "modify":
        local[thread] = local[thread] + 1
    else:
        shared = local[thread]
    print("  ", thread, step, " shared =", shared, " locals =", local)

print("two increments, but shared =", shared, "(expected 2) -> LOST UPDATE")
print()

# --- An ATOMIC increment: read-modify-write is one indivisible step ---
atomic = 0
for thread in ["T1", "T2"]:
    atomic = atomic + 1            # nothing can interleave inside this step
print("with atomic increments, value =", atomic, "(correct)")
print("the fix: make the critical section atomic (a lock / atomic op)")
""",
        ),
        _t(
            "Synchronization: locks, mutexes & atomics",
            "11 min",
            r"""# Synchronization: locks, mutexes & atomics

If shared mutable state causes races, **synchronization** is how you tame it —
imposing order so only safe interleavings happen.

**The mutex (mutual exclusion lock)** is the workhorse. A thread **acquires** the
lock before touching shared data and **releases** it after; only one thread can
hold it at a time, so the protected region — the **critical section** — runs
**atomically** with respect to other threads:

```python
# Python
import threading
lock = threading.Lock()
def increment():
    with lock:            # acquire ... release (even on exception)
        counter[0] += 1   # critical section: now safe
```

```cpp
// Modern C++
#include <mutex>
std::mutex m;
{
    std::lock_guard<std::mutex> guard(m);   // RAII: unlocks at scope exit
    ++counter;                               // critical section
}
```

Other synchronization primitives, each for a job:

- **Atomic operations** — for simple updates (a counter, a flag), an **atomic**
  (`std::atomic<int>`, hardware compare-and-swap) does the read-modify-write as
  one indivisible instruction — **lock-free** and faster than a mutex.
- **Read-write lock** — many concurrent readers **or** one writer; great for
  read-heavy data.
- **Semaphore** — a counter permitting up to N concurrent holders (e.g. limit to
  10 simultaneous downloads).
- **Condition variable** — wait until a condition holds ("buffer not empty"),
  used to coordinate, not just exclude (producer-consumer, next course).
- **Barrier** — all threads wait until everyone reaches a point, then proceed
  together (common in parallel algorithms).

The costs and pitfalls you must respect:

- **Contention** — if many threads fight over one lock, they **serialise** and you
  lose parallelism (the lock becomes the bottleneck). Keep critical sections
  **short** and lock **granularity** fine.
- **Deadlock** — acquire locks in inconsistent orders and threads wait on each
  other forever (a whole lesson in the next course).
- **Overhead** — locking isn't free; over-synchronising kills performance.

The guiding principle: **synchronise the minimum necessary**, prefer **atomics**
for simple cases, prefer **not sharing** at all where you can, and keep critical
sections tiny. Correctness first — a fast program that's occasionally wrong is
worthless — but the art is being correct **and** keeping threads actually running
in parallel.
""",
        ),
        _t(
            "Python concurrency: threads, the GIL & asyncio",
            "12 min",
            r"""# Python concurrency: threads, the GIL & asyncio

Python's concurrency story is dominated by one fact: the **GIL (Global Interpreter
Lock)**. CPython allows only **one thread to execute Python bytecode at a time**,
even on a many-core machine. The consequence is stark and must be internalised:

- **Threads do NOT give CPU parallelism in CPython.** Ten threads doing heavy
  Python computation run no faster than one — they take turns holding the GIL.
- **Threads DO help I/O-bound work**, because the GIL is **released during I/O**
  (and during many numpy/C operations). While one thread waits on the network, the
  others run. So threading is for **waiting**, not **computing**.

Python therefore offers three tools, matched to the workload:

- **`threading`** — concurrency for **I/O-bound** tasks (many network/file waits).
  Shared memory → you still need locks. No CPU speedup.

```python
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(fetch_url, urls))   # great for I/O
```

- **`asyncio`** — **single-threaded** concurrency via an event loop and
  `async`/`await` **coroutines**. Cheaper than threads (no OS thread each, no lock
  worries within one thread), scaling to **tens of thousands** of concurrent I/O
  tasks. The modern choice for high-concurrency I/O (web servers, scrapers).

```python
async def main():
    results = await asyncio.gather(*(fetch(u) for u in urls))
```

- **`multiprocessing`** — **separate processes**, each with its **own Python
  interpreter and GIL**, achieving **true CPU parallelism**. The way to use all
  cores for CPU-bound pure-Python work — at the cost of process overhead and
  having to **pickle** data between processes.

```python
from multiprocessing import Pool
with Pool() as pool:
    results = pool.map(heavy_compute, chunks)   # real multi-core
```

The decision tree every Python developer needs:

```
I/O-bound, lots of waiting?     -> asyncio (or threads)
CPU-bound, pure Python?         -> multiprocessing (escape the GIL)
CPU-bound, numerical?           -> numpy/numba/C-extensions (release the GIL) — next
```

Note: alternative interpreters and recent work (PyPy, and **free-threaded
"no-GIL" CPython**, 3.13+) change this picture, but for now the GIL is the
defining constraint — and choosing the right one of these three is the single most
important Python concurrency decision.
""",
        ),
        _code(
            "Vectorization = data parallelism",
            "12 min",
            r"""# The fastest 'parallelism' in Python often isn't threads at all — it's
# VECTORIZATION. numpy applies one operation across a whole array at once (SIMD /
# parallel hardware under the hood, with the GIL released). Compare a scalar loop
# to a vectorized op. Press Run.

import numpy as np

# Scalar / sequential: a Python loop processes one element at a time.
small = np.arange(1, 11)            # 1..10
loop_total = 0
for x in small:
    loop_total = loop_total + int(x) * int(x)
print("loop sum of squares (1..10):", loop_total)

# Data-parallel: ONE vectorized expression over the whole array.
n = 1_000_000
big = np.arange(1, n + 1)
vec_total = int((big * big).sum())            # squared & summed in one parallel op
print("vectorized sum of squares (1..%d): %d" % (n, vec_total))
print("closed-form n(n+1)(2n+1)/6:        %d" % (n * (n + 1) * (2 * n + 1) // 6))

# Vectorization is 'data parallelism': the SAME operation applied to MANY elements
# simultaneously. A matmul is the same idea at higher dimension:
A = np.ones((100, 100))
B = np.ones((100, 100))
C = A @ B                                      # 100x100x100 multiply-adds, parallel
print("matmul (100x100) element [0,0] =", float(C[0, 0]))
print("for numerical work, vectorize first — it beats Python threads every time")
""",
        ),
        _t(
            "Modern C++ concurrency",
            "10 min",
            r"""# Modern C++ concurrency

Unlike Python, C++ has **no GIL** — threads run with **true parallelism** across
cores, which is why C++ (with CUDA) is the language of high-performance computing.
Since C++11 the standard library has first-class concurrency.

**`std::thread`** — launch a thread directly:

```cpp
#include <thread>
void work(int id) { /* ... */ }
std::thread t1(work, 1);
std::thread t2(work, 2);
t1.join();                 // wait for completion
t2.join();
```

**`std::async` / `std::future`** — task-based: run a function asynchronously and
get its result later via a **future** (often nicer than raw threads):

```cpp
#include <future>
std::future<int> fut = std::async(std::launch::async, compute, x);
int result = fut.get();    // blocks until ready
```

**Synchronization** mirrors the primitives you met, with **RAII** making them
safe:

```cpp
std::mutex m;
{
    std::lock_guard<std::mutex> lk(m);   // auto-unlocks at end of scope
    shared += 1;
}
std::atomic<int> counter{0};
counter.fetch_add(1);                    // lock-free atomic increment
```

Because C++ threads are real and the compiler/CPU **reorder** memory operations,
C++ exposes a **memory model** (`std::memory_order`) so you can reason about what
one thread sees of another's writes (Intermediate course) — power that also means
a **data race in C++ is undefined behaviour**: it can crash, corrupt, or silently
misbehave. No GIL to save you.

The modern toolkit also includes higher-level options: **`std::jthread`** (C++20,
auto-joining + cooperative cancellation), **parallel STL algorithms**
(`std::execution::par` — `std::sort(std::execution::par, ...)` parallelises across
cores for free), **OpenMP** pragmas for easy loop parallelism, and **Thread
Building Blocks (TBB)** for task graphs.

The C++ mindset: you have **real parallelism and total control** — and therefore
**total responsibility**. You manage lifetimes (`join`), avoid data races
(undefined behaviour), and respect the memory model. That control is exactly why,
when raw compute speed matters, the path runs through modern C++ — and onto the
GPU with CUDA (Advanced course).
""",
        ),
        quiz_lesson(
            "Quiz: Concurrency Foundations",
            (
                q(
                    "What is the difference between concurrency and parallelism?",
                    (
                        opt(
                            "Concurrency is structuring work as interleavable tasks (dealing with many things); parallelism is executing them simultaneously (doing many at once)",
                            correct=True,
                        ),
                        opt("They are exactly the same thing"),
                        opt("Concurrency requires multiple cores; parallelism needs only one"),
                        opt("Parallelism is only about I/O"),
                    ),
                    "Concurrency is about structure (interleaving tasks, even on one core); parallelism is about simultaneous execution on multiple cores/units.",
                ),
                q(
                    "What do threads share that processes do not?",
                    (
                        opt(
                            "The same memory space (heap/globals) — cheap communication, but it requires synchronization",
                            correct=True,
                        ),
                        opt("Nothing — they are identical"),
                        opt("Their CPU registers"),
                        opt("Their program counter"),
                    ),
                    "Threads of one process share memory (fast but race-prone); processes are isolated and communicate via explicit IPC.",
                ),
                q(
                    "Why is 'counter += 1' a race condition without synchronization?",
                    (
                        opt(
                            "It's a non-atomic read-modify-write; interleaved threads can both read the old value and one update is lost",
                            correct=True,
                        ),
                        opt("It is too slow"),
                        opt("It uses too much memory"),
                        opt("Addition is undefined"),
                    ),
                    "The three steps (read, modify, write) can interleave so two increments produce only one — a lost update.",
                ),
                q(
                    "What does CPython's GIL mean for threads?",
                    (
                        opt(
                            "Only one thread runs Python bytecode at a time, so threads help I/O-bound work but give no CPU speedup",
                            correct=True,
                        ),
                        opt("Threads always run fully in parallel on all cores"),
                        opt("Python cannot use threads at all"),
                        opt("The GIL makes CPU-bound code faster"),
                    ),
                    "The GIL serialises bytecode execution; use multiprocessing (or numpy/C) for CPU parallelism, threads/asyncio for I/O.",
                ),
                q(
                    "For CPU-bound numerical work in Python, what's usually the best first move?",
                    (
                        opt(
                            "Vectorize with numpy (data parallelism, GIL released) rather than using threads",
                            correct=True,
                        ),
                        opt("Spawn hundreds of threads"),
                        opt("Use asyncio"),
                        opt("Add more print statements"),
                    ),
                    "Vectorized numpy applies one op across a whole array on parallel hardware, far beating Python-level threads for numeric work.",
                ),
                q(
                    "How does modern C++ concurrency differ fundamentally from Python's?",
                    (
                        opt(
                            "C++ has no GIL, so std::thread gives true multi-core parallelism — with the responsibility that data races are undefined behaviour",
                            correct=True,
                        ),
                        opt("C++ cannot do concurrency"),
                        opt("C++ threads are slower than Python threads"),
                        opt("C++ has a stronger GIL"),
                    ),
                    "C++ threads run truly in parallel; you manage joins, races (UB), and the memory model yourself — full control and full responsibility.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# concurrency-intermediate
# ──────────────────────────────────────────────────────────────────────

_CC_INTERMEDIATE = SeedCourse(
    slug="concurrency-intermediate",
    title="Concurrency & Parallelism — Intermediate",
    description=(
        "Patterns and pitfalls: task-based parallelism and thread pools, parallel "
        "reduction, the core patterns (map-reduce, fork-join, producer-consumer), "
        "deadlock, the scalability laws (Amdahl & Gustafson), and memory models — "
        "with runnable reduction, producer-consumer, and deadlock-detection labs."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Task-based parallelism & thread pools",
            "10 min",
            r"""# Task-based parallelism & thread pools

Creating a thread per unit of work is wasteful — thread creation has real overhead,
and spawning thousands oversubscribes the cores and thrashes the scheduler. The
modern approach is **task-based parallelism**: you express **what** can run
independently (tasks), and a **runtime** schedules them onto a **fixed pool** of
worker threads.

**Thread pools** keep a set of long-lived workers (typically ≈ number of cores)
pulling tasks from a queue:

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
with ProcessPoolExecutor() as pool:               # CPU-bound -> processes
    futures = [pool.submit(work, x) for x in items]
    results = [f.result() for f in futures]
```

```cpp
auto fut = std::async(std::launch::async, work, x);   // C++ task -> future
int r = fut.get();
```

**Futures / promises** are the glue: a **future** is a handle to a result that
**will exist later**. You submit a task, get a future immediately, keep working,
and **`get()`** the result when you need it (blocking only then). This decouples
*starting* work from *collecting* it.

**Work stealing** is the scheduling trick behind great task runtimes (TBB, Cilk,
Go, Rust's rayon, .NET TPL): each worker has its own task deque; an idle worker
**steals** tasks from a busy worker's queue. This balances load automatically even
when tasks have wildly different sizes — no central bottleneck.

Why think in **tasks, not threads**:

- **Right-sized parallelism** — the pool matches threads to hardware; you don't
  over/under-subscribe.
- **Composability** — tasks can spawn sub-tasks (fork-join) and the runtime sorts
  out scheduling.
- **Granularity control** — tasks too **fine** drown in scheduling overhead; too
  **coarse** and load is unbalanced. Aim for tasks big enough to dwarf scheduling
  cost yet numerous enough to keep all cores fed.

The shift from "manage threads" to "submit tasks and await futures" is the single
biggest ergonomic improvement in modern concurrency — you describe the *available
parallelism* and let a tuned runtime exploit it. The next lessons cover the
**patterns** you express on top of this.
""",
        ),
        _code(
            "Parallel reduction",
            "12 min",
            r"""# Summing N numbers sequentially takes N-1 dependent adds. A PARALLEL REDUCTION
# combines pairs simultaneously, halving the count each 'level' -> only log2(N)
# steps. We simulate the tree of parallel additions. Pure builtins.

values = [3, 1, 7, 0, 4, 1, 6, 3]      # 8 values
print("input:", values)
print("sequential sum needs", len(values) - 1, "dependent adds")
print()

level = 0
current = values
while len(current) > 1:
    nxt = []
    i = 0
    while i < len(current):
        if i + 1 < len(current):
            nxt.append(current[i] + current[i + 1])   # this pair adds in PARALLEL
        else:
            nxt.append(current[i])                    # odd one carries up
        i = i + 2
    level = level + 1
    print("after parallel level", level, ":", nxt)
    current = nxt

print()
print("reduced sum:", current[0], "in", level, "parallel levels (log2 of", len(values), ")")
# Each level's additions are independent -> done at once on many cores/GPU lanes.
# This log-depth tree is THE pattern behind parallel sum, max, min, dot-product...
""",
        ),
        _t(
            "Parallel patterns",
            "11 min",
            r"""# Parallel patterns

Most parallel programs are built from a handful of reusable **patterns**. Knowing
them lets you recognise the right structure instead of inventing ad-hoc threading.

- **Map (embarrassingly parallel)** — apply the same independent operation to every
  element of a collection. No dependencies between items → near-perfect speedup.
  (Resize 10,000 images; `pool.map`.) The easiest and best case.
- **Reduce** — combine many values into one (sum, max, count) via the **log-depth
  tree** you just built. Map + reduce together = **MapReduce**, the backbone of big
  data (Data Engineering track).
- **Fork-join** — **fork** a task into independent sub-tasks that run in parallel,
  then **join** (wait for all) and combine results. Naturally **recursive** —
  parallel merge sort, quicksort, tree algorithms. The model behind Cilk, Java's
  ForkJoinPool, and rayon.

```
fork-join (parallel sum of an array):
  split array in half -> [fork left] [fork right] -> join -> add the two sums
```

- **Pipeline** — stages connected in series, each running concurrently on a
  different item, like an assembly line: while stage 3 processes item 1, stage 1
  processes item 3. Throughput rises to the **slowest stage**; great for streaming
  (decode → transform → encode).
- **Producer-consumer** — producers put work on a **shared queue**, consumers take
  it off; the queue **decouples** their rates and provides **backpressure** (a
  bounded queue makes fast producers wait). The fundamental coordination pattern
  (you'll simulate it next).
- **Scatter-gather** — distribute (scatter) a problem across workers, collect
  (gather) the partial results. The shape of most distributed queries.

**Choosing a pattern** comes down to the **dependency structure** of your problem:

```
Independent items?        -> map
Combine to one value?     -> reduce
Recursive divide-conquer? -> fork-join
Sequential stages?        -> pipeline
Decouple producers/consumers rates? -> producer-consumer queue
```

The deeper point: **expose independent work and minimise dependencies**. The
patterns are just well-understood dependency shapes that runtimes parallelise
well. Identify which one your problem fits and the parallelisation almost writes
itself — and dependencies you *can't* remove (the serial part) are exactly what
limits your speedup, which the scalability laws make precise.
""",
        ),
        _code(
            "Producer-consumer with a bounded queue",
            "13 min",
            r"""# Producers add work to a shared QUEUE; consumers take it off. A BOUNDED queue
# decouples their speeds and gives backpressure: producers WAIT when it's full,
# consumers WAIT when it's empty. Simulate a schedule and watch the queue. Builtins.

capacity = 3
buffer = []
blocked_producers = 0
blocked_consumers = 0

# A schedule of operations from several producers/consumers, interleaved.
schedule = [
    ("produce", "a"), ("produce", "b"), ("produce", "c"),
    ("produce", "d"),                       # queue full (3) -> producer blocks
    ("consume", None), ("consume", None),
    ("produce", "d"), ("produce", "e"),
    ("consume", None), ("consume", None), ("consume", None),
    ("consume", None),                      # queue empty -> consumer blocks
]

for action, item in schedule:
    if action == "produce":
        if len(buffer) >= capacity:
            blocked_producers = blocked_producers + 1
            print("  produce", item, "-> BLOCKED (full, backpressure)")
        else:
            buffer.append(item)
            print("  produce", item, "-> queue", buffer)
    else:
        if len(buffer) == 0:
            blocked_consumers = blocked_consumers + 1
            print("  consume  -> BLOCKED (empty)")
        else:
            got = buffer.pop(0)
            print("  consume", got, "-> queue", buffer)

print()
print("blocked producers:", blocked_producers, " blocked consumers:", blocked_consumers)
print("the bounded queue throttles the fast side to the slow side — backpressure.")
""",
        ),
        _t(
            "Deadlock, livelock & starvation",
            "11 min",
            r"""# Deadlock, livelock & starvation

Synchronization fixes races but introduces new failure modes where threads get
**stuck** or **treated unfairly**.

**Deadlock** — two or more threads each **wait forever** for a resource the other
holds. The textbook case: thread A locks resource 1 then wants 2; thread B locks 2
then wants 1 — both wait, neither yields.

```
A: lock(1) ... wants lock(2)   [held by B]
B: lock(2) ... wants lock(1)   [held by A]      -> frozen forever
```

Deadlock requires **all four Coffman conditions** simultaneously — break any one
and deadlock is impossible:

1. **Mutual exclusion** — resources can't be shared.
2. **Hold and wait** — a thread holds one resource while waiting for another.
3. **No preemption** — resources can't be forcibly taken away.
4. **Circular wait** — a cycle of threads each waiting on the next.

The most practical cure attacks **circular wait**: impose a **global lock
ordering** — always acquire locks in the same fixed order, and no cycle can form.
Others: acquire **all locks at once** (break hold-and-wait), use **timeouts**
(break no-preemption, then retry), or avoid multiple locks entirely. The famous
**Dining Philosophers** problem is deadlock in miniature (five philosophers, five
forks, everyone grabs left-then-right and starves) — solved exactly by ordering or
limiting concurrency.

**Livelock** — threads **aren't blocked**, but keep **reacting** to each other and
make **no progress** (two people stepping side-to-side in a corridor). They're
busy, yet stuck.

**Starvation** — a thread is **perpetually denied** a resource because others keep
winning it (e.g. low-priority threads never scheduled, or a writer starved by a
stream of readers). The cure is **fairness** — fair locks, aging, balanced
read-write policies.

The mental checklist whenever you hold more than one lock: **could these acquire in
a different order somewhere?** If yes, you risk deadlock — fix it with a consistent
**lock ordering**. You'll detect a deadlock cycle programmatically next, which is
exactly how the OS and databases find them in a **wait-for graph**.
""",
        ),
        _code(
            "Detect a deadlock (wait-for graph)",
            "12 min",
            r"""# A deadlock is a CYCLE in the 'wait-for' graph: T1 waits on a lock held by T2,
# T2 waits on T1. Operating systems and databases detect deadlocks exactly this
# way. Find cycles in the wait-for graph. Pure builtins.

def find_cycle(wait_for):
    # wait_for[t] = the thread t is blocked waiting on (holds t's wanted lock).
    for start in wait_for:
        seen = []
        node = start
        while node is not None and node in wait_for:
            if node in seen:
                return seen[seen.index(node):] + [node]   # the cycle
            seen.append(node)
            node = wait_for[node]
    return []

# Scenario 1: T1 -> T2 -> T1 (classic two-lock deadlock).
wf1 = {"T1": "T2", "T2": "T1", "T3": None}
print("scenario 1 wait-for:", wf1)
cyc1 = find_cycle(wf1)
print("  deadlock?", len(cyc1) > 0, " cycle:", cyc1)
print()

# Scenario 2: a chain T1 -> T2 -> T3 -> (free). No cycle, no deadlock.
wf2 = {"T1": "T2", "T2": "T3", "T3": None}
print("scenario 2 wait-for:", wf2)
cyc2 = find_cycle(wf2)
print("  deadlock?", len(cyc2) > 0)
print()

# Scenario 3: a 3-way cycle T1 -> T2 -> T3 -> T1.
wf3 = {"T1": "T2", "T2": "T3", "T3": "T1"}
print("scenario 3 wait-for:", wf3)
cyc3 = find_cycle(wf3)
print("  deadlock?", len(cyc3) > 0, " cycle:", cyc3)
print()
print("breaking the cycle (a global lock order) makes circular wait impossible.")
""",
        ),
        _t(
            "Scalability: Amdahl's & Gustafson's laws",
            "11 min",
            r"""# Scalability: Amdahl's & Gustafson's laws

Adding cores does **not** add speed proportionally, because every real program has
a **serial part** that can't be parallelised. Two laws make the limits precise —
and they tell apparently opposite stories that are both true.

**Amdahl's law (fixed problem size).** If a fraction **p** of the work is
parallelisable and **(1 − p)** is serial, the speedup on **n** processors is:

$$ S(n) = \frac{1}{(1 - p) + \frac{p}{n}} $$

The punchline is brutal: as **n → ∞**, speedup is capped at **1/(1 − p)** — the
**serial part dominates**. If just **5%** is serial, the *maximum possible* speedup
is **20×**, no matter how many thousands of cores you throw at it. This is the
sobering ceiling on parallelising a fixed task.

**Gustafson's law (scaled problem size).** Amdahl assumes a *fixed* problem. But in
practice, **bigger machines solve bigger problems** — give more cores more data,
and the parallel part grows while the serial part stays roughly constant. Scaled
speedup is then:

$$ S(n) = (1 - p) + p \cdot n $$

— roughly **linear** in n. This is the optimistic, real-world view: weather
simulations, ML training, and rendering *scale* because we feed bigger workloads to
bigger clusters.

```plot
{"title": "Amdahl (fixed, p=0.95) caps out; Gustafson (scaled) grows", "xLabel": "processors n", "yLabel": "speedup", "xRange": [1, 32], "yRange": [0, 32], "functions": [{"expr": "1 / (0.05 + 0.95 / x)", "label": "Amdahl: 1/((1−p)+p/n)", "color": "#dc2626"}, {"expr": "0.05 + 0.95 * x", "label": "Gustafson: (1−p)+pn", "color": "#16a34a"}]}
```

The reconciliation: **Amdahl** governs **strong scaling** (same problem, more
cores — speedup is capped); **Gustafson** governs **weak scaling** (bigger problem,
more cores — speedup keeps growing). Both are right for their question.

Practical takeaways:

- **Attack the serial fraction.** Since `1/(1−p)` is the ceiling, shrinking the
  serial part (and **synchronization/communication overhead**, the hidden serial
  tax) matters more than adding cores.
- **Real speedup is sub-linear** — overhead, contention, and communication mean you
  rarely hit the theoretical curve; measure it.
- **To use a big machine, grow the problem** (Gustafson) — which is exactly why GPUs
  with thousands of lanes pay off on **massive** data (Advanced course).
""",
        ),
        _t(
            "Memory models & ordering",
            "10 min",
            r"""# Memory models & ordering

Here's a truth that shocks people: on modern hardware, **threads don't
automatically see each other's writes in the order they happened.** Both the
**compiler** and the **CPU reorder** memory operations for speed, and each core has
its own **caches/store buffers**. Without rules, one thread's carefully-ordered
writes can appear **jumbled** to another. A **memory model** defines exactly what
orderings are guaranteed.

The intuitive ideal is **sequential consistency** — operations appear in a single
global order consistent with each thread's program order. Easy to reason about, but
**expensive** (it forbids optimisations), so real hardware is weaker by default.

The classic gotcha (without synchronization):

```
init: x = 0, ready = 0
Thread A: x = 42;  ready = 1;       // writes, in this order
Thread B: while(!ready){}  print(x); // may print 0!
```

Thread B can see `ready == 1` but **still read `x == 0`**, because the two writes
in A were reordered or not yet visible. The fix is **memory ordering**.

**C++ `std::memory_order`** lets you choose the guarantee per atomic operation:

```cpp
std::atomic<bool> ready{false};
data = 42;
ready.store(true, std::memory_order_release);   // publish: prior writes visible
// reader:
if (ready.load(std::memory_order_acquire))      // acquire: see those writes
    use(data);                                   // guaranteed to see 42
```

- **acquire/release** — a release **publishes** all prior writes; a matching
  acquire **sees** them. The standard, cheap way to hand data between threads.
- **relaxed** — atomicity only, **no ordering** (for counters where order doesn't
  matter) — fastest, easy to misuse.
- **seq_cst** — the default in C++ atomics: full sequential consistency, safest,
  most expensive.

A subtle performance trap from the same hardware reality: **false sharing** — two
threads update *different* variables that happen to live on the **same cache
line**, so the cache line ping-pongs between cores and performance collapses even
with no logical sharing. The fix: **pad/align** hot per-thread data to separate
cache lines.

The lesson: **locks and atomics don't just prevent races — they establish memory
ordering** so threads agree on what happened. In high-level languages and with
proper mutexes this is handled for you; in lock-free C++ you reason about it
explicitly. When in doubt, use a mutex or `seq_cst` — reach for relaxed orderings
only when profiling demands it and you can prove correctness.
""",
        ),
        quiz_lesson(
            "Quiz: Patterns, Deadlock & Scaling",
            (
                q(
                    "Why prefer a thread pool / task-based model over creating one thread per task?",
                    (
                        opt(
                            "It right-sizes threads to hardware, reuses workers, and balances load (e.g. work stealing) without oversubscription",
                            correct=True,
                        ),
                        opt("Threads are free to create"),
                        opt("It removes the need for any synchronization"),
                        opt("It disables parallelism"),
                    ),
                    "Pools reuse a fixed set of workers matched to cores; you submit tasks and await futures, and runtimes balance load via work stealing.",
                ),
                q(
                    "How many steps does a parallel reduction of N values take, versus sequential?",
                    (
                        opt("About log2(N) parallel levels vs N−1 sequential adds", correct=True),
                        opt("N levels vs N levels"),
                        opt("1 level always"),
                        opt("N² vs N"),
                    ),
                    "Combining pairs in parallel halves the count each level → log2(N) depth; the tree pattern underlies parallel sum/max/dot-product.",
                ),
                q(
                    "Which set of conditions must ALL hold for a deadlock to occur?",
                    (
                        opt(
                            "Mutual exclusion, hold-and-wait, no preemption, and circular wait (the Coffman conditions)",
                            correct=True,
                        ),
                        opt("Only high CPU usage"),
                        opt("Only a single thread"),
                        opt("Only too much memory"),
                    ),
                    "Break any one Coffman condition (commonly circular wait, via a global lock order) and deadlock becomes impossible.",
                ),
                q(
                    "According to Amdahl's law, if 5% of a task is serial, the maximum speedup is…",
                    (
                        opt("20× — capped at 1/(1−p), no matter how many cores", correct=True),
                        opt("Unlimited"),
                        opt("Exactly the number of cores"),
                        opt("5×"),
                    ),
                    "Speedup → 1/(1−p) as n→∞; with 5% serial that's 1/0.05 = 20× — the serial fraction dominates at scale.",
                ),
                q(
                    "What does Gustafson's law add to the Amdahl picture?",
                    (
                        opt(
                            "With bigger problems on bigger machines (weak scaling), the parallel part grows and speedup can scale ~linearly",
                            correct=True,
                        ),
                        opt("That parallelism never helps"),
                        opt("That the serial part is always zero"),
                        opt("That cores slow each other down"),
                    ),
                    "Amdahl fixes the problem size (strong scaling, capped); Gustafson scales the problem with the machine (weak scaling, ~linear).",
                ),
                q(
                    "Why might Thread B print x==0 even after seeing ready==1 (without proper memory ordering)?",
                    (
                        opt(
                            "Compilers/CPUs reorder writes and caches delay visibility; without acquire/release the writes can appear out of order",
                            correct=True,
                        ),
                        opt("Because x is always 0"),
                        opt("Because Python has a GIL"),
                        opt("Because the variables are encrypted"),
                    ),
                    "Memory reordering and per-core caches mean writes aren't seen in program order without synchronization; acquire/release (or a mutex) fixes it.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# concurrency-advanced
# ──────────────────────────────────────────────────────────────────────

_CC_ADVANCED = SeedCourse(
    slug="concurrency-advanced",
    title="Concurrency & Parallelism — Advanced",
    description=(
        "Massive parallelism on the GPU and beyond: the CUDA/SIMT model, the GPU "
        "memory hierarchy and coalescing, writing kernels, parallel scan and "
        "tiled reduction/matmul, lock-free programming, and multi-GPU/MPI. With "
        "runnable CUDA-index-mapping and parallel-scan labs."
    ),
    level="Advanced",
    lessons=(
        _t(
            "The GPU & the CUDA model",
            "12 min",
            r"""# The GPU & the CUDA model

A CPU has a few powerful cores optimised for **latency** (finish one task fast). A
**GPU** has **thousands** of simpler cores optimised for **throughput** (finish a
*huge number* of tasks per second). For problems with massive **data parallelism**
— the same operation over millions of elements — a GPU can be **10–100×** faster.
**CUDA** is NVIDIA's model for programming them in C++.

**SIMT — Single Instruction, Multiple Thread.** You write a **kernel**: a function
describing what **one** thread does. The GPU runs that kernel across **thousands of
threads** at once, each on a different data element. The threads are organised in a
hierarchy:

```
Grid  ─┬─ Block (0)  ─┬─ Thread (0)
       │              ├─ Thread (1)
       │              └─ ... up to ~1024 threads
       ├─ Block (1)
       └─ ... up to billions of blocks
```

- **Thread** — runs one instance of the kernel.
- **Block** — a group of threads (≤ ~1024) that can **cooperate** via fast
  **shared memory** and **synchronize** (`__syncthreads()`).
- **Grid** — all the blocks for one kernel launch.

You choose the **launch configuration** — how many blocks and threads per block:

```cuda
// launch: gridDim blocks, blockDim threads each
vectorAdd<<<numBlocks, threadsPerBlock>>>(a, b, c, n);
```

**Warps** are the execution reality: the GPU runs threads in lockstep groups of
**32** (a **warp**) — all 32 execute the *same* instruction at once. This drives
the golden rule of GPU performance: **avoid warp divergence**. If threads in a warp
take different branches of an `if`, the warp executes **both** paths serially
(masking off threads), wasting work. Keep threads in a warp on the **same path**.

The fundamental shift from CPU thinking: don't ask "how do I split this across 8
threads?" — ask "**how do I express this as the same operation over a million
independent elements?**" That data-parallel mindset (the vectorization idea from
the Basics course, at massive scale) is what the GPU rewards. Next: feeding those
thousands of threads with data fast enough.
""",
        ),
        _t(
            "The GPU memory hierarchy",
            "11 min",
            r"""# The GPU memory hierarchy

On a GPU, **getting data to the thousands of cores is usually the bottleneck**, not
the arithmetic. Mastering the **memory hierarchy** is most of GPU performance
tuning. From slow/large to fast/small:

- **Host (CPU) memory** — separate from the GPU. Data must be **copied over the
  PCIe/NVLink bus** to the device and back. This transfer is **slow** and a common
  bottleneck — minimise it; keep data resident on the GPU across kernels.
- **Global memory** — the GPU's main DRAM (gigabytes). Accessible by all threads,
  but **high latency** (hundreds of cycles). Most data lives here.
- **Shared memory** — a small (~tens of KB), **fast**, on-chip scratchpad **shared
  by a block's threads**. ~100× faster than global. The key tool: load a tile of
  data from global into shared **once**, then let the block reuse it many times.
- **Registers** — per-thread, fastest, very limited. Hold a thread's locals.
- **Constant / texture memory** — small cached read-only spaces for special access
  patterns.

Two performance ideas dominate:

- **Coalesced access** — when the 32 threads of a warp read **consecutive** memory
  addresses, the hardware combines them into **one** wide transaction. **Coalesced
  vs scattered access can be 10×+ different.** Lay out data and indexing so
  neighbouring threads touch neighbouring memory (the canonical
  `idx = blockIdx*blockDim + threadIdx` mapping does exactly this).
- **Use shared memory to cut global traffic** — algorithms like tiled matrix
  multiply load a block-sized **tile** into shared memory, so each value fetched
  from slow global memory is reused by many threads instead of re-fetched.

The discipline is the opposite of CPU code, where memory is mostly transparent
(caches "just work"). On a GPU you **explicitly stage data** through the hierarchy:
copy host→global as little as possible, stage hot data global→shared, keep
per-thread work in registers, and **coalesce** every global access. Get the memory
right and the thousands of cores stay fed; get it wrong and they starve, idling
while waiting on global memory — which is why GPU optimisation is, more than
anything, a **memory-movement** problem.
""",
        ),
        _code(
            "CUDA thread indexing",
            "12 min",
            r"""# Every CUDA thread computes WHICH data element it handles from its block and
# thread ids:  idx = blockIdx * blockDim + threadIdx.  A grid is launched with
# enough threads to cover the array, and a BOUNDARY CHECK guards the tail. We
# simulate the indexing the GPU does. Pure builtins.

n = 10              # array length to process
block_dim = 4       # threads per block
# Launch enough blocks to cover n (ceiling division).
num_blocks = (n + block_dim - 1) // block_dim
print("array length:", n, " blockDim:", block_dim, " gridDim:", num_blocks, "blocks")
print("threads launched:", num_blocks * block_dim, "(more than n -> need a bound check)")
print()

covered = []
for block_idx in range(num_blocks):
    for thread_idx in range(block_dim):
        idx = block_idx * block_dim + thread_idx       # the global index formula
        if idx < n:                                    # boundary check (the kernel's 'if')
            covered.append(idx)
            print("  block", block_idx, "thread", thread_idx, "-> element", idx)
        else:
            print("  block", block_idx, "thread", thread_idx, "-> idx", idx, "SKIP (>= n)")

print()
print("elements covered:", covered)
print("neighbouring threads -> neighbouring indices -> COALESCED global memory access.")
# This is the body of essentially every elementwise CUDA kernel (e.g. vectorAdd):
#   int idx = blockIdx.x * blockDim.x + threadIdx.x;
#   if (idx < n) c[idx] = a[idx] + b[idx];
""",
        ),
        _t(
            "Writing a CUDA kernel",
            "11 min",
            r"""# Writing a CUDA kernel

Let's put the model and memory hierarchy together into actual CUDA C++. The
canonical first kernel is **vector addition** — `c[i] = a[i] + b[i]` for a million
elements:

```cuda
// __global__ marks a kernel: runs on the GPU, called from the CPU.
__global__ void vectorAdd(const float* a, const float* b, float* c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;   // this thread's element
    if (idx < n)                                        // boundary check
        c[idx] = a[idx] + b[idx];                       // each thread: one add
}
```

The **host (CPU) code** orchestrates the work — allocate, copy, launch, copy back:

```cpp
int n = 1 << 20;                       // ~1M elements
float *dA, *dB, *dC;
cudaMalloc(&dA, n*sizeof(float));      // allocate on the GPU
// ... allocate dB, dC ...
cudaMemcpy(dA, hA, bytes, cudaMemcpyHostToDevice);   // copy input up
cudaMemcpy(dB, hB, bytes, cudaMemcpyHostToDevice);

int threads = 256;
int blocks  = (n + threads - 1) / threads;            // ceil: cover all n
vectorAdd<<<blocks, threads>>>(dA, dB, dC, n);        // LAUNCH the grid
cudaDeviceSynchronize();                              // wait for the GPU

cudaMemcpy(hC, dC, bytes, cudaMemcpyDeviceToHost);    // copy result down
cudaFree(dA); /* ... */                               // free device memory
```

The **lifecycle** every CUDA program follows:

```
1. Allocate device memory (cudaMalloc)
2. Copy inputs  host -> device (cudaMemcpy)
3. Launch the kernel <<<blocks, threads>>>   (asynchronous!)
4. Synchronize and copy results device -> host
5. Free device memory
```

Key realities:

- **Kernel launches are asynchronous** — the CPU continues immediately; you
  **synchronize** before using results.
- **The copies often dominate** — for a simple add, moving data over the bus costs
  more than the arithmetic, so GPUs win when you do **lots of compute per byte
  transferred** and **keep data on the device** across many kernels.
- **Modern CUDA** eases the boilerplate: **unified memory** (`cudaMallocManaged`)
  auto-migrates data, and libraries (**cuBLAS, cuDNN, Thrust, CUB**) provide tuned
  kernels so you rarely hand-write reductions or matmuls.

Higher up, frameworks like **PyTorch/TensorFlow** generate and launch these kernels
for you — every `tensor.cuda()` and GPU matmul is this machinery underneath.
Understanding the kernel + copy + launch model is what lets you reason about *why*
GPU code is fast or slow.
""",
        ),
        _code(
            "Parallel prefix sum (scan)",
            "13 min",
            r"""# A SCAN (prefix sum) turns [a,b,c,d] into running totals [a, a+b, a+b+c, ...].
# It looks sequential, but the Hillis-Steele algorithm does it in log2(N) PARALLEL
# steps: at step with offset d, every element adds the element d positions back.
# Scan is a fundamental GPU primitive (stream compaction, sorting, histograms).

data = [3, 1, 7, 0, 4, 1, 6, 3]
print("input:                ", data)

out = list(data)
offset = 1
step = 0
while offset < len(out):
    nxt = list(out)                       # all updates of a step happen 'at once'
    for i in range(len(out)):
        if i >= offset:
            nxt[i] = out[i] + out[i - offset]   # add neighbour 'offset' back
    out = nxt
    step = step + 1
    print("after step", step, "(offset", offset, "):", out)
    offset = offset * 2

print()
print("inclusive prefix sums:", out)
print("done in", step, "parallel steps (log2 of", len(data), ") vs", len(data) - 1, "sequential adds")
# Each step's element updates are independent -> mapped onto parallel GPU threads.
""",
        ),
        _t(
            "Reduction & tiling on the GPU",
            "10 min",
            r"""# Reduction & tiling on the GPU

Two patterns show how the GPU memory hierarchy turns a naïve algorithm into a fast
one: **parallel reduction** and **tiled matrix multiply**. Both follow the same
recipe — **stage data into fast shared memory and reuse it**.

**Parallel reduction (sum of an array)** on the GPU uses the log-depth tree from
the Intermediate course, but the *implementation* is all about memory:

- Each block loads a chunk of global memory into **shared memory**, then threads
  combine pairs in shared memory over `log2` steps (`__syncthreads()` between
  steps so everyone sees the partial results).
- Each block emits one partial sum; a second pass reduces those. Tuning means
  **avoiding warp divergence** (use index patterns that keep active threads
  contiguous) and **bank conflicts** in shared memory.

**Tiled matrix multiply** is the classic shared-memory win. Naïve matmul re-reads
each row/column from slow **global** memory many times. The tiled version:

```
for each TILE:
   cooperatively load a tile of A and a tile of B into SHARED memory
   __syncthreads()
   each thread computes partial dot-products from the fast shared tiles
   __syncthreads()
accumulate across tiles -> C
```

By loading each value from global memory **once** and reusing it across the whole
tile, tiling slashes global-memory traffic — often a **several-fold** speedup over
the naïve kernel, turning a memory-bound kernel compute-bound.

The transferable lessons:

- **Reuse beats recompute-fetch.** The win is loading slow global data into fast
  shared memory **once** and reusing it many times (an explicit, programmer-managed
  cache).
- **`__syncthreads()` coordinates a block** — threads must agree on when shared data
  is ready before reading it (a barrier, from the synchronization lesson).
- **Don't hand-roll these** in production — **cuBLAS** (matmul), **CUB/Thrust**
  (reduction, scan, sort) are expertly tuned. Understand the pattern so you know
  *why* they're fast and can write custom kernels when no library fits.

This is the heart of high-performance GPU computing: the same parallel patterns
you already know, made fast by **deliberately orchestrating data through the memory
hierarchy**.
""",
        ),
        _t(
            "Lock-free & wait-free programming",
            "10 min",
            r"""# Lock-free & wait-free programming

Locks are correct but have costs: **contention** serialises threads, a thread that
sleeps **holding** a lock blocks everyone, and locks risk **deadlock**.
**Lock-free** programming avoids locks entirely, using **atomic** hardware
operations so threads coordinate without ever blocking each other.

The cornerstone is **Compare-And-Swap (CAS)**: an atomic instruction that says
"if this memory still equals the value I expect, set it to my new value — all in
one indivisible step." It returns whether it succeeded.

```cpp
std::atomic<int> value{0};
int expected = value.load();
int desired;
do {
    desired = expected + 1;                                 // compute new value
} while (!value.compare_exchange_weak(expected, desired));  // retry if it changed
```

The pattern is **optimistic**: read, compute a new value, and CAS it in — if
another thread changed it meanwhile, **retry**. No thread ever waits on another; a
stalled thread can't block the rest. Progress guarantees form a hierarchy:

- **Lock-free** — the system as a whole always makes progress (some thread
  succeeds), though an individual thread might retry.
- **Wait-free** — **every** thread finishes in a bounded number of steps (the
  strongest, hardest guarantee).

The infamous trap is the **ABA problem**: a value reads as **A**, another thread
changes it to **B** and back to **A**, so your CAS **succeeds** as if nothing
changed — but the world did (e.g. a freed-and-reallocated node). Cures: **tagged
pointers** (a version counter alongside the value, so A-with-tag-1 ≠ A-with-tag-2)
or safe reclamation schemes (**hazard pointers**, epoch-based reclamation).

The honest trade-off: lock-free data structures (queues, stacks, hash maps) can
**scale better under contention** and avoid deadlock, but they are **extremely hard
to get right** — subtle memory-ordering bugs, the ABA problem, and reclamation make
them a domain for experts. The pragmatic guidance: **use well-tested library
implementations** (`std::atomic`, concurrent containers, `folly`, `boost`) rather
than rolling your own, and reach for lock-free only where profiling proves lock
contention is the bottleneck. For most code, a short critical section under a good
mutex is correct, fast enough, and *far* safer.
""",
        ),
        _t(
            "Beyond one machine: multi-GPU, MPI & the landscape",
            "10 min",
            r"""# Beyond one machine: multi-GPU, MPI & the landscape

The biggest workloads — training large models, climate simulation, scientific
computing — outgrow a single core, a single GPU, even a single machine. Scaling out
combines every level of parallelism you've learned.

**The levels of parallelism, composed:**

- **Instruction-level / SIMD** — within a core (vector units; numpy/`std::simd`).
- **Multi-core threads** — within a CPU (`std::thread`, OpenMP, TBB).
- **Many-core SIMT** — within a GPU (CUDA).
- **Multi-GPU** — several GPUs in one node, connected by fast **NVLink**; split the
  work and exchange results (e.g. **NCCL** for GPU-to-GPU all-reduce).
- **Distributed (multi-node)** — many machines over a network (Distributed Systems
  track), coordinated by **MPI**.

**MPI (Message Passing Interface)** is the backbone of HPC clusters. There's **no
shared memory** across nodes, so processes coordinate purely by **passing messages**
— with **collective operations** that are themselves parallel algorithms:
**broadcast**, **scatter/gather**, and **all-reduce** (combine values from all
processes and give everyone the result — the operation at the heart of distributed
training).

**Portable / higher-level models** so you don't hand-write everything:

- **OpenMP** — `#pragma omp parallel for` to parallelise CPU loops with one line.
- **SYCL / OpenCL / Kokkos** — vendor-portable parallelism (not just NVIDIA).
- **Frameworks** — **PyTorch/TensorFlow** with **data parallelism** (replicate the
  model, split the batch, all-reduce gradients) and **model/tensor/pipeline
  parallelism** (split a model too big for one GPU) hide MPI/NCCL behind simple
  APIs. This is how large models are trained on thousands of GPUs.

The unifying view of this whole track: parallelism is a **hierarchy you compose** —
vectorize within a core, thread across cores, SIMT across a GPU, message-pass
across nodes — and at **every** level the same questions recur: **expose
independent work**, **minimise the serial part and communication** (Amdahl's hidden
tax), **move data as little as possible**, and **synchronise correctly**. Master
those principles and you can reason about performance from a single `for` loop up to
a thousand-GPU cluster.
""",
        ),
        quiz_lesson(
            "Quiz: GPUs, CUDA & Massive Parallelism",
            (
                q(
                    "What does SIMT (the CUDA execution model) mean?",
                    (
                        opt(
                            "You write a kernel for one thread; the GPU runs it across thousands of threads, executed in lockstep warps of 32",
                            correct=True,
                        ),
                        opt("Each thread runs a different program"),
                        opt("Only one thread runs at a time"),
                        opt("It is the same as a CPU thread pool"),
                    ),
                    "Single Instruction, Multiple Thread: one kernel over many threads, grouped into blocks/grids and executed 32-at-a-time as warps.",
                ),
                q(
                    "Why is the GPU memory hierarchy the key to performance?",
                    (
                        opt(
                            "Feeding thousands of cores is the bottleneck; staging data into fast shared memory and coalescing global access keeps them fed",
                            correct=True,
                        ),
                        opt("GPUs have no memory"),
                        opt("Arithmetic is always the bottleneck"),
                        opt("Memory speed is irrelevant on GPUs"),
                    ),
                    "GPU tuning is mostly memory movement: minimise host↔device copies, coalesce global access, and reuse data via shared memory.",
                ),
                q(
                    "What does each CUDA thread compute with idx = blockIdx*blockDim + threadIdx?",
                    (
                        opt(
                            "Its unique global index — which data element it processes — guarded by a boundary check",
                            correct=True,
                        ),
                        opt("The total number of threads"),
                        opt("The GPU temperature"),
                        opt("A random number"),
                    ),
                    "It maps each thread to one element; neighbouring threads get neighbouring indices (coalesced), with 'if (idx < n)' guarding the tail.",
                ),
                q(
                    "Why can a parallel prefix sum (scan) finish in log2(N) steps?",
                    (
                        opt(
                            "At each step every element adds a neighbour an increasing offset back, and those additions are independent (parallel)",
                            correct=True,
                        ),
                        opt("It only sums one element"),
                        opt("It is actually sequential"),
                        opt("Scan cannot be parallelised"),
                    ),
                    "Hillis-Steele scan does independent per-element adds at offsets 1,2,4,… → log2(N) parallel steps instead of N−1 sequential adds.",
                ),
                q(
                    "What is the ABA problem in lock-free programming?",
                    (
                        opt(
                            "A value changes A→B→A, so a CAS succeeds as if nothing changed even though state did — fixed with version tags or safe reclamation",
                            correct=True,
                        ),
                        opt("A deadlock between two threads"),
                        opt("Running out of GPU memory"),
                        opt("A type of cache miss"),
                    ),
                    "CAS only checks the value, not its history; A→B→A fools it. Tagged pointers / hazard pointers / epochs prevent it.",
                ),
                q(
                    "What is an all-reduce, and why does it matter for distributed training?",
                    (
                        opt(
                            "A collective that combines values from all processes and returns the result to everyone — used to average gradients across GPUs",
                            correct=True,
                        ),
                        opt("A way to delete data"),
                        opt("A single-threaded loop"),
                        opt("A type of mutex"),
                    ),
                    "All-reduce (MPI/NCCL) sums/averages each process's contribution and shares the result — the core op of data-parallel training.",
                ),
            ),
        ),
    ),
)


CONCURRENCY_COURSES = (_CC_BASICS, _CC_INTERMEDIATE, _CC_ADVANCED)
